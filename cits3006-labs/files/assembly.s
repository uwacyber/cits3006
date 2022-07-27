	.arch armv8-a
	.file	"file.c"
	.text
	.align	2
	.global	factorial
	.type	factorial, %function
factorial:
.LFB0:
	.cfi_startproc
	str	x19, [sp, -32]!
	.cfi_def_cfa_offset 32
	.cfi_offset 19, -32
	str	w0, [sp, 28]
	mov	w19, 1
	b	.L2
.L3:
	ldr	w0, [sp, 28]
	sub	w1, w0, #1
	str	w1, [sp, 28]
	mul	w19, w19, w0
.L2:
	ldr	w0, [sp, 28]
	cmp	w0, 0
	bne	.L3
	mov	w0, w19
	ldr	x19, [sp], 32
	.cfi_restore 19
	.cfi_def_cfa_offset 0
	ret
	.cfi_endproc
.LFE0:
	.size	factorial, .-factorial
	.ident	"GCC: (Debian 11.3.0-1) 11.3.0"
	.section	.note.GNU-stack,"",@progbits
