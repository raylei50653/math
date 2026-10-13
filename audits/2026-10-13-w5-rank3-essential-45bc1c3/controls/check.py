#!/usr/bin/env python3
"""Complete essential private rank-three kernel; coverage in structure/PROOF.md.
Literal faces and full fibres; adapted from the standalone unicyclic checker.
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
BASE = '45bc1c3dc9dacaee1b10df9d64f1c6a27bb0e954'
B, U = list(range(5)), list(range(5, 10))
TAUS = list(map(list, itertools.product(range(4), repeat=5)))
BETAS = [list(map(int, x)) for x in
         ('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')]
STEPS = {'O': (0, 0), 'B': (1, 0), 'D': (1, 1), 'U': (0, 1)}


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
    s = r-2
    choices = ['OBUD' if i in (0, 1) else 'BUD' for i in range(s)]
    for letters in itertools.product(*choices):
        if sum(STEPS[x][0] for x in letters) == 4 and sum(STEPS[x][1] for x in letters) == 4:
            yield ''.join(letters)


def make(word):
    assert 5 <= len(word) <= 10
    assert all(x in ('OBUD' if i in (0,1) else 'BUD') for i,x in enumerate(word))
    assert all(sum(STEPS[x][j] for x in word) == 4 for j in (0,1))
    r, b, u = len(word)+2, 0, 0
    s = len(word)
    n = 10+r
    qB, qU = n-2, n-1
    faces = [[0, 4, 3, 2, 1]]
    for i, letter in enumerate(word):
        db, du = STEPS[letter]
        x, y = 10+i, 10+(i+1) % s
        if db:
            faces.append([b % 5, (b+1) % 5, x])
        if du:
            faces.append([5+(u+1) % 5, 5+u % 5, x])
        b, u = b+db, u+du
        if i != 0:
            faces.extend([[b % 5, y, x], [5+u % 5, x, y]])
        else:
            faces.extend([[b % 5, qB, x], [b % 5, (b+1) % 5, qB],
                          [(b+1) % 5, y, qB], [5+u % 5, x, qU],
                          [5+(u+1) % 5, qU, y], [5+(u+1) % 5, 5+u % 5, qU],
                          [x, qB, qU], [y, qU, qB]])
            b, u = b+1, u+1
    assert b == u == 5
    faces.append(U[:])
    edges, rotation = embedding(n, faces)
    private_edges = [e for e in edges if e[0] >= 10]
    expected = [sorted([10+i, 10+(i+1)%s]) for i in range(1,s)]
    expected.extend(sorted(e) for e in [(10,qB),(10,qU),(11,qB),(11,qU),(qB,qU)])
    assert private_edges == sorted(expected)
    wheel_edges = sorted(edges+[[u, n] for u in U])
    wheel_faces = faces[:-1]+[[5+i, 5+(i+1) % 5, n] for i in range(5)]
    we, wr = embedding(n+1, wheel_faces, wheel_edges)
    degree_G = [sum(v in e for e in we) for v in range(n+1)]
    degree_F = [sum(v in e for e in private_edges) for v in range(10,n)]
    assert all(degree_G[x] >= 5 for x in range(10, n))
    assert len(private_edges)-r+1 == 3
    assert len(edges) == 3*r+20 and len(faces)-2 == 2*r+10
    assert all(len(f) == 3 for f in faces[1:-1])
    assert [e for e in edges if e[0] < 10 and e[1] < 10] == sorted(
        [sorted([i,(i+1)%5]) for i in B]+[sorted([5+i,5+(i+1)%5]) for i in B])
    assert sum(degree_G[10:n]) == 4*r+12
    assert sorted(degree_F) == [2]*(r-4)+[3]*4
    assert degree_G[qB] == degree_G[qU] == 5
    assert sum(sorted([qB,v]) in edges for v in B) == 2
    assert sum(sorted([qU,v]) in edges for v in U) == 2
    assert not any(sorted([qB,v]) in edges for v in U)
    assert not any(sorted([qU,v]) in edges for v in B)
    assert sum(all(v >= 10 for v in f) for f in faces[1:-1]) == 2
    assert not any(x in B and y in U for x,y in edges)
    for x in range(10,n):
        for ring in (B,U):
            ns = [v for v in ring if sorted([x,v]) in edges]
            assert 1 <= len(ns) <= 2 or x in (qB,qU)
            assert len(ns) <= 2
            if len(ns) == 2:
                assert (ns[1]-ns[0]) % 5 in (1,4)
    return {'key': word, 'r': r, 'steps': [list(STEPS[s]) for s in word],
            'counts': {'r':r,'c':1,'rho':3,'h':2,'a':0,'p':0,'M':0},
            'vertices': list(range(n)), 'B': B, 'U': U, 'private': list(range(10, n)),
            'faces': faces, 'edges': edges, 'rotation': rotation,
            'wheel_edges': we, 'wheel_faces': wheel_faces, 'wheel_rotation': wr,
            'degree_G': degree_G, 'degree_private': degree_F,
            'ownership': {'outer_face': 0, 'empty_U_face': len(faces)-1,
                          'centre_after_restoration': n, 'pin_map': list(range(10)),
                          'backbone_cycle_order': list(range(10, n-2)),
                          'diamond': {'tip_x':10,'tip_y':11,'qB':qB,'qU':qU}},
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
            'domain': 'r=7..12; backbone cycle r-2; diamond gap 0 adds (1,1); tips O/B/U/D others B/U/D; letter totals (4,4)',
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
        for r in range(7, 13):
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
        assert stats['templates'] == 1283
        assert stats['types'] == {7:22,8:131,9:340,10:440,11:280,12:70}
        assert stats['masks'] == {1023:1283}
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
