#!/usr/bin/env python3
"""Independent unicyclic word generation, edges, and full-graph colouring DFS.

No import of the primary program. Words are selected from all three-letter
words by their two coordinate sums. Edges come from explicit neighbour
intervals, not from the primary program's face construction. Both A and G are
coloured directly, including the actual centre vertex of G.
"""
from collections import Counter
import argparse
import gzip
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STEPS = ((0, 1), (1, 0), (1, 1))
TAUS = list(itertools.product(range(4), repeat=5))


def canonical(row):
    names = {}
    return tuple(names.setdefault(c, len(names)) for c in row)


BETAS = sorted({canonical(row) for row in TAUS
                if all(row[i] != row[(i + 1) % 5] for i in range(5))})


def words():
    for r in range(7, 11):
        for word in itertools.product(STEPS, repeat=r):
            if sum(x for x, _ in word) == sum(y for _, y in word) == 5:
                yield word


def edges_from_intervals(word):
    r = len(word)
    edges = {tuple(sorted((off + i, off + (i + 1) % length)))
             for off, length in ((0, 5), (5, 5), (10, r))
             for i in range(length)}
    b = u = 0
    for i, (db, du) in enumerate(word):
        x = 10 + i
        for neighbour in {b % 5, (b + db) % 5,
                          5 + u % 5, 5 + (u + du) % 5}:
            edges.add((neighbour, x))
        b += db
        u += du
    assert b == u == 5
    assert len(edges) == 3 * r + 20
    degrees = Counter(v for edge in edges for v in edge)
    assert all(degrees[v] in (5, 6) for v in range(10, 10 + r))
    # Source degree is complete G degree. The private induced graph has
    # degree exactly two; testing its degree against five is a category error.
    private = Counter(v for edge in edges if min(edge) >= 10 for v in edge)
    assert set(private.values()) == {2}
    return 10 + r, sorted(edges)


def all_lifts(n, edges, beta, centre):
    adj = [set() for _ in range(n + int(centre))]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    if centre:
        for u in range(5, 10):
            adj[n].add(u)
            adj[u].add(n)
    # Literal fixed variable order, independently of any support transfer.
    order = list(range(5, 10)) + ([n] if centre else []) + list(range(10, n))
    row = list(beta) + [-1] * (len(adj) - 5)
    answer = []

    def visit(depth):
        if depth == len(order):
            answer.append(''.join(map(str, row)))
            return
        vertex = order[depth]
        forbidden = {row[v] for v in adj[vertex]}
        for color in range(4):
            if color not in forbidden:
                row[vertex] = color
                visit(depth + 1)
        row[vertex] = -1

    visit(0)
    return sorted(answer)


def cyclic(row):
    return min(tuple(row[i:] + row[:i]) for i in range(len(row)))


def check_rotation(n, edges, faces, rotation):
    adjacency = [set() for _ in range(n)]
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    assert len(rotation) == n
    for vertex in range(n):
        assert len(rotation[vertex]) == len(set(rotation[vertex]))
        assert set(rotation[vertex]) == adjacency[vertex]
    unused = {(a, b) for a in range(n) for b in adjacency[a]}
    reconstructed = []
    while unused:
        first = min(unused)
        dart = first
        boundary = []
        while True:
            assert dart in unused
            unused.remove(dart)
            a, b = dart
            boundary.append(a)
            neighbours = rotation[b]
            dart = (b, neighbours[(neighbours.index(a) + 1) % len(neighbours)])
            if dart == first:
                break
        reconstructed.append(cyclic(boundary))
    assert sorted(reconstructed) == sorted(map(cyclic, faces))
    assert n - len(edges) + len(faces) == 2
    assert len(set(map(cyclic, faces))) == len(faces)
    assert all(len(set(face)) == len(face) for face in faces)


def check_geometry(g, word, n, edges):
    assert g['B'] == list(range(5))
    assert g['U'] == list(range(5, 10))
    assert g['private'] == list(range(10, n))
    expected_faces = [frozenset(range(5)), frozenset(range(5, 10))]
    b = u = 0
    for i, (db, du) in enumerate(word):
        x = 10 + i
        following = 10 + (i + 1) % len(word)
        if db:
            expected_faces.append(frozenset((b % 5, (b + 1) % 5, x)))
        if du:
            expected_faces.append(frozenset((5 + u % 5, 5 + (u + 1) % 5, x)))
        b += db
        u += du
        expected_faces.extend((frozenset((x, following, b % 5)),
                               frozenset((x, following, 5 + u % 5))))
    assert Counter(map(frozenset, g['faces'])) == Counter(expected_faces)
    # This fixes the actual designated outer B face and empty inner U face,
    # not merely planarity of an abstract graph with two unspecified cycles.
    assert cyclic([0, 4, 3, 2, 1]) in set(map(cyclic, g['faces']))
    assert cyclic(list(range(5, 10))) in set(map(cyclic, g['faces']))
    check_rotation(n, edges, g['faces'], g['rotation'])
    wheel_edges = sorted(edges + [(u, n) for u in range(5, 10)])
    assert g['wheel_edges'] == list(map(list, wheel_edges))
    check_rotation(n + 1, wheel_edges, g['wheel_faces'], g['wheel_rotation'])
    wf = Counter(map(frozenset, g['faces']))
    del wf[frozenset(range(5, 10))]
    wf.update(frozenset((5 + i, 5 + (i + 1) % 5, n)) for i in range(5))
    assert wf == Counter(map(frozenset, g['wheel_faces']))


def compute_graph(word):
    n, edges = edges_from_intervals(word)
    rows = []
    mask = 0
    for index, beta in enumerate(BETAS):
        a_lifts = all_lifts(n, edges, beta, False)
        cells = [[] for _ in TAUS]
        for lift in a_lifts:
            cells[int(lift[5:10], 4)].append(lift)
        g_lifts = all_lifts(n, edges, beta, True)
        if g_lifts:
            mask |= 1 << index
        rows.append({'beta': list(beta), 'cells': cells,
                     'wheel_full_lifts': g_lifts})
    return {'r': len(word), 'steps': list(map(list, word)),
            'vertices': list(range(n)), 'edges': list(map(list, edges)),
            'rows': rows, 'Sigma': mask}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--explore', action='store_true',
                        help='Independent computation before primary certificate exists')
    parser.add_argument('--limit', type=int)
    parser.add_argument('--certificate', type=Path,
                        default=ROOT / 'controls/certificate.jsonl.gz')
    args = parser.parse_args()
    certificate = None
    expected_words = set(words())
    if not args.explore:
        certificate = gzip.open(args.certificate, 'rt')
        header = json.loads(next(certificate))
        assert header['type'] == 'header'
        assert header['base'] == '3097ef5be241b7777451a5ef8a663f3987d6b866'
        assert header['beta_order'] == list(map(list, BETAS))
        assert header['tau_order'] == list(map(list, TAUS))
        inputs = ((tuple(map(tuple, g['steps'])), g)
                  for g in map(json.loads, certificate))
    else:
        inputs = ((word, None) for word in words())
    counts = Counter()
    masks = Counter()
    h_total = g_total = empty_total = 0
    reviewed = set()
    for number, (word, expected) in enumerate(inputs):
        if args.limit is not None and number >= args.limit:
            break
        assert word in expected_words and word not in reviewed
        actual = compute_graph(word)
        if expected is not None:
            letters = {(1, 0): 'B', (1, 1): 'D', (0, 1): 'U'}
            assert expected['key'] == ''.join(letters[step] for step in word)
            for key in ('r', 'steps', 'vertices', 'edges', 'Sigma', 'rows'):
                assert actual[key] == expected[key], (word, key)
            check_geometry(expected, word, len(actual['vertices']),
                           list(map(tuple, actual['edges'])))
        reviewed.add(word)
        counts[len(word)] += 1
        masks[actual['Sigma']] += 1
        for row in actual['rows']:
            h_total += sum(map(len, row['cells']))
            g_total += len(row['wheel_full_lifts'])
            empty_total += sum(not cell for cell in row['cells'])
    if args.limit is None:
        assert dict(counts) == {7: 210, 8: 560, 9: 630, 10: 252}
        assert reviewed == expected_words
    print(json.dumps({
        'status': 'PASS independent computation' if args.explore else 'PASS independent exact comparison',
        'template_count': len(reviewed), 'length_counts': dict(counts),
        'Sigma_counts': dict(masks), 'A_lifts': h_total, 'G_lifts': g_total,
        'full_cells': len(reviewed) * 10240, 'empty_cells': empty_total,
        'source_realizability': 'not triggered; classification is a paper obligation',
        'private_degree_vs_complete_degree': 'triggered and holds',
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
