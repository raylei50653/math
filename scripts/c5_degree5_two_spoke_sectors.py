#!/usr/bin/env python3
"""Two-spoke necessary sector screen, not a graph-realizability enumeration.

Only transports the SAME component's q forbidden set by color permutations
on its named boundary arc. Unknown rows are left unconstrained.
"""
import argparse
from collections import Counter
from itertools import combinations, permutations, product
from hashlib import sha256
import json
from pathlib import Path

Q = (0, 1, 0, 1, 2)
U = frozenset(range(4))
PERMS = tuple(permutations(range(4)))
ROWS = tuple(b for b in product(range(4), repeat=5)
             if all(b[i] != b[(i+1) % 5] for i in range(5)))
OUT = Path(__file__).resolve().parents[1] / 'artifacts/c5_degree5_two_spoke_sectors/observations.json'


def transport(arc, ban, row):
    witnesses = [p for p in PERMS if all(p[Q[i]] == row[i] for i in arc)]
    images = {tuple(sorted(p[c] for c in ban)) for p in witnesses}
    return images, witnesses


def analyze(spokes, parts, sides, bans):
    i, j = spokes
    arcs = (tuple(range(i, j+1)), tuple(range(j, 5)) + tuple(range(i+1)))
    local = [arcs[s] for s in sides]
    record = dict(spokes=spokes, ports=parts, arcs=local, q_bans=bans)
    for k, (arc, ban) in enumerate(zip(local, bans)):
        images, _ = transport(arc, ban, Q)
        if images != {tuple(ban)}:
            record.update(result='symmetry', component=k,
                          inconsistent_images=sorted(images))
            return record
    # Every full four-color row is tested, not just independently named marginals.
    for b in ROWS:
        if len(set(b)) != 4:
            continue
        forced, evidence = set(), []
        for k, (arc, ban) in enumerate(zip(local, bans)):
            images, witnesses = transport(arc, ban, b)
            assert len(images) <= 1
            if images:
                image, = images
                forced.update(image)
                evidence.append(dict(component=k, permutation=witnesses[0], ban=image))
        available = U - {b[i] for i in spokes}
        if available <= forced:
            record.update(result='T4', row=b, available=sorted(available), evidence=evidence)
            return record
    record['result'] = 'retained'
    return record


def controls(records):
    """Replay existing positive witnesses with independent direct colorings."""
    source = OUT.parents[1] / 'c5_degree5_interfaces/observations.json'
    data = json.loads(source.read_text())
    checked = []
    for w in data['witnesses']:
        if not w['accepts_T4'] or w['port_partition'] != [2, 1]:
            continue
        z = w['z']
        edges = w['edges']
        adj = {v: set() for e in edges for v in e}
        for u, v in edges:
            adj[u].add(v)
            adj[v].add(u)
        spokes = sorted(adj[z] & set(range(5)))
        assert len(spokes) == 2
        pieces = w['patterns'][0]['components']
        pieces = sorted(pieces, key=lambda c: -len(c['ports']))
        q_bans = []
        all_bans = []
        for c in pieces:
            vertices, ports = c['vertices'], c['ports']
            row_bans = []
            for b in ROWS:
                lists = [sorted(U - {b[i] for i in adj[v] if i < 5}) for v in vertices]
                possible = set()
                for colors in product(*lists):
                    f = dict(zip(vertices, colors))
                    if all(f[u] != f[v] for u, v in edges if u in f and v in f):
                        possible.update(U - {f[v] for v in ports})
                row_bans.append(U - possible)
            ban = sorted(row_bans[ROWS.index(Q)])
            assert ban == c['forbidden']
            q_bans.append(ban)
            all_bans.append(row_bans)
        matches = []
        for index, r in enumerate(records):
            if list(r['spokes']) != spokes or r['ports'] != (2, 1) or list(r['q_bans']) != q_bans:
                continue
            if not all(set().union(*(adj[v] & set(range(5)) for v in c['vertices'])) <= set(arc)
                       for c, arc in zip(pieces, r['arcs'])):
                continue
            assert r['result'] == 'retained'
            for k, arc in enumerate(r['arcs']):
                for row_index, b in enumerate(ROWS):
                    images, _ = transport(arc, q_bans[k], b)
                    if images:
                        image, = images
                        assert set(image) == all_bans[k][row_index]
            matches.append(index)
        assert matches
        # Check the complete relation directly, in a single fixed color frame.
        for row_index, b in enumerate(ROWS):
            allowed = U - {b[i] for i in spokes} - set().union(*(x[row_index] for x in all_bans))
            assert bool(allowed) == (b not in {tuple(p[c] for c in Q) for p in PERMS})
        checked.append(dict(source_index=w['source_index'], attachment_compatible_records=matches))
    assert len(checked) == 16
    return dict(source_sha256=sha256(source.read_bytes()).hexdigest(),
                witnesses=checked, full_boundary_rows_per_witness=len(ROWS))


def run():
    records = []
    for spokes in combinations(range(5), 2):
        if Q[spokes[0]] == Q[spokes[1]]:
            continue
        available = sorted(U - {Q[i] for i in spokes})
        for side in range(2):
            records.append(analyze(spokes, (3,), (side,), (available,)))
        for sides in product(range(2), repeat=2):
            for c in available:
                records.append(analyze(spokes, (2, 1), sides,
                                       ([c], sorted(set(available)-{c}))))
    assert len(ROWS) == 240 and len(records) == 80
    # Directly verify every rejection certificate independently of transport().
    for r in records:
        if r['result'] == 'symmetry':
            k = r['component']
            assert any(all(p[Q[i]] == Q[i] for i in r['arcs'][k])
                       and {p[c] for c in r['q_bans'][k]} != set(r['q_bans'][k])
                       for p in PERMS)
        elif r['result'] == 'T4':
            b, blocked = r['row'], set()
            assert len(set(b)) == 4 and b in ROWS
            for e in r['evidence']:
                k, p = e['component'], e['permutation']
                assert tuple(sorted(p)) == tuple(range(4))
                assert all(p[Q[i]] == b[i] for i in r['arcs'][k])
                assert set(e['ban']) == {p[c] for c in r['q_bans'][k]}
                blocked.update(e['ban'])
            assert U - {b[i] for i in r['spokes']} <= blocked
    counts = Counter((','.join(map(str, r['ports'])), r['result']) for r in records)
    return dict(scope='necessary sector conditions only; retained does not imply realizable',
                counts={f'{p}:{s}': n for (p, s), n in sorted(counts.items())},
                positive_controls=controls(records), records=records)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = run()
    payload = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.check:
        assert OUT.read_text() == payload, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(result['counts'], sort_keys=True))


if __name__ == '__main__':
    main()
