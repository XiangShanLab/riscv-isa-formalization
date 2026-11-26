# VFMV.S.F — vector floating-point move, scalar to vector element 0

`VFMV.S.F` copies the scalar `f[rs1]` into element 0 of `vd` (Unpriv. §31.16.2,
`sources/riscv-unprivileged.txt:20025-20038`). It ignores `LMUL` and register groups: the
destination is the single register `vd` with $N=\mathrm{VLEN}/\mathrm{SEW}$ element slots, and the
instruction is encoded with `vm=1`; the masked encoding is reserved (§4.5). Elements
$1\le i<N$ are tail elements under the `vta` policy, whatever `vl` is, and if `vstart\ge vl` no
element is updated at all. This is the write model `\mathrm{SOut}` of §3.4 with the condition
`vstart<vl`. No flag is raised and no `f` register is written.

**(VFMV.S.F.0) Extension unavailable, vector or floating-point state Off, or `vill=1` → only IllegalInstruction(2)**

$$
\begin{aligned}
&\bigl(\bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\land(vsstatus.VS=\mathrm{Off}(0)\lor sstatus.VS=\mathrm{Off}(0)\lor vsstatus.FS=\mathrm{Off}(0)\lor sstatus.FS=\mathrm{Off}(0))\bigr)\\
&\qquad\lor\ \neg\mathrm{impl}(V)\ \lor\ (\mathrm{SEW}=16\ \land\ \neg\mathrm{impl}(Zvfh))\ \lor\ (\mathrm{SEW}=32\ \land\ \neg\mathrm{impl}(F))\ \lor\ (\mathrm{SEW}=64\ \land\ \neg\mathrm{impl}(D))\ \lor\ mstatus.VS=\mathrm{Off}(0)\ \lor\ mstatus.FS=\mathrm{Off}(0)\ \lor\ vill=1\bigr)\\
&\land\ (\mathrm{SEW}\in\{16,32,64\})\\
&\land\ (\mathrm{instr}=\mathrm{VFMV}.\mathrm{S}.\mathrm{F})
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(VFMV.S.F.1) No H, M/S/U: scalar insertion into element 0**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow\mathrm{impl}(Zvfh))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(F))\ \land\ (\mathrm{SEW}=64\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32,64\}\\
&\land\ \mathrm{vm}=1\\
&\land\ \mathrm{instr}=\mathrm{VFMV}.\mathrm{S}.\mathrm{F}
\end{aligned}
\longrightarrow
\{\, \mathrm{Im}^{\mathrm{SEW}}_{1}(vd)=\mathrm{SOut}_{\mathrm{SEW}}\bigl(\mathrm{Im}^{\mathrm{SEW}}_{1}(vd),\mathrm{fsrc}_{\mathrm{SEW}}(f[rs1]),vstart<vl,vta\bigr),\ vstart=0,\ mstatus.VS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(VFMV.S.F.2) H, M/HS/U: scalar insertion into element 0**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow\mathrm{impl}(Zvfh))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(F))\ \land\ (\mathrm{SEW}=64\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32,64\}\\
&\land\ \mathrm{vm}=1\\
&\land\ \mathrm{instr}=\mathrm{VFMV}.\mathrm{S}.\mathrm{F}
\end{aligned}
\longrightarrow
\{\, \mathrm{Im}^{\mathrm{SEW}}_{1}(vd)=\mathrm{SOut}_{\mathrm{SEW}}\bigl(\mathrm{Im}^{\mathrm{SEW}}_{1}(vd),\mathrm{fsrc}_{\mathrm{SEW}}(f[rs1]),vstart<vl,vta\bigr),\ vstart=0,\ mstatus.VS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$

**(VFMV.S.F.3) H, VS/VU: scalar insertion into element 0**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\bigr)\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow\mathrm{impl}(Zvfh))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(F))\ \land\ (\mathrm{SEW}=64\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32,64\}\\
&\land\ \mathrm{vm}=1\\
&\land\ \mathrm{instr}=\mathrm{VFMV}.\mathrm{S}.\mathrm{F}
\end{aligned}
\longrightarrow
\{\, \mathrm{Im}^{\mathrm{SEW}}_{1}(vd)=\mathrm{SOut}_{\mathrm{SEW}}\bigl(\mathrm{Im}^{\mathrm{SEW}}_{1}(vd),\mathrm{fsrc}_{\mathrm{SEW}}(f[rs1]),vstart<vl,vta\bigr),\ vstart=0,\ vsstatus.VS=\mathrm{Dirty}(3),\ sstatus.VS=\mathrm{Dirty}(3),\ \mathrm{exception}=\varnothing \,\}
$$
