#!/usr/bin/env python3
"""Directed M/HS/U/VS/VU FS and FCSR-stateen gate experiments (RV64)."""
from pathlib import Path
import itertools,json,re,struct
from run import ROOT,DEFAULT_SAIL,command,configure,signature
from generate import ENC,encoding

def main():
 summaries=[]
 for bank in ['f','x']:
  name='rv64-'+bank+'-privilege';src=ROOT/'generated'/name;src.mkdir(exist_ok=True)
  out=ROOT/'results'/name;out.mkdir(exist_ok=True);build=ROOT/'build'/name;build.mkdir(exist_ok=True)
  cases=[]
  for mode,op in itertools.product(['M','HS','U','VS','VU'],['fadd_s','fclass_s','frcsr']):
   configs=list(itertools.product([0,1],repeat=3)) if bank=='x' else [(2,2),(0,2),(2,0)]
   for cfg in configs:
    if bank=='x':
     m,h,s=cfg;exc=2 if mode!='M' and (not m or (mode=='U' and not s)) else 22 if mode in ['VS','VU'] and (not h or (mode=='VU' and not s)) else 0
     fs=vfs=0
    else:
     fs,vfs=cfg;m=h=s=1;exc=2 if fs==0 or (mode in ['VS','VU'] and vfs==0) else 0
    cases.append(dict(id=len(cases),mode=mode,op=op,fs=fs,vfs=vfs,m=m,h=h,s=s,expected_exception=exc))
  lines=['.section .text.init,"ax"','.option norvc','.globl _start','_start:',' la t0,trap_handler',' csrw mtvec,t0',' csrw mie,zero',' csrw medeleg,zero',' csrw mideleg,zero',' csrw satp,zero',' csrw 0x280,zero',' csrw 0x680,zero',' li t0,-1',' csrw pmpaddr0,t0',' li t0,31',' csrw pmpcfg0,t0',' la s1,begin_signature']
  for c in cases:
   n=c['id'];mode=c['mode'];op=c['op'];pp=3 if mode=='M' else 1 if mode in ['HS','VS'] else 0;virt=mode in ['VS','VU']
   lines+=[' li t0,0x6000',' csrs mstatus,t0'] if bank=='f' else []
   if bank=='f':lines+=[' li t0,0x3f800000',' fmv.w.x f18,t0',' li t0,0x40000000',' fmv.w.x f20,t0',' fmv.w.x f24,zero']
   else:lines+=[' li x18,0x3f800000',' li x20,0x40000000',' li x24,0']
   lines+=[' csrw fcsr,zero',' li t0,-1',' csrw 0x30c,t0',' csrw 0x60c,t0',f' li t0,{2*c["s"]}',' csrw 0x10c,t0',f' li t0,{(1<<63)|2*c["h"]}',' csrw 0x60c,t0',f' li t0,{(1<<63)|2*c["m"]}',' csrw 0x30c,t0',f' li t0,{c["vfs"]<<13}',' csrw 0x200,t0',
            f' li t0,{(1<<39)|0x6000}',' csrc mstatus,t0',f' li t0,{c["fs"]<<13}',' csrs mstatus,t0',f' li t0,{(1<<39)|0x1800}',' csrc mstatus,t0',f' li t0,{(pp<<11)|((1<<39) if virt else 0)}',' csrs mstatus,t0',f' la s2,after_{n}',' li s11,0',' li s10,0',f' la t0,target_{n}',' csrw mepc,t0',' mret',f'.globl target_{n}',f'target_{n}:']
   # The CSR form reads fcsr, FCLASS must still be gated despite no fcsr update.
   word=encoding(op,rs2=None if op=='fclass_s' else 20,rm=0 if op=='fadd_s' else None) if op!='frcsr' else (3<<20)|(2<<12)|(24<<7)|0x73
   c['word']=word;lines += [f' .word 0x{word:08x}',f'.globl finish_{n}',f'finish_{n}:',' ecall',f'after_{n}:',
    ' csrr t0,mstatus',' srli t0,t0,13',' andi t0,t0,3',' sw t0,20(s1)',' sw s11,24(s1)',f' li t0,{n}',' sw t0,28(s1)',' sd s10,48(s1)',' sw s7,32(s1)']
   # Restore access before capturing the FP state, without modifying the measured FS.
   lines+=[' li t0,-1',' csrw 0x30c,t0',' csrw 0x60c,t0',' csrw 0x10c,t0']
   if bank=='f':lines+=[' li t0,0x6000',' csrs mstatus,t0']
   lines+=[' csrr t0,fcsr',' sw t0,16(s1)']
   lines+=[' fsd f24,0(s1)'] if bank=='f' and op=='fadd_s' else [' sd x24,0(s1)']
   lines+=[' csrr t0,misa',' sd t0,56(s1)',' addi s1,s1,64']
  lines+=[' la t0,tohost',' li t1,1',' sd t1,0(t0)','1: j 1b','.balign 4','trap_handler:',' csrr s11,mcause',' mv s7,s11',' csrr s10,mepc',' li t0,8',' bltu s11,t0,2f',' li t0,11',' bltu t0,s11,2f',' li s11,0',' li s10,0','2:',' csrw mepc,s2',f' li t0,{(1<<39)|0x1800}',' csrc mstatus,t0',' li t0,0x1800',' csrs mstatus,t0',' mret',
    '.section .tohost,"aw"','.balign 64','.globl tohost,fromhost','tohost: .dword 0','fromhost: .dword 0','.section .signature,"aw"','.balign 64','.globl begin_signature,end_signature','begin_signature:',f' .zero {64*len(cases)}','end_signature:']
  asm=src/'suite.S';asm.write_text('\n'.join(lines)+'\n');(src/'cases.json').write_text(json.dumps(cases,indent=2)+'\n')
  elf=build/'suite.elf';cc=command(['riscv64-unknown-elf-gcc','-march=rv64imafdh_zicsr','-mabi=lp64','-nostdlib','-nostartfiles','-Wl,--no-relax','-T',ROOT/'link.ld',asm,'-o',elf]);(out/'build.json').write_text(json.dumps(cc,indent=2))
  ext=['f','d'] if bank=='f' else ['zfinx']
  p=dict(xlen=64,bank=bank,ext=ext);cfg=configure(DEFAULT_SAIL,p);cfg['extensions']['H']['supported']=True;cfg['extensions']['Stateen']['Smstateen']['supported']=True;cfg['extensions']['Stateen']['Ssstateen']['supported']=True
  cfgpath=ROOT/'configs'/(name+'.json');cfgpath.write_text(json.dumps(cfg,indent=2))
  isa='rv64imah'+('fd' if bank=='f' else '')+'_zicsr_smstateen_ssstateen'+('_zfinx' if bank=='x' else '')
  # Spike requires single-letter extensions in canonical order.
  isa=isa.replace('imahfd','imafdh')
  commands={'spike':['spike','--isa='+isa,'-m128','+signature='+str(out/'spike.sig'),'+signature-granularity=4',elf],
   'sail':[DEFAULT_SAIL,'--config',cfgpath,'--inst-limit','100000','--test-signature',out/'sail.sig','--signature-granularity','4',elf]}
  rows={};result=dict(profile=name,cases=len(cases),models={})
  syms=command(['riscv64-unknown-elf-nm',elf])['stdout'];pcs={int(m[2]):int(m[1],16) for m in re.finditer(r'^([0-9a-f]+) \w target_(\d+)$',syms,re.M)}
  for model,cmd in commands.items():
   (out/(model+'.sig')).unlink(missing_ok=True);r=command(cmd,30);(out/(model+'.json')).write_text(json.dumps(r,indent=2))
   checked=0;bad=[];harness=[]
   if r['returncode']==0 and (out/(model+'.sig')).exists():
    data=signature(out/(model+'.sig'));rows[model]=[]
    for i,c in enumerate(cases):
     b=data[i*64:(i+1)*64];w=struct.unpack('<16I',b);exc=w[6];trap_pc=int.from_bytes(b[48:56],'little');row=dict(id=i,boundary_cause=w[8],exception=exc,result=b[:16].hex(),fcsr=w[4],fs=w[5],trap_pc=hex(trap_pc));rows[model].append(row)
     if not exc and w[8]!={'M':11,'HS':9,'U':8,'VS':10,'VU':8}[c['mode']]:harness.append(dict(case=c,wrong_boundary_cause=w[8]))
     if exc and trap_pc!=pcs[i]:harness.append(dict(case=c,actual_pc=hex(trap_pc),target_pc=hex(pcs[i])))
     if exc!=c['expected_exception']:bad.append(dict(case=c,actual=exc))
     checked+=1
    (out/(model+'.jsonl')).write_text(''.join(json.dumps(r)+'\n' for r in rows[model]))
   result['models'][model]=dict(returncode=r['returncode'],checked=checked,gate_differences=bad,harness_errors=harness)
  result['paired']=len(cases) if len(rows)==2 else 0
  result['differences']=[dict(case=cases[a['id']],spike=a,sail=b) for a,b in zip(rows.get('spike',[]),rows.get('sail',[])) if any(a[k]!=b[k] for k in ['exception','result','fcsr'])]
  (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n');summaries.append(result)
  print(name,'paired',result['paired'],'diff',len(result['differences']),'models',[(k,v['returncode'],len(v['gate_differences']),len(v['harness_errors'])) for k,v in result['models'].items()],flush=True)
 (ROOT/'results/privilege-summary.json').write_text(json.dumps(summaries,indent=2)+'\n')
if __name__=='__main__':main()
