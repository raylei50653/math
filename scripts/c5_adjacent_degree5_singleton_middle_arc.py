#!/usr/bin/env python3
"""Replay the necessary {b1,b2} long-arc cover and complete target joins.

Arbitrary source size is covered by the paper triangle/annulus and K5 proofs.
Whole forbidden sets are bounded here; records are not disk realizations.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

import c5_adjacent_degree5_singleton_long_arc as base

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_adjacent_degree5_singleton_middle_arc/observations.json'
TABLE = OUT.with_name('support_table.md')
ARC = (2, 3, 4, 0, 1)
X_BOUNDARY = (1, 2)


def row_evidence(kinds, supports, bans, row):
    return base.row_evidence(kinds, supports, bans, row, X_BOUNDARY)


def k5_witness(supports, bans):
    for r in range(2):
        pair = base.forced_pair(supports[2*r], bans[r][0])
        if pair is not None and (landings := sorted(set(X_BOUNDARY) - set(pair))):
            root = ('z', 'w')[r]
            return dict(root=root, component=root+'C2', contacts=(root+'u', root+'v'),
                        forbidden=bans[r][0], tether_pair=pair,
                        original_external_path=(root, 'x', 'b'+str(landings[0])),
                        complement_arc=sorted(set(range(5)) - set(pair)))
    return None


def minor_control(pair, landing, length, cut, style):
    """Relabel only the topology skeleton, not q or the source support table."""
    old_pair = tuple(sorted((i-1) % 5 for i in pair))
    old = base.minor_control(old_pair, (landing-1) % 5, length, cut, style)

    def vertex(v):
        return 'b'+str((int(v[1:])+1) % 5) if v.startswith('b') else v

    edges = {tuple(sorted(map(vertex, e))) for e in old['edges']}
    bags = [set(map(vertex, b)) for b in old['branch_sets']]
    witnesses = base.verify_minor(edges, bags)
    try:
        base.verify_minor(edges - {('x', 'z')}, bags)
    except AssertionError:
        pass
    else:
        raise AssertionError('missing original root-x edge was not detected')
    assert ('b1', 'x') in edges and ('b2', 'x') in edges
    assert landing in X_BOUNDARY and landing not in pair
    return dict(tether_pair=pair, external_path=('z', 'x', f'b{landing}'),
                length=length, cut=cut, style=style, edges=sorted(edges),
                branch_sets=[sorted(b) for b in bags], witnesses=witnesses)


def reflected_key(record):
    supports = tuple(tuple(sorted(base.RHO[i] for i in s)) for s in record['supports'])
    bans = tuple(tuple(tuple(sorted(base.PI[c] for c in f)) for f in fs)
                 for fs in record['bans'])
    return record['kinds'], supports, bans


def reflection_control(record, reflected):
    kinds, supports, bans = reflected_key(record)
    assert reflected['order'] == record['order'][::-1]
    assert reflected['lifted_supports'] == tuple(tuple(sorted(4-i for i in s))
                                                for s in record['lifted_supports'])
    assert sorted(reflected['port_rotations']) == sorted(w[::-1] for w in record['port_rotations'])
    targets = []
    for before in record['targets']:
        row = tuple(base.PI[before['row'][base.RHO[i]]] for i in range(5))
        after = row_evidence(kinds, supports, bans, row)
        assert after['status'] == before['status'] == 'accept'
        assert after['x_list'] == sorted(base.PI[c] for c in before['x_list'])
        for old, new in zip(before['sides'], after['sides']):
            assert sorted(tuple(sorted(base.PI[c] for c in e))
                          for e in old['residual_options']) == new['residual_options']
        targets.append(after)
    assert [e['row'] for e in targets] == [(2, 1, 0, 1, 0), (0, 2, 0, 1, 2)]
    return dict(record_id=reflected['id'], targets=targets)


def x_list_controls():
    """Reusing q's x list at p2 changes both acceptance directions."""
    controls = []
    for left, right in (((0,), (3,)), ((2,), (3,))):
        joins = []
        for xlist in ((0, 3), (2, 3)):
            joins.append([t for t in product(left, right, xlist) if len(set(t)) == 3])
        assert bool(joins[0]) != bool(joins[1])
        controls.append(dict(residuals=(left, right), correct_x_list=(0, 3),
                             correct_joins=joins[0], stale_q_x_list=(2, 3), stale_joins=joins[1]))
    return controls


def build():
    previous = json.loads((ROOT / 'artifacts/c5_adjacent_degree5_shared_singleton/observations.json').read_text())
    abstract = {}
    for index, entry in enumerate(previous['abstract_relations']):
        if entry['pair'] == [2, 3] and entry['planar_necessary_retained']:
            key = tuple((tuple(entry[s]['ports']), tuple(entry[s]['spokes_colors']),
                         tuple(map(tuple, entry[s]['forbidden']))) for s in ('left', 'right'))
            assert key not in abstract
            abstract[key] = index
    records, geometry_counts = [], {}
    for kinds in product((False, True), repeat=2):
        geometry = base.geometries(kinds)
        assert set(geometry) == base.independent_geometries(kinds)
        geometry_counts[str(kinds)] = len(geometry)
        for lifted, order in sorted(geometry.items()):
            supports = tuple(tuple(sorted(ARC[i] for i in s)) for s in lifted)
            for left, right in product(base.q_side_bans(kinds[0], supports[1][0]),
                                       base.q_side_bans(kinds[1], supports[3][0])):
                if left[1] != (2, 3) and right[1] != (2, 3):
                    continue
                bans = (left[0], right[0])
                if not all(base.valid_q_support(supports[2*r+k], f)
                           for r in range(2) for k, f in enumerate(bans[r])):
                    continue
                key = tuple(((2, 1) if kinds[r] else (2,),
                             () if kinds[r] else (base.Q[supports[2*r+1][0]],), bans[r])
                            for r in range(2))
                record = dict(id=len(records), kinds=kinds, supports=supports, bans=bans,
                              order=order, lifted_supports=lifted,
                              port_rotations=base.port_rotations(kinds, order),
                              previous_abstract_index=abstract[key])
                assert row_evidence(kinds, supports, bans, base.Q)['status'] == 'reject'
                witness = k5_witness(supports, bans)
                if witness:
                    record.update(result='source_K5', K5=witness)
                else:
                    for row in base.T4:
                        evidence = row_evidence(kinds, supports, bans, row)
                        if evidence['status'] == 'reject':
                            record.update(result='source_T4', T4=evidence)
                            break
                    else:
                        targets = [row_evidence(kinds, supports, bans, row) for row in base.TARGETS]
                        assert all(e['status'] == 'accept' for e in targets)
                        assert [e['x_list'] for e in targets] == [[2, 3], [0, 3]]
                        assert all(len(fs[0]) == 1 for fs in bans)
                        record.update(result='both_targets', targets=targets)
                records.append(record)
    counts = dict(sorted(Counter(r['result'] for r in records).items()))
    assert geometry_counts == {'(False, False)': 376, '(False, True)': 88,
                               '(True, False)': 88, '(True, True)': 8}
    assert len(records) == 728 and counts == {'both_targets': 296, 'source_K5': 320, 'source_T4': 112}
    keys = {(r['kinds'], r['supports'], r['bans']): r for r in records}
    assert len(keys) == len(records)
    for r in records:
        swapped = (r['kinds'][::-1], r['supports'][2:]+r['supports'][:2], r['bans'][::-1])
        assert keys[swapped]['result'] == r['result']
        reflected = keys[reflected_key(r)]
        assert reflected['result'] == r['result']
        if r['result'] == 'both_targets':
            r['reflection'] = reflection_control(r, reflected)
    controls = [minor_control(pair, landing, length, cut, style)
                for pair in combinations(range(5), 2) if pair[1]-pair[0] in (1, 4)
                for landing in sorted(set(X_BOUNDARY)-set(pair))
                for length in (1, 3, 5) for cut in range(length)
                for style in ('direct', 'shared_trunk')]
    assert len(controls) == 108
    retained = [r for r in records if r['result'] == 'both_targets']
    retained_kinds = dict(sorted(Counter(str(r['kinds']) for r in retained).items()))
    assert retained_kinds == {'(False, False)': 144, '(False, True)': 72,
                              '(True, False)': 72, '(True, True)': 8}
    inputs = ['scripts/c5_adjacent_degree5_singleton_long_arc.py',
              'scripts/c5_single_spoke_cores.py', 'scripts/c5_single_spoke_two_two_external.py',
              'scripts/c5_single_spoke_two_two_minor.py',
              'artifacts/c5_adjacent_degree5_shared_singleton/observations.json',
              'artifacts/c5_adjacent_degree5_singleton_sectors/observations.json']
    return dict(schema=1, scope='necessary supports, not source realizations; paper topology not formalized',
                x_boundary=X_BOUNDARY, long_arc=ARC,
                source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                inputs_sha256={p: sha256((ROOT/p).read_bytes()).hexdigest() for p in inputs},
                summary=dict(geometries=geometry_counts, necessary_records=len(records), counts=counts,
                             retained_kinds=retained_kinds, target_acceptances=2*len(retained),
                             unresolved_queries=0, K5_controls=len(controls),
                             missing_root_x_controls=len(controls), reflected_target_checks=2*len(retained),
                             contact_orientations_per_record=4, stale_x_list_negative_controls=2),
                records=records, minor_controls=controls, x_list_negative_controls=x_list_controls())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build()
    table = base.table(data).replace('{b0,b1}', '{b1,b2}', 1)
    outputs = {OUT: json.dumps(data, sort_keys=True, indent=2)+'\n', TABLE: table}
    for path, payload in outputs.items():
        if args.check:
            assert path.read_bytes() == payload.encode(), f'certificate differs: {path}'
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(payload)
    print(json.dumps(data['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
