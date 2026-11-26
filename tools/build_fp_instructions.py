#!/usr/bin/env python3
"""Build the English scalar-FP instruction collection from checked case data.

The checked fp_arithmetic_seed.json contains the explicit arithmetic partition;
configuration, state transitions, conversions, transfers, and CSR cases are
specified here against the source anchors. Generated output is self-contained.
Run with python3 -I tools/build_fp_instructions.py.
"""
from pathlib import Path
import re, json, hashlib
from functools import lru_cache
from collections import defaultdict
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'build/scalar-fp-instructions'
FMT = {'H':(16,5,10,-14,15),'S':(32,8,23,-126,127),'D':(64,11,52,-1022,1023),'Q':(128,15,112,-16382,16383),'B':(16,8,7,-126,127)}
MODE = ['RNE','RTZ','RDN','RUP','RMM']
FS = r'\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}'
NAN = lambda a: rf'(e_{a}=e_{{\max,{a}}}\land f_{a}\ne0)'
SNAN = lambda a: rf'(e_{a}=e_{{\max,{a}}}\land f_{a}\ne0\land f_{a}[w_{{f,{a}}}-1]=0)'
QNAN = lambda a: rf'(e_{a}=e_{{\max,{a}}}\land f_{a}[w_{{f,{a}}}-1]=1)'
INF = lambda a: rf'(e_{a}=e_{{\max,{a}}}\land f_{a}=0)'
ZERO = lambda a: rf'(e_{a}=0\land f_{a}=0)'
FINITE = lambda a: rf'(e_{a}\ne e_{{\max,{a}}})'

def enum(modes): return r'\{' + ','.join(rf'\mathrm{{{MODE[i]}}}({i})' for i in modes) + r'\}'
def modes(ms):
    e=enum(ms)
    return rf'(\mathrm{{instr}}.rm\in{e}\lor(\mathrm{{instr}}.rm=\mathrm{{DYN}}(7)\land fcsr.frm\in{e}))'
LEGAL=modes(range(5))

@lru_cache(maxsize=None)
def source(volume, first,last, claim,section):
    path=ROOT/'sources'/f'riscv-{volume}.txt'
    lines=path.read_text().splitlines(keepends=True)
    # splitlines includes formfeed as its own boundary; use only newline for line numbers.
    lines=path.read_text().split('\n')
    pages=[];page=1
    for n,line in enumerate(lines,1):
        page+=line.count('\f')
        if first<=n<=last: pages.append(page)
    return {'volume':volume,'first':first,'last':last,'pages':sorted(set(pages)),'section':section,'claim':claim,'quote':'\n'.join(lines[first-1:last])}

REFS = [
 source('unprivileged',6749,6761,'F state and Zicsr dependency','21–21.1'),
 source('unprivileged',6863,6891,'fcsr fields and rounding encodings','21.2'),
 source('unprivileged',6920,6940,'Reserved rounding; sticky flags do not trap','21.2'),
 source('unprivileged',6946,6977,'Canonical NaNs and gradual underflow','21.3–21.4'),
 source('unprivileged',8049,8074,'Tininess requires separate unbounded-exponent rounding, including final normal results','25.3.2.6.1'),
 source('unprivileged',7288,7311,'NaN boxing and raw transfer exceptions','22.2'),
 source('privileged',1582,1585,'misa may return zero','3.1.1'),
 source('privileged',1627,1645,'Implemented means currently available','3.1.1'),
 source('privileged',2286,2289,'Off status prohibits state access','3.1.6.7'),
 source('privileged',2333,2344,'Imprecise dirty tracking and unchanged writes','3.1.6.7'),
 source('privileged',2413,2415,'SD is the disjunction of FS/VS/XS Dirty','3.1.6.7'),
 source('privileged',4556,4597,'State-enable hierarchy and U/VU controls','4.1'),
 source('privileged',4692,4698,'FCSR state-enable semantics','4.2'),
 source('privileged',9538,9540,'Dual FS during virtualization','15.2.11'),
]
SPECREF={
 '01':[(7007,7035,'Arithmetic and minimum/maximum','21.6')],
 '02':[(7007,7035,'Arithmetic operation','21.6')],
 '03':[(7007,7035,'Arithmetic operation','21.6')],
 '04':[(7007,7035,'Arithmetic operation','21.6')],
 '05':[(7007,7035,'Arithmetic operation','21.6')],
 '06':[(7055,7100,'Fused signed products; invalid even with quiet-NaN addend','21.6')],
 '07':[(7030,7040,'Minimum/maximum, signed zero and NaNs','21.6')],
 '08':[(8578,8596,'NaN-propagating minimum/maximum','26.2')],
 '09':[(7145,7155,'Sign injection preserves non-sign bits and NaN payloads','21.7')],
 '10':[(7210,7220,'Quiet and signaling comparisons','21.8'),(8676,8689,'Zfa quiet comparisons','26.6')],
 '11':[(7228,7269,'Classification writes one-hot mask without flags','21.9')],
 '12':[(7103,7142,'Integer range clipping, rounding and sign extension','21.7')],
 '13':[(7103,7142,'Integer conversion, rounding and flags','21.7')],
 '14':[(7387,7410,'Floating-format conversion','22.5'),(7702,7721,'Half conversion directions','24.3'),(7786,7796,'Zfhmin conversion availability','24.6')],
 '15':[(8601,8622,'Floating round-to-integral and flags','26.3')],
 '16':[(8625,8638,'Modular integer conversion and fixed rm encoding','26.4')],
 '17':[(7170,7187,'Raw integer/floating moves','21.7'),(8645,8673,'Split-width move variants','26.5')],
 '18':[(8470,8575,'FLI constants, format availability, and no flags','26.1')],
 '19':[(6980,7002,'Floating loads and stores','21.5'),(7645,7665,'Half transfers','24.1')],
 '20':[(6980,7002,'Floating loads and stores','21.5'),(7645,7665,'Half transfers','24.1')],
 '21':[(6858,6882,'Floating CSR aliases and fields','21.2')],
 '22':[(8102,8112,'Zfbfmin and its transfer subset','25.4.1'),(8225,8244,'Narrowing BF16 conversion and flags','25.5.1'),(8268,8287,'Exact BF16 widening and invalid flag','25.5.2')],
}
FAMILIES={}

def case(title,conds,value=None,flags=(),target='fd',exception=None,raw=False):
 return dict(title=title,conds=conds,value=value,flags=list(flags),target=target,exception=exception,raw=raw)

FAMILIES=json.loads((ROOT/'tools/fp_arithmetic_seed.json').read_text())

def add_family(name,cat):
 return FAMILIES.setdefault(name,{'key':name.lower().replace('.','-'),'variants':[],'cat':cat,'operation':name})
def extfmt(f,transfer=False):
 if f=='H': return [r'(\mathrm{impl}(\mathrm{Zfhmin})\lor\mathrm{impl}(\mathrm{Zfh})\lor\mathrm{impl}(\mathrm{Zfbfmin}))'] if transfer else ['Zfh']
 return [{'S':'F','D':'D','Q':'Q'}[f]]
def variant(fam,instr,fmt,ins,ext,rm,cs,**extra):
 v=dict(instr=instr,fmt=fmt,input_formats=ins,ext=ext,rm=rm,cases=cs,**extra)
 fam['variants'].append(v)
 return v

def finite_cases(f,baseconds,addsub=False):
 emn,emx=FMT[f][3:]
 out=[]
 for title,cond,flags in [
  ('normal exact',rf'(2^{{{emn}}}\le\lvert\mathrm{{rounded}}\rvert<2^{{{emx+1}}})',()),
  ('normal inexact',rf'(2^{{{emn}}}\le\lvert\mathrm{{rounded}}\rvert<2^{{{emx+1}}})',('nx',)),
  ('subnormal exact',rf'(0<\lvert\mathrm{{rounded}}\rvert<2^{{{emn}}})',()),
  ('subnormal inexact',rf'(0<\lvert\mathrm{{rounded}}\rvert<2^{{{emn}}})',('uf','nx'))]:
  if addsub and title=='subnormal inexact': continue
  eq=r'\ne' if flags else '='
  out.append(case(title,baseconds+[r'(\mathrm{exact}\ne0)',cond,rf'(\mathrm{{rounded}}{eq}\mathrm{{exact}})'],r'\mathrm{rounded}',flags))
 if not addsub:
  for sign,k in [('+','>'),('-','<')]:
   out.append(case(f'{sign} underflow to zero',baseconds+[r'(\mathrm{rounded}=0)',rf'(\mathrm{{exact}}{k}0)'],rf'{sign}0_{{{f}}}',('uf','nx')))
 for sign,k,ms,kind in [('+','>',[0,3,4],'infinity'),('+','>',[1,2],'maximum finite'),('-','<',[0,2,4],'infinity'),('-','<',[1,3],'maximum finite')]:
  value=rf'{sign}\infty_{{{f}}}' if kind=='infinity' else rf'{sign}\mathrm{{MAX}}_{{{f}}}'
  out.append(case(f'{sign} overflow to {kind}',[modes(ms)]+baseconds+[rf'(\lvert\mathrm{{rounded}}\rvert\ge2^{{{emx+1}}})',rf'(\mathrm{{exact}}{k}0)'],value,('of','nx')))
 return out

# Integer conversions: all rounding/clipping decisions are on the rounded integer.
for typ in ['W','WU','L','LU']:
 width=32 if typ.startswith('W') else 64
 lo='0' if typ.endswith('U') else rf'-2^{{{width-1}}}'
 hi=rf'2^{{{width if typ.endswith("U") else width-1}}}-1'
 for f in 'HSDQ':
  fam=add_family('FCVT.'+typ,'12')
  cs=[case('NaN clips to maximum',[NAN('a')],hi,('nv',),'rd'),
      case('positive infinity clips to maximum',[INF('a'),r'(s_a=0)'],hi,('nv',),'rd'),
      case('negative infinity clips to minimum',[INF('a'),r'(s_a=1)'],lo,('nv',),'rd'),
      case('rounded integer above range',[FINITE('a'),rf'(\mathrm{{integer}}>{hi})'],hi,('nv',),'rd'),
      case('rounded integer below range',[FINITE('a'),rf'(\mathrm{{integer}}<{lo})'],lo,('nv',),'rd'),
      case('in range, inexact',[FINITE('a'),rf'({lo}\le\mathrm{{integer}}\le {hi})',r'(\mathrm{integer}\ne x)'],r'\mathrm{integer}',('nx',),'rd'),
      case('in range, exact',[FINITE('a'),rf'({lo}\le\mathrm{{integer}}\le {hi})',r'(\mathrm{integer}=x)'],r'\mathrm{integer}',(),'rd')]
  for c in cs: c['value']=rf'\mathrm{{sext}}_{{\mathrm{{XLEN}}}}({c["value"]}\bmod2^{{{width}}},{width})'
  variant(fam,f'FCVT.{typ}.{f}',f,[f],extfmt(f),True,cs,xlen=64 if width==64 else None,inttype=typ)
  fam=add_family('FCVT.from-'+typ,'13')
  cs=[case('integer zero', [r'(n=0)'],rf'+0_{{{f}}}')]
  cs+=finite_cases(f,[r'(n\ne0)'])
  if f!='H': cs=[c for c in cs if 'overflow' not in c['title']]
  # Integer input cannot yield subnormal or underflow-to-zero.
  cs=[c for c in cs if 'subnormal' not in c['title'] and 'underflow' not in c['title']]
  if FMT[f][2]+1 >= (width if typ.endswith('U') else width-1): cs=[c for c in cs if 'nx' not in c['flags']]
  variant(fam,f'FCVT.{f}.{typ}',f,[],extfmt(f),True,cs,xlen=64 if width==64 else None,inttype=typ)

# Floating conversions, including the Zfhmin and Zfbfmin subsets.
for dst in 'HSDQ':
 for src in 'HSDQ':
  if src==dst: continue
  fam=add_family('FCVT.float','14')
  exts=[]
  for f in (dst,src):
   e=r'(\mathrm{impl}(\mathrm{Zfh})\lor\mathrm{impl}(\mathrm{Zfhmin}))' if f=='H' else extfmt(f)[0]
   if e not in exts: exts.append(e)
  cs=[]
  for title,cond,val,flags in [
   ('signaling NaN',[SNAN('a')],rf'\mathrm{{qNaN}}_{{{dst}}}',('nv',)),
   ('quiet NaN',[QNAN('a')],rf'\mathrm{{qNaN}}_{{{dst}}}',()),
   ('positive infinity',[INF('a'),r'(s_a=0)'],rf'+\infty_{{{dst}}}',()),
   ('negative infinity',[INF('a'),r'(s_a=1)'],rf'-\infty_{{{dst}}}',()),
   ('positive zero',[ZERO('a'),r'(s_a=0)'],rf'+0_{{{dst}}}',()),
   ('negative zero',[ZERO('a'),r'(s_a=1)'],rf'-0_{{{dst}}}',())]: cs.append(case(title,cond,val,flags))
  if FMT[dst][0]>FMT[src][0]:
   cs.append(case('exact widening, nonzero finite',[FINITE('a'),rf'\neg{ZERO("a")}'],r'x'))
  else: cs+=finite_cases(dst,[FINITE('a'),rf'\neg{ZERO("a")}'])
  variant(fam,f'FCVT.{dst}.{src}',dst,[src],exts,True,cs)
for dst,src,iname in [('B','S','FCVT.BF16.S'),('S','B','FCVT.S.BF16')]:
 fam=add_family(iname,'22')
 cs=[case('signaling NaN',[SNAN('a')],rf'\mathrm{{qNaN}}_{{{dst}}}',('nv',)),case('quiet NaN',[QNAN('a')],rf'\mathrm{{qNaN}}_{{{dst}}}')]
 for sign,k in [('+',0),('-',1)]:
  cs += [case(sign+' infinity',[INF('a'),rf'(s_a={k})'],rf'{sign}\infty_{{{dst}}}'),case(sign+' zero',[ZERO('a'),rf'(s_a={k})'],rf'{sign}0_{{{dst}}}')]
 if dst=='S': cs.append(case('exact nonzero finite widening',[FINITE('a'),rf'\neg{ZERO("a")}'],'x'))
 else: cs+=finite_cases(dst,[FINITE('a'),rf'\neg{ZERO("a")}'])
 variant(fam,iname,dst,[src],['Zfbfmin'],True,cs)

fam=add_family('FCVTMOD.W.D','16')
cs=[case('NaN',[NAN('a')],'0',('nv',),'rd'),case('infinity',[INF('a')],'0',('nv',),'rd')]
wrap=r'\mathrm{sext}_{\mathrm{XLEN}}(\mathrm{integer}\bmod2^{32},32)'
cs += [case('finite, invalid range',[FINITE('a'),r'(\mathrm{integer}<-2^{31}\lor\mathrm{integer}>2^{31}-1)'],wrap,('nv',),'rd'),
       case('finite in range, inexact',[FINITE('a'),r'(-2^{31}\le\mathrm{integer}\le2^{31}-1)',r'(\mathrm{integer}\ne x)'],wrap,('nx',),'rd'),
       case('finite in range, exact',[FINITE('a'),r'(-2^{31}\le\mathrm{integer}\le2^{31}-1)',r'(\mathrm{integer}=x)'],wrap,(),'rd')]
variant(fam,'FCVTMOD.W.D','D',['D'],['Zfa','D'],False,cs,fixedrm=1)

# Raw transfers do not check source boxing and never canonicalize NaNs.
for f,label,width in [('H','H',16),('S','W',32),('D','D',64)]:
 for direction in ['to-x','from-x']:
  fam=add_family('FMV.'+direction,'17')
  instr=f'FMV.X.{label}' if direction=='to-x' else f'FMV.{label}.X'
  value=rf'\mathrm{{sext}}_{{\mathrm{{XLEN}}}}(a[{width-1}:0],{width})' if direction=='to-x' else rf'n[{width-1}:0]'
  variant(fam,instr,f,[] if direction=='from-x' else [f],extfmt(f,True),False,[case('raw transfer',[],value,target='rd' if direction=='to-x' else 'fd',raw=True)],xlen=64 if f=='D' else None,transfer=True)
for f,width,xlen in [('D',64,32),('Q',128,64)]:
 for base in ['FMVH','FMVP']:
  fam=add_family(base,'17')
  ins=f'{base}.X.{f}' if base=='FMVH' else f'{base}.{f}.X'
  value=rf'a[{width-1}:{width//2}]' if base=='FMVH' else r'n_2\Vert n_1'
  variant(fam,ins,f,[f] if base=='FMVH' else [],['Zfa',f],False,[case('raw high half' if base=='FMVH' else 'pack low and high integer halves',[],value,target='rd' if base=='FMVH' else 'fd',raw=True)],xlen=xlen,transfer=True)

# FLI has an actual immediate operand, not a register value.
fam=add_family('FLI','18')
constants=['-1',None,r'2^{-16}',r'2^{-15}',r'2^{-8}',r'2^{-7}',r'2^{-4}',r'2^{-3}',r'1/4',r'5/16',r'3/8',r'7/16',r'1/2',r'5/8',r'3/4',r'7/8','1',r'5/4',r'3/2',r'7/4','2',r'5/2','3','4','8','16','128','256',r'2^{15}',r'2^{16}',None,None]
for f in 'HSDQ':
 exts=['Zfa']+extfmt(f)
 if f=='H': exts=['Zfa',r'(\mathrm{impl}(\mathrm{Zfh})\lor\mathrm{impl}(\mathrm{Zvfh}))']
 cs=[]
 for k,val in enumerate(constants):
  if k==1: val=rf'2^{{{FMT[f][3]}}}'
  elif k==30 or (f=='H' and k==29): val=rf'+\infty_{{{f}}}'
  elif k==31: val=rf'\mathrm{{qNaN}}_{{{f}}}'
  cs.append(case(f'immediate index {k}',[rf'(\mathrm{{instr}}.rs1={k})'],val))
 variant(fam,f'FLI.{f}',f,[],exts,False,cs)
# Scalar floating CSR aliases and the six underlying Zicsr operations.
CSRADDR={'fflags':1,'frm':2,'fcsr':3}
for name,field,write,imm in [('FRCSR','fcsr',False,False),('FSCSR','fcsr',True,False),('FRRM','frm',False,False),('FSRM','frm',True,False),('FRFLAGS','fflags',False,False),('FSFLAGS','fflags',True,False)]:
 fam=add_family(name,'21')
 c=case('read old field'+(' and replace field' if write else ''),[],rf'\mathrm{{old}}(\mathrm{{fcsr.{field}}})' if field!='fcsr' else r'\mathrm{old}(\mathrm{fcsr})',target='rd')
 if write: c['csrwrite']=(field,r'\mathrm{instr}.uimm' if imm else 'n')
 variant(fam,name,'S',[],['F','Zicsr'],False,[c],csr=True,csrfield=field)
for base in ['CSRRW','CSRRS','CSRRC','CSRRWI','CSRRSI','CSRRCI']:
 fam=add_family(base,'21')
 for field,addr in CSRADDR.items():
  cs=[];imm=base.endswith('I');writealways=base in ['CSRRW','CSRRWI']
  operand=r'\mathrm{instr}.uimm' if imm else 'n'
  opcheck=r'\mathrm{instr}.uimm' if imm else r'\mathrm{instr}.rs1'
  if not writealways:
   cs.append(case('read; suppress write on zero source specifier',[rf'({opcheck}=0)'],rf'\mathrm{{old}}(\mathrm{{fcsr.{field}}})' if field!='fcsr' else r'\mathrm{old}(\mathrm{fcsr})',target='rd'))
  val=operand if writealways else (rf'\mathrm{{old}}(\mathrm{{fcsr.{field}}})\mathbin{{\mathrm{{OR}}}}{operand}' if 'RS' in base else rf'\mathrm{{old}}(\mathrm{{fcsr.{field}}})\mathbin{{\mathrm{{AND}}}}\neg_{{\mathrm{{XLEN}}}}({operand})')
  if field=='fcsr': val=val.replace('fcsr.fcsr','fcsr')
  c=case('read old CSR and write selected bits',[] if writealways else [rf'({opcheck}\ne0)'],rf'\mathrm{{old}}(\mathrm{{fcsr.{field}}})' if field!='fcsr' else r'\mathrm{old}(\mathrm{fcsr})',target='rd')
  c['csrwrite']=(field,val);cs.append(c)
  variant(fam,base,'S',[],['F','Zicsr'],False,cs,csr=True,csrfield=field,csraddr=addr)

# Memory is the same architectural memory-access relation as an integer access.
# Its returned memory includes any already-visible partial store and page-table updates.
for store in [False,True]:
 for f,label in [('H','H'),('S','W'),('D','D'),('Q','Q')]:
  instr=('FS' if store else 'FL')+label
  fam=add_family(instr,'20' if store else '19')
  kind='Store' if store else 'Load'
  cs=[]
  for code,name in [(3,'Breakpoint'),(6 if store else 4,kind+'AddressMisaligned'),(15 if store else 13,kind+'PageFault'),(23 if store else 21,kind+'GuestPageFault'),(7 if store else 5,kind+'AccessFault')]:
   cs.append(case(name,[rf'(\mathrm{{access.exception}}=\{{\mathrm{{{name}}}({code})\}})'],exception=f'{name}({code})',target=None))
  cs.append(case('successful memory access',[r'(\mathrm{access.exception}=\varnothing)'],None if store else r'\mathrm{access.value}',target=None if store else 'fd',raw=True))
  variant(fam,instr,f,[] if not store else [f],extfmt(f,True),False,cs,memory=True,store=store,transfer=True)

# Actual x-register variants of chapters 21,22,24,27. Zfa, BF16, Q and
# floating transfers are deliberately not manufactured as x-register instructions.
for name,fam in list(FAMILIES.items()):
 if fam['cat'] not in [f'{x:02}' for x in range(1,15)]: continue
 if fam['cat']=='08' or name in ['FLEQ','FLTQ']: continue
 xf=add_family(name+'.x','27')
 xf['basecat']=fam['cat'];xf['operation']=name;xf['xregs']=True
 for v in fam['variants']:
  if 'Q' in v['input_formats'] or v['fmt']=='Q': continue
  exts=[]
  for f in set(v['input_formats']+[v['fmt']]):
   if f=='H': e=r'(\mathrm{impl}(\mathrm{Zhinx})\lor\mathrm{impl}(\mathrm{Zhinxmin}))' if fam['cat']=='14' else 'Zhinx'
   else: e={'S':'Zfinx','D':'Zdinx'}[f]
   if e not in exts:exts.append(e)
  nv=dict(v);nv['ext']=exts;nv['cases']=[dict(c,conds=list(c['conds'])) for c in v['cases']]
  xf['variants'].append(nv)
# CSR access exists in Zfinx as well; separate documents keep the register-state model explicit.
for name,fam in list(FAMILIES.items()):
 if fam['cat']!='21':continue
 xf=add_family(name+'.x','27');xf.update(basecat='21',operation=name,xregs=True)
 xf['variants']=[dict(v,ext=['Zfinx','Zicsr'],cases=[dict(c) for c in v['cases']]) for v in fam['variants']]

# Common literal configuration clauses: no bundled enable predicate.
def impl(e):return e if e.startswith('(') else rf'\mathrm{{impl}}(\mathrm{{{e}}})'
LOWER=r'(\mathrm{impl}(\mathrm{Smstateen})\lor\mathrm{impl}(\mathrm{Ssstateen}))'
MGATE=r'(\mathrm{Priv}=\mathrm{M}\lor\neg\mathrm{impl}(\mathrm{Smstateen})\lor misa.F=1\lor mstateen0.FCSR=1)'
HGATE=rf'(\mathrm{{Priv}}\notin\{{\mathrm{{VS}},\mathrm{{VU}}\}}\lor\neg{LOWER}\lor misa.F=1\lor hstateen0.FCSR=1)'
SGATE=rf'(\mathrm{{Priv}}\notin\{{\mathrm{{U}},\mathrm{{VU}}\}}\lor\neg{LOWER}\lor misa.F=1\lor sstateen0.FCSR=1)'
VFS=rf'(\mathrm{{Priv}}\notin\{{\mathrm{{VS}},\mathrm{{VU}}\}}\lor(vsstatus.FS\in{FS}\land sstatus.FS\in{FS}))'
MBLOCK=r'(\mathrm{Priv}\ne\mathrm{M}\land\mathrm{impl}(\mathrm{Smstateen})\land misa.F=0\land mstateen0.FCSR=0)'
HBLOCK=rf'(\mathrm{{Priv}}\in\{{\mathrm{{VS}},\mathrm{{VU}}\}}\land{LOWER}\land misa.F=0\land hstateen0.FCSR=0)'
SUBLOCK=rf'(\mathrm{{Priv}}=\mathrm{{U}}\land{LOWER}\land misa.F=0\land sstateen0.FCSR=0)'
SVBLOCK=rf'(\mathrm{{Priv}}=\mathrm{{VU}}\land{LOWER}\land misa.F=0\land sstateen0.FCSR=0)'

def config(v,xregs=False):
 env=[] if xregs else [VFS]
 env += [MGATE,HGATE,SGATE]
 features=[impl(e) for e in v['ext']]
 if v.get('xlen'):features += [rf'(\mathrm{{XLEN}}={v["xlen"]})']
 mode=[] if xregs else [rf'(mstatus.FS\in{FS})']
 if v['rm']:mode+=[LEGAL]
 if v.get('fixedrm') is not None:mode+=[rf'(\mathrm{{instr}}.rm=\mathrm{{RTZ}}(1))']
 return env,features,mode

def instrterm(v):
 s=rf'(\mathrm{{instr}}=\mathrm{{{v["instr"]}}})'
 if 'csraddr' in v:s=rf'(\mathrm{{instr}}.csr={v["csraddr"]})',s
 return [s] if isinstance(s,str) else list(s)

def formula(label,title,terms,right):
 # One top-level conjunction per line; nested conditions remain parenthesized.
 lines=[]
 for i,t in enumerate(terms):
  lines.append(('&' if i==0 else r'&\land\ ')+t+(r'\\' if i<len(terms)-1 else ''))
 return f'**({label}) {title}**\n\n$$\n\\begin{{aligned}}\n'+'\n'.join(lines)+'\n\\end{aligned}\n\\longrightarrow\n'+r'\{\, '+right+r' \,\}'+'\n$$\n\n'

def guards(v,xregs):
 # Illegal extension/FS/M-state gates have priority over virtual state gates.
 unavailable=[rf'\neg({impl(e)})' for e in v['ext']]
 if v.get('xlen'):unavailable += [rf'(\mathrm{{XLEN}}\ne{v["xlen"]})']
 if not xregs:unavailable += [r'(mstatus.FS=\mathrm{Off}(0))',r'(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\land(vsstatus.FS=\mathrm{Off}(0)\lor sstatus.FS=\mathrm{Off}(0)))']
 unavailable += [MBLOCK]
 # Reserved register encodings and reserved rm are outside the model, not illegal guards.
 bad='('+r'\lor '.join(unavailable)+')'
 env,feat,mode=config(v,xregs)
 active=[c for c in env if c not in [HGATE,SGATE]]+feat+([] if xregs else [rf'(mstatus.FS\in{FS})'])
 return [
  ('extension, FS or machine state gate prohibits execution',[bad],r'\mathrm{IllegalInstruction}(2)'),
  ('hypervisor or virtual-user state gate prohibits execution',active+['('+HBLOCK+r'\lor '+SVBLOCK+')'],r'\mathrm{VirtualInstruction}(22)'),
  ('ordinary user state gate prohibits execution',active+[HGATE,SUBLOCK],r'\mathrm{IllegalInstruction}(2)')]

def normalize_case(c,v):
 c=dict(c);c['conds']=list(c['conds']);f=v['fmt']
 def norm(s):
  s=s.replace(r'\mathit{int}_{\mathrm{res}}',r'\mathrm{integer}')
  for a in 'abc':
   for ff in FMT:
    for sign,k in [('+',0),('-',1)]:
     s=s.replace(rf'({a}={sign}0_{{{ff}}})',rf'(s_{a}={k}\land e_{a}=0\land f_{a}=0)')
     s=s.replace(rf'({a}={sign}\infty_{{{ff}}})',rf'(s_{a}={k}\land e_{a}=e_{{\max,{a}}}\land f_{a}=0)')
  return s
 c['conds']=[norm(s) for s in c['conds'] if s!=r'\mathrm{true}']
 if c['value'] is not None:c['value']=norm(c['value'])
 return c

def emit_case(c,v,xregs):
 target=c['target'];fields=[]
 if v.get('memory'):fields.append(r'\mathrm{mem}=\mathrm{access.mem}')
 if target:
  value=c['value'].replace(r'\mathrm{old}(\mathrm{fcsr.fflags})',r'\mathrm{oldfflags}')
  if xregs and target=='fd':
   # Define floating writeback (including RV32 aligned register pairs) locally.
   fields.append(rf'\mathrm{{XWrite}}_{{{v["fmt"]}}}(\mathrm{{instr}}.rd,{value})')
  else:fields.append(f'{target}={value}')
 if c.get('csrwrite'):
  fld,val=c['csrwrite'];val=val.replace(r'\mathrm{old}(\mathrm{fcsr.fflags})',r'\mathrm{oldfflags}');mask={'fflags':5,'frm':3,'fcsr':8}[fld]
  fields.append(rf'\mathrm{{CSRWrite}}_{{\mathrm{{{fld}}}}}({val})')
 # DirtyFS is a state-update relation, including the permitted implementation choice.
 # It is never applied in x-register mode.
 if not xregs and c['exception'] is None:fields.append(r'\mathrm{DirtyFS}')
 if c['exception'] is None and not c.get('csrwrite'):
  flags=r'\{'+','.join(rf'\mathrm{{{f.upper()}}}({dict(nv=4,dz=3,of=2,uf=1,nx=0)[f]})' for f in c['flags'])+r'\}' if c['flags'] else r'\varnothing'
  fields.append(r'\mathrm{fcsr.fflags}\mathrel{|}='+flags)
 fields.append(r'\mathrm{exception}='+ (r'\varnothing' if c['exception'] is None else rf'\{{\mathrm{{{c["exception"].split("(")[0]}}}({c["exception"].split("(")[1]}\}}'))
 return r',\ '.join(fields)

COMMON_OPERANDS = r'''Each floating operand is the decoded triple $a=(s_a,e_a,f_a)$, and likewise for $b,c$.
Its format is the source format in the variant table. Set $e_{\max,a}=2^{w_{e,a}}-1$;
$w_{f,a}$ is the source fraction width. Operand-specific subscripts matter for conversions.

| Format | Width | Exponent bits | Fraction bits | Minimum normal exponent | Maximum exponent |
|---|---:|---:|---:|---:|---:|
| H | 16 | 5 | 10 | -14 | 15 |
| S | 32 | 8 | 23 | -126 | 127 |
| D | 64 | 11 | 52 | -1022 | 1023 |
| Q | 128 | 15 | 112 | -16382 | 16383 |
| B (BF16) | 16 | 8 | 7 | -126 | 127 |

| Input class | Field condition |
|---|---|
| Negative infinity | $s_a=1,\ e_a=e_{\max,a},\ f_a=0$ |
| Negative normal | $s_a=1,\ 1\le e_a<e_{\max,a}$ |
| Negative subnormal | $s_a=1,\ e_a=0,\ f_a\ne0$ |
| Negative zero | $s_a=1,\ e_a=0,\ f_a=0$ |
| Positive zero | $s_a=0,\ e_a=0,\ f_a=0$ |
| Positive subnormal | $s_a=0,\ e_a=0,\ f_a\ne0$ |
| Positive normal | $s_a=0,\ 1\le e_a<e_{\max,a}$ |
| Positive infinity | $s_a=0,\ e_a=e_{\max,a},\ f_a=0$ |
| Signaling NaN | $e_a=e_{\max,a},\ f_a\ne0,\ f_a[w_{f,a}-1]=0$ |
| Quiet NaN | $e_a=e_{\max,a},\ f_a[w_{f,a}-1]=1$ |

For finite operands the numerical value is

$$
\mathrm{val}_F(a)=
\begin{cases}
(-1)^{s_a}(1+f_a/2^{w_{f,a}})2^{e_a-(2^{w_{e,a}-1}-1)},&1\le e_a<e_{\max,a},\\
(-1)^{s_a}f_a2^{E_{\min}(F)-w_{f,a}},&e_a=0.
\end{cases}
$$

For comparisons extend this value to the two signed infinities. It is not defined on NaNs;
no numeric comparison or exact arithmetic expression is evaluated on a NaN branch.
Write $x=\mathrm{val}_{F_a}(a)$, $y=\mathrm{val}_{F_b}(b)$ and $z=\mathrm{val}_{F_c}(c)$
only where that expression is defined. All unbound format parameters are fixed by the variant table.

A generated NaN is the canonical quiet NaN $\mathrm{qNaN}_F$ with sign zero, all exponent bits one,
and fraction $2^{w_f(F)-1}$. Payload-preserving instructions explicitly copy operand fields instead.
The maximum finite magnitude is

$$
\mathrm{MAX}_F=(2-2^{-w_f(F)})2^{E_{\max}(F)}.
$$

`enc` denotes the exact IEEE encoding of a representable value; it does not round again.
`sign_inject(a,t)` copies the exponent and fraction of $a$ and sets its sign to $t$;
it preserves NaN payloads and the quiet/signaling bit. In minimum/maximum, $\prec$ is numeric order
extended by $-0_F\prec+0_F$; equal nonzero values have the same value and encoding.
`sext(v,k)` takes the low $k$ bits and sign-extends them to the indicated destination width.
`low32(q)` takes $q\bmod2^{32}$ and sign-extends from 32 bits. The integer inputs $n,n_1,n_2$ denote the entry values of the designated integer source registers.
Register $x0$ always reads zero;
integer-destination writes to $x0$ are discarded without suppressing flags or exceptions.
'''

def state_section(xregs):
 if xregs:
  return r'''`mstatus.FS` is hardwired to `Off(0)` and does not gate floating execution or fcsr access.
There are no floating-register Dirty updates. State-enable gates remain active when implemented.
The `misa.F/D/Q` bits are zero. Narrow floating results are sign-extended in x registers;
upper source bits are ignored, rather than checked for NaN boxing.
'''
 return r'''`mstatus.FS`, HS-level `sstatus.FS`, and `vsstatus.FS` use
`Off(0)`, `Initial(1)`, `Clean(2)`, and `Dirty(3)`. The first two names denote the same physical field;
`vsstatus.FS` is separate. A zero active FS always causes `IllegalInstruction(2)`, including in VS/VU.

`DirtyFS` is the permitted FS update relation, not a requirement that every write changes FS.
Let $\sigma$ be the entry state and $\sigma'$ the candidate result after applying the destination
write and flag/CSR updates. Let $\mathcal W_{FP}$ be exactly the f-register and fcsr fields written
by that branch, including NaN-boxed upper destination bits. Define the derived Boolean value

$$
\mathrm{changed}=\bigvee_{q\in\mathcal W_{FP}}(\sigma'(q)\ne\sigma(q)).
$$

For each active FS field $t$ (`mstatus.FS`, and additionally `vsstatus.FS` in VS/VU),
`DirtyFS` means

$$
\begin{cases}
\sigma'(t)=\mathrm{Dirty}(3),&\mathrm{changed}=1,\\
\sigma'(t)\in\{\sigma(t),\mathrm{Dirty}(3)\},&\mathrm{changed}=0.
\end{cases}
$$

The second choice is implementation-defined for unchanged writes; imprecise tracking can also
mark state dirty on a read-only instruction. A particular implementation may choose a more precise
tracking policy. The relation preserves these permitted choices instead of inventing a CSR selector.
When state actually changes in VS/VU, both active FS fields become `Dirty(3)`.
For each status bank the read-only summary is

$$
SD=(FS=3)\lor(VS=3)\lor(XS=3).
$$

The virtual summary uses only virtual-bank fields. `VS` here is the vector-status field,
not the VS privilege mode. These summaries are recomputed after FS updates.
'''

def derived_section(fam):
 base=fam['operation'];cat=fam.get('basecat',fam['cat'])
 op={'FADD':'x+y','FSUB':'x-y','FMUL':r'x\cdot y','FDIV':'x/y','FSQRT':r'\sqrt{x}',
     'FMADD':r'x\cdot y+z','FMSUB':r'x\cdot y-z','FNMSUB':r'-(x\cdot y)+z','FNMADD':r'-(x\cdot y)-z'}
 txt=''
 if base in op:txt+=f'The exact finite result is $\\mathrm{{exact}}={op[base]}$. '
 if cat=='13':txt+=r'Interpret the low 32 or 64 bits of integer $n$ according to W/WU/L/LU, then set $\mathrm{exact}=n$. '
 if cat in ['14','22']:txt+=r'For finite conversion inputs set $\mathrm{exact}=x$. '
 if cat in ['01','02']:txt+=r'''The exact sum/difference is an integer multiple of the minimum subnormal spacing.
Any subnormal result is exact; `UF(1)` and nonzero-to-zero underflow are unreachable. '''
 if cat=='05':txt+='A positive finite square root cannot overflow or underflow in the same format. '
 if cat=='06':txt+=r'''The multiply is exact and is not rounded before addition.
Effective product/addend signs are $(s_a\oplus s_b,s_c)$ for FMADD,
$(s_a\oplus s_b,1\oplus s_c)$ for FMSUB,
$(1\oplus s_a\oplus s_b,s_c)$ for FNMSUB, and
$(1\oplus s_a\oplus s_b,1\oplus s_c)$ for FNMADD.
An exact sum of two negative zero terms is negative zero; equal positive terms give positive zero.
Opposite zero signs or nonzero exact cancellation give negative zero only under `RDN(2)`.
The $0\times\infty$ invalid case takes priority even over a quiet-NaN addend. '''
 if any(v['rm'] for v in fam['variants']):
  txt+=r'''
For finite arithmetic and format conversion, rounding uses the destination precision, a subnormal
spacing of $2^{E_{\min}(F)-w_f(F)}$, and an unbounded upper exponent during overflow detection:

$$
\mathrm{rounded}=
\begin{cases}
\mathrm{round}_{F,\mathrm{instr}.rm}(\mathrm{exact}),&\mathrm{instr}.rm\ne\mathrm{DYN}(7),\\
\mathrm{round}_{F,fcsr.frm}(\mathrm{exact}),&\mathrm{instr}.rm=\mathrm{DYN}(7).
\end{cases}
$$

For tininess detection compute another correctly rounded value with the same precision and
an exponent unbounded in both directions; its input is always normalized, without a subnormal grid:

$$
\mathrm{unbounded}=
\begin{cases}
\mathrm{roundP}_{F,\mathrm{instr}.rm}(\mathrm{exact}),&\mathrm{instr}.rm\ne\mathrm{DYN}(7),\\
\mathrm{roundP}_{F,fcsr.frm}(\mathrm{exact}),&\mathrm{instr}.rm=\mathrm{DYN}(7).
\end{cases}
$$

A result is tiny when $0<\lvert\mathrm{unbounded}\rvert<2^{E_{\min}(F)}$.
The two roundings can yield a final normal value with both UF and NX set; the normal-inexact
rules therefore split on `unbounded`. This is explicitly required by Unprivileged §25.3.2.6.1.

`roundInt` uses the same modes but rounds to an unbounded mathematical integer:

$$
\mathrm{integer}=
\begin{cases}
\mathrm{roundInt}_{\mathrm{instr}.rm}(x),&\mathrm{instr}.rm\ne\mathrm{DYN}(7),\\
\mathrm{roundInt}_{fcsr.frm}(x),&\mathrm{instr}.rm=\mathrm{DYN}(7).
\end{cases}
$$

RNE selects the nearest value, ties to an even trailing significand bit; RTZ rounds toward zero;
RDN toward negative infinity; RUP toward positive infinity; RMM selects nearest, with ties away from zero.
For FROUND/FROUNDNX use `integer`, encoded exactly in the original floating format; retain the input
sign when it rounds to zero. Widening still decodes its rm field normally, even when numerically exact.
Underflow requires both an inexact result and tininess after the separate precision-only rounding. Overflow is detected when
$\lvert\mathrm{rounded}\rvert\ge2^{E_{\max}(F)+1}$; setting `OF(2)` also sets `NX(0)`.
'''
 if any(v['rm'] for v in fam['variants']):
  if cat in ['12','15']:
   a=txt.index('For finite arithmetic and format conversion,');b=txt.index('`roundInt` uses')
   txt=txt[:a]+txt[b:]
   a=txt.index('Underflow requires both');txt=txt[:a]
  else:
   a=txt.index('`roundInt` uses');b=txt.index('RNE selects',a)
   txt=txt[:a]+txt[b:]
   a=txt.index('For FROUND/FROUNDNX use');b=txt.index('Widening still',a)
   txt=txt[:a]+txt[b:]
 if cat=='16':txt+=r'Use $\mathrm{integer}=\operatorname{trunc}(x)$; flags match FCVT.W.D under RTZ before modular reduction. '
 return txt+'\n\n'

def refs_for(fam):
 refs=list(REFS)
 cat=fam.get('basecat',fam['cat'])
 refs += [source('unprivileged',a,b,c,d) for a,b,c,d in SPECREF.get(cat,[])]
 refs += [source('unprivileged',7353,7489,'D analogues, conversion widths and transfers','22.3–22.7'),source('unprivileged',7507,7620,'Q analogues, conversions and transfer restrictions','23.1–23.5'),source('unprivileged',7645,7796,'H analogues and the precise minimal subset','24.1–24.6')]
 refs += [source('unprivileged',7270,7284,'D dependency and register width','22–22.1'),source('unprivileged',7494,7507,'Q dependency and recursive boxing','23'),source('unprivileged',7628,7640,'Zfh dependency and boxing','24')]
 if fam.get('xregs'):
  refs += [source('unprivileged',8715,8819,'Zfinx family, widths, aligned pairs and privileged behavior','27–27.6'),source('privileged',10452,10530,'HS qualification and virtual exception precedence','15.6')]
 if cat=='21':refs += [source('unprivileged',3333,3389,'CSR read/write suppression and immediate variants','6.1')]
 if cat in ['19','20']:
  refs += [source('privileged',3027,3071,'Memory exception priority and alignment choice','3.1.15'),source('privileged',4420,4428,'Partial stores can remain visible after an access fault','3.7.1.3'),source('privileged',2080,2114,'MPRV and effective access privilege','3.1.6.4')]
 return refs

def document(name,fam):
 xregs=fam.get('xregs',False);cat=fam.get('basecat',fam['cat']);vs=fam['variants']
 display={'FCVT.float':'FCVT (floating-format conversions)','FMV.to-x':'FMV.X.{H,W,D}','FMV.from-x':'FMV.{H,W,D}.X'}
 display.update({'FCVT.from-'+t:'FCVT.{H,S,D,Q}.'+t for t in ['W','WU','L','LU']})
 title=display.get(fam['operation'],fam['operation'])+(' (x-register form)' if xregs else '')
 text=f'# {title}\n\n'
 text+='This document specifies the RV32/RV64 scalar forms listed below. Each rule describes execution after successful instruction fetch; trap entry and subsequent handler execution are separate architectural steps.\n\n'
 text+='All left-hand fields are entry-state values. Right-hand assignments constrain the corresponding exit-state fields. Unlisted data-state fields retain their entry value, except for read-only summaries explicitly derived below. Normal sequential PC advance and trap entry belong to the surrounding instruction-step relation; these formulas specify its floating/data-state projection. Rules within a concrete variant are evaluated in numbered order; a later rule applies only if no earlier rule did. Reserved configurations are outside the defined relation, rather than silently made illegal.\n\n'
 text+='## 1. Execution environment\n\n'
 text+='`Priv` is M, HS (ordinary S when H is absent), U, VS, or VU. Only privilege modes implemented by the execution environment are realizable. `XLEN` is 32 or 64.\n\n'
 text+='State-enable control is written out in every execution rule: `mstateen0.FCSR` controls levels below M; `hstateen0.FCSR` controls VS/VU; `sstateen0.FCSR` controls U/VU. Controls apply only when the corresponding state-enable extension is implemented and `misa.F=0`. M ignores these gates. A machine-level denial is illegal; an HS-qualified VS/VU denial by hstateen or its user sstateen is virtual. A U-mode sstateen denial is illegal. FS denial remains illegal in VS/VU.\n\n'
 text+='`impl(X)` means extension X is currently available in the execution environment, including its standardized dependencies. It does not mean fabrication capability independent of runtime enablement. `misa` is allowed to report zero, so extension availability alone is not used to assert `misa.F=1`. All applicable state-enable terms remain explicit.\n\n'
 if cat in ['19','20']:
  text+=r'''Memory operations also use `mstatus.MPRV/MPP/MPV/SUM/MXR`, the corresponding supervisor
status fields, `satp`, `vsatp`, `hgatp`, PMP entries, PMAs, endianness, and the configured address
translation extensions. MPRV selects effective data-access privilege; it does not change the current
privilege used for the floating instruction's FS check.

'''
 text+='## 2. Extension and variant configuration\n\n'
 text+='| Instruction | Destination format | Floating source formats | Required extensions | XLEN restriction |\n|---|---|---|---|---|\n'
 for v in vs:
  ex=' and '.join(e if not e.startswith('(') else e.replace('\\','') for e in v['ext'])
  # use math for compound feature expressions, no vertical bars.
  ex=' and '.join(f'${e}$' if e.startswith('(') else f'`{e}`' for e in v['ext'])
  text+=f'| `{v["instr"]}`'+(f' (CSR {v["csraddr"]})' if 'csraddr'in v else '')+f' | {v["fmt"]} | '+(', '.join(v['input_formats']) or 'none')+f' | {ex} | '+(str(v['xlen']) if v.get('xlen') else '32 or 64')+' |\n'
 text+='\nH arithmetic needs Zfh (Zhinx in x-register form). Zfhmin only adds the listed transfer and cross-format conversion subset; Zhinxmin only the S/H and D/H conversion subset. BF16 is a separate format B, provided by Zfbfmin. Zfa additions require Zfa plus the selected format support. Only FLI.H also accepts Zvfh as specified by its own section.\n\n'
 text+='## 3. Floating CSR and state configuration\n\n'+state_section(xregs)+'\n'
 if any(v['rm'] for v in vs):
  text+='The instruction has an rm field. The exact legal-mode condition repeated in execution rules is:\n\n$$\n'+LEGAL+'\n$$\n\n'
  text+=r'''`RNE(0)`, `RTZ(1)`, `RDN(2)`, `RUP(3)`, and `RMM(4)` are the five standard modes.
`DYN(7)` in the instruction selects `fcsr.frm`. Static modes 5/6, or dynamic frm 5/6/7,
have reserved behavior. A static legal mode does not require frm to be legal.
The reserved-mode region is not assigned either a floating result or a mandatory exception.

'''
 elif any('fixedrm'in v for v in vs):
  text+='FCVTMOD.W.D requires encoded `instr.rm=RTZ(1)`. Other rm encodings are reserved; `fcsr.frm` is ignored.\n\n'
 else:text+='There is no rounding-mode selector for this instruction. Encoded funct3 bits that select an operation are not treated as rm. No frm legality test is imposed.\n\n'
 text+='`fcsr.fflags` is the five-bit set `NV(4), DZ(3), OF(2), UF(1), NX(0)`. Except for explicit CSR writes, a flag update is a union with the old set. An empty increment preserves every old flag. Raising a floating flag does not generate a synchronous trap.\n\n'
 text+='## 4. Operand sets and derived values\n\n'+COMMON_OPERANDS+'\n'
 if xregs:
  text+=r'''Read a narrow source from the low $w_F$ x-register bits without checking upper bits.
`XWrite_F(j,v)` is the following register write set, with $u=\mathrm{enc}_F(v)$:

$$
\mathrm{XWrite}_F(j,v)=
\begin{cases}
\varnothing,&j=0,\\
\{x[j]=\mathrm{sext}_{\mathrm{XLEN}}(u,w_F)\},&0<w_F\le\mathrm{XLEN},\ j\ne0,\\
\{x[j]=u[31:0],\ x[j+1]=u[63:32]\},&w_F=64,\ \mathrm{XLEN}=32,\ j\ne0.
\end{cases}
$$

For RV32 double operands/results every participating double-width register number is even;
odd numbers are reserved, not unconditionally illegal. Lower-numbered registers contain the low bits,
independent of endianness. A double read from x0 returns all zero without reading x1; a double write
to x0 also leaves x1 unchanged. Integer results use their own W/WU/L/LU encoding, not XWrite.
A zero destination does not suppress floating flags or state-enable traps.

'''
 else:
  text+=r'''For computational operands narrower than FLEN, all source upper bits must be one.
Otherwise replace that operand with its format's canonical quiet NaN before applying the rules.
This replacement itself raises no flag; another signaling operand may still set NV.
`FLEN` is 32/64/128 according to the currently provided f-register formats.
Each floating destination is NaN-boxed by setting its upper FLEN-minus-format-width bits to one.
The displayed `fd` value denotes the low-format result and includes this writeback convention.
For raw FMV/load/store instructions boxing is not checked on input: low transferred bits,
including NaN payload and sign, are preserved. Stores ignore upper source bits.
`a` denotes a raw source bitvector in those transfer formulas; `n`, or `n_1,n_2`, denotes integer input bits.

'''
 text+=derived_section(fam)
 if cat=='21':
  text+=r'''The CSR addresses are fflags=1, frm=2, fcsr=3.
$\mathrm{oldfflags}$ is the entry fflags value interpreted as an unsigned five-bit integer;
$\mathrm{old}(q)$ is the entry bit-vector value of CSR field $q$. The width masks are 5, 3 and 8 bits;
within fcsr, frm is bits 7:5 and fflags is bits 4:0. Writing an alias preserves the other field.
In the scalar standard configuration modeled here, fcsr bits 31:8 have no defining extension;
reads return zero and writes to those bits are ignored. A platform adding another fcsr extension
must supply its specified upper-bit behavior. All rd results are zero-extended to XLEN.
The pure write-set operation $\mathrm{CSRWrite}_{q}(v)$ replaces field $q$ with
$v\bmod2^{k_q}$, where $k_{fflags}=5$, $k_{frm}=3$, and $k_{fcsr}=8$; the two
aliases preserve every bit outside their field. It is a write set, not a permission predicate.
Explicit CSR writes may clear flags, unlike arithmetic sticky increments.
CSRRW/CSRRWI with rd=x0 suppress reads; the displayed old value is discarded and no read side effect
occurs. CSRRS/CSRRC suppress writes when rs1 encodes x0 (even if a different register also holds zero,
that does not suppress the write). CSRRSI/CSRRCI suppress writes when uimm=0.
AND and OR denote bitwise operations on XLEN-bit values, and the width-subscripted negation denotes bitwise complement, not a Boolean permission test. Immediate operands are zero-extended from five bits.
The floating CSRs have no read side effects. Suppression does not bypass their access checks.
The aliases with an optional destination use x0 when that operand is omitted.

'''
 if cat in ['19','20']:
  text+=r'''The effective address and payload width are

$$
EA=(n_1+\mathrm{sext}_{\mathrm{AXLEN}}(\mathrm{instr}.imm,12))\bmod2^{\mathrm{AXLEN}},\qquad w=w_F.
$$

`AXLEN` is the current address width when MPRV=0, or the width of the privilege mode selected by MPP when MPRV=1, as specified by the memory-privilege rules.

`access` is the outcome record of the architectural memory-access operation, not a Boolean
fault predicate or a new hardware CSR. Its inputs are EA, width, read/write direction, the raw
store payload, the entry memory, and the execution/translation/protection configuration in section 1.
It uses exactly the ordinary integer memory-access rules at this byte width. `access.value` is the
raw loaded payload; `access.mem` is the resulting memory; `access.exception` is empty or the single
selected exception, after the manual's exception priority. Address translation and protection retain
their Privileged ISA definitions; this floating specification composes with that memory relation.
In particular, permission/page-walk checks use PTE V/R/W/X/U/A/D and SUM/MXR, and G-stage failures
produce guest-page faults. A bare mapping does not create a page fault. PMP/PMA failure can create
an access fault, including during page-table access.

The priority is data breakpoint, then misalignment if the implementation checks it early, then
translation page/guest-page/access faults, then physical access faults, then late misalignment.
Misalignment may instead be supported invisibly, and is never inferred to trap from EA alone.
Translation-stage alternatives follow the translation algorithm, not an invented fixed page-vs-guest order.
Non-atomic accesses may leave already-written store bytes visible after a fault. `access.mem` includes
those effects and any architectural page-table updates; an exception does not assert unchanged memory.
Aligned FLH/FLW are guaranteed atomic; aligned FLD/FSD require XLEN at least 64 for the guarantee;
FLQ/FSQ require aligned addresses and XLEN=128 for their atomicity guarantee; hence RV32/RV64 do not have that guarantee. Other cases inherit the platform's permitted memory behavior.

'''
 text+='## 5. Exception and flag sets\n\n### 5.1 Synchronous exceptions\n\n'
 text+='Execution can produce `IllegalInstruction(2)` from feature/FS/machine/user access checks, or `VirtualInstruction(22)` from the applicable VS/VU state-enable checks. When `misa.F=1`, all FCSR gate clauses are vacuous; the virtual FCSR branch is unreachable. Reserved rm and RV32 odd double-register encodings are excluded rather than forced to trap.\n\n'
 if cat in ['19','20']:text+='Memory execution can additionally report Breakpoint(3), address misalignment, page fault, guest-page fault, or access fault with the exact load/store cause numbers in section 6. Only one cause is selected.\n\n'
 text+='### 5.2 Floating flag increments\n\n'
 flags=sorted({f for v in vs for c in v['cases'] for f in c['flags']},key=lambda f:['nv','dz','of','uf','nx'].index(f))
 text+='Reachable flags: '+(', '.join(f'`{f.upper()}({dict(nv=4,dz=3,of=2,uf=1,nx=0)[f]})`' for f in flags) or 'none')+'. Each formula specifies the increment explicitly.\n\n'
 if cat=='21':text+='These instructions read or replace CSR fields directly; all five flag bits can be changed by an explicit fflags/fcsr write. Their bit masks are the updates, not floating arithmetic exceptions.\n\n'
 text+='## 6. Result formulas\n\n'
 for v in sorted(vs,key=lambda v:(v['instr'],v.get('csraddr',0))):
  text+=f'### {v["instr"]}'+(f' — CSR address {v["csraddr"]}' if 'csraddr'in v else '')+'\n\n'
  if xregs and ('D' in v['input_formats'] or (v['fmt']=='D' and any(c['target']=='fd' for c in v['cases']))):
   text+='For XLEN=32, restrict every double-width source/destination register index to an even number before evaluating these rules.\n\n'
  i=0;label=v['instr']+(f'.CSR{v["csraddr"]}' if 'csraddr'in v else '')
  for title,conds,exc in guards(v,xregs):
   text+=formula(f'{label}.{i}',title,conds+instrterm(v),rf'\mathrm{{exception}}=\{{{exc}\}}');i+=1
  for rawcase in v['cases']:
   c=normalize_case(rawcase,v)
   env,features,mode=config(v,xregs)
   modeconds=[t for t in c['conds'] if r'\mathrm{instr}.rm' in t or 'fcsr.frm' in t]
   operands=[t for t in c['conds'] if t not in modeconds]
   text+=formula(f'{label}.{i}',c['title'],env+features+mode+modeconds+operands+instrterm(v),emit_case(c,v,xregs));i+=1
 text+='### Format generalization\n\n'
 text+='Every listed format is expanded above. Equivalently, substitute the variant-specific extension requirements, concrete instruction name, and format widths/exponents in the same case partition. Cross-format conversions keep separate source and destination parameters. There is no inferred Q x-register form or Zfa x-register form.\n\n'
 text+='## 7. Conventions and completeness\n\n'
 text+='The ordered rules partition the defined instruction configurations. Special inputs are handled before finite numeric expressions. Static and dynamic rounding use the original fields. Results preserve signed zero and IEEE value classes; raw transfers/sign injection preserve the mandated payload bits. The FS relation includes the manual-permitted implementation choice, and CSR writes explicitly replace fields. The memory relation retains its architecture-defined nondeterminism and possible partial effects. No floating flag raises a synchronous trap.\n\n'
 text+='## 8. Manual evidence\n\n| Claim | Source |\n|---|---|\n'
 for ref in refs_for(fam):
  pp=ref['pages'];pages=str(pp[0]) if len(pp)==1 else f'{pp[0]}–{pp[-1]}'
  vol='Unprivileged' if ref['volume']=='unprivileged' else 'Privileged'
  text+=f'| {ref["claim"]} | {vol} ISA §{ref["section"]}, PDF pages {pages}; `sources/riscv-{ref["volume"]}.txt:{ref["first"]}–{ref["last"]}` |\n'
 return text

def refine_tininess():
 for fam in FAMILIES.values():
  cat=fam.get('basecat',fam['cat'])
  if cat not in ['03','04','06','14','22']:continue
  for v in fam['variants']:
   cs=[]
   for c in v['cases']:
    if c['flags']==['nx'] and 'normal' in c['title'] and 'subnormal' not in c['title']:
     emin=FMT[v['fmt']][3]
     good=dict(c,conds=c['conds']+[rf'(\lvert\mathrm{{unbounded}}\rvert\ge2^{{{emin}}})'])
     good['title']+='; non-tiny after precision-only rounding'
     tiny=dict(c,conds=c['conds']+[rf'(\lvert\mathrm{{unbounded}}\rvert<2^{{{emin}}})'],flags=['uf','nx'])
     tiny['title']+='; tiny before final subnormal-grid rounding'
     cs += [good,tiny]
    else: cs.append(c)
   v['cases']=cs

refine_tininess()

def main():
 global OUT
 import argparse
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--output', default='build/scalar-fp-instructions', help='Output directory relative to the project root')
 args=parser.parse_args()
 OUT=ROOT/args.output
 OUT.mkdir(parents=True,exist_ok=True)
 index='# Scalar RISC-V floating-point instruction formalization\n\n'
 index+='English, self-contained documents following the packaged workflow. Scope: scalar instructions in Unprivileged chapters 21–27 for RV32/RV64, floating CSR aliases and the six Zicsr access operations on fcsr/frm/fflags. Vector operations and compressed encodings from other chapters are outside this chapter-bounded collection.\n\n'
 index+='The formulas use the local manual editions in `sources/`. FS dirty tracking, read-only SD summaries, reserved encodings, state-enable gates including `misa=0`, and x-register writeback follow the manual rather than the stronger assumptions in the pilot. A memory access is composed with the ordinary architectural translation/protection relation; its exceptions and partial memory effects are retained.\n\n'
 index+='| Document | Concrete instructions | Formats | Reachable arithmetic flags | Status |\n|---|---:|---|---|---|\n'
 manifest=[]
 for name,fam in sorted(FAMILIES.items()):
  assert fam['variants'],name
  text=document(name,fam);path=OUT/(fam['key']+'.md');path.write_text(text)
  vs=fam['variants'];flags=sorted({f.upper() for v in vs for c in v['cases'] for f in c['flags']})
  index+=f'| [{name}]({path.name}) | {len(vs)} | '+', '.join(sorted({v['fmt'] for v in vs}))+ ' | '+(', '.join(flags) or 'none')+' | specified |\n'
  manifest.append({'document':str(path.relative_to(ROOT)),'family':name,'xregs':fam.get('xregs',False),'variants':[{'instruction':v['instr'],'format':v['fmt'],'input_formats':v['input_formats'],'extensions':v['ext'],'rounding_field':v['rm'],'xlen':v.get('xlen'),'csr_address':v.get('csraddr'),'case_count':len(v['cases'])} for v in vs],'formula_count':text.count(r'\longrightarrow'),'sha256':hashlib.sha256(text.encode()).hexdigest(),'sources':refs_for(fam)})
 index+='\nRebuild: `python3 -I tools/build_fp_instructions.py`. Validate: `python3 -I tools/validate_instructions.py`. The coverage manifest and exact source excerpts are in `reports/scalar-fp-manifest.json`.\n'
 (OUT/'README.md').write_text(index)
 (ROOT/'reports/scalar-fp-manifest.json').write_text(json.dumps({'scope':'scalar chapters 21–27, RV32/RV64, floating CSR accesses','input_hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'sources/riscv-unprivileged.pdf',ROOT/'sources/riscv-unprivileged.txt',ROOT/'sources/riscv-privileged.pdf',ROOT/'sources/riscv-privileged.txt',ROOT/'tools/fp_arithmetic_seed.json']},'documents':manifest},indent=2,ensure_ascii=False)+'\n')
 print('Documents:',len(manifest),'concrete variant rows:',sum(len(f['variants']) for f in manifest),'result formulas:',sum(f['formula_count'] for f in manifest))

if __name__=='__main__':main()
