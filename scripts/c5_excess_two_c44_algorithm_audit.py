#!/usr/bin/env python3
"""Reproducible independent Cartesian controls for the C44 algorithms.

This audit imports the optimized routines solely as the objects under test.
The reference enumerates literal four-colour tuples directly, tests every
actual edge, and uses neither the optimized recursion nor its MRV search.
Sixty seeded framed graphs cover k=1..6, including disconnected and low-degree
graphs outside the source catalogue, so the controls exercise the elementary
algorithm claims without presupposing disk, T4, or Sigma-criticality.

For a rejecting parent, every one-edge-deletion witness is compared with the
complete Cartesian set of assignments having exactly one monochromatic edge.
For an accepting parent the optimized search may stop early, so only its
decision and any returned witnesses are checked.  All ten boundary rows on
each graph also compare the original and peeled graph by independent direct
Cartesian extension decisions.  Finally a separately implemented dart walk
audits the saved named core's induced disk rotation.

Generate once: python3 scripts/c5_excess_two_c44_algorithm_audit.py
Exact replay: python3 scripts/c5_excess_two_c44_algorithm_audit.py --check
"""

from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import random
import time

from c5_excess_two_c44 import FRAME, one_pass, peel
from c5_kempe_screen import REPS


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/c5_excess_two_c44/algorithm_audit.json"
COUNTEREXAMPLE = ROOT / "artifacts/c5_excess_two_c44/counterexample_C44-AD3-row0-44.json"
SEED = 44044


def _encode(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False,
                       separators=(",", ":")) + "\n").encode()


def _assignments(edges, row):
    private = sorted({v for edge in edges for v in edge if v >= 5})
    for colours in product(range(4), repeat=len(private)):
        yield dict(enumerate(REPS[row])) | dict(zip(private, colours))


def _cartesian_decisions(edges, row):
    accepts = False
    deletions = set()
    for assignment in _assignments(edges, row):
        bad = [edge for edge in edges
               if assignment[edge[0]] == assignment[edge[1]]]
        if not bad:
            accepts = True
        elif len(bad) == 1:
            deletions.add(bad[0])
    return accepts, deletions


def _cartesian_accepts(edges, row):
    return any(all(assignment[a] != assignment[b] for a, b in edges)
               for assignment in _assignments(edges, row))


def _embedding(rotation, edges):
    """Validate exact darts and walk an independently coded face permutation."""
    darts = {(v, u) for v, neighbours in rotation.items() for u in neighbours}
    assert all(len(neighbours) == len(set(neighbours))
               for neighbours in rotation.values())
    assert darts == {dart for a, b in edges for dart in ((a, b), (b, a))}
    unseen = set(darts)
    faces = []
    while unseen:
        start = min(unseen)
        current = start
        face = []
        while True:
            assert current in unseen
            face.append(current)
            unseen.remove(current)
            a, b = current
            around = rotation[b]
            current = b, around[(around.index(a) + 1) % len(around)]
            if current == start:
                break
        faces.append(face)
    euler = len(rotation) - len(edges) + len(faces)
    assert euler == 2
    return {"vertices": len(rotation), "edges": len(edges),
            "faces": len(faces), "darts": len(darts), "euler": euler,
            "face_boundaries": [[a for a, _ in face] for face in faces]}


def audit():
    rng = random.Random(SEED)
    controls = []
    rejecting = 0
    for k in range(1, 7):
        possible = [(a, b) for b in range(5, 5 + k) for a in range(b)]
        for sample in range(10):
            density = (sample + 1) / 11
            edges = tuple(sorted(FRAME | {edge for edge in possible
                                          if rng.random() < density}))
            row = rng.randrange(len(REPS))
            vertices, accepting, witnesses = one_pass(edges, row)
            expected_accepts, expected_deletions = _cartesian_decisions(edges, row)
            assert (accepting is not None) == expected_accepts
            if not expected_accepts:
                rejecting += 1
                assert set(witnesses) == expected_deletions
            if accepting is not None:
                assignment = dict(zip(vertices, accepting))
                assert tuple(assignment[i] for i in range(5)) == REPS[row]
                assert all(assignment[a] != assignment[b] for a, b in edges)
            for deleted, colouring in witnesses.items():
                assignment = dict(zip(vertices, colouring))
                assert tuple(assignment[i] for i in range(5)) == REPS[row]
                assert all(assignment[a] != assignment[b]
                           for a, b in edges if (a, b) != deleted)
                assert assignment[deleted[0]] == assignment[deleted[1]]
            peeled = peel(edges)
            original_rows = [_cartesian_accepts(edges, q) for q in range(len(REPS))]
            peeled_rows = [_cartesian_accepts(peeled, q) for q in range(len(REPS))]
            assert original_rows == peeled_rows
            controls.append({"k": k, "sample": sample, "edges": edges,
                             "row_index": row, "accepts": expected_accepts,
                             "complete_deletion_comparison": not expected_accepts,
                             "one_pass_witness_edges": sorted(witnesses),
                             "cartesian_one_bad_edge_set": sorted(expected_deletions),
                             "peeled_edges": peeled,
                             "original_cartesian_row_acceptance": original_rows,
                             "peeled_cartesian_row_acceptance": peeled_rows})

    counterexample = json.loads(COUNTEREXAMPLE.read_bytes())
    core = counterexample["core"]
    edges = {tuple(edge) for edge in core["edges"]}
    rotation = {int(v): neighbours
                for v, neighbours in counterexample["core_augmented_rotation"].items()}
    apex = counterexample["source_graph"]["k"] + 5
    augmented = _embedding(rotation, edges | {(v, apex) for v in range(5)})
    disk_rotation = {v: [w for w in neighbours if w != apex]
                     for v, neighbours in rotation.items() if v != apex}
    disk = _embedding(disk_rotation, edges)
    outer_faces = [face for face in disk["face_boundaries"]
                   if len(face) == 5 and set(face) == set(range(5))]
    assert len(outer_faces) == 1
    qi = counterexample["rejection_row"]["row_index"]
    assert not _cartesian_accepts(tuple(sorted(edges)), qi)
    for witness in counterexample["edge_deletion_witnesses"]:
        deleted = tuple(witness["edge"])
        assignment = dict(zip(witness["vertices"], witness["colouring"]))
        assert tuple(assignment[v] for v in range(5)) == REPS[qi]
        assert all(assignment[a] != assignment[b]
                   for a, b in edges if (a, b) != deleted)
    source_files = ("scripts/c5_excess_two_c44.py",
                    "scripts/c5_excess_two_c44_algorithm_audit.py",
                    "scripts/c5_kempe_screen.py")
    payload = {"name": counterexample["name"], "source_code": counterexample["source_graph"]["code"],
               "row_index": qi, "core_edges": core["edges"],
               "core_augmented_rotation": counterexample["core_augmented_rotation"]}
    return {"schema": "c44-algorithm-audit-v1", "seed": SEED,
            "method": "independent direct Cartesian literal four-colour tuples and dart walks",
            "random_graph_controls": len(controls),
            "rejecting_one_pass_exact_deletion_controls": rejecting,
            "peel_row_equivalence_controls": len(controls) * len(REPS),
            "source_sha256": {path: sha256((ROOT / path).read_bytes()).hexdigest()
                              for path in source_files},
            "controls": controls,
            "named_counterexample": {"path": str(COUNTEREXAMPLE.relative_to(ROOT)),
                                     "payload_sha256": sha256(_encode(payload)).hexdigest(),
                                     "name": counterexample["name"],
                                     "augmented_embedding": augmented,
                                     "disk_embedding": disk,
                                     "ordered_frame_face": outer_faces[0],
                                     "cartesian_rejection": True,
                                     "deletion_witnesses_checked": len(counterexample["edge_deletion_witnesses"])},
            "all_checks_passed": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    started = time.monotonic()
    data = _encode(audit())
    if args.check:
        assert OUT.read_bytes() == data, f"byte mismatch: {OUT}"
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        with OUT.open("xb") as stream:
            stream.write(data)
    print(f"ALGORITHM AUDIT PASS: 60 graphs, 600 Cartesian peel rows; "
          f"seconds={time.monotonic() - started:.3f}")


if __name__ == "__main__":
    main()
