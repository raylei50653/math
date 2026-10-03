#!/usr/bin/env python3
"""Necessary reductions for one original spoke omitted at a unique-mixed source.

The arbitrary-size saturation and minimal-degree-five arguments are paper
dependencies. This checker covers named singleton-position/spoke identities,
small boundary-apex skeleton certificates, and six inherited full-graph
relation controls. It neither classifies marked degree-five cores nor excludes
the remaining single-spoke omission subtype.

Run with: uv run --with networkx==3.5 python scripts/<this file> [--check]
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

import networkx as nx

from c5_independent_support_capacity import B, FRAME, ROWS, T4, U, colorings
from c5_excess_one_subcovers import singleton
from c5_941_two_spoke import relabel_mask, search
from c5_excess_two_mixed_core_spokes import validate_witness, witnesses
from c5_excess_two_mixed_core_spoke_unary import verify_subdivision
from c5_odd_join_cores import kuratowski_certificate

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_mixed_core_single_spoke/observations.json'
SOURCE = ROOT / 'artifacts/c5_independent_support_capacity/observations.json'


def independent(positions):
    return not any((i + 1) % 5 in positions for i in positions)


def rejected_positions(mask):
    assert mask & T4 == T4
    return {singleton(row) for i, row in enumerate(ROWS) if not mask >> i & 1}


def position_mask(positions):
    return sum(1 << i for i, row in enumerate(ROWS)
               if len(set(row)) == 4 or singleton(row) not in positions)


def residual_masks(target):
    rejected = rejected_positions(target)
    records = []
    for bits in range(32):
        remaining = {i for i in B if bits >> i & 1}
        if remaining <= rejected and independent(remaining):
            sigma = position_mask(remaining)
            assert sigma != target and sigma | target == sigma
            records.append(dict(rejected_singleton_positions=sorted(remaining),
                                sigma=sigma, newly_accepted_singleton_positions=
                                sorted(rejected - remaining)))
    return sorted(records, key=lambda r: r['sigma'])


def repeated_rows(target, support, endpoint):
    return {singleton(row) for i, row in enumerate(ROWS)
            if not target >> i & 1
            and any(row[b] == row[endpoint] for b in support if b != endpoint)}


def attachment_constraints(target):
    records = []
    masks = residual_masks(target)
    for size in range(4):
        for support in combinations(sorted(B), size):
            omitted = []
            for endpoint in support:
                forced = repeated_rows(target, support, endpoint)
                pairs = [(a, b) for a, b in combinations(sorted(forced), 2)
                         if (a-b) % 5 in (1, 4)]
                compatible = [r['sigma'] for r in masks
                              if forced <= set(r['rejected_singleton_positions'])]
                assert bool(compatible) == independent(forced)
                row_witnesses = []
                for i, row in enumerate(ROWS):
                    if len(set(row)) == 3 and singleton(row) in forced:
                        same, = [b for b in support if b != endpoint
                                 and row[b] == row[endpoint]]
                        row_witnesses.append(dict(row_index=i, row=row,
                            singleton_position=singleton(row),
                            identical_spoke_colors=[endpoint, same],
                            literal_color=row[endpoint]))
                omitted.append(dict(omitted_boundary_endpoint=endpoint,
                    forced_rejected_positions=sorted(forced),
                    same_row_spoke_witnesses=row_witnesses,
                    adjacent_conflicts=pairs, possible_child_sigmas=compatible))
            records.append(dict(original_root_spoke_support=support,
                omitted_spoke_constraints=omitted,
                passes_necessary_position_conditions=all(
                    not r['adjacent_conflicts'] for r in omitted)))
    assert len(records) == 26
    return records


def validate_rotation(edges, rotation):
    assert all(len(ring) == len(set(ring)) for ring in rotation)
    assert {(min(v, w), max(v, w)) for v, ring in enumerate(rotation)
            for w in ring} == edges
    graph = nx.Graph(sorted(edges))
    faces, seen = Counter(), set()
    component_ids = {v: i for i, part in enumerate(nx.connected_components(graph)) for v in part}
    for v, ring in enumerate(rotation):
        for w in ring:
            if (v, w) in seen:
                continue
            a, b = v, w
            while (a, b) not in seen:
                seen.add((a, b))
                around = rotation[b]
                assert a in around
                a, b = b, around[(around.index(a) - 1) % len(around)]
            assert (a, b) == (v, w)
            faces[component_ids[v]] += 1
    assert len(seen) == 2 * len(edges)
    for i, part in enumerate(nx.connected_components(graph)):
        edge_count = sum(set(e) <= part for e in edges)
        assert len(part) - edge_count + faces[i] == 2


def skeleton_controls(target, attachments):
    supports = [tuple(r['original_root_spoke_support']) for r in attachments
                if r['passes_necessary_position_conditions']]
    records, counts = [], Counter()
    for z_support, w_support in product(supports, repeat=2):
        # These are actual retained edges of a putative source, not a
        # coloring replacement for its original mixed/unary components.
        edges = FRAME | {(5, 6)} | {(b, 5) for b in z_support}
        edges |= {(b, 6) for b in w_support}
        augmented = edges | {(b, 7) for b in sorted(B)}
        graph = nx.Graph(sorted(augmented))
        graph.add_nodes_from(range(8))
        planar = nx.check_planarity(graph)[0]
        data = dict(root_order=[5, 6], original_spoke_supports=[z_support, w_support],
                    retained_source_edges=sorted(edges), boundary_apex=7,
                    augmented_edges=sorted(augmented))
        if not planar:
            certificate = kuratowski_certificate(graph)
            verify_subdivision(augmented, certificate)
            data.update(status='non_disk_subgraph', subdivision=certificate)
            counts['non_disk_subgraphs'] += 1
        else:
            # Store a rotation as well; passing a skeleton check asserts
            # nothing about full source disk realizability or relations.
            embedding = nx.check_planarity(graph)[1]
            data['apex_rotation'] = [list(embedding.neighbors_cw_order(v))
                                    for v in range(8)]
            validate_rotation(augmented, data['apex_rotation'])
            counts['planar_skeletons'] += 1
            if len(z_support) == len(w_support) == 3:
                # Both original sides then have only one C incidence and
                # no unary. This graph is literally G-C, whose full Sigma
                # must be Omega by the inherited omission theorem.
                rows = []
                for ri, row in enumerate(ROWS):
                    choices = colorings((5, 6), edges, dict(enumerate(row)))
                    pairs = sorted({(f[5], f[6]) for f in choices})
                    rows.append(dict(row_index=ri, root_pairs=pairs,
                        tuple_witnesses=[[row[b] for b in range(5)] + list(t)
                                         for t in pairs]))
                sigma = sum(1 << r['row_index'] for r in rows if r['root_pairs'])
                assert sigma != 1023
                data.update(G_minus_C_sigma=sigma, complete_root_relations=rows)
                if sigma & T4 != T4:
                    data.update(status='both_three_spokes_T4_conflict',
                        rejected_source_T4_row_indices=[ri for ri in range(10)
                            if T4 >> ri & 1 and not sigma >> ri & 1])
                    counts['both_three_spokes_T4_conflicts'] += 1
                else:
                    assert (sigma | target) == sigma
                    data['status'] = 'both_three_spokes_original_C_omission_conflict'
                    counts['both_three_spokes_omission_conflicts'] += 1
            else:
                data['status'] = 'necessary_skeleton_only'
                counts['remaining_necessary_skeletons'] += 1
                counts[f"remaining_total_spokes_{len(z_support)+len(w_support)}"] += 1
        records.append(data)
    return dict(ordered_named_support_pairs=len(records),
                counts=dict(sorted(counts.items())), records=records)


def D5_controls(target, attachments, masks):
    allowed = {tuple(r['original_root_spoke_support']) for r in attachments
               if r['passes_necessary_position_conditions']}
    records = []
    for sign, shift in product((-1, 1), range(5)):
        permutation = [(sign*j + shift) % 5 for j in range(5)]
        transformed = relabel_mask(target, permutation)
        assert rejected_positions(transformed) == {
            permutation[j] for j in rejected_positions(target)}
        transformed_allowed = {tuple(r['original_root_spoke_support'])
            for r in attachment_constraints(transformed)
            if r['passes_necessary_position_conditions']}
        assert transformed_allowed == {tuple(sorted(permutation[j] for j in s))
                                       for s in allowed}
        child_masks = {relabel_mask(r['sigma'], permutation) for r in masks}
        assert child_masks == {r['sigma'] for r in residual_masks(transformed)}
        records.append(dict(boundary_permutation=permutation, source_sigma=transformed,
            possible_child_sigmas=sorted(child_masks),
            allowed_named_spoke_supports=sorted(transformed_allowed)))
    return records


def five_spoke_controls(target, skeletons):
    """Original incidence identities plus inherited minimal-core source lemmas.

    Actual component relations are not synthesized here. The (3) exclusion,
    (2,1) allowed positions and split-support D attachment law are paper
    dependencies, with the original components retained in that argument.
    """
    records, counts = [], Counter()
    for skeleton in skeletons['records']:
        supports = skeleton['original_spoke_supports']
        if skeleton['status'] != 'necessary_skeleton_only' or sum(map(len, supports)) != 5:
            continue
        low_side = next(s for s in (0, 1) if len(supports[s]) == 3)
        triple, pair = supports[low_side], supports[1-low_side]
        forced = {e: repeated_rows(target, triple, e) for e in triple}
        all_forced = set().union(*forced.values())
        assert all_forced
        counts['five_spoke_named_pairs'] += 1
        data = dict(original_root_spoke_supports=supports,
            three_spoke_side=low_side, two_spoke_side=1-low_side,
            original_incidence_cases=[
                dict(mixed_incidence_at_three_two_sides=[1, 2], unary_incidences=[],
                    spoke_deleted_high_root_contact_partition=[3],
                    status='excluded_by_inherited_two_spoke_three_contact_source_theorem'),
                dict(mixed_incidence_at_three_two_sides=[1, 1], unary_incidences=[[0, 1]],
                    spoke_deleted_high_root_contact_partition=[2, 1])],
            forced_original_spoke_omissions=[dict(boundary_endpoint=e,
                rejected_singleton_positions=sorted(qs)) for e, qs in sorted(forced.items()) if qs])
        counts['mixed_1_2_original_shapes_excluded'] += 1
        second = data['original_incidence_cases'][1]
        absent = sorted(all_forced - set(pair))
        if absent:
            second.update(status='excluded_by_inherited_two_spoke_21_position_theorem',
                          rejected_singletons_absent_from_high_root_spokes=absent)
            counts['mixed_1_1_unary_position_conflicts'] += 1
        elif tuple(sorted(pair)) in FRAME:
            conflicts = []
            for e, positions in sorted(forced.items()):
                for q in sorted(positions):
                    remaining_support = sorted(set(triple) - {e})
                    row, = [r for r in ROWS if len(set(r)) == 3 and singleton(r) == q]
                    available = U - {row[b] for b in pair}
                    assert len(available) == 2 and 3 in available
                    used, = available - {3}
                    assert used in {row[b] for b in remaining_support}
                    # This demonstrates the contact's strict list slack at
                    # the used query; paper greedy extension excludes that
                    # query from the binary component's forbidden singleton.
                    high_other, = set(pair) - {q}
                    if high_other == (q-1) % 5:
                        D_support = {q, (q+1) % 5, (q+2) % 5}
                    else:
                        assert high_other == (q+1) % 5
                        D_support = {q, (q-1) % 5, (q-2) % 5}
                    outside = sorted(set(remaining_support) - D_support)
                    if outside:
                        conflicts.append(dict(omitted_spoke_endpoint=e, singleton=q,
                            literal_row=row, high_root_available_colors=sorted(available),
                            binary_used_query_excluded_by_leaf_slack=used,
                            binary_forbidden_color=3, unary_forbidden_color=used,
                            inherited_required_binary_support=sorted(D_support),
                            retained_original_root_spokes=remaining_support,
                            actual_retained_attachments_outside_required_support=outside))
            assert conflicts
            second.update(status='excluded_by_inherited_split_support_attachment_law',
                          same_source_attachment_conflicts=conflicts)
            counts['mixed_1_1_unary_split_support_conflicts'] += 1
        else:
            second.update(status='unresolved_marked_nonadjacent_two_spoke_21_core',
                          forced_singletons_in_high_root_spoke_support=sorted(all_forced))
            counts['remaining_mixed_1_1_unary_named_pairs'] += 1
        records.append(data)
    assert counts['five_spoke_named_pairs'] == (24 if target == 933 else 88)
    assert counts['mixed_1_1_unary_position_conflicts'] == (16 if target == 933 else 64)
    assert counts['mixed_1_1_unary_split_support_conflicts'] == (8 if target == 933 else 16)
    assert counts['remaining_mixed_1_1_unary_named_pairs'] == (0 if target == 933 else 8)
    return dict(counts=dict(sorted(counts.items())), records=records,
                remaining_original_named_support_pairs=[r['original_root_spoke_supports']
                    for r in records if r['original_incidence_cases'][1]['status'].startswith('unresolved')])


def full_graph_controls():
    """Six spoke reattachments at the same inherited degree-five graph.

    The inherited graph is not minimal for either of its rejected rows.
    These validate the exact join and expose the marked-coordinate gap;
    they do not refute or independently check the unique-root theorem.
    """
    original = json.loads(SOURCE.read_text())['fixed_graphs'][0]
    assert original['name'] == 'existing_943_k3_t382_submask_2045'
    n, z = original['vertices'], original['roots'][0]
    interior, base_edges = set(range(5, n)), set(map(tuple, original['edges']))
    assert n == 8 and z == 5
    controls, negative = [], None
    direct_checks, pinned_checks = 0, 0
    for w in (6, 7):
        contact, = interior - {z, w}
        for endpoint in sorted(B):
            spoke = (endpoint, w)
            if spoke in base_edges:
                continue
            source_edges = base_edges | {spoke}
            port_order = [z, w, contact]
            graph_order = list(range(n))
            rows, source_sigma = [], 0
            for ri, row in enumerate(ROWS):
                base = witnesses(interior, base_edges, row, port_order)
                for t, f in base.items():
                    validate_witness(f, graph_order, base_edges, row, port_order, t)
                filtered = {t: f for t, f in base.items() if t[1] != row[endpoint]}
                direct = witnesses(interior, source_edges, row, port_order)
                independent_direct = colorings(interior, source_edges, dict(enumerate(row)))
                assert set(filtered) == set(direct) == {
                    tuple(f[v] for v in port_order) for f in independent_direct}
                direct_checks += 1
                for t, f in direct.items():
                    validate_witness(f, graph_order, source_edges, row, port_order, t)
                fibers = []
                for a, b in product(sorted(U), repeat=2):
                    fixed = dict(enumerate(row)) | {z: a, w: b}
                    found = list(search(interior - {z, w}, base_edges, fixed))
                    # search's fixed coordinates need an explicit edge check.
                    found = [f for f in found if all(f[x] != f[y] for x, y in base_edges)]
                    expected = {t[2] for t in base if t[:2] == (a, b)}
                    assert {f[contact] for f in found} == expected
                    fibers.append(dict(root_pair=[a, b], original_contact_colors=sorted(expected)))
                    pinned_checks += 1
                root_pairs = sorted({t[:2] for t in base})
                joined_root_pairs = sorted({t[:2] for t in filtered})
                w_colors = sorted({t[1] for t in base})
                rows.append(dict(row_index=ri, literal_boundary=row,
                    complete_core_tuples=sorted(base), core_tuple_witnesses=[
                        dict(tuple=t, coloring=f) for t, f in sorted(base.items())],
                    complete_restored_tuples=sorted(filtered), restored_tuple_witnesses=[
                        dict(tuple=t, coloring=f) for t, f in sorted(direct.items())],
                    complete_root_pairs=root_pairs, restored_root_pairs=joined_root_pairs,
                    omitted_root_color_fibers=fibers))
                if filtered:
                    source_sigma |= 1 << ri
                if base and not filtered and negative is None and len(set(row)) == 3:
                    assert w_colors == [row[endpoint]]
                    negative = dict(control_index=len(controls), row_index=ri,
                        singleton_position=singleton(row), original_spoke=spoke,
                        omitted_root=w, literal_boundary=row, forced_root_color=w_colors[0],
                        core_tuples=sorted(base), original_colorings=list(base.values()),
                        restored_tuples=[], scope='Exact reattachment control; the inherited core is not q-minimal')
            assert all(sum(v in e for e in source_edges) ==
                       (5 if v in (z, w) else 4) for v in interior)
            criticality = []
            for ri, row in enumerate(ROWS):
                if original['mask'] >> ri & 1:
                    continue
                silent = next(e for e in sorted(base_edges - FRAME)
                              if not next(search(interior, base_edges - {e},
                                                 dict(enumerate(row))), None))
                criticality.append(dict(rejected_row_index=ri,
                    noncritical_original_edge=silent, still_rejects_after_deletion=True))
            controls.append(dict(inherited_graph=original['name'], core_sigma=original['mask'],
                source_sigma=source_sigma, vertex_order=graph_order, root_order=[z, w],
                original_spoke=spoke, retained_original_zw=sorted((z, w)),
                original_mixed=dict(id='C', vertices=[contact], owners=[z, w],
                    ordered_root_contacts=[[contact], [contact]], contact_order=[contact],
                    actual_support=sorted(b for b in B if (b, contact) in base_edges),
                    incident_edges=sorted(e for e in base_edges if contact in e)),
                original_unaries=[], complete_port_order=port_order,
                core_edges=sorted(base_edges), source_edges=sorted(source_edges), rows=rows,
                inherited_core_nonminimality_witnesses=criticality,
                boundary_attachments={str(v): sorted(b for b in B if (b, v) in source_edges)
                                      for v in sorted(interior)},
                scope='Fixed full graph; no disk, source-minimality, or candidate realization claim'))
    assert len(controls) == 6 and direct_checks == 60 and pinned_checks == 960
    assert negative is not None
    return dict(records=controls, whole_graph_join_checks=direct_checks,
                pinned_root_pair_checks=pinned_checks, blocked_nonempty_core_control=negative)


def build():
    targets = []
    for target in (933, 941):
        masks = residual_masks(target)
        attachments = attachment_constraints(target)
        skeletons = skeleton_controls(target, attachments)
        counts = Counter(len(r['original_root_spoke_support']) for r in attachments
                         if r['passes_necessary_position_conditions'])
        assert dict(counts) == ({0: 1, 1: 5, 2: 7, 3: 2} if target == 933
                               else {0: 1, 1: 5, 2: 9, 3: 6})
        assert len(masks) == (8 if target == 933 else 6)
        assert skeletons['ordered_named_support_pairs'] == (225 if target == 933 else 441)
        assert skeletons['counts']['non_disk_subgraphs'] == (10 if target == 933 else 48)
        assert skeletons['counts']['remaining_necessary_skeletons'] == (215 if target == 933 else 379)
        targets.append(dict(source_sigma=target, source_rejected_positions=
            sorted(rejected_positions(target)), possible_spoke_deleted_sigmas=masks,
            original_root_attachment_constraints=attachments,
            allowed_supports_by_size=dict(sorted(counts.items())),
            named_spoke_skeletons=skeletons, five_spoke_reductions=five_spoke_controls(target, skeletons),
            D5_controls=D5_controls(target, attachments, masks)))
    controls = full_graph_controls()
    dependencies = [Path(__file__), SOURCE] + [ROOT / 'scripts' / (name + '.py') for name in (
        'c5_independent_support_capacity', 'c5_excess_one_subcovers', 'c5_941_two_spoke',
        'c5_excess_two_mixed_core_spokes', 'c5_excess_two_mixed_core_spoke_unary',
        'c5_odd_join_cores')]
    paper = [ROOT / 'docs' / (name + '.md') for name in (
        'c5_excess_two_root_deletions', 'c5_excess_two_mixed_omission',
        'c5_excess_two_mixed_core_spokes', 'c5_excess_one_subcovers',
        'c5_two_spoke_three_contacts', 'c5_degree5_two_spoke_sectors',
        'c5_two_spoke_adjacent_21', 'c5_two_spoke_middle_21',
        'c5_two_spoke_reflection', 'c5_two_spoke_split_support')]
    return dict(schema=1, scope=__doc__, pattern_order=ROWS, root_color_frame=sorted(U),
        input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                      for p in dependencies + paper}, targets=targets, full_graph_controls=controls,
        summary=dict(candidate_masks=[933, 941], residual_masks_including_full_acceptance=[8, 6],
            allowed_three_spoke_supports=[2, 6], D5_identity_checks=20,
            named_root_support_pairs=666, non_disk_subdivision_certificates=58,
            planar_both_three_spokes_T4_conflicts=8,
            planar_both_three_spokes_omission_conflicts=6,
            remaining_necessary_spoke_skeletons=[215, 379], total_original_spokes_upper_bound=5,
            candidate_original_spokes_upper_bounds=[4, 5], five_spoke_named_pairs_audited=[24, 88],
            five_spoke_mixed_1_2_cases_excluded=112,
            five_spoke_mixed_1_1_unary_position_conflicts=80,
            five_spoke_mixed_1_1_unary_split_support_conflicts=24,
            five_spoke_mixed_1_1_unary_remaining_named_pairs=[0, 8],
            fixed_reattachment_graphs=6, complete_join_checks=60, pinned_root_pair_checks=960,
            original_single_spoke_omission_excluded=False, new_lean_theorem=False,
            source_graph_enumeration=False, epsilon_three_proved=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    payload = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=1) + '\n'
    if args.check:
        assert OUT.read_bytes() == payload.encode(), f'certificate differs: {OUT}'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
