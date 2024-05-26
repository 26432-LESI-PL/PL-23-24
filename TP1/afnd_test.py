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
    afd = afnd.to_afd(afnd_dict)
    assert isinstance(afd, dict), "Should be True"
    assert isinstance(afd["Q"], list), "Should be True"
    assert isinstance(afd["V"], list), "Should be True"
    assert isinstance(afd["q0"], str), "Should be True"
    assert isinstance(afd["F"], list), "Should be True"
    assert isinstance(afd["delta"], dict), "Should be True"
    assert os.path.isfile("afnd_graph.png"), "Should be True"