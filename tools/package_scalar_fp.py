#!/usr/bin/env python3
"""Assemble a self-contained scalar FP delivery without touching shared instructions/."""
from pathlib import Path
import shutil, tarfile, hashlib, subprocess, sys, json
ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'dist/riscv-scalar-fp-v1'
DEST.mkdir(parents=True,exist_ok=True)
for directory in ['tools','reports','sources','skills/riscv-manual']:(DEST/directory).mkdir(parents=True,exist_ok=True)
for name in ['build_fp_instructions.py','validate_instructions.py','check_fp_semantics.py','fp_arithmetic_seed.json','check_md.py','check_style.py']:
 shutil.copyfile(ROOT/'tools'/name,DEST/'tools'/name)
for name in ['riscv-unprivileged.pdf','riscv-unprivileged.txt','riscv-privileged.pdf','riscv-privileged.txt']:
 shutil.copyfile(ROOT/'sources'/name,DEST/'sources'/name)
with tarfile.open(ROOT/'fp-formalization-workflow-v1.tar.gz') as ar:
 original=ar.extractfile('fp-formalization-workflow/workflow.md').read().decode()
 skill=ar.extractfile('fp-formalization-workflow/skills/riscv-manual/SKILL.md').read()
(DEST/'skills/riscv-manual/SKILL.md').write_bytes(skill)
(DEST/'workflow-original.md').write_text(original)
clarification='''> Application to this scalar collection (2026-11-20): the local ISA manuals take precedence over the historical FADD example wherever they differ. `DirtyFS` is the permitted state-update relation defined in each delivered document, including unchanged writes and imprecise tracking. SD summarizes FS/VS/XS. Because misa can report zero, all applicable state-enable conditions remain explicit, even for f-register operations. Tininess uses separate precision-only rounding with an unbounded exponent, as required by Unprivileged §25.3.2.6.1; it is not inferred solely from the final subnormal class. Memory formulas compose with the ordinary architectural access relation and retain partial effects. See `reports/scalar-fp-review.md` for exact source anchors. The generated `instructions/` documents are the current finished specification; the appendix is the historical pilot.

'''
new_symbols=r'''### 3.2.1 本交付的符号登记补充

下列补充是 §3.2 符号表的一部分；只定义数值与写入集，不隐藏配置条件。

| 符号 | 含义 | 依据 / 定义 |
|---|---|---|
| $\sigma,\sigma'$ | 入口状态与结果候选状态 | 关系式记号 |
| $\mathcal W_{FP}$ | 当前分支实际写入的 f 寄存器及 fcsr 字段集合 | 各分支右端写入集 |
| $\mathrm{changed}$ | 写入字段是否实际改变 | 按字段逐项比较；Priv. §3.1.6.7，PDF p.46 |
| $\mathrm{DirtyFS}$ | 手册允许的 FS 更新关系，包含不变写回的实现选择 | Priv. §3.1.6.7、§15.2.11，PDF pp.46,171 |
| $\mathrm{unbounded},\mathrm{roundP}$ | 精度固定、指数两端无限制的舍入值及舍入函数 | Unpriv. §25.3.2.6.1，PDF pp.154–155 |
| $\mathrm{integer},\mathrm{roundInt}$ | 舍入后的无界整数及整数舍入函数 | Unpriv. §21.7、§26.3–26.4 |
| $n,n_1,n_2$ | 对应整数源寄存器的入口值 | 指令源字段 |
| $F_a,F_b,F_c$ | 各源操作数的格式 | 指令变体表 |
| $e_{\max,a},w_{f,a}$ | 各源格式的最大阶码与尾数位宽 | 格式表；转换时源目的分别取值 |
| $\mathrm{enc},\mathrm{sign\_inject}$ | 精确编码及保留阶码/尾数的符号替换 | Unpriv. §21.7、§22.2 |
| $\mathrm{sext},\mathrm{low32}$ | 指定位宽的符号扩展及低 32 位符号扩展 | Unpriv. §21.7、§26.4 |
| $\mathrm{old}(q),\mathrm{oldfflags}$ | 入口 CSR 值与入口五位 fflags 的无符号数值 | Unpriv. §6.1、§21.2 |
| $\mathrm{CSRWrite}_q(v)$ | 对指定浮点 CSR 字段按位宽掩码赋值的写入集 | Unpriv. §6.1、§21.2；允许清除标志 |
| $\mathrm{XWrite}_F(j,v)$ | x 寄存器浮点结果的写入集 | Unpriv. §27.1–27.3，PDF pp.168–169 |
| $EA,w,\mathrm{AXLEN}$ | 有效地址、访存宽度与 MPRV/MPP 决定的地址位宽 | Unpriv. §21.5；Priv. §3.1.6.4 |
| $\mathrm{mem}$ | 入口/出口内存映射 | 普通架构访存关系 |
| $\mathrm{access}$ | 普通架构访存的结果记录，含 value、mem、exception | Priv. §3.1.15、§3.7、§12、§15.5 |
| $\prec$ | 数值顺序，额外区分负零先于正零 | Unpriv. §21.6 |

'''
workflow=clarification+original.replace('### 3.3 书写语法',new_symbols+'### 3.3 书写语法')
(DEST/'workflow.md').write_text(workflow)
shutil.copyfile(ROOT/'reports/scalar-fp-review.md',DEST/'reports/scalar-fp-review.md')
(DEST/'README.md').write_text('''# RISC-V scalar floating-point formalization

The complete English collection is [instructions/README.md](instructions/README.md).
It covers RV32/RV64 scalar instructions in Unprivileged chapters 21–27: F/D/Q,
Zfh/Zfhmin, Zfa, scalar Zfbfmin, Zfinx/Zdinx/Zhinx/Zhinxmin, and floating CSR access.
Vector operations and compressed encodings from other chapters are outside this scope.

The delivery contains 100 instruction documents, 165 concrete f-register instructions,
84 x-register floating variants, the six named floating CSR aliases in both models,
and six Zicsr operations on the three floating CSR addresses in both models.
There are 297 concrete variant/address rows and 3,355 result formulas.

Each document contains the workflow's eight sections, its own configurations and value
classes, expanded result rules, and a manual-evidence table. All formula rules come from
the included local manuals. Manual corrections to the historical pilot are listed in
[the review notes](reports/scalar-fp-review.md). `workflow.md` registers the additional
symbols and states these corrections; `workflow-original.md` preserves the archive's text.

Rebuild and verify from this directory, using Python 3.12 or newer and no third-party packages:

```bash
python3 -I tools/build_fp_instructions.py --output instructions
python3 -I tools/validate_instructions.py
python3 -I tools/check_fp_semantics.py
```

The manifest records the exact source excerpts, PDF pagination, instruction inventory and
hashes. `scalar-fp-validation.json` records structural/style/coverage/source checks;
`scalar-fp-semantics.json` records bounded arithmetic instantiations across five modes.
The bounded checks do not replace manual evidence or establish an exhaustive proof.
FP memory rules compose with the architectural memory-access relation, including its
translation/protection choices and partial effects. They do not duplicate a complete MMU.
''')
for cmd in [ ['tools/build_fp_instructions.py','--output','instructions'],['tools/validate_instructions.py'],['tools/check_fp_semantics.py'] ]:
 subprocess.run([sys.executable,'-I',str(DEST/cmd[0]),*cmd[1:]],check=True,cwd=DEST)
subprocess.run([sys.executable,'-I',str(DEST/'tools/check_md.py'),str(DEST/'workflow.md')],check=True,cwd=DEST)
provenance={'original_workflow_archive_sha256':hashlib.sha256((ROOT/'fp-formalization-workflow-v1.tar.gz').read_bytes()).hexdigest(),'original_workflow_text_sha256':hashlib.sha256(original.encode()).hexdigest(),'scope':'Unprivileged scalar chapters 21–27, RV32/RV64, floating CSR access'}
(DEST/'reports/provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
archive=ROOT/'riscv-scalar-fp-complete-v1.tar.gz'
with tarfile.open(archive,'w:gz') as ar:
 ar.add(DEST,arcname=DEST.name,filter=lambda info:None if '__pycache__' in info.name else info)
print('Delivery:',DEST)
print('Archive:',archive,'bytes:',archive.stat().st_size)
