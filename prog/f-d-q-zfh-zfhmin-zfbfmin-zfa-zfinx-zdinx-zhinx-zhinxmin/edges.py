#!/usr/bin/env python3
"""Generate directed x0/register-pair and ignored-upper-bit cases."""
import json
from generate import ROOT,write_assembly,encoding,patterns

def main():
 path=ROOT/'generated/profiles.json';profs=json.loads(path.read_text())
 for xl in [32,64]:
  name=f'rv{xl}-x-edges';base=dict(xlen=xl,bank='x',formats='hsd',ext=['zfinx','zdinx','zhinx','zhinxmin']);cases=[]
  def add(fmt,a,b,rs1=18,rs2=20,rd=24,tag=''):
   c=dict(id=len(cases),group='zfinx',op='fadd_'+fmt,fmt=fmt,src=fmt,a=hex(a),b=hex(b),c='0x0',kind='fp',rm=0,frm=0,flags=0,fs=0,tag=tag,boxing=True,doc='instructions/zfinx.md',word=encoding('fadd_'+fmt,rd=rd,rs1=rs1,rs2=rs2,rm=0))
   if rd==0:c['observe_unchanged_dest']=True
   cases.append(c)
  v=patterns('d')
  add('d',0,v['pnormal'],rs1=0,tag='double-source-x0-ignore-x1')
  add('d',v['pnormal'],0,rs2=0,tag='double-source-x0-ignore-x1-rs2')
  add('d',v['pnormal'],v['two'],rd=0,tag='double-dest-x0-discard-x1-preserve-return')
  add('d',0,v['pnormal'],rs1=0,rd=0,tag='double-x0-source-and-dest')
  for fmt in ['h','s']:
   v=patterns(fmt);w={'h':16,'s':32}[fmt]
   for top in [0,0x12345678,0xffffffff]:add(fmt,v['pnormal']|(top<<w),v['two']|(top<<w),tag='ignore-upper-source-bits')
  out=ROOT/'generated'/name;out.mkdir(exist_ok=True);(out/'cases.json').write_text(json.dumps(cases,indent=2)+'\n');write_assembly(out,cases,base)
  profs[name]=dict(**base,cases=len(cases),groups=['zfinx'])
 path.write_text(json.dumps(profs,indent=2)+'\n')
if __name__=='__main__':main()
