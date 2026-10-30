#!/usr/bin/env python3
"""Independent finite-input review: vertex cuts, bit-domain fibres, Kahn peeling.

No imports from the search producer. Catalogue completeness is not certified:
this checks precisely the stored rotations, centers and literal ABACD fibres.
"""
import argparse
from collections import deque
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'audits/2026-10-30-c5-period4-s5'


def bits(mask):
    while mask:
        b = mask & -mask
        yield b.bit_length() - 1
        mask ^= b


def connected_parts(adj, remaining):
    answer = []
    while remaining:
        found = frontier = remaining & -remaining
        while frontier:
            neighbors = 0
            for u in bits(frontier):
                neighbors |= adj[u]
            frontier = neighbors & remaining & ~found
            found |= frontier
        answer.append(found)
        remaining &= ~found
    return answer


def graph_check(line, record):
    size, raw = line.split()
    rotation = [[ord(c) - 97 for c in row] for row in raw.split(',')]
    n = len(rotation)
    assert n == int(size)
    adj = [sum(1 << x for x in row) for row in rotation]
    assert all(len(row) == len(set(row)) and u not in row and len(row) >= 5
               for u, row in enumerate(rotation))
    assert all(u in rotation[v] for u, row in enumerate(rotation) for v in row)
    assert len(connected_parts(adj, (1 << n) - 1)) == 1
    # Face permutation on directed edges; each orbit must be a triangle.
    next_arc = {(u, v): (v, rotation[v][(rotation[v].index(u) + 1) % len(rotation[v])])
                for u, row in enumerate(rotation) for v in row}
    unseen, faces = set(next_arc), 0
    while unseen:
        start = next(iter(unseen))
        orbit, arc = [], start
        while arc not in orbit:
            orbit.append(arc)
            unseen.remove(arc)
            arc = next_arc[arc]
        assert arc == start and len(orbit) == 3
        faces += 1
    assert n - len(next_arc) // 2 + faces == 2
    # In a spherical triangulation, deleting a separating short cycle splits
    # its two nonempty open sides. Absence of shorter separators ensures that
    # each side of a separating C5 is connected (otherwise a <=4 separator).
    counts, bad34, bad5 = {3: 0, 4: 0, 5: 0}, [], []
    whole = (1 << n) - 1
    for start in range(n):
        def walk(path, used):
            last = path[-1]
            if len(path) >= 3 and adj[last] & (1 << start) and path[1] < last:
                k = len(path)
                counts[k] += 1
                components = connected_parts(adj, whole & ~used)
                if len(components) > 1:
                    if k <= 4:
                        bad34.append(tuple(path))
                    else:
                        assert len(components) == 2, 'Requires absence of shorter separators'
                        if min(c.bit_count() for c in components) > 1:
                            bad5.append(tuple(path))
            if len(path) < 5:
                for x in bits(adj[last] & ~used & ~((1 << (start + 1)) - 1)):
                    walk(path + [x], used | (1 << x))
        walk([start], 1 << start)
    claimed = record['topology']
    assert list(map(len, rotation)) == claimed['degrees']
    assert counts == {int(k): v for k, v in claimed['short_cycle_counts'].items()}
    assert not bad34 and not claimed['separating34']
    assert {frozenset(c) for c in bad5} == {frozenset(r['cycle']) for r in claimed['forbidden5']}
    legal = not bad5
    assert legal == claimed['legal']
    return rotation, adj, legal


def check_center(rotation, full_adj, center, claimed):
    n, boundary = len(rotation), rotation[center]
    assert boundary == claimed['boundary'] and len(boundary) == 5
    all_o = ((1 << n) - 1) ^ (1 << center)
    adj = [a & all_o for a in full_adj]
    boundary_mask = sum(1 << b for b in boundary)
    domains, classes = [15] * n, [0] * 4
    todo = all_o & ~boundary_mask
    for v, color in zip(boundary, (0, 1, 0, 2, 3)):
        domains[v] = 1 << color
        classes[color] |= 1 << v
        for w in bits(adj[v] & todo):
            domains[w] &= ~(1 << color)
    states, partial = set(), {}

    def step(old):
        masks = list(old)
        for a, b, j in ((0, 3, 2), (1, 3, 4), (1, 2, 1), (0, 2, 3), (0, 3, 0)):
            active = masks[a] | masks[b]
            found = frontier = 1 << boundary[j]
            while frontier:
                neighborhood = 0
                for x in bits(frontier):
                    neighborhood |= adj[x]
                frontier = neighborhood & active & ~found
                found |= frontier
            if found & boundary_mask != 1 << boundary[j]:
                return None
            masks[a] ^= found
            masks[b] ^= found
        # Color alignment (2,3,1,0), applied to all original vertices.
        return (masks[3], masks[2], masks[0], masks[1])

    def visit(remaining):
        if not remaining:
            c = tuple(classes)
            assert c not in states
            states.add(c)
            h = step(c)
            if h is not None:
                partial[c] = h
            return
        v = min(bits(remaining), key=lambda x: (domains[x].bit_count(), -len(rotation[x]), x))
        rest = remaining ^ (1 << v)
        for color in bits(domains[v]):
            bit, undo, valid = 1 << color, [], True
            for w in bits(adj[v] & rest):
                if domains[w] & bit:
                    undo.append((w, domains[w]))
                    domains[w] ^= bit
                    if not domains[w]:
                        valid = False
            if valid:
                classes[color] |= 1 << v
                visit(rest)
                classes[color] ^= 1 << v
            for w, old in undo:
                domains[w] = old
    visit(todo)
    assert len(states) == claimed['fibre_size']
    assert len(partial) == claimed['complete_rounds']
    assert set(partial.values()) <= states
    indegree = dict.fromkeys(states, 0)
    for target in partial.values():
        indegree[target] += 1
    assert max(indegree.values(), default=0) <= 1
    queue = deque(c for c in states if not indegree[c])
    removed = 0
    while queue:
        c = queue.popleft()
        removed += 1
        if c in partial:
            target = partial[c]
            indegree[target] -= 1
            if not indegree[target]:
                queue.append(target)
    residual = len(states) - removed
    assert residual == sum(claimed['cycle_lengths'])
    # This certificate currently reports no partial-H cycles at all.
    assert residual == 0 and claimed['cycle_lengths'] == []
    return len(states), len(partial)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-order', type=int, default=24)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    source = AUDIT / 'search-certificate.json'
    certificate = json.loads(source.read_text())
    result = []
    for domain in certificate['domains']:
        path = ROOT / domain['input']
        n = int(path.stem[1:])
        if n > args.max_order:
            continue
        assert sha256(path.read_bytes()).hexdigest() == domain['sha256']
        lines = path.read_text().splitlines()
        assert len(lines) == len(domain['records'])
        centers, fibers, rounds, legal_count = 0, 0, 0, 0
        for j, (line, record) in enumerate(zip(lines, domain['records'])):
            assert j == record['graph']
            rotation, adj, legal = graph_check(line, record)
            if legal:
                legal_count += 1
                claimed = {r['center']: r for r in record['centers']}
                assert set(claimed) == {v for v, row in enumerate(rotation) if len(row) == 5}
                for center, row in claimed.items():
                    f, r = check_center(rotation, adj, center, row)
                    centers += 1
                    fibers += f
                    rounds += r
            else:
                assert not record['centers']
            if (j + 1) % 500 == 0:
                print(f'independent n{n}: {j + 1}/{len(lines)}', flush=True)
        result.append(dict(n=n, graphs=len(lines), legal=legal_count, centers=centers,
                           fixed_literal_fibres=fibers, complete_rounds=rounds, cycles=0))
        print(json.dumps(result[-1], sort_keys=True), flush=True)
    output = dict(status='INDEPENDENT SEARCH REVIEW OK', producer_imports=False,
                  method='vertex-deletion separators; bit-domain full fibres; bitset full components; Kahn cycle peeling',
                  search_certificate_sha256=sha256(source.read_bytes()).hexdigest(),
                  max_order=args.max_order, domains=result)
    target = AUDIT / f'search-independent-n{args.max_order}.json'
    encoded = json.dumps(output, indent=2) + '\n'
    if args.check:
        assert target.read_text() == encoded
    else:
        target.write_text(encoded)


if __name__ == '__main__':
    main()
