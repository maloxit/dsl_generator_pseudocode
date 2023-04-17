from enum import Enum
import json

def load_dsl_info(dsl_info_path):
    file = open(dsl_info_path, "r", encoding="UTF-8")
    data = file.read()
    data = json.loads(data)
    terms = data["TERMINALS"]
    keys = data["KEYS"]
    nonterms = data["NONTERMINALS"]
    axiom = data["AXIOM"]
    return terms, keys, nonterms, axiom
