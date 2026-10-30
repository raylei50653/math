#!/usr/bin/env python3
"""Common odd-cycle rotation and full-reference controls; no E932 claim."""
from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

import c5_parity_shared_cut_verification as base
import c5_two_reference_parity_verification as two
from c5_common_odd_cycle_geometry import cycle_geometry
import c5_common_odd_cycle_blocker as blocker

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / 'audits/2026-10-29-parity-shared-cut-e1a90fe/verification.json'
F4 = ROOT / 'audits/2026-10-29-two-reference-parity-e1a90fe/verification.json'
ADJACENT = tuple(p for p in base.PAIRS if p not in base.STAR)


def pieces(edges, selected, vertices=()):
    """Ordered complete paths/cycles plus isolated vertices, with original IDs."""
    rows = two.traces(edges, selected)
    covered = {v for row in rows for v in row['vertices']}
    rows += [dict(vertices=[v], edges=[], ends=[v], isolated=True)
             for v in sorted(set(vertices) - covered)]
    return [dict(row, length=len(row['edges']), parity=len(row['edges']) % 2)
            for row in rows]


def noncrossing(rows, order):
    index = {v: i for i, v in enumerate(order)}
    pairs = [sorted(index[v] for v in row['ends']) for row in rows if row['ends']]
    return all(not (a < c < b < d or c < a < d < b)
               for (a, b), (c, d) in combinations(pairs, 2))


def region_check(edges, n, matching, reference, old_cycles):
    return blocker._regions(edges, n, matching, reference, old_cycles)


def reference_cycle(edges, n, matching, reference, exposed, geometry):
    ce = set(geometry['cycle_edges'])
    vs = geometry['cycle_vertices']
    side = dict(zip(vs, geometry['inside_bits']))
    hits = sorted(ce & reference)
    assert hits
    ports = sorted(v for e in hits for v in edges[e])
    assert len(ports) == len(set(ports))
    mixed = [e for e in hits if side[edges[e][0]] != side[edges[e][1]]]
    assert len(mixed) % 2 == 0
    assert sum(side[v] for v in ports) % 2 == 0
    inside = set(geometry['inside_network_edges'])
    outside = set(geometry['outside_network_edges'])
    current_exposed = two.exposed(edges, n, matching)

    def off_cycle_rows(selected, alternating):
        rows = pieces(edges, selected - ce)
        for row in rows:
            es = set(row['edges'])
            assert es <= inside or es <= outside
            row['side'] = 'inside' if es <= inside else 'outside'
            if not row['ends']:
                assert row['parity'] == 0
                continue
            if row['side'] == 'inside':
                assert all(v in ports and side[v] == 1 for v in row['ends'])
            else:
                assert all((v in ports and side[v] == 0) or v >= n for v in row['ends'])
            if alternating:
                types = []
                for v in row['ends']:
                    if v in ports:
                        types.append('M')
                    else:
                        assert v - n in set(current_exposed) ^ set(exposed)
                        types.append('R' if v - n in current_exposed else 'M')
                row['endpoint_matching_types'] = types
                assert row['parity'] == int(types[0] == types[1])
            elif row['side'] == 'outside':
                assert all(v in ports or v - n in exposed for v in row['ends'])
        inner = [row for row in rows if row['side'] == 'inside']
        assert noncrossing(inner, vs)
        assert sorted(v for row in inner for v in row['ends']) == sorted(v for v in ports if side[v])
        return rows

    difference = off_cycle_rows(matching ^ reference, True)
    returns = off_cycle_rows(set(range(len(edges))) - reference, False)
    singleton_return = None
    if len(hits) == 1:
        assert side[ports[0]] == side[ports[1]]
        if side[ports[0]]:
            inner = [row for row in returns if row['side'] == 'inside' and row['ends']]
            assert len(inner) == 1 and inner[0]['parity'] == 0
            singleton_return = inner[0]
    return dict(hit_edges=hits, mixed_side_hit_edges=mixed,
                active_spoke_vertices=ports, interior_active_parity=0,
                complete_retained_cycle_arcs=pieces(edges, ce - reference, vs),
                complete_difference_segments=difference,
                complete_reference_return_segments=returns,
                singleton_interior_even_return=singleton_return)


def matching_audit(g, matching, good, require_minimum):
    edges, n = g['network_edges'], g['network_internal_vertices']
    old_cycles = [c for c in two.traces(edges, set(range(len(edges))) - matching)
                  if not c['ends'] and len(c['edges']) % 2]
    assert old_cycles
    geometries = [cycle_geometry(g, c, matching) for c in old_cycles]
    references = []
    for family in base.STAR:
        for reference in good[family]:
            references.append(dict(id=len(references), family=family, matching=sorted(reference),
                cycle_checks=[reference_cycle(edges, n, matching, reference, family, geom)
                              for geom in geometries],
                region_check=region_check(edges, n, matching, reference, old_cycles)
                             if require_minimum else None,
                exact_full_rewire=base.parity_rewire(edges, n, matching, reference)))
    pairs = []
    for first, second in combinations(base.STAR, 2):
        products = []
        for a, r in product([x for x in references if tuple(x['family']) == first],
                            [x for x in references if tuple(x['family']) == second]):
            products.append(dict(first_reference_id=a['id'], second_reference_id=r['id'],
                common_retained_cycle_segments=[pieces(edges,
                    set(geom['cycle_edges']) - set(a['matching']) - set(r['matching']),
                    geom['cycle_vertices']) for geom in geometries]))
        assert len(products) == len(good[first]) * len(good[second])
        pairs.append(dict(families=[first, second], reference_products=products,
                          status='checked' if products else 'not triggered'))
    assert len(pairs) == 10
    return dict(matching=sorted(matching), exposed=two.exposed(edges, n, matching),
                minimum_required=require_minimum, odd_cycles=old_cycles,
                common_jordan_geometry=geometries, all_references=references,
                all_ten_family_pairs=pairs)


def graph_audit(g, expected):
    edges, n = g['network_edges'], g['network_internal_vertices']
    base.surgery.check_faces(g['primal_vertices'], g['primal_edges'],
                             [tuple(f) for f in g['oriented_faces']])
    assert [list(e) for e in base.surgery.dual([tuple(e) for e in g['primal_edges']],
                                            g['oriented_faces'])] == edges
    pm = two.graph_pm(edges, n)
    frozen = {''.join(map(str, p)): [sorted(m) for m in ms] for p, ms in pm.items()}
    assert frozen == {p: ms for p, ms in expected.items() if len(p) == 2}
    good = {p: [m for m in pm[p] if base.odd(edges, m) == 0] for p in base.PAIRS}
    targets = []
    for p in ADJACENT:
        minimum = min((base.odd(edges, m) for m in pm[p]), default=None)
        minimizers = [m for m in pm[p] if base.odd(edges, m) == minimum]
        tests = [matching_audit(g, m, good, True) for m in minimizers if minimum]
        targets.append(dict(exposed=p, minimum_odd=minimum,
                            complete_minimizers=[sorted(m) for m in minimizers],
                            positive_minimizer_tests=tests,
                            status='checked' if tests else 'no positive odd minimum'))
    return dict(graph=g, complete_pm_families=frozen,
                complete_even_families={''.join(map(str, p)): [sorted(m) for m in ms]
                                        for p, ms in good.items()},
                adjacent_family_tests=targets)


def chain_profile():
    """A profile relation, explicitly without claimed complete Q matchings."""
    cycle = [(i, (i + 1) % 9) for i in range(9)]
    candidates = [bits for bits in product((0, 1), repeat=9) if bits[0] == 1 and bits[5] == 0]
    profiles = [dict(family=p, singleton_hit_edge=i,
                     retained_arc=pieces(cycle, set(range(9)) - {i}),
                     possible_even_return_length=2,
                     concentration_gain=1,
                     concentration_syndrome=[int(v in set((0, 1)) ^ set(p)) for v in range(5)])
                for i, p in enumerate(base.STAR)]
    rows = []
    for count in range(6):
        for subset in combinations(range(5), count):
            solutions = [bits for bits in candidates
                         if all(bits[i] == bits[i + 1] for i in subset)]
            assert bool(solutions) == (count < 5)
            rows.append(dict(reference_indices=subset, common_side_words=solutions))
    pair_rows = [row for row in rows if len(row['reference_indices']) == 2]
    assert len(pair_rows) == 10 and all(row['common_side_words'] for row in pair_rows)
    return dict(name='F5-CHAIN9', cycle_edges=cycle, fixed_sides={'0': 1, '5': 0},
                singleton_profiles=profiles, all_subset_relations=rows,
                all_ten_pair_relations=pair_rows,
                full_common_relation=rows[-1]['common_side_words'],
                classification='Abstract retained-arc/concentration profile only; no full Q or reference matching families asserted. Each pair has a side witness, all five have none.')


def report():
    old = json.loads(OLD.read_text())
    frozen = json.loads(F4.read_text())
    controls = []
    for row in old['graphs']:
        graph = {k: row[k] for k in ('index', 'primal_vertices', 'primal_edges', 'oriented_faces',
                                   'network_internal_vertices', 'network_edges')}
        controls.append(graph_audit(graph, row['complete_pm_families']))
    failure = frozen['directed_f4']['first_graph_wide_failure']
    g = failure['graph']
    f4_control = graph_audit(g, failure['complete_pm_families'])
    edges, n = g['network_edges'], g['network_internal_vertices']
    pm = two.graph_pm(edges, n)
    good = {p: [m for m in ms if base.odd(edges, m) == 0] for p, ms in pm.items()}
    negative = []
    for pair in failure['reference_pairs']:
        for candidate in pair['candidates']:
            if candidate['target'] and candidate['odd']:
                check = matching_audit(g, frozenset(candidate['matching']), good, False)
                cycle = candidate['odd_cycles'][0]
                assert len(cycle['cycle']['edges']) == 9
                assert len(cycle['selected_to_unselected_segments']) == 2
                negative.append(dict(old_complete_pair=pair, old_candidate=candidate,
                                     common_rotation_check=check,
                                     minimum_note='This candidate is not a minimum in PM04; other even targets exist. No C1 minimum claim is applied.'))
    assert len(negative) == 1
    concentrated = []
    for row in old['graphs']:
        tests = [t for t in row['region_checks']['tests'] if t['minimum_odd']]
        if tests:
            assert row['index'] in (12, 14)
            assert all(t['positive_regions'] == 1 for t in tests)
            assert all(action['feasible_assignments'] for cut in row['actual_reference_cuts']
                       for action in cut['actions'])
            concentrated.append(dict(graph_index=row['index'], old_positive_minimizer_tests=tests,
                                     actual_reference_cuts=row['actual_reference_cuts']))
    assert len(concentrated) == 2
    checks = [test for row in controls + [f4_control] for target in row['adjacent_family_tests']
              for test in target['positive_minimizer_tests']]
    refs = [ref for check in checks for ref in check['all_references']]
    pairs = [pair for check in checks for pair in check['all_ten_family_pairs']]
    deps = ['scripts/c5_five_reference_rotation_verification.py',
            'scripts/c5_common_odd_cycle_geometry.py', 'scripts/c5_common_odd_cycle_blocker.py',
            'scripts/c5_two_reference_parity_verification.py',
            'scripts/c5_parity_shared_cut_verification.py', 'scripts/c5_dual_path_surgery.py',
            str(OLD.relative_to(ROOT)), str(F4.relative_to(ROOT))]
    return dict(base='e1a90fea41702d7c98747716a5960198aecbecb3',
                scope='Local common rotation/segment lemmas; frozen 16 disks plus frozen F4 source; no generator extension or general E932 exclusion.',
                reused_disks=controls, reused_f4_source=f4_control,
                nine_cycle_negative_control=negative,
                three_family_shared_cut_negative_controls=concentrated,
                complete_five_reference_algebraic_control=blocker.report(),
                pairwise_feasible_jointly_empty_profile=chain_profile(),
                totals=dict(disks=17, positive_adjacent_minimizers=len(checks),
                    minimum_reference_combinations=len(refs),
                    odd_cycle_reference_checks=sum(len(ref['cycle_checks']) for ref in refs),
                    all_ten_family_pair_records=len(pairs),
                    full_pair_products=sum(len(p['reference_products']) for p in pairs),
                    full_region_batches=sum(len(ref['region_check']['complete_region_batches']) for ref in refs),
                    five_nonempty_reference_disk_cases=sum(all(row['complete_even_families'][''.join(map(str,p))]
                                                            for p in base.STAR) for row in controls + [f4_control])),
                source_sha256={p: sha256((ROOT / p).read_bytes()).hexdigest() for p in deps})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    result = report()
    payload = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + '\n'
    if args.check:
        assert args.check.read_text() == payload, 'common rotation certificate differs'
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload)
    print(json.dumps(result['totals'], sort_keys=True))


if __name__ == '__main__':
    main()
