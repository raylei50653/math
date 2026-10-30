#!/usr/bin/env python3
"""Necessary three-gap C5 interface and a full-source direct-leaf exclusion.

The side table is not a source existence claim.  Actual references, complete
returns, C1 batches and all ten products are retained in the literal control
and in the byte-replayed predecessor certificate.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

import c5_nonfacial_two_gap_verification as previous
from c5_three_gap_chord_transfer import chord_transfer

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / 'audits/2026-10-30-five-reference-two-gap/verification.json'
EDGES = [(i, (i + 1) % 5) for i in range(5)]
GAMMA = list(previous.five.base.STAR)
HITS = [list(h) for size in (1, 2) for h in combinations(range(5), size)
        if len({v for e in h for v in EDGES[e]}) == 2 * size]


def allowed_hits(bits):
    n_parity = sum(bits) % 2
    return [h for h in HITS
            if sum(bits[v] for e in h for v in EDGES[e]) % 2 == 0
            and (len(h) != 1 or all(bits[v] == n_parity == 0
                                    for e in h for v in EDGES[e]))]


def side_classification():
    rows, survivors = [], []
    for gaps in combinations(range(5), 3):
        e1 = sorted(set(range(5)) - set(gaps))
        for bits in product((0, 1), repeat=5):
            if len(set(bits)) != 2:
                continue
            hits = allowed_hits(bits)
            unavailable = [e for e in e1 if [e] not in hits]
            # E1 is an exact existence projection, with each required edge
            # having some actual singleton witness; the witnesses may differ.
            passed = not unavailable
            row = dict(gaps=list(gaps), required_E1=e1, actual_side_word=list(bits),
                       strict_interior_parity=sum(bits) % 2,
                       necessary_hit_profiles=hits,
                       unavailable_required_singletons=unavailable,
                       necessary_interface_passes=passed)
            rows.append(row)
            if passed:
                inward = [i for i, b in enumerate(bits) if b]
                assert len(inward) == 2 and any(set(EDGES[e]) == set(inward) for e in range(5))
                assert e1 == [e for e, (u, v) in enumerate(EDGES) if not bits[u] and not bits[v]]
                assert len(hits) == 5
                survivors.append(row)
    assert len(rows) == 300 and len(survivors) == 5
    canonical = next(r for r in survivors if r['actual_side_word'] == [1, 1, 0, 0, 0])
    assert canonical['required_E1'] == [2, 3]
    assert canonical['necessary_hit_profiles'] == [[2], [3], [0, 2], [0, 3], [1, 4]]
    return dict(classification='Necessary abstract interface, not full source realizability.',
                cycle_edges=EDGES, all_nonempty_matching_hits=HITS, all_rows=rows,
                surviving_rows=survivors, rows=300, rejected_rows=295)


def complete_local_return_table():
    """Keep each retained arc, including isolated vertices, and formal inner P.

    P is a symbolic complete 0--1 return with odd length, derived from the
    common even strict-vertex count. It does not assert any cap realization.
    """
    rows = []
    for hit in allowed_hits([1, 1, 0, 0, 0]):
        inward = sorted({v for e in hit for v in EDGES[e]} & {0, 1})
        outer = sorted({v for e in hit for v in EDGES[e]} & {2, 3, 4})
        arcs = previous.five.pieces(EDGES, set(range(5)) - set(hit), range(5))
        # A one-edge representative of the required odd P suffices to verify
        # the parity calculation, not to certify arbitrary source geometry.
        formal_edges = EDGES + [(0, 1)]
        retained = (set(range(5)) - set(hit)) | ({5} if inward else set())
        glued = previous.five.pieces(formal_edges, retained)
        paths = [p for p in glued if p['ends']]
        cycles = [p for p in glued if not p['ends']]
        assert len(paths) == 1 and set(paths[0]['ends']) == set(outer)
        assert paths[0]['parity'] == 0
        assert all(c['parity'] == 0 for c in cycles)
        assert inward in ([], [0, 1]) and len(outer) == 2
        rows.append(dict(hit_edges=hit, inward_active_vertices=inward,
                         exterior_active_vertices=outer,
                         complete_retained_cycle_arcs=arcs,
                         required_inner_return=None if not inward else
                             dict(ends=[0, 1], length_parity=1),
                         all_other_inner_components='Complete even cycles; all strict vertices retained.',
                         formal_gluing_with_length_one_representative=glued,
                         induced_exterior_path_parity=0,
                         additional_inner_closed_cycle=bool(cycles),
                         exterior_obligation='Keep every actual return and terminal path; any closed external return must be even.'))
    assert len(rows) == 5
    return rows


def direct_leaf_subtype():
    hits = allowed_hits([1, 1, 0, 0, 0])
    rows = []
    for vertices in combinations((2, 3, 4), 2):
        for terminals in combinations(range(5), 2):
            assignments = []
            for assigned in (terminals, tuple(reversed(terminals))):
                family_rows = []
                for family in GAMMA:
                    forced_matched_vertices = [v for v, t in zip(vertices, assigned) if t not in family]
                    required_hit_vertices = [v for v, t in zip(vertices, assigned) if t in family]
                    possible = [h for h in hits if not any(
                        v in EDGES[e] for v in forced_matched_vertices for e in h)
                        and all(any(v in EDGES[e] for e in h) for v in required_hit_vertices)]
                    if not set(terminals) & set(family):
                        assert not possible
                    family_rows.append(dict(family=family,
                        direct_terminals_exposed=[t for t in terminals if t in family],
                        forced_matched_cycle_vertices=forced_matched_vertices,
                        required_hit_cycle_vertices=required_hit_vertices,
                        all_remaining_hit_profiles=possible,
                        disjoint_terminal_pair=not bool(set(terminals) & set(family))))
                assignments.append(dict(ordered_vertex_terminal_attachments=list(zip(vertices, assigned)),
                    all_five_family_relations=family_rows))
            absent = [family for family in GAMMA if not set(terminals) & set(family)]
            assert 1 <= len(absent) <= 2
            rows.append(dict(exterior_cycle_vertices=vertices, direct_terminal_pair=terminals,
                all_two_terminal_assignments=assignments,
                forced_empty_Gamma_families=absent, full_Gamma_impossible=True))
    assert len(rows) == 30
    assert sum(len(r['forced_empty_Gamma_families']) for r in rows) == 45
    return dict(classification='Exclusion of two directly terminal-attached exterior vertices; all full-reference hit possibilities retained.',
                rows=rows, placement_pair_rows=30, ordered_attachment_rows=60,
                forced_empty_family_records=45)


def literal_control_check(control):
    check = control['parity_check']
    refs = check['all_references']
    assert len(refs) == 6
    geom = check['cycle_projections'][0]
    assert geom['common_geometry']['inside_chord_edges'] == [5]
    assert geom['common_geometry']['inside_bits'] == [1, 1, 0, 0, 0]
    hits = allowed_hits([1, 1, 0, 0, 0])
    for ref in refs:
        assert ref['cycle_checks'][0]['hit_edges'] in hits
        assert ref['cycle_checks'][0]['complete_reference_return_segments']
        assert ref['cycle_checks'][0]['complete_difference_segments']
        assert ref['region_check']['complete_region_batches']
    pairs = check['all_ten_family_pairs']
    assert len(pairs) == 10
    for pair in pairs:
        first, second = map(tuple, pair['families'])
        assert len(pair['reference_products']) == sum(tuple(r['family']) == first for r in refs) * sum(
            tuple(r['family']) == second for r in refs)
    support = sorted(p for p, ms in control['complete_even_families'].items() if ms)
    assert support == ['02', '03', '24', '34']
    # Direct leaves are t0 at v2 and t4 at v4: the subtype predicts all of M13
    # empty, rather than incorrectly rejecting this weaker actual plane source.
    assert control['graph']['network_edges'][6] == (2, 7)
    assert control['graph']['network_edges'][12] == (4, 11)
    assert not control['complete_even_families']['13']
    return dict(complete_even_support=support,
                missing_Gamma_families=['13', '14'], adjacent_even_families=['34'],
                subtype_disjoint_family_for_direct_leaves_0_4='13',
                all_references=len(refs), singleton_references=sum(len(r['cycle_checks'][0]['hit_edges']) == 1 for r in refs),
                double_hit_references=sum(len(r['cycle_checks'][0]['hit_edges']) == 2 for r in refs),
                all_ten_family_pair_records=len(pairs),
                all_pair_products=sum(len(p['reference_products']) for p in pairs),
                all_C1_batches=sum(len(r['region_check']['complete_region_batches']) for r in refs),
                full_Gamma_hypothesis=False)


def report():
    inherited = previous.report()
    assert previous.canonical(inherited) == FROZEN.read_text(), 'Predecessor replay differs'
    control = inherited['sharp_three_gap_plane_control']
    abstract = side_classification()
    literal = literal_control_check(control)
    transfer = chord_transfer(control)
    paths = set(inherited['source_sha256']) | {
        str(FROZEN.relative_to(ROOT)), str(Path(__file__).relative_to(ROOT)),
        'scripts/c5_three_gap_chord_transfer.py'}
    return dict(base=inherited['base'],
        scope='Three-gap side/chord/hit classification and two-exterior-direct-leaf subtype exclusion; remaining three-gap sources, facial C5, four/five gaps, E932 and 4CT OPEN.',
        predecessor=dict(path=str(FROZEN.relative_to(ROOT)), sha256=sha256(FROZEN.read_bytes()).hexdigest(),
            byte_equal_replay=True, all_complete_source_relations_retained_by_reference=True,
            totals=inherited['totals']),
        abstract_side_classification=abstract,
        complete_local_return_parity_table=complete_local_return_table(),
        direct_leaf_subtype=direct_leaf_subtype(),
        retained_literal_three_gap_control=control,
        literal_control_summary=literal, ordinary_PM_chord_transfer=transfer,
        totals=dict(abstract_side_rows=300, rejected_side_rows=295, surviving_rotations=5,
            allowed_hit_profiles=5, subtype_terminal_pair_rows=30, subtype_ordered_attachment_rows=60,
            forced_empty_family_records=45,
            literal_controls=1, full_Gamma_plane_controls=0, **literal),
        source_sha256={p: sha256((ROOT / p).read_bytes()).hexdigest() for p in sorted(paths)})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    result = report()
    payload = previous.canonical(result)
    if args.check:
        assert args.check.read_text() == payload, 'Three-gap certificate differs'
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload)
    print(json.dumps(result['totals'], sort_keys=True))


if __name__ == '__main__':
    main()
