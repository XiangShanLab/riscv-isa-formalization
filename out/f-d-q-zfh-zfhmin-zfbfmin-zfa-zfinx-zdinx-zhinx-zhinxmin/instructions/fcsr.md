# FRCSR, FSCSR, FRRM, FSRM, FRFLAGS, FSFLAGS — `fcsr` access

These are CSR pseudo-instructions. `FRCSR` reads `fcsr`; `FSCSR` swaps it, returning the old value in `rd` and writing `rs1` into `fcsr`. `FRRM`/`FSRM` and `FRFLAGS`/`FSFLAGS` do the same for the rounding-mode field `fcsr.frm` and the accrued-flags field `fcsr.fflags`. Reads copy the field zero-extended into `rd` and do not touch floating-point state; writes modify `fcsr` and set `mstatus.FS` to `Dirty(3)`. No rounding takes place and no flag is raised. Reserved `fcsr` bits 31:8 read as zero and ignore writes. Requires `F` and `Zicsr`.

The `exception` field of every block below lists only the exceptions the instruction itself can raise, and reads `\mathrm{exception}=\varnothing` when it raises none; the instruction-fetch outcomes depend only on the fetch address and are stated once in the README, not repeated here.

**(FRCSR.0) Extension unavailable or effective FS Off → only IllegalInstruction(2)**

$$
\begin{aligned}
&\bigl(\bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\land(vsstatus.FS=\mathrm{Off}(0)\lor sstatus.FS=\mathrm{Off}(0))\bigr)\\
&\qquad\lor\ \neg\mathrm{impl}(\mathrm{F})\ \lor\ \neg\mathrm{impl}(\mathrm{Zicsr})\ \lor\ mstatus.FS=\mathrm{Off}(0)\bigr)\\
&\land\ (\mathrm{instr}=\mathrm{FRCSR})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(FRCSR.1) No H, M/S/U: read `fcsr`**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ \mathrm{impl}(\mathrm{Zicsr})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{instr}=\mathrm{FRCSR})\\
\end{aligned}
\longrightarrow
\{\, rd=\mathrm{zext}_{\mathrm{XLEN}}(fcsr),\ \mathrm{exception}=\varnothing \,\}
$$

**(FRCSR.2) H, M/HS/U: read `fcsr`**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ \mathrm{impl}(\mathrm{Zicsr})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{instr}=\mathrm{FRCSR})\\
\end{aligned}
\longrightarrow
\{\, rd=\mathrm{zext}_{\mathrm{XLEN}}(fcsr),\ \mathrm{exception}=\varnothing \,\}
$$

**(FRCSR.3) H, VS/VU: read `fcsr`**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ \mathrm{impl}(\mathrm{Zicsr})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{instr}=\mathrm{FRCSR})\\
\end{aligned}
\longrightarrow
\{\, rd=\mathrm{zext}_{\mathrm{XLEN}}(fcsr),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSCSR.0) Extension unavailable or effective FS Off → only IllegalInstruction(2)**

$$
\begin{aligned}
&\bigl(\bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\land(vsstatus.FS=\mathrm{Off}(0)\lor sstatus.FS=\mathrm{Off}(0))\bigr)\\
&\qquad\lor\ \neg\mathrm{impl}(\mathrm{F})\ \lor\ \neg\mathrm{impl}(\mathrm{Zicsr})\ \lor\ mstatus.FS=\mathrm{Off}(0)\bigr)\\
&\land\ (\mathrm{instr}=\mathrm{FSCSR})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(FSCSR.1) No H, M/S/U: read old `fcsr`, write new `fcsr`**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ \mathrm{impl}(\mathrm{Zicsr})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{instr}=\mathrm{FSCSR})\\
\end{aligned}
\longrightarrow
\{\, rd=\mathrm{zext}_{\mathrm{XLEN}}(fcsr),\ fcsr=\mathrm{zext}_{32}(x[rs1][7:0]),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSCSR.2) H, M/HS/U: read old `fcsr`, write new `fcsr`**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ \mathrm{impl}(\mathrm{Zicsr})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{instr}=\mathrm{FSCSR})\\
\end{aligned}
\longrightarrow
\{\, rd=\mathrm{zext}_{\mathrm{XLEN}}(fcsr),\ fcsr=\mathrm{zext}_{32}(x[rs1][7:0]),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSCSR.3) H, VS/VU: read old `fcsr`, write new `fcsr`**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ \mathrm{impl}(\mathrm{Zicsr})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{instr}=\mathrm{FSCSR})\\
\end{aligned}
\longrightarrow
\{\, rd=\mathrm{zext}_{\mathrm{XLEN}}(fcsr),\ fcsr=\mathrm{zext}_{32}(x[rs1][7:0]),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FRRM.0) Extension unavailable or effective FS Off → only IllegalInstruction(2)**

$$
\begin{aligned}
&\bigl(\bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\land(vsstatus.FS=\mathrm{Off}(0)\lor sstatus.FS=\mathrm{Off}(0))\bigr)\\
&\qquad\lor\ \neg\mathrm{impl}(\mathrm{F})\ \lor\ \neg\mathrm{impl}(\mathrm{Zicsr})\ \lor\ mstatus.FS=\mathrm{Off}(0)\bigr)\\
&\land\ (\mathrm{instr}=\mathrm{FRRM})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(FRRM.1) No H, M/S/U: read `fcsr.frm`**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ \mathrm{impl}(\mathrm{Zicsr})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{instr}=\mathrm{FRRM})\\
\end{aligned}
\longrightarrow
\{\, rd=\mathrm{zext}_{\mathrm{XLEN}}(fcsr.frm),\ \mathrm{exception}=\varnothing \,\}
$$

**(FRRM.2) H, M/HS/U: read `fcsr.frm`**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ \mathrm{impl}(\mathrm{Zicsr})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{instr}=\mathrm{FRRM})\\
\end{aligned}
\longrightarrow
\{\, rd=\mathrm{zext}_{\mathrm{XLEN}}(fcsr.frm),\ \mathrm{exception}=\varnothing \,\}
$$

**(FRRM.3) H, VS/VU: read `fcsr.frm`**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ \mathrm{impl}(\mathrm{Zicsr})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{instr}=\mathrm{FRRM})\\
\end{aligned}
\longrightarrow
\{\, rd=\mathrm{zext}_{\mathrm{XLEN}}(fcsr.frm),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSRM.0) Extension unavailable or effective FS Off → only IllegalInstruction(2)**

$$
\begin{aligned}
&\bigl(\bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\land(vsstatus.FS=\mathrm{Off}(0)\lor sstatus.FS=\mathrm{Off}(0))\bigr)\\
&\qquad\lor\ \neg\mathrm{impl}(\mathrm{F})\ \lor\ \neg\mathrm{impl}(\mathrm{Zicsr})\ \lor\ mstatus.FS=\mathrm{Off}(0)\bigr)\\
&\land\ (\mathrm{instr}=\mathrm{FSRM})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(FSRM.1) No H, M/S/U: read old `fcsr.frm`, write new `fcsr.frm`**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ \mathrm{impl}(\mathrm{Zicsr})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{instr}=\mathrm{FSRM})\\
\end{aligned}
\longrightarrow
\{\, rd=\mathrm{zext}_{\mathrm{XLEN}}(fcsr.frm),\ fcsr.frm=x[rs1][2:0],\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSRM.2) H, M/HS/U: read old `fcsr.frm`, write new `fcsr.frm`**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ \mathrm{impl}(\mathrm{Zicsr})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{instr}=\mathrm{FSRM})\\
\end{aligned}
\longrightarrow
\{\, rd=\mathrm{zext}_{\mathrm{XLEN}}(fcsr.frm),\ fcsr.frm=x[rs1][2:0],\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSRM.3) H, VS/VU: read old `fcsr.frm`, write new `fcsr.frm`**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ \mathrm{impl}(\mathrm{Zicsr})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{instr}=\mathrm{FSRM})\\
\end{aligned}
\longrightarrow
\{\, rd=\mathrm{zext}_{\mathrm{XLEN}}(fcsr.frm),\ fcsr.frm=x[rs1][2:0],\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FRFLAGS.0) Extension unavailable or effective FS Off → only IllegalInstruction(2)**

$$
\begin{aligned}
&\bigl(\bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\land(vsstatus.FS=\mathrm{Off}(0)\lor sstatus.FS=\mathrm{Off}(0))\bigr)\\
&\qquad\lor\ \neg\mathrm{impl}(\mathrm{F})\ \lor\ \neg\mathrm{impl}(\mathrm{Zicsr})\ \lor\ mstatus.FS=\mathrm{Off}(0)\bigr)\\
&\land\ (\mathrm{instr}=\mathrm{FRFLAGS})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(FRFLAGS.1) No H, M/S/U: read `fcsr.fflags`**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ \mathrm{impl}(\mathrm{Zicsr})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{instr}=\mathrm{FRFLAGS})\\
\end{aligned}
\longrightarrow
\{\, rd=\mathrm{zext}_{\mathrm{XLEN}}(fcsr.fflags),\ \mathrm{exception}=\varnothing \,\}
$$

**(FRFLAGS.2) H, M/HS/U: read `fcsr.fflags`**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ \mathrm{impl}(\mathrm{Zicsr})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{instr}=\mathrm{FRFLAGS})\\
\end{aligned}
\longrightarrow
\{\, rd=\mathrm{zext}_{\mathrm{XLEN}}(fcsr.fflags),\ \mathrm{exception}=\varnothing \,\}
$$

**(FRFLAGS.3) H, VS/VU: read `fcsr.fflags`**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ \mathrm{impl}(\mathrm{Zicsr})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{instr}=\mathrm{FRFLAGS})\\
\end{aligned}
\longrightarrow
\{\, rd=\mathrm{zext}_{\mathrm{XLEN}}(fcsr.fflags),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSFLAGS.0) Extension unavailable or effective FS Off → only IllegalInstruction(2)**

$$
\begin{aligned}
&\bigl(\bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\land(vsstatus.FS=\mathrm{Off}(0)\lor sstatus.FS=\mathrm{Off}(0))\bigr)\\
&\qquad\lor\ \neg\mathrm{impl}(\mathrm{F})\ \lor\ \neg\mathrm{impl}(\mathrm{Zicsr})\ \lor\ mstatus.FS=\mathrm{Off}(0)\bigr)\\
&\land\ (\mathrm{instr}=\mathrm{FSFLAGS})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(FSFLAGS.1) No H, M/S/U: read old `fcsr.fflags`, write new `fcsr.fflags`**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ \mathrm{impl}(\mathrm{Zicsr})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{instr}=\mathrm{FSFLAGS})\\
\end{aligned}
\longrightarrow
\{\, rd=\mathrm{zext}_{\mathrm{XLEN}}(fcsr.fflags),\ fcsr.fflags=x[rs1][4:0],\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSFLAGS.2) H, M/HS/U: read old `fcsr.fflags`, write new `fcsr.fflags`**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ \mathrm{impl}(\mathrm{Zicsr})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{instr}=\mathrm{FSFLAGS})\\
\end{aligned}
\longrightarrow
\{\, rd=\mathrm{zext}_{\mathrm{XLEN}}(fcsr.fflags),\ fcsr.fflags=x[rs1][4:0],\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FSFLAGS.3) H, VS/VU: read old `fcsr.fflags`, write new `fcsr.fflags`**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ \mathrm{impl}(\mathrm{Zicsr})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{instr}=\mathrm{FSFLAGS})\\
\end{aligned}
\longrightarrow
\{\, rd=\mathrm{zext}_{\mathrm{XLEN}}(fcsr.fflags),\ fcsr.fflags=x[rs1][4:0],\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$
