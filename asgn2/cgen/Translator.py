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
				mipsInst = "mult"
			else:
				mipsInst = "div"
		mipsCode = "\t" +  mipsInst + " " + registers[0] + ", " + registers[1] + ", " + registers[2] + "\n"		
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
				mipsCode = "\t" + mipsInst + " " + operands[0] + ", " + label + "\n" 	
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
				mipsCode = "\t" + mipsInst + " " + operands[0] + ", "+ operands[2] + ", " + label + "\n" 	 	
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
		Take type of print statement and return mips assembly code for it.

		Takes two parameters:
		(i). type: 'integer', 'float','double', 'string'
		(ii). address: for string address in data section else register i.e $t0
	"""
	def getInstPrint(self,type, address):
		mipsCode = ""		 
		if type == "integer" :
			mipsCode = "\t" + "li $v0, 1" + "\n\t" + "move $a0, " + address + "\n\t" + "syscall" + "\n"					 

		elif type == "float" :
			mipsCode = "\t" + "li $v0, 2" + "\n\t" + "mov.s $f12, " + address + "\n\t" + "syscall" + "\n"					 		 
		# elif type == "double" : 

		elif type == "string" :
			mipsCode = "\t" + "li $v0, 4" + "\n\t" + "la $a0, " + address + "\n\t" + "syscall" + "\n"
		
		return mipsCode

	"""
		Mips code for exit of a program
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

	print translator.getInstUncondJump('L2')
	print translator.getInstUncondJump('')

	print translator.getInstPrint('integer', 't2')
	print translator.getInstPrint('string', 'name')
	print translator.getInstPrint('float', 'f1')

	print translator.getInstExit()