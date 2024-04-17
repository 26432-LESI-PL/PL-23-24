def to_afnd(regex):
    if "simb" in regex:
        start_state = "q1"
        end_state = "q2"
        return {
            "Q": [start_state, end_state],
            "V": [regex["simb"]],
            "q0": start_state,
            "F": [end_state],
            "delta": {
                start_state: {regex["simb"]: [end_state]}
            }
        }
    elif regex["op"] == "alt":
        nfa1 = to_afnd(regex["args"][0])
        nfa2 = to_afnd(regex["args"][1])
        start_state = "q" + str(len(nfa1["Q"]) + len(nfa2["Q"]) + 1)
        end_state = "q" + str(len(nfa1["Q"]) + len(nfa2["Q"]) + 2)
        return {
            "Q": nfa1["Q"] + nfa2["Q"] + [start_state, end_state],
            "V": list(set(nfa1["V"] + nfa2["V"])),
            "q0": start_state,
            "F": [end_state],
            "delta": {
                **nfa1["delta"],
                **nfa2["delta"],
                start_state: {"ε": [nfa1["q0"], nfa2["q0"]]},
                nfa1["F"][0]: {"ε": [end_state]},
                nfa2["F"][0]: {"ε": [end_state]}
            }
        }
    elif regex["op"] == "seq":
        nfa1 = to_afnd(regex["args"][0])
        nfa2 = to_afnd(regex["args"][1])
        return {
            "Q": nfa1["Q"] + nfa2["Q"],
            "V": list(set(nfa1["V"] + nfa2["V"])),
            "q0": nfa1["q0"],
            "F": nfa2["F"],
            "delta": {
                **nfa1["delta"],
                **nfa2["delta"],
                nfa1["F"][0]: {"ε": [nfa2["q0"]]}
            }
        }
    elif regex["op"] == "kle":
        nfa = to_afnd(regex["args"][0])
        start_state = "q" + str(len(nfa["Q"]) + 1)
        end_state = "q" + str(len(nfa["Q"]) + 2)
        return {
            "Q": nfa["Q"] + [start_state, end_state],
            "V": nfa["V"],
            "q0": start_state,
            "F": [end_state],
            "delta": {
                **nfa["delta"],
                start_state: {"ε": [nfa["q0"], end_state]},
                nfa["F"][0]: {"ε": [nfa["q0"], end_state]}
            }
        }
    else:
        raise Exception("Operação inválida")
