
facts = {
    ("parent", "alice", "bob"),
    ("parent", "bob", "charlie"),
}

rules = [
    {
        "head": ("grandparent", "X", "Y"),
        "body": [
            ("parent", "X", "Z"),
            ("parent", "Z", "Y"),
        ]
    }
]


def is_variable(x):
    return x.isupper()


def unify(pattern, fact, bindings):
    new_bindings = bindings.copy()

    for p, f in zip(pattern, fact):
        if is_variable(p):
            if p in new_bindings:
                if new_bindings[p] != f:
                    return None
            else:
                new_bindings[p] = f
        elif p != f:
            return None

    return new_bindings


def substitute(statement, bindings):
    return tuple(bindings.get(x, x) for x in statement)


def backward_chain(goal, bindings={}):
    for fact in facts:
        result = unify(goal, fact, bindings)
        if result is not None:
            return True

    for rule in rules:
        head = rule["head"]

        result = unify(head, goal, bindings)

        if result is not None:
            success = True

            for condition in rule["body"]:
                new_goal = substitute(condition, result)

                if not backward_chain(new_goal, result):
                    success = False
                    break

            if success:
                return True

    return False


goal = ("grandparent", "alice", "charlie")

print("Goal:", goal)
print("Result:", backward_chain(goal))
