from langchain_core.runnables import RunnableLambda
 
 
facts = [
    ("man", "socrates"),
    ("man", "aristotle"),
    ("man", "plato"),
    ("man", "hercules"),
    ("man", "homer"),
    ("woman", "athena"),
    ("woman", "helen"),
    ("woman", "cleopatra"),
    ("mortal", "helen"),
    ("mortal", "homer"),
]
 
rules = [
    {
        "head": ("mortal", "X"),
        "body": [("man", "X")],
    },
]
 
 
def is_var(x):
    return x[0].isupper()
 
def unify(pattern, fact, bindings):
    if len(pattern) != len(fact):
        return None
    b = bindings.copy()
    for p, f in zip(pattern, fact):
        if is_var(p):
            if p in b and b[p] != f:
                return None
            b[p] = f
        elif p != f:
            return None
    return b
 
def substitute(term, bindings):
    return tuple(bindings.get(x, x) for x in term)
 
def prove(goal, bindings, trace):
    for fact in facts:
        result = unify(goal, fact, bindings)
        if result is not None:
            trace.append(f"  fact: {fact}")
            return True, result
    for rule in rules:
        result = unify(rule["head"], goal, bindings)
        if result is not None:
            trace.append(f"  rule: {rule['head']}")
            b = result.copy()
            success = True
            for condition in rule["body"]:
                sub = substitute(condition, b)
                ok, b = prove(sub, b, trace)
                if not ok:
                    success = False
                    break
            if success:
                return True, b
    return False, bindings
 
# --- LangChain Chain ---
 
def run_query(query):
    trace = [f"Query: {query}"]
    result, _ = prove(query, {}, trace)
    trace.append(f"Result: {'TRUE' if result else 'FALSE'}")
    return "\n".join(trace)
 
chain = RunnableLambda(run_query)
 

 
queries = [
    ("mortal", "socrates"),
    ("mortal", "helen"),
    ("mortal", "cleopatra"),
    ("man", "plato"),
    ("woman", "athena"),
]
 
for q in queries:
    print(chain.invoke(q))
    print()
 