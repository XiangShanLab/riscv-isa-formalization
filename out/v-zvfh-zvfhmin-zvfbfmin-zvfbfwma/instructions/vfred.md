# VFREDOSUM.VS, VFREDUSUM.VS, VFREDMAX.VS, VFREDMIN.VS — vector floating-point reductions

The four floating-point reductions combine the active elements of `vs2` with the scalar seed held in
element 0 of `vs1` and write the result to element 0 of `vd` (Unpriv. §31.14.3,
`sources/riscv-unprivileged.txt:19360-19430`). The seed is always included, whatever the mask
value; the inactive elements are excluded. The destination is a single register with
$N=\mathrm{VLEN}/\mathrm{SEW}$ slots, element 0 receives the result and elements $1\le i<N$ are
tail elements under `vta`; if `vl=0` the destination is not updated. A non-zero `vstart` raises
`IllegalInstruction(2)` (§4.4), so every formula has `vstart=0`.

Write $z=\mathrm{el}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vs1,0)$,
$a_i=\mathrm{el}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vs2,i)$, and $x(i)=(a_i,\varnothing)$ for the
per-element pair. The left side of each formula binds the pair `(v,F)` to the reduction result:
`ordsum` combines the seed with the active elements in increasing index order, `usum` is the set of
sums an unordered tree may produce, and `ordmax`/`ordmin` are the ordered maximum and minimum folds.

**(VFRED.0) Extension unavailable, vector or floating-point state Off, `vill=1`, or `vstart\ne 0` → only IllegalInstruction(2)**

$$
\begin{aligned}
&\bigl(\bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\land(vsstatus.VS=\mathrm{Off}(0)\lor sstatus.VS=\mathrm{Off}(0)\lor vsstatus.FS=\mathrm{Off}(0)\lor sstatus.FS=\mathrm{Off}(0))\bigr)\\
&\qquad\lor\ \neg\mathrm{impl}(V)\ \lor\ (\mathrm{SEW}=16\ \land\ \neg\mathrm{impl}(Zvfh))\ \lor\ (\mathrm{SEW}=32\ \land\ \neg\mathrm{impl}(F))\ \lor\ (\mathrm{SEW}=64\ \land\ \neg\mathrm{impl}(D))\ \lor\ vstart\ne 0\ \lor\ mstatus.VS=\mathrm{Off}(0)\ \lor\ mstatus.FS=\mathrm{Off}(0)\ \lor\ vill=1\bigr)\\
&\land\ (\mathrm{SEW}\in\{16,32,64\})\\
&\land\ (\mathrm{op}\in\{\mathrm{OSUM},\mathrm{USUM},\mathrm{MAX},\mathrm{MIN}\})\\
&\land\ (\mathrm{instr}=\mathrm{VFRED}_{\mathrm{op}}.\mathrm{VS})
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(VFRED.1) No H, M/S/U: ordered sum**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow\mathrm{impl}(Zvfh))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(F))\ \land\ (\mathrm{SEW}=64\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32,64\}\\
&\land\ (v,F)=\mathrm{ordsum}_{\mathrm{SEW}}\bigl(z,\mathrm{Act}(vl,0,\mathrm{vm},\mathrm{V}_0),x\bigr)\\
&\land\ \mathrm{instr}=\mathrm{VFREDOSUM}.\mathrm{VS}
\end{aligned}
\longrightarrow
\{\, \mathrm{Rout}_{\mathrm{SEW}}(\mathrm{V}_{vd},v,vl,vta),\ vstart=0,\ mstatus.VS=\mathrm{Dirty}(3),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=F,\ \mathrm{exception}=\varnothing \,\}
$$

**(VFRED.2) H, M/HS/U: ordered sum**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow\mathrm{impl}(Zvfh))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(F))\ \land\ (\mathrm{SEW}=64\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32,64\}\\
&\land\ (v,F)=\mathrm{ordsum}_{\mathrm{SEW}}\bigl(z,\mathrm{Act}(vl,0,\mathrm{vm},\mathrm{V}_0),x\bigr)\\
&\land\ \mathrm{instr}=\mathrm{VFREDOSUM}.\mathrm{VS}
\end{aligned}
\longrightarrow
\{\, \mathrm{Rout}_{\mathrm{SEW}}(\mathrm{V}_{vd},v,vl,vta),\ vstart=0,\ mstatus.VS=\mathrm{Dirty}(3),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=F,\ \mathrm{exception}=\varnothing \,\}
$$

**(VFRED.3) H, VS/VU: ordered sum**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\bigr)\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow\mathrm{impl}(Zvfh))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(F))\ \land\ (\mathrm{SEW}=64\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32,64\}\\
&\land\ (v,F)=\mathrm{ordsum}_{\mathrm{SEW}}\bigl(z,\mathrm{Act}(vl,0,\mathrm{vm},\mathrm{V}_0),x\bigr)\\
&\land\ \mathrm{instr}=\mathrm{VFREDOSUM}.\mathrm{VS}
\end{aligned}
\longrightarrow
\{\, \mathrm{Rout}_{\mathrm{SEW}}(\mathrm{V}_{vd},v,vl,vta),\ vstart=0,\ vsstatus.VS=\mathrm{Dirty}(3),\ sstatus.VS=\mathrm{Dirty}(3),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=F,\ \mathrm{exception}=\varnothing \,\}
$$

**(VFRED.4) No H, M/S/U: unordered sum**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow\mathrm{impl}(Zvfh))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(F))\ \land\ (\mathrm{SEW}=64\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32,64\}\\
&\land\ (v,F)\in\mathrm{usum}_{\mathrm{SEW}}\bigl(z,\mathrm{Act}(vl,0,\mathrm{vm},\mathrm{V}_0),x\bigr)\\
&\land\ \mathrm{instr}=\mathrm{VFREDUSUM}.\mathrm{VS}
\end{aligned}
\longrightarrow
\{\, \mathrm{Rout}_{\mathrm{SEW}}(\mathrm{V}_{vd},v,vl,vta),\ vstart=0,\ mstatus.VS=\mathrm{Dirty}(3),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=F,\ \mathrm{exception}=\varnothing \,\}
$$

**(VFRED.5) H, M/HS/U: unordered sum**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow\mathrm{impl}(Zvfh))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(F))\ \land\ (\mathrm{SEW}=64\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32,64\}\\
&\land\ (v,F)\in\mathrm{usum}_{\mathrm{SEW}}\bigl(z,\mathrm{Act}(vl,0,\mathrm{vm},\mathrm{V}_0),x\bigr)\\
&\land\ \mathrm{instr}=\mathrm{VFREDUSUM}.\mathrm{VS}
\end{aligned}
\longrightarrow
\{\, \mathrm{Rout}_{\mathrm{SEW}}(\mathrm{V}_{vd},v,vl,vta),\ vstart=0,\ mstatus.VS=\mathrm{Dirty}(3),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=F,\ \mathrm{exception}=\varnothing \,\}
$$

**(VFRED.6) H, VS/VU: unordered sum**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\bigr)\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow\mathrm{impl}(Zvfh))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(F))\ \land\ (\mathrm{SEW}=64\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32,64\}\\
&\land\ (v,F)\in\mathrm{usum}_{\mathrm{SEW}}\bigl(z,\mathrm{Act}(vl,0,\mathrm{vm},\mathrm{V}_0),x\bigr)\\
&\land\ \mathrm{instr}=\mathrm{VFREDUSUM}.\mathrm{VS}
\end{aligned}
\longrightarrow
\{\, \mathrm{Rout}_{\mathrm{SEW}}(\mathrm{V}_{vd},v,vl,vta),\ vstart=0,\ vsstatus.VS=\mathrm{Dirty}(3),\ sstatus.VS=\mathrm{Dirty}(3),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=F,\ \mathrm{exception}=\varnothing \,\}
$$

**(VFRED.7) No H, M/S/U: maximum**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow\mathrm{impl}(Zvfh))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(F))\ \land\ (\mathrm{SEW}=64\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32,64\}\\
&\land\ (v,F)=\mathrm{ordmax}_{\mathrm{SEW}}\bigl(z,\mathrm{Act}(vl,0,\mathrm{vm},\mathrm{V}_0),x\bigr)\\
&\land\ \mathrm{instr}=\mathrm{VFREDMAX}.\mathrm{VS}
\end{aligned}
\longrightarrow
\{\, \mathrm{Rout}_{\mathrm{SEW}}(\mathrm{V}_{vd},v,vl,vta),\ vstart=0,\ mstatus.VS=\mathrm{Dirty}(3),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=F,\ \mathrm{exception}=\varnothing \,\}
$$

**(VFRED.8) H, M/HS/U: maximum**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow\mathrm{impl}(Zvfh))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(F))\ \land\ (\mathrm{SEW}=64\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32,64\}\\
&\land\ (v,F)=\mathrm{ordmax}_{\mathrm{SEW}}\bigl(z,\mathrm{Act}(vl,0,\mathrm{vm},\mathrm{V}_0),x\bigr)\\
&\land\ \mathrm{instr}=\mathrm{VFREDMAX}.\mathrm{VS}
\end{aligned}
\longrightarrow
\{\, \mathrm{Rout}_{\mathrm{SEW}}(\mathrm{V}_{vd},v,vl,vta),\ vstart=0,\ mstatus.VS=\mathrm{Dirty}(3),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=F,\ \mathrm{exception}=\varnothing \,\}
$$

**(VFRED.9) H, VS/VU: maximum**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\bigr)\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow\mathrm{impl}(Zvfh))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(F))\ \land\ (\mathrm{SEW}=64\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32,64\}\\
&\land\ (v,F)=\mathrm{ordmax}_{\mathrm{SEW}}\bigl(z,\mathrm{Act}(vl,0,\mathrm{vm},\mathrm{V}_0),x\bigr)\\
&\land\ \mathrm{instr}=\mathrm{VFREDMAX}.\mathrm{VS}
\end{aligned}
\longrightarrow
\{\, \mathrm{Rout}_{\mathrm{SEW}}(\mathrm{V}_{vd},v,vl,vta),\ vstart=0,\ vsstatus.VS=\mathrm{Dirty}(3),\ sstatus.VS=\mathrm{Dirty}(3),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=F,\ \mathrm{exception}=\varnothing \,\}
$$

**(VFRED.10) No H, M/S/U: minimum**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow\mathrm{impl}(Zvfh))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(F))\ \land\ (\mathrm{SEW}=64\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32,64\}\\
&\land\ (v,F)=\mathrm{ordmin}_{\mathrm{SEW}}\bigl(z,\mathrm{Act}(vl,0,\mathrm{vm},\mathrm{V}_0),x\bigr)\\
&\land\ \mathrm{instr}=\mathrm{VFREDMIN}.\mathrm{VS}
\end{aligned}
\longrightarrow
\{\, \mathrm{Rout}_{\mathrm{SEW}}(\mathrm{V}_{vd},v,vl,vta),\ vstart=0,\ mstatus.VS=\mathrm{Dirty}(3),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=F,\ \mathrm{exception}=\varnothing \,\}
$$

**(VFRED.11) H, M/HS/U: minimum**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow\mathrm{impl}(Zvfh))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(F))\ \land\ (\mathrm{SEW}=64\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32,64\}\\
&\land\ (v,F)=\mathrm{ordmin}_{\mathrm{SEW}}\bigl(z,\mathrm{Act}(vl,0,\mathrm{vm},\mathrm{V}_0),x\bigr)\\
&\land\ \mathrm{instr}=\mathrm{VFREDMIN}.\mathrm{VS}
\end{aligned}
\longrightarrow
\{\, \mathrm{Rout}_{\mathrm{SEW}}(\mathrm{V}_{vd},v,vl,vta),\ vstart=0,\ mstatus.VS=\mathrm{Dirty}(3),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=F,\ \mathrm{exception}=\varnothing \,\}
$$

**(VFRED.12) H, VS/VU: minimum**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\bigr)\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=16\Rightarrow\mathrm{impl}(Zvfh))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(F))\ \land\ (\mathrm{SEW}=64\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{16,32,64\}\\
&\land\ (v,F)=\mathrm{ordmin}_{\mathrm{SEW}}\bigl(z,\mathrm{Act}(vl,0,\mathrm{vm},\mathrm{V}_0),x\bigr)\\
&\land\ \mathrm{instr}=\mathrm{VFREDMIN}.\mathrm{VS}
\end{aligned}
\longrightarrow
\{\, \mathrm{Rout}_{\mathrm{SEW}}(\mathrm{V}_{vd},v,vl,vta),\ vstart=0,\ vsstatus.VS=\mathrm{Dirty}(3),\ sstatus.VS=\mathrm{Dirty}(3),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=F,\ \mathrm{exception}=\varnothing \,\}
$$
