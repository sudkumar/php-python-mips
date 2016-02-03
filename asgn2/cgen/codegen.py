#!/usr/bin/ python

from FlowGraph import FlowGraph

from NextUseLive import NextUseLive

from LineParser import LineParser

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
        self._regDis = {"$1":[], "$2":[], "$3":[], "$4":[], "$5":[]}  

        # a set of empty registers
        self._freeRs = []
        for reg in self._regDis:
            self._freeRs.append(reg)

        self._spillHappen = False       # check if spill happened
        self._splliedSmts = []           # instruction genereated by spill

        self._newBlock = []

        self._globalVars = {}

        # For each node in blockNode of flow graph as node:
        for node in blockNodes:
            blockIns = node._block
            if blockIns == "entry" or blockIns == "exit":
                # entry and exit nodes, continue
                continue

            # Generate the Next-Use-Live for `blockIns`.
            nextUseLiveST, nonTempVars = NextUseLive(blockIns)
            
            # add the nonTemp variables into global data region
            for var in nonTempVars:
                self._globalVars[var] = ""

            #- For each Instruction `Ins` in `blockIns`:
            i = 0
            newBlockIns = []
            for ins in blockIns:
                self._spillHappen = False
                self._splliedSmts = []

                # get the next use info about the current line
                nextUse = nextUseLiveST[i+1]

                # Get the type of `Ins`
                # if `Ins` isOfType "Operations" (dest = src1 op src2):
                parsedIns = LineParser(ins)
                if parsedIns.type == "operation":

                    operands = parsedIns.operands
                    # Get Registers for all operands (using GetReg(Ins) method). Say R_dest, R_src1, R_src2.
                    allocatedRs = self.getReg(parsedIns, nextUse)
                    # print allocatedRs

                    # if spill happened, get the instructions
                    if self._spillHappen:
                        newBlockIns += self._splliedSmts
                        
                    dest = operands[0]          # destination var
                    rDest = allocatedRs[dest]   # register assigned to destination
                    srcs = operands[1:]         # source var

                    # For operand `src` in `Ins.srcOperands`:
                    for src in srcs:
                        error = None
                        if parsedIns._op == "+":
                            try:
                                src = int(src)
                            except ValueError, e:
                                # raise e
                                error = e
                        if error:
                            rSrc = allocatedRs[src]
                            # if `src` not in 'Register' (according to Reg_Des for R_src):
                            if not src in self._regDis[rSrc]: 
                                # Issue `load R_src, src` Instruction.
                                # newBlockIns.append(Translator.load(allocatedRs[src], src))
                                newBlockIns.append("lw "+allocatedRs[src]+", "+src)
                                
                                # Change the Reg_Des[R_src] so it holds only `src`.
                                self._regDis[rSrc] = [src]
                                
                                # Change the Addr_Des[src] by adding `R_src` as an additional location.
                                self._addrDis[src].append(rSrc)         

                    # Issue The Instruction `op R_dest, R_src1, R_src2`
                    # newBlockIns.append(Translator.op(parsedIns._op, operands))
                    newBlockIns.append(parsedIns._op+" "+ ', '.join(map(lambda x: allocatedRs[x], operands)))

                    # Change the Reg_Des[R_dest] so that it holds only `dest`.
                    self._regDis[rDest] = [dest]
                    
                    # Change the Addr_Des[dest] so that it holds only location `R_dest`. We removed any memory location of `dest`
                    #  which was in Addr_Des[dest] and We'll add it at the end of block. NO WORRIES!!!.
                    self._addrDis[dest] = [rDest]

                    # Remove `R_dest` from the Address Descriptor of any variable other than `dest`. 
                    for var in self._addrDis:
                        if not var == dest:
                            if rDest in self._addrDis[var]:
                                self._addrDis[var].remove(rDest)


                # else if `Ins` isOfType "Copy Statement"(dest = src):
                elif parsedIns.type == "copy":

                    operands = parsedIns.operands
                    dest = operands[0]
                    src = operands[1]

                    # Get Registers for all operands (using GetReg(Ins) method). Say R_dest = R_src. 
                    # Both allocated must be same
                    allocatedRs = self.getReg(parsedIns, nextUse)
                    # print allocatedRs
                    rSrc = allocatedRs[src]         # register assigned to source = destination
                    rDest = allocatedRs[dest]
                    isSrcInt = isInt(src)
                    # If src=Ins.srcOperand is not in 'Register' and not a int:
                    if not isSrcInt and (not src in self._regDis[rSrc]):
                        # Issue `load R_src, src` Instruction.
                        # newBlockIns.append(Translator.load(allocatedRs[src], src))
                        newBlockIns.append("li "+allocatedRs[src]+", "+src)
                        
                        # Change the Reg_Des[R_src] so it holds only `src`.
                        self._regDis[rSrc] = [src]

                        # Change the Addr_Des[src] by adding `R_src` as an additional location.
                        self._addrDis[src].append(rSrc)

                    # Adjust the Reg_Des[R_src] to include `dest`.
                    self._regDis[rDest].append(dest)

                    # Change the Addr_Des[dest] so that it holds only location `R_dest`.
                    self._addrDis[dest] = [rDest]

                    if isSrcInt:
                        # newBlockIns.append(Translator.li(allocatedRs[src], src))
                        newBlockIns.append("li "+allocatedRs[dest]+", "+src)

                else:
                    newBlockIns.append(ins)

                i += 1

            # we done with the block, now time to restore the lost values
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
                        # newBlockIns.append(Translator.store(x,rX))
                        newBlockIns.append("sw "+x+", "+rX)

                        # Change the Addr_Des[x] to include it's own memory `x`.
                        self._addrDis[x].append(x)
                    else:
                        print "No register contians value of "+x+" at " + str(ins)

            ##### End of for loop for this block

            # update the node to contain the updated instruction set
            # self._newBlock += newBlockIns
            node._block = newBlockIns

        self._flowGraph = flowGraph


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
                if len(self._regDis[reg]) == 1 and self.isInAddrDis(dest):
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
        # check if the key exists in address discriptor
        if not self.isInAddrDis(var):
            self._addrDis[var] = []    

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
        dest = operands[0]
        srcs = operands[1:]
        scores = {}

        # get the current rs and make sure that we don't give the current var, one of these registers
        rs = []
        for x in allocatedRs:
            rs.append(allocatedRs[x])

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

        if not allocatedR:
            print "Unable to assign a register for variable :" + var
        else:
            # create the added stores for the selected register
            self._spillHappen = True
            for var in self._regDis[allocatedR]:
                # self._splliedSmts.append(Translator.store(var, allocatedR))
                self._splliedSmts.append("sw "+var+", "+allocatedR)

                # update the address discriptor for these variables
                self._addrDis[var].append(var)
        return allocatedR


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
        print var + ":\t.word"
    print "\t .text"
    flowGraph = code._flowGraph
    blockNodes = flowGraph._blockNodes
    countNodes = len(blockNodes)
    i = 0
    for node in blockNodes:
        if node._block == "entry":
            # print "main:"
            i+=1
            continue
        if node._block == "exit":
            print "exit:"
            print "\tli $v0, 10"
            print "\tsyscall"
        else:
            if i == 1:
                print "main:"
            else:    
                print "B"+str(i)+":"
            print "\t"+"\n\t".join(node._block)
        i+=1


