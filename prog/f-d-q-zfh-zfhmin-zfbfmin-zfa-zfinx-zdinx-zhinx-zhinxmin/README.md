# 标量浮点程序与 Spike / Sail 差分测试

本目录把 `out/f-d-q-zfh-zfhmin-zfbfmin-zfa-zfinx-zdinx-zhinx-zhinxmin/` 的指令族、操作数类别、舍入配置和扩展守卫实例化为可执行的裸机测试。交付文档与独立解释器各自编写，本目录的测试不修改交付文档。

2026-11-24 实测结果：**706,793 个测试用例，其中 676,879 个在两个模型上比较，Q 配置的 29,914 个用例（含 34 个定向异常用例）仅在 Spike 上运行。两个模型共有 83 个差异：15 个 stateen 异常码分歧，68 个非对齐访存分歧。**

主体九个配置的 706,263 个用例中，两个模型比较了 676,383 个，全部一致；独立数值解释器对这 676,383 个也与两模型无差异。另有 20 个 x0/寄存器对定向测试、45 个 FS 门控测试和 311 个 F/D/Zfh 定向异常测试，两个模型全部一致；120 个 stateen 门控测试中有 15 个 VS/VU 异常码分歧；定向异常套件共 345 个用例，所有有断言的预期在相应模型上均成立，68 个非对齐访存因实现可选而模型选择不同。详见 [结果报告](results/REPORT.md) 和 [机器可读汇总](results/summary.json)。

这些是有限测试的结果，不是对全部位型、特权配置或全部 487 条公式的证明。各项模型比较均使用**同一个 ELF**。

## 1. 生成物

| 路径 | 内容 |
|---|---|
| `generate.py` | 确定性测试生成器；抽取源文档公式编号及内容摘要 |
| `edges.py` | x0、RV32 双寄存器、高位忽略的补充测试生成器 |
| `privilege.py` | M/HS/U/VS/VU 的 FS/stateen 测试生成、编译和执行 |
| `exceptions.py` | 按 riscv-arch-test `testplans/priv` 改编的定向异常测试生成、编译和执行 |
| `generated/<profile>/*.S` | 每个助记符组的汇编程序；`suite.S` 串联执行 |
| `generated/<profile>/cases.json` | 每条测试的编码、输入、舍入、初始标志及对应文档 |
| `generated/<profile>/order.json` | 签名记录与测试 ID 的对应关系 |
| `generated/formula-inventory.json` | 487 个公式标签及源交付内容 SHA-256 |
| `encodings.json` | 指令编码常量快照；生成时填入寄存器和舍入字段 |
| `link.ld` | 两个模型共享的裸机 ELF 布局 |
| `configs/*.json` | Sail 的完整运行配置 |
| `build/<profile>/suite.elf` | 实际运行的 ELF |
| `run.py` | 编译、双模型运行、签名解码和逐项比较 |
| `reference.py` | 独立的精确有理数解释器，不调用主机浮点或 SoftFloat |
| `test_reference.py` | 解释器的数值边界回归测试 |
| `analyze.py` | 数值解释器核查、文档覆盖清单及汇总报告 |
| `results/<profile>/` | 构建/运行命令、返回码、符号、原始签名、解码记录和差异 |
| `results/environment.json` | 模型/编译器版本、路径及二进制 SHA-256 |
| `results/capabilities.json` | Sail 配置能力及 Zdinx 配置变通说明 |
| `results/document-coverage.json` | 按 43 个源指令文件统计的实例与实际执行情况 |
| `results/reference-findings.json` | 独立数值解释器与模型间的差异 |
| `results/privilege-summary.json` | 特权门控逐用例结果与预期异常码 |
| `results/*-exceptions/summary.json` | 定向异常套件的逐用例结果、断言差异与模型间差异 |

## 2. 复现

在本目录执行，Python 不需要第三方包：

```bash
python3 generate.py --random 16
python3 edges.py
python3 test_reference.py
python3 run.py --jobs 3 --timeout 300
python3 privilege.py
python3 exceptions.py
python3 analyze.py
```

生成器默认覆盖 RV32/RV64 的 f 寄存器、Q、x 寄存器，以及 Zfhmin、Zfbfmin、Zhinxmin 的子集配置。`--random 16` 是每个二元指令/格式的随机补充数量，IEEE 类别组合和定向边界另外生成。随机种子固定，重复生成结果一致。

`run.py` 支持单独重跑部分配置，例如：

```bash
python3 run.py --profiles rv64-f rv32-x --jobs 2
```

也可以用 `--spike`、`--sail`、`--cc`、`--nm` 指定工具。程序遇到异常后由 M 模式 trap handler 保存异常码，并从下一条指令恢复；初始化/捕获阶段异常会被识别为测试框架错误。Sail 的 `--inst-limit` 按用例数 × 80 设定（每个用例约 44–48 条指令，留出裕量），超大程序不会被指令上限提前截断。

`run.py` 遇到模型差异、构建/执行失败或框架错误返回非零。`privilege.py` 与 `exceptions.py` 保留差异供报告分析，正常完成框架运行返回零；不能把该返回值理解为门控或异常结果全部一致。`exceptions.py` 中非对齐访存和保留舍入模式没有预期值，只做两模型对照。

## 3. 测试配置与比较内容

| 配置 | 位宽 | 实现条件 | 用例数 |
|---|---:|---|---:|
| `rv64-f` / `rv32-f` | 64 / 32 | F+D+Zfh+Zfhmin+Zfbfmin+Zfa | 各 141,197 |
| `rv64-q` / `rv32-q` | 64 / 32 | 上述配置加 Q，测试 Q 及跨 Q 转换 | 14,971 / 14,909 |
| `rv64-x` / `rv32-x` | 64 / 32 | Zfinx+Zdinx+Zhinx+Zhinxmin | 各 125,655 |
| `rv64-hmin` | 64 | F+D+Zfhmin，未实现 Zfh/Zfa/Zfbfmin | 49,529 |
| `rv64-bfmin` | 64 | F+D+Zfbfmin，未实现 Zfh/Zfhmin/Zfa | 49,529 |
| `rv64-xmin` | 64 | Zfinx+Zdinx+Zhinxmin，未实现 Zhinx | 43,621 |
| `rv32-x-edges` / `rv64-x-edges` | 32 / 64 | 完整 x 寄存器族的定向边界 | 各 10 |
| `rv64-f-privilege` | 64 | H+F+D+stateen，五种执行模式 | 45 |
| `rv64-x-privilege` | 64 | H+Zfinx+stateen，五种执行模式 | 120 |
| `rv64-f-exceptions` | 64 | F+D+Zfh+Zfa 的定向异常 | 311 |
| `rv64-q-exceptions` | 64 | 上述配置加 Q 的定向异常，仅 Spike | 34 |

二元操作覆盖十个 IEEE 类别的笛卡尔积；FMA 覆盖三个操作数的类别笛卡尔积。操作数取值与 riscv-arch-test 的 `cp_fs1/fs2/fs3_edges` 和 `cp_memval_fp_*` 对齐：除 IEEE 类别与正规/次正规边界外，还包括 ±2.5、±2^prec、中间次正规数、负 sNaN、固定伪随机正规数，并让这些值分别出现在二元指令的每个操作数槽、FMA 的三个槽，以及单目、转换、访存路径。

边界值集合逐字收录 ACT4（riscv-arch-test）`FLOAT_EDGES` 的 28 个值（H、S、D、BF16 各 28 个），并保留本程序原有的额外值；两侧并集后，`FADD`/`FSUB`/`FMUL`/`FDIV` 对 28 个边界值生成**全部 28 × 28 = 784 个有序配对**，每个配对再完整交叉 DYN 与五种静态舍入（共 4,704 个用例/指令/格式）；比较、min/max、符号注入等其余二元指令同样生成全部 784 个有序配对（与已有类别/边界对重合的不再重复）。FMA 让两个乘数与加数分别对全部 28 个边界值交叉。

寄存器编号按 ACT4 `cp_fs1/fs2/fs3/fd` 的方式遍历：`rs1` 取 0、1、15、31，`rs2` 取 0、31，`rd` 取 0、1、31（`FEQ` 等写整数寄存器的指令不改 `rd`），并让目的寄存器与每个源寄存器取同一编号（FMA 六种两两相等组合），别名槽位填同一数值，使结果与装载次序无关。

不规范装箱（bad NaN-boxing）按操作数单独构造：只坏 rs1、只坏 rs2、只坏 rs3、三个全坏，上部位分别使用多种非全一的垃圾位型；覆盖算术、位传送、比较、分类、FMA 和向更宽格式/整数的转换。另按 ACT4 的 `bad_NaN_*` 图像逐个展开：D→S、D→H 各 14 个 S/D 容器位型（含零、正规边界、无穷与 NaN 的低位）与 S→H 的 14 个半精度容器位型，用于算术、比较、min/max、符号注入、开方、FMA 与相关转换，覆盖 ACT4 使用的全部坏装箱图像。

整数源取 ACT4 `get_general_edges(XLEN)` 的全部边界（含 `2^31-2`、`0x5bbc8872`、完整 64 位交替模式、`0x100000001`）。访存指令对 12 位立即数边界集的 19 个非零值（`±1`、`±2047`、`2048`、`1023` 等）各生成一次，其余用例取 `imm=0`；汇编端在同一基址下补偿 `la` 偏移，使有效地址保持不变。CSR 写操作枚举 frm 0–7、fflags 0–31 与逐位 walking-one，并在五种初始 fcsr 状态下重复。此外，`FADD`/`FSUB`/`FMUL`/`FDIV` 的五分之一边界配对预置该指令可能触发的粘性标志（NV/OF/UF/NX，除法另加 DZ），用于检查标志只置位、不清零；其余舍入覆盖仍包括静态五种舍入、DYN 选择五种合法 frm，以及 FLI 的全部 32 个索引。

另有一组极端量级跨度用例：一个操作数取格式的最大有限数（±MAX），另一个取最小次正规数或最小正规数（±MIN_SUB、±MIN_NORM），正负号与前后位置都取到，并让二元指令的两个操作数槽、FMA 的乘数位与加数位都和全部十种舍入配置交叉。小操作数完全落在大量级操作数的舍入网格之外，用来检查粘性标志（NX/OF）、溢出方向以及向零/向上/向下舍入的差别；乘除的这类组合则检查跨约 2·emax 指数的结果。

另有一组极端量级跨度用例：一个操作数取格式的最大有限数（±MAX），另一个取最小次正规数或最小正规数（±MIN_SUB、±MIN_NORM），正负号与前后位置都取到，并让二元指令的两个操作数槽、FMA 的乘数位与加数位都和全部十种舍入配置交叉。小操作数完全落在大量级操作数的舍入网格之外，用来检查粘性标志（NX/OF）、溢出方向以及向零/向上/向下舍入的差别；乘除的这类组合则检查跨约 2·emax 指数的结果。

每条主体用例有 64 字节签名：

| 偏移 | 内容 |
|---:|---|
| 0–15 | 目的寄存器原始内容；包含适用的装箱/符号扩展；未使用字节为零 |
| 16–19 | 指令执行后的完整 fcsr |
| 20–23 | 目标指令执行后、捕获操作之前的 FS |
| 24–27 | 同步异常码；0 表示本次目标指令没有异常 |
| 28–31 | 测试 ID |
| 32–47 | 测试内存区；特权补充程序另用于保存模式边界信息 |
| 48–55 | 发生异常的目标 PC，正常路径为零 |
| 56–63 | misa，用于检查 x 寄存器配置未报告 F/D/Q |

定向异常套件沿用 64 字节记录，但字段含义不同：偏移 0–15 始终是 f25（访存目的是 scratch），16–19 为恢复 FS 后的 fcsr，32–35 保存原始 ECALL 码，36–47 为 scratch 前 12 字节；异常套件用字节 32 区分“目标指令触发异常”和“正常执行到结束”。

两个模型精确比较目的寄存器、fcsr、异常码和内存。FS 单独报告，以便区分状态跟踪策略。正常路径的算术结果与异常路径上的目的保持都可在原始签名中检查。每条记录均核对 ID；出现异常时再核对 PC，避免把加载操作数失败误计为目标指令异常。Sail 必须报告 `SUCCESS`；仅达到指令上限不算完成。

## 4. 实测分歧

**stateen 异常码：** `mstateen0.FCSR=1` 时，VS 被 `hstateen0.FCSR=0` 拒绝的 6 个场景，以及 VU 被 hstateen0/sstateen0 拒绝的 9 个场景，Spike 返回 22，本地 Sail 返回 2。测试涉及 FADD.S、FCLASS.S 和 FRCSR。两模型都能正常执行同组允许配置；ECALL 的异常码还用于检查是否确实进入指定模式。全部实例见 `results/rv64-x-privilege/summary.json`。

**定向异常：** 按 riscv-arch-test `testplans/priv` 的异常覆盖点构造。`mstatus.FS=00` 时，37 种浮点指令形式和 fcsr/frm/fflags 的读/写/置位/清零共 12 种 CSR 访问全部触发非法指令；`FS=01/10/11` 与 frm 0-4 的全部采样组合正常执行；未映射地址 0 的访存分别触发 5（load）和 7（store）。保留舍入模式的用例只做两模型对照：静态 rm=5/6 和 DYN 配 frm=5/6/7 时两模型都报非法指令，frm 0-4 正常执行。唯一分歧是非对齐浮点访存：16 种低 4 位偏移中所有非自然对齐地址，Spike 报 cause 4/6，本地 Sail 完成访问（34 个 load、34 个 store，共 68 个）。RISC-V 允许实现选择是否支持非对齐访问，两种行为都合规。

**舍入边界：** riscv-arch-test 的 `cp_underflow_after_rounding` 向量（包括 D→S 输入 `0x380fffffe8000000`）在 Spike、Sail 和独立解释器上一致：交付值虽为 S 的最小正规数 `0x00800000`，仍置 UF+NX。原因是 tininess 判定使用独立的、无指数上限的舍入（交付 README §6.1，Unpriv. §25.3.2.6.1）；最终网格的舍入只决定交付值。全部主测试中，独立解释器与两模型均无差异。

## 5. 工具能力与边界

本次 Spike 为本地 `~/opt/spike/bin/spike`；Sail 为 `~/projects/testkit4rv/builtin/sail/sail_riscv_sim`，版本 0.15，构建信息为 `0.15-dirty`，旁边有本地适配补丁。因此报告中的 Sail 指这份实际二进制，不能直接概括为所有 Sail 版本。

该 Sail 的配置 schema 没有 Q，故 Q 程序只在 Spike 上执行：数值配置与独立解释器核对，定向异常配置按预期异常码检查；没有把 Sail 的非法指令结果算作 Q 比较通过。

该 Sail 的 `model/core/flen.sail` 只按 `D.supported` 分配 32/64 位辅助类型，没有计入 Zdinx。纯 Zdinx 配置会在 D 操作处触发 `fdext_regs.sail:291` 的内部断言。本次比较采用显式配置变通：x 寄存器配置设置 `D.supported=true` 以分配 64 位辅助存储，同时保留 `F.supported=false` 和 Zfinx/Zdinx。每条主体记录都检查 `misa.F/D/Q=0`。这是配置层变通，没有修改模拟器源代码或二进制；最初失败的运行信息保存在 `results/capability-probes/`。

独立解释器是人工编写的公式语义解释，不是机械翻译、验证过的证明器或第三个权威模型。它使用有理数及整数平方根，支持包括 binary128 在内的数值计算。所有 43 个源指令文件均有对应程序实例，但没有宣称 487 条结果式逐条可达或全部覆盖。

主体测试采用小端、M 模式、Bare 翻译；补充程序覆盖 M/HS/U/VS/VU 的 FS 与 stateen 门控，以及 M 模式的 FS/CSR 非法指令门控、合法与保留 frm、非对齐访存和未映射地址访问故障。分页/客户机页故障、数据断点、PMP 拒绝区域（改用未映射地址）、异常前部分写入和中断期间的异常没有覆盖；保留舍入模式只做观测对照。
