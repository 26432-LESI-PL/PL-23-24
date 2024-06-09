import random
import ply.yacc as yacc
from lexer import tokens

tokens = tokens

# Precedence rules for arithmetic operators
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'CONCAT'),  # Add the CONCAT operator to the precedence rules
)

# This will hold the generated C code
c_code = []

# This will hold the generated Python code
python_code = []


# Helper function to add a line of code
def add_c_code(line):
    c_code.append(line)

def add_python_code(line):
    python_code.append(line)

def p_statements(t):
    '''statements : statements statement
                  | statement'''
    if len(t) == 3:
        t[0] = t[1] + [t[2]]
    else:
        t[0] = [t[1]]

def p_statement_assign(t):
    'statement : ID EQUALS expression SEMICOLON'
    # Removes the last character if it is a question mark or exclamation mark
    # This is to avoid conflicts with the C syntax
    if t[1].endswith('?') or t[1].endswith('!'):
        t[1] = t[1][:-1]
    add_c_code(f"int {t[1]} = {t[3]};")
    add_python_code(f"{t[1]} = {t[3]}")
    t[0] = f"int {t[1]} = {t[3]};"

def p_statement_assign_string(t):
    'statement : ID EQUALS STRING SEMICOLON'
    add_c_code(f"char {t[1]}[] = {t[3]};")
    add_python_code(f"{t[1]} = {t[3]}")

def p_statement_print_string(t):
    'statement : PRINT LPAREN STRING RPAREN SEMICOLON'
    # Check if the string contains variables in between #{}
    if '#{' in t[3]:
        # Example: ESCREVER("Olá #{teste}! Como estás #{nome}?")
        # Result: printf("Olá %s! Como estás %s?", teste, nome);
        parts = t[3].split('#')
        # get the variable names in between #{}
        vars = [part[part.find('{') + 1:part.find('}')] for part in parts if '{' in part]
        python_tmp = t[3]
        python_tmp = python_tmp.replace('#{', '{').replace('}', '}')
        add_python_code(f'print(f{python_tmp})')
        # Replace the #{} with %s
        for var in vars:
            t[3] = t[3].replace(f'#{{{var}}}', '%s')
        # Add the printf statement with the variables
        add_c_code(f'printf({t[3]}, {", ".join(vars)});')
    else:
        add_c_code(f'printf({t[3].replace("%", "%%")});')
        add_python_code(f'print({t[3]})')

def p_statement_print_expr(t):
    'statement : PRINT LPAREN expression RPAREN SEMICOLON'
    add_c_code(f'printf("%s", {t[3]});')
    add_python_code(f'print({t[3]})')

# Generic expression statement
def p_statement_expr(t):
    'statement : expression SEMICOLON'
    # Do nothing, the expression will generate the code
    #add_c_code(f"{t[1]};")

def p_statement_function_oneliner_declaration(t):
    '''statement : FUNCTION ID LPAREN param_list RPAREN COMMA COLON expression SEMICOLON
                 | FUNCTION ID LPAREN RPAREN COMMA COLON expression SEMICOLON'''
    if len(t) == 10:  # If the function has parameters and a return expression
        params = ', '.join([f'int {param}' for param in t[4]])
        add_c_code(f'int {t[2]}({params}) {{ return {t[8]}; }}')
        add_python_code(f'def {t[2]}({", ".join(t[4])}): return {t[8]}')
    else:  # If the function has parameters but no return expression
        add_c_code(f'int {t[2]}() {{ return {t[6]}; }}')
        add_python_code(f'def {t[2]}(): return {t[6]}')


def p_statement_function_declaration(t):
    '''statement : FUNCTION ID LPAREN param_list RPAREN COLON statements END
                 | FUNCTION ID LPAREN RPAREN COLON'''
    if len(t) == 7:  # If the function is only the name and parameters
        params = ', '.join([f'int {param}' for param in t[4]])
        add_c_code(f'int {t[2]}({params}) {{}}')
        add_python_code(f'def {t[2]}({", ".join(t[4])}): pass')
    else:  # If the function has no parameters
        add_c_code(f'int {t[2]}() {{{t[6]}}}')
        add_python_code(f'def {t[2]}():\n    {t[6]}')

def p_param_list(t):
    '''param_list : param_list COMMA ID
                  | ID'''
    if len(t) == 4:
        t[0] = t[1] + [t[3]]
    else:
        t[0] = [t[1]]

def p_statement_end(t):
    'statement : END'
    add_c_code('}')
    add_python_code('')

def p_expression_input(t):
    'expression : ID EQUALS INPUT LPAREN RPAREN'
    add_c_code(f'char {t[1]}[100];')
    add_c_code(f'gets({t[1]});')
    add_python_code(f'{t[1]} = input()')
    t[0] = f'{t[1]}'

def p_expression_random(t):
    'expression : ID EQUALS RANDOM LPAREN expression RPAREN'
    add_c_code(f'srand(time(NULL));')
    add_c_code(f'int {t[1]} = rand() % ({t[5]} + 1);')
    add_python_code(f'import random')
    add_python_code(f'{t[1]} = random.randint(0, {t[5]})')
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
    add_c_code(f"char tmp_{length}[100];")
    add_c_code(f'strcpy(tmp_{length}, {t[1]});')
    add_c_code(f'strcat(tmp_{length}, {t[3]});')
    add_python_code(f'tmp_{length} = {t[1]} + {t[3]}')
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
    return python_code, c_code

