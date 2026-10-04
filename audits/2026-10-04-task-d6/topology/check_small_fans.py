#!/usr/bin/env python3
"""Independent finite sanity control for the paper shield lemmas.

The family has C5 boundary, two distinct roots r,s joined by rs, and two
singleton pieces p~r, q~s.  Each singleton has an arbitrary boundary support.
No audited checker is imported.  NetworkX supplies a rotation; this script
independently traverses faces and computes the shield by its defining face.
This finite family is not a proof for arbitrary connected pieces.
"""
import json
from collections import Counter
from pathlib import Path

import networkx as nx


B = tuple(f"b{i}" for i in range(5))
BEDGES = tuple(frozenset((B[i], B[(i + 1) % 5])) for i in range(5))


def faces(rotation):
    darts = {(u, v) for u, vs in rotation.items() for v in vs}
    result, dart_face = [], {}
    while darts:
        first = min(darts)
        dart, walk = first, []
        while True:
            assert dart in darts, (first, dart, walk)
            darts.remove(dart)
            dart_face[dart] = len(result)
            walk.append(dart)
            u, v = dart
            ns = rotation[v]
            dart = (v, ns[(ns.index(u) - 1) % len(ns)])
            if dart == first:
                break
        result.append(walk)
    return result, dart_face


def shield(rotation, outer, piece, root, support):
    if not support:
        return set()
    vertices = set(B) | {piece}
    restricted = {
        v: [n for n in rotation[v] if n in vertices]
        for v in vertices
    }
    _, df = faces(restricted)
    ns = rotation[piece]
    i = ns.index(root)
    j = (i + 1) % len(ns)
    while ns[j] not in support:
        j = (j + 1) % len(ns)
    # The root ray lies in the corner preceding this retained dart, hence
    # in the face containing the dart from that boundary neighbor to piece.
    containing = df[(ns[j], piece)]
    return {
        i for i, edge in enumerate(BEDGES)
        if df[next((v, u) for u, v in outer if frozenset((u, v)) == edge)]
        != containing
    }


def run():
    counts, witnesses = Counter(), {}
    for mp in range(32):
        for mq in range(32):
            supports = [{B[i] for i in range(5) if m >> i & 1}
                        for m in (mp, mq)]
            g = nx.Graph()
            g.add_edges_from((B[i], B[(i + 1) % 5]) for i in range(5))
            g.add_edges_from([("p", "r"), ("r", "s"), ("s", "q")])
            for v, support in zip(("p", "q"), supports):
                g.add_edges_from((v, b) for b in support)
            # Adding a vertex on the empty side of B enforces a disk embedding.
            g.add_edges_from(("outside", b) for b in B)
            planar, embedding = nx.check_planarity(g)
            if not planar:
                counts["nonplanar_augmented"] += 1
                continue
            counts["planar_augmented"] += 1
            if not any(supports):
                counts["both_shields_empty"] += 1
                continue
            rotation = {
                v: [n for n in embedding.neighbors_cw_order(v)
                    if n != "outside"]
                for v in g if v != "outside"
            }
            full_faces, _ = faces(rotation)
            assert len(rotation) - sum(map(len, rotation.values())) // 2 + len(full_faces) == 2
            outer_options = [f for f in full_faces
                             if len(f) == 5 and {u for u, _ in f} == set(B)]
            assert outer_options, (mp, mq, full_faces)
            outer = outer_options[0]
            sp = shield(rotation, outer, "p", "r", supports[0])
            sq = shield(rotation, outer, "q", "s", supports[1])
            assert not sp & sq, (mp, mq, sp, sq)
            counts["cross_root_disjoint_shields_checked"] += 1
            for support, sigma in zip(supports, (sp, sq)):
                if len(support) >= 2:
                    assert all(any(b in BEDGES[i] for i in sigma) for b in support)
                    counts["support_marking_checked"] += 1
                if len(support) >= 3:
                    assert len(sigma) >= 2
                    counts["three_point_length_checked"] += 1
            if len(sp) == len(sq) == 2:
                witnesses.setdefault("two_disjoint_length_two", {
                    "support_p": sorted(supports[0]),
                    "support_q": sorted(supports[1]),
                    "shield_p_edge_indices": sorted(sp),
                    "shield_q_edge_indices": sorted(sq),
                    "rotation": rotation,
                })
    return {
        "family_size": 1024,
        "networkx_version": nx.__version__,
        "counts": dict(counts),
        "failures": 0,
        "witnesses": witnesses,
        "scope": "Finite sanity control only; arbitrary-size topology is paper evidence.",
    }


if __name__ == "__main__":
    result = run()
    path = Path(__file__).with_name("small_fans.json")
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "witnesses"}, ensure_ascii=False))
