import json
import er
import os

def test_er_afnd():
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
    nfa, _ = er.output(re)  # Unpack the tuple
    assert nfa == "a|ab*", "Should be a|ab*"
    er.afnd_json(nfa, "er_nfa.json")
    assert os.path.exists("er_nfa.json"), "File should exist"
    with open("er_nfa.json", "r") as file:
        nfa_file = json.load(file)
    assert nfa == nfa_file, "Should be equal"
    
def test_afnd_json():
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
    er.afnd_json(nfa, "nfa.json")
    assert os.path.exists("nfa.json"), "File should exist"
    with open("nfa.json", "r") as file:
        nfa_file = json.load(file)
    assert nfa == nfa_file, "Should be equal"
