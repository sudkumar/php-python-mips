#!/usr/bin/python

from Config import *

class RegAlloc():
    """Register Allocator Controller"""
    def __init__(self, st, regDis, addrDis):
        # all the available registers are free
        self._freeRs = AvalRegs 
        # Hold the temp registers, which must be free after instruction execution
        self._toFreeRs = []

        # always keep Symbol Table along !!!
        self._st = st

        # attach the address and register discriptor
        self._addrDis = addrDis
        self._regDis = regDis

        # the generated instructions
        self._genInstrs = []
        self._spillHappen = False

    def getReg(self, var, tac, nextUse, notRs):
        self._spillHappen = False
        """Pick Suitable Register for var.
        
        Arguments:
            var {string} -- variable for which we want to get a register.
        """  

        # if Addr_Des[var] contains a register: assign that register to it.
        if "const_" not  in var["type"]:
            for location in self._addrDis.fetchR(var):
                # check if it's a register
                if self._regDis.isIn(location):
                    # Yes, it is. Return this location
                    return location

        # else if there is a register which is empty, assign that register to it.
        if len(self._freeRs) != 0:
            return self._freeRs[0]

        # else pick a register which is most suitable. Say this register is R. And suppose it holds value for variable `v`
        allocatedR = self.spill(tac, nextUse, notRs)
        if not allocatedR:
            print "Unable to get any register by spill for var at:" + ', '.join(map(str, operands["place"]))

        return allocatedR


    # Spill
    def spill(self, tac, nextUse, notRs):
        dest = None
        srcs = []
        if tac:
            dest = tac.dest
            srcs = tac.srcs

        # get the current rs and make sure that we don't give the current var, one of these registers        
        rs = []
        for x in notRs.keys():
            rs.append(notRs[x])
        scores = {}
        for reg in self._regDis.registers:
            if reg in rs:
                continue
            # for all locations that this register stores
            scores[reg] = 0
            for var in self._regDis.fetchVar(reg):
                # if Addr_Des[v] contains other locations for it's value, then "OK". 
                if len(self._addrDis.fetchR(var)) > 1:
                    return reg

                # if `v` is `dest`, the value being computed by this instruction, and `dest` is not also one of the `other`
                #   operands of this instruction, then we are "OK". We checked for other operands because, if we assign two operands
                #   the same `R`, there value will be overwriten with one of them's value. 
                if var == dest and var not in srcs:
                    return reg

                # if `v` has not next-use and not live (by looking at the Next-Use-Live table), then "OK".
                # print "alloc:84::"
                # print var
                # print nextUse
                if nextUse[var["place"]][0] == 0 and nextUse[var["place"]][1] == -1 and self._regDis.isOnlyVar(reg, var):
                    print nextUse
                    return reg

                # if we are not "OK" by one of the first two cases, then we need to generate the store instruction `store v, R` to 
                #   place a copy in its own memory location ( Spilling). 
                scores[reg] += 1

                # Repeat this for all values `v` that R holds.
        
        # if not "OK". Compute R's "score", the number of store instructions we needed to generate. Pick on of the registers
        #   with lowest score.
        self._spillHappen = True

        minScore = float("inf")
        allocatedR = None
        for reg in scores:
            if scores[reg] < minScore:
                minScore = scores[reg]
                allocatedR = reg
        return allocatedR

    

    # Remove a register from free registers
    def removeFromFree(self, reg):
        try:
            self._freeRs.remove(reg)
        except Exception, e:
            # raise e
            # print "Unable to remove "+reg + " from free list"
            x = e

    # Add to free list of register
    def addToFree(self, regs):
        for reg in regs:
            self._freeRs.append(reg)