import json
import er
import os
import pytest

def setup_module(module):
    if os.path.exists("exemplos/nfa.json"):
        os.remove("exemplos/nfa.json")

def test_re_to_nfa():
    re = {
        "op": "seq",
        "args": [
            {
                "op": "alt",
                "args": [
                    {"simb": "a"},
                    {"simb": "b"}
                ]
            },
            {
                "simb": "c"
            }
        ]
    }
    nfa, _ = er.re_to_nfa(re)  # Unpack the tuple
    assert nfa == "(a|b)c", "Should be (a|b)c"

def test_nfa_to_json():
    nfa = {
        "Q": ["q0", "q1", "q2"],
        "V": ["a", "b"],
        "q0": "q0",
        "F": ["q2"],
        "delta": {
            "q0": {"a": "q1", "b": "q2"},
            "q1": {"a": "q1", "b": "q2"},
            "q2": {"a": "q2", "b": "q2"}
        }
    }
    er.nfa_to_json(nfa, "exemplos/nfa.json")
    assert os.path.exists("exemplos/nfa.json"), "File should exist"
    with open("exemplos/nfa.json", "r") as file:
        nfa_file = json.load(file)
    assert nfa == nfa_file, "Should be equal"
