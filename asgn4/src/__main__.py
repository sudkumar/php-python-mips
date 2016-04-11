#!/usr/bin/python


from parser import runIR
import sys

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
    printStm(stm.root)
