#!/usr/bin/env python3
"""Recreate complete exact-source authority receipts for either experiment.

Production: finished UNSAT backtracking plus direct full SAT witnesses.
Targeted: independently checked disk topology and every full-row witness;
all ten rows are SAT, so no negative decision requires search.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys

import complete_review


HERE = Path(__file__).resolve().parent


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("production", "targeted"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.phase == "production":
        sys.argv = [str(Path(complete_review.__file__)),
                    str(HERE.parent / "production.samples.jsonl"),
                    str(HERE / "production.review.json"),
                    str(HERE / "production.seed17.review.json"), str(args.output)]
        complete_review.main()
        return
    source = HERE.parent / "targeted.samples.jsonl"
    normal_path = HERE / "targeted.full-relation.json"
    seed17_path = HERE / "targeted.seed17.full-relation.json"
    metadata_path = HERE / "targeted.metadata.json"
    normal = json.loads(normal_path.read_bytes())
    seed17 = json.loads(seed17_path.read_bytes())
    metadata = json.loads(metadata_path.read_bytes())
    assert normal == seed17
    assert normal["samples_sha256"] == metadata["samples_sha256"] == digest(source)
    assert normal["checker_sha256"] == digest(HERE / "check_full_relation.py")
    assert normal["topology_and_witness_dependency_sha256"] == digest(HERE / "independent_check.py")
    assert metadata["checker_sha256"] == digest(HERE / "check_targeted_metadata.py")
    assert metadata["metadata_dependency_sha256"] == digest(HERE / "check_metadata.py")
    assert metadata["topology_dependency_sha256"] == digest(HERE / "independent_check.py")
    count = normal["complete_source_sigma_verifications"]
    assert normal["exact_sigma_histogram"] == {"1023": count}
    assert normal["independently_verified_literal_full_witnesses"] == 10 * count
    assert normal["unresolved_decisions"] == 0 and normal["no_rejected_rows_to_refute"]
    assert metadata["sample_count"] == metadata["strict_necessary_geometry_verified"] == count
    assert metadata["ring_seeds_and_vertex_splits_independently_verified"] == count
    diagnostic_paths = [HERE / "targeted.review.json", HERE / "targeted.seed17.review.json"]
    diagnostics = [json.loads(p.read_bytes()) for p in diagnostic_paths]
    assert diagnostics[0]["results"] == diagnostics[1]["results"]
    assert diagnostics[0]["samples_sha256"] == diagnostics[1]["samples_sha256"] == digest(source)
    assert diagnostics[0]["status_counts"].get("FAILED", 0) == 0
    capped = [{"line": r["line"], "rows": r["unresolved_rows"]}
              for r in diagnostics[0]["results"] if r["status"] == "UNRESOLVED"]
    result = dict(schema="c5-independent-targeted-completed-review-v1",
                  complete_source_sigma_verifications=count,
                  independently_validated_SAT_witnesses=10 * count,
                  completed_independent_UNSAT_decisions=0,
                  unresolved_UNSAT_decisions=0,
                  normal_seed17_topology_and_witness_receipts_identical=True,
                  exact_sigma_histogram={"1023": count},
                  strict_necessary_geometry_verified=count,
                  independent_seed_geometry_verifications=count,
                  catalogue_outside_verified=[],
                  samples_sha256=digest(source),
                  direct_normal_receipt_sha256=digest(normal_path),
                  direct_seed17_receipt_sha256=digest(seed17_path),
                  metadata_receipt_sha256=digest(metadata_path),
                  extra_CSP_diagnostic_status_counts=diagnostics[0]["status_counts"],
                  extra_CSP_capped_SAT_rows_already_proved_by_full_witness=capped,
                  extra_CSP_normal_seed17_results_identical=True,
                  extra_CSP_diagnostic_receipt_sha256=[digest(p) for p in diagnostic_paths],
                  completion_checker_sha256=digest(Path(__file__)))
    with args.output.open("x") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps({key: value for key, value in result.items()
                      if key != "extra_CSP_capped_SAT_rows_already_proved_by_full_witness"}, sort_keys=True))


if __name__ == "__main__":
    main()
