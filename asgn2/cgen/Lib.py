#!/usr/bin/python

from Config import LibFns

# The library file
class Lib():

    def genFns(self):
        instrs = {}
        instrs[LibFns["printInt"]]= self.printInt()
        instrs[LibFns["printStr"]]= self.printStr()
        instrs[LibFns["readStr"]]= self.readInt()
        instrs[LibFns["readInt"]]= self.readStr()
        instrs[LibFns["malloc"]]= self.malloc()
        instrs[LibFns["exit"]]= self.exit()
        return instrs

    def printInt(self):
        instr = []
        instr.append("li $v0, 1")
        instr.append("syscall")
        instr.append("jr $ra")
        return instr

    def printStr(self):
        instr = []
        instr.append("li $v0, 4")
        instr.append("syscall")
        instr.append("jr $ra")
        return instr

    def readInt(self):
        instr = []
        instr.append("li $v0, 5")
        instr.append("syscall")
        instr.append("jr $ra")
        return instr

    def readStr(self):
        instr = []
        instr.append("li $v0, 8")
        instr.append("syscall")
        instr.append("jr $ra")
        return instr

    def malloc(self):
        instr = []
        instr.append("li $v0, 9")
        instr.append("syscall")
        instr.append("jr $ra")
        return instr

    def exit(self):
        instr = []
        instr.append("li $v0, 10")
        instr.append("syscall")
        return instr


