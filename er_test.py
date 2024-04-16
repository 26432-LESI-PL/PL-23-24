import json
import er
import os
import pytest

def setup_module(module):
    if os.path.exists("exemplos/nfa.json"):
        os.remove("exemplos/nfa.json")

def test_re_to_nfa():
    re = {
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
    nfa, _ = er.re_to_nfa(re)  # Unpack the tuple
    assert nfa == "a|ab*", "Should be a|ab*"
    er.nfa_to_json(nfa, "exemplos/nfa.json")
    assert os.path.exists("exemplos/nfa.json"), "File should exist"
    with open("exemplos/nfa.json", "r") as file:
        nfa_file = json.load(file)
    assert nfa == nfa_file, "Should be equal"
    
def test_nfa_to_json():
    nfa = {
    "Q": ["q0", "q1", "q2", "q3", "q4", "q5"],
    "V": ["a", "b"],
    "q0": "q0",
    "F": ["q5"],
    "delta": {
        "q0": {"op": "alt", "next": "q1"},
        "q1": {"simb": "a", "next": "q2"},
        "q2": {"op": "seq", "next": "q3"},
        "q3": {"simb": "a", "next": "q4"},
        "q4": {"op": "kle", "args": [{"simb": "b"}], "next": "q5"},
        }
    }
    er.nfa_to_json(nfa, "exemplos/nfa.json")
    assert os.path.exists("exemplos/nfa.json"), "File should exist"
    with open("exemplos/nfa.json", "r") as file:
        nfa_file = json.load(file)
    assert nfa == nfa_file, "Should be equal"
