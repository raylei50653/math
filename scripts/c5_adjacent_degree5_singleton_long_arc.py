#!/usr/bin/env python3
"""Necessary long-arc supports, original-x K5 exclusions, and target joins.

The arbitrary-size triangle/annulus reduction is a paper proof. These records
are whole forbidden-set bounds, not source graphs or endpoint marginals.
"""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from c5_single_spoke_cores import U, Q, TARGETS, PERMS, T4, RHO, PI, transport
from c5_single_spoke_two_two_external import forced_pair
from c5_single_spoke_two_two_minor import verify_minor

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_adjacent_degree5_singleton_long_arc/observations.json'
TABLE = OUT.with_name('support_table.md')
ARC = (1, 2, 3, 4, 0)
UNITS = tuple(product(range(2), range(2)))
SUBSETS = tuple(tuple(i for i in range(5) if mask >> i & 1)
                for mask in range(1, 32))


def unit_supports(kinds, unit):
    r, k = unit
    return tuple(s for s in SUBSETS if (len(s) >= 2 if k == 0 or kinds[r] else len(s) == 1))


def geometries(kinds):
    """Pack four named units along the original b1,b2,b3,b4,b0 arc."""
    result = {}
    for roots in ((0, 1), (1, 0)):
        for flips in product((False, True), repeat=2):
            order = tuple((r, k) for r in roots
                          for k in ((1, 0) if flips[r] else (0, 1)))

            def visit(j, end, assigned):
                if j == 4:
                    lifted = tuple(assigned[u] for u in UNITS)
                    assert lifted not in result
                    result[lifted] = order
                    return
                unit = order[j]
                for support in unit_supports(kinds, unit):
                    if min(support) >= end:
                        visit(j + 1, max(support), assigned | {unit: support})
            visit(0, 0, {})
    return result


def independent_geometries(kinds):
    """Cartesian support choices, then hull separation; no ordered packing."""
    result = set()
    for ss in product(*(unit_supports(kinds, u) for u in UNITS)):
        if not all(max(ss[2*r]) <= min(ss[2*r+1]) or max(ss[2*r+1]) <= min(ss[2*r])
                   for r in range(2)):
            continue
        hulls = [(min(ss[2*r] + ss[2*r+1]), max(ss[2*r] + ss[2*r+1])) for r in range(2)]
        if hulls[0][1] <= hulls[1][0] or hulls[1][1] <= hulls[0][0]:
            result.add(ss)
    return result


def q_side_bans(kind, spoke):
    for residual in ((2,), (3,), (2, 3)):
        lost = {2, 3} - set(residual)
        if kind:  # (2,1), with no root spoke
            for singleton in (0, 1):
                yield (tuple(sorted({1-singleton} | lost)), (singleton,)), residual
        elif Q[spoke] in (0, 1):  # (2), with one original root spoke
            yield (tuple(sorted({1-Q[spoke]} | lost)),), residual


@lru_cache(None)
def valid_q_support(support, forbidden):
    seen = {Q[i] for i in support}
    return (all({p[c] for c in forbidden} == set(forbidden)
                for p in PERMS if all(p[c] == c for c in seen))
            and all(len(seen | {c}) >= 2 for c in forbidden))


@lru_cache(None)
def component_options(arity, support, forbidden, row):
    images, perms = transport(support, forbidden, row)
    assert len(images) <= 1
    if images:
        return dict(exact=True, permutation=perms[0], options=images)
    seen = {row[i] for i in support}
    options = []
    for mask in range(16):
        f = {c for c in U if mask >> c & 1}
        if len(f) <= arity and all({p[c] for c in f} == f for p in PERMS
                                  if all(p[c] == c for c in seen)):
            options.append(tuple(sorted(f)))
    return dict(exact=False, options=tuple(options))


def row_evidence(kinds, supports, bans, row, x_boundary=(0, 1)):
    sides = []
    for r in range(2):
        components = [component_options(2 if k == 0 else 1, supports[2*r+k], f, row)
                      for k, f in enumerate(bans[r])]
        available = U if kinds[r] else U - {row[supports[2*r+1][0]]}
        options = sorted({tuple(sorted(available - set().union(*map(set, fs))))
                          for fs in product(*(c['options'] for c in components))})
        assert options and all(options)
        sides.append(dict(components=components, residual_options=options))
    xlist = U - {row[i] for i in x_boundary}
    joins = []
    for left, right in product(*(s['residual_options'] for s in sides)):
        triples = [(a, b, c) for a, b, c in product(left, right, sorted(xlist))
                   if len({a, b, c}) == 3]
        formula_reject = ((len(left) == len(right) == 1 and left == right)
                          or (len(xlist) == 2 and set(left) <= xlist and set(right) <= xlist))
        assert bool(triples) != formula_reject
        joins.append(dict(residuals=(left, right), witness=triples[0] if triples else None))
    accepted = {j['witness'] is not None for j in joins}
    status = 'accept' if accepted == {True} else 'reject' if accepted == {False} else 'unresolved'
    return dict(row=row, status=status, x_list=sorted(xlist), sides=sides, joins=joins)


def port_rotations(kinds, order):
    """Retain both binary contact orientations on each original root."""
    result = []
    for flips in product((False, True), repeat=2):
        words = []
        for r, k in order:
            name = ('z', 'w')[r]
            if k == 0:
                word = (name + 'u', name + 'v')
                words.extend(reversed(word) if flips[r] else word)
            else:
                words.append(name + ('a' if kinds[r] else '_spoke'))
        result.append(words)
    return result


def k5_witness(supports, bans):
    for r in range(2):
        pair = forced_pair(supports[2*r], bans[r][0])
        if pair is not None and (landings := sorted({0, 1} - set(pair))):
            root = ('z', 'w')[r]
            return dict(root=root, component=root + 'C2', contacts=(root+'u', root+'v'),
                        forbidden=bans[r][0], tether_pair=pair,
                        original_external_path=(root, 'x', 'b'+str(landings[0])),
                        complement_arc=sorted(set(range(5)) - set(pair)))
    return None


def minor_control(pair, landing, length, cut, style):
    edges = {tuple(sorted((f'b{i}', f'b{(i+1)%5}'))) for i in range(5)}
    edges |= {tuple(sorted(e)) for e in [('z', 'w'), ('z', 'x'), ('w', 'x'),
                                        ('x', 'b0'), ('x', 'b1')]}
    path = [f'v{j}' for j in range(length+1)]
    cycle = ['z'] + path + ['z']
    edges |= {tuple(sorted(e)) for e in zip(cycle, cycle[1:])}
    ends = path[cut:cut+2]
    bags = []
    for v in ends:
        bag = {v}
        for i in pair:
            route = [v, f'b{i}'] if style == 'direct' else [v, v+'_trunk', f'b{i}']
            bag.update(route[:-1])
            edges |= {tuple(sorted(e)) for e in zip(route, route[1:])}
        bags.append(bag)
    bags += [({'z', 'x'} | (set(path) - set(ends))
              | {f'b{i}' for i in range(5) if i not in pair}),
             {f'b{pair[0]}'}, {f'b{pair[1]}'}]
    witnesses = verify_minor(edges, bags)
    # Extra original triangle edges stay outside the chosen Z bag; deleting zx
    # must break this particular witness, though the graph can still be nonplanar.
    try:
        verify_minor(edges - {('x', 'z')}, bags)
    except AssertionError:
        pass
    else:
        raise AssertionError('missing original root-x edge was not detected')
    return dict(tether_pair=pair, external_path=('z', 'x', f'b{landing}'),
                length=length, cut=cut, style=style, edges=sorted(edges),
                branch_sets=[sorted(b) for b in bags], witnesses=witnesses)


def reflection_control(record):
    kinds = record['kinds']
    supports = tuple(tuple(sorted(RHO[i] for i in s)) for s in record['supports'])
    bans = tuple(tuple(tuple(sorted(PI[c] for c in f)) for f in fs) for fs in record['bans'])
    raw_targets = []
    for before in record['targets']:
        row = tuple(PI[before['row'][RHO[i]]] for i in range(5))
        after = row_evidence(kinds, supports, bans, row, (2, 3))
        assert after['status'] == before['status'] == 'accept'
        for old, new in zip(before['sides'], after['sides']):
            assert sorted(tuple(sorted(PI[c] for c in e)) for e in old['residual_options']) == new['residual_options']
        raw_targets.append(row)
    assert raw_targets == [(2, 1, 0, 1, 0), (0, 2, 0, 1, 2)]
    return dict(x_boundary=(2, 3), supports=supports, bans=bans, raw_targets=raw_targets)


def build():
    records, geometry_counts = [], {}
    previous = json.loads((ROOT / 'artifacts/c5_adjacent_degree5_shared_singleton/observations.json').read_text())
    abstract = {}
    for index, entry in enumerate(previous['abstract_relations']):
        if entry['pair'] != [2, 3] or not entry['planar_necessary_retained']:
            continue
        key = tuple((tuple(entry[s]['ports']), tuple(entry[s]['spokes_colors']),
                     tuple(map(tuple, entry[s]['forbidden']))) for s in ('left', 'right'))
        assert key not in abstract
        abstract[key] = index
    for kinds in product((False, True), repeat=2):
        geometry = geometries(kinds)
        assert set(geometry) == independent_geometries(kinds)
        geometry_counts[str(kinds)] = len(geometry)
        for lifted, order in sorted(geometry.items()):
            supports = tuple(tuple(sorted(ARC[i] for i in s)) for s in lifted)
            for left, right in product(q_side_bans(kinds[0], supports[1][0]),
                                       q_side_bans(kinds[1], supports[3][0])):
                if left[1] != (2, 3) and right[1] != (2, 3):
                    continue
                bans = (left[0], right[0])
                if not all(valid_q_support(supports[2*r+k], f)
                           for r in range(2) for k, f in enumerate(bans[r])):
                    continue
                record = dict(id=len(records), kinds=kinds, supports=supports, bans=bans,
                              order=order, lifted_supports=lifted,
                              port_rotations=port_rotations(kinds, order))
                abstract_key = tuple(((2, 1) if kinds[r] else (2,),
                                      () if kinds[r] else (Q[supports[2*r+1][0]],), bans[r])
                                     for r in range(2))
                record['previous_abstract_index'] = abstract[abstract_key]
                assert row_evidence(kinds, supports, bans, Q)['status'] == 'reject'
                witness = k5_witness(supports, bans)
                if witness:
                    record.update(result='source_K5', K5=witness)
                else:
                    for row in T4:
                        evidence = row_evidence(kinds, supports, bans, row)
                        if evidence['status'] == 'reject':
                            record.update(result='source_T4', T4=evidence)
                            break
                    else:
                        record.update(result='both_targets', targets=[row_evidence(kinds, supports, bans, row)
                                                                     for row in TARGETS])
                        assert all(e['status'] == 'accept' for e in record['targets'])
                        assert all(len(fs[0]) == 1 for fs in bans)
                        record['reflection'] = reflection_control(record)
                records.append(record)
    counts = dict(sorted(Counter(r['result'] for r in records).items()))
    assert geometry_counts == {'(False, False)': 376, '(False, True)': 88,
                               '(True, False)': 88, '(True, True)': 8}
    assert len(records) == 692 and counts == {'both_targets': 296, 'source_K5': 356, 'source_T4': 40}
    assert len({(r['kinds'], r['supports'], r['bans']) for r in records}) == len(records)
    keys = {(r['kinds'], r['supports'], r['bans']): r['result'] for r in records}
    for r in records:
        key = (r['kinds'][::-1], r['supports'][2:]+r['supports'][:2], r['bans'][::-1])
        assert keys[key] == r['result']
    controls = [minor_control(pair, landing, length, cut, style)
                for pair in combinations(range(5), 2) if (pair[1]-pair[0]) in (1, 4)
                for landing in sorted({0, 1} - set(pair))
                for length in (1, 3, 5) for cut in range(length)
                for style in ('direct', 'shared_trunk')]
    # Keep the familiar whole-relation failure explicit.
    relation = ((2, 3), (3, 2))
    marginals = tuple(product(*(set(t[j] for t in relation) for j in range(2))))
    assert set.intersection(*map(set, relation)) == {2, 3}
    assert not set.intersection(*map(set, marginals))
    inputs = ['scripts/c5_single_spoke_cores.py', 'scripts/c5_single_spoke_two_two_external.py',
              'scripts/c5_single_spoke_two_two_minor.py',
              'artifacts/c5_adjacent_degree5_shared_singleton/observations.json',
              'artifacts/c5_adjacent_degree5_singleton_sectors/observations.json']
    return dict(schema=1, scope='necessary supports, not source realizations; paper topology not formalized',
                source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                inputs_sha256={p: sha256((ROOT/p).read_bytes()).hexdigest() for p in inputs},
                summary=dict(geometries=geometry_counts, necessary_records=len(records), counts=counts,
                             target_acceptances=592, unresolved_queries=0, K5_controls=len(controls),
                             missing_root_x_controls=len(controls), reflected_target_checks=592,
                             contact_orientations_per_record=4),
                records=records, minor_controls=controls,
                marginal_negative_control=dict(relation=relation, marginal_product=marginals))


def table(data):
    lines = ['# 共鄰單點 {b0,b1} 長弧：必要支援表', '',
             '這是必要資料，不是來源圖枚舉；分量與接點次序見 JSON。', '',
             '| ID | 每側分拆 | z 支援／q 禁色 | w 支援／q 禁色 | 結論 |',
             '| ---: | --- | --- | --- | --- |']
    for r in data['records']:
        parts = ' / '.join('(2,1)' if k else '(2)' for k in r['kinds'])
        desc = []
        for root in range(2):
            terms = [''.join(map(str, r['supports'][2*root+k])) + ':' + ''.join(map(str, f))
                     for k, f in enumerate(r['bans'][root])]
            if not r['kinds'][root]:
                terms.append('spoke=' + str(r['supports'][2*root+1][0]))
            desc.append('; '.join(terms))
        lines.append(f"| {r['id']} | {parts} | {desc[0]} | {desc[1]} | {r['result']} |")
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build()
    outputs = {OUT: json.dumps(data, sort_keys=True, indent=2) + '\n', TABLE: table(data)}
    for path, payload in outputs.items():
        if args.check:
            assert path.read_bytes() == payload.encode(), f'certificate differs: {path}'
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(payload)
    print(json.dumps(data['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
