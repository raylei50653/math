#!/usr/bin/env python3
"""Read raw certificates; independently check topology and all graph lifts.

No producer imports or graph-library dependencies. Propagated domains / MRV
enumeration is compared with exact saved lists, including every empty cell.
"""
import argparse
from collections import Counter
import gzip
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B = tuple(range(5))
U = tuple(range(5, 10))
TAUS = list(itertools.product(range(4), repeat=5))


def graph_check(g, kind):
    vertices = g['vertices']
    assert len(vertices) == len(set(vertices))
    edges = [tuple(e) for e in g['edges']]
    assert len(edges) == len(set(edges))
    assert all(a < b and a in vertices and b in vertices for a, b in edges)
    adjacency = {v: set() for v in vertices}
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    seen = {0}
    todo = [0]
    while todo:
        for v in adjacency[todo.pop()] - seen:
            seen.add(v)
            todo.append(v)
    assert seen == set(vertices)
    pins = [B] if kind == 'witness' else [B, U]
    if kind != 'witness':
        assert g['B'] == list(B) and g['U'] == list(U)
    for ring in pins:
        actual = {e for e in edges if e[0] in ring and e[1] in ring}
        expected = {tuple(sorted((ring[i], ring[(i + 1) % 5]))) for i in B}
        assert actual == expected
    rotation = {int(v): ns for v, ns in g['rotation'].items()}
    assert set(rotation) == set(vertices)
    assert all(len(ns) == len(set(ns)) and set(ns) == adjacency[v]
               for v, ns in rotation.items())
    # Traverse every directed dart using the saved vertex cyclic rotations.
    successor = {}
    for v, ns in rotation.items():
        for i, u in enumerate(ns):
            successor[(u, v)] = (v, ns[(i + 1) % len(ns)])
    pending = set(successor)
    faces = []
    while pending:
        start = min(pending)
        dart = start
        face = []
        while dart in pending:
            pending.remove(dart)
            face.append(dart[0])
            dart = successor[dart]
        assert dart == start
        faces.append(face)
    canonical = lambda f: min(tuple(f[i:] + f[:i]) for i in range(len(f)))
    assert Counter(map(canonical, faces)) == Counter(map(canonical, g['faces']))
    assert g['faces'][0] == [0, 4, 3, 2, 1]
    assert len(vertices) - len(edges) + len(faces) == 2
    if kind == 'annulus':
        assert g['faces'][-1] == list(U)
        assert set(g['private']) == set(vertices) - set(B) - set(U)
    if kind == 'capped':
        center = g['center']
        assert center not in B + U
        assert adjacency[center] == set(U)
        triangles = Counter(canonical([center, U[i], U[(i + 1) % 5]]) for i in B)
        assert all(Counter(map(canonical, faces))[f] == n for f, n in triangles.items())
    return adjacency


def full_lifts(g, adjacency, beta):
    vertices = g['vertices']
    initial = {v: set(range(4)) for v in vertices}
    for v, c in zip(B, beta):
        initial[v] = {c}
    result = []

    def search(domains, queue):
        while queue:
            v = queue.pop()
            if not domains[v]:
                return
            if len(domains[v]) != 1:
                continue
            c = next(iter(domains[v]))
            for w in adjacency[v]:
                if c in domains[w]:
                    domains[w] = domains[w] - {c}
                    if not domains[w]:
                        return
                    if len(domains[w]) == 1:
                        queue.append(w)
        free = [v for v in vertices if len(domains[v]) > 1]
        if not free:
            result.append(''.join(str(next(iter(domains[v]))) for v in vertices))
            return
        v = min(free, key=lambda w: (len(domains[w]), -len(adjacency[w]), -w))
        for c in sorted(domains[v]):
            branch = domains.copy()
            branch[v] = {c}
            search(branch, [v])

    search(initial, list(B))
    return sorted(result)


def verify_rows(g, kind, betas):
    adjacency = graph_check(g, kind)
    assert len(g['rows']) == 10
    assert [row['beta'] for row in g['rows']] == betas
    count = 0
    mask = 0
    for i, row in enumerate(g['rows']):
        actual = full_lifts(g, adjacency, row['beta'])
        count += len(actual)
        if actual:
            mask |= 1 << i
        if kind == 'witness':
            assert row['lifts'] == actual
        else:
            assert len(row['cells']) == 1024
            cells = [[] for _ in TAUS]
            for lift in actual:
                t = tuple(int(lift[g['vertices'].index(u)]) for u in U)
                j = sum(c * 4 ** (4 - k) for k, c in enumerate(t))
                cells[j].append(lift)
            assert row['cells'] == cells
    return count, mask


def load_cert(path):
    return json.loads(gzip.decompress(Path(path).read_bytes()))


def run(construction, contract):
    catalogue = json.loads((ROOT / 'frozen/artifacts/c5_cells/cells.json').read_bytes())
    betas = catalogue['pattern_order']
    assert construction['beta_domain'] == contract['beta_domain'] == betas
    assert construction['tau_domain'] == contract['tau_domain'] == [list(t) for t in TAUS]
    assert construction['B'] == list(B) and construction['U'] == list(U)
    eligible = {int(m) for m, g in catalogue['cells'].items()
                if all(max(e) >= 5 for e in g['edges'])}
    assert {g['mask'] for g in construction['representatives']} == eligible
    assert len(construction['representatives']) == len(eligible) == 102
    totals = Counter()
    for target in construction['representatives']:
        m = target['mask']
        expected = catalogue['cells'][str(m)]
        h, a, c = (target[key] for key in ('witness', 'annulus', 'capped'))
        assert target['private_count'] == expected['k_eff'] <= 5
        relabel = lambda v: v if v < 5 else v + 5
        expected_edges = {tuple(sorted((i, (i + 1) % 5))) for i in B}
        expected_edges |= {tuple(sorted((relabel(x), relabel(y)))) for x, y in expected['edges']}
        assert set(map(tuple, h['edges'])) == expected_edges
        assert len(a['vertices']) - 10 == target['private_count']
        assert len(c['vertices']) - 5 == 6 + target['private_count']
        for kind, g in [('witness', h), ('annulus', a), ('capped', c)]:
            n, mask = verify_rows(g, kind, betas)
            totals[kind] += n
            assert mask == m
        assert set(map(tuple, c['edges'])) == set(map(tuple, a['edges'])) | {
            tuple(sorted((c['center'], u))) for u in U}
        assert set(map(tuple, a['edges'])) == expected_edges | {
            tuple(sorted((U[i], U[(i + 1) % 5]))) for i in B} | {(0, 5)}
    for control in construction['strict_shrink_controls']:
        a, c = control['source_annulus'], control['source_capped']
        assert c['vertices'] == a['vertices'] + [c['center']]
        assert set(map(tuple, c['edges'])) == set(map(tuple, a['edges'])) | {
            tuple(sorted((c['center'], u))) for u in U}
        for kind, key in [('annulus', 'source_annulus'), ('capped', 'source_capped')]:
            n, mask = verify_rows(control[key], kind, betas)
            totals['path_source_' + kind] += n
            assert mask == control['target_mask']
        assert control['source_private_count'] > control['target_private_count']
    for g in contract['graphs']:
        c = g['capped']
        assert c['vertices'] == g['vertices'] + [c['center']]
        assert set(map(tuple, c['edges'])) == set(map(tuple, g['edges'])) | {
            tuple(sorted((c['center'], u))) for u in U}
        for kind, graph in [('annulus', g), ('capped', g['capped'])]:
            n, mask = verify_rows(graph, kind, betas)
            totals['prism_' + kind] += n
            assert mask == 1023
    targets = {g['mask']: g for g in construction['representatives']}
    for control in construction['strict_shrink_controls']:
        source = control['source_annulus']
        target = targets[control['target_mask']]['annulus']
        difference = [[i, j]
                      for i, (sr, tr) in enumerate(zip(source['rows'], target['rows']))
                      for j, (tau, x, y) in enumerate(zip(TAUS, sr['cells'], tr['cells']))
                      if len(set(tau)) == 3 and all(tau[k] != tau[(k + 1) % 5] for k in B)
                      and bool(x) != bool(y)]
        assert difference == control['strict_R3_difference_cells'] and difference
    return {'status': 'PASS', 'algorithm': 'raw rotations dart traversal and full propagated-domain MRV',
            'catalogue_representatives': 102, 'exact_lifts': dict(totals),
            'source_minimality': 'not triggered', 'general_nine_point_existence': 'OPEN'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--construction', type=Path, default=ROOT / 'construction/certificate.json.gz')
    parser.add_argument('--contract', type=Path, default=ROOT / 'contract/certificate.json.gz')
    args = parser.parse_args()
    print(json.dumps(run(load_cert(args.construction), load_cert(args.contract)), indent=2))


if __name__ == '__main__':
    main()
