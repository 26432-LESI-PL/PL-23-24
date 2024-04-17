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

def to_afd(nfa):
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
    return dfa