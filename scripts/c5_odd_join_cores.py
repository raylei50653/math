#!/usr/bin/env python3
"""Finite minor tests and path transfer for arbitrary odd-join singleton cores.

uv run --with networkx==3.5 python scripts/c5_odd_join_cores.py [--check]
The arbitrary-length reduction is a paper proof, not a Lean theorem.
"""
import argparse
from collections import Counter
from itertools import permutations, product
import json
from pathlib import Path

import networkx as nx

from c5_cell_enumerator import REPS, T4
from c5_disk_deletions import BOUNDARY, CYCLE, faces_of, relation, sha
from local_closure import direct_graph_extend

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_odd_join_cores/observations.json'
Q = (0, 1, 0, 1, 2)
QI = REPS.index(Q)


def templates(length):
    """All minimal lifts of a boundary triangle in K2 join C_length.

    Fix Q; quotient automorphisms exchange hubs and reverse the cycle.
    Every spoke chooses exactly one vertex of its Q color class.
    The even length 6 is a topology control, not an obstruction claim.
    """
    cycle = range(2, length + 2)
    qe = {(0, 1)} | {(h, v) for h in (0, 1) for v in cycle}
    qe |= {tuple(sorted((v, 2 + (v - 1) % length))) for v in cycle}
    types = [('I', (0, 1, 2)), ('II', (0, 2, 3))]
    if length == 3:  # K5: all boundary triangles equivalent.
        types = [('K5', (0, 1, 2))]
    for kind, triangle in types:
        for colors in permutations(range(3)):
            if kind == 'K5' and colors != (0, 1, 2):
                continue
            if kind == 'I' and colors[0] > colors[1]:
                continue
            if kind == 'II' and colors[1] > colors[2]:
                continue
            boundary_colors = dict(zip(triangle, colors))
            inner = sorted(set(range(length + 2)) - set(triangle))
            labels = {v: 5 + i for i, v in enumerate(inner)}
            fixed, slots = set(CYCLE), []
            for u, v in sorted(qe):
                if u in boundary_colors and v in boundary_colors:
                    continue
                if u in labels and v in labels:
                    fixed.add(tuple(sorted((labels[u], labels[v]))))
                else:
                    b, w = (u, v) if u in boundary_colors else (v, u)
                    slots.append([(i, labels[w]) for i, c in enumerate(Q)
                                  if c == boundary_colors[b]])
            for choices in product(*slots):
                edges = tuple(sorted(fixed | set(choices)))
                path = list(range(5 if kind != 'II' else 6, length + 4))
                neighborhoods = [tuple(b for b in range(5) if (b, v) in edges)
                                 for v in path[1:-1]]
                yield dict(kind=kind, triangle_colors=colors, edges=edges,
                           path=path, middle_neighborhoods=neighborhoods)


def transfer_rows():
    """Exact Boolean transfer: R_(r+2)=R_r for every r>=1, |S|>=2.

    More directly, a walk on K_S has M^(t+2)=M^t for t>=2;
    endpoint-to-list transfer also stabilizes at r=1 (odd), r=2 (even).
    Check the base equalities and retain the ordinary associative induction.
    """
    def compose(a, b):
        return tuple(tuple(any(a[i][k] and b[k][j] for k in range(4))
                           for j in range(4)) for i in range(4))

    rows = []
    for mask in range(16):
        if mask.bit_count() < 2:
            continue
        allowed = {c for c in range(4) if mask >> c & 1}
        matrix = tuple(tuple(i in allowed and j in allowed and i != j
                             for j in range(4)) for i in range(4))
        square = compose(matrix, matrix)
        assert compose(square, square) == square
        # r internal vertices, unrestricted colors x,y at the two ends.
        def accepts(r, x, y):
            possible = allowed - {x}
            for _ in range(r - 1):
                possible = {c for c in allowed if any(d != c for d in possible)}
            return bool(possible - {y})
        odd, even = [], []
        for x, y in product(range(4), repeat=2):
            a, b = accepts(1, x, y), accepts(2, x, y)
            assert a == accepts(3, x, y) == accepts(5, x, y)
            assert b == accepts(4, x, y) == accepts(6, x, y)
            # Closed forms prove the parity induction for all r, not just six.
            assert a == (len(allowed) >= 3 or {x, y} != allowed)
            assert b == (len(allowed) >= 3 or not (x == y and x in allowed))
            odd.append(a)
            even.append(b)
        rows.append(dict(allowed=sorted(allowed), odd=odd, even=even,
                         matrix_square=square))
    return rows


def kuratowski_certificate(graph):
    """Extract, then independently trace a K5 or K3,3 subdivision."""
    planar, witness = nx.check_planarity(graph, counterexample=True)
    assert not planar
    assert set(map(frozenset, witness.edges())) <= set(map(frozenset, graph.edges()))
    branch = sorted(v for v, d in witness.degree() if d != 2)
    paths, used = [], set()
    for u in branch:
        for first in sorted(witness[u]):
            if frozenset((u, first)) in used:
                continue
            path, previous, v = [u, first], u, first
            used.add(frozenset((u, first)))
            while v not in branch:
                following, = set(witness[v]) - {previous}
                assert following not in path
                used.add(frozenset((v, following)))
                path.append(following)
                previous, v = v, following
            paths.append(path)
    assert len(used) == witness.number_of_edges()
    interiors = [v for p in paths for v in p[1:-1]]
    assert len(interiors) == len(set(interiors))
    links = {frozenset((p[0], p[-1])) for p in paths}
    assert len(links) == len(paths)
    from itertools import combinations
    complete = {frozenset(e) for e in combinations(branch, 2)}
    if len(branch) == 5:
        assert links == complete
        model = 'K5'
    else:
        assert len(branch) == 6
        sides = [set(s) for s in combinations(branch, 3)
                 if links == {frozenset((a, b)) for a in s for b in set(branch)-set(s)}]
        assert sides
        model = 'K3,3'
    return dict(model=model, branch_vertices=branch, paths=paths)


def build():
    records, summaries, controls = [], [], []
    for length in (3, 5, 6):
        counts, disk_rows, nonconstant, forbidden = Counter(), [], [], []
        for index, row in enumerate(templates(length)):
            kind, edges = row['kind'], row['edges']
            n = length + 4
            counts[f'{kind}_templates'] += 1
            graph = nx.Graph(edges)
            graph.add_edges_from((n, b) for b in range(5))
            disk, embedding = nx.check_planarity(graph)
            varying = len(set(row['middle_neighborhoods'])) > 1
            if varying:
                assert not disk
                counts[f'{kind}_nonconstant_rejected'] += 1
                nonconstant.append(index)
                if (length, kind) in ((5, 'I'), (6, 'II')):
                    forbidden.append(dict(index=index, **kuratowski_certificate(graph)))
            sigma = None
            if length in (3, 5):
                sigma = sum(1 << j for j, b in enumerate(REPS)
                            if direct_graph_extend(n, edges, b))
                assert not (sigma >> QI & 1)
                if sigma & T4 == T4:
                    counts[f'{kind}_T4'] += 1
                    if sigma.bit_count() < 9:
                        counts[f'{kind}_T4_multiple_missing'] += 1
                        if not controls:
                            assert not disk
                            exact, full = relation(n, edges)
                            assert exact == sigma
                            critical = sorted(set(edges) - CYCLE)
                            assert all(direct_graph_extend(n, tuple(e for e in edges if e != edge), Q)
                                       for edge in critical)
                            controls.append(dict(length=length, **row, sigma=sigma,
                                                 full_relation=full,
                                                 critical_edges=critical,
                                                 apex_obstruction=kuratowski_certificate(graph)))
            # Bit u*n+v is the edge u<v, with n=length+4; no apex edges here.
            encoded = format(sum(1 << (u*n+v) for u, v in edges), 'x')
            records.append([length, index, kind, row['triangle_colors'], encoded, disk, sigma])
            if not disk:
                continue
            counts[f'{kind}_disk'] += 1
            rotation = [list(embedding.neighbors_cw_order(v)) for v in range(n + 1)]
            faces = faces_of(rotation)
            assert n + 1 - graph.number_of_edges() + len(faces) == 2
            saved = dict(index=index, **row, apex_rotation=rotation)
            if length in (3, 5):
                exact, full = relation(n, edges)
                assert exact == sigma
                deletions = []
                for edge in sorted(set(edges) - CYCLE):
                    child = tuple(e for e in edges if e != edge)
                    assert direct_graph_extend(n, child, Q)
                    deletions.append(edge)
                saved.update(sigma=sigma, full_relation=full,
                             critical_edges=deletions)
                if sigma & T4 == T4:
                    assert sigma == 1023 ^ (1 << QI)
                    counts[f'{kind}_disk_T4_single_missing'] += 1
            disk_rows.append(saved)
        summaries.append(dict(length=length, counts=dict(sorted(counts.items())),
                              nonconstant_template_indices=nonconstant,
                              required_minor_obstructions=forbidden,
                              disk_templates=disk_rows))
    counts = {r['length']: r['counts'] for r in summaries}
    assert counts[5]['I_disk'] == counts[5]['II_disk'] == 8
    assert counts[6]['I_disk'] == counts[6]['II_disk'] == 8
    assert counts[5]['I_disk_T4_single_missing'] == 4
    assert counts[5]['II_disk_T4_single_missing'] == 4
    assert controls
    long_lifts = []
    for base in next(r for r in summaries if r['length'] == 5)['disk_templates']:
        old_edges = set(base['edges'])
        old_path = base['path']
        ns = [tuple(b for b in range(5) if (b, v) in old_edges) for v in old_path]
        assert len(set(ns[1:-1])) == 1
        for added in (2, 4, 8):
            path = list(range(old_path[0], old_path[-1] + added + 1))
            neighborhoods = [ns[0]] + [ns[1]] * (len(path) - 2) + [ns[-1]]
            edges = set(CYCLE)
            edges.update(zip(path, path[1:]))
            edges.update((b, v) for v, neighbors in zip(path, neighborhoods) for b in neighbors)
            if base['kind'] == 'II':
                edges.update(e for e in old_edges if e[1] == 5)
                edges.update((5, v) for v in path)
            n = 9 + added
            graph = nx.Graph(sorted(edges))
            graph.add_edges_from((n, b) for b in range(5))
            assert nx.check_planarity(graph)[0]
            actual = format(sum(int(direct_graph_extend(n, sorted(edges), b)) << j
                                for j, b in enumerate(BOUNDARY)), '060x')
            assert actual == base['full_relation']
            long_lifts.append(dict(base_index=base['index'], added=added,
                                   edges=sorted(edges), full_relation=actual))
    dependencies = [Path(__file__).resolve()] + [ROOT / 'scripts' / f'{name}.py' for name in
                    ('c5_cell_enumerator', 'c5_disk_deletions', 'local_closure', 'boundary_relations')]
    return dict(schema=1,
                scope='Finite split-quotient topology tests and transfer identities supporting the documented arbitrary odd-cycle reduction; not a Lean theorem.',
                source_sha256={str(p.relative_to(ROOT)): sha(p) for p in dependencies},
                fixed_pattern=Q, pattern_index=QI, pattern_order=REPS,
                template_record_format=['cycle_length', 'index', 'kind', 'triangle_colors',
                                        'edges_hex_bit_u_times_n_plus_v_n_equals_length_plus_4',
                                        'disk', 'sigma_or_null'],
                # Retain all small controls, including the nonplanar ones.
                enumerated_templates=records, cases=summaries,
                path_transfer=transfer_rows(), no_disk_control=controls[0],
                long_lifts=long_lifts,
                summary={str(k): v for k, v in counts.items()})


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
