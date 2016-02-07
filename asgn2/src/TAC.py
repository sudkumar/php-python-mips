#!/usr/bin/python


class TAC():
    """A Three address code instructions"""
    def __init__(self, typ, op, ln):
        self._typ = typ         # An InstrType attribute
        self._op = op           # An operator attribute
        # Symbol table entries pointers
        self._destST = self._src1ST = self._src2ST = None     
        self._target = None     # an target. my be integer or a label
        self._ln = ln    # line number for tac
       
    def updateTarget(self, nt):
        self._target = nt
    
    @property
    def type(self):
        return self._typ

    @property
    def operator(self):
        return self._op
    
    @property
    def dest(self):
        return self._destST

    @property
    def srcs(self):
        return self._src1ST, self._src2ST

    @property
    def lineNumber(self):
        return self._ln

    @property
    def target(self):
        return self._target

    @property
    def operands(self):
        return self._destST, self._src1ST, self._src2ST
    
    @property
    def src(self):
        return self._src1ST
    