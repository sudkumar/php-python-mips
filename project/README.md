# PHP-PYTHON-MIPS Compiler Design

## Team Members
- Aman Kumar (12085)
- Rohit Anurag (12585)
- Sahil Solanki (11624)
- Sudhir Kumar (12734)

## Key Features
- for variable Integer type assumed 
- basic Arithmetic operations
- Increment, Decrement of a variable 
- two types of if-else stmt
- switch-case stmt
- for loop
- while loop
- function call without parameter
- recursion call
- break
- return
- continue
- library print integer support
- dead code elimination
- type checking

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

<<<<<<< HEAD
=======
- features
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
    - print newline support

>>>>>>> b566c0127eecb01d1a33f65ec690963e3ad71ff8
- test

    Test cases containing php src code.


- makefile
    - to wrap all things together.

## Running Test cases

   in project folder run these command to make assembly code which goes in out.s file-

    make clean
    make


    
## Execute Assembly Code

   run these command in terminal one by one

    $ spim
    $ load "out.s"
    $ run
