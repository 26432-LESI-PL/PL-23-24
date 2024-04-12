from graphviz import Digraph
from typing import Tuple

def check_alphabet(afd: dict, word: str) -> Tuple[bool, str]:
    alphabet = afd["V"]
    for char in word:
        if char not in alphabet:
            return False, char
    return True, ""

def reconhecedor(afd: dict, word: str) -> bool:
    valid, char = check_alphabet(afd, word)
    if not valid:
        print("Simbolo \"" + char + "\" não está no alfabeto do AFD")
        return False
    word = word.replace("ε", "")
    estado_atual = afd["q0"]
    path = [estado_atual]  # Start the path with the initial state
    for char in word:
        if char in afd["delta"][estado_atual]:
            estado_atual = afd["delta"][estado_atual][char]
            path.append(estado_atual)  # Add the new state to the path
        elif "ε" in afd["delta"][estado_atual]:
            estado_atual_aux = afd["delta"][estado_atual]["ε"]
            if char in afd["delta"][estado_atual_aux]:
                estado_atual = afd["delta"][estado_atual_aux][char]
                path.append(estado_atual)  # Add the new state to the path
        else:
            return False
    print("Path: ", ' -> '.join(path))  # Print the path
    return estado_atual in afd["F"]

def graphviz(afd: dict):
    dot = Digraph(comment='Automato Finito Deterministico')
    dot.node('start', shape='none', label='')
    dot.edge('start', afd["q0"], label='')
    for state in afd["delta"].keys():
        if state in afd["F"]:
            dot.node(state, state, shape="doublecircle")
        else:
            dot.node(state, state, shape="circle")
    for estado_inicial, transitions in afd["delta"].items():
        for simbolo, estado_final in transitions.items():
            dot.edge(estado_inicial, estado_final, label = simbolo)
    dot.render('automaton_graph', view=True, format='png')