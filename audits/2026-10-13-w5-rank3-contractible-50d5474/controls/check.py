#!/usr/bin/env python3
"""Complete pentagon-fan-strip necessary domain; paper coverage in ATTACHMENTS.md.

Self-contained stdlib checker. All edges, rotation, empty cells and full lifts.
--write uses exclusive creation; --check reads immutable evidence.
The MRV/facial-dart methods follow the frozen unicyclic audit, without imports.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = '50d5474f2446403f3b3001d5943571184c8c9936'
B, U = list(range(5)), list(range(5, 10))
BETAS = [list(map(int, x)) for x in
         ('01012', '01021', '01023', '01201', '01202', '01203', '01212', '01213', '01231', '01232')]
TAUS = list(map(list, itertools.product(range(4), repeat=5)))
STEPS = {'O': (0, 0), 'B': (1, 0), 'U': (0, 1), 'D': (1, 1)}


def encoded(obj):
    return (json.dumps(obj, sort_keys=True, separators=(',', ':'))+'\n').encode()


def embedding(n, faces, expected_edges=None):
    assert all(len(f) >= 3 and len(f) == len(set(f)) for f in faces)
    darts = Counter((f[i], f[(i+1) % len(f)]) for f in faces for i in range(len(f)))
    assert all(a != b and 0 <= a < n and 0 <= b < n and k == 1 and darts[b, a] == 1
               for (a, b), k in darts.items()), 'invalid facial darts'
    edges = sorted({tuple(sorted(e)) for e in darts})
    if expected_edges is not None:
        assert edges == [tuple(e) for e in expected_edges], 'original edges mismatch'
    assert n-len(edges)+len(faces) == 2, 'Euler characteristic'
    rotation = []
    for v in range(n):
        link = {}
        for f in faces:
            if v in f:
                i = f.index(v)
                assert f[i-1] not in link
                link[f[i-1]] = f[(i+1) % len(f)]
        assert link and set(link) == set(link.values())
        cycle, w = [], min(link)
        while w not in cycle:
            cycle.append(w)
            w = link[w]
        assert w == cycle[0] and len(cycle) == len(link), 'vertex link'
        rotation.append(cycle)
    seen, todo = set(), [0]
    while todo:
        v = todo.pop()
        if v not in seen:
            seen.add(v)
            todo.extend(rotation[v])
    assert len(seen) == n, 'connectedness'
    return [list(e) for e in edges], rotation


def step_words(size, gap=None):
    choices = []
    for i in range(size):
        d = int(i > 0)+int(i+1 < size)+int(gap is not None and i in (gap, gap+1))
        choices.append([s for s, (b, u) in STEPS.items() if d+2+b+u >= 5])
    for letters in itertools.product(*choices):
        b = sum(STEPS[x][0] for x in letters)
        u = sum(STEPS[x][1] for x in letters)
        if b <= 5 and u <= 5:
            yield ''.join(letters), b, u


def parameters():
    # Start at the cross-edge immediately preceding the unique rank-three fan.
    # Preserve duplicate descriptions: no graph-isomorphism quotient is needed.
    for c in (1, 2):
        for r in range(7, 14-2*c):
            for t in ([0] if c == 1 else range(2, r-4)):
                s = r-t-3
                for gap in range(s-1):
                    for word, wb, wu in step_words(s, gap):
                        for apex in ('B', 'U'):
                            for apex_step in (0, 1):
                                db = wb+(apex_step if apex == 'B' else 2)
                                du = wu+(2 if apex == 'B' else apex_step)
                                paths = [('', 0, 0)] if c == 1 else step_words(t)
                                for path, pb, pu in paths:
                                    ab, au = 5-db-pb, 5-du-pu
                                    a = ab+au
                                    if min(ab, au) < 0 or a > 13-2*c-r:
                                        continue
                                    symbols = 'B'*ab+'U'*au+('P' if c == 2 else '')
                                    for order in sorted(set(itertools.permutations(symbols))):
                                        yield {'c': c, 'r': r, 'fan': word, 'gap': gap,
                                               'apex': apex, 'apex_step': apex_step,
                                               'path': path, 'after': ''.join(order)}


def make(param):
    b = u = 0
    next_vertex = 10
    faces = [[0, 4, 3, 2, 1]]
    private_edges = []
    components = []

    def strip(word, gap=None, apex=None, apex_step=None):
        nonlocal b, u, next_vertex
        xs = list(range(next_vertex, next_vertex+len(word)))
        next_vertex += len(word)
        if gap is not None:
            z, w, t = next_vertex, next_vertex+1, next_vertex+2
            next_vertex += 3
        components.append(xs+([z, w, t] if gap is not None else []))
        faces.append([b % 5, xs[0], 5+u % 5])
        for i, letter in enumerate(word):
            x = xs[i]
            db, du = STEPS[letter]
            if db:
                faces.append([b % 5, (b+1) % 5, x])
            if du:
                faces.append([5+(u+1) % 5, 5+u % 5, x])
            b, u = b+db, u+du
            if i+1 == len(xs):
                continue
            y = xs[i+1]
            if i != gap:
                faces.extend([[b % 5, y, x], [5+u % 5, x, y]])
                private_edges.append(sorted([x, y]))
            else:
                # The apex lies on the short side; the opposite contour has w,t.
                # Reflect every gadget face, not just the U coordinates, for apex U.
                short = (lambda d: (b+d) % 5) if apex == 'B' else (lambda d: 5+(u+d) % 5)
                long = (lambda d: 5+(u+d) % 5) if apex == 'B' else (lambda d: (b+d) % 5)
                fs = [[short(0), z, x], [short(apex_step), y, z],
                      [long(0), x, w], [long(1), w, t], [long(1), long(0), w],
                      [long(2), t, y], [long(2), long(1), t],
                      [x, z, w], [w, z, t], [t, z, y]]
                if apex_step:
                    fs.append([short(0), short(1), z])
                faces.extend(fs if apex == 'B' else [list(reversed(f)) for f in fs])
                private_edges.extend(sorted(e) for e in
                                     [(x, z), (y, z), (z, w), (z, t),
                                      (x, w), (w, t), (t, y)])
                b += apex_step if apex == 'B' else 2
                u += 2 if apex == 'B' else apex_step

        faces.append([5+u % 5, xs[-1], b % 5])

    strip(param['fan'], param['gap'], param['apex'], param['apex_step'])
    for region in param['after']:
        if region == 'B':
            faces.append([b % 5, (b+1) % 5, 5+u % 5])
            b += 1
        elif region == 'U':
            faces.append([b % 5, 5+(u+1) % 5, 5+u % 5])
            u += 1
        else:
            assert region == 'P'
            strip(param['path'])
    assert b == u == 5, 'boundary edge coverage'
    faces.append(U[:])
    n = next_vertex
    edges, rotation = embedding(n, faces)
    assert sorted(private_edges) == [e for e in edges if e[0] >= 10]
    wheel_edges = sorted(edges+[[u, n] for u in U])
    wheel_faces = faces[:-1]+[[5+i, 5+(i+1) % 5, n] for i in range(5)]
    we, wr = embedding(n+1, wheel_faces, wheel_edges)
    degree = [sum(x in e for e in we) for x in range(n+1)]
    pd = [sum(x in e for e in private_edges) for x in range(10, n)]
    for x in range(10, n):
        assert degree[x] >= 5
        for ring in (B, U):
            ns = [v for v in ring if sorted([x, v]) in edges]
            assert len(ns) <= 2
            if len(ns) == 2:
                assert (ns[1]-ns[0]) % 5 in (1, 4)
    # Recompute components from literal private edges, including any tree component.
    unseen, actual_components = set(range(10, n)), []
    while unseen:
        todo, reached = [min(unseen)], set()
        while todo:
            x = todo.pop()
            if x in reached:
                continue
            reached.add(x)
            todo.extend(y if x == z else z for z, y in private_edges if x in (z, y))
        unseen -= reached
        actual_components.append(sorted(reached))
    assert sorted(actual_components) == sorted(sorted(x) for x in components)
    c, r = len(actual_components), n-10
    t_P = sum(all(v >= 10 for v in f) for f in faces[1:-1])
    a = sum(all(v < 10 for v in f) for f in faces[1:-1])
    mixed = sum(any(v in B for v in f) and any(v in U for v in f)
                and any(v >= 10 for v in f) for f in faces[1:-1])
    p = sum(x in B and y in U for x, y in edges)
    assert c == param['c'] and r == param['r'] and len(private_edges)-r+c == 3
    assert t_P == 3 and mixed == 2*c and p == a+c
    assert sum(degree[10:n]) == 4*r+13-c-p
    return {'key': json.dumps(param, sort_keys=True, separators=(',', ':')), 'parameters': param,
            'vertices': list(range(n)), 'B': B, 'U': U, 'private': list(range(10, n)),
            'components': components, 'faces': faces, 'edges': edges, 'rotation': rotation,
            'wheel_faces': wheel_faces, 'wheel_edges': we, 'wheel_rotation': wr,
            'degree_G': degree, 'degree_F': pd,
            'counts': {'r': r, 'c': c, 't_P': t_P, 'a': a, 'p': p, 'M': mixed, 'rho': 3},
            'ownership': {'outer_face': 0, 'empty_U_face': len(faces)-1,
                          'centre_after_restoration': n, 'pin_map': list(range(10))},
            'status': 'triggered and holds: necessary template; minimum source not triggered'}


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
        for color in range(4):
            if opts & (1 << color):
                colors[best] = color
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
            cells[int(eta[5:10], 4)].append(eta)
        restored = sorted(eta+next(c for c in '0123' if c not in eta[5:10])
                          for eta in full if len(set(eta[5:10])) == 3)
        assert restored == lifts(n+1, g['wheel_edges'], beta), 'direct G restoration'
        if restored:
            mask |= 1 << i
        rows.append({'beta': beta, 'cells': cells, 'wheel_full_lifts': restored})
    g.update(rows=rows, Sigma=mask)
    return g


def main():
    ap = argparse.ArgumentParser()
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--list', action='store_true')
    ap.add_argument('--certificate', type=Path, default=ROOT/'certificate.jsonl.gz')
    args = ap.parse_args()
    if args.list:
        counts = Counter()
        for param in parameters():
            g = make(param)
            counts[(param['c'], param['r'], g['counts']['a'])] += 1
        print(json.dumps({str(k): v for k, v in sorted(counts.items())}, sort_keys=True))
        return
    stats = {'templates': 0, 'types': Counter(), 'masks': Counter(), 'cells': 0,
             'empty_cells': 0, 'A_full_lifts': 0, 'G_full_lifts': 0}
    digest, index = hashlib.sha256(), []
    if args.write:
        assert all(not p.exists() for p in (args.certificate, ROOT/'summary.json', ROOT/'templates.json'))
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
        accept({'type': 'header', 'base': BASE, 'beta_order': BETAS, 'tau_order': TAUS,
                'domain': 'complete necessary contractible rank-three pentagon fan strips; paper coverage first',
                'source_minimality': 'not triggered'})
        for param in parameters():
            g = fill(make(param))
            accept(g)
            stats['templates'] += 1
            typ = f"c{param['c']}_r{param['r']}_a{g['counts']['a']}"
            stats['types'][typ] += 1
            stats['masks'][g['Sigma']] += 1
            stats['cells'] += 10240
            stats['empty_cells'] += sum(not cell for row in g['rows'] for cell in row['cells'])
            stats['A_full_lifts'] += sum(len(cell) for row in g['rows'] for cell in row['cells'])
            stats['G_full_lifts'] += sum(len(row['wheel_full_lifts']) for row in g['rows'])
            index.append({'parameters': param, 'Sigma': g['Sigma'],
                          'graph_sha256': hashlib.sha256(encoded(g)).hexdigest()})
            if stats['templates'] % 100 == 0:
                print(json.dumps({'done': stats['templates'], 'masks': stats['masks']}), flush=True)
        if not args.write:
            assert not stream.read(1), 'extra certificate record'
    finally:
        stream.close()
        if raw:
            raw.close()
    stats = json.loads(json.dumps(stats))
    stats['mathematical_sha256'] = digest.hexdigest()
    for filename, obj in [('summary.json', stats), ('templates.json', index)]:
        target = ROOT/filename
        if args.write:
            with target.open('x') as f:
                json.dump(obj, f, sort_keys=True, indent=2)
                f.write('\n')
        else:
            assert json.loads(target.read_text()) == obj
    print(json.dumps(stats, sort_keys=True))


if __name__ == '__main__':
    main()
