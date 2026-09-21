# planner.py — search algorithm only. No mention of statues, cracks, or pigment allowed here.
from collections import deque

def bfs_search(start, goal, available_actions, apply_action):
    frontier = deque([(start, [])])
    visited = {start}
    while frontier:
        state, path = frontier.popleft()
        if state == goal:
            return path
        # TODO: for each action available from `state`, compute the next
        # state, and if it hasn't been visited, add it to the frontier
        # with the updated path.
        for action in available_actions(state): #checks for all the potential actions you can do
            next_state = apply_action(state, action) #creates the next state, and can only choose actions that have prerequisites met
            if next_state not in visited:
                visited.add(next_state) #adding the new state to visited to avoid repeats
                frontier.append((next_state, path + [action])) # queue the new state along with the route that reached it

    return None  # no valid sequence exists