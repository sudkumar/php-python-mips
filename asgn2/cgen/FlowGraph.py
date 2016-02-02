#!/usr/bin/ python

from BBGen import BBGen     # Get the basic block generator

from LineParser import LineParser   # Get the line parser

from Config import IRInstructionTypes
from Config import JumpInstructions

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

    def __init__(self, bbs):
        leaders = bbs._leaders
        countLeaders = len(leaders)
        ir = bbs._ir

        # get the functions dictionary
        self._fns = bbs._fns

        # container for all block nodes
        self._blockNodes = []

        # add block nodes
        self.addNodes(ir, leaders)

        # add the links between nodes
        self.addLinks(leaders)



    def addNodes(self, ir, leaders):
        # add the entry node
        self._blockNodes.append(Node("entry"))
        # create node for every leader
        countLeaders = len(leaders)
        for i in range(countLeaders):
            # create a new node with content of current block
            if i < countLeaders-1 :
                node = Node(ir[leaders[i]-1:(leaders[i+1]-1)])   # still a leader is remaining
            else:       
                node = Node(ir[leaders[i]-1:])          # this is the last leader

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
            lastInst = nodes[i]._block[-1]

            # parse the last instruction
            parsedLine = LineParser(lastInst)


            if parsedLine.type in JumpInstructions:
                # it's a jump instruction, so get the target `leader` and add that to my successor
                jumpTarget = parsedLine.jumpTarget
                try:
                    jumpTargetInt = int(jumpTarget)
                except ValueError, e:
                    # raise e
                    # It's a function label, so get it from bbs
                    jumpTargetInt = self._fns[jumpTarget]
                    # update the functions dictionary to point to a block node
                    
                    self._fns[jumpTarget] = "B"+str(leaders.index(jumpTargetInt)+1)
                finally:
                    # append the node
                    nodes[i].addSucc(nodes[leaders.index(jumpTargetInt)])
                    # update the target to point to the successor instead of line number
                    nodes[i]._block[-1] = parsedLine.updateJumpTarget("B"+str(leaders.index(jumpTargetInt)+1))

                # check if it a conditional jump instructions
                if parsedLine.type == IRInstructionTypes["ifgoto"]:
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
    fp = open("sample_input2.ir", "r")
    lines = fp.read()
    fp.close()
    bbs = BBGen(lines)
    fg = FlowGraph(bbs)
    print fg._fns
    for blockNode in fg._blockNodes:
        print blockNode._block

