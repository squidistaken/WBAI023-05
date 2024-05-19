from CSP_solver import *
from utils import all_diff

# Modify here
puzzle = "SEND + MORE = MONEY"

letters = []

# Variables
for ch in puzzle:
    if ch.isalpha() and ch not in letters:
        letters.append(ch)

variables = []

for l in letters:
    v = Variable(l, domain=list(range(0, 10)))
    variables.append(v)

# Constraints
# Each letter stands for a unique digit, and the same letter stands for the same digit throughout the puzzle.
constraints = all_diff(variables)

beginners = []
for i in puzzle.split():
    if i.isalpha():
        # TODO: Fix this constraint
        constraints.append(Constraint(f"{i} = \"\".join({list(i)})"))
        if i[0] not in beginners:
            beginners.append(i[0])
            # There must be no leading zeros.
            constraints.append(Constraint(f"{i[0]} != 0"))


constraints.append(Constraint(puzzle.replace("=", "==")))

csp = CSP(variables, constraints, keep_node=False, keep_arc=False, heuristic=None)
csp.solve(verbose=False)
