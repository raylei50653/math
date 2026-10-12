#!/usr/bin/env python3
"""Finite complete-relation checks; universal topology is proved in REPORT.md."""
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPLITS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))


def norm(word):
    names = {}
    return tuple(names.setdefault(c, len(names)) for c in word)


def proper(word):
    return all(word[i] != word[(i + 1) % len(word)] for i in range(len(word)))


def patterns(n):
    return tuple(sorted({norm(w) for w in it.product(range(4), repeat=n) if proper(w)}))


P4, P5 = patterns(4), patterns(5)
I4, I5 = {p: i for i, p in enumerate(P4)}, {p: i for i, p in enumerate(P5)}


def partitions(xs):
    if not xs:
        yield ()
        return
    x, *tail = xs
    for part in partitions(tail):
        yield ((x,),) + part
        for j in range(len(part)):
            yield part[:j] + ((x,) + part[j],) + part[j + 1:]


def c4_screen():
    obligations = []
    for p in P4:
        row = []
        for split in SPLITS:
            options = set()
            for left in partitions([i for i in range(4) if p[i] in split[0]]):
                for right in partitions([i for i in range(4) if p[i] in split[1]]):
                    blocks = left + right
                    owner = {v: j for j, block in enumerate(blocks) for v in block}
                    if owner[0] == owner[2] and owner[1] == owner[3] and owner[0] != owner[1]:
                        continue
                    if any(any(p[i] in pair and p[(i + 1) % 4] in pair for pair in split)
                           and owner[i] != owner[(i + 1) % 4] for i in range(4)):
                        continue
                    orbit = 0
                    for choice in range(1 << len(blocks)):
                        q = list(p)
                        for j, block in enumerate(blocks):
                            if choice >> j & 1:
                                pair = next(pair for pair in split if p[block[0]] in pair)
                                for i in block:
                                    q[i] = pair[1] if p[i] == pair[0] else pair[0]
                        assert proper(q)
                        orbit |= 1 << I4[norm(q)]
                    options.add(orbit)
            row.append(sorted(options))
        obligations.append(row)
    kempe = [m for m in range(1, 16)
             if all(not (m >> i & 1) or all(any(m & o == o for o in opts) for opts in row)
                    for i, row in enumerate(obligations))]
    exterior = [7, 10, 12, 15]
    necessary = [m for m in kempe if all(m & t for t in exterior)]
    assert kempe == [3, 5, 7, 10, 11, 12, 13, 14, 15]
    assert necessary == [7, 10, 11, 12, 13, 14, 15]
    return dict(pattern_order=P4, obligations=obligations, kempe=kempe,
                exterior_witness_masks=exterior, necessary=necessary)


def member(mask, word, index):
    p = norm(word)
    return p in index and bool(mask >> index[p] & 1)


def crosscut(a, b, start=2, direction=1):
    rows = []
    for p in P5:
        q = [p[(start + direction * j) % 5] for j in range(5)]
        short = [v for v in range(4) if member(a, (q[0], q[1], q[2], v), I4)]
        long = [v for v in range(4) if member(b, (q[2], q[3], q[4], q[0], v), I5)]
        rows.append(dict(short=short, long=long, joint=sorted(set(short) & set(long))))
    mask = sum(1 << j for j, row in enumerate(rows) if row['joint'])
    return mask, rows


def lifts(n, edges, pins):
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    color = [-1] * n
    for v, c in pins.items():
        color[v] = c
    if any(color[u] >= 0 and color[u] == color[v] for u, v in edges):
        return []
    out = []

    def visit():
        uncolored = [v for v in range(n) if color[v] < 0]
        if not uncolored:
            out.append(tuple(color))
            return
        candidates = {v: sorted(set(range(4)) - {color[u] for u in adj[v]}) for v in uncolored}
        v = min(uncolored, key=lambda u: (len(candidates[u]), -len(adj[u]), u))
        for c in candidates[v]:
            color[v] = c
            visit()
        color[v] = -1

    visit()
    return sorted(out)


def cycle(n):
    return {(min(i, (i + 1) % n), max(i, (i + 1) % n)) for i in range(n)}


def complete_mask(n, edges, boundary_patterns):
    return sum(1 << j for j, p in enumerate(boundary_patterns)
               if lifts(n, edges, dict(enumerate(p))))


def build():
    inputs = json.loads((HERE / 'INPUTS.json').read_text())
    for record in inputs['inputs']:
        actual = hashlib.sha256((HERE / 'frozen' / record['path']).read_bytes()).hexdigest()
        assert actual == record['sha256'], record['path']
    data = json.loads((HERE / 'frozen/artifacts/c5_cells/cells.json').read_text())
    assert data['pattern_order'] == [list(p) for p in P5]
    known = sorted(map(int, data['cells']))
    K = set(known)
    assert len(K) == 132
    unions = [a | b for j, a in enumerate(known) for b in known[j:]]
    assert len(unions) == 8778 and set(unions) <= K
    subsets = {str(r): [m for m in known if m & r == m] for r in (933, 941)}
    assert subsets == {'933': [165], '941': [165, 424, 429]}
    pstar = I5[(0, 1, 2, 3, 2)]
    assert all(not (m >> pstar & 1) for vals in subsets.values() for m in vals)
    screen = c4_screen()
    witnesses4 = []
    for name, n, extra in [('cycle', 4, []), ('diagonal02', 4, [(0, 2)]),
                           ('diagonal13', 4, [(1, 3)]),
                           ('wheel', 5, [(i, 4) for i in range(4)])]:
        edges = sorted(cycle(4) | set(extra))
        rows = [lifts(n, edges, dict(enumerate(p))) for p in P4]
        witnesses4.append(dict(name=name, n=n, edges=edges, lifts=rows,
                               mask=sum(1 << i for i, fs in enumerate(rows) if fs)))
    assert sorted(w['mask'] for w in witnesses4) == [7, 10, 12, 15]
    joins = []
    geometries = 0
    negative = None
    for a in screen['necessary']:
        for b in known:
            result, rows = crosscut(a, b)
            assert result in K
            joins.append(dict(short_mask=a, long_mask=b, result=result, fibres=rows))
            for start in range(5):
                for direction in (-1, 1):
                    mask, _ = crosscut(a, b, start, direction)
                    assert mask in K
                    geometries += 1
            if negative is None and a == 7:
                for i, row in enumerate(rows):
                    if row['short'] and row['long'] and not row['joint']:
                        negative = dict(short_mask=a, long_mask=b, row=i, pattern=P5[i], **row)
                        break
    assert len(joins) == 924 and len({r['result'] for r in joins}) == 90
    assert geometries == 9240 and negative is not None
    # Literal short wheel joined to the saved long-patch witness. Full original
    # vertex colorings are enumerated separately from the relational operation.
    b = negative['long_mask']
    witness = data['cells'][str(b)]
    mapping = (4, 0, 1, 2, 5) + tuple(range(7, 7 + witness['k_eff']))
    short_edges = [(2, 3), (3, 4), (4, 5), (2, 5)] + [(u, 6) for u in (2, 3, 4, 5)]
    long_edges = [(mapping[u], mapping[v]) for u, v in cycle(5) | set(map(tuple, witness['edges']))]
    edges = sorted({tuple(sorted(e)) for e in short_edges + long_edges})
    n = 7 + witness['k_eff']
    full = [lifts(n, edges, dict(enumerate(p))) for p in P5]
    actual_mask = sum(1 << j for j, fs in enumerate(full) if fs)
    expected_mask, rows = crosscut(7, b)
    assert actual_mask == expected_mask
    assert [sorted({f[5] for f in fs}) for fs in full] == [r['joint'] for r in rows]
    assert not full[negative['row']]
    literal = dict(n=n, edges=edges, short_cycle=(2, 3, 4, 5),
                   long_cycle=mapping[:5], shared_path=(2, 5, 4),
                   full_lifts=full, complete_mask=actual_mask)
    ring_words = [w for w in it.product(range(4), repeat=5) if proper(w)]
    ring_fibres = [[w for w in ring_words
                    if all(p[i] != w[i] and p[i] != w[(i - 1) % 5] for i in range(5))]
                   for p in P5]
    ring_allowed = [sum({1 << I5[norm(w)] for w in words}) for words in ring_fibres]
    ring = [dict(inner=m, outer=sum(1 << i for i, a in enumerate(ring_allowed) if m & a))
            for m in known]
    assert all(r['outer'] in K for r in ring)
    assert len({r['outer'] for r in ring}) == 11
    arbitrary_ring = [dict(inner=m, outer=sum(1 << i for i, a in enumerate(ring_allowed) if m & a))
                      for m in range(1, 1024)]
    assert all(r['outer'] not in (933, 941) for r in arbitrary_ring)
    assert len({r['outer'] for r in arbitrary_ring}) == 121
    rejected_rows = [I5[p] for p in ((0, 1, 0, 2, 1), (0, 1, 2, 0, 2), (0, 1, 2, 1, 2))]
    forbidden_inner = 0
    for i in rejected_rows:
        forbidden_inner |= ring_allowed[i]
    assert forbidden_inner == 987 and (1023 ^ forbidden_inner) == 36
    assert ring_allowed[pstar] == 960 and ring_allowed[pstar] & forbidden_inner == ring_allowed[pstar]
    ring_obstruction = dict(rejected_rows=rejected_rows, forbidden_inner=forbidden_inner,
                            remaining_inner=1023 ^ forbidden_inner,
                            pstar_required_inner=ring_allowed[pstar])
    spoke_pushes = []
    for m in known:
        for v in range(5):
            output = 0
            for i, p in enumerate(P5):
                for c in range(4):
                    if c in (p[v], p[(v - 1) % 5], p[(v + 1) % 5]):
                        continue
                    q = list(p)
                    q[v] = c
                    if member(m, q, I5):
                        output |= 1 << i
                        break
            assert output in K
            spoke_pushes.append((m, v, output))
    link_words = [w for w in it.product(range(3), repeat=5) if proper(w)]
    link_checks = []
    for w in link_words:
        eq = [i for i in range(5) if w[(i - 1) % 5] == w[(i + 1) % 5]]
        assert len(eq) == 2 and (eq[0] - eq[1]) % 5 in (1, 4)
        link_checks.append(dict(word=w, equal_opposite_spokes=eq))
    assert len(link_checks) == 30
    return dict(schema='neartri-complete-relations-v1', base=inputs['base'],
                pattern_order=P5, union_checks=len(unions), target_subrelations=subsets,
                c4_screen=screen, c4_exterior_witnesses=witnesses4,
                crosscut_joins=joins, crosscut_geometries_checked=geometries,
                independent_fibre_negative=negative, literal_crosscut_control=literal,
                ring_fibres=ring_fibres, ring_allowed_masks=ring_allowed,
                ring_transfers=ring, arbitrary_ring_transfers=arbitrary_ring,
                ring_obstruction=ring_obstruction, spoke_pushes=spoke_pushes, link_checks=link_checks,
                target_source_status='not triggered',
                scope='finite relations, literal complete lifts, and link words; paper topology separate')


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    parser.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    args = parser.parse_args()
    result = build()
    normalized = json.loads(json.dumps(result))
    if args.write:
        with args.certificate.open('x') as f:
            json.dump(result, f, separators=(',', ':'), sort_keys=True)
            f.write('\n')
    else:
        assert json.loads(args.certificate.read_text()) == normalized, 'certificate mismatch'
    print(json.dumps(dict(status='PASS', union_pairs=result['union_checks'],
                          c4_necessary=result['c4_screen']['necessary'],
                          joins=len(result['crosscut_joins']), join_outputs=90,
                          geometries=result['crosscut_geometries_checked'],
                          ring_inputs=len(result['ring_transfers']), ring_outputs=11,
                          arbitrary_ring_inputs=1023, arbitrary_ring_outputs=121,
                          spoke_pushes=len(result['spoke_pushes']), link_words=len(result['link_checks']),
                          literal_control_mask=result['literal_crosscut_control']['complete_mask'],
                          target_source_status=result['target_source_status']), sort_keys=True))


if __name__ == '__main__':
    main()
