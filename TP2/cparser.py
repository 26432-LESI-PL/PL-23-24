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

# Statements and expressions rules
def p_statements(t):
    '''statements : statements statement
                  | statement'''
    if len(t) == 3:
        t[0] = t[1] + [t[2]]
    else:
        t[0] = [t[1]]

def p_statement_assign(t):
    'statement : ID EQUALS expression SEMICOLON'
    # if ID has a ? or a ! reove them
    if t[1].endswith('?') or t[1].endswith('!'):
        t[1] = t[1][:-1]
    if not hasattr(t.lexer, 'inside_function') or not t.lexer.inside_function:
        add_c_code(f"int {t[1]} = {t[3]};")
        add_python_code(f"{t[1]} = {t[3]}")
    else:
        add_c_code(f"{t[1]} = {t[3]};")
        add_python_code(f"{t[1]} = {t[3]}")
    t[0] = f"{t[1]} = {t[3]}"

def p_statement_assign_string(t):
    'statement : ID EQUALS STRING SEMICOLON'
    if t[1].endswith('?') or t[1].endswith('!'):
        t[1] = t[1][:-1]
    if not hasattr(t.lexer, 'inside_function') or not t.lexer.inside_function:
        add_c_code(f"char {t[1]}[] = {t[3]};")
        add_python_code(f"{t[1]} = {t[3]}")
    else:
        add_c_code(f"{t[1]} = {t[3]};")
        add_python_code(f"{t[1]} = {t[3]}")
    t[0] = f"{t[1]} = {t[3]}"

def p_statement_assign_list(t):
    'statement : ID EQUALS list SEMICOLON'
    add_c_code(f"int {t[1]}[] = {{{', '.join(map(str, t[3]))}}};")
    add_python_code(f"{t[1]} = {t[3]}")

def p_list(t):
    '''list : LBRACKET elements RBRACKET
            | LBRACKET RBRACKET'''
    if len(t) == 3:  # Empty list
        t[0] = []
    else:
        t[0] = t[2]

def p_elements(t):
    '''elements : elements COMMA expression
                | expression'''
    if len(t) == 4:
        t[0] = t[1] + [t[3]]
    else:
        t[0] = [t[1]]

def p_statement_print_list(t):
    'statement : PRINT LPAREN ID RPAREN SEMICOLON'
    add_c_code(f'printf("[");')
    add_c_code(f'int n = sizeof({t[3]}) / sizeof({t[3]}[0]);')
    add_c_code(f'for(int i = 0; i < n; i++) {{')
    add_c_code(f'    printf("%d", {t[3]}[i]);')
    add_c_code(f'    if (i < n - 1) printf(", ");')
    add_c_code(f'}}')
    add_c_code(f'printf("]");')
    add_python_code(f'print({t[3]})')

def p_statement_print_string(t):
    'statement : PRINT LPAREN STRING RPAREN SEMICOLON'
    if '#{' in t[3]:
        parts = t[3].split('#')
        vars = [part[part.find('{') + 1:part.find('}')] for part in parts if '{' in part]
        python_tmp = t[3]
        python_tmp = python_tmp.replace('#{', '{').replace('}', '}')
        add_python_code(f'print(f{python_tmp})')
        for var in vars:
            t[3] = t[3].replace(f'#{{{var}}}', '%s')
        add_c_code(f'printf({t[3]}, {", ".join(vars)});')
    else:
        add_c_code(f'printf({t[3].replace("%", "%%")});')
        add_python_code(f'print({t[3]})')

def p_statement_print_expr(t):
    'statement : PRINT LPAREN expression RPAREN SEMICOLON'
    add_c_code(f'printf("%d", {t[3]});')
    add_python_code(f'print({t[3]})')

def p_statement_expr(t):
    'statement : expression SEMICOLON'
    t[0] = t[1]

def p_statement_function_oneliner_declaration(t):
    '''statement : FUNCTION ID LPAREN param_list RPAREN COMMA COLON expression SEMICOLON
                 | FUNCTION ID LPAREN RPAREN COMMA COLON expression SEMICOLON'''
    if len(t) == 10:
        params = ', '.join([f'int {param}' for param in t[4]])
        add_c_code(f'int {t[2]}({params}) {{ return {t[8]}; }}')
        add_python_code(f'def {t[2]}({", ".join(t[4])}): return {t[8]}')
    else:
        add_c_code(f'int {t[2]}() {{ return {t[7]}; }}')
        add_python_code(f'def {t[2]}(): return {t[7]}')

def p_statement_function_declaration(t):
    '''statement : FUNCTION ID LPAREN param_list RPAREN COLON statements END
                 | FUNCTION ID LPAREN RPAREN COLON statements END'''
    t.lexer.inside_function = True
    if len(t) == 9:
        params = ', '.join([f'int {param}' for param in t[4]])
        add_c_code(f'int {t[2]}({params}) {{')
        add_python_code(f'def {t[2]}({", ".join(t[4])}):')
        for stmt in t[7][:-1]:  # Iterate over all but the last statement
            if stmt:
                if stmt == c_code[-2]:
                    c_code.pop(-2)
                if stmt == python_code[-2]:
                    python_code.pop(-2)
                add_c_code(stmt)
                add_python_code(f'    {stmt}')
        add_c_code(f'return {t[7][-1]};')  # Set the last statement as the return value
        add_python_code(f'    return {t[7][-1]}')
        add_c_code('}')
    else:
        add_c_code(f'int {t[2]}() {{')
        add_python_code(f'def {t[2]}():')
        for stmt in t[6][:-1]:  # Iterate over all but the last statement
            if stmt:
                add_c_code(stmt)
                add_python_code(f'    {stmt}')
        add_c_code(f'return {t[6][-1]};')  # Set the last statement as the return value
        add_python_code(f'    return {t[6][-1]}')
        add_c_code('}')
    t.lexer.inside_function = False

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
    'expression : INPUT LPAREN RPAREN'
    t[0] = 'input()'
    add_c_code(f'gets({t[1]});')
    add_python_code(f'{t[1]} = input()')

def p_expression_random(t):
    'expression : RANDOM LPAREN expression RPAREN'
    t[0] = f'random.randint(0, {t[3]})'
    add_c_code(f'int {t[1]} = rand() % ({t[3]} + 1);')
    add_python_code("import random")
    add_python_code(f'{t[1]} = random.randint(0, {t[3]})')

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

def p_expression_string(t):
    'expression : STRING'
    t[0] = t[1]

def p_expression_number(t):
    'expression : NUMBER'
    t[0] = str(t[1])

def p_expression_id(t):
    'expression : ID'
    t[0] = t[1]

def p_expression_function_call(t):
    'expression : ID LPAREN arg_list RPAREN'
    t[0] = f"{t[1]}({', '.join(t[3])})"
    #add_c_code(f"{t[1]}({', '.join(t[3])});")
    #add_python_code(f"{t[1]}({', '.join(t[3])})")
    #add_c_code(f"{t[1]}({', '.join(t[3])});")
    #add_python_code(f"{t[1]}({', '.join(t[3])})")

def p_arg_list(t):
    '''arg_list : arg_list COMMA expression
                | arg_list COMMA list
                | expression
                | list'''
    if len(t) == 4:
        if isinstance(t[3], list):
            t[0] = t[1] + [f"[{', '.join(t[3])}]"]
        else:
            t[0] = t[1] + [t[3]]
    else:
        if isinstance(t[1], list):
            t[0] = [f"[{', '.join(t[1])}]"]
        else:
            t[0] = [t[1]]

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
