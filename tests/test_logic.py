import json
import random
from pathlib import Path

import pytest
import validate as validate_module
from logic import forward_chain
from report_rules import CLAUSES
from validate import validate, to_facts


#finds the data file from where this test file lives
PROJECT_FOLDER = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_FOLDER / "data" / "reports.jsonl"


def load_reports():
    reports = {}

    with open(DATA_FILE) as file:
        for line in file:
            report = json.loads(line)
            reports[report["id"]] = report

    return reports


REPORTS = load_reports()


def test_chain_derives_transitively():
    facts = {"a"}
    rules = [
        (frozenset({"a"}), "b"),
        (frozenset({"b"}), "c")
    ]

    known, _ = forward_chain(facts, rules)

    assert known == {"a", "b", "c"}


def test_cycle_terminates():
    facts = {"a"}
    rules = [
        (frozenset({"a"}), "b"),
        (frozenset({"b"}), "a")
    ]  #a gives b, b gives a

    known, _ = forward_chain(facts, rules)

    assert known == {"a", "b"}  #if the loop never ends, we never get here


def test_clause_order_irrelevant():
    facts = to_facts(REPORTS["r9"])
    expected, _ = forward_chain(facts, CLAUSES)

    for seed in range(20):
        shuffled_rules = list(CLAUSES)

        #each seed gives a repeatable shuffle
        generator = random.Random(seed)
        generator.shuffle(shuffled_rules)

        known, _ = forward_chain(facts, shuffled_rules)

        assert known == expected


@pytest.mark.parametrize("report_id", ["r1", "r3", "r5", "r7"])
def test_valid_reports_accepted(report_id):
    ok, reasons, _ = validate(REPORTS[report_id])

    assert ok
    assert reasons == []


@pytest.mark.parametrize("report_id, expected_reason", [
    ("r2", "invalid:structural_risk_marked_minor"),
    ("r4", "invalid:rot_on_inorganic"),
    ("r6", "invalid:corrosion_on_organic"),
    ("r8", "invalid:none_but_damaged")
])
def test_each_rule_fires_alone(report_id, expected_reason):
    ok, reasons, _ = validate(REPORTS[report_id])

    assert not ok
    assert reasons == [expected_reason]


def test_multiple_violations_all_reported():
    ok, reasons, _ = validate(REPORTS["r9"])  #r9 breaks two rules at once

    expected_reasons = [
        "invalid:rot_on_inorganic",
        "invalid:structural_risk_marked_minor"
    ]

    assert not ok
    assert reasons == expected_reasons  #both, in sorted order


@pytest.mark.parametrize("report_id, expected_text", [
    ("r10", "missing field"),
    ("r11", "unknown material")
])
def test_schema_errors_are_not_logic_errors(report_id, expected_text):
    ok, reasons, proofs = validate(REPORTS[report_id])

    assert not ok
    assert reasons[0].startswith("schema:")
    assert expected_text in reasons[0]
    assert proofs == {}


def test_proofs_bottom_out_in_given_facts():
    ok, reasons, proofs = validate(REPORTS["r2"])
    proof_lines = proofs["invalid:structural_risk_marked_minor"]  #the proof lines for r2

    leaves = []

    for line in proof_lines:
        if "because" not in line:  #lines with no "because" are the end of a chain
            leaves.append(line)

    assert len(leaves) >= 1  #there has to be at least one leaf

    for leaf in leaves:
        assert "(given)" in leaf  #every leaf should be a fact straight from the report


def test_deleting_a_rule_is_caught():
    original_rules = validate_module.CLAUSES  #save the real rulebook so it can be put back
    remaining_rules = []

    for premises, conclusion in original_rules:
        if conclusion != "invalid:rot_on_inorganic":
            remaining_rules.append((premises, conclusion))

    try:
        validate_module.CLAUSES = remaining_rules  #same rulebook minus the rot rule
        ok, reasons, _ = validate(REPORTS["r4"])

        assert ok  #r4 is wrongly accepted now, so the rule mattered
        assert reasons == []

    finally:
        validate_module.CLAUSES = original_rules  #always restore, even if the assert above fails

    ok, reasons, _ = validate(REPORTS["r4"])

    assert not ok  #rule is back, r4 is rejected again
    assert reasons == ["invalid:rot_on_inorganic"]

def test_microfractures_create_structural_risk():
    ok, reasons, _ = validate(REPORTS["r12"])

    assert not ok
    assert reasons == ["invalid:structural_risk_marked_minor"]

    #without a loose base, microfractures alone do not trigger this rule
    near_miss = {
        "id": "near_miss_microfracture",
        "material": "stone",
        "damage": ["microfracture"],
        "severity": "minor"
    }

    facts = to_facts(near_miss)
    known, _ = forward_chain(facts, CLAUSES)

    assert "structural_risk" not in known

    ok, reasons, _ = validate(near_miss)

    assert ok
    assert reasons == []


def test_acid_damage_on_metal_marked_minor():
    ok, reasons, _ = validate(REPORTS["r13"])

    assert not ok
    assert reasons == ["invalid:acid_damage_on_metal_marked_minor"]

    #same material and damage, but major severity is accepted
    near_miss = {
        "id": "near_miss_acid",
        "material": "metal",
        "damage": ["acid_damage"],
        "severity": "major"
    }

    ok, reasons, _ = validate(near_miss)

    assert ok
    assert reasons == []