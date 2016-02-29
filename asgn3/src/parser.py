import os, sys, lexer, logging, ply.yacc as yacc

tokens = lexer.tokens

precedence = (
  ('left', 'INCLUDE', 'INCLUDE_ONCE', 'EVAL', 'REQUIRE', 'REQUIRE_ONCE'),
  ('left', 'COMMA'),
  ('left', 'BIT_OR'),
  ('left', 'BIT_XOR'),
  ('left', 'BIT_AND'),
  ('left', 'EQUAL', 'PLUS_EQ','MINUS_EQ', 'MULTIPLY_EQ', 'DIVIDE_EQ', 'MOD_EQ', 'DOT_EQ'),
  ('left', 'COND_OP', 'COLON'),
  ('left', 'AND_OP', 'OR_OP'),
  ('left', 'BIT_RSHIFT', 'BIT_LSHIFT'),
  ('left', 'PLUS', 'MINUS', 'MULT', 'DIV', 'MOD', 'DOT'),
  ('left', 'ENDIF'),
  ('right', 'PRINT'),
  ('right', 'NOT'),
  ('right', 'BIT_NOT', 'INC', 'DEC',),
  ('right', 'LBRACKET'),
  ('right', 'STATIC', 'ABSTRACT', 'FINAL', 'PRIVATE', 'PROTECTED', 'PUBLIC'),
  ('nonassoc', 'EQ_EQ', 'IDENTICAL', 'NOT_IDENTICAL', 'LESSER', 'LESSER_EQ', 'GREATER', 'GREATER_EQ'),
  ('nonassoc', 'INSTANCEOF', 'NEW', 'CLONE'),
  )

tree = [];

def p_start(p):
    'start : top_statement_list'
  
    p[0] = p[1]
    tree.append({"start":[p[1]]}) 

def p_top_statement_list(p):
    '''top_statement_list : top_statement_list top_statement
                        | empty '''
    if len(p) == 3 :
        p[0] = [p[1],p[2]]        
        # tree.top_statement_list = [p[1],p[2]]
        tree.append({"top_statement_list":[p[1],p[2]]})
    else:         
        p[0] = p[1]
        tree.append({"top_statement_list":[p[1]]})

def p_top_statement(p):
    '''top_statement : function_declaration_statement
    '''
    p[0] = p[1]
    tree.append({"top_statement":[p[1]]})


def p_top_statement(p):
    '''top_statement : statement'''
    p[0] = p[1]
    tree.append({"top_statement":[p[1]]})


#--------------------------------------------------------------------------------------------------------                 

# --- var $a, $b, $c

def p_top_statement_constant(p):
    'top_statement : VAR constant_declarations SEMICOLON'

    # tree.p_top_statement = {p[1],p[2],p[3]}
    p[0] =  [p[1],p[2],p[3]]
    tree.append({"top_statement":[p[1],p[2],p[3]]})
  

def p_constant_declarations(p):
    '''constant_declarations : constant_declarations COMMA constant_declaration
                             | constant_declaration'''
    if (len(p) == 4) :
        p[0] = [p[1],p[2],p[3]]
        tree.append({"constant_declarations":[p[1],p[2],p[3]]})
    else:
        p[0] = p[1]
        tree.append({"constant_declarations":[p[1]]})
         
def p_constant_declaration(p):
    '''constant_declaration : IDENTIFIER EQUAL variable
                  | IDENTIFIER'''                                    
    if (len(p) == 4) :
        p[0] = [p[1],p[2],p[3]]
        tree.append({"constant_declaration":[p[1],p[2],p[3]]})
    else:
        p[0] = p[1]
        tree.append({"constant_declaration":[p[1]]})

#--------------------------------------------------------------------------------------------------------                 

# --- Function

def p_function_declaration_statement(p):
    'function_declaration_statement : FUNCTION STRING LPAREN parameter_list RPAREN LBRACE inner_statement_list RBRACE'
    p[0] = [p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8]]
    tree.append({"function_declaration_statement":[p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8]]})

def p_parameter_list(p):
    '''parameter_list : empty'''    

    p[0] = p[1]
    tree.append({"function_declaration_statement":[p[1]]})

def p_parameter_list(p):
    '''parameter_list : parameter_list COMMA parameter
                      | parameter'''
    if(len(p)==2):                      
        p[0] = p[1]
        tree.append({"parameter_list":[p[1]]})
    else:
        p[0] = [p[1],p[2],p[3]]
        tree.append({"parameter_list":[p[1],p[2],p[3]]})


def p_parameter(p):
    '''parameter : IDENTIFIER
                 | BIT_AND IDENTIFIER
                 | IDENTIFIER EQUAL scalar
                 | BIT_AND IDENTIFIER EQUAL scalar'''

    if(len(p)==2):                      
        p[0] = p[1]
        tree.append({"parameter":[p[1]]})
    elif(len(p)==3):
        p[0] = [p[1],p[2]]
        tree.append({"parameter":[p[1],p[2]]})
    elif(len(p)==4):
        p[0] = [p[1],p[2],p[3]]
        tree.append({"parameter":[p[1],p[2],p[3]]})
    else:
        p[0] = [p[1],p[2],p[3],p[4]]
        tree.append({"parameter":[p[1],p[2],p[3],p[4]]})
    
#--------------------------------------------------------------------------------------------------------                 

# --- IF ELSE

def p_statement_if(p):
    '''statement : IF LPAREN expr RPAREN statement elseif_list else_single
                 | IF LPAREN expr RPAREN COLON inner_statement_list new_elseif_list new_else_single ENDIF SEMICOLON'''


def p_elseif_list(p):
    '''elseif_list : empty
                   | elseif_list ELSEIF LPAREN expr RPAREN statement'''

def p_else_single(p):
    '''else_single : empty
                   | ELSE statement'''

def p_new_elseif_list(p):
    '''new_elseif_list : empty
                       | new_elseif_list ELSEIF LPAREN expr RPAREN COLON inner_statement_list'''

def p_new_else_single(p):
    '''new_else_single : empty
                       | ELSE COLON inner_statement_list'''

#--------------------------------------------------------------------------------------------------------                 

# --- While Statement

def p_statement_while(p):
    'statement : WHILE LPAREN expr RPAREN while_statement'

def p_while_statement(p):
    '''while_statement : statement
                       | COLON inner_statement_list ENDWHILE SEMICOLON'''  

#--------------------------------------------------------------------------------------------------------                 

# --- Do while

def p_statement_do_while(p):
    'statement : DO statement WHILE LPAREN expr RPAREN SEMICOLON'

#--------------------------------------------------------------------------------------------------------                 

# --- for loop

def p_statement_for(p):
    'statement : FOR LPAREN for_expr SEMICOLON for_expr SEMICOLON for_expr RPAREN for_statement'

def p_for_expr(p):
    '''for_expr : empty
                | non_empty_for_expr'''

def p_non_empty_for_expr(p):
    '''non_empty_for_expr : non_empty_for_expr COMMA expr
                          | expr'''


def p_for_statement(p):
    '''for_statement : statement
                     | COLON inner_statement_list ENDFOR SEMICOLON'''

#--------------------------------------------------------------------------------------------------------                 

# --- foreach

def p_statement_foreach(p):
    'statement : FOREACH LPAREN expr AS foreach_variable foreach_optional_arg RPAREN foreach_statement'

def p_foreach_variable(p):
    '''foreach_variable : IDENTIFIER
                        | BIT_AND IDENTIFIER'''

def p_foreach_optional_arg(p):
    '''foreach_optional_arg : empty
                            | DOUBLE_ARROW foreach_variable'''

def p_foreach_statement(p):
    '''foreach_statement : statement
                         | COLON inner_statement_list ENDFOREACH SEMICOLON'''

#--------------------------------------------------------------------------------------------------------                 

# --- SWITCH Case

def p_statement_switch(p):
    'statement : SWITCH LPAREN expr RPAREN switch_case_list'


def p_switch_case_list(p):
    '''switch_case_list : LBRACE case_list RBRACE
                        | LBRACE SEMICOLON case_list RBRACE'''  
                       
def p_switch_case_list_colon(p):
    '''switch_case_list : COLON case_list ENDSWITCH SEMICOLON
                        | COLON SEMICOLON case_list ENDSWITCH SEMICOLON'''

def p_case_list(p):
    '''case_list : empty
                 | case_list CASE expr case_separator inner_statement_list
                 | case_list DEFAULT case_separator inner_statement_list'''


def p_case_separator(p):
    '''case_separator : COLON
                      | SEMICOLON'''    
    p[0] = p[1]
    tree.append({"case_separator":[p[1]]})


#--------------------------------------------------------------------------------------------------------                 

# -- break, continue, return, global, static, echo

#-- Break----
def p_statement_break(p):
    '''statement : BREAK SEMICOLON
                 | BREAK expr SEMICOLON'''
#-------------

#-- Continue--
def p_statement_continue(p):
    '''statement : CONTINUE SEMICOLON
                 | CONTINUE expr SEMICOLON'''                
#-------------

#-- Return----
def p_statement_return(p):
    '''statement : RETURN SEMICOLON
                 | RETURN expr SEMICOLON'''
#-------------

#-- Global----
def p_statement_global(p):
    'statement : GLOBAL global_var_list SEMICOLON'

def p_global_var_list(p):
    '''global_var_list : global_var_list COMMA IDENTIFIER
                       | IDENTIFIER'''
#-------------

#-- Static----
def p_statement_static(p):
    'statement : STATIC static_var_list SEMICOLON'

def p_static_var_list(p):
    '''static_var_list : static_var_list COMMA static_var
                       | static_var'''

def p_static_var(p):
    '''static_var : IDENTIFIER EQUAL scalar
                  | IDENTIFIER'''
    if(len(p)==2):                  
        p[0] = p[1]
        tree.append({"static_var":[p[1]]})
    else:
        p[0] = [p[1],p[2],p[3]]
        tree.append({"static_var":[p[1],p[2],p[3]]})

#-------------

#--- ECHO ----
def p_statement_echo(p):
    'statement : ECHO echo_expr_list SEMICOLON'

def p_echo_expr_list(p):
    '''echo_expr_list : echo_expr_list COMMA expr
                      | expr'''
#-------------


#--------------------------------------------------------------------------------------------------------                 

# --- statement block

def p_statement_block(p):
    'statement : LBRACE inner_statement_list RBRACE'

def p_statement_empty(p):
    'statement : SEMICOLON'          
    p[0] = p[1]                                                                                                              
    tree.append({"statement":[p[1]]})

def p_statement_expr(p):
    'statement : expr SEMICOLON'
    p[0] = p[1]
    tree.append({"statement":[p[1],p[2]]})

def p_inner_statement_list(p):
    '''inner_statement_list : inner_statement_list inner_statement
                            | empty'''

def p_inner_statement(p):
    '''inner_statement : statement
               | function_declaration_statement'''

#--------------------------------------------------------------------------------------------------------                 

# --- expression defined

def p_expr_variable(p):
    'expr : variable'
    p[0] = p[1]
    tree.append({"expr":[p[1]]})

def p_variable(p):
    '''variable : base_variable
          | function_call'''
    p[0] = p[1]
    tree.append({"variable":[p[1]]})

def p_function_call(p):
  'function_call : STRING LPAREN function_call_parameter_list RPAREN'


def p_function_call_parameter_list(p):
    '''function_call_parameter_list : function_call_parameter_list COMMA function_call_parameter
                                    | function_call_parameter
                                    | empty'''

def p_function_call_parameter(p):
    '''function_call_parameter : expr
                               | BIT_AND variable'''


def p_reference_variable_array_offset(p):
    '''base_variable : base_variable LBRACKET dim_offset RBRACKET
           | base_variable LBRACE expr RBRACE
             | IDENTIFIER'''
    if(len(p)==2):
        p[0] = p[1]
        tree.append({"base_variable":[p[1]]})
    else:
        p[0] = [p[1],p[2],p[3],p[4]]
        tree.append({"base_variable":[p[1],p[2],p[3],p[4]]})

def p_dim_offset(p):
    '''dim_offset : expr
                  | empty'''
    p[0] = p[1]
    tree.append({"dim_offset":[p[1]]})

def p_expr_assign(p):
    '''expr : variable EQUAL expr
            | variable EQUAL BIT_AND expr'''
    if(len(p)==4):  
        p[0] = [p[1],p[2],p[3]]            
        tree.append({"expr":[p[1],p[2],p[3]]})
    else:
        p[0] = [p[1],p[2],p[3],p[4]]
        tree.append({"expr":[p[1],p[2],p[3],p[4]]})
        
def p_expr_clone(p):
  'expr : CLONE expr'

def p_expr_list_assign(p):
    'expr : LIST LPAREN assignment_list RPAREN EQUAL expr'

def p_assignment_list(p):
    '''assignment_list : assignment_list COMMA assignment_list_element
                       | assignment_list_element'''

def p_assignment_list_element(p):
    '''assignment_list_element : variable
                               | empty
                               | LIST LPAREN assignment_list RPAREN'''

def p_expr_scalar(p):
    'expr : scalar'
    p[0] = p[1]
    tree.append({"expr":[p[1]]})

def p_scalar(p):
    '''scalar : CONST_DECIMAL
        | CONST_DOUBLE
        | CONST_STRING
        | NULL'''    
    
    p[0] = p[1]
    tree.append({"scalar":[p[1]]})

def p_expr_array(p):
    'expr : ARRAY LPAREN array_pair_list RPAREN'

def p_array_pair_list(p):
    '''array_pair_list : empty
                       | non_empty_array_pair_list possible_comma'''

def p_possible_comma(p):
    '''possible_comma : empty
                      | COMMA'''
    p[0] = p[1]
    tree.append({"expr":[p[1]]})

def p_non_empty_array_pair_list_item(p):
    '''non_empty_array_pair_list : non_empty_array_pair_list COMMA BIT_AND variable
                                 | non_empty_array_pair_list COMMA expr
                                 | BIT_AND variable
                                 | expr'''

def p_non_empty_array_pair_list_pair(p):
    '''non_empty_array_pair_list : non_empty_array_pair_list COMMA expr DOUBLE_ARROW BIT_AND variable
                                 | non_empty_array_pair_list COMMA expr DOUBLE_ARROW expr
                                 | expr DOUBLE_ARROW BIT_AND variable
                                 | expr DOUBLE_ARROW expr'''                                 


def p_expr_assign_op(p):
    '''expr : variable PLUS_EQ expr
        | variable MINUS_EQ expr
            | variable MULTIPLY_EQ expr
            | variable DIVIDE_EQ expr
            | variable DOT_EQ expr
            | variable MOD_EQ expr'''
    p[0] = [p[1],p[2],p[3]]
    tree.append({"expr":[p[1],p[2],p[3]]})

def p_expr_binary_op(p):
    '''expr : expr AND_OP expr
            | expr OR_OP expr
            | expr AND expr
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
    p[0] = [p[1],p[2],p[3]]
    tree.append({"expr":[p[1],p[2],p[3]]})

def p_expr_unary_op(p):
    '''expr : PLUS expr
            | MINUS expr
            | BIT_NOT expr
            | NOT expr'''
    p[0] = [p[1],p[2]]
    tree.append({"expr":[p[1],p[2]]})

def p_expr_ternary_op(p):
    'expr : expr COND_OP expr COLON expr'
    p[0] = [p[1],p[2],p[3],p[4],p[5]]
    tree.append({"expr":[p[1],p[2],p[3],p[4],p[5]]})
    
def p_expr_pre_incdec(p):
    '''expr : INC variable
            | DEC variable'''

def p_expr_post_incdec(p):
    '''expr : variable INC
            | variable DEC'''

def p_expr_empty(p):
    'expr : EMPTY LPAREN expr RPAREN'
    p[0] = [p[1],p[2],p[3],p[4]]
    tree.append({"expr":[p[1],p[2],p[3],p[4]]})
    
def p_expr_eval(p):
    'expr : EVAL LPAREN expr RPAREN'

def p_expr_group(p):
    'expr : LPAREN expr RPAREN'

def p_expr_include(p):
    'expr : INCLUDE expr'

def p_expr_include_once(p):
    'expr : INCLUDE_ONCE expr'

def p_expr_require(p):
    'expr : REQUIRE expr'

def p_expr_require_once(p):
    'expr : REQUIRE_ONCE expr'

def p_expr_exit(p):
  '''expr : EXIT
      | EXIT LPAREN RPAREN
      | EXIT LPAREN expr RPAREN'''

def p_expr_print(p):
  'expr : PRINT expr'
#--------------------------------------------------------------------------------------------------------                 

def p_empty(p):
    'empty : '
    p[0] = None
    tree.append({"empty":['']})

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

print(result)

print (tree)

