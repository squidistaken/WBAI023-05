from CSP_solver import *

"""
Danger lies before you, while safety lies behind,
Two of us will help you, whichever you would find,
One among us seven will let you move ahead,
Another will transport the drinker back instead,
Two among our number hold only nettle wine,
Three of us are killers, waiting hidden in line.
Choose, unless you wish to stay here for evermore,
To help you in your choice, we give you these clues four:
First, however slyly the poison tries to hide
You will always find some on nettle wine’s left side;
Second, different are those who stand at either end,
But if you would move onwards, neither is your friend;
Third, as you see clearly, all are different size,
Neither dwarf nor giant holds death in their insides;
Fourth, the second left and the second on the right
Are twins once you taste them, though different at first sight.
"""

variables = [
    Variable("potion1", domain=["wine", "poison", "onwards", "back"]),
    Variable("potion2", domain=["wine", "poison", "onwards", "back"]),
    Variable("potion3", domain=["wine", "poison", "onwards", "back"]),
    Variable("potion4", domain=["wine", "poison", "onwards", "back"]),
    Variable("potion5", domain=["wine", "poison", "onwards", "back"]),
    Variable("potion6", domain=["wine", "poison", "onwards", "back"]),
    Variable("potion7", domain=["wine", "poison", "onwards", "back"]),
]

constraints = [
    Constraint("[potion1,potion2,potion3,potion4,potion5,potion6,potion7].count(\"wine\") == 2"),
    Constraint("[potion1,potion2,potion3,potion4,potion5,potion6,potion7].count(\"poison\") == 3"),
    Constraint("[potion1,potion2,potion3,potion4,potion5,potion6,potion7].count(\"onwards\") == 1"),
    Constraint("[potion1,potion2,potion3,potion4,potion5,potion6,potion7].count(\"back\") == 1"),
]

# First, however slyly the poison tries to hide You will always find some on nettle wine’s left side;
for i in range(2, 8):
    constraints.append(Constraint(f"potion{i} != \"wine\" or potion{i - 1} == \"poison\""))
constraints.append(Constraint(f"potion1 != \"wine\""))

# second, different are those who stand at either end, But if you would move onwards, neither is your friend;
constraints.append(Constraint(f"potion1 != potion7"))
constraints.append(Constraint(f"potion1 != \"onwards\""))
constraints.append(Constraint(f"potion7 != \"onwards\""))

# Third, as you see clearly, all are different size, Neither dwarf nor giant holds death in their insides;
constraints.append(Constraint(f"potion3 != \"poison\""))
constraints.append(Constraint(f"potion6 != \"poison\""))

# Fourth, the second left and the second on the right Are twins once you taste them, though different at first sight.
constraints.append(Constraint(f"potion2 == potion6"))

csp = CSP(variables, constraints, keep_node=False, keep_arc=False, heuristic=None)
csp.solve(verbose=False)
