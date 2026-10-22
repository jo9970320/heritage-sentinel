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

Part D

The same report can be rejected for the same reason but show different steps depending on rule order, so keeping the order consistent makes the log easier to check during an audit.

Part E


This rule is not possible to write, using the current Horn clauses because they only check facts that are present, not whether damage is missing. To make it work, I could have to_facts add a no_damage fact when the damage list is empty, then write a rule that rejects a report with both severity_major and no_damage. This would require extra code to check for an empty list, and it would assume the report lists all damage, so an empty list means there is no damage rather than someone forgetting to record it.

Lab 1 P5
Predictions:
{"id": "a100", "material": "stone", "damage": ["fading"], "severity": "minor"} - Accept because fading on stone is normal and plausible
{"id": "a-odd1", "material": "stone", "damage": ["corrosion"], "severity": "minor"} - Quarantine because corrosion on stone is unusual however not impossible
{"id": "a-odd2", "material": "ceramic", "damage": ["crack", "fading", "corrosion"], "severity": "major"} - Quarantine because corrosion on ceramic is highly unlikely but still not impossible
{"id": "a-odd3", "material": "textile", "damage": ["crack", "loose_base"], "severity": "major"} - Quarantine due to a textile object with both a crack and a loose base is unusual
{"id": "a-bad1", "material": "stone", "damage": ["rot"], "severity": "minor"} - Reject because rot on stone violates the logic rules
{"id": "a-bad2", "material": "marble", "damage": ["crack"], "severity": "minor"} - Reject because marle is not a recognized material in the schema
1. The predictions matched the pipeline's results. Reports a-odd1, a-odd2, a-odd3 were quarantined as they were statistically unusual, while a-bad1 and a-bad2 were rejected as they violated the validation rules

Independence:
2. The model assumes that damage types are independent however, a crack could realistically weaken the structure and cause the base to become lose. In other words, the presence of one type of damage could increase the likelihood of another.

Parameters:
3. The model has 35 free parameters which are 4 for materials, 25 for damage probabilities, and 6 for severity. Having 400 reference reports is able to provide a reasonable amount of data, but with only 40 reports, the probability estimates would be less reliable due to some damage combinations rarly or never appearing.

Smoothing:
4. A realistic situation would be receiving a report with a damage combination that was never seen in the historical data. Without smoothing, the model would be able to assign it a probability of zero which can cause an error when calculating its log-likelihood.

Calibration:
5. The gap was small because the training and test reports were generated using the same probability distributions which led to their patterns being similar. The gap could become larger if the model overfitted the training data, had fewer reference reports, or the new reports came from a different distribution.

Quaratine versus reject:
6. The system quarantines rare but valid reports for human review, which could delay important discoveries. If missing a rare discovery were more costly than accepting a typo, I would lower the likelihood threshold so that fewer reports get quarantined, but this would also allow more incorrect reports to be accepted.