[English](README.md) | 中文

# RISC-V 指令形式化

一套编写 **按配置索引的指令形式化规格** 的框架，以及用这套框架产出的规格。仓库围绕方法
组织，而不是围绕某一类指令：`specs/` 里是实例，新增一个扩展家族就是新增一个实例。

每条指令写成一组形如

$$
\begin{aligned}
&\text{特权配置}\ \land\ \text{扩展条件}\\
&\land\ \text{状态字段}\\
&\land\ \text{操作数}\\
&\land\ (\mathrm{instr}=I)
\end{aligned}
\longrightarrow
\{\, \text{状态变化},\ \mathrm{exception}=\{\ldots\} \,\}
$$

的公式。左端是使某一具体行为成立的执行配置；右端是该指令产生的寄存器、内存、CSR 与标志
更新，以及它能触发的异常。结果不同就拆成不同公式，按求值顺序编号；公式 `.0` 固定是守卫，
处理扩展不可用或执行配置不允许的情况。

## 框架组成

| 组成 | 作用 |
|---|---|
| [`workflow.md`](workflow.md) | 方法：公式结构、左端四组、右端、写作流程，以及如何代入非浮点家族（§11） |
| [`templates/`](templates/README.zh.md) | 交付 README 与指令文件的骨架及占位符约定 |
| [`specs/`](specs/README.zh.md) | 已发布实例（见下） |
| [`tools/`](tools/README.md) | 所有实例共用的结构与风格校验器 |
| [`sources/`](sources/README.md) | 实例引用的两份手册：PDF 与抽取文本 |
| [`CONTRIBUTING.md`](CONTRIBUTING.zh.md) | 范围、写作步骤、写作规则、校验与评审清单 |

## 已发布实例

| 实例 | 范围 |
|---|---|
| [`specs/f-d-q-zfh-zfhmin-zfbfmin-zfa-zfinx-zdinx-zhinx-zhinxmin/`](specs/f-d-q-zfh-zfhmin-zfbfmin-zfa-zfinx-zdinx-zhinx-zhinxmin/README.zh.md) | 标量浮点：`F`、`D`、`Q`、`Zfh`、`Zfhmin`、`Zfbfmin`、`Zfa`、`Zfinx`、`Zdinx`、`Zhinx`、`Zhinxmin` |
| [`specs/v-zvfh-zvfhmin-zvfbfmin-zvfbfwma/`](specs/v-zvfh-zvfhmin-zvfbfmin-zvfbfwma/README.md) | 向量浮点：`V` 与 `Zvfh`、`Zvfhmin`、`Zvfbfmin`、`Zvfbfwma` |
| [`specs/h-svinval/`](specs/h-svinval/README.md) | H 扩展 `HLV`/`HSV`/`HLVX`、`HFENCE.VVMA`/`HFENCE.GVMA`、Svinval `HINVAL.VVMA`/`HINVAL.GVMA` |

[`specs/README.md`](specs/README.zh.md) 是实例索引：范围、依据章节、文件与公式条数，以及各
实例共用的约定。

## 新建实例

1. 读 [`workflow.md`](workflow.md) 了解方法，读 [`CONTRIBUTING.md`](CONTRIBUTING.zh.md)
   了解协作约定；非浮点家族从工作流 §11 入手。
2. 在 `sources/*.txt` 中定位规范原文；不要凭记忆添加规则。
3. 从 [`templates/`](templates/README.zh.md) 复制骨架，替换全部 `{{…}}` 占位符。
4. 先写交付 README（符号、格式、值类、状态写入、异常优先级），再按助记符组写指令文件。
5. 对每个改动过的文件跑两个校验器，并在 [`specs/README.md`](specs/README.zh.md) 中登记。

## 共用约定

- 每条公式一个 `aligned` 块，每行最多一个顶层 `\land`。
- 左端各组按固定顺序排列，`\mathrm{instr}=…` 在最后。
- 右端顺序：目的 → 状态写入 → 粘性标志 → `exception` 在最后。
- 公式 `.0` 是守卫，不写任何状态。
- 所有共享定义（符号、格式、值类、异常优先级）都在实例 README 中；指令文件只放结果公式。
- 结果是域内规范值或类别，不写硬件位型。
- 粘性状态用 `\mathrel{|}=` 更新。

## 校验

`specs/` 下的每个 Markdown 文件都必须通过两个校验器（退出码 0）：

```bash
find specs -name '*.md' -exec python3 -I tools/check_md.py {} \;
find specs -name '*.md' -exec python3 -I tools/check_style.py {} \;
```

`check_md.py` 检查公式定界符、环境配平、表格列数与行内数学定界符；`check_style.py` 检查公式
风格：每行最多一个顶层 `\land`、`\mathrm{instr}` 在左端最后、右端以 `\mathrm{exception}` 结尾、
粘性标志写法，以及禁用 `\wedge`/`\vee` 与位型字面量。

## 依据与引用

实例按行号引用两份 RISC-V 手册，例如 `sources/riscv-unprivileged.txt:18374`。两份 PDF
均由 RISC-V International 以 CC BY 4.0 发布；`.txt` 是行号所指的抽取文本。
[`sources/README.md`](sources/README.md) 说明该查哪一卷以及引用约定。

## 参与

见 [`CONTRIBUTING.zh.md`](CONTRIBUTING.zh.md)（或英文 [`CONTRIBUTING.md`](CONTRIBUTING.md)）：
范围、写作步骤、写作规则、校验与评审清单。交付文档只用英文；框架文档以英文为准，并提供
中文对照。
