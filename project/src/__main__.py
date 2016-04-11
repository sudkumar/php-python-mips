#!/usr/bin/python


from parser import runIR
from CodeGen import CodeGen
from Config import *
from Lib import Lib

def printStm(root):
    for sym in root.symbols.keys():
        print root.symbols[sym]
        if(root.symbols[sym]["type"] == "proc"):
            print ">>>"
            printStm(root.symbols[sym]["st"])
            print "<<<"

if __name__ == '__main__':
    result = runIR()
    ir = result["ir"]
    ir.printTac()
    stm = result["stm"]
    code = CodeGen(ir, stm)
    print "\t.text"
    print "\t.globl main\n"
    print "main:\n"
    codeBlocks = code._codeBlocks
    # add the library functions
    # Now add the generated block by code generator
    i = 1
    for node in codeBlocks:   
        print "B"+str(i)+":"
        print "\t"+"\n\t".join(node)
        i += 1

    print "\tj "+LibFns["exit"]

    # lib = Lib()
    # instrs = lib.genFns()
    # for ins in instrs.keys():
    #    print str(ins)+":"
    #    print "\t"+"\n\t".join(instrs[ins])



    print "\n\t.data"
    for var in code._globalVars:
        print "g_"+str(var) + ":\t.word\t0"
    
    