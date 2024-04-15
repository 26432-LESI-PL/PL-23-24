import json
import afd
import os
import pytest

def setup_module(module):
    global afd_dict
    afd_dict = {}
    with open("exemplos/afd.json", "r") as file:
        afd_dict = json.load(file)

def test_re_to_nfa():
    result, char = afd.check_alphabet(afd_dict, "aaaaabbbb")
    assert result == True, "Should be True"
    assert char == "", "Should be empty"

def test_nfa_to_json():
    result, char = afd.check_alphabet(afd_dict, "aaaaccbb")
    assert result == False, "Should be False"
    assert char == "c", "Should be c"
