"""Controlled full-relation semijoins, not whole-graph speed benchmarks."""
from dataclasses import dataclass
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import sys

SOURCE = Path(__file__).resolve().parent / "none/source/scripts"
sys.path.insert(0, str(SOURCE))
from four_color_intersections import SharedInterfaceIndex, intersect_on_shared


@dataclass(eq=False)
class Factor:
    scope: tuple
    rows: frozenset
    revision: int = 0


def run(lost_count, mode):
    left = Factor((0, 1, 2), frozenset(product(range(4), repeat=3)))
    right = Factor((0, 1, 3, 4, 5, 6, 7, 8), frozenset(product(range(4), repeat=8)))
    index = SharedInterfaceIndex(1_000_000, monotone_updates=True, support_loss=mode == "support")
    index.sync([left, right])
    checks = 0
    def tick():
        nonlocal checks
        checks += 1
    answer = index.intersect(left, right, charge=tick)
    assert answer["left_rows"] == left.rows and answer["right_rows"] == right.rows
    index.mark_seen(left, right, len(answer["common_rows"]),
                    common_rows=answer["common_rows"], common_scope=answer["scope"])
    setup_checks, checks = checks, 0
    forbidden = set(sorted(product(range(4), repeat=2))[:lost_count])
    left.rows = frozenset(r for r in left.rows if r[:2] not in forbidden)
    left.revision += 1
    answer = index.intersect(left, right, charge=tick)
    expected = intersect_on_shared(left.scope, left.rows, right.scope, right.rows)
    assert answer == expected
    canonical = {k: sorted(v) if k != "scope" else v for k, v in answer.items()}
    return dict(setup_checks=setup_checks, update_checks=checks,
                left_rows=len(answer["left_rows"]), right_rows=len(answer["right_rows"]),
                complete_result_sha256=hashlib.sha256(json.dumps(canonical, sort_keys=True).encode()).hexdigest())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    cases = {}
    for lost_count in (1, 15):
        results = {mode: run(lost_count, mode) for mode in ("delta", "support")}
        assert results["delta"]["complete_result_sha256"] == results["support"]["complete_result_sha256"]
        cases[str(lost_count)] = results
    report = dict(interface_supports=16, right_rows_before=65536, private_rows_per_support=4096,
                  cases_by_lost_support_count=cases,
                  interpretation="Exact pair control; setup and update charges separated; no whole-solver speed claim.",
                  source_sha256=hashlib.sha256((SOURCE/"four_color_intersections.py").read_bytes()).hexdigest())
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(cases, indent=2))


if __name__ == "__main__":
    main()
