#!/usr/bin/env python3
"""Read-only custody and independent fixed-graph replay for the 5/5/5 repair."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent


def run(script, *args):
    result = subprocess.run([sys.executable, "-B", str(HERE / script), *map(str, args)],
                            check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, default=HERE / "INPUTS.json")
    parser.add_argument("--certificate", type=Path, default=HERE / "C/certificate.json.gz")
    args = parser.parse_args()
    custody = run("check_inputs.py", "--inputs", args.inputs)
    finite = run("C/check.py", args.certificate)
    keys = ("prior_controls_classified", "selected_controls", "perfect_matchings",
            "anchored_cut_masks", "complete_mark_fibres", "complete_even_mark_fibres",
            "all_primal_pairs", "joint_even_rows")
    totals = {key: finite[key] for key in keys}
    if totals != dict(zip(keys, (7, 1, 56, 4096, 8, 8, 78, 6))):
        raise ValueError("fixed finite domain changed")
    print(json.dumps({**custody, "finite_domain": totals,
                      "paper_result": "conditional 5/5/5 repair by X={h,A,B,tau}; C4 plus C_(|O|+3)",
                      "all_source_coverage": "OPEN", "source_realizability": "not triggered",
                      "new_lean_theorem": False}, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError, subprocess.CalledProcessError) as error:
        raise SystemExit(f"REJECTED: {error}")
