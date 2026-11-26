# FCVTMOD.W.D — modular convert to signed 32-bit integer

`FCVTMOD.W.D` converts $x=\mathrm{val}_D(a)$ to a signed 32-bit integer with the fixed RTZ rounding of its encoding: $\mathrm{trunc}(x)$ is taken as an unbounded two's-complement result, its low 32 bits are written sign-extended to `XLEN` bits, and NaN and $\pm\infty$ produce zero (Unpriv. §26.4, `sources/riscv-unprivileged.txt:8625-8635`). The flags are those of `FCVT.W.D` on the same input: NaN, $\pm\infty$, and finite values outside $[-2^{31},2^{31}-1]$ set `NV(4)`, while in-range inexact values set `NX(0)`. The `rm` field is fixed to `RTZ(1)` by the encoding and other values are reserved, so no rounding conjunct appears. Requires `D` and `Zfa`.

The `exception` field of every block below lists only the exceptions the instruction itself can raise, and reads `\mathrm{exception}=\varnothing` when it raises none; the instruction-fetch outcomes depend only on the fetch address and are stated once in the README, not repeated here.

**(FCVTMOD.W.D.0) Extension unavailable or effective FS Off → only IllegalInstruction(2)**

$$
\begin{aligned}
&\bigl(\bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\land(vsstatus.FS=\mathrm{Off}(0)\lor sstatus.FS=\mathrm{Off}(0))\bigr)\\
&\qquad\lor\ \neg\mathrm{impl}(\mathrm{D})\ \lor\ \neg\mathrm{impl}(\mathrm{Zfa})\ \lor\ mstatus.FS=\mathrm{Off}(0)\bigr)\\
&\land\ (\mathrm{instr}=\mathrm{FCVTMOD.W.D})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(FCVTMOD.W.D.1) No H, M/S/U: the source is not correctly NaN-boxed → 0, set NV(4)**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \neg\mathrm{boxed}_{D}(f[rs1])\\
&\land\ (\mathrm{instr}=\mathrm{FCVTMOD.W.D})\\
\end{aligned}
\longrightarrow
\{\, rd=0,\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVTMOD.W.D.2) H, M/HS/U: the source is not correctly NaN-boxed → 0, set NV(4)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \neg\mathrm{boxed}_{D}(f[rs1])\\
&\land\ (\mathrm{instr}=\mathrm{FCVTMOD.W.D})\\
\end{aligned}
\longrightarrow
\{\, rd=0,\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVTMOD.W.D.3) H, VS/VU: the source is not correctly NaN-boxed → 0, set NV(4)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ \neg\mathrm{boxed}_{D}(f[rs1])\\
&\land\ (\mathrm{instr}=\mathrm{FCVTMOD.W.D})\\
\end{aligned}
\longrightarrow
\{\, rd=0,\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVTMOD.W.D.4) No H, M/S/U: any NaN → 0, set NV(4)**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (e_a=e_{\max}\land f_a\ne0)\\
&\land\ (\mathrm{instr}=\mathrm{FCVTMOD.W.D})\\
\end{aligned}
\longrightarrow
\{\, rd=0,\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVTMOD.W.D.5) H, M/HS/U: any NaN → 0, set NV(4)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (e_a=e_{\max}\land f_a\ne0)\\
&\land\ (\mathrm{instr}=\mathrm{FCVTMOD.W.D})\\
\end{aligned}
\longrightarrow
\{\, rd=0,\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVTMOD.W.D.6) H, VS/VU: any NaN → 0, set NV(4)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (e_a=e_{\max}\land f_a\ne0)\\
&\land\ (\mathrm{instr}=\mathrm{FCVTMOD.W.D})\\
\end{aligned}
\longrightarrow
\{\, rd=0,\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVTMOD.W.D.7) No H, M/S/U: $+\infty_D$ → 0, set NV(4)**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (s_a=0\land e_a=e_{\max}\land f_a=0)\\
&\land\ (\mathrm{instr}=\mathrm{FCVTMOD.W.D})\\
\end{aligned}
\longrightarrow
\{\, rd=0,\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVTMOD.W.D.8) H, M/HS/U: $+\infty_D$ → 0, set NV(4)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (s_a=0\land e_a=e_{\max}\land f_a=0)\\
&\land\ (\mathrm{instr}=\mathrm{FCVTMOD.W.D})\\
\end{aligned}
\longrightarrow
\{\, rd=0,\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVTMOD.W.D.9) H, VS/VU: $+\infty_D$ → 0, set NV(4)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (s_a=0\land e_a=e_{\max}\land f_a=0)\\
&\land\ (\mathrm{instr}=\mathrm{FCVTMOD.W.D})\\
\end{aligned}
\longrightarrow
\{\, rd=0,\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVTMOD.W.D.10) No H, M/S/U: $-\infty_D$ → 0, set NV(4)**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (s_a=1\land e_a=e_{\max}\land f_a=0)\\
&\land\ (\mathrm{instr}=\mathrm{FCVTMOD.W.D})\\
\end{aligned}
\longrightarrow
\{\, rd=0,\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVTMOD.W.D.11) H, M/HS/U: $-\infty_D$ → 0, set NV(4)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (s_a=1\land e_a=e_{\max}\land f_a=0)\\
&\land\ (\mathrm{instr}=\mathrm{FCVTMOD.W.D})\\
\end{aligned}
\longrightarrow
\{\, rd=0,\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVTMOD.W.D.12) H, VS/VU: $-\infty_D$ → 0, set NV(4)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (s_a=1\land e_a=e_{\max}\land f_a=0)\\
&\land\ (\mathrm{instr}=\mathrm{FCVTMOD.W.D})\\
\end{aligned}
\longrightarrow
\{\, rd=0,\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVTMOD.W.D.13) No H, M/S/U: finite, outside the signed 32-bit range → wrapped, set NV(4)**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (e_a\ne e_{\max})\\
&\land\ \big(\mathrm{trunc}(x)<-2^{31}\lor\mathrm{trunc}(x)>2^{31}-1\big)\\
&\land\ (\mathrm{instr}=\mathrm{FCVTMOD.W.D})\\
\end{aligned}
\longrightarrow
\{\, rd=\mathrm{sext}_{\mathrm{XLEN}}(\mathrm{low32}(\mathrm{trunc}(x))),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVTMOD.W.D.14) H, M/HS/U: finite, outside the signed 32-bit range → wrapped, set NV(4)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (e_a\ne e_{\max})\\
&\land\ \big(\mathrm{trunc}(x)<-2^{31}\lor\mathrm{trunc}(x)>2^{31}-1\big)\\
&\land\ (\mathrm{instr}=\mathrm{FCVTMOD.W.D})\\
\end{aligned}
\longrightarrow
\{\, rd=\mathrm{sext}_{\mathrm{XLEN}}(\mathrm{low32}(\mathrm{trunc}(x))),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVTMOD.W.D.15) H, VS/VU: finite, outside the signed 32-bit range → wrapped, set NV(4)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (e_a\ne e_{\max})\\
&\land\ \big(\mathrm{trunc}(x)<-2^{31}\lor\mathrm{trunc}(x)>2^{31}-1\big)\\
&\land\ (\mathrm{instr}=\mathrm{FCVTMOD.W.D})\\
\end{aligned}
\longrightarrow
\{\, rd=\mathrm{sext}_{\mathrm{XLEN}}(\mathrm{low32}(\mathrm{trunc}(x))),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NV}(4)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVTMOD.W.D.16) No H, M/S/U: in range, inexact → wrapped value, set NX(0)**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (e_a\ne e_{\max})\\
&\land\ \big(-2^{31}\le\mathrm{trunc}(x)\le2^{31}-1\big)\\
&\land\ (\mathrm{trunc}(x)\ne x)\\
&\land\ (\mathrm{instr}=\mathrm{FCVTMOD.W.D})\\
\end{aligned}
\longrightarrow
\{\, rd=\mathrm{sext}_{\mathrm{XLEN}}(\mathrm{low32}(\mathrm{trunc}(x))),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVTMOD.W.D.17) H, M/HS/U: in range, inexact → wrapped value, set NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (e_a\ne e_{\max})\\
&\land\ \big(-2^{31}\le\mathrm{trunc}(x)\le2^{31}-1\big)\\
&\land\ (\mathrm{trunc}(x)\ne x)\\
&\land\ (\mathrm{instr}=\mathrm{FCVTMOD.W.D})\\
\end{aligned}
\longrightarrow
\{\, rd=\mathrm{sext}_{\mathrm{XLEN}}(\mathrm{low32}(\mathrm{trunc}(x))),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVTMOD.W.D.18) H, VS/VU: in range, inexact → wrapped value, set NX(0)**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (e_a\ne e_{\max})\\
&\land\ \big(-2^{31}\le\mathrm{trunc}(x)\le2^{31}-1\big)\\
&\land\ (\mathrm{trunc}(x)\ne x)\\
&\land\ (\mathrm{instr}=\mathrm{FCVTMOD.W.D})\\
\end{aligned}
\longrightarrow
\{\, rd=\mathrm{sext}_{\mathrm{XLEN}}(\mathrm{low32}(\mathrm{trunc}(x))),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\{\mathrm{NX}(0)\},\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVTMOD.W.D.19) No H, M/S/U: in range, exact → wrapped value**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (e_a\ne e_{\max})\\
&\land\ \big(-2^{31}\le\mathrm{trunc}(x)\le2^{31}-1\big)\\
&\land\ (\mathrm{trunc}(x)=x)\\
&\land\ (\mathrm{instr}=\mathrm{FCVTMOD.W.D})\\
\end{aligned}
\longrightarrow
\{\, rd=\mathrm{sext}_{\mathrm{XLEN}}(\mathrm{low32}(\mathrm{trunc}(x))),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVTMOD.W.D.20) H, M/HS/U: in range, exact → wrapped value**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (e_a\ne e_{\max})\\
&\land\ \big(-2^{31}\le\mathrm{trunc}(x)\le2^{31}-1\big)\\
&\land\ (\mathrm{trunc}(x)=x)\\
&\land\ (\mathrm{instr}=\mathrm{FCVTMOD.W.D})\\
\end{aligned}
\longrightarrow
\{\, rd=\mathrm{sext}_{\mathrm{XLEN}}(\mathrm{low32}(\mathrm{trunc}(x))),\ \mathrm{exception}=\varnothing \,\}
$$

**(FCVTMOD.W.D.21) H, VS/VU: in range, exact → wrapped value**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ \mathrm{impl}(\mathrm{Zfa})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (e_a\ne e_{\max})\\
&\land\ \big(-2^{31}\le\mathrm{trunc}(x)\le2^{31}-1\big)\\
&\land\ (\mathrm{trunc}(x)=x)\\
&\land\ (\mathrm{instr}=\mathrm{FCVTMOD.W.D})\\
\end{aligned}
\longrightarrow
\{\, rd=\mathrm{sext}_{\mathrm{XLEN}}(\mathrm{low32}(\mathrm{trunc}(x))),\ \mathrm{exception}=\varnothing \,\}
$$
