#!/usr/bin/ python

from LineParser import LineParser

from Config import IRInstructionTypes
from Config import JumpInstructions

class BBGen():    
    """Basic Block Generator for Intermediate representation of code 

        The first statement of a Basic Block is called `leader`. So let's find that first 
        and then we can create Basic Block by creating block of instructions from a leader 
        until another leader.

    Algorithm:
        1. The first ir instruction is a `leader`.
        2. Any instruction that is the target of a conditional or unconditional jump
        is a `leader`.
        3. Any instruction that immediately follows a conditional or unconditional jump
        is a `leader`.
    
    Arguments:
        ir  {string}    An string of intermediate representation of program

    Returns:
        {array} An array consisting of line numbers, which are start of a Basic Block
    """

    def __init__(self, ir):
        self._ir = ir.split("\n")           # get an array of lines
        self._leaders = [1]                  # initialize the empty leaders array
        countIRLines = len(self._ir)         # get the number of total lines in ir

        # loop through all the lines and, get and store all the `leaders` in leaders
        i = 0
        while i < countIRLines:
            lnParser = LineParser(self._ir[i])       # parse the current line
            opType = lnParser.type

            if(i == 0):
                self.addLeader(int(lnParser._ln))    # add the first line to leaders
            # check for instruction type to be a label
            if(opType == IRInstructionTypes["label"]):
                self.addLeader(int(lnParser._ln))       # it was a label, so is a `leader`
            
            # check for instruction type to be a jump
            elif(opType in JumpInstructions):
                # get the jump target of this line, as it'll be a `leader`, must be an integer
                try:
                    x = int(lnParser.jumpTarget)
                except ValueError, e:
                    # raise e
                    x = e
                else:
                    self.addLeader(int(lnParser.jumpTarget))

                # it was a jump statement, so next line will be the `leader` if it exists
                i += 1
                if i < countIRLines:
                    lnParser = LineParser(self._ir[i])
                    self.addLeader(int(lnParser._ln))  

                else:
                    break                                   # reached at end of file

            i += 1      # go to next line

    def addLeader(self, leader):
        """Add a new leader
        Adds a new leader to leaders lists, check for duplications before adding

        Arguments:
            leader {int} -- The new leader to be added
        """
        # if leader is already not present in leaders, add it, else...
        if not leader in self._leaders:
            self._leaders.append(leader)


if __name__ == '__main__':
    fp = open("sample_input2.ir", "r")
    bbGen = BBGen(fp.read())
    print bbGen._leaders


