# FCLASS — floating-point classify

`FCLASS` writes to $rd$ a one-hot mask classifying $x=\mathrm{val}_F(a)$: bit 0 for $-\infty_F$, bit 7 for $+\infty_F$, and the remaining bits for negative normal, negative subnormal, $-0_F$, $+0_F$, positive subnormal, positive normal, signaling NaN, and quiet NaN. No flag is raised. Formats H, S, D, Q; the extension condition is `impl(Ext(F))`.

The `exception` field of every block below lists only the exceptions the instruction itself can raise, and reads `\mathrm{exception}=\varnothing` when it raises none; the instruction-fetch outcomes depend only on the fetch address and are stated once in the README, not repeated here.

**(FCLASS.0) Extension unavailable or effective FS Off → only IllegalInstruction(2)**

$$
\begin{aligned}
&\bigl(\bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\land(vsstatus.FS=\mathrm{Off}(0)\lor sstatus.FS=\mathrm{Off}(0))\bigr)\\
&\qquad\lor\ \neg\mathrm{impl}(\mathrm{Ext}(F))\ \lor\ mstatus.FS=\mathrm{Off}(0)\bigr)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FCLASS}.F)
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(FCLASS.1) No H, M/S/U: $a$ is not correctly NaN-boxed → $rd=2^{9}$**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \neg\mathrm{boxed}_{F}(f[rs1])\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FCLASS}.F)\\
\end{aligned}
\longrightarrow
\{\, rd=2^{9},\ rd[\mathrm{XLEN}-1:10]=0,\ \mathrm{exception}=\varnothing \,\}
$$

**(FCLASS.2) H, M/HS/U: $a$ is not correctly NaN-boxed → $rd=2^{9}$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \neg\mathrm{boxed}_{F}(f[rs1])\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FCLASS}.F)\\
\end{aligned}
\longrightarrow
\{\, rd=2^{9},\ rd[\mathrm{XLEN}-1:10]=0,\ \mathrm{exception}=\varnothing \,\}
$$

**(FCLASS.3) H, VS/VU: $a$ is not correctly NaN-boxed → $rd=2^{9}$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \neg\mathrm{boxed}_{F}(f[rs1])\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FCLASS}.F)\\
\end{aligned}
\longrightarrow
\{\, rd=2^{9},\ rd[\mathrm{XLEN}-1:10]=0,\ \mathrm{exception}=\varnothing \,\}
$$

**(FCLASS.4) No H, M/S/U: $a$ is $-\infty_F$ → $rd=2^{0}$**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (a=-\infty_F)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FCLASS}.F)\\
\end{aligned}
\longrightarrow
\{\, rd=2^{0},\ rd[\mathrm{XLEN}-1:10]=0,\ \mathrm{exception}=\varnothing \,\}
$$

**(FCLASS.5) H, M/HS/U: $a$ is $-\infty_F$ → $rd=2^{0}$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (a=-\infty_F)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FCLASS}.F)\\
\end{aligned}
\longrightarrow
\{\, rd=2^{0},\ rd[\mathrm{XLEN}-1:10]=0,\ \mathrm{exception}=\varnothing \,\}
$$

**(FCLASS.6) H, VS/VU: $a$ is $-\infty_F$ → $rd=2^{0}$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (a=-\infty_F)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FCLASS}.F)\\
\end{aligned}
\longrightarrow
\{\, rd=2^{0},\ rd[\mathrm{XLEN}-1:10]=0,\ \mathrm{exception}=\varnothing \,\}
$$

**(FCLASS.7) No H, M/S/U: $a$ is negative normal → $rd=2^{1}$**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big((1\le e_a\le e_{\max}-1)\land(s_a=1)\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FCLASS}.F)\\
\end{aligned}
\longrightarrow
\{\, rd=2^{1},\ rd[\mathrm{XLEN}-1:10]=0,\ \mathrm{exception}=\varnothing \,\}
$$

**(FCLASS.8) H, M/HS/U: $a$ is negative normal → $rd=2^{1}$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big((1\le e_a\le e_{\max}-1)\land(s_a=1)\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FCLASS}.F)\\
\end{aligned}
\longrightarrow
\{\, rd=2^{1},\ rd[\mathrm{XLEN}-1:10]=0,\ \mathrm{exception}=\varnothing \,\}
$$

**(FCLASS.9) H, VS/VU: $a$ is negative normal → $rd=2^{1}$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big((1\le e_a\le e_{\max}-1)\land(s_a=1)\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FCLASS}.F)\\
\end{aligned}
\longrightarrow
\{\, rd=2^{1},\ rd[\mathrm{XLEN}-1:10]=0,\ \mathrm{exception}=\varnothing \,\}
$$

**(FCLASS.10) No H, M/S/U: $a$ is negative subnormal → $rd=2^{2}$**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big((e_a=0\land1\le f_a\le f_{\max})\land(s_a=1)\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FCLASS}.F)\\
\end{aligned}
\longrightarrow
\{\, rd=2^{2},\ rd[\mathrm{XLEN}-1:10]=0,\ \mathrm{exception}=\varnothing \,\}
$$

**(FCLASS.11) H, M/HS/U: $a$ is negative subnormal → $rd=2^{2}$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big((e_a=0\land1\le f_a\le f_{\max})\land(s_a=1)\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FCLASS}.F)\\
\end{aligned}
\longrightarrow
\{\, rd=2^{2},\ rd[\mathrm{XLEN}-1:10]=0,\ \mathrm{exception}=\varnothing \,\}
$$

**(FCLASS.12) H, VS/VU: $a$ is negative subnormal → $rd=2^{2}$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big((e_a=0\land1\le f_a\le f_{\max})\land(s_a=1)\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FCLASS}.F)\\
\end{aligned}
\longrightarrow
\{\, rd=2^{2},\ rd[\mathrm{XLEN}-1:10]=0,\ \mathrm{exception}=\varnothing \,\}
$$

**(FCLASS.13) No H, M/S/U: $a$ is $-0_F$ → $rd=2^{3}$**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ ((s_a=1\land e_a=0\land f_a=0))\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FCLASS}.F)\\
\end{aligned}
\longrightarrow
\{\, rd=2^{3},\ rd[\mathrm{XLEN}-1:10]=0,\ \mathrm{exception}=\varnothing \,\}
$$

**(FCLASS.14) H, M/HS/U: $a$ is $-0_F$ → $rd=2^{3}$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ ((s_a=1\land e_a=0\land f_a=0))\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FCLASS}.F)\\
\end{aligned}
\longrightarrow
\{\, rd=2^{3},\ rd[\mathrm{XLEN}-1:10]=0,\ \mathrm{exception}=\varnothing \,\}
$$

**(FCLASS.15) H, VS/VU: $a$ is $-0_F$ → $rd=2^{3}$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ ((s_a=1\land e_a=0\land f_a=0))\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FCLASS}.F)\\
\end{aligned}
\longrightarrow
\{\, rd=2^{3},\ rd[\mathrm{XLEN}-1:10]=0,\ \mathrm{exception}=\varnothing \,\}
$$

**(FCLASS.16) No H, M/S/U: $a$ is $+0_F$ → $rd=2^{4}$**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ ((s_a=0\land e_a=0\land f_a=0))\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FCLASS}.F)\\
\end{aligned}
\longrightarrow
\{\, rd=2^{4},\ rd[\mathrm{XLEN}-1:10]=0,\ \mathrm{exception}=\varnothing \,\}
$$

**(FCLASS.17) H, M/HS/U: $a$ is $+0_F$ → $rd=2^{4}$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ ((s_a=0\land e_a=0\land f_a=0))\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FCLASS}.F)\\
\end{aligned}
\longrightarrow
\{\, rd=2^{4},\ rd[\mathrm{XLEN}-1:10]=0,\ \mathrm{exception}=\varnothing \,\}
$$

**(FCLASS.18) H, VS/VU: $a$ is $+0_F$ → $rd=2^{4}$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ ((s_a=0\land e_a=0\land f_a=0))\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FCLASS}.F)\\
\end{aligned}
\longrightarrow
\{\, rd=2^{4},\ rd[\mathrm{XLEN}-1:10]=0,\ \mathrm{exception}=\varnothing \,\}
$$

**(FCLASS.19) No H, M/S/U: $a$ is positive subnormal → $rd=2^{5}$**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big((e_a=0\land1\le f_a\le f_{\max})\land(s_a=0)\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FCLASS}.F)\\
\end{aligned}
\longrightarrow
\{\, rd=2^{5},\ rd[\mathrm{XLEN}-1:10]=0,\ \mathrm{exception}=\varnothing \,\}
$$

**(FCLASS.20) H, M/HS/U: $a$ is positive subnormal → $rd=2^{5}$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big((e_a=0\land1\le f_a\le f_{\max})\land(s_a=0)\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FCLASS}.F)\\
\end{aligned}
\longrightarrow
\{\, rd=2^{5},\ rd[\mathrm{XLEN}-1:10]=0,\ \mathrm{exception}=\varnothing \,\}
$$

**(FCLASS.21) H, VS/VU: $a$ is positive subnormal → $rd=2^{5}$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big((e_a=0\land1\le f_a\le f_{\max})\land(s_a=0)\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FCLASS}.F)\\
\end{aligned}
\longrightarrow
\{\, rd=2^{5},\ rd[\mathrm{XLEN}-1:10]=0,\ \mathrm{exception}=\varnothing \,\}
$$

**(FCLASS.22) No H, M/S/U: $a$ is positive normal → $rd=2^{6}$**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big((1\le e_a\le e_{\max}-1)\land(s_a=0)\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FCLASS}.F)\\
\end{aligned}
\longrightarrow
\{\, rd=2^{6},\ rd[\mathrm{XLEN}-1:10]=0,\ \mathrm{exception}=\varnothing \,\}
$$

**(FCLASS.23) H, M/HS/U: $a$ is positive normal → $rd=2^{6}$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big((1\le e_a\le e_{\max}-1)\land(s_a=0)\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FCLASS}.F)\\
\end{aligned}
\longrightarrow
\{\, rd=2^{6},\ rd[\mathrm{XLEN}-1:10]=0,\ \mathrm{exception}=\varnothing \,\}
$$

**(FCLASS.24) H, VS/VU: $a$ is positive normal → $rd=2^{6}$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \big((1\le e_a\le e_{\max}-1)\land(s_a=0)\big)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FCLASS}.F)\\
\end{aligned}
\longrightarrow
\{\, rd=2^{6},\ rd[\mathrm{XLEN}-1:10]=0,\ \mathrm{exception}=\varnothing \,\}
$$

**(FCLASS.25) No H, M/S/U: $a$ is $+\infty_F$ → $rd=2^{7}$**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (a=+\infty_F)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FCLASS}.F)\\
\end{aligned}
\longrightarrow
\{\, rd=2^{7},\ rd[\mathrm{XLEN}-1:10]=0,\ \mathrm{exception}=\varnothing \,\}
$$

**(FCLASS.26) H, M/HS/U: $a$ is $+\infty_F$ → $rd=2^{7}$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (a=+\infty_F)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FCLASS}.F)\\
\end{aligned}
\longrightarrow
\{\, rd=2^{7},\ rd[\mathrm{XLEN}-1:10]=0,\ \mathrm{exception}=\varnothing \,\}
$$

**(FCLASS.27) H, VS/VU: $a$ is $+\infty_F$ → $rd=2^{7}$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (a=+\infty_F)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FCLASS}.F)\\
\end{aligned}
\longrightarrow
\{\, rd=2^{7},\ rd[\mathrm{XLEN}-1:10]=0,\ \mathrm{exception}=\varnothing \,\}
$$

**(FCLASS.28) No H, M/S/U: $a$ is sNaN → $rd=2^{8}$**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FCLASS}.F)\\
\end{aligned}
\longrightarrow
\{\, rd=2^{8},\ rd[\mathrm{XLEN}-1:10]=0,\ \mathrm{exception}=\varnothing \,\}
$$

**(FCLASS.29) H, M/HS/U: $a$ is sNaN → $rd=2^{8}$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FCLASS}.F)\\
\end{aligned}
\longrightarrow
\{\, rd=2^{8},\ rd[\mathrm{XLEN}-1:10]=0,\ \mathrm{exception}=\varnothing \,\}
$$

**(FCLASS.30) H, VS/VU: $a$ is sNaN → $rd=2^{8}$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=0)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FCLASS}.F)\\
\end{aligned}
\longrightarrow
\{\, rd=2^{8},\ rd[\mathrm{XLEN}-1:10]=0,\ \mathrm{exception}=\varnothing \,\}
$$

**(FCLASS.31) No H, M/S/U: $a$ is qNaN → $rd=2^{9}$**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=1)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FCLASS}.F)\\
\end{aligned}
\longrightarrow
\{\, rd=2^{9},\ rd[\mathrm{XLEN}-1:10]=0,\ \mathrm{exception}=\varnothing \,\}
$$

**(FCLASS.32) H, M/HS/U: $a$ is qNaN → $rd=2^{9}$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=1)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FCLASS}.F)\\
\end{aligned}
\longrightarrow
\{\, rd=2^{9},\ rd[\mathrm{XLEN}-1:10]=0,\ \mathrm{exception}=\varnothing \,\}
$$

**(FCLASS.33) H, VS/VU: $a$ is qNaN → $rd=2^{9}$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (e_a=e_{\max}\land1\le f_a\le f_{\max}\land f_a[w_f-1]=1)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FCLASS}.F)\\
\end{aligned}
\longrightarrow
\{\, rd=2^{9},\ rd[\mathrm{XLEN}-1:10]=0,\ \mathrm{exception}=\varnothing \,\}
$$
