#!/usr/bin/env python3
"""Task S: replay named realizable T4-full Sigma-minimal disk witnesses.

Only the saved cells.json witnesses are used, never its enumerator or a
four-colour-theorem oracle. Colours, actual supports and vertex labels stay
in one ordered frame. --check recomputes every byte without writing files.
"""
from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path
import random

import networkx as nx

from c5_shield_calibration_faces import disk_embedding, piece_shield

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/c5_cells/cells.json"
OUT = ROOT / "artifacts/c5_shield_calibration"
FRAME = tuple(range(5))
FRAME_EDGES = frozenset(tuple(sorted((i, (i + 1) % 5))) for i in FRAME)
T4_INDICES = (2, 5, 7, 8, 9)
T4_MASK = sum(1 << i for i in T4_INDICES)
SEED = 20261004
ORDERS = 40
COLOUR_PERMUTATIONS = tuple(permutations(range(4)))
BOUNDARY = tuple(b for b in product(range(4), repeat=5)
                 if all(b[u] != b[v] for u, v in FRAME_EDGES))
PATTERNS = tuple(sorted({tuple(dict(zip(dict.fromkeys(b), range(4)))[c]
                                    for c in b) for b in BOUNDARY}))
assert len(BOUNDARY) == 240 and len(PATTERNS) == 10


def normalise(row):
    mapping = dict(zip(dict.fromkeys(row), range(4)))
    return tuple(mapping[c] for c in row)


def graph(vertices, edges):
    g = nx.Graph()
    g.add_nodes_from(vertices)
    g.add_edges_from(edges)
    return g


def extension(vertices, edges, boundary):
    """Exact deterministic search, with a full same-graph colouring witness."""
    adj = {v: [] for v in vertices}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    colours = dict(zip(FRAME, boundary))
    if any(colours[u] == colours[v] for u, v in edges if u < 5 and v < 5):
        return None
    left = set(vertices) - set(FRAME)

    def visit():
        if not left:
            return [colours[v] for v in vertices]
        domains = {v: tuple(c for c in range(4)
                            if all(colours.get(w) != c for w in adj[v]))
                   for v in sorted(left)}
        v = min(left, key=lambda w: (len(domains[w]), -len(adj[w]), w))
        left.remove(v)
        for c in domains[v]:
            colours[v] = c
            result = visit()
            if result is not None:
                left.add(v)
                del colours[v]
                return result
        left.add(v)
        colours.pop(v, None)
        return None

    return visit()


@lru_cache(None)
def mask(vertices, edges):
    return sum(1 << i for i, p in enumerate(PATTERNS)
               if extension(vertices, edges, p) is not None)


def sigma_certificate(vertices, edges):
    bits = mask(vertices, edges)
    witnesses = []
    # Independent exhaustive private tuples on all ten representative rows.
    for i, row in enumerate(PATTERNS):
        brute = None
        for private in product(range(4), repeat=len(vertices) - 5):
            colours = dict(zip(vertices, row + private))
            if all(colours[u] != colours[v] for u, v in edges):
                brute = list(row + private)
                break
        assert (brute is not None) == bool(bits & (1 << i))
        if brute is not None:
            witnesses.append(dict(pattern_index=i, colours_by_vertex=brute))
    # All 240 literal ordered rows are independently queried; only S4 is used.
    accepted, rejected = [], []
    for row in BOUNDARY:
        expected = bool(bits & (1 << PATTERNS.index(normalise(row))))
        assert (extension(vertices, edges, row) is not None) == expected
        (accepted if expected else rejected).append(list(row))
    for row in PATTERNS:
        assert all(normalise(tuple(p[c] for c in row)) == row
                   for p in COLOUR_PERMUTATIONS)
    return dict(mask=bits, accepted_pattern_indices=[i for i in range(10)
                if bits & (1 << i)], accepted_patterns=[list(p) for i, p in
                enumerate(PATTERNS) if bits & (1 << i)],
                accepted_ordered_rows=accepted, rejected_ordered_rows=rejected,
                representative_extensions=witnesses)


def contiguous_vertices(points):
    s = set(points)
    return len(s) <= 1 or len(s) == 5 or sum((v - 1) % 5 not in s for v in s) == 1


def contiguous_edges(edges):
    chosen = {i for i in FRAME if tuple(sorted((i, (i + 1) % 5))) in
              {tuple(e) for e in edges}}
    return contiguous_vertices(chosen)


def subset_of_frame_edge(points):
    return any(set(points) <= set(e) for e in FRAME_EDGES)


def analyse(vertices, edges, source_mask, singleton):
    g = graph(vertices, edges)
    inner = sorted(set(vertices) - set(FRAME))
    h = g.subgraph(inner)
    roots = sorted(v for v in inner if g.degree(v) >= 5)
    assert all(g.degree(v) >= 4 for v in inner)
    touched = sorted({b for v in inner for b in g[v] if b in FRAME})
    embedding = disk_embedding(vertices, edges)
    pieces = []
    comps = sorted((sorted(c) for c in nx.connected_components(
        h.subgraph(set(inner) - set(roots)))), key=tuple)
    for index, comp in enumerate(comps):
        root_nbrs = sorted({w for v in comp for w in g[v] if w in roots})
        others = sorted(set(inner) - set(comp))
        support = sorted({w for v in comp for w in g[v] if w in FRAME})
        one_sided = bool(others) and nx.is_connected(h.subgraph(others))
        # Literally follow the supplied unary iff one root definition.
        # Zero-root whole-H pieces are separately marked and never one-sided.
        kind = "unary" if len(root_nbrs) == 1 else "mixed"
        shield = piece_shield(embedding, comp) if one_sided else None
        pieces.append(dict(id=f"P{index}", vertices=comp,
                           degree_by_vertex=[[v, g.degree(v)] for v in comp],
                           kind=kind, rootless=not root_nbrs,
                           adjacent_roots=root_nbrs,
                           root_attachments=sorted([v, w] for v in comp
                                                   for w in g[v] if w in roots),
                           actual_support=support,
                           frame_attachments=sorted([v, w] for v in comp
                                                    for w in g[v] if w in FRAME),
                           other_interior_vertices=others, one_sided=one_sided,
                           support_contiguous=contiguous_vertices(support),
                           short_support=subset_of_frame_edge(support),
                           shield=shield))
    # Importantly: record violations; no assumed theorem filters the corpus.
    checks = []
    for p in pieces:
        if p["kind"] == "unary":
            checks.append(dict(property="unary_shield_ge2", piece=p["id"],
                               holds=p["one_sided"] and len(p["shield"]["shield_edges"]) >= 2))
        if p["one_sided"]:
            sh = p["shield"]["shield_edges"]
            checks.append(dict(property="shield_contiguous", piece=p["id"],
                               holds=contiguous_edges(sh)))
            checks.append(dict(property="support_contiguous", piece=p["id"],
                               holds=p["support_contiguous"]))
            if nx.is_connected(h) and len(touched) == 5 and len(p["actual_support"]) >= 2:
                checks.append(dict(property="lemma2_support_equals_shield_vertices",
                    piece=p["id"], holds=p["actual_support"] ==
                    sorted({v for e in sh for v in e})))
            rest_support = {b for v in p["other_interior_vertices"]
                            for b in g[v] if b in FRAME}
            gap = {tuple(e) for e in p["shield"]["frame_edges_on_rest_face"]}
            checks.append(dict(property="lemma1c_rest_support_outside_shield_interior",
                piece=p["id"], holds=not gap or rest_support <= {v for e in gap for v in e}))
    for p, q in combinations([p for p in pieces if p["one_sided"]], 2):
        a = {tuple(e) for e in p["shield"]["shield_edges"]}
        b = {tuple(e) for e in q["shield"]["shield_edges"]}
        checks.append(dict(property="shields_edge_disjoint", pieces=[p["id"], q["id"]],
                           holds=not a & b))
    unary_count = sum(p["kind"] == "unary" for p in pieces)
    checks.append(dict(property="at_most_two_unary", holds=unary_count <= 2))
    deletions = []
    for e in sorted(set(edges) - FRAME_EDGES):
        child = tuple(x for x in edges if x != e)
        child_bits = mask(vertices, child)
        gained = [i for i in range(10) if child_bits & (1 << i) and not source_mask & (1 << i)]
        assert gained and source_mask & child_bits == source_mask
        # Independent tuple enumeration and literal rows also replay the children.
        child_cert = sigma_certificate(vertices, child)
        deletions.append(dict(edge=list(e), sigma_after=child_bits,
            gained_pattern_indices=gained,
            gained_patterns=[list(PATTERNS[i]) for i in gained],
            gained_ordered_rows=[r for r in child_cert["accepted_ordered_rows"]
                                if not source_mask & (1 << PATTERNS.index(normalise(r)))],
            gained_extensions=[w for w in child_cert["representative_extensions"]
                               if w["pattern_index"] in gained]))
    q = sorted(singleton[i] for i in singleton if not source_mask & (1 << i))
    q_edges = [list(e) for e in sorted(FRAME_EDGES) if set(e) <= set(q)]
    q_components = len(list(nx.connected_components(graph(q, q_edges)))) if q else 0
    return dict(id=f"S{source_mask}", vertices=list(vertices), edges=[list(e) for e in edges],
        frame=list(FRAME), private_vertices=inner, roots=roots,
        degree_by_vertex=[[v, g.degree(v)] for v in inner],
        epsilon=sum(g.degree(v) - 4 for v in inner),
        interior_nonempty=bool(inner), interior_connected=bool(inner) and nx.is_connected(h),
        touched_frame_vertices=touched, Q=q, c_Q=q_components, e_Q=len(q_edges),
        embedding=embedding, sigma=sigma_certificate(vertices, edges),
        nonframe_edge_deletions=deletions, pieces=pieces,
        unary_count=unary_count, property_checks=checks)


def rejection_witnesses(record, piece):
    """Exact G-P colourings that fail to extend across the named short piece."""
    vertices = tuple(record["vertices"])
    edges = tuple(map(tuple, record["edges"]))
    pv = set(piece["vertices"])
    others = tuple(v for v in vertices if v not in pv)
    rest_edges = tuple(e for e in edges if not set(e) & pv)
    out = []
    for i, row in enumerate(PATTERNS):
        if record["sigma"]["mask"] & (1 << i):
            continue
        colourings = []
        for private in product(range(4), repeat=len(others) - 5):
            colours = dict(zip(others, row + private))
            if not all(colours[u] != colours[v] for u, v in rest_edges):
                continue
            extends = False
            for pc in product(range(4), repeat=len(pv)):
                whole = colours | dict(zip(sorted(pv), pc))
                if all(whole[u] != whole[v] for u, v in edges):
                    extends = True
                    break
            assert not extends
            root_colours = [colours[v] for v in piece["adjacent_roots"]]
            assert len(set(root_colours)) >= 2
            colourings.append(dict(colours_by_vertex=[[v, colours[v]] for v in others],
                                   adjacent_root_colours=root_colours))
        out.append(dict(pattern_index=i, boundary=list(row), witnesses=colourings))
    return out


def build():
    assert nx.__version__ == "3.5", "use .venv/bin/python or networkx==3.5"
    raw = SOURCE.read_bytes()
    data = json.loads(raw)
    assert data["pattern_order"] == [list(p) for p in PATTERNS]
    assert T4_INDICES == tuple(i for i, p in enumerate(PATTERNS) if len(set(p)) == 4)
    singleton = {int(i): v for i, v in data["singleton_of_three_colour"].items()}
    assert all(PATTERNS[i].count(PATTERNS[i][v]) == 1 for i, v in singleton.items())
    sources = sorted((int(k), cell) for k, cell in data["cells"].items()
                     if int(k) & T4_MASK == T4_MASK)
    trials, records = [], {}
    for bits, cell in sources:
        vertices = tuple(range(5 + cell["k_eff"]))
        initial = tuple(sorted(FRAME_EDGES | {tuple(sorted(e)) for e in cell["edges"]}))
        assert {e for e in initial if e[1] < 5} == FRAME_EDGES
        assert mask(vertices, initial) == bits
        for trial in range(ORDERS):
            order = sorted(set(initial) - FRAME_EDGES)
            if trial:
                random.Random(SEED + bits * ORDERS + trial).shuffle(order)
            current = initial
            removed = []
            deletion_masks = []
            for e in order:
                child = tuple(x for x in current if x != e)
                after = mask(vertices, child)
                deletion_masks.append(after)
                if after == bits:
                    current = child
                    removed.append(list(e))
            active = tuple(sorted(set(FRAME) | {v for e in current for v in e}))
            key = (active, current)
            if key not in records:
                records[key] = analyse(active, current, bits, singleton)
            record = records[key]
            trials.append(dict(source_cell=str(bits), trial=trial, final_graph=record["id"],
                removal_order=[list(e) for e in order], sigma_after_each_attempt=deletion_masks,
                removed_edges=removed, dropped_isolated_private_vertices=sorted(set(vertices) - set(active))))
    graphs = sorted(records.values(), key=lambda r: r["sigma"]["mask"])
    properties = Counter()
    failures = []
    piece_counts = Counter()
    shield_histogram = Counter()
    counterexamples = []
    for r in graphs:
        for c in r["property_checks"]:
            properties[c["property"]] += 1
            if not c["holds"]:
                failures.append(dict(graph=r["id"], **c))
        for p in r["pieces"]:
            subtype = "rootless" if p["rootless"] else p["kind"]
            piece_counts[subtype] += 1
            if p["one_sided"]:
                piece_counts[f"one_sided_{subtype}"] += 1
                shield_histogram[f"{subtype}_length_{len(p['shield']['shield_edges'])}"] += 1
            if p["kind"] == "mixed" and not p["rootless"] and p["one_sided"] and p["short_support"]:
                counterexamples.append(dict(graph=r["id"], piece=p["id"],
                    private_vertices=p["vertices"], actual_support=p["actual_support"],
                    shield_edges=p["shield"]["shield_edges"]))
    summary = dict(source_T4_full_cells=len(sources), nonfull_sigma_cells=sum(b != 1023 for b, _ in sources),
        greedy_trials=len(trials), distinct_labelled_final_graphs=len(graphs),
        trials_removing_an_edge=sum(bool(t["removed_edges"]) for t in trials),
        min_private_vertices=min(len(g["private_vertices"]) for g in graphs),
        max_private_vertices=max(len(g["private_vertices"]) for g in graphs),
        nonframe_critical_edges=sum(len(g["nonframe_edge_deletions"]) for g in graphs),
        pieces=sum(len(g["pieces"]) for g in graphs), piece_counts=dict(sorted(piece_counts.items())),
        shield_histogram=dict(sorted(shield_histogram.items())),
        graphs_by_unary_count=dict(sorted(Counter(str(g["unary_count"]) for g in graphs).items())),
        property_checks=dict(sorted(properties.items())), property_failures=failures,
        short_one_sided_mixed=len(counterexamples),
        counterexample_graphs=[c["graph"] for c in counterexamples],
        counterexample_sigma_patterns=graphs[0]["sigma"]["accepted_patterns"],
        fixed_933_941_S="unresolved", realizable_T4_generalisation="false")
    observations = dict(schema=1, task="S", base_commit="ca3870f9b79684c2100480d0dc04523899666928",
        source=str(SOURCE.relative_to(ROOT)), source_sha256=sha256(raw).hexdigest(),
        scope="Saved labelled witnesses only; not all graphs with <=5 private vertices, nor arbitrary size.",
        networkx_version=nx.__version__, seed=SEED, orders_per_source=ORDERS,
        frame=list(FRAME), pattern_order=[list(p) for p in PATTERNS],
        singleton_of_three_colour=data["singleton_of_three_colour"],
        T4_indices=list(T4_INDICES), T4_mask=T4_MASK, boundary_rows=[list(b) for b in BOUNDARY],
        summary=summary, counterexamples=counterexamples, graphs=graphs, greedy_trials=trials)
    example = next(g for g in graphs if g["id"] == "S935")
    piece = next(p for p in example["pieces"] if p["one_sided"] and p["short_support"])
    return {"observations.json": observations,
            "counterexample_S935.json": dict(graph=example, short_piece=piece["id"],
                rejected_pattern_G_minus_P_witnesses=rejection_witnesses(example, piece),
                conclusion="Refutes the realizable T4-full generalisation, not fixed Sigma=933/941 S.")}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="read-only exact byte replay")
    args = parser.parse_args()
    result = build()
    payloads = {name: (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()
                for name, value in result.items()}
    if args.check:
        for name, payload in payloads.items():
            assert (OUT / name).read_bytes() == payload, f"certificate differs: {OUT / name}"
    else:
        # Generation is intentionally no-clobber, including the task's own artifacts.
        assert not any((OUT / name).exists() for name in payloads), "use --check; refuses to overwrite"
        OUT.mkdir(parents=True, exist_ok=True)
        for name, payload in payloads.items():
            (OUT / name).write_bytes(payload)
    print(json.dumps(result["observations.json"]["summary"], sort_keys=True))


if __name__ == "__main__":
    main()
