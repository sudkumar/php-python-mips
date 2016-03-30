#!/usr/bin/python


class TAC():
    """A Three address code instructions"""
    def __init__(self, _typ, _op):
        self.typ = _typ         # An InstrType attribute
        self.op = _op           # An operator attribute
        # Symbol table entries pointers
        self.dest = self.src1 = self.src2 = None
        self.target = None     # an target. my be integer or a label

    def updateTarget(self, nt):
        self._target = nt

    @property
    def type(self):
        return self.typ

    @property
    def operator(self):
        return self.op

    @property
    def dest(self):
        return self.dest

    @property
    def srcs(self):
        return self.src1, self.src2


    @property
    def target(self):
        return self.target

    @property
    def operands(self):
        return self.dest, self.src1, self.src2

    @property
    def src(self):
        return self.src1
