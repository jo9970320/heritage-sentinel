# toy problem, using tacos

ACTIONS = {
    "warm_tortilla": {"requires": set(), "cost": 1},
    "cook_meat": {"requires": set(), "cost": 3},
    "add_cheese": {"requires": {"warm_tortilla"}, "cost": 1},
    "fold_taco": {"requires": {"add_cheese", "cook_meat"}, "cost": 1},
}

GOAL = frozenset(ACTIONS.keys())  # every step done
START = frozenset()

def available_actions(state): #same as the restoration graph's
    return [a for a, info in ACTIONS.items()
            if a not in state and info["requires"].issubset(state)]

def apply_action(state, action):
    return state | {action}