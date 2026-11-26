import sys

path = sys.argv[1]
src = open(path, encoding='utf-8').read().split('\n')
out, i = [], 0
BEGIN, END = r'\begin{aligned}', r'\end{aligned}'
while i < len(src):
    if src[i].strip() == BEGIN:
        j = i + 1
        while j < len(src) and not src[j].strip().startswith(END):
            j += 1
        # only rewrite blocks whose closer stands alone (skip underbrace template)
        if j >= len(src) or src[j].strip() != END:
            out.extend(src[i:j + 1]); i = j + 1; continue
        block = src[i + 1:j]
        if any(r'&\qquad' in l for l in block):
            out.extend(src[i:j + 1]); i = j + 1; continue
        toks = []
        for l in block:
            s = l.strip()
            if s.startswith('&'):
                s = s[1:].strip()
            if s.endswith('\\\\'):
                s = s[:-2].strip()
            if s.startswith(r'\land\ '):
                s = s[len(r'\land\ '):].strip()
            elif s == r'\land':
                s = ''
            if not s:
                continue
            toks.extend(p.strip() for p in s.split(r'\ \land\ ') if p.strip())
        instr = [t for t in toks if r'\mathrm{instr}' in t]
        rest = [t for t in toks if r'\mathrm{instr}' not in t]
        toks = rest + instr
        out.append(BEGIN)
        for k, t in enumerate(toks):
            pre = '&' if k == 0 else r'&\land\ '
            suf = '' if k == len(toks) - 1 else r'\\'
            out.append(pre + t + suf)
        out.append(END)
        i = j + 1
    else:
        out.append(src[i]); i += 1
open(path, 'w', encoding='utf-8').write('\n'.join(out))
