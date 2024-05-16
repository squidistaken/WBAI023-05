from  CSP_solver import *

variables = [
    Variable("A", domain = [4,5,6,7,8] ),
    Variable("B", domain = [1,2,3,4,5] ),
    Variable("C", domain = [1,2,3,4,5,6,7,8,9] ),
    Variable("D", domain = [0,1,2,3,4,5,6] ),
    Variable("E", domain = [0,1] ),
    Variable("F", domain = [0,1] )
]

constraints = [
    Constraint("A  < D + B"),
    Constraint("B  > D + C"),
    Constraint("C  > D - A"),
    Constraint("B * D == A * C"),
    Constraint("A*E + B* F + C != D")
]

csp = CSP(variables, constraints, keep_node=False, keep_arc=False, heuristic="deg")
csp.solve()