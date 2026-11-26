import sys

def split_top(s):
    parts, buf, depth, i = [], [], 0, 0
    while i < len(s):
        if s.startswith(r'\land', i) and depth == 0:
            parts.append(''.join(buf).strip())
            buf = []
            i += 5
            while i < len(s):
                if s.startswith(r'\ ', i):
                    i += 2
                elif s[i] == ' ':
                    i += 1
                else:
                    break
            continue
        c = s[i]
        if c in '([{':
            depth += 1
        elif c in ')]}':
            depth -= 1
        buf.append(c)
        i += 1
    parts.append(''.join(buf).strip())
    return [p for p in parts if p]

path = sys.argv[1]
src = open(path, encoding='utf-8').read().split('\n')
out, i = [], 0
BEGIN, END = r'\begin{aligned}', r'\end{aligned}'
while i < len(src):
    if src[i].strip() == BEGIN:
        j = i + 1
        while j < len(src) and not src[j].strip().startswith(END):
            j += 1
        block = src[i + 1:j]
        if j >= len(src) or src[j].strip() != END or any(r'&\qquad' in l for l in block):
            out.extend(src[i:j + 1]); i = j + 1; continue
        toks = []
        for l in block:
            s = l.strip()
            if s.startswith('&'):
                s = s[1:].strip()
            if s.endswith('\\\\'):
                s = s[:-2].strip()
            toks.extend(split_top(s))
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
