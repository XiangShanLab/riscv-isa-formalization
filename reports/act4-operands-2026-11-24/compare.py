#!/usr/bin/env python3
"""Compare checked-in scalar FP operands; read inputs without running either suite."""
import argparse
import ast
import csv
import importlib.util
import itertools
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

WORK = Path(__file__).resolve().parents[2]
NAME = 'f-d-q-zfh-zfhmin-zfbfmin-zfa-zfinx-zdinx-zhinx-zhinxmin'
PROG = WORK / 'prog' / NAME
BINARY = set('fadd fsub fmul fdiv fmin fmax fminm fmaxm fsgnj fsgnjn fsgnjx feq flt fle fleq fltq'.split())
FMA = set('fmadd fmsub fnmadd fnmsub'.split())
WIDTH = {'h': (16, 5, 10), 's': (32, 8, 23), 'd': (64, 11, 52), 'bf16': (16, 8, 7)}
SUITES = ['F', 'D', 'Zfh', 'Zfhmin', 'Zfbfmin', 'Zfa']
LOAD = re.compile(r'LOAD_FLOAT_(HALF|SINGLE|DOUBLE).*# load fs[123]: (f\d+) = (0x[0-9a-fA-F]+)')
TARGET = re.compile(r'^\s+([a-z0-9]+)\.([hsd])\s+([^#]+)# perform operation')
ROUND = {'rne': 0, 'rtz': 1, 'rdn': 2, 'rup': 3, 'rmm': 4, 'dyn': 7}


def classify(v, fmt):
    w, e, f = WIDTH[fmt]
    sign, exp, frac = v >> (w-1), (v >> f) & ((1 << e)-1), v & ((1 << f)-1)
    if exp == (1 << e)-1:
        if frac:
            return 'qNaN' if frac & (1 << (f-1)) else 'sNaN'
        return '-inf' if sign else '+inf'
    return ('-' if sign else '+') + ('zero' if exp == frac == 0 else 'sub' if exp == 0 else 'normal')


def own_cases(xlen):
    tuples, modes, evidence = defaultdict(set), defaultdict(set), {}
    path = PROG / 'generated' / f'rv{xlen}-f' / 'cases.json'
    rows = json.loads(path.read_text())
    for c in rows:
        op, _, fmt = c['op'].partition('_')
        if op not in BINARY | FMA or fmt not in WIDTH or c['fs'] == 0:
            continue
        arity = 3 if op in FMA else 2
        if not all(c['boxing'][:arity]):
            continue
        key = (op, fmt)
        values = tuple(int(c[k], 16) for k in 'abc'[:arity])
        tuples[key].add(values)
        if c['rm'] is not None:
            modes[key].add((*values, c['rm'], c['frm']))
        evidence.setdefault((key, values), f'{path.relative_to(WORK)}#id={c["id"]}:{c["tag"]}')
    return tuples, modes, evidence


def act_cases(root, xlen):
    tuples, modes, evidence = defaultdict(set), defaultdict(set), {}
    counts, skipped = Counter(), Counter()
    for suite in SUITES:
        for path in sorted((root / 'tests' / f'rv{xlen}i' / suite).glob('*.S')):
            # File stem narrows the scan to the 20 target operation groups.
            if not any(f'-{op}.' in path.name for op in BINARY | FMA):
                continue
            registers, title, frm = {}, '', 0
            for lineno, line in enumerate(path.open(), 1):
                if line.startswith('# Testcase '):
                    registers, title, frm = {}, line.strip(), 0
                m = LOAD.search(line)
                if m:
                    size, reg, val = m.groups()
                    registers[reg] = (int(val, 16), {'HALF': 16, 'SINGLE': 32, 'DOUBLE': 64}[size])
                m = re.match(r'\s+fsrmi\s+(0x[0-9a-f]+|\d+)', line)
                if m:
                    frm = int(m[1], 0)
                m = TARGET.match(line)
                if not m or m[1] not in BINARY | FMA:
                    continue
                op, fmt, args = m.groups()
                key = (op, fmt)
                arity = 3 if op in FMA else 2
                args = [v.strip() for v in args.strip().split(',')]
                srcs = args[1:arity+1]
                if any(reg not in registers for reg in srcs):
                    skipped['missing_load'] += 1
                    continue
                w = WIDTH[fmt][0]
                # A wider load is a valid narrow source iff all intervening bits are ones.
                if any(size > w and val >> w != (1 << (size-w))-1
                       for val, size in (registers[reg] for reg in srcs)):
                    skipped['bad_box'] += 1
                    continue
                values = tuple(registers[reg][0] & ((1 << w)-1) for reg in srcs)
                tuples[key].add(values)
                if op in FMA | {'fadd', 'fsub', 'fmul', 'fdiv'}:
                    rm = ROUND[args[arity+1]] if len(args) > arity+1 else 7
                    modes[key].add((*values, rm, frm if rm == 7 else 0))
                evidence.setdefault((key, values), f'{path.relative_to(root)}:{lineno}')
                counts[key] += 1
    if skipped['missing_load']:
        raise RuntimeError(f'Unparsed source loads: {skipped}')
    return tuples, modes, evidence, counts, skipped


def edge_constants(root):
    tree = ast.parse((root / 'generators/testgen/src/testgen/data/edges.py').read_text())
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'FLOAT_EDGES')
    return {n.targets[0].id: ast.literal_eval(n.value) for n in cls.body if isinstance(n, ast.Assign)}


def csv_write(path, headers, rows):
    with path.open('w', newline='') as out:
        writer = csv.writer(out)
        writer.writerow(headers)
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--act4', type=Path, default=WORK.parent / 'riscv-arch-test')
    parser.add_argument('--out', type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    summary, diff_rows, class_rows, mode_rows = [], [], [], []
    diagnostics = {}
    for xlen in (32, 64):
        ours, our_modes, our_refs = own_cases(xlen)
        theirs, their_modes, their_refs, counts, skipped = act_cases(args.act4, xlen)
        diagnostics[str(xlen)] = {'act4_parsed': sum(counts.values()), 'skipped': dict(skipped)}
        assert len(ours) == len(theirs) == 60, (len(ours), len(theirs))
        for key in sorted(ours):
            op, fmt = key
            a, b = ours[key], theirs[key]
            edge = set(edge_constants(args.act4)[{'h': 'half', 's': 'single', 'd': 'double'}[fmt]])
            edge_pairs = set(itertools.product(edge, repeat=2)) if op in BINARY else set()
            if edge_pairs:
                assert edge_pairs <= b, (xlen, key, len(edge_pairs-b))
                # The fix under test: every ACT4 edge pair must also be generated here.
                assert edge_pairs <= a, (xlen, key, len(edge_pairs-a))
            ca = {tuple(classify(v, fmt) for v in t) for t in a}
            cb = {tuple(classify(v, fmt) for v in t) for t in b}
            assert len(ca) == (1000 if op in FMA else 100), (xlen, key, len(ca))
            summary.append(dict(xlen=xlen, instruction=f'{op}.{fmt}', arity=len(next(iter(a))),
                                ours=len(a), act4=len(b), common=len(a & b),
                                act4_only=len(b-a), ours_only=len(a-b),
                                ours_classes=len(ca), act4_classes=len(cb),
                                common_classes=len(ca & cb),
                                act4_edge_pairs=len(edge_pairs),
                                edge_pairs_common=len(edge_pairs & a),
                                edge_pairs_missing_here=len(edge_pairs-a)))
            for direction, diff, refs in [('act4_only', b-a, their_refs), ('ours_only', a-b, our_refs)]:
                for values in sorted(diff):
                    diff_rows.append([xlen, f'{op}.{fmt}', direction, *[hex(v) for v in values],
                                      *([''] * (3-len(values))), refs[(key, values)]])
            for direction, diff in [('act4_only', cb-ca), ('ours_only', ca-cb)]:
                for values in sorted(diff):
                    class_rows.append([xlen, f'{op}.{fmt}', direction, *values,
                                       *([''] * (3-len(values)))])
            if op in {'fadd', 'fsub', 'fmul', 'fdiv'}:
                # Compare ACT4's guaranteed complete 28 x 28 x five static modes.
                target = {(*v, rm, 0) for v in edge_pairs for rm in range(5)}
                assert target <= their_modes[key], (xlen, key, len(target-their_modes[key]))
                mode_rows.append([xlen, f'{op}.{fmt}', len(target), len(target & our_modes[key]),
                                  len(target-our_modes[key])])
    csv_write(args.out/'instruction-summary.csv', list(summary[0]), [list(v.values()) for v in summary])
    csv_write(args.out/'operand-differences.csv', ['xlen', 'instruction', 'direction', 'a', 'b', 'c', 'evidence'], diff_rows)
    csv_write(args.out/'class-differences.csv', ['xlen', 'instruction', 'direction', 'class_a', 'class_b', 'class_c'], class_rows)
    csv_write(args.out/'static-rounding-summary.csv', ['xlen', 'instruction', 'act4_28x28x5', 'ours_common', 'missing_here'], mode_rows)
    spec = importlib.util.spec_from_file_location('local_generate', PROG/'generate.py')
    gen = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gen)
    edges, edge_diff = edge_constants(args.act4), {}
    for fmt, field in [('h', 'half'), ('s', 'single'), ('d', 'double'), ('bf16', 'bf16')]:
        a, b = set(gen.patterns(fmt).values()), set(edges[field])
        edge_diff[fmt] = {'ours': len(a), 'act4': len(b), 'common': len(a & b),
                          'act4_only': [hex(v) for v in sorted(b-a)],
                          'ours_only': {k: hex(v) for k, v in gen.patterns(fmt).items() if v not in b}}
    result = {'scope': 'RV32/RV64; f-register H/S/D; 16 binary and four FMA groups; checked-in well-boxed inputs; numeric tuple comparison ignores rounding, registers and initial flags; static-rounding-summary compares them separately',
              'diagnostics': diagnostics, 'edge_sets': edge_diff, 'instructions': summary}
    (args.out/'summary.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'diagnostics': diagnostics, 'edge_sets': edge_diff,
                      'diff_rows': len(diff_rows), 'class_diff_rows': len(class_rows)}, indent=2))
    for s in summary:
        if s['xlen'] == 64 and s['instruction'] in ['fadd.s', 'fmadd.s', 'fadd.h', 'fadd.d', 'fmadd.h', 'fmadd.d']:
            print(s)


if __name__ == '__main__':
    main()
