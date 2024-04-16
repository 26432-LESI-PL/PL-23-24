import json
import afd
import os

afd_dict: dict = {}
with open("exemplos/afd.json", "r", encoding="utf8") as file:
    afd_dict = json.load(file)

def test_afd_word_in_alphabet():
    result, char = afd.check_alphabet(afd_dict, "aaaaabbbb")
    assert result == True, "Should be True"
    assert char == "", "Should be empty"

def test_afd_word_not_in_alphabet():
    result, char = afd.check_alphabet(afd_dict, "aaaaccbb")
    assert result == False, "Should be False"
    assert char == "c", "Should be c"

def test_afd_reconhecedor():
    assert afd.reconhecedor(afd_dict, "abbb") == True, "Should be True"

def test_afd_reconhecedor_false():
    assert afd.reconhecedor(afd_dict, "aabb") == False, "Should be False"

def test_afd_reconhecedor_not_final_state():
    assert afd.reconhecedor(afd_dict, "a") == False, "Should be False"

def test_afd_graphviz():
    afd.graphviz(afd_dict)
    assert os.path.isfile("afd_graph.png") == True, "Should be True"