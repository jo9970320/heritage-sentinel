import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from planner import bfs_search
import restoration_graph as rg #gives the restoration graph a nickname
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

if __name__ == '__main__':
    unittest.main()