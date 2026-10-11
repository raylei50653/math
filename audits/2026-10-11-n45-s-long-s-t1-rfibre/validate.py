#!/usr/bin/env python3
"""Read-only delivery validation; this does not prove the paper theorem."""
import argparse
import hashlib
import itertools
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = "f2692089ad4259808e27d9b7e882ac09505b180a"
DISPATCH = ROOT / "audits/2026-10-11-n45-s-long-s-rfibre-dispatch"


def pin(path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def read(name):
    return json.loads((HERE / name).read_text())


def contents():
    inputs, claims, coverage, checks = [read(x) for x in
                                       ["inputs.json", "claims.json", "coverage.json", "checks.json"]]
    assert inputs["base"] == claims["base"] == coverage["base"] == BASE
    assert all(x["review_status"] == "待獨立驗收" for x in [inputs, claims, coverage, checks])
    assert len(inputs["BASE_blobs"]) == 12 and len(inputs["sealed_audit_SHA256"]) == 11
    for record in inputs["BASE_blobs"] + inputs["sealed_audit_SHA256"]:
        wanted = {"bytes": record["bytes"], "sha256": record["sha256"]}
        assert pin(ROOT / record["path"]) == wanted
        assert pin(ROOT / record["dispatch_frozen_path"]) == wanted
        if record["authority"] == "BASE Git blob":
            got = subprocess.check_output(["git", "show", BASE + ":" + record["path"]], cwd=ROOT)
            assert hashlib.sha256(got).hexdigest() == record["sha256"]
        else:
            assert record["git_blob"] is None and not record["included_in_BASE_claimed"]
    for record in inputs["external_theorem_pins"]:
        assert pin(ROOT / record["path"]) == {"bytes": record["bytes"], "sha256": record["sha256"]}
        assert record["git_blob"] is None
    assert inputs["review_corrections"] == {"query_partition": [12, 4, 10, 4],
                                           "SF-RESIDUAL_extra_dependency": "SF-T2-Q0-Q1-RESTORED"}
    prior = json.loads((DISPATCH / "authority/sealed/audits/2026-10-11-n45-s-long-s-fibre/obligations.json").read_text())
    expected = {(s["SigmaG_orbit"], tuple(s["QG"]), s["beta_q"], h)
                for s in prior["schedules"] if s["t_s"] == 1 for h in [0, 2]}
    queries = coverage["queries"]
    actual = {(q["SigmaG_orbit"], tuple(q["QG"]), q["beta_q"], q["original_s_spokes"][0]) for q in queries}
    assert actual == expected and len(queries) == 28
    literal_order = coverage["literal_order"]
    assert literal_order == ["01012", "01021", "01023", "01201", "01202", "01203", "01212", "01213", "01231", "01232"]
    for q in queries:
        assert q["original_e"] == ["r", "b4"] and q["original_r_split"] == [2, 2]
        assert q["profile"] == [1, 2, 2] and q["arbitrary_size"]
        assert q["Delta"] == [x for x in q["QG"] if x != q["beta_q"]]
        assert q["QX"] == [q["beta_q"]]
        source = q["actual_source"]
        assert source["status"] == "not triggered" and not source["executed"]
        assert source["trigger_count"] is None and source["preimages"] is None
        if q["beta_q"] == 3:
            assert q["proved_restoration_rows"] == [0, 1]
            assert q["selected_Delta_restoration_row"] in set(q["Delta"]) & {0, 1}
        else:
            assert q["source_minor"] and q["selected_Delta_restoration_row"] is None
        rows = q["all_ten_literal_obligations"]
        assert len(rows) == 10
        for index, row in enumerate(rows):
            assert "".join(map(str, row["literal"])) == literal_order[index]
            assert row["gamma_b4"] == int(literal_order[index][-1])
            assert {(p["r"], p["s"]) for p in row["pins"]} == set(itertools.product(range(4), repeat=2))
            assert len(row["pins"]) == 16 and not row["full_relations_materialized"]
            assert all(p["source_preimages"] is None for p in row["pins"])
    assert coverage["schedule_count"] == 14 and coverage["paper_candidate_closed_queries"] == 28
    assert coverage["paper_restoration_queries"] == coverage["paper_source_minor_queries"] == 14
    assert len(coverage["C_ambient_template"]) == 64 and len(coverage["U_ambient_template"]) == 16
    for claim in claims["claims"]:
        assert claim["quantifier"] and claim["premises"] and claim["conclusion_type"] and claim["dependencies"]
        assert claim["coordinates"]["omitted_original_edge"] == ["r", "b4"]
        assert claim["review_status"] == "待獨立驗收"
    assert checks["finite_calibration"]["stdout_stderr_byte_equal"]
    assert checks["negative_controls"]["corrupt_certificate_exit"] != 0
    custody = read("custody-after.json")
    assert custody["immutable_input_drift"] == [] and custody["tracked_diff_changed"] is False
    assert custody["protected_original_B_manifest_mismatches"] == []
    return {"status": "passes", "scope": "delivery consistency only; paper pending independent acceptance",
            "schedule_spoke_queries": 28, "literal_rows": 280, "ordered_pin_slots": 4480,
            "source_graph_count": None, "target_source_executed": False}


def manifest():
    delivery = read("delivery.json")
    assert delivery["review_status"] == "待獨立驗收"
    assert delivery["metadata_exclusions"] == [{"path": "delivery.json", "reason": "Manifest self hash excluded."}]
    actual = {str(p.relative_to(HERE)): pin(p) for p in HERE.rglob("*") if p.is_file() and p.name != "delivery.json"}
    declared = {f["path"]: {"bytes": f["bytes"], "sha256": f["sha256"]} for f in delivery["files"]}
    assert actual == declared, "delivery manifest mismatch"
    assert delivery["payload_files"] == len(actual)
    assert delivery["payload_bytes"] == sum(x["bytes"] for x in actual.values())
    assert not any(p.is_symlink() for p in HERE.rglob("*"))
    return {"manifest": "passes", "payload_files": len(actual)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--contents", action="store_true")
    parser.add_argument("--manifest", action="store_true")
    args = parser.parse_args()
    assert args.contents or args.manifest
    output = {}
    if args.contents:
        output.update(contents())
    if args.manifest:
        output.update(manifest())
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
