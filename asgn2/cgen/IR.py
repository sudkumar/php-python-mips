#!/usr/bin/python

from config import *
from SymbolTable import SymbolTable

class TAC():
    """Three address code instructions"""
    def __init__(self, typ, op, ln):
        self._typ = typ         # An InstrType attribute
        self._op = op           # An operator attribute
        # Symbol table entries pointers
        self._destST = self._src1ST = self._src2ST = None     
        self._target = None     # an target. my be integer or a label
        self._ln = 0    # line number for tac
        
        
class IR():
    """Intermediate Representation controller"""
    def __init__(self):
        self._tac = []
        self._st = SymbolTable()
        
    def parseLine(self, irLine):
        # split the line and get the parts
        irParts = map(lambda x: x.strip(), irLine.split(","))

        # the first part is line number
        ln = irParts[0]

        # second part is operator
        op = irParts[1]

        # depending upon operator, src, dest and target will be determined
        instrType = Operators[op]

        # create the new tac object for this line
        tac = TAC(instrType, op, ln)

        # switch case for instruction types and determine src, dest and targets
        dest = srcs = src1 = src2 = destST = srcST = src1ST = src2ST = None
        if instrType == InstrType.copy:
            # for destination
            # check if it's already declared, else create a new entry for it
            dest = irParts[2]
            destST = self._st.lookup(dest)
            if not destST:
                destST = self._st.insert(dest, "ID")

            # for source
            src1  = irParts[3]
            # look into the symbol table for this lexeme
            src1ST = self._st.lookup(src1)
            if not src1ST:
                if IsInt(src1):
                    src1ST = self._st.insert(src1, "INT")
                else:
                    print src1 +" not declared."

            # update the tc
            tac._destST = destST
            tac._src1ST = src1ST
        elif instrType == InstrType.assgn:
            # for destination
            dest = irParts[2]
            destST = self._st.lookup(dest)
            if not destST:
                destST = self._st.insert(dest, "ID")

            # for sources
            srcs = irParts[3:]
            i = 0
            for src in srcs:
                srcST = self._st.lookup(src)
                if srcST == None:
                    if IsInt(src):
                        srcST = self._st.insert(src, "INT")
                    else:
                        print "No entry for "+ src  
                if i == 0:
                    src1ST = srcST
                else:
                    src2ST = srcST
                i += 1

            # update the tc
            tac._destST = destST
            tac._src1ST = src1ST
            tac._src2ST = src2ST

        elif instrType == InstrType.label:
            # update the label. It'll be just after label operator
            target = irParts[2]

        elif instrType == InstrType.ujump:
            # update the target, it will be last on line
            target = irParts[-1]

        elif instrType == InstrType.cjump:
            # get the srcs
            srcs = [irParts[2], irParts[4]]
            i = 0
            for src in srcs:
                srcST = self._st.lookup(src)
                if srcST == None:
                    if IsInt(src):
                        srcST = self._st.insert(src, "INT")
                    else:
                        print "No entry for "+ src  
                if i == 0:
                    src1ST = srcST
                else:
                    src2ST = srcST
                i += 1
            # get the relational operator
            relop = irParts[3]
            # get the target
            target = irParts[-1]            


            # update the tac
            tac._src1ST = src1ST
            tac._src2ST = src2ST
            tac._op = relop
            tac._target = target

        elif instrType == InstrType.params:
            # get the src
            src1 = irParts[2]
            # look into the symbol table for this lexeme
            src1ST = self._st.lookup(src1)
            if not src1ST:
                if not IsInt(src1):
                    src1ST = self._st.insert(src1, "INT")
                else:    
                    print src1 +" not declared."

            # update the tac
            tac._src1ST = src1ST

        elif instrType == InstrType.call:
            # get the number of params
            if len(irParts) >= 4:
                src1 = irParts[3]
            else:
                # pass zero argument
                src1 = "0"
            # look into the symbol table for this lexeme
            src1ST = self._st.lookup(src1)
            if not src1ST:
                if IsInt(src1):
                    src1ST = self._st.insert(src1, "INT")
                else:
                    print src1 +" not declared."
            # get the target label
            target = irParts[2]

            # update the tac
            tac._src1ST = src1ST
            tac._target = target

        elif instrType == InstrType.ret:
            # get the return val
            src1 = irParts[2]
            # look into the symbol table for this lexeme
            src1ST = self._st.lookup(src1)
            if not src1ST:
                if IsInt(src1):
                    src1ST = self._st.insert(src1, "INT")
                else:
                    print src1 +" not declared."

            # update the tac
            tac._src1ST = src1ST


        self._tac.append(tac)


if __name__ == '__main__':
    ir = IR()
    with open('sample_input.ir', "r") as f:
        for line in f:
            ir.parseLine(line)
