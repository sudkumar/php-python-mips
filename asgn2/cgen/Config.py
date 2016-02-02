#!/usr/bin/ python


# Type of instructions in ir
IRInstructionTypes = {
    "="     :   "copy", 
    "+"     :   "operation", 
    "-"     :   "operation", 
    "*"     :   "operation", 
    "/"     :   "operation", 
    "ifgoto":   "cond_jump", 
    "goto"  :   "uncond_jump",  
    "call"  :   "func_call", 
    "label" :   "func_label", 
    "return":   "return",
    "print" :   "print"
}

# Jump Instructions
JumpInstructions = ["cond_jump", "uncond_jump", "func_call"]


# Assignment Instructions
AssignmentInstructions = ["=", "+", "-", "*", "/"]