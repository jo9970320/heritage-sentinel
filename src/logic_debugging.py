from logic import forward_chain

known, why = forward_chain({"a"}, [(frozenset({"a"}), "b"), (frozenset({"b"}), "c")])
print(sorted(known))

print(list(frozenset({"damage_crack", "damage_loose_base", "severity_minor"})))