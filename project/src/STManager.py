#!/usr/bin/python

"""
Symbol Table manager
"""

from SymbolTable import SymbolTable as ST

class STManager():
    def __init__(self):
        # create the root symbol table
        self.root = ST()
        # intialize the stack of symbol tables for activation record
        self.activeSTs = [self.root]



    """ Make Symbol Table
        create a new table and return a pointer to new table
        @params _prev {SymbolTable}  --  parent symbol table pointer
        @return {SymbolTable} -- newly created symbol table
    """
    def makeTable(self, _prev):
        # create a new symbol table table
        newST = ST()
        # make _prev the parent of new table
        newST.parent = _prev
        # return the new symbol table
        return newST


    """ Lookup
        Loopup for the symbol in the activation record
        @params _symbol {string} -- symbol for which look to be done
        @return {bool} -- symbol found or not
    """
    def lookup(self, _symbol):
        # get the number of active symbol tables
        countActiveRecords = len(self.activeSTs)
        # search for symbol in activation records in reverse order ( with most closely nested rule )
        while(countActiveRecords > 0):
            # search for symbol in a symbol table
            attrs = self.activeSTs[countActiveRecords-1].search(_symbol)
            # if symbol found, return the attribute for the symbol
            if attrs:
                return attrs
            # else loop in most closely nested symbol table
            countActiveRecords -= 1


        # symbol not found, return None
        return None



    """ Push
        push symbol table onto symbol tables stack
        @params _st {SymbolTable} -- symbol table to be pushed onto the stack
    """
    def push(self, _st):
        # push the new symbol on activation record's stack
        self.activeSTs.append(_st)


    """ Pop
        remove the top of the symbol tables stack
        @return {SymbolTable} -- removed symbol table
    """
    def pop(self):
        return self.activeSTs.pop()


    """ Insert into symbol table
        create a new entry into symbol table and put the data
        @params _name {string} -- name (key | id) of the new entry
        @params _type {string} -- type of name (an attribute)
        @params _offset {integer} -- size | offset for the name
    """
    def insert(self, _name, _type, _offset):
        self.currActive.insert(_name, _type, _offset)


    """ Enter a new entry for a procedure
        Create a new entry for a procedure.
        @params _name {string} -- name of the procedure
        @params _lineNumber {int}  -- liner number where function is defined
        @params _procST {SymbolTable} -- symbol table for a procedure
    """
    def enterProc(self, _name, _lineNumber, _numParams, _procST):
        self.currActive.enterProc(_name, _lineNumber, _numParams, _procST)


    """ Set attribute
        set attributes for a symbol in symbol table
        @params _symbol {string} -- symbol for which attribute is to be set
        @params _key {string} -- key for the attribute
        @params _val {object} -- value for the attribute
    """
    def setAttr(self, _symbol, _key, _val):
        self.currActive.setAttr(_symbol, _key, _val)


    """ Get attribute
        get attribute for a symbol in symbol table
        @params _symbol {string} -- symbol for which attribute should be fetched
        @params _key {string} -- attribute key
        @return {object} -- value of attribute for key if found else None
    """
    def getAttr(self, _symbol, _key):
        return self.currActive.getAttr(_symbol, _key)


    """ Get all the attributes
        get attribute for a symbol in symbol table
        @params _symbol {string} -- symbol for which attribute should be fetched
        @return {object} -- value of attribute for key if found else None
    """
    def getAttrs(self, _symbol):
        return self.currActive.getAttrs(_symbol)


    """ Current Active Symbol Table
        (getter) get the current active symbol table. Just a convenient method
    """
    @property
    def currActive(self):
        # return the top
        return self.activeSTs[-1]



    """ Insert all the keywords
        insert the keywords into the root of the symbol table
        so that they can be easily accessible
    """
    def insertKeywords(self):

        return None
