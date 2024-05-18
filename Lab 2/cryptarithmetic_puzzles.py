from CSP_solver import *

puzzle = "ONE + NINE + TWENTY + FIFTY = EIGHTY"

letters = []

for ch in puzzle:
    if str.isalpha(ch) and ch not in letters:
        letters.append(ch)

variables = []

for l in letters:
    v = Variable(l, domain=list(range(len(letters))))
    variables.append(v)

constraints = []
combinations = []

# TODO: Fix constraints

"""
So for the example ONE + NINE + TWENTY + FIFTY = EIGHTY, we need it so each ch, when assigned a var, will follow the equation and equate to the solution, EIGHTY, or whatever the sum of that word is.
"""
for i in range(len(letters)):
    for j in range(len(letters)):

        if i != j:
            c = Constraint(f"{letters[i]} != {letters[j]}")
            constraints.append(c)
        else:
            c = Constraint(f"{letters[i]} == {letters[j]}")
            constraints.append(c)
"""            if (i, j) not in combinations and (j, i) not in combinations:
                combinations.append((i, j))
                c = Constraint(f"{i} != {j}")
                constraints.append(c)"""


csp = CSP(variables, constraints, keep_node=False, keep_arc=False, heuristic=None)
csp.solve(verbose=False)
