# A simple ir generator from src code.

## File Structure
- src
    - Config: Configuration file for operators, registers and Instr types.
    - IR: IR generation handler.
    - STManager: Symbol Tables Manager
    - SymbolTable: Symbol Table
    - TAC: In memory representation of 3 address code.
    - lexer: lexer file
    - parser: parser file
    - __main__: program start here.

- features
    - declarations of vars and functions.
    - conditional if, if-else, if-elseif.
    - ternary operator.
    - switch case statement.
    - for loop.
    - while, do-while.
    - break, continue.
    - function call with params and return value.
    - ECHO supports.
    - pre-Increment and pre-Decrement. 
    - error handling for undefined decls and types.

- test

Test cases contaning Intermediate 3AC.

      
    - test1.php          // function call and ternary
    - test2.php          // switch stmt
    - test3.php          // for loop
    - test4.php          // both kind of if-else stmt 
    - test5.php          // while stmt
     

- makefile
    - to wrap all things together.

## Running Test cases

   in asgn4 folder run these command to make executable irgen in bin folder-

    make clean
    make

   test cases can be run with this command:

    ./bin/irgen ./test/test1.php

