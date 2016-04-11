#!/usr/bin/python

from Config import *

class AddrDis():
    """Address Discriptor Controller"""
    def __init__(self):
        # address discriptor table
        self._addrs = {}


    @property
    def addrs(self):
        return self._addrs


    # check if a variable has entry in addr discriptor table or not
    def isInAddrDis(self, var):
        if var["place"] in self._addrs.keys():
            return True
        return False
        

    # fetch regs for a given var
    def fetchR(self, var):
        return self._addrs[var["place"]]


    # Remove a given register from address discriptor of any other then from variable `me`
    def removeR(self, reg, me=None):
        if  me:
            for var in self._addrs.keys():
                if  var != me["place"]:
                    if reg in self._addrs[var]:
                        self._addrs[var].remove(reg)
        else:
            for var in self._addrs.keys():
                if reg in self._addrs[var]:
                    self._addrs[var].remove(reg)
    


    # append a given register to a given var's address discriptor
    def appendR(self, var, reg):
        self._addrs[var["place"]].append(reg)

    # set the reg as the only thing in a var
    def setR(self, var, reg):
        self._addrs[var["place"]] = [reg]


    # add vars to table
    def add(self, vars):
        for var in vars:
            if not self.isInAddrDis(var):
                self._addrs[var["place"]] = [var["place"]]



            