# FLI.H, FLI.S, FLI.D, FLI.Q — load immediate

`FLI.F` writes the constant selected by the five-bit immediate field, $\mathrm{FLI}_F(\mathrm{imm})$, to `fd`. The constants are listed in §2.1 of the [index](../README.md); entry 1 is the minimum positive normal of format $F$, and entry 29 is $2^{16}$ except in H, where it is $+\infty_F$. No constant is a signaling NaN, so the instruction raises no flag and performs no rounding. Formats H, S, D, Q; the extension condition is `impl(Ext(F)) ∧ impl(Zfa)`.

The manual also allows `FLI.H` when `Zvfh` is implemented without `Zfh`
(`sources/riscv-unprivileged.txt:8558-8572`). Vector configurations are outside this document, so
the H condition is written as `impl(Zfh)`; a configuration that implements `Zvfh` but not `Zfh`
adds `impl(Zvfh)` to it.

The `exception` field of every block below lists only the exceptions the instruction itself can raise, and reads `\mathrm{exception}=\varnothing` when it raises none; the instruction-fetch outcomes depend only on the fetch address and are stated once in the README, not repeated here.

**(FLI.0) Extension unavailable or effective FS Off → only IllegalInstruction(2)**

$$
\begin{aligned}
&\bigl(\bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\land(vsstatus.FS=\mathrm{Off}(0)\lor sstatus.FS=\mathrm{Off}(0))\bigr)\\
&\qquad\lor\ \neg\mathrm{impl}(\mathrm{Ext}(F))\ \lor\ \neg\mathrm{impl}(\mathrm{Zfa})\ \lor\ mstatus.FS=\mathrm{Off}(0)\bigr)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FLI}.F)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(FLI.1) No H, M/S/U: the encoded constant → `fd`**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{imm}\in\{0,1,\dots,31\})\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FLI}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{FLI}_F(\mathrm{imm})),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FLI.2) H, M/HS/U: the encoded constant → `fd`**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{imm}\in\{0,1,\dots,31\})\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FLI}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{FLI}_F(\mathrm{imm})),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FLI.3) H, VS/VU: the encoded constant → `fd`**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{imm}\in\{0,1,\dots,31\})\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FLI}.F)\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{enc}_{F}(\mathrm{FLI}_F(\mathrm{imm})),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$
