#!/usr/bin/env python3
"""Generate deterministic bare-metal programs, vectors and document inventory.
No floating-point instruction is executed by the host generator.
"""
from pathlib import Path
import argparse, hashlib, itertools, json, random, re
ROOT=Path(__file__).resolve().parent
DOC=ROOT.parent.parent/'out'/ROOT.name
ENC=json.loads((ROOT/'encodings.json').read_text())
FMT={'h':(16,5,10),'s':(32,8,23),'d':(64,11,52),'q':(128,15,112),'bf16':(16,8,7)}
RMS=[(i,0) for i in range(5)]+[(7,i) for i in range(5)]
# riscv-arch-test (ACT4) operand tables, see reports/act4-operands-2026-11-24/REPORT.md.
# FLOAT_EDGES and the bad-NaN-boxing images are copied literally from
# generators/testgen/src/testgen/data/edges.py; imm_12bit and the integer edges from
# the same file (IMMEDIATE_EDGES, get_general_edges).
ACT4_EDGES={
 'h':(0x0000,0x8000,0x3C00,0xBC00,0x4100,0xC100,0x6800,0xE800,0x0400,0x8400,
      0x7BFF,0xFBFF,0x03FF,0x83FF,0x0200,0x8200,0x0001,0x8001,0x7C00,0xFC00,
      0x7E00,0x7FFF,0xFE00,0x7C01,0x7DFF,0xFC01,0x58B4,0xC93A),
 's':(0x00000000,0x80000000,0x3F800000,0xBF800000,0x40200000,0xC0200000,
      0x4B800000,0xCB800000,0x00800000,0x80800000,0x7F7FFFFF,0xFF7FFFFF,
      0x007FFFFF,0x807FFFFF,0x00400000,0x80400000,0x00000001,0x80000001,
      0x7F800000,0xFF800000,0x7FC00000,0x7FFFFFFF,0xFFFFFFFF,0x7F800001,
      0x7FBFFFFF,0xFFBFFFFF,0x7EF8654F,0x813D9AB0),
 'd':(0x0000000000000000,0x8000000000000000,0x3FF0000000000000,0xBFF0000000000000,
      0x4004000000000000,0xC004000000000000,0x4340000000000000,0xC340000000000000,
      0x0010000000000000,0x8010000000000000,0x7FEFFFFFFFFFFFFF,0xFFEFFFFFFFFFFFFF,
      0x000FFFFFFFFFFFFF,0x800FFFFFFFFFFFFF,0x0008000000000000,0x8008000000000000,
      0x0000000000000001,0x8000000000000001,0x7FF0000000000000,0xFFF0000000000000,
      0x7FF8000000000000,0x7FFFFFFFFFFFFFFF,0xFFF8000000000000,0x7FF0000000000001,
      0x7FF7FFFFFFFFFFFF,0xFFF0000000000001,0x5A392534A57711AD,0xA6E895993737426C),
 'bf16':(0x0000,0x8000,0x3F80,0xBF80,0x4020,0xC020,0x4380,0xC380,0x0080,0x8080,
         0x7F7F,0xFF7F,0x007F,0x807F,0x0040,0x8040,0x0001,0x8001,0x7F80,0xFF80,
         0x7FC0,0x7FFF,0xFFFF,0x7F81,0x7FBF,0xFFBF,0x7EF8,0x813D),
}
# FLOAT_EDGES values that the named patterns() entries above do not already cover.
ACT4_EXTRA={
 'h':{0x7DFF:'asnanmax',0xFE00:'anqnan0',0x58B4:'arandp',0xC93A:'arandn'},
 's':{0x7FBFFFFF:'asnanmax',0xFFBFFFFF:'ansnanmax',0x7EF8654F:'arandp',0x813D9AB0:'arandn'},
 'd':{0x7FF7FFFFFFFFFFFF:'asnanmax',0xFFF8000000000000:'anqnan0',
      0x5A392534A57711AD:'arandp',0xA6E895993737426C:'arandn'},
 'bf16':{0x7FBF:'asnanmax',0xFFBF:'ansnanmax',0x7EF8:'arandp',0x813D:'arandn'},
}
# Bad NaN-boxing images, keyed by (container width, operand format).
ACT4_BOX={(64,32):(0xFFFFEFFF00000000,0xAAAAAAAA80000000,0x000000003F800000,
                   0xDEADBEEFBF800000,0xA1B2C3D400800000,0xFFFFFFEF80800000,
                   0xFEFFFFEF7F7FFFFF,0x7E7E7E7EFF7FFFFF,0x7FFFFFFF7F800000,
                   0xFFFFFFFEFF800000,0xFEEDBEE57FC00000,0xFFC0DEFF7FFFFFFF,
                   0xFEFFFFFF7F800001,0xFFFFFEFF7FBFFFFF),
          (64,16):(0xFFFFFFFF00000000,0xFFFFFFFFFFFE8000,0x7FFFFFFFFFFF3C00,
                   0xFEEDBEE5BEEFBC00,0xFFFFFFEFFFFF0400,0x00000000FFFF8400,
                   0xEFFFFFFFFFFF7BFF,0xC0DEC0DEC0DEFBFF,0xA83EF1CC4F1A7C00,
                   0xFFFFFFFF0FFFFC00,0xFFFEFFFFFFFF7E00,0xFFFFFFEFFFFF7FFF,
                   0xA1B2C3D4E5F67C01,0xFFFFFFFCFFFF7DFF)}
ACT4_IMM12=(0,1,2,3,4,8,16,32,64,128,256,512,1023,1024,1795,2047,-2048,-2047,-2,-1)
ACT4_INT={32:(0,1,2,2**31,2**31+1,2**31-1,2**31-2,2**32-1,2**32-2,
              0b01011011101111001000100001110010,0b10101010101010101010101010101010,
              0b01010101010101010101010101010101),
          64:(0,1,2,2**63,2**63+1,2**63-1,2**63-2,2**64-1,2**64-2,
              0b0101101110111100100010000111011101100011101011101000011011110010,
              0b1010101010101010101010101010101010101010101010101010101010101010,
              0b0101010101010101010101010101010101010101010101010101010101010101,
              0xFFFFFFFF,0xFFFFFFFE,0x100000000,0x100000001,0x80000000,0x7FFFFFFF)}
# ACT4 cr_fp_reg_edges.py frm_modes = (dyn, rdn, rmm, rne, rtz, rup).
ACT4_RMS=[(7,0)]+[(i,0) for i in range(5)]
# Flags an arithmetic instruction may raise, preset before it executes (ACT4
# sticky-flag initialisation): NV|OF|UF|NX, plus DZ for FADD/FSUB/FMUL/FDIV.
ACT4_FLAGS={'fadd':16|4|2|1,'fsub':16|4|2|1,'fmul':16|4|2|1,'fdiv':16|8|4|2|1}
PROFILES={
 'rv64-f':dict(xlen=64,bank='f',formats='hsd',ext=['f','d','zfh','zfhmin','zfbfmin','zfa']),
 'rv32-f':dict(xlen=32,bank='f',formats='hsd',ext=['f','d','zfh','zfhmin','zfbfmin','zfa']),
 'rv64-q':dict(xlen=64,bank='f',formats='q',ext=['f','d','q','zfh','zfhmin','zfbfmin','zfa'],flen=128),
 'rv32-q':dict(xlen=32,bank='f',formats='q',ext=['f','d','q','zfh','zfhmin','zfbfmin','zfa'],flen=128),
 'rv64-x':dict(xlen=64,bank='x',formats='hsd',ext=['zfinx','zdinx','zhinx','zhinxmin']),
 'rv32-x':dict(xlen=32,bank='x',formats='hsd',ext=['zfinx','zdinx','zhinx','zhinxmin']),
 'rv64-hmin':dict(xlen=64,bank='f',formats='h',ext=['f','d','zfhmin']),
 'rv64-bfmin':dict(xlen=64,bank='f',formats='h',ext=['f','d','zfbfmin']),
 'rv64-xmin':dict(xlen=64,bank='x',formats='h',ext=['zfinx','zdinx','zhinxmin']),
}
def patterns(fmt):
 w,e,f=FMT[fmt]; sign=1<<(w-1); em=(1<<e)-1; inf=em<<f; bias=(1<<(e-1))-1
 twohalf=((bias+1)<<f)|(1<<(f-2)); twoprec=(bias+f+1)<<f; midsub=1<<(f-1)
 prand=((bias+4)<<f)|(((0x2D5A5A>>1)&((1<<f)-1))|1)
 d={'ninf':sign|inf,'nnormal':sign|(bias<<f),'nsub':sign|1,'nzero':sign,'pzero':0,
         'psub':1,'pnormal':bias<<f,'pinf':inf,'snan':inf|1,'qnan':inf|(1<<(f-1)),
         'max':inf-1,'nmax':sign|(inf-1),'minnormal':1<<f,'maxsub':(1<<f)-1,
         'half':(bias-1)<<f,'two':(bias+1)<<f,'threehalf':(bias<<f)|(1<<(f-1)),
         'nminnormal':sign|(1<<f),'nmaxsub':sign|((1<<f)-1),'nqnan':sign|inf|(1<<(f-1))|3,
         # riscv-arch-test cp_fs1/fs2/fs3_edges and cp_memval_fp_* bins not otherwise present.
         'twohalf':twohalf,'ntwohalf':sign|twohalf,'twoprec':twoprec,'ntwoprec':sign|twoprec,
         'midsub':midsub,'nmidsub':sign|midsub,'nsnan':sign|inf|1,'prand':prand,'nrand':sign|prand,
         'qnanmax':inf|((1<<f)-1),'nqnanmax':sign|inf|((1<<f)-1)}
 # Remaining ACT4 FLOAT_EDGES values (max-payload sNaN, negative canonical qNaN,
 # two fixed normals per format).
 d.update({name:value for value,name in ACT4_EXTRA.get(fmt,{}).items()})
 return d
def encoding(name,rd=24,rs1=18,rs2=20,rm=None,rs3=None):
 word=ENC[name]|rd<<7|rs1<<15
 if rs2 is not None: word=(word&~(31<<20))|(rs2<<20)
 if rs3 is not None: word|=rs3<<27
 if rm is not None: word|=rm<<12
 return word

def generate(profile,options):
 p=PROFILES[profile]; xlen=p['xlen']; bank=p['bank']; flen=p.get('flen',64); cases=[]
 rng=random.Random(0x46504420261120+xlen+(bank=='x'))
 def add(group,name,fmt,a=0,b=0,c=0,*,src=None,kind='fp',rm=None,frm=0,flags=0,fs=2,word=None,imm=None,tag='',boxing=True,upper=(0,0,0),rd=24,rs1=18,rs2=20,rs3=22):
  if isinstance(boxing,bool): boxing=(boxing,boxing,boxing)
  case=dict(id=len(cases),group=group,op=name,fmt=fmt,src=src or fmt,a=hex(a),b=hex(b),c=hex(c),kind=kind,rm=rm,frm=frm,flags=flags,fs=fs,tag=tag,boxing=list(boxing),upper=[hex(int(u)) for u in upper],regs=[rd,rs1,rs2,rs3])
  case['doc']='instructions/'+('zfinx' if bank=='x' else group)+'.md'
  if word is None: word=encoding(name,rd=rd,rs1=rs1,rs2=None if kind in ['unary','intout','intin','convert'] else rs2,rm=rm,rs3=rs3 if kind=='fma' else None)
  case['word']=word
  if imm is not None:case['imm']=imm
  cases.append(case)
 for fmt in p['formats']:
  vals=patterns(fmt); classes=list(vals.items())[:10]; allv=list(vals.items()); w=FMT[fmt][0]
  newkeys=[k for k in vals if k not in {ka for ka,_ in classes}]
  # Extreme dynamic range: one operand at the top of the exponent range and the other at the
  # bottom, so the small operand lies wholly outside the large operand's rounding grid.
  span=[('max','psub'),('max','nmaxsub'),('nmax','psub'),('nmax','nmaxsub'),
        ('psub','max'),('nmaxsub','max'),('minnormal','max'),('maxsub','max')]
  # Every pair of ten IEEE classes, plus boundary cases and seeded bit patterns.
  pairs=[(a,b,'class:'+ka+','+kb) for ka,a in classes for kb,b in classes]
  pairs += [(vals[a],vals[b],'boundary:'+a+','+b) for a,b in [('max','two'),('psub','half'),('minnormal','threehalf'),('minnormal','maxsub'),('nzero','pzero'),('pnormal','nnormal'),('max','minnormal')]]
  pairs += [(vals[a],vals[b],'span:'+a+','+b) for a,b in span]
  # Remaining arch-test edge values in each operand slot, against a fixed partner.
  pairs += [(vals[k],vals['two'],'edge:'+k+',two') for k in newkeys]
  pairs += [(vals['two'],vals[k],'edge:two,'+k) for k in newkeys]
  pairs += [(rng.getrandbits(w),rng.getrandbits(w),'random') for _ in range(options.random)]
  # ACT4 FLOAT_EDGES: every ordered pair of the 28 edge values, once each; pairs
  # already produced by the lines above are not repeated.
  act4=ACT4_EDGES.get(fmt)
  seen={(a,b) for a,b,_ in pairs}
  act4pairs=[] if act4 is None else [(x,y,'act4:%d,%d'%(i,j)) for i,x in enumerate(act4) for j,y in enumerate(act4) if (x,y) not in seen]
  roundops=['fadd','fsub','fmul','fdiv']; plain=['fmin','fmax','fsgnj','fsgnjn','fsgnjx','feq','flt','fle']
  if bank=='f':plain+=['fminm','fmaxm','fleq','fltq']
  for op in roundops+plain:
   group='fsgnj' if op.startswith('fsgnj') else op; name=op+'_'+fmt
   for n,(a,b,tag) in enumerate(pairs if op in roundops else pairs+act4pairs):
    rm,frm=RMS[n%len(RMS)] if op in roundops else (None,0)
    add(group,name,fmt,a,b,rm=rm,frm=frm,flags=8 if n%11==0 else 0,tag=tag)
   if op in roundops:
    for (rm,frm),(aa,bb) in itertools.product(RMS,[('max','two'),('psub','half'),('minnormal','threehalf'),('pnormal','nnormal'),('twohalf','two'),('twoprec','nmax'),('midsub','pnormal'),('prand','nrand'),('nsnan','snan')]+span):
     add(group,name,fmt,vals[aa],vals[bb],rm=rm,frm=frm,tag='rounding:'+aa+','+bb)
    # ACT4 cr_fp_reg_edges.py: the full 28 x 28 edge cross under each static
    # rounding mode plus DYN; a fifth of the cases start from preset sticky flags.
    for (rm,frm),(i,x),(j,y) in itertools.product(ACT4_RMS,enumerate(act4 or ()),enumerate(act4 or ())):
     add(group,name,fmt,x,y,rm=rm,frm=frm,flags=ACT4_FLAGS[op] if (i*31+j)%5==0 else 0,tag='act4-round:%d,%d'%(i,j))
  if bank=='f':
   # ACT4 cp_fs1/fs2/fs3/fd: each operand slot reaches the low and high ends of the
   # floating-point register file, and the destination is made to alias every source.
   # Aliased slots hold one and the same value, so the result does not depend on which
   # role won the load.  feq & co. write an integer register, so their rd is not varied
   # (x1 would clobber the return address).
   for op in ['fadd','fmul','fdiv','fsgnj','fmin','feq','fmadd']:
    group='fsgnj' if op.startswith('fsgnj') else op; name=op+'_'+fmt
    fma=op=='fmadd'; rm=0 if op in roundops else None
    for slot,regs in [('rs1',[0,1,15,31]),('rs2',[0,31])]+([] if op=='feq' else [('rd',[0,1,31])]):
     for r in regs:
      kw=dict(rd=24,rs1=18,rs2=20,rs3=22);kw[slot]=r
      if fma:add(group,name,fmt,vals['pnormal'],vals['twohalf'],vals['threehalf'],kind='fma',rm=0,**kw,tag='reg:%s=%d'%(slot,r))
      else:add(group,name,fmt,vals['pnormal'],vals['twohalf'],rm=rm,**kw,tag='reg:%s=%d'%(slot,r))
    pairs_alias=[('rs1','rs2')] if op=='feq' else [('rd','rs1'),('rd','rs2'),('rs1','rs2')]
    if fma:pairs_alias=[('rd','rs1'),('rd','rs2'),('rd','rs3'),('rs1','rs2'),('rs1','rs3'),('rs2','rs3')]
    for s1,s2 in pairs_alias:
     kw=dict(rd=24,rs1=18,rs2=20,rs3=22);kw[s2]=kw[s1]
     if fma:add(group,name,fmt,vals['pnormal'],vals['pnormal'],vals['pnormal'],kind='fma',rm=0,**kw,tag='overlap:%s=%s'%(s1,s2))
     else:add(group,name,fmt,vals['pnormal'],vals['pnormal'],rm=rm,**kw,tag='overlap:%s=%s'%(s1,s2))
  for op in ['fsqrt','fclass']+(['fround','froundnx'] if bank=='f' else []):
   for n,(rmfrm,kv) in enumerate(itertools.product(RMS if op!='fclass' else [(None,0)],allv)):
    (rm,frm),(k,a)=rmfrm,kv
    add(op,op+'_'+fmt,fmt,a,kind='unary',rm=rm,frm=frm,flags=8 if n%11==0 else 0,tag=k)
  for op in ['fmadd','fmsub','fnmsub','fnmadd']:
   triples=[(a,b,c,'class:'+ka+','+kb+','+kc) for (ka,a),(kb,b),(kc,c) in itertools.product(classes,repeat=3)]
   for n,(a,b,c,tag) in enumerate(triples):
    rm,frm=RMS[n%len(RMS)]
    add(op,op+'_'+fmt,fmt,a,b,c,kind='fma',rm=rm,frm=frm,tag=tag)
   for (rm,frm),(ka,kb,kc) in itertools.product(RMS,[('nzero','pnormal','nzero'),('pzero','pnormal','pzero'),('minnormal','threehalf','nminnormal'),('max','two','nmax')]):
    add(op,op+'_'+fmt,fmt,vals[ka],vals[kb],vals[kc],kind='fma',rm=rm,frm=frm,tag='boundary:'+ka+','+kb+','+kc)
   # One factor huge and the addend tiny (or vice versa): the small term is far off the grid.
   for (rm,frm),(ka,kb,kc) in itertools.product(RMS,[('max','two','psub'),('two','max','nmaxsub'),('max','psub','pnormal'),('minnormal','maxsub','nmax')]):
    add(op,op+'_'+fmt,fmt,vals[ka],vals[kb],vals[kc],kind='fma',rm=rm,frm=frm,tag='span:'+ka+','+kb+','+kc)
   for k in newkeys:
    for slot in range(3):
     tr=[vals['two'],vals['threehalf'],vals['pnormal']];tr[slot]=vals[k]
     add(op,op+'_'+fmt,fmt,*tr,kind='fma',rm=0,frm=0,tag='edge:'+k+',slot'+str(slot))
   # ACT4's FMA cross points: both multiplicands and the addend each take the whole
   # 28-value edge set against two fixed partners.
   for i,x in enumerate(act4 or ()):
    for j,y in enumerate(act4 or ()):
     rm,frm=RMS[(i*28+j)%len(RMS)]
     add(op,op+'_'+fmt,fmt,x,y,vals['threehalf'],kind='fma',rm=rm,frm=frm,tag='act4:%d,%d'%(i,j))
     add(op,op+'_'+fmt,fmt,x,vals['threehalf'],y,kind='fma',rm=0,frm=0,tag='act4:%d,threehalf,%d'%(i,j))
  # Tininess-after-rounding vectors from riscv-arch-test testplans/priv/ZicsrF
  # (cp_underflow_after_rounding). Tininess uses its own rounding with an unbounded
  # exponent, so underflow can be signalled by a result that rounds back to MIN_NORM.
  # Each operand set runs under all ten rounding configurations; depending on the mode
  # the exact value is tiny before but not after rounding, or tiny after rounding even
  # though the delivered result is +-MIN_NORM.
  ur={'h':[('fmadd',0x0BC7,0x03FF,0x8400),('fmul',0x0401,0x3BFE,None)],
      's':[('fmadd',0x3F00FBFF,0x80000001,0x807FFFFF),('fmul',0x00800001,0x3F7FFFFE,None)],
      'd':[('fmadd',0x802FFFFFFFBFFEFF,0x000FFFFFFFFFFFFE,0x0010000000000000),('fmul',0x0010000000000001,0xBFEFFFFFFFFFFFFE,None)],
      'q':[('fmadd',0x3F9800000000000001FFFFFFFF7FFFFE,0x00000000000000000000000000000001,0x80010000000000000000000000000000),
           ('fmul',0x0000FFFFFFFFFFFFFFFFFFFFFFFFFFFF,0x3FFF0000000000000000000000000001,None)]}
  for op,a,b,c in ur.get(fmt,[]):
   for rm,frm in RMS:
    if c is None:add('fmul','fmul_'+fmt,fmt,a,b,rm=rm,frm=frm,tag='underflow-after-rounding')
    else:add('fmadd','fmadd_'+fmt,fmt,a,b,c,kind='fma',rm=rm,frm=frm,tag='underflow-after-rounding')
  for typ in ['w','wu','l','lu']:
   for (rm,frm),(k,a) in itertools.product(RMS,allv):
    add('fcvt-to-int','fcvt_'+typ+'_'+fmt,fmt,a,kind='intout',rm=rm,frm=frm,tag=k)
   width=32 if typ.startswith('w') else 64
   # ACT4 get_general_edges(XLEN): signed extremes, walking patterns, Wmax/W7F/...
   intvalues=set(ACT4_INT[width])|{65519,65520,65535,65536,1<<24,(1<<24)+1}
   if width==64:intvalues|={(1<<53)-1,1<<53,(1<<53)+1}
   for (rm,frm),u in itertools.product(RMS,sorted(intvalues)):
    add('fcvt-from-int','fcvt_'+fmt+'_'+typ,fmt,u,kind='intin',rm=rm,frm=frm,tag='integer:'+str(u))
  if bank=='f':
   for imm in range(32):
    add('fli','fli_'+fmt,fmt,word=encoding('fli_'+fmt,rs1=imm,rs2=None),imm=imm)
   for op in ['fl','fs']:
    name=op+{'h':'h','s':'w','d':'d','q':'q'}[fmt]
    # load/store base register is t4 (x29); loads write f24, stores read f20.
    # The 12-bit immediate field is swept over ACT4 imm_12bit; write_assembly moves
    # the base register by -imm so the effective address stays scratch_memory.
    for imm in sorted(set([0]+list(ACT4_IMM12))):
     if imm==0:
      word=ENC[name]|(24<<7 if op=='fl' else 20<<20)|29<<15
     elif op=='fl':
      word=ENC[name]|(24<<7)|(29<<15)|((imm&0xfff)<<20)
     else:
      word=ENC[name]|(20<<20)|(29<<15)|((imm&0xfe0)<<20)|((imm&0x1f)<<7)
     for k,a in (allv if imm==0 else [('imm:%d'%imm,vals['pnormal'])]):
      add(name,name,fmt,a,a,kind='load' if op=='fl' else 'store',word=word,imm=imm,tag=k)
   if fmt in 'hs' or (fmt=='d' and xlen==64):
    suf={'h':'h','s':'w','d':'d'}[fmt]
    for k,a in allv:
     add('fmv-'+suf,'fmv_x_'+suf,fmt,a,kind='intout',tag=k)
     add('fmv-'+suf,'fmv_'+suf+'_x',fmt,a,kind='intin',tag=k)
   if (fmt=='d' and xlen==32) or (fmt=='q' and xlen==64):
    for k,a in allv:
     add('fmvh','fmvh_x_'+fmt,fmt,a,kind='intout',tag=k)
     add('fmvp','fmvp_'+fmt+'_x',fmt,a,a>>xlen,kind='pack',word=encoding('fmvp_'+fmt+'_x'),tag=k)
  # FS Off guards; boxing failure applies to every non-transfer narrow arithmetic op.
  for op in ['fadd','fsqrt','fclass','fcvt_w']:
   add('fcvt-to-int' if op=='fcvt_w' else op,op+'_'+fmt,fmt,vals['pnormal'],vals['pnormal'],kind='intout' if op=='fcvt_w' else ('unary' if op in ['fsqrt','fclass'] else 'fp'),rm=None if op=='fclass' else 0,fs=0,tag='FS-off') if bank=='f' else None
  if bank=='f' and w<flen:
   # Bad NaN-boxing: only some upper bits of a narrow operand are non-zero garbage.
   gap=((1<<flen)-1)^((1<<w)-1)
   garbage=[(gap>>1)&gap,(0xDEADBEEF_DEADBEEF&gap) or (1<<w),1<<w]
   def badup(box,i):return [garbage[(i+j)%3] if not box[j] else 0 for j in range(3)]
   for op,kind_,rm in [('fadd','fp',0),('fsgnj','fp',None),('feq','fp',None),('fclass','unary',None)]:
    for i,(name,box) in enumerate([('source',(False,True,True)),('second',(True,False,True)),('all',(False,False,False))]):
     if name=='second' and op=='fclass':continue
     add(op,op+'_'+fmt,fmt,vals['pnormal'],vals['two'],vals['threehalf'],kind=kind_,rm=rm,boxing=box,upper=badup(box,i),tag='bad-box:'+name)
   for op in ['fmadd','fmsub','fnmsub','fnmadd']:
    for i,(name,box) in enumerate([('source',(False,True,True)),('second',(True,False,True)),('third',(True,True,False)),('all',(False,False,False))]):
     add(op,op+'_'+fmt,fmt,vals['pnormal'],vals['two'],vals['threehalf'],kind='fma',rm=0,boxing=box,upper=badup(box,i),tag='bad-box:'+name)
   for dst in p['formats']:
    if FMT[dst][0]>w:
     add('fcvt-fp-fp','fcvt_'+dst+'_'+fmt,dst,vals['pnormal'],src=fmt,kind='convert',rm=0,boxing=(False,True,True),upper=badup((False,True,True),0),tag='bad-box:source')
   for typ in ['w','wu']:
    add('fcvt-to-int','fcvt_'+typ+'_'+fmt,fmt,vals['pnormal'],kind='intout',rm=0,boxing=(False,True,True),upper=badup((False,True,True),0),tag='bad-box:source')
   imgs=ACT4_BOX.get((flen,w))
   if imgs:
    # ACT4 bad_NaN_* images: one source broken at a time, its low bits spanning zero,
    # normal, infinity and NaN patterns, the remaining sources correctly boxed.  The
    # arithmetic, comparison, min/max, sign-injection, sqrt, FMA and conversion
    # families all sit behind the same bad-boxing rule.
    mask=(1<<w)-1
    for op in ['fadd','fsub','fmul','fdiv','fmin','fmax','fminm','fmaxm','fsgnj','fsgnjn','fsgnjx','feq','flt','fle','fleq','fltq']:
     group='fsgnj' if op.startswith('fsgnj') else op
     rm=0 if op in ['fadd','fsub','fmul','fdiv'] else None
     for n,img in enumerate(imgs):
      for slot in (0,1):
       box=[True,True,True];box[slot]=False
       up=[0,0,0];up[slot]=img&gap
       a,b=(img&mask,vals['threehalf']) if slot==0 else (vals['threehalf'],img&mask)
       add(group,op+'_'+fmt,fmt,a,b,rm=rm,boxing=box,upper=up,tag='act4-bad-box:%d:%d'%(n,slot))
    for op in ['fsqrt','fclass','fround','froundnx']:
     for n,img in enumerate(imgs):
      add(op,op+'_'+fmt,fmt,img&mask,kind='unary',boxing=(False,True,True),upper=[img&gap,0,0],tag='act4-bad-box:%d'%n)
    for op in ['fmadd','fmsub','fnmsub','fnmadd']:
     for n,img in enumerate(imgs):
      for slot in range(3):
       box=[True,True,True];box[slot]=False
       up=[0,0,0];up[slot]=img&gap
       tr=[vals['pnormal'],vals['two'],vals['threehalf']];tr[slot]=img&mask
       add(op,op+'_'+fmt,fmt,*tr,kind='fma',rm=0,boxing=box,upper=up,tag='act4-bad-box:%d:%d'%(n,slot))
    for typ in ['w','wu','l','lu']:
     for n,img in enumerate(imgs):
      add('fcvt-to-int','fcvt_'+typ+'_'+fmt,fmt,img&mask,kind='intout',rm=0,boxing=(False,True,True),upper=[img&gap,0,0],tag='act4-bad-box:%d'%n)
    for dst in p['formats']:
     if FMT[dst][0]>w:
      for n,img in enumerate(imgs):
       add('fcvt-fp-fp','fcvt_'+dst+'_'+fmt,dst,img&mask,src=fmt,kind='convert',rm=0,boxing=(False,True,True),upper=[img&gap,0,0],tag='act4-bad-box:%d'%n)
 # FP-to-FP conversions: full pair sets, Q profile includes cross-Q cases.
 fmts='hsdq' if flen==128 else 'hsd'
 for dst,src in itertools.permutations(fmts,2):
  if p['formats']=='q' and 'q' not in [dst,src]:continue
  if 'min' in profile and 'h' not in [dst,src]:continue
  for (rm,frm),(k,a) in itertools.product(RMS,patterns(src).items()):
   add('fcvt-fp-fp','fcvt_'+dst+'_'+src,dst,a,src=src,kind='convert',rm=rm,frm=frm,tag=k)
 # Tininess-after-rounding conversion vectors from the same testplan, all rounding configurations.
 if flen==128:
  for rm,frm in RMS:add('fcvt-fp-fp','fcvt_s_q','s',0x3F80FFFFFFFE0000000000FFFFFFFFFF,src='q',kind='convert',rm=rm,frm=frm,tag='underflow-after-rounding')
 if 'd' in p['formats'] and not p['formats']=='q':
  for rm,frm in RMS:add('fcvt-fp-fp','fcvt_s_d','s',0xB80FFFFFFFFDFEFF,src='d',kind='convert',rm=rm,frm=frm,tag='underflow-after-rounding')
 if 's' in p['formats'] and 'h' in p['formats']:
  for rm,frm in RMS:add('fcvt-fp-fp','fcvt_h_s','h',0x387FF000,src='s',kind='convert',rm=rm,frm=frm,tag='underflow-after-rounding')
 # directed tiny boundary and WU sign extension inputs.
 if flen!=128 and 'd' in p['ext'] or bank=='x' and 'zdinx' in p['ext']:
  add('fcvt-fp-fp','fcvt_s_d','s',0x380fffffe8000000,src='d',kind='convert',rm=0,tag='tiny-rounds-normal')
  # Exact result just above 2^Emin, delivered as a subnormal by a directed mode: not tiny, NX only.
  add('fcvt-fp-fp','fcvt_s_d','s',0x3810000000000001,src='d',kind='convert',rm=2,tag='subnormal-not-tiny')
  add('fcvt-fp-fp','fcvt_s_d','s',0x3810000000000001,src='d',kind='convert',rm=1,tag='subnormal-not-tiny')
  add('fcvt-to-int','fcvt_wu_s','s',0x4f000000,kind='intout',rm=0,tag='WU-bit31')
 if bank=='f' and 'q' not in p['formats']:
  for dst,src in [('bf16','s'),('s','bf16')]:
   for (rm,frm),(k,a) in itertools.product(RMS,patterns(src).items()):
    add('bf16','fcvt_'+dst+'_'+src,dst,a,src=src,kind='convert',rm=rm,frm=frm,tag=k)
  for k,a in patterns('d').items():
   add('fcvttmod','fcvtmod_w_d','d',a,kind='intout',tag=k)
 # CSR pseudo-instructions, encoded as CSRRS/CSRRW targeting x24.  ACT4 ZicsrF
 # enumerates every legal frm (0-7) and the whole fflags field (0-31) on write, and
 # walks a single one through each CSR.
 csr_writes={'frcsr':[0],'frrm':[0],'frflags':[0],
             'fscsr':list(range(256))+[1<<b for b in range(8)],
             'fsrm':list(range(8)),'fsflags':list(range(32))+[1<<b for b in range(5)]}
 for name,csr,funct in [('frcsr',3,2),('fscsr',3,1),('frrm',2,2),('fsrm',2,1),('frflags',1,2),('fsflags',1,1)]:
  for initial,u in itertools.product([0,1,0x1f,0x80,0xff],csr_writes[name]):
   add('fcsr',name,'s',u,kind='csr',frm=initial>>5,flags=initial&31,word=(csr<<20)|(18<<15 if funct==1 else 0)|(funct<<12)|(24<<7)|0x73,tag='csr')
 out=ROOT/'generated'/profile;out.mkdir(parents=True,exist_ok=True)
 (out/'cases.json').write_text(json.dumps(cases,indent=2)+'\n')
 write_assembly(out,cases,p)
 return dict(**p,cases=len(cases),groups=sorted(set(c['group'] for c in cases)))

def write_assembly(out,cases,p):
 xlen=p['xlen'];bank=p['bank'];flen=p.get('flen',64)
 loadx='ld' if xlen==64 else 'lw'; storex='sd' if xlen==64 else 'sw'
 fload='fld' if flen==64 else '.word '+hex(ENC['flq']|(18<<7)|(29<<15))
 def frload(reg,offset):
  return f'fld f{reg},{offset}(t4)' if flen==64 else f'.word {hex(ENC["flq"]|(reg<<7)|(29<<15)|(offset<<20))}'
 def frstore(reg):return f'fsd f{reg},0(s1)' if flen==64 else '.word '+hex(ENC['fsq']|(reg<<20)|(9<<15))
 prefix='''# Generated by generate.py; edit the generator, not this file.
.section .text.init,"ax"
.option norvc
.globl _start
_start:
 la t0,trap_handler
 csrw mtvec,t0
 csrw mie,zero
 csrw satp,zero
 csrw medeleg,zero
 la s1,begin_signature
'''
 if bank=='f': prefix+=' li t0,0x6000\n csrs mstatus,t0\n'
 groups={}
 data=['.section .rodata,"a"','.balign 16']
 for case in cases:
  n=case['id'];fmt=case['fmt'];src=case['src'];kind=case['kind'];w=FMT[src][0]
  drd,drs1,drs2,drs3=case.get('regs') or [24,18,20,22]
  # Load the operand slots in reverse priority so that when the destination aliases
  # a source, the source value is the one left in the register.
  slots=[(drd,48),(drs3,32),(drs2,16),(drs1,0)]
  lines=[f'# {n}: {case["op"]} {case["tag"]}; {case["doc"]}',f' la t4,operand_{n}']
  if bank=='f':
   lines += [' li t3,0x6000',' csrs mstatus,t3']
   for reg,off in slots:lines.append(' '+frload(reg,off))
  # Integer operands for integer-source instructions and x-register FP forms.
  if bank=='x' or kind in ['intin','pack','csr']:
   for reg,off in slots:
    lines.append(f' {loadx} x{reg},{off}(t4)')
    if bank=='x' and xlen==32 and (src=='d' or fmt=='d'):
     lines.append(f' lw x{reg+1},{off+4}(t4)')
  # Reset writable scratch memory for loads/stores and output capture.
  if kind in ['load','store']:
   lines += [' la t4,scratch_memory']
   a=int(case['a'],16)
   for off in range(0,16,4):lines += [f' li t3,0x{(a>>(off*8))&0xffffffff:x}',f' sw t3,{off}(t4)']
   # A non-zero load/store immediate is absorbed into the base register, so the
   # effective address stays scratch_memory and the signature layout is unchanged.
   imm=case.get('imm',0)
   if imm:lines.append(f' la t4,scratch_memory+{-imm}')
  lines += [f' li t3,{case["frm"]*32+case["flags"]}',' csrw fcsr,t3']
  if bank=='f':lines+=[' li t3,0x6000',' csrc mstatus,t3',f' li t3,{case["fs"]<<13}',' csrs mstatus,t3']
  lines += [' li s11,0',' li s10,0',f'.globl target_{n}',f'target_{n}:',f' .word 0x{case["word"]:08x}',
            ' csrr t3,mstatus',' srli t3,t3,13',' andi t3,t3,3',' sw t3,20(s1)',
            ' sw s11,24(s1)',f' li t3,{n}',' sw t3,28(s1)',f' {storex} s10,48(s1)']
  if bank=='f':lines += [' li t3,0x6000',' csrs mstatus,t3']
  lines += [' csrr t3,fcsr',' sw t3,16(s1)']
  intdest=kind in ['intout','csr'] or case['op'].split('_')[0] in ['feq','flt','fle','fleq','fltq','fclass']
  if bank=='x' or intdest:
   lines.append(f' {storex} x{drd},0(s1)')
   if bank=='x' and xlen==32 and fmt=='d' and not intdest:lines.append(f' sw x{drd+1},4(s1)')
  else: lines.append(' '+frstore(drd))
  lines+=[' la t4,scratch_memory']
  for off in range(0,16,4):lines += [f' lw t3,{off}(t4)',f' sw t3,{off+32}(s1)']
  lines+=[' csrr t3,misa',f' {storex} t3,56(s1)',' addi s1,s1,64']
  groups.setdefault(case['group'],[]).extend(lines)
  def image(key,fmt):
   i={'a':0,'b':1,'c':2}[key]
   u=int(case[key],16);w=FMT[fmt][0]
   if bank=='f' and kind not in ['intin','pack','csr']:
    gap=((1<<flen)-1)^((1<<w)-1)
    u |= gap if case['boxing'][i] else (int(case['upper'][i],16)&gap)
   return u&((1<<128)-1)
  data += [f'operand_{n}:']
  for key in ['a','b','c']:
   u=image(key,src if key=='a' else fmt)
   data += [f' .dword 0x{u&((1<<64)-1):016x},0x{u>>64:016x}']
  data+=[' .dword 0x1122334455667788,0x99aabbccddeeff00']
 # Files are included into one translation unit in the same order as cases.
 # Cases are grouped by the generator but conversion/guard additions revisit groups.
 # Emit assembly in exact case order using cached per-case slices instead below.
 all_lines=[]
 # groups above may interleave IDs: reconstruct chunks keyed by their comment ID.
 chunks={}
 for lines in groups.values():
  starts=[i for i,s in enumerate(lines) if s.startswith('# ')]
  for i,start in enumerate(starts):chunks[int(lines[start].split(':')[0][2:])]=lines[start:starts[i+1] if i+1<len(starts) else len(lines)]
 # Per-group files are real subroutines, called in group order. Signature IDs remain explicit.
 ordered=[]
 for group in groups:
  gcases=[c for c in cases if c['group']==group]
  text=['.section .text,"ax"',f'group_{group.replace("-","_")}:']
  for c in gcases: text+=chunks[c['id']];ordered.append(c['id'])
  text+=[' ret']
  (out/(group+'.S')).write_text('\n'.join(text)+'\n')
  prefix+=f' call group_{group.replace("-","_")}\n'
 # The signature output is in group-call order; preserve manifest mapping.
 (out/'order.json').write_text(json.dumps(ordered)+'\n')
 prefix+=' la t0,tohost\n li t1,1\n'+(' sd t1,0(t0)\n' if xlen==64 else ' sw t1,0(t0)\n sw zero,4(t0)\n')+'''done:
 j done
.balign 4
trap_handler:
 csrr s11,mcause
 csrr s10,mepc
 addi t6,s10,4
 csrw mepc,t6
 mret
'''
 for group in groups:prefix+=f'#include "{group}.S"\n'
 prefix+='\n'.join(data)+'\n'+'''.section .data,"aw"
.balign 16
scratch_memory: .zero 16
.section .tohost,"aw"
.balign 64
.globl tohost,fromhost
tohost: .dword 0
fromhost: .dword 0
.section .signature,"aw"
.balign 64
.globl begin_signature,end_signature
begin_signature:
'''+f' .zero {len(cases)*64}\nend_signature:\n'
 (out/'suite.S').write_text(prefix)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--profiles',nargs='*',default=list(PROFILES));ap.add_argument('--random',type=int,default=16);args=ap.parse_args()
 inv=[];dig=hashlib.sha256()
 for f in [DOC/'README.md',*sorted((DOC/'instructions').glob('*.md'))]:
  text=f.read_text();dig.update(str(f.relative_to(DOC)).encode()+b'\0'+f.read_bytes()+b'\0')
  for label in re.findall(r'^\*\*\(([^)]+)\)',text,re.M):inv.append(dict(file=str(f.relative_to(DOC)),formula=label))
 (ROOT/'generated'/'formula-inventory.json').write_text(json.dumps(dict(source_sha256=dig.hexdigest(),formulas=inv),indent=2)+'\n')
 profiles={name:generate(name,args) for name in args.profiles}
 (ROOT/'generated'/'profiles.json').write_text(json.dumps(profiles,indent=2)+'\n')
 print(json.dumps({k:v['cases'] for k,v in profiles.items()},indent=2))
if __name__=='__main__':main()
