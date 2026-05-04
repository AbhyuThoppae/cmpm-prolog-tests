import re
import os
import tempfile
from pyswip import Prolog
 
 
 
KB_FACTS = """
Man(Socrates, True)
Man(Aristotle, True)
Man(Plato, True)
Man(Hercules, True)
Man(Homer, True)
Woman(Athena, True)
Woman(Helen, True)
Woman(Cleopatra, True)
Mortal(Helen, True)
Mortal(Homer, True)
""".strip()
 
KB_RULES = """
Man($x, True) >>> Mortal($x, True)
""".strip()
 
# Each test: (plain English question, logic query string, expected answer)
TESTS = [
    ("Is Socrates mortal?",   "Mortal(Socrates, True)",  True),
    ("Is Athena mortal?",     "Mortal(Athena, True)",    False),
    ("Is Cleopatra a man?",   "Man(Cleopatra, True)",    False),
    ("Is Helen mortal?",      "Mortal(Helen, True)",     True),
    ("Is Homer mortal?",      "Mortal(Homer, True)",     True),
    ("Is Plato mortal?",      "Mortal(Plato, True)",     True),
    ("Is Athena a woman?",    "Woman(Athena, True)",     True),
    ("Is Hercules a woman?",  "Woman(Hercules, True)",   False),
]
 
 

def build_prolog_kb(facts_str, rules_str):
    """
    Convert the repo's Facts/Rules format into Prolog clauses.
 
    Fact:  Man(Socrates, True)          → man(socrates).
    Fact:  Man(Socrates, False)         → (skipped — false facts are just absent)
    Rule:  Man($x, True) >>> Mortal($x, True)  → mortal(X) :- man(X).
    """
    clauses = []
 
    for line in facts_str.splitlines():
        line = line.split(":::")[0].strip()
        if not line:
            continue
        m = re.match(r"(\w+)\((\w+),\s*(True|False)\)", line)
        if m:
            pred, entity, value = m.group(1).lower(), m.group(2).lower(), m.group(3)
            if value == "True":
                clauses.append(f"{pred}({entity}).")
 
    for line in rules_str.splitlines():
        line = line.split(":::")[0].strip()
        if ">>>" not in line:
            continue
        premise_str, conclusion_str = line.split(">>>")
        # parse premise atoms like "Man($x, True)"
        def to_prolog_atom(s):
            m = re.match(r"(\w+)\(\$x,\s*(True|False)\)", s.strip())
            if not m:
                return None
            pred, value = m.group(1).lower(), m.group(2)
            return f"{pred}(X)" if value == "True" else f"\\+{pred}(X)"
 
        premises    = [to_prolog_atom(p) for p in premise_str.split("&&")]
        conclusions = [to_prolog_atom(c) for c in conclusion_str.split("&&")]
        if None not in premises and None not in conclusions:
            clauses.append(f"{conclusions[0]} :- {', '.join(premises)}.")
 
    return "\n".join(clauses)
 
 
def ask(prolog_kb_text, query_str):
    """
    Write the KB to a temp file, load it into SWI-Prolog, run the query.
    Returns True/False.
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".pl", delete=False) as f:
        f.write(prolog_kb_text)
        path = f.name
    try:
        p = Prolog()
        p.consult(path)
        # parse "Mortal(Socrates, True)" → "mortal(socrates)"
        m = re.match(r"(\w+)\((\w+),\s*(True|False)\)", query_str)
        if not m:
            return None
        pl_query = f"{m.group(1).lower()}({m.group(2).lower()})"
        return bool(list(p.query(pl_query)))
    finally:
        os.unlink(path)
 
 
# ─────────────────────────────────────────────────────────────────────────────
# Run all tests
# ─────────────────────────────────────────────────────────────────────────────
 
if __name__ == "__main__":
    kb = build_prolog_kb(KB_FACTS, KB_RULES)
 
    print("Generated Prolog KB:")
    print("─" * 40)
    print(kb)
    print("─" * 40)
 
    print("\nRunning tests:\n")
    passed = 0
    for question, query, expected in TESTS:
        result = ask(kb, query)
        ok = result == expected
        if ok:
            passed += 1
        print(f"  {'✓' if ok else '✗'}  {question}")
        print(f"     Query:    {query}")
        print(f"     Expected: {expected}  |  Got: {result}")
        print()
 
    print(f"Result: {passed}/{len(TESTS)} passed")
 