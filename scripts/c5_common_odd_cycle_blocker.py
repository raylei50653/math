#!/usr/bin/env python3
"""Complete algebraic five-reference control, explicitly outside the disk class.

Expand every vertex of the marked pentagram pole into a triangle.  This
preserves its even-complement support, while making every ordinary two-leaf
family nonempty.  The ordinary double-dimer counts pass; existing actual
boundary noncrossing and shared-cut tests already reject the marked graph.
An additional proposed local side word on an odd triangle is rejected by the
common odd-cycle side equations.  None of these data is a plane 932 source.
"""
from __future__ import annotations

from itertools import combinations, product

import c5_parity_shared_cut_verification as base


def make_graph():
    """Original edge IDs are assigned once, before any matching enumeration."""
    ports = {}
    for i in range(5):
        neighbors = sorted(j for pair in base.STAR if i in pair
                           for j in pair if j != i) + [5 + i]
        ports[i] = {j: 3 * i + k for k, j in enumerate(neighbors)}
    edges = [pair for i in range(5)
             for pair in combinations(range(3 * i, 3 * i + 3), 2)]
    edges += [(ports[i][j], ports[j][i]) for i, j in base.STAR]
    edges += [(ports[i][5 + i], 15 + i) for i in range(5)]
    return dict(network_internal_vertices=15, network_edges=edges,
                terminal_vertices=list(range(15, 20)),
                requested_terminal_order=list(range(5)),
                triangle_ports={str(i): {str(j): v for j, v in ps.items()}
                                for i, ps in ports.items()},
                provenance='Deterministic triangle expansion of marked step-two five-pole; no primal disk supplied.')


def traces(edges, selected):
    ids = sorted(selected)
    return [dict(s, edges=[ids[e] for e in s['edges']])
            for s in base.surgery.strands([edges[e] for e in ids])]


def _regions(edges, n, matching, reference, old_cycles):
    regions = base.components(edges, set(range(len(edges))) - (matching & reference),
                              range(n + 5))
    rows = []
    for region in regions:
        vs = set(region['vertices'])
        toggle = frozenset(e for e in matching ^ reference if set(edges[e]) <= vs)
        gain = sum(set(c['vertices']) <= vs for c in old_cycles)
        syndrome = [int(any(n + i in edges[e] for e in toggle)) for i in range(5)]
        rows.append(dict(vertices=region['vertices'], region_edges=region['edges'],
                         toggle=sorted(toggle), gain=gain, syndrome=syndrome))
    wm = base.word(edges, n, matching)
    batches = []
    minimum = base.odd(edges, matching)
    for mask in range(1 << len(rows)):
        new, gain, syndrome = matching, 0, [0] * 5
        selected = [i for i in range(len(rows)) if mask >> i & 1]
        for i in selected:
            row = rows[i]
            new ^= frozenset(row['toggle'])
            gain += row['gain']
            syndrome = [a ^ b for a, b in zip(syndrome, row['syndrome'])]
        assert base.saturated(edges, n, new)
        assert base.odd(edges, new) == minimum - gain
        assert base.word(edges, n, new) == tuple(a ^ b for a, b in zip(wm, syndrome))
        if not any(syndrome):
            assert gain == 0
        batches.append(dict(selected_regions=selected, matching=sorted(new),
                            odd=minimum - gain, syndrome=syndrome,
                            exposed=[i for i, x in enumerate(base.word(edges, n, new)) if not x]))
    positive = [i for i, row in enumerate(rows) if row['gain']]
    changed = sum(a != b for a, b in zip(wm, base.word(edges, n, reference)))
    assert len(positive) <= changed // 2
    assert all(any(rows[i]['syndrome']) for i in positive)
    return dict(regions=rows, positive_region_ids=positive,
                terminal_support_bound=changed // 2, complete_region_batches=batches)


def _shared_cut_audit(edges, n, reference):
    """Replay the existing necessary test; do not assume this control passes."""
    labels = [1 if e in reference else 0 for e in range(len(edges))]
    selected = [e for e in range(len(edges)) if e not in reference]
    for strand in base.surgery.strands([edges[e] for e in selected]):
        assert len(strand['edges']) % 2 == 0
        for j, local_e in enumerate(strand['edges']):
            labels[selected[local_e]] = 2 + j % 2
    rows = []
    for pair in base.face.PAIRS:
        for strand in base.surgery.pair_strands(edges, labels, pair):
            if not strand['ends']:
                continue
            _, cut = base.surgery.ordered_surgery(edges, labels, n, pair, strand)
            normalized = dict(ends=[5 + v - n for v in strand['ends']])
            sides = base.shared.side_assignments(normalized, cut)
            rows.append(dict(pair=pair, path_vertices=strand['vertices'],
                             path_edges=strand['edges'], cut=cut,
                             tested_assignments=sides['tested_assignments'],
                             side_only_assignments=len(sides['side_only_assignments']),
                             feasible_assignments=len(sides['feasible_assignments'])))
    return dict(edge_colors=labels, actions=rows)


def report():
    graph = make_graph()
    edges, n = graph['network_edges'], graph['network_internal_vertices']
    families = {p: base.matchings(edges, n, p)
                for size in (0, 2, 4) for p in combinations(range(5), size)}
    pm = {p: families[p] for p in base.PAIRS}
    good = {p: [m for m in ms if base.odd(edges, m) == 0] for p, ms in pm.items()}
    assert all(len(ms) == 2 for ms in pm.values())
    assert all(len(good[p]) == int(p in base.STAR) for p in base.PAIRS)
    target = (0, 1)
    minimum = min(base.odd(edges, m) for m in pm[target])
    minimizers = [m for m in pm[target] if base.odd(edges, m) == minimum]
    assert minimum == 1 and len(minimizers) == 1
    matching = minimizers[0]
    old_cycles = [c for c in base.components(edges, set(range(len(edges))) - matching)
                  if c['cycle'] and len(c['edges']) % 2]
    assert len(old_cycles) == 1
    cycle = old_cycles[0]
    assert cycle['vertices'] == [9, 10, 11] and cycle['edges'] == [9, 10, 11]
    proposed_side = {9: 1, 10: 0, 11: 0}  # 1 denotes Jordan interior.
    references = []
    for pair in base.STAR:
        for rid, reference in enumerate(good[pair]):
            hit = sorted(set(cycle['edges']) & reference)
            assert len(hit) == 1
            arcs = traces(edges, set(cycle['edges']) - reference)
            for arc in arcs:
                arc['parity'] = len(arc['edges']) % 2
            assert len(arcs) == 1 and arcs[0]['parity'] == 0
            active = sorted(v for e in hit for v in edges[e])
            parity = sum(proposed_side[v] for v in active) % 2
            references.append(dict(exposed=pair, reference_index=rid,
                matching=sorted(reference), odd_cycle_hits=hit,
                complete_retained_odd_cycle_arcs=arcs, active_spoke_vertices=active,
                proposed_interior_active_parity=parity,
                proposed_side_equation_holds=(parity == 0),
                region_check=_regions(edges, n, matching, reference, old_cycles),
                exact_full_rewire=base.parity_rewire(edges, n, matching, reference),
                previous_actual_shared_cut=_shared_cut_audit(edges, n, reference)))
    pairs = []
    for first, second in combinations(base.STAR, 2):
        products = []
        for a, r in product(good[first], good[second]):
            difference = traces(edges, a ^ r)
            leaf_paths = [sorted(v - n for v in row['ends'])
                          for row in difference if row['ends']]
            crossing = False
            if len(leaf_paths) == 2:
                (u, v), (x, y) = leaf_paths
                crossing = u < x < v < y or x < u < y < v
            products.append(dict(first_matching=sorted(a), second_matching=sorted(r),
                first_cycle_hits=sorted(set(cycle['edges']) & a),
                second_cycle_hits=sorted(set(cycle['edges']) & r),
                first_retained_cycle_arcs=traces(edges, set(cycle['edges']) - a),
                second_retained_cycle_arcs=traces(edges, set(cycle['edges']) - r),
                complete_reference_difference=difference,
                previous_leaf_path_pairs=leaf_paths,
                previous_boundary_noncrossing_holds=not crossing))
        pairs.append(dict(families=[first, second], reference_products=products,
                          status='triggered and holds' if products else 'not triggered'))
    assert len(pairs) == 10 and all(len(p['reference_products']) == 1 for p in pairs)
    # All five equations use one side word.  The three distinct hit edges
    # force all triangle vertices onto one side.  Its leaf spoke is exterior.
    solutions = []
    for bits in product((0, 1), repeat=3):
        side = dict(zip(cycle['vertices'], bits))
        if all(sum(side[v] for v in row['active_spoke_vertices']) % 2 == 0
               for row in references):
            solutions.append(bits)
    assert solutions == [(0, 0, 0), (1, 1, 1)]
    exterior_leaf_spoke = next(e for e in matching if 11 in edges[e] and 18 in edges[e])
    assert exterior_leaf_spoke == 23
    assert any(not row['proposed_side_equation_holds'] for row in references)
    cuts = [action for row in references
            for action in row['previous_actual_shared_cut']['actions']]
    assert len(cuts) == 25 and all(row['feasible_assignments'] == 0 for row in cuts)
    crossings = sum(not product_row['previous_boundary_noncrossing_holds']
                    for pair in pairs for product_row in pair['reference_products'])
    assert crossings == 5
    return dict(graph=graph,
        classification='Complete algebraic five-reference control with a deliberately impossible proposed local side word; not a plane disk or a 932 source.',
        complete_pm_families={''.join(map(str, p)): [sorted(m) for m in ms]
                              for p, ms in families.items()},
        complete_even_families={''.join(map(str, p)): [sorted(m) for m in ms]
                                for p, ms in good.items()},
        ordinary_counts={''.join(map(str, p)): len(ms) for p, ms in families.items()},
        even_counts={''.join(map(str, p)): len(ms) for p, ms in good.items()},
        double_dimer=base.double_dimer(edges, families),
        selected_target=target, selected_matching=sorted(matching),
        minimum_odd=minimum, minimum_matchings=[sorted(m) for m in minimizers],
        odd_cycle=cycle, all_five_references=references, all_ten_family_pairs=pairs,
        proposed_jordan_interior_bits={str(v): bit for v, bit in proposed_side.items()},
        common_side_solutions=solutions,
        leaf_spoke_forced_exterior=dict(vertex=11, terminal=18, edge=exterior_leaf_spoke),
        previous_conditions=dict(T1_all_five_hits=True, C1_all_five_complete_regions=True,
            exact_full_rewires=True, double_dimer_all_five=True,
            boundary_noncrossing_rejects_family_products=crossings,
            canonical_shared_cut_actions=len(cuts), canonical_shared_cut_feasible_actions=0,
            scope='New side equations strengthen the listed algebraic summaries; the existing full boundary/shared-cut package already rejects this graph.'))


if __name__ == '__main__':
    import json
    print(json.dumps(report(), ensure_ascii=False, sort_keys=True, indent=2))
