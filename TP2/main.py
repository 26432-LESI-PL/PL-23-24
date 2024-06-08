import ply.yacc as yacc
from mylexer import tokens
# Precedence rules for arithmetic operators
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'CONCAT'),  # Add the CONCAT operator to the precedence rules
)
# This will hold the generated C code
c_code = []
# Helper function to add a line of code
def add_code(line):
    c_code.append(line)
def p_statements(t):
    '''statements : statements statement
                  | statement'''
    pass
def p_statement_assign(t):
    'statement : ID EQUALS expression SEMICOLON'
    add_code(f"int {t[1]} = {t[3]};")
def p_statement_print(t):
    'statement : PRINT LPAREN STRING RPAREN SEMICOLON'
    add_code(f'printf({t[3]});')
def p_statement_expr(t):
    'statement : expression SEMICOLON'
    add_code(f"{t[1]};")
def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if t[2] == '+':
        t[0] = f"({t[1]} + {t[3]})"
    elif t[2] == '-':
        t[0] = f"({t[1]} - {t[3]})"
    elif t[2] == '*':
        t[0] = f"({t[1]} * {t[3]})"
    elif t[2] == '/':
        t[0] = f"({t[1]} / {t[3]})"
def p_expression_concat(t):
    'expression : expression CONCAT expression'
    t[0] = f"({t[1]} + {t[3]})"
def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = f"({t[2]})"
def p_expression_number(t):
    'expression : NUMBER'
    t[0] = str(t[1])
def p_expression_id(t):
    'expression : ID'
    t[0] = t[1]
def p_error(t):
    if t:
        print(f"Syntax error at '{t.value}'")
    else:
        print("Syntax error at EOF")
# Build the parser
parser = yacc.yacc()
# Test it
data = '''
tmp_01 = 2*3+4;
a1_ = 12345 - (5191 * 15);
idade_valida? = 1;
mult_3! = a1_ * 3;
curso = "ESI";
ESCREVER("Olá" <> curso);
ESCREVER(a2);
'''
parser.parse(data)
# Print the generated C code
print("\n".join(c_code))