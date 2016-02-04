# A simple code generator from three address code.

## File Structure
- cgen
    - BBGen: Basic block generation from given three address code.
    - Config: Configuration setup file.
    - FlowGraph: From the intermediate represtation create nodes for each basic blocks.
    - LineParser: Parser for parsing a line in IR code.
    - NextUseLive: Finds next use and liveness for each statement in given basic block.
    - Translator: Translate code in mips assembly instruction set.
    - codegen: Generate Instructions from the IRResponsible for creating the Register and Address Descriptor for all available register and variables and generate
- IrngMIPS
- test
    - test cases contaning Intermediate 3AC. 
- makefile
    - to wrap all things together.

## Intermediate Code Representation

- assignments
    + '=' operator
        * 1. assigning a variable to another variable
            - IR: "=, a, b"
        * 2. assigning a constant to a variable
            - IR: "=, a, 2"  
             
    + '+' operator
        * 1. adding variable with constant and stroring in another variable
            * IR: "+, a, b, 2"
        * 2. adding two variable and store result in other variable
            * IR: "+, a, b, c"
    + '-' operator
        * IR: "-, a, b, c"
    + '*' and '/' operators
        * IR: 

- jump instructions
    + conditional jump
        * 1. compare a variable to another
            - IR: "ifgoto a, <=, b, 5"
        * 2. compare a variable with a constant
            - IR: "ifgoto a, ==, 0, 6"

    + unconditional jump
        * IR: "goto, 5"  // go to ir code with line no 5.

    + function call
        * IR: "call, func"

- function definitation
    + IR: "label, func"      

- return instructions
    + simple return
        * IR: "return"
    + return with parameter
        * IR: "return var" 

- print instruction
    + IR: "print var"


## Running Test cases

