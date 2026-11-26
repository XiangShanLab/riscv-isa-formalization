#!/usr/bin/env python3
"""Independent exact-rational interpretation of the delivery's numerical rules.
It is intentionally not SoftFloat or host IEEE arithmetic. Tininess detection uses its own
rounding with an unbounded exponent (README 6.1); disagreement is evidence to inspect, not
proof of a simulator bug.
"""
from fractions import Fraction as Q
from math import isqrt
from generate import FMT
NV,DZ,OF,UF,NX=16,8,4,2,1

def pow2(n):return Q(1<<n) if n>=0 else Q(1,1<<-n)
def decode(bits,fmt):
 w,e,f=FMT[fmt];bits&=(1<<w)-1;s=bits>>(w-1);exp=(bits>>f)&((1<<e)-1);frac=bits&((1<<f)-1);bias=(1<<(e-1))-1
 if exp==(1<<e)-1:return ('snan' if frac and not frac>>(f-1) else 'qnan' if frac else 'inf',s,None)
 value=Q(frac if exp==0 else (1<<f)+frac)*pow2((1-bias if exp==0 else exp-bias)-f)
 return ('zero' if value==0 else 'finite',s,-value if s else value)
def canonical(fmt):
 w,e,f=FMT[fmt];return (((1<<e)-1)<<f)|(1<<(f-1))
def inf(fmt,sign):
 w,e,f=FMT[fmt];return (sign<<(w-1))|(((1<<e)-1)<<f)
def zero(fmt,sign):return sign<<(FMT[fmt][0]-1)
def floor_log2(v):
 e=v.numerator.bit_length()-v.denominator.bit_length()
 return e-1 if v<pow2(e) else e
def round_unbounded(v,fmt,rm):
 # Tininess detection rounds to the format's precision with no exponent cap.
 if v==0:return Q(0)
 sign=v<0;v=abs(v);step=pow2(floor_log2(v)-FMT[fmt][2])
 return abs(rounded_integer((-v if sign else v)/step,rm))*step*(-1 if sign else 1)
def rounded_integer(v,rm):
 sign=v<0;v=abs(v);q,r=divmod(v.numerator,v.denominator);d=v.denominator
 inc=bool(r) and ((rm==0 and (2*r>d or (2*r==d and q&1))) or (rm==4 and 2*r>=d) or (rm==2 and sign) or (rm==3 and not sign))
 return (-1 if sign else 1)*(q+inc)
def rounded(v,fmt,rm,signzero=0,sqrt=False):
 w,e,f=FMT[fmt];emin=2-(1<<(e-1));emax=(1<<(e-1))-1
 if v==0:return zero(fmt,signzero),0
 sign=v<0;v=abs(v)
 exp=floor_log2(v)//2 if sqrt else floor_log2(v)
 step=pow2(max(exp,emin)-f)
 if sqrt:
  scaled=v/(step*step);num,den=scaled.numerator,scaled.denominator;q=isqrt(num//den)
  exact=q*q*den==num
  midpoint=(2*q+1)**2*den
  inc=not exact and ((rm==0 and (4*num>midpoint or (4*num==midpoint and q&1))) or (rm==4 and 4*num>=midpoint) or rm==3)
  r=(q+inc)*step;inexact=not exact
 else:
  signed=-v if sign else v;r=abs(rounded_integer(signed/step,rm))*step;inexact=r!=v
 tiny=(not sqrt) and 0<abs(round_unbounded(-v if sign else v,fmt,rm))<pow2(emin)
 if r>=pow2(emax+1):
  outward=rm in [0,4] or (rm==2 and sign) or (rm==3 and not sign)
  return (inf(fmt,int(sign)) if outward else inf(fmt,int(sign))-1),OF|NX
 if not r:return zero(fmt,int(sign)),UF|NX
 re=floor_log2(r);is_sub=re<emin
 frac=int(r/pow2(emin-f)) if is_sub else int(r/pow2(re-f))-(1<<f)
 raw=zero(fmt,int(sign))|((0 if is_sub else re+((1<<(e-1))-1))<<f)|frac
 return raw,(NX if inexact else 0)|(UF if tiny and inexact else 0)
def available(c,p):
 ext=set(p['ext']);op=c['op'];fmt=c['fmt'];src=c['src'];bank=p['bank'];kind=c['kind']
 if bank=='f' and c['fs']==0:return False
 if any('_'+t in op for t in ['l','lu']) and op.startswith('fcvt_') and p['xlen']==32:return False
 if kind=='csr':return True
 if bank=='x':
  if 'd' in [fmt,src] and 'zdinx' not in ext:return False
  if 'h' in [fmt,src]:
   if kind=='convert':return 'zhinxmin' in ext or 'zhinx' in ext
   return 'zhinx' in ext
  return True
 if any(op.startswith(x) for x in ['fli_','fminm_','fmaxm_','fround_','froundnx_','fleq_','fltq_','fcvtmod_','fmvh_','fmvp_']) and 'zfa' not in ext:return False
 if 'bf16' in op:return 'zfbfmin' in ext
 if fmt=='h' or src=='h':
  if kind=='convert':return 'zfhmin' in ext or 'zfh' in ext
  if kind in ['load','store'] or op in ['fmv_x_h','fmv_h_x']:return bool(ext&{'zfh','zfhmin','zfbfmin'})
  return 'zfh' in ext
 return True

def expect(c,p):
 """Return (result bytes, fcsr, exception) or None for an unmodelled operation."""
 if not available(c,p):return (None,None,2)
 fmt=c['fmt'];src=c['src'];op=c['op'];root=op.split('_')[0];kind=c['kind'];xlen=p['xlen'];bank=p['bank'];flen=p.get('flen',64)
 bits=[int(c[k],16) for k in ['a','b','c']];rm=c['frm'] if c['rm']==7 else c['rm'];flags=0;fp=True
 if bank=='f':
  # A narrow operand whose upper bits are not all ones reads as the canonical NaN.
  box=c['boxing'] if isinstance(c['boxing'],list) else [c['boxing']]*3
  bits=[canonical(src) if not box[0] else bits[0],
        canonical(fmt) if not box[1] else bits[1],
        canonical(fmt) if not box[2] else bits[2]]
 a=decode(bits[0],src);b=decode(bits[1],fmt);d=decode(bits[2],fmt)
 raw=None;fcsr_override=None
 if kind=='store':
  return ((0x99aabbccddeeff001122334455667788&((1<<flen)-1)).to_bytes(16,'little').hex(),(c['frm']<<5)|c['flags'],0)
 if kind=='load':raw=bits[0]&((1<<FMT[fmt][0])-1)
 elif kind=='csr':
  fp=False;old=(c['frm']<<5)|c['flags'];u=bits[0]
  raw=old if op in ['frcsr','fscsr'] else c['frm'] if op in ['frrm','fsrm'] else c['flags']
  fcsr_override=(u&255) if op=='fscsr' else ((u&7)<<5)|(old&31) if op=='fsrm' else (old&224)|(u&31) if op=='fsflags' else old
 elif root=='fli':
  i=c['imm'];emin=2-(1<<(FMT[fmt][1]-1))
  constants=[-1,pow2(emin),pow2(-16),pow2(-15),pow2(-8),pow2(-7),pow2(-4),pow2(-3),pow2(-2),Q(5,16),Q(3,8),Q(7,16),Q(1,2),Q(5,8),Q(3,4),Q(7,8),1,Q(5,4),Q(3,2),Q(7,4),2,Q(5,2),3,4,8,16,128,256,1<<15,1<<16]
  if i==31:raw=canonical(fmt)
  elif i==30 or (i==29 and fmt=='h'):raw=inf(fmt,0)
  else:raw,_=rounded(Q(constants[i]),fmt,0)
 elif root in ['fmv','fmvh','fmvp']:
  if root=='fmvh':fp=False;raw=bits[0]>>xlen
  elif root=='fmvp':raw=(bits[0]&((1<<xlen)-1))|((bits[1]&((1<<xlen)-1))<<xlen)
  elif op.startswith('fmv_x_'):
   fp=False;w=FMT[fmt][0];raw=bits[0]&((1<<w)-1)
   if w<xlen and raw>>(w-1):raw|=((1<<xlen)-1)^((1<<w)-1)
  else:raw=bits[0]&((1<<FMT[fmt][0])-1)
 elif root in ['fadd','fsub','fmul','fdiv','fmadd','fmsub','fnmsub','fnmadd','fsqrt']:
  ops=[a] if root=='fsqrt' else [a,b,d] if kind=='fma' else [a,b]
  invalid=any(x[0]=='snan' for x in ops)
  nan=any('nan' in x[0] for x in ops)
  if kind=='fma':
   ps=a[1]^b[1]^(root in ['fnmsub','fnmadd']);cs=d[1]^(root in ['fmsub','fnmadd'])
   invalid|=(a[0]=='zero' and b[0]=='inf') or (a[0]=='inf' and b[0]=='zero')
   pinf=(a[0]=='inf' and b[0] in ['finite','inf']) or (b[0]=='inf' and a[0] in ['finite','inf'])
   invalid|=pinf and d[0]=='inf' and ps!=cs
   if invalid or nan:raw=canonical(fmt);flags=NV if invalid else 0
   elif pinf:raw=inf(fmt,ps)
   elif d[0]=='inf':raw=inf(fmt,cs)
   else:
    v=a[2]*b[2]*(-1 if root in ['fnmsub','fnmadd'] else 1)+d[2]*(-1 if root in ['fmsub','fnmadd'] else 1)
    zs=ps if (a[0]=='zero' or b[0]=='zero') and d[0]=='zero' and ps==cs else int(rm==2)
    raw,flags=rounded(v,fmt,rm,zs)
  elif root in ['fadd','fsub']:
   bs=b[1]^(root=='fsub');invalid|=a[0]==b[0]=='inf' and a[1]!=bs
   if invalid or nan:raw=canonical(fmt);flags=NV if invalid else 0
   elif a[0]=='inf':raw=inf(fmt,a[1])
   elif b[0]=='inf':raw=inf(fmt,bs)
   else:
    v=a[2]+(-b[2] if root=='fsub' else b[2]);zs=a[1] if a[0]==b[0]=='zero' and a[1]==bs else int(rm==2)
    raw,flags=rounded(v,fmt,rm,zs)
  elif root=='fmul':
   invalid|={a[0],b[0]}=={'zero','inf'}
   if invalid or nan:raw=canonical(fmt);flags=NV if invalid else 0
   elif 'inf' in [a[0],b[0]]:raw=inf(fmt,a[1]^b[1])
   else:raw,flags=rounded(a[2]*b[2],fmt,rm,a[1]^b[1])
  elif root=='fdiv':
   invalid|=a[0]==b[0] and a[0] in ['zero','inf']
   if invalid or nan:raw=canonical(fmt);flags=NV if invalid else 0
   elif a[0]=='inf':raw=inf(fmt,a[1]^b[1])
   elif b[0]=='zero':raw=inf(fmt,a[1]^b[1]);flags=DZ
   elif b[0]=='inf':raw=zero(fmt,a[1]^b[1])
   else:raw,flags=rounded(a[2]/b[2],fmt,rm,a[1]^b[1])
  else:
   invalid|=a[1]==1 and a[0] in ['finite','inf']
   if invalid or nan:raw=canonical(fmt);flags=NV if invalid else 0
   elif a[0]=='inf':raw=inf(fmt,0)
   else:raw,flags=rounded(a[2],fmt,rm,a[1],sqrt=True)
 elif root in ['fsgnj','fsgnjn','fsgnjx']:
  sign=b[1] if root=='fsgnj' else b[1]^1 if root=='fsgnjn' else a[1]^b[1]
  raw=(bits[0]&((1<<(FMT[fmt][0]-1))-1))|zero(fmt,sign)
 elif root in ['fmin','fmax','fminm','fmaxm']:
  an='nan' in a[0];bn='nan' in b[0];flags=NV if 'snan' in [a[0],b[0]] else 0
  if (an and bn) or ((an or bn) and root.endswith('m')):raw=canonical(fmt)
  elif an:raw=bits[1]
  elif bn:raw=bits[0]
  else:
   def key(v):return (-1 if v[1] else 1,None) if v[0]=='inf' else (0,v[2])
   ka,kb=key(a),key(b)
   if ka==kb:raw=(bits[0]|bits[1]) if root=='fmin' or root=='fminm' else (bits[0]&bits[1])
   else:raw=bits[0] if ((ka<kb)==root.startswith('fmin')) else bits[1]
 elif root in ['feq','flt','fle','fleq','fltq']:
  fp=False;nan=any('nan' in v[0] for v in [a,b]);flags=NV if any(v[0]=='snan' for v in [a,b]) or (nan and root in ['flt','fle']) else 0
  def key(v):return (-1 if v[1] else 1,None) if v[0]=='inf' else (0,v[2])
  raw=0 if nan else int(key(a)==key(b) if root=='feq' else key(a)<key(b) if root in ['flt','fltq'] else key(a)<=key(b))
 elif root=='fclass':
  fp=False
  w,e,f=FMT[fmt];ex=(bits[0]>>f)&((1<<e)-1)
  ix={'inf':0 if a[1] else 7,'zero':3 if a[1] else 4,'snan':8,'qnan':9}.get(a[0],(1 if a[1] else 6) if ex else (2 if a[1] else 5))
  raw=1<<ix
 elif root in ['fround','froundnx']:
  if 'nan' in a[0]:raw=canonical(fmt);flags=NV if a[0]=='snan' else 0
  elif a[0]=='inf':raw=inf(fmt,a[1])
  else:
   u=rounded_integer(a[2],rm);raw,_=rounded(Q(u),fmt,0,a[1]);flags=NX if root=='froundnx' and u!=a[2] else 0
 elif kind=='convert':
  if 'nan' in a[0]:raw=canonical(fmt);flags=NV if a[0]=='snan' else 0
  elif a[0]=='inf':raw=inf(fmt,a[1])
  else:raw,flags=rounded(a[2],fmt,rm,a[1])
 elif root=='fcvtmod':
  fp=False
  if 'nan' in a[0] or a[0]=='inf':raw=0;flags=NV
  else:
   u=rounded_integer(a[2],1);raw=u&0xffffffff;flags=NV if not -(1<<31)<=u<(1<<31) else NX if u!=a[2] else 0
   if xlen==64 and raw>>31:raw|=0xffffffff00000000
 elif root=='fcvt' and kind=='intout':
  fp=False;typ=op.split('_')[1];width=32 if typ in ['w','wu'] else 64
  lo=0 if typ.endswith('u') else -(1<<(width-1));hi=(1<<width)-1 if typ.endswith('u') else (1<<(width-1))-1
  if 'nan' in a[0] or a[0]=='inf':u=lo if a[0]=='inf' and a[1] else hi;flags=NV
  else:
   u=rounded_integer(a[2],rm)
   if not lo<=u<=hi:u=max(lo,min(hi,u));flags=NV
   elif u!=a[2]:flags=NX
  raw=u&((1<<width)-1)
  if width==32 and raw>>31:raw|=((1<<xlen)-1)^((1<<32)-1)
 elif root=='fcvt' and kind=='intin':
  typ=op.split('_')[2];width=32 if typ in ['w','wu'] else 64;u=bits[0]&((1<<min(width,xlen))-1)
  if not typ.endswith('u') and (u>>(width-1)):u-=1<<width
  raw,flags=rounded(Q(u),fmt,rm)
 else:return None
 if raw is None:return None
 if c.get('observe_unchanged_dest'):
  return ((0x1122334455667788&((1<<max(FMT[fmt][0],xlen))-1)).to_bytes(16,'little').hex(),(c['frm']<<5)|c['flags']|flags,0)
 if fp:
  if bank=='f':raw|=((1<<flen)-1)^((1<<FMT[fmt][0])-1)
  elif FMT[fmt][0]<xlen and (raw>>(FMT[fmt][0]-1))&1:raw|=((1<<xlen)-1)^((1<<FMT[fmt][0])-1)
 width=flen if fp and bank=='f' else max(FMT[fmt][0],xlen) if fp else xlen
 return (int(raw&((1<<width)-1)).to_bytes(16,'little').hex(),fcsr_override if fcsr_override is not None else (c['frm']<<5)|c['flags']|flags,0)
