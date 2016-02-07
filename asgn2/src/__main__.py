#!/usr/bin/python


from CodeGen import CodeGen
from Lib import *
from IR import IR
import sys

def main():
    fileName = "./../test/test1.ir"
    if len(sys.argv) == 2:
        fileName = sys.argv[1]
    ir = IR(fileName)
    code = CodeGen(ir)
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

    lib = Lib()
    instrs = lib.genFns()
    for ins in instrs.keys():
       print str(ins)+":"
       print "\t"+"\n\t".join(instrs[ins])



    print "\n\t.data"
    for var in code._globalVars:
        print "g_"+str(var) + ":\t.word\t0"


if __name__ == '__main__':
    main()