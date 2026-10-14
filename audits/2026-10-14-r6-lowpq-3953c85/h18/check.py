#!/usr/bin/env python3
"""Small exact incidence audit; no graph generation or source realizability."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CERT = HERE / "certificate.json"
AUTHORITIES = [
    "audits/2026-10-13-c5-no4ct-collar-6cafdfb/REPORT.md",
    "audits/2026-10-14-c4-mask13-joint6-fdd3e22/SOURCE_GEOMETRY.md",
    "audits/2026-10-14-c4-return-branches-a11d4bb/pq/PROOF.md",
    "audits/2026-10-14-c4-return-branches-a11d4bb/r_high/PROOF.md",
    "audits/2026-10-14-lowpq-source-676b102/classification/SOURCE_TABLE.md",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evaluate() -> dict:
    rows = {"nonnegative_edges": [], "connected": [], "cycle_rank_at_least_two": []}
    for k in range(28):
        for h in range(3, 28):
            excess = k - h - 6
            if excess < 3:
                continue
            for collar_excess in range(2, excess + 1):
                private_excess = excess - collar_excess
                private_vertices = k - (h + 5)
                assert private_vertices == excess + 1
                # Count actual C-P edges by each collar vertex's lost contacts.
                cross_edges = 5 + 2 * h + collar_excess
                # Count independently at all original private degrees.
                private_degree_sum = 5 * private_vertices + private_excess
                difference = private_degree_sum - cross_edges
                if difference < 0 or difference % 2:
                    continue
                private_edges = difference // 2
                rho = private_edges - private_vertices + 1
                assert h == 3 * excess - collar_excess - private_edges
                assert 2 * k == 3 * h + 12 + collar_excess + rho
                row = [k, h, excess, collar_excess, private_excess,
                       private_vertices, private_edges, rho,
                       cross_edges, private_degree_sum]
                rows["nonnegative_edges"].append(row)
                if rho >= 0:
                    rows["connected"].append(row)
                if rho >= 2:
                    rows["cycle_rank_at_least_two"].append(row)
                    assert h <= 12
                    assert 2 * k >= 3 * h + 16

    maxima = {key: max(row[1] for row in value) for key, value in rows.items()}
    assert maxima == {"nonnegative_edges": 15, "connected": 13,
                      "cycle_rank_at_least_two": 12}

    extreme = []
    for kind, collar_excess, private_excess in [("LH_or_HL", 3, 0), ("LL", 2, 1)]:
        k, h = 27, 18
        n = k - h - 5
        cross = 5 + 2 * h + collar_excess
        degree_sum = 5 * n + private_excess
        forced_edges = (degree_sum - cross) // 2
        assert forced_edges < 0
        extreme.append({"type": kind, "k": k, "h": h, "private_vertices": n,
                        "collar_excess": collar_excess, "private_excess": private_excess,
                        "C_to_P_edges": cross, "private_degree_sum": degree_sum,
                        "forced_private_edges": forced_edges})

    return {
        "schema": 1,
        "base": "3953c85e334b96533e44652df065640f5463715a",
        "scope": "necessary original-degree arithmetic only; no source realization",
        "authorities": {path: digest(ROOT / path) for path in AUTHORITIES},
        "checker_sha256": digest(Path(__file__)),
        "proof_sha256": digest(HERE / "PROOF.md"),
        "row_fields": ["k", "h", "E", "E_C", "E_P", "n_P", "e_P", "rho", "A", "sum_d_P"],
        "bounded_domain": {"k": [0, 27], "h": [3, 27], "E_min": 3, "E_C_min": 2},
        "relaxation_max_h": maxima,
        "h18_contradictions": extreme,
        "rows": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--write", action="store_true")
    action.add_argument("--check", action="store_true")
    parser.add_argument("--certificate", type=Path, default=CERT)
    args = parser.parse_args()
    expected = evaluate()
    if args.write:
        with args.certificate.open("x", encoding="utf-8") as handle:
            json.dump(expected, handle, indent=2, sort_keys=True)
            handle.write("\n")
    else:
        actual = json.loads(args.certificate.read_text(encoding="utf-8"))
        if actual != expected:
            raise SystemExit("FAIL: certificate differs from exact replay or input hashes")
    print("PASS: h18 impossible; bounded max h = 12 with rho >= 2")
    print("Necessary arithmetic rows:", {key: len(value) for key, value in expected["rows"].items()})


if __name__ == "__main__":
    main()
