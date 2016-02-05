#!/usr/bin/ python

from FlowGraph import FlowGraph

from NextUseLive import NextUseLive

from IR import IR

# from Translator import Translator

from Config import *

from AddrDis import AddrDis
from RegDis import RegDis
from alloc import RegAlloc


"""Code Generator

    This is the code generator for PHP, assembles all the components for generating code.
"""

class CodeGen():
    """Code Generator"""
    def __init__(self, ir):

        # Create a flow graph 
        flowGraph = FlowGraph(ir.tac)
        blockNodes = flowGraph._blockNodes
        countNodes = len(blockNodes)

        # Create the Register and Address Descriptor for all available register and variables.
        # The Address Descriptor table, contains information about all the non local variables's value location
        self._addrDis = AddrDis()      
        # The Register Descriptor table, contains information about allocation of all the registers
        self._regDis = RegDis()

        # self._tr = Translator()

        self._st = ir.symbolTable

        self._regAlloc = RegAlloc(self._st, self._regDis, self._addrDis)

        # a set of empty registers
        self._freeRs = AvalRegs
        
        self._codeBlocks = []

        self._globalVars = {}
        self._newBlockIns = []
        # Holds register which stores constant for a instruction. 
        # There registers must be free after execution of that instruction
        self._toFreeRs = []  

        # For each node in blockNode of flow graph as node:
        for node in blockNodes:
            blockIns = node._block
            if blockIns == "entry" or blockIns == "exit":
                # entry and exit nodes, continue
                continue

            # Generate the Next-Use-Live for `blockIns`.
            nextUseLiveST, nonTempVars = NextUseLive(blockIns, ir.symbolTable)
            # check if the key exists in address discriptor
            self._addrDis.add(nonTempVars)

            # add the nonTemp variables into global data region
            for var in nonTempVars:
                self._globalVars[var] = ""

            #- For each Instruction `Ins` in `blockIns`:
            i = 0
            self._newBlockIns = []
            jumpIns = []
            for tac in blockIns:
                self._toFreeRs = []
                # get the next use info about the current line
                nextUse = nextUseLiveST[i+1]

                # Get the type of `Ins`
                # if `Ins` isOfType "Operations" (dest = src1 op src2):
                if tac.type == InstrType.assgn:
                    #  handle to operation type and return generated instructions
                    self.handleOps(tac, nextUse)                    

                # else if `Ins` isOfType "Copy Statement"(dest = src):
                elif tac.type == InstrType.copy:
                    self.handleCopy(tac, nextUse)

                # else if `Ins` isOfType "cond_jump"
                elif tac.type == InstrType.cjump:
                    srcs = tac.srcs
                    # get registers for all variabels
                    allocatedRs = {}
                    for src in srcs:
                        rSrc = self._regAlloc.getReg(src, tac, nextUse, allocatedRs)
                        allocatedRs[src] = rSrc
                        attrs = self._st.getAttrs(src)
                        if attrs["type"] == "const_int":
                            # generate a li instruction
                            self.genLiInstr(rSrc, src)

                    newExp = [allocatedRs[srcs[0]], tac.operator ,allocatedRs[srcs[1]]]
                    self._newBlockIns.append("ifgoto "+ ", ".join(newExp)+", "+str(tac.target))

                # else if `Ins` is of type "uncond_jump"
                elif tac.type == InstrType.ujump:
                    jumpIns.append("j "+str(tac.target))

                # else if `Ins` is of type "func_call"    
                elif tac.type == InstrType.call:
                    jumpIns.append("addi $sp, -4")
                    jumpIns.append("sw $ra, 0($sp)")
                    jumpIns.append("jal "+tac.target)
                    jumpIns.append("lw $ra, 0($sp)")
                    jumpIns.append("addi $sp, 4")

                # else if `Ins` is of type "func_label"
                elif tac.type == InstrType.label:
                    # self._newBlockIns.append(""+parsedIns.operands[0])
                    x = 1
                # the return type
                elif tac.type == InstrType.ret:
                    src = tac.src
                    attrs = self._st.getAttrs(src)
                    if attrs["type"] == "const_int":
                        jumpIns.append("li $v0, "+str(attrs["val"]))
                    else:     
                        allocatedR = self._regAlloc.getReg(tac.src, tac, nextUse, {})
                        jumpIns.append("move $v"+str(i)+", "+allocatedR)
                    # add the load for return value
                    jumpIns.append("jr $ra")


                # elif tac.type == InstrType.libFn:
                #     arg = parsedIns.printArgs
                #     allocatedRs = self.regForOperands([arg], nextUse)
                #     self._newBlockIns.append(self._tr.getInstPrintInt(allocatedRs[arg]))

                else:
                    print "code:142:: Unhandled instruction at "+tac.lineNumber
                    self._newBlockIns.append(tac)
                
                # For register to be free, Free them
                self._regAlloc.addToFree(self._toFreeRs)
                # print nextUse
                i += 1

            # we done with the block, now time to restore the lost values 
            self.restoreAtEnd(nonTempVars)
            self._newBlockIns += jumpIns
            ##### End of for loop for this block
            self._codeBlocks.append(self._newBlockIns)


        # self._flowGraph = flowGraph

    # Handler for operation type instructions
    def handleOps(self, tac, nextUse):

        operands = tac.operands
        dest = tac.dest
        srcs = tac.srcs

        # Get Registers for all operands (using GetReg(Ins) method). Say R_dest, R_src1, R_src2.
        allocatedRs = {}
        ## selection of registers for sources:
        srcInt = False
        bothInt = False
        for src in srcs:
            # if source is an integer, don't assign a real register. Make a fake register with the same value
            # but if both the srcs are integers, then we must store one of them in register
            if srcInt:
                bothInt = True

            attrs = self._st.getAttrs(src)
            srcInt = attrs["type"] == "const_int"
            if not srcInt:
                rSrc = self._regAlloc.getReg(src, tac, nextUse, allocatedRs)
                self.storeSpilled(rSrc)
                allocatedRs[src] = rSrc
                self._regAlloc.removeFromFree(rSrc)     # remove from free list
                # if `src` not in 'Register' (according to Reg_Des for R_src):
                if not src in self._regDis.fetchVar(rSrc): 
                    # Issue `load R_src, src` Instruction.
                    self._newBlockIns.append("lw "+str(rSrc)+", "+str(src))
                    
                    # Change the Reg_Des[R_src] so it holds only `src`.
                    self._regDis.setVar(rSrc, src)
                    
                    # Change the Addr_Des[src] by adding `R_src` as an additional location.
                    self._addrDis.appendR(src, rSrc)
            else: 
                intVal = attrs["val"]
                # check if the source is already alloted. This will be case 
                # when both operands are same
                if src in allocatedRs.keys():
                    continue
                if tac.operator == "+" and (not bothInt):
                    allocatedRs[src] = str(intVal)
                else:
                    rSrc = self._regAlloc.getReg(src, tac, nextUse, allocatedRs)
                    allocatedRs[src] = rSrc
                    self.storeSpilled(rSrc)
                    # if op is addition and src is int, then we know, we added a fake register. so no need
                    # to for a load or change in addr and register discriptor tables. else
                    # load that contant
                    self.genLiInstr(rSrc, src)


        ## selection of registers for destination:
        # issues are the same as for srcs, just a minor differences
        # select a register that only holds value for x, if there is one.
        found = False
        reg = self._regDis.onlyVarReg(dest)
        if reg != None:
            allocatedRs[dest] = reg
            self._regAlloc.removeFromFree(reg)      # remove the register from free list
            found = True
        if not found:
            # for all srcs:
            for src in srcs:
                attrs = self._st.getAttrs(src)
                if attrs["type"] == "const_int":
                    continue    
                # if src has not next-use and not live and R_src holds only src, after being loaded, then R_src can be use as R_dest. "OK".
                if nextUse[src][0] == 0 and nextUse[src][1] == -1:
                    # get all the locations that src is present in
                    for location in self._addrDis.fetchR(src):
                        if self._regDis.isIn(location):
                            # a register location
                            # Now check if R_src holds only src. if so, return it
                            if regDis.isOnlyVar(location, src):
                                allocatedRs[dest] = location
                                self._regAlloc.removeFromFree(location)     # remove the location (register) from free list
                                found = True
                                break
                # check if found, else loop for other sources
                if found:
                    break

            # if still not found, get from regs
            if not found:
                rDest = self._regAlloc.getReg(dest, tac, nextUse, allocatedRs)
                self.storeSpilled(rDest)
                allocatedRs[dest] = rDest
                self._regAlloc.removeFromFree(rDest)        # remove from free registers

        # create instruction for addi if operator is "+" and srcs are int
        if srcInt and  tac.operator == "+":
            consts = None
            regs = []
            for src in operands:
                try:
                    c = int(allocatedRs[src])
                except Exception, e:
                    # raise e
                    regs.append(str(allocatedRs[src]))
                else:
                    consts = c
            # consts will be none when both of them are same intergers
            if consts != None:
                self._newBlockIns.append("addi " +  ', '.join(regs) + ', '+str(consts))
            else:
                self._newBlockIns.append("addi " +  ', '.join(regs))    
        else:
            self._newBlockIns.append(tac.operator+ " " + ', '.join(map(lambda x: str(allocatedRs[x]), operands)))

        # Issue The Instruction `op R_dest, R_src1, R_src2`
        # genereatedIns.append(parsedIns._op+" "+ ', '.join(map(lambda x: allocatedRs[x], operands)))
        rDest = allocatedRs[dest]
        # Change the Reg_Des[R_dest] so that it holds only `dest`.
        self._regDis.setVar(rDest, dest)
        
        # Change the Addr_Des[dest] so that it holds only location `R_dest`. We removed any memory location of `dest`
        #  which was in Addr_Des[dest] and We'll add it at the end of block. NO WORRIES!!!.
        self._addrDis.setR(dest, rDest)

        # Remove `R_dest` from the Address Descriptor of any variable other than `dest`. 
        self._addrDis.removeR(rDest, dest)

    

    def handleCopy(self, tac, nextUse):
        dest = tac.dest
        src = tac.src  
        # Get Registers for all operands (using GetReg(Ins) method). Say R_dest = R_src. 
        attrs = self._st.getAttrs(src)
        isSrcInt = attrs["type"] == "const_int"
        if not isSrcInt:
            # pick the R_src as above.
            rSrc = self._regAlloc.getReg(src, tac, nextUse, {})
            self.storeSpilled(rSrc)
            # set R_dest = R_src
            rDest = rSrc
            self._regAlloc.removeFromFree(rDest)    # now remove from free registers

            # Both allocated must be same
            # If src=Ins.srcOperand is not in 'Register':
            if not src in self._regDis.fetchVar(rSrc):
                # Issue `load R_src, src` Instruction.
                # self._newBlockIns.append(Translator.load(allocatedRs[src], src))
                self._newBlockIns.append("lw "+str(rSrc)+", g_"+str(src))
                
                # Change the Reg_Des[R_src] so it holds only `src`.
                self._regDis.setVar(rSrc, src)

                # Change the Addr_Des[src] by adding `R_src` as an additional location.
                self._addrDis.appendR(src, rSrc)

        else:
            # make a fake register for interger and assign that to it.
            rSrc = src
            rDest = self._regAlloc.getReg(dest, tac, nextUse, {})
            self.storeSpilled(rDest)
            # Now generate the li instruction
            self.genLiInstr(rDest, src)

        
        # Adjust the Reg_Des[R_src] to include `dest`.
        self._regDis.appendVar(rDest, dest)

        # Change the Addr_Des[dest] so that it holds only location `R_dest`.
        self._addrDis.setR(dest, rDest)



    # Restore the variables at the end block which are needed. 
    def restoreAtEnd(self, nonTempVars):
        # For Each non temporary variable `x` in `node`:
        for x in nonTempVars:
            # if Addr_Des[x] don't say that its value is located in the memory location x:
            if not x in self._addrDis.fetchR(x):
                # Get the register R_x = Addr_Des[x], which contains value of `x` at the end of block.
                rX = None 
                for location in self._addrDis.fetchR(x):
                    if self._regDis.isIn(location):
                        # location is a register
                        if x in self._regDis.fetchVar(location):
                            rX = location
                            break
                if rX:
                    # Issue `store x, R_x` Instruction.
                    # genereatedIns.append(Translator.store(x,rX))
                    self._newBlockIns.append("sw "+str(rX)+", g_"+str(x))
                    # Change the Addr_Des[x] to include it's own memory `x`.
                    self._addrDis.setR(x, x)
                else:
                    print "code:351::"
                    print self._regDis.registers
                    print self._addrDis.addrs
                    print self._st._lexems
                    print "Unable to restore value of: g_"+str(x)

    # if Spill Happens, Store the locations in from spilled register
    def storeSpilled(self, allocatedR):
        if self._regAlloc._spillHappen:
            # create the added stores for the selected register
            for var in self._regDis.fetchVar(allocatedR):
                # self._newBlockIns.append(Translator.store(var, allocatedR))
                self._newBlockIns.append("sw "+str(allocatedR)+", g_"+str(var))
                # update the address discriptor for these variables, add there own location
                self._addrDis.appendR(var, var)

    # Generate instruction for tmp assigned register to integers
    def genLiInstr(self, reg, val):
        self._regAlloc.removeFromFree(reg)        # remove the register from free list
        # get the value of constant
        attrs = self._st.getAttrs(val)
        self._newBlockIns.append("li "+str(reg)+", "+str(attrs["val"]))
        self._toFreeRs.append(reg)

if __name__ == '__main__':
    ir = IR("sample_input.ir")
    code = CodeGen(ir)
    print "\t.data"
    for var in code._globalVars:
        print "g_"+str(var) + ":\t.word\t0"
    print "\t.text"
    print "\t.global B1"
    codeBlocks = code._codeBlocks
    i = 1
    for node in codeBlocks:   
        print "B"+str(i)+":"
        print "\t"+"\n\t".join(node)
        i += 1

    print "exit:"
    print "\tli, $v0, 10"
    print "\tsyscall"
