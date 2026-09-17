#!/usr/bin/env python3
"""Exhaust four-active-interior minimal singleton cores using list constraints.

uv run --with networkx==3.5 python scripts/c5_four_vertex_cores.py [--check]
No all-graph k=4 enumeration and no general weak-exit theorem.
"""
import argparse
from collections import Counter
from functools import reduce
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

import networkx as nx

from c5_cell_enumerator import REPS, T4
from c5_disk_deletions import CYCLE, faces_of, relation, sha

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_four_vertex_cores/observations.json'
VERTICES = tuple(range(4))
PAIRS = tuple(combinations(VERTICES, 2))
ASSIGNMENTS = tuple(product(range(4), repeat=4))
FULL = (1 << len(ASSIGNMENTS)) - 1
VERTEX_MASKS = [[sum(1 << i for i, c in enumerate(ASSIGNMENTS) if s >> c[v] & 1)
                 for s in range(16)] for v in VERTICES]


def meet(values):
    return reduce(int.__and__, values, FULL)


def graph_shapes():
    shapes = {}
    for mask in range(64):
        edges = [e for i, e in enumerate(PAIRS) if mask >> i & 1]
        graph = nx.Graph()
        graph.add_nodes_from(VERTICES)
        graph.add_edges_from(edges)
        if not nx.is_connected(graph):
            continue
        canonical = min(sum(1 << PAIRS.index(tuple(sorted((p[u], p[v])))) for u, v in edges)
                        for p in permutations(VERTICES))
        shapes.setdefault(canonical, []).append(mask)
    assert len(shapes) == 6 and sum(map(len, shapes.values())) == 38
    return shapes


def list_colorable(edges, lists):
    return any(all(lists[v] >> c[v] & 1 for v in VERTICES)
               and all(c[u] != c[v] for u, v in edges) for c in ASSIGNMENTS)


def critical_lists(edges):
    degrees = [sum(v in e for e in edges) for v in VERTICES]
    allowed = [[s for s in range(8, 16) if s.bit_count() <= d] for d in degrees]
    edge_masks = [sum(1 << i for i, c in enumerate(ASSIGNMENTS) if c[u] != c[v])
                  for u, v in edges]
    proper = meet(edge_masks)
    rejected = Counter()
    rows = []
    for lists in product(*allowed):
        vertices = [VERTEX_MASKS[v][lists[v]] for v in VERTICES]
        if proper & meet(vertices):
            rejected['colorable'] += 1
            continue
        if any(not (meet(vertices) & meet(edge_masks[:i] + edge_masks[i+1:]))
               for i in range(len(edges))):
            rejected['nonminimal_internal_edge'] += 1
            continue
        if any(not (proper & VERTEX_MASKS[v][lists[v] | (1 << c)]
                    & meet(vertices[:v] + vertices[v+1:]))
               for v in VERTICES for c in range(3) if not lists[v] >> c & 1):
            rejected['nonminimal_spoke_color'] += 1
            continue
        # Independently validate each retained abstract assignment by tuple search.
        assert not list_colorable(edges, lists)
        for i in range(len(edges)):
            assert list_colorable(edges[:i] + edges[i+1:], lists)
        for v in VERTICES:
            for c in range(3):
                if not lists[v] >> c & 1:
                    relaxed = list(lists)
                    relaxed[v] |= 1 << c
                    assert list_colorable(edges, relaxed)
        rows.append(dict(lists=lists, total_degrees=[degrees[v]+4-lists[v].bit_count()
                                                   for v in VERTICES]))
    return rows, dict(sorted(rejected.items()))


def quotient_witness(edges, neighborhoods, boundary):
    # Equal-color boundary identification, NOT a planar contraction claim.
    q = nx.Graph()
    q.add_nodes_from(range(7))
    q.add_edges_from(combinations(range(4, 7), 2))
    q.add_edges_from(edges)
    q.add_edges_from((v, 4+boundary[b]) for v, ns in enumerate(neighborhoods) for b in ns)
    hubs = sorted(v for v in q if q.degree(v) == 6)
    assert len(hubs) == 2 and q.has_edge(*hubs)
    cycle = q.subgraph(set(q) - set(hubs))
    assert nx.is_connected(cycle) and all(d == 2 for _, d in cycle.degree())
    return dict(universal_vertices=hubs, cycle_edges=sorted(map(sorted, cycle.edges())),
                quotient_edges=sorted(map(sorted, q.edges())))


def stretch_family(disk_rows):
    selected = None
    for row in disk_rows:
        if not row['accepts_T4'] or row['shape'] != 13:
            continue
        edges = CYCLE | set(map(tuple, row['edges']))
        faces = faces_of(row['apex_rotation'])
        for u, v in sorted(edges):
            if u < 5 or v < 5:
                continue
            first, second = map(set, (row['neighborhoods'][u-5], row['neighborhoods'][v-5]))
            if first != second or len(first) != 2:
                continue
            a, b = sorted(first)
            if all(any(len(f) == 3 and set(f) == {u, v, t} for f in faces) for t in (a, b)):
                selected = row, edges, u, v, a, b
                break
        if selected:
            break
    assert selected is not None
    row, edges, u, v, a, b = selected
    boundary = REPS[row['pattern']]
    assert boundary[a] != boundary[b]
    # Include unrestricted endpoint colors to validate the lifting step when
    # an old endpoint spoke was deleted in a minimality witness.
    local_rows = []
    for ca, cb, cu, cv in product(range(4), repeat=4):
        exists = any(cs not in (ca, cb) and ct not in (ca, cb)
                     and cu != cs and cs != ct and ct != cv
                     for cs, ct in product(range(4), repeat=2))
        available = set(range(4)) - {ca, cb}
        assert exists == (ca == cb or not (cu == cv and cu in available))
        local_rows.append([ca, cb, cu, cv, exists])
    patch = {tuple(sorted(e)) for e in [(u, 9), (9, 10), (10, v),
                                      (a, 9), (a, 10), (b, 9), (b, 10)]}
    expanded = (edges - {(u, v)}) | patch
    sigma, full = relation(11, tuple(sorted(expanded)))
    assert sigma == row['sigma']
    child_rows = []
    for e in sorted(expanded - CYCLE):
        child_sigma, child_full = relation(11, tuple(sorted(expanded - {e})))
        assert child_sigma == 1023
        child_rows.append(dict(deleted=e, sigma=child_sigma, full_relation=child_full))
    graph = nx.Graph(sorted(expanded))
    graph.add_edges_from((11, i) for i in range(5))
    planar, embedding = nx.check_planarity(graph)
    assert planar
    rotation = [list(embedding.neighbors_cw_order(i)) for i in range(12)]
    faces = faces_of(rotation)
    assert all(any(len(f) == 3 and set(f) == {9, 10, t} for f in faces) for t in (a, b))
    return dict(pattern=row['pattern'], base_edges=row['edges'], stretched_edge=[u, v],
                boundary_hubs=[a, b], local_patch_rows=local_rows,
                six_interior_edges=sorted(expanded - CYCLE), sigma=sigma,
                full_relation=full, one_edge_deletions=child_rows, apex_rotation=rotation,
                next_stretch_edge=[9, 10],
                general_family_status='Paper induction using the local patch; computed instances have four and six active interiors.')


def build():
    shapes, disk_rows, counts = [], [], Counter()
    digest = sha256()
    for mask, labeled_masks in sorted(graph_shapes().items()):
        edges = [e for i, e in enumerate(PAIRS) if mask >> i & 1]
        lists, rejected = critical_lists(edges)
        shape_counts = Counter()
        for row in lists:
            for p, boundary in enumerate(REPS):
                if len(set(boundary)) != 3:
                    continue
                choices = [list(product(*[[b for b in range(5) if boundary[b] == c]
                                          for c in range(3) if not row['lists'][v] >> c & 1]))
                           for v in VERTICES]
                for neighborhoods in product(*choices):
                    graph_edges = (set(CYCLE) | {(u+5, v+5) for u, v in edges}
                                   | {(b, v+5) for v in VERTICES for b in neighborhoods[v]})
                    counts['templates'] += 1
                    shape_counts['templates'] += 1
                    graph = nx.Graph(sorted(graph_edges))
                    graph.add_edges_from((9, b) for b in range(5))
                    planar, embedding = nx.check_planarity(graph)
                    digest.update(json.dumps([mask, row['lists'], p, neighborhoods, planar],
                                             separators=(',', ':')).encode() + b'\n')
                    if not planar:
                        continue
                    counts['disk'] += 1
                    shape_counts['disk'] += 1
                    sigma, full_relation = relation(9, tuple(sorted(graph_edges)))
                    assert not sigma >> p & 1
                    # Full boundary-row replay on every one-edge child as well.
                    for e in graph_edges - CYCLE:
                        assert relation(9, tuple(sorted(graph_edges - {e})))[0] >> p & 1
                    accepts_t4 = sigma & T4 == T4
                    if accepts_t4:
                        counts['disk_T4'] += 1
                        shape_counts['disk_T4'] += 1
                        assert sigma == 1023 ^ (1 << p)
                        quotient = quotient_witness(edges, neighborhoods, boundary)
                    else:
                        quotient = None
                    disk_rows.append(dict(shape=mask, pattern=p, lists=row['lists'],
                                          total_degrees=row['total_degrees'],
                                          neighborhoods=neighborhoods,
                                          edges=sorted(graph_edges - CYCLE), sigma=sigma,
                                          full_relation=full_relation, accepts_T4=accepts_t4,
                                          apex_rotation=[list(embedding.neighbors_cw_order(v))
                                                         for v in range(10)],
                                          join_quotient=quotient))
        shapes.append(dict(mask=mask, edges=edges, labeled_masks=labeled_masks,
                           critical_lists=lists, rejected_list_counts=rejected,
                           template_counts=dict(sorted(shape_counts.items()))))
    assert counts == dict(templates=4965, disk=200, disk_T4=100)
    assert [len(s['critical_lists']) for s in shapes] == [0, 3, 0, 0, 12, 3]
    by_mask = {s['mask']: s['template_counts'] for s in shapes}
    assert by_mask[13]['disk_T4'] == 20 and by_mask[31]['disk_T4'] == 80
    assert by_mask[63].get('disk', 0) == 0
    family = stretch_family(disk_rows)
    dependencies = [Path(__file__).resolve()] + [ROOT / 'scripts' / f'{name}.py' for name in
                    ('c5_cell_enumerator', 'c5_disk_deletions', 'local_closure', 'boundary_relations')]
    return dict(schema=1,
                scope='All minimal singleton obstructions with exactly four active interior vertices, under the documented chord-free and distinct-spoke-color reduction.',
                source_sha256={str(p.relative_to(ROOT)): sha(p) for p in dependencies},
                pattern_order=REPS, shapes=shapes, enumeration_sha256=digest.hexdigest(),
                disk_templates=disk_rows, odd_path_family=family,
                summary=dict(connected_labeled_shapes=38, unlabeled_shapes=6,
                             minimal_list_assignments=18, **dict(counts),
                             disk_T4_path=20, disk_T4_diamond=80, disk_K4=0,
                             single_missing_failures=0, join_K2_C5_witnesses=100,
                             stretch_verified_interiors=[4, 6], stretch_strict_deletions=19))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    data = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == data, 'artifact differs; rebuild explicitly'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__':
    main()
