#!/usr/bin/env python3
"""Exact second-cut fibres and weighted directional separation controls."""
import argparse
from collections import defaultdict
from itertools import combinations, product
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
INPUT = 'audits/2026-10-15-route-research-6ddea32/cut-certificate.json'


def components(n, edges):
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    seen, result = set(), []
    for start in range(n):
        if start in seen:
            continue
        todo, block = [start], []
        seen.add(start)
        while todo:
            u = todo.pop()
            block.append(u)
            for v in sorted(adj[u]):
                if v not in seen:
                    seen.add(v)
                    todo.append(v)
        result.append(sorted(block))
    return sorted(result)


def four_colourings(n, edges):
    prior = [[] for _ in range(n)]
    for u, v in edges:
        prior[max(u, v)].append(min(u, v))
    row, result = [0]*n, []

    def visit(v):
        if v == n:
            result.append(tuple(row))
            return
        for colour in range(4):
            if all(row[u] != colour for u in prior[v]):
                row[v] = colour
                visit(v+1)
    visit(1)
    return sorted(result)


def compute_control(control):
    n, edges, faces = control['vertices'], control['edges'], control['faces']
    edge_set = {tuple(e) for e in edges}
    assert len(edge_set) == len(edges) == 3*n-6
    assert len(faces) == 2*n-4 and len(components(n, edges)) == 1
    incident = defaultdict(list)
    for i, face in enumerate(faces):
        assert len(set(face)) == 3
        for edge in combinations(sorted(face), 2):
            assert edge in edge_set
            incident[edge].append(i)
    assert all(len(incident[tuple(edge)]) == 2 for edge in edges)
    # Orient adjacent triangles oppositely; connected closed orientable
    # triangulated surface with Euler characteristic two is a sphere.
    signs = {0: 1}
    todo = [0]
    face_directions = []
    for face in faces:
        face_directions.append({tuple(sorted((u, v))): (1 if u < v else -1)
                                for u, v in zip(face, face[1:]+face[:1])})
    while todo:
        f = todo.pop()
        for edge, direction in face_directions[f].items():
            g = next(i for i in incident[edge] if i != f)
            target = -signs[f]*direction*face_directions[g][edge]
            if g in signs:
                assert signs[g] == target
            else:
                signs[g] = target
                todo.append(g)
    assert len(signs) == len(faces)
    # Vertex links must also be connected cycles, excluding pinched surfaces.
    for v in range(n):
        link = [tuple(u for u in face if u != v) for face in faces if v in face]
        vertices = sorted({u for e in link for u in e})
        relabel = {u: i for i, u in enumerate(vertices)}
        assert all(sum(u in e for e in link) == 2 for u in vertices)
        assert len(components(len(vertices), [(relabel[u], relabel[w]) for u, w in link])) == 1
    dual = [incident[tuple(edge)] for edge in edges]
    rows, complete, tait_by_matching = [], set(), {}
    for tail in product(range(2), repeat=n-1):
        a = (0,)+tail
        if any(len({a[v] for v in face}) == 1 for face in faces):
            continue
        matching = [i for i, (u, v) in enumerate(edges) if a[u] == a[v]]
        assert all(sum(v in dual[i] for i in matching) == 1 for v in range(len(faces)))
        mono = components(n, [edges[i] for i in matching])
        complement = components(len(faces), [e for i, e in enumerate(dual) if i not in matching])
        assert len(mono) == len(complement)+1
        lifts, taits = [], []
        for btail in product(range(2), repeat=n-1):
            b = (0,)+btail
            if all(a[u] != a[v] or b[u] != b[v] for u, v in edges):
                lifts.append(b)
                colouring = tuple(2*a[v]+b[v] for v in range(n))
                complete.add(colouring)
                taits.append(tuple(colouring[u] ^ colouring[v] for u, v in edges))
        even = all(len(c) % 2 == 0 for c in complement)
        assert len(lifts) == (2**len(complement) if even else 0)
        tait_by_matching[tuple(matching)] = sorted(taits)
        rows.append({'a': a, 'matching': matching, 'monochromatic_components': mono,
                     'dual_complement_components': complement, 'all_root_fixed_b_lifts': lifts})
    assert sorted(complete) == four_colourings(n, edges)
    all_taits = {t for ts in tait_by_matching.values() for t in ts}
    assert len(all_taits) == len(complete)
    pairs = []
    for e, f in combinations(range(len(edges)), 2):
        left = sorted(t for t in all_taits if t[e] == 1 and t[f] != 1)
        right = sorted(t for t in all_taits if t[f] == 1 and t[e] != 1)
        images = []
        for t in left:
            beta = t[f]
            image = tuple(beta if x == 1 else 1 if x == beta else x for x in t)
            assert image in all_taits and image[f] == 1 and image[e] != 1
            inverse_beta = image[e]
            assert tuple(inverse_beta if x == 1 else 1 if x == inverse_beta else x
                         for x in image) == t
            images.append(image)
        assert sorted(images) == right
        pairs.append({'e': e, 'f': f, 'W_e_given_f': len(left), 'W_f_given_e': len(right)})
    return {'name': control['name'], 'vertices': n, 'edges': edges, 'faces': faces,
            'rows': rows, 'all_root_fixed_four_colourings': sorted(complete),
            'directional_weights': pairs,
            'summary': {'ordinary_matchings': len(rows),
                        'even_complement_matchings': sum(bool(r['all_root_fixed_b_lifts']) for r in rows),
                        'root_fixed_four_colourings': len(complete), 'edge_pairs': len(pairs)}}


def certificate():
    manifest = json.loads((HERE/'BASE.json').read_text())
    entry = next(x for x in manifest['prior_round_files'] if x['path'] == INPUT)
    raw = (ROOT/INPUT).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == entry['sha256'], 'prior input drift'
    data = json.loads(raw)
    return {'schema': 'cut-count-bridge-v1', 'base': manifest['base'],
            'input_sha256': entry['sha256'], 'source_status': 'not triggered',
            'controls': [compute_control(c) for c in data['controls']]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--write', type=Path)
    group.add_argument('--check', type=Path)
    args = parser.parse_args()
    expected = json.loads(json.dumps(certificate()))
    if args.write:
        with args.write.open('x') as stream:
            json.dump(expected, stream, indent=2)
            stream.write('\n')
    elif json.loads(args.check.read_text()) != expected:
        raise SystemExit('FAIL: certificate differs from complete recomputation')
    print(json.dumps({'status': 'PASS', 'source_status': 'not triggered',
                      'controls': [{'name': c['name'], **c['summary']} for c in expected['controls']]}))


if __name__ == '__main__':
    main()
