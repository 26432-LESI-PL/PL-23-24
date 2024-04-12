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

def re_to_nfa(re):
    # Avalia operadores, símbolos e epsilon
    if isinstance(re, dict):
        if 'op' in re:  # Avalia operações
            op, op_priority = operadores[re['op']]
            args_res = [re_to_nfa(a) for a in re['args']]
            # Processa os argumentos com base na prioridade
            processed_args = [a[0] if op_priority < a[1] else f'({a[0]})' for a in args_res]
            return op(processed_args), op_priority

        elif 'simb' in re:
            return re['simb'], 3

        elif 'epsilon' in re:
            return 'ε', 3

    raise Exception("Formato de árvore de expressão regular inválido")

def nfa_to_json(nfa, filename):
    with open(filename, "w") as f:
        json.dump(nfa, f, indent=4)
    
def main():
    re = {
        "op": "alt",
        "args": [
            {
                "op": "seq",
                "args": [
                    {
                        "simb": "a"
                    },
                    {
                        "op": "kle",
                        "args": [
                            {
                                "simb": "b"
                            }
                        ]
                    }
                ]
            },
            {
                "simb": "c"
            }
        ]
    }
    nfa = re_to_nfa(re)
    nfa_to_json(nfa, "nfa.json")
