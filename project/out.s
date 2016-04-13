t1 = 10
t2 = 20
t3 = t1 + t2
$c = t3
t4 = 12342340
t5 = $c + t4
$d = t5
t6 = 112
$a = t6
t7 = 1
t8 = $a + t7
$b = t8
t9 = 1
t10 = $a + t9
$a = t10
t11 = 1
t12 = $b + t11
$a = t12
t13 = 25
if $a > t13 goto 21
goto 24
t14 = 10
t15 = $a - t14
goto 27
t16 = 5
t17 = $b + t16
goto 29
t18 = t15
goto 30
t18 = t17
$c = t18
t19 = 3
if $c == t19 goto 37
goto 34
t20 = 9
if $c == t20 goto 37
goto 40
t21 = 1
$c = t21
goto 45
t22 = 0
if $c > t22 goto 43
goto 45
t23 = 1
$c = t23
t24 = 0
if $c > t24 goto 48
goto 50
$c = $c - 1
goto 45
t25 = 0
$c = t25
t26 = 10
if $c < t26 goto 58
goto 61
t27 = $c
$c = $c + 1
goto 52
t28 = 1
$c = $c + t28
goto 55
t29 = 10
$d = t29
t30 = 1
t31 = $d + t30
$e = t31
t32 = $d * $e
$f = t32
goto 72
t33 = 11111
$c = t33
ret $c
goto 80
t34 = 11113
$d = t34
t35 = 1
$d = $d + t35
call 73 0 t36
$d = t36
ret $d
call 69 0 t37
$f = t37
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
	j B11
B9:
	li $9, 1
	sw $9, g_t21
	sw $9, g__c
	j B14
B10:
	j B14
B11:
	li $10, 1
	sw $10, g_t23
	sw $10, g__c
B12:
	li $11, 0
	lw $12, g__c
	sw $11, g_t24
	bgt $12, $11, B16
B13:
	j B17
B14:
	lw $13, g__c
	li $17, 1
	sub $13, $13, $17
	sw $13, g__c
	j B14
B15:
	li $14, 0
	sw $14, g_t25
	sw $14, g__c
B16:
	li $15, 10
	lw $24, g__c
	sw $15, g_t26
	blt $24, $15, B21
B17:
	j B22
B18:
	lw $25, g__c
	addi $16, $25, 1
	sw $25, g_t27
	sw $16, g__c
	j B18
B19:
	li $18, 1
	lw $19, g__c
	add $19, $19, $18
	sw $18, g_t28
	sw $19, g__c
	j B20
B20:
	li $21, 10
	li $20, 1
	add $22, $21, $20
	mul $4, $21, $22
	sw $21, g_t29
	sw $21, g__d
	sw $20, g_t30
	sw $22, g_t31
	sw $22, g__e
	sw $4, g_t32
	sw $4, g__f
	j B24
B21:
	li $23, 11111
	sw $23, 0($sp)
	sw $23, 4($sp)
	move $v0, $23
	move $sp, $fp
	lw $ra, 0($sp)
	lw $fp, 4($sp)
	addi $sp, $sp, 8
	jr $ra
B22:
	j B27
B23:
	addi $sp, -8
	sw $ra, 0($sp)
	sw $fp, 4($sp)
	move $fp, $sp
	addi $sp, -8
	lw $5, 12($sp)
	sw $5, 4($sp)
	move $v0, $5
	move $sp, $fp
	lw $ra, 0($sp)
	lw $fp, 4($sp)
	addi $sp, $sp, 8
	jr $ra
B24:
	lw $6, g_t37
	sw $6, g__f
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
