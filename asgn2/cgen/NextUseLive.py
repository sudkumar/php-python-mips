#!/usr/bin/ python

from LineParser import LineParser

"""Get the Next-Use and Liveness information for a Basic Block
Given a Basic Block, our aim is to attach the information about Next-Use and Liveness for each statement line in that 
Basic Block. We store information for each statement in a symbol table.
Algorithm:
    We set symbol table to intially set all nontemporary variables as been live on exit.
    We start at the last statement in Basic Block `B` and scan backwards to beginning of B.
    At each step i, oprt,opnd1, opnd2, opnd3... in B, we do the following:
    1. Attach to statement i, the information currently found in symbol table
    regarding the next use and live of all variables.
    2. if opnd1 get assigned some value, set it's entry to "not live" and "no next use".
    3. In the sumbol table, set opnd2, opnd3 to "live" and the next uses of these to i 
"""
def NextUseLive(basicBlock):
    """ Get the information for next and liveness
    Argemtents:
        basicBlock list  --- A list of instruction

    Returns:
        {list} ---- {symbolTable, nonTempVars}
    """


    symbolTable = []            # The symbol table that contains the information of next-use and liveness
    countLines = len(basicBlock)# The number of lines in basic block

    """
    symbolTable = [
        i      { "var1" : [1, -1],      "var2" : [0, i+1] },
        i+1    { "var1" : [0, i+2"],    "var2" : [0, i+2] }
        i+2    { "var1" : [0, -1],      "var2" : [1, -1] },
        .
        .
        i+n+1    { "var1" : [1, -1],      "var2" : [1, -1] } # exit line number
    ]
    """

    # nontemporary variables in basic block
    nonTempVars = []
    for line in basicBlock:
        lineParser = LineParser(line)
        # check if the instruction is an assignment
        if lineParser.type == "copy" or lineParser.type == "operation":
            # get the destination and sources
            operands = lineParser.operands
            for operand in operands:
                # check for int constants
                try:
                    operand = int(operand)
                except Exception, e:
                    # raise e
                    if not operand in nonTempVars:
                        nonTempVars.append(operand)

    # Now intialize out symbol table
    for i in range(countLines+1):             # for each line
        varsObject = {}
        for var in nonTempVars:             # for each variable
            varsObject[var] = [0,-1]        # init the live and nextuse to 0 and -1
        symbolTable.append(varsObject)

    # For exist line, make all live
    for var in nonTempVars:
        symbolTable[countLines][var][0] = 1

    # scan backword the basic block and apply the changes in symbol table
    for i in range(countLines):
        currLine = countLines-i-1 
        lineParser = LineParser(basicBlock[currLine])
        # copy the info of next line in symbol table into the current line in symbol table
        for var in nonTempVars:
            symbolTable[currLine][var] = symbolTable[currLine+1][var]

        # update the entries for variables if necessary
        variables = []    
        if lineParser.type == "copy" or lineParser.type == "operation":
            # get the operands
            operands = lineParser.operands
            # get the dest
            dest = operands[0]
            symbolTable[currLine][dest] = [0,-1]    # set no next use, not live

            # update the sources
            variables = operands[1:]
            
        elif lineParser.type == "cond_jump":
            # get the conditional expressions
            expr = lineParser.condExpr
            variables = [expr[0], expr[2]]
            
        elif lineParser.type == "return":
            # get the return value
            variables = lineParser.returnVals
            
        elif lineParser.type == "func_call":
            # get the parameters val
            variables = lineParser.funParameters

        elif lineParser.type == "print":
            # get arguments of print
            variables = lineParser.printArgs

        # now update the necessary variables
        for src in variables:
            try:
                src = int(src)
            except Exception, e:
                symbolTable[currLine][src] = [1,currLine+1]  # set next use to current line and live


    return symbolTable, nonTempVars

if __name__ == '__main__':
    basicBlock = [
        "1, =, a, 2",
        "2, +, b, a, 2",
        "3, +, a, a, 2",
        "4, =, c, 2",
        "5, ifgoto, a, < , c, 3"
    ]
    print NextUseLive(basicBlock)
    