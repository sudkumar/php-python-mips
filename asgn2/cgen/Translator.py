from LineParser import LineParser
from NextUseLive import NextUseLive

class Translator():
	def __init__(self):
		self.Instr = []

#  assgn + - * /
#  = ==> load store 

	def getInstOp(self,op,registers):
		mipsInst = ""
		mipsCode = ""
		if op == "+" or op == "-" :
			try:
				operand = int(registers[2])
				if op == "+": 
					mipsInst = "addi"
				else:
					mipsInst = "addi" # operand need to set equal to it -ve value
			except Exception, e:
				#raise error
				if e:
					if op == "+": 
						mipsInst = "add"
					else:
						mipsInst = "sub"

		elif op == "*" or op== "/":
			if op == "*"  :
				mipsInst = "mul"
			else:
				mipsInst = "div"
		mipsCode =   mipsInst + " " + registers[0] + ", " + registers[1] + ", " + registers[2]		
		return mipsCode

	"""
		call methods: getInstLoad([$t1,$t0]) or getInstLoad([$t1, 5])

		not complete lw remaining
	"""	
	def getInstLoad(self,registers):
		mipsInst = ""
		dest = registers[0]
		src = registers[1]

		try:
			integer = int(src)
			mipsInst = "li"
		except Exception, e:
			if e:
				mipsInst = "la"
		mipsCode = "\t" + mipsInst + " " + registers[0] + ", " + registers[1]
		return mipsCode
	"""
		call methods: getInstStore([src,dest])

		not complete
	"""	
	def getInstStore(self,registers):
		mipsInst = "sw"
		src = registers[0]
		dest = registers[1]
		mipsCode = "\t" + mipsInst + " "+ src + ", " + dest 
		return mipsCode

	"""
		call for conditional branch jump instructions.
		arguments given like this: (['t1','>','t2'],Label1) or (['t1','>','0'],Label1)

		Note: no mips instruction for ($t1 >= 0) and ($t1 < 0)
	"""	
	# caall method: translator.getInstCondJump(['t1','<','t2'],'L1')		
	def getInstCondJump(self, operands ,label):
		mipsInst = ""
		mipsCode = ""
		try:
			# case when compared with 0
			zero = int(operands[2])
			if operands[1] == ">":
			 	mipsInst = "bgtz"
			elif operands[1] == "<=":
			 	mipsInst = "blez"
			elif operands[1] == "==":
			 	mipsInst = "beqz"
			elif operands[1] == "!=":
			 	mipsInst = "bnez"
			if mipsInst : 
				mipsCode = mipsInst + " " + operands[0] + ", " + label 	
		except Exception, e:
			if operands[1] == ">":
			 	mipsInst = "bgt"
			elif operands[1] == "<":
			 	mipsInst = "blt"
			elif operands[1] == ">=":
			 	mipsInst = "bge"
			elif operands[1] == "<=":
			 	mipsInst = "ble"
 			elif operands[1] == "==":
			 	mipsInst = "beq"
			elif operands[1] == "!=":
			 	mipsInst = "bne"
			if mipsInst:
				mipsCode = mipsInst + " " + operands[0] + ", "+ operands[2] + ", " + label 	 	
		return mipsCode	

	"""
		Unconditional Jumps: two types 
		(i). jump to an address (label)
		(ii). jump and return

		not complete
	"""
	# for jumping to a label mean jal inst else no label => jump to $ra variable
	def getInstUncondJump(self,label):
		mipsInst = ""
		if label != "":
			mipsInst = "jal"
			mipsCode = "\t" + mipsInst + " " + label
		elif label == "":
			mipsInst = "jr" 
			mipsCode = "\t" + mipsInst + " $ra"
		return mipsCode	


	"""
		Print functions which return mips assembly code for it.		
	"""
	# print function which gives mips code for integers
	# input: a reg in which value is present
	def getInstPrintInt(self,variable):
		mipsCode =  "li $v0, 1" + "\n\t" + "move $a0, " + variable + "\n\t" + "syscall" 					 
		return mipsCode

	# print function which gives mips code for floats  
	# input: A reg in which value is present
	def getInstPrintFloat(self,variable):
		mipsCode =  "li $v0, 2" + "\n\t" + "mov.s $f12, " + variable + "\n\t" + "syscall"					 
		return mipsCode

	# print function which gives mips code for string  
	# input: an address in data section.
	def getInstPrintStr(self,address):
		mipsCode = "li $v0, 4" + "\n\t" + "la $a0, " + address + "\n\t" + "syscall"				 
		return mipsCode 

	"""
		Read input functions which return mips assembly code for it.		
	"""

	# read integers from console
	# input: an register in which we want to read the input
	def getInstReadInt(self, reg):
		mipsCode =  "li $v0, 5" + "\n\t" + "syscall" + "\n\t" + "move " + reg + ", $v0" 					 
		return mipsCode

	# read floats from console  
	# input: an register in which we want to read the input
	# not sure working
	def getInstReadFloat(self,reg):
		mipsCode =  "li $v0, 6" + "\n\t" + "syscall" + "\n\t" + "swc1 " + reg + ", $v0" 					 
		return mipsCode

	# read string from console 
	# input: an address in data section and amount of size, ex.   getInstReadStr('inputStr',35)
	# 
	def getInstReadStr(self,address,sizeReg):
		mipsCode = "li $v0, 8" + "\n\t" + "la $a0, "+ address + "\n\t"
		mipsCode += "move $a1, "+ sizeReg + "\n\t" # if size is integer
		mipsCode += "syscall"				 
		return mipsCode 


	"""
		Mips code for allocating memory
	"""
	# assuming no of bytes is in a register
	# address in $v0, amount in $a0
	def getInstMalloc(self,noOfBytes):
		mipsCode = "move $a0, "+ str(noOfBytes) + "\n\t"
		mipsCode += "li $v0, 9" + "\n\t" + "syscall" + "\n\t" 
		return mipsCode


	"""
		MIPS library support 	

		suppose we have file name in our data section with same address name i.e
		.data fInput: .asciiz "filename.ir"
	"""	

	"""
		Function to open file for read
		takes two parameter: 
		1. filename referenced in data section
		2. reg: register in which file descriptor will be stored
	"""
	def openFileForRead(self,filename,fileDespReg):
		mipsCode = "\t" + "li $v0, 13" + "\n\t"
		mipsCode += "la $a0, " + filename + "\n\t"
		mipsCode += "li $a1, 0" + "\n\t"	# open for reading
		mipsCode += "li $a2, 0" + "\n\t"	# mode is none
		mipsCode += "syscall" + "\n\t"
		mipsCode += "move " + fileDespReg + ", $v0" + "\n" # saving file descriptor
		return mipsCode

	"""
		Function to read from file
		takes 3 parameters:
		1. register where file descriptor is stored
		2. buffer name where we will read input
		3. reg where size of buffer is stored

		strName contains the string, by calling loadByte function we can use each character if we want.
	"""
	def readFile(self,fileDespReg,strName,sizeReg):	
		mipsCode = "\t" + "li $v0, 14" + "\n\t"
		mipsCode += "move $a0, " + fileDespReg + "\n\t"
		mipsCode += "la $a1, " + strName + "\n\t"	# address of buffer to which to read
		mipsCode += "move $a2, " + sizeReg + "\n\t"	# buffer length
		mipsCode += "syscall" + "\n"	# read from file
		return mipsCode

	"""
		Function to open file for write
		takes filename referenced in data section as parameter and a reg where descriptor will be stored
	"""
	def openFileForWrite(self,filename,fileDespReg):
		mipsCode = "\t" +"li $v0, 13" + "\n\t"
		mipsCode += "la $a0, " + filename + "\n\t"
		mipsCode += "li $a1, 1" + "\n\t"	# open for writing
		mipsCode += "li $a2, 0" + "\n\t"	# mode is none
		mipsCode += "syscall" + "\n\t"		# file descriptor is in $v0
		mipsCode += "move " + fileDespReg + ", $v0" + "\n"
		return mipsCode

 
	"""
		Function to write in file
		takes 3 parameter:
		1. register where file descriptor is stored
		2. buffer name where we will read input
		3. reg where size of buffer is stored
		suppose we writing a string which address is in our data section   
	"""
	def writeFile(self,fileDespReg,strName,sizeReg ):
		mipsCode = "\t" + "move $a0, "+fileDespReg + "\n"	# load file descriptor for syscall
		mipsCode += "li $v0, 15" + "\n\t"	 
		mipsCode += "la $a1, " + strName + "\n\t"	# address of buffer to which to read
		mipsCode += "move $a2, " + sizeReg + "\n\t"	# buffer length
		mipsCode += "syscall" + "\n"	# write to file
		return mipsCode


	"""
		Function to load a byte from stored string buffer at position index into dest register
	"""
	def loadByte(self,destReg,strName,index):
		mipsCode = "\t" + "lb " + destReg + ", " + strName + "(" + index + ")"
		return mipsCode

	"""
		Function to close a file after each operation is done
	"""	
	def CloseFile(self,fileDespReg):
		mipsCode = "\t" + "li $v0, 16" + "\n\t"
		mipsCode += "move $a0, " + fileDespReg + "\n\t"
		mipsCode += "syscall" + "\n"
		return mipsCode

	"""
		Mips code for exit state of a program
	"""	
	def getInstExit(self):
		mipsCode = 	"\t" + "li $v0, 10" + "\n\t" + "syscall"
		return mipsCode

if __name__ == '__main__':

	translator = Translator()
	print translator.getInstOp('+',['t1','t2','2'])
	print translator.getInstOp('*',['t1','t1','t2'])

	print translator.getInstLoad(['t1','5'])
	print translator.getInstLoad(['a0','t2'])
	print translator.getInstStore(['a1','t2'])

	print translator.getInstCondJump(['t1','<','t2'],'L1')
	print translator.getInstCondJump(['t1','<=','t2'],'L2')
	print translator.getInstCondJump(['t1','>','t2'],'L1')
	print translator.getInstCondJump(['t1','>=','t2'],'L2')
	print translator.getInstCondJump(['t1','==','t2'],'L2')
	print translator.getInstCondJump(['t1','!=','t2'],'L2')

	print translator.getInstCondJump(['t1','<','0'],'L1')
	print translator.getInstCondJump(['t1','<=','0'],'L2')
	print translator.getInstCondJump(['t1','>','0'],'L1')
	print translator.getInstCondJump(['t1','>=','0'],'L2')
	print translator.getInstCondJump(['t1','==','0'],'L2')
	print translator.getInstCondJump(['t1','!=','0'],'L2')

	# print translator.getInstUncondJump('L2')
	# print translator.getInstUncondJump('')

	print translator.getInstPrintInt('$t0')
	print translator.getInstPrintFloat('$t0')
	print translator.getInstPrintStr('str_name')

	print translator.getInstReadInt('$t0')
	print translator.getInstReadFloat('$t0')
	print translator.getInstReadStr('input_str', "$t6")

	print translator.getInstMalloc('$t1')
	
	print translator.getInstExit()


	print translator.openFileForRead("fInput",'$s6')
	print "\n"
	print translator.readFile('$s6',"buffer","$t6")	# t6 contains buffer size

	print translator.openFileForWrite("fOut","$t6")
	print translator.writeFile("$t6","text", "$t6" )	# t6 contains buffer size
	print "\n"	
	print translator.CloseFile("$t6")