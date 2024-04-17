import json
import er
import os

er_dict: dict = {}
with open("exemplos/exemplo01.er.json", "r") as file:
    er_dict = json.load(file)

def test_er_to_afnd():
    afnd = er.to_afnd(er_dict)
    assert isinstance(afnd, dict), "Should be a dictionary"