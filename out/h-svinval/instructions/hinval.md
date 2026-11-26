# HINVAL.VVMA, HINVAL.GVMA — fine-grained hypervisor translation invalidation

`HINVAL.VVMA` and `HINVAL.GVMA` are the Svinval fine-grained counterparts of `HFENCE.VVMA` and
`HFENCE.GVMA`. Executed in order with `SFENCE.W.INVAL` before and `SFENCE.INVAL.IR` after, the
sequence has the same effect as the corresponding `HFENCE` with the same operands; the two
`HINVAL` instructions therefore carry only the invalidation part of the fence. Neither writes a
register or memory, and the right-hand side contains only `exception`.

`HINVAL.VVMA` takes a guest virtual address in `rs1` and a VS-level ASID in `rs2`.
`HINVAL.GVMA` takes a guest physical address shifted right by 2 bits in `rs1` and a VMID in
`rs2`; it uses VMIDs instead of ASIDs. The instructions require the same permissions and raise
the same exceptions as their `HFENCE` counterparts (Priv. §12.9,
`sources/riscv-privileged.txt:8318-8340`). Requires `H` and `Svinval`.

The `exception` field of every block below lists only the exceptions the instruction itself can raise, and reads `\mathrm{exception}=\varnothing` when it raises none; the instruction-fetch outcomes depend only on the fetch address and are stated once in the README, not repeated here.

**(HINVAL.0) Extension unavailable → only IllegalInstruction(2)**

$$
\begin{aligned}
&\big(\neg\mathrm{impl}(\mathrm{H})\ \lor\ \neg\mathrm{impl}(\mathrm{Svinval})\big)\\
&\land\ (\mathrm{instr}=\mathrm{HINVAL.VVMA}\ \lor\ \mathrm{instr}=\mathrm{HINVAL.GVMA})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(HINVAL.1) Executed with $V=1$ → only VirtualInstruction(22)**

$$
\begin{aligned}
&(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\})\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ \mathrm{impl}(\mathrm{Svinval})\\
&\land\ (\mathrm{instr}=\mathrm{HINVAL.VVMA}\ \lor\ \mathrm{instr}=\mathrm{HINVAL.GVMA})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{VirtualInstruction}(22)\} \,\}
$$

**(HINVAL.2) Executed in U-mode → only IllegalInstruction(2)**

$$
\begin{aligned}
&(\mathrm{Priv}=\mathrm{U})\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ \mathrm{impl}(\mathrm{Svinval})\\
&\land\ (\mathrm{instr}=\mathrm{HINVAL.VVMA}\ \lor\ \mathrm{instr}=\mathrm{HINVAL.GVMA})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(HINVAL.3) `HINVAL.GVMA` in HS-mode with `mstatus.TVM=1` → only IllegalInstruction(2)**

$$
\begin{aligned}
&(\mathrm{Priv}=\mathrm{HS}\land mstatus.TVM=1)\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ \mathrm{impl}(\mathrm{Svinval})\\
&\land\ (\mathrm{instr}=\mathrm{HINVAL.GVMA})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(HINVAL.4) `HINVAL.VVMA` in M-mode or HS-mode → VS-stage invalidation**

$$
\begin{aligned}
&(\mathrm{Priv}=\mathrm{M}\ \lor\ \mathrm{Priv}=\mathrm{HS})\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ \mathrm{impl}(\mathrm{Svinval})\\
&\land\ (\mathrm{instr}=\mathrm{HINVAL.VVMA})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\varnothing \,\}
$$

**(HINVAL.5) `HINVAL.GVMA` in M-mode, or in HS-mode with `mstatus.TVM=0` → G-stage invalidation**

$$
\begin{aligned}
&(\mathrm{Priv}=\mathrm{M}\ \lor\ (\mathrm{Priv}=\mathrm{HS}\land mstatus.TVM=0))\\
&\land\ \mathrm{impl}(\mathrm{H})\\
&\land\ \mathrm{impl}(\mathrm{Svinval})\\
&\land\ (\mathrm{instr}=\mathrm{HINVAL.GVMA})\\
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\varnothing \,\}
$$
