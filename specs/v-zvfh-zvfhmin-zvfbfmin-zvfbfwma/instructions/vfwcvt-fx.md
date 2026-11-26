# VFWCVT.F.X{U}.V — vector widening integer/floating-point type-convert

`VFWCVT.F.XU.V` and `VFWCVT.F.X.V` convert a `SEW`-wide integer element to a `2\cdot\mathrm{SEW}`-wide
floating-point element with the rules of §8.2 (Unpriv. §31.13.18,
`sources/riscv-unprivileged.txt:19240-19275`). The result is exact when the integer fits the
destination precision and otherwise is rounded once with `fcsr.frm`. The destination has
`EEW=2\cdot\mathrm{SEW}` and `EMUL=2\cdot\mathrm{LMUL}`, so `LMUL=8` is reserved. The extension
condition follows the destination format: `SEW=8` needs `Zvfh`, `SEW=16` needs `F`, and `SEW=32`
needs `D`.

**(VFWCVT.F.X.0) Extension unavailable, vector or floating-point state Off, or `vill=1` → only IllegalInstruction(2)**

$$
\begin{aligned}
&\bigl(\bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\land(vsstatus.VS=\mathrm{Off}(0)\lor sstatus.VS=\mathrm{Off}(0)\lor vsstatus.FS=\mathrm{Off}(0)\lor sstatus.FS=\mathrm{Off}(0))\bigr)\\
&\qquad\lor\ \neg\mathrm{impl}(V)\ \lor\ (\mathrm{SEW}=8\ \land\ \neg\mathrm{impl}(Zvfh))\ \lor\ (\mathrm{SEW}=16\ \land\ \neg\mathrm{impl}(F))\ \lor\ (\mathrm{SEW}=32\ \land\ \neg\mathrm{impl}(D))\ \lor\ mstatus.VS=\mathrm{Off}(0)\ \lor\ mstatus.FS=\mathrm{Off}(0)\ \lor\ vill=1\bigr)\\
&\land\ (\mathrm{SEW}\in\{8,16,32\})\\
&\land\ (\mathrm{instr}=\mathrm{VFWCVT}.\mathrm{F}.\mathrm{XU}.\mathrm{V}\ \lor\ \mathrm{instr}=\mathrm{VFWCVT}.\mathrm{F}.\mathrm{X}.\mathrm{V})
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**(VFWCVT.F.X.1) No H, M/S/U: unsigned integer to float, widened**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=8\Rightarrow\mathrm{impl}(Zvfh))\ \land\ (\mathrm{SEW}=16\Rightarrow\mathrm{impl}(F))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{8,16,32\}\\
&\land\ \mathrm{LMUL}\le 4\\
&\land\ \mathrm{instr}=\mathrm{VFWCVT}.\mathrm{F}.\mathrm{XU}.\mathrm{V}
\end{aligned}
\longrightarrow
\{\, \mathrm{Im}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vd)=\mathrm{Out}_{2\mathrm{SEW},2\mathrm{LMUL}}(\mathrm{Im}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vd),\lambda i.\pi_1(\mathrm{i2f}^{\mathrm{u}}_{2\mathrm{SEW}\to2\mathrm{SEW},fcsr.frm}(\mathrm{el}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vs2,i))),vl,vstart,\mathrm{vm},\mathrm{V}_0,vta,vma),\ vstart=0,\ mstatus.VS=\mathrm{Dirty}(3),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\bigcup_{i\in\mathrm{Act}(vl,vstart,\mathrm{vm},\mathrm{V}_0)}\pi_2(\mathrm{i2f}^{\mathrm{u}}_{2\mathrm{SEW}\to2\mathrm{SEW},fcsr.frm}(\mathrm{el}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vs2,i))),\ \mathrm{exception}=\varnothing \,\}
$$

**(VFWCVT.F.X.2) H, M/HS/U: unsigned integer to float, widened**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=8\Rightarrow\mathrm{impl}(Zvfh))\ \land\ (\mathrm{SEW}=16\Rightarrow\mathrm{impl}(F))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{8,16,32\}\\
&\land\ \mathrm{LMUL}\le 4\\
&\land\ \mathrm{instr}=\mathrm{VFWCVT}.\mathrm{F}.\mathrm{XU}.\mathrm{V}
\end{aligned}
\longrightarrow
\{\, \mathrm{Im}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vd)=\mathrm{Out}_{2\mathrm{SEW},2\mathrm{LMUL}}(\mathrm{Im}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vd),\lambda i.\pi_1(\mathrm{i2f}^{\mathrm{u}}_{2\mathrm{SEW}\to2\mathrm{SEW},fcsr.frm}(\mathrm{el}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vs2,i))),vl,vstart,\mathrm{vm},\mathrm{V}_0,vta,vma),\ vstart=0,\ mstatus.VS=\mathrm{Dirty}(3),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\bigcup_{i\in\mathrm{Act}(vl,vstart,\mathrm{vm},\mathrm{V}_0)}\pi_2(\mathrm{i2f}^{\mathrm{u}}_{2\mathrm{SEW}\to2\mathrm{SEW},fcsr.frm}(\mathrm{el}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vs2,i))),\ \mathrm{exception}=\varnothing \,\}
$$

**(VFWCVT.F.X.3) H, VS/VU: unsigned integer to float, widened**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\bigr)\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=8\Rightarrow\mathrm{impl}(Zvfh))\ \land\ (\mathrm{SEW}=16\Rightarrow\mathrm{impl}(F))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{8,16,32\}\\
&\land\ \mathrm{LMUL}\le 4\\
&\land\ \mathrm{instr}=\mathrm{VFWCVT}.\mathrm{F}.\mathrm{XU}.\mathrm{V}
\end{aligned}
\longrightarrow
\{\, \mathrm{Im}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vd)=\mathrm{Out}_{2\mathrm{SEW},2\mathrm{LMUL}}(\mathrm{Im}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vd),\lambda i.\pi_1(\mathrm{i2f}^{\mathrm{u}}_{2\mathrm{SEW}\to2\mathrm{SEW},fcsr.frm}(\mathrm{el}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vs2,i))),vl,vstart,\mathrm{vm},\mathrm{V}_0,vta,vma),\ vstart=0,\ vsstatus.VS=\mathrm{Dirty}(3),\ sstatus.VS=\mathrm{Dirty}(3),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\bigcup_{i\in\mathrm{Act}(vl,vstart,\mathrm{vm},\mathrm{V}_0)}\pi_2(\mathrm{i2f}^{\mathrm{u}}_{2\mathrm{SEW}\to2\mathrm{SEW},fcsr.frm}(\mathrm{el}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vs2,i))),\ \mathrm{exception}=\varnothing \,\}
$$

**(VFWCVT.F.X.4) No H, M/S/U: signed integer to float, widened**

$$
\begin{aligned}
&\neg\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{S},\mathrm{U}\}\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=8\Rightarrow\mathrm{impl}(Zvfh))\ \land\ (\mathrm{SEW}=16\Rightarrow\mathrm{impl}(F))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{8,16,32\}\\
&\land\ \mathrm{LMUL}\le 4\\
&\land\ \mathrm{instr}=\mathrm{VFWCVT}.\mathrm{F}.\mathrm{X}.\mathrm{V}
\end{aligned}
\longrightarrow
\{\, \mathrm{Im}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vd)=\mathrm{Out}_{2\mathrm{SEW},2\mathrm{LMUL}}(\mathrm{Im}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vd),\lambda i.\pi_1(\mathrm{i2f}^{\mathrm{s}}_{2\mathrm{SEW}\to2\mathrm{SEW},fcsr.frm}(\mathrm{el}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vs2,i))),vl,vstart,\mathrm{vm},\mathrm{V}_0,vta,vma),\ vstart=0,\ mstatus.VS=\mathrm{Dirty}(3),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\bigcup_{i\in\mathrm{Act}(vl,vstart,\mathrm{vm},\mathrm{V}_0)}\pi_2(\mathrm{i2f}^{\mathrm{s}}_{2\mathrm{SEW}\to2\mathrm{SEW},fcsr.frm}(\mathrm{el}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vs2,i))),\ \mathrm{exception}=\varnothing \,\}
$$

**(VFWCVT.F.X.5) H, M/HS/U: signed integer to float, widened**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \mathrm{Priv}\in\{\mathrm{M},\mathrm{HS},\mathrm{U}\}\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=8\Rightarrow\mathrm{impl}(Zvfh))\ \land\ (\mathrm{SEW}=16\Rightarrow\mathrm{impl}(F))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{8,16,32\}\\
&\land\ \mathrm{LMUL}\le 4\\
&\land\ \mathrm{instr}=\mathrm{VFWCVT}.\mathrm{F}.\mathrm{X}.\mathrm{V}
\end{aligned}
\longrightarrow
\{\, \mathrm{Im}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vd)=\mathrm{Out}_{2\mathrm{SEW},2\mathrm{LMUL}}(\mathrm{Im}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vd),\lambda i.\pi_1(\mathrm{i2f}^{\mathrm{s}}_{2\mathrm{SEW}\to2\mathrm{SEW},fcsr.frm}(\mathrm{el}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vs2,i))),vl,vstart,\mathrm{vm},\mathrm{V}_0,vta,vma),\ vstart=0,\ mstatus.VS=\mathrm{Dirty}(3),\ mstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\bigcup_{i\in\mathrm{Act}(vl,vstart,\mathrm{vm},\mathrm{V}_0)}\pi_2(\mathrm{i2f}^{\mathrm{s}}_{2\mathrm{SEW}\to2\mathrm{SEW},fcsr.frm}(\mathrm{el}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vs2,i))),\ \mathrm{exception}=\varnothing \,\}
$$

**(VFWCVT.F.X.6) H, VS/VU: signed integer to float, widened**

$$
\begin{aligned}
&\mathrm{impl}(H)\ \land\ \bigl(\mathrm{Priv}\in\{\mathrm{VS},\mathrm{VU}\}\ \land\ vsstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ vsstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\ \land\ sstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\bigr)\\
&\land\ \bigl(\mathrm{impl}(V)\ \land\ (\mathrm{SEW}=8\Rightarrow\mathrm{impl}(Zvfh))\ \land\ (\mathrm{SEW}=16\Rightarrow\mathrm{impl}(F))\ \land\ (\mathrm{SEW}=32\Rightarrow\mathrm{impl}(D))\bigr)\\
&\land\ mstatus.VS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ mstatus.FS\in\{\mathrm{Initial}(1),\mathrm{Clean}(2),\mathrm{Dirty}(3)\}\\
&\land\ fcsr.frm\in\{\mathrm{RNE}(0),\mathrm{RTZ}(1),\mathrm{RDN}(2),\mathrm{RUP}(3),\mathrm{RMM}(4)\}\\
&\land\ \mathrm{SEW}\in\{8,16,32\}\\
&\land\ \mathrm{LMUL}\le 4\\
&\land\ \mathrm{instr}=\mathrm{VFWCVT}.\mathrm{F}.\mathrm{X}.\mathrm{V}
\end{aligned}
\longrightarrow
\{\, \mathrm{Im}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vd)=\mathrm{Out}_{2\mathrm{SEW},2\mathrm{LMUL}}(\mathrm{Im}^{2\mathrm{SEW}}_{2\mathrm{LMUL}}(vd),\lambda i.\pi_1(\mathrm{i2f}^{\mathrm{s}}_{2\mathrm{SEW}\to2\mathrm{SEW},fcsr.frm}(\mathrm{el}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vs2,i))),vl,vstart,\mathrm{vm},\mathrm{V}_0,vta,vma),\ vstart=0,\ vsstatus.VS=\mathrm{Dirty}(3),\ sstatus.VS=\mathrm{Dirty}(3),\ vsstatus.FS=\mathrm{Dirty}(3),\ sstatus.FS=\mathrm{Dirty}(3),\ \mathrm{fcsr.fflags}\mathrel{|}=\bigcup_{i\in\mathrm{Act}(vl,vstart,\mathrm{vm},\mathrm{V}_0)}\pi_2(\mathrm{i2f}^{\mathrm{s}}_{2\mathrm{SEW}\to2\mathrm{SEW},fcsr.frm}(\mathrm{el}^{\mathrm{SEW}}_{\mathrm{LMUL}}(vs2,i))),\ \mathrm{exception}=\varnothing \,\}
$$
