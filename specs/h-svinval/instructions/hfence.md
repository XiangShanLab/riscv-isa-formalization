# HFENCE.VVMA, HFENCE.GVMA — hypervisor memory-management fences

`HFENCE.VVMA` orders every store already visible to the current hart before all subsequent
implicit reads made for VS-stage address translation, for instructions that execute while
`hgatp.VMID` has the same value as when the fence executed. `HFENCE.GVMA` orders stores before
all subsequent implicit reads made for G-stage address translation. Neither instruction writes a
register or memory; the ordering guarantee is the whole result, and the right-hand side therefore
contains only `exception`.

For `HFENCE.VVMA`, `rs1` selects a guest virtual address and `rs2` a VS-level ASID; for
`HFENCE.GVMA`, `rs1` selects a guest physical address shifted right by 2 bits and `rs2` a VMID.
A zero operand selects all addresses or all identifiers. The arguments narrow which cached
translations must be invalidated; a simpler implementation may ignore them and fence globally
(Priv. §15.3.2, `sources/riscv-privileged.txt:9850-9930`). Requires `H`.

The `exception` field of every block below lists only the exceptions the instruction itself can raise, and reads `\mathrm{exception}=\varnothing` when it raises none; the instruction-fetch outcomes depend only on the fetch address and are stated once in the README, not repeated here.

**(HFENCE.0) Extension unavailable → only IllegalInstruction(2)**

$$
\begin{aligned}
&\neg\mathrm{impl}(\mathrm{H})\\
&\land\ (\mathrm{instr}=\mathrm{HFENCE.VVMA}\ \lor\ \mathrm{instr}=\mathrm{HFENCE.GVMA})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(HFENCE.1) Executed with $V=1$ → only VirtualInstruction(22)**

$$
\begin{aligned}
&(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\})\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ (\mathrm{instr}=\mathrm{HFENCE.VVMA}\ \lor\ \mathrm{instr}=\mathrm{HFENCE.GVMA})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{VirtualInstruction}(22)\} \,\}
$$

**(HFENCE.2) Executed in U-mode → only IllegalInstruction(2)**

$$
\begin{aligned}
&(\mathrm{Priv}=\mathrm{U})\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ (\mathrm{instr}=\mathrm{HFENCE.VVMA}\ \lor\ \mathrm{instr}=\mathrm{HFENCE.GVMA})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(HFENCE.3) `HFENCE.GVMA` in HS-mode with `mstatus.TVM=1` → only IllegalInstruction(2)**

$$
\begin{aligned}
&(\mathrm{Priv}=\mathrm{HS}\land mstatus.TVM=1)\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ (\mathrm{instr}=\mathrm{HFENCE.GVMA})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(HFENCE.4) `HFENCE.VVMA` in M-mode or HS-mode → VS-stage fence**

$$
\begin{aligned}
&(\mathrm{Priv}=\mathrm{M}\ \lor\ \mathrm{Priv}=\mathrm{HS})\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ (\mathrm{instr}=\mathrm{HFENCE.VVMA})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\varnothing \,\}
$$

**(HFENCE.5) `HFENCE.GVMA` in M-mode, or in HS-mode with `mstatus.TVM=0` → G-stage fence**

$$
\begin{aligned}
&(\mathrm{Priv}=\mathrm{M}\ \lor\ (\mathrm{Priv}=\mathrm{HS}\land mstatus.TVM=0))\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ (\mathrm{instr}=\mathrm{HFENCE.GVMA})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\varnothing \,\}
$$
