#!/usr/bin/python


class SymbolTable():

    def __init__(self, _parent=None):
        # intialize the parent
        self.parent = _parent
        # intialize the symbols
        self.symbols = {};
        # intialize the size (width | offset) of the table
        self.width = 0




    """ Insert into symbol table
        create a new entry into symbol table and put the data
        @params _name {string} -- name (key | id) of the new entry
        @params _type {string} -- type of name (an attribute)
        @params _width {integer} -- size | offset for the name
    """
    def insert(self, _name, _type, _width, _scope=None):
        # create a attribute's dictionary
        attrs = {}
        # attach the information about the _name in attrs
        attrs["place"] = _name
        attrs["type"] = _type
        attrs["width"] = _width
        # add the scope to the variable
        if _scope != None:
            attrs["scope"] = _scope
        else:
            if self.parent != None:
                # We are not in the root symbol table
                # This is a function table and so symbol needs a memory location on stack
                # Assign it a offset from base of the function which is current width of the table
                attrs["scope"] = "local"
                attrs["offset"] = self.width
            else:
                # We are in root symbol table
                # Variables are in global scope. Memory location for these variables is statically 
                # assigned at compile time which is equal to place of these symboles
                # No need to assign them an offset
                attrs["scope"] = "global"
                attrs["offset"] = -1

        # attach the attributes for the name in the symbol table
        self.symbols[_name] = attrs
        # update the width of the symbol table by adding the width of the current symbol
        self.addWidth(_width)



    """ Enter a new entry for a procedure
        Create a new entry for a procedure.
        @params _st {SymbolTable}  -- parent symbol table
        @params _name {string} -- name of the procedure
        @params _procST {SymbolTable} -- symbol table for a procedure
    """
    def enterProc(self, _name, _lineNumber, _numParams, _procST):
        # create a attribute's dictionary
        attrs = {}
        # attach the information about the _name in attrs
        attrs["place"] = _name
        attrs["lineNumber"] = _lineNumber
        attrs["numParams"] = _numParams
        attrs["type"] = "proc"
        attrs["st"] = _procST

        # attach the attributes for the name in the symbol table
        self.symbols[_name] = attrs




    """ search
        search for a symbol in the table
        @params _symbol {string} -- symbol for which search should be done
        @return  -- if symbol found in the scope, return it's attribute else return None
    """
    def search(self, _symbol):
        # search for symbol in the table
        if _symbol in self.symbols.keys():
            # if found, return it's attributes
            return self.symbols[_symbol]
        return None



    """ Set attribute
        set attributes for a symbol in symbol table
        @params _symbol {string} -- symbol for which attribute is to be set
        @params _key {string} -- key for the attribute
        @params _val {object} -- value for the attribute
    """
    def setAttr(self, _symbol, _key, _val):
        # try to set the attribute
        try:
            self.symbols[_symbol][_key] = _val
        except:
            # if there was an exception, due to undefined dictionary,
            # create a attributes dictionary for symbol
            self.symbols[_symbol] = {}
            self.symbols[_symbol][_key] = _val
        # check of we added the any width
        if _key == "width":
            # update the offset of that symbol
            self.symbols[_symbol]["offset"] = self.width
            # update the width of the current symbol table
            self.addWidth(_val)

    """ Get attribute
        get attribute for a symbol in symbol table
        @params _symbol {string} -- symbol for which attribute should be fetched
        @params _key {string} -- attribute key
        @return {object} -- value of attribute for key if found else None
    """
    def getAttr(self, _symbol, _key):
        # try to get the attribute value if exists
        try:
            return self.symbols[_symbol][_key]
        except:
            print "Can't get ", _key, " value for ", _symbol
            return None

    """ Get all the attributes
        get attribute for a symbol in symbol table
        @params _symbol {string} -- symbol for which attribute should be fetched
        @return {object} -- value of attribute for key if found else None
    """
    def getAttrs(self, _symbol):
        # try to get the attribute value if exists
        try:
            return self.symbols[_symbol]
        except:
            print "Can't get attributes for :"+_symbol
            return None


    """ Add width
        Records cumulative with of all the entries in a symbol table
        @params {integer} _width - width to be addded
    """
    def addWidth(self, _width):
        self.width += _width
