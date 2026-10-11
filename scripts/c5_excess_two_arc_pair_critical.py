#!/usr/bin/env python3
"""Fixed-source controls for the E-ARC2 proper-subgraph lemma.

Reads the 179 saved ER critical representatives and their saved C44 cores.
Recomputes complete Sigma for each source, edge deletion, and listed core.
Does not rerun graph search or claim completeness of the saved core search.
Generation is exclusive; --check performs a read-only deterministic replay.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

from c5_excess_two_independent_coloring import find_extension, sigma_mask
from c5_kempe_screen import REPS

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "artifacts/c5_excess_two_arc_pair_critical/observations.json"
FRAME = frozenset(tuple(sorted((i, (i + 1) % 5))) for i in range(5))
SINGLETON = {6: 0, 4: 1, 3: 2, 1: 3, 0: 4}
ROW = {position: REPS[index] for index, position in SINGLETON.items()}


def encode(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + "\n").encode()


def edges_of(value):
    return tuple(sorted(tuple(sorted(e)) for e in value))


def rejected(mask):
    assert mask & 932 == 932
    return sorted(position for index, position in SINGLETON.items()
                  if not (mask >> index & 1))


def excess(edges):
    degrees = Counter(v for e in edges for v in e)
    assert all(d >= 4 for v, d in degrees.items() if v >= 5)
    return sum(d - 4 for v, d in degrees.items() if v >= 5)


def produce():
    inputs = []

    def read(path):
        raw = path.read_bytes()
        inputs.append({"path": str(path.relative_to(ROOT)),
                       "sha256": sha256(raw).hexdigest()})
        return json.loads(raw)

    core_sources = {}
    for path in sorted((ROOT / "artifacts/c5_excess_two_c44/orbits").glob("chunk_*.json")):
        for graph in read(path)["orbits"]:
            if graph["critical"]:
                key = edges_of(graph["canonical_edges"])
                assert key not in core_sources
                core_sources[key] = graph
    assert len(core_sources) == 179

    records, negative, counts = [], [], Counter()
    source_paths = sorted({graph["source"] for graph in core_sources.values()})
    for relative in source_paths:
        path = ROOT / relative
        source_chunk = read(path)
        for ordinal, source in enumerate(source_chunk["q_orbits"], 1):
            if not source["critical"]:
                continue
            edges = edges_of(source["canonical_edges"])
            core_source = core_sources.pop(edges)
            assert core_source["source"] == relative
            assert core_source["source_sha256"] == inputs[-1]["sha256"]
            mask = sigma_mask(edges)
            assert mask == source["sigma_mask"] == core_source["sigma_mask"]
            assert excess(edges) == 2
            q = rejected(mask)
            core_sets, zero_rows, core_records = {}, set(), []
            for row in core_source["rows"]:
                position = row["singleton_position"]
                assert position == SINGLETON[row["row_index"]]
                core_sets[position] = []
                for core in row["cores"]:
                    core_edges = edges_of(core["edges"])
                    assert set(core_edges) <= set(edges)
                    core_mask = sigma_mask(core_edges)
                    assert core_mask == core["sigma_mask"]
                    assert position in rejected(core_mask)
                    epsilon = excess(core_edges)
                    assert epsilon in (0, 1, 2)
                    for removed in set(core_edges) - FRAME:
                        child = tuple(e for e in core_edges if e != removed)
                        assert sigma_mask(child, rep_indices=(row["row_index"],)) >> row["row_index"] & 1
                        counts["listed_core_minimality_deletions_checked"] += 1
                    if epsilon <= 1:
                        assert rejected(core_mask) == [position]
                    if epsilon == 0:
                        zero_rows.add(position)
                    if epsilon == 2:
                        assert core_edges == edges
                    core_sets[position].append(set(core_edges))
                    core_records.append({"q": position, "epsilon": epsilon,
                                         "edges": core_edges, "sigma_mask": core_mask})
                    counts["listed_core_occurrences_recolored"] += 1
            assert sorted(core_sets) == q
            trigger = len(zero_rows) <= 1
            deletions = []
            for saved in source["deletion_sigmas"]:
                edge = tuple(saved["edge"])
                assert edge in edges and edge not in FRAME
                smaller = tuple(e for e in edges if e != edge)
                deletion_mask = sigma_mask(smaller)
                assert deletion_mask == saved["sigma_mask"]
                assert deletion_mask != mask
                assert deletion_mask | mask == deletion_mask
                remaining = rejected(deletion_mask)
                if trigger:
                    assert len(remaining) <= 1
                deletion = {"edge": edge, "sigma_mask": deletion_mask, "Q": remaining}
                deletions.append(deletion)
                if len(remaining) > 1:
                    assert not trigger
                    witnesses = {}
                    for index in range(10):
                        coloring = find_extension(smaller, index)
                        assert (coloring is not None) == bool(deletion_mask >> index & 1)
                        if coloring is not None:
                            assert all(coloring[a] != coloring[b] for a, b in smaller)
                            witnesses[str(index)] = coloring
                    negative.append({"source": str(path.relative_to(ROOT)), "ordinal": ordinal,
                                     "edges": edges, "sigma_mask": mask, "Q": q,
                                     "augmented_rotation": source["augmented_rotation"], "zero_core_rows": sorted(zero_rows),
                                     "cores": core_records, "deletion": deletion,
                                     "deletion_accepted_colorings": witnesses})
                counts["edge_deletions_recolored"] += 1
            assert {tuple(d["edge"]) for d in deletions} == set(edges) - FRAME
            pair_checks = 0
            if trigger:
                for p, r in combinations(q, 2):
                    for first in core_sets[p]:
                        for second in core_sets[r]:
                            assert first | second == set(edges)
                            pair_checks += 1
                for v in sorted({v for edge in edges for v in edge if v >= 5}):
                    support = [b for b in range(5) if (b, v) in edges]
                    for b in support:
                        redundant = [p for p in q if any(c != b and ROW[p][b] == ROW[p][c]
                                                        for c in support)]
                        assert len(redundant) <= 1
            counts["graphs"] += 1
            counts["hypothesis_triggered" if trigger else "hypothesis_not_triggered"] += 1
            if trigger and len(q) >= 2:
                counts["hypothesis_triggered_with_multiple_rejections"] += 1
            counts["core_pair_unions_checked"] += pair_checks
            counts[f"zero_core_rows_{len(zero_rows)}"] += 1
            counts["target_933_941_orbit_triggered"] += int(len(q) + len(q) - sum(a in q and b in q for a, b in FRAME) > 4)
            records.append({"source": str(path.relative_to(ROOT)), "ordinal": ordinal,
                            "edges": edges, "sigma_mask": mask, "Q": q,
                            "zero_core_rows": sorted(zero_rows), "hypothesis_triggered": trigger,
                            "core_pair_unions_checked": pair_checks,
                            "cores": core_records, "deletions": deletions})
    assert not core_sources
    assert counts["graphs"] == 179 and counts["edge_deletions_recolored"] == 4138
    assert len(negative) == 2
    assert counts["target_933_941_orbit_triggered"] == 0

    columns = []
    for mask in (933, 940, 941):
        q = rejected(mask)
        allowed, forbidden = [], []
        for size in range(6):
            for support in combinations(range(5), size):
                failures = [{"endpoint": b,
                             "Q": [p for p in q if any(c != b and ROW[p][b] == ROW[p][c]
                                                       for c in support)]}
                            for b in support]
                failures = [failure for failure in failures if len(failure["Q"]) >= 2]
                (forbidden if failures else allowed).append(
                    {"support": support, "failures": failures})
        columns.append({"sigma_mask": mask, "Q": q, "allowed": allowed, "forbidden": forbidden})

    for name in ("scripts/c5_excess_two_independent_coloring.py", "scripts/c5_kempe_screen.py"):
        inputs.append({"path": name, "sha256": sha256((ROOT / name).read_bytes()).hexdigest()})
    return {"scope": "fixed saved 179 graphs; saved C44 core completeness inherited, not rerun",
            "counts": dict(sorted(counts.items())), "inputs": inputs,
            "records": records, "hypothesis_removed_counterexamples": negative,
            "canonical_target_column_necessities": columns,
            "target_source_status": "not triggered", "E_ARC2": "OPEN"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=DEFAULT)
    args = parser.parse_args()
    result = produce()
    raw = encode(result)
    if args.check:
        assert args.output.read_bytes() == raw, "artifact mismatch"
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("xb") as stream:
            stream.write(raw)
    print(json.dumps({"check": args.check, "sha256": sha256(raw).hexdigest(),
                      "bytes": len(raw), **result["counts"]}, sort_keys=True))


if __name__ == "__main__":
    main()
