#!/usr/bin/env python3
"""Four original spokes: mixed-(1,1) with two named singleton unaries.

The arbitrary-size proof combines original critical-edge witnesses, short
unary supports, and degree-independent common lifts to obtain six spans on
five frame edges. This checker also transports inherited marked-core support
records and checks complete fixed-graph joins. It does not enumerate source
graphs or assert realization of support records.
"""
import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

from c5_independent_support_capacity import B, FRAME, ROWS, U
from c5_excess_one_subcovers import singleton
from c5_941_two_spoke import relabel_mask
from c5_single_spoke_cores import row_evidence, verify_evidence
from c5_excess_two_mixed_core_single_spoke import repeated_rows, residual_masks
from c5_excess_two_mixed_core_leaf_fibers import transport
from c5_excess_two_four_spoke_joint_controls import common_support_controls, graph_controls

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_mixed_core_four_spoke_singles/observations.json'
SINGLE = ROOT / 'artifacts/c5_excess_two_mixed_core_single_spoke/observations.json'
CORES = ROOT / 'artifacts/c5_single_spoke_cores/observations.json'


def edge(a, b):
    return tuple(sorted((a, b)))


def inherited_support_records():
    """The saved 114 records plus the 42 reflected s=0,1 records.

    A reflection is the one inherited whole-source transport, retaining the
    named binary and the two named unary components. No component orbit is
    independently selected or normalized.
    """
    source = json.loads(CORES.read_text())
    records = []
    for index, item in enumerate(source['records']):
        if item['status'] == 'T4_rejected':
            continue
        variants = [('original', item)]
        if item['spoke'] != 4:
            variants.append(('reflection', item['reflection']))
        for branch, data in variants:
            record = dict(spoke=data['spoke'],
                bans=tuple(tuple(f) for f in data['bans']),
                supports=tuple(tuple(s) for s in data['supports']),
                placements=data['placements'],
                provenance=dict(artifact=str(CORES.relative_to(ROOT)),
                    record_index=index, branch=branch,
                    original_record_status=item['status']))
            assert tuple(sorted(f[0] for f in record['bans'])) == tuple(
                sorted(U - {ROWS[0][record['spoke']]}))
            assert all(len(f) == 1 for f in record['bans'])
            records.append(record)
    assert len(records) == 156
    assert Counter(r['spoke'] for r in records) == {0: 24, 1: 18, 2: 18, 3: 24, 4: 72}
    assert len({(r['spoke'], r['bans'], r['supports']) for r in records}) == 156
    return records


def original_frames(target):
    records = []
    for index, item in enumerate(target['named_spoke_skeletons']['records']):
        supports = item['original_spoke_supports']
        if (item['status'] != 'necessary_skeleton_only'
                or sorted(map(len, supports)) != [1, 3]):
            continue
        aside, = [s for s in (0, 1) if len(supports[s]) == 3]
        bside = 1 - aside
        a, b = item['root_order'][aside], item['root_order'][bside]
        spoke, = supports[bside]
        records.append(dict(frame_index=len(records),
            inherited_skeleton_index=index, original_root_order=item['root_order'],
            a_three_spoke_side=aside, b_one_spoke_side=bside, a=a, b=b,
            original_a_spoke_support=tuple(supports[aside]), original_b_spoke=spoke,
            retained_original_root_spoke_edges=item['retained_source_edges'],
            original_component_contract=dict(C=dict(owners=[a, b],
                ordered_contacts=['x', 'y'], incidence=[1, 1],
                shared_contact_permitted=True),
                U=dict(owner=b, original_contact='u', incidence=1),
                V=dict(owner=b, original_contact='v', incidence=1))))
    assert len(records) == (20 if target['source_sigma'] == 933 else 60)
    return records


def marked_queries(target, frame, inherited, counts):
    """Necessary child masks and full-support identities for each original omission."""
    result = []
    sigma = target['source_sigma']
    triple, s = frame['original_a_spoke_support'], frame['original_b_spoke']
    for omitted in triple:
        forced = repeated_rows(sigma, triple, omitted)
        for qpos in sorted(forced):
            counts['marked_original_omission_q_queries'] += 1
            qi, = [i for i, row in enumerate(ROWS)
                   if len(set(row)) == 3 and singleton(row) == qpos]
            q = ROWS[qi]
            permutation = tuple((i + 4 - qpos) % 5 for i in range(5))
            q_transport = transport(q, permutation)
            assert tuple(q_transport['transported_row']) == ROWS[0]
            colors = q_transport['color_permutation']
            canonical_sigma = relabel_mask(sigma, permutation)
            kept = {permutation[i] for i in triple if i != omitted}
            available = U - {colors[q[i]] for i in triple if i != omitted}
            assert len(available) == 2
            children = [r for r in residual_masks(canonical_sigma)
                if {permutation[i] for i in forced}
                <= set(r['rejected_singleton_positions'])]
            assert children
            candidates = []
            for inherited_index, core in enumerate(inherited):
                if core['spoke'] != permutation[s]:
                    continue
                counts['inherited_support_lookups'] += 1
                if not kept <= set(core['supports'][0]):
                    continue
                counts['retained_leaf_attachment_passes'] += 1
                if core['bans'][0][0] not in available:
                    continue
                counts['marked_leaf_slack_passes'] += 1
                evidence = [row_evidence(core['spoke'], core['supports'], core['bans'], row)
                            for row in ROWS]
                for item in evidence:
                    verify_evidence(core, item)
                possible = [r['sigma'] for r in children if not any(
                    (ev['status'] == 'reject' and r['sigma'] >> ri & 1)
                    or (ev['status'] == 'accept' and not (r['sigma'] >> ri & 1))
                    for ri, ev in enumerate(evidence))]
                if not possible:
                    continue
                counts['necessary_child_mask_passes'] += 1
                inverse_boundary = {p: i for i, p in enumerate(permutation)}
                inverse_colors = {p: i for i, p in enumerate(colors)}
                candidates.append(dict(candidate_index=len(candidates),
                    inherited_support_record_index=inherited_index,
                    original_core_supports=[tuple(sorted(inverse_boundary[i] for i in support))
                                            for support in core['supports']],
                    original_q_forbidden_colors=[inverse_colors[f[0]] for f in core['bans']],
                    possible_canonical_child_sigmas=possible,
                    canonical_complete_row_evidence=evidence))
            result.append(dict(query_index=len(result), original_row_index=qi,
                original_literal_row=q, original_singleton_position=qpos,
                omitted_original_spoke=edge(frame['a'], omitted),
                omitted_original_boundary_endpoint=omitted,
                all_forced_rejected_positions=sorted(forced),
                retained_original_leaf_spoke_support=sorted(set(triple) - {omitted}),
                one_global_boundary_permutation=permutation,
                one_global_color_permutation=colors,
                complete_row_transports=[transport(row, permutation) for row in ROWS],
                canonical_source_sigma=canonical_sigma,
                canonical_retained_leaf_spoke_support=sorted(kept),
                canonical_marked_leaf_available_colors=sorted(available),
                necessary_canonical_child_masks=children, candidates=candidates))
    assert result
    return result


def same_source_supports(frame, queries):
    """Intersect actual C/U/V supports before applying any source exclusion.

    K=C union {a}; its support is the actual C support union the retained a
    spokes. Both original omitted edges and all forced rows query the same C,
    U and V. For repeated queries at the same literal row their three forbidden
    colors must also agree, because the retained leaf lists are identical.
    """
    lookups = []
    for query in queries:
        found = defaultdict(list)
        leaf = set(query['retained_original_leaf_spoke_support'])
        for candidate in query['candidates']:
            k_support, u_support, v_support = candidate['original_core_supports']
            for bits in range(32):
                c_support = tuple(i for i in sorted(B) if bits >> i & 1)
                if set(c_support) | leaf != set(k_support):
                    continue
                found[(c_support, tuple(u_support), tuple(v_support))].append(candidate)
        lookups.append(found)
    common = set.intersection(*(set(found) for found in lookups))
    domains = []
    for key in sorted(common):
        assignments = []
        for choice in product(*(lookup[key] for lookup in lookups)):
            by_row, coherent = {}, True
            for query, candidate in zip(queries, choice, strict=True):
                row = query['original_row_index']
                bans = tuple(candidate['original_q_forbidden_colors'])
                if row in by_row and by_row[row] != bans:
                    coherent = False
                    break
                by_row[row] = bans
            if coherent:
                assignments.append(dict(query_candidate_indices=[c['candidate_index'] for c in choice],
                    original_row_forbidden_colors=[dict(row_index=row,
                        component_order=['K=C+a', 'U', 'V'], forbidden_colors=bans)
                        for row, bans in sorted(by_row.items())]))
        if assignments:
            assert key[0] and all(len(s) == 2 and edge(*s) in FRAME for s in key[1:])
            assert all(item['forbidden_colors'][0] == 3 for assignment in assignments
                       for item in assignment['original_row_forbidden_colors'])
            domains.append(dict(domain_index=len(domains),
                original_component_order=['C', 'U', 'V'],
                actual_original_supports=[list(s) for s in key],
                compatible_same_source_query_assignments=assignments))
    return domains


def short_unary_exclusions(frame, domain):
    """Check literal original paths; the unbounded short-support theorem is paper."""
    edges = set(map(tuple, frame['retained_original_root_spoke_edges']))
    a, b = frame['a'], frame['b']
    assert edge(a, b) in edges and edge(b, frame['original_b_spoke']) in edges
    exclusions = []
    for index, name in ((1, 'U'), (2, 'V')):
        support = domain['actual_original_supports'][index]
        assert len(support) == 2 and edge(*support) in FRAME
        endpoints = sorted(set(frame['original_a_spoke_support']) - set(support))
        assert endpoints
        h = endpoints[0]
        path = [b, a, h]
        assert len(path) == len(set(path)) and h in B - set(support)
        assert all(edge(x, y) in edges for x, y in zip(path, path[1:]))
        demanded = [dict(row_index=item['row_index'],
            singleton_forbidden_color=item['forbidden_colors'][index])
            for assignment in domain['compatible_same_source_query_assignments']
            for item in assignment['original_row_forbidden_colors']]
        exclusions.append(dict(original_component=name, original_owner=b,
            original_contact='u' if name == 'U' else 'v',
            actual_original_support=support, adjacent_support_edge=edge(*support),
            original_root_spoke=edge(b, frame['original_b_spoke']),
            actual_original_exterior_path=path,
            path_internal_original_root=a,
            path_internal_H_minus_b_component='K=C+a',
            path_internal_avoids_original_unary=True,
            demanded_nonempty_forbidden_queries=demanded,
            paper_dependency='docs/c5_short_support_singleton.md',
            paper_conclusion='F_original_unary(row)=empty for every proper boundary row',
            status='excluded_by_original_short_support_theorem',
            scope='Original path premise check; arbitrary-size Gallai/minor exclusion is paper'))
    assert len(exclusions) == 2 and all(x['demanded_nonempty_forbidden_queries'] for x in exclusions)
    return exclusions


def support_reductions():
    source = json.loads(SINGLE.read_text())
    inherited = inherited_support_records()
    targets = []
    for original in source['targets']:
        counts, frames = Counter(), []
        for frame in original_frames(original):
            queries = marked_queries(original, frame, inherited, counts)
            domains = same_source_supports(frame, queries)
            counts['original_named_root_support_frames'] += 1
            counts['frames_with_same_source_support_domains'] += bool(domains)
            counts['same_source_actual_support_domains'] += len(domains)
            for domain in domains:
                domain['original_unary_exclusions'] = short_unary_exclusions(frame, domain)
                counts['original_short_unary_path_exclusions'] += 2
            frame.update(marked_original_omission_queries=queries,
                same_source_actual_support_domains=domains,
                status='excluded_by_original_short_unary_support' if domains
                    else 'excluded_by_marked_core_support_identity')
            frames.append(frame)
        sigma = original['source_sigma']
        expected = ({'original_named_root_support_frames': 20,
            'marked_original_omission_q_queries': 40, 'inherited_support_lookups': 1248,
            'retained_leaf_attachment_passes': 352, 'marked_leaf_slack_passes': 152,
            'necessary_child_mask_passes': 152, 'frames_with_same_source_support_domains': 12,
            'same_source_actual_support_domains': 96, 'original_short_unary_path_exclusions': 192}
            if sigma == 933 else {'original_named_root_support_frames': 60,
            'marked_original_omission_q_queries': 160, 'inherited_support_lookups': 4992,
            'retained_leaf_attachment_passes': 1232, 'marked_leaf_slack_passes': 648,
            'necessary_child_mask_passes': 536, 'frames_with_same_source_support_domains': 24,
            'same_source_actual_support_domains': 192, 'original_short_unary_path_exclusions': 384})
        assert dict(counts) == expected
        targets.append(dict(source_sigma=sigma, counts=dict(sorted(counts.items())),
            original_named_frames=frames, remaining_same_source_support_domains=[]))
    return dict(inherited_named_support_records=inherited, targets=targets,
        scope='Necessary actual-support identities and original path checks; no source realization')


def build():
    reductions = support_reductions()
    supports, controls = common_support_controls(), graph_controls()
    dependencies = [Path(__file__), SINGLE, CORES]
    dependencies += [ROOT / 'scripts' / (name + '.py') for name in (
        'c5_independent_support_capacity', 'c5_excess_one_subcovers', 'c5_941_two_spoke',
        'c5_single_spoke_cores', 'c5_excess_two_mixed_core_single_spoke',
        'c5_excess_two_mixed_core_leaf_fibers', 'c5_excess_two_mixed_core_spokes',
        'c5_excess_two_four_spoke_joint_controls')]
    dependencies += [ROOT / 'docs' / (name + '.md') for name in (
        'c5_excess_two_mixed_core_single_spoke', 'c5_excess_two_mixed_core_leaf_fibers',
        'c5_single_spoke_cores', 'c5_short_support_singleton',
        'c5_independent_support_capacity')]
    return dict(schema=1, scope=__doc__, pattern_order=ROWS, root_color_frame=sorted(U),
        input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in dependencies},
        original_joint_contract=dict(component_order=['C', 'U', 'V'],
            C_ordered_contacts=['x', 'y'], C_shared_contact_permitted=True,
            joint_port_order=['b', 'a', 'y', 'u', 'v'],
            whole_C_tuple_required=['x', 'y'],
            original_spoke_restoration='filter the same joint tuple by a != boundary[e]',
            pinned_fiber='for every literal (b,a), retain the complete (y,u,v) fiber, including empty'),
        marked_core_support_reductions=reductions,
        common_original_support_controls=supports,
        fixed_complete_original_graph_controls=controls,
        summary=dict(candidate_masks=[933, 941], inherited_named_support_records=156,
            original_named_root_support_frames=[20, 60], marked_original_omission_q_queries=200,
            necessary_child_support_records=[152, 536],
            same_source_actual_support_domains=[96, 192], original_short_unary_path_exclusions=576,
            common_three_long_support_lift_checks=46305,
            original_three_spoke_exterior_path_controls=50,
            fixed_original_graph_controls=12, independent_whole_graph_joins=360,
            independent_pinned_b_a_fibers=5760, same_color_spoke_equalities=72,
            remaining_selected_subtype_support_domains=0,
            four_spoke_31_mixed_11_two_singleton_unary_sources_excluded=True,
            all_four_spoke_sources_excluded=False, all_original_single_spoke_omissions_excluded=False,
            epsilon_three_proved=False, new_lean_theorem=False, source_graph_enumeration=False))


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
