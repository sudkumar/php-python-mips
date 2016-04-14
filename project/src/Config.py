#!/usr/bin/python

from enum import Enum

#The Configuration files for application

# Instruction types
class InstrType(Enum):
    copy    = 1         # the copy instruction type i.e. "="
    assgn   = 2         # the assignment instruction type i.e. "+,-,*,\"
    label   = 3         # label for a function call, i.e. label foo
    ujump   = 4         # unconditional jump i.e. goto
    cjump   = 5         # conditinal jump i.e. ifgoto
    call    = 6         # call to a function, call foo
    params  = 7         # params for a function, params a
    libFn   = 8         # any call to library function
    relOp   = 9         # any relation operator i.e. <, <=, ==, >=, >
    ret     = 10        # the return instruction

Operators = {
    "="             : InstrType.copy,
    "+"             : InstrType.assgn,
    "-"             : InstrType.assgn,
    "*"             : InstrType.assgn,
    "/"            : InstrType.assgn,
    "%"             : InstrType.assgn,
    "label"         : InstrType.label,
    "goto"          : InstrType.ujump,
    "ifgoto"        : InstrType.cjump,
    "params"        : InstrType.params,
    "call"          : InstrType.call,
    "return"        : InstrType.ret,
    "printInt"      : InstrType.libFn,
    "printFloat"    : InstrType.libFn,
    "printStr"      : InstrType.libFn,
    "readInt"       : InstrType.libFn,
    "readFloat"     : InstrType.libFn,
    "readStr"       : InstrType.libFn,
    "malloc"        : InstrType.libFn,
    "exit"          : InstrType.libFn,
    "open"          : InstrType.libFn,
    "readFile"      : InstrType.libFn,
    "writeFile"     : InstrType.libFn,
    "closeFile"     : InstrType.libFn
}


LibFns = {
    "printInt"      :     "_printInt_",
    "printFload"    :     "_printFloat_",
    "printStr"      :     "_printStr_",
    "readInt"       :     "_readInt_",
    "readFloat"     :     "_readFloat_",
    "readStr"       :     "_readStr_",
    "malloc"        :     "_malloc_",
    "exit"          :     "_exit_",
    "open"          :     "_open_",
    "readFile"      :     "_readFile_",
    "writeFile"     :     "_writeFile_",
    "closeFile"     :     "_closeFile_"

}

JumpInstructions = [InstrType.ujump, InstrType.cjump, InstrType.call, InstrType.ret, InstrType.libFn]      

# Available register
TempRegs = ["$8", "$9", "$10", "$11", "$12", "$13", "$14", "$15", "$24", "$25"]
SavedRegs = ["$16", "$17", "$18", "$19", "$20", "$21", "$22", "$23"]
ArgRegs = ["$4", "$5", "$6", "$7"]

AvalRegs = TempRegs + SavedRegs + ArgRegs

RetRegs = ["$v0", "$v1"]

OperatorMap = {
    "+"     : "add",
    "-"     : "sub",
    "*"     : "mul",
    "/"     : "div",
    "%"     : "rem",
    ">"     : "bgt",
    ">="    : "bge",
    "<"     : "blt",
    "<="    : "ble",
    "=="    : "beq",
    "!="    : "bne"
}
# Checks whether a val is integer or not        
def IsInt(val):
    try:
        val = int(val)
    except Exception, e:
        # raise e
        return False
    else:
        return True