[English](README.md) | 中文

# templates

新实例的骨架，只含结构与约定，不含任何指令语义。复制后替换全部 `{{…}}` 占位符，再填入
从手册推导出的内容。

| 文件 | 用途 |
|---|---|
| `delivery-README.md` | 复制为 `specs/<instance>/README.md`，承载该实例的全部共享定义 |
| `instruction.md` | 复制为 `specs/<instance>/instructions/<mnemonic>.md`，每个助记符组一份 |

## 占位符

| 占位符 | 含义 |
|---|---|
| `{{INSTANCE_TITLE}}` | 实例的可读标题 |
| `{{INSTANCE_SLUG}}` | `specs/` 下的目录名 |
| `{{MNEMONIC}}` | 助记符组，按公式中的写法（如 `\mathrm{FADD}`） |
| `{{EXT}}` | 扩展条件，如 `\mathrm{Ext}(F)` 或 `Zfhmin` |
| `{{UNSUPPORTED_CONFIGURATION}}` | 使指令非法的执行配置 |
| `{{ONE_LINE_DESCRIPTION}}`、`{{RESULT_CATEGORY}}`、`{{VARIANTS}}` | 标题与索引表的文字 |
| `{{SYMBOL}}`、`{{MEANING}}`、`{{VALUES}}`、`{{SOURCE}}` | 符号表中的一行 |
| `{{PRIVILEGE_CONFIGURATION}}` | 一类结果对应的特权模式合取 |
| `{{STATE_CONDITION}}`、`{{OPERAND_CONDITION}}` | 状态与操作数条件 |
| `{{DESTINATION}}`、`{{RESULT}}` | 目的寄存器/CSR/内存及其新值形式 |

## 新建实例

```bash
mkdir -p specs/{{INSTANCE_SLUG}}/instructions
cp templates/delivery-README.md specs/{{INSTANCE_SLUG}}/README.md
cp templates/instruction.md     specs/{{INSTANCE_SLUG}}/instructions/{{mnemonic}}.md
grep -R '{{' specs/*/   # 编辑完成后必须没有输出
```

然后按 [`CONTRIBUTING.md`](../CONTRIBUTING.zh.md) 操作：

1. 先写交付 README——符号、格式、值类、状态写入、异常优先级。之后用到的符号都必须先登记。
2. 每个助记符组一个指令文件；先写 `.0` 守卫块，再按求值顺序写各结果类别。
3. 对每个改动过的文件跑两个校验器。
4. 在 [`specs/README.md`](../specs/README.md) 的表中加入该实例。

## 骨架默认遵守的规则

- 每条公式一个 `aligned` 块；左端每行以 `&` 开头。
- 每行最多一个顶层 `\land`；`\mathrm{instr}=…` 是最后一个合取项。
- 右端为 `\{\, … \,\}`，`\mathrm{exception}` 在最后。
- 粘性状态用 `\mathrel{|}=` 更新。
- 指令文件只放结果公式；共享定义写在交付 README。
- 交付文档只用英文；本目录的中文说明见 [`README.zh.md`](README.zh.md)。

两个骨架本身即可通过校验：`python3 -I tools/check_md.py` 与
`python3 -I tools/check_style.py` 对它们返回 0，复制出来的文件从一个合法的结构开始。
替换占位符后，它们作为 `specs/` 的一部分接受校验。
