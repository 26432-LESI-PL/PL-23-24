import ply.lex as lex

# List of token names
tokens = [
    'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN',
    'ID', 'EQUALS', 'SEMICOLON', 'STRING', 'CONCAT', 'COMMENT',
    'COMMA', 'COLON', 'LBRACKET', 'RBRACKET'
]

# Reserved words
reserved = {
    'ESCREVER': 'PRINT',
    'ENTRADA': 'INPUT',
    'ALEATORIO': 'RANDOM',
    'FUNCAO': 'FUNC',
    'FIM': 'END'
}
tokens = tokens + list(reserved.values())

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQUALS = r'\='
t_SEMICOLON = r'\;'
t_CONCAT = r'\<\>'  # String concatenation operator
t_COMMA = r'\,'
t_COLON = r'\:'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

# String literals
t_STRING = r'"(?:\\.|[^"\\])*"'  # Double-quoted strings with escaped characters and any character except unescaped newline

# Comment handling
def t_COMMENT(t):
    r'\-\-.*'
    pass  # No return value. Token discarded.

# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*[\?\!]?'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()