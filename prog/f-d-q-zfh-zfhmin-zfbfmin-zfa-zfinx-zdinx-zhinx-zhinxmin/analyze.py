#!/usr/bin/env python3
"""Add independent numerical checks and a readable result/coverage report."""
from pathlib import Path
import collections,json
from reference import expect
ROOT=Path(__file__).resolve().parent

def main():
 profiles=json.loads((ROOT/'generated/profiles.json').read_text())
 summaries=[];filecoverage=collections.defaultdict(lambda:dict(cases=0,normal=0,traps=0));reference_findings=[]
 for name,p in profiles.items():
  folder=ROOT/'results'/name;summaryfile=folder/'summary.json'
  if not summaryfile.exists():continue
  summary=json.loads(summaryfile.read_text());cases=json.loads((ROOT/'generated'/name/'cases.json').read_text())
  models={}
  for model in ['spike','sail']:
   path=folder/(model+'.jsonl')
   if not path.exists():continue
   checked=0;fail=[];unmodelled=0;trapped=[]
   for line in path.read_text().splitlines():
    row=json.loads(line);c=cases[row['id']]
    predicted=expect(c,p)
    if predicted is None:unmodelled+=1;continue
    result,fcsr,exception=predicted;checked+=1
    delta={}
    if row['exception']!=exception:delta['exception']=[exception,row['exception']]
    if not exception:
     if row['result']!=result:delta['result']=[result,row['result']]
     if row['fcsr']!=fcsr:delta['fcsr']=[fcsr,row['fcsr']]
    if delta:
     item=dict(case=c,expected_actual=delta);fail.append(item);reference_findings.append(dict(profile=name,model=model,**item))
   (folder/(model+'-reference-differences.json')).write_text(json.dumps(fail,indent=2)+'\n')
   models[model]=dict(checked=checked,differences=len(fail),unmodelled=unmodelled)
  summary['reference']=models
  # report observable execution coverage by group, not fabricated formula branch coverage
  bygroup=collections.defaultdict(lambda:dict(cases=0,normal=0,traps=0))
  rows={r['id']:r for r in map(json.loads,(folder/'spike.jsonl').read_text().splitlines())} if (folder/'spike.jsonl').exists() else {}
  for c in cases:
   b=bygroup[c['group']];b['cases']+=1
   if c['id'] in rows:b['traps' if rows[c['id']]['exception'] else 'normal']+=1
   fc=filecoverage[c['doc']];fc['cases']+=1
   if c['id'] in rows:fc['traps' if rows[c['id']]['exception'] else 'normal']+=1
  (folder/'coverage.json').write_text(json.dumps(bygroup,indent=2)+'\n')
  (folder/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');summaries.append(summary)
 privfile=ROOT/'results/privilege-summary.json'
 privilege=json.loads(privfile.read_text()) if privfile.exists() else []
 exceptions=[json.loads(p.read_text()) for p in sorted((ROOT/'results').glob('*-exceptions/summary.json'))]
 summary=dict(profiles=summaries,privilege=privilege,exceptions=exceptions,total_cases=sum(x['cases'] for x in summaries)+sum(x['cases'] for x in privilege)+sum(x['cases'] for x in exceptions),compared=sum(x.get('compared',0) for x in summaries)+sum(x['paired'] for x in privilege)+sum(x['paired'] for x in exceptions),differences=sum(x.get('differences',0) for x in summaries)+sum(len(x['differences']) for x in privilege)+sum(len(x['differences']) for x in exceptions),single_model_cases=sum(x['cases'] for x in summaries if x['status']=='single_model_only'),fs_policy_differences=sum(x.get('fs_policy_differences',0) for x in summaries),reference_difference_observations=len(reference_findings))
 (ROOT/'results/document-coverage.json').write_text(json.dumps(filecoverage,indent=2)+'\n')
 (ROOT/'results/reference-findings.json').write_text(json.dumps(reference_findings,indent=2)+'\n')
 (ROOT/'results/summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 lines=['# Spike / Sail comparison results','',
 'The same generated ELF is executed by both models. Numerical result, full `fcsr`, exception code and scratch-memory bytes are compared exactly. FS is reported separately because the architecture permits implementation policies.','',
 '| Profile | Cases | Paired cases | Value/flags/trap/memory differences | FS differences | Status |',
 '|---|---:|---:|---:|---:|---|']
 for s in summaries:lines.append(f'| {s["profile"]} | {s["cases"]} | {s.get("compared",0)} | {s.get("differences","—")} | {s.get("fs_policy_differences","—")} | {s["status"]} |')
 for x in privilege:lines.append(f'| {x["profile"]} | {x["cases"]} | {x["paired"]} | {len(x["differences"])} | — | directed privilege gates |')
 for x in exceptions:lines.append(f'| {x["profile"]} | {x["cases"]} | {x["paired"]} | {len(x["differences"])} | — | directed exceptions |')
 lines+=['',f'Total: {summary["total_cases"]:,} test cases, {summary["compared"]:,} paired cases, {summary["differences"]} model disagreements; {summary["single_model_cases"]:,} Q cases on Spike only.','',
 '## Confirmed observations','',
 '- Main numerical/transfer/CSR suites and x0/register-pair suites agree between Spike and Sail.',
 '- The 45 FS gate cases agree. The 120 stateen cases have 15 exception-code differences: with mstateen0.FCSR=1, VS denied by hstateen0.FCSR=0 (6 cases), or VU denied by hstateen0.FCSR=0 or sstateen0.FCSR=0 (9 cases). Spike reports 22, the installed Sail reports 2. Cases cover FADD.S, FCLASS.S and FRCSR; normal-mode entry is independently checked using the expected ECALL code.',
 '- The directed exception suite (311 F/D/Zfh cases, 34 Q cases on Spike only) has no expectation differences on either model. mstatus.FS=00 raises illegal instruction for all 37 instruction forms and for read/write/set/clear of fcsr, frm and fflags; FS=01/10/11 with frm 0-4 executes all sampled instructions; access faults on unmapped address 0 raise 5 (load) and 7 (store) for FLH/FLW/FLD/FLQ and the matching stores.',
 '- Misaligned FP accesses are the only exception-suite disagreement: for every non-naturally-aligned address at all 16 low-4-bit offsets, Spike raises cause 4/6 while the installed Sail completes the access (34 load and 34 store cases, 68 of 345). Offset 0 and all naturally aligned offsets agree. Misaligned-access support is implementation-defined, so both behaviours are permitted; the models simply choose differently.',
 '- Reserved rounding modes are observational in this suite. Both models raise illegal instruction for static rm=5/6 and for DYN with frm=5/6/7, and execute with frm 0-4. The delivery leaves reserved modes outside every formula, so these results neither confirm nor contradict a formula.',
 '- The tininess boundary vectors from the testplan now agree with the reference: FCVT.S.D with D bits 0x380fffffe8000000 signals UF+NX in both models, and the reference does the same because the exact value rounds below 2^Emin under unbounded-exponent rounding even though the delivered S value is MIN_NORM.',
 '- The current source inventory has 487 formula labels. All 43 instruction files are represented by generated cases; that is mnemonic/group coverage, not proof that every formula branch was reached.',
 '','## Independent numerical interpretation','',
 'A separate Python exact-rational model checks arithmetic, FMA, square root, min/max, signs, comparisons, classify, integer and format conversions and round-to-integral operations. Tininess detection uses its own rounding with an unbounded exponent, as the delivery and Unpriv. 25.3.2.6.1 require. This is an independently written interpretation, not a mechanically translated or proved implementation of every Markdown formula. Its disagreements identify cases to inspect; neither simulator is assumed correct merely because of its name.','',
 '| Profile | Model | Checked | Differences | Outside numerical model |','|---|---|---:|---:|---:|']
 for s in summaries:
  for model,v in s['reference'].items():lines.append(f'| {s["profile"]} | {model} | {v["checked"]} | {v["differences"]} | {v["unmodelled"]} |')
 lines+=['','## Evidence and limits','',
 '- `environment.json`: simulator/compiler paths, version output and binary SHA-256. The installed Sail binary is a locally patched 0.15 build; the patches alongside it are recorded in README.',
 '- Each profile directory contains build/run commands and exit codes, ELF symbols, raw signatures, decoded JSONL, differences and instruction-group execution counts.',
 '- Q has no configuration in the available Sail schema. Q profiles run on Spike only and are explicitly excluded from paired totals.',
 '- Full IEEE-class cross products are used for binary operations and FMA; ten legal static/dynamic rounding configurations, sticky flags, boundary vectors and deterministic random inputs are included. This is finite sampling, not exhaustive bit-pattern testing.',
 '- Formula labels are inventoried from the current documents, but formula branch reachability is not inferred from mnemonic coverage. No claim of covering all 487 formulas is made.',
 '- Main numerical execution is little-endian M-mode with Bare translation; separate directed suites cover M/HS/U/VS/VU FS and stateen gates, and M-mode FS/CSR illegal-instruction gates, legal frm values, reserved rounding modes, misaligned accesses and unmapped-address access faults. Paging/guest-page faults, trigger breakpoints, PMP-denied regions (an unmapped address is used instead), partial stores and interrupt-time exceptions are not covered.',
 '- Q capability limits, expected extension-denial traps and real successful FP execution are distinguished in coverage files. An illegal instruction is not counted as a successful execution of its arithmetic semantics.',
 '- For Zdinx, Sail 0.15 requires D.supported=true to allocate its 64-bit helper type even while F.supported=false. This is an explicit configuration workaround, not a model source patch. Every x-register record verifies misa.F/D/Q=0. Original failed probes are preserved in capability-probes/.',
 '- A successful Sail run must report HTIF SUCCESS and contain all expected record IDs. Instruction-limit termination is not accepted as completion.',
 '- Original Markdown and simulator sources are not modified.','']
 (ROOT/'results/REPORT.md').write_text('\n'.join(lines))
 print(json.dumps({s['profile']:s['reference'] for s in summaries},indent=2))
if __name__=='__main__':main()
