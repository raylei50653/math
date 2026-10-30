#!/usr/bin/env python3
"""Replay a five-transfer obstruction stronger than boundary D/count data.

The arbitrary-source theorem is the paper argument accompanying this finite
six-history certificate. No source search, 4CT, or topology oracle is used.
"""
from __future__ import annotations

import argparse
from collections import deque
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from ck_kempe_obstruction import (
    PAIRS, failure, noncrossing, normalize, obligations, partition_options,
    partitions, patterns,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "audits/2026-10-29-kempe-realizability/transport/return-certificate.json"
STEPS = (((0, 3), 2), ((1, 3), 4), ((1, 2), 1),
         ((0, 2), 3), ((0, 3), 0))
BOUNDARIES = ((0, 1, 0, 2, 3), (0, 1, 3, 2, 3),
              (0, 1, 3, 2, 1), (0, 2, 3, 2, 1),
              (0, 2, 3, 0, 1), (3, 2, 3, 0, 1))
SIGMA = (3, 2, 0, 1)
INVERSE = (2, 3, 1, 0)


def swap(values, pair, vertices):
    result = list(values)
    for v in vertices:
        assert values[v] in pair
        result[v] = sum(pair) - values[v]
    return tuple(result)


def admissible_partitions(boundary, split):
    """Direct labelled enumeration, independent of normalized D options."""
    answer = []
    left, right = PAIRS[split]
    for p in partitions([i for i, c in enumerate(boundary) if c in left]):
        for q in partitions([i for i, c in enumerate(boundary) if c in right]):
            blocks = tuple(sorted(p + q))
            owner = {v: j for j, b in enumerate(blocks) for v in b}
            if not noncrossing(blocks):
                continue
            if any(any(boundary[i] in pair and boundary[(i + 1) % 5] in pair
                       for pair in PAIRS[split])
                   and owner[i] != owner[(i + 1) % 5] for i in range(5)):
                continue
            orbit = []
            for bits in product((0, 1), repeat=len(blocks)):
                changed = boundary
                for selected, block in zip(bits, blocks):
                    if selected:
                        pair = next(p for p in PAIRS[split] if boundary[block[0]] in p)
                        changed = swap(changed, pair, block)
                orbit.append(changed)
            if all(len(set(b)) == 4 for b in orbit):
                answer.append((blocks, tuple(sorted(orbit))))
    return answer


def point_histories():
    rows = []
    for initial in range(4):
        for membership in product((0, 1), repeat=5):
            colors = [initial]
            for bit, (pair, _) in zip(membership, STEPS):
                if bit and colors[-1] not in pair:
                    break
                colors.append(sum(pair) - colors[-1] if bit else colors[-1])
            else:
                if colors[-1] == SIGMA[initial]:
                    rows.append(dict(colors=colors, membership=membership))
    assert len(rows) == 6
    edges = [(i, j) for i, j in combinations(range(len(rows)), 2)
             if all(a != b for a, b in zip(rows[i]["colors"], rows[j]["colors"]))]
    triangle = [(i, j, k) for i, j, k in combinations(range(len(rows)), 3)
                if (i, j) in edges and (i, k) in edges and (j, k) in edges]
    assert not triangle
    boundary_roles = [next(i for i, row in enumerate(rows)
                           if row["colors"] == [b[v] for b in BOUNDARIES])
                      for v in range(5)]
    expected_edges = sorted(tuple(sorted((boundary_roles[v], boundary_roles[(v + 1) % 5])))
                            for v in range(5))
    assert sorted(edges) == expected_edges
    isolated = sorted(set(range(6)) - set(boundary_roles))
    assert len(isolated) == 1
    return dict(histories=rows, compatibility_edges=edges,
                boundary_roles=boundary_roles, isolated=isolated,
                triangle_witnesses=triangle)


def report():
    canonical = patterns(5)
    four_mask = sum(1 << i for i, b in enumerate(canonical) if max(b) == 3)
    assert four_mask == 932 and failure(four_mask, obligations(5)) is None
    d_rows = []
    for i, b in enumerate(canonical):
        if max(b) != 3:
            continue
        for split in range(3):
            choices = [dict(mask=mask, blocks=blocks)
                       for mask, blocks in partition_options(5, i, split)
                       if not mask & ~four_mask]
            assert len(choices) == 1
            direct = admissible_partitions(b, split)
            assert len(direct) == 1
            assert direct[0][0] == choices[0]["blocks"]
            d_rows.append(dict(boundary=b, split=split, choices=choices))
    labelled = tuple(b for b in product(range(4), repeat=5)
                     if len(set(b)) == 4 and all(b[i] != b[(i + 1) % 5] for i in range(5)))
    assert len(labelled) == 120
    states = set(labelled)
    automaton = {}
    for b in labelled:
        moves = []
        for split in range(3):
            options = admissible_partitions(b, split)
            assert len(options) == 1
            blocks, orbit = options[0]
            assert set(orbit) <= states
            for block in blocks:
                pair = next(p for p in PAIRS[split] if b[block[0]] in p)
                target = swap(b, pair, block)
                inverse_options = admissible_partitions(target, split)
                assert len(inverse_options) == 1 and inverse_options[0][0] == blocks
                assert swap(target, pair, block) == b
                moves.append(dict(pair=pair, block=block, target=target))
        automaton[b] = moves
    seen = {labelled[0]}
    queue = deque(seen)
    while queue:
        for m in automaton[queue.popleft()]:
            if m["target"] not in seen:
                seen.add(m["target"])
                queue.append(m["target"])
    assert len(seen) == 120
    loop = []
    for t, (pair, root) in enumerate(STEPS):
        moves = [m for m in automaton[BOUNDARIES[t]] if m["pair"] == pair and root in m["block"]]
        assert len(moves) == 1 and moves[0]["block"] == (root,)
        assert moves[0]["target"] == BOUNDARIES[t + 1]
        assert tuple(INVERSE[c] for c in BOUNDARIES[-1]) == BOUNDARIES[0]
        loop.append(dict(step=t + 1, before=BOUNDARIES[t], **moves[0]))
    # Bare C5 realizes exactly these five singleton swaps and a fixed return.
    # Its full Kempe class also includes three-colour boundary states.
    cycle_edges = tuple((v, (v + 1) % 5) for v in range(5))
    assert all(all(b[u] != b[v] for u, v in cycle_edges) for b in BOUNDARIES)
    for t, (pair, root) in enumerate(STEPS):
        active = {v for v, c in enumerate(BOUNDARIES[t]) if c in pair}
        comp = {root}
        todo = [root]
        for v in todo:
            for u, w in cycle_edges:
                other = w if u == v else u if w == v else None
                if other in active and other not in comp:
                    comp.add(other)
                    todo.append(other)
        assert comp == {root}
    counts = [int(max(b) == 3) for b in canonical]
    hashes = {str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
              for p in (Path(__file__), ROOT / "scripts/ck_kempe_obstruction.py")}
    return dict(
        schema="c5-blocked-five-transfer-return-v1", hashes=hashes,
        trust="Exact finite algebra and boundary D replay. General source implication is a paper proof. No 4CT or source existence oracle; no Lean theorem.",
        sigma=SIGMA, sigma_inverse=INVERSE, boundary_loop=loop,
        fixed_return_history_certificate=point_histories(),
        named_obstruction=dict(name="SINGLE-FIBRE-5", is_graph=False,
            support_mask=four_mask, canonical_counts=counts,
            labelled_states=labelled,
            automaton=[dict(boundary=b, moves=automaton[b]) for b in labelled],
            component_count=1, labelled_state_count=len(seen),
            canonical_D_choices=d_rows,
            excluded_contract="Connected same-source blocked component with a triangle, exactly one extension per fixed four-colour boundary assignment; H is forced to fix its sole 02-fibre state, which the six-history certificate forbids."),
        control=dict(name="bare-C5-fixed-return", edges=cycle_edges,
            boundaries=BOUNDARIES, full_class_blocked=False,
            explanation="The five prescribed swaps are actual singleton-component swaps and return after normalization. This source has no triangle."),
        open="Fixed-point exclusion does not exclude multiplicity >=2, arbitrary return cycles, all D-allowed blocked components, or the user's quantified configuration-family proposition.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = report()
    encoded = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.check:
        assert OUT.read_text() == encoded, "Certificate differs; inspect before regeneration"
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        with OUT.open("x") as target:
            target.write(encoded)
    print(json.dumps(dict(check="OK", named_obstruction="SINGLE-FIBRE-5",
                          D_mask=result["named_obstruction"]["support_mask"],
                          labelled_states=120, point_histories=6,
                          history_triangles=0), sort_keys=True))


if __name__ == "__main__":
    main()
