import os, sys, lexer, logging, ply.yacc as yacc, json
from print_table import ParseTree

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
    'start : stmt_list'
    p[0] = {"start":[p[1]]}    

def p_stmt_list(p):
    '''stmt_list : stmt_list top_stmt
                        | empty '''
    if len(p) == 3 :        
        p[0] = {"stmt_list":[p[1],p[2]]}
    else:        
        p[0] = p[1]

def p_top_stmt(p):
    '''top_stmt : stmt
                   | func_decl'''
    p[0] = p[1]

#--------------------------------------------------------------------------------------------------------                 

# --- var $a, $b, $c

def p_stmt_const(p):
    'top_stmt : VAR const_decls SEMICOLON'
    p[0] =  {"top_stmt": [p[1],p[2],p[3]]}


def p_const_decls(p):
    '''const_decls : const_decls COMMA const_decl
                             | const_decl'''
    if (len(p) == 4) :        
        p[0] = {"const_decls":[p[1],p[2],p[3]]}
    else:        
        p[0] = p[1]

def p_const_decl(p):
    '''const_decl : IDENTIFIER EQUAL expr
                            | IDENTIFIER'''      
    if (len(p) == 4) :        
        p[0] = {"const_decl":[p[1],p[2],p[3]]}
    else:
        p[0] = p[1] 

#--------------------------------------------------------------------------------------------------------                 

# --- Function

def p_func_decl(p):
    'func_decl : FUNCTION STRING LPAREN params RPAREN LBRACE inner_stmts RBRACE'
    p[0] = {"func_decl":[p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8]]}

def p_params(p):
    '''params : params COMMA param
                      | param
                      | empty'''
    if(len(p)==2):                      
        p[0] = p[1]
    else:        
        p[0] = {"params": [p[1],p[2],p[3]]}

def p_param(p):
    '''param : IDENTIFIER
                 | BIT_AND IDENTIFIER
                 | IDENTIFIER EQUAL scalar
                 | BIT_AND IDENTIFIER EQUAL scalar'''
    if(len(p)==2):                      
        p[0] = {"param":[p[1]]}

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
             | if_stmt_without_else ELSE stmt'''
    if(len(p)==4):
        p[0] = {"if_stmt":[p[1],p[2],p[3]]}    
    else:
        print str(len(p)) + 'sss'
        p[0] = {"if_stmt":[p[1]]} 

            
def p_if_stmt_without_else(p):
    '''if_stmt_without_else : IF LPAREN expr RPAREN stmt
                          | if_stmt_without_else ELSEIF LPAREN expr RPAREN stmt'''
    if(len(p)==6):
        p[0] = {"if_stmt":[p[1],p[2],p[3],p[4],p[5]]}
    else:
        p[0] = {"if_stmt":[p[1],p[2],p[3],p[4],p[5],p[6]]}    


def p_alt_if_stmt(p):
    '''alt_if_stmt : alt_if_stmt_without_else ENDIF SEMICOLON
                 | alt_if_stmt_without_else ELSE COLON inner_stmts ENDIF SEMICOLON'''
    if(len(p)==4):
        p[0] = {"if_stmt":[p[1],p[2],p[3]]}
    else:
        p[0] = {"if_stmt":[p[1],p[2],p[3],p[4],p[5],p[6]]}    

def p_alt_if_stmt_without_else(p):
    '''alt_if_stmt_without_else : IF LPAREN expr RPAREN COLON inner_stmts
                              | alt_if_stmt_without_else ELSEIF LPAREN expr RPAREN COLON inner_stmts'''
    if(len(p)==7):
        p[0] = {"if_stmt":[p[1],p[2],p[3],p[4],p[5],p[6]]}
    else:
        p[0] = {"if_stmt":[p[1],p[2],p[3],p[4],p[5],p[6],p[7]]}    


#--------------------------------------------------------------------------------------------------------                 

# --- While Stmt

def p_stmt_while(p):
    'stmt : WHILE LPAREN expr RPAREN while_stmt'
    p[0] = {"stmt":[p[1],p[2],p[3],p[4],p[5]]}

def p_while_stmt(p):
    '''while_stmt : stmt
                       | COLON inner_stmts ENDWHILE SEMICOLON'''  
    if(len(p)==2):
        p[0] = {"while_stmt":[p[1]]}
    else:
        p[0] = {"while_stmt":[p[1],p[2],p[3],p[4]]}

#--------------------------------------------------------------------------------------------------------                 

# --- Do while

def p_stmt_do_while(p):
    'stmt : DO stmt WHILE LPAREN expr RPAREN SEMICOLON'
    p[0] = {"stmt":[p[1],p[2],p[3],p[4],p[5],p[6],p[7]]}
#--------------------------------------------------------------------------------------------------------                 

# --- for loop

def p_stmt_for(p):
    'stmt : FOR LPAREN for_expr SEMICOLON for_expr SEMICOLON for_expr RPAREN for_stmt'
    p[0] = {"stmt":[p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9]]}

def p_for_expr(p):
    '''for_expr : empty
                | non_empty_for_expr'''
    p[0] = p[1] 


def p_non_empty_for_expr(p):
    '''non_empty_for_expr : non_empty_for_expr COMMA expr
                          | expr'''
    if(len(p)==4):                          
        p[0] = {"for_expr":[p[1],p[2],p[3]]}
    else:
        p[0] = {"for_expr":[p[1]]}

def p_for_stmt(p):
    '''for_stmt : stmt
                     | COLON inner_stmts ENDFOR SEMICOLON'''
    if(len(p)==2):                          
        p[0] = {"for_stmt":[p[1]]}
    else:
        p[0] = {"for_stmt":[p[1],p[2],p[3],p[4]]}

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
    'stmt : SWITCH LPAREN expr RPAREN switch_stmt'
    p[0] = {"stmt":[p[1],p[2],p[3],p[4],p[5]]}

def p_switch_stmt(p):
    '''switch_stmt : LBRACE case_stmt RBRACE
                        | LBRACE SEMICOLON case_stmt RBRACE'''  
    if(len(p)==4):
        p[0] = {"switch_stmt":[p[1],p[2],p[3]]}
    else:
        p[0] = {"switch_stmt":[p[1],p[2],p[3],p[4]]}

def p_switch_stmt_colon(p):
    '''switch_stmt : COLON case_stmt ENDSWITCH SEMICOLON
                        | COLON SEMICOLON case_stmt ENDSWITCH SEMICOLON'''
    if(len(p)==5):
        p[0] = {"switch_stmt":[p[1],p[2],p[3],p[4]]}
    else:
        p[0] = {"switch_stmt":[p[1],p[2],p[3],p[4],p[5]]}

def p_case_stmt(p):
    '''case_stmt : empty
                 | case_stmt CASE expr case_separator inner_stmts
                 | case_stmt DEFAULT case_separator inner_stmts'''
    if(len(p)==2):
        p[0] = p[1]
    elif(len(p)==6):
        p[0] = {"case_stmt":[p[1],p[2],p[3],p[4],p[5]]}
    else:
        p[0] = {"case_stmt":[p[1],p[2],p[3],p[4]]}

def p_case_separator(p):
    '''case_separator : COLON
                      | SEMICOLON'''    
    p[0] = p[1]

#--------------------------------------------------------------------------------------------------------                 

# -- break, continue, return, global, static, echo

#-- Break----
def p_stmt_break(p):
    '''stmt : BREAK SEMICOLON
                 | BREAK expr SEMICOLON'''
    if(len(p)==3):
        p[0] = {"stmt":[p[1],p[2]]}
    else:
        p[0] = {"stmt":[p[1],p[2],p[3]]}

#-------------

#-- Continue--
def p_stmt_continue(p):
    '''stmt : CONTINUE SEMICOLON
                 | CONTINUE expr SEMICOLON'''                
    if(len(p)==3):
        p[0] = {"stmt":[p[1],p[2]]}
    else:
        p[0] = {"stmt":[p[1],p[2],p[3]]}

#-------------

#-- Return----
def p_stmt_return(p):
    '''stmt : RETURN SEMICOLON
                 | RETURN expr SEMICOLON'''
    if(len(p)==3):
        p[0] = {"stmt":[p[1],p[2]]}
    else:
        p[0] = {"stmt":[p[1],p[2],p[3]]}

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
    p[0] = {"stmt":[p[1],p[2],p[3]]}

def p_echo_expr_list(p):
    '''echo_expr_list : echo_expr_list COMMA expr
                      | expr'''
    if(len(p)==4):                  
        p[0] = {"echo_expr_list":[p[1],p[2],p[3]]}
    else:        
        p[0] = p[1]
#-------------

#--------------------------------------------------------------------------------------------------------                 

# --- stmt block

def p_stmt_block(p):
    'stmt : LBRACE inner_stmts RBRACE'
    p[0] = {"stmt":[p[1],p[2],p[3]]}

def p_stmt_empty(p):
    'stmt : SEMICOLON'                                                                                                                    
    p[0] = p[1]                                  

def p_stmt_expr(p):
    'stmt : expr SEMICOLON'
    p[0] = {"stmt":[p[1],p[2]]} 

def p_inner_stmts(p):
    '''inner_stmts : inner_stmts inner_stmt
                            | empty'''
    if(len(p)==2):
        p[0] = p[1] 
    else:
        p[0] = {"inner_stmts":[p[1],p[2]]}

def p_inner_stmt(p):
    '''inner_stmt : stmt
               | func_decl'''
    p[0] = p[1] 

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
    p[0] = {"func_call":[p[1],p[2],p[3],p[4]]}

def p_func_params(p):
    '''func_params : func_params COMMA func_param
                                  | func_param
                                  | empty'''
    if(len(p)==2):
        p[0] = p[1] 
    else:
        p[0] = {"func_params":[p[1],p[2],p[3]]}

def p_func_param(p):
    '''func_param : expr
                    | BIT_AND variable'''
    if(len(p)==2):
        p[0] = p[1] 
    else:
        p[0] = {"func_param":[p[1],p[2]]}


def p_reference_variable_array_offset(p):
    '''base_var : base_var LBRACKET dim_offset RBRACKET
                   | base_var LBRACE expr RBRACE
                   | IDENTIFIER'''

    if(len(p)==2):
        p[0] = p[1]
    else:        
        p[0] = {"base_var":[p[1],p[2],p[3],p[4]]}

def p_dim_offset(p):
    '''dim_offset : expr
                | empty'''
    p[0] = p[1]

def p_expr_assign(p):
    '''expr : variable EQUAL expr
          | variable EQUAL BIT_AND expr'''
    if(len(p)==4):          
        p[0] = {"expr":[p[1],p[2],p[3]]}
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
    p[0] = {"expr":[p[1],p[2],p[3]]}

def p_expr_binary_op(p):
    '''expr : expr AND_OP expr
          | expr OR_OP expr
          | expr BIT_OR expr
          | expr BIT_XOR expr
          | expr BIT_AND expr
          | expr DOT expr
          | expr PLUS expr
          | expr MINUS expr
          | expr MULT expr
          | expr DIV expr
          | expr BIT_LSHIFT expr
          | expr BIT_RSHIFT expr
          | expr MOD expr
          | expr IDENTICAL expr
          | expr NOT_IDENTICAL expr
          | expr EQ_EQ expr
          | expr NOT_EQ expr
          | expr LESSER expr
          | expr LESSER_EQ expr
          | expr GREATER expr
          | expr GREATER_EQ expr
          | expr INSTANCEOF expr'''
    p[0] = {"expr":[p[1],p[2],p[3]]}


def p_expr_unary_op(p):
    '''expr : PLUS expr
          | MINUS expr
          | BIT_NOT expr
          | NOT expr'''
    p[0] = {"expr":[p[1],p[2]]}

def p_exp_scalar(p):
    '''expr : CONST_DECIMAL
          | CONST_DOUBLE
          | CONST_STRING
          | NULL
          | TRUE
          | FALSE'''  
    p[0] = p[1]          
def p_expr_ternary_op(p):
    'expr : expr COND_OP expr COLON expr'
    p[0] = {"expr":[p[1],p[2],p[3],p[4],p[5]]}

def p_expr_pre_incdec(p):
    '''expr : INC variable
          | DEC variable'''
    p[0] = {"expr":[p[1],p[2]]}

def p_expr_post_incdec(p):
    '''expr : variable INC
          | variable DEC'''
    p[0] = {"expr":[p[1],p[2]]}

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
#--------------------------------------------------------------------------------------------------------                 

def p_empty(p):
    'empty : '
    p[0] = ''
def p_error(p):
    if p:
        raise SyntaxError('invalid syntax', (None, p.lineno, None, p))
    else:
        raise SyntaxError('unexpected EOF while parsing', (None, None, None, None))

parser = yacc.yacc(debug=True)

inputStr = open(sys.argv[1], "r")
data= ""
for line in inputStr:
  data += (line)

log = logging.getLogger()

file = sys.argv[1]
filename = file.split('test')[2]
filename = filename.split('.')[0]
result = parser.parse(data,debug=log)
file = open('output.json', 'w+')
file.write(json.dumps(result))

ParseTree(result).create_html("test"+filename+".html")