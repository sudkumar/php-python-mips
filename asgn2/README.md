# A simple code generator from three address code.

## File Structure
- cgen
    - BBGen: Basic block generation from given three address code.
    - Config: Configuration setup file.
    - FlowGraph: From the intermediate represtation create nodes for each basic blocks.
    - LineParser: Parser for parsing a line in IR code.
    - NextUseLive: Finds next use and liveness for each statement in given basic block.
    - Translator: Translate code in mips assembly instruction set.
    - codegen: Generate Instructions from the IR. Responsible for creating the Register and Address Descriptor for all available register and variables and generate
- IrngMIPS
- test
    - test cases contaning Intermediate 3AC. 
- makefile
    - to wrap all things together.

## Intermediate Code Representation


        HR                  Instruction type                IR

        a = b                   assign                       =, a, b

        a = 2                   assign                       =, a, 2

        a = b + c               assign                       +, a, b, c

        a = b + 1               assign                      +, a, b, 1

        a = b - c               assign                      -, a, b, c

        a = b * c               assign                      *, a, b, c

        a = b / c               assign                      /, a, b, c

        

        if(a < b){              jump                    ifgoto a, > , b, L1 
            stmt1                                       stmt1
        }else{                                          goto L2
            stmt2                                       L1: stmt2
            }                                           L2:              

        func()                  function call           call, func

        func(a,b)               function call           param a
                                                       param b
                                                       call, func, 2   // no of params at the end 

        return var              return                  return var
 
        print var               print                   print var     

        read var                read                    read var     

        fread("input","r")      file read           fread fileLabel     

        fwrite("output","w")    file write          fwrite fileLabel     

## Running Test cases

