"""Audit result-formula blocks.

A result formula is an `aligned` block that contains `\\mathrm{instr}`.
It must:
  - start with the full CSR config (`&(mstatus.FS...`);
  - end with the instruction conjunct (`\\mathrm{instr}`);
  - have at most one top-level `\\land` per line.

Blocks without `\\mathrm{instr}` are definitions or standalone config
blocks (`enabled(I)` definition, FMV/load/store preambles, Zfinx
substitution table) and are skipped.

Usage: python3 -I audit_formulas.py <file.md>
Exit code 0 if no issue, 1 otherwise.
"""
import re
import sys

lines = open(sys.argv[1], encoding='utf-8').read().split('\n')
issues = []
blocks = 0
i = 0
while i < len(lines):
    if lines[i].strip() != r'\begin{aligned}':
        i += 1
        continue
    j = i + 1
    while j < len(lines) and not lines[j].strip().startswith(r'\end{aligned}'):
        j += 1
    if j >= len(lines) or lines[j].strip() != r'\end{aligned}':
        i = j + 1
        continue
    start = i
    block = lines[start + 1:j]
    i = j + 1
    if not any(r'\mathrm{instr}' in l for l in block):
        continue
    blocks += 1
    if not block[0].startswith('&(mstatus.FS'):
        issues.append((start + 2, 'first line', block[0]))
    if r'\mathrm{instr}' not in block[-1]:
        issues.append((j, 'instr not last', block[-1]))
    for k, l in enumerate(block):
        s = l.strip()
        if s.startswith('&'):
            s = s[1:]
        if s.endswith('\\\\'):
            s = s[:-2]
        cnt = 0
        for m in re.finditer(r'\\land(?![a-zA-Z])', s):
            pre = s[:m.start()]
            d = (pre.count('(') + pre.count('[') + pre.count('{')
                 - pre.count(')') - pre.count(']') - pre.count('}'))
            if d == 0:
                cnt += 1
        if cnt > 1:
            issues.append((start + 2 + k, 'multi top-level land', l[:80]))

print('formula blocks:', blocks)
for b in issues:
    print(b)
sys.exit(0 if not issues else 1)
