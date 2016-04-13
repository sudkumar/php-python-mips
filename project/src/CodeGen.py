#!/usr/bin/python

import sys

from FlowGraph import FlowGraph
from NextUseLive import NextUseLive
from IR import IR

# from Translator import Translator
from Config import *
from AddrDis import AddrDis
from RegDis import RegDis
from RegAlloc import RegAlloc
from Lib import *

"""Code Generator

    This is the code generator for PHP, assembles all the components for generating code.
"""

class CodeGen():
    """Code Generator"""
    def __init__(self, ir, stm):

        # Create a flow graph 
        flowGraph = FlowGraph(ir.tac)
        blockNodes = flowGraph._blockNodes
        countNodes = len(blockNodes)


        self._st = stm


        self._fns = flowGraph._fns

        self._codeBlocks = []

        self._globalVars = {}
        self._newBlockIns = []
        # Holds register which stores constant for a instruction. 
        # There registers must be free after execution of that instruction
        self._toFreeRs = []  

        # For each node in blockNode of flow graph as node:
        nodeNumber = -1
        for node in blockNodes:
            # Create the Register and Address Descriptor for all available register and variables.
            # The Address Descriptor table, contains information about all the non local variables's value location
            self._addrDis = AddrDis()      
            # The Register Descriptor table, contains information about allocation of all the registers
            self._regDis = RegDis()
            # self._tr = Translator()
            

            self._regAlloc = RegAlloc(self._st, self._regDis, self._addrDis)
            self._newBlockIns = []

            blockIns = node._block
            if blockIns == "entry" or blockIns == "exit":
                # entry and exit nodes, continue
                continue

            # Some dead code elimination if a node don't have link to it's parents
            if(len(node._parentNodes)==0):
                self._codeBlocks.append(self._newBlockIns)
                continue

            # Generate the Next-Use-Live for `blockIns`.
            nextUseLiveST, nonTempVars = NextUseLive(blockIns)
            # print nonTempVars
            # check if the key exists in address discriptor
            self._addrDis.add(nonTempVars)

            # add the nonTemp variables into global data region
            # for var in nonTempVars:
            #     self._globalVars[var] = ""

            #- For each Instruction `Ins` in `blockIns`:
            i = 0
            jumpIns = []
            countBlock = len(blockIns)
            nodeNumber+= 1
            if nodeNumber in self._fns.keys():
                self._newBlockIns.append("addi $sp, -8")
                self._newBlockIns.append("sw $ra, 0($sp)")
                self._newBlockIns.append("sw $fp, 4($sp)")
                self._newBlockIns.append("move $fp, $sp")
                self._newBlockIns.append("addi $sp, -"+ str(self._st.ftable[self._fns[nodeNumber]]["st"].width))
            while i < countBlock:
                tac = blockIns[i]
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
                    jumpIns += self.handleCondJump(tac, nextUse)

                # else if `Ins` is of type "uncond_jump"
                elif tac.type == InstrType.ujump:
                    jumpIns.append("j "+str(tac.target))

                # else if `Ins` is of type "func_call"    
                elif tac.type == InstrType.call or tac.type == InstrType.libFn:
                    jumpIns += self.handleFnsCalls(tac, nextUse)

                # else if `Ins` is of type "func_label"
                elif tac.type == InstrType.label:
                    self._newBlockIns.append("addi $sp, $sp, -4")
                    self._newBlockIns.append("sw $ra, 0($sp)")
                # the return type
                elif tac.type == InstrType.ret:
                   jumpIns += self.handleReturns(tac, nextUse)

                # Handle the parametes, Handle the parameters right here as
                # we need other parameters here too     
                elif tac.type == InstrType.params:
                    # handle the parameters
                    # push them onto the stack
                    self.handleParams(tac, nextUse)
                    
                else:
                    print "code:142:: Unhandled instruction at "+tac.lineNumber
                    self._newBlockIns.append("tac")
                
                # For register to be free, Free them
                self._regAlloc.addToFree(self._toFreeRs)
                i += 1
            # we done with the block, now time to restore the lost values 
            self.restoreAtEnd(nonTempVars)
            self._newBlockIns += jumpIns
            ##### End of for loop for this block
            self._codeBlocks.append(self._newBlockIns)
            self._regAlloc.addToFree(self._toFreeRs)
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

            srcInt = True if "const_" in src["type"] else False
            if not srcInt:
                rSrc = self._regAlloc.getReg(src, tac, nextUse, allocatedRs)
                self.storeSpilled(rSrc)
                allocatedRs[src["place"]] = rSrc
                self._regAlloc.removeFromFree(rSrc)     # remove from free list
                # if `src` not in 'Register' (according to Reg_Des for R_src):
                # get it from memory and store it in a register
                self.lwInR(src, rSrc)

            else: 
                # get the int value
                intVal = src["place"]
                # check if the source is already alloted. This will be case 
                # when both operands are same
                if src in allocatedRs.keys():
                    continue
                if tac.operator == "+" and (not bothInt):
                    allocatedRs[src["place"]] = str(intVal)
                else:
                    rSrc = self._regAlloc.getReg(src, tac, nextUse, allocatedRs)
                    allocatedRs[src["place"]] = rSrc
                    self.storeSpilled(rSrc)
                    # if op is addition and src is int, then we know, we added a fake register. so no need
                    # to for a load or change in addr and register discriptor tables. else
                    # load that contant
                    self.genLiInstr(rSrc, src)
                    # set the register to be free after execution of this instruction
                    self._toFreeRs.append(rSrc)

        ## selection of registers for destination:
        # issues are the same as for srcs, just a minor differences
        # select a register that only holds value for x, if there is one.
        found = False
        reg = self._regDis.onlyVarReg(dest)
        if reg != None:
            rDest = reg
            self._regAlloc.removeFromFree(reg)      # remove the register from free list
            found = True
        if not found:
            # for all srcs:
            for src in srcs:
                if "const_" in src["type"]:
                    continue    
                # if src has not next-use and not live and R_src holds only src, after being loaded, then R_src can be use as R_dest. "OK".
                if nextUse[src["place"]][0] == 0 and nextUse[src["place"]][1] == -1:
                    # get all the locations that src is present in
                    for location in self._addrDis.fetchR(src):
                        if self._regDis.isIn(location):
                            # a register location
                            # Now check if R_src holds only src. if so, return it
                            if self._regDis.isOnlyVar(location, src):
                                rDest = location
                                self._regAlloc.removeFromFree(location)     # remove the location (register) from free list
                                found = True
                                break
                # check if found, else loop for other sources
                if found:
                    break

            # if still not found, get from regs
            if not found:
                rDest = self._regAlloc.spill(tac, nextUse, allocatedRs)
                self.storeSpilled(rDest)
                self._regAlloc.removeFromFree(rDest)        # remove from free registers

        # create instruction for addi if operator is "+" and srcs are int
        # Issue The Instruction `op R_dest, R_src1, R_src2`
        if srcInt and  tac.operator == "+":
            consts = None
            regs = []
            for src in srcs:
                try:
                    c = int(allocatedRs[src["place"]])
                except Exception, e:
                    # raise e
                    regs.append(str(allocatedRs[src["place"]]))
                else:
                    consts = c
            # consts will be none when both of them are same intergers
            if consts != None:
                self._newBlockIns.append("addi "+ str(rDest) +", " +', '.join(regs) + ', '+str(consts))
            else:
                self._newBlockIns.append("addi "+ str(rDest) +", "+  ', '.join(regs))    
        else:
            self._newBlockIns.append(OperatorMap[tac.operator]+ " " + rDest +", " +  ', '.join(map(lambda x: str(allocatedRs[x["place"]]), srcs)))

        # update the resigster and address discriptor of destination
        self.updateRegAddrOfDest(dest, rDest)

    

    def handleCopy(self, tac, nextUse):
        dest = tac.dest
        src = tac.src  
        # Get Registers for all operands (using GetReg(Ins) method). Say R_dest = R_src. 
        srcInt = True if "const_" in src["type"] else False
        if not srcInt:
            # pick the R_src as above.
            rSrc = self._regAlloc.getReg(src, tac, nextUse, {})
            self.storeSpilled(rSrc)
            # Both allocated must be same
            # set R_dest = R_src
            rDest = rSrc
            self._regAlloc.removeFromFree(rDest)    # now remove from free registers
            # If src=Ins.srcOperand is not in 'Register':
            # get it from memory and store in the register
            self.lwInR(src, rSrc)

        else:
            # make a fake register for interger and assign that to it.
            rSrc = src["place"]
            rDest = self._regAlloc.getReg(dest, tac, nextUse, {})
            self.storeSpilled(rDest)
            self._regAlloc.removeFromFree(rDest)
            # Now generate the li instruction
            self.genLiInstr(rDest, src)

        if not srcInt:
            # Adjust the Reg_Des[R_src] to include `dest`.
            self._regDis.appendVar(rSrc, dest)

        else:
            # add the dest at the a location in Reg_Des[R-Dest]
            self._regDis.setVar(rDest, dest)

         # remove dest from all regs that contains it till now
        for location in self._addrDis.fetchR(dest):
            # check if the location is a register
            if self._regDis.isIn(location):
                # now remove the dest from the regdis of location
                self._regDis.removeVar(location, dest)

        # Change the Addr_Des[dest] so that it holds only location `R_dest`.
        self._addrDis.setR(dest, rDest)



    # Handle the function call
    def handleFnsCalls(self, tac, nextUse):

        jumpIns = []

        insrts = []

        if tac.target != "exit":

            # insrts.append("addi $sp, -4")
            # insrts.append("sw $ra, 0($sp)")

            if tac.type == InstrType.call:
                jumpIns.append("jal "+tac.target)
            else:
                insrts.append("jal "+LibFns[tac.target])
                insrts.append("addi  $sp, 4")
                
            # insrts.append("lw $ra, 0($sp)")
            # insrts.append("addi $sp, 4")
            # get the return register
            dest = tac.dest
            # check if we want to store the return value
            if dest != None:
                # so it's just a copy statement, so we assign $v0 to dest
                allocatedR = self._regAlloc.getReg(dest, tac, nextUse, {})
                self._regAlloc.removeFromFree(allocatedR) 
                self.storeSpilled(allocatedR) 
                jumpIns.append("move "+ allocatedR + ", $v0")
                if dest["offset"] == -1:
                    jumpIns.append("sw "+ allocatedR + ", g_"+dest["place"].replace("$","_",1))
                else:
                    jumpIns.append("sw "+ allocatedR + ", "+str(dest["offset"])+"($sp)")

                # allocatedR = "$v0"
                # update the discriptor of destination and allocated R
                self.updateRegAddrOfDest(dest, allocatedR)
                
        else:
            insrts.append("j "+LibFns[tac.target])

        # if tac.type == InstrType.call:
        #     jumpIns = insrts 
        # else:
        self._newBlockIns += insrts

        return jumpIns


    def handleParams(self, tac, nextUse):
        src = tac.src
        allocatedR = self._regAlloc.getReg(src, tac, nextUse, {})
        self._regAlloc.removeFromFree(allocatedR)     # remove from free list

        # If src=Ins.srcOperand is not in 'Register':
        # get it from memory and store in the register
        self.lwInR(src, allocatedR)
        # if allocatedR != "$v0":
        self._newBlockIns.append("addi $sp, -"+str(src["width"]))
        self._newBlockIns.append("sw "+allocatedR+", 0($sp)" )

    # Handle return type of instructions
    def handleReturns(self, tac, nextUse):
        jumpIns = []
        # get the value to return
        src = tac.src
        if "const_" in src["type"]:
            jumpIns.append("li $v0, "+src["place"])
        else:     
            allocatedR = self._regAlloc.getReg(tac.src, tac, nextUse, {})
            self._regAlloc.removeFromFree(allocatedR)     # remove from free list

            # If src=Ins.srcOperand is not in 'Register':
            # get it from memory and store in the register
            self.lwInR(src, allocatedR)

            # if allocatedR != "$v0":
            jumpIns.append("move $v0, "+allocatedR)

        # add the load for return value
        jumpIns.append("move $sp, $fp")
        jumpIns.append("lw $ra, 0($sp)")
        jumpIns.append("lw $fp, 4($sp)")
        jumpIns.append("addi $sp, $sp, 8")
        jumpIns.append("jr $ra")        

        return jumpIns


    # Handle the conditional jump instructions
    def handleCondJump(self, tac, nextUse):
        genereatedIns = []
        srcs = tac.srcs
        # get registers for all variabels
        allocatedRs = {}
        # self._newBlockIns.append(str(self._regDis.registers))
        # self._newBlockIns.append(str(self._addrDis.addrs))
        for src in srcs:
            rSrc = self._regAlloc.getReg(src, tac, nextUse, allocatedRs)
            # self._newBlockIns.append(str(allocatedRs))
            allocatedRs[src["place"]] = rSrc
            self._regAlloc.removeFromFree(rSrc)     # remove from free list
            self.storeSpilled(rSrc)
            if "const_" in src["type"]:
                # generate a li instruction
                self.genLiInstr(rSrc, src)
            else:
                # If src=Ins.srcOperand is not in 'Register':
                # get it from memory and store in the register
                self.lwInR(src, rSrc)
            
        newExp = [allocatedRs[srcs[0]["place"]], allocatedRs[srcs[1]["place"]]]
        genereatedIns.append(OperatorMap[tac.operator]+" "+", ".join(newExp)+", "+str(tac.target))

        return genereatedIns

    # Restore the variables at the end block which are needed. 
    def restoreAtEnd(self, nonTempVars):
        # For Each non temporary variable `x` in `node`:
        for x in nonTempVars:
            # if Addr_Des[x] don't say that its value is located in the memory location x:
            if not x["place"] in self._addrDis.fetchR(x):
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
                    if x["offset"] == -1:
                        self._newBlockIns.append("sw "+str(rX)+", g_"+str(x["place"]).replace("$", "_", 1))
                    else:
                        self._newBlockIns.append("sw "+str(rX)+", "+str(x["offset"])+"($sp)")

                    # Change the Addr_Des[x] to include it's own memory `x`.
                    self._addrDis.setR(x, x["place"])

                    # make the register free
                    self._toFreeRs.append(rX)

                else:
                    self._newBlockIns.append("code:427::")
                    self._newBlockIns.append(str(self._regDis.registers))
                    self._newBlockIns.append(str(self._addrDis.addrs))
                    self._newBlockIns.append("Unable to restore value of: "+str(x))

            else:
                # remove other location and if there is a register 
                # set that to free
                for r in self._addrDis.fetchR(x):
                    if self._regDis.isIn(r):
                        # yes , it a register
                        self._toFreeRs.append(r)
                # set that x only holds it's memory location
                self._addrDis.setR(x, x["place"])

    # if Spill Happens, Store the locations in from spilled register
    def storeSpilled(self, allocatedR):
        if self._regAlloc._spillHappen:
            # create the added stores for the selected register
            for var in self._regDis.fetchVar(allocatedR):
                # self._newBlockIns.append(Translator.store(var, allocatedR))
                if var["offset"] == -1:
                    self._newBlockIns.append("sw "+str(allocatedR)+", g_"+str(var["place"]).replace("$", "_", 1))
                else:
                    self._newBlockIns.append("sw "+str(allocatedR)+", "+str(var["offset"])+"($sp)")

                # update the address discriptor for these variables, add there own location
                self._addrDis.setR(var, var["place"])
            toRemoveVars = self._regDis.fetchVar(allocatedR)
            for var in toRemoveVars:
                # remove the var from register discriptor of allocatedR
                self._regDis.removeVar(allocatedR, var)


    # Generate instruction for tmp assigned register to integers
    def genLiInstr(self, reg, val):
        self._regAlloc.removeFromFree(reg)        # remove the register from free list
        # get the value of constant
        self._newBlockIns.append("li "+str(reg)+", "+str(val["place"]))


    # Load from memory and store in a register
    def lwInR(self, src, rSrc):
        # if `src` not in 'Register' (according to Reg_Des for R_src):
        if not src in self._regDis.fetchVar(rSrc):
            # Issue `load R_src, src` Instruction.
            # self._newBlockIns.append(Translator.load(allocatedRs[src], src))
            if src["offset"] == -1:
                self._newBlockIns.append("lw "+str(rSrc)+", g_"+str(src["place"]).replace("$", "_", 1))
            else:
                self._newBlockIns.append("lw "+str(rSrc)+", "+str(src["offset"])+"($sp)")

            # Change the Reg_Des[R_src] so it holds only `src`.
            self._regDis.setVar(rSrc, src)

            # Change the Addr_Des[src] by adding `R_src` as an additional location.
            self._addrDis.appendR(src, rSrc)
 
    # Update the destination's register and address discriptors after assignment
    def updateRegAddrOfDest(self, dest, rDest):
        # Change the Reg_Des[R_dest] so that it holds only `dest`.
        self._regDis.setVar(rDest, dest)
        
        # Change the Addr_Des[dest] so that it holds only location `R_dest`. We removed any memory location of `dest`
        #  which was in Addr_Des[dest] and We'll add it at the end of block. NO WORRIES!!!.
        self._addrDis.setR(dest, rDest)

        # Remove `R_dest` from the Address Descriptor of any variable other than `dest`. 
        self._addrDis.removeR(rDest, dest)

        # Remove the dest from resiters other than rDest if there is anyone who contains the value 
        # of dest
        self._regDis.removeVarOtherThen(dest, rDest)

if __name__ == '__main__':
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