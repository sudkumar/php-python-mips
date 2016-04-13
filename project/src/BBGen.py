#!/usr/bin/python

from IR import IR

# from Config import IRInstructionTypes
# from Config import JumpInstructions

from Config import *

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

    def __init__(self, tacs):
        self._leaders = []                 # initialize the empty leaders array
        self._fns = []                      # map the function label to it's leader's line number
        countIRLines = len(tacs)        # get the number of total lines in ir
        # loop through all the lines and, get and store all the `leaders` in leaders
        i = 0
        while i < countIRLines:
            tac = tacs[i]       # parse the current line
            opType = tac.type
            if(i == 0):
                self.addLeader(i)    # add the first line to leaders
            # check for instruction type to be a label
            # if(opType == InstrType.label):
                # self._fns[tac.target] = int(tac.lineNumber)   # map the line to label
                # self.addLeader(tac.lineNumber)       # it was a label, so is a `leader`
            
            # check for instruction type to be a jump
            if(opType in JumpInstructions):
                if not (opType == InstrType.ret or opType == InstrType.libFn):
                    # get the jump target of this line, as it'll be a `leader`, must be an integer
                    self.addLeader(tac.target)
                
                if(opType == InstrType.call ):
                    if(not tac.target in self._fns):
                        self._fns.append(tac.target)

                # it was a jump statement, so next line will be the `leader` if it exists
                # if (opType in [InstrType.cjump, InstrType.ujump, InstrType.ret, InstrType.call]):
                i += 1
                if i < countIRLines:
                    self.addLeader(i) 
                    continue 
                else:
                    break                                   # reached at end of file
            i += 1      # go to next line

        # finally sort the `leaders` 
        self._leaders.sort() 

    def addLeader(self, leader):
        """Add a new leader
        Adds a new leader to leaders lists, check for duplications before adding

        Arguments:
            leader {int} -- The new leader to be added
        """

        try:
            leader = int(leader)
        except ValueError, e:
            # raise e
            x = e
        else:
            # if leader is already not present in leaders, add it, else...
            if not leader in self._leaders:
                self._leaders.append(leader)


if __name__ == '__main__':
    ir = IR("./../test/gcd.ir")
    tac = ir.tac
    bbGen = BBGen(tac)
    print bbGen._leaders
    print bbGen._fns


