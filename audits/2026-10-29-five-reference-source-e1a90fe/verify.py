#!/usr/bin/env python3
"""Source-derived singleton-hit faciality on the frozen common-rotation domain.

The old certificate is regenerated, not accepted as an oracle.  Its complete
references, C1 batches and ten family products remain attached to each source
test.  No new plane graphs or five-reference realization are asserted.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'scripts'))
import c5_five_reference_rotation_verification as five

FROZEN = ROOT / 'audits/2026-10-29-five-reference-rotation-e1a90fe/verification.json'


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n'


def source_projection(graph, check, label):
    """Keep the shared side word and every singleton witness in one relation."""
    edges = graph['network_edges']
    cycles = []
    for index, geometry in enumerate(check['common_jordan_geometry']):
        vertices = geometry['cycle_vertices']
        cycle_edges = geometry['cycle_edges']
        bits = geometry['inside_bits']
        side = dict(zip(vertices, bits))
        singleton = set()
        witnesses = []
        for reference in check['all_references']:
            hit = reference['cycle_checks'][index]['hit_edges']
            assert hit == sorted(set(cycle_edges) & set(reference['matching']))
            if len(hit) == 1:
                edge = hit[0]
                singleton.add(edge)
                assert side[edges[edge][0]] == side[edges[edge][1]]
                witnesses.append(dict(reference_id=reference['id'],
                    family=reference['family'], matching=reference['matching'],
                    singleton_hit_edge=edge, endpoints=edges[edge]))
        transitions = [edge for edge in cycle_edges
                       if side[edges[edge][0]] != side[edges[edge][1]]]
        missing = sorted(set(cycle_edges) - singleton)
        components = five.base.components(edges, singleton, vertices)
        connected = len(components) == 1
        facial = not geometry['inside_network_vertices'] and not geometry['inside_network_edges']
        assert len(transitions) % 2 == 0
        assert not set(transitions) & singleton
        assert 0 in bits, 'Connected source with exterior leaves has an outward spoke'
        assert (not facial) == bool(any(bits))
        if not facial:
            assert len(transitions) >= 2 and len(missing) >= 2
        if connected:
            assert not any(bits) and facial
        assert connected == (len(missing) <= 1)
        terminal_incidents = []
        if len(vertices) == 3:
            assert all(len(reference['cycle_checks'][index]['hit_edges']) == 1
                       for reference in check['all_references'])
            present = {tuple(reference['family']) for reference in check['all_references']}
            star = set(five.base.STAR)
            n = graph['network_internal_vertices']
            for vertex, edge in zip(vertices, geometry['off_cycle_edges']):
                other = next(v for v in edges[edge] if v != vertex)
                if other < n:
                    continue
                leaf = other - n
                assert 0 <= leaf < 5 and side[vertex] == 0
                exposing = {family for family in star if leaf in family}
                matching = star - exposing
                exposing_present = exposing & present
                matching_present = matching & present
                exposed_witnesses, matched_witnesses = [], []
                for reference in check['all_references']:
                    hit = reference['cycle_checks'][index]['hit_edges'][0]
                    incident_hit = vertex in edges[hit]
                    exposes = leaf in reference['family']
                    assert incident_hit == exposes
                    assert (edge in reference['matching']) == (not exposes)
                    witness = dict(reference_id=reference['id'],
                                   family=reference['family'], singleton_hit_edge=hit)
                    (exposed_witnesses if exposes else matched_witnesses).append(witness)
                both_statuses = bool(exposing_present and matching_present)
                if both_statuses:
                    assert len(singleton) >= 2 and connected and facial
                terminal_incidents.append(dict(cycle_vertex=vertex, terminal=other,
                    terminal_index=leaf, original_terminal_edge=edge,
                    required_exposing_families=sorted(exposing),
                    present_exposing_families=sorted(exposing_present),
                    missing_exposing_families=sorted(exposing-present),
                    required_matching_families=sorted(matching),
                    present_matching_families=sorted(matching_present),
                    missing_matching_families=sorted(matching-present),
                    exposing_reference_witnesses=exposed_witnesses,
                    matching_reference_witnesses=matched_witnesses,
                    full_five_family_support_triggered=star <= present,
                    both_terminal_statuses_triggered=both_statuses,
                    status='triggered and facial' if both_statuses else 'not triggered'))
        cycles.append(dict(cycle_index=index, actual_cycle=check['odd_cycles'][index],
            common_geometry=geometry, all_singleton_witnesses=witnesses,
            singleton_hit_union_edges=sorted(singleton),
            singleton_hit_graph_components=components,
            singleton_hit_graph_connected=connected,
            actual_side_transition_edges=transitions,
            edges_missing_from_singleton_union=missing,
            bounds_empty_network_interior=facial,
            triangle_terminal_incidence_checks=terminal_incidents,
            nonfacial_cover_exclusion_passes=facial or len(missing) >= 2,
            connected_hit_faciality_passes=not connected or facial))
    return dict(source_label=label, graph_index=graph['index'],
        minimum_required=check['minimum_required'], matching=check['matching'],
        exposed=check['exposed'], all_references=check['all_references'],
        all_ten_family_pairs=check['all_ten_family_pairs'], cycle_projections=cycles)


def report():
    old = five.report()
    assert canonical(old) == FROZEN.read_text(), 'Frozen five-reference replay differs'
    projections = []
    for row in old['reused_disks'] + [old['reused_f4_source']]:
        for family in row['adjacent_family_tests']:
            for check in family['positive_minimizer_tests']:
                projections.append(source_projection(row['graph'], check,
                    'fixed-adjacent-family positive odd minimum'))
    for control in old['nine_cycle_negative_control']:
        projections.append(source_projection(old['reused_f4_source']['graph'],
            control['common_rotation_check'], 'actual nine-cycle nonminimum negative control'))
    cycles = [cycle for row in projections for cycle in row['cycle_projections']]
    nonfacial = [row for row in cycles if not row['bounds_empty_network_interior']]
    connected = [row for row in cycles if row['singleton_hit_graph_connected']]
    terminal_checks = [terminal for cycle in cycles
                      for terminal in cycle['triangle_terminal_incidence_checks']]
    assert len(projections) == 4 and len(cycles) == 5
    assert len(nonfacial) == 3 and len(connected) == 1
    assert {row['graph_index'] for row in old['three_family_shared_cut_negative_controls']} == {12, 14}
    import cut_audit
    cuts = cut_audit.report(old)
    paths = {Path(__file__).relative_to(ROOT),
             (HERE / 'cut_audit.py').relative_to(ROOT), FROZEN.relative_to(ROOT)}
    paths.update(Path(path) for path in old['source_sha256'])
    paths.update(Path('scripts') / name for name in (
        'four_color_shared_cut_obstruction.py', 'four_color_counts_face.py',
        'c5_equivalent_forms_check.py'))
    return dict(base=old['base'],
        scope='R5-FACIALITY, F5-NONFACIAL-COVER and F5-TRIANGLE-LEAF; complete frozen-source calibration, no generator extension, five-family plane realization, E932 or 4CT conclusion.',
        frozen_replay=dict(path=str(FROZEN.relative_to(ROOT)),
            sha256=sha256(FROZEN.read_bytes()).hexdigest(), byte_equal_independent_replay=True,
            old_totals=old['totals']),
        source_projections=projections, full_old_common_cut_phase_audit=cuts,
        retained_nine_cycle_controls=old['nine_cycle_negative_control'],
        retained_three_family_controls=old['three_family_shared_cut_negative_controls'],
        totals=dict(source_tests=len(projections), positive_minimum_tests=len(projections)-1,
            actual_odd_cycles=len(cycles), nonfacial_odd_cycles=len(nonfacial),
            connected_singleton_hit_graphs=len(connected),
            forced_facial_cases=len(connected), nonfacial_cover_violations=0,
            triangle_terminal_incidence_checks=len(terminal_checks),
            triangle_two_status_triggers=sum(row['both_terminal_statuses_triggered']
                                            for row in terminal_checks),
            triangle_full_five_family_triggers=sum(row['full_five_family_support_triggered']
                                                 for row in terminal_checks),
            full_five_family_plane_sources=old['totals']['five_nonempty_reference_disk_cases'],
            retained_nine_cycle_controls=len(old['nine_cycle_negative_control']),
            retained_three_family_controls=len(old['three_family_shared_cut_negative_controls'])),
        source_sha256={str(path): sha256((ROOT / path).read_bytes()).hexdigest()
                       for path in sorted(paths)})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    result = report()
    payload = canonical(result)
    if args.check:
        assert args.check.read_text() == payload, 'Source-faciality certificate differs'
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload)
    print(json.dumps(result['totals'], sort_keys=True))


if __name__ == '__main__':
    main()
