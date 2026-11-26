# VFNCVT.F.F.W, VFNCVT.ROD.F.F.W — vector narrowing floating-point type-convert

`VFNCVT.F.F.W` converts a `2\cdot\mathrm{SEW}`-wide floating-point element to a `SEW`-wide
floating-point element with the rules of §8.3, and `VFNCVT.ROD.F.F.W` performs the round-to-odd
conversion of the same section (Unpriv. §31.13.19, `sources/riscv-unprivileged.txt:19880-19990`).
The plain form rounds with `fcsr.frm` and can overflow, underflow, and round; the `.rod` form
truncates and sets the least-significant bit, raises `NX(0)` only, and saturates at the largest
finite value. A NaN becomes the canonical quiet NaN of the destination format and raises `NV(4)`
only when it is signaling. `SEW=16` is enabled by `Zvfh` or `Zvfhmin`, and `SEW=32` needs `D`; the
source image has `EMUL=2\cdot\mathrm{LMUL}`, so `LMUL=8` is reserved.

**(VFNCVT.F.F.0) Extension unavailable, vector or floating-point state Off, or `vill=1` → only IllegalInstruction(2)**

$$
\begin{aligned}
&\bigl(\bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\land(vsstatus.VS=\mathrm{Off}(0)\lor sstatus.VS=\mathrm{Off}(0)\lor vsstatus.FS=\mathrm{Off}(0)\lor sstatus.FS=\mathrm{Off}(0))\bigr)\\
&\qquad\lor\ \neg\mathrm{impl}(V)\ \lor\ (\mathrm{SEW}=16\ \land\ \neg\mathrm{impl}(Zvfh)\ \land\ \neg\mathrm{impl}(Zvfhmin))\ \lor\ (\mathrm{SEW}=32\ \land\ \neg\mathrm{impl}(D))\ \lor\ mstatus.VS=\mathrm{Off}(0)\ \lor\ mstatus.FS=\mathrm{Off}(0)\ \lor\ vill=1\bigr)\\
&\land\ (\mathrm{SEW}\in\{16,32\})\\
&\land\ (\mathrm{op}\in\{\mathrm{F.F},\mathrm{ROD.F.F}\})\\
&\land\ (\mathrm{instr}=\mathrm{VFNCVT}.\mathrm{op}.\mathrm{W})
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(VFNCVT.F.F.1) No H, M/S/U: narrowing float conversion**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow(\mathrm{impl}(Zvfh)\lor\mathrm{impl}(Zvfhmin)))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32\}\\
&\land\ \mathrm{LMUL}\le 4\\
&\land\ \mathrm{instr}=\mathrm{VFNCVT}.\mathrm{F}.\mathrm{F}.\mathrm{W}
\end{aligned}
\longrightarrow
\{\, \mathrm{Im}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vd)=\mathrm{Out}_{\mathrm{SEW},\mathrm{LMUL}}(\mathrm{Im}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vd),\lambda i.\pi_1(\mathrm{f2f}_{2\mathrm{SEW}\to\mathrm{SEW},fcsr.frm}(\mathrm{el}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vs2,i))),vl,vstart,\mathrm{vm},\mathrm{V}_0,vta,vma),\ vstart=0,\ mstatus.VS=\mathrm{Dirty}(3),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\bigcup_{i\in\mathrm{Act}(vl,vstart,\mathrm{vm},\mathrm{V}_0)}\pi_2(\mathrm{f2f}_{2\mathrm{SEW}\to\mathrm{SEW},fcsr.frm}(\mathrm{el}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vs2,i))),\ \mathrm{exception}=\varnothing \,\}
$$

**(VFNCVT.F.F.2) H, M/HS/U: narrowing float conversion**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow(\mathrm{impl}(Zvfh)\lor\mathrm{impl}(Zvfhmin)))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32\}\\
&\land\ \mathrm{LMUL}\le 4\\
&\land\ \mathrm{instr}=\mathrm{VFNCVT}.\mathrm{F}.\mathrm{F}.\mathrm{W}
\end{aligned}
\longrightarrow
\{\, \mathrm{Im}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vd)=\mathrm{Out}_{\mathrm{SEW},\mathrm{LMUL}}(\mathrm{Im}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vd),\lambda i.\pi_1(\mathrm{f2f}_{2\mathrm{SEW}\to\mathrm{SEW},fcsr.frm}(\mathrm{el}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vs2,i))),vl,vstart,\mathrm{vm},\mathrm{V}_0,vta,vma),\ vstart=0,\ mstatus.VS=\mathrm{Dirty}(3),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\bigcup_{i\in\mathrm{Act}(vl,vstart,\mathrm{vm},\mathrm{V}_0)}\pi_2(\mathrm{f2f}_{2\mathrm{SEW}\to\mathrm{SEW},fcsr.frm}(\mathrm{el}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vs2,i))),\ \mathrm{exception}=\varnothing \,\}
$$

**(VFNCVT.F.F.3) H, VS/VU: narrowing float conversion**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\bigr)\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow(\mathrm{impl}(Zvfh)\lor\mathrm{impl}(Zvfhmin)))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32\}\\
&\land\ \mathrm{LMUL}\le 4\\
&\land\ \mathrm{instr}=\mathrm{VFNCVT}.\mathrm{F}.\mathrm{F}.\mathrm{W}
\end{aligned}
\longrightarrow
\{\, \mathrm{Im}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vd)=\mathrm{Out}_{\mathrm{SEW},\mathrm{LMUL}}(\mathrm{Im}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vd),\lambda i.\pi_1(\mathrm{f2f}_{2\mathrm{SEW}\to\mathrm{SEW},fcsr.frm}(\mathrm{el}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vs2,i))),vl,vstart,\mathrm{vm},\mathrm{V}_0,vta,vma),\ vstart=0,\ vsstatus.VS=\mathrm{Dirty}(3),\ sstatus.VS=\mathrm{Dirty}(3),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\bigcup_{i\in\mathrm{Act}(vl,vstart,\mathrm{vm},\mathrm{V}_0)}\pi_2(\mathrm{f2f}_{2\mathrm{SEW}\to\mathrm{SEW},fcsr.frm}(\mathrm{el}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vs2,i))),\ \mathrm{exception}=\varnothing \,\}
$$

**(VFNCVT.F.F.4) No H, M/S/U: narrowing round-to-odd conversion**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow(\mathrm{impl}(Zvfh)\lor\mathrm{impl}(Zvfhmin)))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32\}\\
&\land\ \mathrm{LMUL}\le 4\\
&\land\ \mathrm{instr}=\mathrm{VFNCVT}.\mathrm{ROD}.\mathrm{F}.\mathrm{F}.\mathrm{W}
\end{aligned}
\longrightarrow
\{\, \mathrm{Im}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vd)=\mathrm{Out}_{\mathrm{SEW},\mathrm{LMUL}}(\mathrm{Im}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vd),\lambda i.\pi_1(\mathrm{f2f}^{\mathrm{rod}}_{2\mathrm{SEW}\to\mathrm{SEW}}(\mathrm{el}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vs2,i))),vl,vstart,\mathrm{vm},\mathrm{V}_0,vta,vma),\ vstart=0,\ mstatus.VS=\mathrm{Dirty}(3),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\bigcup_{i\in\mathrm{Act}(vl,vstart,\mathrm{vm},\mathrm{V}_0)}\pi_2(\mathrm{f2f}^{\mathrm{rod}}_{2\mathrm{SEW}\to\mathrm{SEW}}(\mathrm{el}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vs2,i))),\ \mathrm{exception}=\varnothing \,\}
$$

**(VFNCVT.F.F.5) H, M/HS/U: narrowing round-to-odd conversion**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow(\mathrm{impl}(Zvfh)\lor\mathrm{impl}(Zvfhmin)))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32\}\\
&\land\ \mathrm{LMUL}\le 4\\
&\land\ \mathrm{instr}=\mathrm{VFNCVT}.\mathrm{ROD}.\mathrm{F}.\mathrm{F}.\mathrm{W}
\end{aligned}
\longrightarrow
\{\, \mathrm{Im}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vd)=\mathrm{Out}_{\mathrm{SEW},\mathrm{LMUL}}(\mathrm{Im}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vd),\lambda i.\pi_1(\mathrm{f2f}^{\mathrm{rod}}_{2\mathrm{SEW}\to\mathrm{SEW}}(\mathrm{el}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vs2,i))),vl,vstart,\mathrm{vm},\mathrm{V}_0,vta,vma),\ vstart=0,\ mstatus.VS=\mathrm{Dirty}(3),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\bigcup_{i\in\mathrm{Act}(vl,vstart,\mathrm{vm},\mathrm{V}_0)}\pi_2(\mathrm{f2f}^{\mathrm{rod}}_{2\mathrm{SEW}\to\mathrm{SEW}}(\mathrm{el}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vs2,i))),\ \mathrm{exception}=\varnothing \,\}
$$

**(VFNCVT.F.F.6) H, VS/VU: narrowing round-to-odd conversion**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\bigr)\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow(\mathrm{impl}(Zvfh)\lor\mathrm{impl}(Zvfhmin)))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32\}\\
&\land\ \mathrm{LMUL}\le 4\\
&\land\ \mathrm{instr}=\mathrm{VFNCVT}.\mathrm{ROD}.\mathrm{F}.\mathrm{F}.\mathrm{W}
\end{aligned}
\longrightarrow
\{\, \mathrm{Im}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vd)=\mathrm{Out}_{\mathrm{SEW},\mathrm{LMUL}}(\mathrm{Im}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vd),\lambda i.\pi_1(\mathrm{f2f}^{\mathrm{rod}}_{2\mathrm{SEW}\to\mathrm{SEW}}(\mathrm{el}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vs2,i))),vl,vstart,\mathrm{vm},\mathrm{V}_0,vta,vma),\ vstart=0,\ vsstatus.VS=\mathrm{Dirty}(3),\ sstatus.VS=\mathrm{Dirty}(3),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\bigcup_{i\in\mathrm{Act}(vl,vstart,\mathrm{vm},\mathrm{V}_0)}\pi_2(\mathrm{f2f}^{\mathrm{rod}}_{2\mathrm{SEW}\to\mathrm{SEW}}(\mathrm{el}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vs2,i))),\ \mathrm{exception}=\varnothing \,\}
$$
