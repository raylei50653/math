#!/usr/bin/env python3
"""Original four-spoke (3,1), mixed-(1,2) plus one singleton unary.

Same-color spoke omission gives the original minimal (3,1) one-spoke core.
The unbounded active-triangle exclusion is inherited paper evidence. This
checker audits named identities, whole-frame transport and full fixed-graph
ternary joins; it does not enumerate source graphs or realize source Sigma.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from c5_independent_support_capacity import B, ROWS, U
from c5_excess_one_subcovers import singleton
from c5_941_two_spoke import relabel_mask
from c5_excess_two_mixed_core_leaf_fibers import transport
from c5_single_spoke_three_one import connected, edge, minor, run as replay_three_one, validate_minor
from c5_excess_two_four_spoke_ternary_joint_controls import fixed_graph_controls

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_mixed_core_four_spoke_ternary/observations.json'
SOURCE = ROOT / 'artifacts/c5_excess_two_mixed_core_single_spoke/observations.json'
THREE = ROOT / 'artifacts/c5_single_spoke_three_one/observations.json'


def subsets(values):
    return [set(c) for n in range(len(values)+1) for c in combinations(sorted(values), n)]


def cover_options(row, spoke, leaf_support):
    """Complete necessary ban covers; not independent contact marginals."""
    available = U - {row[spoke]}
    leaf = U - {row[i] for i in leaf_support}
    assert len(available) == 3 and len(leaf) == 2
    options = []
    for fk, fu in product(subsets(U), repeat=2):
        if (not fk or len(fk) > 3 or len(fu) != 1 or fk | fu != available
                or not fk - fu or not fu - fk):
            continue
        assert len(fk) == 2 and fk == available - fu
        # If b=d is already seen by the marked leaf's boundary spokes,
        # that leaf has a list of size two and internal degree one: slack.
        if not fk <= leaf:
            continue
        assert fk == leaf and fu == available - leaf
        options.append(dict(K_complete_relation_forbidden_colors=sorted(fk),
            U_complete_relation_forbidden_colors=sorted(fu),
            marked_leaf_lists=[dict(b_color=d, list=sorted(leaf - {d}), degree_in_K=1)
                               for d in sorted(fk)]))
    assert len(options) == int(leaf <= available)
    return options


def omission_identity(kept, spoke):
    """Once a loses its original spoke, no further loss on a is possible."""
    factors = [dict(id=f'a:spoke:{i}', incidence=[1, 0]) for i in kept]
    factors += [dict(id=f'b:spoke:{spoke}', incidence=[0, 1]),
        dict(id='original:C', incidence=[1, 2]), dict(id='original:U', incidence=[0, 1])]
    admissible = []
    for bits in range(1 << len(factors)):
        removed = [f for j, f in enumerate(factors) if bits >> j & 1]
        loss = [sum(f['incidence'][i] for f in removed) for i in (0, 1)]
        degrees = [4-loss[0], 5-loss[1]]
        if min(degrees) >= 4:
            admissible.append(dict(omitted_original_factors=[f['id'] for f in removed],
                resulting_a_b_degrees=degrees,
                status='original_M_itself' if not removed else 'excluded_original_4_4_q_core'))
    assert len(admissible) == 3
    assert {tuple(e['omitted_original_factors']) for e in admissible} == {
        (), (f'b:spoke:{spoke}',), ('original:U',)}
    return dict(retained_original_factors=factors, all_degree_admissible_further_omissions=admissible,
        original_C_cannot_be_omitted=True, original_M_is_minimal_if_it_rejects=True,
        paper_dependencies=['both original root deletions accept all rows',
            'original zw deletion accepts all rows', 'all original (4,4) q cores excluded',
            'saturation of original degree-four components'])


def marked_minor_controls(frame):
    """Keep original a as an arm endpoint; do not create a new ternary factor.

    These inherited skeletons are topology controls, not full degree/list
    realizations. The fixed full-degree graphs are checked separately.
    """
    result = []
    a, b = frame['a'], frame['b']
    for lengths, coincident in product(((1, 1, 1), (2, 0, 0)), (False, True)):
        s = frame['original_b_spoke']
        targets = (s, s, s) if coincident else tuple((s+i) % 5 for i in (1, 3, 4))
        original = minor(s, lengths, (True, False, True), targets)
        rename = {'z': f'original_b{b}', original['ports'][0]: f'original_a{a}',
            original['arms'][0][-2]: 'original_C_x', original['ports'][1]: 'original_C_y0',
            original['ports'][2]: 'original_C_y1', 'd0': 'original_U_u'}
        move = lambda v: rename.get(v, v)
        edges = {edge(move(u), move(v)) for u, v in original['edges']}
        edges.update(edge(f'original_a{a}', f'b{i}') for i in frame['original_a_spoke_support'])
        bags = [[move(v) for v in bag] for bag in original['branch_sets']]
        cert = dict(edges=sorted(edges), branch_sets=bags)
        assert validate_minor(cert)
        root_a, root_b = f'original_a{a}', f'original_b{b}'
        assert sum(root_a in e for e in edges) == sum(root_b in e for e in edges) == 5
        for i in frame['original_a_spoke_support']:
            assert validate_minor(dict(cert, edges=sorted(edges - {edge(root_a, f'b{i}')})))
        c_vertices = {v for e in edges for v in e} - {f'b{i}' for i in range(5)} - {root_a, root_b, 'original_U_u', 'd1'}
        assert connected(c_vertices, edges)
        result.append(dict(**cert, original_a=root_a, original_b=root_b,
            original_C_vertices=sorted(c_vertices), original_C_ordered_contacts=['original_C_x', 'original_C_y0', 'original_C_y1'],
            original_K_ordered_contacts=[root_a, 'original_C_y0', 'original_C_y1'],
            original_U_contact='original_U_u', original_C_connected=True,
            original_triangle=[move(f'v{i}') for i in range(3)],
            arms=[[move(v) for v in arm] for arm in original['arms']],
            actual_tethers=[[move(v) for v in tether] for tether in original['tethers']],
            original_a_spokes=frame['original_a_spoke_support'], original_b_spoke=s,
            adjacency=[dict(pair=entry['pair'], edge=edge(*(move(v) for v in entry['edge']))) for entry in original['adjacency']],
            scope='Inherited marked original K5 skeleton; not full degree/list or disk/Sigma realization'))
    return result


def build():
    inherited = json.loads(SOURCE.read_text())
    three = replay_three_one()
    assert json.loads(THREE.read_text()) == json.loads(json.dumps(three)), 'old (3,1) certificate differs'
    assert all(validate_minor(r) for r in three['minors'])
    targets, exchange, marked_minors = [], {}, []
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
            triple = supports[aside]
            spoke, = supports[1-aside]
            queries = []
            for omitted in triple:
                kept = sorted(set(triple) - {omitted})
                for ri, row in enumerate(ROWS):
                    if sigma >> ri & 1 or not any(row[omitted] == row[i] for i in kept):
                        continue
                    qpos = singleton(row)
                    boundary = [(i+4-qpos) % 5 for i in range(5)]
                    moved = transport(row, boundary)
                    assert tuple(moved['transported_row']) == ROWS[0]
                    options = cover_options(row, spoke, kept)
                    for option in options:
                        colors = moved['color_permutation']
                        key = (boundary[spoke], tuple(sorted(colors[c] for c in option['K_complete_relation_forbidden_colors'])),
                            tuple(sorted(colors[c] for c in option['U_complete_relation_forbidden_colors'])))
                        matches = [i for i, cover in enumerate(three['covers']) if
                            (cover['spoke'], tuple(cover['bans'][0]), tuple(cover['bans'][1])) == key]
                        assert len(matches) == 1
                        option['inherited_three_one_cover_index'] = matches[0]
                    query = dict(query_index=len(queries), original_row_index=ri, original_literal_row=row,
                        omitted_original_spoke=sorted((a, omitted)), retained_a_spoke_support=kept,
                        same_color_retained_original_spokes=[sorted((a, i)) for i in kept if row[i] == row[omitted]],
                        original_M_a_b_degrees=[4, 5], core_components=['K=original C + original a', 'original U'],
                        core_contact_partition=[3, 1], K_ordered_contacts=['a', 'y0', 'y1'],
                        original_C_ordered_contacts=['x', 'y0', 'y1'],
                        original_contact_ownership=['a', 'b', 'b'],
                        distinct_core_contacts=True, x_may_equal_y0_or_y1=True,
                        marked_a_degree_in_K=1, necessary_complete_relation_ban_covers=options,
                        one_global_boundary_permutation=boundary, one_global_color_permutation=moved['color_permutation'],
                        inherited_one_spoke_position=boundary[spoke],
                        status='excluded_by_inherited_three_one_active_triangle_K5' if options else 'excluded_by_marked_leaf_slack_cover')
                    queries.append(query)
                    counts[query['status']] += 1
                    for sign, shift in product((-1, 1), range(5)):
                        move = [(sign*i+shift) % 5 for i in range(5)]
                        trans = transport(row, move)
                        moved_row, colors = trans['transported_row'], trans['color_permutation']
                        assert not relabel_mask(sigma, move) >> ROWS.index(tuple(moved_row)) & 1
                        assert any(moved_row[move[i]] == moved_row[move[omitted]] for i in kept)
                        moved_options = cover_options(moved_row, move[spoke], [move[i] for i in kept])
                        assert [(o['K_complete_relation_forbidden_colors'], o['U_complete_relation_forbidden_colors']) for o in moved_options] == [
                            (sorted(colors[c] for c in o['K_complete_relation_forbidden_colors']),
                             sorted(colors[c] for c in o['U_complete_relation_forbidden_colors'])) for o in options]
                        d5_checks += 1
            assert queries
            frame = dict(frame_index=len(frames), inherited_named_skeleton_index=index, a=a, b=b,
                original_root_order=item['root_order'], original_a_spoke_support=triple, original_b_spoke=spoke,
                original_root_and_boundary_edges=item['retained_source_edges'],
                original_component_contract=dict(C=dict(owners=[a, b], incidence=[1, 2], ordered_contacts=['x', 'y0', 'y1'],
                    y0_y1_distinct=True, x_may_equal_y0_or_y1=True, retain_all_actual_attachments_and_bridges=True),
                    U=dict(owner=b, incidence=1, ordered_contacts=['u'], retain_all_actual_attachments_and_bridges=True)),
                omission_identities=[dict(omitted_original_spoke=sorted((a, e)),
                    certificate=omission_identity(sorted(set(triple)-{e}), spoke)) for e in triple],
                marked_original_queries=queries, status='entire_original_incidence_subtype_excluded')
            frames.append(frame)
            marked_minors.extend(dict(source_sigma=sigma, frame_index=frame['frame_index'], certificate=c)
                                 for c in marked_minor_controls(frame))
            total_queries += len(queries)
            exchange[(sigma, tuple(triple), spoke, a, b)] = [
                (q['original_row_index'], q['status'], q['necessary_complete_relation_ban_covers']) for q in queries]
        assert len(frames) == (20 if sigma == 933 else 60)
        targets.append(dict(source_sigma=sigma, excluded_named_frames=len(frames), remaining_named_frames=0,
            counts=dict(sorted(counts.items())), frames=frames))
    for key, value in exchange.items():
        assert exchange[(*key[:-2], key[-1], key[-2])] == value
    selected = [f for t in targets for f in t['frames'] if f['a'] == 6 and f['b'] == 5
                and f['original_a_spoke_support'] == [0, 1, 2] and f['original_b_spoke'] == 2]
    assert len(selected) == 2
    for f in selected:
        qs = [q for q in f['marked_original_queries'] if q['original_literal_row'] == (0, 1, 0, 2, 1)]
        assert len(qs) == 2
        assert all(q['necessary_complete_relation_ban_covers'][0]['K_complete_relation_forbidden_colors'] == [2, 3]
                   and q['necessary_complete_relation_ban_covers'][0]['U_complete_relation_forbidden_colors'] == [1] for q in qs)
    controls = fixed_graph_controls()
    paths = [Path(__file__), SOURCE, THREE,
        ROOT / 'scripts/c5_excess_two_four_spoke_ternary_joint_controls.py',
        ROOT / 'scripts/c5_single_spoke_three_one.py',
        ROOT / 'artifacts/c5_excess_two_mixed_core_spokes/observations.json',
        ROOT / 'artifacts/c5_excess_two_mixed_omission/observations.json']
    source_drift = [dict(path=p, recorded_sha256=digest,
        current_sha256=sha256((ROOT / p).read_bytes()).hexdigest())
        for p, digest in sorted(inherited['input_sha256'].items())
        if sha256((ROOT / p).read_bytes()).hexdigest() != digest]
    assert all(d['path'].startswith('docs/') for d in source_drift)
    return dict(schema=1, scope=__doc__, pattern_order=ROWS,
        input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths},
        original_single_spoke_provenance=dict(recorded_source_artifact_sha256=sha256(SOURCE.read_bytes()).hexdigest(),
            document_provenance_drift=source_drift, artifact_rewritten=False,
            mathematical_payload_replay='Separate read-only source build audit recorded in the history report'),
        inherited_three_one_exact_replay=dict(artifact=str(THREE.relative_to(ROOT)), summary=three['summary'],
            complete_mathematical_payload_equal=True, artifact_rewritten=False),
        targets=targets, selected_entry_original_frames=selected, marked_original_K5_skeleton_controls=marked_minors,
        fixed_full_degree_graph_controls=controls,
        summary=dict(targets=[dict(source_sigma=t['source_sigma'], excluded_named_frames=t['excluded_named_frames'],
            remaining_named_frames=0, **t['counts']) for t in targets],
            complete_original_omission_queries=total_queries, root_swap_frame_checks=len(exchange),
            simultaneous_D5_query_checks=d5_checks, fixed_full_degree_graphs=len(controls['records']),
            independent_whole_graph_joins=controls['independent_whole_graph_joins'],
            independent_complete_K_relations=controls['independent_complete_K_relations'],
            independent_pinned_b_a_fibers=controls['independent_pinned_b_a_fibers'],
            same_color_original_spoke_equalities=controls['same_color_spoke_equalities'],
            marked_original_K5_skeleton_controls=len(marked_minors),
            original_mixed_one_two_plus_unary_subtype_excluded=True,
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
