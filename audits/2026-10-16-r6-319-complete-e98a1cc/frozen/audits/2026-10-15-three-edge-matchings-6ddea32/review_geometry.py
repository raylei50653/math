#!/usr/bin/env python3
"""Read-only independent checks of literal two-star fibres and full-J cubes."""
import gzip
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
GEOMETRY = HERE.parent / '2026-10-15-j-source-geometry-6ddea32'
BRIDGE = HERE.parent / '2026-10-15-route-round4-6ddea32'


def full_colourings(vertices, edges):
    # Different fixed order: hubs first, then reverse lexical boundary order.
    order = ['z', 'm'] + sorted(set(vertices) - {'m', 'z'}, reverse=True)
    adjacency = {v: set() for v in vertices}
    for a, b in edges: adjacency[a].add(b); adjacency[b].add(a)
    assignment, result = {}, []
    def rec(i):
        if i == len(order):
            result.append([assignment[v] for v in vertices]); return
        v = order[i]
        for c in range(4):
            if all(assignment.get(w) != c for w in adjacency[v]):
                assignment[v] = c; rec(i + 1); del assignment[v]
    rec(0)
    return sorted(result)


def review_patch(p):
    vertices, edges, boundary = p['vertices'], p['edges'], p['boundary']
    direct = full_colourings(vertices, edges)
    assert direct == p['all_complete_patch_colourings']
    collected, seen, unequal = [], set(), []
    all_colours = set(range(4))
    for saved in p['all_proper_boundary_fibres_including_empty']:
        row = saved['boundary_row']; key = tuple(row)
        assert key not in seen; seen.add(key)
        assert all(row[i] != row[(i + 1) % len(row)] for i in range(len(row)))
        f = dict(zip(boundary, row))
        pairs, full = [], []
        # Test every hub pair on every retained original edge, not just a
        # palette formula supplied by the other checker.
        for m, z in itertools.product(range(4), repeat=2):
            extended = f | {'m': m, 'z': z}
            if all(extended[a] != extended[b] for a, b in edges):
                pairs.append([m, z]); full.append(list(row) + [m, z])
        assert pairs == saved['all_hub_pairs_including_empty']
        assert full == [r['full_J_patch_colouring'] for r in saved['all_full_lifts']]
        am = sorted(all_colours - {f[v] for v in p['m_link_without_z']})
        az = sorted(all_colours - {f[v] for v in p['z_link_without_m']})
        assert am == saved['A_m'] and az == saved['A_z']
        for details in saved['all_full_lifts']:
            m, z = details['hub_pair']
            r = sorted(all_colours - {m, f['v'], f['w']})
            assert r == details['all_r_lifts'] and len(r) == 1
            palette = {f['p'], f['q']}
            raw_allowed = palette == {f['v'], f['w']} if z == r[0] else bool(palette & ({f['v'], f['w']} - {z}))
            e, ff, g = f['v'] ^ f['w'], f['p'] ^ f['q'], m ^ z
            assert raw_allowed == ((e == ff) == (e == g)) == details['all_r_source_allowed']
        if len(am) == len(az) == 2 and am != az:
            assert len(pairs) == 3 and sorted(m ^ z for m, z in pairs) == [1, 2, 3]
            assert sum(not x['all_r_source_allowed'] for x in saved['all_full_lifts']) == 1
            unequal.append(row)
        collected.extend(full)
    assert len(seen) == 3 ** len(boundary) + 3 * (-1) ** len(boundary)
    assert sorted(collected) == direct
    return {'boundary_length': len(boundary), 'full_count': len(direct),
            'proper_fibres': len(seen), 'empty_fibres': sum(not r['all_full_lifts'] for r in p['all_proper_boundary_fibres_including_empty']),
            'unequal_two_palette_fibres': len(unequal), 'alpha': p['alpha'], 'beta': p['beta']}


def independent_partitions(items):
    seen = set()
    for labels in itertools.product(range(len(items)), repeat=len(items)):
        blocks = tuple(sorted(tuple(items[i] for i, x in enumerate(labels) if x == value) for value in set(labels)))
        seen.add(blocks)
    return seen


def review_bridge(data):
    truth = lambda t: (t[0] == t[1]) == (t[0] == t[2])
    expected = set()
    for values in itertools.product((1, 2, 3), repeat=3):
        if not truth(values): continue
        for pair in itertools.combinations((1, 2, 3), 2):
            active = tuple(i for i, x in enumerate(values) if x in pair)
            for blocks in independent_partitions(active): expected.add((values, pair, blocks))
    actual = set()
    for row in data['combined_cycle_cubes']:
        values, pair = tuple(row['marked_colours']), tuple(row['pair'])
        blocks = tuple(tuple(block) for block in row['blocks'])
        key = (values, pair, tuple(sorted(blocks)))
        assert key not in actual; actual.add(key)
        targets = []
        for mask in range(1 << len(blocks)):
            t = list(values)
            for i, block in enumerate(blocks):
                if mask >> i & 1:
                    for edge in block: t[edge] = pair[1] if t[edge] == pair[0] else pair[0]
            targets.append(t)
        bad = [i for i, t in enumerate(targets) if not truth(t)]
        assert targets == row['all_targets'] and bad == row['forbidden_masks']
        assert row['source_safe'] == (not bad)
        assert bool(bad) == any(not truth(targets[1 << i]) for i in range(len(blocks)))
    assert actual == expected and len(expected) == 117
    rows = []
    for m, v, w, z, p, q in itertools.product(range(4), repeat=6):
        if len({m, v, w}) < 3 or len({z, p, q}) < 3 or m == z: continue
        missing = next(iter(set(range(4)) - {m, v, w}))
        raw = {p, q} == {v, w} if z == missing else bool({p, q} & ({v, w} - {z}))
        values = [v ^ w, p ^ q, m ^ z]
        assert raw == truth(values)
        rows.append(([m, v, w, z, p, q], raw))
    assert rows == [(r['literal_row'], r['source_allowed']) for r in data['proper_rows']]
    assert len(rows) == 432 and sum(allowed for _, allowed in rows) == 240
    return {'proper_rows': len(rows), 'allowed_rows': 240, 'cycle_cubes': len(expected)}


def main():
    geometry = json.loads((GEOMETRY / 'certificate.json').read_text())
    even = json.loads(gzip.decompress((GEOMETRY / 'two-palette.json.gz').read_bytes()))
    bridge = json.loads((BRIDGE / 'full-j-certificate.json').read_text())
    patches = [review_patch(p) for p in geometry['patch_controls']]
    patches.append(review_patch(even['complete_patch']))
    assert [p['unequal_two_palette_fibres'] for p in patches] == [0, 0, 0, 24]
    result = {'status': 'PASS', 'patches': patches, 'full_J_bridge': review_bridge(bridge),
              'weights_independently_verified_in': 'certificate.json primal and weights fields',
              'reviewed_hashes': {str(path): hashlib.sha256(path.read_bytes()).hexdigest()
                                  for path in [GEOMETRY / 'PROOF.md', GEOMETRY / 'REPORT.md',
                                               GEOMETRY / 'check.py', GEOMETRY / 'check_two_palette.py',
                                               GEOMETRY / 'certificate.json', GEOMETRY / 'two-palette.json.gz',
                                               BRIDGE / 'FULL_J_BRIDGE.md', BRIDGE / 'full-j-certificate.json']}}
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__': main()
