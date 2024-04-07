"""
	Processamento de Linguagens (ESI) 
	Trabalho Prático 1
	Exemplo de Apoio: er_eval.py 
	Calcular a string que representa a expressão regular especificada numa árvore (dicionário) - lida json 
"""
# global counter
# counter = 0
# Definindo funções para cada operação


def alt(args): # args = ['a','ab*']             -> args = ["a"]
    # global counter

    # novo_estado_1 = f'q{counter}'
    # counter = counter + 1
    # novo_estado_2 = f'q{counter}'
    # counter = counter + 1

    # novas_transicoes : dict = {
    #     args[0] : novo_estado_1,                 #  a : q1
    #     args[0] : novo_estado_2,                 #  a : q2 
    # }


    return f'{args[0]}|{args[1]}'

def seq(args):
    return f'{args[0]}{args[1]}'

def kle(args):
    return f'{args[0]}*'

def trans(args):
    return f'{args[0]}+'


# Dicionário de operadores para mapear operações e suas prioridades
operadores : dict = {
    "alt": (alt, 0),			# união 		   |
    "seq": (seq, 1),			# concatenação     .
    "kle": (kle, 2),			# fecho de kleene  *
    "trans": (trans, 2) 		# fecho transitivo +
}

def evaluate(arv):
    # Avalia operadores, símbolos e epsilon
    if isinstance(arv, dict):
        if 'op' in arv:  # Avalia operações
            op, op_priority = operadores[arv['op']]
            args_res = [evaluate(a) for a in arv['args']]
            # Processa os argumentos com base na prioridade
            processed_args = [a[0] if op_priority < a[1] else f'({a[0]})' for a in args_res]
            return op(processed_args), op_priority

        elif 'simb' in arv:
            return arv['simb'], 3

        elif 'epsilon' in arv:
            return 'ε', 3

    raise Exception("Formato de árvore de expressão regular inválido")


def main():
    
	import json

	with open("aula05\exemplo01.er.json","r") as f:
		arvore = json.load(f)
		
		res, _ = evaluate(arvore)
		print(res)
		
	with open("exemplo02.er.json","r") as f:
		arvore = json.load(f)
		
		res, _ = evaluate(arvore)
		print(res)
		
	with open("exemplo03.er.json","r") as f:
		arvore = json.load(f)
		
		res, _ = evaluate(arvore)
		print(res)
          
if __name__ == "__main__":
    main()