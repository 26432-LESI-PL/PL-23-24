import json
import er
import os

er_dict: dict = {}
with open("exemplos/afnd.json", "r") as file:
    er_dict = json.load(file)

def test_regex_to_nfa():
    regex = {
        "op": "alt",
        "args": [
            {"simb": "a"},
            {
                "op": "seq",
                "args": [
                    {"simb": "a"},
                    {"op": "kle", "args": [{"simb": "b"}]}
                ]
            }
        ]
    }
    nfa = er.regex_to_nfa(regex)
    if nfa is not None:
            er.afnd_json(nfa, "afnd.json")
    with open("afnd.json", "r") as file:
            nfa_file = json.load(file)
    assert nfa == nfa_file, "Should be equal"

    def test_er_graphviz():
        er.graphviz(er_dict)
    assert os.path.isfile("automaton_graph_2.png") == True, "Should be True"