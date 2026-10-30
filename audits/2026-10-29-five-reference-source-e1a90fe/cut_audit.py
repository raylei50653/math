"""Exhaust every complement phase of every complete two-leaf reference.

The predicate is the existing common-cut predicate, unchanged.  The extra
enumeration avoids confusing one canonical 2/3 alternation with all phases.
This is a comparison audit, not a claim of a stronger obstruction.
"""
from itertools import product
from hashlib import sha256
import json

import c5_parity_shared_cut_verification as base


def reference_audit(edges, n, reference):
    complement = sorted(set(range(len(edges))) - set(reference))
    strands = base.surgery.strands([edges[e] for e in complement])
    components = [dict(s, edges=[complement[e] for e in s['edges']]) for s in strands]
    assert all(len(s['edges']) % 2 == 0 for s in components)
    phases = []
    for bits in product((0, 1), repeat=len(components)):
        labels = [1 if e in reference else 0 for e in range(len(edges))]
        for bit, component in zip(bits, components):
            for i, e in enumerate(component['edges']):
                labels[e] = 2 + (i + bit) % 2
        assert all({labels[e] for e, ends in enumerate(edges) if v in ends} == {1, 2, 3}
                   for v in range(n))
        actions = []
        for pair in base.face.PAIRS:
            for strand in base.surgery.pair_strands(edges, labels, pair):
                if not strand['ends']:
                    continue  # The existing predicate concerns boundary crosscuts.
                _, cut = base.surgery.ordered_surgery(edges, labels, n, pair, strand)
                normalized = dict(ends=[5 + v - n for v in strand['ends']])
                sides = base.shared.side_assignments(normalized, cut)
                payload = json.dumps(sides, sort_keys=True, separators=(',', ':'))
                actions.append(dict(pair=pair, path_vertices=strand['vertices'],
                    path_edges=strand['edges'], boundary_ends=[v - n for v in strand['ends']],
                    complete_ordered_cut=cut,
                    tested_assignments=sides['tested_assignments'],
                    side_only_assignments=len(sides['side_only_assignments']),
                    feasible_assignments=len(sides['feasible_assignments']),
                    complete_side_relation_sha256=sha256(payload.encode()).hexdigest()))
        assert len(actions) == 5
        phases.append(dict(component_phase=bits, edge_colors=labels, actions=actions))
    assert len(phases) == 2 ** len(components)
    assert len({tuple(row['edge_colors']) for row in phases}) == len(phases)
    return dict(matching=sorted(reference), complete_complement_components=components,
                all_component_phases=phases)


def graph_audit(graph, families, plane):
    edges, n = graph['network_edges'], graph['network_internal_vertices']
    references = []
    for family in base.PAIRS:
        for matching in families[''.join(map(str, family))]:
            references.append(dict(family=family,
                **reference_audit(edges, n, frozenset(matching))))
    actions = [action for ref in references for phase in ref['all_component_phases']
               for action in phase['actions']]
    if plane:
        assert all(a['feasible_assignments'] for a in actions)
    else:
        assert actions and all(not a['feasible_assignments'] for a in actions)
    return dict(graph=graph, all_complete_two_leaf_references=references,
                full_cut_actions=len(actions),
                feasible_actions=sum(bool(a['feasible_assignments']) for a in actions),
                status='all phases/actions pass' if plane else 'all phases/actions rejected')


def report(five):
    controls = []
    for row in five['reused_disks']:
        if row['graph']['index'] in (12, 14):
            controls.append(dict(source='original-16',
                **graph_audit(row['graph'], row['complete_even_families'], True)))
    f4 = five['reused_f4_source']
    controls.append(dict(source='frozen-F4',
        **graph_audit(f4['graph'], f4['complete_even_families'], True)))
    algebraic = five['complete_five_reference_algebraic_control']
    rejected = graph_audit(algebraic['graph'], algebraic['complete_even_families'], False)
    return dict(predicate='Existing side_assignments, both mixed systems together; all ten complete even two-leaf families, every complement phase including global 2/3 swaps, every open two-color strand, every port side word. Every Tait coloring has terminal color multiplicities 3,1,1; naming its dominant color 1 covers all states modulo color permutations, which preserve the cut predicate.',
                plane_controls=controls, non_disk_expanded_pentagram=rejected,
                strict_gain_claim=False,
                implication_between_new_source_lemma_and_old_cut_predicate='Not proved in either direction; no passing-old/rejected-new contrast is supplied.')
