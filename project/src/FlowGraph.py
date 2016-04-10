#!/usr/bin/python

from BBGen import BBGen     # Get the basic block generator

from IR import IR   # Get the line parser

from Config import *

class Node():
    """A Node in Flow Grpth"""
    def __init__(self, block):
        self._block = block
        self._nextNodes = []
        
    def addSucc(self, newNode):
        self._nextNodes.append(newNode)


class FlowGraph():
    """Create the Flow Graph for Intermediate Representation
    
    Algorithm:
      If there are two blocks, A and B, then there can exists an edge from A to B if 
        1. There is a conditional or unconditional jump from the end of A to the beginning of B.
        2. B immediately follows A in the original order of the three-address instructions, and
           A does not end in an unconditional jump.
    Arguments:
        ir {string} -- An string consisting of Intermediate Representation of code.
    """

    def __init__(self, tac):

        # Generate the basic blocks
        bbs = BBGen(tac)


        # container for all block nodes
        self._blockNodes = []

        # add block nodes
        self.addNodes(tac, bbs._leaders)

        # get the functions dictionary
        self._fns ={}
        for ln in bbs._fns:
            self._fns[str(ln)] = bbs._leaders.index(ln)

        # add the links between nodes
        self.addLinks(bbs._leaders)



    def addNodes(self, tac, leaders):
        # add the entry node
        self._blockNodes.append(Node("entry"))
        # create node for every leader
        countLeaders = len(leaders)
        for i in range(countLeaders):
            # create a new node with content of current block
            if i < countLeaders-1 :
                node = Node(tac[leaders[i]:(leaders[i+1])])   # still a leader is remaining
            else:       
                node = Node(tac[leaders[i]:])          # this is the last leader

            self._blockNodes.append(node)

        self._blockNodes.append(Node("exit"))

    def addLinks(self, leaders):
        exitNode = self._blockNodes[-1]
        nodes = self._blockNodes
        countLeaders = len(nodes)
        for i in range(countLeaders-1):
            # at start or end
            if i == 0:
                # add the link between entry and 1st block
                nodes[0].addSucc(nodes[1])
                continue    

            # get the last instruction
            ltac = nodes[i]._block[-1]

            if ltac.type in JumpInstructions:
                if ltac.type == InstrType.ret:
                    continue

                # it's a jump instruction, so get the target `leader` and add that to my successor  
                nodes[i].addSucc(nodes[leaders.index(ltac.target)])
                # update the target to point to the successor instead of line number   
                ltac.updateTarget("B"+str(leaders.index(ltac.target)))

                # check if it a conditional jump instructions
                if ltac.type == InstrType.cjump:
                    # the next `leader` is my successor
                    if i < countLeaders-1:
                        nodes[i].addSucc(nodes[i+1])
                    else:
                        # it is the last `leader`
                        nodes[i].addSucc(exitNode)
                

            # else next `leader` is my successor
            else:
                # the next `leader` is my successor
                if i < countLeaders-1:
                    nodes[i].addSucc(nodes[i+1])
                else:
                    # at end of program
                    nodes[i].addSucc(exitNode)

        self._blockNodes = nodes

if __name__ == '__main__':
    ir = IR("sample_input3.ir")
    fg = FlowGraph(ir.tac)
    print fg._fns
    i = 0
    blocs = len(fg._blockNodes)
    for blockNode in fg._blockNodes:
        if i == 0 or i == blocs-1:
            i += 1
            continue
        for t in blockNode._block:
            print t._ln
        print "===================="    
        i += 1
