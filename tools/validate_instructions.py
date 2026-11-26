#!/usr/bin/env python3
"""Validate the scalar instruction build, source provenance, and coverage."""
from pathlib import Path
import json, re, subprocess, sys, hashlib
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'reports/scalar-fp-manifest.json').read_text())
errors=[];checks=[];total=0
for name,digest in manifest.get('input_hashes',{}).items():
 if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:errors.append((name,'source input hash mismatch'))
for doc in manifest['documents']:
 path=ROOT/doc['document'];text=path.read_text()
 if hashlib.sha256(text.encode()).hexdigest()!=doc['sha256']:errors.append((doc['document'],'generated file changed after build'))
 for tool in ['check_md.py','check_style.py']:
  run=subprocess.run([sys.executable,'-I',str(ROOT/'tools'/tool),str(path)],text=True,capture_output=True)
  if run.returncode:errors.append((doc['document'],tool,run.stdout+run.stderr))
 labels=re.findall(r'^\*\*\(([^\n]+?)\)',text,re.M)
 if len(labels)!=doc['formula_count']:errors.append((doc['document'],'formula count'))
 if len(labels)!=len(set(labels)):errors.append((doc['document'],'duplicate labels'))
 if re.findall(r'^## (\d+)\.',text,re.M)!=list(map(str,range(1,9))):errors.append((doc['document'],'section skeleton'))
 if re.search('[\u4e00-\u9fff]',text):errors.append((doc['document'],'English-only output'))
 for forbidden in [r'\mathrm{Finite}(',r'\mathrm{NaN}(',r'\mathrm{sNaN}(',r'\mathrm{qNaN}(',r'\mathrm{Zero}(',r'\mathrm{Normal}(',r'\mathrm{Subnormal}(',r'\mathrm{Inf}(',r'\mathrm{enabled}',r'\mathrm{Stateen}',r'\mathrm{exc}=']:
  if forbidden in text:errors.append((doc['document'],'hidden or obsolete notation',forbidden))
 for body in re.findall(r'\\begin\{aligned\}\n(.*?)\\end\{aligned\}',text,re.S):
  if r'\longrightarrow' not in text:continue
  rows=body.splitlines()
  for row in rows[:-1]:
   if not row.endswith('\\\\') or row.endswith('\\\\\\'):
    errors.append((doc['document'],'LaTeX row terminator',row[-50:]))
 for r in doc['sources']:
  lines=(ROOT/'sources'/f'riscv-{r["volume"]}.txt').read_text().split('\n')
  if '\n'.join(lines[r['first']-1:r['last']])!=r['quote']:errors.append((doc['document'],'source excerpt changed',r['first']))
  actual=sorted({1+'\n'.join(lines[:n]).count('\f') for n in [r['first'],r['last']]})
  if actual[0]!=r['pages'][0] or actual[-1]!=r['pages'][-1]:errors.append((doc['document'],'source PDF pagination',r['first']))
 checks.append({'document':doc['document'],'formulas':doc['formula_count'],'sha256':doc['sha256']})
 total+=doc['formula_count']

actual={str(p.relative_to(ROOT)) for p in (ROOT/manifest['documents'][0]['document']).parent.glob('*.md') if p.name!='README.md'}
expected_files={d['document'] for d in manifest['documents']}
if actual!=expected_files:errors.append(('coverage','orphan or missing documents',sorted(actual^expected_files)))

# Independent inventory reconstructed from Unprivileged chapters 21–27.
# 18 computational/comparison families + 8 integer conversions per format;
# transfers, format conversions and Zfa additions are enumerated separately.
base=['FADD','FSUB','FMUL','FDIV','FSQRT','FMADD','FMSUB','FNMSUB','FNMADD','FMIN','FMAX','FSGNJ','FSGNJN','FSGNJX','FEQ','FLT','FLE','FCLASS']
expected={f'{op}.{f}' for op in base for f in 'HSDQ'}
for f in 'HSDQ':
 for t in ['W','WU','L','LU']:expected.update([f'FCVT.{t}.{f}',f'FCVT.{f}.{t}'])
for f in 'HSDQ':
 for g in 'HSDQ':
  if f!=g:expected.add(f'FCVT.{f}.{g}')
for f,label in [('H','H'),('S','W'),('D','D'),('Q','Q')]:
 expected.update(['FL'+label,'FS'+label])
 if f!='Q':expected.update([f'FMV.X.{label}',f'FMV.{label}.X'])
for f in 'HSDQ':
 for op in ['FLI','FMINM','FMAXM','FROUND','FROUNDNX','FLEQ','FLTQ']:expected.add(f'{op}.{f}')
expected.update(['FCVTMOD.W.D','FMVH.X.D','FMVH.X.Q','FMVP.D.X','FMVP.Q.X','FCVT.BF16.S','FCVT.S.BF16'])
assert len(expected)==165
csr={'FRCSR','FSCSR','FRRM','FSRM','FRFLAGS','FSFLAGS','CSRRW','CSRRS','CSRRC','CSRRWI','CSRRSI','CSRRCI'}
floating={v['instruction'] for d in manifest['documents'] if not d['xregs'] for v in d['variants']}
xregs={v['instruction'] for d in manifest['documents'] if d['xregs'] for v in d['variants']}
if floating!=expected|csr:errors.append(('coverage','scalar inventory mismatch',sorted(floating^(expected|csr))))
expectedx={f'{op}.{f}' for op in base for f in 'HSD'}
for f in 'HSD':
 for t in ['W','WU','L','LU']:expectedx.update([f'FCVT.{t}.{f}',f'FCVT.{f}.{t}'])
for f in 'HSD':
 for g in 'HSD':
  if f!=g:expectedx.add(f'FCVT.{f}.{g}')
assert len(expectedx)==84
if xregs!=expectedx|csr:errors.append(('coverage','x-register inventory mismatch',sorted(xregs^(expectedx|csr))))
for ins in xregs:
 if '.Q' in ins or 'BF16' in ins or ins.startswith(('FLI.','FROUND','FMINM','FMAXM','FLEQ','FLTQ','FMV','FLH','FLW','FLD','FSH','FSW','FSD')):
  errors.append(('coverage','unsupported x-register variant',ins))
for d in manifest['documents']:
 text=(ROOT/d['document']).read_text()
 if d['xregs']:
  if r'\mathrm{DirtyFS}' in text:errors.append((d['document'],'x-register form updates FS'))
 else:
  if 'mstateen0.FCSR' not in text or 'hstateen0.FCSR' not in text or 'sstateen0.FCSR' not in text:errors.append((d['document'],'missing state-enable level'))
 for v in d['variants']:
  if v['instruction'].startswith('FCVTMOD') and v['rounding_field']:errors.append((d['document'],'modular conversion wrongly accepts dynamic rm'))
report={'documents':len(checks),'formulas':total,'unique_floating_instructions':len(floating),'unique_x_instructions':len(xregs),'issues':errors,'files':checks}
(ROOT/'reports/scalar-fp-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(f"Validated {len(checks)} documents and {total} formulas: {len(errors)} issues")
for e in errors[:15]:print(e)
sys.exit(bool(errors))
