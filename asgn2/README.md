# A simple code generator from three address code.

## File Structure
- src
    - AddrDis: Address descriptor file. 
    - BBGen: Basic block generation from given three address code.
    - Codegen: Generate Instructions from the IR. Responsible for creating the Register and Address Descriptor for all available register and variables and generate.
    - Config: Configuration setup file.
    - FlowGraph: From the intermediate represtation create nodes for each   basic blocks.
    - IR: Controls Intermediate Representation.
    - Lib: Library support file.
    - LineParser: Parser for parsing a line in IR code.
    - NextUseLive: Finds next use and liveness for each statement in given basic block.
    - RegAlloc: Handles register allocation.
    - RegDis: Register descriptor file.
    - SymbolTable: symbol table which store all information about lexemes and tokens.
    - TAC: 3 address code instructions file. 
    - __main__: program start here.

- test

Test cases contaning Intermediate 3AC.

      
    - test1.ir          // computes gcd for two numbers
    - test2.ir          // square of a number
    - test3.ir          // finds numbers which are divisible by 3 which are    less than a number n. 
    - test4.ir          // reverse an integer digits 
    - test5.ir          // finds factorial of a number
     

- makefile
    - to wrap all things together.

## Intermediate Code Representation


        HR                  Instruction type                    IR

        a = b                   assign                       =, a, b

        a = 2                   assign                       =, a, 2

        a = b + c               assign                       +, a, b, c

        a = b + 1               assign                      +, a, b, 1

        a = b - c               assign                      -, a, b, c

        a = b * c               assign                      *, a, b, c

        a = b / c               assign                      /, a, b, c

        a = b % c               assign                      %, a, b, c

        if(a < b){              jump                    ifgoto a, > , b, L1 
            stmt1                                       stmt1
        }else{                                          goto L2
            stmt2                                       L1: stmt2
            }                                           L2:              

        func()                  function def.           label, func

        x = func(a,b)           function call          param a
                                                       param b
                                                       call, func, x   // no of params at the end 

        return var              return                  return, var

        malloc(length)          memory allocate         params, length 
                                                        malloc      
 
        print var               print integer           params, var
                                                        printInt   

        print var               print float             params, var
                                                        printFloat   

        print var               print string            params, var
                                                        printStr   

        read var               read integer             readInt, var   

        read var               read float               readFloat, var   

        read var               read string              readStr, var 

        fopen("output")        file open                open, fileName     

        fread("input","r")     file read                readFile, fin     

        fwrite("output","w")   file write               writeFile, fo     

        fclose(filename)       file close               close, fileDesp    

        exit()                 abort program            exit    

## Running Test cases

   in asgn2 folder run these command to make executable codegen in bin folder-

    make clean
    make

   test cases can be run with this command:

    ./bin/codegen ./test/test1.ir

   this will give mips code, put the code in a file say "output.s" and execute these command to see the result-

    spim
    load "output.s"             // make sure outout.s is in same directory
    run

