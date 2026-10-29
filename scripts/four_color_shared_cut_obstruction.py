#!/usr/bin/env python3
"""Exact common-side obstruction for the marked pentagram countermodel.

This tests a necessary condition for ONE boundary-to-boundary path in a
plane disk, using its two actual exterior matchings on a common cut.
It excludes this non-disk countermodel, not arbitrary support 932.
See docs/four_color_counts_surgery_verification.md for the paper contract.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

import c5_dual_path_surgery as surgery
import four_color_counts_face as face


ROOT = Path(__file__).resolve().parents[1]


def side_assignments(strand, cut, systems=None):
    """Enumerate common side labels and ordered noncrossing constraints.

    The oriented path runs from e_s to e_t, s<t. The two complementary
    boundary arcs have orders (t-1,...,s+1) and (t+1,...,4,0,...,s-1).
    Each cut port t_i has ONE side shared by both exterior systems.
    Input consists only of ordered ports and exterior-segment endpoints.
    """
    start, end = [v - 5 for v in strand['ends']]
    assert 0 <= start < end < 5
    arcs = [list(reversed(range(start + 1, end))),
            list(range(end + 1, 5)) + list(range(start))]
    rows = cut['cuts'] if systems is None else [cut['cuts'][i] for i in systems]
    m = len(cut['port_vertices'])
    feasible, side_only, rejected = [], [], []
    for bits in product((0, 1), repeat=m):
        side = {f't{i}': z for i, z in enumerate(bits)}
        for z, arc in enumerate(arcs):
            side.update({f'e{i}': z for i in arc})
        orders = [[f't{i}' for i in range(m) if bits[i] == z]
                  + [f'e{i}' for i in arc] for z, arc in enumerate(arcs)]
        mismatch = None
        for ci, row in enumerate(rows):
            for si, segment in enumerate(row['exterior_segments']):
                u, v = segment['ends']
                if side[u] != side[v]:
                    mismatch = dict(kind='opposite_sides', system=ci, segment=si,
                                    ends=[u, v], sides=[side[u], side[v]])
                    break
            if mismatch is not None:
                break
        if mismatch is not None:
            rejected.append(dict(bits=bits, witness=mismatch))
            continue
        side_only.append(bits)
        crossing = None
        for ci, row in enumerate(rows):
            for z, order in enumerate(orders):
                endpoints = [tuple(sorted(order.index(v) for v in segment['ends']))
                             for segment in row['exterior_segments']
                             if side[segment['ends'][0]] == z]
                for (a, b), (c, d) in combinations(endpoints, 2):
                    if a < c < b < d or c < a < d < b:
                        crossing = dict(kind='interleaving', system=ci, side=z,
                                        order=order, pairs=[[a, b], [c, d]])
                        break
                if crossing is not None:
                    break
            if crossing is not None:
                break
        if crossing is not None:
            rejected.append(dict(bits=bits, witness=crossing))
        else:
            feasible.append(dict(bits=bits, side_orders=orders))
    assert len(rejected) + len(feasible) == 2 ** m
    return dict(boundary_arcs=arcs, tested_assignments=2 ** m,
                side_only_assignments=side_only, feasible_assignments=feasible,
                rejected_assignments=rejected)


def cycle_states(edges):
    """All actual Tait colorings, for either step-one or step-two cycle."""
    states = []
    for values in product((1, 2, 3), repeat=5):
        ports = []
        for v in range(5):
            incident = [values[i] for i, e in enumerate(edges[5:]) if v in e]
            if len(set(incident)) != 2:
                break
            ports.append(6 - sum(incident))
        else:
            states.append(tuple(ports) + values)
    return tuple(sorted(states))


def audit_pole(edges, states):
    rows = []
    for sid, labels in enumerate(states):
        for pair in face.PAIRS:
            for strand in surgery.pair_strands(edges, labels, pair):
                assert strand['ends']  # these two odd-cycle poles have no 2-color cycles
                _, cut = surgery.ordered_surgery(edges, labels, 5, pair, strand)
                test = side_assignments(strand, cut)
                rows.append(dict(state=sid, source_edge_colors=labels, pair=pair,
                                 path_vertices=strand['vertices'], path_edges=strand['edges'],
                                 boundary_ends=[v - 5 for v in strand['ends']],
                                 cut=cut, sides=test))
    assert len(rows) == 150
    return rows


def report():
    negative_edges = face.EDGES
    negative_states = cycle_states(negative_edges)
    assert negative_states == face.colorings()
    negative = audit_pole(negative_edges, negative_states)
    assert all(not r['sides']['feasible_assignments'] for r in negative)
    side_failures = [r for r in negative if not r['sides']['side_only_assignments']]
    assert len(side_failures) == 60
    assert len({r['state'] for r in negative}) == 30

    # Positive control has the same number of vertices, edges, states and
    # true path actions; its terminals follow the actual internal cycle.
    positive_edges = tuple((i, 5 + i) for i in range(5)) + tuple((i, (i + 1) % 5) for i in range(5))
    positive_states = cycle_states(positive_edges)
    assert len(positive_states) == 30
    positive = audit_pole(positive_edges, positive_states)
    assert all(r['sides']['feasible_assignments'] for r in positive)

    # The first rejection has a minimal two-system same-side conflict:
    # t0 connects to e4 in E13 and to e2 in E23, across opposite boundary arcs.
    first = negative[0]
    assert first['boundary_ends'] == [0, 3] and first['pair'] == (1, 2)
    assert first['cut']['port_vertices'] == [0, 3]
    endpoints = [set(tuple(seg['ends']) for seg in row['exterior_segments'])
                 for row in first['cut']['cuts']]
    assert ('t0', 'e4') in endpoints[0] and ('t0', 'e2') in endpoints[1]
    strand = dict(ends=[5, 8])
    # Removing either exterior system loses the contradiction.
    erasures = [side_assignments(strand, first['cut'], [i]) for i in (0, 1)]
    assert all(r['feasible_assignments'] for r in erasures)
    # Even choosing different side labels independently for the two systems
    # accepts this source, showing why one shared port label is necessary.
    common = {tuple(r['bits']) for r in erasures[0]['feasible_assignments']} & {
              tuple(r['bits']) for r in erasures[1]['feasible_assignments']}
    assert not common

    deps = [Path(__file__), ROOT / 'scripts/four_color_counts_face.py',
            ROOT / 'scripts/c5_dual_path_surgery.py', ROOT / 'scripts/c5_kempe_connectivity.py',
            ROOT / 'scripts/four_color_counts_cone_verification.py',
            ROOT / 'scripts/ck_kempe_obstruction.py',
            ROOT / 'scripts/c5_adjacent_singleton_counts.py', ROOT / 'scripts/c5_kempe_screen.py']
    return dict(scope='Necessary one-cut common-side test. Excludes this marked non-disk pole, not all 932 sources.',
                soundness='A simple boundary-to-boundary component is a disk crosscut. Each third edge has one common side; each actual exterior strand stays on that side and strands of either one system do not interleave.',
                negative=dict(edges=negative_edges, states=len(negative_states), actions=len(negative),
                              shared_side_failures=len(side_failures),
                              noncrossing_failures_after_sides=len(negative) - len(side_failures),
                              rows=negative),
                positive=dict(edges=positive_edges, states=len(positive_states), actions=len(positive),
                              feasible_histogram=dict(sorted(Counter(len(r['sides']['feasible_assignments']) for r in positive).items())),
                              rows=positive),
                minimal_two_system_conflict=dict(negative_row=0, shared_port='t0',
                    first_system_ends=['t0', 'e4'], second_system_ends=['t0', 'e2'],
                    forced_sides=[1, 0], deleting_each_system=erasures,
                    independent_system_side_choices_accepted=True),
                source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in deps})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    result = report()
    payload = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + '\n'
    if args.check:
        assert args.check.read_text() == payload, 'Shared-cut certificate differs'
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload)
    print(json.dumps(dict(negative_actions=result['negative']['actions'],
                          shared_side_failures=result['negative']['shared_side_failures'],
                          noncrossing_failures=result['negative']['noncrossing_failures_after_sides'],
                          positive_actions=result['positive']['actions'],
                          positive_feasible_histogram=result['positive']['feasible_histogram']), sort_keys=True))


if __name__ == '__main__':
    main()
