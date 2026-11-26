# FMV.X.H, FMV.H.X — half-precision moves

`FMV.X.H` copies the low 16 bits of $a$ to `rd`, sign-extending to `XLEN`; `FMV.H.X` writes the low 16 bits of `rs1` to `fd` and boxes them. Neither instruction rounds or raises a flag; writing `rd` alone leaves the floating-point state unchanged and writing `fd` sets `mstatus.FS` to `Dirty(3)`. Requires `Zfhmin` or `Zfbfmin`.

The `exception` field of every block below lists only the exceptions the instruction itself can raise, and reads `\mathrm{exception}=\varnothing` when it raises none; the instruction-fetch outcomes depend only on the fetch address and are stated once in the README, not repeated here.

**(FMV.X.H.0) Extension unavailable or effective FS Off → only IllegalInstruction(2)**

$$
\begin{aligned}
&\bigl(\bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\land(vsstatus.FS=\mathrm{Off}(0)\lor sstatus.FS=\mathrm{Off}(0))\bigr)\\
&\qquad\lor\ \neg\big(\mathrm{impl}(\mathrm{Zfhmin})\lor\mathrm{impl}(\mathrm{Zfbfmin})\big)\ \lor\ mstatus.FS=\mathrm{Off}(0)\bigr)\\
&\land\ (\mathrm{instr}=\mathrm{FMV.X.H})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(FMV.X.H.1) No H, M/S/U: raw bits of $a$ → `rd`, sign-extended to `XLEN`**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \big(\mathrm{impl}(\mathrm{Zfhmin})\lor\mathrm{impl}(\mathrm{Zfbfmin})\big)\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{instr}=\mathrm{FMV.X.H})\\
\end{aligned}
\longrightarrow
\{\, rd=\mathrm{sext}_{\mathrm{XLEN}}(f[rs1][15:0]),\ \mathrm{exception}=\varnothing \,\}
$$

**(FMV.X.H.2) H, M/HS/U: raw bits of $a$ → `rd`, sign-extended to `XLEN`**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \big(\mathrm{impl}(\mathrm{Zfhmin})\lor\mathrm{impl}(\mathrm{Zfbfmin})\big)\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{instr}=\mathrm{FMV.X.H})\\
\end{aligned}
\longrightarrow
\{\, rd=\mathrm{sext}_{\mathrm{XLEN}}(f[rs1][15:0]),\ \mathrm{exception}=\varnothing \,\}
$$

**(FMV.X.H.3) H, VS/VU: raw bits of $a$ → `rd`, sign-extended to `XLEN`**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \big(\mathrm{impl}(\mathrm{Zfhmin})\lor\mathrm{impl}(\mathrm{Zfbfmin})\big)\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{instr}=\mathrm{FMV.X.H})\\
\end{aligned}
\longrightarrow
\{\, rd=\mathrm{sext}_{\mathrm{XLEN}}(f[rs1][15:0]),\ \mathrm{exception}=\varnothing \,\}
$$

**(FMV.H.X.0) Extension unavailable or effective FS Off → only IllegalInstruction(2)**

$$
\begin{aligned}
&\bigl(\bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\land(vsstatus.FS=\mathrm{Off}(0)\lor sstatus.FS=\mathrm{Off}(0))\bigr)\\
&\qquad\lor\ \neg\big(\mathrm{impl}(\mathrm{Zfhmin})\lor\mathrm{impl}(\mathrm{Zfbfmin})\big)\ \lor\ mstatus.FS=\mathrm{Off}(0)\bigr)\\
&\land\ (\mathrm{instr}=\mathrm{FMV.H.X})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(FMV.H.X.1) No H, M/S/U: low 16 bits of `rs1` → `fd`, boxed**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \big(\mathrm{impl}(\mathrm{Zfhmin})\lor\mathrm{impl}(\mathrm{Zfbfmin})\big)\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{instr}=\mathrm{FMV.H.X})\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_H(x[rs1][15:0]),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FMV.H.X.2) H, M/HS/U: low 16 bits of `rs1` → `fd`, boxed**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \big(\mathrm{impl}(\mathrm{Zfhmin})\lor\mathrm{impl}(\mathrm{Zfbfmin})\big)\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{instr}=\mathrm{FMV.H.X})\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_H(x[rs1][15:0]),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FMV.H.X.3) H, VS/VU: low 16 bits of `rs1` → `fd`, boxed**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \big(\mathrm{impl}(\mathrm{Zfhmin})\lor\mathrm{impl}(\mathrm{Zfbfmin})\big)\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{instr}=\mathrm{FMV.H.X})\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_H(x[rs1][15:0]),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$
