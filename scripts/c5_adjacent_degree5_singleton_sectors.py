#!/usr/bin/env python3
"""Replay the connected-complement sector reduction for a shared singleton.

The disk crosscut argument is a paper proof. This checks named boundary arcs,
same-support recolorings, and signature constraints, not graph realizability.
"""
import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

import c5_adjacent_degree5_interfaces as base

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/c5_adjacent_degree5_singleton_sectors/observations.json"
CONTROL = ROOT / "artifacts/c5_degree5_interfaces/observations.json"
Q = base.Q
TARGETS = ((0, 1, 0, 2, 1), (0, 1, 2, 1, 2))
REPS = base.CANONICAL
ROW_INDEX = {row: REPS.index(base.normalized(row)) for row in base.ROWS}
T4_MASK = sum(1 << i for i, row in enumerate(REPS) if len(set(row)) == 4)
Q_INDEX = REPS.index(Q)


def recolor(row, vertex):
    missing, = set(base.U) - set(row)
    changed = row[:vertex] + (missing,) + row[vertex + 1:]
    assert changed in base.ROWS and len(set(changed)) == 4
    return changed


def signature_masks(arc):
    """Independent exhaustive constraint check on all ten-orbit signatures."""
    fibers = defaultdict(set)
    for row in base.ROWS:
        fibers[tuple(row[i] for i in arc)].add(ROW_INDEX[row])
    return [mask for mask in range(1 << len(REPS))
            if not mask & (1 << Q_INDEX) and mask & T4_MASK == T4_MASK
            and all(len({(mask >> i) & 1 for i in fiber}) == 1
                    for fiber in fibers.values())]


def sector_audit():
    records = []
    for i, j in combinations(range(5), 2):
        arcs = (tuple(range(i, j + 1)), tuple(range(j, 5)) + tuple(range(i + 1)))
        for arc in arcs:
            outside = sorted(set(range(5)) - set(arc))
            record = dict(x_boundary=[i, j], occupied_arc=arc, untouched=outside)
            if Q[i] == Q[j]:
                # At q the original degree-four x has at least three list colors.
                # Every root pair extends x, so no x-edge can be critical.
                xlist = set(base.U) - {Q[i], Q[j]}
                assert all(xlist - {a, b} for a, b in base.PAIRS)
                record.update(result="q_repeated_at_x", q_x_list=sorted(xlist))
            else:
                witnesses = []
                for v in outside:
                    if Q.count(Q[v]) == 1:
                        continue
                    changed = recolor(Q, v)
                    assert all(changed[k] == Q[k] for k in arc)
                    witnesses.append(dict(vertex=v, T4_row=changed))
                masks = signature_masks(arc)
                record["compatible_signature_masks"] = masks
                if witnesses:
                    assert not masks
                    record.update(result="q_conflicts_with_T4", witnesses=witnesses)
                elif outside:
                    assert outside == [4]
                    assert masks == [1023 ^ (1 << Q_INDEX)]
                    target_witnesses = []
                    for row in TARGETS:
                        changed = recolor(row, 4)
                        assert all(changed[k] == row[k] for k in arc)
                        target_witnesses.append(dict(row=row, vertex=4, T4_row=changed))
                    record.update(result="only_q_missing", target_witnesses=target_witnesses)
                else:
                    assert len(masks) == 16 and len(arc) == 5
                    record["result"] = "adjacent_long_arc_open"
            records.append(record)
    counts = dict(sorted(Counter(r["result"] for r in records).items()))
    assert counts == {"adjacent_long_arc_open": 5, "only_q_missing": 1,
                      "q_conflicts_with_T4": 10, "q_repeated_at_x": 4}
    designated = []
    for pair, row in zip(((1, 4), (2, 4)), TARGETS):
        assert row[pair[0]] == row[pair[1]]
        assert {pair} == {p for p in combinations(range(5), 2)
                          if Q[p[0]] != Q[p[1]] and row[p[0]] == row[p[1]]}
        indices = [i for i, r in enumerate(records) if r["x_boundary"] == list(pair)]
        assert len(indices) == 2
        assert all(records[i]["result"] == "q_conflicts_with_T4" for i in indices)
        designated.append(dict(x_boundary=pair, target=row, excluded_sector_records=indices))
    return records, counts, designated


def components(vertices, edges):
    remaining = set(vertices)
    result = []
    while remaining:
        seen = {min(remaining)}
        while True:
            reached = seen | {v for u, v in edges if u in seen and v in remaining} | {
                u for u, v in edges if v in seen and u in remaining}
            if reached == seen:
                break
            seen = reached
        remaining -= seen
        result.append(sorted(seen))
    return result


def check_rotation(edges, rotation):
    """Verify an existing sphere rotation, without a planarity search."""
    vertices = tuple(range(len(rotation)))
    for v in vertices:
        assert len(rotation[v]) == len(set(rotation[v]))
        assert set(rotation[v]) == {b if a == v else a for a, b in edges if v in (a, b)}
    assert len(components(vertices, edges)) == 1
    pending = {(u, v) for a, b in edges for u, v in ((a, b), (b, a))}
    faces = []
    while pending:
        start = min(pending)
        dart = start
        face = []
        while True:
            assert dart in pending
            pending.remove(dart)
            u, v = dart
            face.append(u)
            neighbors = rotation[v]
            dart = (v, neighbors[(neighbors.index(u) - 1) % len(neighbors)])
            if dart == start:
                break
        faces.append(face)
    assert len(vertices) - len(edges) + len(faces) == 2
    return faces


def disconnected_control():
    """A saved disk q-core shows why H-x connected is essential to this lemma.

    Its separator x has degree five, so it is outside the current root class.
    """
    data = json.loads(CONTROL.read_text())
    source, = [w for w in data["witnesses"] if w["source_index"] == 8]
    edges = frozenset(base.edge(*e) for e in source["edges"])
    vertices = tuple(sorted({v for e in edges for v in e}))
    x = source["z"]
    spokes = sorted(v for v in range(5) if base.edge(x, v) in edges)
    assert spokes == [1, 4]
    pieces = components(set(vertices) - set(range(5)) - {x}, edges)
    assert pieces == [[6], [7, 8, 9]]
    supports = [sorted({b for v in piece for b in range(5) if base.edge(v, b) in edges})
                for piece in pieces]
    assert supports == [[0, 1, 4], [1, 2, 3]]
    assert all(any(base.edge(v, b) in edges for v in vertices[5:]) for b in range(5))
    assert not any(set().union(*map(set, supports)) <= set(arc)
                   for arc in ((1, 2, 3, 4), (4, 0, 1)))
    apex = len(vertices)
    apex_edges = edges | {base.edge(apex, b) for b in range(5)}
    faces = check_rotation(apex_edges, source["apex_rotation"])
    for a, b in base.CYCLE:
        assert any(len(face) == 3 and set(face) == {apex, a, b} for face in faces)
    transcript, t4_witnesses = [], []
    for row in base.ROWS:
        coloring = base.first_coloring(vertices, edges, dict(enumerate(row)))
        accepted = coloring is not None
        assert accepted == (base.normalized(row) != Q)
        transcript.append([row, accepted])
        if len(set(row)) == 4:
            t4_witnesses.append(dict(row=row, coloring=[coloring[v] for v in vertices]))
    deletion_witnesses = []
    for e in sorted(edges - base.CYCLE):
        coloring = base.first_coloring(vertices, edges - {e}, dict(enumerate(Q)))
        assert coloring is not None and coloring[e[0]] == coloring[e[1]]
        deletion_witnesses.append(dict(edge=e, coloring=[coloring[v] for v in vertices]))
    return dict(scope="countercontrol to dropping H-x connected; x degree five, outside current class",
                source_index=8, vertices=vertices, edges=sorted(edges), x=x,
                x_degree=sum(x in e for e in edges), x_boundary=spokes,
                components=pieces, boundary_supports=supports,
                apex_rotation=source["apex_rotation"], apex_faces=faces,
                T4_witnesses=t4_witnesses, q_deletion_witnesses=deletion_witnesses,
                all_rows_sha256=sha256(json.dumps(transcript).encode()).hexdigest())


def build():
    records, counts, designated = sector_audit()
    control = disconnected_control()
    inputs = ["scripts/c5_adjacent_degree5_interfaces.py",
              "artifacts/c5_degree5_interfaces/observations.json",
              "docs/c5_unattached_boundary.md"]
    return dict(schema=1, source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                inputs_sha256={p: sha256((ROOT / p).read_bytes()).hexdigest() for p in inputs},
                scope="necessary disk sectors with T4; neither arbitrary-planar exclusion nor realizability",
                summary=dict(sectors=len(records), counts=counts, signature_cases=16 * 1024,
                             designated_pairs=len(designated), designated_sectors=4,
                             disconnected_control_rows=len(base.ROWS),
                             disconnected_control_T4=len(control["T4_witnesses"]),
                             disconnected_control_deletions=len(control["q_deletion_witnesses"])),
                sectors=records, designated=designated, disconnected_control=control)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build()
    payload = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if args.check:
        assert OUT.read_bytes() == payload.encode(), "certificate differs"
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(result["summary"], sort_keys=True))


if __name__ == "__main__":
    main()
