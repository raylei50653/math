#!/usr/bin/env python3
"""Complete 70-template forest source kernel. Stdlib, fixed labels, full lifts.

Template completeness is a PAPER lemma in REPORT.md, not inferred from search.
--write exclusively creates evidence; --check is read-only.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
B, U = tuple(range(5)), tuple(range(5, 10))
TAUS = tuple(itertools.product(range(4), repeat=5))


def canonical(t):
    names = {}
    return tuple(names.setdefault(x, len(names)) for x in t)


def proper(t):
    return all(t[i] != t[(i+1) % 5] for i in range(5))


BETAS = tuple(sorted({canonical(t) for t in TAUS if proper(t)}))


def embedding(n, faces):
    darts = Counter((f[i], f[(i+1) % len(f)]) for f in faces for i in range(len(f)))
    assert all(k == 1 and darts[b, a] == 1 for (a, b), k in darts.items())
    edges = sorted({tuple(sorted(e)) for e in darts})
    assert n-len(edges)+len(faces) == 2
    rotations = []
    for v in range(n):
        links = {}
        for f in faces:
            if v in f:
                i = f.index(v)
                assert f[i-1] not in links
                links[f[i-1]] = f[(i+1) % len(f)]
        assert set(links) == set(links.values())
        start = min(links)
        cycle, x = [], start
        while x not in cycle:
            cycle.append(x)
            x = links[x]
        assert x == start and len(cycle) == len(links)
        rotations.append(cycle)
    seen, todo = set(), [0]
    while todo:
        v = todo.pop()
        if v not in seen:
            seen.add(v)
            todo.extend(rotations[v])
    assert len(seen) == n
    return edges, rotations


def make(kind, word):
    # Start beyond the unique all-terminal triangle, if present.
    b, u = (1 if kind == 'B_triangle' else 0), (1 if kind == 'U_triangle' else 0)
    steps = [(1, 1)] + list(word) + [(1, 1)]
    n = 10+len(steps)
    faces = [[0, 4, 3, 2, 1]]
    if kind == 'B_triangle':
        faces.append([0, 1, 5])
    if kind == 'U_triangle':
        faces.append([0, 6, 5])
    faces.append([b % 5, 10, 5+u % 5])
    for i, (db, du) in enumerate(steps):
        x = 10+i
        if db:
            faces.append([b % 5, (b+1) % 5, x])
        if du:
            faces.append([5+(u+1) % 5, 5+u % 5, x])
        b, u = b+db, u+du
        if i+1 < len(steps):
            faces.extend([[b % 5, x+1, x], [5+u % 5, x, x+1]])
    assert b == u == 5
    faces.extend([[5, n-1, 0], list(U)])
    edges, rotation = embedding(n, faces)
    degrees = Counter(v for e in edges for v in e)
    assert all(degrees[v] >= 5 for v in range(10, n))
    assert [e for e in edges if e[0] >= 10] == [(v, v+1) for v in range(10, n-1)]
    return {'kind': kind, 'middle_steps': word, 'vertices': list(range(n)),
            'B': B, 'U': U, 'private': list(range(10, n)),
            'faces': faces, 'edges': edges, 'rotation': rotation,
            'ownership': {'private': 'annulus', 'U_inside': 'empty',
                          'centre_after_restoration': n, 'pin_map': list(range(10))}}


def templates():
    types = [('p1_r8', [(1, 0)]*3+[(0, 1)]*3),
             ('p1_r7', [(1, 0)]*2+[(0, 1)]*2+[(1, 1)]),
             ('B_triangle', [(1, 0)]*2+[(0, 1)]*3),
             ('U_triangle', [(1, 0)]*3+[(0, 1)]*2)]
    for kind, steps in types:
        for word in sorted(set(itertools.permutations(steps))):
            yield make(kind, word)


def lifts(n, edges, beta):
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    colors = list(beta)+[-1]*(n-5)
    result = []

    def dfs(left):
        if not left:
            result.append(''.join(map(str, colors)))
            return
        options = [(tuple(c for c in range(4) if all(colors[w] != c for w in adj[v])), v)
                   for v in left]
        choices, v = min(options, key=lambda cv: (len(cv[0]), -len(adj[cv[1]]), cv[1]))
        for c in choices:
            colors[v] = c
            dfs(left-{v})
        colors[v] = -1

    dfs(set(range(5, n)))
    return sorted(result)


def certificate():
    cat_path = ROOT.parent/'conditional/frozen/cells.json'
    raw = cat_path.read_bytes()
    catalogue = set(map(int, json.loads(raw)['cells']))
    assert len(catalogue) == 132
    graphs = []
    for g in templates():
        n = len(g['vertices'])
        wheel_edges = sorted(g['edges']+[(u, n) for u in U])
        wheel_faces = g['faces'][:-1]+[[5+i, 5+(i+1) % 5, n] for i in range(5)]
        # The empty U face was oriented forward, so new triangle darts match.
        we, wr = embedding(n+1, wheel_faces)
        assert we == wheel_edges
        rows, mask = [], 0
        for i, beta in enumerate(BETAS):
            full = lifts(n, g['edges'], beta)
            cells = [[] for _ in TAUS]
            for eta in full:
                ix = sum(int(eta[5+j])*4**(4-j) for j in range(5))
                cells[ix].append(eta)
            restored = sorted(eta+str(next(iter(set(range(4))-set(map(int, eta[5:10])))))
                              for eta in full if len(set(eta[5:10])) == 3)
            assert restored == lifts(n+1, wheel_edges, beta)
            if restored:
                mask |= 1 << i
            rows.append({'beta': beta, 'cells': cells, 'wheel_full_lifts': restored})
        assert mask in catalogue, (g['kind'], g['middle_steps'], mask)
        g.update({'rows': rows, 'wheel_edges': wheel_edges, 'wheel_faces': wheel_faces,
                  'wheel_rotation': wr, 'Sigma': mask,
                  'status': 'triggered and holds: necessary template; not minimal source'})
        graphs.append(g)
    assert len(graphs) == 70
    return {'base': '19209f4cf68261fdce5e84a7804cfe04ae0957bf',
            'catalogue_sha256': hashlib.sha256(raw).hexdigest(),
            'beta_order': BETAS, 'tau_order': TAUS, 'graphs': graphs,
            'source_minimality': 'not triggered; source exclusion is conditional theorem'}


def summary(cert):
    gs = cert['graphs']
    return {'templates': len(gs), 'types': dict(Counter(g['kind'] for g in gs)),
            'masks': dict(sorted(Counter(g['Sigma'] for g in gs).items())),
            'cells': len(gs)*10240,
            'empty_cells': sum(not c for g in gs for row in g['rows'] for c in row['cells']),
            'H_full_lifts': sum(len(c) for g in gs for row in g['rows'] for c in row['cells']),
            'G_full_lifts': sum(len(row['wheel_full_lifts']) for g in gs for row in g['rows']),
            'catalogue_sha256': cert['catalogue_sha256']}


def main():
    p = argparse.ArgumentParser()
    m = p.add_mutually_exclusive_group(required=True)
    m.add_argument('--write', action='store_true')
    m.add_argument('--check', action='store_true')
    p.add_argument('--certificate', type=Path, default=ROOT/'certificate.json.gz')
    args = p.parse_args()
    cert = certificate()
    # Normalize tuples for the stored JSON comparison.
    data = json.dumps(cert, sort_keys=True, separators=(',', ':')).encode()
    out = summary(cert)
    if args.write:
        with args.certificate.open('xb') as f:
            f.write(gzip.compress(data, mtime=0))
        with (ROOT/'summary.json').open('x') as f:
            json.dump(out, f, indent=2, sort_keys=True)
            f.write('\n')
    else:
        assert gzip.decompress(args.certificate.read_bytes()) == data, 'certificate mismatch'
    print(json.dumps(out, sort_keys=True))


if __name__ == '__main__':
    main()
