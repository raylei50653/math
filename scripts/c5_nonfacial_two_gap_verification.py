#!/usr/bin/env python3
"""Finite replay for nonfacial odd-cycle singleton parity and the C5 two-gap exclusion.

Actual source rows retain every reference, every family product and all C1
batches.  The separate twenty-row C5 table is an abstract necessary interface,
not a claim of source realization or a proof by finite source non-triggering.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path
import sys

import c5_five_reference_rotation_verification as five

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / 'audits/2026-10-29-five-reference-source-e1a90fe'
FROZEN_SOURCE = SOURCE_DIR / 'verification.json'
FROZEN_FIVE = ROOT / 'audits/2026-10-29-five-reference-rotation-e1a90fe/verification.json'


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n'


def full_regions(edges, n, matching, reference, old_cycles):
    """Exact C1 without imposing a minimum on the extra nonminimum controls."""
    rows = []
    for region in five.base.components(edges,
            set(range(len(edges))) - (matching & reference), range(n + 5)):
        vs = set(region['vertices'])
        toggle = frozenset(e for e in matching ^ reference if set(edges[e]) <= vs)
        syndrome = [int(any(n + i in edges[e] for e in toggle)) for i in range(5)]
        rows.append(dict(vertices=region['vertices'], region_edges=region['edges'],
            toggle=sorted(toggle), gain=sum(set(c['vertices']) <= vs for c in old_cycles),
            syndrome=syndrome))
    batches = []
    old_odd = five.base.odd(edges, matching)
    wm = five.base.word(edges, n, matching)
    for mask in range(1 << len(rows)):
        new, gain, syndrome = matching, 0, [0] * 5
        selected = [i for i in range(len(rows)) if mask >> i & 1]
        for i in selected:
            new ^= frozenset(rows[i]['toggle'])
            gain += rows[i]['gain']
            syndrome = [a ^ b for a, b in zip(syndrome, rows[i]['syndrome'])]
        assert five.base.saturated(edges, n, new)
        assert five.base.odd(edges, new) == old_odd - gain
        assert five.base.word(edges, n, new) == tuple(a ^ b for a, b in zip(wm, syndrome))
        batches.append(dict(selected_regions=selected, matching=sorted(new),
            odd=old_odd - gain, syndrome=syndrome,
            exposed=[i for i, x in enumerate(five.base.word(edges, n, new)) if not x]))
    return dict(regions=rows, complete_region_batches=batches,
        minimum_constraint_imposed=False)


def parity_projection(graph, check):
    edges = graph['network_edges']
    matching = frozenset(check['matching'])
    n = graph['network_internal_vertices']
    result = []
    for index, geom in enumerate(check['common_jordan_geometry']):
        vertices = geom['cycle_vertices']
        ce = set(geom['cycle_edges'])
        strict = set(geom['inside_network_vertices'])
        inside = set(geom['inside_network_edges'])
        side = dict(zip(vertices, geom['inside_bits']))
        k = sum(side.values())
        cut = [e for e in inside if len(set(edges[e]) & strict) == 1]
        assert set(cut) <= matching
        assert len(cut) == k - 2 * len(geom['inside_chord_edges'])
        assert len(strict) % 2 == len(cut) % 2 == k % 2
        singleton, witnesses, inner_forbidden = set(), [], []
        for ref in check['all_references']:
            local = ref['cycle_checks'][index]
            hit = local['hit_edges']
            assert hit == sorted(ce & set(ref['matching']))
            if len(hit) != 1:
                continue
            edge = hit[0]
            u, v = edges[edge]
            assert side[u] == side[v] == len(strict) % 2
            singleton.add(edge)
            retained = five.pieces(edges, inside - set(ref['matching']))
            paths = [p for p in retained if p['ends']]
            cycles = [p for p in retained if not p['ends']]
            assert all(p['parity'] == 0 for p in cycles)
            assert set(strict) <= {v for p in retained for v in p['vertices']}
            if side[u]:
                assert len(paths) == 1 and set(paths[0]['ends']) == {u, v}
                assert paths[0]['parity'] == 0
                assert len(set(paths[0]['vertices']) & strict) % 2 == 1
            else:
                assert not paths
            assert all(set(p['vertices']) <= strict for p in cycles)
            strict_parts = [set(p['vertices']) & strict for p in retained]
            assert sum(map(len, strict_parts)) == len(strict)
            strict_vertex_occurrences = {v: sum(v in p['vertices'] for p in retained) for v in strict}
            assert all(count == 1 for count in strict_vertex_occurrences.values())
            regions = ref['region_check']['regions']
            containing = [r for r in regions if set(vertices) <= set(r['vertices'])]
            assert len(containing) == 1
            region = containing[0]
            if side[u]:
                assert all(v < n for v in region['vertices'])
                assert set(region['vertices']) <= set(vertices) | strict
                assert not any(region['syndrome']) and region['gain'] >= 1
                inner_forbidden.append(ref['id'])
                assert not check['minimum_required'], 'C1 forbids an inward singleton at a minimum'
            witnesses.append(dict(reference_id=ref['id'], family=ref['family'],
                singleton_hit_edge=edge, endpoint_side=side[u],
                complete_interior_reference_complement_segments=retained,
                strict_interior_vertex_occurrences=strict_vertex_occurrences,
                full_region_containing_cycle=region))
        forbidden = sorted(v for v in vertices if side[v] != len(strict) % 2)
        forbidden_incident = sorted(e for e in ce if set(edges[e]) & set(forbidden))
        missing = sorted(ce - singleton)
        nonfacial = bool(k)
        if nonfacial:
            assert 0 in side.values()
            assert len(forbidden) >= 2 and len(forbidden) % 2 == 0
            assert len(forbidden_incident) >= 3
            assert set(forbidden_incident) <= set(missing) and len(missing) >= 3
        result.append(dict(cycle_index=index, actual_cycle=check['odd_cycles'][index],
            common_geometry=geom, strict_interior_vertices=sorted(strict),
            inward_incidence_count=k, original_strict_interior_cut_edges=cut,
            strict_vertex_and_cut_parity=len(strict) % 2,
            allowed_singleton_endpoint_side=len(strict) % 2,
            all_singleton_witnesses=witnesses,
            singleton_hit_union_edges=sorted(singleton), missing_singleton_edges=missing,
            forbidden_side_vertices=forbidden,
            forbidden_side_incident_cycle_edges=forbidden_incident,
            inward_singletons_excluded_by_minimum_c1=inner_forbidden,
            nonfacial=nonfacial, nonfacial_c5=nonfacial and len(vertices) == 5,
            nonfacial_three_missing_bound_passes=not nonfacial or len(missing) >= 3,
            c5_two_gap_hypothesis_triggered=nonfacial and len(vertices) == 5 and len(missing) == 2))
    return dict(graph_index=graph['index'], minimum_required=check['minimum_required'],
        matching=check['matching'], exposed=check['exposed'],
        all_references=check['all_references'], all_ten_family_pairs=check['all_ten_family_pairs'],
        cycle_projections=result)


def abstract_c5():
    edges = [(i, (i + 1) % 5) for i in range(5)]
    all_hits = [list(h) for size in (1, 2) for h in combinations(range(5), size)
                if len({v for e in h for v in edges[e]}) == 2 * size]
    rows = []
    for gaps in combinations(range(5), 2):
        required = sorted(set(range(5)) - set(gaps))
        components = five.base.components(edges, required, range(5))
        assert len(components) == 2
        for component_bits in ((0, 1), (1, 0)):
            bits = [None] * 5
            for region, bit in zip(components, component_bits):
                for v in region['vertices']:
                    bits[v] = bit
            assert {e for e, (u, v) in enumerate(edges) if bits[u] != bits[v]} == set(gaps)
            allowed_side = sum(bits) % 2
            profiles = []
            for hit in all_hits:
                side_pass = sum(bits[v] for e in hit for v in edges[e]) % 2 == 0
                singleton_pass = len(hit) != 1 or all(bits[v] == allowed_side for e in hit for v in edges[e])
                profiles.append(dict(hit_edges=hit,
                    complete_retained_cycle_segments=five.pieces(edges, set(range(5)) - set(hit), range(5)),
                    side_equation_passes=side_pass,
                    singleton_interior_vertex_parity_passes=singleton_pass))
            impossible = [e for e in required if any(bits[v] != allowed_side for v in edges[e])]
            assert impossible
            assert all(not any(p['hit_edges'] == [e] and p['side_equation_passes']
                              and p['singleton_interior_vertex_parity_passes'] for p in profiles)
                       for e in impossible)
            rows.append(dict(missing_edges=list(gaps), required_singleton_edges=required,
                union_components=components, actual_side_word=bits,
                inward_vertex_count=sum(bits), implied_strict_interior_vertex_parity=allowed_side,
                all_nonempty_cycle_matching_hit_profiles=profiles,
                impossible_required_singleton_edges=impossible,
                two_gap_interface_feasible=False))
    assert len(rows) == 20
    return dict(classification='Abstract necessary C5 interface only; no full Q, references or C1 regions are claimed.',
        cycle_edges=edges, rows=rows, totals=dict(gap_pairs=10, mixed_side_rows=20,
        nonempty_hit_profiles_per_row=len(all_hits), rejected_rows=len(rows)))


def sharp_three_gap_control():
    """A literal plane rotation with an inner parallel chord, not full Gamma."""
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 1), (2, 7),
             (3, 5), (5, 8), (5, 6), (6, 9), (6, 10), (4, 11)]
    rotation = {0: [0, 5, 4], 1: [1, 5, 0], 2: [2, 1, 6], 3: [3, 2, 7],
                4: [4, 3, 12], 5: [7, 8, 9], 6: [9, 10, 11],
                7: [6], 8: [8], 9: [10], 10: [11], 11: [12]}
    for v, order in rotation.items():
        assert sorted(order) == [e for e, ends in enumerate(edges) if v in ends]
        assert len(order) == (3 if v < 7 else 1)
    unseen = {(v, e) for e, ends in enumerate(edges) for v in ends}
    faces = []
    while unseen:
        start = min(unseen)
        current = start
        darts, vs, es = [], [], []
        while current not in darts:
            v, e = current
            darts.append(current)
            vs.append(v)
            es.append(e)
            unseen.remove(current)
            w = next(w for w in edges[e] if w != v)
            order = rotation[w]
            current = (w, order[(order.index(e) + 1) % len(order)])
        assert current == start
        faces.append(dict(vertices=vs + [vs[0]], edges=es))
    assert len(rotation) - len(edges) + len(faces) == 2
    outer = next(i for i, face in enumerate(faces) if all(v in face['vertices'] for v in range(7, 12)))
    leaf_order = [v - 7 for v in faces[outer]['vertices'][:-1] if v >= 7]
    assert leaf_order == list(range(5))
    inner = [face for i, face in enumerate(faces) if i != outer]
    assert {v for face in inner for v in face['vertices']} == set(range(5))
    counts = {e: sum(face['edges'].count(e) for face in inner) for e in range(len(edges))}
    assert {e for e, count in counts.items() if count == 1} == set(range(5))
    assert {e for e, count in counts.items() if count == 2} == {5}
    graph = dict(index='literal-three-gap-control', network_edges=edges,
        network_internal_vertices=7, literal_rotation={str(v): es for v, es in rotation.items()},
        oriented_face_walks=faces, outer_face_index=outer, outer_terminal_order=leaf_order)
    geom = dict(cycle_vertices=list(range(5)), cycle_edges=list(range(5)),
        inside_network_vertices=[], outside_network_vertices=[5, 6],
        inside_network_edges=[5], outside_network_edges=list(range(6, 13)),
        off_cycle_edges=[5, 5, 6, 7, 12], inside_bits=[1, 1, 0, 0, 0],
        inside_chord_edges=[5])
    assert geom['inside_bits'] == [int(e in geom['inside_network_edges']) for e in geom['off_cycle_edges']]
    families = {p: five.base.matchings(edges, 7, p)
                for size in (0, 2, 4) for p in combinations(range(5), size)}
    # Independent all-subset enumeration: no matching/odd/component helper is
    # used to derive this second copy of the new graph's complete relations.
    brute = {p: [] for p in families}
    brute_odd = {}
    for mask in range(1 << len(edges)):
        chosen = frozenset(e for e in range(len(edges)) if mask >> e & 1)
        degrees = [sum(v in edges[e] for e in chosen) for v in range(12)]
        if degrees[:7] != [1] * 7 or any(d > 1 for d in degrees[7:]):
            continue
        exposed = tuple(i for i, d in enumerate(degrees[7:]) if d == 0)
        assert exposed in brute
        brute[exposed].append(chosen)
        adjacency = {v: [] for v in range(12)}
        for e, (u, v) in enumerate(edges):
            if e not in chosen:
                adjacency[u].append(v)
                adjacency[v].append(u)
        unseen, odd = set(adjacency), 0
        while unseen:
            reached = {min(unseen)}
            queue = list(reached)
            for v in queue:
                for w in adjacency[v]:
                    if w not in reached:
                        reached.add(w)
                        queue.append(w)
            unseen -= reached
            if all(len(adjacency[v]) == 2 for v in reached):
                odd += len(reached) % 2
        brute_odd[chosen] = odd
    assert all(set(brute[p]) == set(ms) for p, ms in families.items())
    assert all(brute_odd[m] == five.base.odd(edges, m) for ms in families.values() for m in ms)
    good = {p: [m for m in families[p] if five.base.odd(edges, m) == 0] for p in five.base.PAIRS}
    matching = frozenset({5, 6, 7, 11, 12})
    assert matching in families[(1, 2)]
    assert min(five.base.odd(edges, m) for m in families[(1, 2)]) == 1
    assert len(families[(1, 2)]) == 2
    old_cycles = [c for c in five.two.traces(edges, set(range(len(edges))) - matching)
                  if not c['ends'] and len(c['edges']) % 2]
    assert len(old_cycles) == 1 and set(old_cycles[0]['edges']) == set(range(5))
    refs = []
    for family in five.base.STAR:
        for reference in good[family]:
            refs.append(dict(id=len(refs), family=family, matching=sorted(reference),
                cycle_checks=[five.reference_cycle(edges, 7, matching, reference, family, geom)],
                region_check=five.region_check(edges, 7, matching, reference, old_cycles),
                exact_full_rewire=five.base.parity_rewire(edges, 7, matching, reference)))
    pairs = []
    for a, b in combinations(five.base.STAR, 2):
        products = [dict(first_reference_id=r['id'], second_reference_id=s['id'],
            common_retained_cycle_segments=[five.pieces(edges,
                set(range(5)) - set(r['matching']) - set(s['matching']), range(5))])
            for r, s in product([r for r in refs if tuple(r['family']) == a],
                                [s for s in refs if tuple(s['family']) == b])]
        pairs.append(dict(families=[a, b], reference_products=products,
            status='checked' if products else 'not triggered'))
    check = dict(matching=sorted(matching), exposed=(1, 2), minimum_required=True,
        odd_cycles=old_cycles, common_jordan_geometry=[geom], all_references=refs,
        all_ten_family_pairs=pairs)
    projected = parity_projection(graph, check)
    assert projected['cycle_projections'][0]['singleton_hit_union_edges'] == [2, 3]
    assert projected['cycle_projections'][0]['missing_singleton_edges'] == [0, 1, 4]
    assert {p for p in five.base.STAR if good[p]} == {(0, 2), (0, 3), (2, 4)}
    return dict(classification='Actual plane C5 with exactly three singleton gaps, minimum M, an inner parallel chord, and only three nonempty Gamma families; no full-five-family claim.',
        graph=graph, complete_pm_families={''.join(map(str, p)): [sorted(m) for m in ms] for p, ms in families.items()},
        independent_all_subset_crosscheck=dict(subsets_examined=1 << len(edges),
            total_matchings=sum(map(len, brute.values())), complete_pm_relations_equal=True,
            full_complement_odd_counts_equal=True),
        complete_even_families={''.join(map(str, p)): [sorted(m) for m in ms] for p, ms in good.items()},
        full_target_family_minimizers=[sorted(m) for m in families[(1, 2)] if five.base.odd(edges, m) == 1],
        parity_check=projected)


def report():
    sys.path.insert(0, str(SOURCE_DIR))
    spec = importlib.util.spec_from_file_location('frozen_source_replay', SOURCE_DIR / 'verify.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    source = module.report()
    assert canonical(source) == FROZEN_SOURCE.read_text(), 'Frozen source certificate replay differs'
    old = json.loads(FROZEN_FIVE.read_text())
    graphs = old['reused_disks'] + [old['reused_f4_source']]
    projections = []
    # A graph's local generator index is not a source identity: the frozen F4
    # prefix and the original sixteen sources both contain an index fourteen.
    baseline = [(r['graph'], test) for r in graphs
                for family in r['adjacent_family_tests'] for test in family['positive_minimizer_tests']]
    baseline += [(old['reused_f4_source']['graph'], c['common_rotation_check'])
                 for c in old['nine_cycle_negative_control']]
    assert len(baseline) == len(source['source_projections'])
    for (graph, check), row in zip(baseline, source['source_projections']):
        assert check['matching'] == row['matching'] and check['minimum_required'] == row['minimum_required']
        if not check['minimum_required']:
            for ref in check['all_references']:
                ref['region_check'] = full_regions(graph['network_edges'], graph['network_internal_vertices'],
                    frozenset(check['matching']), frozenset(ref['matching']), check['odd_cycles'])
        projections.append(dict(parity_projection(graph, check), source_label=row['source_label']))
    extra = []
    scanned_matchings = 0
    for row in graphs:
        graph = row['graph']
        edges, n = graph['network_edges'], graph['network_internal_vertices']
        pm = five.two.graph_pm(edges, n)
        good = {p: [m for m in ms if five.base.odd(edges, m) == 0] for p, ms in pm.items()}
        for family, ms in pm.items():
            for matching in ms:
                scanned_matchings += 1
                c5 = [c for c in five.two.traces(edges, set(range(len(edges))) - matching)
                      if not c['ends'] and len(c['edges']) == 5]
                if not any(any(five.cycle_geometry(graph, c, matching)['inside_bits']) for c in c5):
                    continue
                check = five.matching_audit(graph, matching, good, False)
                for ref in check['all_references']:
                    ref['region_check'] = full_regions(edges, n, matching,
                        frozenset(ref['matching']), check['odd_cycles'])
                extra.append(dict(graph=graph,
                    complete_pm_families=row['complete_pm_families'],
                    complete_even_families=row['complete_even_families'],
                    classification='Actual nonfacial C5 control; no minimum claim imposed.',
                    parity_check=parity_projection(graph, check)))
    cycles = [c for row in projections for c in row['cycle_projections']]
    extra_cycles = [c for row in extra for c in row['parity_check']['cycle_projections']]
    abstract = abstract_c5()
    sharp = sharp_three_gap_control()
    paths = set(source['source_sha256']) | {
        str(Path(__file__).relative_to(ROOT)), str(FROZEN_SOURCE.relative_to(ROOT)),
        str(FROZEN_FIVE.relative_to(ROOT))}
    all_checks = projections + [row['parity_check'] for row in extra] + [sharp['parity_check']]
    return dict(base=old['base'],
        scope='Singleton interior vertex parity and nonfacial three-missing-edge bound; full frozen-source replay and abstract C5 two-gap table, not general five-reference/E932/4CT exclusion.',
        frozen_source_replay=dict(path=str(FROZEN_SOURCE.relative_to(ROOT)),
            sha256=sha256(FROZEN_SOURCE.read_bytes()).hexdigest(), byte_equal=True,
            retained_complete_certificate=source),
        source_parity_checks=projections, actual_nonfacial_c5_controls=extra,
        sharp_three_gap_plane_control=sharp,
        abstract_c5_two_gap_table=abstract,
        totals=dict(frozen_sources=17, baseline_source_tests=len(projections),
            baseline_odd_cycles=len(cycles), baseline_nonfacial_odd_cycles=sum(c['nonfacial'] for c in cycles),
            scanned_ordinary_two_leaf_matchings=scanned_matchings,
            additional_nonfacial_c5_matching_controls=len(extra),
            additional_nonfacial_c5_cycle_controls=sum(c['nonfacial_c5'] for c in extra_cycles),
            literal_three_gap_plane_controls=1,
            actual_two_gap_c5_triggers=sum(c['c5_two_gap_hypothesis_triggered']
                for row in all_checks for c in row['cycle_projections']),
            full_five_family_plane_sources=source['totals']['full_five_family_plane_sources'],
            all_reference_records=sum(len(c['all_references']) for c in all_checks),
            all_ten_family_pair_records=sum(len(c['all_ten_family_pairs']) for c in all_checks),
            all_pair_products=sum(len(p['reference_products']) for c in all_checks for p in c['all_ten_family_pairs']),
            complete_region_batches=sum(len(r['region_check']['complete_region_batches']) for c in all_checks for r in c['all_references']),
            singleton_witnesses=sum(len(c['all_singleton_witnesses']) for row in all_checks for c in row['cycle_projections']),
            abstract_c5_two_gap_rows=20, abstract_rejected_rows=20,
            retained_nine_cycle_controls=source['totals']['retained_nine_cycle_controls'],
            retained_three_family_controls=source['totals']['retained_three_family_controls']),
        source_sha256={p: sha256((ROOT / p).read_bytes()).hexdigest() for p in sorted(paths)})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    result = report()
    payload = canonical(result)
    if args.check:
        assert args.check.read_text() == payload, 'Nonfacial two-gap certificate differs'
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload)
    print(json.dumps(result['totals'], sort_keys=True))


if __name__ == '__main__':
    main()
