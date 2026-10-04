#!/usr/bin/env python3
"""E6 additive local/query controls: endpoint, conservation, F1/F2 and G3.

Input graphs are only the nine saved AD controls and their ten D5 images. The
four G3 boundary queries enumerate literal necessary palettes, never source
keys or frame catalogs. All local relations retain original named contacts.
Exclusive-create generation; --check independently replays every output byte.
"""
from __future__ import annotations
import argparse
from itertools import combinations, product
import json
from pathlib import Path
from hashlib import sha256
import networkx as nx
import c5_excess_two_e6_controls as base


def subset_family(values):
    values = tuple(sorted(values))
    return tuple(frozenset(c) for n in range(len(values) + 1)
                 for c in combinations(values, n))


def local_endpoint_queries(graph, patterns):
    edges = tuple(map(tuple, graph['all_edges'])); vertices = tuple(graph['vertices'])
    ad = base.adjacency(edges, vertices)
    records = []; conservation = []
    for piece in graph['structural_checks']['pieces']:
        if piece['kind'] != 'unary' or len(piece['support']) != 3 or piece['shield_length'] != 2:
            continue
        assert graph['structural_checks']['full_B_touch_measured']
        p = tuple(piece['vertices']); pset = set(p)
        outside = nx.Graph(); outside.add_nodes_from(set(vertices) - pset)
        outside.add_edges_from(e for e in edges if not (set(e) & pset))
        assert nx.is_connected(outside)
        shields = tuple(map(tuple, piece['actual_shield_edges']))
        endpoints = sorted(v for v in base.B if sum(v in e for e in shields) == 1)
        assert len(endpoints) == 2
        contacts = tuple(v for vv in piece['root_contacts'].values() for v in vv)
        local_edges = tuple(e for e in edges if set(e) <= set(base.B + p))
        local_rows = base.relations(local_edges, patterns, p)
        queries = []; singletons = []
        for i, row in enumerate(local_rows):
            assert row
            contact_tuples = sorted(set(tuple(t[p.index(v)] for v in contacts) for t in row))
            forbidden = set.intersection(*(set(t) for t in contact_tuples))
            endpoint_colours = {patterns[i][v] for v in endpoints}
            assert not (forbidden & endpoint_colours)
            queries.append(dict(row_index=i, literal_boundary=list(patterns[i]),
                                original_contact_roles=list(contacts),
                                complete_joint_contact_relation=[list(t) for t in contact_tuples],
                                F_U=sorted(forbidden), endpoint_colours=sorted(endpoint_colours)))
            if len(contacts) == 1 and len(contact_tuples) == 1 and len(set(patterns[i])) == 3:
                # Pin the actual owner to the unique contact colour. This is a
                # refused owner query; full degree-four tightness is tested.
                owner = next(int(r) for r, vv in piece['root_contacts'].items() if vv)
                colour = contact_tuples[0][0]
                f = dict(zip(base.B, patterns[i])); f[owner] = colour
                exact_lists = []; d_membership = []
                for v in p:
                    ns = sorted(set(ad[v]) - pset)
                    used = [f[w] for w in ns]
                    allowed = sorted(set(range(4)) - set(used))
                    internal_degree = len(set(ad[v]) & pset)
                    assert len(allowed) == internal_degree and len(set(used)) == len(used)
                    if v != contacts[0]:
                        assert 3 in allowed
                    d_membership.append(3 in allowed)
                    exact_lists.append(dict(vertex=v, actual_external_neighbours=ns,
                                            exact_list=allowed, internal_degree=internal_degree))
                singletons.append(dict(row_index=i, owner=owner, owner_colour=colour,
                                       unique_contact_colour=colour, exact_degree_lists=exact_lists,
                                       D_membership_by_original_vertex=d_membership))
        if singletons:
            memberships = [row['D_membership_by_original_vertex'] for row in singletons]
            assert all(m == memberships[0] for m in memberships)
            forced_unused = [row['unique_contact_colour'] == 3 for row in singletons]
            assert len(set(forced_unused)) == 1
        records.append(dict(original_piece_vertices=list(p), actual_support=piece['support'],
                            actual_shield_edges=piece['actual_shield_edges'], actual_endpoints=endpoints,
                            complete_original_U_relation_summary=base.relation_summary(local_rows),
                            all_ten_literal_boundary_queries=queries))
        conservation.append(dict(original_piece_vertices=list(p), original_contact_roles=list(contacts),
                                 unused_literal_colour=3, exact_singleton_refusal_queries=singletons,
                                 applicable_query_pair_count=len(singletons) * (len(singletons) - 1) // 2,
                                 membership_constant=True))
    return records, conservation


def all_four_core_queries(graph, patterns, singletons):
    edges = tuple(map(tuple, graph['all_edges'])); private = tuple(graph['private_roles'])
    valid = base.degree_valid_subgraphs(edges, patterns, private, singletons)
    order = tuple(map(tuple, valid['nonframe_edge_bit_order']))
    source_pieces = graph['structural_checks']['pieces']
    results = []; f1 = []; f2 = []
    for m in valid['all_degree_valid_subgraphs']:
        active = tuple(m['active_private_vertices'])
        if m['epsilon'] != 0 or not m['Q'] or not {5, 6} <= set(active):
            continue
        kept = base.CYCLE + tuple(e for i, e in enumerate(order) if m['kept_nonframe_bits'] >> i & 1)
        if (5, 6) not in kept:
            continue
        h = nx.Graph(); h.add_nodes_from(active); h.add_edges_from(
            e for e in kept if set(e) <= set(active))
        assert nx.is_connected(h) and len(m['Q']) == 1
        q = m['Q'][0]; index = singletons[q]
        rows = base.relations(kept, patterns, active)
        assert not rows[index]
        witnesses = []
        for e in kept:
            if e in base.CYCLE:
                continue
            minus = tuple(ee for ee in kept if ee != e)
            row = base.relation(minus, patterns[index], active)
            assert row
            f = dict(zip(base.B, patterns[index])); f.update(zip(active, row[0]))
            assert f[e[0]] == f[e[1]]
            witnesses.append([list(e), [[v, f[v]] for v in base.B + active]])
        triangles = []
        blocks = sorted(tuple(sorted(b)) for b in nx.biconnected_components(h))
        for block in blocks:
            assert len(block) in (2, 3)
            if len(block) == 3:
                assert h.subgraph(block).number_of_edges() == 3
                assert not set(block) & set().union(*(set(t) for t in triangles)) if triangles else True
                triangles.append(block)
        core = dict(active_private_vertices=list(active), kept_nonframe_bits=m['kept_nonframe_bits'],
                    sigma_mask=m['sigma_mask'], Q=m['Q'], actual_H_blocks=[list(b) for b in blocks],
                    exact_q_criticality_witnesses=witnesses,
                    complete_same_frame_relations_summary=base.relation_summary(rows))
        results.append(core)
        # F1: one root spoke and the entire opposite unit-unary are omitted;
        # the original mixed11 is retained with a single shared contact.
        for a, b in ((5, 6), (6, 5)):
            for omitted_u in source_pieces:
                if omitted_u['kind'] != 'unary' or omitted_u['root_incidence'][(5, 6).index(a)] != 0 or omitted_u['root_incidence'][(5, 6).index(b)] != 1:
                    continue
                omitted_set = set(omitted_u['vertices'])
                if set(active) != set(private) - omitted_set:
                    continue
                without_u = tuple(e for e in edges if not (set(e) & omitted_set))
                spoke_losses = tuple(e for e in without_u if e not in kept)
                if len(spoke_losses) != 1 or a not in spoke_losses[0] or not any(v in base.B for v in spoke_losses[0]):
                    continue
                mixed = [p for p in source_pieces if p['kind'] == 'mixed']
                if len(mixed) != 1 or mixed[0]['root_incidence'] != [1, 1] or mixed[0]['root_contacts']['5'] != mixed[0]['root_contacts']['6']:
                    continue
                assert set(mixed[0]['vertices']) <= set(active)
                assert graph['structural_checks']['unary'] <= 2
                remaining_u = [u for u in source_pieces if u['kind'] == 'unary' and u != omitted_u]
                assert all(sum(u['root_incidence']) == 1 for u in remaining_u)
                ua = sum(u['root_incidence'][(5, 6).index(a)] for u in remaining_u)
                ub = sum(u['root_incidence'][(5, 6).index(b)] for u in remaining_u)
                assert ua <= 1 and ub <= 1 and (ua, ub) != (1, 1)
                t = {budget['root']: len(budget['actual_spokes']) for budget in graph['structural_checks']['root_budgets']}
                assert (t[a], t[b]) == (3 - ua, 2 - ub)
                f1.append(dict(core_bits=m['kept_nonframe_bits'], Q=m['Q'], ordered_roots=[a, b],
                               actual_omitted_spoke=list(spoke_losses[0]), omitted_original_unit_unary=omitted_u['vertices'],
                               remaining_original_unary_counts=[ua, ub], original_root_spoke_counts=[t[a], t[b]],
                               classified_entry={(0, 0):'G2', (0, 1):'3,1 singles', (1, 0):'J4'}[(ua, ub)]))
        # F2 requires the rejecting core to be precisely G minus sole mixed11.
        mixed = [p for p in source_pieces if p['kind'] == 'mixed']
        if len(mixed) == 1 and mixed[0]['root_incidence'] == [1, 1]:
            omitted = set(mixed[0]['vertices'])
            if set(active) == set(private) - omitted and set(kept) == {e for e in edges if not (set(e) & omitted)}:
                assert (5, 6) in set(nx.bridges(h)) or (6, 5) in set(nx.bridges(h))
                root_class = []
                for i, r in enumerate((5, 6)):
                    unary = [p for p in source_pieces if p['kind'] == 'unary' and p['root_incidence'][i]]
                    capacity = sum(p['root_incidence'][i] for p in unary)
                    assert capacity <= 2
                    if capacity == 0:
                        assert not unary
                    elif capacity == 1:
                        assert len(unary) == 1 and unary[0]['root_incidence'][i] == 1
                    else:
                        assert len(unary) == 1 and unary[0]['root_incidence'][i] == 2
                    t = next(len(b['actual_spokes']) for b in graph['structural_checks']['root_budgets'] if b['root'] == r)
                    assert t == 3 - capacity
                    root_class.append(dict(root=r, original_unary_incidence=capacity,
                                           original_unary_vertices=[p['vertices'] for p in unary], original_spoke_count=t))
                f2.append(dict(core_bits=m['kept_nonframe_bits'], Q=m['Q'], omitted_original_mixed=mixed[0]['vertices'],
                               original_root_classes=root_class, actual_zw_is_bridge=True))
    return results, f1, f2


def g3_literal_queries(patterns, singletons):
    specified = (((0, 1, 2), 3, (0, 3, 4), (0, 2)),
                 ((1, 2, 3), 0, (0, 3, 4), (1, 3)),
                 ((0, 1, 4), 3, (1, 2, 3), (1, 4)),
                 ((0, 3, 4), 1, (1, 2, 3), (0, 3)))
    records = []
    for support, q, expected_u, expected_b in specified:
        beta = patterns[singletons[q]]
        a_arcs = [tuple((start + j) % 5 for j in range(3)) for start in base.B
                  if set((start, (start + 1) % 5, (start + 2) % 5)) == set(support)]
        assert len(a_arcs) == 1
        a_arc = a_arcs[0]; c = beta[a_arc[0]]; r = beta[a_arc[1]]
        assert c == beta[a_arc[2]] and c != r
        leaf_list = frozenset(set(range(4)) - {c, r})
        gap = tuple((a_arc[-1] + j) % 5 for j in range(4))
        assert gap[-1] == a_arc[0]
        u_arcs = (gap[:3], gap[1:])
        survivors = []
        for u_arc in u_arcs:
            endpoints = (u_arc[0], u_arc[-1]); banned = {beta[v] for v in endpoints}
            for fk in subset_family(leaf_list):
                for fu in subset_family(set(range(4)) - banned):
                    if len(fu) > 2:
                        continue
                    for b_spoke in base.B:
                        if b_spoke == u_arc[1]:
                            continue
                        b_palette = frozenset(set(range(4)) - {beta[b_spoke]})
                        if not b_palette <= fk | fu:
                            continue
                        assert beta[b_spoke] == c and r in fu
                        assert set(u_arc) == set(expected_u) and beta[u_arc[1]] == r
                        assert b_spoke in expected_b
                        survivors.append(dict(actual_U_arc=list(u_arc), b_actual_single_spoke=b_spoke,
                                              exact_necessary_F_K=sorted(fk), exact_necessary_F_U=sorted(fu),
                                              complete_b_palette=sorted(b_palette)))
        assert survivors
        assert {record['b_actual_single_spoke'] for record in survivors} == set(expected_b)
        records.append(dict(a_actual_three_spoke_support=list(support), query_singleton=q,
                            literal_boundary=list(beta), a_actual_arc=list(a_arc), complementary_three_edge_gap=list(gap),
                            leaf_list=sorted(leaf_list), repeated_endpoint_colour=c, middle_colour=r,
                            forced_original_U_support=list(expected_u), allowed_actual_b_spokes=list(expected_b),
                            complete_literal_necessary_palette_survivors=survivors))
    return records


def g4_literal_singleton_schedules(patterns, singletons):
    records = []
    for start in base.B:
        arc = tuple((start + j) % 5 for j in range(3))
        for e in base.CYCLE:
            if arc[1] in e:
                continue
            domains = []; literal_queries = []
            for q in (0, 1, 3):
                beta = patterns[singletons[q]]
                seen = {beta[v] for v in arc}
                assert len(seen) in (2, 3)
                domain = set(range(4)) - {beta[v] for v in e} - {beta[arc[0]], beta[arc[-1]]}
                if len(seen) == 2:
                    domain &= seen  # unseen-colour swap cannot fix a singleton.
                domains.append(tuple(sorted(domain)))
                literal_queries.append(dict(singleton=q, literal_boundary=list(beta),
                                            actual_U_seen_colours=sorted(seen),
                                            endpoint_colours=[beta[arc[0]], beta[arc[-1]]],
                                            actual_a_spoke_colours=[beta[v] for v in e],
                                            necessary_singleton_domain=sorted(domain)))
            before = tuple(product(*domains))
            after = tuple(t for t in before if len({d == 3 for d in t}) == 1)
            assert not after
            records.append(dict(actual_U_arc=list(arc), actual_a_spoke_frame_edge=list(e),
                                ordered_singleton_queries=[0, 1, 3], literal_queries=literal_queries,
                                necessary_schedules_before_D_conservation=[list(t) for t in before],
                                schedules_after_D_conservation=[]))
    assert len(records) == 15
    return records


def build(root):
    input_path = 'artifacts/c5_excess_two_e6/controls.json'
    main_source = 'scripts/c5_excess_two_e6_controls.py'
    raw = (root / input_path).read_bytes(); bundle = json.loads(raw)
    patterns = tuple(map(tuple, bundle['pattern_order']))
    singletons = {int(q): i for q, i in bundle['singleton_to_pattern_index'].items()}
    images = []; counts = dict(D5_images_checked=0, endpoint_U_applicable=0,
                              endpoint_literal_boundary_queries=0, unused_D_singleton_refusal_queries=0,
                              unused_D_actual_query_pairs=0, all_four_rejecting_qcores=0,
                              F1_actual_antecedents=0, F2_actual_antecedents=0)
    for source in bundle['AD_controls']:
        for image in source['all_D5_images']:
            graph = image['actual_control']
            endpoint, conservation = local_endpoint_queries(graph, patterns)
            cores, f1, f2 = all_four_core_queries(graph, patterns, singletons)
            counts['D5_images_checked'] += 1
            counts['endpoint_U_applicable'] += len(endpoint)
            counts['endpoint_literal_boundary_queries'] += sum(len(p['all_ten_literal_boundary_queries']) for p in endpoint)
            counts['unused_D_singleton_refusal_queries'] += sum(len(p['exact_singleton_refusal_queries']) for p in conservation)
            counts['unused_D_actual_query_pairs'] += sum(p['applicable_query_pair_count'] for p in conservation)
            counts['all_four_rejecting_qcores'] += len(cores)
            counts['F1_actual_antecedents'] += len(f1); counts['F2_actual_antecedents'] += len(f2)
            images.append(dict(original_source_path=source['source_path'], frame_D5_map=image['frame_D5_map'],
                               actual_graph_sigma=graph['sigma_mask'], actual_graph_edges=graph['all_edges'],
                               endpoint_queries=endpoint, unused_D_conservation=conservation,
                               all_four_rejecting_original_qcores=cores, F1_actual_queries=f1, F2_actual_queries=f2))
    literal = g3_literal_queries(patterns, singletons)
    counts['G3_literal_boundary_queries'] = len(literal)
    counts['G3_literal_necessary_palette_survivors'] = sum(len(r['complete_literal_necessary_palette_survivors']) for r in literal)
    g4 = g4_literal_singleton_schedules(patterns, singletons)
    counts['G4_literal_arc_and_spoke_queries'] = len(g4)
    counts['G4_schedules_before_D_conservation'] = sum(len(r['necessary_schedules_before_D_conservation']) for r in g4)
    counts['G4_schedules_after_D_conservation'] = 0
    counts['controls_excluded'] = 0
    assert counts['D5_images_checked'] == 90
    return dict(schema='c5-excess-two-e6-local-controls-v1', base='d00aba4', workers_used=1,
                four_colour_oracle_used=False, source_key_enumeration=False,
                source_sha256={input_path:sha256(raw).hexdigest(), main_source:sha256((root / main_source).read_bytes()).hexdigest()},
                evidence_boundary='Exact saved positive controls and four literal necessary palette queries only; no arbitrary-source or topology proof is certified by these finite loops.',
                summary=counts, all_D5_local_controls=images,
                G3_four_literal_necessary_queries=literal,
                G4_literal_arc_and_spoke_singleton_schedules=g4)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output', type=Path)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    output = args.output or args.root / 'artifacts/c5_excess_two_e6/local_controls.json'
    raw = base.canonical(build(args.root)) + b'\n'
    if args.check:
        assert output.read_bytes() == raw, 'byte replay mismatch'
        print(f'CHECK OK: {output}; {len(raw)} bytes')
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open('xb') as stream:
            stream.write(raw)
        print(f'GENERATED: {output}; {len(raw)} bytes')


if __name__ == '__main__':
    main()
