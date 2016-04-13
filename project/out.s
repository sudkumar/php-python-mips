	.text
	.globl main

main:

B0:
	li $8, 10
	li $9, 20
	add $10, $8, $9
	li $11, 12342340
	add $12, $10, $11
	li $13, 112
	li $14, 1
	add $15, $13, $14
	li $24, 1
	add $25, $13, $24
	li $16, 1
	add $17, $15, $16
	li $18, 25
	sw $8, g_t1
	sw $9, g_t2
	sw $10, g_t3
	sw $10, g__c
	sw $11, g_t4
	sw $12, g_t5
	sw $12, g__d
	sw $13, g_t6
	sw $17, g__a
	sw $14, g_t7
	sw $15, g_t8
	sw $15, g__b
	sw $24, g_t9
	sw $25, g_t10
	sw $16, g_t11
	sw $17, g_t12
	sw $18, g_t13
	bgt $17, $18, B2
B1:
	j B3
B2:
	li $19, 10
	lw $20, g__a
	sub $21, $20, $19
	sw $19, g_t14
	sw $21, g_t15
	j B4
B3:
	li $22, 5
	lw $23, g__b
	add $4, $23, $22
	sw $22, g_t16
	sw $4, g_t17
	j B5
B4:
	lw $5, g_t15
	sw $5, g_t18
	j B6
B5:
	lw $6, g_t17
	sw $6, g_t18
B6:
	lw $7, g_t18
	li $8, 3
	sw $7, g__c
	sw $8, g_t19
	beq $7, $8, B10
B7:
	j B8
B8:
	li $9, 9
	lw $10, g__c
	sw $9, g_t20
	beq $10, $9, B10
B9:
	j B11
B10:
	li $11, 1
	sw $11, g_t21
	sw $11, g__c
	j B14
B11:
	li $12, 0
	lw $13, g__c
	sw $12, g_t22
	bgt $13, $12, B13
B12:
	j B14
B13:
	li $17, 1
	sw $17, g_t23
	sw $17, g__c
B14:
	li $14, 0
	lw $15, g__c
	sw $14, g_t24
	bgt $15, $14, B16
B15:
	j B17
B16:
	lw $24, g__c
	li $25, 1
	sub $24, $24, $25
	sw $24, g__c
	j B14
B17:
	li $16, 0
	sw $16, g_t25
	sw $16, g__c
B18:
	li $18, 10
	lw $19, g__c
	sw $18, g_t26
	blt $19, $18, B21
B19:
	j B22
B20:
	lw $21, g__c
	addi $20, $21, 1
	sw $21, g_t27
	sw $20, g__c
	j B18
B21:
	li $22, 1
	lw $4, g__c
	add $4, $4, $22
	sw $22, g_t28
	sw $4, g__c
	j B20
B22:
	li $23, 10
	li $5, 1
	add $6, $23, $5
	mul $7, $23, $6
	sw $23, g_t29
	sw $23, g__d
	sw $5, g_t30
	sw $6, g_t31
	sw $6, g__e
	sw $7, g_t32
	sw $7, g__f
	j B24
B23:
	addi $sp, -8
	sw $ra, 0($sp)
	sw $fp, 4($sp)
	move $fp, $sp
	addi $sp, -12
	li $8, 2
	lw $9, g__d
	add $10, $9, $8
	sw $8, 0($sp)
	sw $10, 4($sp)
	sw $10, 8($sp)
	move $v0, $10
	move $sp, $fp
	lw $ra, 0($sp)
	lw $fp, 4($sp)
	addi $sp, $sp, 8
	jr $ra
B24:
	j B27
B25:
	addi $sp, -8
	sw $ra, 0($sp)
	sw $fp, 4($sp)
	move $fp, $sp
	addi $sp, -12
	li $11, 3
	jal B23
	move $12, $v0
	sw $11, 0($sp)
	sw $11, 4($sp)
	sw $12, 8($sp)
B26:
	lw $13, 8($sp)
	move $v0, $13
	move $sp, $fp
	lw $ra, 0($sp)
	lw $fp, 4($sp)
	addi $sp, $sp, 8
	jr $ra
B27:
	jal B23
	move $17, $v0
	sw $17, g_t37
B28:
	lw $14, g_t37
	jal B25
	move $15, $v0
	sw $14, g__f
	sw $15, g_t38
B29:
	lw $25, g_t38
	addi $sp, -4
	sw $25, 0($sp)
	jal _printInt_
	addi  $sp, 4
	sw $25, g__e
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
g__f:	.space	4
g__d:	.space	4
g__e:	.space	4
g__b:	.space	4
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
g_t37:	.space	4
g_t18:	.space	4
g_t19:	.space	4
g_t30:	.space	4
g_t31:	.space	4
g_t38:	.space	4
g_t32:	.space	4
g_t8:	.space	4
g_t9:	.space	4
g_t6:	.space	4
g_t7:	.space	4
g_t4:	.space	4
g_t5:	.space	4
g_t2:	.space	4
g_t3:	.space	4
g_t1:	.space	4
g_t29:	.space	4
g_t28:	.space	4
g_t21:	.space	4
g_t20:	.space	4
g_t23:	.space	4
g_t22:	.space	4
g_t25:	.space	4
g_t24:	.space	4
g_t27:	.space	4
g_t26:	.space	4
