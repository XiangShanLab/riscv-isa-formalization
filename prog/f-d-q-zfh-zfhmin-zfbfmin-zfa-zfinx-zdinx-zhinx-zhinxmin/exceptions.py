#!/usr/bin/env python3
"""Directed exception experiments adapted from riscv-arch-test testplans/priv.

Sources: Exceptions_F.yaml (cp_mstatus_fs_illegal_instr, cp_mstatus_fs_csr_access,
cp_mstatus_fs_legal, cp_load/store_address_misaligned, cp_load/store_access_fault)
and Ssstrict_Sm.yaml (cp_reserved_frm).

All cases run in M mode, which this harness can enter without delegation. A case either
traps (the trap handler records mcause/mepc and resumes after the case) or reaches an
ECALL that ends the case; the raw ECALL cause is kept separately so a normal path is
never confused with a target-instruction exception. Cases whose outcome is architecturally
implementation-defined (misaligned accesses, reserved rounding modes) are observational:
the two models are compared with each other, no expected value is asserted.
"""
from pathlib import Path
import json,re,struct
from run import ROOT,DEFAULT_SAIL,command,configure,signature
from generate import ENC,encoding

def csrword(f3,csr,rd=24,rs1=0):return (csr<<20)|(rs1<<15)|(f3<<12)|(rd<<7)|0x73

def build_cases(formats):
 cs=[]
 def add(kind,word,*,fs=3,frm=0,expected=None,off=None,addr=None,fmt=None,note=''):
  cs.append(dict(id=len(cs),kind=kind,word=word,fs=fs,frm=frm,expected=expected,off=off,addr=addr,fmt=fmt,note=note))
 if 's' in formats:
  # cp_mstatus_fs_illegal_instr: every FP instruction group, mstatus.FS=00.
  ops=[('fadd_s',dict(rm=0)),('fsub_s',dict(rm=0)),('fmul_s',dict(rm=0)),('fdiv_s',dict(rm=0)),
       ('fsqrt_s',dict(rs2=None,rm=0)),('fsgnj_s',{}),('fmin_s',{}),('fmax_s',{}),
       ('feq_s',{}),('flt_s',{}),('fle_s',{}),('fclass_s',dict(rs2=None)),
       ('fmv_x_w',dict(rs2=None)),('fmv_w_x',dict(rs1=24,rs2=None)),
       ('fcvt_w_s',dict(rs2=None,rm=0)),('fcvt_s_w',dict(rs1=24,rs2=None,rm=0)),
       ('fcvt_wu_s',dict(rs2=None,rm=0)),('fcvt_s_wu',dict(rs1=24,rs2=None,rm=0)),
       ('fcvt_s_d',dict(rs2=None,rm=0)),('fcvt_d_s',dict(rs2=None,rm=0)),
       ('fround_s',dict(rs2=None)),('froundnx_s',dict(rs2=None)),
       ('fleq_s',{}),('fltq_s',{}),('fminm_s',{}),('fmaxm_s',{}),
       ('fmadd_s',dict(rs3=22,rm=0)),('fmsub_s',dict(rs3=22,rm=0)),
       ('fnmsub_s',dict(rs3=22,rm=0)),('fnmadd_s',dict(rs3=22,rm=0))]
  for name,kw in ops:
   add('fs-off',encoding(name,**kw),fs=0,expected=2,note=name)
  add('fs-off',encoding('fli_s',rs1=2,rs2=None),fs=0,expected=2,note='fli_s')
  for fmt,op in [('h','flh'),('h','fsh'),('s','flw'),('s','fsw'),('d','fld'),('d','fsd')]:
   rd=(25<<7) if op[1]=='l' else 0
   rs2=(20<<20) if op[1]=='s' else 0
   add('fs-off',ENC[op]|(28<<15)|rd|rs2,fs=0,expected=2,off=0,fmt=fmt,note=op)
  # cp_mstatus_fs_csr_access: read/write/set/clear fcsr, frm, fflags.
  for csr in [1,2,3]:
   names={1:'fflags',2:'frm',3:'fcsr'}[csr]
   for f3,rs1,rd,form in [(2,0,24,'csrr'),(1,24,0,'csrw'),(3,24,0,'csrc'),(2,24,0,'csrs')]:
    add('fs-off',csrword(f3,csr,rd,rs1),fs=0,expected=2,note=form+'_'+names)
  # cp_mstatus_fs_legal: FS=01/10/11 x legal frm 0-4.
  legal=[('fadd_s',dict(rm=7)),('fmul_s',dict(rm=7)),('fsqrt_s',dict(rs2=None,rm=7)),
         ('fcvt_w_s',dict(rs2=None,rm=7)),('fcvt_s_d',dict(rs2=None,rm=7)),
         ('fmadd_s',dict(rs3=22,rm=7)),('fsgnj_s',{}),('fclass_s',dict(rs2=None)),
         ('fmv_x_w',dict(rs2=None)),('fli_s',dict(rs1=2,rs2=None))]
  for fs in [1,2,3]:
   for frm in range(5):
    for name,kw in legal:add('fs-legal',encoding(name,**kw),fs=fs,frm=frm,expected=0,note=f'{name}_fs{fs}_frm{frm}')
  # cp_reserved_frm: reserved static modes, and DYN with reserved frm. Observational.
  for rm in [5,6]:add('reserved',encoding('fadd_s',rm=rm),expected=None,note=f'static_rm{rm}')
  for frm in range(8):add('reserved',encoding('fadd_s',rm=7),frm=frm,expected=None,note=f'dyn_frm{frm}')
 for fmt in formats:
  suf={'h':'h','s':'w','d':'d','q':'q'}[fmt]
  # cp_load_address_misaligned / cp_store_address_misaligned: all 16 low-4-bit offsets.
  for off in range(16):
   add('misaligned-load',ENC['fl'+suf]|(28<<15)|(25<<7),off=off,fmt=fmt,expected=None,note=f'fl{suf}+{off}')
   add('misaligned-store',ENC['fs'+suf]|(28<<15)|(20<<20),off=off,fmt=fmt,expected=None,note=f'fs{suf}+{off}')
  # cp_load_access_fault / cp_store_access_fault: address 0 has no memory behind it in
  # either bare-metal model, the role of the testplan's fixed access-fault address.
  add('fault-load',ENC['fl'+suf]|(28<<15)|(25<<7),off=0,addr=0,fmt=fmt,expected=5,note='fl'+suf)
  add('fault-store',ENC['fs'+suf]|(28<<15)|(20<<20),off=0,addr=0,fmt=fmt,expected=7,note='fs'+suf)
 return cs

def emit(cases):
 L=['.section .text.init,"ax"','.option norvc','.globl _start','_start:',
    ' la t0,trap_handler',' csrw mtvec,t0',' csrw mie,zero',' csrw medeleg,zero',' csrw mideleg,zero',
    ' csrw satp,zero',' li t0,-1',' csrw pmpaddr0,t0',' li t0,31',' csrw pmpcfg0,t0',
    ' la s1,begin_signature',
    # FP inputs: f18=1.0, f20=2.0, f22=3.0, f24=dest, f25=memory dest; x24=1.
    ' li t0,0x6000',' csrs mstatus,t0',' csrw fcsr,zero',
    ' li t0,0x3f800000',' fmv.w.x f18,t0',' li t0,0x40000000',' fmv.w.x f20,t0',
    ' li t0,0x40400000',' fmv.w.x f22,t0',' fmv.w.x f24,zero',' fmv.w.x f25,zero',' li x24,1']
 for c in cases:
  n=c['id'];frm=c['frm']<<5
  L+=[' li t0,0x6000',' csrc mstatus,t0',' li t0,0x6000',' csrs mstatus,t0',
      f' li t0,{frm}',' csrw fcsr,t0']
  if c['off'] is not None:L+=[' la t3,scratch',f' addi t3,t3,{c["off"]}']
  if c['addr'] is not None:L+=[' li t3,0']
  # Each case starts from a known scratch and destination so earlier cases cannot leak state.
  L+=[' la t1,scratch']+[f' sd zero,{k}(t1)' for k in range(0,64,8)]+[' fmv.w.x f25,zero']
  # Lower FS last: after this point FP CSR writes would themselves trap.
  L+=[' li t0,0x6000',' csrc mstatus,t0',f' li t0,{c["fs"]<<13}',' csrs mstatus,t0',
      ' li s11,0',' li s10,0',' li s7,0',f' la s2,after_{n}',f'.globl target_{n}',f'target_{n}:',
      f' .word 0x{c["word"]:08x}',' ecall',f'after_{n}:',
      # Capture FS before any state change, then fcsr and dest.
      ' csrr t0,mstatus',' srli t0,t0,13',' andi t0,t0,3',' sw t0,20(s1)',
      ' sw s11,24(s1)',f' li t0,{n}',' sw t0,28(s1)',' sd s10,48(s1)',' sw s7,32(s1)',
      ' la t0,scratch',' lw t1,0(t0)',' sw t1,36(s1)',' lw t1,4(t0)',' sw t1,40(s1)',' lw t1,8(t0)',' sw t1,44(s1)',
      ' li t0,0x6000',' csrs mstatus,t0',' csrr t0,fcsr',' sw t0,16(s1)',
      ' fsd f25,0(s1)',' csrr t0,misa',' sd t0,56(s1)',' addi s1,s1,64']
 L+=[' la t0,tohost',' li t1,1',' sd t1,0(t0)','1: j 1b','.balign 4','trap_handler:',
     ' csrr s11,mcause',' mv s7,s11',' csrr s10,mepc',' li t0,8',' bltu s11,t0,2f',
     ' li t0,11',' bltu t0,s11,2f',' li s11,0',' li s10,0','2:',' csrw mepc,s2',
     ' li t0,0x1800',' csrs mstatus,t0',' mret',
     '.section .data','.balign 64','.globl scratch','scratch: .zero 64',
     '.section .tohost,"aw"','.balign 64','.globl tohost,fromhost','tohost: .dword 0','fromhost: .dword 0',
     '.section .signature,"aw"','.balign 64','.globl begin_signature,end_signature','begin_signature:',
     f' .zero {64*len(cases)}','end_signature:']
 return '\n'.join(L)+'\n'

def main():
 for name,formats,paired in [('rv64-f-exceptions',['h','s','d'],True),('rv64-q-exceptions',['q'],False)]:
  cases=build_cases(formats);src=ROOT/'generated'/name;src.mkdir(exist_ok=True)
  out=ROOT/'results'/name;out.mkdir(exist_ok=True);build=ROOT/'build'/name;build.mkdir(exist_ok=True)
  asm=src/'suite.S';asm.write_text(emit(cases));(src/'cases.json').write_text(json.dumps(cases,indent=2)+'\n')
  # Q cases are raw .word encodings (gcc does not accept a q single letter), as in the main suite.
  march='rv64imafd_zicsr'+('' if 'q' in formats else '_zfh_zfa')
  elf=build/'suite.elf';cc=command(['riscv64-unknown-elf-gcc','-march='+march,'-mabi=lp64','-nostdlib','-nostartfiles','-Wl,--no-relax','-T',ROOT/'link.ld',asm,'-o',elf]);(out/'build.json').write_text(json.dumps(cc,indent=2))
  p=dict(xlen=64,bank='f',ext=['f','d']+(['q'] if 'q' in formats else ['zfh','zfhmin','zfa']))
  cfg=configure(DEFAULT_SAIL,p);cfgpath=ROOT/'configs'/(name+'.json');cfgpath.write_text(json.dumps(cfg,indent=2))
  isa='rv64ima'+('fdq' if 'q' in formats else 'fdh')+'_zicsr'+('' if 'q' in formats else '_zfh_zfhmin_zfa')
  commands={'spike':['spike','--isa='+isa,'-m128','+signature='+str(out/'spike.sig'),'+signature-granularity=4',elf]}
  if paired:commands['sail']=[DEFAULT_SAIL,'--config',cfgpath,'--inst-limit','1000000','--test-signature',out/'sail.sig','--signature-granularity','4',elf]
  syms=command(['riscv64-unknown-elf-nm',elf])['stdout'];pcs={int(m[2]):int(m[1],16) for m in re.finditer(r'^([0-9a-f]+) \w target_(\d+)$',syms,re.M)}
  rows={};result=dict(profile=name,cases=len(cases),models={})
  for model,cmd in commands.items():
   (out/(model+'.sig')).unlink(missing_ok=True);r=command(cmd,60);(out/(model+'.json')).write_text(json.dumps(r,indent=2))
   checked=0;bad=[];harness=[]
   if r['returncode']==0 and (out/(model+'.sig')).exists():
    data=signature(out/(model+'.sig'));rows[model]=[]
    if len(data)!=64*len(cases):harness.append(dict(error=f'signature length {len(data)}, expected {64*len(cases)}'))
    for i,c in enumerate(cases):
     b=data[i*64:(i+1)*64];w=struct.unpack('<16I',b);exc=w[6];trap_pc=int.from_bytes(b[48:56],'little')
     row=dict(id=i,exception=exc,result=b[:16].hex(),fcsr=w[4],fs=w[5],memory=b[36:48].hex(),ecall_cause=w[8],trap_pc=hex(trap_pc));rows[model].append(row)
     if exc and trap_pc!=pcs.get(i,0):harness.append(dict(case=c,actual_pc=hex(trap_pc),target_pc=hex(pcs.get(i,0))))
     if not exc and w[8]!=11:harness.append(dict(case=c,ecall_cause=w[8]))
     if c['expected'] is not None and exc!=c['expected']:bad.append(dict(case=c,actual=exc))
     checked+=1
    (out/(model+'.jsonl')).write_text(''.join(json.dumps(x)+'\n' for x in rows[model]))
   result['models'][model]=dict(returncode=r['returncode'],checked=checked,expectation_differences=bad,harness_errors=harness)
  result['paired']=len(cases) if len(rows)==2 else 0
  result['differences']=[dict(case=cases[a['id']],spike=a,sail=b) for a,b in zip(rows.get('spike',[]),rows.get('sail',[])) if any(a[k]!=b[k] for k in ['exception','result','fcsr','fs','memory'])]
  (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
  print(name,'paired',result['paired'],'model diff',len(result['differences']),'models',[(k,v['returncode'],len(v['expectation_differences']),len(v['harness_errors'])) for k,v in result['models'].items()],flush=True)
if __name__=='__main__':main()
