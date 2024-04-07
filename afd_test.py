import json
import afd

def test_afd_word_in_alphabet():
    afd_dict: dict = {}
    with open("exemplos/afd.json", "r") as file:
        afd_dict = json.load(file)
    assert afd.check_alphabet(afd_dict, "aaaaabbbb") == True, "Should be True"

def test_afd_word_not_in_alphabet():
    afd_dict: dict = {}
    with open("exemplos/afd.json", "r") as file:
        afd_dict = json.load(file)
    assert afd.check_alphabet(afd_dict, "aaaaccbb") == False, "Should be False"
