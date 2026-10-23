#!/usr/bin/env python3
"""Read-only fixed skeleton checks. Jordan and arbitrary-size claims are paper proofs."""
import argparse
from collections import Counter, deque
from copy import deepcopy
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import random
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PREVDIR = 'audits/2026-10-23-941-patch-order-6b09cd4'
BASE = '6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def authority():
    m = json.loads((HERE / 'INPUTS.json').read_text())
    require(m['base'] == BASE, 'BASE changed')
    for row in m['inputs']:
        data = (HERE / row['snapshot']).read_bytes()
        require((len(data), sha256(data).hexdigest()) == (row['bytes'], row['sha256']), 'frozen authority drift')
        require(data == (ROOT / row['path']).read_bytes(), 'live authority drift: ' + row['path'])
    for row in m['preserved_previous_outputs']:
        data = (ROOT / row['path']).read_bytes()
        require((len(data), sha256(data).hexdigest()) == (row['bytes'], row['sha256']), 'previous output drift')
    routing = []
    for row in m['routing_entry']:
        data = (HERE / row['snapshot']).read_bytes()
        require((len(data), sha256(data).hexdigest()) == (row['bytes'], row['sha256']), 'routing snapshot drift')
        routing.append(dict(path=row['path'], changed=data != (ROOT / row['path']).read_bytes()))
    return m, routing


def predecessor(c, seed):
    old = json.loads((HERE / 'frozen' / PREVDIR / 'certificate.json').read_text())
    require(c['complete_predecessor_certificate'] == old, 'complete predecessor fibres/lifts changed')
    spec = importlib.util.spec_from_file_location('frozen_patch_order', HERE / 'frozen' / PREVDIR / 'check.py')
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module); module.HERE = HERE
    stats = module.validate(old, seed)
    wanted = [r for r in old['exact_two_shared_schemas'] if r['shared_colors'] == [0, 2]]
    records = c['shared02_short_segments']
    require(len(records) == 4, 'missing shared02 center choice')
    require(sorted(r['complete_predecessor_schema']['diagonal_choices'] for r in records) == [[0, 0], [0, 1], [1, 0], [1, 1]], 'center choice domain incomplete')
    for row in records:
        prev = row['complete_predecessor_schema']; require(prev in wanted, 'shared02 inherited original faces changed')
        require(row['internal_beta_midpoint_colors'] == [0, 2] and row['missing_P_bridge_midpoint_colors'] == [0, 1], 'P bridge identity lost')
        require(row['exactly_two_crossing_six_point_branch'] == 'excluded', 'six-point child wrongly retained')
        # The only interior midpoint on this two-face beta chain is its shared02 edge.
        require(prev['consecutive_interface'] == 'beta' and prev['intervening_side'] == 'K', 'short segment side changed')
    return stats


def ownership(record):
    require(record['states'] == list(range(4)) and record['adjacent_face_maximum_change'] == 1, 'face ownership domain changed')
    require(record['p_incident_face_values'] == [0, 0] and record['center_face_value'] == 3, 'rootless/center face ownership changed')
    todo = deque([(3, 0)]); visited = {3}; distance = None
    while todo:
        value, steps = todo.popleft()
        if value == 0:
            distance = steps; break
        for nxt in range(4):
            if abs(nxt - value) <= 1 and nxt not in visited:
                visited.add(nxt); todo.append((nxt, steps + 1))
    inside = 2 * (distance + 1)
    word = record['shortest_count_word']
    require(word == [3, 2, 1, 0, 0, 1, 2, 3] and len(word) == inside, 'shortest ownership count word changed')
    require(record['minimum_inside_faces'] == inside == 8 and record['minimum_with_outside_center_faces'] == inside + 2 == 10, 'face-chain lower bound changed')
    require(record['count_word_not_a_source_realization'] is True, 'count word promoted to source')
    return dict(ownership_step_distance=distance, inside_face_lower_bound=inside, total_face_lower_bound=inside + 2)


def gamma8(g, seed):
    order = ['r', 'T', 's', 'x', 'h', 'W', 'e', 'd']
    phi = dict(zip(order, [1, 0, 1, 0, 1, 3, 1, 0]))
    original = dict(zip(order, ['N', 'M', 'N', 'K', 'B', 'B', 'B', 'K']))
    exchanged = dict(zip(order, ['C', 'Q', 'E', 'E', 'E', 'Q', 'C', 'C']))
    psi = {v: col ^ 2 if original[v] == 'K' else col for v, col in phi.items()}
    require(g['order'] == order and g['original_colors'] == phi and g['exchanged_colors'] == psi, 'joint source/color frame changed')
    require(g['original_components'] == original and g['exchanged_components'] == exchanged, 'complete component labels changed')
    require(g['segment_lengths'] == dict(P=4, B13=2, C_path=2), 'minimal joint circle segments changed')
    require(g['x_not_identified_with_xprime'] is True and g['h_not_identified_with_b'] is True, 'first meeting confused with last exit')
    require(g['ear_faces_may_be_inside_or_outside_Gamma'] is True, 'external triangle ears wrongly deleted')
    tree = {frozenset(e) for e in g['original_tree_edges']}
    require(tree == {frozenset(e) for e in [('M', 'N'), ('N', 'K'), ('K', 'B')]}, 'original tree changed')
    boundary = {frozenset((a, b)) for a, b in zip(order, order[1:] + order[:1])}
    require(all(phi[a] != phi[b] and psi[a] != psi[b] for a, b in zip(order, order[1:] + order[:1])), 'joint cycle not proper in both same-source colorings')
    pairs = {frozenset(p) for p in combinations(order, 2)} - boundary
    rows = list(g['noncycle_pairs']); random.Random(seed).shuffle(rows)
    require(len(rows) == 20 and {frozenset(r['pair']) for r in rows} == pairs, 'noncycle pair coverage incomplete')
    counts, allowed = Counter(), []
    for row in rows:
        a, b = row['pair']
        if phi[a] == phi[b]:
            kind = 'original_same_color'
        elif original[a] != original[b] and phi[a] % 2 == phi[b] % 2:
            kind = 'merges_original_13_components'
        elif original[a] != original[b] and frozenset((original[a], original[b])) not in tree:
            kind = 'original_J_cycle'
        elif psi[a] in (1, 2) and psi[b] in (1, 2) and exchanged[a] != exchanged[b]:
            kind = 'merges_complete_psi12_components'
        else:
            kind = 'possible_triangle_ear_chord'; allowed.append(sorted((a, b)))
        require(row['classification'] == kind, 'incorrect joint chord classification'); counts[kind] += 1
    require(counts == Counter(original_same_color=9, original_J_cycle=3, merges_original_13_components=2, merges_complete_psi12_components=4, possible_triangle_ear_chord=2), 'joint chord totals changed')
    require(sorted(allowed) == [['W', 'd'], ['W', 'x']], 'unexpected surviving chord')
    return dict(noncycle_pairs=20, classifications=dict(sorted(counts.items())), possible_chords=sorted(allowed))


def validate(c, seed=0):
    require(c['schema'] == '941-p-b13-v2' and c['base'] == BASE, 'certificate scope/base changed')
    claims = dict(r_T_edge_in_Omega=True, r_and_T_anticomplete_to_B=True,
        R_neq_r_only_wrong_side_type4=True, p_original01_and_n_original13_distinct=True,
        n_may_be_boundary_Yq=True, Gamma_minimum_even_length=8,
        Gamma_keeps_P_and_B13_bridges=True, Gamma_need_not_keep_last_K_exit_m=True,
        Gamma_has_no_K2=True, odd_centers_inside_and_outside_Gamma=True,
        at_least_two_distinct_private_K2_in_Q=True, one_patch_K2_differs_from_Z=True,
        new_patch_K2_not_given_marked_Z_link=True,
        exactly_two_crossings_minimum_patch_union=7,
        exactly_two_crossings_shared_roles=['k0', 'b1', 'b3'],
        shared_k0_and_nonendpoint_b1_separate_C_r_e=True,
        shared_b3_on_fixed_B_subpath=True, shared_b3_degree_at_least_5_plus_D0_count=True,
        T_has_private_original3_neighbor_on_each_Gamma_side=True, Gamma_is_not_empty_cap=True)
    require(c['paper_claims'] == claims, 'paper/source claim contract changed (general proof is in PROOF.md)')
    require(c['boundaries'] == dict(source_control='not triggered', finite_calibration='triggered and holds',
        initial_pair_exclusions=0, smaller_bad=False, source_realized=False, new_Lean=False,
        no_source_enumeration_or_LP=True, rootless_and_boundary_tips_retained=True,
        Wstar_may_equal_q=True, b_may_equal_c=True, multiple_P_B13_intersections_retained=True,
        high_degrees_and_ordinary_degree5_sides_retained=True, M_not_identified_with_L=True,
        general_wrong_side_and_eight_pairs='OPEN'), 'unjustified branch/theorem promotion')
    return dict(inherited=predecessor(c, seed), face_ownership=ownership(c['face_ownership']), gamma8=gamma8(c['gamma8'], seed))


def negatives(c):
    tests = [
        ('lose_shared02_choice', lambda x: x['shared02_short_segments'].pop()),
        ('erase_rootless_P_midpoint', lambda x: x['shared02_short_segments'][0].update(missing_P_bridge_midpoint_colors=[0, 2])),
        ('retain_six_point_child', lambda x: x['shared02_short_segments'][0].update(exactly_two_crossing_six_point_branch='OPEN')),
        ('promote_source', lambda x: x['boundaries'].update(source_realized=True)),
        ('exclude_initial_pair', lambda x: x['boundaries'].update(initial_pair_exclusions=1)),
        ('erase_q_exception', lambda x: x['boundaries'].update(Wstar_may_equal_q=False)),
        ('force_n_internal', lambda x: x['paper_claims'].update(n_may_be_boundary_Yq=False)),
        ('force_Gamma_to_keep_m', lambda x: x['paper_claims'].update(Gamma_need_not_keep_last_K_exit_m=False)),
        ('allow_shared_k2', lambda x: x['paper_claims']['exactly_two_crossings_shared_roles'].append('k2')),
        ('erase_C_separator', lambda x: x['paper_claims'].update(shared_k0_and_nonendpoint_b1_separate_C_r_e=False)),
        ('reuse_Z_link_for_new_point', lambda x: x['paper_claims'].update(new_patch_K2_not_given_marked_Z_link=False)),
        ('invent_empty_cap', lambda x: x['paper_claims'].update(Gamma_is_not_empty_cap=False)),
        ('allow_ownership_jump', lambda x: x['face_ownership'].update(adjacent_face_maximum_change=2)),
        ('erase_p_face_rootlessness', lambda x: x['face_ownership'].update(p_incident_face_values=[1, 1])),
        ('lower_face_count', lambda x: x['face_ownership'].update(minimum_inside_faces=7)),
        ('erase_one_Gamma_pair', lambda x: x['gamma8']['noncycle_pairs'].pop()),
        ('merge_C_with_E', lambda x: x['gamma8']['exchanged_components'].update(s='C')),
        ('move_d_out_of_K', lambda x: x['gamma8']['original_components'].update(d='M')),
        ('delete_external_triangle_ears', lambda x: x['gamma8'].update(ear_faces_may_be_inside_or_outside_Gamma=False)),
        ('erase_empty_fibres', lambda x: x['complete_predecessor_certificate']['complete_predecessor_certificate']['upstream_complete_fibre_custody'].update(empty_seven_point_fibres=0)),
    ]
    out = []
    for name, mutate in tests:
        bad = deepcopy(c); mutate(bad)
        try:
            validate(bad)
        except (ValueError, KeyError, TypeError, IndexError):
            out.append(dict(name=name, status='rejected'))
        else:
            raise ValueError('corrupted certificate accepted: ' + name)
    return out


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--negative', action='store_true'); parser.add_argument('--certificate', type=Path, default=HERE / 'certificate-v2.json')
    args = parser.parse_args(); m, routing = authority()
    c = json.loads(args.certificate.read_text()); stats = validate(c, args.seed)
    result = dict(status='PASS', seed=args.seed, frozen_authorities=len(m['inputs']),
        preserved_previous_outputs=len(m['preserved_previous_outputs']), immutable_input_drift=0,
        routing_live_drift=routing, general_topology='paper proof; not a finite-source exclusion',
        source_control='not triggered', initial_pair_exclusions=0, **stats)
    if args.negative:
        result['semantic_negatives'] = negatives(c)
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, IndexError, TypeError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps(dict(status='REJECT', reason=str(exc)))); sys.exit(1)
