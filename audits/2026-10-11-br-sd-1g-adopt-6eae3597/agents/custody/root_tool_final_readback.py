#!/usr/bin/env python3
"""Read-only root tool delta and actual precheck receipt consistency check."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parents[1]

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    source = (AUDIT / "verify.py").read_text()
    lines = source.splitlines(keepends=True)
    start = next(i for i, line in enumerate(lines) if "root receipt digest drift" in line)
    end = next(i for i in range(start, len(lines)) if lines[i].startswith("    decision ="))
    previous = "".join(lines[:start] + lines[end:]).encode()
    assert sha(previous) == "4e2de6c8e27874175241d869f9f6246b8a114c12bb009c9f5a4ce8ba64d98b9d", "delta differs from previously accepted code"
    checks = json.loads((AUDIT / "CHECKS.json").read_text())
    result = {}
    for label, expected_actual, expected_declared in (("audit-precheck-v1", 1, 0), ("audit-precheck-v2", 0, 0)):
        path = AUDIT / "logs" / (label + ".json")
        row = json.loads(path.read_text())
        assert row["exit_code"] == expected_actual and row["expected_exit_code"] == expected_declared
        for field in ("stdout", "stderr"):
            assert sha((AUDIT / row[field + "_path"]).read_bytes()) == row[field + "_sha256"]
        grouped = checks["retained_failed_commands"] if label.endswith("v1") else checks["commands"]
        enriched = next(x for x in grouped if x["receipt_path"] == "logs/" + label + ".json")
        assert enriched["receipt_sha256"] == sha(path.read_bytes())
        assert all(enriched[key] == value for key, value in row.items())
        result[label] = {"actual_exit": row["exit_code"], "expected_exit": row["expected_exit_code"],
                         "receipt_sha256": sha(path.read_bytes()), "outputs_digest_matched": True,
                         "group": "retained_failed_commands" if label.endswith("v1") else "commands"}
    assert not any(x["receipt_path"] == "logs/audit-precheck-v1.json" for x in checks["commands"])
    assert checks["all_recorded_expectations_met"] is True
    print(json.dumps({"status": "tool delta and superseding precheck evidence matched",
                      "verify_sha256": sha(source.encode()), "prior_verify_reconstructed_sha256": sha(previous),
                      "record_check_sha256": sha((AUDIT / "record_check.py").read_bytes()),
                      "aggregate_checks_sha256": sha((AUDIT / "aggregate_checks.py").read_bytes()),
                      "prechecks": result}, sort_keys=True))

if __name__ == "__main__":
    main()
