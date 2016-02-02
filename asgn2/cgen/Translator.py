from LineParser import LineParser
from NextUseLive import NextUseLive

class Translator():
	def __init__(self):
		self.Instr = []
	# nextUseLive = NextUseLive(basicBlock)

	# for line in basicBlock:
	# 	mipsCode = []
	# 	lineParser = LineParser(line)
	# 	registers = getReg(lineParser)
	# 	mipsInst =  getInst(lineParser)
	# 	mipsCode.append(mipsInst)
	# 	for register in registers:
	# 		mipsCode.append(register)
	# 	print mipsCode
	# 	# print Instr.append(mipsInst).append(registers)
	# return "sah" 

#  assgn + - * /
#  = ==> load store 

	def getInstOp(self,op,registers):
		mipsInst = "";
		if op == "+" or op == "-" :
			try:
				operand = int(registers[2])
				if op == "+": 
					mipsInst = "addi"
				else:
					mipsInst = "subi"
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
		return mipsInst

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
		return mipsInst

	def getInstStore(self,registers):
		mipsInst = "sw"
		src = registers[0]
		dest = registers[1]
		return mipsInst

	def getInstJump(self, label):
		


	def getReg(self,registers):
		regs = []
		for reg in registers:	
			if not reg in regs:
				regs.append('$'+reg)
		return regs

if __name__ == '__main__':

	translator = Translator()
	print translator.getInstOp('+',['t1','t2','2'])
	print translator.getInstLoad(['v0','t2']);
	print translator.getInstStore(['v0','t2']);
