#!/usr/bin/env python3
"""Left-hand-side gate coverage for every instruction file.

Coverage is defined on the left-hand side only: every instruction representative is
executed under every privilege configuration that appears in the guard block.

  f bank : 5 modes x (4 mstatus.FS values, and for VS/VU all 4 vsstatus.FS values)
           = 44 configurations per representative
  x bank : 5 modes x 8 (mstateen0, hstateen0, sstateen0) FCSR-bit configurations
           = 40 configurations per representative

A second matrix covers the rounding-mode legality conjunct: ten legal configurations
(rm=0..4, and rm=DYN with frm=0..4) and five reserved ones, which the formulas leave
outside every branch and are recorded observationally.  Cases are never merged by
right-hand result: the same gate is run for every file even where the outcome repeats.
"""
from pathlib import Path
import itertools, json, re, struct
from run import ROOT, DEFAULT_SAIL, command, configure, signature
from generate import ENC, encoding

MODES = ['M', 'HS', 'U', 'VS', 'VU']
ECALL = {'M': 11, 'HS': 9, 'U': 8, 'VS': 10, 'VU': 8}
RMS = [(i, 0) for i in range(5)] + [(7, i) for i in range(5)]
RESERVED = [(5, 0), (6, 0), (7, 5), (7, 6), (7, 7)]

# (directory stem, mnemonic, operand setup, destination, rounds)
F_REPS = [
    ('fadd', 'fadd_s', 'f', 'fp', True),
    ('fsub', 'fsub_s', 'f', 'fp', True),
    ('fmul', 'fmul_s', 'f', 'fp', True),
    ('fdiv', 'fdiv_s', 'f', 'fp', True),
    ('fsqrt', 'fsqrt_s', 'f', 'fp', True),
    ('fmin', 'fmin_s', 'f', 'fp', False),
    ('fmax', 'fmax_s', 'f', 'fp', False),
    ('fminm', 'fminm_s', 'f', 'fp', False),
    ('fmaxm', 'fmaxm_s', 'f', 'fp', False),
    ('fsgnj', 'fsgnj_s', 'f', 'fp', False),
    ('feq', 'feq_s', 'f', 'int', False),
    ('flt', 'flt_s', 'f', 'int', False),
    ('fle', 'fle_s', 'f', 'int', False),
    ('fleq', 'fleq_s', 'f', 'int', False),
    ('fltq', 'fltq_s', 'f', 'int', False),
    ('fclass', 'fclass_s', 'f', 'int', False),
    ('fround', 'fround_s', 'f', 'fp', True),
    ('froundnx', 'froundnx_s', 'f', 'fp', True),
    ('fli', 'fli_s', 'none', 'fp', False),
    ('fmadd', 'fmadd_s', 'f', 'fp', True),
    ('fmsub', 'fmsub_s', 'f', 'fp', True),
    ('fnmsub', 'fnmsub_s', 'f', 'fp', True),
    ('fnmadd', 'fnmadd_s', 'f', 'fp', True),
    ('fcvt-fp-fp', 'fcvt_s_d', 'd', 'fp', True),
    ('fcvt-to-int', 'fcvt_w_s', 'f', 'int', True),
    ('fcvt-from-int', 'fcvt_s_w', 'i', 'fp', True),
    ('fcvttmod', 'fcvtmod_w_d', 'd', 'int', False),
    ('bf16', 'fcvt_bf16_s', 'f', 'fp', True),
    ('fmv-w', 'fmv_x_w', 'f', 'int', False),
    ('fmv-d', 'fmv_x_d', 'd', 'int', False),
    ('fmv-h', 'fmv_x_h', 'h', 'int', False),
    ('fmvh', 'fmvh_x_d', 'd', 'int', False),
    ('fmvp', 'fmvp_d_x', 'i', 'fp', False),
    ('flw', 'flw', 'ldw', 'fp', False),
    ('fld', 'fld', 'ldd', 'fp', False),
    ('flh', 'flh', 'ldh', 'fp', False),
    ('fsw', 'fsw', 'f', 'mem', False),
    ('fsd', 'fsd', 'd', 'mem', False),
    ('fsh', 'fsh', 'h', 'mem', False),
    ('fcsr', 'frcsr', 'none', 'int', False),
    ('fcsr', 'fscsr', 'i', 'int', False),
]

# The Zfinx file covers every x-register form; no transfers, no loads/stores, no
# Zfa in this configuration (Zfa is only combined with the f-register files).
X_REPS = [
    ('zfinx', 'fadd_s', 'f', 'fp', True),
    ('zfinx', 'fsub_s', 'f', 'fp', True),
    ('zfinx', 'fmul_s', 'f', 'fp', True),
    ('zfinx', 'fdiv_s', 'f', 'fp', True),
    ('zfinx', 'fsqrt_s', 'f', 'fp', True),
    ('zfinx', 'fmin_s', 'f', 'fp', False),
    ('zfinx', 'fmax_s', 'f', 'fp', False),
    ('zfinx', 'fsgnj_s', 'f', 'fp', False),
    ('zfinx', 'feq_s', 'f', 'int', False),
    ('zfinx', 'flt_s', 'f', 'int', False),
    ('zfinx', 'fle_s', 'f', 'int', False),
    ('zfinx', 'fclass_s', 'f', 'int', False),
    ('zfinx', 'fmadd_s', 'f', 'fp', True),
    ('zfinx', 'fcvt_s_d', 'd', 'fp', True),
    ('zfinx', 'fcvt_w_s', 'f', 'int', True),
    ('zfinx', 'fcvt_s_w', 'i', 'fp', True),
    ('zfinx', 'frcsr', 'none', 'int', False),
    ('zfinx', 'fscsr', 'i', 'int', False),
]

RM_F = ['fadd_s', 'fsqrt_s', 'fmadd_s', 'fdiv_s', 'fcvt_s_d', 'fcvt_w_s', 'fcvt_s_w', 'fround_s']
RM_X = ['fadd_s', 'fsqrt_s', 'fmadd_s', 'fdiv_s', 'fcvt_s_d', 'fcvt_w_s', 'fcvt_s_w']
UNARY = {'fsqrt_s', 'fclass_s', 'fround_s', 'froundnx_s', 'fcvt_w_s',
         'fmv_x_w', 'fmv_x_d', 'fmv_x_h', 'fmvh_x_d', 'fcvt_s_w'}
FMA = {'fmadd_s', 'fmsub_s', 'fnmsub_s', 'fnmadd_s'}
LOADS = {'flw', 'fld', 'flh'}
STORES = {'fsw', 'fsd', 'fsh'}


def gate_configs(bank):
    if bank == 'f':
        out = [(m, fs, 3) for m in ['M', 'HS', 'U'] for fs in range(4)]
        out += [(m, fs, vfs) for m in ['VS', 'VU'] for fs in range(4) for vfs in range(4)]
        return out
    return [(m, mst, hst, sst) for m in MODES
            for mst, hst, sst in itertools.product([0, 1], repeat=3)]


def expected_gate(bank, cfg, mode):
    if bank == 'f':
        _, fs, vfs = cfg
        return 2 if fs == 0 or (mode in ['VS', 'VU'] and vfs == 0) else 0
    _, m, h, s = cfg
    if mode != 'M' and (not m or (mode == 'U' and not s)):
        return 2
    if mode in ['VS', 'VU'] and (not h or (mode == 'VU' and not s)):
        return 22
    return 0


def make_word(op, rm=None):
    if op in LOADS:
        return ENC[op] | (24 << 7) | (29 << 15)
    if op in STORES:
        return ENC[op] | (20 << 20) | (29 << 15)
    if op == 'frcsr':
        return (3 << 20) | (2 << 12) | (24 << 7) | 0x73
    if op == 'fscsr':
        return (3 << 20) | (1 << 12) | (18 << 15) | (24 << 7) | 0x73
    if op == 'fli_s':
        return encoding('fli_s', rd=24, rs1=0, rs2=None)
    rs2 = None if op in UNARY else 20
    rs3 = 22 if op in FMA else None
    return encoding(op, rd=24, rs1=18, rs2=rs2, rm=rm, rs3=rs3)


def setup_lines(bank, setup):
    L = []
    if setup == 'f':
        if bank == 'f':
            L += [' li t0,0x3f800000', ' fmv.w.x f18,t0',
                  ' li t0,0x40000000', ' fmv.w.x f20,t0',
                  ' li t0,0x40400000', ' fmv.w.x f22,t0']
        else:
            L += [' li x18,0x3f800000', ' li x20,0x40000000', ' li x22,0x40400000']
    elif setup == 'd':
        if bank == 'f':
            L += [' li t0,0x3ff0000000000000', ' fmv.d.x f18,t0',
                  ' li t0,0x4000000000000000', ' fmv.d.x f20,t0',
                  ' li t0,0x4008000000000000', ' fmv.d.x f22,t0']
        else:
            L += [' li x18,0x3ff0000000000000', ' li x20,0x4000000000000000',
                  ' li x22,0x4008000000000000']
    elif setup == 'h':
        if bank == 'f':
            L += [' li t0,0xffffffffffff3c00', ' fmv.d.x f18,t0',
                  ' li t0,0xffffffffffff4000', ' fmv.d.x f20,t0',
                  ' li t0,0xffffffffffff4200', ' fmv.d.x f22,t0']
        else:
            L += [' li x18,0x3c00', ' li x20,0x4000', ' li x22,0x4200']
    elif setup == 'i':
        L += [' li x18,1', ' li x20,2', ' li x22,3']
    elif setup == 'ldw':
        L += [' la x29,scratch', ' li t0,0x3f800000', ' sw t0,0(x29)']
    elif setup == 'ldd':
        L += [' la x29,scratch', ' li t0,0x3ff0000000000000', ' sd t0,0(x29)']
    elif setup == 'ldh':
        L += [' la x29,scratch', ' li t0,0x3c00', ' sh t0,0(x29)']
    return L


def build_cases(bank):
    reps = F_REPS if bank == 'f' else X_REPS
    cases = []
    for label, op, setup, dest, rounds in reps:
        for cfg in gate_configs(bank):
            mode = cfg[0]
            c = dict(id=len(cases), bank=bank, section='gate', file=label, op=op,
                     setup=setup, dest=dest, mode=mode,
                     word=make_word(op, 0 if rounds else None), rm=0, frm=0,
                     expected=expected_gate(bank, cfg, mode))
            if bank == 'f':
                c.update(fs=cfg[1], vfs=cfg[2], m=1, h=1, s=1)
            else:
                c.update(fs=0, vfs=0, m=cfg[1], h=cfg[2], s=cfg[3])
            cases.append(c)
    rm_reps = RM_F if bank == 'f' else RM_X
    for op in rm_reps:
        label = op
        setup = 'f' if op in ['fadd_s', 'fsqrt_s', 'fmadd_s', 'fdiv_s', 'fround_s'] else \
                'd' if op == 'fcvt_s_d' else 'f' if op == 'fcvt_w_s' else 'i' if op == 'fcvt_s_w' else 'f'
        dest = 'int' if op in ['fcvt_w_s'] else 'fp'
        for rm, frm in RMS:
            c = dict(id=len(cases), bank=bank, section='rm', file=label, op=op,
                     setup=setup, dest=dest, mode='M', word=make_word(op, rm),
                     rm=rm, frm=frm, expected=0, fs=3, vfs=3, m=1, h=1, s=1)
            cases.append(c)
        for rm, frm in RESERVED:
            c = dict(id=len(cases), bank=bank, section='reserved', file=label, op=op,
                     setup=setup, dest=dest, mode='M', word=make_word(op, rm),
                     rm=rm, frm=frm, expected=None, fs=3, vfs=3, m=1, h=1, s=1)
            cases.append(c)
    return cases


def emit(bank, cases):
    lines = ['.section .text.init,"ax"', '.option norvc', '.globl _start', '_start:',
             ' la t0,trap_handler', ' csrw mtvec,t0', ' csrw mie,zero',
             ' csrw medeleg,zero', ' csrw mideleg,zero', ' csrw satp,zero',
             ' csrw 0x280,zero', ' csrw 0x680,zero',
             ' li t0,-1', ' csrw pmpaddr0,t0', ' li t0,31', ' csrw pmpcfg0,t0',
             ' la s1,begin_signature']
    for c in cases:
        n = c['id']; mode = c['mode']; op = c['op']
        pp = 3 if mode == 'M' else 1 if mode in ['HS', 'VS'] else 0
        virt = mode in ['VS', 'VU']
        L = [f'# {n}: {c["file"]} {mode} gate={c["fs"]}/{c["vfs"]} mhs={c["m"]}{c["h"]}{c["s"]} rm={c["rm"]}',
             f' la s3,after_{n}', ' li s11,0', ' li s10,0']
        if bank == 'f':
            L += [' li t0,0x6000', ' csrs mstatus,t0']
        L += setup_lines(bank, c['setup'])
        if op in STORES:
            L += [' la x29,scratch', ' sd zero,0(x29)', ' sd zero,8(x29)']
        L += [' csrw fcsr,zero']
        if c['frm']:
            L += [f' li t0,{c["frm"] << 5}', ' csrw fcsr,t0']
        if bank == 'f':
            L += [' li t0,-1', ' csrw 0x30c,t0', ' csrw 0x60c,t0', ' csrw 0x10c,t0',
                  f' li t0,{c["vfs"] << 13}', ' csrw 0x200,t0',
                  f' li t0,{(1 << 39) | 0x6000}', ' csrc mstatus,t0',
                  f' li t0,{c["fs"] << 13}', ' csrs mstatus,t0',
                  f' li t0,{(1 << 39) | 0x1800}', ' csrc mstatus,t0']
        else:
            L += [' li t0,-1', ' csrw 0x30c,t0', ' csrw 0x60c,t0',
                  f' li t0,{2 * c["s"]}', ' csrw 0x10c,t0',
                  f' li t0,{(1 << 63) | 2 * c["h"]}', ' csrw 0x60c,t0',
                  f' li t0,{(1 << 63) | 2 * c["m"]}', ' csrw 0x30c,t0']
        L += [f' li t0,{(pp << 11) | ((1 << 39) if virt else 0)}', ' csrs mstatus,t0',
              f' la t0,target_{n}', ' csrw mepc,t0', ' mret',
              f'.globl target_{n}', f'target_{n}:', f' .word 0x{c["word"]:08x}', ' ecall',
              f'after_{n}:', ' csrr t0,mstatus', ' srli t0,t0,13', ' andi t0,t0,3',
              ' sw t0,20(s1)', ' sw s11,24(s1)', f' li t0,{n}', ' sw t0,28(s1)',
              ' sd s10,48(s1)', ' sw s7,32(s1)',
              ' li t0,-1', ' csrw 0x30c,t0', ' csrw 0x60c,t0', ' csrw 0x10c,t0']
        if bank == 'f':
            L += [' li t0,0x6000', ' csrs mstatus,t0']
        L += [' csrr t0,fcsr', ' sw t0,16(s1)']
        if c['dest'] == 'fp':
            L += [' fsd f24,0(s1)'] if bank == 'f' else [' sd x24,0(s1)']
        elif c['dest'] == 'int':
            L += [' sd x24,0(s1)']
        else:
            L += [' ld t0,0(x29)', ' sd t0,40(s1)']
        if op in LOADS:
            L += [' ld t0,0(x29)', ' sd t0,40(s1)']
        L += [' csrr t0,misa', ' sd t0,56(s1)', ' addi s1,s1,64']
        lines += L
    lines += [' la t0,tohost', ' li t1,1', ' sd t1,0(t0)', '1: j 1b', '.balign 4',
              'trap_handler:', ' csrr s11,mcause', ' mv s7,s11', ' csrr s10,mepc',
              ' li t0,8', ' bltu s11,t0,2f', ' li t0,11', ' bltu t0,s11,2f',
              ' li s11,0', ' li s10,0',
              '2:', ' csrw mepc,s3', f' li t0,{(1 << 39) | 0x1800}', ' csrc mstatus,t0',
              ' li t0,0x1800', ' csrs mstatus,t0', ' mret',
              '.section .data,"aw"', '.balign 16', 'scratch: .zero 16',
              '.section .tohost,"aw"', '.balign 64', '.globl tohost,fromhost',
              'tohost: .dword 0', 'fromhost: .dword 0',
              '.section .signature,"aw"', '.balign 64',
              '.globl begin_signature,end_signature', 'begin_signature:',
              f' .zero {64 * len(cases)}', 'end_signature:']
    return '\n'.join(lines) + '\n'


def run_bank(bank):
    name = 'rv64-' + bank + '-lhs'
    src = ROOT / 'generated' / name; src.mkdir(exist_ok=True)
    out = ROOT / 'results' / name; out.mkdir(exist_ok=True)
    build = ROOT / 'build' / name; build.mkdir(exist_ok=True)
    cases = build_cases(bank)
    asm = src / 'suite.S'; asm.write_text(emit(bank, cases))
    (src / 'cases.json').write_text(json.dumps(cases, indent=2) + '\n')
    elf = build / 'suite.elf'
    cc = command(['riscv64-unknown-elf-gcc', '-march=rv64imafdh_zicsr', '-mabi=lp64',
                  '-nostdlib', '-nostartfiles', '-Wl,--no-relax', '-T', ROOT / 'link.ld',
                  asm, '-o', elf], 600)
    (out / 'build.json').write_text(json.dumps(cc, indent=2) + '\n')
    if cc['returncode'] != 0:
        print(name, 'BUILD FAILED', cc['stderr'][:2000]); return dict(profile=name, status='build_failed')
    ext = ['f', 'd', 'zfh', 'zfhmin', 'zfbfmin', 'zfa'] if bank == 'f' else \
          ['zfinx', 'zdinx', 'zhinx', 'zhinxmin']
    p = dict(xlen=64, bank=bank, ext=ext)
    cfg = configure(DEFAULT_SAIL, p)
    cfg['extensions']['H']['supported'] = True
    cfg['extensions']['Stateen']['Smstateen']['supported'] = True
    cfg['extensions']['Stateen']['Ssstateen']['supported'] = True
    cfgpath = ROOT / 'configs' / (name + '.json'); cfgpath.write_text(json.dumps(cfg, indent=2) + '\n')
    isa = 'rv64imafdh_zicsr_smstateen_ssstateen_zfh_zfhmin_zfbfmin_zfa' if bank == 'f' else \
          'rv64imah_zicsr_smstateen_ssstateen_zfinx_zdinx_zhinx_zhinxmin'
    commands = {
        'spike': ['spike', '--isa=' + isa, '-m128', '+signature=' + str(out / 'spike.sig'),
                  '+signature-granularity=4', elf],
        'sail': [DEFAULT_SAIL, '--config', cfgpath, '--inst-limit', '5000000',
                 '--test-signature', out / 'sail.sig', '--signature-granularity', '4', elf],
    }
    rows = {}; result = dict(profile=name, cases=len(cases), models={})
    syms = command(['riscv64-unknown-elf-nm', elf])['stdout']
    pcs = {int(m[2]): int(m[1], 16) for m in re.finditer(r'^([0-9a-f]+) \w target_(\d+)$', syms, re.M)}
    for model, cmd in commands.items():
        (out / (model + '.sig')).unlink(missing_ok=True)
        r = command(cmd, 1200)
        (out / (model + '.json')).write_text(json.dumps(r, indent=2) + '\n')
        checked = 0; bad = []; harness = []
        if r['returncode'] == 0 and (out / (model + '.sig')).exists():
            data = signature(out / (model + '.sig')); rows[model] = []
            for i, c in enumerate(cases):
                b = data[i * 64:(i + 1) * 64]; w = struct.unpack('<16I', b)
                exc = w[6]; trap_pc = int.from_bytes(b[48:56], 'little')
                row = dict(id=i, boundary_cause=w[8], exception=exc,
                           result=b[:16].hex(), fcsr=w[4], fs=w[5],
                           memory=b[40:48].hex(), trap_pc=hex(trap_pc))
                rows[model].append(row)
                if c['expected'] is None:
                    checked += 1; continue
                if not exc and w[8] != ECALL[c['mode']]:
                    harness.append(dict(case=c, wrong_boundary_cause=w[8]))
                if exc and trap_pc != pcs[i]:
                    harness.append(dict(case=c, actual_pc=hex(trap_pc), target_pc=hex(pcs[i])))
                if exc != c['expected']:
                    bad.append(dict(case=c, actual=exc))
                checked += 1
            (out / (model + '.jsonl')).write_text(''.join(json.dumps(r) + '\n' for r in rows[model]))
        result['models'][model] = dict(returncode=r['returncode'], checked=checked,
                                       gate_differences=bad, harness_errors=harness)
    if len(rows) == 2:
        result['paired'] = len(cases)
        result['differences'] = [dict(case=cases[a['id']], spike=a, sail=b)
                                 for a, b in zip(rows['spike'], rows['sail'])
                                 if any(a[k] != b[k] for k in ['exception', 'result', 'fcsr', 'memory'])]
    else:
        result['paired'] = 0
    (out / 'summary.json').write_text(json.dumps(result, indent=2) + '\n')
    print(name, 'cases', len(cases), 'paired', result['paired'],
          'diff', len(result.get('differences', [])),
          'models', [(k, v['returncode'], len(v['gate_differences']), len(v['harness_errors']))
                     for k, v in result['models'].items()], flush=True)
    return result


def main():
    summaries = [run_bank('f'), run_bank('x')]
    (ROOT / 'results' / 'lhs-summary.json').write_text(json.dumps(summaries, indent=2) + '\n')
    total = sum(s.get('cases', 0) for s in summaries)
    print('lhs total', total)


if __name__ == '__main__':
    main()
