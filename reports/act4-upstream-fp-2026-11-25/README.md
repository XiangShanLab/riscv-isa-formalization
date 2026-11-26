# ACT4 scalar floating-point additions, 2026-11-25

改动位于 `/nfs/home/pushaoyong/xs-work/riscv-arch-test`（实际 ACT4 仓库；`~/xs-work/act4` 不存在）。本地分支为 `fp-formalization-coverage`，基点和当前 HEAD 均为 `95ca74cb2dbadba39452cbe9b11b619b83b177a3`。**未提交、未推送、未创建 PR。**

依据是本工作区 `specs/f-d-q-zfh-zfhmin-zfbfmin-zfa-zfinx-zdinx-zhinx-zhinxmin/`，以及前次差异报告 §6。新增内容使用 ACT4 的 CSV testplan、注册式 Python generator/formatter、SystemVerilog coverpoint template、normative-rule YAML 和 CTP AsciiDoc。`tests/` 与生成的 `coverpoints/` 均经原生生成器生成。

浮点章节预览：[floating-point-ctp-preview.html](floating-point-ctp-preview.html)。

## 补充内容

| 原缺口 | ACT4 改动 |
|---|---|
| FMA 三源类别不完整 | H/S/D/Q 四种 FMA 均增加十个 FCLASS 类别的 1000 种三元组；覆盖 infinity × zero + qNaN 的 NV 要求 |
| 固定输入与舍入配置缺少完整交叉 | `cr_fp_rounding` 固定定向二元组/三元组，交叉五种静态 rm 和 DYN × 五种 frm；包括 MAX + 2、极端指数差、奇偶 tie、融合消去和两种加数符号 |
| 转换/平方根的定向边界 | `cr_fp_unary_rounding` 覆盖零附近、整数上下界，以及窄化的溢出、最小次正规数中点和正规/次正规数边界；BF16 的源次正规数中点单独处理 |
| 多源坏 NaN 装箱 | 单/双/三源分别 4/40/304 个用例：所有非空坏源掩码、正确装箱的 sNaN 幸存者，以及坏源低位统一取 normal 或 sNaN，并独立枚举各源符号；包含 S/H、D/H、D/S、Q/H、Q/S、Q/D 容器组合 |
| 缺少普通 Q testplan | 新增 `Q.csv`：算术、FMA、比较、分类、符号注入、转换、FLQ/FSQ；扩展 Zfa 的 Q 指令计划；覆盖 128 位寄存器中的窄格式装箱 |
| 缺少普通整数寄存器浮点计划 | 新增 Zfinx、Zdinx、Zhinx、Zhinxmin 和 XFP formatter：类别交叉、定向舍入、窄源高位忽略、结果符号扩展、RV32 D 寄存器对、x0/x1，以及预置 fflags 的保留和累积 |

装箱测试未声称枚举所有低位载荷组合。类别积也不是全部浮点位型的穷举。Q 的访存原子性仍明确标为单 hart 签名测试不能认证。

Zhinxmin 只生成其规定的转换；涉及 D 的转换额外要求 Zdinx。未把本工作区选择的保守 Dirty 策略、某种未对齐异常策略或保留 rm 编码的实现选择变成上游的强制结果。

取指异常继续使用 ACT4 已有的通用取指/虚拟内存/保护测试；本改动**没有**新增“每个浮点助记符 × 所有取指异常”的交叉矩阵，不能将本次结果解读成该矩阵已经覆盖。

## 为执行这些测试修复的基础支持

- binary128 数据使用 `.octa`，避免 `.dword` 截断高 64 位。
- RV32Q 检查全部四个结果字和 fflags；16 字节主签名槽的 canary 使用完整槽，trap canary 保持 XLEN 宽度，保证诊断字段对齐和签名标签一致。
- Zfinx 使用 fflags 时也生成对应的失败处理入口，无需 F 扩展。
- 精确扩宽转换在 GNU assembler 不接受显式 rm 的情况下，通过 `.insn` 保留合法 rm；编码与仓库导入的 riscv-opcodes decoder 核对。
- 同名的 XFP 指令不再生成重复的指令采样 case；XFP 覆盖点根据编码读取整数寄存器。
- 宽于 64 位的覆盖比较先映射到小的 bin 索引，避免把 96/128/192/256/384 位值直接作为覆盖 bin。

手册依据包括：Unprivileged ISA PDF p.133（精确转换也必须按通常规则解码 rm）、pp.135–136（FMA 的 infinity × zero）、p.140（坏装箱解释为 canonical NaN）、pp.168–170（Zfinx 系列、窄值、寄存器对和 x0）。对应本地 `sources/riscv-unprivileged.txt` 的锚点包含 6898、7096–7097、7286–7310、8732、8766、8772–8775。

## 已完成验证

| 检查 | 结果 |
|---|---|
| 原生 `make tests`，11 个 suite，RV32/RV64 | 22 套生成成功 |
| 再次调用原生生成器 | 1363 个生成文件逐个 SHA-256 不变 |
| Ruff、Ruff format、Pyright、`git diff --check` | 通过；Pyright 0 errors/0 warnings |
| `generators/testgen/tests/test_scalar_fp.py` | 12 项回归检查通过，包括独立 Fraction 中点计算、实际装载数据类别、装箱 bin、导入编码核对和寄存器对 |
| 相关汇编的对象编译，GNU toolchain 16.1.0，assembler `--fatal-warnings` | 1337/1337 通过；使用临时最小配置头，不是完整 UDB 配置构建 |
| Sail 0.16 期望签名 → 自检 ELF → Sail 与 Spike 各执行 | 448/448 文件通过；覆盖修改的常规浮点和 Sail 可执行的整数寄存器浮点文件 |
| Q 与 Sail 0.16 阻塞的 Zdinx 文件：Spike 生成签名并执行自检 | 407/407 文件通过，其中 339 个 Q 相关文件、68 个 Zdinx 相关文件；这是签名流程检查，不能替代独立参考模型比较 |
| RV32Q 签名故障注入 | 分别翻转首个结果四个 32 位字中的一个期望位，4/4 均正确拒绝（退出码 1），并核对失败寄存器、实际值与期望值 |
| 新增覆盖模板独立 Verilator 检查 | 194 个模板通过，未关闭 warning-as-error；尚未取得完整 ACT4 coverage hit 报告 |
| 规范条款名称及 coverpoint 引用 | 原生 norm table 生成通过；676 个展开后的覆盖点引用全部解析 |
| 浮点 CTP 章节 HTML 预览 | Asciidoctor `--failure-level=WARN` 通过；预览省略全书参数附表，非完整 CTP 构建 |

本次原生生成命令：

```sh
EXTENSIONS=F,D,Q,Zfh,Zfhmin,Zfbfmin,Zfa,Zfinx,Zdinx,Zhinx,Zhinxmin make tests
uv run ruff check
uv run ruff format --check
uv run pyright
uv run python -m unittest discover -s generators/testgen/tests -v
```

此机器实际使用临时 uv 并指定 `/usr/bin/python3`（3.12.3），未修改依赖锁文件。模型/编译的临时日志与 ELF 在 `/tmp/act4-fp-*`，交叉模型回归汇总为 `/tmp/act4-final-model-regression.log`，Spike 补充回归为 `/tmp/act4-spike-model-regression.log`。

## 贡献上游前仍需完成的集成验证

1. **参考模型。** Sail 0.16 不支持 Q；Zdinx 的 68 个文件在其 `fdext_regs.sail:291/321` 的 `flen >= 64` 断言处停止。已确认同一合法 RV32 指令 `fadd.d x22, x16, x30, rne` 能在 Spike 执行。现有本地上游 Sail 源码中的提交 `390a0784`（#2108）已将断言改为允许 Zdinx。尚未构建/运行该版本，也没有修改 ACT4 的版本检查、删除用例或忽略相应覆盖 bin。
2. **完整覆盖率。** 本机 Verilator 5.052 不支持 ACT4 脚本使用的 `--coverage-max-bins`；去掉该参数的诊断性尝试又遇到参数化 covergroup 的内部 `V3Param.cpp` 错误。独立模板检查已经通过，但仍需在支持完整 ACT4 harness 的模拟器版本上执行原生 `make coverage`。
3. **完整 CTP / UDB 构建。** 原生全书构建在 UDB 参数查询所需的安装步骤阻塞：GitHub 上固定版本 Z3 二进制下载反复超时。已通过生成表格、规范映射和浮点章节预览；尚未完成全书 HTML/PDF、完整 UDB 配置构建和整套 prek/CI。

因此，本地实现和上述局部/跨模型验证已完成，**不能标注为已通过完整上游 CI**。所有改动保留在工作区供审阅。


## 审查问题修正（2026-11-25）

独立审查发现的三项覆盖缺口及主线程复现的一项诊断缺陷均已修正，仍未提交：

1. `fsub` 将第二源符号取反以构造真实消去/中点；`fdiv` 使用独立除法向量，最小次正规数除以 2 形成下溢中点。CSV 和 SV 改用各自的 `sub`/`div` 模板，Q 规范映射同步更新。新增 Fraction 回归独立检查 H/S/D/Q 的运算结果。
2. 坏装箱增加独立源符号组合，覆盖 bin 同时区分符号；单/双/三源为 4/40/304 个用例。新增回归确认 FSGNJ/FSGNJN/FSGNJX 的第二源漏检会产生可观察的结果差异。
3. XFP 窄源覆盖用每源“十种类别 × 三种高位模式”的独立 wildcard bin，主规范覆盖点要求所有源的 bin 命中。实际 SV 分类函数在 RV32/RV64 上通过 120 个断言；Python 回归核对实际生成输入与全部 bin 的对应关系。
4. RV32Q 四字检查使用浮点失败入口，从临时 FP 内存恢复出错字，避免链接寄存器被 jal 覆盖。分别对四字做故障注入，Spike trace 核对 `failure_type=1`、`failing_reg=f31`、正确实际值及错误期望值，4/4 通过。诊断显示出错的 32 位字。

修正后复跑：原生 22 套生成、1363 个文件重复生成一致、12 项 unittest、Ruff/format/Pyright、1337 个对象编译、194 个独立 SV 模板、448 个 Sail→Sail/Spike 文件、407 个 Spike 签名流程文件、676 个规范引用均通过。新增 120 个 SV 分类断言及 4 个 RV32Q 错误诊断检查通过。浮点章节预览重新生成，无 Asciidoctor 警告；原生 testplan/norm table 使用已有规则快照成功生成，全书参数阶段仍未完成。

修正验证日志：`/tmp/act4-review-{generate,compile,model,spike,quad,template-lint,repro,doc-tables,doc-preview}.log`。完整 coverage/UDB/CI 的限制仍适用，不能视为已通过上游完整 CI。


## 2026-11-26：拆分 FMA 独立提交

本地分支 `act4` 已包含提交 `863b51346d17d9ee4b3553dd3b34fdfa85c23b46`，作者为 `xyz517 <yuanmiaomiao@bosc.ac.cn>`，尚未推送。

范围仅为现有 F/D/Zfh 的四种 FMA：三源十类的 1000 组合、9 个操作数三元组与 10 种静态/动态舍入配置，以及 304 种多源坏装箱组合；包括生成器、18 个 SV 模板、CSV、规范映射、文档和生成的汇编。利用已有 `TestChunk.split_name` 分组，按首源类别拆分，所有新增文件小于 500 KB。Q 与 XFP 基础设施及其他浮点改动仍保留未提交。

独立提交版本：288 个文件的 Sail 签名生成、Sail 自检与 Spike 交叉验证全部通过；922 个文件重复生成完全一致；18 个 SV 模板通过 Verilator；393 个规范映射引用可解析；F/D/Zfh 原生 testplan/norm 表及浮点章节预览生成通过。Ruff、Pyright、Prettier、codespell、文件大小、换行/空白、YAML、制表符及汇编指令检查直接执行通过。完整 `prek` 未通过：钩子安装在 NFS 上报 `Errno 39 Directory not empty`，另有 Go 依赖下载超时；未声明完整钩子、原生覆盖率或完整 UDB/CTP 流水线通过。

接回主工作区后重新生成 22 套测试，15 项 unittest 通过；对拆分前的 1115 个更改文件进行散列核对，变化只涉及 FMA 汇编和分组所需的三个源文件，其余原有改动保持。Git 暂存区为空，其他改动均未提交。

本次日志见 [fma-commit-validation/](fma-commit-validation/)。临时工作区、脚本及缓存已迁至 `~/tmp`；用户偏好已记录在 `~/.codex/AGENTS.md`。

用户要求直接在原来的 `act4` 主分支继续工作；已将该分支快进到 FMA 提交并删除临时工作分支，未推送。切换前后核对全部未提交文件的内容和暂存区，保持一致。
