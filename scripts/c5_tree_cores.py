#!/usr/bin/env python3
"""Finite minors for arbitrary degree-four tree cores, plus one cyclic control.

uv run --with networkx==3.5 python scripts/c5_tree_cores.py [--check]
No enumeration of general five/six-interior graphs; no Lean theorem.
"""
import argparse
from collections import Counter
from itertools import combinations, permutations, product
import json
from pathlib import Path

import networkx as nx

from c5_cell_enumerator import REPS, T4
from c5_disk_deletions import BOUNDARY, CYCLE, faces_of, relation, sha
from c5_odd_join_cores import kuratowski_certificate
from local_closure import direct_graph_extend

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_tree_cores/observations.json'
PREVIOUS = ROOT / 'artifacts/c5_odd_join_cores/observations.json'
Q = (0, 1, 0, 1, 2)
QI = REPS.index(Q)


def options(colors):
    return list(product(*[[i for i, c in enumerate(Q) if c == f] for f in colors]))


def lifted_edges(inner, neighborhoods):
    return tuple(sorted(set(CYCLE) | {(u+5, v+5) for u, v in inner}
                        | {(b, v+5) for v, ns in enumerate(neighborhoods) for b in ns}))


def disk_check(n, edges):
    graph = nx.Graph(edges)
    graph.add_edges_from((n, b) for b in range(5))
    disk, embedding = nx.check_planarity(graph)
    if not disk:
        return False, kuratowski_certificate(graph)
    rotation = [list(embedding.neighbors_cw_order(v)) for v in range(n+1)]
    assert n + 1 - graph.number_of_edges() + len(faces_of(rotation)) == 2
    return True, dict(apex_rotation=rotation)


def exact_core(n, edges, require_degree_four=True):
    sigma, full = relation(n, edges)
    assert not (sigma >> QI & 1)
    degrees = [sum(v in e for e in edges) for v in range(5, n)]
    assert min(degrees) >= 4
    if require_degree_four:
        assert set(degrees) == {4}
    deletions = []
    for edge in sorted(set(edges) - CYCLE):
        child = tuple(e for e in edges if e != edge)
        assert direct_graph_extend(n, child, Q)
        deletions.append(edge)
    return dict(sigma=sigma, full_relation=full, critical_edges=deletions,
                interior_degrees=degrees)


def branch_minors():
    inner = [(0, 1), (0, 2), (2, 3), (0, 4), (4, 5)]
    rows = []
    for a, b in combinations(range(3), 2):
        lists = [{3, a, b}, {3}, {3, a}, {3}, {3, b}, {3}]
        for ns in product(*(options(c for c in range(3) if c not in ls) for ls in lists)):
            edges = lifted_edges(inner, ns)
            disk, certificate = disk_check(11, edges)
            assert not disk
            rows.append(dict(palettes=[a, b], neighborhoods=ns, edges=edges,
                             obstruction=certificate))
    assert len(rows) == 2304
    # One full coloring/minimality check per palette assignment; attachment
    # choices do not change the Q lists, so all lifts share this property.
    checked = []
    for palettes in combinations(range(3), 2):
        row = next(r for r in rows if tuple(r['palettes']) == palettes)
        checked.append(dict(palettes=palettes, **exact_core(11, row['edges'])))
    return dict(templates=rows, representative_criticality=checked)


def path_lifts(word):
    palette_order = sorted(set(word))
    allowed = [options(c for c in range(3) if c != a) for a in palette_order]
    for assigned in product(*allowed):
        mapping = dict(zip(palette_order, assigned))
        for left, right in product(options(range(3)), repeat=2):
            ns = [left] + [mapping[a] for a in word for _ in range(2)] + [right]
            edges = lifted_edges([(v, v+1) for v in range(len(ns)-1)], ns)
            yield ns, edges


def path_minors():
    rows, counts, survivors = [], Counter(), []
    words = list(permutations(range(3), 2)) + [(0, 1, 0), (1, 0, 1)]
    for word in words:
        key = ''.join(map(str, word))
        for ns, edges in path_lifts(word):
            n = len(ns) + 5
            disk, certificate = disk_check(n, edges)
            counts[f'{key}_templates'] += 1
            row = dict(word=word, neighborhoods=ns, edges=edges,
                       disk=disk, topology=certificate)
            if disk:
                assert word in ((0, 1), (1, 0))
                row.update(exact_core(n, edges))
                assert row['sigma'] == 1023 ^ (1 << QI)
                counts[f'{key}_disk_single_missing'] += 1
                survivors.append(row)
            rows.append(row)
    assert len(rows) == 768 and len(survivors) == 2
    # Expand both runs independently; full 240-row comparison checks the
    # local transfer in a different-palette context, not just odd-join paths.
    long_rows = []
    for base in survivors:
        faces = faces_of(base['topology']['apex_rotation'])
        for offset in (1, 3):
            u, v = 5 + offset, 6 + offset
            assert all(any(len(face) == 3 and set(face) == {u, v, b} for face in faces)
                       for b in base['neighborhoods'][offset])
        for first, second in ((1, 2), (2, 1), (2, 3), (4, 3)):
            a, b = base['word']
            ns = ([base['neighborhoods'][0]] + [base['neighborhoods'][1]]*(2*first)
                  + [base['neighborhoods'][3]]*(2*second) + [base['neighborhoods'][-1]])
            edges = lifted_edges([(v, v+1) for v in range(len(ns)-1)], ns)
            n = 5 + len(ns)
            disk, topology = disk_check(n, edges)
            assert disk
            full = format(sum(int(direct_graph_extend(n, edges, boundary)) << j
                              for j, boundary in enumerate(BOUNDARY)), '060x')
            assert full == base['full_relation']
            long_rows.append(dict(word=[a]*first + [b]*second, edges=edges,
                                  full_relation=full, topology=topology))
    return dict(templates=rows, counts=dict(sorted(counts.items())), long_lifts=long_rows)


def cyclic_probe():
    # Two K4-minus-edge pieces identify vertex 0; connect 1 to 4, then add hub 7.
    edges = (set(combinations(range(4), 2)) | set(combinations((0, 4, 5, 6), 2)))
    edges -= {(0, 1), (0, 4)}
    edges.add((1, 4))
    edges |= {(v, 7) for v in range(7)}
    graph = nx.Graph(sorted(edges))
    autos = list(nx.algorithms.isomorphism.GraphMatcher(graph, graph).isomorphisms_iter())
    triangles = [t for t in permutations(range(8), 3)
                 if all(graph.has_edge(u, v) for u, v in combinations(t, 2))]
    representatives = sorted({min(tuple(p[v] for v in t) for p in autos) for t in triangles})
    counts, rows, enumeration = Counter(), [], []
    for triangle in representatives:
        inner = sorted(set(graph) - set(triangle))
        labels = {v: 5+i for i, v in enumerate(inner)}
        fixed, slots = set(CYCLE), []
        for u, v in sorted(edges):
            if u in triangle and v in triangle:
                continue
            if u in labels and v in labels:
                fixed.add(tuple(sorted((labels[u], labels[v]))))
            else:
                b, w = (u, v) if u in triangle else (v, u)
                slots.append([(i, labels[w]) for i, c in enumerate(Q) if c == triangle.index(b)])
        for choice in product(*slots):
            lift = tuple(sorted(fixed | set(choice)))
            apex = nx.Graph(lift)
            apex.add_edges_from((10, b) for b in range(5))
            disk, embedding = nx.check_planarity(apex)
            counts['templates'] += 1
            enumeration.append([triangle, format(sum(1 << (u*10+v) for u, v in lift), 'x'), disk])
            if not disk:
                continue
            counts['disk'] += 1
            row = dict(triangle=triangle, edges=lift,
                       **exact_core(10, lift, require_degree_four=False))
            row['apex_rotation'] = [list(embedding.neighbors_cw_order(v)) for v in range(11)]
            assert 11 - apex.number_of_edges() + len(faces_of(row['apex_rotation'])) == 2
            if row['sigma'] & T4 == T4:
                assert row['sigma'] == 1023 ^ (1 << QI)
                counts['disk_T4_single_missing'] += 1
            rows.append(row)
    assert len(autos) == 8 and len(triangles) == 90 and len(representatives) == 24
    assert counts == dict(templates=2048, disk=48, disk_T4_single_missing=32)
    counts['disk_all_degree_four'] = sum(set(r['interior_degrees']) == {4} for r in rows)
    counts['disk_T4_all_degree_four'] = sum(set(r['interior_degrees']) == {4}
                                         and r['sigma'] & T4 == T4 for r in rows)
    return dict(quotient_edges=sorted(edges), automorphisms=autos,
                ordered_triangles=triangles, triangle_orbit_representatives=representatives,
                enumeration=enumeration, disk_templates=rows, counts=dict(counts))


def build():
    previous = json.loads(PREVIOUS.read_text())
    for name, expected in previous['source_sha256'].items():
        assert sha(ROOT / name) == expected, name
    five = next(case for case in previous['cases'] if case['length'] == 5)
    assert len(five['required_minor_obstructions']) == 256
    branches, paths, cyclic = branch_minors(), path_minors(), cyclic_probe()
    dependencies = [Path(__file__).resolve()] + [ROOT / 'scripts' / f'{name}.py' for name in
                    ('c5_odd_join_cores', 'c5_cell_enumerator', 'c5_disk_deletions',
                     'local_closure', 'boundary_relations')]
    return dict(schema=1,
                scope='Finite minor certificates for the paper reduction of arbitrary degree-four tree cores; one separate eight-vertex cyclic quotient probe.',
                fixed_pattern=Q, pattern_order=REPS,
                inputs={str(PREVIOUS.relative_to(ROOT)): sha(PREVIOUS)},
                source_sha256={str(p.relative_to(ROOT)): sha(p) for p in dependencies},
                branch_minors=branches, path_minors=paths, cyclic_probe=cyclic,
                summary=dict(Y_templates=2304, Y_disk=0,
                             reused_same_palette_obstructions=256,
                             two_palette_templates=640, two_palette_disk_single_missing=2,
                             returning_palette_templates=128, returning_palette_disk=0,
                             longer_two_run_lifts=8, cyclic_probe=cyclic['counts']))


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
