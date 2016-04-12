#!/usr/bin/python

from IR import IR

from FlowGraph import FlowGraph

from Config import *

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
def NextUseLive(bbNode):
    """ Get the information for next and liveness
    Argemtents:
        bbNode list  --- A list of three address code instruction
        st      -- the symbol table for all variables

    Returns:
        {list} ---- {symbolTable of next use and live, nonTempVars}
    """


    symbolTable = []            # The symbol table that contains the information of next-use and liveness
    countLines = len(bbNode)# The number of lines in basic block

    """
    symbolTable = [
        i      { "var1ST" : [1, -1],      "var2" : [0, i+1] },
        i+1    { "var1ST" : [0, i+2"],    "var2" : [0, i+2] }
        i+2    { "var1ST" : [0, -1],      "var2" : [1, -1] },
        .
        .
        i+n+1    { "var1" : [1, -1],      "var2" : [1, -1] } # exit line number
    ]
    """

    # nontemporary variables in basic block
    nonTempVars = []
    for tac in bbNode:
        # for all arguments, check if it's a variable, if, then add it
        operands = tac.operands
        for operand in operands:
            if operand != None: 
                if "const_" not in operand["type"]:
                    if not operand in nonTempVars:
                        nonTempVars.append(operand)       
    # Now intialize out symbol table
    for i in range(countLines+1):             # for each line
        varsObject = {}
        for var in nonTempVars:             # for each variable
            varsObject[var["place"]] = [0,-1]        # init the live and nextuse to 0 and -1
        symbolTable.append(varsObject)

    # For exist line, make all live as all are global
    for var in nonTempVars:
        symbolTable[countLines][var["place"]][0] = 1

    # scan backword the basic block and apply the changes in symbol table
    currLine = countLines - 1
    while currLine >= 0:
        # copy the info of next line in symbol table into the current line in symbol table
        for var in nonTempVars:
            symbolTable[currLine][var["place"]] = symbolTable[currLine+1][var["place"]]


        tac = bbNode[currLine]
        # trace line by line and update the nextuse table if necessary
        operands = tac.operands
        activeVars = []
        for operand in operands:
            if operand != None:
                if "const_" not in operand["type"]:
                    activeVars.append(operand["place"])  

        # update the entries for variables if necessary   
        if tac.type == InstrType.copy or tac.type == InstrType.assgn:
            # get the dest
            dest = activeVars[0]
            symbolTable[currLine][dest] = [0,-1]    # set no next use, not live

            # update the sources
            activeVars = activeVars[1:]
        
        # and take this special case, where we set function parameters to live 
        # untill function is get called
        elif tac.type == InstrType.params:
            funcCallAt = currLine + 1
            while tac.type == InstrType.params:
                attrs = st.getAttrs(tac.src)
                if "const_" not in tac.src["type"]:
                    symbolTable[currLine][tac.src["place"]] = [1,funcCallAt+1]
                currLine -= 1 
                tac = bbNode[currLine]
            continue

        # now update the necessary variables
        for src in activeVars:
            symbolTable[currLine][src] = [1,currLine+1]  # set next use to current line and live

        currLine -= 1

    return symbolTable, nonTempVars

if __name__ == '__main__':
    ir = IR("sample_input.ir")
    tac = ir._tac
    fg = FlowGraph(ir.tac)
    blockNode = fg._blockNodes[4]._block
    print NextUseLive(blockNode, ir.symbolTable)
    