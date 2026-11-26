# FSD — store, format D

`FSD` stores the low 64 bits of `fs2` to memory at $\mathrm{EA}=(x[\mathrm{rs1}]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}}$. A store reads `fs2` but does not write floating-point state, so it leaves `mstatus.FS` unchanged. Requires `D`.

The `exception` field of every block below lists only the exceptions the instruction itself can raise, and reads `\mathrm{exception}=\varnothing` when it raises none; the instruction-fetch outcomes depend only on the fetch address and are stated once in the README, not repeated here.

**(FSD.0) Extension unavailable or effective FS Off → only IllegalInstruction(2)**

$$
\begin{aligned}
&\bigl(\bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\land(vsstatus.FS=\mathrm{Off}(0)\lor sstatus.FS=\mathrm{Off}(0))\bigr)\\
&\qquad\lor\ \neg\mathrm{impl}(\mathrm{D})\ \lor\ mstatus.FS=\mathrm{Off}(0)\bigr)\\
&\land\ (\mathrm{instr}=\mathrm{FSD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(FSD.1) No H, M/S/U: data breakpoint**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{Breakpoint}(\mathrm{EA})\\
&\land\ (\mathrm{instr}=\mathrm{FSD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{Breakpoint}(3,\mathrm{data})\} \,\}
$$

**(FSD.2) H, M/HS/U: data breakpoint**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{Breakpoint}(\mathrm{EA})\\
&\land\ (\mathrm{instr}=\mathrm{FSD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{Breakpoint}(3,\mathrm{data})\} \,\}
$$

**(FSD.3) H, VS/VU: data breakpoint**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{Breakpoint}(\mathrm{EA})\\
&\land\ (\mathrm{instr}=\mathrm{FSD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{Breakpoint}(3,\mathrm{data})\} \,\}
$$

**(FSD.4) No H, M/S/U: misaligned, checked before address translation**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{MisalignedPre}(\mathrm{EA},64)\\
&\land\ (\mathrm{instr}=\mathrm{FSD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOAddressMisaligned}(6)\} \,\}
$$

**(FSD.5) H, M/HS/U: misaligned, checked before address translation**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{MisalignedPre}(\mathrm{EA},64)\\
&\land\ (\mathrm{instr}=\mathrm{FSD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOAddressMisaligned}(6)\} \,\}
$$

**(FSD.6) H, VS/VU: misaligned, checked before address translation**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{MisalignedPre}(\mathrm{EA},64)\\
&\land\ (\mathrm{instr}=\mathrm{FSD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOAddressMisaligned}(6)\} \,\}
$$

**(FSD.7) No H, M/S/U: page fault during address translation**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{PageFault}(\mathrm{EA},\mathrm{store})\\
&\land\ (\mathrm{instr}=\mathrm{FSD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOPageFault}(15)\} \,\}
$$

**(FSD.8) H, M/HS/U: page fault during address translation**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{PageFault}(\mathrm{EA},\mathrm{store})\\
&\land\ (\mathrm{instr}=\mathrm{FSD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOPageFault}(15)\} \,\}
$$

**(FSD.9) H, VS/VU: page fault during address translation**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{PageFault}(\mathrm{EA},\mathrm{store})\\
&\land\ (\mathrm{instr}=\mathrm{FSD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOPageFault}(15)\} \,\}
$$

**(FSD.10) No H, M/S/U: guest-page fault during address translation**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{GuestPageFault}(\mathrm{EA},\mathrm{store})\\
&\land\ (\mathrm{instr}=\mathrm{FSD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOGuestPageFault}(23)\} \,\}
$$

**(FSD.11) H, M/HS/U: guest-page fault during address translation**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{GuestPageFault}(\mathrm{EA},\mathrm{store})\\
&\land\ (\mathrm{instr}=\mathrm{FSD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOGuestPageFault}(23)\} \,\}
$$

**(FSD.12) H, VS/VU: guest-page fault during address translation**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{GuestPageFault}(\mathrm{EA},\mathrm{store})\\
&\land\ (\mathrm{instr}=\mathrm{FSD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOGuestPageFault}(23)\} \,\}
$$

**(FSD.13) No H, M/S/U: access fault during address translation**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{AccessFaultPre}(\mathrm{EA},\mathrm{store})\\
&\land\ (\mathrm{instr}=\mathrm{FSD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOAccessFault}(7)\} \,\}
$$

**(FSD.14) H, M/HS/U: access fault during address translation**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{AccessFaultPre}(\mathrm{EA},\mathrm{store})\\
&\land\ (\mathrm{instr}=\mathrm{FSD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOAccessFault}(7)\} \,\}
$$

**(FSD.15) H, VS/VU: access fault during address translation**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{AccessFaultPre}(\mathrm{EA},\mathrm{store})\\
&\land\ (\mathrm{instr}=\mathrm{FSD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOAccessFault}(7)\} \,\}
$$

**(FSD.16) No H, M/S/U: access fault after address translation**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{AccessFaultPost}(\mathrm{EA},\mathrm{store})\\
&\land\ (\mathrm{instr}=\mathrm{FSD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOAccessFault}(7)\} \,\}
$$

**(FSD.17) H, M/HS/U: access fault after address translation**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{AccessFaultPost}(\mathrm{EA},\mathrm{store})\\
&\land\ (\mathrm{instr}=\mathrm{FSD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOAccessFault}(7)\} \,\}
$$

**(FSD.18) H, VS/VU: access fault after address translation**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{AccessFaultPost}(\mathrm{EA},\mathrm{store})\\
&\land\ (\mathrm{instr}=\mathrm{FSD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOAccessFault}(7)\} \,\}
$$

**(FSD.19) No H, M/S/U: misaligned, checked after address translation**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{MisalignedPost}(\mathrm{EA},64)\\
&\land\ (\mathrm{instr}=\mathrm{FSD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOAddressMisaligned}(6)\} \,\}
$$

**(FSD.20) H, M/HS/U: misaligned, checked after address translation**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{MisalignedPost}(\mathrm{EA},64)\\
&\land\ (\mathrm{instr}=\mathrm{FSD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOAddressMisaligned}(6)\} \,\}
$$

**(FSD.21) H, VS/VU: misaligned, checked after address translation**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{MisalignedPost}(\mathrm{EA},64)\\
&\land\ (\mathrm{instr}=\mathrm{FSD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOAddressMisaligned}(6)\} \,\}
$$

**(FSD.22) No H, M/S/U: otherwise → store**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{MemOK}_{\mathrm{store}}(\mathrm{EA},64)\\
&\land\ (\mathrm{instr}=\mathrm{FSD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{mem}[\mathrm{EA},64]=f[rs2][63:0],\ \mathrm{exception}=\varnothing \,\}
$$

**(FSD.23) H, M/HS/U: otherwise → store**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{MemOK}_{\mathrm{store}}(\mathrm{EA},64)\\
&\land\ (\mathrm{instr}=\mathrm{FSD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{mem}[\mathrm{EA},64]=f[rs2][63:0],\ \mathrm{exception}=\varnothing \,\}
$$

**(FSD.24) H, VS/VU: otherwise → store**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{D})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{MemOK}_{\mathrm{store}}(\mathrm{EA},64)\\
&\land\ (\mathrm{instr}=\mathrm{FSD})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{mem}[\mathrm{EA},64]=f[rs2][63:0],\ \mathrm{exception}=\varnothing \,\}
$$
