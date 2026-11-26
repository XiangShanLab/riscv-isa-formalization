# FSGNJ, FSGNJN, FSGNJX — sign injection

`FSGNJ` takes every bit except the sign from $a$ (rs1) and takes the sign from $b$ (rs2);
`FSGNJN` takes the opposite of the sign of $b$; `FSGNJX` takes the exclusive OR of the two signs.
Exponent and significand are copied verbatim, NaNs are not canonicalized, and no flag is raised.
Formats H, S, D, Q; the extension condition is `impl(Ext(F))`.

The `exception` field of every block below lists only the exceptions the instruction itself can raise, and reads `\mathrm{exception}=\varnothing` when it raises none; the instruction-fetch outcomes depend only on the fetch address and are stated once in the README, not repeated here.

**(FSGNJ.0) Extension unavailable or effective FS Off → only IllegalInstruction(2)**

$$
\begin{aligned}
&\bigl(\bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\land(vsstatus.FS=\mathrm{Off}(0)\lor sstatus.FS=\mathrm{Off}(0))\bigr)\\
&\qquad\lor\ \neg\mathrm{impl}(\mathrm{Ext}(F))\ \lor\ mstatus.FS=\mathrm{Off}(0)\bigr)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ \bigl(\mathrm{instr}\in\{\mathrm{FSGNJ}.F,\mathrm{FSGNJN}.F,\mathrm{FSGNJX}.F\}\bigr)
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(FSGNJ.1) No H, M/S/U: `FSGNJ`: both sources are not correctly NaN-boxed → canonical qNaN**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \bigl(\neg\mathrm{boxed}_{F}(f[rs1])\land\neg\mathrm{boxed}_{F}(f[rs2])\bigr)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FSGNJ}.F)
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_{F}(0,e_{\max},2^{w_f-1}),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSGNJ.2) No H, M/S/U: `FSGNJ`: $a$ is not correctly NaN-boxed → canonical qNaN with the injected sign**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \neg\mathrm{boxed}_{F}(f[rs1])\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FSGNJ}.F)
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_{F}(s_b,e_{\max},2^{w_f-1}),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSGNJ.3) No H, M/S/U: `FSGNJ`: $b$ is not correctly NaN-boxed → $a$'s magnitude with the injected sign**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \neg\mathrm{boxed}_{F}(f[rs2])\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FSGNJ}.F)
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_{F}(0,e_a,f_a),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSGNJ.4) H, M/HS/U: `FSGNJ`: both sources are not correctly NaN-boxed → canonical qNaN**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \bigl(\neg\mathrm{boxed}_{F}(f[rs1])\land\neg\mathrm{boxed}_{F}(f[rs2])\bigr)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FSGNJ}.F)
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_{F}(0,e_{\max},2^{w_f-1}),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSGNJ.5) H, M/HS/U: `FSGNJ`: $a$ is not correctly NaN-boxed → canonical qNaN with the injected sign**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \neg\mathrm{boxed}_{F}(f[rs1])\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FSGNJ}.F)
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_{F}(s_b,e_{\max},2^{w_f-1}),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSGNJ.6) H, M/HS/U: `FSGNJ`: $b$ is not correctly NaN-boxed → $a$'s magnitude with the injected sign**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \neg\mathrm{boxed}_{F}(f[rs2])\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FSGNJ}.F)
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_{F}(0,e_a,f_a),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSGNJ.7) H, VS/VU: `FSGNJ`: both sources are not correctly NaN-boxed → canonical qNaN**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \bigl(\neg\mathrm{boxed}_{F}(f[rs1])\land\neg\mathrm{boxed}_{F}(f[rs2])\bigr)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FSGNJ}.F)
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_{F}(0,e_{\max},2^{w_f-1}),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSGNJ.8) H, VS/VU: `FSGNJ`: $a$ is not correctly NaN-boxed → canonical qNaN with the injected sign**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \neg\mathrm{boxed}_{F}(f[rs1])\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FSGNJ}.F)
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_{F}(s_b,e_{\max},2^{w_f-1}),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSGNJ.9) H, VS/VU: `FSGNJ`: $b$ is not correctly NaN-boxed → $a$'s magnitude with the injected sign**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \neg\mathrm{boxed}_{F}(f[rs2])\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FSGNJ}.F)
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_{F}(0,e_a,f_a),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSGNJ.10) No H, M/S/U: `FSGNJ`: sign of $b$, exponent and significand of $a$**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FSGNJ}.F)
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_{F}(s_b,e_a,f_a),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSGNJ.11) H, M/HS/U: `FSGNJ`: sign of $b$, exponent and significand of $a$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FSGNJ}.F)
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_{F}(s_b,e_a,f_a),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSGNJ.12) H, VS/VU: `FSGNJ`: sign of $b$, exponent and significand of $a$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FSGNJ}.F)
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_{F}(s_b,e_a,f_a),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSGNJN.1) No H, M/S/U: `FSGNJN`: both sources are not correctly NaN-boxed → canonical qNaN**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \bigl(\neg\mathrm{boxed}_{F}(f[rs1])\land\neg\mathrm{boxed}_{F}(f[rs2])\bigr)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FSGNJN}.F)
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_{F}(1,e_{\max},2^{w_f-1}),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSGNJN.2) No H, M/S/U: `FSGNJN`: $a$ is not correctly NaN-boxed → canonical qNaN with the injected sign**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \neg\mathrm{boxed}_{F}(f[rs1])\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FSGNJN}.F)
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_{F}(1\oplus s_b,e_{\max},2^{w_f-1}),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSGNJN.3) No H, M/S/U: `FSGNJN`: $b$ is not correctly NaN-boxed → $a$'s magnitude with the injected sign**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \neg\mathrm{boxed}_{F}(f[rs2])\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FSGNJN}.F)
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_{F}(1,e_a,f_a),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSGNJN.4) H, M/HS/U: `FSGNJN`: both sources are not correctly NaN-boxed → canonical qNaN**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \bigl(\neg\mathrm{boxed}_{F}(f[rs1])\land\neg\mathrm{boxed}_{F}(f[rs2])\bigr)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FSGNJN}.F)
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_{F}(1,e_{\max},2^{w_f-1}),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSGNJN.5) H, M/HS/U: `FSGNJN`: $a$ is not correctly NaN-boxed → canonical qNaN with the injected sign**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \neg\mathrm{boxed}_{F}(f[rs1])\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FSGNJN}.F)
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_{F}(1\oplus s_b,e_{\max},2^{w_f-1}),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSGNJN.6) H, M/HS/U: `FSGNJN`: $b$ is not correctly NaN-boxed → $a$'s magnitude with the injected sign**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \neg\mathrm{boxed}_{F}(f[rs2])\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FSGNJN}.F)
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_{F}(1,e_a,f_a),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSGNJN.7) H, VS/VU: `FSGNJN`: both sources are not correctly NaN-boxed → canonical qNaN**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \bigl(\neg\mathrm{boxed}_{F}(f[rs1])\land\neg\mathrm{boxed}_{F}(f[rs2])\bigr)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FSGNJN}.F)
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_{F}(1,e_{\max},2^{w_f-1}),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSGNJN.8) H, VS/VU: `FSGNJN`: $a$ is not correctly NaN-boxed → canonical qNaN with the injected sign**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \neg\mathrm{boxed}_{F}(f[rs1])\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FSGNJN}.F)
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_{F}(1\oplus s_b,e_{\max},2^{w_f-1}),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSGNJN.9) H, VS/VU: `FSGNJN`: $b$ is not correctly NaN-boxed → $a$'s magnitude with the injected sign**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \neg\mathrm{boxed}_{F}(f[rs2])\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FSGNJN}.F)
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_{F}(1,e_a,f_a),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSGNJN.10) No H, M/S/U: `FSGNJN`: opposite sign of $b$, exponent and significand of $a$**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FSGNJN}.F)
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_{F}(1\oplus s_b,e_a,f_a),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSGNJN.11) H, M/HS/U: `FSGNJN`: opposite sign of $b$, exponent and significand of $a$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FSGNJN}.F)
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_{F}(1\oplus s_b,e_a,f_a),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSGNJN.12) H, VS/VU: `FSGNJN`: opposite sign of $b$, exponent and significand of $a$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FSGNJN}.F)
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_{F}(1\oplus s_b,e_a,f_a),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSGNJX.1) No H, M/S/U: `FSGNJX`: both sources are not correctly NaN-boxed → canonical qNaN**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \bigl(\neg\mathrm{boxed}_{F}(f[rs1])\land\neg\mathrm{boxed}_{F}(f[rs2])\bigr)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FSGNJX}.F)
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_{F}(0,e_{\max},2^{w_f-1}),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSGNJX.2) No H, M/S/U: `FSGNJX`: $a$ is not correctly NaN-boxed → canonical qNaN with the injected sign**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \neg\mathrm{boxed}_{F}(f[rs1])\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FSGNJX}.F)
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_{F}(s_b,e_{\max},2^{w_f-1}),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSGNJX.3) No H, M/S/U: `FSGNJX`: $b$ is not correctly NaN-boxed → $a$'s magnitude with the injected sign**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \neg\mathrm{boxed}_{F}(f[rs2])\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FSGNJX}.F)
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_{F}(s_a,e_a,f_a),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSGNJX.4) H, M/HS/U: `FSGNJX`: both sources are not correctly NaN-boxed → canonical qNaN**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \bigl(\neg\mathrm{boxed}_{F}(f[rs1])\land\neg\mathrm{boxed}_{F}(f[rs2])\bigr)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FSGNJX}.F)
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_{F}(0,e_{\max},2^{w_f-1}),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSGNJX.5) H, M/HS/U: `FSGNJX`: $a$ is not correctly NaN-boxed → canonical qNaN with the injected sign**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \neg\mathrm{boxed}_{F}(f[rs1])\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FSGNJX}.F)
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_{F}(s_b,e_{\max},2^{w_f-1}),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSGNJX.6) H, M/HS/U: `FSGNJX`: $b$ is not correctly NaN-boxed → $a$'s magnitude with the injected sign**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \neg\mathrm{boxed}_{F}(f[rs2])\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FSGNJX}.F)
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_{F}(s_a,e_a,f_a),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSGNJX.7) H, VS/VU: `FSGNJX`: both sources are not correctly NaN-boxed → canonical qNaN**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \bigl(\neg\mathrm{boxed}_{F}(f[rs1])\land\neg\mathrm{boxed}_{F}(f[rs2])\bigr)\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FSGNJX}.F)
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_{F}(0,e_{\max},2^{w_f-1}),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSGNJX.8) H, VS/VU: `FSGNJX`: $a$ is not correctly NaN-boxed → canonical qNaN with the injected sign**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \neg\mathrm{boxed}_{F}(f[rs1])\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FSGNJX}.F)
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_{F}(s_b,e_{\max},2^{w_f-1}),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSGNJX.9) H, VS/VU: `FSGNJX`: $b$ is not correctly NaN-boxed → $a$'s magnitude with the injected sign**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \neg\mathrm{boxed}_{F}(f[rs2])\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FSGNJX}.F)
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_{F}(s_a,e_a,f_a),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSGNJX.10) No H, M/S/U: `FSGNJX`: XOR of the two signs, exponent and significand of $a$**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FSGNJX}.F)
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_{F}(s_a\oplus s_b,e_a,f_a),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSGNJX.11) H, M/HS/U: `FSGNJX`: XOR of the two signs, exponent and significand of $a$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FSGNJX}.F)
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_{F}(s_a\oplus s_b,e_a,f_a),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSGNJX.12) H, VS/VU: `FSGNJX`: XOR of the two signs, exponent and significand of $a$**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{Ext}(F))\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (F\in\{\mathrm{H},\mathrm{S},\mathrm{D},\mathrm{Q}\})\\
&\land\ (\mathrm{instr}=\mathrm{FSGNJX}.F)
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_{F}(s_a\oplus s_b,e_a,f_a),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$
