import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from planner import bfs_search
from restoration_graph import START, GOAL, available_actions, apply_action

class TestPlanner(unittest.TestCase):
    def test_valid_plan(self):
        plan = bfs_search(START, GOAL, available_actions, apply_action)
        self.assertIsNotNone(plan) #no possible sequence, where our function returns none

        state = START

        for action in plan: #loop through each possible action in the plan
            self.assertIn(action, available_actions(state)) #this will fail if the move is illegal
            state = apply_action(state, action) #take the valid move, update the state

        self.assertEqual(state, GOAL) #after looping through, the repair plan should be done


if __name__ == '__main__':
    unittest.main()
