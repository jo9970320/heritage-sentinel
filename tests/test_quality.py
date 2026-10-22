import hashlib, json, os, subprocess, sys, tempfile
import pytest
import make_data
from quality import load, classify, run, batch_drift
from report_model import ReportModel, calibrate
from validate import validate

REF = load("data/reference.jsonl")
MODEL = ReportModel(REF)
THRESHOLD = calibrate(MODEL, REF, 0.02)

def by_id(path):
    return {r["id"]: r for r in load(path)}

A = by_id("data/incoming_a.jsonl")

def test_reference_data_passes_the_logic_gate():
    # Your "trusted" data must itself obey the Lab 4 rules.
    assert all(validate(r)[0] for r in REF)

def test_calibration_flags_about_two_percent_of_reference():
    flagged = sum(MODEL.log_likelihood(r) < THRESHOLD for r in REF)
    assert 7 <= flagged <= 9          # 2% of 400 = 8, allow +/-1 for percentile conventions

@pytest.mark.parametrize("rid", ["a-odd1", "a-odd2", "a-odd3"])
def test_logic_valid_but_improbable_is_quarantined(rid):
    assert validate(A[rid])[0]                       # Lab 4 alone would accept it
    verdict, detail = classify(A[rid], MODEL, THRESHOLD)
    assert verdict == "quarantine" and "improbable" in detail[0]

@pytest.mark.parametrize("rid", ["a-bad1", "a-bad2"])
def test_impossible_is_rejected_not_quarantined(rid):
    verdict, _ = classify(A[rid], MODEL, THRESHOLD)
    assert verdict == "reject"

def test_unseen_combination_scores_finite():
    ll = MODEL.log_likelihood(A["a-odd1"])           # stone + corrosion never occurs in reference
    assert ll == ll and ll > -100                    # not NaN, not -inf

def test_without_smoothing_unseen_combination_blows_up():
    model = ReportModel(REF, alpha=0.0)

    with pytest.raises(ValueError):
        model.log_likelihood(A["a-odd1"])

def test_batch_a_summary():
    res = run("data/incoming_a.jsonl")
    assert res["summary"] == {"accept": 100, "quarantine": 3, "reject": 2}
    assert res["drift"]["material_mix"][2] is False

def test_drifted_batch_passes_every_record_check_but_fails_the_batch_check():
    result = run("data/incoming_b.jsonl")

    assert result["summary"] == {"accept": 100}
    assert result["drift"]["material_mix"][2] is True

def test_heldout_quarantine_rate_is_near_target():
    total_reports = 0
    quarantined = 0

    for seed in range(100, 120):
        batch = make_data.make_batch(
            seed, 100, "h", make_data.MATERIAL_P
        )

        for report in batch:
            total_reports += 1

            if MODEL.log_likelihood(report) < THRESHOLD:
                quarantined += 1

    rate = quarantined / total_reports

    assert 0.005 <= rate <= 0.04

def test_clean_batches_rarely_raise_drift_alarms():
    alarms = sum(
        batch_drift(make_data.make_batch(s, 100, "c", make_data.MATERIAL_P), MODEL)["material_mix"][2]
        for s in range(100, 150))
    assert alarms <= 1

def test_data_generation_is_deterministic():
    with tempfile.TemporaryDirectory() as dir1, tempfile.TemporaryDirectory() as dir2:

        subprocess.run(
            [sys.executable, "tools/make_data.py", dir1],
            check=True
        )

        subprocess.run(
            [sys.executable, "tools/make_data.py", dir2],
            check=True
        )

        for filename in ["reference.jsonl", "incoming_a.jsonl", "incoming_b.jsonl"]:
            with open(os.path.join(dir1, filename), "rb") as f:
                hash1 = hashlib.sha256(f.read()).hexdigest()

            with open(os.path.join(dir2, filename), "rb") as f:
                hash2 = hashlib.sha256(f.read()).hexdigest()

            assert hash1 == hash2

def test_pipeline_output_is_reproducible_across_processes():
    runs = [subprocess.run([sys.executable, "src/quality.py", "data/incoming_a.jsonl",
                            os.devnull], capture_output=True, text=True, check=True).stdout
            for _ in range(2)]
    assert runs[0] == runs[1]

def test_severity_drift_detected():
    batch = make_data.make_batch(
        100, 100, "s", make_data.MATERIAL_P
    )

    # Change every report's severity to major
    for report in batch:
        report["severity"] = "major"

    result = batch_drift(batch, MODEL)

    assert result["severity_mix"][2] is True

def test_clean_batch_no_severity_drift():
    batch = make_data.make_batch(
        100, 100, "s", make_data.MATERIAL_P
    )

    result = batch_drift(batch, MODEL)

    assert result["severity_mix"][2] is False