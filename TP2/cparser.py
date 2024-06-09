import random
import ply.yacc as yacc
from lexer import tokens

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
    # Removes the last character if it is a question mark or exclamation mark
    # This is to avoid conflicts with the C syntax
    if t[1].endswith('?') or t[1].endswith('!'):
        t[1] = t[1][:-1]
    add_code(f"int {t[1]} = {t[3]};")

def p_statement_assign_string(t):
    'statement : ID EQUALS STRING SEMICOLON'
    add_code(f"char {t[1]}[] = {t[3]};")

def p_statement_print_string(t):
    'statement : PRINT LPAREN STRING RPAREN SEMICOLON'
    # Check if the string contains variables in between #{}
    if '#{' in t[3]:
        # Example: ESCREVER("Olá #{teste}! Como estás #{nome}?")
        # Result: printf("Olá %s! Como estás %s?", teste, nome);
        parts = t[3].split('#')
        # get the variable names in between #{}
        vars = [part[part.find('{') + 1:part.find('}')] for part in parts if '{' in part]
        # Replace the #{} with %s
        for var in vars:
            t[3] = t[3].replace(f'#{{{var}}}', '%s')
        # Add the printf statement with the variables
        add_code(f'printf({t[3]}, {", ".join(vars)});')
    else:
        add_code(f'printf("{t[3].replace("%", "%%")}");')

def p_statement_print_expr(t):
    'statement : PRINT LPAREN expression RPAREN SEMICOLON'
    add_code(f'printf("%s", {t[3]});')

# Generic expression statement
def p_statement_expr(t):
    'statement : expression SEMICOLON'
    # Do nothing, the expression will generate the code
    #add_code(f"{t[1]};")

def p_expression_input(t):
    'expression : ID EQUALS INPUT LPAREN RPAREN'
    add_code(f'char {t[1]}[100];')
    add_code(f'gets({t[1]});')
    t[0] = f'{t[1]}'

def p_expression_random(t):
    'expression : ID EQUALS RANDOM LPAREN expression RPAREN'
    add_code(f'srand(time(NULL));')
    add_code(f'int {t[1]} = rand() % ({t[5]} + 1);')
    t[0] = f'{t[1]}'

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
    # Ensure the expressions being concatenated are strings
    length = len(c_code) + 1 * random.randint(1, 100) + random.randint(30, 100)
    add_code(f"char tmp_{length}[100];")
    add_code(f'strcpy(tmp_{length}, {t[1]});')
    add_code(f'strcat(tmp_{length}, {t[3]});')
    t[0] = f"tmp_{length}"
    
def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = f"({t[2]})"

def p_expression_string(t):
    'expression : STRING'
    t[0] = t[1]

def p_expression_number(t):
    'expression : NUMBER'
    t[0] = str(t[1])

def p_expression_id(t):
    'expression : ID'
    if t[1] == 'tmp':
        t[0] = f'tmp'
    else:
        t[0] = t[1]

def p_error(t):
    if t:
        print(f"Syntax error at '{t.value}'")
    else:
        print("Syntax error at EOF")

# Build the parser
parser = yacc.yacc()

def parse(data):
    parser.parse(data)
    return c_code

