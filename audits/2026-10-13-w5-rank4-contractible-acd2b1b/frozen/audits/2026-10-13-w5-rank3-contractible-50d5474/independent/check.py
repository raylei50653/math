#!/usr/bin/env python3
"""Independent exhaustive parameters, neighbour intervals, rotation and DFS.

No primary-checker import. Parameter words are filtered from four-letter
products; terminal region orders from three-letter products. Edges are built
from vertex-neighbour intervals, not facial triples. A and capped G are both
coloured directly in a fixed order. Every empty cell and full lift is compared.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = '50d5474f2446403f3b3001d5943571184c8c9936'
INCREMENT = {'O': (0, 0), 'B': (1, 0), 'U': (0, 1), 'D': (1, 1)}
TAUS = list(itertools.product(range(4), repeat=5))


def normalise(row):
    seen = {}
    return tuple(seen.setdefault(x, len(seen)) for x in row)


BETAS = sorted({normalise(t) for t in TAUS
                if all(t[i] != t[(i + 1) % 5] for i in range(5))})


def catalogue():
    meta = json.loads((ROOT/'CATALOGUE_INPUT.json').read_text())
    assert meta['base'] == BASE
    raw = (ROOT/'frozen'/meta['path']).read_bytes()
    assert len(raw) == meta['bytes']
    assert hashlib.sha256(raw).hexdigest() == meta['sha256']
    cells = json.loads(raw)
    assert cells['pattern_order'] == list(map(list, BETAS))
    masks = set(map(int, cells['cells']))
    assert len(masks) == 132 and cells['distinct_sigma'] == 132
    return masks


def key(param):
    return json.dumps(param, sort_keys=True, separators=(',', ':'))


def admissible_words(size, gap):
    for word in itertools.product('OBUD', repeat=size):
        valid = True
        for i, letter in enumerate(word):
            # Original private neighbours: path neighbours, plus a second
            # branch neighbour exactly at the two ends of the pentagon fan gap.
            neighbours = (i != 0) + (i != size - 1)
            if gap is not None and i in (gap, gap + 1):
                neighbours += 1
            if neighbours + 2 + sum(INCREMENT[letter]) < 5:
                valid = False
                break
        if valid:
            yield ''.join(word)


def parameters():
    # Different nesting from the primary budget recursion: enumerate full
    # words and complete region orders, then retain exact integral advances.
    for r in range(7, 12):
        for c in (1, 2):
            for a in range(14-2*c-r):
                orders = [''.join(s) for s in itertools.product('BUP', repeat=a+c-1)
                          if s.count('P') == c-1]
                path_sizes = [0] if c == 1 else range(2, r-4)
                for t in path_sizes:
                    size = r-t-3
                    path_words = [''] if not t else list(admissible_words(t, None))
                    for gap in range(size-1):
                        for fan in admissible_words(size, gap):
                            for path in path_words:
                                wb = sum(INCREMENT[s][0] for s in fan+path)
                                wu = sum(INCREMENT[s][1] for s in fan+path)
                                for apex in ('B', 'U'):
                                    for apex_step in (0, 1):
                                        db, du = ((apex_step, 2) if apex == 'B'
                                                  else (2, apex_step))
                                        for after in orders:
                                            if (wb+db+after.count('B') == 5 and
                                                    wu+du+after.count('U') == 5):
                                                yield {'c': c, 'r': r, 'fan': fan,
                                                       'gap': gap, 'apex': apex,
                                                       'apex_step': apex_step,
                                                       'path': path, 'after': after}


def graph_from_neighbours(param):
    es = set()

    def edge(x, y):
        assert x != y
        es.add(tuple(sorted((x, y))))

    for off in (0, 5):
        for i in range(5):
            edge(off+i, off+(i+1) % 5)
    b = u = 0
    label = 10

    def crosscut():
        edge(b % 5, 5+u % 5)

    def strip(word, gap=None):
        nonlocal b, u, label
        xs = list(range(label, label+len(word)))
        label += len(word)
        if gap is not None:
            z, w, t = label, label+1, label+2
            label += 3
        crosscut()
        for i, letter in enumerate(word):
            x = xs[i]
            db, du = INCREMENT[letter]
            for neighbour in {b % 5, (b+db) % 5,
                              5+u % 5, 5+(u+du) % 5}:
                edge(x, neighbour)
            b += db
            u += du
            if i == len(xs)-1:
                continue
            y = xs[i+1]
            if i != gap:
                edge(x, y)
            else:
                for left, right in ((x, z), (z, y), (x, w), (w, t),
                                    (t, y), (z, w), (z, t)):
                    edge(left, right)
                step = param['apex_step']
                if param['apex'] == 'B':
                    for neighbour in {b % 5, (b+step) % 5}:
                        edge(z, neighbour)
                    for neighbour in (5+u % 5, 5+(u+1) % 5):
                        edge(w, neighbour)
                    for neighbour in (5+(u+1) % 5, 5+(u+2) % 5):
                        edge(t, neighbour)
                    b += step
                    u += 2
                else:
                    assert param['apex'] == 'U'
                    for neighbour in {5+u % 5, 5+(u+step) % 5}:
                        edge(z, neighbour)
                    for neighbour in (b % 5, (b+1) % 5):
                        edge(w, neighbour)
                    for neighbour in ((b+1) % 5, (b+2) % 5):
                        edge(t, neighbour)
                    b += 2
                    u += step
        crosscut()

    strip(param['fan'], param['gap'])
    for region in param['after']:
        crosscut()
        if region == 'P':
            strip(param['path'])
        elif region == 'B':
            b += 1
        else:
            assert region == 'U'
            u += 1
        crosscut()
    assert b == u == 5
    assert label == param['r']+10
    return label, sorted(es)


def canonical_cycle(row):
    return min(tuple(row[i:]+row[:i]) for i in range(len(row)))


def rotation_faces(n, edges, faces, rotation):
    adjacency = [set() for _ in range(n)]
    for x, y in edges:
        adjacency[x].add(y)
        adjacency[y].add(x)
    assert len(rotation) == n
    for x in range(n):
        assert len(rotation[x]) == len(set(rotation[x]))
        assert set(rotation[x]) == adjacency[x]
    darts = {(x, y) for x in range(n) for y in adjacency[x]}
    walked = []
    while darts:
        first = min(darts)
        current = first
        cycle = []
        while True:
            assert current in darts
            darts.remove(current)
            x, y = current
            cycle.append(x)
            around = rotation[y]
            current = (y, around[(around.index(x)+1) % len(around)])
            if current == first:
                break
        walked.append(canonical_cycle(cycle))
    assert all(len(f) == len(set(f)) for f in faces)
    assert Counter(walked) == Counter(map(canonical_cycle, faces))
    assert len(set(walked)) == len(walked)
    assert n-len(edges)+len(faces) == 2
    reached, todo = set(), [0]
    while todo:
        x = todo.pop()
        if x not in reached:
            reached.add(x)
            todo.extend(adjacency[x]-reached)
    assert len(reached) == n


def geometry(record, param, n, edges):
    assert record['B'] == list(range(5))
    assert record['U'] == list(range(5, 10))
    assert record['private'] == list(range(10, n))
    assert record['vertices'] == list(range(n))
    assert record['edges'] == list(map(list, edges)), 'original edges mismatch'
    faces = record['faces']
    assert faces[0] == [0, 4, 3, 2, 1]
    assert faces[-1] == list(range(5, 10))
    assert all(len(f) == 3 for f in faces[1:-1])
    rotation_faces(n, edges, faces, record['rotation'])
    assert record['ownership'] == {'outer_face': 0, 'empty_U_face': len(faces)-1,
                                   'centre_after_restoration': n,
                                   'pin_map': list(range(10))}
    wheel_edges = sorted(edges+[(u, n) for u in range(5, 10)])
    assert record['wheel_edges'] == list(map(list, wheel_edges))
    rotation_faces(n+1, wheel_edges, record['wheel_faces'], record['wheel_rotation'])
    wanted_faces = Counter(map(canonical_cycle, faces[:-1]))
    wanted_faces.update(canonical_cycle([5+i, 5+(i+1) % 5, n]) for i in range(5))
    assert Counter(map(canonical_cycle, record['wheel_faces'])) == wanted_faces
    dg = [sum(x in e for e in wheel_edges) for x in range(n+1)]
    private_edges = [e for e in edges if min(e) >= 10]
    df = [sum(x in e for e in private_edges) for x in range(10, n)]
    assert record['degree_G'] == dg and record['degree_F'] == df
    assert all(dg[x] >= 5 for x in range(10, n))
    adjacency = {x: set() for x in range(10, n)}
    for x, y in private_edges:
        adjacency[x].add(y)
        adjacency[y].add(x)
    components = []
    unseen = set(adjacency)
    while unseen:
        reached, todo = set(), [min(unseen)]
        while todo:
            x = todo.pop()
            if x not in reached:
                reached.add(x)
                todo.extend(adjacency[x]-reached)
        unseen -= reached
        components.append(reached)
    assert set(map(frozenset, record['components'])) == set(map(frozenset, components))
    c, r = len(components), n-10
    ranks = sorted(sum(x in comp and y in comp for x, y in private_edges)
                   -len(comp)+1 for comp in components)
    assert ranks == ([3] if c == 1 else [0, 3])
    h = sum(all(x >= 10 for x in f) for f in faces[1:-1])
    a = sum(all(x < 10 for x in f) for f in faces[1:-1])
    p = sum(x < 5 <= y < 10 for x, y in edges)
    m = sum(any(x < 5 for x in f) and any(5 <= x < 10 for x in f)
            and any(x >= 10 for x in f) for f in faces[1:-1])
    assert record['counts'] == {'c': c, 'r': r, 't_P': h, 'a': a,
                                 'p': p, 'M': m, 'rho': len(private_edges)-r+c}
    assert c == param['c'] and r == param['r']
    assert len(private_edges)-r+c == 3
    assert h == 3 and m == 2*c and p == a+c
    assert sum(dg[10:n]) == 4*r+13-c-p
    for x in range(10, n):
        for off in (0, 5):
            ns = [y-off for y in range(off, off+5) if tuple(sorted((x, y))) in edges]
            assert len(ns) <= 2
            if len(ns) == 2:
                assert (ns[1]-ns[0]) % 5 in (1, 4)


def colour(n, edges, beta, capped):
    adjacency = [set() for _ in range(n+int(capped))]
    for x, y in edges:
        adjacency[x].add(y)
        adjacency[y].add(x)
    if capped:
        for u in range(5, 10):
            adjacency[u].add(n)
            adjacency[n].add(u)
    # Literal fixed order; unlike the primary MRV algorithm no dynamic
    # variable choice or transfer through annular support is used.
    order = list(range(5, 10))+([n] if capped else [])+list(range(10, n))
    assignment = list(beta)+[-1]*(len(adjacency)-5)
    answer = []

    def visit(depth):
        if depth == len(order):
            answer.append(''.join(map(str, assignment)))
            return
        x = order[depth]
        forbidden = {assignment[y] for y in adjacency[x]}
        for colour_value in range(4):
            if colour_value not in forbidden:
                assignment[x] = colour_value
                visit(depth+1)
        assignment[x] = -1

    visit(0)
    return sorted(answer)


def verify_rows(record, n, edges):
    assert len(record['rows']) == 10
    mask = 0
    counts = Counter()
    for i, beta in enumerate(BETAS):
        row = record['rows'][i]
        assert row['beta'] == list(beta)
        expected = [[] for _ in range(1024)]
        lifts = colour(n, edges, beta, False)
        for lift in lifts:
            expected[int(lift[5:10], 4)].append(lift)
        assert row['cells'] == expected, 'full A fibres mismatch'
        full_g = colour(n, edges, beta, True)
        assert row['wheel_full_lifts'] == full_g, 'full G lifts mismatch'
        if full_g:
            mask |= 1 << i
        counts['A_full_lifts'] += len(lifts)
        counts['G_full_lifts'] += len(full_g)
        counts['empty_cells'] += sum(not cell for cell in expected)
        counts['cells'] += len(expected)
    assert record['Sigma'] == mask
    return counts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path,
                        default=ROOT/'controls/certificate.jsonl.gz')
    parser.add_argument('--list', action='store_true')
    parser.add_argument('--limit', type=int)
    args = parser.parse_args()
    catalogue_masks = catalogue()
    domain = {key(param): param for param in parameters()}
    types = Counter((p['c'], p['r'], len(p['after'])-(p['c']-1)) for p in domain.values())
    if args.list:
        print(json.dumps({'templates': len(domain),
                          'types': {str(k): v for k, v in sorted(types.items())}}, sort_keys=True))
        return
    visited = set()
    totals = Counter()
    masks = Counter()
    with gzip.open(args.certificate, 'rt') as stream:
        header = json.loads(next(stream))
        assert header['type'] == 'header' and header['base'] == BASE
        assert header['beta_order'] == list(map(list, BETAS))
        assert header['tau_order'] == list(map(list, TAUS))
        for line in stream:
            if args.limit is not None and len(visited) == args.limit:
                break
            record = json.loads(line)
            identity = key(record['parameters'])
            assert identity in domain and identity not in visited
            assert record['key'] == identity
            n, edges = graph_from_neighbours(domain[identity])
            geometry(record, domain[identity], n, edges)
            totals.update(verify_rows(record, n, edges))
            assert record['Sigma'] in catalogue_masks, 'outside frozen K132'
            masks[record['Sigma']] += 1
            visited.add(identity)
            if len(visited) % 100 == 0:
                print(json.dumps({'done': len(visited), 'masks': dict(masks)}), flush=True)
    if args.limit is None:
        assert visited == set(domain), 'incomplete template coverage'
    print(json.dumps({'status': 'PASS independent exact comparison',
                      'templates': len(visited), 'Sigma_counts': dict(masks),
                      **dict(totals),
                      'catalogue_membership': 'every complete mask in frozen K132',
                      'source_realizability': 'not triggered; universal coverage is a paper theorem'},
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
