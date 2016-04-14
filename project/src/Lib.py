#!/usr/bin/python

from Config import LibFns

# The library file
class Lib():

    def genFns(self):
        instrs = {}
        instrs[LibFns["printInt"]]= self.printInt()
        instrs[LibFns["printStr"]]= self.printStr()
        instrs[LibFns["readInt"]]= self.readInt()
        instrs[LibFns["readStr"]]= self.readStr()
        instrs[LibFns["malloc"]]= self.malloc()
        instrs[LibFns["exit"]]= self.exit()
        instrs[LibFns["open"]]= self.open()
        instrs[LibFns["readFile"]]= self.readFile()
        instrs[LibFns["writeFile"]]= self.writeFile()
        instrs[LibFns["closeFile"]]= self.closeFile()
        return instrs

    # print the content of $a0
    def printInt(self):
        instr = []
        instr.append("lw $a0, 0($sp)")
        instr.append("li $v0, 1")
        instr.append("syscall")
        instr.append("jr $ra")
        return instr

    # print the string at address $a0
    def printStr(self):
        instr = []
        instr.append("lw $a0, 0($sp)")
        instr.append("li $v0, 4")
        instr.append("syscall")
        instr.append("jr $ra")
        return instr

    # read integer and return it in $v0
    def readInt(self):
        instr = []
        instr.append("li $v0, 5")
        instr.append("syscall")
        instr.append("jr $ra")
        return instr

    # read float and return it in $v0
    def readFloat(self):
        instr = []
        instr.append("li $v0, 6")
        instr.append("syscall")
        instr.append("jr $ra")
        return instr

    # read string and store at address $a0 with size in $a1
    def readStr(self):
        instr = []
        instr.append("li $v0, 8")
        instr.append("syscall")
        instr.append("jr $ra")
        return instr

    # get the block of memory address with number of bytes in $a0
    # return the start address of block in $v0
    def malloc(self):
        instr = []
        instr.append("li $v0, 9")
        instr.append("syscall")
        instr.append("jr $ra")
        return instr

    # exit the program!!!
    def exit(self):
        instr = []
        instr.append("li $v0, 10")
        instr.append("syscall")
        return instr

    # open a file with name (address) in $a0
    # only read $a1 = 0
    # only write $a1 = 1
    # $a2 = 0
    # return file descriptor in $v0
    def open(self):
        instr = []
        instr.append("li $v0, 13")
        instr.append("syscall")
        return instr


    # get the content of file
    # $a0 contains the file descriptor
    # $a1 buffer address in which file should be read
    # $a2 contains the size of the buffer
    def readFile(self):
        instr = []
        instr.append("li $v0, 14")
        instr.append("syscall")
        return instr

    # write buffer to a file
    # $a0 contains the file descriptor
    # $a1 container the buffer address
    # $a2 contains the buffer size
    def writeFile(self):
        instr = []
        instr.append("li $v0, 15")
        instr.append("syscall")
        return instr

    # close a file
    # $a0 contains the file descriptor
    def closeFile(self):
        instr = []
        instr.append("li $v0, 16")
        instr.append("syscall")
        return instr


