#!/usr/bin/env python3
"""Finite named controls only; no enumeration of source graphs.

Requires NetworkX 3.5. Enumerates all 4^n interior colorings of each explicitly
named graph, saves all successes and failures, and independently checks the
saved planar rotation's faces and Euler characteristic.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import random

import networkx as nx

BASE = "4dd11f422c6fa49265a412085116b088786d0344"
B = ["b0", "b1", "b2", "b3", "b4"]
CYCLE = [(B[i], B[(i + 1) % 5]) for i in range(5)]
NAMED = [
    dict(id="original-domain-triangle", s="s", interior=["s", "x", "y"],
         h_edges=[("s", "x"), ("s", "y"), ("x", "y")],
         attachments={"s": [0, 1, 2], "x": [3, 4], "y": [2, 3]},
         beta=[0, 1, 2, 1, 2], status="triggered and holds",
         claim="The full original-domain implication.", expected_original=True),
    dict(id="biconnectivity-removed-path", s="s", interior=["s", "x", "y"],
         h_edges=[("s", "x"), ("x", "y")],
         attachments={"s": [0, 1, 2, 3], "x": [0, 3], "y": [0, 3, 4]},
         beta=[0, 1, 2, 3, 1], status="counterexample",
         claim="Remove biconnectivity, keep all other graph and row premises.",
         expected_original=False),
    dict(id="second-degree5-diamond", s="s", interior=["s", "x", "t", "y"],
         h_edges=[("s", "x"), ("x", "t"), ("t", "y"), ("y", "s"), ("s", "t")],
         attachments={"s": [0, 1], "x": [1, 2], "t": [2, 3], "y": [0, 3]},
         beta=[0, 1, 0, 1, 2], status="counterexample",
         claim="Allow a second interior degree-5 vertex, retain biconnectivity and proper beta.",
         expected_original=False),
    dict(id="improper-beta-diamond", s="s", interior=["s", "x", "t", "y"],
         h_edges=[("s", "x"), ("x", "t"), ("t", "y"), ("y", "s"), ("s", "t")],
         attachments={"s": [0, 1], "x": [1, 2], "t": [3], "y": [0, 4]},
         beta=[0, 0, 0, 0, 0], status="counterexample",
         claim="Allow improper beta while retaining the full graph premises.",
         expected_original=False),
    dict(id="actual-attachments-lost-k4", s="s", interior=["s", "x", "t", "y"],
         h_edges=list(itertools.combinations(["s", "x", "t", "y"], 2)),
         attachments={"s": [0], "x": [], "t": [], "y": []},
         beta=[0, 1, 0, 1, 2], status="counterexample",
         claim="The intermediate inference H contains K4, so H together with B contains K5, without original attachments.",
         expected_original=False),
    dict(id="honest-supergraph-degree-bookkeeping", s="s", interior=["s", "x", "y"],
         h_edges=[("s", "x"), ("s", "y"), ("x", "y")],
         attachments={"s": [1, 2], "x": [3, 4], "y": [2, 3]},
         source_attachments={"s": [0, 1, 2], "x": [3, 4], "y": [2, 3]},
         beta=[0, 1, 2, 1, 2], status="triggered and holds",
         claim="Honest M subset G supplies upper bounds but does not identify d_M with d_G; this example is not a theorem counterexample.",
         expected_original=False),
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def graph(spec):
    g = nx.Graph()
    g.add_nodes_from(B + spec["interior"])
    g.add_edges_from(CYCLE)
    g.add_edges_from(spec["h_edges"])
    for v, indices in spec["attachments"].items():
        g.add_edges_from((v, B[i]) for i in indices)
    return g


def gallai(g):
    if not nx.is_connected(g):
        return False
    for vertices in nx.biconnected_components(g):
        q = g.subgraph(vertices)
        n = len(q)
        if q.number_of_edges() == n * (n - 1) // 2:
            continue
        if n % 2 == 1 and n >= 3 and all(q.degree(v) == 2 for v in q):
            continue
        return False
    return True


def rotation_certificate(g):
    augmented = g.copy()
    augmented.add_edges_from(("outside-apex", b) for b in B)
    planar, augmented_embedding = nx.check_planarity(augmented)
    assert planar
    rot = {v: [w for w in augmented_embedding.neighbors_cw_order(v)
               if w != "outside-apex"] for v in g}
    embedding = nx.PlanarEmbedding()
    embedding.set_data(rot)
    embedding.check_structure()
    seen = set()
    faces = []
    for u in g:
        for v in rot[u]:
            if (u, v) not in seen:
                faces.append(embedding.traverse_face(u, v, seen))
    outer = [f for f in faces if len(f) == 5 and set(f) == set(B)]
    assert len(outer) == 1
    assert len(g) - g.number_of_edges() + len(faces) == 2
    return dict(rotation=rot, faces=faces, outer_face=outer[0],
                disk_verified=True, disk_method="boundary-apex planarity; then independently replay saved rotation, faces, outer C5 and Euler characteristic",
                apex_rotation={v: list(augmented_embedding.neighbors_cw_order(v))
                               for v in augmented})


def make_record(spec):
    g = graph(spec)
    h = g.subgraph(spec["interior"])
    beta = dict(zip(B, spec["beta"]))
    proper_beta = all(beta[u] != beta[v] for u, v in CYCLE)
    degrees = {v: g.degree(v) for v in spec["interior"]}
    exact_degrees = degrees[spec["s"]] == 5 and all(
        degrees[v] == 4 for v in spec["interior"] if v != spec["s"])
    lists = {v: sorted(set(range(4)) - {beta[B[i]] for i in spec["attachments"][v]})
             for v in spec["interior"]}
    outcomes = []
    edges = sorted(tuple(sorted(e)) for e in g.edges())
    for colors in itertools.product(range(4), repeat=len(spec["interior"])):
        assignment = beta | dict(zip(spec["interior"], colors))
        conflicts = [list(e) for e in edges if assignment[e[0]] == assignment[e[1]]]
        h_conflicts = [list(e) for e in spec["h_edges"] if assignment[e[0]] == assignment[e[1]]]
        list_violation = [v for v in spec["interior"] if assignment[v] not in lists[v]]
        outcomes.append(dict(interior_colors=list(colors),
                             boundary_preserving_assignment=assignment,
                             conflicts=conflicts, h_conflicts=h_conflicts,
                             list_violation=list_violation,
                             list_coloring=not h_conflicts and not list_violation,
                             extension=not conflicts))
    extension_count = sum(o["extension"] for o in outcomes)
    list_colorings = sum(o["list_coloring"] for o in outcomes)
    # Independent list-restricted search; seed 17 only changes traversal order
    # within the same named graph and never creates additional source graphs.
    shuffled_vertices = list(spec["interior"])
    random.Random(17).shuffle(shuffled_vertices)
    shuffled_domains = [list(lists[v]) for v in shuffled_vertices]
    independent_count = 0
    for colors in itertools.product(*shuffled_domains):
        assignment = dict(zip(shuffled_vertices, colors))
        independent_count += all(assignment[u] != assignment[v] for u, v in h.edges())
    assert independent_count == list_colorings
    conclusion = h.degree(spec["s"]) == 2 and gallai(h.subgraph([v for v in h if v != spec["s"]]))
    original_premises = exact_degrees and nx.is_biconnected(h) and proper_beta
    original_trigger = original_premises and extension_count == 0
    assert original_trigger == spec["expected_original"]
    if spec["id"] == "original-domain-triangle":
        assert conclusion
    elif spec["status"] == "counterexample" and spec["id"] != "actual-attachments-lost-k4":
        assert extension_count == 0 and not conclusion
    elif spec["id"] == "actual-attachments-lost-k4":
        assert extension_count > 0
    elif spec["id"] == "honest-supergraph-degree-bookkeeping":
        assert extension_count == 0 and conclusion and nx.is_biconnected(h) and proper_beta
    if spec["id"] == "biconnectivity-removed-path":
        assert exact_degrees and proper_beta and not nx.is_biconnected(h)
        assert sorted(dict(h.degree()).values()) == [1, 1, 2]
    if spec["id"] == "second-degree5-diamond":
        assert nx.is_biconnected(h) and proper_beta
        assert sorted(degrees.values()) == [4, 4, 5, 5]
    if spec["id"] == "improper-beta-diamond":
        assert exact_degrees and nx.is_biconnected(h) and not proper_beta
        assert list_colorings > 0
    source_record = None
    if "source_attachments" in spec:
        source = graph(spec | {"attachments": spec["source_attachments"]})
        assert set(g.edges()) <= set(source.edges())
        source_record = dict(edges=[list(e) for e in sorted(tuple(sorted(e)) for e in source.edges())],
                             full_degrees={v: source.degree(v) for v in spec["interior"]},
                             source_to_M_deleted_edges=[["s", "b0"]],
                             **rotation_certificate(source))
    return spec | dict(boundary=B, edges=[list(e) for e in edges],
                       full_degrees=degrees, interior_degrees=dict(h.degree()),
                       exact_degree_premise=exact_degrees, biconnected=nx.is_biconnected(h),
                       beta_proper=proper_beta, actual_lists=lists,
                       original_domain_status="triggered and holds" if original_trigger else "not triggered",
                       original_domain_trigger=original_trigger,
                       extension_count=extension_count, list_coloring_count=list_colorings,
                       conclusion_holds=conclusion,
                       coloring_order=spec["interior"], coloring_count=len(outcomes),
                       seed17_independent_list_coloring_count=independent_count,
                       seed17_independent_vertex_order=shuffled_vertices,
                       honest_source_G=source_record,
                       complete_coloring_outcomes=outcomes,
                       k4_branch_sets=[[v] for v in spec["interior"]]
                       if spec["id"] == "actual-attachments-lost-k4" else None,
                       proposed_fifth_branch_set=B if spec["id"] == "actual-attachments-lost-k4" else None,
                       proposed_fifth_missing_adjacencies=[v for v in spec["interior"] if not spec["attachments"][v]]
                       if spec["id"] == "actual-attachments-lost-k4" else None,
                       **rotation_certificate(g))


def negative_controls(records):
    results = []
    for key, mutate, condition in [
        ("delete-original-attachment", lambda d: d["attachments"]["s"].pop(),
         lambda d: not d["exact_degree_premise"]),
        ("improper-row-from-baseline", lambda d: d.update(beta=[0]*5),
         lambda d: not d["beta_proper"]),
    ]:
        spec = json.loads(json.dumps(NAMED[0]))
        mutate(spec)
        # Do not call make_record, whose domain-specific assertions are fixed.
        g = graph(spec)
        degree_premise = g.degree("s") == 5 and all(g.degree(v) == 4 for v in ["x", "y"])
        proper = all(spec["beta"][i] != spec["beta"][(i+1)%5] for i in range(5))
        probe = dict(exact_degree_premise=degree_premise, beta_proper=proper)
        assert condition(probe)
        results.append(dict(id=key, status="triggered and holds", claim="validator detects the stated mutated premise", mutated_input=spec, observed=probe))
    return results


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", default=str(Path(__file__).with_name("certificates-final-v1.json")))
    p.add_argument("--check", action="store_true")
    args = p.parse_args()
    root = Path(__file__).resolve().parents[4]
    records = [make_record(spec) for spec in NAMED]
    payload = dict(base=BASE, scope="six named controls only, not source enumeration or theorem coverage",
                   networkx_version=nx.__version__, replay_sha256=digest(Path(__file__)),
                   input_hashes={str(p.relative_to(root)): digest(p) for p in
                                 [root / "docs" / x for x in ["HANDOFF.md", "STATUS.md", "c5_weak_list_cores.md", "c5_degree5_guide.md"]]},
                   controls=records, negative_controls=negative_controls(records))
    output = Path(args.output)
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.check:
        assert output.read_text() == encoded, "saved full certificate differs from replay"
        print("PASS: exact replay of all six named controls, full colorings, rotations, seed17 list searches and negative controls")
    else:
        with output.open("x") as destination:
            destination.write(encoded)
        print(f"Saved {output}; controls={len(records)}; full assignments={sum(r['coloring_count'] for r in records)}")


if __name__ == "__main__":
    main()
