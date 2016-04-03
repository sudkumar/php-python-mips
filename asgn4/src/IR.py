#!/usr/bin/python

from Config import *
from TAC import TAC

class IR():
    """Intermediate Representation controller"""
    def __init__(self):
        # intialize the three address code list
        self.tac = []

        # intialize the nextquad
        self.nextquad = 0

        # intialize the temp
        self.temp = 0



    def emit(self, _line):
        self.tac.append(_line)
        self.nextquad += 1


    def makeList(self, _i=None):
        if _i != None:
            return [_i]
        return []

    def mergeList(self, *_list):
        merged = []
        for list in _list:
            merged += list
        return merged

    def backpatch(self, _list, _i):
        for lineNumber in _list:
            self.tac[lineNumber] = self.tac[lineNumber] + str(_i+1)

    def emitTmp(self, irLine):
        # split the line and get the parts
        irParts = map(lambda x: x.strip(), irLine.split(","))

        # first part is operator
        op = irParts[0]

        # depending upon operator, src, dest and target will be determined
        instrType = Operators[op]

        # create the new tac object for this line
        tac = TAC(instrType, op, ln)

        # switch case for instruction types and determine src, dest and targets
        dest = srcs = src1 = src2 = None
        if instrType == InstrType.copy:
            # for destination
            # check if it's already declared, else create a new entry for it
            dest = irParts[1]
            src1  = irParts[2]

            # update the tc
            tac.dest = dest
            tac.src1 = src1
        elif instrType == InstrType.assgn:
            # for destination
            dest = irParts[1]

            # for sources
            srcs = irParts[2:]

            # update the tc
            tac.dest = dest
            tac.src1 = src1
            tac.src2 = src2

        elif instrType == InstrType.label:
            # update the label. It'll be just after label operator
            tac.target = irParts[1]

        elif instrType == InstrType.ujump:
            # update the target, it will be las on line
            tac.target = irParts[-1]

        elif instrType == InstrType.cjump:
            # get the srcs
            src1, src2 = [irParts[1], irParts[3]]

            # get the relational operator
            relop = irParts[2]
            # get the target
            target = irParts[-1]

            # update the tac
            tac.src1 = src1
            tac.src2 = src2
            tac.op = relop
            tac.target = target

        elif instrType == InstrType.params:
            # get the src
            src1 = irParts[1]

            # update the tac
            tac.src1 = src1

        elif instrType == InstrType.call:
            # get the return val
            if len(irParts) >= 3:
                dest = irParts[2]

            # get the target label
            target = irParts[1]

            # update the tac
            tac.dest = dest
            tac.target = target

        elif instrType == InstrType.ret:
            # get the return val
            src1 = irParts[1]

            # update the tac
            tac.src1 = src1

        elif instrType == InstrType.libFn:
            # get the return val
            if len(irParts) >= 2:
                dest = irParts[1]

            # get the target label
            target = irParts[0]

            # update the tac
            tac.dest = dest
            tac.target = target
            tac.typ = InstrType.libFn

        # append the tac to list of tac
        self.tac.append(tac)

        # increment the nextquad
        self.nextquad += 1

    # return a new temporary
    def newTemp(self):
        self.temp += 1
        return "t"+str(self.temp)
