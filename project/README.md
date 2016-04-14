# PHP-PYTHON-MIPS Compiler Design

## Team Members
- Aman Kumar (12085)
- Rohit Anurag (12585)
- Sahil Solanki (11624)
- Sudhir Kumar (12734)


## File Structure
- src
    - AddrDist: Address descriptor file.
    - BBGen: Basic block generation from given three address code.
    - Codegen: Generate Instructions from the IR, responsible for creating the Register and Address Descriptor for all available register and variables.
    - Config: Configuration file for operators, registers and Instr types.
    - FlowGraph: From the IR create nodes for each basic blocks.
    - IR: IR generation handler.
    - Lib: Library function handler.
    - NextUseLive: Finds next use and liveness for each statement in given basic block.
    - RegAlloc: Handles register allocation.
    - RegDis: Register descriptor file.
    - STManager: Symbol Tables Manager
    - SymbolTable: Symbol Table
    - TAC: In memory representation of 3 address code.
    - lexer: lexer file
    - parser: parser file
    - __main__: program start here.


## features
    - declarations of vars and functions.
    - conditional if, if-else, if-elseif.
    - ternary operator.
    - switch case statement.
    - for loop.
    - while, do-while.
    - break, continue.
    - function call with params and return value.
    - function call without a return statement
    - echo supports.
    - pre-Increment and pre-Decrement. 
    - error handling for undefined decls and types.
    - error handling for function params count and undefined functions.
    - exit 
    - dead code elimination
    - print support for 4 character string


## test
    Test cases containing php src code.


# makefile
    - to wrap all things together.

## Running Test cases

In project folder run these command to make assembly code which goes in out.s file-

        ./run.sh test/switch.php

After generating assebmly code, run the spim assembler

        spim
        load "out.s"
        run


    