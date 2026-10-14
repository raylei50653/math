#!/usr/bin/env python3
"""Replay small-cycle and triangle-core claims on frozen K15 sphere controls.

This filters an existing finite control set; it does not enumerate new sources.
"""
import argparse
from collections import Counter
import gzip
import hashlib
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parent
SOURCE = 'audits/2026-10-13-k15-sphere-6cafdfb/certificate.json.gz'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def adj_from_edges(vertices, edges):
    adj = {v: set() for v in vertices}
    for v, w in edges:
        need(v != w, 'loop')
        adj[v].add(w)
        adj[w].add(v)
    return adj


def components(adj, removed):
    unseen = set(adj) - set(removed)
    result = []
    while unseen:
        v = min(unseen)
        unseen.remove(v)
        comp = {v}
        todo = [v]
        while todo:
            for w in adj[todo.pop()] & unseen:
                unseen.remove(w)
                comp.add(w)
                todo.append(w)
        result.append(comp)
    return result


def cycles(adj, length):
    out = set()
    for start in sorted(adj):
        def visit(path):
            if len(path) == length:
                if start in adj[path[-1]] and path[1] < path[-1]:
                    out.add(tuple(path))
                return
            for v in sorted(adj[path[-1]]):
                if v > start and v not in path:
                    visit(path + [v])
        visit([start])
    return sorted(out)


def triangles(adj):
    return [tuple(vs) for vs in combinations(sorted(adj), 3)
            if all(w in adj[v] for v, w in combinations(vs, 2))]


def sphere_faces(adj, faces):
    darts = Counter((f[i], f[(i + 1) % 3]) for f in faces for i in range(3))
    need(all(len(f) == 3 and len(set(f)) == 3 for f in faces), 'triangle faces')
    need(darts == Counter({(v, w): 1 for v in adj for w in adj[v]}),
         'complete oriented face incidence')
    need(len(adj) - sum(map(len, adj.values())) // 2 + len(faces) == 2,
         'sphere Euler characteristic')
    need(len(components(adj, ())) == 1, 'connected sphere')


def calculate():
    manifest = json.loads((PACKAGE / 'INPUTS.json').read_text())
    for item in manifest['files']:
        need(digest((PACKAGE / 'frozen' / item['path']).read_bytes()) == item['sha256'],
             'frozen drift: ' + item['path'])
    raw = (PACKAGE / 'frozen' / SOURCE).read_bytes()
    data = json.loads(gzip.decompress(raw))
    need(len(data['records']) == 2714, 'missing rooted input')
    by_sphere = {}
    for record in data['records']:
        by_sphere.setdefault(record['sphere'], []).append(record)
    need(len(by_sphere) == 192, 'missing sphere input')
    stats = Counter()
    sphere_records = []
    core_records = []
    examples = {}
    for sid, records in sorted(by_sphere.items()):
        r = records[0]
        n = len(r['rotation'])
        es = {tuple(e) for e in r['edges']} | {(v, n) for v in range(5)}
        adj = adj_from_edges(range(n + 1), es)
        faces = [f for f in r['faces'] if len(f) == 3]
        # The original outer face is clockwise relative to the disk faces.
        outer = r['outer_face']
        faces += [[outer[i], outer[(i + 1) % 5], n] for i in range(5)]
        sphere_faces(adj, faces)
        need(min(map(len, adj.values())) >= 5, 'minimum sphere degree')
        sep = {}
        for length in (3, 4, 5):
            sep[length] = [c for c in cycles(adj, length)
                           if len(components(adj, c)) > 1]
        i6 = (not sep[3] and not sep[4]
              and all(sorted(map(len, components(adj, c)))[0] == 1
                      and len(components(adj, c)) == 2 for c in sep[5]))
        stats['spheres'] += 1
        stats['internally_six_connected_spheres'] += int(i6)
        sphere_records.append({'sphere': sid, 'I6': i6,
                               'separating_cycles': {k: len(v) for k, v in sep.items()}})
        if not i6:
            continue
        for r in records:
            g = adj_from_edges(range(n), r['edges'])
            for shift in range(5):
                x, y, a, b, c = [(i + shift) % 5 for i in range(5)]
                need(g[a] & g[c] == {b}, 'nonconsecutive frame common neighbor')
                project = lambda v: a if v == c else v
                te = {tuple(sorted((project(v), project(w)))) for v, w in r['edges']}
                tv = set(g) - {c}
                t = adj_from_edges(tv, te)
                tf = [[project(v) for v in f] for f in r['faces'] if len(f) == 3]
                tf.append([x, a, y])
                sphere_faces(t, tf)
                need(len(t[x]) == len(g[x]) >= 4, 'x degree')
                need(len(t[y]) == len(g[y]) >= 4, 'y degree')
                need(len(t[b]) == len(g[b]) - 1 >= 3, 'b degree')
                need(len(t[a]) == len(g[a]) + len(g[c]) - 1 >= 7, 'z degree')
                need(all(len(t[v]) >= 5 for v in tv - {x, y, a, b}), 'other degrees')
                nonfacial = [q for q in triangles(t) if len(components(t, q)) > 1]
                if len(t[b]) == 3:
                    expected = [tuple(sorted(t[b]))]
                    need(nonfacial == expected, 'degree-three unique separator')
                    p, q = sorted(t[b] - {a})
                    need(p not in {x, y} and q not in {x, y}, 'internal p and q')
                    t0 = {v: ns - {b} for v, ns in t.items() if v != b}
                    need(all(len(components(t0, tri)) == 1 for tri in triangles(t0)),
                         'T0 separating triangle')
                    need(len(t0[p]) >= 4 and len(t0[q]) >= 4 and len(t0[a]) >= 6,
                         'T0 degrees')
                    branch = 'T0'
                else:
                    need(not nonfacial, 'T separating triangle')
                    branch = 'T'
                stats['rooted_openings'] += 1
                stats[branch + '_branch'] += 1
                stats['b_degree_' + str(len(t[b]))] += 1
                row = {'rooted_id': r['id'], 'shift': shift,
                       'b_degree': len(t[b]), 'branch': branch,
                       'edges_sha256': digest(json.dumps(sorted(te)).encode()),
                       'separating_triangles': nonfacial}
                core_records.append(row)
                examples.setdefault(branch, dict(row, original_edges=r['edges'],
                                    T_edges=sorted(te), pins={'x': x, 'y': y, 'z': a, 'b': b}))
    need(set(examples) == {'T', 'T0'}, 'both structural branches must trigger')
    # Actual negative controls for the low-level custody and embedding checks.
    for bad_faces in (faces[:-1], faces + faces[:1]):
        try:
            sphere_faces(adj, bad_faces)
        except ValueError:
            stats['rejected_face_corruptions'] += 1
        else:
            raise ValueError('accepted corrupt face list')
    return {'schema': 'c4-triangle-core-structure-v1', 'base': manifest['base'],
            'input_sha256': digest(raw), 'script_sha256': digest(Path(__file__).read_bytes()),
            'summary': dict(stats), 'spheres': sphere_records,
            'cores': core_records, 'examples': examples,
            'target_source_realized': False, 'external_enumeration_replayed': False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--certificate', type=Path, default=HERE / 'structure.json')
    args = parser.parse_args()
    result = calculate()
    payload = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.check:
        need(args.certificate.read_text() == payload, 'certificate differs')
    else:
        with args.certificate.open('x') as f:
            f.write(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
