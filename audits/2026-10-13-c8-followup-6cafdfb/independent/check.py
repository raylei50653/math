#!/usr/bin/env python3
"""Independent fixed-order DFS from frozen literal collar edges.

Does not import or execute the primary checker. Rebuilds every original graph
using the prior accepted literal collar rather than its extras parametrization.
"""
from pathlib import Path
import argparse
import copy
import gzip
import hashlib
import json

ROOT = Path(__file__).resolve().parent


def edge(a, b):
    return tuple(sorted((a, b)))


def exact_lifts(vertices, edges, collar, row):
    index = {v: i for i, v in enumerate(vertices)}
    adjacency = [[] for _ in vertices]
    for a, b in edges:
        i, j = index[a], index[b]
        adjacency[i].append(j)
        adjacency[j].append(i)
    colors = [-1] * len(vertices)
    for i, color in enumerate(row):
        colors[index[f'b{i}']] = int(color)
    names = ['r']
    for i in range(8):
        names.extend((f't{i}', collar[i]))
    order = [index[v] for v in names]
    result = []

    def dfs(position):
        if position == len(order):
            result.append(''.join(map(str, colors)))
            return
        v = order[position]
        forbidden = 0
        for w in adjacency[v]:
            if colors[w] >= 0:
                forbidden |= 1 << colors[w]
        for color in range(4):
            if not forbidden & (1 << color):
                colors[v] = color
                dfs(position + 1)
        colors[v] = -1

    dfs(0)
    return sorted(result)


def run(certificate=None):
    raw = (ROOT / 'RESULTS.frozen.json').read_bytes()
    inputs = json.loads((ROOT / 'INPUT.json').read_text())
    assert hashlib.sha256(raw).hexdigest() == inputs['sha256']
    prior = json.loads(raw)
    queries = {q['query_id']: q for q in prior['queries']
               if q['status'] == 'necessary-condition residual'}
    assert len(queries) == 8
    if certificate is None:
        certificate = json.loads(gzip.decompress((ROOT.parent / 'certificate.json.gz').read_bytes()))
    cases = certificate['cases']
    assert {c['id'] for c in cases} == set(queries) and len(cases) == 8
    receipts = []
    for c in cases:
        q = queries[c['id']]
        assert c['target'] == q['target']
        assert c['e'] == q['extras']
        collar = q['boundary_order']
        vertices = [f'b{i}' for i in range(5)] + collar + [f't{i}' for i in range(8)] + ['r']
        edges = {edge(a, b) for a, b in q['collar_edges']}
        for i in range(8):
            edges.update((edge(collar[i], f't{i}'),
                          edge(collar[(i+1) % 8], f't{i}'),
                          edge(f't{i}', f't{(i+1) % 8}'),
                          edge('r', f't{i}')))
        assert c['vertices'] == vertices
        assert c['outer_B'] == vertices[:5]
        assert c['collar_C'] == collar
        assert c['edges'] == [list(e) for e in sorted(edges)]
        assert c['row_order'] == [''.join(map(str, row)) for row in prior['outer_pattern_order']]

        # Reconstruct rotations from coherent oriented triangles, then walk all
        # darts. A single outer face B is required, with 37 inner triangles.
        following = {v: {} for v in vertices}
        faces = c['oriented_inner_faces'] + [vertices[:5][::-1]]
        for face in faces:
            for i, v in enumerate(face):
                previous, nxt = face[i-1], face[(i+1) % len(face)]
                assert previous not in following[v]
                following[v][previous] = nxt
        assert len(faces) == 38
        for v in vertices:
            neighbors = {w if u == v else u for u, w in edges if v in (u, w)}
            assert set(following[v]) == neighbors == set(following[v].values())
            start = next(iter(neighbors)); seen = set(); w = start
            while w not in seen:
                seen.add(w); w = following[v][w]
            assert seen == neighbors and w == start
        counts, digests = [], []
        for row in c['row_order']:
            lifts = exact_lifts(vertices, edges, collar, row)
            assert lifts == c['complete_fibres'][row], (c['id'], row)
            counts.append(len(lifts))
            digests.append(hashlib.sha256(('\n'.join(lifts)+'\n').encode()).hexdigest())
        sigma = sum((1 << i) for i, count in enumerate(counts) if count)
        assert counts == c['counts'] and sigma == c['sigma'] == 1023
        receipts.append({'id': c['id'], 'counts': counts, 'sigma': sigma,
                         'complete_fibre_sha256': digests})
    return {'status': 'pass', 'method': 'literal prior collar; independent fixed-order DFS',
            'all_ten_fibres_compared': True, 'full_lifts_compared': True,
            'cases': receipts}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--negative', action='store_true')
    args = parser.parse_args()
    if not args.negative:
        result = run()
    else:
        original = json.loads(gzip.decompress((ROOT.parent / 'certificate.json.gz').read_bytes()))
        rejected = []
        for mutation in ('deleted_full_lift', 'changed_original_collar_edge', 'missing_query'):
            damaged = copy.deepcopy(original)
            if mutation == 'deleted_full_lift':
                damaged['cases'][0]['complete_fibres']['01012'].pop()
            elif mutation == 'changed_original_collar_edge':
                damaged['cases'][0]['edges'].pop()
            else:
                damaged['cases'].pop()
            try:
                run(damaged)
            except AssertionError:
                rejected.append(mutation)
            else:
                raise AssertionError(('negative accepted', mutation))
        result = {'status': 'pass', 'rejected': rejected}
    print(json.dumps(result, sort_keys=True))
