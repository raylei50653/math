#!/usr/bin/env python3
"""Complete fixed-skeleton fibre calibration, not a whole-source search.

The arbitrary-size skeleton proof is in ../paper/REPORT.md. This independent
finite check keeps every original vertex, attachment and ambient ordered pin,
including empty fibres. Certificates are exclusive-created; --check is read-only.
"""
from __future__ import annotations

import argparse
from collections import Counter
import gzip
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

AUDIT = Path(__file__).resolve().parents[1]
DEFAULT = AUDIT / "controls/observations.json.gz"
QS = {0: (0, 1, 2, 1, 2), 1: (0, 1, 2, 0, 2), 3: (0, 1, 0, 2, 1)}
ROOTS = (5, 6)
SHAPES = (
    ("bridge", 2, ((0, 1),), (0, 1)),
    ("triangle", 3, ((0, 1), (1, 2), (0, 2)), (0, 1)),
    ("triangle_bridge", 4, ((0, 1), (1, 2), (0, 2), (2, 3)), (0, 3)),
    ("two_triangles_shared", 5,
     ((0, 1), (1, 2), (0, 2), (2, 3), (3, 4), (2, 4)), (0, 4)),
    ("two_triangles_bridged", 6,
     ((0, 1), (1, 2), (0, 2), (2, 3), (3, 4), (4, 5), (3, 5)), (0, 5)),
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def encode(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def normalized(colors):
    names = {}
    return tuple(names.setdefault(c, len(names)) for c in colors)


ROWS = sorted({normalized(q) for q in product(range(4), repeat=5)
               if all(q[i] != q[(i + 1) % 5] for i in range(5))})


def authority():
    raw = (AUDIT / "BASE.json").read_bytes()
    base = json.loads(raw)
    require(len(base["inputs"]) == 18, "incomplete frozen input manifest")
    for entry in base["inputs"]:
        data = (AUDIT / "frozen" / entry["path"]).read_bytes()
        require(len(data) == entry["bytes"] and sha256(data).hexdigest() == entry["sha256"],
                "frozen input drift: " + entry["path"])
    return sha256(raw).hexdigest()


def dfs_fibre(vertices, edges, fixed):
    adjacency = {v: set() for v in set(vertices) | set(fixed)}
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    coloring = dict(fixed)
    answer = []

    def visit(index):
        if index == len(vertices):
            answer.append([coloring[v] for v in vertices])
            return
        v = vertices[index]
        forbidden = {coloring[w] for w in adjacency[v] if w in coloring}
        for c in range(4):
            if c not in forbidden:
                coloring[v] = c
                visit(index + 1)
        coloring.pop(v, None)

    visit(0)
    return answer


def minor_witness(edges, arc, vertices, attachments):
    """The bags use original edges; no claim that contraction preserves Sigma."""
    a, b, c = arc
    left, right = ((0, 1, 2), (3, 4, 5))
    if attachments[0] != [a]:
        left, right = right, left
    bags = [[a], *[[vertices[v]] for v in left],
            sorted([b, ROOTS[0], *(vertices[v] for v in right)])]
    require(len({v for bag in bags for v in bag}) == sum(map(len, bags)),
            "minor bags overlap")
    adjacency = {v: set() for v in set().union(*map(set, bags))}
    for x, y in edges:
        if x in adjacency and y in adjacency:
            adjacency[x].add(y)
            adjacency[y].add(x)
    for bag in bags:
        reached, pending = set(), [bag[0]]
        while pending:
            v = pending.pop()
            if v not in reached:
                reached.add(v)
                pending.extend(adjacency[v] & set(bag) - reached)
        require(reached == set(bag), "disconnected original minor bag")
    witnesses = []
    for i, j in combinations(range(5), 2):
        links = sorted([list(e) for e in edges
                        if (e[0] in bags[i] and e[1] in bags[j])
                        or (e[1] in bags[i] and e[0] in bags[j])])
        require(links, "missing original K5 inter-bag edge")
        witnesses.append({"bag_pair": [i, j], "original_edge": links[0]})
    return {"type": "K5", "bags": bags, "ten_original_edges": witnesses}


def calculate():
    base_hash = authority()
    require(len(ROWS) == 10, "unexpected complete frame rows")
    counts = Counter()
    records = []
    for shape, n, internal, contacts in SHAPES:
        vertices = list(range(7, 7 + n))
        proper_internal = [t for t in product(range(4), repeat=n)
                           if all(t[a] != t[b] for a, b in internal)]
        for start in range(5):
            arc = [start, (start + 1) % 5, (start + 2) % 5]
            options = []
            for v in range(n):
                boundary_degree = 4 - sum(v in e for e in internal) - (v in contacts)
                require(boundary_degree in (0, 1, 2), "invalid fixed skeleton degree")
                options.append([[]] if boundary_degree == 0 else [[b] for b in arc]
                               if boundary_degree == 1 else [arc[:2], arc[1:]])
            for attachments in product(*options):
                pairs = [tuple(sorted(bs)) for bs in attachments if len(bs) == 2]
                if len(set(pairs)) != len(pairs):
                    continue
                if {b for bs in attachments for b in bs} != set(arc):
                    continue
                edges = {tuple(sorted((vertices[a], vertices[b]))) for a, b in internal}
                edges.update(tuple(sorted((vertices[v], ROOTS[0]))) for v in contacts)
                edges.update(tuple(sorted((vertices[v], b)))
                             for v, bs in enumerate(attachments) for b in bs)
                require(all(sum(v in edge for edge in edges) == 4 for v in vertices),
                        "original complete degree is not four")
                rows = []
                diff_forbidden = []
                for q in ROWS:
                    owner_cells = []
                    for owner_color in range(4):
                        fixed = {**dict(enumerate(q)), ROOTS[0]: owner_color, ROOTS[1]: 0}
                        lifts = dfs_fibre(vertices, edges, fixed)
                        # Independent whole-tuple filter of internally proper assignments.
                        filtered = [list(t) for t in proper_internal
                                    if all(t[v] != q[b] for v, bs in enumerate(attachments) for b in bs)
                                    and all(t[v] != owner_color for v in contacts)]
                        require(lifts == filtered, "independent complete tuple mismatch")
                        owner_cells.append(lifts)
                        counts["independently_checked_owner_cells"] += 1
                    forbidden = [c for c, lifts in enumerate(owner_cells) if not lifts]
                    diff = len({q[b] for b in arc}) == 3
                    if diff and forbidden:
                        diff_forbidden.append({"beta": list(q), "forbidden_owner_colors": forbidden})
                    # Explicit ambient16 coordinate: the nonowner pin is retained.
                    cells = [{"pins": [x, y], "full_lifts": owner_cells[x]}
                             for x, y in product(range(4), repeat=2)]
                    counts["ambient_ordered_cells"] += 16
                    counts["empty_ambient_cells"] += sum(not c["full_lifts"] for c in cells)
                    counts["ambient_complete_lift_tuples"] += sum(len(c["full_lifts"]) for c in cells)
                    rows.append({"beta": list(q), "support_type": "Diff" if diff else "Eq",
                                 "forbidden_owner_colors": forbidden, "cells": cells})
                if diff_forbidden:
                    require(shape == "two_triangles_bridged", "unexpected Diff rejection skeleton")
                    a, b, c = arc
                    expected = ([a], [a, b], [a], [c], [b, c], [c])
                    reversed_expected = ([c], [b, c], [c], [a], [a, b], [a])
                    require(attachments in (expected, reversed_expected),
                            "Diff-rejecting barbell attachment forcing failed")
                    for row in rows:
                        require(row["forbidden_owner_colors"] == [row["beta"][b]],
                                "barbell middle-color full relation mismatch")
                    full_edges = edges | {tuple(sorted((i, (i + 1) % 5))) for i in range(5)}
                    minor = minor_witness(full_edges, arc, vertices, attachments)
                    counts["nonplanar_barbell_controls"] += 1
                    status = "counterexample"
                else:
                    minor = None
                    status = "triggered and holds"
                    counts["diff_accepting_attachment_controls"] += 1
                counts["attachment_controls"] += 1
                counts["shape_" + shape] += 1
                target_rows = [row for row in rows if tuple(row["beta"]) in QS.values()]
                require(len(target_rows) == 3, "missing named target frame rows")
                if all(row["forbidden_owner_colors"] for row in target_rows):
                    counts["all_three_target_rows_locally_rejected"] += 1
                    require(minor is not None, "uneliminated local all-row control")
                records.append({"id": len(records), "shape": shape,
                                "original_vertices": vertices, "roots": list(ROOTS),
                                "original_ordered_root_contacts": [[vertices[v] for v in contacts], []],
                                "actual_support_arc": arc,
                                "actual_attachments": [[vertices[v], bs] for v, bs in enumerate(attachments)],
                                "original_local_edges": [list(e) for e in sorted(edges)],
                                "rows": rows, "local_diff_control_status": status,
                                "K5_planarity_negative": minor,
                                "full_source_status": "not triggered"})
    require(counts["attachment_controls"] == 1050, "incomplete fixed attachment coverage")
    require(counts["nonplanar_barbell_controls"] == 10, "incomplete barbell negative coverage")
    return {"schema": "n2-two-contact-unary-full-fibres-v1", "base_sha256": base_hash,
            "authority_inputs_checked": 18, "counts": dict(sorted(counts.items())),
            "full_source_status": "not triggered", "source_inputs_verified": 0,
            "scope": "derived fixed original skeletons; no whole-source enumeration; no Lean proof",
            "records": records}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--artifact", type=Path, default=DEFAULT)
    args = parser.parse_args()
    try:
        value = calculate()
        raw = encode(value)
        compressed = gzip.compress(raw, compresslevel=9, mtime=0)
        if args.check:
            require(args.artifact.read_bytes() == compressed, "artifact mismatch")
        else:
            with args.artifact.open("xb") as handle:
                handle.write(compressed)
        print(json.dumps({"status": "PASS", "mode": "check" if args.check else "exclusive-create",
                          "artifact_sha256": sha256(compressed).hexdigest(),
                          "artifact_bytes": len(compressed), "uncompressed_bytes": len(raw),
                          "counts": value["counts"], "full_source_status": "not triggered"}, sort_keys=True))
    except (OSError, ValueError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, sort_keys=True))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
