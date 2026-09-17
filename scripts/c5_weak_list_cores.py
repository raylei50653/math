#!/usr/bin/env python3
"""List-critical core diagnostics and 22 local disk vertex splits.

uv run --with networkx==3.5 python scripts/c5_weak_list_cores.py [--check]
This is not a k=4 enumeration or a proof of the general exit conjecture.
"""
import argparse
from collections import Counter
from itertools import combinations, combinations_with_replacement, permutations, product
import json
from pathlib import Path

import networkx as nx

from c5_cell_enumerator import REPS, T4, compat_tables
from c5_disk_deletions import CYCLE, relation, sha
from c5_disk_weak_successors import members

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / 'artifacts/c5_weak_critical_cores/observations.json'
FLOW = ROOT / 'artifacts/c5_weak_flow_repairs/observations.json'
OUT = ROOT / 'artifacts/c5_weak_list_cores/observations.json'


def profile(edges, pattern):
    graph = nx.Graph(edges)
    inner = sorted(v for v in graph if v >= 5)
    h = graph.subgraph(inner)
    assert nx.is_connected(h)
    rows = []
    for v in inner:
        boundary = sorted(u for u in graph[v] if u < 5)
        colors = [REPS[pattern][u] for u in boundary]
        assert len(colors) == len(set(colors))
        assert graph.degree(v) >= 4
        lists = sorted(set(range(4)) - set(colors))
        rows.append(dict(vertex=v, boundary_neighbors=boundary, colors=lists,
                         degree=graph.degree(v), interior_degree=h.degree(v)))
    assert all(r['degree'] == 4 for r in rows)
    assert all(len(r['colors']) == r['interior_degree'] for r in rows)
    assert all(r['colors'] == rows[0]['colors'] for r in rows)
    assert h.number_of_edges() == len(inner) * (len(inner) - 1) // 2
    return dict(pattern=pattern, edges=edges, lists=rows,
                mechanism='edge_one_color' if len(inner) == 2 else 'triangle_two_colors')


def local_exits(run):
    edges, sigma = run['edges'], run['sigma_by_mask']
    root = len(sigma) - 1
    p, q = [REPS[c['pattern']] for c in run['cores']]
    alignments = []
    for perm in permutations(range(4)):
        renamed = tuple(perm[c] for c in q)
        diff = [i for i in range(5) if p[i] != renamed[i]]
        if len(diff) == 1:
            alignments.append(dict(first=p, second=renamed, pivot=diff[0]))
    assert len(alignments) == 1
    stars = []
    for v in range(5):
        allowed = sum(1 << i for i, e in enumerate(edges) if v in e)
        exits = sorted({sigma[m ^ (1 << i)] for m in range(root + 1)
                        if not (root ^ m) & ~allowed and sigma[m] == sigma[root]
                        for i in members(m & allowed)
                        if sigma[m ^ (1 << i)] != sigma[root]})
        stars.append(dict(vertex=v, edges=[edges[i] for i in members(allowed)], exits=exits))
    assert stars[alignments[0]['pivot']]['exits'] == [1023]
    return dict(sigma=sigma[root], alignment=alignments[0], boundary_stars=stars)


def subset_table(edges, k):
    size = 1 << len(edges)
    sigma = [0] * size
    tables, full = compat_tables(k, edges)
    for j, boundary in enumerate(REPS):
        exists = bytearray(size)
        for inner in product(range(4), repeat=k):
            c = boundary + inner
            exists[sum(1 << i for i, (u, v) in enumerate(edges) if c[u] != c[v])] = 1
        for i in range(len(edges)):
            bit = 1 << i
            for m in range(size):
                if not m & bit:
                    exists[m] |= exists[m | bit]
        viable = [full] * size
        for m in range(1, size):
            bit = m & -m
            viable[m] = viable[m ^ bit] & tables[bit.bit_length() - 1][j]
        for m in range(size):
            assert bool(viable[m]) == bool(exists[m])
            sigma[m] |= int(exists[m]) << j
    return sigma


def small_core_templates():
    """Complete templates from the paper classification for <=3 active interiors.

    Quotient interior permutations only; keep boundary labels fixed.
    """
    rows = []
    for p, boundary in enumerate(REPS):
        if len(set(boundary)) != 3:
            continue
        types = [('edge', 2, [ns for ns in combinations(range(5), 3)
                             if len({boundary[t] for t in ns}) == 3])]
        for palette in combinations(sorted(set(boundary)), 2):
            types.append(('triangle', 3, [ns for ns in combinations(range(5), 2)
                                         if {boundary[t] for t in ns} == set(palette)]))
        for kind, n, options in types:
            for neighborhoods in combinations_with_replacement(options, n):
                edges = (set(CYCLE) | set(combinations(range(5, 5+n), 2))
                         | {(t, 5+i) for i, ns in enumerate(neighborhoods) for t in ns})
                sigma, full = relation(5+n, tuple(sorted(edges)))
                assert not sigma >> p & 1
                for e in edges - CYCLE:
                    assert relation(5+n, tuple(sorted(edges - {e})))[0] >> p & 1
                graph = nx.Graph(sorted(edges))
                graph.add_edges_from((5+n, t) for t in range(5))
                disk = nx.check_planarity(graph)[0]
                t4 = sigma & T4 == T4
                if disk and t4:
                    assert sigma == 1023 ^ (1 << p)
                rows.append(dict(pattern=p, kind=kind, neighborhoods=neighborhoods,
                                 edges=sorted(edges - CYCLE), sigma=sigma, full_relation=full,
                                 boundary_apex_planar=disk, accepts_T4=t4))
    assert len(rows) == 190
    assert sum(r['boundary_apex_planar'] for r in rows) == 35
    assert sum(r['boundary_apex_planar'] and r['accepts_T4'] for r in rows) == 25
    return rows


def split_probe(run):
    base = CYCLE | set(map(tuple, run['edges']))
    graph = nx.Graph(sorted(base))
    graph.add_edges_from((8, i) for i in range(5))
    planar, embedding = nx.check_planarity(graph)
    assert planar
    rows = []
    for v in range(5, 8):
        ring = list(embedding.neighbors_cw_order(v))
        for i in range(len(ring)):
            for j in range(i + 1, len(ring)):
                first, second = ring[i:j+1], ring[j:] + ring[:i+1]
                edges = ({e for e in base if v not in e}
                         | {tuple(sorted((v, t))) for t in first}
                         | {tuple(sorted((8, t))) for t in second} | {(v, 8)})
                extra = sorted(edges - CYCLE)
                candidate = nx.Graph(sorted(edges))
                candidate.add_edges_from((9, t) for t in range(5))
                assert nx.check_planarity(candidate)[0]
                sigma, full = relation(9, tuple(sorted(edges)))
                row = dict(vertex=v, first_arc=first, second_arc=second, edges=extra,
                           sigma=sigma, full_relation=full, boundary_apex_planar=True)
                if sigma == run['sigma']:
                    table = subset_table(extra, 4)
                    assert table[-1] == sigma
                    cores = []
                    for old in run['cores']:
                        p = old['pattern']
                        masks = [m for m in range(len(table)) if not table[m] >> p & 1
                                 and all(table[m ^ (1 << t)] >> p & 1 for t in members(m))]
                        assert len(masks) == 1
                        core_edges = [extra[t] for t in members(masks[0])]
                        cores.append(profile(core_edges, p))
                    # Every preserved case merely adds a degree-three vertex.
                    plain = nx.Graph(sorted(edges))
                    removable = [u for u in (v, 8) if plain.degree(u) == 3]
                    assert removable
                    restored = False
                    for u in removable:
                        kept = {e for e in edges if u not in e}
                        if u == v:
                            kept = {tuple(sorted(v if x == 8 else x for x in e)) for e in kept}
                        restored |= kept == base
                    assert restored
                    row.update(subsets_checked=len(table), silent_states=table.count(sigma),
                               cores=cores, degree_three_decoration=True)
                rows.append(row)
    assert len(rows) == 22
    assert sum(r['sigma'] == run['sigma'] for r in rows) == 13
    return rows


def build():
    source, flow = [json.loads(p.read_text()) for p in (INPUT, FLOW)]
    for data in (source, flow):
        for name, expected in (data['inputs'] | data['source_sha256']).items():
            assert sha(ROOT / name) == expected, name
    profiles = [profile(c['edges'], c['pattern']) for r in source['runs'] for c in r['cores']]
    control = flow['noncofacial_control']
    for field in ('first_gadget_edges', 'second_gadget_edges'):
        edges = control[field]
        sigma = relation(9, tuple(sorted(CYCLE | set(map(tuple, edges)))))[0]
        p, = [j for j in range(10) if not sigma >> j & 1]
        for i in range(len(edges)):
            child = tuple(sorted(CYCLE | set(map(tuple, edges[:i] + edges[i+1:]))))
            assert relation(9, child)[0] == 1023
        profiles.append(profile(edges, p))
    splits = split_probe(source['runs'][0])
    templates = small_core_templates()
    # Hall's condition specialized to the source triangle, checked on all 240 rows.
    base = CYCLE | set(map(tuple, source['runs'][0]['edges']))
    from local_closure import direct_graph_extend
    hall_rows = 0
    for b in product(range(4), repeat=5):
        if any(b[u] == b[v] for u, v in CYCLE):
            continue
        forbidden = b[2] == b[4] and b[3] in (b[0], b[1])
        assert direct_graph_extend(8, tuple(sorted(base)), b) == (not forbidden)
        hall_rows += 1
    assert hall_rows == 240
    dependencies = [Path(__file__).resolve()] + [ROOT / 'scripts' / f'{name}.py' for name in
                    ('c5_cell_enumerator', 'c5_disk_deletions', 'c5_disk_weak_successors',
                     'local_closure', 'boundary_relations')]
    return dict(schema=1, scope='Existing cores and 22 local splits of one disk representative only.',
                inputs={str(p.relative_to(ROOT)): sha(p) for p in (INPUT, FLOW)},
                source_sha256={str(p.relative_to(ROOT)): sha(p) for p in dependencies},
                core_profiles=profiles, local_exits=[local_exits(r) for r in source['runs']],
                split_probe=splits, small_core_templates=templates,
                summary=dict(old_triangle_cores=10, control_edge_cores=2,
                             pivot_star_only_common_exit=5, hall_boundary_rows=hall_rows,
                             local_splits=len(splits), preserved_relation=13,
                             preserved_nontrivial_cores=0,
                             small_core_templates=len(templates), small_disk_templates=35,
                             small_disk_T4_templates=25, small_core_single_missing_failures=0,
                             preserved_subset_checks=sum(r.get('subsets_checked', 0) for r in splits),
                             split_relation_counts=dict(sorted(Counter(r['sigma'] for r in splits).items()))))


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
