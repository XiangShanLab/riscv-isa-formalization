# HSV — hypervisor virtual-machine store

`HSV.T` stores the low $w(T)$ bits of `x[rs2]` to memory at $\mathrm{EA}=\mathrm{x}[rs1]$. The
memory access is performed with two-stage translation at the effective privilege mode selected by
`hstatus.SPVP`, independent of `mstatus.MPRV`. A store reads `rs2` but writes no register. The
eleven formulas are tried in order and the last is the remaining case; the address predicates
are defined in §5.3 of the [index](../README.md). Requires `H`.

`T` ranges over `B`, `H`, `W`, and `D`; `D` is defined only when `XLEN=64`. The width is given
by §4.2 of the index.

The `exception` field of every block below lists only the exceptions the instruction itself can raise, and reads `\mathrm{exception}=\varnothing` when it raises none; the instruction-fetch outcomes depend only on the fetch address and are stated once in the README, not repeated here.

**(HSV.0) Extension unavailable → only IllegalInstruction(2)**

$$
\begin{aligned}
&\neg\mathrm{impl}(\mathrm{H})\\
&\land\ \big(T\in\{\mathrm{B},\mathrm{H},\mathrm{W}\}\ \lor\ \mathrm{XLEN}=64\big)\\
&\land\ (\mathrm{instr}=\mathrm{HSV}.T)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(HSV.1) Executed with $V=1$ → only VirtualInstruction(22)**

$$
\begin{aligned}
&(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\})\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ \big(T\in\{\mathrm{B},\mathrm{H},\mathrm{W}\}\ \lor\ \mathrm{XLEN}=64\big)\\
&\land\ (\mathrm{instr}=\mathrm{HSV}.T)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{VirtualInstruction}(22)\} \,\}
$$

**(HSV.2) U-mode with `hstatus.HU=0` → only IllegalInstruction(2)**

$$
\begin{aligned}
&(\mathrm{Priv}=\mathrm{U}\land hstatus.HU=0)\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ \big(T\in\{\mathrm{B},\mathrm{H},\mathrm{W}\}\ \lor\ \mathrm{XLEN}=64\big)\\
&\land\ (\mathrm{instr}=\mathrm{HSV}.T)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(HSV.3) data breakpoint at the effective address → only Breakpoint(3, data)**

$$
\begin{aligned}
&\big(\mathrm{Priv}\in\{\mathrm{M},\mathrm{HS}\}\ \lor\ (\mathrm{Priv}=\mathrm{U}\land hstatus.HU=1)\big)\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ (\mathrm{EA}=x[rs1])\\
&\land\ \mathrm{Breakpoint}(\mathrm{EA})\\
&\land\ \big(T\in\{\mathrm{B},\mathrm{H},\mathrm{W}\}\ \lor\ \mathrm{XLEN}=64\big)\\
&\land\ (\mathrm{instr}=\mathrm{HSV}.T)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{Breakpoint}(3,\mathrm{data})\} \,\}
$$

**(HSV.4) misaligned, checked before address translation → only StoreAMOAddressMisaligned(6)**

$$
\begin{aligned}
&\big(\mathrm{Priv}\in\{\mathrm{M},\mathrm{HS}\}\ \lor\ (\mathrm{Priv}=\mathrm{U}\land hstatus.HU=1)\big)\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ (\mathrm{EA}=x[rs1])\\
&\land\ \mathrm{MisalignedPre}(\mathrm{EA},\mathrm{w}(T))\\
&\land\ \big(T\in\{\mathrm{B},\mathrm{H},\mathrm{W}\}\ \lor\ \mathrm{XLEN}=64\big)\\
&\land\ (\mathrm{instr}=\mathrm{HSV}.T)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOAddressMisaligned}(6)\} \,\}
$$

**(HSV.5) VS-stage page fault during address translation → only StoreAMOPageFault(15)**

$$
\begin{aligned}
&\big(\mathrm{Priv}\in\{\mathrm{M},\mathrm{HS}\}\ \lor\ (\mathrm{Priv}=\mathrm{U}\land hstatus.HU=1)\big)\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ (\mathrm{EA}=x[rs1])\\
&\land\ \mathrm{PageFault}(\mathrm{EA},\mathrm{store})\\
&\land\ \big(T\in\{\mathrm{B},\mathrm{H},\mathrm{W}\}\ \lor\ \mathrm{XLEN}=64\big)\\
&\land\ (\mathrm{instr}=\mathrm{HSV}.T)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOPageFault}(15)\} \,\}
$$

**(HSV.6) G-stage guest-page fault during address translation → only StoreAMOGuestPageFault(23)**

$$
\begin{aligned}
&\big(\mathrm{Priv}\in\{\mathrm{M},\mathrm{HS}\}\ \lor\ (\mathrm{Priv}=\mathrm{U}\land hstatus.HU=1)\big)\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ (\mathrm{EA}=x[rs1])\\
&\land\ \mathrm{GuestPageFault}(\mathrm{EA},\mathrm{store})\\
&\land\ \big(T\in\{\mathrm{B},\mathrm{H},\mathrm{W}\}\ \lor\ \mathrm{XLEN}=64\big)\\
&\land\ (\mathrm{instr}=\mathrm{HSV}.T)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOGuestPageFault}(23)\} \,\}
$$

**(HSV.7) access fault during address translation → only StoreAMOAccessFault(7)**

$$
\begin{aligned}
&\big(\mathrm{Priv}\in\{\mathrm{M},\mathrm{HS}\}\ \lor\ (\mathrm{Priv}=\mathrm{U}\land hstatus.HU=1)\big)\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ (\mathrm{EA}=x[rs1])\\
&\land\ \mathrm{AccessFaultPre}(\mathrm{EA},\mathrm{store})\\
&\land\ \big(T\in\{\mathrm{B},\mathrm{H},\mathrm{W}\}\ \lor\ \mathrm{XLEN}=64\big)\\
&\land\ (\mathrm{instr}=\mathrm{HSV}.T)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOAccessFault}(7)\} \,\}
$$

**(HSV.8) access fault after address translation → only StoreAMOAccessFault(7)**

$$
\begin{aligned}
&\big(\mathrm{Priv}\in\{\mathrm{M},\mathrm{HS}\}\ \lor\ (\mathrm{Priv}=\mathrm{U}\land hstatus.HU=1)\big)\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ (\mathrm{EA}=x[rs1])\\
&\land\ \mathrm{AccessFaultPost}(\mathrm{EA},\mathrm{store})\\
&\land\ \big(T\in\{\mathrm{B},\mathrm{H},\mathrm{W}\}\ \lor\ \mathrm{XLEN}=64\big)\\
&\land\ (\mathrm{instr}=\mathrm{HSV}.T)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOAccessFault}(7)\} \,\}
$$

**(HSV.9) misaligned, checked after address translation → only StoreAMOAddressMisaligned(6)**

$$
\begin{aligned}
&\big(\mathrm{Priv}\in\{\mathrm{M},\mathrm{HS}\}\ \lor\ (\mathrm{Priv}=\mathrm{U}\land hstatus.HU=1)\big)\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ (\mathrm{EA}=x[rs1])\\
&\land\ \mathrm{MisalignedPost}(\mathrm{EA},\mathrm{w}(T))\\
&\land\ \big(T\in\{\mathrm{B},\mathrm{H},\mathrm{W}\}\ \lor\ \mathrm{XLEN}=64\big)\\
&\land\ (\mathrm{instr}=\mathrm{HSV}.T)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{StoreAMOAddressMisaligned}(6)\} \,\}
$$

**(HSV.10) otherwise → store**

$$
\begin{aligned}
&\big(\mathrm{Priv}\in\{\mathrm{M},\mathrm{HS}\}\ \lor\ (\mathrm{Priv}=\mathrm{U}\land hstatus.HU=1)\big)\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ (\mathrm{EA}=x[rs1])\\
&\land\ \mathrm{MemOK}_{\mathrm{store}}(\mathrm{EA},\mathrm{w}(T))\\
&\land\ \big(T\in\{\mathrm{B},\mathrm{H},\mathrm{W}\}\ \lor\ \mathrm{XLEN}=64\big)\\
&\land\ (\mathrm{instr}=\mathrm{HSV}.T)\\
\end{aligned}
\longrightarrow
\{\, \mathrm{mem}[\mathrm{EA},\mathrm{w}(T)]=\mathrm{low}_{\mathrm{w}(T)}(\mathrm{x}[rs2]),\ \mathrm{exception}=\varnothing \,\}
$$
