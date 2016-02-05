#!/usr/bin/python

from Config import *

class RegAlloc():
    """Register Allocator Controller"""
    def __init__(self, st):
        # all the available registers are free
        self._freeRs = AvalRegs 
        # Hold the temp registers, which must be free after instruction execution
        self._toFreeRs = []

        # always keep Symbol Table along !!!
        self._st = st

    def getReg(self, tac, nextUse, regDis, addrDis):
        """Get Register
            Get registers for given Instruction.
        Arguments:
            inst {string} -- Instruction for which registers are needed
        
        Returns:
            {dictionay} -- An key value dictionay with key as variable and value to be a register.
        """
        # the return value. Allocated registers.
        allocatedRs = {}
        typeOfIns = tac._type

        # if Instruction isOfType Operation:
        if typeOfIns == InstrType.assgn:
            # Get the operands from the instruction. dest = src op src
            dest = tac._destST
            srcs = [tac._src1ST, tac._src2ST]
            ## selection of registers for sources:
            for src in srcs:
                # if source is an integer, don't assign a real register. Make a fake register with the same value
                attrs = self._st.getAttrs(src)
                srcInt = attrs["typ"] == "const_int"
                if not srcInt:
                    rSrc = self.pickSuitableR(src, tac, nextUse, allocatedRs)
                    allocatedRs[src] = rSrc
                    self.removeFromFreeRs(rSrc)     # remove from free list
                else 
                    intVal = attrs["val"]
                    if tac._op == "+":
                        allocatedRs[str(src)] = str(intVal)
                    else:
                        allocatedSrcs[str(src)] = self.regForIntConst(nextUse, intVal)

            ## selection of registers for destination:
            # issues are the same as for srcs, just a minor differences
            # select a register that only holds value for x, if there is one.
            found = False
            reg = regDis.onlyVarReg(dest)
            if reg != None:
                allocatedRs[dest] = reg
                self.removeFromFreeRs(reg)      # remove the register from free list
                found = True
            if not found:
                # for all srcs:
                for src in srcs:
                    attrs = self._st.getAttrs(src)
                    if attrs["typ"] == "const_int":
                        continue    
                    # if src has not next-use and not live and R_src holds only src, after being loaded, then R_src can be use as R_dest. "OK".
                    if nextUse[src][0] == 0 and nextUse[src][1] == -1:
                        # get all the locations that src is present in
                        for location in addrDis.fetchR(src):
                            if self.isInRegDis(location):
                                # a register location
                                # Now check if R_src holds only src. if so, return it
                                if regDis.isOnlyVar(location, src):
                                    allocatedRs[dest] = location
                                    self.removeFromFreeRs(location)     # remove the location (register) from free list
                                    found = True
                                    break
                    # check if found, else loop for other sources
                    if found:
                        break

                # if still not found, get from pickSoutable
                if not found:
                    rDest = self.pickSuitableR(dest, tac, nextUse, allocatedRs, regDis, addrDis)
                    allocatedRs[dest] = rDest
                    self.removeFromFreeRs(rDest)        # remove from free registers

        # else if instruction isOfType copy (dest = src):
        elif typeOfIns == "copy":

            dest = tac._destST
            src = tac._src1ST  

            attrs = self._st.getAttrs(src)
            isSrcInt = attrs["typ"] == "const_int"
            if not isSrcInt:
                # pick the R_src as above.
                rSrc = self.pickSuitableR(src, tac, nextUse, allocatedRs, regDis, addrDis)
                # set R_dest = R_src
                rDest = rSrc
                self.removeFromFreeRs(rDest)    # now remove from free registers

            else:
                # make a fake register for interger and assign that to it.
                rSrc = src
                rDest = self.pickSuitableR(dest, tac, nextUse, allocatedRs, regDis, addrDis)
                self.removeFromFreeRs(rDest)        # remove the register from free list

            allocatedRs[src] = rSrc
            allocatedRs[dest] = rDest

        return allocatedRs


    def pickSuitableR(self, var, operands, nextUse, allocatedRs, regDis, addrDis):
        """Pick Suitable Register for var.
        
        Arguments:
            var {strinf} -- variable for which we want to get a register.
        """  

        # if Addr_Des[var] contains a register: assign that register to it.
        for location in addrDis.fetchR(var):
            # check if it's a register
            if regDis.isIn(location):
                # Yes, it is. Return this location
                return location

        # else if there is a register which is empty, assign that register to it.
        if len(self._freeRs) != 0:
            return self._freeRs[0]

        # else pick a register which is most suitable. Say this register is R. And suppose it holds value for variable `v`
        allocatedR = self.spill(nextUse, tac, allocatedRs)
        if allocatedR:
            # create the added stores for the selected register
            for var in regDis.fetchVar(allocatedR):
                # self._newBlockIns.append(Translator.store(var, allocatedR))
                self._newBlockIns.append("sw "+allocatedR+", "+var)

                # update the address discriptor for these variables, add there own location
                addrDis.appendR(var, var)
        else:
            print "Unable to get any register by spill for var at:" + ', '.join(operands)

        return allocatedR

    # Spilling 
    def spill(self, nextUse, tac, allocatedRs, regDis, addrDis):
        dest = tac._destST
        srcs = [tac._src1ST, tac._src2ST]

        # get the current rs and make sure that we don't give the current var, one of these registers        
        rs = []
        for x in allocatedRs:
            rs.append(allocatedRs[x])

        scores = {}
        for reg in regDis.registers:
            if reg in rs:
                continue
            # for all locations that this register stores
            scores[reg] = 0
            for var in regDis.fetchVar(reg):
                # if Addr_Des[v] contains other locations for it's value, then "OK". 
                if len(addrDis.fetchR(var)) > 1:
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
            attrs = self._st.getAttrs(op)
            if attrs["typ"] == "const_int":
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

    def setNotFree(self, reg): 
        self._freeRs.remove(reg)

    def setFree(sef, reg):
        self._toFreeRs.append(reg)