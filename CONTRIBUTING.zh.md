[English](CONTRIBUTING.md) | 中文

# 贡献指南

本仓库是一套框架：`specs/` 是用它产出的实例。新增一个扩展家族就是新增一个实例；修改方法
本身则改 `workflow.md`、`templates/` 或 `tools/`。

## 目录职责

| 路径 | 内容 |
|---|---|
| `specs/<instance>/README.md` | 该实例的全部共享定义：符号、格式、值类、状态写入、异常优先级 |
| `specs/<instance>/instructions/<mnemonic>.md` | 只放结果公式，每个助记符组一个文件 |
| `templates/` | 骨架与占位符约定 |
| `sources/` | 手册 PDF 与抽取文本 |
| `tools/` | 所有实例共用的结构校验器 |

## 动笔之前

1. 先读 [`workflow.md`](workflow.md)：方法、公式形态，以及 §11 对非浮点家族的说明。
2. 先在 `sources/*.txt` 里定位规范原文。**不要凭记忆添加规则。** 每个条件、值类、标志和
   异常都要能追溯到手册行号或 IEEE 754。
3. 确定范围：每个助记符组一个指令文件；操作数形式不同且状态行为不同的，要拆成不同公式块；
   结果类别不同就拆成不同公式。

## 新建实例

1. 在 `specs/` 下取一个列出所覆盖扩展的目录名（如 `h-svinval`、
   `v-zvfh-zvfhmin-zvfbfmin-zvfbfwma`）。
2. 从 [`templates/`](templates/README.zh.md) 复制骨架，替换全部 `{{…}}` 占位符；
   `grep -R '{{' specs/*/` 必须没有输出。
3. 先写交付 README，再写指令文件。所有符号在 README 中登记；指令文件不得引入隐藏谓词或
   未登记的符号。
4. 在 [`specs/README.md`](specs/README.md) 的表中加一行。

## 写作规则

以下为不可协商的约定，完整说明见 `workflow.md` §2–§5 与各实例 README。

- 左端各组按固定顺序排列，`\mathrm{instr}=…` 在最后。
- 每条公式一个 `aligned` 块；每行最多一个顶层 `\land`。
- 右端是结果集合 `\{\, … \,\}`：目的 → 状态写入 → 粘性标志 → `exception` 在最后。
- 公式 `.0` 是守卫：扩展不可用或执行配置不允许，只产生对应异常。
- 结果类别互斥，按求值顺序编号；后面的公式不再重复前面已排除的条件。
- 左端析取只允许在“取任意一项结果都不变”时使用；否则拆块。
- 结果是域内规范值或类别，不写硬件位型。
- 粘性状态用 `\mathrel{|}=` 更新，不用 `=` 赋值。
- 指令文件只列该指令自身能抛的异常；取指链在实例 README 中统一说明一次。

## 语言

- 交付文档（`specs/**/instructions/*.md`、各实例 `README.md`）只用英文。
- 框架文档以英文为准，并提供完整的 `*.zh.md` 对照。
- `workflow.md` 是详细的中文方法说明，开头有英文概览。
- 交付 README 的中文译本（如标量实例的 `README.zh.md`）只是阅读辅助，不是规范。

## 校验

每次修改后，在仓库根目录运行：

```bash
python3 -I tools/check_md.py    <file.md>
python3 -I tools/check_style.py <file.md>
```

或对整个实例：

```bash
find specs/<instance> -name '*.md' \
  -exec python3 -I tools/check_md.py {} \; \
  -exec python3 -I tools/check_style.py {} \;
```

两者都必须返回 0。校验器只检查结构，不检查语义；通过它们不代表公式与手册一致，也不能为了
迁就公式而放宽校验器。

## 评审清单

- 结果类别覆盖完整，各块互斥且顺序正确。
- 每个异常码只出现在能抛出它的块里，且没有块列出它抛不出的异常。
- 所有符号都已在实例 README 登记；每条新规则都有手册依据。
- 没有位型结果、隐藏谓词或被削弱的舍入模式条件。
- 实例 README 与 `specs/README.md` 的索引、计数和交叉引用已同步。
- `grep -R '{{' specs/*/` 为空，两个校验器均通过。

## 提交

提交要小而聚焦：一个指令组一处提交，README 改动一处，工具改动一处。未经维护者要求不要推送。
