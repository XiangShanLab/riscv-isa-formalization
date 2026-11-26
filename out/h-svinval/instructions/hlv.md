# HLV — hypervisor virtual-machine load

`HLV.T` loads a $w(T)$-bit little-endian word from memory at $\mathrm{EA}=\mathrm{x}[rs1]$ and
writes its $\mathrm{ext}_T$ image to `rd`. The memory access is performed with two-stage
translation at the effective privilege mode selected by `hstatus.SPVP`, independent of
`mstatus.MPRV`. The eleven formulas are tried in order and the last is the remaining case; the
address predicates are defined in §5.3 of the [index](../README.md). Requires `H`.

`T` ranges over `B`, `BU`, `H`, `HU`, `W`, `WU`, and `D`; `WU` and `D` are defined only when
`XLEN=64`. The width and extension are given by §4.2 of the index.

The `exception` field of every block below lists only the exceptions the instruction itself can raise, and reads `\mathrm{exception}=\varnothing` when it raises none; the instruction-fetch outcomes depend only on the fetch address and are stated once in the README, not repeated here.

**(HLV.0) Extension unavailable → only IllegalInstruction(2)**

$$
\begin{aligned}
&\neg\mathrm{impl}(\mathrm{H})\\
&\land\ \big(T\in\{\mathrm{B},\mathrm{BU},\mathrm{H},\mathrm{HU},\mathrm{W}\}\ \lor\ \mathrm{XLEN}=64\big)\\
&\land\ (\mathrm{instr}=\mathrm{HLV}.T)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(HLV.1) Executed with $V=1$ → only VirtualInstruction(22)**

$$
\begin{aligned}
&(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\})\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ \big(T\in\{\mathrm{B},\mathrm{BU},\mathrm{H},\mathrm{HU},\mathrm{W}\}\ \lor\ \mathrm{XLEN}=64\big)\\
&\land\ (\mathrm{instr}=\mathrm{HLV}.T)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{VirtualInstruction}(22)\} \,\}
$$

**(HLV.2) U-mode with `hstatus.HU=0` → only IllegalInstruction(2)**

$$
\begin{aligned}
&(\mathrm{Priv}=\mathrm{U}\land hstatus.HU=0)\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ \big(T\in\{\mathrm{B},\mathrm{BU},\mathrm{H},\mathrm{HU},\mathrm{W}\}\ \lor\ \mathrm{XLEN}=64\big)\\
&\land\ (\mathrm{instr}=\mathrm{HLV}.T)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(HLV.3) data breakpoint at the effective address → only Breakpoint(3, data)**

$$
\begin{aligned}
&\big(\mathrm{Priv}\in\{\mathrm{M},\mathrm{HS}\}\ \lor\ (\mathrm{Priv}=\mathrm{U}\land hstatus.HU=1)\big)\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ (\mathrm{EA}=x[rs1])\\
&\land\ \mathrm{Breakpoint}(\mathrm{EA})\\
&\land\ \big(T\in\{\mathrm{B},\mathrm{BU},\mathrm{H},\mathrm{HU},\mathrm{W}\}\ \lor\ \mathrm{XLEN}=64\big)\\
&\land\ (\mathrm{instr}=\mathrm{HLV}.T)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{Breakpoint}(3,\mathrm{data})\} \,\}
$$

**(HLV.4) misaligned, checked before address translation → only LoadAddressMisaligned(4)**

$$
\begin{aligned}
&\big(\mathrm{Priv}\in\{\mathrm{M},\mathrm{HS}\}\ \lor\ (\mathrm{Priv}=\mathrm{U}\land hstatus.HU=1)\big)\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ (\mathrm{EA}=x[rs1])\\
&\land\ \mathrm{MisalignedPre}(\mathrm{EA},\mathrm{w}(T))\\
&\land\ \big(T\in\{\mathrm{B},\mathrm{BU},\mathrm{H},\mathrm{HU},\mathrm{W}\}\ \lor\ \mathrm{XLEN}=64\big)\\
&\land\ (\mathrm{instr}=\mathrm{HLV}.T)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{LoadAddressMisaligned}(4)\} \,\}
$$

**(HLV.5) VS-stage page fault during address translation → only LoadPageFault(13)**

$$
\begin{aligned}
&\big(\mathrm{Priv}\in\{\mathrm{M},\mathrm{HS}\}\ \lor\ (\mathrm{Priv}=\mathrm{U}\land hstatus.HU=1)\big)\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ (\mathrm{EA}=x[rs1])\\
&\land\ \mathrm{PageFault}(\mathrm{EA},\mathrm{load})\\
&\land\ \big(T\in\{\mathrm{B},\mathrm{BU},\mathrm{H},\mathrm{HU},\mathrm{W}\}\ \lor\ \mathrm{XLEN}=64\big)\\
&\land\ (\mathrm{instr}=\mathrm{HLV}.T)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{LoadPageFault}(13)\} \,\}
$$

**(HLV.6) G-stage guest-page fault during address translation → only LoadGuestPageFault(21)**

$$
\begin{aligned}
&\big(\mathrm{Priv}\in\{\mathrm{M},\mathrm{HS}\}\ \lor\ (\mathrm{Priv}=\mathrm{U}\land hstatus.HU=1)\big)\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ (\mathrm{EA}=x[rs1])\\
&\land\ \mathrm{GuestPageFault}(\mathrm{EA},\mathrm{load})\\
&\land\ \big(T\in\{\mathrm{B},\mathrm{BU},\mathrm{H},\mathrm{HU},\mathrm{W}\}\ \lor\ \mathrm{XLEN}=64\big)\\
&\land\ (\mathrm{instr}=\mathrm{HLV}.T)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{LoadGuestPageFault}(21)\} \,\}
$$

**(HLV.7) access fault during address translation → only LoadAccessFault(5)**

$$
\begin{aligned}
&\big(\mathrm{Priv}\in\{\mathrm{M},\mathrm{HS}\}\ \lor\ (\mathrm{Priv}=\mathrm{U}\land hstatus.HU=1)\big)\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ (\mathrm{EA}=x[rs1])\\
&\land\ \mathrm{AccessFaultPre}(\mathrm{EA},\mathrm{load})\\
&\land\ \big(T\in\{\mathrm{B},\mathrm{BU},\mathrm{H},\mathrm{HU},\mathrm{W}\}\ \lor\ \mathrm{XLEN}=64\big)\\
&\land\ (\mathrm{instr}=\mathrm{HLV}.T)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{LoadAccessFault}(5)\} \,\}
$$

**(HLV.8) access fault after address translation → only LoadAccessFault(5)**

$$
\begin{aligned}
&\big(\mathrm{Priv}\in\{\mathrm{M},\mathrm{HS}\}\ \lor\ (\mathrm{Priv}=\mathrm{U}\land hstatus.HU=1)\big)\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ (\mathrm{EA}=x[rs1])\\
&\land\ \mathrm{AccessFaultPost}(\mathrm{EA},\mathrm{load})\\
&\land\ \big(T\in\{\mathrm{B},\mathrm{BU},\mathrm{H},\mathrm{HU},\mathrm{W}\}\ \lor\ \mathrm{XLEN}=64\big)\\
&\land\ (\mathrm{instr}=\mathrm{HLV}.T)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{LoadAccessFault}(5)\} \,\}
$$

**(HLV.9) misaligned, checked after address translation → only LoadAddressMisaligned(4)**

$$
\begin{aligned}
&\big(\mathrm{Priv}\in\{\mathrm{M},\mathrm{HS}\}\ \lor\ (\mathrm{Priv}=\mathrm{U}\land hstatus.HU=1)\big)\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ (\mathrm{EA}=x[rs1])\\
&\land\ \mathrm{MisalignedPost}(\mathrm{EA},\mathrm{w}(T))\\
&\land\ \big(T\in\{\mathrm{B},\mathrm{BU},\mathrm{H},\mathrm{HU},\mathrm{W}\}\ \lor\ \mathrm{XLEN}=64\big)\\
&\land\ (\mathrm{instr}=\mathrm{HLV}.T)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{LoadAddressMisaligned}(4)\} \,\}
$$

**(HLV.10) otherwise → load and extend**

$$
\begin{aligned}
&\big(\mathrm{Priv}\in\{\mathrm{M},\mathrm{HS}\}\ \lor\ (\mathrm{Priv}=\mathrm{U}\land hstatus.HU=1)\big)\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ (\mathrm{EA}=x[rs1])\\
&\land\ \mathrm{MemOK}_{\mathrm{load}}(\mathrm{EA},\mathrm{w}(T))\\
&\land\ \big(T\in\{\mathrm{B},\mathrm{BU},\mathrm{H},\mathrm{HU},\mathrm{W}\}\ \lor\ \mathrm{XLEN}=64\big)\\
&\land\ (\mathrm{instr}=\mathrm{HLV}.T)\\
\end{aligned}
\longrightarrow
\{\, rd=\mathrm{ext}_T(\mathrm{mem}[\mathrm{EA},\mathrm{w}(T)]),\ \mathrm{exception}=\varnothing \,\}
$$
