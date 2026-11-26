# RISC-V 标量浮点形式化（中文译本）

> 本文件是
> [`README.md`](README.md)
> 的中文译本，供阅读使用；英文原文为准。产出目录本身保持英文，本译本不属于交付内容。

本目录形式化 RISC-V 指令集手册中标量浮点的全部内容：第 21 章（`F`）、第 22 章（`D`）、
第 23 章（`Q`）、第 24 章（`Zfh`/`Zfhmin`）、第 25 章（`Zfbfmin`，标量 BF16）、第 26 章
（`Zfa`）以及第 27 章（`Zfinx`/`Zdinx`/`Zhinx`/`Zhinxmin`）。覆盖取数、存数、算术、符号注入、
最小/最大、比较、分类、转换、传送、浮点 CSR 指令以及整数寄存器形式。

每个指令文件只含公式：每个可区分的结果类别一条公式。所有共享材料——符号、格式、操作数类别、
舍入规则、状态规则、异常码——都在本文件中定义一次。只以本文件为背景，就能读懂指令文件中的
任一公式。

每个文件建模其指令的 32 位编码。压缩编码（`C.FLW`、`C.FSW` 及其他 `C.*` 形式）属于另外的
ISA 章节，不在此建模。

## 1. 公式形态

每条公式形如

$$
\text{特权配置}\ \land\ \text{扩展配置}\ \land\ \text{浮点 CSR}\ \land\ \text{操作数}\ \land\ \mathrm{instr}=I
\ \longrightarrow\
\{\, \text{更新} \,\}.
$$

左端各组始终按此顺序出现；某条指令没有的组留空，其余组保持位置。指令合取项永远在最后。

每条公式左端的第一行固定特权执行配置；右端按顺序列出：目的（`fd`、`rd`、内存或 CSR）、
浮点状态改变时 §6.2 的 `FS` 写、粘性标志增量 `fcsr.fflags \mathrel{|}= S`，以及最后的
`exception`。

每条指令的公式 0 是纯异常配置：扩展不可用或有效 `FS` 为 Off 时，指令不写任何状态，抛出
`IllegalInstruction(2)`。在 `zfinx.md` 中用 `stateen` 门控替代 `FS` 项，另有一个守卫覆盖抛
`VirtualInstruction(22)` 的 VS/VU 情形。取数、存数在其地址异常公式之前也有同样的公式 0。
每条指令也可能在译码之前陷入；因此每条公式的 `exception` 字段都以 §7.1.2 的取指结果开头，
右端的寄存器、`FS`、内存与标志更新仅当链中任何码都不发生时才会出现。

在 `f` 寄存器文件中，每个结果类别出现三次，每种特权配置一次，每份副本左端第一行固定该配置。
是否实现 hypervisor 扩展 `H` 决定存在哪些模式名（Priv. 表 1，`sources/riscv-privileged.txt:748-752`；
表 44，`sources/riscv-privileged.txt:8719-8727`）：

| 特权行 | 配置 |
|---|---|
| `¬impl(H) ∧ Priv∈{M,S,U}` | 未实现 hypervisor 扩展：supervisor 模式为 `S` |
| `impl(H) ∧ Priv∈{M,HS,U}` | 已实现 hypervisor 扩展，`V=0`：supervisor 模式为 `HS` |
| `impl(H) ∧ (Priv∈{VS,VU} ∧ vsstatus.FS∈{1,2,3} ∧ sstatus.FS∈{1,2,3})` | 已实现 hypervisor 扩展，`V=1`：guest 运行在 `VS` 或 `VU` |

在前两种配置中，唯一的浮点门控是后面的 `mstatus.FS` 合取项。第三种中，guest 字段和 HS 级
字段都必须使能；由于 `sstatus.FS` 就是 `mstatus.FS`，后面的 `mstatus.FS` 合取项是同一字段。
每个块固定一种配置，因此右端只写该配置的 `FS`。这三行加上 `mstatus.FS` 合取项，恰好穷尽
公式 0 中特权与 `FS` 析取项的否定：每种特权配置要么进入某个结果块，要么抛出
`IllegalInstruction(2)`。

## 2. 符号

以下是各指令文件使用的全部符号。新增符号必须先登记于此。

| 符号 | 含义 | 取值/形式 | 出处 |
|---|---|---|---|
| `Priv` | 当前特权模式 | `U`、`S`、`HS`、`M`、`VS`、`VU` | Priv. 表 1 与表 44 |
| `mstatus.FS` | 浮点状态，M/HS/U 视图 | `Off(0)`、`Initial(1)`、`Clean(2)`、`Dirty(3)` | Priv. 表 13 |
| `sstatus.FS` | HS 级视图；与 `mstatus.FS` 为同一字段 | 同上 | Priv. §15.2.11 |
| `vsstatus.FS` | VS/VU 中的浮点状态 | 同上 | Priv. 表 13 |
| `misa.F` | `misa` 的 F 位 | 0、1 | Priv. §3.1.1 |
| `\mathrm{stateen}` | stateen CSR 已实现 | 布尔 | Priv. §4.2 |
| `mstateen0.FCSR` | `fcsr` 访问位，机器视图；控制 M 以下的所有模式 | 0、1 | Priv. §4.2 |
| `hstateen0.FCSR` | `fcsr` 访问位，hypervisor 视图；控制 VS 与 VU | 0、1 | Priv. §4.2 |
| `sstateen0.FCSR` | `fcsr` 访问位，supervisor 视图；控制 U 与 VU | 0、1 | Priv. §4.2 |
| `impl(X)` | 扩展 X 已实现 | 布尔；X 为手册中的扩展名 | Priv. §3.1 与各扩展章节 |
| `Ext(F)` | 提供格式 F 的扩展 | 见 §4 | — |
| `instr` | 正在执行的指令 | 带格式后缀的助记符 | — |
| `instr.rm` | 编码中的舍入字段 | `RNE(0)`…`RMM(4)`、5、6、`DYN(7)` | Unpriv. 表 24 |
| `fcsr.frm` | 动态舍入模式 | `RNE(0)`…`RMM(4)`、5、6、7 | Unpriv. 表 24 |
| `fcsr.fflags` | 粘性浮点标志 | `NV(4)`、`DZ(3)`、`OF(2)`、`UF(1)`、`NX(0)` | Unpriv. §21.2 |
| `exception` | 按优先级排列的同步异常结果 | 用 `>`（左码优先级更高）、`=`（优先级相同）连接的码链，块能抛异常时末端是该块自身的码，否则止于取指链；`\mathrm{fetch}`、`\mathrm{walk}`、`\mathrm{phys}`、`\mathrm{data}` 标注手册中重复的两行 | §7.1.1、§7.1.2 |
| `\mathrm{fetch}`、`\mathrm{walk}`、`\mathrm{phys}`、`\mathrm{data}`、`\mathrm{lowest}` | 异常码的行来源标签；本文档的简写，不是手册术语——手册只用表 17、表 51 的行标题描述区分这些行 | `fetch`：指令地址断点行（`:10540`）；`data`：数据地址断点行（`:10550`），或码 5/7 的最终访问行（`:10556`）；`walk`：码 1/5/7 的地址转换行（`:10542`、`:10554`）；`phys`：码 1/5/7 的物理地址行（`:10544`、`:10556`）；`lowest`：第二条未对齐行（`:10558`） | Priv. 表 17、表 51 |
| `F` | 格式参数 | `H`、`S`、`D`、`Q` | — |
| `a`、`b` | 源操作数 | `f[rs1]`、`f[rs2]` 正确装箱后低 $w_F$ 位的三元组 $(s,e,f)$；转换的源格式 `G` 用 $w_G$ | §5.1、§5.4 |
| `c` | FMA 的第三个乘数 | 同样从 `f[rs3]` 读取 | §5.1、§5.4 |
| `w_F`、`w_e`、`w_f` | 格式 `F` 的总位宽、指数位宽、有效数位宽；第二种格式 `G` 用 `w_G`、`w_{e,G}`、`w_{f,G}` | 按格式 | §5.1 |
| `e_{\max}`、`f_{\max}` | 格式 `F` 的最大偏置指数与最大有效数；转换的源格式 `G` 用 `e_{\max,G}`、`f_{\max,G}` | `2^{w_e}-1`、`2^{w_f}-1` | — |
| `E_{\min}`、`E_{\max}` | 最小与最大无偏指数 | 按格式 | §5.1 |
| `\mathrm{val}_F(a)` | 位域三元组的值 | 分段 | §5.2 |
| `x`、`y`、`z` | 源的数值 | `\mathrm{val}_F(a)` 等 | — |
| `\mathrm{exact}` | 舍入前的精确结果 | 按指令 | — |
| `\mathrm{rounded}` | `\mathrm{exact}` 按有效模式正确舍入 | 分段 | §6.1 |
| `\mathrm{round}_{F,m}(v)` | 按模式 `m` 在格式网格上把 `v` 舍入到格式 F，含次正规步长；`MAX` 之上不设指数上限 | — | §6.1 |
| `\mathrm{round}^{\infty}_{F,m}(v)` | 按模式 `m` 把 `v` 舍入到格式 F 的精度，两端都不设指数上限；仅用于 tiny 判定 | — | §6.1 |
| `\mathrm{tiny}` | 舍入后判定的下溢，针对指令的目的格式：`0<\lvert\mathrm{round}^{\infty}_{F,m}(\mathrm{exact})\rvert<2^{E_{\min}}` | 布尔 | Unpriv. §21.4、§25.3.2.6.1 |
| `\mathrm{FLEN}` | 浮点寄存器宽度 | 实现定义 | Unpriv. §22.2 |
| `\mathrm{XLEN}` | 整数寄存器宽度 | 32 或 64 | Unpriv. §1.2 |
| `\mathrm{qNaN}_F` | 规范 quiet NaN | `s=0`、`e=e_{\max}`、`f=2^{w_f-1}` | Unpriv. §21.3 |
| `\mathrm{sNaN}`、`\mathrm{qNaN}` | 输入 NaN 类别 | 见 §5.2 | — |
| `+\infty_F`、`-\infty_F` | 无穷结果类别 | 按格式 | — |
| `+0_F`、`-0_F` | 零结果类别 | 按格式 | — |
| `0_F(p)` | 格式 `F` 中符号位为 `p` 的零：`p=0` 时为 `+0_F`，`p=1` 时为 `-0_F` | `p` 为 0 或 1 | — |
| `+\mathrm{MAX}_F`、`-\mathrm{MAX}_F` | 最大有限结果类别 | 按格式 | — |
| `fd`、`fs1`、`fs2`、`fs3` | 浮点寄存器 | 寄存器标识符 | — |
| `rd`、`rs1`、`rs2`、`rs3` | 整数寄存器 | 寄存器标识符 | — |
| `f[i]`、`x[i]` | 寄存器堆项 | 宽度 `FLEN` / `XLEN` | — |
| `mem[a,w]` | 地址 `a` 处的 `w` 位内存字 | 小端位向量 | Unpriv. §1.4 |
| `imm` | 编码中的立即数字段 | 按指令 | — |
| `u` | 类型 `T` 的整数操作数值 | `W`/`L` 为二补码，`WU`/`LU` 为无符号；`FCVT.F.T` 绑定 `u=\mathrm{sext}_n(x[\mathrm{rs1}][n-1:0])`（`W`/`L`）或 `u=\mathrm{zext}_n(x[\mathrm{rs1}][n-1:0])`（`WU`/`LU`）；`FCVT.T.F` 以 `\mathrm{enc}_T(u)` 写出 | §5.1，Unpriv. §21.7 |
| `n` | 类型 `T` 的位宽 | `W`/`WU` 为 32；`L`/`LU` 为 64，其公式块要求 `\mathrm{XLEN}=64` | Unpriv. §21.7 |
| `T` | 浮点—整数转换的整数类型 | `W`、`WU`、`L`、`LU` | Unpriv. §21.7 |
| `\min T`、`\max T` | 类型 `T` 的最小值与最大值 | `W`：$-2^{31}$、$2^{31}-1$；`WU`：$0$、$2^{32}-1$；`L`：$-2^{63}$、$2^{63}-1$；`LU`：$0$、$2^{64}-1$ | Unpriv. 表 27 |
| `I` | 家族文件中所讨论的指令 | 带格式后缀的助记符 | — |
| `G` | 浮点转换的源格式 | `H`、`S`、`D`、`Q` | — |
| `\mathrm{fcsr}` | 浮点控制与状态寄存器 | 32 位寄存器 | Unpriv. §21.1 |
| `\mathrm{Extm}(F)` | 提供 H 转换子集的扩展 | `Zfhmin`、`F`、`D`、`Q` | §4 |
| `\mathrm{Extx}(F)` | 提供格式 F 的 x 寄存器扩展 | `Zhinx`、`Zfinx`、`Zdinx` | §4 |
| `\mathrm{EA}` | 取数或存数的有效地址 | $(x[\mathrm{rs1}]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}}$，在每个访存块左端绑定 | §5.1 |
| `\mathrm{PC}` | 正在取指的指令地址 | 指令地址 | Unpriv. §2.2 |
| `\mathrm{sext}_n`、`\mathrm{zext}_n` | 符号扩展与零扩展到 $n$ 位 | — | — |
| `\mathrm{low}_n(v)`、`\mathrm{high}_n(v)` | `v` 的低 $n$ 位及其上的各位 | — | — |
| `\mathrm{raw}_F(v)` | 值或类别的 $w_F$ 位 IEEE 编码 | — | — |
| `\mathrm{box}_F`、`\mathrm{enc}_F(v)` | 装箱到 `FLEN` 位及其结果 | — | §5.4 |
| `\mathrm{boxed}_F(v)` | 寄存器映像是否已正确 NaN 装箱 | $\mathrm{FLEN}=w_F$ 或 $v[\mathrm{FLEN}-1:w_F]=1^{\mathrm{FLEN}-w_F}$；`G`、`D`、`S`、`B` 为其余格式名下的同一谓词 | §5.4、Unpriv. §22.2 |
| `\mathrm{senc}_F(v)` | $w_F$ 位编码符号扩展到 `XLEN` | — | §5.4 |
| `\mathrm{xop}_F(i)` | `Zfinx` 下从 `x[i]` 读出的源操作数 | 分段；$w_F=2\,\mathrm{XLEN}$（RV32Zdinx 的 `D`）读对齐寄存器对 `x[i]`:`x[i+1]`，`i=0` 读零 | §5.4、Unpriv. §27.3 |
| `\mathrm{xwr}_F(i,v)` | `Zfinx` 下把 $v$ 写入 `x[i]` 的结果集元素 | 分段；展开为一条或两条寄存器赋值，经 `x0` 写时保持 `x[0]=0` | §5.4、Unpriv. §27.3 |
| `\mathrm{enc}_T(u)` | $T$ 类型写回后的整数值：`XLEN=32` 时各类型都写 $u$；`XLEN=64` 时 `W` 与 `WU` 都写 $\mathrm{sext}_{64}(\mathrm{low32}(u))$，而 `L` 与 `LU` 写 $u$ | `T` 为 `W`、`WU`、`L`、`LU` | Unpriv. §21.7 |
| `\mathrm{roundInt}(x)` | 按有效模式把 $x$ 舍入为整数 | — | — |
| `\mathrm{ires}` | 截断到范围之前的舍入整数 | — | — |
| `\mathrm{trunc}(x)` | 把 $x$ 向零截断 | — | — |
| `\mathrm{low32}(v)` | 整数的低 32 位 | — | — |
| `\min_\prec`、`\max_\prec` | 全序下的最小值与最大值 | §5.3.1 | — |
| `\mathrm{FLI}_F(imm)` | 由 FLI 立即数选出的常量 | §2.1 | Unpriv. §26.1 |

十种 IEEE 值类别（quiet/signaling NaN、两个无穷、两个零、正规、次正规）不是单独的符号：
公式用 $e_{\max}$ 与 $f_{\max}$ 把它们写成 $s,e,f$ 上的范围。

### 2.1 FLI 常量

$\mathrm{FLI}_F(imm)$ 从下表 32 个常量中选一个（Unpriv. 表 35，
`sources/riscv-unprivileged.txt:8470-8576`）。第 1 项是目的格式的最小正规格数，因此在 H、S、D、Q
之间不同；其余各项在四种格式下数值相同，唯一例外是第 29 项：在 S、D、Q 中是 $2^{16}$，
而在 H 中是 $+\infty_F$，因为 $2^{16}$ 在 H 中不可表示。第 2、3 项在 H 中是次正规数。

| `imm` | 值 | `imm` | 值 |
|---:|---|---:|---|
| 0 | $-1$ | 16 | $1$ |
| 1 | $2^{E_{\min}}$ | 17 | $1.25$ |
| 2 | $2^{-16}$ | 18 | $1.5$ |
| 3 | $2^{-15}$ | 19 | $1.75$ |
| 4 | $2^{-8}$ | 20 | $2$ |
| 5 | $2^{-7}$ | 21 | $2.5$ |
| 6 | $2^{-4}$ | 22 | $3$ |
| 7 | $2^{-3}$ | 23 | $4$ |
| 8 | $2^{-2}$ | 24 | $8$ |
| 9 | $0.3125$ | 25 | $16$ |
| 10 | $0.375$ | 26 | $128$ |
| 11 | $0.4375$ | 27 | $256$ |
| 12 | $0.5$ | 28 | $2^{15}$ |
| 13 | $0.625$ | 29 | $2^{16}$（H：$+\infty$） |
| 14 | $0.75$ | 30 | $+\infty$ |
| 15 | $0.875$ | 31 | $\mathrm{qNaN}_F$ |

## 3. 写作规则

1. 一条结果公式是一个 display 块，只含一个 `aligned` 环境；左端每行以 `&` 开头。
2. 每行至多一个顶层 `\land`；括号内的 `\land` 不计。
3. `\longrightarrow` 分隔左右两端；右端是 `\{\, … \,\}`，字段以逗号分隔。
4. 右端顺序：目的、`FS` 写、标志、`exception`；异常永远最后。一种配置更新多个状态字段时，
   把它们作为逗号分隔的结果列出，因为列出的每个结果都会发生；`\land` 只用于左端。
5. 多字母名称用 `\mathrm{}`；单字母操作数符号与下标用斜体（$s_a$、$e_a$、$f_a$）；格式下标为
   $H$、$S$、$D$、$Q$，参数化时用 $F$。
6. 枚举写 `Name(code)`，中间无空格；集合写 `\{…\}`；空集写 `\varnothing`；单元素集写 `\{X\}`。
7. 逻辑记号只用 `\land`、`\lor`、`\neg`、`\longrightarrow`、`\in`、`\notin`、`=`、`\ne`、
   `\le`、`<`、`\ge`、`>`；不使用文字连接词。
8. 派生符号以 `\mathrm{name}=…` 定义一次，之后作为整体使用，不在公式内联展开。
9. 结果是 IEEE 类别或正规/次正规值 $r$，绝不写位型。唯一例外是按位逐字拷贝的指令——符号注入、
   传送与 `FCLASS`——它们的结果写成位域三元组 `(s,e,f)` 或整数字。
10. 表格单元内不得出现含竖线的行内数学。
11. 特权配置是左端第一行，取 §1 三种之一：`¬impl(H) ∧ Priv∈{M,S,U}`、
    `impl(H) ∧ Priv∈{M,HS,U}` 或
    `impl(H) ∧ (Priv∈{VS,VU} ∧ vsstatus.FS∈{1,2,3} ∧ sstatus.FS∈{1,2,3})`。右端只写该配置的
    `FS`（§6.2）。

不允许隐藏的析取谓词。特别是舍入模式的合法性，每次都要在 `instr.rm` 与 `fcsr.frm` 上写开。
操作数类别上的辅助谓词同样禁止：直接在 $s,e,f$ 上写范围。

## 4. 格式与扩展

| 格式 | 扩展 `Ext(F)` | `w_F` | `w_e` | `w_f` | `E_{\min}` | `E_{\max}` |
|---|---|---:|---:|---:|---:|---:|
| H | `Zfh` | 16 | 5 | 10 | $-14$ | $15$ |
| S | `F` | 32 | 8 | 23 | $-126$ | $127$ |
| D | `D` | 64 | 11 | 52 | $-1022$ | $1023$ |
| Q | `Q` | 128 | 15 | 112 | $-16382$ | $16383$ |

`D` 蕴含 `F`，`Q` 蕴含 `D`，`Zfh`、`Zfhmin`、`Zfbfmin` 各自蕴含 `F`，因此对四种格式都提供的
指令，一个 `impl(Ext(F))` 合取项就足够。

在这些公式中 $F$ 是格式变量，不是 `F` 扩展：每个块是 $F$ 上的模式（schema），助记符固定取值。
`FADD.D` 即 $F=D$，其格式合取项为 `impl(Ext(D))`，也就是 `impl(D)`，指令合取项为
`instr=FADD.D`。`F` 扩展本身用正体书写，如下面 `FLW`/`FSW` 行的 `impl(F)`；斜体 $F$ 始终在
H、S、D、Q 上取值。

`impl(X)` 表示扩展 `X` 已实现。模型不为 `misa` 报告的值另设谓词：这里考虑的每种配置中 `misa`
都如实报告已实现的扩展，因此 `impl(F)` 蕴含 `misa.F=1`。这对 `stateen` 很重要：当 `misa.F=1`
时，`mstateen0.FCSR` 为只读零、不门控任何东西；但实现可以把 `misa` 硬连为零（Priv. §3.1.1，
`sources/riscv-privileged.txt:1578-1583`），这时该位可写，且为零时*所有*浮点指令都抛非法指令
异常，无论使用 `f` 还是 `x` 寄存器（Priv. §4.2，`sources/riscv-privileged.txt:4692-4699`）。
`zfinx.md` 为 x 寄存器形式写出该门控；在 `misa` 读零的配置中，`f` 寄存器文件会带同样的合取项。

`\mathrm{impl}(H)` 是 Priv. 第 15 章的 hypervisor 扩展，不是 16 位格式 `H`（该格式的扩展是
`Zfh`，即 $\mathrm{Ext}(H)=\mathrm{Zfh}$）：格式本身绝不单独出现在 `impl(...)` 里。模式名
`HS`、`VS`、`VU` 只在实现 `H` 时存在；未实现时 supervisor 模式为 `S`（Priv. 表 1，
`sources/riscv-privileged.txt:748-752`；表 44，`sources/riscv-privileged.txt:8719-8727`）。

`Zfhmin` 只提供第 24.6 章的数据传送与转换指令，不提供算术指令。BF16（`Zfbfmin`）提供
`bf16.md` 中的两条转换，以及第 24 章的四条 16 位传送指令 `FLH`、`FSH`、`FMV.X.H`、`FMV.H.X`；
BF16 不属于四格式族，显式写出。

BF16 宽 16 位、8 位指数、$w_{f,B}=7$ 位有效数，$E_{\min,B}=-126$、$E_{\max,B}=127$；其类别带
下标 $B$：$\mathrm{qNaN}_B$、$+\infty_B$、$+0_B$、$\pm\mathrm{MAX}_B$。x 寄存器扩展的格式映射为
$\mathrm{Extx}(H)=\mathrm{Zhinx}$、$\mathrm{Extx}(S)=\mathrm{Zfinx}$、$\mathrm{Extx}(D)=\mathrm{Zdinx}$；
不存在 `Zqinx`，因此 `zfinx.md` 只覆盖 H、S、D。

$\mathrm{Extm}(F)$ 是提供 H 转换子集的最小扩展：$\mathrm{Extm}(H)=\mathrm{Zfhmin}$，S、D、Q
时 $\mathrm{Extm}(F)=\mathrm{Ext}(F)$。它是每条涉及 H 的 `FCVT` 转换的实现条件，因为 `Zfhmin`
已经包含这些 H 转换，而 H 算术指令需要 `Zfh`（Unpriv. §24.6，
`sources/riscv-unprivileged.txt:7786-7799`）。四条 16 位传送指令 `FLH`、`FSH`、`FMV.X.H`、
`FMV.H.X` 由 `Zfhmin`（第 24 章）与 `Zfbfmin`（第 25.4.1 章）各自独立提供，因此其条件是析取
`impl(Zfhmin) ∨ impl(Zfbfmin)`（`sources/riscv-unprivileged.txt:8109-8110`）。

逐指令的格式可用性：

| 指令组 | 格式 | 扩展条件 |
|---|---|---|
| 算术、符号注入、最小/最大、比较、分类 | H、S、D、Q | `impl(Ext(F))` |
| `FMINM`、`FMAXM`、`FROUND`、`FROUNDNX`、`FLEQ`、`FLTQ`、`FLI` | H、S、D、Q | `impl(Ext(F)) ∧ impl(Zfa)` |
| `FCVTMOD.W.D` | D | `impl(D) ∧ impl(Zfa)` |
| `FLW`/`FSW` | S | `impl(F)` |
| `FLD`/`FSD` | D | `impl(D)` |
| `FLQ`/`FSQ` | Q | `impl(Q)` |
| `FLH`/`FSH` | H | `impl(Zfhmin) ∨ impl(Zfbfmin)` |
| `FMV.X.W`/`FMV.W.X` | S | `impl(F)` |
| `FMV.X.D`/`FMV.D.X` | D | `impl(D)` |
| `FMV.X.H`/`FMV.H.X` | H | `impl(Zfhmin) ∨ impl(Zfbfmin)` |
| `FMVH.X.D`/`FMVP.D.X` | D | `impl(D) ∧ impl(Zfa)` |
| `FMVH.X.Q`/`FMVP.Q.X` | Q | `impl(Q) ∧ impl(Zfa)` |
| `FCVT.dst.src` | H、S、D、Q | `impl(Extm(F)) ∧ impl(Extm(G))` |
| `FCVT.BF16.S`、`FCVT.S.BF16` | BF16 | `impl(F) ∧ impl(Zfbfmin)` |
| `FRCSR`、`FSCSR`、`FRRM`、`FSRM`、`FRFLAGS`、`FSFLAGS` | — | `impl(F) ∧ impl(Zicsr)` |
| 上述指令的 x 寄存器形式（不含传送） | H、S、D | `impl(Extx(F)) ∧ impl(Zicsr)` |

在 x 寄存器家族中，仅 `Zhinxmin` 提供 `FCVT.S.H`/`FCVT.H.S`，并在 `Zdinx` 存在时提供
`FCVT.D.H`/`FCVT.H.D`——与 `Zfhmin` 的 H 转换子集对应；该家族其他 H 指令都需要 `Zhinx`
（Unpriv. §27.5）。

`FADD.H` 及其他 H 算术指令需要 `Zfh`，因此在每个可用配置中 `misa.F=1`。只要 `misa.F=1`，
`mstateen0.FCSR` 就是只读零，没有 stateen 位门控，也不会出现虚拟指令异常。`f` 寄存器文件的
任何公式都不带 stateen 合取项；`misa.F=0`、stateen 门控生效的 Zfinx 形式由 `zfinx.md` 处理。

stateen CSR 只控制更低特权模式（Priv. §4.1），因此 M 模式永不受 `mstateen0` 门控。Zfinx 形式
的控制位为：HS 模式用 `mstateen0.FCSR`，U 模式用 `mstateen0.FCSR` 与 `sstateen0.FCSR`，
VS 模式用 `mstateen0.FCSR` 与 `hstateen0.FCSR`，VU 模式三者共同控制（Priv. §4.2，
`sources/riscv-privileged.txt:4556-4562`、`4575-4577`）。`mstateen0` 为零在 M 以下的每种模式
都是非法指令条件；而 `hstateen0` 或 `sstateen0` 从 VS 或 VU 访问时为零，抛
`VirtualInstruction(22)`。

## 5. 操作数

### 5.1 位域

每个操作数是三元组 $a=(s_a,e_a,f_a)$：符号、偏置指数、尾随有效数（不含隐藏位）。
$e_{\max}=2^{w_e}-1$，$f_{\max}=2^{w_f}-1$。`f` 寄存器源取其低 $w_F$ 位的三元组，
且每条公式都要求该寄存器正确装箱（§5.4）；这一要求由指令文件开头那些 `¬boxed` 块承担，
其后的块只写字段条件。`Zfinx` 的 `x` 寄存器源为
$a=\mathrm{xop}_F(\mathrm{rs1})$，不做装箱检查。取数/存数绑定
$\mathrm{EA}=(x[\mathrm{rs1}]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}}$。`FCVT.F.T` 的整数源按类型绑定为
$u=\mathrm{sext}_n(x[\mathrm{rs1}][n-1:0])$（有符号类型）或 $u=\mathrm{zext}_n(x[\mathrm{rs1}][n-1:0])$（无符号类型），
$n$ 为该类型的位宽（Unpriv. §21.7，`:7107-7113`）。

### 5.2 值类别

| 类别 | 条件（$s$ 为 0 或 1） |
|---|---|
| $-\infty_F$ | $s=1,\ e=e_{\max},\ f=0$ |
| 负正规数 | $s=1,\ 1\le e\le e_{\max}-1$ |
| 负次正规数 | $s=1,\ e=0,\ 1\le f\le f_{\max}$ |
| $-0_F$ | $s=1,\ e=0,\ f=0$ |
| $+0_F$ | $s=0,\ e=0,\ f=0$ |
| 正次正规数 | $s=0,\ e=0,\ 1\le f\le f_{\max}$ |
| 正正规数 | $s=0,\ 1\le e\le e_{\max}-1$ |
| $+\infty_F$ | $s=0,\ e=e_{\max},\ f=0$ |
| sNaN | $e=e_{\max},\ 1\le f\le f_{\max},\ f[w_f-1]=0$ |
| qNaN | $e=e_{\max},\ 1\le f\le f_{\max},\ f[w_f-1]=1$ |

对不做舍入的操作，公式直接用类别整体（例如 $fd=\mathrm{enc}_F(+\infty_F)$）。对有数值结果的操作，公式用值：

$$
\mathrm{val}_F(a)=
\begin{cases}
(-1)^{s}\,\bigl(1+f/2^{w_f}\bigr)\,2^{\,e-(2^{w_e-1}-1)}, & 1\le e\le e_{\max}-1,\\[2pt]
(-1)^{s}\,f\,2^{\,E_{\min}-w_f}, & e=0,\\[2pt]
(-1)^{s}\,\infty, & e=e_{\max},\ f=0.
\end{cases}
$$

最后一种情形是无穷 $(-1)^s\infty$；NaN（$e=e_{\max}$，$f\ne0$）没有值，因此每条公式在使用
$\mathrm{val}_F$ 之前先对 NaN 输入分类。

### 5.3 规范 NaN

NaN 结果永远是规范 quiet NaN，符号为正、载荷为零：

$$
\mathrm{qNaN}_F:\quad s=0,\quad e=e_{\max},\quad f=2^{w_f-1}.
$$

输入 NaN 的载荷从不传播（Unpriv. §21.3，`sources/riscv-unprivileged.txt:6946,6952`）。

### 5.3.1 最小/最大的全序

`MIN`/`MAX` 按 IEEE 全序 $\prec$ 比较非 NaN 操作数：数值序，且 $-0_F\prec+0_F$，其他数对按值
排序。$\min_\prec(a,b)$ 与 $\max_\prec(a,b)$ 返回较小/较大的*位域三元组*，所以 `+0_F` 与 `-0_F`
的最小值为 $-0_F$，最大值为 $+0_F$。该序只在排除 NaN 类别之后使用。

### 5.3.2 比较结果

比较把整数写入 `rd`：记号 `rd=(P)` 表示谓词 $P$ 成立时 $rd=1$，否则 $rd=0$。整数结果不是
IEEE 值，本身不置任何标志。

### 5.4 装箱

窄类型的 `f` 寄存器值采用 NaN 装箱：$w_F$ 位放在 `FLEN` 位寄存器的低位，高位
$\mathrm{FLEN}-w_F$ 位全为 1（Unpriv. §22.2，`sources/riscv-unprivileged.txt:7288-7295`）。记

$$
\mathrm{boxed}_F(v):\quad
\mathrm{FLEN}=w_F\ \ \lor\ \ v[\mathrm{FLEN}-1:w_F]=1^{\mathrm{FLEN}-w_F},
$$

其余格式名同理写 $\mathrm{boxed}_G$、$\mathrm{boxed}_D$、$\mathrm{boxed}_S$、$\mathrm{boxed}_B$。
除传送类之外，所有浮点运算都检查每个 `f` 寄存器源：正确装箱的寄存器贡献其低 $w_F$ 位的三元组
$(s,e,f)$，未正确装箱的寄存器当作 $w_F$ 位的规范 NaN（Unpriv. §22.2，`:7306-7309`）。因此每个
指令文件的结果块，按三类特权配置各以带 `¬boxed` 合取项的块开头：

1. 第一块按可能的信号 NaN 源展开成一个析取式：该源正确装箱且是信号 NaN，另有一个源未正确
   装箱；结果给出该指令的 NaN 结果并置 `NV(4)`——低位的样子像信号 NaN 但未正确装箱的寄存器
   本身不置标志。每个析取项里的 `¬boxed` 子句对其余源的所有非空子集都成立，与哪个源充当信号
   NaN 无关；只有"没有任何正确装箱的源"这一组合落在此块之外，它正是第 2 块的静默 NaN 情形；
2. 第二块只带 `¬boxed` 合取项，给出该指令对静默 NaN 源的定义——可能完全不置标志；转换到整数
   或有序比较置 `NV(4)`；`FCLASS` 写 `rd=2^{9}`；`FSGNJ*` 写注入符号后的规范 NaN。只有当结果
   与"哪个源未装箱"无关时，这个合取项才写成析取式：其任意一项或几项成立，块的结果都不变；
   若结果与之有关，则写成对所有源合取，并按源另设块。

块互斥且按编号优先，所以其后的块只描述正确装箱的操作数。因此 `FMIN`、`FMAX` 与符号注入类的
第 2 块是"所有源都未装箱"这一种组合，其余组合由紧随的块给出：按未装箱的源 × 另一个源的
NaN/非 NaN 形状各设一块；`FMINM`、`FMAXM` 任一个 NaN 输入都收敛到规范 NaN，仍由第 1、2 块
直接覆盖。

传送类指令——`FLn`、`FSn`、`FMV.X.n`、`FMV.n.X`、`FMVH.X.D`、`FMVH.X.Q`、`FMVP`——直接搬
寄存器的低位，不做装箱检查（`:7302-7304`），所以它们的公式直接写 `f[rs1][j:i]`，不带
`\mathrm{boxed}` 合取项。

公式右端直接写寄存器映像，结果的装箱因此属于公式本身而不是写回：类别或数值 $v$ 写
`fd=\mathrm{enc}_F(v)`，符号、有效数等位域写 `fd=\mathrm{box}_F(\text{bits})`（Unpriv. §22.2）。
逐位拷贝指令——取数、`FMV.W.X`、`FMV.H.X`、`FMV.D.X` 或 `FMVP`——右端直接写装箱后的寄存器映像。

三种编码的关系为

$$
\mathrm{enc}_F(v)=\mathrm{box}_F(\mathrm{raw}_F(v)),\qquad
\mathrm{senc}_F(v)=\mathrm{sext}_{\mathrm{XLEN}}(\mathrm{raw}_F(v)),
$$

其中 $\mathrm{raw}_F(v)$ 是值或类别 $v$ 的 $w_F$ 位 IEEE 位型。`f` 寄存器文件写
$\mathrm{enc}_F(v)$（记作 `fd=\mathrm{enc}_F(…)`）；x 寄存器家族经
$\mathrm{xwr}_F(\mathrm{rd},v)$ 写，不装箱。RV32Zdinx 的一个 `D` 值占据对齐寄存器对
`x[i]`:`x[i+1]`，低编号寄存器存低位；奇数编号保留，`x0` 读出为零、写入被完全丢弃
（Unpriv. §27.3，`:8765-8779`）。

### 5.5 访存谓词

取数与存数用有效地址和访问宽度 $w$ 上的谓词建模存储系统：

| 谓词 | 含义 |
|---|---|
| $\mathrm{Breakpoint}(\mathrm{EA})$ | 环境报告 `EA` 处有数据断点 |
| $\mathrm{MisalignedPre}(\mathrm{EA},w)$ | 在地址翻译之前判定，宽度 $w$ 的访问未对齐 |
| $\mathrm{PageFault}(\mathrm{EA},\mathrm{kind})$ | 翻译失败，发生缺页 |
| $\mathrm{GuestPageFault}(\mathrm{EA},\mathrm{kind})$ | 翻译失败，发生 guest 缺页 |
| $\mathrm{AccessFaultPre}(\mathrm{EA},\mathrm{kind})$ | 翻译失败，发生访问错误 |
| $\mathrm{AccessFaultPost}(\mathrm{EA},\mathrm{kind})$ | 翻译后的访问发生访问错误 |
| $\mathrm{MisalignedPost}(\mathrm{EA},w)$ | 在翻译之后判定，宽度 $w$ 的访问未对齐 |
| $\mathrm{MemOK}_{\mathrm{kind}}(\mathrm{EA},w)$ | 访问正常完成 |

`kind` 为 `load` 或 `store`。这些谓词依赖环境：哪些谓词成立、未对齐在翻译前还是翻译后检查，
都是存储系统的性质而非指令的性质。每个取数/存数文件中的八条公式按约定有序互斥：某条公式在
其谓词成立且前面的谓词都不成立时适用，最后一条是其余七条的补集。

其中一些谓词可能由指令本身并未执行的访问间接触发。页表遍历用隐式访问读取 PTE：这类读取违反
PMA/PMP 时，按原访问类型抛访问错误；PTE 无效时也按原访问类型抛缺页
（`sources/riscv-privileged.txt:7770-7774`）。两阶段翻译中，VS 阶段 PTE 的隐式访问可导致
guest 缺页（`sources/riscv-privileged.txt:9349-9352`）。这些事件对应 `AccessFaultPre`、
`PageFault`、`GuestPageFault` 三行。未对齐访问以及宽于 `XLEN` 的存数还可能被拆成多次内存
操作、各自独立检查：只要有至少一次失败，指令就抛访问错误，而其余操作可能已成功并可见
（`sources/riscv-privileged.txt:4421-4428`、`4451-4457`）。所有这些错误都归到原指令名下，
这也是谓词写在 `EA` 与 $w$ 上、而不是写在单个字节或 PTE 地址上的原因。

模型假定小端存储，`EA` 由当前 `rs1` 值与立即数构成，地址翻译、PMP/PMA 检查与两阶段翻译都由
上述谓词概括；有效特权模式（含 `MPRV`）只决定适用概括表的哪些行。存数公式描述预期的整宽写入。
发生异常时，未对齐存数或宽于 `XLEN` 的存数可能已经提交了部分字节——PMP 检查与拆分按每次
内存操作进行——因此异常分支只陈述异常，不约束任何部分内存效果（Priv. §3.7.1.3，
`sources/riscv-privileged.txt:4421-4428`）。取数公式同样描述整宽读取；未对齐或跨页访问的
首次错误规则属于存储系统的谓词指派。

### 5.6 代表操作数

公式的守卫检查值类、符号、标志与舍入模式，从不检查单个位模式，因此每个值类一个代表元即可
到达每个块。操作数写成 §5.1 的三元组 $(s,e,f)$。

**值类代表元。** §5.2 的十个类由下列三元组到达：

| 值类 | 三元组 |
|---|---|
| $+0_F$ / $-0_F$ | $(0,0,0)$ / $(1,0,0)$ |
| 正次正规，最小 / 最大 | $(0,0,1)$ / $(0,0,f_{\max})$ |
| 正正规，最小 / 最大 | $(0,1,0)$ / $(0,e_{\max}-1,f_{\max})$ |
| $+\infty_F$ / $-\infty_F$ | $(0,e_{\max},0)$ / $(1,e_{\max},0)$ |
| sNaN，最小 / 最大载荷 | $(0,e_{\max},1)$ / $(0,e_{\max},2^{w_f-1}-1)$ |
| qNaN，规范 / 最大载荷 | $(0,e_{\max},2^{w_f-1})$ / $(0,e_{\max},f_{\max})$ |

次正规、正规、NaN 三行取 $s=1$ 即得负号那一类。这十行也正好是 `FCLASS` 的十个结果位，因此
这一组操作数就把该指令测全。

**位模式族。** `FCLASS`、三条符号注入、两个方向的 `FMV` 以及 §5.4 的装箱检查单个位，其操作数
是固定 $e$ 上的 $f$ 图案。这些图案位于一个标量操作数的尾数内，不涉及向量寄存器或通道复制。
取 $0\le i<w_f$，各族为

| 族 | 图案 | 考察内容 |
|---|---|---|
| 走 1 | $f=2^i$ | 每次只置一位；可达安静位 $f[w_f-1]$ |
| 走 1 且最低位置位 | $f=2^i+1$ | 同上，最低位保持置位 |
| 走 0 | $f=f_{\max}\oplus2^i$ | 每次只清一位 |
| 走 0 且最低位清零 | 走 0 图案再清最低位 | 同上，最低位保持清零 |
| march 1 | $f=2^{i+1}-1$ | 从最低位起一列 1 逐步加长 |
| march 0 | $f=f_{\max}-(2^{i+1}-1)$ | 从最低位起一列 0 逐步加长 |
| 两端填充 | $f=(2^k-1)\,(2^{w_f-k}+1)$，$1\le k\le\lfloor (w_f-1)/2\rfloor$ | 1 从两端进入并在中间会合 |
| 中间填充 | 居中一段 $w_f-2k$ 个 1，$1\le k\le\lfloor (w_f-1)/2\rfloor$ | 1 从两端向中间退缩 |
| $k$ 位周期图案，$2\le k\le5$ | 每个非零 $k$ 位块从第 $w_f-1$ 位起按周期 $k$ 重复；共 $2^k-1$ 个，全 1 块即 $f=f_{\max}$ | 相距 $k$ 的位之间的耦合 |

其中两族正好到达 NaN 边界：$i=w_f-1$ 的走 1 是规范 $\mathrm{qNaN}_F$，$i=w_f-2$ 的 march 1
是最大 sNaN 载荷 $2^{w_f-1}-1$。除这些位位置外，同一族的各图案都与相邻图案同属一类，因此对
其余指令的守卫没有增量；它们的作用是在检查单个位的指令里把“拷贝、宽度、符号注入”错误与
“值类”错误区分开。

**字段隔离。** 让三个字段取互不相同的可辨识值，可以在一份结果里暴露字段、宽度或字节序错误；
$s=1$、$e=11$、$f=22$ 就是这样一个三元组。

**成对操作数。** 有些结果取决于两个操作数之间的关系，单个代表元表达不了：$+0_F$ 与 $-0_F$
相加（FADD.19）、异号的两个无穷（FADD.4），以及 §6 中的 tie 与上溢边界——它们精确和或精确积
的性质，而不是任一操作数的性质。这些必须按 §5.1 与 §6.1 构造，不能从值类清单里抽样。

## 6. 舍入与状态

### 6.1 有效舍入模式

`instr.rm` 与 `fcsr.frm` 都是 3 位字段。`RNE(0)`、`RTZ(1)`、`RDN(2)`、`RUP(3)`、`RMM(4)`
合法；5 与 6 保留；`instr.rm` 另有 `DYN(7)`，选择 `fcsr.frm`。舍入字段合法当且仅当

$$
\bigl(\mathrm{instr}.rm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\ \lor\ (\mathrm{instr}.rm=\mathrm{DYN}(7)\land fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\})\bigr).
$$

每条带 `rm` 字段的指令都带这个合取项。有效模式在 `instr.rm` 不为 `DYN(7)` 时就是它，否则是
`fcsr.frm`：

$$
\mathrm{rounded}=
\begin{cases}
\mathrm{round}_{F,\mathrm{instr}.rm}(\mathrm{exact}), & \mathrm{instr}.rm\ne\mathrm{DYN}(7),\\
\mathrm{round}_{F,fcsr.frm}(\mathrm{exact}), & \mathrm{instr}.rm=\mathrm{DYN}(7).
\end{cases}
$$

$\mathrm{round}_{F,m}(v)$ 按模式 $m$ 把 $v$ 一次舍入到格式网格上：在 $2^{E_{\min}}$ 以下网格
步长为 $2^{E_{\min}-w_f}$（次正规网格），在 $\mathrm{MAX}_F$ 以上不设指数上限，因此溢出通过
比较 $\mathrm{rounded}$ 与 $\mathrm{MAX}_F$ 检测，而不是在舍入内饱和。

下溢的 tiny 判定在舍入之后，并且使用它自己的舍入，与交付结果的舍入不同。令
$\mathrm{round}^{\infty}_{F,m}(v)$ 按模式 $m$ 把 $v$ 舍入到 $F$ 的精度、两端都不设指数上限；
该舍入的每个非零结果都是同号的正规 $F$ 数。于是

$$
\mathrm{tiny}\iff 0<\bigl|\mathrm{round}^{\infty}_{F,m}(\mathrm{exact})\bigr|<2^{E_{\min}}.
$$

这两种舍入在指数范围底部可能不一致。$\mathrm{round}^{\infty}_{F,m}$ 可以产生低于
$2^{E_{\min}}$ 的幅值，而 $\mathrm{round}_{F,m}$ 交付 $\pm2^{E_{\min}}$，且仍然置 `UF(1)`。
判定用的舍入比交付用的次正规网格更细，所以不一致只有一个方向：$\mathrm{tiny}$ 的结果可以交付
为 $\pm2^{E_{\min}}$（或次正规数），而非零且非 $\mathrm{tiny}$ 的结果总交付为正规数。因此
下溢跟随 $\mathrm{tiny}$，而不跟随交付值的类别：`UF(1)` 与 `NX(0)` 同时置位，当且仅当
$\mathrm{tiny}$ 成立且 $\mathrm{rounded}\ne\mathrm{exact}$（Unpriv. §21.4、§25.3.2.6.1，
`sources/riscv-unprivileged.txt:6972-6978,8058-8073`）。因此指令文件把"只置 `NX(0)`"的类别
限制在正规交付值并要求 $\neg\mathrm{tiny}$，而 tiny 且不精确的类别不设类别限制：其交付值可以是
正规数，并且它总是一同置 `UF(1)` 与 `NX(0)`。

保留舍入模式的行为是保留的，因此那些配置不在任何指令文件之内：它们不出现在任何公式中，既不作
结果也不作异常。抛 `IllegalInstruction(2)` 是实现允许的选择，但不是要求（Unpriv. §21.2，
`sources/riscv-unprivileged.txt:6889-6894,6920-6924`）。

### 6.2 Dirty 状态

写任何浮点状态——`f` 寄存器或 `fcsr`——都把浮点状态置为 Dirty（Priv. §15.2.11，
`sources/riscv-privileged.txt:9538-9540`）。每个结果块固定一种特权配置，因此右端只写该配置的
状态：`M/S/U` 与 `M/HS/U` 块写 `mstatus.FS=Dirty(3)`，`VS/VU` 块写
`vsstatus.FS=Dirty(3),\ sstatus.FS=Dirty(3)`。`VS/VU` 的两个写是同一条公式的逗号并列结果，
不是合取：两者都会发生。

在 `U`、`S`、`HS`、`M` 模式下只有 `mstatus.FS` 存在。在 `VS` 与 `VU` 下，`vsstatus.FS` 与
HS 级的 `sstatus.FS` 都生效，并且都置位（Priv. §15.2.11，`sources/riscv-privileged.txt:9538-9540`）。
`mstatus.FS` 与 `sstatus.FS` 是同一字段，所以 `VS/VU` 的赋值同时更新 HS 级字段。

因此：

- 写 `fd` 的指令在右端总带该赋值；
- 只写 `rd` 的指令，仅在同时置 `fcsr.fflags` 中某标志的分支里带该赋值（此时 `fcsr` 被修改）；
- 只写 `rd` 且不置标志的比较或传送不改变浮点状态，不带该赋值；
- `FSCSR`、`FSRM`、`FSFLAGS` 写 `fcsr`，因此带该赋值，尽管仅凭它们的 `rd` 写不会带；
  `FRCSR`、`FRRM`、`FRFLAGS` 不带。

这是精确（保守）策略。特权规范也允许不精确跟踪：实现可以在状态实际未修改时置 Dirty，也可以
完全不跟踪，此时可达的 `FS` 值为 Off 与 Dirty（Priv. §15.2.3，
`sources/riscv-privileged.txt:2333-2346`）。公式陈述最小的 Dirty 集合；更粗的实现可以增加
Dirty 迁移，但绝不能省略必需的迁移。

## 7. 异常与标志

### 7.1 异常码

| 码 | 名称 |
|---:|---|
| 0 | `InstructionAddressMisaligned` |
| 1 | `InstructionAccessFault` |
| 2 | `IllegalInstruction` |
| 3 | `Breakpoint` |
| 4 | `LoadAddressMisaligned` |
| 5 | `LoadAccessFault` |
| 6 | `StoreAMOAddressMisaligned` |
| 7 | `StoreAMOAccessFault` |
| 8 | `EnvironmentCallFromU` |
| 9 | `EnvironmentCallFromS` |
| 11 | `EnvironmentCallFromM` |
| 12 | `InstructionPageFault` |
| 13 | `LoadPageFault` |
| 15 | `StoreAMOPageFault` |
| 20 | `InstructionGuestPageFault` |
| 21 | `LoadGuestPageFault` |
| 22 | `VirtualInstruction` |
| 23 | `StoreAMOGuestPageFault` |

（Priv. 表 50，`sources/riscv-privileged.txt:10424-10456`。）所有 `zfinx` 公式使用同一套码；
虚拟指令情形在 `zfinx.md` 中写开。

在 `f` 寄存器形式中，操作数全为寄存器的指令在执行阶段只抛 `IllegalInstruction(2)`；Zfinx
形式在 `stateen` 门控拒绝虚拟机上执行时还会抛 `VirtualInstruction(22)`。取数与存数另外建模
地址未对齐与存储访问/缺页错误，其触发条件依赖存储系统，在取数、存数文件中作为单独公式陈述。
每条指令也可能在自己的取指阶段陷入；这类结果只取决于 `PC` 而与指令无关，因此每条公式的
`exception` 字段都以它开头（§7.1.2）。当该表达式选中某个码时，该块的寄存器、内存、`FS` 与
标志字段都不发生。

#### 7.1.1 优先级

同一次执行可能抛出多个同步异常时，由表 17（`sources/riscv-privileged.txt:3027-3045`）的降序
决定上报哪一个；实现 `H` 时改用表 51（`sources/riscv-privileged.txt:10538-10560`）。“先遇到者
优先”以及未对齐位置由实现决定这两点见 `sources/riscv-privileged.txt:3051-3060`。本目录指令能
直接抛出、在取指阶段抛出、或经隐式访问间接抛出的全部码及其来源：

| 码 | 直接触发 | 间接触发 |
|---|---|---|
| `Breakpoint(3)` | `PC` 处有指令地址断点，优先级最高（`:3029`、`:10540`）；或地址转换后环境报告 `EA` 处有数据断点 | — |
| `InstructionPageFault(12)` | `PC` 的第一阶段翻译失败（`:3031`、`:10542`） | — |
| `InstructionGuestPageFault(20)` | 实现 `H` 且 `V=1` 时 `PC` 的 G 阶段翻译失败（`:10542`） | VS 阶段 PTE 的隐式访问失败（`:9349-9352`） |
| `InstructionAccessFault(1)` | `PC` 的物理取指未通过 PMA/PMP（`:3033`、`:10544`）；或 `PC` 的页表遍历失败（`:7770-7771`） | — |
| `IllegalInstruction(2)` | 扩展未实现、有效 `FS` 为 Off、`stateen` 判非法 | —（编码合法，是环境否决执行） |
| `VirtualInstruction(22)` | — | `zfinx` 在 VS/VU 且 `hstateen0`/`sstateen0` 拒绝、`mstateen0.FCSR=1` |
| `LoadAddressMisaligned(4)`、`StoreAMOAddressMisaligned(6)` | `EA` 未对齐（在实现选择的检查点判定） | —（手册也允许以访问错误代替，`:4033-4034`） |
| `LoadPageFault(13)`、`StoreAMOPageFault(15)` | VS 阶段走表失败：PTE 无效或权限不符、超大页未对齐、`Svade` 要求置 A/D 位（`:7771-7787`） | 拆分访问的某一段（`:10286-10292`） |
| `LoadGuestPageFault(21)`、`StoreAMOGuestPageFault(23)` | G 阶段走表失败 | VS 阶段 PTE 的隐式访问失败（`:9349-9352`）；拆分访问的某一段（`:10286-10292`） |
| `LoadAccessFault(5)`、`StoreAMOAccessFault(7)` | 最终访问未通过 PMA/PMP | PTE 读违反 PMA/PMP（`:7770-7771`）；PTE 的 A/D 写违反（`:7788-7789`）；多次内存操作中某一次失败而其余成功（`:4451-4457`） |

`InstructionAddressMisaligned(0)` 不可达：它由目标未对齐的控制流指令抛出，而不是由取指抛出
（`:3069-3071`），并且 §8 中没有控制流指令。环境调用与环境断点同样不在范围内，它们分别属于
`ECALL` 与 `EBREAK`。

`sstatus` 或 `vsstatus` 中 `FS`、`VS` 为 0 时抛 `IllegalInstruction(2)`，永远不抛
`VirtualInstruction(22)`（`:10525-10527`），所以 `f` 寄存器各组没有 22。

优先级链（实现 `H` 时，从高到低）：

| 指令组 | 优先级 |
|---|---|
| 算术、FMA、`FSQRT`、`FDIV`、最小/最大、符号注入、比较、`FCLASS`、`FCVT`、`FMV`、`FLI`、六条 `fcsr` 指令 | `Breakpoint(3, fetch) > InstructionPageFault(12) = InstructionGuestPageFault(20) = InstructionAccessFault(1, walk) > InstructionAccessFault(1, phys) > IllegalInstruction(2)` |
| `zfinx` 形式 | `Breakpoint(3, fetch) > InstructionPageFault(12) = InstructionGuestPageFault(20) = InstructionAccessFault(1, walk) > InstructionAccessFault(1, phys) > IllegalInstruction(2) > VirtualInstruction(22)` |
| `FLW`、`FLD`、`FLQ`、`FLH` | `Breakpoint(3, fetch) > InstructionPageFault(12) = InstructionGuestPageFault(20) = InstructionAccessFault(1, walk) > InstructionAccessFault(1, phys) > IllegalInstruction(2) > Breakpoint(3, data) > LoadAddressMisaligned(4) > LoadPageFault(13) = LoadGuestPageFault(21) = LoadAccessFault(5, walk) > LoadAccessFault(5, data) > LoadAddressMisaligned(4, lowest)` |
| `FSW`、`FSD`、`FSQ`、`FSH` | `Breakpoint(3, fetch) > InstructionPageFault(12) = InstructionGuestPageFault(20) = InstructionAccessFault(1, walk) > InstructionAccessFault(1, phys) > IllegalInstruction(2) > Breakpoint(3, data) > StoreAMOAddressMisaligned(6) > StoreAMOPageFault(15) = StoreAMOGuestPageFault(23) = StoreAMOAccessFault(7, walk) > StoreAMOAccessFault(7, data) > StoreAMOAddressMisaligned(6, lowest)` |

链中 `>` 表示左码优先级高于右码，`=` 表示两码优先级相同；次序取自表 17（未实现 `H`）或
表 51（实现 `H`）。未实现 `H` 时同一串去掉 20、21、23，22 也不可能出现。取指前缀对所有指令组相同，出现在
每条公式的 `exception` 字段开头（§7.1.2）：`Breakpoint(3, fetch)` 最高，手册“取指地址转换期间”一行中的码并列于“首先遇到者”，
随后是物理取指的访问错误；它们都排在 `IllegalInstruction(2)` 之前，因为在指令译码之前就已
抛出。标签 `fetch`、`walk`、`phys`、`data`、`lowest` 不是手册术语，手册只用表中的行标题描述区分
这些行。`fetch`、`data` 标注码 3 的两个来源，手册把它们放在两个不同的优先级：指令地址断点在
最高处，数据断点在地址转换之后；`walk`、`phys` 标注手册为取指给出的码 1 的
两行。`=` 表示手册的“地址转换中首先遇到者”组：转换在第一次失败处停止，这些码不会
同时出现，优先级并列。有两对码在链上出现两次，因为手册为它们各列了两行：4/6 一处是
“Optionally”排在翻译组之前，一处是“If not higher priority”排在最低，`MisalignedPre` 与
`MisalignedPost` 公式分别编码这两种排法；5/7 一处是走表（PTE 读或 A/D 写）失败、位于“首先
遇到者”组，一处是翻译后显式访问失败，二者不会同时发生，因为走表失败就不会再有访问。
`walk`、`data` 标注访存来源，`lowest` 标注第二个未对齐位置。每条公式的 `exception` 字段是
该配置可能抛出的码的优先级链，块能抛异常时末端是该配置实际抛出的码，否则止于取指链。

#### 7.1.2 公式中的取指阶段

每条指令都在译码之前取指，所以取指失败会完全抢占该指令：取指未完成时，指令不写任何寄存器、
内存或 CSR，也不置任何标志。取指只取决于 `PC`，与指令无关，因此每条结果公式都在 `exception`
字段开头写同一条优先级链。对允许 `V=1` 的块，链为

$$
\mathrm{Breakpoint}(3,\mathrm{fetch}) > \mathrm{InstructionPageFault}(12)
= \mathrm{InstructionGuestPageFault}(20)
= \mathrm{InstructionAccessFault}(1,\mathrm{walk})
> \mathrm{InstructionAccessFault}(1,\mathrm{phys})
> \text{该块自身的码（若有）},
$$

配置排除 `V=1` 的块没有 `InstructionGuestPageFault(20)` 这一项。块能抛异常时链止于该块自身
的码，否则止于 `\mathrm{InstructionAccessFault}(1,\mathrm{phys})`，不再补空集。码按优先级排列，
其中任何一个发生时，该块的寄存器、内存、`FS` 与标志字段都不发生。
限定词 `\mathrm{fetch}`、`\mathrm{walk}`、`\mathrm{phys}`、`\mathrm{data}` 标注手册为码 3
和码 1 各列的两行（§7.1.1）。顺序见表 17（`sources/riscv-privileged.txt:3029-3033`）；表 51
把 20 插入翻译组（`:10540-10544`）。16 位对齐的取指跨页时，两次翻译都属于本次取指，任一处
失败都按指令地址 `PC` 上报（`:10286-10292`）。

### 7.2 浮点标志

`fcsr.fflags` 是粘性的：`fcsr.fflags \mathrel{|}= S` 置位 $S$ 中每个标志，其余标志不变。
标志为 `NV(4)`、`DZ(3)`、`OF(2)`、`UF(1)`、`NX(0)`；从不清零任何标志。

| 条件 | 置位标志 |
|---|---|
| 存在 signaling NaN 操作数，或非法操作 | `NV(4)` |
| 有限非零值除以零 | `DZ(3)` |
| 结果过大无法表示 | `OF(2)` |
| 结果过小且不精确 | `UF(1)` |
| 结果与精确值不同 | `NX(0)` |

没有舍入步骤的指令（符号注入、最小/最大、分类、传送、取数、存数）不置任何标志，除非手册
指定 `NV(4)`。

### 7.3 逐指令汇总

| 指令组 | 异常码 | 可能的标志 |
|---|---|---|
| 算术（`FADD`、`FSUB`、`FMUL`、`FMA`） | 2 | `NV(4)`、`OF(2)`、`UF(1)`、`NX(0)`（无 `DZ(3)`） |
| `FDIV` | 2 | `NV(4)`、`DZ(3)`、`OF(2)`、`UF(1)`、`NX(0)` |
| `FSQRT` | 2 | `NV(4)`、`NX(0)` |
| `FMIN`/`FMAX`/`FMINM`/`FMAXM` | 2 | `NV(4)`（sNaN） |
| `FSGNJ`/`FSGNJN`/`FSGNJX`、`FLI`、传送、取数、存数 | 2 | 无 |
| `FEQ`/`FLT`/`FLE`/`FLEQ`/`FLTQ` | 2 | `NV(4)`（sNaN；quiet 比较不同） |
| `FCLASS` | 2 | 无 |
| `FCVT` 到整数 | 2 | `NV(4)`、`NX(0)` |
| `FCVT` 从整数 | 2 | `OF(2)`、`NX(0)` |
| `FCVT` 浮点—浮点、`FCVT.BF16.S`、`FCVT.S.BF16` | 2 | `NV(4)`、`OF(2)`、`UF(1)`、`NX(0)` |
| `FROUND`/`FROUNDNX`/`FCVTMOD` | 2 | `NV(4)`、`NX(0)` |
| `FRCSR`/`FSCSR`/`FRRM`/`FSRM`/`FRFLAGS`/`FSFLAGS` | 2 | 无 |
| 取数 | 2、3、4、5、13、21 | 无 |
| 存数 | 2、3、6、7、15、23 | 无 |

表中码按升序列出；多个码可能适用时的上报顺序见 §7.1.1。每个指令组还都有取指阶段的码 1、3、
12，实现 `H` 且 `V=1` 时还有 20；它们只取决于 `PC`，出现在每条公式的 `exception` 字段开头
（§7.1.2），故表中省略。这些组的
`zfinx` 形式抛 2 和 22，不抛访存码，因为其操作数全为寄存器。

## 8. 指令文件

所有指令文件都在 `instructions/` 下；本 README 留在目录根部。每个文件含一个助记符组的公式。
`F` 是格式参数；适用于四种格式的文件左端带 `(F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})`，
最后一个合取项为 `(instr=MNEMONIC.F)`。只适用于一种格式的文件写具体后缀。

### 算术与 FMA

| 文件 | 助记符 | 格式 | 状态 |
|---|---|---|---|
| [fadd.md](instructions/fadd.md) | `FADD` | H、S、D、Q | 完成 |
| [fsub.md](instructions/fsub.md) | `FSUB` | H、S、D、Q | 完成 |
| [fmul.md](instructions/fmul.md) | `FMUL` | H、S、D、Q | 完成 |
| [fdiv.md](instructions/fdiv.md) | `FDIV` | H、S、D、Q | 完成 |
| [fsqrt.md](instructions/fsqrt.md) | `FSQRT` | H、S、D、Q | 完成 |
| [fmadd.md](instructions/fmadd.md) | `FMADD` | H、S、D、Q | 完成 |
| [fmsub.md](instructions/fmsub.md) | `FMSUB` | H、S、D、Q | 完成 |
| [fnmsub.md](instructions/fnmsub.md) | `FNMSUB` | H、S、D、Q | 完成 |
| [fnmadd.md](instructions/fnmadd.md) | `FNMADD` | H、S、D、Q | 完成 |

### 最小/最大、符号、比较、分类

| 文件 | 助记符 | 格式 | 状态 |
|---|---|---|---|
| [fmin.md](instructions/fmin.md) | `FMIN` | H、S、D、Q | 完成 |
| [fmax.md](instructions/fmax.md) | `FMAX` | H、S、D、Q | 完成 |
| [fminm.md](instructions/fminm.md) | `FMINM` | H、S、D、Q | 完成 |
| [fmaxm.md](instructions/fmaxm.md) | `FMAXM` | H、S、D、Q | 完成 |
| [fsgnj.md](instructions/fsgnj.md) | `FSGNJ`、`FSGNJN`、`FSGNJX` | H、S、D、Q | 完成 |
| [feq.md](instructions/feq.md) | `FEQ` | H、S、D、Q | 完成 |
| [flt.md](instructions/flt.md) | `FLT` | H、S、D、Q | 完成 |
| [fle.md](instructions/fle.md) | `FLE` | H、S、D、Q | 完成 |
| [fleq.md](instructions/fleq.md) | `FLEQ` | H、S、D、Q | 完成 |
| [fltq.md](instructions/fltq.md) | `FLTQ` | H、S、D、Q | 完成 |
| [fclass.md](instructions/fclass.md) | `FCLASS` | H、S、D、Q | 完成 |

### 转换

| 文件 | 助记符 | 格式 | 状态 |
|---|---|---|---|
| [fcvt-to-int.md](instructions/fcvt-to-int.md) | `FCVT.W`、`FCVT.WU`、`FCVT.L`、`FCVT.LU` | H、S、D、Q | 完成 |
| [fcvt-from-int.md](instructions/fcvt-from-int.md) | `FCVT.F.W`、`FCVT.F.WU`、`FCVT.F.L`、`FCVT.F.LU` | H、S、D、Q | 完成 |
| [fcvt-fp-fp.md](instructions/fcvt-fp-fp.md) | `FCVT.dst.src` | H、S、D、Q | 完成 |
| [fround.md](instructions/fround.md) | `FROUND` | H、S、D、Q | 完成 |
| [froundnx.md](instructions/froundnx.md) | `FROUNDNX` | H、S、D、Q | 完成 |
| [fcvttmod.md](instructions/fcvttmod.md) | `FCVTMOD.W.D` | D | 完成 |
| [bf16.md](instructions/bf16.md) | `FCVT.BF16.S`、`FCVT.S.BF16` | BF16 | 完成 |

### 传送、取数、存数、CSR

| 文件 | 助记符 | 格式 | 状态 |
|---|---|---|---|
| [fmv-w.md](instructions/fmv-w.md) | `FMV.X.W`、`FMV.W.X` | S | 完成 |
| [fmv-d.md](instructions/fmv-d.md) | `FMV.X.D`、`FMV.D.X` | D | 完成 |
| [fmv-h.md](instructions/fmv-h.md) | `FMV.X.H`、`FMV.H.X` | H | 完成 |
| [fmvh.md](instructions/fmvh.md) | `FMVH.X.D`、`FMVH.X.Q` | D、Q | 完成 |
| [fmvp.md](instructions/fmvp.md) | `FMVP.D.X`、`FMVP.Q.X` | D、Q | 完成 |
| [fli.md](instructions/fli.md) | `FLI` | H、S、D、Q | 完成 |
| [flw.md](instructions/flw.md) | `FLW` | S | 完成 |
| [fld.md](instructions/fld.md) | `FLD` | D | 完成 |
| [flq.md](instructions/flq.md) | `FLQ` | Q | 完成 |
| [flh.md](instructions/flh.md) | `FLH` | H | 完成 |
| [fsw.md](instructions/fsw.md) | `FSW` | S | 完成 |
| [fsd.md](instructions/fsd.md) | `FSD` | D | 完成 |
| [fsq.md](instructions/fsq.md) | `FSQ` | Q | 完成 |
| [fsh.md](instructions/fsh.md) | `FSH` | H | 完成 |
| [fcsr.md](instructions/fcsr.md) | `FRCSR`、`FSCSR`、`FRRM`、`FSRM`、`FRFLAGS`、`FSFLAGS` | — | 完成 |

### 整数寄存器形式

| 文件 | 助记符 | 格式 | 状态 |
|---|---|---|---|
| [zfinx.md](instructions/zfinx.md) | x 寄存器上的整套标量浮点指令 | S、D、H | 完成 |

## 9. 校验

```bash
python3 -I tools/check_md.py    specs/f-d-q-zfh-zfhmin-zfbfmin-zfa-zfinx-zdinx-zhinx-zhinxmin/README.md
python3 -I tools/check_style.py specs/f-d-q-zfh-zfhmin-zfbfmin-zfa-zfinx-zdinx-zhinx-zhinxmin/README.md
python3 -I tools/check_md.py    specs/f-d-q-zfh-zfhmin-zfbfmin-zfa-zfinx-zdinx-zhinx-zhinxmin/instructions/fadd.md
python3 -I tools/check_style.py specs/f-d-q-zfh-zfhmin-zfbfmin-zfa-zfinx-zdinx-zhinx-zhinxmin/instructions/fadd.md
```

同样对 `instructions/` 下的每个文件运行这两条命令。

在标记为完成之前，本文件与每个指令文件都必须通过这两个校验器。
