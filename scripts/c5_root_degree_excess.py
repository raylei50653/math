#!/usr/bin/env python3
"""Finite controls for the source degree-excess budget and tree list lemma.

The arbitrary-size proofs are in the report. These are list assignments,
not C5 source graphs, planar realizations, or Lean proofs.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/c5_adjacent_degree5_no_mixed/observations.json"
OUT = ROOT / "artifacts/c5_root_degree_excess/observations.json"
# All unlabelled tree shapes, with fixed named vertices in each representative.
TREES = (
    ("point", 1, 4, ()),
    ("edge", 2, 4, ((0, 1),)),
    ("path3", 3, 4, ((0, 1), (1, 2))),
    ("path4", 4, 4, ((0, 1), (1, 2), (2, 3))),
    ("star4", 4, 4, ((0, 1), (0, 2), (0, 3))),
    ("path5", 5, 3, ((0, 1), (1, 2), (2, 3), (3, 4))),
    ("fork5", 5, 3, ((0, 1), (0, 2), (0, 3), (3, 4))),
    ("star5", 5, 3, ((0, 1), (0, 2), (0, 3), (0, 4))),
)


def colors(mask, k):
    return [c for c in range(k) if mask >> c & 1]


def tree_messages(lists, neighbors, k):
    cache = {}

    def message(v, parent):
        key = v, parent
        if key not in cache:
            children = [message(w, v) for w in neighbors[v] if w != parent]
            cache[key] = sum(1 << c for c in colors(lists[v], k)
                             if all(s & ~(1 << c) for s in children))
        return cache[key]

    return message


def direct_oracle(n, k, edges):
    """Bitsets of EVERY literal coloring; independent of tree messages."""
    assignments = tuple(product(range(k), repeat=n))
    allowed = [[sum(1 << i for i, a in enumerate(assignments)
                    if mask >> a[v] & 1) for mask in range(1 << k)] for v in range(n)]
    proper = sum(1 << i for i, a in enumerate(assignments)
                 if all(a[u] != a[v] for u, v in edges))
    deleted = [sum(1 << i for i, a in enumerate(assignments)
                   if all(a[u] != a[v] for j, (u, v) in enumerate(edges) if j != cut))
               for cut in range(len(edges))]
    return assignments, allowed, proper, deleted


def audit_tree(name, n, k, edges):
    neighbors = [[w if v == u else u for u, w in edges if v in (u, w)] for v in range(n)]
    assignments, allowed, proper, deleted = direct_oracle(n, k, edges)
    full = (1 << len(assignments)) - 1
    critical, count = [], 0
    for lists in product(range(1 << k), repeat=n):
        permitted = full
        for v, mask in enumerate(lists):
            permitted &= allowed[v][mask]
        message = tree_messages(lists, neighbors, k)
        colorable = bool(message(0, -1))
        assert colorable == bool(permitted & proper)
        count += 1
        if colorable:
            continue
        half_sets = [(message(u, v), message(v, u)) for u, v in edges]
        minimal = all(a and b for a, b in half_sets)
        assert minimal == all(permitted & d for d in deleted)
        if not minimal:
            continue
        labels = []
        for a, b in half_sets:
            assert a == b and a.bit_count() == 1
            labels.append(colors(a, k)[0])
        for v in range(n):
            incident = [labels[i] for i, e in enumerate(edges) if v in e]
            assert len(incident) == len(set(incident))
            assert colors(lists[v], k) == sorted(incident)
        witnesses = []
        for i, (u, v) in enumerate(edges):
            choices = permitted & deleted[i]
            first = (choices & -choices).bit_length() - 1
            a = assignments[first]
            assert a[u] == a[v] == labels[i]
            witnesses.append(a)
        critical.append(dict(lists=[colors(s, k) for s in lists],
                             edge_colors=labels, deletion_colorings=witnesses))
    # Independently generate all proper edge labels, including the empty tree.
    generated = set()
    for labels in product(range(k), repeat=len(edges)):
        incidence = [[labels[i] for i, e in enumerate(edges) if v in e] for v in range(n)]
        if all(len(cs) == len(set(cs)) for cs in incidence):
            generated.add(tuple(tuple(sorted(cs)) for cs in incidence))
    assert generated == {tuple(map(tuple, c["lists"])) for c in critical}
    return dict(name=name, vertices=n, colors=k, edges=edges,
                assignments=count, critical_count=len(critical), critical=critical)


def budget(side, skeleton_degree=1):
    fs = [set(f) for f in side["forbidden"]]
    covered = set().union(*fs)
    residual = set(side["available"]) - covered
    deficits = [k - len(f) for k, f in zip(side["ports"], fs)]
    overlap = sum(map(len, fs)) - len(covered)
    kappa = skeleton_degree - len(residual)
    complete_degree = skeleton_degree + len(side["root_boundary"]) + sum(side["ports"])
    assert all(d >= 0 for d in deficits) and overlap >= 0 and kappa >= 0
    assert sum(deficits) + overlap + kappa == complete_degree - 4
    return dict(component_deficits=deficits, D=sum(deficits), O=overlap,
                kappa=kappa, complete_degree=complete_degree,
                skeleton_degree=skeleton_degree, residual=sorted(residual))


def build():
    trees = [audit_tree(*tree) for tree in TREES]
    inherited = json.loads(SOURCE.read_text())
    sides = [dict(side_id=s["id"], **budget(s)) for s in inherited["side_normal_forms"]]
    retained_ids = {i for ij in inherited["abstract_conditions"]["retained"] for i in ij}
    kinds = Counter((s["D"], s["O"], s["kappa"]) for s in sides if s["side_id"] in retained_ids)
    summary = dict(tree_assignments=sum(t["assignments"] for t in trees),
                   edge_minimal_list_obstructions=sum(t["critical_count"] for t in trees),
                   tree_shapes=len(trees), source_side_budgets=len(sides),
                   retained_budget_counts={str(k): v for k, v in sorted(kinds.items())})
    assert summary["tree_assignments"] == 233744
    assert summary["edge_minimal_list_obstructions"] == 113
    assert kinds == {(1, 0, 0): 94, (0, 1, 0): 24}
    # Without edge minimality, a tree need not have degree-sized lists.
    negative_edges = ((0, 1), (1, 2))
    _, allowed, proper, deleted = direct_oracle(3, 2, negative_edges)
    permitted = allowed[0][1] & allowed[1][1] & allowed[2][1]
    assert not permitted & proper and not any(permitted & d for d in deleted)
    return dict(schema=1, scope="paper lemmas with finite list controls; no source realizability or Lean theorem",
                source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                inputs_sha256={str(SOURCE.relative_to(ROOT)): sha256(SOURCE.read_bytes()).hexdigest()},
                summary=summary, trees=trees, side_budgets=sides,
                negative_control=dict(edges=negative_edges, lists=[[0], [0], [0]],
                                      kappa=[0, 1, 0], edge_minimal=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build()
    payload = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if args.check:
        assert OUT.read_bytes() == payload.encode(), f"certificate differs: {OUT}"
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(result["summary"], sort_keys=True))


if __name__ == "__main__":
    main()
