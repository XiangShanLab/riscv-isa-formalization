OUTPUT_ARCH(riscv)
ENTRY(_start)
SECTIONS {
 . = 0x80000000;
 .text : { *(.text.init) *(.text*) }
 . = ALIGN(16);
 .rodata : { *(.rodata*) }
 . = ALIGN(16);
 .data : { *(.data*) }
 . = ALIGN(64);
 .tohost : { *(.tohost) }
 . = ALIGN(64);
 .signature : { *(.signature) }
 .bss : { *(.bss*) }
 /DISCARD/ : { *(.comment) *(.note*) *(.eh_frame*) *(.riscv.attributes) }
}
