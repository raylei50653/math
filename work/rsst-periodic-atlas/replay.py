#!/usr/bin/env python3
"""Independent standard-library replay of RSST periodic coloring witnesses.

Run: python3 -I work/rsst-periodic-atlas/replay.py
No SAT solver or atlas generator is imported. The one-cell decisions are
independently decided by backtracking; larger SAT witnesses are checked against
the original source edges. Larger UNSAT decisions are not certified here.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE_HASH = '1c92fc280a9b384f736b94077fc59aac75e3d830d441ffd2d18683ee4b524e84'


def read_sources(path):
    """Parse the original adjacency records, independently of the generator."""
    lines = path.read_text().splitlines()
    pos, result = 0, []
    while pos < len(lines):
        if not lines[pos].strip():
            pos += 1
            continue
        name = lines[pos].strip()
        n, r, _, _ = map(int, lines[pos + 1].split())
        adj = []
        for v in range(n):
            label, degree, *neighbors = map(int, lines[pos + 3 + v].split())
            assert label == v + 1 and degree == len(neighbors)
            adj.append([w - 1 for w in neighbors])
        for v, neighbors in enumerate(adj):
            assert len(neighbors) == len(set(neighbors))
            assert all(v in adj[w] for w in neighbors)
        edges = [(v, w) for v, neighbors in enumerate(adj) for w in neighbors if v < w]
        faces = {}
        for v, neighbors in enumerate(adj):
            for j in range(len(neighbors) - (v < r)):
                face = (v, neighbors[j], neighbors[(j + 1) % len(neighbors)])
                faces.setdefault(tuple(sorted(face)), face)
        assert len(edges) == 3 * n - r - 3
        assert len(faces) == 2 * n - r - 2
        result.append(dict(name=name, n=n, r=r, adj=adj, edges=edges,
                           faces=list(faces.values())))
        pos += n + 3
        coordinate_count = 0
        while coordinate_count < n:
            coordinate_count += len(lines[pos].split())
            pos += 1
        assert coordinate_count == n
    assert len(result) == 633
    return result


def source_map(source, kind, subdivisions=None):
    """Reconstruct the intended seam identifications from the polygon."""
    if kind == 'hexagon':
        assert source['r'] == 6
        polygon = [(F(x, 3), F(y, 3)) for x, y in
                   [(1, 1), (-1, 2), (-2, 1), (-1, -1), (1, -2), (2, -1)]]
    else:
        a, b, aa, bb = subdivisions
        assert a == aa and b == bb and 2 * (a + b) == source['r']
        polygon = ([(F(i, a), F(0)) for i in range(a)]
                   + [(F(1), F(i, b)) for i in range(b)]
                   + [(1 - F(i, a), F(1)) for i in range(a)]
                   + [(F(0), 1 - F(i, b)) for i in range(b)])
    keys, mapping = {}, []
    for x, y in polygon:
        sx, sy = int(x // 1), int(y // 1)
        key = (x - sx, y - sy)
        if key not in keys:
            keys[key] = len(keys)
        mapping.append([keys[key], sx, sy])
    count = len(keys)
    for _ in range(source['n'] - source['r']):
        mapping.append([count, 0, 0])
        count += 1
    return mapping, count


def edge_orbit(u, v, dx, dy):
    return min((u, v, dx, dy), (v, u, -dx, -dy))


def check_structure(source, mapping, count, edges, faces, degrees):
    rebuilt = set()
    for u, v in source['edges']:
        i, x, y = mapping[u]
        j, s, t = mapping[v]
        rebuilt.add(edge_orbit(i, j, s - x, t - y))
    assert rebuilt == set(map(tuple, edges))
    assert len(rebuilt) == 3 * count
    rebuilt_degrees = [0] * count
    for u, v, _, _ in rebuilt:
        rebuilt_degrees[u] += 1
        rebuilt_degrees[v] += 1
    assert rebuilt_degrees == degrees
    assert all(degrees[mapping[v][0]] == len(source['adj'][v])
               for v in range(source['r'], source['n']))
    expected_faces = [[mapping[v] for v in face] for face in source['faces']]
    assert faces == expected_faces and len(faces) == 2 * count


def color_graph(count, edges):
    """Exact DSATUR search; color-name symmetry is removed by first use."""
    graph = [set() for _ in range(count)]
    for u, v in edges:
        if u == v:
            return None
        graph[u].add(v)
        graph[v].add(u)
    assigned = [-1] * count

    def search(remaining, used):
        if not remaining:
            return assigned.copy()
        vertex = max(remaining, key=lambda v:
                     (len({assigned[w] for w in graph[v] if assigned[w] >= 0}),
                      len(graph[v]), -v))
        forbidden = {assigned[w] for w in graph[vertex] if assigned[w] >= 0}
        for color in range(min(4, used + 1)):
            if color not in forbidden:
                assigned[vertex] = color
                result = search(remaining - {vertex}, max(used, color + 1))
                if result is not None:
                    return result
        assigned[vertex] = -1
        return None

    result = search(set(range(count)), 0)
    if result is not None:
        assert all(result[u] != result[v] for u, v in edges)
    return result


def one_cell(source, mapping, count, recorded_status):
    edges = [(mapping[u][0], mapping[v][0]) for u, v in source['edges']]
    coloring = color_graph(count, edges)
    status = 'SAT' if coloring is not None else 'UNSAT'
    assert status == recorded_status
    return status, any(u == v for u, v in edges)


def check_hnf(source, mapping, count, rec):
    a, b, d = rec['a'], rec['b'], rec['d']
    assert a > 0 and d > 0 and 0 <= b < a and rec['index'] == a * d
    assert rec['generators'] == [[a, 0], [b, d]]
    if rec['status'] == 'UNSAT':
        assert not rec.get('witness')
        return 0
    assert rec['status'] == 'SAT'
    colors = rec['witness']['colors']
    assert len(colors) == d and all(len(row) == a for row in colors)
    assert all(len(cell) == count and all(type(c) is int and 0 <= c < 4 for c in cell)
               for row in colors for cell in row)

    def at(v, x, y):
        vertical = y // d
        return colors[y - vertical * d][(x - vertical * b) % a][v]

    checked = 0
    for y in range(d):
        for x in range(a):
            for u, v in source['edges']:
                i, sx, sy = mapping[u]
                j, tx, ty = mapping[v]
                assert at(i, x + sx, y + sy) != at(j, x + tx, y + ty)
                checked += 1
            for face in source['faces']:
                assert len({at(mapping[v][0], x + mapping[v][1], y + mapping[v][2])
                            for v in face}) == 3
    return checked


def all_hnf_records(source, mapping, count, records, minimum):
    expected = [(a, b, index // a) for index in range(1, 5)
                for a in range(1, index + 1) if index % a == 0 for b in range(a)]
    assert [(r['a'], r['b'], r['d']) for r in records] == expected
    edges_checked = sum(check_hnf(source, mapping, count, rec) for rec in records)
    sat = [r['index'] for r in records if r['status'] == 'SAT']
    assert minimum == min(sat, default=None)
    status, loop = one_cell(source, mapping, count, records[0]['status'])
    # Every present minimum is at most two. Thus independently deciding index
    # one plus checking a minimum witness verifies all smaller exclusions.
    assert minimum in (1, 2)
    assert (minimum == 1) == (status == 'SAT')
    return edges_checked, sum(r['status'] == 'SAT' for r in records), loop


def permutation_power(perm, exponent):
    if exponent < 0:
        perm = [perm.index(c) for c in range(4)]
        exponent = -exponent
    result = list(range(4))
    for _ in range(exponent):
        result = [perm[c] for c in result]
    return result


def check_equivariant(source, mapping, count, records):
    expected = {(a, b) for a in permutations(range(4)) for b in permutations(range(4))
                if all(a[b[c]] == b[a[c]] for c in range(4))}
    assert len(expected) == 120
    assert {(tuple(r['alpha']), tuple(r['beta'])) for r in records} == expected
    assert len(records) == 120
    witnesses, checked = 0, 0
    for rec in records:
        if rec['status'] == 'UNSAT':
            assert 'witness' not in rec
            continue
        assert rec['status'] == 'SAT'
        alpha, beta = rec['alpha'], rec['beta']
        colors = rec['witness']['motif_colors']
        assert len(colors) == count and all(c in range(4) for c in colors)
        ox = next(k for k in range(1, 5) if permutation_power(alpha, k) == list(range(4)))
        oy = next(k for k in range(1, 5) if permutation_power(beta, k) == list(range(4)))
        assert rec['witness']['axis_periods'] == [ox, oy]

        def at(v, x, y):
            return permutation_power(alpha, x)[permutation_power(beta, y)[colors[v]]]

        for y in range(oy):
            for x in range(ox):
                for u, v in source['edges']:
                    i, sx, sy = mapping[u]
                    j, tx, ty = mapping[v]
                    assert at(i, x + sx, y + sy) != at(j, x + tx, y + ty)
                    checked += 1
        identity_shifts = [[x, y] for y in range(oy) for x in range(ox)
                           if all(at(v, 0, 0) == at(v, x, y) for v in range(count))]
        assert identity_shifts == rec['witness']['same_color_shifts_in_axis_rectangle']
        assert ox * oy // len(identity_shifts) == rec['witness']['literal_translation_index']
        witnesses += 1
    return witnesses, checked


def check_k5(source, mapping, example):
    clique = example['one_cell_k5']
    if clique is None:
        return None
    assert len(clique) == len(set(clique)) == 5
    edges = set(source['edges'])
    witnesses = example['one_cell_k5_source_edges']
    assert len(witnesses) == 10
    for pair, (u, v) in zip(combinations(clique, 2), witnesses):
        u, v = u - 1, v - 1
        assert tuple(sorted((u, v))) in edges
        assert sorted([mapping[u][0], mapping[v][0]]) == list(pair)
    return {'example': example['id'], 'clique': clique,
            'source_edges_1_based': witnesses, 'checked_clique_edges': 10}


def main():
    source_path, atlas_path = HERE / 'sources/unavoidable.conf', HERE / 'atlas.json'
    assert sha256(source_path.read_bytes()).hexdigest() == SOURCE_HASH
    sources = read_sources(source_path)
    atlas = json.loads(atlas_path.read_text())
    assert atlas['source']['sha256'] == SOURCE_HASH
    # Known-answer controls for the independent exact search.
    assert color_graph(4, list(combinations(range(4), 2))) is not None
    assert color_graph(5, list(combinations(range(5), 2))) is None
    assert color_graph(1, [(0, 0)]) is None
    assert color_graph(5, [(v, (v + 1) % 5) for v in range(5)]) is not None
    assert len(atlas['inventory']) == 633
    totals = Counter()
    for source, row in zip(sources, atlas['inventory']):
        assert row['name'] == source['name'] and row['r'] == source['r'] and row['n'] == source['n']
        if source['r'] % 2:
            assert 'hnf_decisions' not in row
            totals['odd_ring_not_tested'] += 1
            continue
        mapping, count = source_map(source, 'square', row['side_subdivisions'])
        assert mapping == row['source_map'] and count == row['motif_n']
        check_structure(source, mapping, count, row['motif_edges'], row['motif_faces'], row['degrees'])
        checked, witnesses, loop = all_hnf_records(source, mapping, count,
                                                 row['hnf_decisions'], row['minimum_index'])
        assert loop == row['quotient_has_self_loop']
        totals['inventory_one_cell_decisions'] += 1
        totals['inventory_hnf_sat_witnesses'] += witnesses
        totals['inventory_source_edge_instances'] += checked
        totals['inventory_minimum_' + str(row['minimum_index'])] += 1
        totals['inventory_one_cell_loops'] += loop
    cliques = []
    for ex in atlas['examples']:
        source = sources[ex['source_index'] - 1]
        mapping, count = source_map(source, ex['kind'], ex['side_subdivisions'])
        assert mapping == ex['source_patch']['map'] and count == len(ex['points'])
        check_structure(source, mapping, count, ex['edges'], ex['faces'], ex['degrees'])
        checked, witnesses, _ = all_hnf_records(source, mapping, count,
                                               ex['period_analysis']['sublattices'], ex['minimum_index'])
        assert len(ex['periods']) == len(ex['period_analysis']['sublattices'])
        for display, rec in zip(ex['periods'], ex['period_analysis']['sublattices']):
            assert all(display[k] == rec[k] for k in ('a', 'b', 'd', 'index', 'status'))
            if rec['status'] == 'SAT':
                flat = [color for row in rec['witness']['colors']
                        for cell in row for color in cell]
                assert display['witness']['colors'] == flat
            else:
                assert display['witness'] is None
        totals['selected_one_cell_decisions'] += 1
        totals['selected_hnf_sat_witnesses'] += witnesses
        totals['selected_hnf_source_edge_instances'] += checked
        witnesses, checked = check_equivariant(source, mapping, count,
                                               ex['period_analysis']['equivariant'])
        totals['selected_equivariant_sat_witnesses'] += witnesses
        totals['selected_equivariant_source_edge_instances'] += checked
        clique = check_k5(source, mapping, ex)
        if clique:
            cliques.append(clique)
    assert totals['inventory_one_cell_decisions'] == 349
    assert totals['selected_one_cell_decisions'] == 7
    assert len(cliques) == 2
    assert {str(i): totals['inventory_minimum_' + str(i)] for i in (1, 2)} == atlas['scan_summary']['square_minimum_index_counts']
    report = {'schema': 'rsst-periodic-replay/1', 'status': 'PASS',
              'command': 'python3 -I work/rsst-periodic-atlas/replay.py',
              'inputs_sha256': {str(path.relative_to(HERE)): sha256(path.read_bytes()).hexdigest()
                                for path in [source_path, atlas_path, Path(__file__)]},
              'checks': {'source_parser_independent_of_generator': True,
                         'polygon_seams_reconstructed_independently': True,
                         'all_source_edges_and_faces_retained': True,
                         'all_one_cell_decisions_independent_dsatur': True,
                         'all_saved_hnf_sat_witnesses_checked_on_original_source': True,
                         'selected_equivariant_sat_witnesses_checked_on_original_source': True,
                         'display_colors_match_verified_hnf_witnesses': True,
                         'all_claimed_minima_checked_by_one_cell_decision_and_sat_witness': True,
                         'two_k5_obstructions_checked_against_original_source_edges': True,
                         'known_answer_graph_controls': True},
              'counts': dict(totals), 'k5_certificates': cliques,
              'scope': 'One-cell SAT and UNSAT decisions and minima 1 or 2 independently redecided. All stored SAT witnesses replayed against source edges. Larger-quotient and equivariant UNSAT decisions remain the original solver results, without formal UNSAT certificates. No general four-color or reducibility claim.'}
    target = HERE / 'replay-checks.json'
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'status': report['status'], 'counts': dict(totals)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
