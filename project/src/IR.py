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


        # three address code in string format
        self.strTac = []


    def emitCopy(self, _dest, _src):
        tac = TAC(InstrType.copy, "=")
        tac.dest = _dest
        tac.src1 = _src
        self.addTac(tac, tac.dest["place"] + " = " + tac.src["place"])

    def emitAssgn(self, _op, _dest, _src1, _src2):
        tac = TAC(InstrType.assgn, _op)
        tac.dest = _dest
        tac.src1 = _src1
        tac.src2 = _src2

        self.addTac(tac, tac.dest["place"] + " = " + tac.src1["place"] + " " + tac.op +" " + tac.src2["place"])


    def emitCjump(self, _op, _src1, _src2, _target=None):
        tac = TAC(InstrType.cjump, _op)
        tac.src1 = _src1
        tac.src2 = _src2
        tac.target = _target

        # make the target a string (for printing purpose only)
        _target = _target if _target != None else ""
        self.addTac(tac, "if " + tac.src1["place"] + " " + tac.op +" " + tac.src2["place"] + " goto " + str(_target))

    def emitUjump(self, _target=None):
        tac = TAC(InstrType.ujump, "goto")
        tac.target = _target

        # make the target a string (for printing purpose only)
        _target = _target if _target != None else ""
        self.addTac(tac, "goto "+ str(_target))

    def emitCall(self, _target, _nParams = None, _returnVal = None):
        tac = TAC(InstrType.call, "call")
        tac.target = _target
        tac.src1 = {
            "place":_nParams,
            "type": "const_int",
            "width": 4
        }
        tac.dest = _returnVal
        # make the target a string (for printing purpose only)
        _nParams = _nParams if _nParams != None else ""
        _returnVal = _returnVal if _returnVal != None else {"place": ""}
        self.addTac(tac, "call "+ str(_target) + " "+str(_nParams) + " " + str(_returnVal["place"]))

    def emitEcho(self):
        tac = TAC(InstrType.libFn, "echo")
        self.addTac(tac, "echo")

    def emitParams(self, _src):
        tac = TAC(InstrType.params, "params")
        tac.src =_src
        self.addTac( tac,  "params "+str(_src["place"]))

    def emitRet(self, _src=None):
        tac = TAC(InstrType.ret, "ret")
        tac.src =_src

        # make the _src a string (for printing purpose only)
        _src = _src if _src != None else {"place": ""}
        self.addTac( tac,  "ret "+str(_src["place"]))



    def addTac(self, _tac, _line):
        self.tac.append(_tac)
        self.strTac.append(_line)
        self.nextquad += 1



    def printTac(self):
        print "\n".join(self.strTac)

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
            self.tac[lineNumber].target = _i
            self.strTac[lineNumber] = self.strTac[lineNumber] + str(_i)

    # return a new temporary
    def newTemp(self):
        self.temp += 1
        return "t"+str(self.temp)
