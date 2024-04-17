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

def convert_to_afd(afnd):
    afd = {
        "Q": [],
        "V": afnd["V"],
        "delta": {},
        "q0": [afnd["q0"]],
        "F": []
    }
    queue = [afd["q0"]]
    while queue:
        state = queue.pop(0)
        afd["Q"].append(state)
        afd["delta"][str(state)] = {}
        for symbol in afd["V"]:
            next_state = []
            for substate in state:
                if symbol in afnd["delta"].get(substate, {}):
                    next_state += afnd["delta"][substate][symbol]
            next_state = list(set(next_state))  # remove duplicates
            if next_state and next_state not in afd["Q"]:
                queue.append(next_state)
            afd["delta"][str(state)][symbol] = next_state
        if any(substate in afnd["F"] for substate in state):
            afd["F"].append(state)
    return afd

afd_dict: dict = {}
with open("exemplos/afnd.json", "r", encoding="utf8") as file:
    afd_dict = json.load(file)

print(convert_to_afd(afd_dict))