#!/usr/bin/env python3
"""Reconcile normal/seed17 CSP receipts with independently checked witnesses.

Finite-domain UNSAT decisions must finish.  A capped SAT search is discharged
only by validating its actual full original-graph coloring.  No rejected row
may remain unresolved, and no incomplete query is classified as UNSAT.
"""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import sys

import independent_check as checker


def main():
    sample_path, normal_path, seed17_path, output_path = map(Path, sys.argv[1:])
    raw = sample_path.read_bytes()
    digest = sha256(raw).hexdigest()
    samples = [json.loads(line) for line in raw.splitlines() if line]
    normal, seed17 = [json.loads(p.read_bytes()) for p in (normal_path, seed17_path)]
    source_digest = sha256(Path(checker.__file__).read_bytes()).hexdigest()
    for report in (normal, seed17):
        assert report["samples_sha256"] == digest
        assert report["sample_count"] == len(samples)
        assert report["review_source_sha256"] == source_digest
        assert [r["line"] for r in report["results"]] == list(range(1, len(samples) + 1))
        assert report["selection"] == {"stride": 1, "offset": 0, "limit": None}
        assert report["status_counts"].get("FAILED", 0) == 0
    assert normal["results"] == seed17["results"]
    assert normal["catalogue_sha256"] == seed17["catalogue_sha256"]
    discharged = []
    accepted = rejected = 0
    for line, (s, result) in enumerate(zip(samples, normal["results"]), 1):
        assert result["sigma"] == s["sigma"]
        assert result["status"] in {"VERIFIED", "UNRESOLVED"}
        assert len(result["nodes_by_row"]) == 10
        assert bool(result["unresolved_rows"]) == (result["status"] == "UNRESOLVED")
        for row_index, word in enumerate(checker.PATTERNS):
            if s["sigma"] & (1 << row_index):
                checker.check_witness(s["witnesses"][row_index], s["n"], s["boundary"], word, s["edges"])
                accepted += 1
            else:
                assert word not in result["unresolved_rows"], "UNSAT query remained unresolved"
                assert s["witnesses"][row_index] is None
                rejected += 1
            if word in result["unresolved_rows"]:
                assert s["sigma"] & (1 << row_index)
                discharged.append(dict(line=line, id=s["id"], word=word,
                    authority="independent validation of complete original-graph witness",
                    full_colors=s["witnesses"][row_index]))
        if result["status"] == "VERIFIED":
            assert result["exact_sigma"] == s["sigma"]
    report = dict(schema="c5-independent-completed-source-review-v1",
                  samples_sha256=digest,
                  normal_receipt_sha256=sha256(normal_path.read_bytes()).hexdigest(),
                  seed17_receipt_sha256=sha256(seed17_path.read_bytes()).hexdigest(),
                  independent_checker_sha256=source_digest,
                  completion_checker_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                  normal_seed17_row_results_identical=True,
                  complete_source_sigma_verifications=len(samples),
                  complete_ten_row_CSP_rechecks=normal["status_counts"].get("VERIFIED", 0),
                  independently_validated_SAT_witnesses=accepted,
                  completed_independent_UNSAT_decisions=rejected,
                  unresolved_UNSAT_decisions=0,
                  capped_SAT_queries_discharged_by_full_witness=discharged,
                  catalogue_outside_verified=normal["catalogue_outside_verified"])
    with output_path.open("x") as handle:
        json.dump(report, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps({k: v for k, v in report.items()
                      if k != "capped_SAT_queries_discharged_by_full_witness"}, sort_keys=True))


if __name__ == "__main__":
    main()
