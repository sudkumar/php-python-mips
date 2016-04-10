#!/usr/bin/python

from Config import *

class RegDis():
    """Register Discriptor Controller"""
    def __init__(self):
         # register discriptor table
        self._rs = {} 
        
        # add the intial registers to table
        for reg in (AvalRegs+ArgRegs+RetRegs):
            self._rs[reg] = []

    @property
    def registers(self):
        return self._rs
    
    # checks wether a given value is a valid register location or not
    def isIn(self, reg):
        if reg in self._rs.keys():
            return True
        return False

    # Empty a given register
    def emptyR(self, reg):
        self._rs[reg] = []

    # fetch vars from a given register
    def fetchVar(self, reg):
        return self._rs[reg]


    # var is the only var in a register. If we found a register then return that
    # else return None
    def onlyVarReg(self, var):
        for reg in self._rs:
            if self.isOnlyVar(reg, var):
                # found one. So return this register
                return reg

        # else return none
        return None


    # Is var tha only one in the reg
    def isOnlyVar(self, reg, var):
        if len(self._rs[reg]) == 1 and var in self._rs[reg]:
            return True
        return False

    # append a var to a register
    def appendVar(self, reg, var):
        self._rs[reg].append(var)

    # set the var as the only thing in a register
    def setVar(self, reg, var):
        self._rs[reg] = [var]