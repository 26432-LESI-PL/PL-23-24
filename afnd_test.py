import json
import os
import afnd

afd_dict: dict = {}
with open("exemplos/afnd.json", "r") as file:
    afd_dict = json.load(file)

def test_afnd_graphviz():
    afnd.graphviz(afd_dict)
    assert os.path.isfile("afd_graph.png") == True, "Should be True"