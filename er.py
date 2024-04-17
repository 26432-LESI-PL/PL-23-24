import json
from graphviz import Digraph

def regex_to_nfa(regex: dict):
    if "simb" in regex:
        return {"Q": ["q0", "q1"], "V": [regex["simb"]], "q0": "q0", "F": ["q1"], "delta": {"q0": {"simb": regex["simb"], "next": "q1"}}}
    else:
        op = regex["op"]
        args = regex["args"]
        if op == "alt":
            nfa1 = regex_to_nfa(args[0])
            nfa2 = regex_to_nfa(args[1])
            return alt_nfa(nfa1, nfa2)
        elif op == "seq":
            nfa1 = regex_to_nfa(args[0])
            nfa2 = regex_to_nfa(args[1])
            return seq_nfa(nfa1, nfa2)
        elif op == "kle":
            nfa = regex_to_nfa(args[0])
            return kle_nfa(nfa)

def alt_nfa(nfa1: dict, nfa2: dict) -> dict:
    Q = list(set(["q0"] + nfa1["Q"] + nfa2["Q"]))
    V = list(set(nfa1["V"] + nfa2["V"]))
    q0 = "q0"
    F = list(set(nfa1["F"] + nfa2["F"]))
    delta = {"q0": {"op": "alt", "next": [nfa1["q0"], nfa2["q0"]]}}

    delta.update(nfa1["delta"])
    delta.update(nfa2["delta"])
    return {"Q": Q, "V": V, "q0": q0, "F": F, "delta": delta}

def seq_nfa(nfa1: dict, nfa2: dict) -> dict:
    Q = list(set(nfa1["Q"] + nfa2["Q"]))
    V = list(set(nfa1["V"] + nfa2["V"]))
    q0 = nfa1["q0"]
    F = nfa2["F"]
    delta = nfa1["delta"]
    delta.update(nfa2["delta"])
    delta[nfa1["F"][0]] = {"op": "seq", "next": nfa2["q0"]}
    return {"Q": Q, "V": V, "q0": q0, "F": F, "delta": delta}

def kle_nfa(nfa: dict) -> dict:
    Q = list(set(["q0"] + nfa["Q"]))
    V = list(set(nfa["V"]))
    q0 = "q0"
    F = list(set(nfa["F"] + ["q0"]))
    delta = {"q0": {"op": "kle", "next": nfa["q0"]}}
    delta.update(nfa["delta"])
    delta[nfa["F"][0]] = {"op": "kle", "next": nfa["q0"]}
    return {"Q": Q, "V": V, "q0": q0, "F": F, "delta": delta}

def afnd_json(nfa: dict, filename: str):
    with open(filename, "w") as file:
        json.dump(nfa, file)

def graphviz(nfa: dict):
    dot = Digraph(comment='Automato Finito Nao Deterministico')
    dot.node('start', shape='none', label='')
    dot.edge('start', nfa["q0"], label='')
    for state in nfa["delta"].keys():
        if state in nfa["F"]:
            dot.node(state, state, shape="doublecircle")
        else:
            dot.node(state, state, shape="circle")
    for estado_inicial, transitions in nfa["delta"].items():
        for simbolo, estados_finais in transitions.items():
            for estado_final in estados_finais:  # handle the case where estado_final is a list
                dot.edge(estado_inicial, estado_final, label = simbolo)
    dot.render('automaton_graph_2', view=True, format='png')