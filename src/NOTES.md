# if you swapped the problem file, did the planner need to change? Why or why not?
As long as the action format stays in the given manner in which we organized it, the planner wouldn't need to be changed. This is simply due to the structure of our BFS algorithm as it checks the entrance of the actions and searches through similar keywords. This can be seen as modular as our BFS search algorithm is a completely independent "module" that can only explore the states that it is given. 

Lab 1 P2
test_no_solution_returns_none confirmed that BFS correctly returns None when the goal is unreachable instead of crashing or looping forever.

test_large_action_set_terminates confirmed that BFS can handle a larger chain of actions and still finish without looping forever.

Lab 1 P3
1. What did you see in the hidden-trap experiment, and why?
When variables was created from a set, the plan could change between separate runs. This is due to sets not having a stable iteration order across Python processes.

2. Your Lab 2 oracle was correct when you wrote it. What does its failure here tell you about tests over time?
The old oracle becoming incomplete shows that tests need to evolve when the system's requirements change, especially if the tests were correct when they were orginally
written.

Lab 1 P4
1. Why does the while loop always terminate? What quantity grows each pass, and what bounds it?

The while loop is ends because it is bounded by a finite ruleset/list of symbol/labels. So through each pass, it finds atleast one of these symbols and grows the known, but is only capable of doing so for each unique symbol. As such, it'll always end, and consequently ends because it is bounded to the amount of symbols in the ruleset

2. Why does explain call sorted(premises)? (Think back to Lab 3.)

Premises is a frozenset, a collection of strings with no fixed order. Sorted puts them in a uniform alphabetical order, so the proof lines come out the same on every run. Without it, the rejection log could differ between runs even though the reports and rules didn’t change, so it couldn’t be compared or trusted as a record.