#!/usr/bin/env python3
"""Original four-spoke (3,1), mixed-(1,3), no unary: leaf-slack exclusion.

Same-color original spoke omission retains K=C+a with FOUR ordered contacts.
Rejection requires three forbidden b colors, while the marked leaf permits at
most two. The arbitrary-size proof is constructive reverse-tree coloring;
fixed named frames and complete original graph relations are audited here.
No source enumeration, disk realization, new Lean theorem, or epsilon>=3.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from c5_independent_support_capacity import ROWS, U
from c5_941_two_spoke import relabel_mask
from c5_excess_two_mixed_core_leaf_fibers import transport
from c5_excess_two_four_spoke_quaternary_joint_controls import fixed_graph_controls

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_mixed_core_four_spoke_quaternary/observations.json'
SOURCE = ROOT / 'artifacts/c5_excess_two_mixed_core_single_spoke/observations.json'


def leaf_slack_certificate(row, spoke, kept):
    seen = {row[i] for i in kept}
    available, leaf = U - {row[spoke]}, U - seen
    assert len(seen) == len(leaf) == 2 and len(available) == 3
    escape = sorted(seen & available)
    assert escape
    d = escape[0]
    candidates = [set(c) for size in range(5) for c in combinations(sorted(U), size)]
    covers = [sorted(f) for f in candidates if available <= f and f <= leaf]
    assert not covers
    return dict(b_available_colors=sorted(available), marked_a_available_colors=sorted(leaf),
        required_complete_K_forbidden_colors=sorted(available),
        necessary_complete_K_forbidden_color_envelope=sorted(leaf),
        compatible_three_color_ban_covers=covers, constructive_b_colors=escape,
        selected_b_color=d, exact_marked_leaf_list=sorted(leaf - {d}),
        marked_a_degree_in_K=1, leaf_list_size=2, leaf_slack=1,
        all_other_original_K_lists_at_least_internal_degree=True,
        proof='Reverse a-rooted spanning tree: nonroots keep an uncolored parent; a has slack',
        status='original_M_and_G_accept_the_supposed_rejected_row')


def omission_identity(kept, spoke):
    factors = [dict(id=f'a:spoke:{i}', incidence=[1, 0]) for i in kept]
    factors += [dict(id=f'b:spoke:{spoke}', incidence=[0, 1]),
                dict(id='original:C', incidence=[1, 3])]
    admissible = []
    for bits in range(1 << len(factors)):
        removed = [f for j, f in enumerate(factors) if bits >> j & 1]
        degrees = [4 - sum(f['incidence'][0] for f in removed),
                   5 - sum(f['incidence'][1] for f in removed)]
        if min(degrees) >= 4:
            admissible.append(dict(omitted_original_factors=[f['id'] for f in removed],
                resulting_a_b_degrees=degrees,
                status='original_M_itself' if not removed else 'excluded_original_4_4_q_core'))
    assert {tuple(e['omitted_original_factors']) for e in admissible} == {(), (f'b:spoke:{spoke}',)}
    return dict(retained_original_factors=factors, all_degree_admissible_further_omissions=admissible,
        original_C_cannot_be_omitted=True, original_K_contact_partition=[4],
        identity_only=True, minimality_required_by_leaf_slack_proof=False)


def build():
    inherited = json.loads(SOURCE.read_text())
    targets, exchange = [], {}
    total_queries, d5_checks = 0, 0
    for target in inherited['targets']:
        sigma = target['source_sigma']
        frames, counts = [], Counter()
        for index, item in enumerate(target['named_spoke_skeletons']['records']):
            supports = item['original_spoke_supports']
            if item['status'] != 'necessary_skeleton_only' or sorted(map(len, supports)) != [1, 3]:
                continue
            aside, = [i for i in (0, 1) if len(supports[i]) == 3]
            a, b = item['root_order'][aside], item['root_order'][1-aside]
            triple, (spoke,) = supports[aside], supports[1-aside]
            queries = []
            for omitted in triple:
                kept = sorted(set(triple) - {omitted})
                for ri, row in enumerate(ROWS):
                    if sigma >> ri & 1 or not any(row[omitted] == row[i] for i in kept):
                        continue
                    cert = leaf_slack_certificate(row, spoke, kept)
                    query = dict(query_index=len(queries), original_row_index=ri, original_literal_row=row,
                        omitted_original_spoke=sorted((a, omitted)), retained_a_spoke_support=kept,
                        same_color_retained_original_spokes=[sorted((a, i)) for i in kept if row[i] == row[omitted]],
                        original_M_a_b_degrees=[4, 5], core_components=['K=original C + original a'],
                        core_contact_partition=[4], K_ordered_contacts=['a', 'y0', 'y1', 'y2'],
                        original_C_ordered_contacts=['x', 'y0', 'y1', 'y2'],
                        original_contact_ownership=['a', 'b', 'b', 'b'], distinct_core_contacts=True,
                        x_may_equal_any_y=True, unary_components=[], leaf_slack_certificate=cert,
                        original_G_restoration='Omitted a-spoke has same color as a retained original spoke',
                        status='excluded_by_complete_four_contact_leaf_slack')
                    queries.append(query)
                    counts[query['status']] += 1
                    for sign, shift in product((-1, 1), range(5)):
                        move = [(sign*i+shift) % 5 for i in range(5)]
                        trans = transport(row, move)
                        moved_row, colors = trans['transported_row'], trans['color_permutation']
                        assert not relabel_mask(sigma, move) >> ROWS.index(tuple(moved_row)) & 1
                        assert any(moved_row[move[i]] == moved_row[move[omitted]] for i in kept)
                        transported = leaf_slack_certificate(moved_row, move[spoke], [move[i] for i in kept])
                        for key in ('b_available_colors', 'marked_a_available_colors',
                                    'required_complete_K_forbidden_colors',
                                    'necessary_complete_K_forbidden_color_envelope', 'constructive_b_colors'):
                            assert transported[key] == sorted(colors[c] for c in cert[key])
                        d5_checks += 1
            assert queries
            frames.append(dict(frame_index=len(frames), inherited_named_skeleton_index=index, a=a, b=b,
                original_root_order=item['root_order'], original_a_spoke_support=triple, original_b_spoke=spoke,
                original_root_and_boundary_edges=item['retained_source_edges'],
                inherited_skeleton_boundary_apex=item['boundary_apex'],
                inherited_skeleton_augmented_edges=item['augmented_edges'],
                inherited_skeleton_apex_rotation=item['apex_rotation'],
                rotation_scope='Retained necessary skeleton only; full source embedding stays original in the paper proof',
                original_component_contract=dict(C=dict(owners=[a, b], incidence=[1, 3],
                    ordered_contacts=['x', 'y0', 'y1', 'y2'], y_contacts_distinct=True,
                    x_may_equal_any_y=True, retain_all_actual_attachments_and_bridges=True), unary_components=[]),
                omission_identities=[dict(omitted_original_spoke=sorted((a, e)),
                    certificate=omission_identity(sorted(set(triple)-{e}), spoke)) for e in triple],
                marked_original_queries=queries, status='entire_original_incidence_subtype_excluded'))
            total_queries += len(queries)
            exchange[(sigma, tuple(triple), spoke, a, b)] = queries
        assert len(frames) == (20 if sigma == 933 else 60)
        targets.append(dict(source_sigma=sigma, excluded_named_frames=len(frames), remaining_named_frames=0,
            counts=dict(sorted(counts.items())), frames=frames))
    for key, queries in exchange.items():
        partner = exchange[(*key[:-2], key[-1], key[-2])]
        for q, p in zip(queries, partner, strict=True):
            assert q['original_row_index'] == p['original_row_index']
            assert q['leaf_slack_certificate'] == p['leaf_slack_certificate']
            assert q['retained_a_spoke_support'] == p['retained_a_spoke_support']
    selected = [f for t in targets for f in t['frames'] if f['a'] == 6 and f['b'] == 5
                and f['original_a_spoke_support'] == [0, 1, 2] and f['original_b_spoke'] == 2]
    assert len(selected) == 2
    for f in selected:
        qs = [q for q in f['marked_original_queries'] if q['original_literal_row'] == (0, 1, 0, 2, 1)]
        assert len(qs) == 2
        assert all(q['leaf_slack_certificate']['required_complete_K_forbidden_colors'] == [1, 2, 3]
            and q['leaf_slack_certificate']['necessary_complete_K_forbidden_color_envelope'] == [2, 3]
            and q['leaf_slack_certificate']['constructive_b_colors'] == [1] for q in qs)
    controls = fixed_graph_controls()
    paths = [Path(__file__), SOURCE,
             ROOT / 'scripts/c5_excess_two_four_spoke_quaternary_joint_controls.py']
    drift = [dict(path=p, recorded_sha256=digest,
                  current_sha256=sha256((ROOT / p).read_bytes()).hexdigest())
             for p, digest in sorted(inherited['input_sha256'].items())
             if sha256((ROOT / p).read_bytes()).hexdigest() != digest]
    assert all(d['path'].startswith('docs/') for d in drift)
    return dict(schema=1, scope=__doc__, pattern_order=ROWS,
        input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths},
        original_single_spoke_provenance=dict(document_provenance_drift=drift, artifact_rewritten=False,
            mathematical_payload_replay='Inherited read-only audit recorded in preceding ternary history; not rerun here'),
        targets=targets, selected_entry_original_frames=selected, fixed_full_degree_graph_controls=controls,
        original_three_one_incidence_budget=dict(a_mixed_incidence=1, a_unary_partition=[],
            remaining_b_contact_budget=3,
            all_original_b_cases=[dict(mixed_incidence=1, unary_partition=[1, 1],
                    completed_by='c5_excess_two_mixed_core_four_spoke_singles.md'),
                dict(mixed_incidence=1, unary_partition=[2],
                    completed_by='c5_excess_two_mixed_core_four_spoke_hubs.md'),
                dict(mixed_incidence=2, unary_partition=[1],
                    completed_by='c5_excess_two_mixed_core_four_spoke_ternary.md'),
                dict(mixed_incidence=3, unary_partition=[], completed_by='this leaf-slack proof')],
            scope='Integer incidence identity; completion uses each cited paper theorem under its hypotheses'),
        summary=dict(targets=[dict(source_sigma=t['source_sigma'], excluded_named_frames=t['excluded_named_frames'],
            remaining_named_frames=0, **t['counts']) for t in targets],
            complete_original_omission_queries=total_queries, root_swap_frame_checks=len(exchange),
            simultaneous_D5_query_checks=d5_checks, fixed_full_degree_graphs=len(controls['records']),
            independent_whole_graph_joins=controls['independent_whole_graph_joins'],
            independent_complete_K_relations=controls['independent_complete_K_relations'],
            independent_pinned_b_a_fibers=controls['independent_pinned_b_a_fibers'],
            constructive_whole_graph_extensions=controls['constructive_whole_graph_extensions'],
            same_color_original_spoke_equalities=controls['same_color_spoke_equalities'],
            original_mixed_one_three_no_unary_subtype_excluded=True,
            source_graphs_enumerated=False, epsilon_three_proved=False, new_lean_theorem=False))


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
