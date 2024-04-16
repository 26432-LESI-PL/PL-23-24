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