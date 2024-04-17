import json
import os
import afnd

afnd_dict: dict = {}
with open("exemplos/afnd.json", "r", encoding="utf8") as file:
    afnd_dict = json.load(file)

def test_afnd_graphviz():
    afnd.graphviz(afnd_dict)
    assert os.path.isfile("afnd_graph.png") == True, "Should be True"

def test_convert_to_afd():
    afd = afnd.nfa_to_dfa(afnd_dict)
    with open("afd_output.json", "w", encoding="utf8") as file:
        json.dump(afd, file)
    assert os.path.isfile("afnd_graph.png"), "Should be True"