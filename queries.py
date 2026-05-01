from pyswip import Prolog

prolog = Prolog()
prolog.consult("knowledge_base.pl")



print("\nQuery 1: Is Socrates mortal?")
result = list(prolog.query("mortal(socrates)"))
print("  SWI-Prolog: true" if result else "  SWI-Prolog: false")
print("  Python:     true" if result else "  Python:     false")

print("\nQuery 2: Is Athena mortal?")
result = list(prolog.query("mortal(athena)"))
print("  SWI-Prolog: true" if result else "  SWI-Prolog: false")
print("  Python:     true" if result else "  Python:     false")


print("\nQuery 3: Who are all the men?")
results = list(prolog.query("man(X)"))
names = [str(r["X"]) for r in results]
print(f"  SWI-Prolog: {names}")
print(f"  Python:     {names}")

print("\nQuery 4: Who are all the women?")
results = list(prolog.query("woman(X)"))
names = [str(r["X"]) for r in results]
print(f"  SWI-Prolog: {names}")
print(f"  Python:     {names}")

print("\nQuery 5: Who is mortal? (rule + direct facts combined)")
results = list(prolog.query("mortal(X)"))
names = list(dict.fromkeys([str(r["X"]) for r in results]))
print(f"  SWI-Prolog: {names}")
print(f"  Python:     {names}")

