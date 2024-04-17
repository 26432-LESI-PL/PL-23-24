import json
from graphviz import Digraph

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

def convert_to_afd(afnd: dict) -> dict:
    afd = {
        "Q": [],
        "V": afnd["V"],
        "q0": afnd["q0"],
        "F": [],
        "delta": {}
    }
    # Adiciona os estados do AFND ao AFD
    for state in afnd["Q"]:
        afd["Q"].append(state)
        afd["delta"][state] = {}
    # Adiciona os estados finais do AFND ao AFD
    for state in afnd["F"]:
        afd["F"].append(state)
    # Adiciona as transições do AFND ao AFD
    for state in afnd["Q"]:
        if state in afnd["delta"]:
            for transition in afnd["delta"][state].keys():
                for next_state in afnd["delta"][state][transition]:
                    if transition not in afd["delta"][state]:
                        afd["delta"][state][transition] = next_state
                    else:
                        afd["delta"][state][transition] += next_state
    return afd


afd_dict: dict = {}
with open("exemplos/afnd.json", "r", encoding="utf8") as file:
    afd_dict = json.load(file)
print(convert_to_afd(afd_dict))