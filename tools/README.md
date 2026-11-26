# tools

所有脚本都用 `-I` 运行，并把目标 Markdown 作为参数传入。

## 校验器（三个交付通用）

```bash
python3 -I tools/check_md.py    <file.md>
python3 -I tools/check_style.py <file.md>
```

两者幂等，退出码 0 表示通过。`out/` 下的 README 与每个指令文件都必须过这两项。

| 脚本 | 作用 |
|---|---|
| `check_md.py` | 公式定界符配对、`aligned`/`cases`/`pmatrix` 环境配平、表格列数、行内数学定界符、表格内竖线 |
| `check_style.py` | 公式块左端以 `&` 开头、`instr` 在末、每行最多一个顶层 `\land`、右端形状、`exception` 在末、标志粘性、禁用 `\wedge`/`\vee` 与位型字面量 |

## 退役文档的脚本

以下脚本属于已删除的 compact 单文件文档（`riscv-fp-compact.md`）及其 dist 打包流程，
当前交付不使用，保留作历史参考：

| 脚本 | 原用途 |
|---|---|
| `validate.sh` | compact 文档的一键校验入口（默认目标已不存在） |
| `audit_formulas.py` | compact 公式审计（要求首行为 `mstatus.FS`） |
| `gen_section25.py` / `gen_section25_grid.py` | 重写 compact 文档 §2.5 组合表 |
| `expand_config_block.py` | 一次性变换：`enabled(I)` → 完整 CSR 配置块 |
| `normalize_aligned.py` / `normalize_aligned_v1.py` | 历史排版归一化，会重排合取项，只可在副本上运行 |
| `build_fp_instructions.py`、`validate_instructions.py`、`check_fp_semantics.py`、`package_scalar_fp.py` | dist 快照的生成、校验与打包 |
| `fp_arithmetic_seed.json` | 上述生成脚本的输入种子 |
