[English](README.md) | 中文

# 已发布实例

`specs/` 下的每个目录是一个**实例**：用一个指令家族（或一组密切相关扩展）的完整形式化，
按 [`workflow.md`](../workflow.md) 的方法和 [`templates/`](../templates) 的骨架产出。
框架本身不依赖任何实例；新增扩展家族就是新建一个目录并在下表加一行。

每个实例的结构相同：

```
specs/<instance>/
├── README.md          # 全部共享定义：公式形态、符号、书写约定、异常
└── instructions/      # 每个助记符组一个文件，只放结果公式
```

| 实例 | 范围 | 依据章节 | 文件数 | 公式块数 | 文档 |
|---|---|---|---:|---:|---|
| [`f-d-q-zfh-zfhmin-zfbfmin-zfa-zfinx-zdinx-zhinx-zhinxmin/`](f-d-q-zfh-zfhmin-zfbfmin-zfa-zfinx-zdinx-zhinx-zhinxmin/README.md) | 标量浮点：`F`、`D`、`Q`、`Zfh`、`Zfhmin`、`Zfbfmin`、`Zfa`、`Zfinx`、`Zdinx`、`Zhinx`、`Zhinxmin` | Unpriv. 21–27；Priv. FS/SD 与 `stateen` | 43 | 1504 | [EN](f-d-q-zfh-zfhmin-zfbfmin-zfa-zfinx-zdinx-zhinx-zhinxmin/README.md) · [中文](f-d-q-zfh-zfhmin-zfbfmin-zfa-zfinx-zdinx-zhinx-zhinxmin/README.zh.md)（阅读辅助） |
| [`v-zvfh-zvfhmin-zvfbfmin-zvfbfwma/`](v-zvfh-zvfhmin-zvfbfmin-zvfbfwma/README.md) | 向量浮点：`V` 与 `Zvfh`、`Zvfhmin`、`Zvfbfmin`、`Zvfbfwma` | Unpriv. 25、31；Priv. VS/SD | 34 | 193 | [EN](v-zvfh-zvfhmin-zvfbfmin-zvfbfwma/README.md) |
| [`h-svinval/`](h-svinval/README.md) | `HLV`、`HSV`、`HLVX`、`HFENCE.VVMA`、`HFENCE.GVMA`、`HINVAL.VVMA`、`HINVAL.GVMA` | Priv. 15；Svinval | 5 | 45 | [EN](h-svinval/README.md) |

标量实例中的中文文件是其英文 `README.md` 的译本，供阅读使用；英文文档为准。

## 共享约定

所有实例采用同一外形；所有共享定义都写在各自的交付 README 里。

- 每条公式一个 `aligned` 块，左端是合取，右端是 `\{\, … \,\}`。
- 左端各组按固定顺序排列，`\mathrm{instr}=…` 在最后。
- 右端顺序：目的 → 状态写入 → 粘性标志 → `exception` 在最后。
- 公式 `.0` 是守卫：扩展不可用或执行配置不允许，只抛对应异常、不写任何状态。
- 指令文件只放结果公式；符号、格式、值类与异常优先级在交付 README 中定义一次。
- 粘性状态用 `\mathrel{|}=` 更新；结果是域内规范值或类别，不写硬件位型。

## 新增实例

1. 读 [`CONTRIBUTING.md`](../CONTRIBUTING.md) 与 [`workflow.md`](../workflow.md) 的方法；
   非浮点家族看 §11。
2. 从 [`templates/`](../templates) 复制骨架，替换全部 `{{…}}` 占位符。
3. 先写交付 README，再写指令文件。
4. 对每个文件跑两个校验器，并在上表加一行。

## 校验

在仓库根目录运行：

```bash
find specs -name '*.md' -exec python3 -I tools/check_md.py {} \;
find specs -name '*.md' -exec python3 -I tools/check_style.py {} \;
```

若实例的粘性状态不是 `fcsr.fflags` 或 `vxsat`，给 `check_style.py` 加
`--sticky-flag <name>`。

## 计数

“文件数”指 `instructions/` 下的 `*.md` 文件数；“公式块数”指粗体 `**(…)**` 标题的个数，
每个公式一条。新增或扩展实例时手工维护本表。
