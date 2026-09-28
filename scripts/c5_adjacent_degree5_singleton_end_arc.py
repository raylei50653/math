#!/usr/bin/env python3
"""Exclude the necessary {b3,b4} long-arc cover and reflect it to {b4,b0}.

The paper supplies arbitrary-size triangle/annulus and original-path K5 proofs.
These are whole forbidden-set bounds, not realizable sources or marginals.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

import c5_adjacent_degree5_singleton_long_arc as base

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_adjacent_degree5_singleton_end_arc/observations.json'
TABLE = OUT.with_name('support_table.md')
ARC = (4, 0, 1, 2, 3)
X_BOUNDARY = (3, 4)
REFLECTED_ARC = (0, 1, 2, 3, 4)
REFLECTED_X = (0, 4)


def q_side_bans(kind, spoke, pair):
    """Use the actual x list; its complement supplies the private colors."""
    outside = base.U - set(pair)
    for residual in ((pair[0],), (pair[1],), pair):
        lost = set(pair) - set(residual)
        if kind:
            for singleton in sorted(outside):
                yield (tuple(sorted((outside - {singleton}) | lost)), (singleton,)), residual
        elif base.Q[spoke] in outside:
            yield (tuple(sorted((outside - {base.Q[spoke]}) | lost)),), residual


def abstract_key(kinds, supports, bans):
    return tuple(((2, 1) if kinds[r] else (2,),
                  () if kinds[r] else (base.Q[supports[2*r+1][0]],), bans[r])
                 for r in range(2))


def admissible_supports(supports, bans):
    return all(base.valid_q_support(supports[2*r+k], f)
               for r in range(2) for k, f in enumerate(bans[r]))


def k5_witness(supports, bans, x_boundary):
    for r in range(2):
        pair = base.forced_pair(supports[2*r], bans[r][0])
        if pair is not None and (landings := sorted(set(x_boundary) - set(pair))):
            root = ('z', 'w')[r]
            return dict(root=root, component=root+'C2', contacts=(root+'u', root+'v'),
                        forbidden=bans[r][0], tether_pair=pair,
                        original_external_path=(root, 'x', 'b'+str(landings[0])),
                        complement_arc=sorted(set(range(5)) - set(pair)))
    return None


def cover(arc, x_boundary, previous, geometries):
    pair = tuple(sorted(base.U - {base.Q[i] for i in x_boundary}))
    abstract = {}
    for index, entry in enumerate(previous['abstract_relations']):
        if entry['pair'] == list(pair) and entry['planar_necessary_retained']:
            key = tuple((tuple(entry[s]['ports']), tuple(entry[s]['spokes_colors']),
                         tuple(map(tuple, entry[s]['forbidden']))) for s in ('left', 'right'))
            assert key not in abstract
            abstract[key] = index
    assert len(abstract) == 80
    records = []
    for kinds, geometry in geometries.items():
        for lifted, order in sorted(geometry.items()):
            supports = tuple(tuple(sorted(arc[i] for i in s)) for s in lifted)
            candidates = set()
            for left, right in product(q_side_bans(kinds[0], supports[1][0], pair),
                                       q_side_bans(kinds[1], supports[3][0], pair)):
                if left[1] != pair and right[1] != pair:
                    continue
                bans = (left[0], right[0])
                if admissible_supports(supports, bans):
                    candidates.add(bans)
            # Independent q-domain check: filter the earlier complete minimality
            # relations by ports, actual spokes, and actual support stabilizers.
            from_abstract = set()
            for key in abstract:
                bans = (key[0][2], key[1][2])
                if (abstract_key(kinds, supports, bans) == key
                        and admissible_supports(supports, bans)):
                    from_abstract.add(bans)
            assert candidates == from_abstract
            for bans in sorted(candidates):
                record = dict(id=len(records), kinds=kinds, supports=supports, bans=bans,
                              order=order, lifted_supports=lifted,
                              port_rotations=base.port_rotations(kinds, order),
                              previous_abstract_index=abstract[abstract_key(kinds, supports, bans)])
                assert base.row_evidence(kinds, supports, bans, base.Q, x_boundary)['status'] == 'reject'
                witness = k5_witness(supports, bans, x_boundary)
                if witness:
                    record.update(result='source_K5', K5=witness)
                else:
                    for row in base.T4:
                        evidence = base.row_evidence(kinds, supports, bans, row, x_boundary)
                        if evidence['status'] == 'reject':
                            record.update(result='source_T4', T4=evidence)
                            break
                    else:
                        raise AssertionError(('source exclusion incomplete', record))
                records.append(record)
    keys = {(r['kinds'], r['supports'], r['bans']): r for r in records}
    assert len(keys) == len(records) == 152
    assert Counter(r['result'] for r in records) == {'source_K5': 120, 'source_T4': 32}
    for r in records:
        swapped = (r['kinds'][::-1], r['supports'][2:]+r['supports'][:2], r['bans'][::-1])
        assert keys[swapped]['result'] == r['result']
    return records, keys


def reflection_control(record, keys):
    supports = tuple(tuple(sorted(base.RHO[i] for i in s)) for s in record['supports'])
    bans = tuple(tuple(tuple(sorted(base.PI[c] for c in f)) for f in fs)
                 for fs in record['bans'])
    reflected = keys[(record['kinds'], supports, bans)]
    assert reflected['result'] == record['result']
    assert reflected['order'] == record['order'][::-1]
    assert reflected['lifted_supports'] == tuple(tuple(sorted(4-i for i in s))
                                                for s in record['lifted_supports'])
    assert sorted(reflected['port_rotations']) == sorted(w[::-1] for w in record['port_rotations'])
    result = dict(record_id=reflected['id'])
    if record['result'] == 'source_K5':
        old, new = record['K5'], reflected['K5']
        assert old['root'] == new['root']
        assert new['tether_pair'] == sorted(base.RHO[i] for i in old['tether_pair'])
        landing = base.RHO[int(old['original_external_path'][-1][1:])]
        assert landing in REFLECTED_X and landing not in new['tether_pair']
        result['external_path'] = (old['root'], 'x', f'b{landing}')
    else:
        before = record['T4']
        row = tuple(base.PI[before['row'][base.RHO[i]]] for i in range(5))
        assert row in base.T4
        after = base.row_evidence(record['kinds'], supports, bans, row, REFLECTED_X)
        assert after['status'] == 'reject'
        assert after['x_list'] == sorted(base.PI[c] for c in before['x_list'])
        for old, new in zip(before['sides'], after['sides']):
            assert sorted(tuple(sorted(base.PI[c] for c in e))
                          for e in old['residual_options']) == new['residual_options']
            for old_c, new_c in zip(old['components'], new['components']):
                assert old_c['exact'] == new_c['exact']
                assert sorted(tuple(sorted(base.PI[c] for c in f))
                              for f in old_c['options']) == sorted(new_c['options'])
        result['T4'] = after
    return result


def post_k5_forms(records):
    """Check the eight near-b4 forms times two far spokes and root exchange."""
    near = [dict(kind=False, supports=(support, (spoke,)), bans=((ban,),))
            for support, spoke, ban in (((0, 4), 1, 2), ((0, 1, 4), 4, 1),
                                       ((0, 1, 4), 1, 2), ((1, 4), 4, 1),
                                       ((1, 4), 1, 2), ((0, 1), 4, 1))]
    near += [dict(kind=True, supports=((0, 4), (0, 1)), bans=((2,), (1,))),
             dict(kind=True, supports=((0, 1), (0, 4)), bans=((1,), (2,)))]
    expected = set()
    for n in near:
        for spoke in (1, 3):
            far = dict(kind=False, supports=((1, 2, 3), (spoke,)), bans=((2, 3),))
            for left, right in ((n, far), (far, n)):
                expected.add(((left['kind'], right['kind']), left['supports']+right['supports'],
                              (left['bans'], right['bans'])))
    actual = {(r['kinds'], r['supports'], r['bans']) for r in records if r['result'] == 'source_T4'}
    assert actual == expected and len(actual) == 32
    for r in records:
        if r['result'] == 'source_T4':
            e = r['T4']
            assert e['row'] == (0, 1, 2, 1, 3) and e['x_list'] == [0, 2]
            assert all(c['exact'] for s in e['sides'] for c in s['components'])
            assert sorted(s['residual_options'] for s in e['sides']) == [[(0, 2)], [(2,)]]
            assert len(e['joins']) == 1 and e['joins'][0]['witness'] is None
    return near


def minor_control(x_boundary, shift, pair, landing, length, cut, style):
    """Rotate the topology skeleton only; all row algebra uses fixed q."""
    old_pair = tuple(sorted((i-shift) % 5 for i in pair))
    old = base.minor_control(old_pair, (landing-shift) % 5, length, cut, style)

    def vertex(v):
        return 'b'+str((int(v[1:])+shift) % 5) if v.startswith('b') else v

    edges = {tuple(sorted(map(vertex, e))) for e in old['edges']}
    bags = [set(map(vertex, b)) for b in old['branch_sets']]
    witnesses = base.verify_minor(edges, bags)
    try:
        base.verify_minor(edges - {('x', 'z')}, bags)
    except AssertionError:
        pass
    else:
        raise AssertionError('missing original root-x edge was not detected')
    assert {i for i in range(5) if (f'b{i}', 'x') in edges} == set(x_boundary)
    assert landing in x_boundary and landing not in pair
    return dict(x_boundary=x_boundary, tether_pair=pair,
                external_path=('z', 'x', f'b{landing}'), length=length, cut=cut, style=style,
                edges=sorted(edges), branch_sets=[sorted(b) for b in bags], witnesses=witnesses)


def summary(records):
    return dict(necessary_records=len(records), counts=dict(sorted(Counter(r['result'] for r in records).items())),
                partition_counts={str(k): dict(sorted(Counter(r['result'] for r in records if r['kinds'] == k).items()))
                                  for k in product((False, True), repeat=2)},
                retained_records=0, target_acceptances=0, unresolved_queries=0)


def build():
    assert tuple(base.PI[base.Q[base.RHO[i]]] for i in range(5)) == base.Q
    assert tuple(base.RHO[i] for i in ARC[::-1]) == REFLECTED_ARC
    previous = json.loads((ROOT / 'artifacts/c5_adjacent_degree5_shared_singleton/observations.json').read_text())
    geometries = {k: base.geometries(k) for k in product((False, True), repeat=2)}
    for kinds, geometry in geometries.items():
        assert set(geometry) == base.independent_geometries(kinds)
    geometry_counts = {str(k): len(v) for k, v in geometries.items()}
    assert list(geometry_counts.values()) == [376, 88, 88, 8]
    records, _ = cover(ARC, X_BOUNDARY, previous, geometries)
    near_forms = post_k5_forms(records)
    reflected, keys = cover(REFLECTED_ARC, REFLECTED_X, previous, geometries)
    for r in records:
        r['reflection'] = reflection_control(r, keys)
    assert len({r['reflection']['record_id'] for r in records}) == len(reflected)
    controls = [minor_control(xb, shift, pair, landing, length, cut, style)
                for xb, shift in ((X_BOUNDARY, 3), (REFLECTED_X, 4))
                for pair in combinations(range(5), 2) if pair[1]-pair[0] in (1, 4)
                for landing in sorted(set(xb)-set(pair))
                for length in (1, 3, 5) for cut in range(length)
                for style in ('direct', 'shared_trunk')]
    assert len(controls) == 216
    relation = ((1, 2), (2, 1))
    marginals = tuple(product(*(sorted({t[j] for t in relation}) for j in range(2))))
    assert set.intersection(*map(set, relation)) == {1, 2}
    assert not set.intersection(*map(set, marginals))
    inputs = ['scripts/c5_adjacent_degree5_singleton_long_arc.py',
              'scripts/c5_single_spoke_cores.py', 'scripts/c5_single_spoke_two_two_external.py',
              'scripts/c5_single_spoke_two_two_minor.py',
              'artifacts/c5_adjacent_degree5_shared_singleton/observations.json',
              'artifacts/c5_adjacent_degree5_singleton_sectors/observations.json']
    return dict(schema=1, scope='necessary source cover excluded; paper topology not formalized',
                x_boundary=X_BOUNDARY, long_arc=ARC, q_x_list=(0, 3),
                reflected_x_boundary=REFLECTED_X, reflected_long_arc=REFLECTED_ARC,
                reflected_q_x_list=(1, 3),
                source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                inputs_sha256={p: sha256((ROOT/p).read_bytes()).hexdigest() for p in inputs},
                summary=dict(geometries=geometry_counts, direct=summary(records), reflected=summary(reflected),
                             q_domain_cross_checks=2*sum(geometry_counts.values()),
                             reflected_records=len(records), reflected_T4_checks=32,
                             post_K5_near_forms=len(near_forms), common_rejected_T4=(0, 1, 2, 1, 3),
                             K5_controls=len(controls), missing_root_x_controls=len(controls),
                             contact_orientations_per_record=4),
                records=records, reflected_records=reflected, minor_controls=controls,
                post_K5_near_forms=near_forms,
                marginal_negative_control=dict(relation=relation, marginal_product=marginals))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build()
    table = base.table(data).replace('{b0,b1}', '{b3,b4}', 1)
    table += '\n' + base.table({'records': data['reflected_records']}).replace('{b0,b1}', '{b4,b0}', 1)
    for path, payload in {OUT: json.dumps(data, sort_keys=True, indent=2)+'\n', TABLE: table}.items():
        if args.check:
            assert path.read_bytes() == payload.encode(), f'certificate differs: {path}'
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(payload)
    print(json.dumps(data['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
