def test_no_solution_returns_none():
    # TODO: this is your job. Construct a problem where the goal is
    # unreachable — e.g. a goal that includes an action name not in
    # ACTIONS, or an action whose "requires" set can never be satisfied
    # (a circular or impossible prerequisite). Then assert that
    # bfs_search returns None instead of crashing or hanging forever.
    impossible_goal = GOAL | {"impossible_action"}
    plan = bfs_search(
        START,
        impossible_goal,
        available_actions,
        apply_action
    )
    assert plan is None
