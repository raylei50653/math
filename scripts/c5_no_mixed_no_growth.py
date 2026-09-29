#!/usr/bin/env python3
"""Replay the short-side no-growth lemma, without old target acceptance flags.

The paper proof uses common ordered side intervals, singleton-ban symmetry,
and adjacent singleton positions of two proper three-colorings of C5.
Finite controls and the existing necessary-support replay are separate layers.
No source graph or new support catalogue is generated.
"""

import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'artifacts/c5_no_mixed_root_transport/observations.json'
OUT = ROOT / 'artifacts/c5_no_mixed_no_growth/observations.json'
U = frozenset(range(4))
Q = (0, 1, 0, 1, 2)
TARGETS = ((0, 1, 0, 2, 1), (0, 1, 2, 1, 2))
PERMS = tuple(permutations(range(4)))
OMEGA = dict(A=2, B=2, C=3, D=4, E=3)


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def subsets(values, cap):
    return tuple(F for n in range(cap + 1) for F in combinations(values, n))


@lru_cache(None)
def invariant_options(colors, cap):
    stabilizer = [pi for pi in PERMS if all(pi[a] == a for a in colors)]
    return tuple(F for F in subsets(tuple(range(4)), cap)
                 if all({pi[a] for a in F} == set(F) for pi in stabilizer))


@lru_cache(None)
def options(support, source_ban, ports, row):
    pp = [pi for pi in PERMS if all(pi[Q[h]] == row[h] for h in support)]
    if pp:
        images = {tuple(sorted(pi[a] for a in source_ban)) for pi in pp}
        assert len(images) == 1
        return tuple(sorted(images))
    return invariant_options(tuple(sorted({row[h] for h in support})), ports)


def residuals(record, row, Fs):
    return {r: U - {row[h] for h in record['root_boundary'][r]}
            - set().union(*(set(F) for c, F in zip(record['components'], Fs, strict=True)
                            if c['root'] == r)) for r in ('z', 'w')}


def singleton_position(row):
    assert len(set(row)) == 3
    return next(h for h, a in enumerate(row) if row.count(a) == 1)


def elementary_controls():
    # All legal short-side layouts, allowing sparse binary support and empty F.
    layouts = []
    for S in ((0, 1), (1, 2), (0, 2), (0, 1, 2)):
        for spokes in combinations(range(3), 2):
            if all(not min(S) < h < max(S) for h in spokes):
                layouts.append(dict(kind='A', supports=[S], spokes=spokes))
    for h in range(3):
        layouts.append(dict(kind='B', supports=[(0, 1), (1, 2)], spokes=(h,)))
    counts, witnesses = Counter(), []
    for triple in product(range(4), repeat=3):
        if triple[0] == triple[1] or triple[1] == triple[2]:
            continue
        for layout in layouts:
            domains = [invariant_options(tuple(sorted({triple[h] for h in S})), 1)
                       for S in layout['supports']]
            for Fs in product(*domains):
                E = U - {triple[h] for h in layout['spokes']} - set().union(*map(set, Fs))
                counts['short_side_assignments'] += 1
                if len(E) != 1:
                    continue
                assert len(set(triple)) == 3
                missing = next(iter(U - set(triple)))
                assert E <= {missing, triple[1]}
                if missing in set().union(*map(set, Fs)):
                    assert layout['kind'] == 'A'
                    assert layout['supports'] == [(0, 1, 2)]
                    assert layout['spokes'] == (0, 2) and E == {triple[1]}
                counts['short_side_singletons'] += 1
                witnesses.append(dict(row=triple, layout=layout, Fs=Fs, E=sorted(E)))
    rows = [row for row in product(range(4), repeat=5)
            if len(set(row)) == 3 and all(row[i] != row[(i + 1) % 5] for i in range(5))]
    assert len(rows) == 120
    for row in rows:
        s = singleton_position(row)
        for start in range(5):
            arc = tuple((start + j) % 5 for j in range(3))
            assert (len({row[h] for h in arc}) == 3) == (s in arc)
            counts['rainbow_arc_controls'] += 1
        for target in rows:
            t = singleton_position(target)
            if (s - t) % 5 not in (1, 4):
                continue
            counts['adjacent_singleton_row_pairs'] += 1
            for start in range(5):
                arc = tuple((start + j) % 5 for j in range(3))
                if all(len({beta[h] for h in arc}) == 3 for beta in (row, target)):
                    assert arc[1] in (s, t)
                    counts['common_rainbow_midpoint_controls'] += 1
    # Dropping common unit order permits a spoke inside the component hull.
    bad = dict(row=[0, 1, 2], component_support=[0, 1, 2], F=[3], spokes=[0, 1], E=[2])
    assert set(bad['E']) == U - set(bad['F']) - {bad['row'][h] for h in bad['spokes']}
    assert not set(bad['E']) <= {3, bad['row'][1]}
    return dict(counts=dict(counts), short_side_witnesses_sha256=digest(witnesses),
                missing_order_negative_control=bad,
                capacity_only_negative_control=dict(E_z=[3], E_w=[3], scope='abstract lists only'))


def geometry(record, saved):
    """Reconstruct the SAME common lift and retain every named unit."""
    pl = saved['saved_placement']
    units = record['units']
    by_name = {u['name']: u for u in units}
    assert len(by_name) == len(units) == len(pl['lifts'])
    assert set(pl['order']) == set(by_name) and len(pl['order']) == len(units)
    ordered = []
    for name in pl['order']:
        u = by_name[name]
        ll = pl['lifts'][u['support_index']]
        assert ll and len(ll) == len(set(ll)) == len(u['support'])
        assert 0 <= min(ll) <= max(ll) <= 5
        assert sorted({(pl['anchor'] + x) % 5 for x in ll}) == u['support']
        ordered.append(dict(name=name, root=u['root'], lifts=ll))
    assert all(max(a['lifts']) <= min(b['lifts']) for a, b in zip(ordered, ordered[1:]))
    assert sum(u['root'] != ordered[i - 1]['root'] for i, u in enumerate(ordered)) == 2
    start = next(i for i, u in enumerate(ordered) if u['root'] != ordered[i - 1]['root'])
    cyclic = [dict(u, lifts=[x + (5 if i < start else 0) for x in u['lifts']])
              for i in list(range(start, len(ordered))) + list(range(start)) for u in [ordered[i]]]
    assert all(max(a['lifts']) <= min(b['lifts']) for a, b in zip(cyclic, cyclic[1:]))
    assert max(cyclic[-1]['lifts']) <= min(cyclic[0]['lifts']) + 5
    intervals, masks = {}, {}
    for r, typ in zip(('z', 'w'), record['family'], strict=True):
        coords = [x for u in cyclic if u['root'] == r for x in u['lifts']]
        lo, hi = min(coords), max(coords)
        assert hi - lo >= OMEGA[typ]
        intervals[r] = [lo, hi]
        masks[r] = sum(1 << ((pl['anchor'] + x) % 5) for x in range(lo, hi))
        assert saved['side_intervals'][r] == dict(lift_interval=[lo, hi], span=hi-lo)
    assert not masks['z'] & masks['w']
    assert sum(hi-lo for lo, hi in intervals.values()) <= 5
    for c in record['components']:
        ll = next(u['lifts'] for u in cyclic if u['name'] == c['name'])
        span = max(ll) - min(ll)
        assert span >= (2 if len(c['Fq']) == 2 else 1)
    short = [r for r in ('z', 'w') if intervals[r][1] - intervals[r][0] == 2]
    assert short
    return dict(anchor=pl['anchor'], ordered_units=cyclic, side_intervals=intervals,
                short_roots=short)


def short_lemma(record, geo, root, row, Fs, E):
    """Check the paper lemma's steps, not only its final disjunction."""
    lo, hi = geo['side_intervals'][root]
    assert hi - lo == 2
    arc = [(geo['anchor'] + x) % 5 for x in range(lo, hi + 1)]
    own = [(c, F) for c, F in zip(record['components'], Fs, strict=True) if c['root'] == root]
    assert all(len(F) <= 1 for c, F in own)
    if len(E) != 1:
        return arc
    assert len({row[h] for h in arc}) == 3
    missing = next(iter(U - set(row)))
    exotic = [c for c, F in own if missing in F]
    if exotic:
        assert len(exotic) == len(own) == 1
        assert set(exotic[0]['support']) == set(arc)
        assert set(record['root_boundary'][root]) == {arc[0], arc[2]}
        assert E == {row[arc[1]]}
    else:
        assert E == {missing}
    return arc


def build():
    raw = SOURCE.read_bytes()
    data = json.loads(raw)
    inputs = {str(SOURCE.relative_to(ROOT)): sha256(raw).hexdigest()}
    for path, expected in data['inputs_sha256'].items():
        assert sha256((ROOT / path).read_bytes()).hexdigest() == expected, path
        inputs[path] = expected
    elementary = elementary_controls()
    records, counts, families = [], Counter(), {}
    for ri, record in enumerate(data['records']):
        comps = record['components']
        source_Fs = [tuple(c['Fq']) for c in comps]
        Eq = residuals(record, Q, source_Fs)
        assert len(Eq['z']) == 1 and Eq['z'] == Eq['w']
        for r in ('z', 'w'):
            assert len(record['root_boundary'][r]) + sum(len(c['Fq']) for c in comps if c['root'] == r) == 3
        for c in comps:
            assert tuple(c['Fq']) in invariant_options(tuple(sorted({Q[h] for h in c['support']})), c['ports'])
        geos = [geometry(record, pl) for pl in record['placements']]
        for geo in geos:
            for root in geo['short_roots']:
                arc = short_lemma(record, geo, root, Q, source_Fs, Eq[root])
                # If the source singleton position were the midpoint, the other
                # side's residual would be invariant under swapping its two
                # unseen colors; it could not equal this singleton.
                assert arc[1] != singleton_position(Q)
                assert singleton_position(Q) in (arc[0], arc[2])
                counts['source_short_sides'] += 1
        queries = []
        for ti, row in enumerate(TARGETS):
            saved_target = record['targets'][ti]
            domains = [options(tuple(c['support']), tuple(c['Fq']), c['ports'], row) for c in comps]
            full = list(product(*domains))
            saved = [tuple(tuple(j['F_by_component'][c['name']]) for c in comps)
                     for j in saved_target['candidates']]
            assert len(saved) == len(set(saved)) and set(saved) == set(full)
            index = {Fs: ji for ji, Fs in enumerate(saved)}
            root = geos[0]['short_roots'][0]
            other = 'w' if root == 'z' else 'z'
            lo, hi = geos[0]['side_intervals'][root]
            arc = [(geos[0]['anchor'] + x) % 5 for x in range(lo, hi + 1)]
            rainbow = len({row[h] for h in arc}) == 3
            if rainbow:
                assert arc[1] == singleton_position(row)
                hidden = [row[arc[1]], next(iter(U - set(row)))]
                other_support = set(record['root_boundary'][other]).union(
                    *(set(c['support']) for c in comps if c['root'] == other))
                assert arc[1] not in other_support
                assert not set(hidden) & {row[h] for h in other_support}
            else:
                hidden = []
            witnesses = []
            for Fs in full:
                if any(len(F) > len(c['Fq']) for c, F in zip(comps, Fs, strict=True)):
                    continue
                E = residuals(record, row, Fs)
                assert all(E.values())  # Capacity, independently of the arc argument.
                for r in ('z', 'w'):
                    if len(E[r]) == 1:
                        assert all(len(F) == len(c['Fq']) for c, F in zip(comps, Fs) if c['root'] == r)
                        pieces = [{row[h]} for h in record['root_boundary'][r]]
                        pieces += [set(F) for c, F in zip(comps, Fs) if c['root'] == r]
                        assert all(not a & b for a, b in combinations(pieces, 2))
                for geo in geos:
                    for short_root in geo['short_roots']:
                        short_lemma(record, geo, short_root, row, Fs, E[short_root])
                if not rainbow:
                    assert len(E[root]) >= 2
                else:
                    a, b = hidden
                    swap = tuple(b if x == a else a if x == b else x for x in range(4))
                    assert {swap[x] for x in E[other]} == E[other]
                    if len(E[root]) == 1:
                        assert E[root] <= set(hidden)
                        assert E[other] != E[root]
                pairs = sorted([a, b] for a, b in product(E['z'], E['w']) if a != b)
                assert pairs
                witnesses.append(dict(join=index[Fs], E={r: sorted(E[r]) for r in ('z', 'w')}, root_pair=pairs[0]))
            mechanism = 'target_midpoint_symmetry' if rainbow else 'target_short_side_not_rainbow'
            queries.append(dict(target=ti+1, row=row, short_root=root, short_arc=arc,
                                mechanism=mechanism, invisible_swap=hidden,
                                ordered_candidate_domain_sha256=digest(saved), no_growth_joins=witnesses))
            metrics = dict(queries=1, all_joins=len(full), no_growth_joins=len(witnesses))
            metrics[mechanism] = 1
            counts.update(metrics)
            families.setdefault(record['family'], Counter()).update(metrics)
        records.append(dict(family=record['family'], record_id=record['record_id'],
                            input_pointer=f'/records/{ri}', input_record_sha256=digest(record),
                            original_record=record['original_record'], geometry=record['geometry'],
                            common_lifts=geos, queries=queries))
    assert counts['queries'] == 4164 and counts['all_joins'] == 11096
    assert counts['no_growth_joins'] == 7848 and counts['source_short_sides'] == 2264
    for path, expected in inputs.items():
        assert sha256((ROOT / path).read_bytes()).hexdigest() == expected
    return dict(schema=1, scope='table-free conditional paper lemma; finite algebra controls and necessary-support replay; '
                'no new target accepts, source exclusions, disk realizability, full Sigma or Lean theorem',
                inputs_sha256=inputs, script_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                elementary_controls=elementary, summary=dict(counts), families=families, records=records)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build()
    raw = (json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()
    if args.check:
        assert OUT.read_bytes() == raw, f'stale artifact: {OUT}'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_bytes(raw)
    print(json.dumps(dict(summary=data['summary'], controls=data['elementary_controls']['counts'],
                          families=data['families']), sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
