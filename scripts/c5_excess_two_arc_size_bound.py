#!/usr/bin/env python3
"""Fixed controls for the N2 original-55 size bound; no source search.

Retains literal graphs and pointers to every complete local fibre in the frozen
63-graph input. Synthetic minors and cactus counts test separate paper steps.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

import networkx as nx

from c5_excess_two_arc_leaf_blocks import (
    adjacency, blocks, clean, connected, digest, encode,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/c5_excess_two_arc_component_slack/observations.json"
DEFAULT = ROOT / "artifacts/c5_excess_two_arc_size_bound/observations.json"
BEDGES = clean((i, (i + 1) % 5) for i in range(5))


def graph(vertices, edges):
    g = nx.Graph()
    g.add_nodes_from(vertices)
    g.add_edges_from(edges)
    return g


def block_data(vertices, edges):
    vertices, edges = tuple(sorted(vertices)), clean(edges)
    g = graph(vertices, edges)
    ours = blocks(vertices, edges)
    independent = tuple(sorted(tuple(sorted(b)) for b in nx.biconnected_components(g)))
    assert ours == independent
    cycles, valid = [], True
    for b in ours:
        h = g.subgraph(b)
        if len(b) == 2:
            continue
        is_cycle = len(b) % 2 == 1 and all(d == 2 for _, d in h.degree())
        valid &= is_cycle
        if is_cycle:
            cycles.append(b)
    degrees = Counter(dict(g.degree()).values())
    low = tuple(v for v in vertices if g.degree(v) <= 2)
    info = {"blocks": ours, "odd_cycle_blocks": cycles,
            "degree_counts": dict(sorted(degrees.items())), "low_vertices": low,
            "odd_cactus_max_degree_four": valid and max(dict(g.degree()).values()) <= 4}
    if len(vertices) > 1 and info["odd_cactus_max_degree_four"]:
        n, ell, c = len(vertices), len(low), len(cycles)
        assert c == len(edges) - n + 1
        assert n == ell + degrees[1] + 2 * c - 2 - degrees[4]
        # Replace each cycle by its incidence star: this must be a tree.
        tree = nx.Graph()
        tree.add_nodes_from(("v", v) for v in vertices)
        cycle_edges = set()
        for i, b in enumerate(cycles):
            tree.add_edges_from((("c", i), ("v", v)) for v in b)
            cycle_edges.update(e for e in edges if set(e) <= set(b))
        tree.add_edges_from((("v", a), ("v", b)) for a, b in edges if (a, b) not in cycle_edges)
        assert nx.is_tree(tree)
        leaves = tuple(sorted(v for v, d in tree.degree() if d == 1))
        assert all(kind == "v" and v in low for kind, v in leaves)
        assert c <= len(leaves) - 2 <= ell - 2
        assert n <= 3 * ell + degrees[1] - 6
        info["count_status"] = "triggered and holds"
        info["incidence_tree_edges"] = sorted(tuple(sorted(e)) for e in tree.edges())
        info["incidence_tree_leaves"] = leaves
    else:
        info["count_status"] = "not triggered: singleton handled separately" if len(vertices) == 1 else "not triggered"
    return info


def minor(edges, bags, pairs):
    edges, bags = clean(edges), tuple(tuple(sorted(b)) for b in bags)
    assert len(set(v for b in bags for v in b)) == sum(map(len, bags))
    trees = []
    for bag in bags:
        assert connected(bag, edges)
        g = graph(bag, (e for e in edges if set(e) <= set(bag)))
        trees.append(clean(nx.bfs_edges(g, min(bag))))
    witnesses = []
    for i, j in pairs:
        choices = [e for e in edges if (e[0] in bags[i] and e[1] in bags[j]) or
                   (e[1] in bags[i] and e[0] in bags[j])]
        assert choices
        witnesses.append({"pair": (i, j), "edge": choices[0]})
    assert not nx.check_planarity(graph(set(v for e in edges for v in e), edges))[0]
    return {"bags": bags, "bag_trees": trees, "original_edge_witnesses": witnesses,
            "minor_status": "triggered and holds", "disk_source_status": "not triggered: nonplanar"}


def same_cycle_controls():
    result = []
    for a, b, length, shift, sign in product(range(2, 6), range(1, 5), range(3), range(5), (-1, 1)):
        cycle = tuple(range(5, 5 + a + b))
        u, v, x = cycle[0], cycle[a], cycle[1]
        internal = clean(zip(cycle, cycle[1:] + cycle[:1]))
        extra = tuple(range(5 + a + b, 5 + a + b + length))
        tether = (x,) + extra + (2,)
        edges = clean(BEDGES + internal + tuple(zip(tether, tether[1:])) + ((u, 0), (u, 1), (v, 0), (v, 1)))
        bags = ((u,) + cycle[a + 1:], (v,), (0,), (1,), (2, 3, 4) + cycle[1:a] + extra)
        move = lambda z: (shift + sign * z) % 5 if z < 5 else z
        edges = clean((move(p), move(q)) for p, q in edges)
        bags = tuple(tuple(move(z) for z in bag) for bag in bags)
        assert all(len(adjacency(edges)[w] - set(range(5))) == 2 for w in (u, v))
        result.append({"parameters": (a, b, length, shift, sign), "edges": edges,
                       "marked_vertices": (u, v), "K5": minor(edges, bags, combinations(range(5), 2))})
    return result


def different_block_controls():
    result = []
    for left, right, shift, sign in product((3, 5, 7), (3, 5, 7), range(5), (-1, 1)):
        # Two cycles share only x=5; marked vertices are in different blocks.
        c1 = (5,) + tuple(range(6, 5 + left))
        c2 = (5,) + tuple(range(5 + left, 4 + left + right))
        u, v = c1[1], c2[1]
        interior = tuple(sorted(set(c1 + c2)))
        edges = clean(BEDGES + tuple(zip(c1, c1[1:] + c1[:1])) +
                      tuple(zip(c2, c2[1:] + c2[:1])) + ((u, 0), (u, 1), (v, 0), (v, 1), (5, 2)))
        assert connected(set(interior) - {u, v}, edges)
        bags = ((0,), (1,), tuple(w for w in interior if w not in (u, v)), (u,), (v,), (2, 3, 4))
        move = lambda z: (shift + sign * z) % 5 if z < 5 else z
        edges = clean((move(p), move(q)) for p, q in edges)
        bags = tuple(tuple(move(z) for z in bag) for bag in bags)
        result.append({"parameters": (left, right, shift, sign), "edges": edges,
                       "marked_vertices": (u, v), "K33": minor(edges, bags, product(range(3), range(3, 6)))})
    return result


def named_cacti():
    yield "single_vertex", (0,), ()
    for n in range(2, 13):
        yield f"path_{n}", tuple(range(n)), clean((i, i + 1) for i in range(n - 1))
    for length in (3, 5, 7):
        for count in range(1, 7):
            edges, nxt, previous = [], 0, None
            for _ in range(count):
                cycle = tuple(range(nxt, nxt + length))
                edges.extend(zip(cycle, cycle[1:] + cycle[:1]))
                if previous is not None:
                    edges.append((previous, cycle[0]))
                previous, nxt = cycle[1], nxt + length
            base = clean(edges)
            yield f"bridge_cycle_chain_{length}_{count}", tuple(range(nxt)), base
            # Maximal port use shows why n <= 3*ell-6 alone is false.
            adj = adjacency(base)
            for v in range(nxt):
                if len(adj[v]) == 2:
                    edges.append((v, nxt))
                    nxt += 1
            yield f"leaf_completed_chain_{length}_{count}", tuple(range(nxt)), clean(edges)
    for count in range(1, 9):
        edges, cut, nxt = [], 0, 1
        for _ in range(count):
            edges.extend(((cut, nxt), (nxt, nxt + 1), (nxt + 1, cut)))
            cut, nxt = nxt + 1, nxt + 2
        yield f"shared_triangle_chain_{count}", tuple(range(nxt)), clean(edges)
    yield "three_arm_tree", (0, 1, 2, 3), ((0, 1), (0, 2), (0, 3))
    yield "four_arm_tree", (0, 1, 2, 3, 4), ((0, 1), (0, 2), (0, 3), (0, 4))


def disk_certificate(vertices, edges):
    apex = max(vertices) + 1
    augmented = clean(edges + tuple((apex, b) for b in range(5)))
    ok, embedding = nx.check_planarity(graph(tuple(vertices) + (apex,), augmented))
    assert ok
    embedding.check_structure()
    seen, faces = set(), []
    for a, b in sorted(embedding.edges()):
        if (a, b) not in seen:
            faces.append(tuple(embedding.traverse_face(a, b, seen)))
    assert len(vertices) + 1 - len(augmented) + len(faces) == 2
    return {"apex": apex, "augmented_edges": augmented,
            "rotation": [[v, list(embedding.neighbors_cw_order(v))] for v in sorted(embedding)],
            "faces": faces, "euler_characteristic": 2}


def produce():
    raw = SOURCE.read_bytes()
    saved = json.loads(raw)
    counts, records = Counter(), []
    for gi, g in enumerate(saved["records"]):
        edges, roots, interior = clean(g["edges"]), tuple(g["roots"]), tuple(g["interior_coordinates"])
        adj = adjacency(edges)
        assert len(set(roots)) == 2 and all(len(adj[v]) == 5 for v in roots)
        assert all(len(adj[v]) == 4 for v in set(interior) - set(roots))
        he = tuple(e for e in edges if set(e) <= set(interior))
        h = graph(interior, he)
        actual_components = tuple(sorted(tuple(sorted(c)) for c in
                                         nx.connected_components(h.subgraph(set(interior) - set(roots)))))
        assert actual_components == tuple(sorted(tuple(c["vertices"]) for c in g["components"]))
        bs = blocks(interior, he)
        assert bs == tuple(sorted(tuple(sorted(b)) for b in nx.biconnected_components(h)))
        full = all(adj[b] & set(interior) for b in range(5))
        boundary_ok = all(len(adj[v] & set(range(5))) <= 2 and
                          (len(adj[v] & set(range(5))) < 2 or clean((tuple(sorted(adj[v] & set(range(5)))),))[0] in BEDGES)
                          for v in interior)
        d2 = tuple(v for v in interior if h.degree(v) == 2)
        injection_trigger = full and boundary_ok and not list(nx.bridges(h)) and all(v not in roots for v in d2)
        if injection_trigger:
            pairs = [tuple(sorted(adj[v] & set(range(5)))) for v in d2]
            assert len(set(pairs)) == len(pairs) <= 5
        counts["low_degree_injection_triggered"] += int(injection_trigger)
        pieces = []
        for ci, c in enumerate(g["components"]):
            verts = tuple(c["vertices"])
            ce = tuple(e for e in edges if set(e) <= set(verts))
            data = block_data(verts, ce)
            k = sum(len(adj[v] & set(roots)) for v in verts)
            d = sum(v in d2 for v in verts)
            count_trigger = boundary_ok and data["odd_cactus_max_degree_four"]
            if count_trigger:
                if len(verts) > 1:
                    assert len(data["low_vertices"]) + data["degree_counts"].get(1, 0) <= k + d
                else:
                    assert (k, d) == (2, 1)
                assert len(verts) <= 3 * (k + d) - 6
            counts["component_size_inequality_triggered"] += int(count_trigger)
            refs = [{"json_pointer": f"/records/{gi}/components/{ci}/rows/{ri}/local_full_fibres_by_pins",
                     "beta": row["beta"], "sha256": digest(row["local_full_fibres_by_pins"]),
                     "counts_in_original_pin_order": list(map(len, row["local_full_fibres_by_pins"]))}
                    for ri, row in enumerate(c["rows"])]
            pieces.append({"vertices": verts, "edges": ce, "root_incidences": k,
                           "H_degree_two_count": d, "complete_fibre_references": refs,
                           "size_inequality_status": "triggered and holds" if count_trigger else "not triggered", **data})
        counts["fixed_graphs"] += 1
        counts["fixed_components"] += len(pieces)
        counts["complete_fibre_references"] += sum(len(c["rows"]) for c in g["components"])
        target = any({(shift + sign * i) % 5 for i in (0, 1, 3)} <= set(g["Q"])
                     for shift, sign in product(range(5), (-1, 1)))
        counts["target_source_triggered"] += int(target)
        records.append({"source_record_index": gi, "edges": edges, "roots": roots,
                        "interior_coordinates": interior, "sigma_mask": g["sigma_mask"],
                        "H_blocks": bs, "H_degree_two_vertices": d2,
                        "injection_status": "triggered and holds" if injection_trigger else "not triggered",
                        "components": pieces, "target_source_status": "triggered" if target else "not triggered"})
    cactus = [{"name": name, "vertices": vs, "edges": es, **block_data(vs, es)}
              for name, vs, es in named_cacti()]
    # K4 violates the count when the no-K4 premise is dropped.
    k4edges = clean(combinations(range(4), 2))
    k4 = {"edges": k4edges, **block_data(tuple(range(4)), k4edges),
          "stronger_claim_status": "counterexample: cactus premise removed"}
    # The n1 term is needed for general cacti: triangle with one leaf at each vertex.
    star = next(c for c in cactus if c["name"] == "leaf_completed_chain_3_1")
    assert len(star["vertices"]) > 3 * len(star["low_vertices"]) - 6
    # Without full B-touch, repeated adjacent supports can occur in one block.
    negative_edges = clean(BEDGES + ((5, 6), (6, 7), (7, 8), (8, 5), (5, 0), (5, 1), (7, 0), (7, 1)))
    negative = {"vertices": tuple(range(9)), "edges": negative_edges, "marked_vertices": (5, 7),
                "disk": disk_certificate(tuple(range(9)), negative_edges),
                "status": "counterexample to injection without full B-touch",
                "target_source_status": "not triggered: degrees and boundary touch fail"}
    k5, k33 = same_cycle_controls(), different_block_controls()
    counts.update({"named_cactus_controls": len(cactus), "K5_controls": len(k5), "K33_controls": len(k33)})
    assert counts["target_source_triggered"] == 0
    return {"scope": "fixed input graphs, named minors and cactus counts; no source enumeration",
            "input": {"path": str(SOURCE.relative_to(ROOT)), "sha256": sha256(raw).hexdigest()},
            "networkx_version": nx.__version__, "original_pin_order": saved["pin_order"],
            "counts": dict(sorted(counts.items())), "records": records,
            "same_cycle_K5_controls": k5, "different_block_K33_controls": k33,
            "named_cactus_controls": cactus, "K4_negative_control": k4,
            "missing_leaf_term_negative_control": star, "missing_full_touch_negative_control": negative,
            "target_source_status": "not triggered", "N2_exclusion": "OPEN", "E_ARC2": "OPEN",
            "evidence_limit": "size bound is paper-only; finite controls do not establish source existence or exclusion"}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--check", action="store_true")
    p.add_argument("--output", type=Path, default=DEFAULT)
    args = p.parse_args()
    result = produce()
    raw = encode(result)
    if args.check:
        assert args.output.read_bytes() == raw, "artifact mismatch"
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("xb") as f:
            f.write(raw)
    print(json.dumps({"check": args.check, "sha256": sha256(raw).hexdigest(),
                      "bytes": len(raw), **result["counts"]}, sort_keys=True))


if __name__ == "__main__":
    main()
