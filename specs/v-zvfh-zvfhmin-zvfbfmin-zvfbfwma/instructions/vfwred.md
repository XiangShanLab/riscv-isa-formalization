# VFWREDOSUM.VS, VFWREDUSUM.VS — vector widening floating-point reductions

The two widening reductions add a `2\cdot\mathrm{SEW}`-wide accumulator to the widened `SEW`-wide
elements of `vs2` (Unpriv. §31.14.4, `sources/riscv-unprivileged.txt:19470-19490`). The seed is
element 0 of `vs1`, read at `2\cdot\mathrm{SEW}` bits with `EMUL=2\cdot\mathrm{LMUL}`; the
destination is a single register with $N=\mathrm{VLEN}/(2\cdot\mathrm{SEW})$ slots, element 0
receives the result and the rest are tail elements under `vta`. A non-zero `vstart` raises
`IllegalInstruction(2)`, and `2\cdot\mathrm{LMUL}\le 8` makes `LMUL=8` reserved. `SEW=16` needs
`Zvfh` and `SEW=32` needs `D`.

Write $z=\mathrm{el}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vs1,0)$ and
$x(i)=(\mathrm{widen}(\mathrm{el}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vs2,i)),\varnothing)$; the
widening is exact and raises no flag, so a signaling NaN raises `NV(4)` at the first combining
step. The left side binds `(v,F)` to the ordered fold or to the set of unordered outcomes.

**(VFWRED.0) Extension unavailable, vector or floating-point state Off, `vill=1`, or `vstart\ne 0` → only IllegalInstruction(2)**

$$
\begin{aligned}
&\bigl(\bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\land(vsstatus.VS=\mathrm{Off}(0)\lor sstatus.VS=\mathrm{Off}(0)\lor vsstatus.FS=\mathrm{Off}(0)\lor sstatus.FS=\mathrm{Off}(0))\bigr)\\
&\qquad\lor\ \neg\mathrm{impl}(V)\ \lor\ (\mathrm{SEW}=16\ \land\ \neg\mathrm{impl}(Zvfh))\ \lor\ (\mathrm{SEW}=32\ \land\ \neg\mathrm{impl}(F))\ \lor\ (\mathrm{SEW}=64\ \land\ \neg\mathrm{impl}(D))\ \lor\ vstart\ne 0\ \lor\ mstatus.VS=\mathrm{Off}(0)\ \lor\ mstatus.FS=\mathrm{Off}(0)\ \lor\ vill=1\bigr)\\
&\land\ (\mathrm{SEW}\in\{16,32\})\\
&\land\ (\mathrm{op}\in\{\mathrm{OSUM},\mathrm{USUM}\})\\
&\land\ (\mathrm{instr}=\mathrm{VFWRED}_{\mathrm{op}}.\mathrm{VS})
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(VFWRED.1) No H, M/S/U: ordered widening sum**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow\mathrm{impl}(Zvfh))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(F))\ \land\ (\mathrm{SEW}=64\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32\}\\
&\land\ \mathrm{LMUL}\le 4\\
&\land\ (v,F)=\mathrm{ordsum}_{2\mathrm{SEW}}\bigl(z,\mathrm{Act}(vl,0,\mathrm{vm},\mathrm{V}_0),x\bigr)\\
&\land\ \mathrm{instr}=\mathrm{VFWREDOSUM}.\mathrm{VS}
\end{aligned}
\longrightarrow
\{\, \mathrm{Rout}_{2\mathrm{SEW}}(\mathrm{V}_{vd},v,vl,vta),\ vstart=0,\ mstatus.VS=\mathrm{Dirty}(3),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=F,\ \mathrm{exception}=\varnothing \,\}
$$

**(VFWRED.2) H, M/HS/U: ordered widening sum**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow\mathrm{impl}(Zvfh))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(F))\ \land\ (\mathrm{SEW}=64\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32\}\\
&\land\ \mathrm{LMUL}\le 4\\
&\land\ (v,F)=\mathrm{ordsum}_{2\mathrm{SEW}}\bigl(z,\mathrm{Act}(vl,0,\mathrm{vm},\mathrm{V}_0),x\bigr)\\
&\land\ \mathrm{instr}=\mathrm{VFWREDOSUM}.\mathrm{VS}
\end{aligned}
\longrightarrow
\{\, \mathrm{Rout}_{2\mathrm{SEW}}(\mathrm{V}_{vd},v,vl,vta),\ vstart=0,\ mstatus.VS=\mathrm{Dirty}(3),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=F,\ \mathrm{exception}=\varnothing \,\}
$$

**(VFWRED.3) H, VS/VU: ordered widening sum**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\bigr)\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow\mathrm{impl}(Zvfh))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(F))\ \land\ (\mathrm{SEW}=64\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32\}\\
&\land\ \mathrm{LMUL}\le 4\\
&\land\ (v,F)=\mathrm{ordsum}_{2\mathrm{SEW}}\bigl(z,\mathrm{Act}(vl,0,\mathrm{vm},\mathrm{V}_0),x\bigr)\\
&\land\ \mathrm{instr}=\mathrm{VFWREDOSUM}.\mathrm{VS}
\end{aligned}
\longrightarrow
\{\, \mathrm{Rout}_{2\mathrm{SEW}}(\mathrm{V}_{vd},v,vl,vta),\ vstart=0,\ vsstatus.VS=\mathrm{Dirty}(3),\ sstatus.VS=\mathrm{Dirty}(3),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=F,\ \mathrm{exception}=\varnothing \,\}
$$

**(VFWRED.4) No H, M/S/U: unordered widening sum**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow\mathrm{impl}(Zvfh))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(F))\ \land\ (\mathrm{SEW}=64\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32\}\\
&\land\ \mathrm{LMUL}\le 4\\
&\land\ (v,F)\in\mathrm{usum}_{2\mathrm{SEW}}\bigl(z,\mathrm{Act}(vl,0,\mathrm{vm},\mathrm{V}_0),x\bigr)\\
&\land\ \mathrm{instr}=\mathrm{VFWREDUSUM}.\mathrm{VS}
\end{aligned}
\longrightarrow
\{\, \mathrm{Rout}_{2\mathrm{SEW}}(\mathrm{V}_{vd},v,vl,vta),\ vstart=0,\ mstatus.VS=\mathrm{Dirty}(3),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=F,\ \mathrm{exception}=\varnothing \,\}
$$

**(VFWRED.5) H, M/HS/U: unordered widening sum**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow\mathrm{impl}(Zvfh))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(F))\ \land\ (\mathrm{SEW}=64\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32\}\\
&\land\ \mathrm{LMUL}\le 4\\
&\land\ (v,F)\in\mathrm{usum}_{2\mathrm{SEW}}\bigl(z,\mathrm{Act}(vl,0,\mathrm{vm},\mathrm{V}_0),x\bigr)\\
&\land\ \mathrm{instr}=\mathrm{VFWREDUSUM}.\mathrm{VS}
\end{aligned}
\longrightarrow
\{\, \mathrm{Rout}_{2\mathrm{SEW}}(\mathrm{V}_{vd},v,vl,vta),\ vstart=0,\ mstatus.VS=\mathrm{Dirty}(3),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=F,\ \mathrm{exception}=\varnothing \,\}
$$

**(VFWRED.6) H, VS/VU: unordered widening sum**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\bigr)\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow\mathrm{impl}(Zvfh))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(F))\ \land\ (\mathrm{SEW}=64\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32\}\\
&\land\ \mathrm{LMUL}\le 4\\
&\land\ (v,F)\in\mathrm{usum}_{2\mathrm{SEW}}\bigl(z,\mathrm{Act}(vl,0,\mathrm{vm},\mathrm{V}_0),x\bigr)\\
&\land\ \mathrm{instr}=\mathrm{VFWREDUSUM}.\mathrm{VS}
\end{aligned}
\longrightarrow
\{\, \mathrm{Rout}_{2\mathrm{SEW}}(\mathrm{V}_{vd},v,vl,vta),\ vstart=0,\ vsstatus.VS=\mathrm{Dirty}(3),\ sstatus.VS=\mathrm{Dirty}(3),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=F,\ \mathrm{exception}=\varnothing \,\}
$$
