#!/usr/bin/env python3
"""Read-only custody, fixed-control, and independent pair replay."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def run(path, *args):
    result = subprocess.run(
        [sys.executable, "-B", str(path), *map(str, args)],
        cwd=REPO, check=True, capture_output=True, text=True,
    )
    return json.loads(result.stdout)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, default=HERE / "INPUTS.json")
    parser.add_argument("--certificate", type=Path,
                        default=HERE / "C/certificate.json.gz")
    args = parser.parse_args()
    custody = run(HERE / "check_inputs.py", "--inputs", args.inputs)
    controls = run(HERE / "C/check.py", args.certificate)
    independent = run(HERE / "A/check.py", "--certificate", args.certificate)
    expected_independent = json.loads((HERE / "A/independent-check.json").read_text())
    if independent != expected_independent:
        raise ValueError("independent fixed-control replay differs")
    prior = run(REPO / "audits/2026-10-20-r6-two-cycle-repair-9c36e3c/check.py")
    if controls["perfect_matchings"] != independent["perfect_matchings"]:
        raise ValueError("complete matching coverage differs")
    totals = {key: controls[key] for key in (
        "controls", "perfect_matchings", "anchored_primal_cut_masks",
        "complete_spoke_mask_fibres", "complete_marked_matching_fibres",
        "safe_adjacent_pair_tests",
    )}
    if totals != {
        "controls": 7, "perfect_matchings": 275,
        "anchored_primal_cut_masks": 16384,
        "complete_spoke_mask_fibres": 224,
        "complete_marked_matching_fibres": 56,
        "safe_adjacent_pair_tests": 9,
    }:
        raise ValueError("fixed finite domain differs")
    if sum(c["candidate_pairs"] for c in independent["controls"][1:]) != 9:
        raise ValueError("literal candidate-pair coverage differs")
    print(json.dumps({
        **custody,
        "fixed_domain": totals,
        "independent_admissible_pairs":
            sum(c["admissible_pairs"] for c in independent["controls"]),
        "independent_even_pair_successes":
            sum(len(c["successful_pairs"]) for c in independent["controls"]),
        "independent_negative_checks": independent["negative_checks"],
        "prior_replay": {
            "frozen_inputs": prior["frozen_inputs"],
            "spoke_masks": prior["spoke_masks"],
            "states_without_internal_odd_cycle":
                prior["states_without_internal_odd_cycle"],
        },
        "source_realizability": "not triggered",
        "paper_status": "conditional two-face repair; universal existence OPEN",
        "new_lean_theorem": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError,
            subprocess.CalledProcessError) as error:
        raise SystemExit(f"REJECTED: {error}")
