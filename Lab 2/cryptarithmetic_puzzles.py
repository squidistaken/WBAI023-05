from CSP_solver import *

variables = [
    #Puzzle letters. With the correct range, excluding 0 when it's the first character of a word
    Variable("U", domain=list(range(1, 10))),
    Variable("N", domain=list(range(1, 10))),
    Variable("O", domain=list(range(1, 10))),
    Variable("E", domain=list(range(10))),
    Variable("F", domain=list(range(10))),
    Variable("Z", domain=list(range(10)))
]

constraints = [
    #Each letter must have a different value
    Constraint("U != N"), Constraint("U != E"), Constraint("U != F"), Constraint("U != O"), Constraint("U != Z"), 
    Constraint("N != E"), Constraint("N != F"), Constraint("N != O"), Constraint("N != Z"),
    Constraint("E != F"), Constraint("E != O"), Constraint("E != Z"),
    Constraint("F != O"), Constraint("F != Z"), 
    Constraint("O != Z"),
    #When added together with the numbers for the letters filled in should result in the original words
    Constraint("10*U + N + 10*U + N + 1000*N + 100*E + 10*U + F == 1000*O + 100*N + 10*Z + E")
]

csp = CSP(variables, constraints, keep_node=False, keep_arc=False, heuristic="mrv")
csp.solve(verbose=False)