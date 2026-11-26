"""Check result-formula style, independent of instruction domain.

A result formula is an `aligned` block that contains `\\mathrm{instr}`.
Each such block must:
  - use `\\begin{aligned}` ... `\\end{aligned}` (no bare multi-line math);
  - have every left-hand line start with `&`;
  - end the left side with a conjunct containing `\\mathrm{instr}`;
  - have at most one top-level `\\land` per line;
  - separate the two sides with `\\longrightarrow`;
  - write the right side as `\\{\\, ... \\,\\}`;
  - list `\\mathrm{exception}=` as the last right-hand field;
  - set known sticky flags with `\\mathrel{|}=`, never `=`;
  - avoid `\\wedge`/`\\vee` and hardware bit-pattern literals.

Blocks without `\\mathrm{instr}` are definitions or standalone value
blocks and are skipped.

Usage: python3 -I check_style.py <file.md> [--sticky-flag NAME ...]
Exit code 0 if no issue, 1 otherwise.
"""
import argparse
import re
import sys

DEFAULT_STICKY_FLAGS = ('fcsr.fflags', 'vxsat')

parser = argparse.ArgumentParser(description='Check result-formula style.')
parser.add_argument('path', help='Markdown file to check')
parser.add_argument('--sticky-flag', action='append', default=[], metavar='NAME',
                    help='extra sticky-state name (e.g. fcsr.fflags); repeatable')
args = parser.parse_args()
sticky_flags = DEFAULT_STICKY_FLAGS + tuple(args.sticky_flag)

path = args.path
lines = open(path, encoding='utf-8').read().split('\n')

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
    start, end = i, j
    body = lines[start + 1:end]
    i = j + 1
    if not any(r'\mathrm{instr}' in l for l in body):
        continue
    blocks += 1
    line0 = start + 2

    # left side: every line starts with '&'
    for k, l in enumerate(body):
        s = l.strip()
        if s and not s.startswith('&'):
            issues.append((line0 + k, 'left line does not start with &', l[:80]))

    # last left line carries the instruction
    if r'\mathrm{instr}' not in body[-1]:
        issues.append((end, 'instr not last', body[-1][:80]))

    # at most one top-level \land per line
    for k, l in enumerate(body):
        s = l.strip()
        if s.startswith('&'):
            s = s[1:]
        if s.endswith('\\\\'):
            s = s[:-2]
        cnt = 0
        for m in re.finditer(r'\\land(?![a-zA-Z])', s):
            pre = s[:m.start()]
            depth = (pre.count('(') + pre.count('[') + pre.count('{')
                     - pre.count(')') - pre.count(']') - pre.count('}'))
            if depth == 0:
                cnt += 1
        if cnt > 1:
            issues.append((line0 + k, 'multi top-level land', l[:80]))

    # separator and right side live after \end{aligned}, up to the closing $$
    k = end + 1
    after = []
    while k < len(lines) and lines[k].strip() != '$$':
        after.append(lines[k])
        k += 1
    if r'\longrightarrow' not in '\n'.join(after):
        issues.append((line0, 'missing \\longrightarrow', ''))
        continue
    tail = []
    seen = False
    for l in after:
        if r'\longrightarrow' in l:
            seen = True
            continue
        if seen:
            tail.append(l.strip())
    tail = [t for t in tail if t and not t.startswith('%')]
    if not tail:
        issues.append((end, 'empty right side', ''))
        continue
    right = ' '.join(tail)
    if not right.startswith(r'\{\,'):
        issues.append((line0, 'right side must start with \\{\\,', right[:60]))
    if not right.endswith(r'\,\}'):
        issues.append((end, 'right side must end with \\,\\}', right[-40:]))

    m = re.search(r'\\mathrm\{exception\}(=|\\in)', right)
    if not m:
        issues.append((end, 'missing exception field', right[:60]))
    else:
        pos = m.start()
        depth = 0
        bad = False
        for n, ch in enumerate(right[pos:]):
            if ch in '({[':
                depth += 1
            elif ch in ')}]':
                depth -= 1
            elif ch == ',' and depth == 0 and right[pos + n - 1] != '\\':
                bad = True
                break
        if bad:
            issues.append((end, 'exception is not the last field', right[pos:][:60]))

    for flag in sticky_flags:
        if r'\mathrm{' + flag + '}' in right:
            pattern = r'\\mathrm\{' + re.escape(flag) + r'\}(.{0,16})'
            for m in re.finditer(pattern, right):
                if r'\mathrel{|}=' not in m.group(1):
                    issues.append((end, 'sticky flag not set with \\mathrel{|}=: ' + flag,
                                   m.group(1)[:40]))

    joined = '\n'.join(body)
    for bad in (r'\wedge', r'\vee'):
        if bad in joined:
            issues.append((line0, 'use \\land/\\lor, not ' + bad, ''))
    for m in re.finditer(r"\b\d+'[hHdDbBoO]", joined):
        issues.append((line0, 'bit-pattern literal', m.group(0)))

print('formula blocks:', blocks)
for b in issues:
    print(b)
sys.exit(0 if not issues else 1)
