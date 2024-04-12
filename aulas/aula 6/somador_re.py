import re

text: str = "Hoje é dia 11 de abril de 2024. Isto é = a dizer que hoje é 11=/04/2024."

regex = r'='
eq : list = re.findall(regex, text)

text_cpy : str = text
result_parcial : int = 0

for e in eq:
    idx = text_cpy.index("=")

    regex = r'\d+'
    numbers : list = re.findall(regex, text_cpy[:idx])
    numbers = [int(number) for number in numbers]
    
    print(f"Soma parcial: {(sum(numbers) + result_parcial)}")
    
    result_parcial += sum(numbers)
    text_cpy = text_cpy[idx+1:]

regex = r'\d+'
numbers : list = re.findall(regex, text)
numbers = [int(number) for number in numbers]
result : int = sum(numbers)

print(f"Números encontrados: {numbers}")
print(f"Soma total: {result}")


#########################


import ply.lex as lex

tokens = ("NUM", "EQ")
result : int = 0
numbers : list = []

text: str = "Hoje é dia 11 de abril de 2024. Isto é = a dizer que hoje é 11=/04/2024."

def t_NUM(t):   # token: "NUM"
    r"[0-9]+"
    #  t.value  # lexema: valor do token 

    global result
    result += int(t.value)

    global numbers
    numbers.append(int(t.value))

def t_EQ(t):    # token:  "EQ"  
    r"="
    print(f"Soma parcial: {result}")

def t_error(t):
    # print(f"Invalid character {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()
lexer.input(text)

# iterate over each token (character) and process token functions
for token in lexer:
    pass

print(f"Números encontrados: {numbers}")
print(f"Soma total: {result}")