import restoration_graph
import taco_graph
from planner import bfs_search

problem = taco_graph #change this statement to which graph you're testing

if __name__ == "__main__":
    plan = bfs_search(problem.START, problem.GOAL,
                      problem.available_actions, problem.apply_action)
    print("Plan:", plan)