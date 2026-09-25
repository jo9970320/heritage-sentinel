# if you swapped the problem file, did the planner need to change? Why or why not?
As long as the action format stays in the given manner in which we organized it, the planner wouldn't need to be changed. This is simply due to the structure of our BFS algorithm as it checks the entrance of the actions and searches through similar keywords. This can be seen as modular as our BFS search algorithm is a completely independent "module" that can only explore the states that it is given. 

Lab 1 P2
test_no_solution_returns_none confirmed that BFS correctly returns None when the goal is unreachable instead of crashing or looping forever.

test_large_action_set_terminates confirmed that BFS can handle a larger chain of actions and still finish without looping forever.