#!/usr/bin/env python3
"""Same-row endpoint-hub exclusion of the inherited 32/64 binary domains.

The unbounded tight-list/Gallai and two/three-hub K5 arguments are paper.
These checks retain named original domains and complete ordered U schemas;
hub contractions are topology only. No source graph catalogue is generated.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from c5_excess_two_four_spoke_binary_star import component_relation
from c5_short_support_singleton import connected, edge, k5_witness

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_four_spoke_binary_hubs/observations.json'
SOURCE = ROOT / 'artifacts/c5_excess_two_four_spoke_binary_star/observations.json'
SHORT = ROOT / 'artifacts/c5_short_support_singleton/observations.json'
FRAME = {edge(i, (i + 1) % 5) for i in range(5)}
COLORS = set(range(4))


def forbidden(relation):
    assert relation
    return set.intersection(*(set(t) for t in relation))


def released(relation, bans):
    return all(any(t[j] == c and t[1-j] != c for t in relation)
               for c in bans for j in (0, 1))


def schema_catalogue():
    """Replay the inherited IDs from their sixteen full ordered tuples."""
    pairs = list(product(range(4), repeat=2))
    schemas = []
    for bits in range(1, 1 << 16):
        relation = [t for i, t in enumerate(pairs) if bits >> i & 1]
        bans = forbidden(relation)
        if bans and released(relation, bans):
            schemas.append(dict(id=len(schemas), forbidden=sorted(bans), tuples=relation))
    assert len(schemas) == 386
    return schemas


def endpoint_hubs(frame, support, row, color):
    """Explicit exterior bags, checked before any hypothetical U contraction."""
    a, b = frame['a'], frame['b']
    external = FRAME | {edge(a, b), edge(b, frame['original_b_spoke'])}
    external |= {edge(a, i) for i in frame['original_a_spoke_support']}
    choices = []
    for z in support:
        if row[z] != color:
            continue
        others = sorted(set(support) - {z})
        if len(others) == 2 and edge(*others) not in FRAME:
            continue
        if len(others) not in (1, 2):
            continue
        merged = sorted((set(range(5)) - set(others)) | {a, b})
        bags = [[v] for v in others] + [merged]
        if not all(connected(bag, external) for bag in bags):
            continue
        hub_colors = [row[v] for v in others] + [color]
        if len(set(hub_colors)) != len(bags):
            continue
        witnesses = []
        for i, j in combinations(range(len(bags)), 2):
            adjacent = [e for e in sorted(external)
                        if (e[0] in bags[i] and e[1] in bags[j])
                        or (e[1] in bags[i] and e[0] in bags[j])]
            if not adjacent:
                break
            witnesses.append(dict(hub_pair=[i, j], original_edge=adjacent[0]))
        else:
            assert all(not set(x) & set(y) for x, y in combinations(bags, 2))
            mapping = {v: next(i for i, bag in enumerate(bags) if v in bag)
                       for v in [*range(5), a, b]}
            assert mapping[b] == mapping[z]
            assert all(mapping[x] != mapping[y] for x, y in combinations(support, 2))
            choices.append(dict(merged_boundary_endpoint=z, forbidden_color=color,
                original_exterior_edges=sorted(external), connected_exterior_hub_bags=bags,
                auxiliary_hub_colors=hub_colors, all_hub_adjacencies=witnesses,
                exterior_vertex_to_hub=mapping,
                only_possible_U_neighbor_collision=[b, z],
                collision_excluded_by='Same-row tightness: a U contact cannot also attach to the boundary endpoint of color b',
                paper_lemma='two_hub_Gallai_K5' if len(bags) == 2 else 'three_hub_Gallai_K5'))
    assert choices, (frame['frame_index'], support, row, color)
    return choices[0]


def tightness_controls(support, row, color, endpoint):
    records = []
    for size in range(len(support) + 1):
        for attachments, contact in product(combinations(support, size), (False, True)):
            degree = 4 - size - int(contact)
            if degree < 1:
                continue
            outside = [row[i] for i in attachments] + ([color] if contact else [])
            available = sorted(COLORS - set(outside))
            slack = len(available) - degree
            assert slack == len(outside) - len(set(outside)) >= 0
            if contact and endpoint in attachments:
                assert slack > 0
            records.append(dict(boundary_attachments=attachments, original_b_contact=contact,
                internal_degree=degree, literal_available_colors=available, slack=slack,
                merged_neighbor_collision=contact and endpoint in attachments))
    assert any(r['merged_neighbor_collision'] for r in records)
    return records


def full_u_options(query, candidate, inherited, catalogue):
    base = inherited[candidate['inherited_record_index']]
    inverse = {v: i for i, v in enumerate(query['one_global_color_permutation'])}
    boundary = query['one_global_boundary_permutation']
    support = candidate['actual_original_U_support']
    assert sorted(boundary[i] for i in support) == base['supports'][1]
    bans = candidate['original_forbidden_colors'][1]
    assert sorted(inverse[c] for c in base['bans'][1]) == bans
    row = query['original_literal_row']
    options = []
    for ident in base['relation_schema_ids'][1]:
        relation = sorted(tuple(inverse[c] for c in t) for t in catalogue[ident]['tuples'])
        assert forbidden(relation) == set(bans) and released(relation, bans)
        seen = {row[i] for i in support}
        for p in permutations(range(4)):
            if all(p[c] == c for c in seen):
                assert {tuple(p[c] for c in t) for t in relation} == set(relation)
        options.append(dict(inherited_schema_id=ident, complete_literal_U_tuples=relation))
    assert options
    return options


def fixed_controls():
    """Actual degree-four U graphs lifting both hub lemmas; never disk sources."""
    motifs = []
    for length in (3, 5, 7):
        vertices = list(range(length + 1))
        edges = {edge(u, v) for u, v in zip(vertices, vertices[1:])}
        attachments = {v: [2, 3] if v in (0, length) else [2, 4] for v in vertices}
        motifs.append(dict(name=f'path_{length}', vertices=vertices, edges=edges,
            contacts=[0, length], attachments=attachments, hub_count=3,
            minor_groups=[[2], [3], 'Z', ['U', 0], ['Urest', *vertices[1:]]]))
    for length in (3, 5, 7):
        vertices = list(range(length))
        edges = {edge(i, (i + 1) % length) for i in vertices}
        attachments = {v: [2] if v in (0, 1) else [2, 4] for v in vertices}
        motifs.append(dict(name=f'cycle_{length}', vertices=vertices, edges=edges,
            contacts=[0, 1], attachments=attachments, hub_count=2,
            minor_groups=[[2], 'Z', ['U', 0], ['U', 1], ['Urest', *vertices[2:]]]))
    # One inherited leaf-cycle witness with a third hub touching the remainder.
    source = json.loads(SHORT.read_text())['three_hub_controls']['rejected_cases']
    selected = None
    for case in source:
        if case['reason'] != 'leaf_cycle_with_third_hub':
            continue
        for z in case['hub_order']:
            neighbors = [v for v, hs in zip(case['component_vertices'], case['attachments']) if z in hs]
            if len(neighbors) >= 3:
                selected = (case, z, neighbors[:2])
                break
        if selected:
            break
    assert selected
    case, z, contacts = selected
    other = [h for h in case['hub_order'] if h != z]
    boundary_map = dict(zip(other, [2, 3]))
    attachments = {v: sorted(boundary_map[h] if h != z else 4
        for h in hs if h != z or v not in contacts)
        for v, hs in zip(case['component_vertices'], case['attachments'])}
    groups = []
    for bag in case['branch_sets']:
        group = []
        for v in bag:
            group.extend(['Z'] if v == z else [['B', boundary_map[v]]]
                         if v in boundary_map else [['U', v]])
        groups.append(group)
    motifs.append(dict(name='inherited_leaf_cycle_third_hub',
        vertices=case['component_vertices'], edges=set(map(tuple, case['component_edges'])),
        contacts=contacts, attachments=attachments, hub_count=3, inherited_groups=groups))
    records = []
    q = [0, 1, 0, 2, 1]
    for c_length, motif, swapped in product((0, 2, 4), motifs, (False, True)):
        a, b = (5, 6) if swapped else (6, 5)
        cv = list(range(9, 10 + c_length))
        ce = {edge(u, v) for u, v in zip(cv, cv[1:])}
        # x=y has two owners and two original boundary attachments.
        ca = {v: [0, 4] for v in cv}
        mapping = {v: 20 + v for v in motif['vertices']}
        uv = [mapping[v] for v in motif['vertices']]
        ue = {edge(mapping[u], mapping[v]) for u, v in motif['edges']}
        ua = {mapping[v]: support for v, support in motif['attachments'].items()}
        u, v = [mapping[w] for w in motif['contacts']]
        x, y = cv[0], cv[-1]
        original = FRAME | ce | ue | {edge(a, b), edge(a, x), edge(b, y), edge(b, u), edge(b, v)}
        original |= {edge(a, i) for i in (0, 1, 2)} | {edge(b, 2)}
        original |= {edge(w, i) for w, support in {**ca, **ua}.items() for i in support}
        interior = [a, b, *cv, *uv]
        assert all(sum(w in e for e in original) == (5 if w in (a, b) else 4) for w in interior)
        rc = component_relation(cv, ce, ca, q, (x, y))
        ru = component_relation(uv, ue, ua, q, (u, v))
        assert set(rc['complete_tuples']) == {(2, 2), (3, 3)}
        assert forbidden(ru['complete_tuples']) == {1} and released(ru['complete_tuples'], {1})
        joint = [(d, ac, yc, uc, vc) for xc, yc in rc['complete_tuples']
            for uc, vc in ru['complete_tuples'] for ac in sorted(COLORS - {q[i] for i in (0, 1, 2)} - {xc})
            for d in sorted(COLORS - {q[2], ac, yc, uc, vc})]
        assert not joint
        merged = {a, b, 0, 1, 4} if motif['hub_count'] == 3 else {a, b, 0, 1, 3, 4}
        assert connected(merged, original)
        bags = []
        if 'inherited_groups' in motif:
            for group in motif['inherited_groups']:
                bag = set()
                for item in group:
                    bag |= merged if item == 'Z' else {item[1]} if item[0] == 'B' else {mapping[item[1]]}
                bags.append(bag)
        else:
            for group in motif['minor_groups']:
                bags.append(merged if group == 'Z' else
                    {mapping[w] for w in group[1:]} if group[0] in ('U', 'Urest') else set(group))
        witness = k5_witness(original, bags)
        # No same-colored b/4 neighbor is duplicated in the topology image.
        assert all(not (edge(b, w) in original and edge(4, w) in original) for w in uv)
        image = {w: ('Z' if w in merged else w) for w in [*range(5), *interior]}
        for w in uv:
            original_neighbors = {z if w == t else t for t, z in original if w in (t, z)}
            assert len({image[t] for t in original_neighbors}) == 4
        records.append(dict(control_index=len(records), a=a, b=b, C_even_path_length=c_length,
            U_motif=motif['name'], original_edges=sorted(original), original_C_vertices=cv,
            original_U_vertices=uv, original_contacts=dict(C=[x, y], U=[u, v]),
            actual_attachments={**ca, **ua}, literal_row=q, complete_C_relation=rc,
            complete_U_relation=ru, complete_original_joint=joint,
            topology_only_merged_exterior_bag=sorted(merged), **witness,
            scope='Fixed full degree graph with literal relations and original K5 bags; no disk/Sigma/criticality claim'))
    assert len(records) == 42
    return records


def build():
    source = json.loads(SOURCE.read_text())
    catalogue = schema_catalogue()
    targets, exchange_keys = [], {}
    query_checks, schema_checks, d5_checks, tight_checks = 0, 0, 0, 0
    for target in source['targets']:
        counts, records = Counter(), []
        for inherited_frame in target['frames']:
            frame = inherited_frame['original_frame_context']
            for inherited_domain in inherited_frame['domains']:
                if inherited_domain['status'] != 'necessary_residual_not_realization':
                    continue
                domain = inherited_domain['original_domain']
                support = domain['actual_original_supports'][1]
                assignments = []
                for assignment in domain['compatible_same_source_query_assignments']:
                    queries = []
                    for query, candidate_index in zip(frame['marked_original_queries'],
                            assignment['query_candidate_indices'], strict=True):
                        candidate = query['candidates'][candidate_index]
                        bans = candidate['original_forbidden_colors'][1]
                        assert len(bans) == 1
                        cert = endpoint_hubs(frame, support, query['original_literal_row'], bans[0])
                        options = full_u_options(query, candidate,
                            source['source_inherited_named_relation_records'], catalogue)
                        tight = tightness_controls(support, query['original_literal_row'], bans[0],
                            cert['merged_boundary_endpoint'])
                        queries.append(dict(query_context={k: v for k, v in query.items() if k != 'candidates'},
                            original_candidate=candidate, complete_U_relation_options=options,
                            endpoint_hub_certificate=cert, local_degree_tightness_controls=tight))
                        query_checks += 1
                        schema_checks += len(options)
                        tight_checks += len(tight)
                        for sign, shift in product((-1, 1), range(5)):
                            move = [(sign * i + shift) % 5 for i in range(5)]
                            moved_row = [None] * 5
                            for i in range(5):
                                moved_row[move[i]] = query['original_literal_row'][i]
                            moved_frame = dict(frame,
                                original_a_spoke_support=sorted(move[i] for i in frame['original_a_spoke_support']),
                                original_b_spoke=move[frame['original_b_spoke']])
                            moved = endpoint_hubs(moved_frame, sorted(move[i] for i in support), moved_row, bans[0])
                            assert moved['paper_lemma'] == cert['paper_lemma']
                            d5_checks += 1
                    assert queries
                    assignments.append(dict(original_assignment=assignment, query_certificates=queries))
                assert assignments
                lemmas = {q['endpoint_hub_certificate']['paper_lemma'] for a in assignments for q in a['query_certificates']}
                assert len(lemmas) == 1
                lemma, = lemmas
                counts[lemma] += 1
                counts['excluded_domains'] += 1
                record = dict(original_frame_context={k: v for k, v in frame.items() if k != 'marked_original_queries'},
                    original_domain=domain, inherited_star_sectors=inherited_domain['original_star_sectors'],
                    status='excluded_by_same_row_endpoint_hubs', complete_assignment_certificates=assignments)
                records.append(record)
                key = (target['source_sigma'], tuple(frame['original_a_spoke_support']), frame['original_b_spoke'],
                       tuple(map(tuple, domain['actual_original_supports'])), frame['a'], frame['b'])
                exchange_keys[key] = (domain['compatible_same_source_query_assignments'], lemma)
        expected = 32 if target['source_sigma'] == 933 else 64
        assert counts['excluded_domains'] == expected
        assert counts['two_hub_Gallai_K5'] == counts['three_hub_Gallai_K5'] == expected // 2
        targets.append(dict(source_sigma=target['source_sigma'], counts=dict(sorted(counts.items())), domains=records))
    for key, value in exchange_keys.items():
        assert exchange_keys[(*key[:-2], key[-1], key[-2])] == value
    assert len(exchange_keys) == 96 and query_checks == 192 and d5_checks == 1920
    paths = [Path(__file__), SOURCE, SHORT, ROOT / 'scripts/c5_excess_two_four_spoke_binary_star.py',
             ROOT / 'scripts/c5_short_support_singleton.py']
    return dict(schema=1, scope=__doc__, pattern_order=source['pattern_order'],
        input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths},
        inherited_base_replay_audit=source['inherited_base_replay_audit'], targets=targets,
        fixed_original_graph_controls=fixed_controls(),
        summary=dict(target_counts=[dict(source_sigma=t['source_sigma'], **t['counts'], remaining_domains=0) for t in targets],
            complete_original_query_certificates=query_checks, full_ordered_U_schema_checks=schema_checks,
            local_degree_tightness_checks=tight_checks,
            root_swap_domain_checks=len(exchange_keys), simultaneous_D5_hub_checks=d5_checks,
            fixed_full_degree_graph_controls=42, selected_entry_excluded=True,
            selected_binary_subtype_excluded=True, cross_row_palette_theorem_proved=False,
            epsilon_three_proved=False, new_lean_theorem=False))


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
