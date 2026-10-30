#!/usr/bin/env python3
"""Exact cocycles obstructing short cycles of the normalized five-step return.

No source enumeration: histories relax actual Kempe component membership to
independent vertex decisions. A triangulated disk supplies a mod-2 face chain.
The paper proof explains why its boundary cannot have the cocycles below.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "audits/2026-10-29-kempe-realizability/history-cocycles.json"
PAIRS = ((0, 3), (1, 3), (1, 2), (0, 2), (0, 3))
SIGMA = (3, 2, 0, 1)
INVERSE = tuple(SIGMA.index(i) for i in range(4))
BOUNDARY = (
    (0, 0, 0, 0, 0, 3), (1, 1, 1, 2, 2, 2),
    (0, 3, 3, 3, 3, 3), (2, 2, 2, 2, 0, 0),
    (3, 3, 1, 1, 1, 1),
)


def histories(period):
    result = []

    def visit(row, rounds_left, step):
        if step == 5:
            successor = INVERSE[row[-1]]
            if rounds_left == 1:
                if successor == row[0]:
                    result.append(row)
            else:
                visit(row + (successor,), rounds_left - 1, 0)
            return
        a, b = PAIRS[step]
        visit(row + (row[-1],), rounds_left, step + 1)
        if row[-1] in (a, b):
            visit(row + (a + b - row[-1],), rounds_left, step + 1)

    for color in range(4):
        visit((color,), period, 0)
    assert len(result) == len(set(result))
    return sorted(result)


def complex_data(rows, period):
    masks = []
    for h in rows:
        mask = [0] * 4
        for t, c in enumerate(h):
            mask[c] |= 1 << t
        masks.append(mask)
    edges = [(i, j) for i, j in combinations(range(len(rows)), 2)
             if not any(a & b for a, b in zip(masks[i], masks[j]))]
    edge_id = {e: i for i, e in enumerate(edges)}
    adjacent = [set() for _ in rows]
    for i, j in edges:
        adjacent[i].add(j)
        adjacent[j].add(i)
    triangles = [(i, j, k) for i, j in edges
                 for k in sorted(adjacent[i] & adjacent[j]) if j < k]
    lookup = {h: i for i, h in enumerate(rows)}
    boundary = [lookup[h * period] for h in BOUNDARY]
    boundary_edges = [edge_id[tuple(sorted((i, j)))]
                      for i, j in zip(boundary, boundary[1:] + boundary[:1])]
    return edges, edge_id, triangles, boundary, boundary_edges


def cocycle_for_period(period):
    rows = histories(period)
    edges, ids, triangles, boundary, boundary_edges = complex_data(rows, period)
    basis = {}
    for i, j, k in triangles:
        x = (1 << ids[i, j]) ^ (1 << ids[i, k]) ^ (1 << ids[j, k])
        while x:
            pivot = x.bit_length() - 1
            if pivot in basis:
                x ^= basis[pivot]
            else:
                basis[pivot] = x
                break
    boundary_chain = sum(1 << e for e in boundary_edges)
    reduced = boundary_chain
    for pivot in sorted(basis, reverse=True):
        if reduced >> pivot & 1:
            reduced ^= basis[pivot]
    assert reduced, "Boundary bounds a triangle chain: no obstruction here"
    free_edge = reduced.bit_length() - 1
    assert free_edge not in basis
    # Define a dual functional on free edges and extend through the triangular
    # echelon basis. Each row has its pivot strictly above all its other bits.
    marked = 0
    for edge in range(len(edges)):
        value = (basis[edge] & marked).bit_count() % 2 if edge in basis else int(edge == free_edge)
        if value:
            marked |= 1 << edge
    assert (boundary_chain & marked).bit_count() % 2 == 1
    for i, j, k in triangles:
        assert sum((marked >> ids[a, b]) & 1 for a, b in ((i, j), (i, k), (j, k))) % 2 == 0
    return dict(period=period, histories=rows, edges=edges,
                triangle_count=len(triangles), triangle_rank=len(basis),
                boundary_vertices=boundary, boundary_edges=boundary_edges,
                cocycle_marked_edges=[e for e in range(len(edges)) if marked >> e & 1],
                boundary_cocycle_sum=1)


def verify(item):
    """Verify dual certificates directly, without trusting elimination/rank."""
    period = item["period"]
    rows = histories(period)
    edges, ids, triangles, boundary, boundary_edges = complex_data(rows, period)
    assert [list(h) for h in rows] == item["histories"]
    assert [list(e) for e in edges] == item["edges"]
    assert boundary == item["boundary_vertices"]
    assert boundary_edges == item["boundary_edges"]
    assert len(triangles) == item["triangle_count"]
    marked = set(item["cocycle_marked_edges"])
    assert len(marked) == len(item["cocycle_marked_edges"])
    assert marked <= set(range(len(edges)))
    for i, j, k in triangles:
        assert sum(ids[e] in marked for e in ((i, j), (i, k), (j, k))) % 2 == 0
    assert sum(e in marked for e in boundary_edges) % 2 == item["boundary_cocycle_sum"] == 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        certificate = json.loads(OUT.read_text())
        assert certificate["schema"] == "c5-five-return-history-cocycles-v1"
        assert certificate["script_sha256"] == sha256(Path(__file__).read_bytes()).hexdigest()
        assert [row["period"] for row in certificate["certificates"]] == [1, 2, 3]
        for item in certificate["certificates"]:
            verify(item)
        # Ensure a corrupted dual certificate cannot silently pass.
        damaged = json.loads(json.dumps(certificate["certificates"][1]))
        damaged["cocycle_marked_edges"] = []
        try:
            verify(damaged)
        except AssertionError:
            pass
        else:
            raise AssertionError("Corrupt zero cocycle was accepted")
    else:
        certificate = dict(
            schema="c5-five-return-history-cocycles-v1",
            script_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
            evidence="Finite exact F2 cocycles. Disk-to-face-chain implication is paper proof; no Lean or 4CT.",
            sigma=SIGMA, pairs=PAIRS, boundary_histories=BOUNDARY,
            named_obstructions="THIN-932(m): all five fixed literal fibres have m elements, all three-colour fibres empty; m=1,2,3 excluded for triangulated disk sources.",
            open="No exclusion of support 932 with larger fibres, no upper bound on H periods, no universal Kempe escape theorem.",
            certificates=[cocycle_for_period(k) for k in (1, 2, 3)])
        OUT.parent.mkdir(parents=True, exist_ok=True)
        with OUT.open("x") as target:
            json.dump(certificate, target, ensure_ascii=False, indent=2)
            target.write("\n")
    print(json.dumps(dict(check="OK", periods=[dict(
        k=x["period"], histories=len(x["histories"]), edges=len(x["edges"]),
        triangles=x["triangle_count"], boundary_cocycle_sum=x["boundary_cocycle_sum"])
        for x in certificate["certificates"]]), sort_keys=True))


if __name__ == "__main__":
    main()
