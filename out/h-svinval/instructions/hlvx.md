# HLVX — hypervisor virtual-machine load for instruction fetch

`HLVX.T` loads a $w(T)$-bit little-endian word from memory at $\mathrm{EA}=\mathrm{x}[rs1]$ and
writes its zero-extended image to `rd`. It is identical to `HLV.T` for the two unsigned variants,
except that execute permission takes the place of read permission during both stages of address
translation; the supervisor physical memory attributes must still grant both execute and read
permission, and machine-level physical memory protection cannot be overridden. The instruction
raises load exceptions, not fetch exceptions, and its access is exempt from pointer masking. The
eleven formulas are tried in order and the last is the remaining case; the address predicates
are defined in §5.3 of the [index](../README.md). Requires `H`.

`T` ranges over `HU` and `WU`; both are defined on RV32 and RV64. The width and extension are
given by §4.2 of the index.

The `exception` field of every block below lists only the exceptions the instruction itself can raise, and reads `\mathrm{exception}=\varnothing` when it raises none; the instruction-fetch outcomes depend only on the fetch address and are stated once in the README, not repeated here.

**(HLVX.0) Extension unavailable → only IllegalInstruction(2)**

$$
\begin{aligned}
&\neg\mathrm{impl}(\mathrm{H})\\
&\land\ (T\in\{\mathrm{HU},\mathrm{WU}\})\\
&\land\ (\mathrm{instr}=\mathrm{HLVX}.T)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(HLVX.1) Executed with $V=1$ → only VirtualInstruction(22)**

$$
\begin{aligned}
&(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\})\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ (T\in\{\mathrm{HU},\mathrm{WU}\})\\
&\land\ (\mathrm{instr}=\mathrm{HLVX}.T)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{VirtualInstruction}(22)\} \,\}
$$

**(HLVX.2) U-mode with `hstatus.HU=0` → only IllegalInstruction(2)**

$$
\begin{aligned}
&(\mathrm{Priv}=\mathrm{U}\land hstatus.HU=0)\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ (T\in\{\mathrm{HU},\mathrm{WU}\})\\
&\land\ (\mathrm{instr}=\mathrm{HLVX}.T)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(HLVX.3) data breakpoint at the effective address → only Breakpoint(3, data)**

$$
\begin{aligned}
&\big(\mathrm{Priv}\in\{\mathrm{M},\mathrm{HS}\}\ \lor\ (\mathrm{Priv}=\mathrm{U}\land hstatus.HU=1)\big)\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ (\mathrm{EA}=x[rs1])\\
&\land\ \mathrm{Breakpoint}(\mathrm{EA})\\
&\land\ (T\in\{\mathrm{HU},\mathrm{WU}\})\\
&\land\ (\mathrm{instr}=\mathrm{HLVX}.T)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{Breakpoint}(3,\mathrm{data})\} \,\}
$$

**(HLVX.4) misaligned, checked before address translation → only LoadAddressMisaligned(4)**

$$
\begin{aligned}
&\big(\mathrm{Priv}\in\{\mathrm{M},\mathrm{HS}\}\ \lor\ (\mathrm{Priv}=\mathrm{U}\land hstatus.HU=1)\big)\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ (\mathrm{EA}=x[rs1])\\
&\land\ \mathrm{MisalignedPre}(\mathrm{EA},\mathrm{w}(T))\\
&\land\ (T\in\{\mathrm{HU},\mathrm{WU}\})\\
&\land\ (\mathrm{instr}=\mathrm{HLVX}.T)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{LoadAddressMisaligned}(4)\} \,\}
$$

**(HLVX.5) VS-stage page fault during address translation → only LoadPageFault(13)**

$$
\begin{aligned}
&\big(\mathrm{Priv}\in\{\mathrm{M},\mathrm{HS}\}\ \lor\ (\mathrm{Priv}=\mathrm{U}\land hstatus.HU=1)\big)\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ (\mathrm{EA}=x[rs1])\\
&\land\ \mathrm{PageFault}(\mathrm{EA},\mathrm{loadx})\\
&\land\ (T\in\{\mathrm{HU},\mathrm{WU}\})\\
&\land\ (\mathrm{instr}=\mathrm{HLVX}.T)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{LoadPageFault}(13)\} \,\}
$$

**(HLVX.6) G-stage guest-page fault during address translation → only LoadGuestPageFault(21)**

$$
\begin{aligned}
&\big(\mathrm{Priv}\in\{\mathrm{M},\mathrm{HS}\}\ \lor\ (\mathrm{Priv}=\mathrm{U}\land hstatus.HU=1)\big)\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ (\mathrm{EA}=x[rs1])\\
&\land\ \mathrm{GuestPageFault}(\mathrm{EA},\mathrm{loadx})\\
&\land\ (T\in\{\mathrm{HU},\mathrm{WU}\})\\
&\land\ (\mathrm{instr}=\mathrm{HLVX}.T)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{LoadGuestPageFault}(21)\} \,\}
$$

**(HLVX.7) access fault during address translation → only LoadAccessFault(5)**

$$
\begin{aligned}
&\big(\mathrm{Priv}\in\{\mathrm{M},\mathrm{HS}\}\ \lor\ (\mathrm{Priv}=\mathrm{U}\land hstatus.HU=1)\big)\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ (\mathrm{EA}=x[rs1])\\
&\land\ \mathrm{AccessFaultPre}(\mathrm{EA},\mathrm{loadx})\\
&\land\ (T\in\{\mathrm{HU},\mathrm{WU}\})\\
&\land\ (\mathrm{instr}=\mathrm{HLVX}.T)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{LoadAccessFault}(5)\} \,\}
$$

**(HLVX.8) access fault after address translation → only LoadAccessFault(5)**

$$
\begin{aligned}
&\big(\mathrm{Priv}\in\{\mathrm{M},\mathrm{HS}\}\ \lor\ (\mathrm{Priv}=\mathrm{U}\land hstatus.HU=1)\big)\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ (\mathrm{EA}=x[rs1])\\
&\land\ \mathrm{AccessFaultPost}(\mathrm{EA},\mathrm{loadx})\\
&\land\ (T\in\{\mathrm{HU},\mathrm{WU}\})\\
&\land\ (\mathrm{instr}=\mathrm{HLVX}.T)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{LoadAccessFault}(5)\} \,\}
$$

**(HLVX.9) misaligned, checked after address translation → only LoadAddressMisaligned(4)**

$$
\begin{aligned}
&\big(\mathrm{Priv}\in\{\mathrm{M},\mathrm{HS}\}\ \lor\ (\mathrm{Priv}=\mathrm{U}\land hstatus.HU=1)\big)\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ (\mathrm{EA}=x[rs1])\\
&\land\ \mathrm{MisalignedPost}(\mathrm{EA},\mathrm{w}(T))\\
&\land\ (T\in\{\mathrm{HU},\mathrm{WU}\})\\
&\land\ (\mathrm{instr}=\mathrm{HLVX}.T)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{LoadAddressMisaligned}(4)\} \,\}
$$

**(HLVX.10) otherwise → load and zero-extend**

$$
\begin{aligned}
&\big(\mathrm{Priv}\in\{\mathrm{M},\mathrm{HS}\}\ \lor\ (\mathrm{Priv}=\mathrm{U}\land hstatus.HU=1)\big)\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ (\mathrm{EA}=x[rs1])\\
&\land\ \mathrm{MemOK}_{\mathrm{loadx}}(\mathrm{EA},\mathrm{w}(T))\\
&\land\ (T\in\{\mathrm{HU},\mathrm{WU}\})\\
&\land\ (\mathrm{instr}=\mathrm{HLVX}.T)\\
\end{aligned}
\longrightarrow
\{\, rd=\mathrm{ext}_T(\mathrm{mem}[\mathrm{EA},\mathrm{w}(T)]),\ \mathrm{exception}=\varnothing \,\}
$$
