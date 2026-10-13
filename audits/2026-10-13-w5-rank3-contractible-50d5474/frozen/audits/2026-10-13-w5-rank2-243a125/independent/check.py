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
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = '243a125a80e4d8de40957f59d8da0bdbc974cf69'
INCREMENT = {'O': (0, 0), 'B': (1, 0), 'U': (0, 1), 'D': (1, 1)}
TAUS = list(itertools.product(range(4), repeat=5))


def normalise(row):
    seen = {}
    return tuple(seen.setdefault(x, len(seen)) for x in row)


BETAS = sorted({normalise(t) for t in TAUS
                if all(t[i] != t[(i + 1) % 5] for i in range(5))})


def key(param):
    return json.dumps(param, sort_keys=True, separators=(',', ':'))


def admissible_words(size, gap):
    for word in itertools.product('OBUD', repeat=size):
        valid = True
        for i, letter in enumerate(word):
            # Original private neighbours: path neighbours, plus a second
            # branch neighbour exactly at the two ends of the diamond gap.
            neighbours = (i != 0) + (i != size - 1)
            if gap is not None and i in (gap, gap + 1):
                neighbours += 1
            if neighbours + 2 + sum(INCREMENT[letter]) < 5:
                valid = False
                break
        if valid:
            yield ''.join(word)


def parameters():
    # Independent ordering and enumeration: choose total vertices first,
    # brute-force all region strings, and test exact rim increments last.
    for r in range(7, 11):
        for c in (1, 2):
            for a in range(13 - 2*c - r):
                orders = [''.join(s) for s in itertools.product('BUP', repeat=a+c-1)
                          if s.count('P') == c-1]
                path_sizes = [0] if c == 1 else range(2, r-3)
                for t in path_sizes:
                    size = r-t-2
                    for gap in range(size-1):
                        for diamond in admissible_words(size, gap):
                            choices = [''] if not t else admissible_words(t, None)
                            for path in choices:
                                wb = 1 + sum(INCREMENT[s][0] for s in diamond+path)
                                wu = 1 + sum(INCREMENT[s][1] for s in diamond+path)
                                for after in orders:
                                    if wb+after.count('B') == wu+after.count('U') == 5:
                                        yield {'c': c, 'r': r, 'diamond': diamond,
                                               'gap': gap, 'path': path, 'after': after}


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
            outer, inner = label, label+1
            label += 2
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
                for left, right in ((x, outer), (x, inner), (outer, inner),
                                    (outer, y), (inner, y)):
                    edge(left, right)
                for neighbour in (b % 5, (b+1) % 5):
                    edge(outer, neighbour)
                for neighbour in (5+u % 5, 5+(u+1) % 5):
                    edge(inner, neighbour)
                b += 1
                u += 1
        crosscut()

    strip(param['diamond'], param['gap'])
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
    h = sum(all(x >= 10 for x in f) for f in faces[1:-1])
    a = sum(all(x < 10 for x in f) for f in faces[1:-1])
    p = sum(x < 5 <= y < 10 for x, y in edges)
    m = sum(any(x < 5 for x in f) and any(5 <= x < 10 for x in f)
            and any(x >= 10 for x in f) for f in faces[1:-1])
    assert record['counts'] == {'c': c, 'r': r, 'h': h, 'a': a,
                                 'p': p, 'M': m, 'rho': len(private_edges)-r+c}
    assert c == param['c'] and r == param['r']
    assert len(private_edges)-r+c == 2
    assert h == 2 and m == 2*c and p == a+c
    assert sum(dg[10:n]) == 4*r+12-c-p
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


def prism_geometry(record):
    edges = {tuple(sorted((off+i, off+(i+1) % 5)))
             for off in (0, 5) for i in range(5)}
    edges.update((i, 5+i) for i in range(5))
    edges = sorted(edges)
    assert record['key'] == 'prism'
    assert record['vertices'] == list(range(10))
    assert record['B'] == list(range(5)) and record['U'] == list(range(5, 10))
    assert record['private'] == []
    assert record['edges'] == list(map(list, edges))
    expected_faces = [[0, 4, 3, 2, 1]]
    expected_faces += [[i, (i+1) % 5, 5+(i+1) % 5, 5+i] for i in range(5)]
    expected_faces += [list(range(5, 10))]
    assert record['faces'] == expected_faces
    rotation_faces(10, edges, expected_faces, record['rotation'])
    assert record['ownership'] == {'outer_face': 0, 'empty_U_face': 6,
                                   'centre_after_restoration': 10,
                                   'pin_map': list(range(10))}
    wheel_edges = sorted(edges+[(u, 10) for u in range(5, 10)])
    assert record['wheel_edges'] == list(map(list, wheel_edges))
    wheel_faces = expected_faces[:-1]+[[5+i, 5+(i+1) % 5, 10] for i in range(5)]
    assert record['wheel_faces'] == wheel_faces
    rotation_faces(11, wheel_edges, wheel_faces, record['wheel_rotation'])
    return 10, edges


def representatives(representative_path, source_path, expected_domain):
    with gzip.open(representative_path, 'rt') as stream:
        cert = json.load(stream)
    assert cert['base'] == BASE
    assert cert['beta_order'] == list(map(list, BETAS))
    assert cert['tau_order'] == list(map(list, TAUS))
    assert len(cert['representatives']) == 4
    expected = {639: ('BU', 'BBBUUU'), 959: ('BD', 'BUUBU'),
                1021: ('UU', 'BBUBBU')}
    by_mask = {}
    stats = Counter()
    for graph in cert['representatives']:
        mask = graph['Sigma']
        assert mask not in by_mask
        if mask == 1023:
            n, edges = prism_geometry(graph)
        else:
            word, order = expected[mask]
            param = {'r': 4, 'c': 1, 'diamond': word, 'gap': 0, 'path': '', 'after': order}
            assert graph['parameters'] == param
            assert graph['key'] == key(param)
            n, edges = graph_from_neighbours(param)
            geometry(graph, param, n, edges)
        stats.update(verify_rows(graph, n, edges))
        by_mask[mask] = graph
    assert set(by_mask) == {639, 959, 1021, 1023}
    transfers = {entry['source_key']: entry for entry in cert['transfers']}
    assert len(transfers) == len(cert['transfers']) == len(expected_domain)
    assert set(transfers) == expected_domain
    witness = cert['strength_counterexample']
    assert witness['status'] == 'counterexample'
    assert witness['claim'] == 'equal Sigma implies equal R3'
    assert witness['Sigma'] == 1023
    assert len(witness['tau']) == 5 and len(set(witness['tau'])) == 3
    witness_checked = False
    distribution, reductions = Counter(), Counter()
    with gzip.open(source_path, 'rt') as stream:
        next(stream)
        for line in stream:
            source = json.loads(line)
            entry = transfers[source['key']]
            rep = by_mask[source['Sigma']]
            r, rp = len(source['private']), len(rep['private'])
            assert entry['Sigma'] == source['Sigma'] == rep['Sigma']
            assert (entry['r'], entry['r_prime'], entry['k'], entry['k_prime'], entry['delta_k']) == \
                (r, rp, r+6, rp+6, r-rp)
            assert rp < r
            assert entry['pin_map'] == list(range(10))
            assert entry['preservation'] == 'complete Sigma only'
            assert len(entry['rows']) == 10
            for row_index, (left, right, selectors) in enumerate(zip(source['rows'], rep['rows'], entry['rows'])):
                beta = list(BETAS[row_index])
                assert left['beta'] == right['beta'] == selectors['beta'] == beta
                sf, tf = left['wheel_full_lifts'], right['wheel_full_lifts']
                assert bool(sf) == bool(tf)
                # The constant selector on each nonempty full beta fibre is
                # a total map preserving every literal B pin; the reverse
                # map has the same property. Empty rows have no inputs.
                assert selectors['source_selector'] == (sf[0] if sf else None)
                assert selectors['representative_selector'] == (tf[0] if tf else None)
            if source['key'] == witness['source_key']:
                row_index = BETAS.index(tuple(witness['beta']))
                cell_index = TAUS.index(tuple(witness['tau']))
                left = source['rows'][row_index]['cells'][cell_index]
                right = rep['rows'][row_index]['cells'][cell_index]
                assert bool(left) != bool(right)
                assert witness['source_nonempty'] == bool(left)
                assert witness['representative_nonempty'] == bool(right)
                assert witness['source_A_lift'] == (left[0] if left else None)
                assert witness['representative_A_lift'] == (right[0] if right else None)
                witness_checked = True
            distribution[source['Sigma']] += 1
            reductions[r-rp] += 1
    assert witness_checked
    summary = {'representatives': 4, 'source_templates': len(transfers),
               'masks': dict(distribution), 'strict_reductions': dict(reductions),
               'representative_cells': stats['cells'],
               'representative_empty_cells': stats['empty_cells'],
               'representative_A_lifts': stats['A_full_lifts'],
               'representative_G_lifts': stats['G_full_lifts'],
               'actual_minimum_933_941_source': 'not triggered'}
    assert cert['summary'] == json.loads(json.dumps(summary))
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path,
                        default=ROOT/'controls/certificate.jsonl.gz')
    parser.add_argument('--list', action='store_true')
    parser.add_argument('--limit', type=int)
    parser.add_argument('--representatives', type=Path,
                        default=ROOT/'controls/representatives.json.gz')
    args = parser.parse_args()
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
            masks[record['Sigma']] += 1
            visited.add(identity)
            if len(visited) % 100 == 0:
                print(json.dumps({'done': len(visited), 'masks': dict(masks)}), flush=True)
    if args.limit is None:
        assert visited == set(domain), 'incomplete template coverage'
        representative_summary = representatives(args.representatives, args.certificate, set(domain))
    else:
        representative_summary = None
    print(json.dumps({'status': 'PASS independent exact comparison',
                      'templates': len(visited), 'Sigma_counts': dict(masks),
                      **dict(totals),
                      'representatives': representative_summary,
                      'source_realizability': 'not triggered; universal coverage is a paper theorem'},
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
