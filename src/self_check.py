from csp import backtracking_search
from restoration_csp import VARIABLES, DOMAINS, build_constraints

for cap in (4, 3, 2):
    solutions = backtracking_search(VARIABLES, DOMAINS, build_constraints(tranche_cap=cap), all_solutions=True)
    print(cap, len(solutions))