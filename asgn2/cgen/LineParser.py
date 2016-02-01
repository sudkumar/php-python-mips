#!/usr/bin/ python

from Config import  IRInstructionTypes

class LineParser():
    """A parser to parse a line in intermediate represented code"""
    def __init__(self, line):
        self._line = line.split(",")                # store the line as an array
        for i in range(len(self._line)):
            self._line[i] = self._line[i].strip() 
        self._ln = self._line[0]                    # get the line number of line
        self._op = self._line[1]                    # get the operator from the line

    @property
    def type(self):
        """Get the type of the instruction

        Returns:
            [string] -- Type of the current instruction
        """

        # Match the _op with a instruction in IRInstructionTypes Dictionary and return
        typeOfInstruction = IRInstructionTypes[self._op]
        if(typeOfInstruction):
            return typeOfInstruction
        
        # unknown type of instruction 
        return None    

    @property
    def jumpTarget(self):
        """ Get the jump target from current line
            It's a jump statement, so get the target label
        Returns:
            {string} -- Name of the label operands
        """
        
        return self._line[-1]       # Jump targets are at the end of statements
    

    @property
    def operands(self):
        return self._line[2:]       # Operands start from 3rd index till end
    