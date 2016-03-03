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
  ('left', 'ELSEIF'),
  ('left', 'ELSE'),
  ('left', 'ENDIF'),
  ('right', 'STATIC', 'ABSTRACT', 'FINAL', 'PRIVATE', 'PROTECTED', 'PUBLIC'),
  )

def p_start(p):
    'start : top_statement_list'
    p[0] = {"start":[p[1]]}    

def p_top_statement_list(p):
    '''top_statement_list : top_statement_list top_statement
                        | empty '''
    if len(p) == 3 :        
        p[0] = {"top_statement_list":[p[1],p[2]]}
    else:        
        p[0] = p[1]

def p_top_statement(p):
    '''top_statement : statement
                   | function_declaration_statement'''
    p[0] = p[1]

#--------------------------------------------------------------------------------------------------------                 

# --- var $a, $b, $c

def p_top_statement_constant(p):
    '''top_statement : VAR constant_declarations SEMICOLON
            | constant_declarations SEMICOLON'''
    if(len(p)==4):
        p[0] =  {"top_statement": [p[1],p[2],p[3]]}
    else:
        p[0] =  {"top_statement": [p[1],p[2]]}

def p_constant_declarations(p):
    '''constant_declarations : constant_declarations COMMA constant_declaration
                             | constant_declaration'''
    if (len(p) == 4) :        
        p[0] = {"constant_declarations":[p[1],p[2],p[3]]}
    else:        
        p[0] = p[1]

def p_constant_declaration(p):
    '''constant_declaration : IDENTIFIER EQUAL expr
                            | IDENTIFIER'''      
    if (len(p) == 4) :        
        p[0] = {"constant_declaration":[p[1],p[2],p[3]]}
    else:
        p[0] = p[1] 

#--------------------------------------------------------------------------------------------------------                 

# --- Function

def p_function_declaration_statement(p):
    'function_declaration_statement : FUNCTION STRING LPAREN parameter_list RPAREN LBRACE inner_statement_list RBRACE'
    p[0] = {"function_decl_statement":[p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8]]}

def p_parameter_list(p):
    '''parameter_list : parameter_list COMMA parameter
                      | parameter
                      | empty'''
    if(len(p)==2):                      
        p[0] = p[1]
    else:        
        p[0] = {"parameter_list": [p[1],p[2],p[3]]}

def p_parameter(p):
    '''parameter : IDENTIFIER
                 | BIT_AND IDENTIFIER
                 | IDENTIFIER EQUAL scalar
                 | BIT_AND IDENTIFIER EQUAL scalar'''
    if(len(p)==2):                      
        p[0] = {"parameter":[p[1]]}

    elif(len(p)==3):        
        p[0] = {"parameter":[p[1],p[2]]}
    elif(len(p)==4):
        p[0] = {"parameter":[p[1],p[2],p[3]]}
    else:        
        p[0] = {"parameter":[p[1],p[2],p[3],p[4]]}

#--------------------------------------------------------------------------------------------------------                 

# --- IF ELSE

def p_statement_if(p):
    '''statement : if_stmt
               | alt_if_stmt'''
    p[0] = p[1]             
def p_if_stmt(p):
    '''if_stmt : if_stmt_without_else ELSE statement'''
    p[0] = {"if_stmt":[p[1],p[2],p[3]]}    

def p_if_stmt_without_else(p):
    '''if_stmt_without_else : IF LPAREN expr RPAREN statement
                          | if_stmt_without_else ELSEIF LPAREN expr RPAREN statement'''
    if(len(p)==6):
        p[0] = {"if_stmt_without_else":[p[1],p[2],p[3],p[4],p[5]]}
    else:
        p[0] = {"if_stmt_without_else":[p[1],p[2],p[3],p[4],p[5],p[6]]}    


def p_alt_if_stmt(p):
    '''alt_if_stmt : alt_if_stmt_without_else ENDIF SEMICOLON
                 | alt_if_stmt_without_else ELSE COLON inner_statement_list ENDIF SEMICOLON'''
    if(len(p)==4):
        p[0] = {"alt_if_stmt":[p[1],p[2],p[3]]}
    else:
        p[0] = {"alt_if_stmt":[p[1],p[2],p[3],p[4],p[5],p[6]]}    

def p_alt_if_stmt_without_else(p):
    '''alt_if_stmt_without_else : IF LPAREN expr RPAREN COLON inner_statement_list
                              | alt_if_stmt_without_else ELSEIF LPAREN expr RPAREN COLON inner_statement_list'''
    if(len(p)==7):
        p[0] = {"alt_if_stmt_without_else":[p[1],p[2],p[3],p[4],p[5],p[6]]}
    else:
        p[0] = {"alt_if_stmt_without_else":[p[1],p[2],p[3],p[4],p[5],p[6],p[7]]}    


#--------------------------------------------------------------------------------------------------------                 

# --- While Statement

def p_statement_while(p):
    'statement : WHILE LPAREN expr RPAREN while_statement'
    p[0] = {"statement":[p[1],p[2],p[3],p[4],p[5]]}

def p_while_statement(p):
    '''while_statement : statement
                       | COLON inner_statement_list ENDWHILE SEMICOLON'''  
    if(len(p)==2):
        p[0] = {"while_statement":[p[1]]}
    else:
        p[0] = {"while_statement":[p[1],p[2],p[3],p[4]]}

#--------------------------------------------------------------------------------------------------------                 

# --- Do while

def p_statement_do_while(p):
    'statement : DO statement WHILE LPAREN expr RPAREN SEMICOLON'
    p[0] = {"statement":[p[1],p[2],p[3],p[4],p[5],p[6],p[7]]}

#--------------------------------------------------------------------------------------------------------                 

# --- for loop

def p_statement_for(p):
    'statement : FOR LPAREN for_expr SEMICOLON for_expr SEMICOLON for_expr RPAREN for_statement'
    p[0] = {"statement":[p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9]]}

def p_for_expr(p):
    '''for_expr : empty
                | non_empty_for_expr'''
    p[0] = {"for_expr":[p[1]]}


def p_non_empty_for_expr(p):
    '''non_empty_for_expr : non_empty_for_expr COMMA expr
                          | expr'''
    if(len(p)==4):                          
        p[0] = {"non_empty_for_expr":[p[1],p[2],p[3]]}
    else:
        p[0] = {"non_empty_for_expr":[p[1]]}

def p_for_statement(p):
    '''for_statement : statement
                     | COLON inner_statement_list ENDFOR SEMICOLON'''
    if(len(p)==2):                          
        p[0] = {"for_statement":[p[1]]}
    else:
        p[0] = {"for_statement":[p[1],p[2],p[3],p[4]]}

#--------------------------------------------------------------------------------------------------------                 

# --- foreach

def p_statement_foreach(p):
    'statement : FOREACH LPAREN expr AS foreach_variable foreach_optional_arg RPAREN foreach_statement'
    p[0] = {"statement":[p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8]]}

def p_foreach_variable(p):
    '''foreach_variable : IDENTIFIER
                        | BIT_AND IDENTIFIER'''
    if(len(p)==2):                          
        p[0] = p[1]
    else:
        p[0] = {"foreach_variable":[p[1],p[2]]}

def p_foreach_optional_arg(p):
    '''foreach_optional_arg : empty
                            | DOUBLE_ARROW foreach_variable'''
    if(len(p)==2):
        p[0] = p[1]
    else:
        p[0] = {"foreach_optional_arg":[p[1],p[2]]}

def p_foreach_statement(p):
    '''foreach_statement : statement
                         | COLON inner_statement_list ENDFOREACH SEMICOLON'''
    if(len(p)==2):
        p[0] = p[1]
    else:
        p[0] = {"foreach_statement":[p[1],p[2],p[3],p[4]]}

#--------------------------------------------------------------------------------------------------------                 

# --- SWITCH Case

def p_statement_switch(p):
    'statement : SWITCH LPAREN expr RPAREN switch_case_list'
    p[0] = {"statement":[p[1],p[2],p[3],p[4],p[5]]}

def p_switch_case_list(p):
    '''switch_case_list : LBRACE case_list RBRACE
                        | LBRACE SEMICOLON case_list RBRACE'''  
    if(len(p)==4):
        p[0] = {"switch_case_list":[p[1],p[2],p[3]]}
    else:
        p[0] = {"switch_case_list":[p[1],p[2],p[3],p[4]]}

def p_switch_case_list_colon(p):
    '''switch_case_list : COLON case_list ENDSWITCH SEMICOLON
                        | COLON SEMICOLON case_list ENDSWITCH SEMICOLON'''
    if(len(p)==5):
        p[0] = {"switch_case_list":[p[1],p[2],p[3],p[4]]}
    else:
        p[0] = {"switch_case_list":[p[1],p[2],p[3],p[4],p[5]]}

def p_case_list(p):
    '''case_list : empty
                 | case_list CASE expr case_separator inner_statement_list
                 | case_list DEFAULT case_separator inner_statement_list'''
    if(len(p)==2):
        p[0] = p[1]
    elif(len(p)==6):
        p[0] = {"case_list":[p[1],p[2],p[3],p[4],p[5]]}
    else:
        p[0] = {"case_list":[p[1],p[2],p[3],p[4]]}

def p_case_separator(p):
    '''case_separator : COLON
                      | SEMICOLON'''    
    p[0] = p[1]

#--------------------------------------------------------------------------------------------------------                 

# -- break, continue, return, global, static, echo

#-- Break----
def p_statement_break(p):
    '''statement : BREAK SEMICOLON
                 | BREAK expr SEMICOLON'''
    if(len(p)==3):
        p[0] = {"statement":[p[1],p[2]]}
    else:
        p[0] = {"statement":[p[1],p[2],p[3]]}

#-------------

#-- Continue--
def p_statement_continue(p):
    '''statement : CONTINUE SEMICOLON
                 | CONTINUE expr SEMICOLON'''                
    if(len(p)==3):
        p[0] = {"statement":[p[1],p[2]]}
    else:
        p[0] = {"statement":[p[1],p[2],p[3]]}

#-------------

#-- Return----
def p_statement_return(p):
    '''statement : RETURN SEMICOLON
                 | RETURN expr SEMICOLON'''
    if(len(p)==3):
        p[0] = {"statement":[p[1],p[2]]}
    else:
        p[0] = {"statement":[p[1],p[2],p[3]]}

#-------------

#-- Global----
def p_statement_global(p):
    'statement : GLOBAL global_var_list SEMICOLON'
    p[0] = {"statement":[p[1],p[2],p[3]]}

def p_global_var_list(p):
    '''global_var_list : global_var_list COMMA IDENTIFIER
                       | IDENTIFIER'''
    if(len(p)==2):
        p[0] = p[1]
    else:
        p[0] = {"statement":[p[1],p[2],p[3]]}

#-------------

#-- Static----
def p_statement_static(p):
    'statement : STATIC static_var_list SEMICOLON'
    p[0] = {"statement":[p[1],p[2],p[3]]}

def p_static_var_list(p):
    '''static_var_list : static_var_list COMMA static_var
                       | static_var'''
    if(len(p)==2):
        p[0] = p[1]
    else:
        p[0] = {"statement":[p[1],p[2],p[3]]}


def p_static_var(p):
    '''static_var : IDENTIFIER EQUAL scalar
                  | IDENTIFIER'''
    if(len(p)==2):                  
        p[0] = p[1]
    else:        
        p[0] = {"static_var":[p[1],p[2],p[3]]}

#-------------

#--- ECHO ----
def p_statement_echo(p):
    'statement : ECHO echo_expr_list SEMICOLON'
    p[0] = {"statement":[p[1],p[2],p[3]]}

def p_echo_expr_list(p):
    '''echo_expr_list : echo_expr_list COMMA expr
                      | expr'''
    if(len(p)==4):                  
        p[0] = {"echo_expr_list":[p[1],p[2],p[3]]}
    else:        
        p[0] = p[1]
#-------------

#--------------------------------------------------------------------------------------------------------                 

# --- statement block

def p_statement_block(p):
    'statement : LBRACE inner_statement_list RBRACE'
    p[0] = {"statement":[p[1],p[2],p[3]]}

def p_statement_empty(p):
    'statement : SEMICOLON'                                                                                                                    
    p[0] = p[1]                                  

def p_statement_expr(p):
    'statement : expr SEMICOLON'
    p[0] = {"statement":[p[1],p[2]]} 

def p_inner_statement_list(p):
    '''inner_statement_list : inner_statement_list inner_statement
                            | empty'''
    if(len(p)==2):
        p[0] = p[1] 
    else:
        p[0] = {"inner_statement_list":[p[1],p[2]]}

def p_inner_statement(p):
    '''inner_statement : statement
               | function_declaration_statement'''
    p[0] = p[1] 

#--------------------------------------------------------------------------------------------------------                 

# --- expression defined

def p_expr_variable(p):
    'expr : variable'
    p[0] = p[1] 

def p_variable(p):
    '''variable : base_variable
              | function_call'''
    p[0] = p[1]

def p_function_call(p):
    'function_call : STRING LPAREN function_call_parameter_list RPAREN'
    p[0] = {"function_call":[p[1],p[2],p[3],p[4]]}

def p_function_call_parameter_list(p):
    '''function_call_parameter_list : function_call_parameter_list COMMA function_call_parameter
                                  | function_call_parameter
                                  | empty'''
    if(len(p)==2):
        p[0] = p[1] 
    else:
        p[0] = {"function_call_parameter_list":[p[1],p[2],p[3]]}

def p_function_call_parameter(p):
    '''function_call_parameter : expr
                               | BIT_AND variable'''
    if(len(p)==2):
        p[0] = p[1] 
    else:
        p[0] = {"function_call_parameter":[p[1],p[2]]}


def p_reference_variable_array_offset(p):
    '''base_variable : base_variable LBRACKET dim_offset RBRACKET
                   | base_variable LBRACE expr RBRACE
                   | IDENTIFIER'''

    if(len(p)==2):
        p[0] = p[1]
    else:        
        p[0] = {"base_variable":[p[1],p[2],p[3],p[4]]}

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
        p[0] = {"scalar_array_pair_list":[p[1],p[2]]}

def p_static_non_empty_array_pair_list_item(p):
    '''scalar_non_empty_array_pair_list : scalar_non_empty_array_pair_list COMMA scalar
                                      | scalar'''
    if(len(p)==2):          
        p[0] = p[1]
    else:
        p[0] = {"scalar_non_empty_array_pair_list":[p[1],p[2],p[3]]}

def p_static_non_empty_array_pair_list_pair(p):
    '''scalar_non_empty_array_pair_list : scalar_non_empty_array_pair_list COMMA scalar DOUBLE_ARROW scalar
                                        | scalar DOUBLE_ARROW scalar'''
    if(len(p)==6):          
        p[0] = {"scalar_non_empty_array_pair_list":[p[1],p[2],p[3],p[4],p[5]]}
    else:
        p[0] = {"scalar_non_empty_array_pair_list":[p[1],p[2],p[3]]}

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
        p[0] = {"array_pair_list":[p[1],p[2]]}

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
        p[0] = {"non_empty_array_pair_list":[p[1],p[2],p[3],p[4]]}
    elif(len(p)==4): 
        p[0] = {"non_empty_array_pair_list":[p[1],p[2],p[3]]}
    elif(len(p)==3):
        p[0] = {"non_empty_array_pair_list":[p[1],p[2]]}
    else:
        p[0] = p[1]


def p_non_empty_array_pair_list_pair(p):
    '''non_empty_array_pair_list : non_empty_array_pair_list COMMA expr DOUBLE_ARROW BIT_AND variable
                                 | non_empty_array_pair_list COMMA expr DOUBLE_ARROW expr
                                 | expr DOUBLE_ARROW BIT_AND variable
                                 | expr DOUBLE_ARROW expr
                                 '''                                 
    if(len(p)==7): 
        p[0] = {"non_empty_array_pair_list":[p[1],p[2],p[3],p[4],p[5],p[6]]}
    elif(len(p)==6): 
        p[0] = {"non_empty_array_pair_list":[p[1],p[2],p[3],p[4],p[5]]}
    elif(len(p)==5):
        p[0] = {"non_empty_array_pair_list":[p[1],p[2],p[3],p[4]]}
    elif(len(p)==4):
        p[0] = {"non_empty_array_pair_list":[p[1],p[2],p[3]]}
 
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
def p_error(t):
    if t:
        raise SyntaxError('invalid syntax', (None, t.lineno, None, t.value))
    else:
        raise SyntaxError('unexpected EOF while parsing', (None, None, None, None))

parser = yacc.yacc(debug=True)

inputStr = open(sys.argv[1], "r")
data= ""
for line in inputStr:
  data += (line)
# try:
#    s = data
# except EOFError:
#    pass
# # if not s: continue
log = logging.getLogger()

result = parser.parse(data,debug=log)

# print(json.dumps(result))
file = open('output.json', 'w+')
input = json.dumps(result)
file.write(input)
# create the parse table and print it to index.html file
ParseTree(json.loads(input)).create_html("index.html")