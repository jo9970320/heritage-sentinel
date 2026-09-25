import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from restoration_graph import ACTIONS, START, GOAL, available_actions, apply_action


from planner import bfs_search
import restoration_graph as rg #gives the restoration graph a nickname/alias
import taco_graph as tc #same thing for taco graph

class TestPlanner(unittest.TestCase):
    def check_plan_validity(self, problem):
        plan = bfs_search(problem.START, problem.GOAL,
                          problem.available_actions, problem.apply_action)
        self.assertIsNotNone(plan) #no possible sequence, where our function returns none

        state = problem.START

        for action in plan: #loop through each possible action in the plan
            self.assertIn(action, problem.available_actions(state)) #this will fail if the move is illegal
            state = problem.apply_action(state, action)  #take the valid move, update the state

        self.assertEqual(state, problem.GOAL) #after looping through, the repair plan should be done

    def test_statue_plan(self):
        self.check_plan_validity(rg)

    def test_taco_plan(self):
        self.check_plan_validity(tc)

def is_valid_plan(plan, actions=ACTIONS):
    """A plan is valid if every action's prerequisites are satisfied by
    the actions before it, and every required action appears exactly once."""
    completed = set()
    for action in plan:
        if action in completed:
            return False          # duplicate action
        if not actions[action]["requires"].issubset(completed):
            return False          # prerequisite violated
        completed.add(action)
    return completed == set(actions.keys())


def test_finds_a_valid_plan():
    plan = bfs_search(START, GOAL, available_actions, apply_action)
    assert plan is not None
    assert is_valid_plan(plan)


def test_trivial_already_done():
    # start == goal: the plan should be empty, not None, not a crash
    plan = bfs_search(GOAL, GOAL, available_actions, apply_action)
    assert plan == []


def test_plan_has_no_duplicate_actions():
    plan = bfs_search(START, GOAL, available_actions, apply_action)
    assert len(plan) == len(set(plan))


def test_no_solution_returns_none():
    impossible_goal = GOAL | {"impossible_action"}
    plan = bfs_search(
        START,
        impossible_goal,
        available_actions,
        apply_action
    )
    assert plan is None


def test_large_action_set_terminates():
    actions = {}

    for i in range(20):
        action = f"action_{i}"

        if i == 0:
            requires = set()
        else:
            requires = {f"action_{i - 1}"}

        actions[action] = {
            "requires": requires
        }

    start = frozenset()
    goal = frozenset(actions.keys())

    def available_actions_large(state):
        available = []

        for action in actions:
            if action not in state and actions[action]["requires"].issubset(state):
                available.append(action)

        return available

    def apply_action_large(state, action):
        return state | {action}

    plan = bfs_search(
        start,
        goal,
        available_actions_large,
        apply_action_large
    )

    assert plan is not None
    assert is_valid_plan(plan, actions)



if __name__ == '__main__':
    unittest.main()