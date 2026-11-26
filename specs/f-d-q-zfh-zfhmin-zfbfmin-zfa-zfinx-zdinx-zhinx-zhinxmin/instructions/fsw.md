# FSW — store, format S

`FSW` stores the low 32 bits of `fs2` to memory at $\mathrm{EA}=(x[\mathrm{rs1}]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}}$. A store reads `fs2` but does not write floating-point state, so it leaves `mstatus.FS` unchanged. Requires `F`.

The `exception` field of every block below lists only the exceptions the instruction itself can raise, and reads `\mathrm{exception}=\varnothing` when it raises none; the instruction-fetch outcomes depend only on the fetch address and are stated once in the README, not repeated here.

**(FSW.0) Extension unavailable or effective FS Off → only IllegalInstruction(2)**

$$
\begin{aligned}
&\bigl(\bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\land(vsstatus.FS=\mathrm{Off}(0)\lor sstatus.FS=\mathrm{Off}(0))\bigr)\\
&\qquad\lor\ \neg\mathrm{impl}(\mathrm{F})\ \lor\ mstatus.FS=\mathrm{Off}(0)\bigr)\\
&\land\ (\mathrm{instr}=\mathrm{FSW})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(FSW.1) No H, M/S/U: data breakpoint**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{Breakpoint}(\mathrm{EA})\\
&\land\ (\mathrm{instr}=\mathrm{FSW})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{Breakpoint}(3,\mathrm{data})\} \,\}
$$

**(FSW.2) H, M/HS/U: data breakpoint**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{Breakpoint}(\mathrm{EA})\\
&\land\ (\mathrm{instr}=\mathrm{FSW})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{Breakpoint}(3,\mathrm{data})\} \,\}
$$

**(FSW.3) H, VS/VU: data breakpoint**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{Breakpoint}(\mathrm{EA})\\
&\land\ (\mathrm{instr}=\mathrm{FSW})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{Breakpoint}(3,\mathrm{data})\} \,\}
$$

**(FSW.4) No H, M/S/U: misaligned, checked before address translation**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{MisalignedPre}(\mathrm{EA},32)\\
&\land\ (\mathrm{instr}=\mathrm{FSW})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOAddressMisaligned}(6)\} \,\}
$$

**(FSW.5) H, M/HS/U: misaligned, checked before address translation**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{MisalignedPre}(\mathrm{EA},32)\\
&\land\ (\mathrm{instr}=\mathrm{FSW})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOAddressMisaligned}(6)\} \,\}
$$

**(FSW.6) H, VS/VU: misaligned, checked before address translation**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{MisalignedPre}(\mathrm{EA},32)\\
&\land\ (\mathrm{instr}=\mathrm{FSW})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOAddressMisaligned}(6)\} \,\}
$$

**(FSW.7) No H, M/S/U: page fault during address translation**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{PageFault}(\mathrm{EA},\mathrm{store})\\
&\land\ (\mathrm{instr}=\mathrm{FSW})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOPageFault}(15)\} \,\}
$$

**(FSW.8) H, M/HS/U: page fault during address translation**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{PageFault}(\mathrm{EA},\mathrm{store})\\
&\land\ (\mathrm{instr}=\mathrm{FSW})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOPageFault}(15)\} \,\}
$$

**(FSW.9) H, VS/VU: page fault during address translation**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{PageFault}(\mathrm{EA},\mathrm{store})\\
&\land\ (\mathrm{instr}=\mathrm{FSW})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOPageFault}(15)\} \,\}
$$

**(FSW.10) No H, M/S/U: guest-page fault during address translation**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{GuestPageFault}(\mathrm{EA},\mathrm{store})\\
&\land\ (\mathrm{instr}=\mathrm{FSW})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOGuestPageFault}(23)\} \,\}
$$

**(FSW.11) H, M/HS/U: guest-page fault during address translation**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{GuestPageFault}(\mathrm{EA},\mathrm{store})\\
&\land\ (\mathrm{instr}=\mathrm{FSW})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOGuestPageFault}(23)\} \,\}
$$

**(FSW.12) H, VS/VU: guest-page fault during address translation**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{GuestPageFault}(\mathrm{EA},\mathrm{store})\\
&\land\ (\mathrm{instr}=\mathrm{FSW})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOGuestPageFault}(23)\} \,\}
$$

**(FSW.13) No H, M/S/U: access fault during address translation**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{AccessFaultPre}(\mathrm{EA},\mathrm{store})\\
&\land\ (\mathrm{instr}=\mathrm{FSW})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOAccessFault}(7)\} \,\}
$$

**(FSW.14) H, M/HS/U: access fault during address translation**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{AccessFaultPre}(\mathrm{EA},\mathrm{store})\\
&\land\ (\mathrm{instr}=\mathrm{FSW})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOAccessFault}(7)\} \,\}
$$

**(FSW.15) H, VS/VU: access fault during address translation**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{AccessFaultPre}(\mathrm{EA},\mathrm{store})\\
&\land\ (\mathrm{instr}=\mathrm{FSW})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOAccessFault}(7)\} \,\}
$$

**(FSW.16) No H, M/S/U: access fault after address translation**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{AccessFaultPost}(\mathrm{EA},\mathrm{store})\\
&\land\ (\mathrm{instr}=\mathrm{FSW})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOAccessFault}(7)\} \,\}
$$

**(FSW.17) H, M/HS/U: access fault after address translation**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{AccessFaultPost}(\mathrm{EA},\mathrm{store})\\
&\land\ (\mathrm{instr}=\mathrm{FSW})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOAccessFault}(7)\} \,\}
$$

**(FSW.18) H, VS/VU: access fault after address translation**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{AccessFaultPost}(\mathrm{EA},\mathrm{store})\\
&\land\ (\mathrm{instr}=\mathrm{FSW})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOAccessFault}(7)\} \,\}
$$

**(FSW.19) No H, M/S/U: misaligned, checked after address translation**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{MisalignedPost}(\mathrm{EA},32)\\
&\land\ (\mathrm{instr}=\mathrm{FSW})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOAddressMisaligned}(6)\} \,\}
$$

**(FSW.20) H, M/HS/U: misaligned, checked after address translation**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{MisalignedPost}(\mathrm{EA},32)\\
&\land\ (\mathrm{instr}=\mathrm{FSW})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOAddressMisaligned}(6)\} \,\}
$$

**(FSW.21) H, VS/VU: misaligned, checked after address translation**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{MisalignedPost}(\mathrm{EA},32)\\
&\land\ (\mathrm{instr}=\mathrm{FSW})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOAddressMisaligned}(6)\} \,\}
$$

**(FSW.22) No H, M/S/U: otherwise → store**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{MemOK}_{\mathrm{store}}(\mathrm{EA},32)\\
&\land\ (\mathrm{instr}=\mathrm{FSW})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{mem}[\mathrm{EA},32]=f[rs2][31:0],\ \mathrm{exception}=\varnothing \,\}
$$

**(FSW.23) H, M/HS/U: otherwise → store**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{MemOK}_{\mathrm{store}}(\mathrm{EA},32)\\
&\land\ (\mathrm{instr}=\mathrm{FSW})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{mem}[\mathrm{EA},32]=f[rs2][31:0],\ \mathrm{exception}=\varnothing \,\}
$$

**(FSW.24) H, VS/VU: otherwise → store**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \big(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\big)\\
&\land\ \mathrm{impl}(\mathrm{F})\\
&\land\ (mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\})\\
&\land\ (\mathrm{EA}=(x[rs1]+\mathrm{sext}_{12}(\mathrm{imm}))\bmod 2^{\mathrm{XLEN}})\\
&\land\ \mathrm{MemOK}_{\mathrm{store}}(\mathrm{EA},32)\\
&\land\ (\mathrm{instr}=\mathrm{FSW})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{mem}[\mathrm{EA},32]=f[rs2][31:0],\ \mathrm{exception}=\varnothing \,\}
$$
