#report_rules.py — the knowledge base. Domain vocabulary lives here and only here.

MATERIALS = {"stone", "ceramic", "metal", "wood", "textile"}

DAMAGE = {
    "crack", "loose_base", "fading", "rot", "corrosion",
    "microfracture", "acid_damage"
}

SEVERITIES = {"none", "minor", "major"}


def rule(conclusion, *premises):
    return (frozenset(premises), conclusion)


CLAUSES = [
    #material classes
    rule("inorganic", "material_stone"),
    rule("inorganic", "material_ceramic"),
    rule("inorganic", "material_metal"),
    rule("organic", "material_wood"),
    rule("organic", "material_textile"),

    #any damage type counts as damage
    *[rule("has_damage", f"damage_{d}") for d in sorted(DAMAGE)],

    #derived concepts
    rule("structural_risk", "damage_crack", "damage_loose_base"),

    #microfractures with a loose base also create structural risk
    rule("structural_risk", "damage_microfracture", "damage_loose_base"),

    #a conclusion starting with "invalid:" is a violation
    rule("invalid:rot_on_inorganic", "damage_rot", "inorganic"),
    rule("invalid:corrosion_on_organic", "damage_corrosion", "organic"),
    rule("invalid:none_but_damaged", "severity_none", "has_damage"),
    rule("invalid:structural_risk_marked_minor", "structural_risk", "severity_minor"),

    #acid damage on metal should not be marked minor
    rule("invalid:acid_damage_on_metal_marked_minor",
         "material_metal", "damage_acid_damage", "severity_minor"),
]