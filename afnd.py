import json
from graphviz import Digraph
from collections import deque

def graphviz(afnd: dict):
    dot = Digraph(comment="Automato Finito Não Deterministico")
    dot.node("start", shape="none", label="")
    dot.edge("start", afnd["q0"], label="")
    # Renderiza o double circle corretamente
    for state in afnd["Q"]:
        if state in afnd["F"]:
            dot.node(state, state, shape="doublecircle")
        else:
            dot.node(state, state, shape="circle")
    for state in afnd["delta"].keys():
        for transition in afnd["delta"][state].keys():
            for next_state in afnd["delta"][state][transition]:
                dot.edge(state, next_state, label=transition)
    dot.render("afnd_graph", view=True, format="png")

#Exemplo AFND/NFA
'''{
    "Q": [
        "q1",
        "q2",
        "q3",
        "q4",
        "q5",
        "q6",
        "q7",
        "q8",
        "q9",
        "q10",
        "q11"
    ],
    "V": [
        "ε",
        "b",
        "a"
    ],
    "q0": "q1",
    "F": [
        "q2"
    ],
    "delta": {
        "q3": {
            "a": [
                "q4"
            ]
        },
        "q1": {
            "ε": [
                "q3",
                "q5"
            ]
        },
        "q4": {
            "ε": [
                "q2"
            ]
        },
        "q6": {
            "a": [
                "q7"
            ]
        },
        "q5": {
            "ε": [
                "q6"
            ]
        },
        "q10": {
            "b": [
                "q11"
            ]
        },
        "q8": {
            "ε": [
                "q10",
                "q9"
            ]
        },
        "q11": {
            "ε": [
                "q8",
                "q9"
            ]
        },
        "q7": {
            "ε": [
                "q8"
            ]
        },
        "q9": {
            "ε": [
                "q2"
            ]
        }
    }
}'''

#Exemplo AFD/DFA
'''{
    "Q": [
        "A",
        "B",
        "C"
    ],
    "V": [
        "b",
        "a"
    ],
    "q0": "A",
    "F": [
        "C"
    ],
    "delta": {
        "A": {
            "a": "B"
        },
        "B": {
            "b": "C"
        },
        "C": {
            "b": "C"
        }
    }
}'''
def epsilon_closure(state, transition_function):
    states = set(state)
    for s in state:
        states.update(transition_function.get(s, {}).get('ε', []))
    return states

def move(state, symbol, transition_function):
    states = set()
    for s in state:
        states.update(transition_function.get(s, {}).get(symbol, []))
    return states

def nfa_to_dfa(nfa):
    dfa = {"Q": [], "V": nfa["V"], "q0": nfa["q0"], "F": [], "delta": {}}
    unmarked_states = [epsilon_closure([nfa["q0"]], nfa["delta"])]
    while unmarked_states:
        T = unmarked_states.pop()
        dfa["Q"].append(''.join(sorted(T)))
        if set(nfa["F"]).intersection(T):
            dfa["F"].append(''.join(sorted(T)))
        for symbol in nfa["V"]:
            if symbol == 'ε':
                continue
            U = epsilon_closure(move(T, symbol, nfa["delta"]), nfa["delta"])
            if U and ''.join(sorted(U)) not in dfa["Q"]:
                unmarked_states.append(U)
            dfa["delta"].setdefault(''.join(sorted(T)), {})[symbol] = ''.join(sorted(U))
    return json.dumps(dfa, indent=4)

with open("exemplos/afnd.json", "r", encoding="utf8") as file:
    afnd = json.load(file)
    afd = nfa_to_dfa(afnd)
    print(afd)