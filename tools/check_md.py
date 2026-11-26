"""Structural checks for the formalization Markdown.

Usage: python3 -I check_md.py <file.md>
Exit code 0 if all checks pass, 1 otherwise.
"""
import re
import sys

p = sys.argv[1]
text = open(p, encoding='utf-8').read()
lines = text.split('\n')
ok = True

print("lines:", len(lines))

n_dd = text.count('$$')
print("$$ count:", n_dd, "even" if n_dd % 2 == 0 else "ODD!")
ok &= n_dd % 2 == 0

for env in ('aligned', 'cases', 'pmatrix'):
    a = text.count('\\begin{%s}' % env)
    b = text.count('\\end{%s}' % env)
    print("begin/end %s:" % env, a, b)
    ok &= a == b

# inline $ balance per line (remove $$ first)
bad_inline = []
for i, l in enumerate(lines, 1):
    s = l.replace('$$', '')
    if s.count('$') % 2 == 1:
        bad_inline.append(i)
print("lines with odd inline $:", bad_inline[:20], "total", len(bad_inline))
ok &= not bad_inline

# tables: every row in one block must have the same column count
tables = []
i = 0
while i < len(lines):
    if lines[i].strip().startswith('|'):
        j = i
        while j < len(lines) and lines[j].strip().startswith('|'):
            j += 1
        tables.append((i + 1, j, i))
        i = j
    else:
        i += 1
print("tables:", len(tables))

bad = []
for start, end, _ in tables:
    counts = [lines[k].strip().strip('|').count('|') + 1 for k in range(start - 1, end)]
    if len(set(counts)) != 1:
        bad.append((start, counts))
print("bad tables:", len(bad))
for b in bad[:10]:
    print("  ", b)
ok &= not bad

# pipes inside math within table rows
pb = []
for start, end, _ in tables:
    for k in range(start - 1, end):
        l = lines[k]
        for m in re.finditer(r'\$[^$]*\$', l):
            if '|' in m.group(0):
                pb.append((k + 1, m.group(0)[:60]))
print("math-with-pipe in tables:", len(pb))
for x in pb[:10]:
    print("  ", x)
ok &= not pb

sys.exit(0 if ok else 1)
