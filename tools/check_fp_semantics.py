#!/usr/bin/env python3
"""Instantiate emitted field conditions on scalar boundary cases.

Independent exact Fraction arithmetic checks the arithmetic partition, including
all five modes. This is bounded regression evidence, not a proof of the ISA.
"""
from pathlib import Path
from fractions import Fraction
from itertools import product
import re, runpy, json
ROOT=Path(__file__).resolve().parents[1]
m=runpy.run_path(str(ROOT/'tools/build_fp_instructions.py'))

def p2(e):return Fraction(2)**e

def round_precision(v,p,emin=None,mode=0):
 if not v:return Fraction(0)
 sign=-1 if v<0 else 1;a=abs(v)
 e=a.numerator.bit_length()-a.denominator.bit_length()
 if a<p2(e):e-=1
 step=p2(e-(p-1))
 if emin is not None:step=max(step,p2(emin-(p-1)))
 q=a/step;n=q.numerator//q.denominator;tail=q-n
 up=(tail>Fraction(1,2) or (tail==Fraction(1,2) and n%2==1)) if mode==0 else \
    False if mode==1 else (sign<0 and tail!=0) if mode==2 else \
    (sign>0 and tail!=0) if mode==3 else tail>=Fraction(1,2)
 return sign*(n+int(up))*step

def decode(u):
 s=u>>15;e=(u>>10)&31;f=u&1023
 v=(-1 if s else 1)*(Fraction(1024+f)*p2(e-25) if e else Fraction(f)*p2(-24)) if e!=31 else None
 return (s,e,f,v)

def translate(cond):
 s=cond
 for word in ['bigl','bigr','big','left','right']:
  s=s.replace('\\'+word,'')
 s=s.replace(r'\mathrm{instr}.rm','rm').replace('fcsr.frm','frm')
 for a in 'abc':
  s=s.replace(rf'f_{a}[w_{{f,{a}}}-1]',f'((f_{a}>>9)&1)').replace(rf'e_{{\max,{a}}}',f'emax_{a}')
 for k in ['exact','rounded','unbounded']:s=s.replace(rf'\mathrm{{{k}}}',k)
 s=re.sub(r'\\mathrm\{(?:RNE|RTZ|RDN|RUP|RMM|DYN)\}\((\d)\)',r'\1',s)
 s=re.sub(r'2\^\{(-?\d+)\}',r'p2(\1)',s)
 s=re.sub(r'\\lvert\s*(.*?)\\rvert',r'abs(\1)',s)
 for a,b in [(r'\notin',' not in '),(r'\in',' in '),(r'\land',' and '),(r'\lor',' or '),(r'\neg',' not '),(r'\ne','!='),(r'\le','<='),(r'\ge','>='),(r'\oplus','^'),(r'\{','{'),(r'\}','}')]:s=s.replace(a,b)
 s=re.sub(r'(?<![<>=!])=(?!=)','==',s)
 return compile(s.strip(),'<emitted operand condition>','eval')

def run():
 # Every input class, both zero signs, exact cancellation, subnormal and overflow boundaries.
 bits=[0,0x8000,1,0x8001,0x3ff,0x400,0x3c00,0xbc00,0x7bff,0xfbff,0x7c00,0xfc00,0x7c01,0x7e00]
 decoded={u:decode(u) for u in bits};count=0;fail=[]
 for name in ['FADD','FSUB','FMUL','FDIV','FMADD','FMSUB','FNMSUB','FNMADD']:
  v=next(v for v in m['FAMILIES'][name]['variants'] if v['fmt']=='H')
  cs=[m['normalize_case'](c,v) for c in v['cases']]
  compiled=[[(translate(t),t) for t in c['conds']] for c in cs]
  n=3 if name in ['FMADD','FMSUB','FNMSUB','FNMADD'] else 2
  for us in product(bits,repeat=n):
   ds=[decoded[u] for u in us]
   finite=all(d[1]!=31 for d in ds)
   for rm in range(5):
    env={'rm':rm,'frm':6,'p2':p2,'abs':abs,'exact':Fraction(0),'rounded':Fraction(0),'unbounded':Fraction(0)}
    for a,d in zip('abc',ds):env.update({f's_{a}':d[0],f'e_{a}':d[1],f'f_{a}':d[2],f'emax_{a}':31})
    if finite:
     x,y=ds[0][3],ds[1][3]
     if name=='FADD':exact=x+y
     elif name=='FSUB':exact=x-y
     elif name=='FMUL':exact=x*y
     elif name=='FDIV':exact=x/y if y else Fraction(0)
     else:
      z=ds[2][3];exact=(-1 if name in ['FNMSUB','FNMADD'] else 1)*x*y+(-z if name in ['FMSUB','FNMADD'] else z)
     env.update(exact=exact,rounded=round_precision(exact,11,-14,rm),unbounded=round_precision(exact,11,None,rm))
    chosen=None
    for i,conditions in enumerate(compiled):
     if all(eval(code,{'__builtins__':{}},env) for code,_ in conditions):chosen=i;break
    count+=1
    if chosen is None:
     fail.append((name,list(us),rm,'no matching result'));continue
    c=cs[chosen]
    # Equal negative effective zero terms must remain negative for every rounding mode.
    if name in ['FMADD','FMSUB','FNMSUB','FNMADD'] and all(d[1]==0 and d[2]==0 for d in ds):
     ps=ds[0][0]^ds[1][0]^int(name in ['FNMSUB','FNMADD'])
     zs=ds[2][0]^int(name in ['FMSUB','FNMADD'])
     neg=ps if ps==zs else int(rm==2)
     expected=('-' if neg else '+')+'0_{H}'
     if c['value']!=expected:fail.append((name,list(us),rm,'zero sign',c['value'],expected))
    # Invalid dominates quiet NaNs in the mandated FMA 0*infinity case.
    if n==3 and ((ds[0][1]==31 and ds[0][2]==0 and ds[1][1]==0 and ds[1][2]==0) or (ds[1][1]==31 and ds[1][2]==0 and ds[0][1]==0 and ds[0][2]==0)):
     if c['flags']!=['nv']:fail.append((name,list(us),rm,'FMA invalid lost'))
    # The RISC-V table expressly excludes UF and DZ on addition/subtraction.
    if name in ['FADD','FSUB'] and set(c['flags'])&{'uf','dz'}:fail.append((name,list(us),rm,'unreachable add/sub flag'))
 # Explicit manual counterexample: final normal BF16 result can still underflow.
 exact=p2(-126)-3*p2(-136)
 final=round_precision(exact,8,-126,0);unbounded=round_precision(exact,8,None,0)
 assert final==p2(-126) and 0<unbounded<p2(-126) and final!=exact
 # RNE can preserve max finite with NX below its overflow boundary.
 assert round_precision(Fraction(65504)+8,11,-14,0)==65504
 assert round_precision(Fraction(65504)+16,11,-14,0)==65536
 result={'arithmetic_instantiations':count,'modes':[0,1,2,3,4],'issues':fail,'additional_checks':['BF16 normal-result UF+NX boundary','H RNE overflow threshold']}
 (ROOT/'reports/scalar-fp-semantics.json').write_text(json.dumps(result,indent=2)+'\n')
 print('Arithmetic instantiations:',count,'issues:',len(fail))
 for f in fail[:10]:print(f)
 return bool(fail)

if __name__=='__main__':raise SystemExit(run())
