from CSP_solver import *

variables = [
    Variable("A", domain=[1, 2, 3, 4]),
    Variable("B", domain=[1, 2, 3, 4]),
    Variable("C", domain=[1, 2, 3, 4]),
    Variable("D", domain=[1, 2, 3, 4]),
    Variable("E", domain=[1, 2, 3, 4])
]

constraints = [
    Constraint("B >= A"),
    Constraint("A > D"),
    Constraint("C != A"),
    Constraint("B != C"),
    Constraint("C != D + 1"),
    Constraint("C != D"),
    Constraint("D > E"),
    Constraint("C > E"),
]

csp = CSP(variables, constraints, keep_node=False, keep_arc=False, heuristic=None)
csp.solve(verbose=False)
