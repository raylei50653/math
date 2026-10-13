#!/usr/bin/env python3
"""Complete essential-unicyclic kernel; coverage is proved in structure/STRUCTURE.md.
All 1652 words, literal faces and full fibres; stream one graph at a time.
No imports from prior checkers. --check is read-only, --write refuses overwrites.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = '3097ef5be241b7777451a5ef8a663f3987d6b866'
B, U = list(range(5)), list(range(5, 10))
TAUS = list(map(list, itertools.product(range(4), repeat=5)))
BETAS = [list(map(int, x)) for x in
         ('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')]
STEPS = {'B': (1, 0), 'D': (1, 1), 'U': (0, 1)}


def encoded(obj):
    return (json.dumps(obj, sort_keys=True, separators=(',', ':'))+'\n').encode()


def embedding(n, faces, expected_edges=None):
    darts = Counter((f[i], f[(i+1) % len(f)]) for f in faces for i in range(len(f)))
    assert all(a != b and 0 <= a < n and 0 <= b < n and k == 1 and darts[b, a] == 1
               for (a, b), k in darts.items()), 'invalid facial darts'
    edges = sorted({tuple(sorted(e)) for e in darts})
    if expected_edges is not None:
        assert edges == [tuple(e) for e in expected_edges], 'edges do not match faces'
    assert n-len(edges)+len(faces) == 2, 'not sphere Euler characteristic'
    rotations = []
    for v in range(n):
        link = {}
        for f in faces:
            for i, w in enumerate(f):
                if w == v:
                    assert f[i-1] not in link
                    link[f[i-1]] = f[(i+1) % len(f)]
        assert link and set(link) == set(link.values())
        start = min(link)
        cycle, w = [], start
        while w not in cycle:
            cycle.append(w)
            w = link[w]
        assert w == start and len(cycle) == len(link), 'nonmanifold vertex rotation'
        rotations.append(cycle)
    seen, todo = set(), [0]
    while todo:
        v = todo.pop()
        if v not in seen:
            seen.add(v)
            todo.extend(rotations[v])
    assert len(seen) == n
    return [list(e) for e in edges], rotations


def words(r):
    counts = {'B': r-5, 'D': 10-r, 'U': r-5}
    def visit(prefix):
        if len(prefix) == r:
            yield prefix
        for letter in 'BDU':
            if counts[letter]:
                counts[letter] -= 1
                yield from visit(prefix+letter)
                counts[letter] += 1
    yield from visit('')


def make(word):
    r, b, u = len(word), 0, 0
    n = 10+r
    faces = [[0, 4, 3, 2, 1]]
    for i, letter in enumerate(word):
        db, du = STEPS[letter]
        x, y = 10+i, 10+(i+1) % r
        if db:
            faces.append([b % 5, (b+1) % 5, x])
        if du:
            faces.append([5+(u+1) % 5, 5+u % 5, x])
        b, u = b+db, u+du
        faces.extend([[b % 5, y, x], [5+u % 5, x, y]])
    assert b == u == 5
    faces.append(U[:])
    edges, rotation = embedding(n, faces)
    private_edges = [e for e in edges if e[0] >= 10]
    cycle_edges = sorted([sorted([10+i, 10+(i+1) % r]) for i in range(r)])
    assert private_edges == cycle_edges
    wheel_edges = sorted(edges+[[u, n] for u in U])
    wheel_faces = faces[:-1]+[[5+i, 5+(i+1) % 5, n] for i in range(5)]
    we, wr = embedding(n+1, wheel_faces, wheel_edges)
    degree_G = [sum(v in e for e in we) for v in range(n+1)]
    assert all(degree_G[x] >= 5 for x in range(10, n))
    return {'key': word, 'r': r, 'steps': [list(STEPS[s]) for s in word],
            'vertices': list(range(n)), 'B': B, 'U': U, 'private': list(range(10, n)),
            'faces': faces, 'edges': edges, 'rotation': rotation,
            'wheel_edges': we, 'wheel_faces': wheel_faces, 'wheel_rotation': wr,
            'degree_G': degree_G, 'degree_private': [2]*r,
            'ownership': {'outer_face': 0, 'empty_U_face': len(faces)-1,
                          'centre_after_restoration': n, 'pin_map': list(range(10)),
                          'private_cycle_order': list(range(10, n))},
            'status': 'triggered and holds: necessary template; minimum-source identity not triggered'}


def lifts(n, edges, beta):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    colors = list(beta)+[-1]*(n-5)
    result = []
    def dfs(left):
        if not left:
            result.append(''.join(map(str, colors)))
            return
        best, opts, score = None, None, (5, 0, 0)
        for v in left:
            mask = 15
            for w in adj[v]:
                if colors[w] >= 0:
                    mask &= ~(1 << colors[w])
            trial = (mask.bit_count(), -len(adj[v]), v)
            if trial < score:
                best, opts, score = v, mask, trial
                if not mask:
                    return
        tail = tuple(v for v in left if v != best)
        for c in range(4):
            if opts & (1 << c):
                colors[best] = c
                dfs(tail)
        colors[best] = -1
    dfs(tuple(range(5, n)))
    return sorted(result)


def fill(g):
    n = len(g['vertices'])
    rows, mask = [], 0
    for i, beta in enumerate(BETAS):
        full = lifts(n, g['edges'], beta)
        cells = [[] for _ in TAUS]
        for eta in full:
            ix = int(eta[5:10], 4)
            cells[ix].append(eta)
        restored = sorted(eta+next(c for c in '0123' if c not in eta[5:10])
                          for eta in full if len(set(eta[5:10])) == 3)
        assert restored == lifts(n+1, g['wheel_edges'], beta), 'centre/direct G mismatch'
        if restored:
            mask |= 1 << i
        rows.append({'beta': beta, 'cells': cells, 'wheel_full_lifts': restored})
    g.update(rows=rows, Sigma=mask)
    return g


def header():
    return {'type': 'header', 'base': BASE, 'beta_order': BETAS, 'tau_order': TAUS,
            'domain': 'all linear BD U words: r=7..10; B,U totals 5,5; no (0,0)',
            'source_minimality': 'not triggered; exclusion requires paper completeness'}


def run(args):
    stats = {'templates': 0, 'types': Counter(), 'masks': Counter(), 'cells': 0,
             'empty_cells': 0, 'H_full_lifts': 0, 'G_full_lifts': 0}
    digest = hashlib.sha256()
    index = []
    if args.write:
        assert not args.certificate.exists() and not args.summary.exists() and not args.index.exists(), 'refuse overwrite'
        raw = args.certificate.open('xb')
        stream = gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0)
    else:
        raw = None
        stream = gzip.open(args.certificate, 'rb')
    def accept(record):
        data = encoded(record)
        digest.update(data)
        if args.write:
            stream.write(data)
        else:
            assert stream.readline() == data, 'certificate mismatch: '+str(record.get('key', 'header'))
    try:
        accept(header())
        for r in range(7, 11):
            for word in words(r):
                g = fill(make(word))
                accept(g)
                stats['templates'] += 1
                stats['types'][r] += 1
                stats['masks'][g['Sigma']] += 1
                stats['cells'] += 10240
                stats['empty_cells'] += sum(not c for row in g['rows'] for c in row['cells'])
                stats['H_full_lifts'] += sum(len(c) for row in g['rows'] for c in row['cells'])
                stats['G_full_lifts'] += sum(len(row['wheel_full_lifts']) for row in g['rows'])
                index.append({'key': word, 'r': r, 'Sigma': g['Sigma'],
                              'graph_sha256': hashlib.sha256(encoded(g)).hexdigest()})
            print(json.dumps({'r_complete': r, 'templates_so_far': stats['templates'],
                              'masks': dict(stats['masks'])}, sort_keys=True), flush=True)
        assert stats['templates'] == 1652
        if not args.write:
            assert not stream.read(1), 'extra certificate record'
    finally:
        stream.close()
        if raw:
            raw.close()
    stats = json.loads(json.dumps(stats))
    stats['mathematical_sha256'] = digest.hexdigest()
    if args.write:
        with args.summary.open('x') as f:
            json.dump(stats, f, indent=2, sort_keys=True)
            f.write('\n')
        with args.index.open('x') as f:
            json.dump(index, f, indent=2, sort_keys=True)
            f.write('\n')
    else:
        assert json.loads(args.summary.read_text()) == stats, 'summary mismatch'
        assert json.loads(args.index.read_text()) == index, 'complete template list mismatch'
    print(json.dumps(stats, sort_keys=True), flush=True)


def main():
    p = argparse.ArgumentParser()
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    p.add_argument('--certificate', type=Path, default=ROOT/'certificate.jsonl.gz')
    p.add_argument('--summary', type=Path, default=ROOT/'summary.json')
    p.add_argument('--index', type=Path, default=ROOT/'templates.json')
    run(p.parse_args())


if __name__ == '__main__':
    main()
