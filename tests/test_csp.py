import subprocess
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from csp import backtracking_search
from restoration_csp import VARIABLES, DOMAINS, build_constraints
from test_planner import is_valid_plan

def solve(seed=0, cap=4, all_solutions=False):
    return backtracking_search(VARIABLES, DOMAINS, build_constraints(tranche_cap=cap),
                               seed=seed, all_solutions=all_solutions)

def to_plan(assignment):
    return sorted(assignment, key=assignment.get)

def test_solution_is_valid():
    plan = to_plan(solve()[0])
    assert is_valid_plan(plan, tranche_cap=4)

def test_same_seed_same_plan():
    assert solve(seed=7) == solve(seed=7)

def test_solution_counts():
    assert len(solve(cap=4, all_solutions=True)) == 5
    assert len(solve(cap=3, all_solutions=True)) == 1
    assert len(solve(cap=2, all_solutions=True)) == 0

def test_old_oracle_gap_is_closed():
    bad = ["stabilize_base", "seal_crack", "clean_surface", "restore_pigment"]
    assert not is_valid_plan(bad, tranche_cap=4)

def test_reproducible_across_processes():
    run1 = subprocess.run(
        [sys.executable, "src/main_csp.py"],
        capture_output=True,
        text=True,
        check=True
    ).stdout

    run2 = subprocess.run(
        [sys.executable, "src/main_csp.py"],
        capture_output=True,
        text=True,
        check=True
    ).stdout

    assert run1 == run2