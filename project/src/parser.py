import os, sys, lexer, logging, ply.yacc as yacc, json

from STManager import STManager
from IR import IR

stm = None
ir = IR()

tokens = lexer.tokens

precedence = (
  ('left', 'INCLUDE', 'INCLUDE_ONCE', 'EVAL', 'REQUIRE', 'REQUIRE_ONCE'),
  ('left', 'COMMA'),
  ('left', 'BIT_OR'),
  ('left', 'BIT_XOR'),
  ('left', 'BIT_AND'),
  ('right', 'PRINT'),
  ('left', 'EQUAL', 'PLUS_EQ','MINUS_EQ', 'MULTIPLY_EQ', 'DIVIDE_EQ', 'MOD_EQ', 'DOT_EQ'),
  ('left', 'COND_OP', 'COLON'),
  ('left', 'OR_OP'),
  ('left', 'AND_OP'),
  ('nonassoc', 'EQ_EQ', 'IDENTICAL', 'NOT_IDENTICAL', 'NOT_EQ'),
  ('nonassoc', 'LESSER', 'LESSER_EQ', 'GREATER', 'GREATER_EQ'),
  ('left', 'BIT_LSHIFT', 'BIT_RSHIFT'),
  ('left', 'PLUS', 'MINUS', 'DOT'),
  ('left', 'MULT', 'DIV', 'MOD'),
  ('right', 'NOT'),
  ('nonassoc', 'INSTANCEOF'),
  ('right', 'BIT_NOT', 'INC', 'DEC',),
  ('right', 'LBRACKET'),
  ('nonassoc', 'NEW', 'CLONE'),
  ('left', 'NOELSE'),
  ('left', 'ELSEIF'),
  ('left', 'ELSE'),
  ('left', 'ENDIF'),
  ('right', 'STATIC', 'ABSTRACT', 'FINAL', 'PRIVATE', 'PROTECTED', 'PUBLIC'),
  )

def p_start(p):
    'start : start_marker stmt_list'
    global stm
    stm.pop()
    # print stm.root.symbols
    global ir
    p[0] = {}
    p[0]["ir"] = ir
    p[0]["stm"] = stm

def p_start_marker(p):
    'start_marker : empty'
    global stm
    stm = STManager()

def p_stmt_list(p):
    '''stmt_list : top_stmt jump_marker stmt_list
                        | empty '''
    p[0] = {}
    global ir
    if len(p) == 4 :
        ir.backpatch(p[1]["nextlist"], p[2]["quad"])
        p[0]["nextlist"] = p[3]["nextlist"]
    else:
        p[0]["nextlist"] = ir.makeList()

def p_top_stmt(p):
    '''top_stmt : stmt
                   | func_decl'''
    global ir
    p[0] = {}
    try:
        p[0]["nextlist"] = p[1]["nextlist"]
    except:
        p[0]["nextlist"] = ir.makeList()


#--------------------------------------------------------------------------------------------------------

# --- Function

def p_func_decl(p):
    'func_decl : FUNCTION goto_marker  STRING func_table_marker LPAREN jump_marker params RPAREN LBRACE inner_stmts RBRACE jump_marker'
    global ir
    global stm
    p[0] = {}
    # put the start goto to skip the function defination
    ir.backpatch(p[2]["nextlist"], p[12]["quad"])
    # remove the function table
    procST = stm.pop()
    stm.enterProc(p[3], p[6]["quad"], p[7]["numParams"], procST)

def p_func_table_marker(p):
    'func_table_marker : empty'
    p[0] = {}
    global stm
    stm.push(stm.makeTable(stm.currActive))

def p_params(p):
    '''params : params COMMA param
                      | param
                      | empty'''
    p[0] = {}
    if(len(p)==2):
        try:
            paramsType = p[1]["type"]
            p[0]["numParams"] = 1
        except:
            p[0]["numParams"] = 0
    else:
        p[0]["numParams"] = p[1]["numParams"] + p[3]["numParams"]

def p_param(p):
    '''param : IDENTIFIER
                 | BIT_AND IDENTIFIER
                 | IDENTIFIER EQUAL scalar
                 | BIT_AND IDENTIFIER EQUAL scalar'''
    global stm
    p[0] ={}
    if(len(p)==2):
        stm.insert(p[1], "int", 4)
        p[0]["type"] = "int"
        p[0]["numParams"] = 1
    elif(len(p)==3):
        p[0] = {"param":[p[1],p[2]]}
    elif(len(p)==4):
        p[0] = {"param":[p[1],p[2],p[3]]}
    else:
        p[0] = {"param":[p[1],p[2],p[3],p[4]]}

#--------------------------------------------------------------------------------------------------------

# --- IF ELSE

def p_stmt_if(p):
    '''stmt : if_stmt
               | alt_if_stmt'''
    p[0] = p[1]

def p_if_stmt(p):
    '''if_stmt : if_stmt_without_else %prec NOELSE
             | if_stmt_without_else ELSE goto_marker jump_marker stmt'''
    global ir
    p[0] = {}
    if(len(p)==6):
        # if with else statement
        # resolve the false list of if_stmt_without_else to go to else statement
        ir.backpatch(p[1]["falselist"], p[4]["quad"])

        # now pass the information from subtree to if_stmt
        p[0]["nextlist"] = ir.mergeList(ir.mergeList(p[1]["nextlist"], p[3]["nextlist"]), p[5]["nextlist"])
        p[0]["breaklist"] = ir.mergeList(p[1]["breaklist"], p[5]["breaklist"])
        p[0]["continuelist"] = ir.mergeList(p[1]["continuelist"], p[5]["continuelist"])
    else:
        # print str(len(p)) + 'sss'
        # pass the information from if_stmt_without_else to if_stmt
        p[0] = p[1]
        p[0]["nextlist"] = ir.mergeList(p[1]["falselist"], p[1]["nextlist"])


def p_if_stmt_without_else(p):
    '''if_stmt_without_else : IF LPAREN expr RPAREN jump_marker stmt
                          | if_stmt_without_else ELSEIF goto_marker LPAREN jump_marker expr RPAREN jump_marker stmt'''
    global ir
    p[0] = {}
    if(len(p)==7):
        ir.backpatch(p[3]["truelist"], p[5]["quad"])
        p[0]["falselist"] = p[3]["falselist"]
        p[0]["nextlist"] = p[6]["nextlist"]
        p[0]["breaklist"] = p[6]["breaklist"]
        p[0]["continuelist"] = p[6]["continuelist"]
    else:
        ir.backpatch(p[6]["truelist"], p[8]["quad"])
        ir.backpatch(p[1]["falselist"], p[5]["quad"])
        p[0]["falselist"] = p[6]["falselist"]
        p[0]["nextlist"] = ir.mergeList(ir.mergeList(p[1]["nextlist"], p[3]["nextlist"]), p[9]["nextlist"])
        p[0]["breaklist"] = ir.mergeList(p[1]["breaklist"], p[9]["breaklist"])
        p[0]["continuelist"] = ir.mergeList(p[1]["continuelist"], p[9]["continuelist"])


def p_alt_if_stmt(p):
    '''alt_if_stmt : alt_if_stmt_without_else ENDIF SEMICOLON
                 | alt_if_stmt_without_else ELSE goto_marker jump_marker COLON inner_stmts ENDIF SEMICOLON'''
    if(len(p)==4):
        # p[0] = {"if_stmt":[p[1],p[2],p[3]]}
        p[0] = p[1]
        p[0]["nextlist"] = ir.mergeList(p[1]["falselist"], p[1]["nextlist"])

    else:
        p[0] = {}
        # p[0] = {"if_stmt":[p[1],p[2],p[3],p[4],p[5],p[6]]}
        ir.backpatch(p[1]["falselist"], p[4]["quad"])

        # 
        p[0]["nextlist"] = ir.mergeList(ir.mergeList(p[1]["nextlist"], p[3]["nextlist"]), p[6]["nextlist"])
        p[0]["breaklist"] = ir.mergeList(p[1]["breaklist"], p[6]["breaklist"])
        p[0]["continuelist"] = ir.mergeList(p[1]["continuelist"], p[6]["continuelist"])


def p_alt_if_stmt_without_else(p):
    '''alt_if_stmt_without_else : IF LPAREN expr RPAREN COLON jump_marker inner_stmts
                              | alt_if_stmt_without_else ELSEIF goto_marker LPAREN jump_marker expr RPAREN COLON jump_marker inner_stmts'''

    if(len(p)==8):
        # p[0] = {"if_stmt":[p[1],p[2],p[3],p[4],p[5],p[6]]}
        p[0] = {}
        ir.backpatch(p[3]["truelist"], p[6]["quad"])
        p[0]["falselist"] = p[3]["falselist"]
        p[0]["nextlist"] = p[7]["nextlist"]
        p[0]["breaklist"] = p[7]["breaklist"]
        p[0]["continuelist"] = p[7]["continuelist"]
 # | if_stmt_without_else ELSEIF goto_marker LPAREN jump_marker expr RPAREN jump_marker stmt'''
 
    else:
        p[0] = {}
        # p[0] = {"if_stmt":[p[1],p[2],p[3],p[4],p[5],p[6],p[7]]}
        ir.backpatch(p[6]["truelist"], p[9]["quad"])
        ir.backpatch(p[1]["falselist"], p[5]["quad"])
        p[0]["falselist"] = p[6]["falselist"]
        p[0]["nextlist"] = ir.mergeList(ir.mergeList(p[1]["nextlist"], p[3]["nextlist"]), p[10]["nextlist"])
        p[0]["breaklist"] = ir.mergeList(p[1]["breaklist"], p[10]["breaklist"])
        p[0]["continuelist"] = ir.mergeList(p[1]["continuelist"], p[10]["continuelist"])

#--------------------------------------------------------------------------------------------------------

# --- While Stmt

def p_stmt_while(p):
    'stmt : WHILE LPAREN jump_marker expr jump_marker RPAREN while_stmt goto_marker'
    global ir
    p[0] = {}
    looplist = ir.mergeList(p[7]["continuelist"], p[7]["nextlist"], p[8]["nextlist"])
    ir.backpatch(looplist, p[3]["quad"])
    ir.backpatch(p[4]["truelist"], p[5]["quad"])
    p[0]["nextlist"] = ir.mergeList(p[4]["falselist"], p[7]["breaklist"])

def p_while_stmt(p):
    '''while_stmt : stmt
                       | COLON inner_stmts ENDWHILE SEMICOLON'''
    if(len(p)==2):
        p[0] = p[1]
    else:
        p[0] = p[2]

#--------------------------------------------------------------------------------------------------------

# --- Do while

def p_stmt_do_while(p):
    'stmt : DO stmt WHILE LPAREN expr RPAREN SEMICOLON'
    p[0] = {"stmt":[p[1],p[2],p[3],p[4],p[5],p[6],p[7]]}
#--------------------------------------------------------------------------------------------------------

# --- for loop

def p_stmt_for(p):
    'stmt : FOR LPAREN for_expr SEMICOLON jump_marker for_expr SEMICOLON jump_marker for_expr goto_marker RPAREN jump_marker for_stmt goto_marker'
    p[0] = {}
    global ir
    # set the true list of for_expr_2 to go to for_stmt
    ir.backpatch(p[6]["truelist"], p[12]["quad"])

    # put the update next to start of the for_expr_2 (conditional expression)
    ir.backpatch(p[10]["nextlist"], p[5]["quad"])

    # put the loop to update condition
    looplist = ir.mergeList(p[13]["nextlist"], p[13]["continuelist"], p[14]["nextlist"])
    ir.backpatch(looplist, p[8]["quad"])
    p[0]["nextlist"] = ir.mergeList(p[6]["falselist"], p[13]["breaklist"])
def p_for_expr(p):
    '''for_expr : empty
                | non_empty_for_expr'''
    p[0] = p[1]


def p_non_empty_for_expr(p):
    '''non_empty_for_expr : non_empty_for_expr COMMA expr
                          | expr'''
    global ir
    p[0] = {}
    if(len(p)==2):
        # it may be a conditional expr, so pass it on
        p[0] = p[1]

def p_for_stmt(p):
    '''for_stmt : stmt
                     | COLON inner_stmts ENDFOR SEMICOLON'''
    if(len(p)==2):
        p[0] = p[1]
    else:
        p[0] = p[2]

#--------------------------------------------------------------------------------------------------------

# --- foreach

def p_stmt_foreach(p):
    'stmt : FOREACH LPAREN expr AS foreach_var foreach_arg RPAREN foreach_stmt'
    p[0] = {"stmt":[p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8]]}

def p_foreach_var(p):
    '''foreach_var : IDENTIFIER
                        | BIT_AND IDENTIFIER'''
    if(len(p)==2):
        p[0] = p[1]
    else:
        p[0] = {"foreach_var":[p[1],p[2]]}

def p_foreach_arg(p):
    '''foreach_arg : empty
                            | DOUBLE_ARROW foreach_var'''
    if(len(p)==2):
        p[0] = p[1]
    else:
        p[0] = {"foreach_arg":[p[1],p[2]]}

def p_foreach_stmt(p):
    '''foreach_stmt : stmt
                         | COLON inner_stmts ENDFOREACH SEMICOLON'''
    if(len(p)==2):
        p[0] = p[1]
    else:
        p[0] = {"foreach_stmt":[p[1],p[2],p[3],p[4]]}

#--------------------------------------------------------------------------------------------------------

# --- SWITCH Case

def p_stmt_switch(p):
    'stmt : SWITCH LPAREN expr RPAREN goto_marker switch_stmt jump_marker'

    global  ir
    p[0] ={}
    exprs = p[6]["expr"]
    jumps = p[6]["jumps"]
    default = p[6]["default"]
    # backpack the goto_marker to current quad
    ir.backpatch(p[5]["nextlist"], p[7]["quad"])
    # emit the conditions for switch cases
    for i in range(len(exprs)):
        expr = exprs[i]
        jump = jumps[i]
        isDefault = default[i]
        if not isDefault:
            ir.emitCjump("==", p[3], expr, str(jump))
        else:
            ir.emitUjump(str(jump))
    p[0]["nextlist"] = p[6]["nextlist"]


def p_switch_stmt(p):
    '''switch_stmt : LBRACE case_stmt RBRACE
                        | LBRACE SEMICOLON case_stmt RBRACE'''
    p[0] = {}
    if(len(p)==4):
        # pass the synthesized attributes
        p[0] = p[2]
    else:
        p[0] = p[3]

def p_switch_stmt_colon(p):
    '''switch_stmt : COLON case_stmt ENDSWITCH SEMICOLON
                        | COLON SEMICOLON case_stmt ENDSWITCH SEMICOLON'''
    if(len(p)==5):
        p[0] = p[2]
    else:
        p[0] = p[3]

def p_case_stmt(p):
    '''case_stmt : empty
                 | case_stmt CASE expr case_separator jump_marker inner_stmts
                 | case_stmt DEFAULT case_separator jump_marker inner_stmts'''
    global ir
    p[0] = {}
    if(len(p)==2):
        # we are at empty state
        # create an empty nextlist
        p[0]["nextlist"] = ir.makeList()
        p[0]["expr"] = []
        p[0]["jumps"] = []
        p[0]["default"] = []
    else:
        if(len(p)==7):
            # attach the expression for later usage
            p[0]["expr"] = p[1]["expr"] +  [p[3]]
            p[0]["jumps"] = p[1]["jumps"] +  [p[5]["quad"]]
            p[0]["default"] = p[1]["default"] + [False]
            p[0]["nextlist"] = ir.mergeList(p[1]["nextlist"], p[6]["breaklist"])
        else:
            p[0]["expr"] = p[1]["expr"] +  ["Subhojit"]
            p[0]["jumps"] = p[1]["jumps"] +  [p[4]["quad"]]
            p[0]["default"] = p[1]["default"] + [True]
            p[0]["nextlist"] = ir.mergeList(p[1]["nextlist"], p[5]["breaklist"])

        # combine the next list of all the children

def p_case_separator(p):
    '''case_separator : COLON
                      | SEMICOLON'''
    p[0] = p[1]

#--------------------------------------------------------------------------------------------------------

# -- break, continue, return, global, static, echo

#-- Break----
def p_stmt_break(p):
    '''stmt : BREAK  goto_marker SEMICOLON
                 | BREAK expr goto_marker SEMICOLON'''
    global ir
    p[0] = {}
    if(len(p)==4):
        p[0]["breaklist"] = p[2]["nextlist"]
    else:
        p[0] = {"stmt":[p[1],p[2],p[3]]}

#-------------

#-- Continue--
def p_stmt_continue(p):
    '''stmt : CONTINUE goto_marker SEMICOLON
                 | CONTINUE expr  goto_marker SEMICOLON'''
    global ir
    p[0] = {}
    if(len(p)==4):
        p[0]["continuelist"] = p[2]["nextlist"]
    else:
        p[0] = {"stmt":[p[1],p[2],p[3]]}


#-------------

#-- Return----
def p_stmt_return(p):
    '''stmt : RETURN SEMICOLON
                 | RETURN expr SEMICOLON'''
    global ir

    if(len(p)==3):
        ir.emitRet()
    else:
        ir.emitRet(p[2])
        p[0] = p[2]

#-------------

#-- Global----
def p_stmt_global(p):
    'stmt : GLOBAL global_var_list SEMICOLON'
    p[0] = {"stmt":[p[1],p[2],p[3]]}

def p_global_var_list(p):
    '''global_var_list : global_var_list COMMA IDENTIFIER
                       | IDENTIFIER'''
    if(len(p)==2):
        p[0] = p[1]
    else:
        p[0] = {"global_var_list":[p[1],p[2],p[3]]}

#-------------

#-- Static----
def p_stmt_static(p):
    'stmt : STATIC static_var_list SEMICOLON'
    p[0] = {"stmt":[p[1],p[2],p[3]]}

def p_static_var_list(p):
    '''static_var_list : static_var_list COMMA static_var
                       | static_var'''
    if(len(p)==2):
        p[0] = p[1]
    else:
        p[0] = {"stmt":[p[1],p[2],p[3]]}


def p_static_var(p):
    '''static_var : IDENTIFIER EQUAL scalar
                  | IDENTIFIER'''
    if(len(p)==2):
        p[0] = p[1]
    else:
        p[0] = {"static_var":[p[1],p[2],p[3]]}

#-------------

#--- ECHO ----
def p_stmt_echo(p):
    'stmt : ECHO echo_expr_list SEMICOLON'
    # p[0] = {"stmt":[p[1],p[2],p[3]]}
    global ir
    ir.emitEcho()
    p[0] = p[2]
def p_echo_expr_list(p):
    '''echo_expr_list : echo_expr_list COMMA expr
                      | expr'''
    if(len(p)==4):
        p[0] = {"echo_expr_list":[p[1],p[2],p[3]]}
    else:
        global ir
        ir.emitParams(p[1])
        p[0] = p[1]
        p[0]["numParams"] = 1
#-------------

#--------------------------------------------------------------------------------------------------------

# --- stmt block

def p_stmt_block(p):
    'stmt : LBRACE inner_stmts RBRACE'
    p[0] = p[2]

def p_stmt_empty(p):
    'stmt : SEMICOLON'
    # p[0] = p[1]

def p_stmt_expr(p):
    'stmt : expr SEMICOLON'
    p[0] = p[1]

def p_inner_stmts(p):
    '''inner_stmts : inner_stmts jump_marker inner_stmt
                            | empty'''

    p[0] = {}
    global ir
    if len(p) == 4 :
        ir.backpatch(p[1]["nextlist"], p[2]["quad"])
        # attach the information from inner_stmt to inner_stmts
        p[0]["nextlist"] = p[3]["nextlist"]
        p[0]["breaklist"] = ir.mergeList(p[1]["breaklist"], p[3]["breaklist"])
        p[0]["continuelist"] = ir.mergeList(p[1]["continuelist"], p[3]["continuelist"])
    else:
        p[0]["nextlist"] = ir.makeList()
        p[0]["breaklist"] = ir.makeList()
        p[0]["continuelist"] = ir.makeList()

def p_inner_stmt(p):
    '''inner_stmt : stmt
               | func_decl'''
    global ir
    p[0] = {}
    # get the nextlist if it exists other create one
    try:
        p[0]["nextlist"] = p[1]["nextlist"]
    except:
        p[0]["nextlist"] = ir.makeList()
    # get the breaklist if there is any else create one
    try:
        p[0]["breaklist"] = p[1]["breaklist"]
    except Exception as e:
        p[0]["breaklist"] = ir.makeList()

    # get the continuelist if there is any else create one
    try:
        p[0]["continuelist"] = p[1]["continuelist"]
    except Exception as e:
        p[0]["continuelist"] = ir.makeList()

#--------------------------------------------------------------------------------------------------------

# --- expression defined

def p_expr_variable(p):
    'expr : variable'
    p[0] = p[1]

def p_variable(p):
    '''variable : base_var
              | func_call'''
    p[0] = p[1]

def p_func_call(p):
    'func_call : STRING LPAREN func_params RPAREN'
    # p[0] = {"func_call":[p[1],p[2],p[3],p[4]]}
    global stm
    global ir
    name = p[1]
    attrs = stm.lookup(name)
    if(not attrs):
        print 'undefined function ' + name + '!'
    else:
        tmp = ir.newTemp()
        p[0] = {"place" : tmp , "type": "int" , "offset" : 4}
        ir.emitCall(attrs["lineNumber"], p[3]["numParams"],p[0])

def p_func_params(p):
    '''func_params : func_params COMMA func_param
                                  | func_param
                                  | empty'''
    p[0] = {}
    if(len(p)==2):
        try:
            tmp = p[1]["place"] 
            p[0]["numParams"] = 1
        except:
            p[0]["numParams"] = 0            
    else:
        p[0]["numParams"]  = p[1]["numParams"] + p[3]["numParams"]
        # p[0] = {"func_params":[p[1],p[2],p[3]]}

def p_func_param(p):
    '''func_param : expr
                    | BIT_AND variable'''
    global ir
    p[0] = {}
    if(len(p)==2):
        ir.emitParams(p[1])
        p[0] = p[1]
        p[0]["numParams"] =  1
    else:
        p[0] = {"func_param":[p[1],p[2]]}


def p_reference_variable_array_offset(p):
    '''base_var : base_var LBRACKET dim_offset RBRACKET
                   | base_var LBRACE expr RBRACE
                   | IDENTIFIER'''

    if(len(p)==2):
        global stm
        name = p[1]
        attrs = stm.lookup(name)
        symType = None
        offset = 0
        if not attrs:
            stm.insert(p[1], symType, offset)
        else:
            symType = attrs["type"]
            offset = attrs["offset"]
        p[0] = {"place": p[1], "type": symType, "offset": offset}
    else:
        p[0] = {"base_var":[p[1],p[2],p[3],p[4]]}

def p_dim_offset(p):
    '''dim_offset : expr
                | empty'''
    p[0] = p[1]

def p_expr_assign(p):
    '''expr : base_var EQUAL expr
          | base_var EQUAL BIT_AND expr'''

    # SYMBOL TABLE STUFF
    # lookup for the variable into symbol table
    global stm

    name = p[1]["place"]
    attrs = stm.lookup(name)
    symType = attrs["type"]
    offset = attrs["offset"]
    
    if(len(p)==4):
        if not p[3]["type"]:
            print "Variable "+ p[3]["place"]+" used before assignment."
        if(symType and symType != p[3]["type"]):
            print "type casting error for "+ str(name) + " and " + p[3]["place"]
        else:
            # update the type and offset for the variable
            symType = p[3]["type"]
            offset = p[3]["offset"]
            stm.setAttr(name, "place", name)
            stm.setAttr(name, "type", symType)
            stm.setAttr(name, "offset", offset)
            p[1]["type"] = symType
            p[1]["offset"] = offset
            
        global ir
        ir.emitCopy(p[1], p[3])
    else:
        p[0] = {"expr":[p[1],p[2],p[3],p[4]]}

def p_expr_clone(p):
    'expr : CLONE expr'
    p[0] = {"expr":[p[1],p[2]]}

# ----- SCALAR -----------------------

def p_scalar(p):
    '''scalar : CONST_DECIMAL
              | CONST_DOUBLE
              | CONST_STRING
              | NULL
              | TRUE
              | FALSE'''
    p[0] = {'scalar':[p[1]]}

def p_scalar_unary_op(p):
    '''scalar : PLUS scalar
              | MINUS scalar'''
    p[0] = {"scalar":[p[1],p[2]]}

def p_scalar_array(p):
    'scalar : ARRAY LPAREN scalar_array_pair_list RPAREN'
    p[0] = {"scalar":[p[1],p[2],p[3],p[4]]}

def p_static_array_pair_list(p):
    '''scalar_array_pair_list : empty
                            | scalar_non_empty_array_pair_list possible_comma'''
    if(len(p)==2):
        p[0] = p[1]
    else:
        p[0] = {"scalar_list":[p[1],p[2]]}

def p_static_non_empty_array_pair_list_item(p):
    '''scalar_non_empty_array_pair_list : scalar_non_empty_array_pair_list COMMA scalar
                                      | scalar'''
    if(len(p)==2):
        p[0] = p[1]
    else:
        p[0] = {"scalar_list":[p[1],p[2],p[3]]}

def p_static_non_empty_array_pair_list_pair(p):
    '''scalar_non_empty_array_pair_list : scalar_non_empty_array_pair_list COMMA scalar DOUBLE_ARROW scalar
                                        | scalar DOUBLE_ARROW scalar'''
    if(len(p)==6):
        p[0] = {"scalar_list":[p[1],p[2],p[3],p[4],p[5]]}
    else:
        p[0] = {"scalar_list":[p[1],p[2],p[3]]}

#---------------------------------------
def p_expr_array(p):
    'expr : ARRAY LPAREN array_pair_list RPAREN'
    p[0] = {"expr":[p[1],p[2],p[3],p[4]]}

def p_array_pair_list(p):
    '''array_pair_list : empty
                       | non_empty_array_pair_list possible_comma'''
    if(len(p)==2):
        p[0] = p[1]
    else:
        p[0] = {"array_list":[p[1],p[2]]}

def p_possible_comma(p):
    '''possible_comma : empty
                      | COMMA'''
    p[0] = p[1]

def p_non_empty_array_pair_list_item(p):
    '''non_empty_array_pair_list : non_empty_array_pair_list COMMA BIT_AND variable
                                 | non_empty_array_pair_list COMMA expr
                                 | BIT_AND variable
                                 | expr'''
    if(len(p)==5):
        p[0] = {"array_list":[p[1],p[2],p[3],p[4]]}
    elif(len(p)==4):
        p[0] = {"array_list":[p[1],p[2],p[3]]}
    elif(len(p)==3):
        p[0] = {"array_list":[p[1],p[2]]}
    else:
        p[0] = p[1]


def p_non_empty_array_pair_list_pair(p):
    '''non_empty_array_pair_list : non_empty_array_pair_list COMMA expr DOUBLE_ARROW BIT_AND variable
                                 | non_empty_array_pair_list COMMA expr DOUBLE_ARROW expr
                                 | expr DOUBLE_ARROW BIT_AND variable
                                 | expr DOUBLE_ARROW expr
                                 '''
    if(len(p)==7):
        p[0] = {"array_list":[p[1],p[2],p[3],p[4],p[5],p[6]]}
    elif(len(p)==6):
        p[0] = {"array_list":[p[1],p[2],p[3],p[4],p[5]]}
    elif(len(p)==5):
        p[0] = {"array_list":[p[1],p[2],p[3],p[4]]}
    elif(len(p)==4):
        p[0] = {"array_list":[p[1],p[2],p[3]]}

# def p_non_empty_array_list(p):
#     '''non_empty_array_list : non_empty_array_list COMMA scalar
#                                 | scalar'''
#     if(len(p)==2):
#         p[0] = p[1]
#     else:
#         p[0] = {"array_pair_list":[p[1],p[2],p[3]]}


def p_expr_assign_op(p):
    '''expr : variable PLUS_EQ expr
          | variable MINUS_EQ expr
          | variable MULTIPLY_EQ expr
          | variable DIVIDE_EQ expr
          | variable DOT_EQ expr
          | variable MOD_EQ expr'''
    global ir
    if p[1]["type"] != p[3]["type"]:
        print "Type mismatch for operator "+ p[2] + " with operands "+ p[1]["place"] + " and "+ p[3]["place"]
    ir.emitAssgn(p[2][0], p[1], p[1], p[3])
    p[0] = p[1]


def p_expr_arith(p):
    '''expr : expr DOT expr
          | expr PLUS expr
          | expr MINUS expr
          | expr MULT expr
          | expr DIV expr
          | expr MOD expr
          | expr BIT_OR expr
          | expr BIT_XOR expr
          | expr BIT_AND expr
          | expr BIT_LSHIFT expr
          | expr BIT_RSHIFT expr'''
    global ir
    name = ir.newTemp()
    if p[1]["type"] != p[3]["type"]:
        print "Type mismatch for operator "+ p[2] + " with operands "+ p[1]["place"] + " and "+ p[3]["place"]
    symType = p[1]["type"]
    offset = p[1]["offset"]
    global stm
    stm.insert(name, symType, offset)

    p[0] = {"place": name, "type": symType, "offset": offset}

    ir.emitAssgn(p[2], p[0], p[1], p[3])

def p_expr_binary_op(p):
    '''expr : expr AND_OP jump_marker expr
          | expr OR_OP jump_marker expr'''

    global ir
    p[0] = {}
    if p[2] == "||":
        ir.backpatch(p[1]["falselist"], p[3]["quad"])
        p[0]["truelist"] = ir.mergeList(p[1]["truelist"], p[4]["truelist"])
        p[0]["falselist"] = p[4]["falselist"]
    else:
        ir.backpatch(p[1]["truelist"], p[3]["quad"])
        p[0]["truelist"] = p[4]["truelist"]
        p[0]["falselist"] = ir.mergeList(p[1]["falselist"], p[4]["falselist"])

def p_expr_binary_relop(p):
    '''expr : expr IDENTICAL  expr
          | expr NOT_IDENTICAL  expr
          | expr EQ_EQ  expr
          | expr NOT_EQ  expr
          | expr LESSER  expr
          | expr LESSER_EQ  expr
          | expr GREATER  expr
          | expr GREATER_EQ  expr
          | expr INSTANCEOF  expr'''
    global ir
    p[0] = {}
    p[0]["truelist"] = ir.makeList(ir.nextquad)
    p[0]["falselist"] = ir.makeList(ir.nextquad+1)
    ir.emitCjump(p[2], p[1], p[3])
    ir.emitUjump()

def p_expr_unary_op(p):
    '''expr : PLUS expr
          | MINUS expr
          | BIT_NOT expr
          | NOT expr'''
    if p[1] == "!":
        p[0] = {}
        p[0]["falselist"] = p[2]["truelist"]
        p[0]["truelist"] = p[2]["falselist"]

    else:
        global ir
        name = ir.newTemp()
        symType = p[2]["type"]
        offset = p[2]["offset"]
        global stm
        stm.insert(name, symType, offset)

        p[0] = {"place": name, "type": symType, "offset": offset}
        ir.emitAssgn( p[1], p[0],
            {"place": "0", "type": "CONST_DECIMAL", "offset": 4},
            p[2])

def p_exp_scalar(p):
    '''expr : CONST_DECIMAL
          | CONST_DOUBLE
          | CONST_STRING
          | NULL
          | TRUE
          | FALSE'''
    global ir
    global stm
    tmp = ir.newTemp()
    p[0] = {}
    p[0]["type"] = p[1]["type"]
    p[0]["offset"] = p[1]["offset"]
    p[0]["place"] = tmp

    p[1]["type"] = "const_"+p[1]["type"]
    ir.emitCopy(p[0], p[1])
    if(p[1]["place"].upper() == "TRUE"):
        p[0]["truelist"] = ir.makeList(ir.nextquad)
        ir.emitUjump()
    elif(p[1]["place"].upper() == "FALSE"):
        p[0]["falselist"] = ir.makeList(ir.nextquad)
        ir.emitUjump()


def p_expr_ternary_op(p):
    'expr : expr COND_OP jump_marker  expr goto_marker  jump_marker COLON expr'
    global ir
    global stm
    p[0] = {}
    p[0]["place"] = ir.newTemp()
    # send the truelist to first expr
    ir.backpatch(p[1]["truelist"], p[3]["quad"])
    # send the falselist to second expr
    ir.backpatch(p[1]["falselist"], p[6]["quad"])

    # after evaluvating expressions, we have into two different variables
    # p[4]["place"] and p[8]["place"]
    # Now we need to assign these variables to p[0]["place"]
    secondAsgnList = ir.makeList(ir.nextquad)
    ir.emitUjump()

    # assgn to the first value
    ir.backpatch(p[5]["nextlist"], ir.nextquad)
    ir.emitCopy(p[0], p[4])

    firstAsgnList = ir.makeList(ir.nextquad)
    ir.emitUjump()

    # assgn to second value
    ir.backpatch(secondAsgnList, ir.nextquad)
    ir.emitCopy(p[0], p[8])

    ir.backpatch(firstAsgnList, ir.nextquad)

    p[0]["type"] = p[4]["type"]
    p[0]["offset"] = p[4]["offset"]
    stm.insert(p[0]["place"], p[0]["type"], p[0]["offset"])

def p_expr_pre_incdec(p):
    '''expr : INC variable
          | DEC variable'''
    global ir
    ir.emitAssgn(p[1][0], p[2], p[2], {"place":"1", "type": "int", "offset": 4})
    p[0] = p[2]

def p_expr_post_incdec(p):
    '''expr : variable INC
          | variable DEC'''
    p[0] = p[1]

def p_expr_empty(p):
    'expr : EMPTY LPAREN expr RPAREN'
    p[0] = {"expr":[p[2],p[3],p[4]]}

def p_expr_eval(p):
    'expr : EVAL LPAREN expr RPAREN'
    p[0] = {"expr":[p[1],p[2],p[3],p[4]]}

def p_expr_group(p):
    'expr : LPAREN expr RPAREN'
    p[0] = {"expr":[p[1],p[2],p[3]]}

def p_expr_include(p):
    'expr : INCLUDE expr'
    p[0] = {"expr":[p[1],p[2]]}

def p_expr_include_once(p):
    'expr : INCLUDE_ONCE expr'
    p[0] = {"expr":[p[1],p[2]]}

def p_expr_require(p):
    'expr : REQUIRE expr'
    p[0] = {"expr":[p[1],p[2]]}

def p_expr_require_once(p):
    'expr : REQUIRE_ONCE expr'
    p[0] = {"expr":[p[1],p[2]]}

def p_expr_exit(p):
    '''expr : EXIT
          | EXIT LPAREN RPAREN
          | EXIT LPAREN expr RPAREN'''
    if(len(p)==2):
        p[0] = p[1]
    elif(len(p)==4):
        p[0] = {"expr":[p[1],p[2],p[3]]}
    else:
        p[0] = {"expr":[p[1],p[2],p[3],p[4]]}

def p_expr_print(p):
    'expr : PRINT expr'
    p[0] = {"expr":[p[1],p[2]]}

def p_jump_marker(p):
    'jump_marker : empty'
    global ir
    p[0] ={}
    p[0]["quad"] = ir.nextquad

def p_goto_marker(p):
    'goto_marker : empty'
    global ir
    p[0] ={}
    p[0]["nextlist"] = ir.makeList(ir.nextquad)
    ir.emitUjump()
#--------------------------------------------------------------------------------------------------------

def p_empty(p):
    'empty : '
    p[0] = ''
def p_error(t):
    if t:
        raise SyntaxError('invalid syntax', (None, t.lineno, None, t))
    else:
        raise SyntaxError('unexpected EOF while parsing', (None, None, None, None))

def runIR():
    parser = yacc.yacc(debug=True)

    inputStr = open(sys.argv[1], "r")
    data= ""
    for line in inputStr:
      data += (line)

    log = logging.getLogger()


    result = parser.parse(data,debug=0)
    # result = parser.parse(data,debug=log)
    return result

if __name__ == '__main__':
    result = runIR()
    result["ir"].printTac()