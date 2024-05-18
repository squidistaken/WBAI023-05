from CSP_solver import *
from utils import all_diff

# Modify here
puzzle = "ONE + NINE + TWENTY + FIFTY = EIGHTY"

letters = []

for ch in puzzle:
    if str.isalpha(ch) and ch not in letters:
        letters.append(ch)

# TODO: Do we even need this?
formatted_puzzle = ""
for ch in puzzle:
    if ch.isalpha():
        formatted_puzzle += "{" + ch + "}"
    elif ch == "=":
        formatted_puzzle += "=="
    else:
        formatted_puzzle += ch

variables = []

for l in letters:
    v = Variable(l, domain=list(range(len(letters))))
    variables.append(v)

constraints = all_diff(variables)

# TODO: Fix constraint for puzzle
c = Constraint(puzzle.replace("=", "=="))
constraints.append(c)

csp = CSP(variables, constraints, keep_node=False, keep_arc=False, heuristic=None)
csp.solve(verbose=False)
