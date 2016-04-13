	.text
	.globl main

main:

B0:
	li $8, 10
	sw $8, g_t1
	sw $8, g__y
	j B6
B1:
	
B2:
	li $9, 1
	sw $9, g_t3
	sw $9, g__y
	j B9
B3:
	
B4:
	li $10, 2
	sw $10, g_t5
	sw $10, g__y
	j B9
B5:
	li $11, 3
	sw $11, g_t6
	sw $11, g__y
	j B9
B6:
	lw $12, g__y
	lw $13, g_t2
	beq $12, $13, B2
B7:
	lw $14, g__y
	lw $15, g_t4
	beq $14, $15, B4
B8:
	j B5
B9:
	li $24, 10
	sw $24, g_t7
	sw $24, g__y
	j _exit_
_readInt_:
	li $v0, 5
	syscall
	jr $ra
_exit_:
	li $v0, 10
	syscall
_closeFile_:
	li $v0, 16
	syscall
_malloc_:
	li $v0, 9
	syscall
	jr $ra
_readFile_:
	li $v0, 14
	syscall
_writeFile_:
	li $v0, 15
	syscall
_open_:
	li $v0, 13
	syscall
_printInt_:
	lw $a0, 0($sp)
	li $v0, 1
	syscall
	jr $ra
_printStr_:
	li $v0, 4
	syscall
	jr $ra
_readStr_:
	li $v0, 8
	syscall
	jr $ra

	.data
g_t6:	.space	4
g_t7:	.space	4
g_t4:	.space	4
g_t5:	.space	4
g_t2:	.space	4
g_t3:	.space	4
g_t1:	.space	4
g__y:	.space	4
