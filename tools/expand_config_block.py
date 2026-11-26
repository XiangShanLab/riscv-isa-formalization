import re, sys

path = sys.argv[1]
src = open(path, encoding='utf-8').read().split('\n')

no_rm = ('FMIN','FMAX','FSGNJ','FEQ','FLT','FLE','FCLASS','FCVTMOD',
         'FLI','FRCSR','FSCSR','FSRM','FSFLAGS','FRRM','FRFLAGS')

pat = re.compile(r'^&\(\\mathrm\{enabled\}\((.+)\)\)\\\\$')

def block(arg, has_rm):
    lines = [
        r'&(mstatus.FS\in\{1,2,3\})\\',
        r'&\land\ \mathrm{impl}(%s)\\' % arg,
        r'&\land\ \big(V=0\lor(vsstatus.FS\in\{1,2,3\}\land sstatus.FS\in\{1,2,3\})\big)\\',
        r'&\land\ \big(\neg\mathrm{Stateen}\lor misa.F=1\lor st=1\big)\\',
    ]
    if has_rm:
        lines.append(r'&\land\ \big(rm\in\{0,1,2,3,4\}\lor(rm=7\land fcsr.frm\in\{0,1,2,3,4\})\big)\\')
    return lines

out = []
n = 0
for line in src:
    m = pat.match(line)
    if not m:
        out.append(line)
        continue
    arg = m.group(1)
    has_rm = not any(k in arg for k in no_rm)
    out.extend(block(arg, has_rm))
    n += 1

open(path, 'w', encoding='utf-8').write('\n'.join(out))
print('expanded', n, 'formulas')
