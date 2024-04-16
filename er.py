import json

def alt(args): 
    return f'{args[0]}|{args[1]}'

def seq(args):
    return f'{args[0]}{args[1]}'

def kle(args):
    return f'{args[0]}*'

def trans(args):
    return f'{args[0]}+'


operadores : dict = {
    "alt": (alt, 0),			# união 		   |
    "seq": (seq, 1),			# concatenação     .
    "kle": (kle, 2),			# fecho de kleene  *
    "trans": (trans, 2) 		# fecho transitivo +
}

def output(er):
    # Avalia operadores, símbolos e epsilon
    if isinstance(er, dict):
        if 'op' in er:  # Avalia operações
            op, op_priority = operadores[er['op']]
            args_res = [output(a) for a in er['args']]
            # Processa os argumentos com base na prioridade
            processed_args = [a[0] if op_priority < a[1] else f'({a[0]})' for a in args_res]
            return op(processed_args), op_priority

        elif 'simb' in er:
            return er['simb'], 3

        elif 'epsilon' in er:
            return 'ε', 3

    raise Exception("Formato de árvore de expressão regular inválido")

def afnd_json(afnd, filename):
    with open(filename, "w") as f:
        json.dump(afnd, f, indent=4)
