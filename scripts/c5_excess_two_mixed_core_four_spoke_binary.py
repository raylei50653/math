#!/usr/bin/env python3
"""Necessary marked-leaf reduction for four spokes (3,1) and one binary unary.

Keep the two contacts of the original binary together. Inherited (2,2)
source exclusions, exact leaf inversions, same-row whole relations and the
original short-support theorem reduce necessary support domains. Remaining
domains are not realizations or complete-Sigma models; no source enumeration.
"""
import argparse
from collections import Counter, defaultdict
from functools import lru_cache
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path

from c5_independent_support_capacity import B, FRAME, ROWS, U, span
from c5_excess_one_subcovers import singleton
from c5_941_two_spoke import relabel_mask
from c5_excess_two_mixed_core_single_spoke import repeated_rows, residual_masks
from c5_excess_two_mixed_core_leaf_fibers import transport
from c5_single_spoke_two_two import (SCHEMAS, placements, row_record, schema_ids,
    run as replay_original_base, support_table as original_support_table)
from c5_excess_two_four_spoke_binary_joint_controls import graph_controls

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_mixed_core_four_spoke_binary/observations.json'
SINGLE = ROOT / 'artifacts/c5_excess_two_mixed_core_single_spoke/observations.json'
CORES = ROOT / 'artifacts/c5_single_spoke_two_two/observations.json'
FINAL = ROOT / 'artifacts/c5_single_spoke_residual_locality/observations.json'


def edge(a, b):
    return tuple(sorted((a, b)))


def inherited_records():
    base, final = [json.loads(p.read_text()) for p in (CORES, FINAL)]
    original = {r['id']: r for r in base['records']}
    records = []
    for entry in final['table']['retained']:
        item = entry['original_record']
        assert item == original[entry['source_id']]
        assert item['T4_status'] == 'retained'
        assert all(t['status'] == 'accept' for t in entry['targets'])
        variants = [('original', item)]
        if item['spoke'] != 4:
            variants.append(('reflection', item['reflection']))
        for branch, data in variants:
            records.append(dict(spoke=data['spoke'],
                supports=tuple(map(tuple, data['supports'])),
                bans=tuple(map(tuple, data['bans'])), placements=data['placements'],
                relation_schema_ids=[schema_ids(tuple(s), tuple(f))
                    for s, f in zip(data['supports'], data['bans'], strict=True)],
                canonical_all_ten_row_bounds=[row_record(data['spoke'],
                    tuple(map(tuple, data['supports'])), tuple(map(tuple, data['bans'])), row)
                    for row in ROWS],
                proved_accepted_rows=[t['row'] if branch == 'original'
                    else t['canonical_row'] for t in data['targets']],
                provenance=dict(artifact=str(CORES.relative_to(ROOT)),
                    source_id=item['id'], branch=branch,
                    completed_source_table=str(FINAL.relative_to(ROOT)))))
    assert len(records) == 196
    assert Counter(r['spoke'] for r in records) == {0: 46, 1: 48, 2: 48, 3: 46, 4: 8}
    return records


def inherited_base_audit():
    """Recompute the complete old mathematical payload without rewriting history."""
    saved = json.loads(CORES.read_text())
    current_raw = replay_original_base()
    current = json.loads(json.dumps(current_raw))
    drift = [dict(path=p, recorded_sha256=saved['inputs'][p], current_sha256=digest)
        for p, digest in sorted(current['inputs'].items()) if saved['inputs'][p] != digest]
    assert all(d['path'].startswith('docs/') for d in drift)
    original_inputs = saved['inputs']
    saved['inputs'] = current['inputs']
    assert saved == current, 'inherited base mathematical payload differs'
    assert CORES.with_name('support_table.md').read_text() == original_support_table(current_raw)
    return dict(source_artifact=str(CORES.relative_to(ROOT)),
        recorded_source_artifact_sha256=sha256(CORES.read_bytes()).hexdigest(),
        complete_mathematical_payload_equal=True, complete_support_table_equal=True,
        original_recorded_input_sha256=original_inputs, document_provenance_drift=drift,
        source_artifact_rewritten=False)


def original_frames(target):
    records = []
    for index, item in enumerate(target['named_spoke_skeletons']['records']):
        supports = item['original_spoke_supports']
        if (item['status'] != 'necessary_skeleton_only'
                or sorted(map(len, supports)) != [1, 3]):
            continue
        aside, = [i for i in (0, 1) if len(supports[i]) == 3]
        a, b = item['root_order'][aside], item['root_order'][1 - aside]
        spoke, = supports[1 - aside]
        records.append(dict(frame_index=len(records), inherited_skeleton_index=index,
            original_root_order=item['root_order'], a=a, b=b,
            original_a_spoke_support=tuple(supports[aside]), original_b_spoke=spoke,
            retained_original_root_spoke_edges=item['retained_source_edges'],
            original_component_contract=dict(
                C=dict(owners=[a, b], ordered_contacts=['x', 'y'],
                    incidence=[1, 1], shared_contact_permitted=True),
                U=dict(owner=b, ordered_contacts=['u', 'v'], incidence=2,
                    distinct_original_contacts=True))))
    assert len(records) == (20 if target['source_sigma'] == 933 else 60)
    return records


@lru_cache(None)
def leaf_inversions(c_support, leaf_colors, k_support, k_ban):
    """Exact existence of a support-invariant full C relation for each K schema.

    The maximum preimage is an algebra witness, not a coloring witness or a
    claim that every actual C tuple occurs. Every leaf image is nonempty.
    """
    q = ROWS[0]
    seen = {q[i] for i in c_support}
    stabilizer = [p for p in permutations(range(4)) if all(p[c] == c for c in seen)]
    result = []
    for ident in schema_ids(k_support, k_ban):
        rk = set(SCHEMAS[ident]['tuples'])
        allowed = {(x, y) for x, y in product(sorted(U), repeat=2)
            if {(a, y) for a in leaf_colors if a != x} <= rk}
        rc = {t for t in allowed if all(tuple(p[c] for c in t) in allowed for p in stabilizer)}
        if {(a, y) for x, y in rc for a in leaf_colors if a != x} != rk:
            continue
        assert rc and all({tuple(p[c] for c in t) for t in rc} == rc for p in stabilizer)
        result.append(dict(K_schema_id=ident, complete_K_tuples=sorted(rk),
            maximum_complete_C_preimage=sorted(rc),
            shared_contact_compatible={(a, y) for x, y in rc if x == y
                for a in leaf_colors if a != x} == rk,
            scope='Full ordered relation algebra; no source realization'))
    return result


def marked_queries(target, frame, inherited, counts):
    result = []
    sigma = target['source_sigma']
    triple, spoke = frame['original_a_spoke_support'], frame['original_b_spoke']
    for omitted in triple:
        forced = repeated_rows(sigma, triple, omitted)
        for qpos in sorted(forced):
            counts['marked_queries'] += 1
            qi, = [i for i, q in enumerate(ROWS) if len(set(q)) == 3 and singleton(q) == qpos]
            q = ROWS[qi]
            boundary_perm = tuple((i + 4 - qpos) % 5 for i in range(5))
            moved = transport(q, boundary_perm)
            assert tuple(moved['transported_row']) == ROWS[0]
            colors = moved['color_permutation']
            kept = {boundary_perm[i] for i in triple if i != omitted}
            available = U - {colors[q[i]] for i in triple if i != omitted}
            assert len(available) == 2
            children = [r for r in residual_masks(relabel_mask(sigma, boundary_perm))
                if {boundary_perm[i] for i in forced} <= set(r['rejected_singleton_positions'])]
            inverse_boundary = {p: i for i, p in enumerate(boundary_perm)}
            inverse_colors = {p: i for i, p in enumerate(colors)}
            candidates = []
            for core_index, core in enumerate(inherited):
                if core['spoke'] != boundary_perm[spoke]:
                    continue
                counts['inherited_support_lookups'] += 1
                if not kept <= set(core['supports'][0]):
                    continue
                counts['leaf_support_passes'] += 1
                if not set(core['bans'][0]) <= available:
                    continue
                counts['leaf_slack_passes'] += 1
                evidence = core['canonical_all_ten_row_bounds']
                possible = [c['sigma'] for c in children
                    if all(c['sigma'] >> ROWS.index(tuple(t)) & 1 for t in core['proved_accepted_rows'])
                    and not any((e['status'] == 'reject' and c['sigma'] >> ri & 1)
                        or (e['status'] == 'accept' and not c['sigma'] >> ri & 1)
                        for ri, e in enumerate(evidence))]
                if not possible:
                    continue
                counts['child_mask_passes'] += 1
                k_support, u_support = [tuple(sorted(inverse_boundary[i] for i in s))
                    for s in core['supports']]
                c_options = []
                for bits in range(32):
                    c_support = tuple(i for i in sorted(B) if bits >> i & 1)
                    if set(c_support) | (set(triple) - {omitted}) != set(k_support):
                        continue
                    counts['raw_C_support_preimages'] += 1
                    canonical_c = tuple(sorted(boundary_perm[i] for i in c_support))
                    inversions = leaf_inversions(canonical_c, tuple(sorted(available)),
                        core['supports'][0], core['bans'][0])
                    if not inversions:
                        continue
                    counts['leaf_relation_support_preimages'] += 1
                    literal = [dict(K_schema_id=t['K_schema_id'],
                        complete_K_tuples=sorted(tuple(inverse_colors[c] for c in pair)
                            for pair in t['complete_K_tuples']),
                        maximum_complete_C_preimage=sorted(tuple(inverse_colors[c] for c in pair)
                            for pair in t['maximum_complete_C_preimage']),
                        shared_contact_compatible=t['shared_contact_compatible']) for t in inversions]
                    c_options.append(dict(actual_original_C_support=c_support,
                        complete_leaf_inversions=literal))
                candidates.append(dict(candidate_index=len(candidates),
                    inherited_record_index=core_index, original_K_support=k_support,
                    actual_original_U_support=u_support,
                    original_forbidden_colors=[tuple(sorted(inverse_colors[c] for c in f))
                        for f in core['bans']], possible_canonical_child_sigmas=possible,
                    canonical_all_ten_row_bounds_record=core_index,
                    original_C_support_preimages=c_options))
            result.append(dict(query_index=len(result), original_row_index=qi,
                original_literal_row=q, omitted_original_spoke=edge(frame['a'], omitted),
                retained_original_leaf_support=sorted(set(triple) - {omitted}),
                literal_leaf_available_colors=sorted(U - {q[i] for i in triple if i != omitted}),
                forced_rejected_positions=sorted(forced),
                one_global_boundary_permutation=boundary_perm,
                one_global_color_permutation=colors,
                complete_row_transports=[transport(row, boundary_perm) for row in ROWS],
                necessary_canonical_child_masks=children, candidates=candidates))
    assert result
    return result


def same_source_domains(frame, queries, counts):
    lookups = []
    for query in queries:
        lookup = defaultdict(list)
        for candidate in query['candidates']:
            for option in candidate['original_C_support_preimages']:
                key = (tuple(option['actual_original_C_support']),
                    tuple(candidate['actual_original_U_support']))
                lookup[key].append((candidate, option))
        lookups.append(lookup)
    common = set.intersection(*(set(d) for d in lookups))
    domains = []
    for key in sorted(common):
        assignments = []
        for choice in product(*(d[key] for d in lookups)):
            by_row = {}
            for query, (candidate, option) in zip(queries, choice, strict=True):
                row = query['original_row_index']
                bans = tuple(map(tuple, candidate['original_forbidden_colors']))
                relations = {tuple(map(tuple, t['complete_K_tuples'])):
                    tuple(map(tuple, t['maximum_complete_C_preimage']))
                    for t in option['complete_leaf_inversions']}
                if row not in by_row:
                    by_row[row] = (bans, relations)
                else:
                    old_bans, old_relations = by_row[row]
                    if old_bans != bans:
                        break
                    relations = {rk: rc for rk, rc in relations.items() if rk in old_relations}
                    assert all(rc == old_relations[rk] for rk, rc in relations.items())
                    by_row[row] = (bans, relations)
                if not relations:
                    break
            else:
                assignments.append(dict(query_candidate_indices=[c['candidate_index'] for c, _ in choice],
                    same_literal_row_whole_relation_domains=[dict(row_index=ri,
                        component_order=['K=C+a', 'U'], forbidden_colors=bans,
                        common_complete_K_C_options=[dict(complete_K_tuples=rk,
                            maximum_complete_C_preimage=rc) for rk, rc in sorted(rels.items())])
                        for ri, (bans, rels) in sorted(by_row.items())]))
        if not assignments:
            continue
        counts['same_source_domains'] += 1
        u_support = key[1]
        k_support = tuple(sorted(set(key[0]) | set(frame['original_a_spoke_support'])))
        lifts = placements(frame['original_b_spoke'], (k_support, u_support))
        data = dict(domain_index=len(domains), original_component_order=['C', 'U'],
            actual_original_supports=key, actual_original_H_minus_b_K_support=k_support,
            compatible_same_source_query_assignments=assignments,
            original_K_U_common_lifts=lifts)
        if span(u_support) < 2:
            pair = next(p for p in sorted(FRAME) if set(u_support) <= set(p))
            h = min(set(frame['original_a_spoke_support']) - set(pair))
            path = [frame['b'], frame['a'], h]
            edges = set(map(tuple, frame['retained_original_root_spoke_edges']))
            assert all(edge(v, w) in edges for v, w in zip(path, path[1:]))
            assert h in B - set(pair)
            data.update(status='excluded_by_original_short_support',
                adjacent_U_support_envelope=pair, original_exterior_path=path,
                paper_dependency='docs/c5_short_support_singleton.md')
            counts['short_U_excluded_domains'] += 1
        elif not lifts:
            data['status'] = 'excluded_by_original_common_lifts'
            counts['original_lift_excluded_domains'] += 1
        else:
            data['status'] = 'necessary_residual_not_realization'
            counts['remaining_necessary_domains'] += 1
        domains.append(data)
    return domains


def support_reduction():
    inherited = inherited_records()
    targets = []
    for target in json.loads(SINGLE.read_text())['targets']:
        counts, frames = Counter(), []
        for frame in original_frames(target):
            counts['original_named_frames'] += 1
            queries = marked_queries(target, frame, inherited, counts)
            domains = same_source_domains(frame, queries, counts)
            frame.update(marked_original_queries=queries, same_source_domains=domains)
            frames.append(frame)
        targets.append(dict(source_sigma=target['source_sigma'], counts=dict(sorted(counts.items())),
            frames=frames))
        expected = ({'original_named_frames': 20, 'marked_queries': 40,
            'inherited_support_lookups': 1568, 'leaf_support_passes': 704,
            'leaf_slack_passes': 480, 'child_mask_passes': 480,
            'raw_C_support_preimages': 1920, 'leaf_relation_support_preimages': 1240,
            'same_source_domains': 376, 'short_U_excluded_domains': 260,
            'remaining_necessary_domains': 116} if target['source_sigma'] == 933 else
            {'original_named_frames': 60, 'marked_queries': 160,
            'inherited_support_lookups': 6272, 'leaf_support_passes': 2368,
            'leaf_slack_passes': 1452, 'child_mask_passes': 1388,
            'raw_C_support_preimages': 5552, 'leaf_relation_support_preimages': 3540,
            'same_source_domains': 776, 'short_U_excluded_domains': 520,
            'remaining_necessary_domains': 256})
        assert dict(counts) == expected
        arities = Counter()
        for frame in frames:
            for domain in frame['same_source_domains']:
                if domain['status'] != 'necessary_residual_not_realization':
                    continue
                schedules = {tuple(sorted({len(r['forbidden_colors'][0])
                    for r in a['same_literal_row_whole_relation_domains']}))
                    for a in domain['compatible_same_source_query_assignments']}
                assert len(schedules) == 1
                shape, = schedules
                arities['all_pair' if shape == (2,) else 'singleton_and_pair'] += 1
                for assignment in domain['compatible_same_source_query_assignments']:
                    for row in assignment['same_literal_row_whole_relation_domains']:
                        if len(row['forbidden_colors'][0]) != 2:
                            continue
                        pair = row['forbidden_colors'][0]
                        for option in row['common_complete_K_C_options']:
                            assert set(map(tuple, option['maximum_complete_C_preimage'])) == {(c, c) for c in pair}
        assert dict(arities) == ({'all_pair': 116} if target['source_sigma'] == 933
            else {'all_pair': 232, 'singleton_and_pair': 24})
        targets[-1]['remaining_K_forbidden_arity_domains'] = dict(sorted(arities.items()))
    return dict(inherited_named_records=inherited, targets=targets,
        scope='Necessary support and relation domains; rows are not a realized complete-Sigma model')


def named_residual(reduction):
    matches = []
    for target in reduction['targets']:
        frame, = [f for f in target['frames'] if f['a'] == 6 and f['b'] == 5
            and f['original_a_spoke_support'] == (0, 1, 2) and f['original_b_spoke'] == 0]
        domain, = [d for d in frame['same_source_domains']
            if d['actual_original_supports'] == ((0, 1, 2), (2, 3, 4))]
        assert domain['status'] == 'necessary_residual_not_realization'
        assert all(any(row['row_index'] == 1 and row['forbidden_colors'] == ((2, 3), (1,))
            and any(set(option['maximum_complete_C_preimage']) == {(2, 2), (3, 3)}
                for option in row['common_complete_K_C_options'])
            for row in assignment['same_literal_row_whole_relation_domains'])
            for assignment in domain['compatible_same_source_query_assignments'])
        matches.append(dict(source_sigma=target['source_sigma'], frame_index=frame['frame_index'],
            domain_index=domain['domain_index']))
    q = ROWS[1]
    assert q == (0, 1, 0, 2, 1)
    rc = ((2, 2), (3, 3))
    rk = ((2, 3), (3, 2))
    ru = ((1, 2), (1, 3), (2, 1), (3, 1))
    assert {(a, y) for x, y in rc for a in (2, 3) if a != x} == set(rk)
    assert not {(d, a, y, u, v) for (a, y), (u, v) in product(rk, ru)
        for d in U - {q[0], a, y, u, v}}
    assert all(any(t[j] == 1 and t[1 - j] != 1 for t in ru) for j in (0, 1))
    qmove = transport(q, tuple((i + 1) % 5 for i in range(5)))
    moved_u = tuple(sorted((i + 1) % 5 for i in (2, 3, 4)))
    p = qmove['color_permutation']
    moved_relation = tuple(sorted(tuple(p[c] for c in t) for t in ru))
    assert moved_relation in {tuple(SCHEMAS[i]['tuples']) for i in schema_ids(moved_u, (p[1],))}
    return dict(original_a=6, original_b=5, a_spokes=[0, 1, 2], b_spoke=0,
        actual_C_support=[0, 1, 2], actual_U_support=[2, 3, 4],
        literal_row=q, literal_leaf_colors=[2, 3], complete_C_tuples=rc,
        complete_K_tuples=rk, complete_U_tuples=ru, complete_rejecting_joint=[],
        K_U_forbidden_colors=[[2, 3], [1]], matching_necessary_domains=matches,
        scope='One literal-row algebra witness only; not a graph or full ten-row realization')


def build():
    reduction, controls = support_reduction(), graph_controls()
    base_audit = inherited_base_audit()
    dependencies = [Path(__file__), SINGLE, CORES, CORES.with_name('support_table.md'), FINAL]
    dependencies += [ROOT / 'scripts' / (name + '.py') for name in (
        'c5_independent_support_capacity', 'c5_excess_one_subcovers', 'c5_941_two_spoke',
        'c5_excess_two_mixed_core_single_spoke', 'c5_excess_two_mixed_core_leaf_fibers',
        'c5_single_spoke_two_two', 'c5_single_spoke_cores',
        'c5_excess_two_four_spoke_binary_joint_controls')]
    dependencies += [ROOT / 'docs' / (name + '.md') for name in (
        'c5_short_support_singleton', 'c5_single_spoke_residual_locality',
        'c5_single_spoke_two_two', 'c5_single_spoke_cores', 'c5_single_spoke_bridge_path')]
    return dict(schema=1, scope=__doc__, pattern_order=ROWS,
        input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in dependencies},
        original_joint_contract=dict(component_order=['C', 'U'],
            C_ordered_contacts=['x', 'y'], C_shared_contact_permitted=True,
            U_ordered_distinct_contacts=['u', 'v'], joint_port_order=['b', 'a', 'y', 'u', 'v'],
            original_spoke_restoration='filter the same tuple by a != boundary[e]',
            pinned_fiber='complete (y,u,v) fiber for every literal (b,a), including empty'),
        marked_core_reduction=reduction, named_necessary_residual=named_residual(reduction),
        inherited_base_replay_audit=base_audit,
        fixed_complete_original_graph_controls=controls,
        summary=dict(inherited_named_records=196,
            inherited_base_document_hash_drifts=len(base_audit['document_provenance_drift']),
            target_counts=[dict(source_sigma=t['source_sigma'], **t['counts']) for t in reduction['targets']],
            independent_whole_graph_joins=controls['independent_whole_graph_joins'],
            independent_pinned_b_a_fibers=controls['independent_pinned_b_a_fibers'],
            selected_binary_subtype_excluded=False, epsilon_three_proved=False,
            new_lean_theorem=False, source_graph_enumeration=False))


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
