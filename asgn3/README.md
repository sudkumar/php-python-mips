# A Simple Cross compiler for PHP, build with Python

## Dependencies
- python-ply v2.5
    - a token generator
- pyinstaller 
    - for creating executable binary file from python
- python-tabulate 
    - for tabular view of results

## File Structure
- src
    -ply: necessary plugin for python-ply
    -lexer.py: code for token generation
    -parser.py: code for parser
    -print_table: create html file for given parse tree json. 
- test
    - Contains some test cases as input for parser
- makefile
    - To wrap all things and running

## Running the test cases
    
    make clean
    make

> This will create our executable binary parser file in a bin folder
> To run test cases

    ./bin/parser ./test/test1.php

> This will create test1.html file in root folder, to see parse tree
 
    firefox test1.html

