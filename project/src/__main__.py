#!/usr/bin/python


from parser import runIR
from CodeGen import CodeGen
from Config import *
from Lib import Lib

def printStm(root):
    print root.width
    for sym in root.symbols.keys():
        print root.symbols[sym]
        if(root.symbols[sym]["type"] == "proc"):
            print ">>>"
            printStm(root.symbols[sym]["st"])
            print "<<<"

if __name__ == '__main__':
    result = runIR()
    errors = result["errors"]
    if len(errors) != 0:
        for error in errors:
            print error
        exit()
    ir = result["ir"]
    # ir.printTac()
    stm = result["stm"]
    # printStm(stm.root)
    code = CodeGen(ir, stm)
    print "\t.text"
    print "\t.globl main\n"
    print "main:\n"
    codeBlocks = code._codeBlocks
    # add the library functions
    # Now add the generated block by code generator
    i = 0
    for node in codeBlocks:   
        print "B"+str(i)+":"
        print "\t"+"\n\t".join(node)
        i += 1

    print "\tj "+LibFns["exit"]

    lib = Lib()
    instrs = lib.genFns()
    for ins in instrs.keys():
       print str(ins)+":"
       print "\t"+"\n\t".join(instrs[ins])



    print "\n\t.data"
    globalSyms = stm.root.symbols
    for var in globalSyms.keys():
        if globalSyms[var]["type"] != "proc":
            print "g_"+str(globalSyms[var]["place"]).replace("$", "_", 1) + ":\t.space\t"+ str(globalSyms[var]["width"])
    
    
