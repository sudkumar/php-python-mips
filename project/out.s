	.text
	.globl main

main:

B0:
	li $8, 7
	sw $8, g_t1
	sw $8, g__n
	j B13
B1:
	addi $sp, -8
	sw $ra, 0($sp)
	sw $fp, 4($sp)
	move $fp, $sp
	addi $sp, -52
	li $9, 0
	lw $10, 8($fp)
	sw $9, 0($sp)
	beq $10, $9, B3
B2:
	j B5
B3:
	li $11, 0
	sw $11, 4($sp)
	move $v0, $11
	move $sp, $fp
	lw $ra, 0($sp)
	lw $fp, 4($sp)
	addi $sp, $sp, 8
	jr $ra
B4:
	
B5:
	li $12, 1
	lw $13, 8($fp)
	sw $12, 8($sp)
	beq $13, $12, B7
B6:
	j B9
B7:
	li $14, 1
	sw $14, 12($sp)
	move $v0, $14
	move $sp, $fp
	lw $ra, 0($sp)
	lw $fp, 4($sp)
	addi $sp, $sp, 8
	jr $ra
B8:
	
B9:
	li $15, 1
	lw $24, 8($fp)
	sub $24, $24, $15
	sw $15, 16($sp)
	sw $24, 20($sp)
	sw $24, 8($fp)
	sw $25, 24($sp)
	addi $sp, -4
	sw $24, 0($sp)
	jal B1
	move $25, $v0
	addi  $sp, 4
	sw $25, 24($sp)
B10:
	lw $16, 24($sp)
	li $17, 1
	lw $18, 8($fp)
	sub $18, $18, $17
	sw $16, 28($sp)
	sw $17, 32($sp)
	sw $18, 36($sp)
	sw $18, 8($fp)
	sw $19, 40($sp)
	addi $sp, -4
	sw $18, 0($sp)
	jal B1
	move $19, $v0
	addi  $sp, 4
	sw $19, 40($sp)
B11:
	lw $20, 40($sp)
	lw $21, 28($sp)
	add $22, $21, $20
	sw $20, 44($sp)
	sw $22, 48($sp)
	move $v0, $22
	move $sp, $fp
	lw $ra, 0($sp)
	lw $fp, 4($sp)
	addi $sp, $sp, 8
	jr $ra
B12:
	
B13:
	lw $23, g__n
	sw $4, g_t13
	addi $sp, -4
	sw $23, 0($sp)
	jal B1
	move $4, $v0
	addi  $sp, 4
	sw $4, g_t13
B14:
	lw $5, g_t13
	sw $5, g__c
	addi $sp, -4
	sw $5, 0($sp)
	jal _printInt_
	addi  $sp, 4
