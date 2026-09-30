#!/usr/bin/env python3
"""Inventory existing C5 classes and replay their two-vertex projections.

No graph search, disk validation, or eight-port successor enumeration is run.
--check is read-only and compares the complete deterministic artifact.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CELL_SOURCE = "artifacts/c5_cells/cells.json"
LIBRARY_SOURCE = "artifacts/boundary_relations/library.json"
OUTPUT = ROOT / "artifacts/c5_two_vertex_overlap/pair_interfaces.json"
STATUSES = ("infeasible", "forced_equal", "forced_different", "free")


def build() -> dict:
    catalogue = json.loads((ROOT / CELL_SOURCE).read_text())
    library = json.loads((ROOT / LIBRARY_SOURCE).read_text())
    patterns = [tuple(p) for p in catalogue["pattern_order"]]
    colour_perms = tuple(permutations(range(4)))
    labelled = [p for p in product(range(4), repeat=5)
                if all(p[i] != p[(i + 1) % 5] for i in range(5))]
    representatives = {
        p: min(tuple(g[c] for c in p) for g in colour_perms) for p in labelled
    }
    assert len(labelled) == 240
    assert patterns == sorted(set(representatives.values()))
    assert len(patterns) == 10
    assert patterns == [tuple(p) for p in library["pattern_order"]]
    index = {p: i for i, p in enumerate(patterns)}
    masks = sorted(map(int, catalogue["cells"]))
    assert len(masks) == catalogue["distinct_sigma"]
    assert len(set(masks)) == len(masks)
    assert all(0 < mask < (1 << len(patterns)) for mask in masks)

    library_ids = [entry["id"] for entry in library["entries"]]
    assert len(set(library_ids)) == len(library_ids) == library["distinct_relations"]
    assert set(library_ids) <= set(masks)
    for entry in library["entries"]:
        assert entry["relation"]["ports"] == [f"b{i}" for i in range(5)]
        encoded = sum(1 << index[tuple(p)] for p in entry["relation"]["patterns"])
        assert encoded == entry["id"]

    totals = {name: Counter() for name in ("all", "adjacent", "diagonal")}
    cells = []
    labelled_pair_checks = 0
    for mask in masks:
        rows = [p for i, p in enumerate(patterns) if mask & (1 << i)]
        accepted = [p for p in labelled if mask & (1 << index[representatives[p]])]
        pairs = []
        for i, j in combinations(range(5), 2):
            equal = [p for p in rows if p[i] == p[j]]
            different = [p for p in rows if p[i] != p[j]]
            status = ("free" if equal and different else "forced_equal" if equal
                      else "forced_different" if different else "infeasible")
            expected = {(a, b) for a, b in product(range(4), repeat=2)
                        if (a == b and equal) or (a != b and different)}
            actual = {(p[i], p[j]) for p in accepted}
            assert actual == expected
            labelled_pair_checks += 1
            equal_mask = sum(1 << index[p] for p in equal)
            different_mask = sum(1 << index[p] for p in different)
            assert equal_mask | different_mask == mask
            assert equal_mask & different_mask == 0
            kind = "adjacent" if j - i in (1, 4) else "diagonal"
            totals["all"][status] += 1
            totals[kind][status] += 1
            pairs.append({
                "pair": [i, j], "kind": kind, "status": status,
                "equal_mask": equal_mask, "different_mask": different_mask,
                "equal_witness": list(equal[0]) if equal else None,
                "different_witness": list(different[0]) if different else None,
            })
        cells.append({"id": mask, "source_cell_key": str(mask),
                      "k_eff": catalogue["cells"][str(mask)]["k_eff"],
                      "pair_interfaces": pairs})

    source_paths = (CELL_SOURCE, LIBRARY_SOURCE,
                    str(Path(__file__).resolve().relative_to(ROOT)))
    return {
        "schema": "c5-two-vertex-pair-interfaces-v1",
        "scope": "Existing catalogue relations only; graph witnesses and disk embeddings are not replayed.",
        "source_sha256": {p: sha256((ROOT / p).read_bytes()).hexdigest() for p in source_paths},
        "pattern_order": patterns,
        "catalogue": {
            "classes": len(masks), "reported_max_k": catalogue["k"],
            "reported_nested_by_k_eff": catalogue["nested_by_k_eff"],
            "reported_d5_orbits": catalogue["d5_orbits"],
            "library_classes": len(library_ids),
            "library_entry_specific_forcing_rules": sum(
                len(entry["extra_forcings"]) for entry in library["entries"]),
        },
        "checks": {"proper_labelled_c5_assignments": len(labelled),
                   "labelled_pair_projection_checks": labelled_pair_checks,
                   "library_patterns_agree_with_catalogue": True},
        "counts": {name: {status: totals[name][status] for status in STATUSES}
                   for name in totals},
        "all_pairs_allow_different": all(
            pair["different_mask"] != 0 for cell in cells for pair in cell["pair_interfaces"]),
        "geometry": "not_rechecked; no pair-gluing geometry certified",
        "successors": "eight-port joins and subsequent five-port projections not enumerated",
        "cells": cells,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="recompute and compare without writing")
    args = parser.parse_args()
    result = build()
    payload = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_bytes() != payload:
            raise SystemExit("FAIL: saved pair interfaces differ or are missing")
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_bytes(payload)
    print(json.dumps({"mode": "check" if args.check else "write", "status": "pass",
                      "classes": result["catalogue"]["classes"],
                      "counts": result["counts"], "bytes": len(payload)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
