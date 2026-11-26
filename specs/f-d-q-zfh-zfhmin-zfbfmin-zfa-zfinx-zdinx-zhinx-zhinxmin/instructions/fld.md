# FLD — load, format D

`FLD` loads a 64-bit little-endian value from memory at $\mathrm{EA}=(x[\mathrm{rs1}]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}}$, boxes it as format $D$, and writes it to `fd`. The eight formulas are tried in order and the last is the remaining case; the address predicates are defined in §5.5 of the [index](../README.md). Requires `D`.

The `exception` field of every block below lists only the exceptions the instruction itself can raise, and reads `\mathrm{exception}=\varnothing` when it raises none; the instruction-fetch outcomes depend only on the fetch address and are stated once in the README, not repeated here.

**(FLD.0) Extension unavailable or effective FS Off → only IllegalInstruction(2)**

$$
\begin{aligned}
&\bigl(\bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\land(vsstatus.FS=\mathrm{Off}(0)\lor sstatus.FS=\mathrm{Off}(0))\bigr)\\
&\qquad\lor\ \neg\mathrm{impl}(\mathrm{D})\ \lor\ mstatus.FS=\mathrm{Off}(0)\bigr)\\
&\land\ (\mathrm{instr}=\mathrm{FLD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(FLD.1) No H, M/S/U: data breakpoint**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{Breakpoint}(\mathrm{EA})\\
&\land\ (\mathrm{instr}=\mathrm{FLD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{Breakpoint}(3,\mathrm{data})\} \,\}
$$

**(FLD.2) H, M/HS/U: data breakpoint**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{Breakpoint}(\mathrm{EA})\\
&\land\ (\mathrm{instr}=\mathrm{FLD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{Breakpoint}(3,\mathrm{data})\} \,\}
$$

**(FLD.3) H, VS/VU: data breakpoint**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{Breakpoint}(\mathrm{EA})\\
&\land\ (\mathrm{instr}=\mathrm{FLD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{Breakpoint}(3,\mathrm{data})\} \,\}
$$

**(FLD.4) No H, M/S/U: misaligned, checked before address translation**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{MisalignedPre}(\mathrm{EA},64)\\
&\land\ (\mathrm{instr}=\mathrm{FLD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{LoadAddressMisaligned}(4)\} \,\}
$$

**(FLD.5) H, M/HS/U: misaligned, checked before address translation**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{MisalignedPre}(\mathrm{EA},64)\\
&\land\ (\mathrm{instr}=\mathrm{FLD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{LoadAddressMisaligned}(4)\} \,\}
$$

**(FLD.6) H, VS/VU: misaligned, checked before address translation**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{MisalignedPre}(\mathrm{EA},64)\\
&\land\ (\mathrm{instr}=\mathrm{FLD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{LoadAddressMisaligned}(4)\} \,\}
$$

**(FLD.7) No H, M/S/U: page fault during address translation**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{PageFault}(\mathrm{EA},\mathrm{load})\\
&\land\ (\mathrm{instr}=\mathrm{FLD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{LoadPageFault}(13)\} \,\}
$$

**(FLD.8) H, M/HS/U: page fault during address translation**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{PageFault}(\mathrm{EA},\mathrm{load})\\
&\land\ (\mathrm{instr}=\mathrm{FLD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{LoadPageFault}(13)\} \,\}
$$

**(FLD.9) H, VS/VU: page fault during address translation**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{PageFault}(\mathrm{EA},\mathrm{load})\\
&\land\ (\mathrm{instr}=\mathrm{FLD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{LoadPageFault}(13)\} \,\}
$$

**(FLD.10) No H, M/S/U: guest-page fault during address translation**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{GuestPageFault}(\mathrm{EA},\mathrm{load})\\
&\land\ (\mathrm{instr}=\mathrm{FLD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{LoadGuestPageFault}(21)\} \,\}
$$

**(FLD.11) H, M/HS/U: guest-page fault during address translation**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{GuestPageFault}(\mathrm{EA},\mathrm{load})\\
&\land\ (\mathrm{instr}=\mathrm{FLD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{LoadGuestPageFault}(21)\} \,\}
$$

**(FLD.12) H, VS/VU: guest-page fault during address translation**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{GuestPageFault}(\mathrm{EA},\mathrm{load})\\
&\land\ (\mathrm{instr}=\mathrm{FLD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{LoadGuestPageFault}(21)\} \,\}
$$

**(FLD.13) No H, M/S/U: access fault during address translation**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{AccessFaultPre}(\mathrm{EA},\mathrm{load})\\
&\land\ (\mathrm{instr}=\mathrm{FLD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{LoadAccessFault}(5)\} \,\}
$$

**(FLD.14) H, M/HS/U: access fault during address translation**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{AccessFaultPre}(\mathrm{EA},\mathrm{load})\\
&\land\ (\mathrm{instr}=\mathrm{FLD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{LoadAccessFault}(5)\} \,\}
$$

**(FLD.15) H, VS/VU: access fault during address translation**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{AccessFaultPre}(\mathrm{EA},\mathrm{load})\\
&\land\ (\mathrm{instr}=\mathrm{FLD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{LoadAccessFault}(5)\} \,\}
$$

**(FLD.16) No H, M/S/U: access fault after address translation**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{AccessFaultPost}(\mathrm{EA},\mathrm{load})\\
&\land\ (\mathrm{instr}=\mathrm{FLD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{LoadAccessFault}(5)\} \,\}
$$

**(FLD.17) H, M/HS/U: access fault after address translation**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{AccessFaultPost}(\mathrm{EA},\mathrm{load})\\
&\land\ (\mathrm{instr}=\mathrm{FLD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{LoadAccessFault}(5)\} \,\}
$$

**(FLD.18) H, VS/VU: access fault after address translation**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{AccessFaultPost}(\mathrm{EA},\mathrm{load})\\
&\land\ (\mathrm{instr}=\mathrm{FLD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{LoadAccessFault}(5)\} \,\}
$$

**(FLD.19) No H, M/S/U: misaligned, checked after address translation**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{MisalignedPost}(\mathrm{EA},64)\\
&\land\ (\mathrm{instr}=\mathrm{FLD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{LoadAddressMisaligned}(4)\} \,\}
$$

**(FLD.20) H, M/HS/U: misaligned, checked after address translation**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{MisalignedPost}(\mathrm{EA},64)\\
&\land\ (\mathrm{instr}=\mathrm{FLD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{LoadAddressMisaligned}(4)\} \,\}
$$

**(FLD.21) H, VS/VU: misaligned, checked after address translation**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{MisalignedPost}(\mathrm{EA},64)\\
&\land\ (\mathrm{instr}=\mathrm{FLD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{LoadAddressMisaligned}(4)\} \,\}
$$

**(FLD.22) No H, M/S/U: otherwise → load and box**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{MemOK}_{\mathrm{load}}(\mathrm{EA},64)\\
&\land\ (\mathrm{instr}=\mathrm{FLD})\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_D(\mathrm{mem}[\mathrm{EA},64]),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FLD.23) H, M/HS/U: otherwise → load and box**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{MemOK}_{\mathrm{load}}(\mathrm{EA},64)\\
&\land\ (\mathrm{instr}=\mathrm{FLD})\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_D(\mathrm{mem}[\mathrm{EA},64]),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(FLD.24) H, VS/VU: otherwise → load and box**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{MemOK}_{\mathrm{load}}(\mathrm{EA},64)\\
&\land\ (\mathrm{instr}=\mathrm{FLD})\\
\end{aligned}
\longrightarrow
\{\, fd=\mathrm{box}_D(\mathrm{mem}[\mathrm{EA},64]),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$
