#!/usr/bin/python


class SymbolTable():
    """A Symbol Table to store all information about lexems and tokens"""
    def __init__(self):
        self._table = []
        self._lexems = {}
        self._len = 0

    def insert(self, lxm, tkn):
        """Insert entry into Symbol Table

        Saves lexeme `lxm` and token `tkn`, and returns it's entry location

        Arguments:
            lexeme {string} -- A literal string of lexeme
            token {strinf} -- Token Associated with lexeme

        Returns:
            {location} -- location in Symbol Table
        """

        i = self._len
        # add lexeme to dictionary of lexems as key, and value to be it's index in table
        self._lexems[lxm] = i
        # create attributes for this lexeme and add them to table
        attrs = {"token":tkn}
        if tkn == "INT":
            attrs["type"] = "const_int"
            attrs["val"] = int(lxm)
        elif tkn == "STRING":
            attrs["type"] = "const_str"
            attrs["val"] = lxm
        else:
            attrs["type"] = "variable"
            attrs["name"] = lxm
        self._table.append(attrs)
        # increment the length of table
        self._len += 1
        # now return the index, assigned to lexeme
        return i


    def lookup(self, lxm):
        """Lookup for a lexeme

        Get the location of the lexeme `lxm` from the Symbol Table, if it exists,
        else return None

        Arguments:
            lxm {string} -- A lexeme for search

        Returns:
            {location} -- location in Symbol Table
        """
        try:
            i = self._lexems[lxm]
        except KeyError, e:
            # raise e
            return None
        else:
            return i

    def getAttrs(self, i):
        """Get attributes from table with index i

        Arguments:
            i {int} -- location in table
        Returns:
            {dictionary} -- attributes dictionary
        """
        try:
            val = self._table[i]
        except IndexError, e:
            # raise e
            return None
        else:
            return val
            pass
