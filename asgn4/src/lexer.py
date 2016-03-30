
import sys
import ply.lex as lex
from tabulate import tabulate

reserved_keywords = ['__HALT_COMPILER', 'ABSTRACT', 'AND', 'ARRAY', 'AS', 'BREAK', 'CALLABLE', 'CASE', 'CATCH', 'CLASS', 'CLONE', 'CONST', 'CONTINUE', 'DECLARE', 'DEFAULT', 'DIE', 'DO', 'ECHO', 'ELSE', 'ELSEIF', 'EMPTY', 'ENDDECLARE', 'ENDFOR', 'ENDFOREACH', 'ENDIF', 'ENDSWITCH', 'ENDWHILE', 'EVAL', 'EXIT', 'EXTENDS', 'FINAL', 'FOR', 'FOREACH', 'FUNCTION', 'GLOBAL', 'GOTO', 'IF', 'IMPLEMENTS', 'INCLUDE', 'INCLUDE_ONCE', 'INSTANCEOF', 'INSTEADOF', 'INTERFACE', 'ISSET', 'LIST', 'NAMESPACE', 'NEW', 'OR', 'PRINT', 'PRIVATE', 'PROTECTED', 'PUBLIC', 'REQUIRE', 'REQUIRE_ONCE', 'RETURN', 'STATIC', 'SWITCH', 'THROW', 'TRAIT', 'TRY', 'UNSET', 'USE', 'VAR', 'WHILE', 'XOR','NULL','TRUE','FALSE']

predefined_const = ['__CLASS__', '__DIR__', '__FILE__', '__FUNCTION__', '__LINE__', '__METHOD__', '__NAMESPACE__', '__TRAIT__']

literal = ['IDENTIFIER','STRING','CONST_DECIMAL','CONST_HEX', 'CONST_OCTAL', 'CONST_BINARY', 'CONST_DOUBLE','CONST_STRING', 'START_TAG', 'END_TAG']

		#arithematic operators :   + - * / %  **
operators = ['PLUS','MINUS','MULT','DIV','MOD', 'EXPONENT',

		#equal operators:  = += -= *= /= %=
		'EQUAL', 'PLUS_EQ', 'MINUS_EQ','MULTIPLY_EQ','DIVIDE_EQ','MOD_EQ',

		#comparison operators: == === !=    !==  > < >= <=
		'EQ_EQ','IDENTICAL','NOT_EQ' ,'NOT_IDENTICAL','GREATER','LESSER','GREATER_EQ','LESSER_EQ',

		# operators: ++ --  && || ! . .=
		'INC','DEC','AND_OP','OR_OP','NOT','DOT','DOT_EQ',

		# bitwise operators: | & ^ ~ << >>
		'BIT_OR', 'BIT_AND', 'BIT_XOR', 'BIT_NOT', 'BIT_LSHIFT', 'BIT_RSHIFT',

		# other operators: ; ( ) [ ] { } -> , ? :
		'SEMICOLON','COLON','LPAREN','RPAREN','LBRACKET','RBRACKET','LBRACE','RBRACE','ACCESS_OP','COMMA',
		'COND_OP', 'COND_COLON','QUOTE','DOUBLE_ARROW',
		]

tokens = reserved_keywords+ predefined_const +literal + operators


# php start and end tags
def t_START_TAG(t):
	r'((<\?php)|(<\?))'

def t_END_TAG(t):
	r'(\?>)'


#reserved keywords are case insensitive so if If iF are same but not variables.
def t_IDENTIFIER(t):
	r'[\$]+[a-zA-Z_][a-zA-Z_0-9]*'
	# t.value = {'ID' : t.value}
	return t

def t_STRING(t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'
	if((t.value).upper() in reserved_keywords): # Check for reserved words
		t.type = t.value.upper()
	elif((t.value).upper() in predefined_const): # Check for reserved words
		t.type = t.value.upper()
 	return t


#floating constant defination
def t_CONST_DOUBLE(t):
    r'(([0-9]*[.]*[0-9]+)([eE][-]?)([0-9]+))|([0-9]*[\.][0-9]+)'
    t.value = {"type" : t.type, "value": t.value, "offset": 8}
    return t

#string constant defination
def t_CONST_STRING(t):
    r'(("(\\?(.|[\r\n]))*?")|(\'(\\?(.|[\r\n]))*?\'))'
    t.value = {"type" : "string", "place": t.value, "offset": len(t.value)-2}
    return t

def t_COMMENT(t):
	r'((/\*((\*+([^*/]|[\r\n]))|[^*]|[\r\n])*\*+/)|(//.*)|(\#.*))'

#integer constant defination
def t_CONST_DECIMAL(t):
    r'([1-9]\d*)|(0)'
    t.value = {"type" : "int", "place": t.value, "offset": 4}
    return t
def t_CONST_HEX(t):
    r'0[xX][\da-fA-F]+'
    t.value = {"type" : "hex", "place": t.value, "offset": 4}
    return t
def t_CONST_OCTAL(t):
    r'0[0-7]+'
    t.value = {"type" : "octal", "place": t.value, "offset": 8}
    return t
def t_CONST_BINARY(t):
    r'0b[01]+'
    t.value = {"type" : "bin", "place": t.value, "offset": 1}
    return t


# Conditional ternery operators
t_COND_OP =  r'\?'
# t_COND_COLON = r'(:)'


t_INC  = r'\+\+'
t_PLUS_EQ  = r'\+='
t_PLUS    = r'\+'

t_DEC  = r'--'
t_MINUS_EQ  = r'-='
t_MINUS   = r'-'

t_EXPONENT  = r'\*\*'
t_MULTIPLY_EQ  = r'\*='
t_MULT   = r'\*'

t_DIVIDE_EQ  = r'/='
t_DIV  = r'/'

t_MOD_EQ  = r'%='
t_MOD  = r'%'

t_IDENTICAL  = r'==='
t_EQ_EQ  = r'=='
t_EQUAL  = r'='

t_NOT_IDENTICAL  = r'!=='
t_NOT_EQ  = r'!='
t_NOT  = r'!'

t_DOT_EQ  = r'\.='
t_DOT  = r'\.(?!\d|=)'

t_LESSER_EQ  = r'<='
t_ACCESS_OP = r'<-'
t_BIT_LSHIFT = r'<<'
t_LESSER  = r'<'

t_GREATER_EQ  = r'>='
t_BIT_RSHIFT = r'>>'
t_GREATER  = r'>'

t_AND_OP  = r'&&'
t_OR_OP  = r'\|\|'

#Bitwise operators
t_BIT_AND = r'&'
t_BIT_OR = r'\|'
t_BIT_XOR = r'\^'
t_BIT_NOT = r'~'

#other operators
t_SEMICOLON  = r';'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACKET  = r'\['
t_RBRACKET  = r'\]'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_COMMA = r','
t_QUOTE = r'"'
t_COLON = r':'

t_DOUBLE_ARROW = r'=>'


def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# regex for comment is remaining
t_ignore  = ' \t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex();

inputStr = open(sys.argv[1], "r")
data= ""
for line in inputStr:
  data += (line)

# input data to lexer
lexer.input(data)
symbols = {}
last_token = None
# Tokenize input
while True:
    tok = lexer.token()
    if not tok:
        break

    if(not symbols.get(tok.type)):
    	symbols[tok.type] = {'count':1,'lexemes':[tok.value]}
    else:
		symbols[tok.type]['count']+=1
		if(tok.value not in  symbols[tok.type]['lexemes']):
			symbols[tok.type]['lexemes'] += [tok.value]


# Now let's print in a tabular format
# first create input format for tabulate
tabulateInput = []
for tok in symbols:
	currEntry = []
	currEntry.append(tok)
	currEntry.append(symbols[tok]['count'])
	currEntry.append(symbols[tok]['lexemes'][0])
	tabulateInput.append(currEntry)

	flag = 0
	for lexeme in symbols[tok]['lexemes']:
		if flag:
			currEntry.append(lexeme)
			tabulateInput.append(currEntry)
		else:
			flag = 1
		currEntry = ['','']

# now print the tabular formated string
# tabularFormatedString = tabulate(tabulateInput, headers=['Tokens', 'Occurance', 'Lexems'], tablefmt='orgtbl')
# print "\n\n"
# print tabularFormatedString
# print "\n\n"
