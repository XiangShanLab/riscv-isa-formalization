# {{MNEMONIC}} — {{ONE_LINE_DESCRIPTION}}

<!-- TEMPLATE: copy to specs/{{INSTANCE_SLUG}}/instructions/{{mnemonic}}.md.
     English only. Result formulas only; symbols and shared definitions live in the
     instance README. Replace every {{...}} placeholder and delete this comment. -->

{{Semantics paragraph: what the instruction computes, which formats and operand forms it has,
and which extension condition enables it.}}

The `exception` field of every block below lists only the exceptions this instruction itself can
raise, and reads `\mathrm{exception}=\varnothing` when it raises none; instruction-fetch outcomes
depend only on the fetch address and are stated once in the instance README.

**({{MNEMONIC}}.0) Extension unavailable or execution configuration not permitted → only IllegalInstruction(2)**

$$
\begin{aligned}
&\neg\mathrm{impl}({{EXT}})\ \lor\ ({{UNSUPPORTED_CONFIGURATION}})\\
&\land\ (\mathrm{instr}={{MNEMONIC}})
\end{aligned}
\longrightarrow
\{\, \mathrm{exception}=\{\mathrm{IllegalInstruction}(2)\} \,\}
$$

**({{MNEMONIC}}.1) {{RESULT_CATEGORY}}**

$$
\begin{aligned}
&{{PRIVILEGE_CONFIGURATION}}\ \land\ \mathrm{impl}({{EXT}})\\
&\land\ ({{STATE_CONDITION}})\\
&\land\ ({{OPERAND_CONDITION}})\\
&\land\ (\mathrm{instr}={{MNEMONIC}})
\end{aligned}
\longrightarrow
\{\, {{DESTINATION}}={{RESULT}},\ \mathrm{exception}=\varnothing \,\}
$$

<!-- Add further result blocks in evaluation order, numbered {{MNEMONIC}}.2, .3, ...
     Later blocks do not repeat conditions already excluded by earlier ones.
     If the result depends on which of several sources is exceptional, split the block
     by source rather than merging the cases into one disjunction. -->
