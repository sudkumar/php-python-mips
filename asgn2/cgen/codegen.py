#!/usr/bin/ python

from FlowGraph import FlowGraph

from NextUseLive import NextUseLive

from LineParser import LineParser


from Translator import Translator

"""Code Generator

    This is the code generator for PHP, assembles all the components for generating code.
"""

class CodeGen():
    """Code Generator"""
    def __init__(self, ir):

        # Create a flow graph 
        flowGraph = FlowGraph(ir)
        blockNodes = flowGraph._blockNodes
        countNodes = len(blockNodes)

        # Create the Register and Address Descriptor for all available register and variables.
        # The Address Descriptor table, contains information about all the non local variables's value location
        self._addrDis = {}      
        # The Register Descriptor table, contains information about allocation of all the registers
        self._regDis = {"$t0":[], "$t1":[], "$t2":[], "$t3":[], "$s0":[], "$s1":[]}  

        self._tr = Translator()

        # a set of empty registers
        self._freeRs = []
        for reg in self._regDis:
            self._freeRs.append(reg)

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
            nextUseLiveST, nonTempVars = NextUseLive(blockIns)
            
            # check if the key exists in address discriptor
            for var in nonTempVars:
                if not self.isInAddrDis(var):
                    self._addrDis[var] = [var]  

            # add the nonTemp variables into global data region
            for var in nonTempVars:
                self._globalVars[var] = ""

            #- For each Instruction `Ins` in `blockIns`:
            i = 0
            self._newBlockIns = []
            jumpIns = []
            for ins in blockIns:
                self._toFreeRs = []
                # get the next use info about the current line
                nextUse = nextUseLiveST[i+1]

                # Get the type of `Ins`
                # if `Ins` isOfType "Operations" (dest = src1 op src2):
                parsedIns = LineParser(ins)
                if parsedIns.type == "operation":
                    #  handle to operation type and return generated instructions
                    self.handleOps(parsedIns, nextUse)                    

                # else if `Ins` isOfType "Copy Statement"(dest = src):
                elif parsedIns.type == "copy":
                    self.handleCopy(parsedIns, nextUse)

                # else if `Ins` isOfType "cond_jump"
                elif parsedIns.type == "cond_jump":
                    condExpr = parsedIns.condExpr
                    variabels = [condExpr[0], condExpr[2]]
                    # get registers for all variabels
                    allocatedRs = self.regForOperands(variabels, nextUse)
                    
                    newExp = [allocatedRs[variabels[0]], condExpr[1] ,allocatedRs[variabels[1]]]
                    self._newBlockIns.append(self._tr.getInstCondJump(newExp, parsedIns.jumpTarget))

                # else if `Ins` is of type "uncond_jump"
                elif parsedIns.type == "uncond_jump":
                    jumpIns.append("j "+parsedIns.operands[0])

                # else if `Ins` is of type "func_call"    
                elif parsedIns.type == "func_call":
                    parms = parsedIns.funParameters
                    # get registers for all variabels
                    allocatedRs = self.regForOperands(parms, nextUse)
                        
                    # add the argument instructions
                    i = 0
                    for parm in parms:
                        jumpIns.append("move $a"+str(i)+", "+allocatedRs[parm])
                        i += 1
                    jumpIns.append("jal "+parsedIns.operands[0])

                # else if `Ins` is of type "func_label"
                elif parsedIns.type == "func_label":
                    # self._newBlockIns.append(""+parsedIns.operands[0])
                    x = 1
                elif parsedIns.type == "return":
                    returnVals = parsedIns.returnVals
                    allocatedRs = self.regForOperands(returnVals, nextUse)
                   
                    # add the load for return value
                    i = 0
                    for ret in returnVals:
                        jumpIns.append("move $v"+str(i)+", "+allocatedRs[ret])
                        i += 1
                    jumpIns.append("jr $ra")


                elif parsedIns.type == "print":
                    arg = parsedIns.printArgs
                    allocatedRs = self.regForOperands([arg], nextUse)
                    self._newBlockIns.append(self._tr.getInstPrint("integer", allocatedRs[arg]))

                else:
                    self._newBlockIns.append(ins)

                i += 1

            # we done with the block, now time to restore the lost values 
            self._newBlockIns += self.restoreAtEnd(nonTempVars)
            self._newBlockIns += jumpIns
            ##### End of for loop for this block
            # update the node to contain the updated instruction set
            # self._newBlock += self._newBlockIns
            node._block = self._newBlockIns

            # For register to be free, Free them
            for reg in self._toFreeRs:
                self._freeRs.append(reg)

        self._flowGraph = flowGraph


    # Handler for operation type instructions
    def handleOps(self, parsedIns, nextUse):
        operands = parsedIns.operands
        dest = operands[0]          # destination var
        srcs = operands[1:]         # source var

        # check if there is any int constant in srcs and the the operation is not addition 
        # if there is any, make a register allotment and store contant in that register
        # and remove that src from srcs
        allocatedSrcs = {}       
        for src in srcs:
            if isInt(src):
                if parsedIns._op != "+":
                    # allocate a register for this contant integer
                    allocatedSrcs[str(src)] = self.regForIntConst(nextUse, src)

        # Get Registers for all operands (using GetReg(Ins) method). Say R_dest, R_src1, R_src2.
        allocatedRs = self.getReg(parsedIns, nextUse)

        # update the allocated registers if srcs were already alloted by the above method
        for src in allocatedSrcs:
            allocatedRs[src] = allocatedSrcs[src]

        # print allocatedRs
        rDest = allocatedRs[dest]   # register assigned to destination


        # For operand `src` in `Ins.srcOperands`:
        for src in srcs:
            error = None
            # if op is addition and src is int, then we know, we added a fake register. so no need
            # to for a load or change in addr and register discriptor tables
            # else
            if not isInt(src):
                rSrc = allocatedRs[src]
                # if `src` not in 'Register' (according to Reg_Des for R_src):
                if not src in self._regDis[rSrc]: 
                    # Issue `load R_src, src` Instruction.
                    self._newBlockIns.append("lw "+allocatedRs[src]+", "+src)
                    
                    # Change the Reg_Des[R_src] so it holds only `src`.
                    self._regDis[rSrc] = [src]
                    
                    # Change the Addr_Des[src] by adding `R_src` as an additional location.
                    self._addrDis[src].append(rSrc)         

        # handle the same src case, as mips wont allow that
        # if (srcs[0] == srcs[1]):
        #     newReg = self.regForIntConst(nextUse, '0', allocatedRs)
        #     self._newBlockIns.append("move "+newReg+", "+allocatedRs[srcs[0]])
        #     self._newBlockIns.append(self._tr.getInstOp(parsedIns._op, [rDest, newReg, allocatedRs[srcs[1]]] ))
        # else:
        self._newBlockIns.append(self._tr.getInstOp(parsedIns._op, map(lambda x: allocatedRs[x], operands)))

        # Issue The Instruction `op R_dest, R_src1, R_src2`
        # genereatedIns.append(parsedIns._op+" "+ ', '.join(map(lambda x: allocatedRs[x], operands)))

        # Change the Reg_Des[R_dest] so that it holds only `dest`.
        self._regDis[rDest] = [dest]
        
        # Change the Addr_Des[dest] so that it holds only location `R_dest`. We removed any memory location of `dest`
        #  which was in Addr_Des[dest] and We'll add it at the end of block. NO WORRIES!!!.
        self._addrDis[dest] = [rDest]

        # Remove `R_dest` from the Address Descriptor of any variable other than `dest`. 
        self.removeRFromAddrDis(rDest, dest)


    def handleCopy(self, parsedIns, nextUse):

        operands = parsedIns.operands
        dest = operands[0]
        src = operands[1]

        # Get Registers for all operands (using GetReg(Ins) method). Say R_dest = R_src. 
        # Both allocated must be same
        allocatedRs = self.getReg(parsedIns, nextUse)
        rSrc = allocatedRs[src]         # register assigned to source = destination
        rDest = allocatedRs[dest]
        isSrcInt = isInt(src)
        # If src=Ins.srcOperand is not in 'Register' and not a int:
        if not isSrcInt and (not src in self._regDis[rSrc]):
            # Issue `load R_src, src` Instruction.
            # self._newBlockIns.append(Translator.load(allocatedRs[src], src))
            self._newBlockIns.append("lw "+allocatedRs[src]+", "+src)
            
            # Change the Reg_Des[R_src] so it holds only `src`.
            self._regDis[rSrc] = [src]

            # Change the Addr_Des[src] by adding `R_src` as an additional location.
            self._addrDis[src].append(rSrc)

        # Adjust the Reg_Des[R_src] to include `dest`.
        self._regDis[rDest].append(dest)

        # Change the Addr_Des[dest] so that it holds only location `R_dest`.
        self._addrDis[dest] = [rDest]

        if isSrcInt:
            # self._newBlockIns.append(Translator.li(allocatedRs[src], src))
            self._newBlockIns.append("li "+allocatedRs[dest]+", "+src)

    def getReg(self, parsedIns, nextUse):
        """Get Register
            Get registers for given Instruction.
        Arguments:
            inst {string} -- Instruction for which registers are needed
        
        Returns:
            {dictionay} -- An key value dictionay with key as variable and value to be a register.
        """
        # the return value. Allocated registers.
        allocatedRs = {}
        typeOfIns = parsedIns.type
        operands = parsedIns.operands

        # if Instruction isOfType Operation:
        if typeOfIns == "operation":
            # Get the operands from the instruction. dest = src op src
            dest = operands[0]
            srcs = operands[1:]

            ## selection of registers for sources:
            for src in srcs:
                # if source is an integer, don't assign a real register. Make a fake register with the same value
                srcInt = isInt(src)
                if not srcInt:
                    # raise e
                    rSrc = self.pickSuitableR(src, operands, nextUse, allocatedRs)
                    allocatedRs[src] = rSrc
                    self.removeFromFreeRs(rSrc)     # remove from free list
                else:
                    allocatedRs[str(src)] = str(src)
            ## selection of registers for destination:
            # issues are the same as for srcs, just a minor differences
            # select a register that only holds value for x, if there is one.
            found = False
            for reg in self._regDis:
                if len(self._regDis[reg]) == 1 and dest in self._regDis[reg]:
                    allocatedRs[dest] = reg
                    self.removeFromFreeRs(reg)      # remove the register from free list
                    found = True
                    break
            if not found:
                # for all srcs:
                for src in srcs:
                    if isInt(src):
                        continue    
                    # if src has not next-use and not live and R_src holds only src, after being loaded, then R_src can be use as R_dest. "OK".
                    if nextUse[src][0] == 0 and nextUse[src][1] == -1:
                        # get all the locations that src is present in
                        for location in self._addrDis[src]:
                            if self.isInRegDis(location):
                                # a register location
                                # Now check if R_src holds only src. if so, return it
                                if len(self._regDis[location]) == 1 and src in self._regDis[location]:
                                    allocatedRs[dest] = location
                                    self.removeFromFreeRs(location)     # remove the location (register) from free list
                                    found = True
                                    break
                    # check if found, else loop for other sources
                    if found:
                        break

                # if still not found, get from pickSoutable
                if not found:
                    rDest = self.pickSuitableR(dest, operands, nextUse, allocatedRs)
                    allocatedRs[dest] = rDest
                    self.removeFromFreeRs(rDest)        # remove from free registers

        # else if instruction isOfType copy (dest = src):
        elif typeOfIns == "copy":

            dest = operands[0]
            src = operands[1]  

            isSrcInt = isInt(src)
            if not isSrcInt:
                # pick the R_src as above.
                rSrc = self.pickSuitableR(src, operands, nextUse, allocatedRs)
                # set R_dest = R_src
                rDest = rSrc
                self.removeFromFreeRs(rDest)    # now remove from free registers

            else:
                # make a fake register for interger and assign that to it.
                rSrc = src
                rDest = self.pickSuitableR(dest, operands, nextUse, allocatedRs)
                self.removeFromFreeRs(rDest)        # remove the register from free list

            allocatedRs[src] = rSrc
            allocatedRs[dest] = rDest

        return allocatedRs


    def pickSuitableR(self, var, operands, nextUse, allocatedRs):
        """Pick Suitable Register for var.
        
        Arguments:
            var {strinf} -- variable for which we want to get a register.
        """  

        # if Addr_Des[var] contains a register: assign that register to it.
        for location in self._addrDis[var]:
            # check if it's a register
            if self.isInRegDis(location):
                # Yes, it is. Return this location
                return location

        # else if there is a register which is empty, assign that register to it.
        if len(self._freeRs) != 0:
            return self._freeRs[0]

        # else pick a register which is most suitable. Say this register is R. And suppose it holds value for variable `v`
        allocatedR = self.spill(nextUse, operands, allocatedRs)
        if allocatedR:
            # create the added stores for the selected register
            for var in self._regDis[allocatedR]:
                # self._newBlockIns.append(Translator.store(var, allocatedR))
                self._newBlockIns.append("sw "+allocatedR+", "+var)

                # update the address discriptor for these variables
                self._addrDis[var].append(var)
        else:
            print "Unable to get any register by spill for var at:" + ', '.join(operands)

        return allocatedR

    # Spilling 
    def spill(self, nextUse, operands, allocatedRs):
        dest = operands[0]
        srcs = operands[1:]

        # get the current rs and make sure that we don't give the current var, one of these registers        
        rs = []
        for x in allocatedRs:
            rs.append(allocatedRs[x])

        scores = {}
        for reg in self._regDis:
            if reg in rs:
                continue
            # for all locations that this register stores
            scores[reg] = 0
            for var in self._regDis[reg]:
                # if Addr_Des[v] contains other locations for it's value, then "OK". 
                if len(self._addrDis[var]) > 1:
                    return reg

                # if `v` is `dest`, the value being computed by this instruction, and `dest` is not also one of the `other`
                #   operands of this instruction, then we are "OK". We checked for other operands because, if we assign two operands
                #   the same `R`, there value will be overwriten with one of them's value. 
                if var == dest and var not in srcs:
                    return reg

                # if `v` has not next-use and not live (by looking at the Next-Use-Live table), then "OK".
                if nextUse[var][0] == 0 and nextUse[var][1] == -1:
                    return reg

                # if we are not "OK" by one of the first two cases, then we need to generate the store instruction `store v, R` to 
                #   place a copy in its own memory location ( Spilling). 
                scores[reg] += 1

                # Repeat this for all values `v` that R holds.
        
        # if not "OK". Compute R's "score", the number of store instructions we needed to generate. Pick on of the registers
        #   with lowest score.

        minScore = float("inf")
        allocatedR = None
        for reg in scores:
            if scores[reg] < minScore:
                minScore = scores[reg]
                allocatedR = reg

        return allocatedR

    # Get register for variables. These instructions are other than copy and operations.
    def regForOperands(self, operands, nextUse):
        allocatedRs = {}
        for op in operands:
            if isInt(op):
                allocatedRs[str(op)] = self.regForIntConst(nextUse, op)
            else:
                allocatedRs[op] = self.pickSuitableR(op, operands, nextUse, allocatedRs)
        return allocatedRs

    # Allocate a register for integer constant loading
    def regForIntConst(self, nextUse, const, allocatedRs=[]):
        # generate a fake instruction for copy and get the register allocation for it
        fakeIn= "0, , "
        fakeParsedIn = LineParser(fakeIn)
        # get the register
        fakeReg = self.spill(nextUse, fakeParsedIn.operands, allocatedRs)
        # genereatedIns.append(Translator.load(allocatedRs[src], src))
        self._newBlockIns.append("li "+fakeReg+", "+const)
        self.removeFromFreeRs(fakeReg)
        # update the register descriptor
        self._regDis[fakeReg] = []
        # Remove `fakeReg` from the Address Descriptor of any variable
        self.removeRFromAddrDis(fakeReg)
        # add this register to list of register which must be free after instruction execution
        self._toFreeRs.append(fakeReg)
        return fakeReg

    # Restore the variables at the end block which are needed. 
    def restoreAtEnd(self, nonTempVars):
        genereatedIns = []          # generated instructions by store
        # For Each non temporary variable `x` in `node`:
        for x in nonTempVars:
            # if Addr_Des[x] don't say that its value is located in the memory location x:
            if not x in self._addrDis[x]:
                # Get the register R_x = Addr_Des[x], which contains value of `x` at the end of block.
                rX = None 
                for location in self._addrDis[x]:
                    if self.isInRegDis(location):
                        # location is a register
                        if x in self._regDis[location]:
                            rX = location
                            break
                if rX:
                    # Issue `store x, R_x` Instruction.
                    # genereatedIns.append(Translator.store(x,rX))
                    genereatedIns.append("sw "+rX+", "+x)

                    # Change the Addr_Des[x] to include it's own memory `x`.
                    self._addrDis[x].append(x)
                else:
                    print self._regDis
                    print self._addrDis
                    print "Unable to restore value of:"+x

        return genereatedIns        # return the generated instructions

    # Remove a register from free list
    def removeFromFreeRs(self, reg):
        if reg in self._freeRs:
            self._freeRs.remove(reg)

    # checks wether a given value is a valid register location or not
    def isInRegDis(self, val):
        if val in self._regDis.keys():
            return True
        return False

    # check if a variable has entry in addr discriptor table or not
    def isInAddrDis(self, var):
        if var in self._addrDis.keys():
            return True
        return False

    # Remove a given register from address discriptor of any other then from variable `me`
    def removeRFromAddrDis(self, reg, me=None):    
        for var in self._addrDis:
            if not var == me:
                if reg in self._addrDis[var]:
                    self._addrDis[var].remove(reg)


def isInt(val):
    try:
        val = int(val)
    except ValueError, e:
        # raise e
        return False
    else:
        return True


if __name__ == '__main__':
    fp = open("sample_input3.ir", "r")
    inputLines = fp.read()
    fp.close()
    code = CodeGen(inputLines)
    print "\t .data"
    for var in code._globalVars:
        print var + ":\t.word\t0"
    print "\t .text"
    # print "\t .global main"
    flowGraph = code._flowGraph
    blockNodes = flowGraph._blockNodes
    countNodes = len(blockNodes)
    tr =  Translator()
    i = 0
    for node in blockNodes:
        if node._block == "entry":
            # print "main:"
            i+=1
            continue
        if node._block == "exit":
            print "exit:"
            print tr.getInstExit()
        else:
            if i == 1:
                print "main:"
            else:    
                print "B"+str(i)+":"
            print "\t"+"\n\t".join(node._block)
        i+=1


