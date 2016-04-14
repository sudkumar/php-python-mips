	.text
	.globl main

main:

B0:
	li $8, 2016
	li $9, 0
	li $10, 400
	rem $11, $8, $10
	li $12, 0
	sw $8, g_t1
	sw $8, g__a
	sw $9, g_t2
	sw $9, g__isLeap
	sw $10, g_t3
	sw $11, g_t4
	sw $12, g_t5
	beq $11, $12, B2
B1:
	j B3
B2:
	li $13, 1
	sw $13, g_t6
	sw $13, g__isLeap
	j B10
B3:
	li $14, 100
	lw $15, g__a
	rem $24, $15, $14
	li $25, 0
	sw $14, g_t7
	sw $24, g_t8
	sw $25, g_t9
	beq $24, $25, B5
B4:
	j B6
B5:
	li $16, 0
	sw $16, g_t10
	sw $16, g__isLeap
	j B10
B6:
	li $17, 4
	lw $18, g__a
	rem $19, $18, $17
	li $20, 0
	sw $17, g_t11
	sw $19, g_t12
	sw $20, g_t13
	beq $19, $20, B8
B7:
	j B9
B8:
	li $21, 1
	sw $21, g_t14
	sw $21, g__isLeap
	j B10
B9:
	li $22, 0
	sw $22, g_t15
	sw $22, g__isLeap
B10:
	li $23, 0
	lw $4, g__isLeap
	sw $23, g_t16
	beq $4, $23, B12
B11:
	j B13
B12:
	la $5, str_224e6f2e2e22
	sw $5, g_t17
	j B14
B13:
	la $6, str_225965732e22
	sw $6, g_t18
	j B15
B14:
	lw $7, g_t17
	sw $7, g_t19
	j B16
B15:
	lw $8, g_t18
	sw $8, g_t19
B16:
	lw $9, g_t19
	sw $9, g__c
	addi $sp, -4
	sw $9, 0($sp)
	jal _printStr_
	addi  $sp, 4
B17:
	la $10, str_225c6e5c6e22
	sw $10, g_t20
	addi $sp, -4
	sw $10, 0($sp)
	jal _printStr_
	addi  $sp, 4
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
	lw $a0, 0($sp)
	li $v0, 4
	syscall
	jr $ra
_readStr_:
	li $v0, 8
	syscall
	jr $ra

	.data
g__c:	.space	4
g__a:	.space	4
g_t14:	.space	4
g_t15:	.space	4
g_t16:	.space	4
g_t17:	.space	4
g_t10:	.space	4
g_t11:	.space	4
g_t12:	.space	4
g_t13:	.space	4
g_t18:	.space	4
g_t19:	.space	4
g__isLeap:	.space	4
g_t8:	.space	4
g_t9:	.space	4
g_t6:	.space	4
g_t7:	.space	4
g_t4:	.space	4
g_t5:	.space	4
g_t2:	.space	4
g_t3:	.space	4
g_t1:	.space	4
g_t20:	.space	4
str_225c6e5c6e22:	.asciiz	"\n\n"
str_225965732e22:	.asciiz	"Yes."
str_224e6f2e2e22:	.asciiz	"No.."
