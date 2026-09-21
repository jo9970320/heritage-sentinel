import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from planner import bfs_search
from restoration_graph import START, GOAL, available_actions, apply_action

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
