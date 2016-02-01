#!/usr/bin/ python


# Type of instructions in ir
IRInstructionTypes = {
    "="     :   "assgn", 
    "+"     :   "assgn", 
    "-"     :   "assgn", 
    "*"     :   "assgn", 
    "/"     :   "assgn", 
    "ifgoto":   "cond_jump", 
    "goto"  :   "uncond_jump",  
    "call"  :   "func_call", 
    "label" :   "func_label", 
    "return":   "return",
    "print" :   "print"
}

# Jump Instructions
JumpInstructions = ["cond_jump", "uncond_jump"]


# Assignment Instructions
AssignmentInstructions = ["=", "+", "-", "*", "/"]