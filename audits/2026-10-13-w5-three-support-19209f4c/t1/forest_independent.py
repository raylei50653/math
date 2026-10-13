#!/usr/bin/env python3
"""Independent 70-template edges and fixed-order full graph DFS.

Does not import the primary checker. It generates words by testing all words
over a three-letter alphabet, generates edges from neighbor intervals, and
compares every H fibre and every G full lift with the primary certificate.
"""
from collections import Counter
import gzip
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
B = list(range(5))
U = list(range(5, 10))
COLORS = range(4)


def canonical(row):
    d = {}
    return tuple(d.setdefault(x, len(d)) for x in row)


def make_edges(kind, word):
    # Generate by explicit private neighbor intervals, independently of the
    # primary program's oriented-face construction.
    steps = [(1, 1)] + list(word) + [(1, 1)]
    r = len(steps)
    edges = {tuple(sorted((i, (i + 1) % 5))) for i in range(5)}
    edges |= {tuple(sorted((5 + i, 5 + (i + 1) % 5))) for i in range(5)}
    edges |= {(i, i + 1) for i in range(10, 10 + r - 1)}
    b = int(kind == 'B_triangle')
    u = int(kind == 'U_triangle')
    edges.add((b, 5 + u))
    edges.add((0, 5))
    for i, (db, du) in enumerate(steps):
        x = 10 + i
        for neighbor in {b % 5, (b + db) % 5, 5 + u % 5, 5 + (u + du) % 5}:
            edges.add((neighbor, x))
        b += db
        u += du
    assert b == u == 5
    return 10 + r, sorted(edges)


def full_dfs(n, edges, beta, wheel):
    adjacency = [set() for _ in range(n + int(wheel))]
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    if wheel:
        for u in U:
            adjacency[n].add(u)
            adjacency[u].add(n)
    # Fixed literal order: U, actual center if present, and the private path.
    # This searches G directly; no H-lift color-count filtering is used.
    order = U + ([n] if wheel else []) + list(range(10, n))
    coloring = list(beta) + [-1] * (len(adjacency) - 5)
    answer = []

    def search(k):
        if k == len(order):
            answer.append(''.join(str(c) for c in coloring))
            return
        v = order[k]
        for c in COLORS:
            if any(coloring[w] == c for w in adjacency[v]):
                continue
            coloring[v] = c
            search(k + 1)
            coloring[v] = -1

    search(0)
    return sorted(answer)


def main():
    cert = json.loads(gzip.decompress((ROOT / 'forest/certificate.json.gz').read_bytes()))
    source_graphs = {(g['kind'], tuple(map(tuple, g['middle_steps']))): g for g in cert['graphs']}
    assert len(source_graphs) == len(cert['graphs']) == 70
    betas = [tuple(row) for row in cert['beta_order']]
    proper = [row for row in itertools.product(COLORS, repeat=5)
              if all(row[i] != row[(i + 1) % 5] for i in range(5))]
    assert sorted(set(map(canonical, proper))) == sorted(betas)
    assert len(betas) == 10
    taus = list(itertools.product(COLORS, repeat=5))
    assert cert['tau_order'] == list(map(list, taus))

    types = [
        ('p1_r8', 6, (3, 3)), ('p1_r7', 5, (3, 3)),
        ('B_triangle', 5, (2, 3)), ('U_triangle', 5, (3, 2)),
    ]
    counts = Counter()
    masks = Counter()
    total_h = total_g = total_empty = 0
    reviewed = set()
    for kind, length, target in types:
        for word in itertools.product(((0, 1), (1, 0), (1, 1)), repeat=length):
            if tuple(map(sum, zip(*word))) != target:
                continue
            key = kind, word
            reviewed.add(key)
            g = source_graphs[key]
            n, edges = make_edges(kind, word)
            assert g['vertices'] == list(range(n))
            assert sorted(map(tuple, g['edges'])) == edges
            mask = 0
            for i, beta in enumerate(betas):
                assert g['rows'][i]['beta'] == list(beta)
                h_lifts = full_dfs(n, edges, beta, False)
                cells = [[] for _ in taus]
                for lift in h_lifts:
                    # Base-four parse of the actual named U vector.
                    cell_index = int(lift[5:10], 4)
                    cells[cell_index].append(lift)
                assert cells == g['rows'][i]['cells'], (kind, word, beta, 'H cells')
                g_lifts = full_dfs(n, edges, beta, True)
                assert g_lifts == g['rows'][i]['wheel_full_lifts'], (kind, word, beta, 'G lifts')
                if g_lifts:
                    mask |= 1 << i
                total_h += len(h_lifts)
                total_g += len(g_lifts)
                total_empty += sum(not cell for cell in cells)
            assert mask == g['Sigma'] == 1023
            counts[kind] += 1
            masks[mask] += 1
    assert reviewed == set(source_graphs)
    assert dict(counts) == {'p1_r8': 20, 'p1_r7': 30, 'B_triangle': 10, 'U_triangle': 10}
    assert (total_h, total_g, total_empty) == (18282, 9308, 701956)

    cat = json.loads((ROOT / 'conditional/frozen/cells.json').read_bytes())
    catalogue = set(map(int, cat['cells']))
    assert len(catalogue) == 132 and 1023 in catalogue
    # Extra finite check of all named boundary dihedral transforms. Forest
    # masks are 1023, so their transfer actually requires only 1023 in K.
    for mask in catalogue:
        for shift in range(5):
            for sign in (-1, 1):
                moved = 0
                for i, beta in enumerate(betas):
                    if mask & (1 << i):
                        transformed = canonical(tuple(beta[(shift + sign * j) % 5] for j in range(5)))
                        moved |= 1 << betas.index(transformed)
                assert moved in catalogue
    print(json.dumps({
        'status': 'PASS independent exact comparison',
        'template_count': len(reviewed), 'types': dict(counts), 'masks': dict(masks),
        'full_cells_compared': len(reviewed) * 10240, 'empty_cells': total_empty,
        'H_lifts': total_h, 'G_lifts': total_g,
        'catalogue_dihedral_checks': 1320,
        'source_realizability': 'not triggered; source exclusion depends on paper classification',
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
