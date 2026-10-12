#!/usr/bin/env python3
"""Deterministic fixed topology domain; deliberately computes no colourings.

All transformed rotations are inherited by local surgery, never reembedded.
The upstream catalogue supplies literal edges but no historical rotation.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
B = list(range(5))
CYCLE = {tuple(sorted((i, (i + 1) % 5))) for i in B}


def canon_cycle(seq):
    seq = list(seq)
    return min(seq[i:] + seq[:i] for i in range(len(seq))) if seq else []


def edge(a, b):
    return tuple(sorted((a, b)))


def face_walks(rotation):
    """Faces from the predecessor in the stored clockwise order."""
    unseen = {(u, v) for u, ns in rotation.items() for v in ns}
    faces = []
    while unseen:
        start = min(unseen)
        dart = start
        walk = []
        while True:
            assert dart in unseen, (start, dart)
            unseen.remove(dart)
            u, v = dart
            walk.append(u)
            ns = rotation[v]
            dart = (v, ns[(ns.index(u) - 1) % len(ns)])
            if dart == start:
                break
        faces.append(canon_cycle(walk))
    return sorted(faces)


def graph_record(rotation):
    rotation = {u: canon_cycle(ns) for u, ns in sorted(rotation.items())}
    es = sorted({edge(u, v) for u, ns in rotation.items() for v in ns})
    assert all(u != v for u, v in es)
    assert all(len(ns) == len(set(ns)) for ns in rotation.values())
    assert all(u in rotation[v] for u, ns in rotation.items() for v in ns)
    g = nx.Graph()
    g.add_nodes_from(rotation)
    g.add_edges_from(es)
    assert nx.is_connected(g)
    faces = face_walks(rotation)
    assert len(rotation) - len(es) + len(faces) == 2
    assert B in faces
    return {"nodes": sorted(rotation), "boundary": B[:],
            "edges": [list(e) for e in es],
            "rotation": {str(u): ns for u, ns in rotation.items()},
            "faces": faces}


def as_rotation(graph):
    return {int(u): ns[:] for u, ns in graph["rotation"].items()}


def source_embedding(nodes, edges):
    apex = max(nodes) + 1
    g = nx.Graph()
    g.add_nodes_from(sorted(nodes) + [apex])
    g.add_edges_from(sorted(set(map(tuple, edges)) | {edge(b, apex) for b in B}))
    planar, embedding = nx.check_planarity(g)
    assert planar
    rotation = {u: [v for v in embedding.neighbors_cw_order(u) if v != apex]
                for u in sorted(nodes)}
    fs = face_walks(rotation)
    if B not in fs:
        assert canon_cycle(list(reversed(B))) in fs
        rotation = {u: list(reversed(ns)) for u, ns in rotation.items()}
    return graph_record(rotation)


def remove_edge(rotation, u, v):
    result = {x: ns[:] for x, ns in rotation.items()}
    result[u].remove(v)
    result[v].remove(u)
    return result


def remove_vertex(rotation, v):
    return {u: [w for w in ns if w != v]
            for u, ns in rotation.items() if u != v}


def dart_face(rotation, u, v):
    start = (u, v)
    dart = start
    result = []
    while True:
        u, v = dart
        result.append(u)
        ns = rotation[v]
        dart = (v, ns[(ns.index(u) - 1) % len(ns)])
        if dart == start:
            return result


def add_face_chord(rotation, face, a, b):
    result = {u: ns[:] for u, ns in rotation.items()}
    for u, other in ((a, b), (b, a)):
        i = face.index(u)
        next_u = face[(i + 1) % len(face)]
        previous_u = face[(i - 1) % len(face)]
        ns = result[u]
        assert ns[(ns.index(next_u) + 1) % len(ns)] == previous_u
        ns.insert(ns.index(next_u) + 1, other)
    return result


def partitions(n):
    """Restricted-growth strings, each set partition exactly once."""
    def visit(labels):
        if len(labels) == n:
            blocks = [[i for i, t in enumerate(labels) if t == j]
                      for j in range(max(labels) + 1)]
            yield labels, blocks
        else:
            for j in range(max(labels) + 2):
                yield from visit(labels + [j])
    return list(visit([0]))


def noncrossing(labels):
    n = len(labels)
    crossings = []
    for a in range(n):
        for b in range(a + 1, n):
            for c in range(b + 1, n):
                for d in range(c + 1, n):
                    if labels[a] == labels[c] != labels[b] == labels[d]:
                        crossings.append([a, b, c, d])
    return crossings


def quotient_surgery(source, v, L, blocks):
    """Insert disjoint polygon fans in star slots, contract, simplify parallels.

    Ribbons carry persistent source-edge IDs, so a parallel simplification cannot
    silently choose a new embedding. The five original boundary edges survive.
    """
    original = as_rotation(source)
    source_edges = [tuple(e) for e in source["edges"] if v not in e]
    chords = [edge(block[0], x) for block in blocks for x in block[1:]]
    assert not (set(chords) & set(source_edges))
    augmented = remove_vertex(original, v)
    # Circle L uses the clockwise order at v. At l_i the new darts replacing
    # its old spoke occur in the cyclic order l_(i+1), ..., l_(i-1).
    for i, u in enumerate(L):
        targets = {b if a == u else a for a, b in chords if u in (a, b)}
        replacement = [L[(i + j) % 5] for j in range(1, 5)
                       if L[(i + j) % 5] in targets]
        ns = original[u][:]
        pos = ns.index(v)
        augmented[u] = ns[:pos] + replacement + ns[pos + 1:]
    augmented_graph = graph_record(augmented)
    endpoints = {"s:%d,%d" % e: e for e in source_edges}
    endpoints.update({"c:%d,%d" % e: e for e in chords})
    dart_id = {e: eid for eid, e in endpoints.items()}
    ribbon = {u: [dart_id[edge(u, x)] for x in ns]
              for u, ns in augmented.items()}
    mapping = {u: u for u in augmented}
    contraction_steps = []
    for block in blocks:
        representative = next((x for x in block if x in B), min(block))
        for x in block:
            mapping[x] = representative
    for a, b in chords:
        eid = "c:%d,%d" % (a, b)
        u, w = endpoints[eid]
        assert u != w
        representative = mapping[a]
        # The representative need not yet be incident with this tree edge.
        # Use either currently existing endpoint, preferring the final name.
        keep = representative if representative in (u, w) else min(u, w)
        drop = w if keep == u else u
        left, right = ribbon[keep], ribbon[drop]
        i, j = left.index(eid), right.index(eid)
        merged = left[i + 1:] + left[:i] + right[j + 1:] + right[:j]
        ribbon[keep] = merged
        del ribbon[drop]
        del endpoints[eid]
        for key, (x, y) in list(endpoints.items()):
            endpoints[key] = (keep if x == drop else x, keep if y == drop else y)
        contraction_steps.append({"chord": [a, b], "edge_id": eid,
                                  "keep": keep, "drop": drop,
                                  "rotation_after": {str(x): ns[:] for x, ns in sorted(ribbon.items())}})
    # Relabel final blocks if temporary fan-root contraction names differ.
    final_name = {u: mapping[u] for u in ribbon}
    assert len(set(final_name.values())) == len(final_name)
    ribbon = {final_name[u]: ns for u, ns in ribbon.items()}
    endpoints = {eid: edge(final_name[a], final_name[b])
                 for eid, (a, b) in endpoints.items()}
    groups = defaultdict(list)
    for eid, e in endpoints.items():
        assert e[0] != e[1]
        groups[e].append(eid)
    preimages = []
    for e, ids in sorted(groups.items()):
        def priority(eid):
            old = tuple(map(int, eid[2:].split(",")))
            return (0 if old in CYCLE else 1, old)
        ids.sort(key=priority)
        for eid in ids[1:]:
            for u in e:
                ribbon[u].remove(eid)
            del endpoints[eid]
        source_preimages = [list(map(int, eid[2:].split(","))) for eid in ids]
        preimages.append({"edge": list(e), "source_edges": source_preimages,
                          "retained_source_edge": source_preimages[0],
                          "removed_parallel_source_edges": source_preimages[1:]})
    rotation = {u: [b if a == u else a for eid in ns
                    for a, b in [endpoints[eid]]]
                for u, ns in ribbon.items()}
    result = graph_record(rotation)
    expected = sorted({edge(mapping[a], mapping[b]) for a, b in source_edges})
    assert result["edges"] == [list(e) for e in expected]
    assert all(mapping[b] == b for b in B)
    return {"graph": result, "vertex_map": {str(u): mapping[u] for u in sorted(mapping)},
            "edge_preimages": preimages,
            "surgery": {"method": "star-slot noncrossing chord fans, ribbon contractions, edge deletions",
                        "chords": [list(e) for e in chords],
                        "augmented_graph": augmented_graph,
                        "contractions": contraction_steps,
                        "parallel_rule": "keep original boundary edge first, otherwise lexicographically first source edge"}}


def ownership(graph, v, L):
    es = [tuple(e) for e in graph["edges"]]
    interface = sorted(set(B + L))
    g = nx.Graph()
    g.add_nodes_from(u for u in graph["nodes"] if u not in interface)
    g.add_edges_from((a, b) for a, b in es if a not in interface and b not in interface)
    bridges = []
    for component in sorted(sorted(c) for c in nx.connected_components(g)):
        support = sorted({u for e in es for u in e if u in interface
                          and any(w in component for w in e)})
        owned_edges = [list(e) for e in es if any(u in component for u in e)]
        bridges.append({"kind": "component", "vertices": component,
                        "support": support, "edges": owned_edges,
                        "contains_center": v in component})
    for e in es:
        if all(u in interface for u in e):
            bridges.append({"kind": "interface_edge", "vertices": [],
                            "support": list(e), "edges": [list(e)], "contains_center": False})
    flat = [tuple(e) for b in bridges for e in b["edges"]]
    assert sorted(flat) == sorted(es)
    remaining = nx.Graph()
    remaining.add_nodes_from(u for u in graph["nodes"] if u != v)
    remaining.add_edges_from(e for e in es if v not in e)
    return {"interface": interface,
            "boundary_positions": [{"label": b, "B_position": b,
                                     "L_position": L.index(b) if b in L else None} for b in B],
            "spokes": [list(edge(v, u)) for u in L],
            "bridges_over_named_interface": bridges,
            "deleted_center_components": sorted(sorted(c) for c in nx.connected_components(remaining)),
            "deleted_center_cut_edges": [list(e) for e in sorted(edge(a, b) for a, b in nx.bridges(remaining))]}


def build_mark(source, v):
    sg = source["graph"]
    rotation = as_rotation(sg)
    L = rotation[v][:]
    assert len(L) == 5
    mark_id = source["id"] + ":v" + str(v)
    es = set(map(tuple, sg["edges"]))
    ops, flips, quotients = [], [], []
    for i, u in enumerate(L):
        deleted = remove_edge(rotation, v, u)
        spoke = list(edge(v, u))
        ops.append({"id": mark_id + ":delete:" + str(i), "kind": "delete",
                    "spoke": spoke, "spoke_index": i, "graph": graph_record(deleted),
                    "legality": {"status": "triggered and holds", "method": "delete original spoke darts"}})
        left, right = dart_face(rotation, v, u), dart_face(rotation, u, v)
        triangles = len(left) == len(right) == 3 and left != right
        distinct_quad = len(set(left + right)) == 4
        inner = canon_cycle(left) != B and canon_cycle(right) != B
        opposite = sorted((set(left + right) - {u, v}))
        diagonal_absent = len(opposite) == 2 and tuple(opposite) not in es
        eligible = triangles and distinct_quad and inner and diagonal_absent
        rec = {"spoke": spoke, "spoke_index": i,
               "incident_faces": [left, right], "opposite": opposite,
               "two_triangles": triangles, "distinct_quadrilateral": distinct_quad,
               "both_inner": inner, "opposite_diagonal_absent": diagonal_absent,
               "eligible": eligible}
        if eligible:
            face = next(f for f in face_walks(deleted) if len(f) == 4 and set(f) == set(left + right))
            operation_id = mark_id + ":flip:" + str(i)
            rec["operation_id"] = operation_id
            ops.append({"id": operation_id, "kind": "flip", "spoke": spoke,
                        "spoke_index": i, "diagonal": opposite,
                        "graph": graph_record(add_face_chord(deleted, face, *opposite)),
                        "legality": {"status": "triggered and holds", "method": "delete spoke and insert opposite diagonal in inherited quadrilateral",
                                     "incident_faces": [left, right], "quadrilateral_face": face}})
        flips.append(rec)
    for labels, positions in partitions(5):
        blocks = [[L[i] for i in block] for block in positions]
        nontrivial = any(len(block) > 1 for block in blocks)
        crossing = noncrossing(labels)
        bad_boundary = [block for block in blocks if len(set(block) & set(B)) > 1]
        forbidden_edges = sorted({edge(a, b) for block in blocks for a in block for b in block
                                  if a < b and edge(a, b) in es})
        eligible = nontrivial and not crossing and not bad_boundary and not forbidden_edges
        rec = {"restricted_growth": labels, "position_blocks": positions, "blocks": blocks,
               "nontrivial": nontrivial, "crossing_position_quadruples": crossing,
               "multiple_boundary_blocks": bad_boundary,
               "adjacent_identified_pairs": [list(e) for e in forbidden_edges],
               "eligible": eligible}
        if eligible:
            operation_id = mark_id + ":quotient:" + "".join(map(str, labels))
            rec["operation_id"] = operation_id
            result = quotient_surgery(sg, v, L, blocks)
            ops.append({"id": operation_id, "kind": "quotient", "partition": blocks,
                        "restricted_growth": labels, **result,
                        "legality": {"status": "triggered and holds", "noncrossing": True,
                                     "boundary_injective": True, "loopless": True,
                                     "each_identified_pair_nonadjacent": True,
                                     "each_identified_pair_has_original_interior_endpoint": True}})
        quotients.append(rec)
    ops.sort(key=lambda op: {"delete": 0, "flip": 1, "quotient": 2}[op["kind"]])
    return {"id": mark_id, "source_id": source["id"], "v": v, "L": L,
            "link_edges_present": [list(edge(L[i], L[(i + 1) % 5])) in sg["edges"] for i in range(5)],
            "is_C5_link": all(edge(L[i], L[(i + 1) % 5]) in es for i in range(5)),
            "star_ownership": ownership(sg, v, L),
            "deleted_center_graph": graph_record(remove_vertex(rotation, v)),
            "flip_candidates": flips, "quotient_candidates": quotients, "operations": ops}


def build_domain():
    assert nx.__version__ == "3.5", "frozen embedding policy requires NetworkX 3.5"
    cells_path = next((ROOT / "frozen").rglob("cells.json"))
    certificate_path = next((ROOT / "frozen").rglob("certificate.v2.json"))
    data = json.loads(cells_path.read_text())
    certificate = json.loads(certificate_path.read_text())
    assert data["pattern_order"] == certificate["pattern_order"]
    assert len(data["cells"]) == 132
    sources = []
    for mask, cell in sorted(data["cells"].items(), key=lambda pair: int(pair[0])):
        nodes = list(range(5 + cell["k_eff"]))
        edges = sorted(CYCLE | set(map(tuple, cell["edges"])))
        graph = source_embedding(nodes, edges)
        sources.append({"id": "catalogue:" + mask, "catalogue_sigma": int(mask),
                        "graph": graph, "kind": "catalogue_literal",
                        "degree5_vertices": [v for v in nodes if v not in B and len(graph["rotation"][str(v)]) == 5]})
    wheel = source_embedding(list(range(6)), sorted(CYCLE | {(b, 5) for b in B}))
    sources.append({"id": "W5", "catalogue_sigma": None, "kind": "explicit_W5_control",
                    "graph": wheel, "degree5_vertices": [5]})
    # Complete source list and rotations exist before any operation is constructed.
    source_json = json.dumps(sources, sort_keys=True, separators=(",", ":")).encode()
    marks = [build_mark(source, v) for source in sources for v in source["degree5_vertices"]]
    counts = Counter(op["kind"] for mark in marks for op in mark["operations"])
    assert len(marks) == 77
    return {"schema": "degree5-star-fixed-topology-v1", "networkx_version": nx.__version__,
            "embedding_policy": "sorted nodes and sorted edges; append an exterior apex adjacent to B; NetworkX 3.5 check_planarity; remove apex; reflect globally if needed to make B=[0,1,2,3,4] a forward face; canonical cyclic rotations",
            "historical_rotation_status": "not supplied upstream; this is one reconstructed and frozen valid disk embedding per literal graph, not a claim about the unavailable historical embedding or every embedding",
            "source_rotations_sha256": hashlib.sha256(source_json).hexdigest(),
            "sources": sources, "marks": marks, "patterns": data["pattern_order"],
            "mark_rule": "all original interior labels with graph degree exactly 5, all catalogue sources in numeric sigma order, then explicit W5 center",
            "partition_rule": "all 52 set partitions of the five clockwise named neighbors; identity is recorded ineligible; reject alternating blocks, two distinct B labels in a block, or an original edge inside a block",
            "counts": {"catalogue_sources": 132, "extra_W5_sources": 1, "sources": len(sources),
                       "catalogue_marks": 76, "extra_W5_marks": 1, "marks": len(marks),
                       "source_mark_pattern_rows": 10 * len(marks),
                       "flip_candidates": 5 * len(marks), "quotient_partitions_per_mark": 52,
                       "quotient_candidates": 52 * len(marks),
                       "operations": sum(counts.values()), "operation_pattern_rows": 10 * sum(counts.values()),
                       "operations_by_kind": dict(sorted(counts.items()))}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "controls/domain.json")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    domain = build_domain()
    if args.check:
        assert json.loads(args.output.read_text()) == domain
    else:
        with args.output.open("x") as handle:
            json.dump(domain, handle, sort_keys=True, separators=(",", ":"))
            handle.write("\n")
    print(json.dumps(domain["counts"], sort_keys=True))


if __name__ == "__main__":
    main()
