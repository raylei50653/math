#!/usr/bin/env python3
"""Replay E6's nine saved AD crit-orbit controls, with all ten D5 images.

This is a fixed-control certificate, not source-key or graph enumeration. Every
colouring is computed by finite MRV backtracking, never a four-colour oracle.
L1 for all edge subgraphs follows from the actually checked maximal proper edge
subgraphs and rejection monotonicity. All degree-valid control subgraphs are
also checked using saturation of the original degree-four components.
Generation exclusively creates the output; --check compares every byte.
"""
from __future__ import annotations
import argparse
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import networkx as nx

B = tuple(range(5))
CYCLE = tuple(sorted(tuple(sorted((i, (i + 1) % 5))) for i in B))
D5 = tuple(tuple((s * i + r) % 5 for i in B) for s in (1, -1) for r in B)
T4 = 932
TRIPLE = {0, 1, 3}
BASE = 'd00aba4'


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(',', ':')).encode()


def digest(value):
    return sha256(canonical(value)).hexdigest()


def edge(u, v):
    return tuple(sorted((u, v)))


def profile(mask, singletons):
    return sorted(q for q, i in singletons.items() if not (mask >> i & 1))


def adjacent_profile(q):
    return len(q) <= 1 or (len(q) == 2 and edge(*q) in CYCLE)


def adjacency(edges, vertices):
    graph = {v: set() for v in vertices}
    for u, v in edges:
        graph[u].add(v); graph[v].add(u)
    return graph


def relation(edges, row, private):
    """Complete named-private relation in one literal boundary colour frame."""
    vertices = B + tuple(private)
    graph = adjacency(edges, vertices)
    colours = dict(zip(B, row))
    answer = []
    assert all(colours[u] != colours[v] for u, v in CYCLE)

    def visit():
        if len(colours) == len(vertices):
            answer.append(tuple(colours[v] for v in private))
            return
        choices = []
        for v in private:
            if v in colours:
                continue
            used = {colours[w] for w in graph[v] if w in colours}
            allowed = tuple(c for c in range(4) if c not in used)
            if not allowed:
                return
            choices.append((len(allowed), -len(graph[v]), v, allowed))
        _, _, v, allowed = min(choices)
        for c in allowed:
            colours[v] = c
            visit()
        del colours[v]

    visit()
    return tuple(sorted(answer))


def relations(edges, patterns, private):
    return tuple(relation(edges, row, private) for row in patterns)


def sigma(rows):
    return sum(1 << i for i, row in enumerate(rows) if row)


def relation_summary(rows):
    return dict(complete_relation_sha256=digest(rows),
                tuple_counts=[len(row) for row in rows])


def components(edges, private):
    graph = nx.Graph(); graph.add_nodes_from(private); graph.add_edges_from(
        (u, v) for u, v in edges if u in private and v in private)
    roots = tuple(v for v in private if graph.degree(v) + sum(
        edge(v, b) in edges for b in B) == 5)
    assert roots == (5, 6)
    assert nx.is_connected(graph) and edge(*roots) in edges
    return roots, tuple(tuple(sorted(c)) for c in sorted(
        nx.connected_components(graph.subgraph(set(private) - set(roots))),
        key=lambda c: min(c)))


def shield(edges, rotation, private, piece):
    """Extract the actual shield from K_P's embedding, not support counts."""
    pset = set(piece); kset = set(B) | pset
    kept_rotation = {v: [w for w in rotation[v] if w in kset] for v in kset}
    emb = nx.PlanarEmbedding(); emb.set_data(kept_rotation); emb.check_structure()
    outside_faces = []
    # Every edge from B to H-P lies in the same open face F_P. The next kept
    # clockwise neighbour identifies its original embedding wedge exactly.
    for b, v in edges:
        if b not in B or v not in set(private) - pset:
            continue
        around = rotation[b]; j = around.index(v)
        nxt = next(around[(j + t) % len(around)] for t in range(1, len(around))
                   if around[(j + t) % len(around)] in kset)
        walk = emb.traverse_face(nxt, b)
        directed = tuple((walk[i], walk[(i + 1) % len(walk)])
                         for i in range(len(walk)))
        outside_faces.append(frozenset(directed))
    assert outside_faces and len(set(outside_faces)) == 1
    face = outside_faces[0]
    face_edges = {edge(u, v) for u, v in face}
    shield_edges = tuple(e for e in CYCLE if e not in face_edges)
    return dict(K_P_vertices=sorted(kset),
                K_P_rotation={str(v): kept_rotation[v] for v in sorted(kset)},
                outside_face_directed_edges=[list(e) for e in sorted(face)],
                actual_shield_edges=[list(e) for e in shield_edges],
                shield_length=len(shield_edges))


def structural_checks(edges, rotation, private, singletons, value):
    roots, pieces = components(edges, private)
    graph = nx.Graph(); graph.add_nodes_from(B + private); graph.add_edges_from(edges)
    emb = nx.PlanarEmbedding(); emb.set_data(rotation); emb.check_structure()
    assert set(emb.edges()) == {(u, v) for e in edges for u, v in (e, e[::-1])}
    assert any(set(emb.traverse_face(u, v)) == set(B) and
               len(emb.traverse_face(u, v)) == 5
               for u, v in (e for ab in CYCLE for e in (ab, ab[::-1])))
    assert graph.subgraph(B).number_of_edges() == 5
    ds = dict(graph.degree()); assert [ds[v] for v in private] == [5, 5] + [4] * (len(private) - 2)
    assert sum(ds[v] - 4 for v in private) == 2
    h = graph.subgraph(private); k = len(private)
    actual_h_edges = h.number_of_edges()
    actual_spokes = sum(u in B and v in private for u, v in edges)
    assert 4 * k + 2 == 2 * actual_h_edges + actual_spokes
    assert graph.number_of_edges() <= 3 * k + 7
    assert actual_h_edges >= k  # H is connected and cannot be a tree.
    hypothetical_tree_spokes = 2 * k + 4
    assert 5 + (k - 1) + hypothetical_tree_spokes == 3 * k + 8 > 3 * k + 7
    full_touch = set().union(*(set(graph[v]) & set(B) for v in private)) == set(B)
    # FullB-touch is a measured fact for each control; the theoretical assertion
    # is applied only when at least two singleton rows are rejected.
    q = profile(value, singletons)
    if len(q) >= 2:
        assert full_touch
    records = []; all_shields = []
    for piece in pieces:
        pset = set(piece)
        contacts = {str(r): sorted(pset & set(graph[r])) for r in roots}
        incidences = [len(contacts[str(r)]) for r in roots]
        assert any(incidences)
        mixed = all(incidences)
        support = sorted(set().union(*(set(graph[v]) & set(B) for v in piece)))
        outside = graph.subgraph(set(private) - pset)
        assert nx.is_connected(outside)  # zw remains in H-P.
        if mixed:
            assert support  # N-empty's exclusion, measured on all controls.
        arc = shield(edges, rotation, private, piece)
        es = set(map(tuple, arc['actual_shield_edges']))
        assert not (es & set().union(*all_shields)) if all_shields else True
        all_shields.append(es)
        if es:
            arc_graph = nx.Graph(); arc_graph.add_edges_from(es)
            assert nx.is_connected(arc_graph)
        if not mixed:
            assert len(es) >= 2
        if full_touch and len(support) >= 2:
            assert set(support) == {v for e in es for v in e}
        if len(es) < 5:
            internal = {v for v in B if sum(v in e for e in es) == 2}
            for v in internal:
                assert not (set(graph[v]) & (set(private) - pset))
        records.append(dict(vertices=list(piece), kind='mixed' if mixed else 'unary',
                            root_contacts=contacts, root_incidence=incidences,
                            support=support, one_sided=True,
                            internal_edges=[list(e) for e in edges if set(e) <= pset],
                            actual_boundary_attachments=[list(e) for e in edges
                                if e[0] in B and e[1] in pset],
                            **arc))
    mixed_count = sum(r['kind'] == 'mixed' for r in records)
    unary_count = len(records) - mixed_count
    assert mixed_count <= 2
    assert unary_count <= 2
    assert sum(r['shield_length'] for r in records) <= 5
    root_budget = []
    for r in roots:
        spokes = sorted(set(graph[r]) & set(B))
        contacts = [v for v in graph[r] if v in set(private) - set(roots)]
        assert len(spokes) + len(contacts) == 4
        root_budget.append(dict(root=r, actual_spokes=spokes,
                               actual_piece_contacts=sorted(contacts),
                               capacity_excluding_zw=4))
    return dict(full_B_touch_measured=full_touch,
                full_B_touch_two_rejections_applicable=len(q) >= 2,
                H_edge_count=actual_h_edges, boundary_attachment_count=actual_spokes,
                hypothetical_tree_boundary_attachment_count=hypothetical_tree_spokes,
                disk_edge_count=graph.number_of_edges(), disk_edge_upper_bound=3 * k + 7,
                H_is_tree=False, root_budgets=root_budget,
                pieces=records, m=mixed_count, unary=unary_count,
                total_actual_shield_length=sum(r['shield_length'] for r in records),
                N_empty_antecedent_count=sum(not r['support'] and r['kind'] == 'mixed' for r in records),
                m_three_antecedent=mixed_count >= 3)


def degree_valid_subgraphs(edges, patterns, private, singletons):
    """Exactly all control subgraphs with active private degrees >=4.

A retained original degree-four vertex keeps all original edges; propagation
selects its entire original H-{z,w} component and original root contacts.
Only original root spokes and zw remain freely selectable. Isolated private
vertices are treated as absent, so each named edge subset appears once.
"""
    roots, pieces = components(edges, private)
    nonframe = tuple(e for e in edges if e not in CYCLE)
    index = {e: i for i, e in enumerate(nonframe)}
    full = (1 << len(nonframe)) - 1
    seen = {}; rows = []
    for root_flags in product((False, True), repeat=2):
        kept_roots = {r for r, keep in zip(roots, root_flags) if keep}
        for piece_flags in product((False, True), repeat=len(pieces)):
            retained = set().union(*(set(p) for p, keep in zip(pieces, piece_flags) if keep))
            forced = tuple(e for e in nonframe if set(e) & retained)
            if any(v in roots and v not in kept_roots for e in forced for v in e):
                continue
            free = tuple(e for e in nonframe if not (set(e) & (set(private) - set(roots)))
                         and all(v in B or v in kept_roots for v in e))
            for free_flags in product((False, True), repeat=len(free)):
                kept = tuple(sorted(forced + tuple(e for e, keep in zip(free, free_flags) if keep)))
                bits = sum(1 << index[e] for e in kept)
                if bits in seen:
                    continue
                ds = Counter(v for e in kept for v in e)
                active = tuple(v for v in private if ds[v])
                if any(ds[v] < 4 for v in active):
                    continue
                seen[bits] = True
                epsilon = sum(ds[v] - 4 for v in active)
                rel = relations(CYCLE + kept, patterns, active)
                value = sigma(rel); q = profile(value, singletons)
                assert epsilon <= 2
                if bits != full:
                    assert epsilon <= 1 and adjacent_profile(q)
                if epsilon == 2:
                    assert bits == full
                if epsilon == 0:
                    assert len(q) <= 1
                rows.append(dict(kept_nonframe_bits=bits, active_private_vertices=list(active),
                                 active_private_degrees=[ds[v] for v in active], epsilon=epsilon,
                                 sigma_mask=value, Q=q, **relation_summary(rel)))
    assert full in seen
    proper = [row for row in rows if row['kept_nonframe_bits'] != full]
    maximal_proper = [row['kept_nonframe_bits'] for row in proper if not any(
        row['kept_nonframe_bits'] != other['kept_nonframe_bits'] and
        row['kept_nonframe_bits'] & other['kept_nonframe_bits'] == row['kept_nonframe_bits']
        for other in proper)]
    return dict(nonframe_edge_bit_order=[list(e) for e in nonframe],
                all_degree_valid_subgraphs=sorted(rows, key=lambda row: row['kept_nonframe_bits']),
                degree_valid_count=len(rows), proper_degree_valid_count=len(proper),
                maximal_proper_degree_valid_bits=sorted(maximal_proper),
                same_epsilon_two_subgraph_count=sum(row['epsilon'] == 2 for row in rows))


def local_refusal_checks(edges, patterns, private, full_relations, structure):
    graph = adjacency(edges, B + private)
    records = []
    for piece_record in structure['pieces']:
        piece = tuple(piece_record['vertices']); pset = set(piece)
        outside = tuple(v for v in private if v not in pset)
        indices = tuple(private.index(v) for v in outside)
        exterior_edges = tuple(e for e in edges if not (set(e) & pset))
        exterior = relations(exterior_edges, patterns, outside)
        complete_projections = [set(tuple(t[j] for j in indices) for t in row)
                                for row in full_relations]
        refused = []
        induced = nx.Graph(); induced.add_nodes_from(piece); induced.add_edges_from(
            e for e in edges if set(e) <= pset)
        blocks = sorted((tuple(sorted(c)) for c in nx.biconnected_components(induced)))
        for i, row in enumerate(patterns):
            for t in exterior[i]:
                if t in complete_projections[i]:
                    continue
                f = dict(zip(B, row)); f.update(zip(outside, t))
                lists = []
                for v in piece:
                    external = sorted(set(graph[v]) - pset)
                    used = [f[w] for w in external]
                    allowed = sorted(set(range(4)) - set(used))
                    internal_degree = len(set(graph[v]) & pset)
                    assert len(set(used)) == len(used)
                    assert len(allowed) == internal_degree
                    lists.append(dict(vertex=v, actual_external_neighbours=external,
                                      actual_external_colours=used, allowed_colours=allowed,
                                      internal_degree=internal_degree))
                # Gallai necessity is checked on the actual refused component,
                # without claiming that this finite test proves the theorem.
                for block in blocks:
                    bgraph = induced.subgraph(block)
                    assert (bgraph.number_of_edges() == len(block) * (len(block) - 1) // 2 or
                            (len(block) % 2 == 1 and all(d == 2 for _, d in bgraph.degree())))
                refused.append(dict(row_index=i, complete_outside_colouring=[
                    [v, f[v]] for v in B + outside], exact_degree_lists=lists))
        records.append(dict(piece_vertices=list(piece), outside_private_roles=list(outside),
                            complete_exterior_relation_summary=relation_summary(exterior),
                            actual_Gallai_blocks=[list(b) for b in blocks],
                            refused_exterior_pin_count=len(refused), refused_exterior_pins=refused))
    return records


def control(edges, rotation, patterns, singletons, private, original=None, include_relations=False):
    edges = tuple(sorted(edges))
    rel = relations(edges, patterns, private); value = sigma(rel)
    q = profile(value, singletons)
    assert value & T4 == T4 and q and not TRIPLE <= set(q)
    structure = structural_checks(edges, rotation, private, singletons, value)
    nonframe = tuple(e for e in edges if e not in CYCLE)
    saved_deletions = {} if original is None else {
        tuple(row['edge']): row for row in original['deletion_sigmas']}
    deletion_records = []
    for e in nonframe:
        kept = tuple(ee for ee in edges if ee != e)
        rows = relations(kept, patterns, private); new = sigma(rows)
        assert new != value and new | value == new
        qq = profile(new, singletons); assert adjacent_profile(qq)
        newly = [i for i in range(10) if (new & ~value) >> i & 1]
        witnesses = []
        for i in newly:
            f = tuple(patterns[i]) + rows[i][0]
            assert f[e[0]] == f[e[1]]
            assert all(f[u] != f[v] for u, v in kept)
            witnesses.append(dict(pattern_index=i, complete_colouring=list(f)))
        if original is not None:
            old = saved_deletions[e]
            assert old['sigma_mask'] == new and old['new_indices'] == newly
            for old_w in old['witnesses']:
                f = old_w['colouring']; i = old_w['pattern_index']
                assert tuple(f[:5]) == patterns[i]
                assert tuple(f[5:]) in rows[i]
                assert f[e[0]] == f[e[1]]
        deletion_records.append(dict(edge=list(e), sigma_mask=new, Q=qq,
                                     newly_accepted_indices=newly,
                                     criticality_witnesses=witnesses,
                                     **relation_summary(rows)))
    # Actual root and zw omission checks precede any q-minimality inference.
    root_omissions = []
    for r in (5, 6):
        kept = tuple(e for e in edges if r not in e)
        roles = tuple(v for v in private if v != r)
        rows = relations(kept, patterns, roles)
        assert sigma(rows) == 1023
        root_omissions.append(dict(omitted_root=r, kept_private_roles=list(roles),
                                   sigma_mask=1023, **relation_summary(rows)))
    zw_row = next(row for row in deletion_records if row['edge'] == [5, 6])
    assert zw_row['sigma_mask'] == 1023
    l3_applicable = False
    if structure['m'] == 1 and structure['unary'] == 1:
        mixed = next(p for p in structure['pieces'] if p['kind'] == 'mixed')
        unary = next(p for p in structure['pieces'] if p['kind'] == 'unary')
        budgets = structure['root_budgets']
        if mixed['root_incidence'] == [1, 1] and sorted(len(b['actual_spokes']) for b in budgets) == [2, 3]:
            a = next(b['root'] for b in budgets if len(b['actual_spokes']) == 3)
            b = 11 - a
            if unary['root_incidence'][(5, 6).index(a)] == 0:
                l3_applicable = True
                for row in deletion_records:
                    if a in row['edge'] and any(v in B for v in row['edge']):
                        assert len(row['Q']) <= 1
    spoke_redundancy = []
    for budget in structure['root_budgets']:
        r = budget['root']; spokes = budget['actual_spokes']
        for j in spokes:
            redundant = sorted(q0 for q0 in q if any(
                patterns[singletons[q0]][j] == patterns[singletons[q0]][k]
                for k in spokes if k != j))
            after = next(row for row in deletion_records if tuple(row['edge']) == edge(r, j))
            assert set(redundant) <= set(after['Q']) and adjacent_profile(redundant)
            spoke_redundancy.append(dict(root=r, actual_spoke=[r, j],
                                        all_actual_root_spokes=spokes,
                                        redundant_rejected_singletons=redundant,
                                        actual_deletion_Q=after['Q']))
    g2_g3_long_unary_applicable = False
    if structure['m'] == 1 and structure['unary'] == 1:
        unary = next(p for p in structure['pieces'] if p['kind'] == 'unary')
        mixed = next(p for p in structure['pieces'] if p['kind'] == 'mixed')
        if unary['shield_length'] >= 3 and sorted(len(b['actual_spokes']) for b in structure['root_budgets']) in ([2, 3], [1, 3]):
            g2_g3_long_unary_applicable = True
            complement = nx.Graph(); complement.add_edges_from(
                set(CYCLE) - set(map(tuple, unary['actual_shield_edges'])))
            endpoints = {v for v, d in complement.degree() if d == 1}
            b = next(r for r, incidence in zip((5, 6), unary['root_incidence']) if incidence == 0)
            assert set(next(bb['actual_spokes'] for bb in structure['root_budgets'] if bb['root'] == b)) <= endpoints
            assert set(mixed['support']) <= endpoints and len(mixed['support']) <= 1
    no_mixed_three_spoke_applicable = 0
    if structure['m'] == 0:
        consecutive = {frozenset((i, (i + 1) % 5, (i + 2) % 5)) for i in B}
        for budget in structure['root_budgets']:
            if len(budget['actual_spokes']) == 3:
                no_mixed_three_spoke_applicable += 1
                assert frozenset(budget['actual_spokes']) not in consecutive
    data = dict(vertices=list(B + private), all_edges=[list(e) for e in edges],
                disk_rotation={str(v): rotation[v] for v in sorted(rotation)},
                private_roles=list(private), sigma_mask=value, Q=q,
                accepted_complete_colourings={str(i): list(patterns[i]) + list(rows[0])
                    for i, rows in enumerate(rel) if rows},
                structural_checks=structure, nonframe_edge_deletions=deletion_records,
                L1_maximal_proper_edge_subgraph_count=len(deletion_records),
                L1_all_proper_edge_subgraphs_covered=(1 << len(nonframe)) - 1,
                L1_coverage_argument='Every proper nonframe edge subset is contained in a checked G-e; Q(subgraph) is contained in Q(G-e). The L1 profile class is downward closed.',
                root_omissions=root_omissions, zw_omission_sigma=zw_row['sigma_mask'],
                L3_J2_actual_antecedent=l3_applicable,
                universal_spoke_redundancy_controls=spoke_redundancy,
                G2_G3_long_unary_actual_antecedent=g2_g3_long_unary_applicable,
                no_mixed_three_spoke_actual_antecedents=no_mixed_three_spoke_applicable,
                **relation_summary(rel))
    if include_relations:
        data['complete_same_frame_private_relations'] = [dict(
            row_index=i, literal_boundary=list(patterns[i]), private_roles=list(private),
            complete_tuples=[list(t) for t in row]) for i, row in enumerate(rel)]
        data['degree_valid_subgraphs'] = degree_valid_subgraphs(edges, patterns, private, singletons)
        data['local_refusal_checks'] = local_refusal_checks(edges, patterns, private, rel, structure)
    else:
        # The actual image is still independently solved above. Summaries bind
        # the complete relations without printing all tuples a second time.
        data['complete_edge_deletion_records_sha256'] = digest(deletion_records)
        data['nonframe_edge_deletions_columns'] = [
            'edge', 'sigma_mask', 'Q', 'newly_accepted_indices',
            'criticality_witnesses_as_pattern_and_complete_colouring']
        data['nonframe_edge_deletions'] = [
            [row['edge'], row['sigma_mask'], row['Q'], row['newly_accepted_indices'],
             [[w['pattern_index'], w['complete_colouring']] for w in row['criticality_witnesses']]]
            for row in deletion_records]
        valid = degree_valid_subgraphs(edges, patterns, private, singletons)
        data['degree_valid_subgraph_count'] = valid['degree_valid_count']
        data['degree_valid_subgraphs_sha256'] = digest(valid)
        pins = local_refusal_checks(edges, patterns, private, rel, structure)
        data['local_refusal_checks_sha256'] = digest(pins)
        data['local_refusal_pin_count'] = sum(p['refused_exterior_pin_count'] for p in pins)
    return data


def build(root):
    cell_path = 'artifacts/c5_cells/cells.json'
    source_paths = [f'artifacts/c5_excess_two_finite_search/AD_k{k}_validate/crit_orbits/orbit_{i:04d}.json'
                    for k, n in ((3, 1), (6, 2), (7, 1), (9, 5)) for i in range(1, n + 1)]
    discovered = sorted(str(p.relative_to(root)) for k in (3, 6, 7, 9) for p in
                        (root / f'artifacts/c5_excess_two_finite_search/AD_k{k}_validate/crit_orbits').glob('*.json'))
    assert discovered == sorted(source_paths), 'AD catalogue changed; review scope before replay'
    archive_path = 'artifacts/c5_excess_two_finite_search/positive_controls.json'
    raws = {p: (root / p).read_bytes() for p in source_paths + [cell_path, archive_path]}
    patterns = tuple(map(tuple, json.loads(raws[cell_path])['pattern_order']))
    singletons = {next(v for v in B if row.count(row[v]) == 1): i
                  for i, row in enumerate(patterns) if len(set(row)) == 3}
    assert singletons == {4: 0, 3: 1, 2: 3, 1: 4, 0: 6}
    source_controls = []
    for path in source_paths:
        saved = json.loads(raws[path]); edges = tuple(map(tuple, saved['canonical_edges']))
        private = tuple(range(5, max(v for e in edges for v in e) + 1))
        rotation = {int(v): ns for v, ns in saved['embedding']['disk_rotation'].items()}
        original = control(edges, rotation, patterns, singletons, private, saved, True)
        assert original['sigma_mask'] == saved['sigma_mask'] and original['Q'] == saved['Q']
        assert original['structural_checks']['m'] == saved['structure']['m']
        assert original['structural_checks']['unary'] == saved['structure']['unary']
        for old, new in zip(saved['structure']['components'], original['structural_checks']['pieces']):
            assert old['vertices'] == new['vertices'] and old['support'] == new['support']
            assert old['root_incidence'] == new['root_incidence'] and old['kind'] == new['kind']
        images = []
        for phi in D5:
            mapping = {v: phi[v] if v in B else v for v in B + private}
            image_edges = tuple(sorted(edge(mapping[u], mapping[v]) for u, v in edges))
            image_rotation = {mapping[v]: [mapping[w] for w in ns] for v, ns in rotation.items()}
            image = control(image_edges, image_rotation, patterns, singletons, private)
            # The shared literal colour frame is transported globally once.
            transported_rel = [set() for _ in patterns]
            for old_row in original['complete_same_frame_private_relations']:
                literal = [None] * 5
                for v in B:
                    literal[phi[v]] = old_row['literal_boundary'][v]
                names = {}; norm = []
                for c in literal:
                    names.setdefault(c, len(names)); norm.append(names[c])
                for c in range(4):
                    if c not in names:
                        names[c] = next(d for d in range(4) if d not in names.values())
                i = patterns.index(tuple(norm))
                transported_rel[i].update(tuple(names[c] for c in t) for t in old_row['complete_tuples'])
            transported_rel = tuple(tuple(sorted(row)) for row in transported_rel)
            assert relation_summary(transported_rel) == {k: image[k] for k in relation_summary(transported_rel)}
            images.append(dict(frame_D5_map=list(phi), globally_shared_colour_transport_verified=True,
                               actual_control=image))
        source_controls.append(dict(source_path=path, source_sha256=sha256(raws[path]).hexdigest(),
                                    source_graph_and_criticality_certificate=saved,
                                    independently_recomputed=original, all_D5_images=images))
    archive = json.loads(raws[archive_path])
    record_935 = next(r for r in archive['records'] if r['graph']['sigma_mask'] == 935)
    graph_935 = record_935['graph']
    assert sha256((json.dumps(graph_935, sort_keys=True, indent=2) + '\n').encode()).hexdigest() == record_935['record_sha256']
    exact_edges = tuple(map(tuple, graph_935['all_edges']))
    exact_private = tuple(v for v in graph_935['vertices'] if v not in B)
    exact_rotation = {int(v): ns for v, ns in graph_935['embedding']['disk_rotation'].items()}
    exact = control(exact_edges, exact_rotation, patterns, singletons, exact_private,
                    include_relations=True)
    assert exact['sigma_mask'] == 935 and exact['degree_valid_subgraphs']['degree_valid_count'] == 19
    target_edges = source_controls[0]['independently_recomputed']['all_edges']
    matching_maps = []
    for phi in D5:
        for swap in (False, True):
            mapping = {v: phi[v] if v in B else (11 - v if swap and v in (5, 6) else v)
                       for v in B + exact_private}
            if [list(e) for e in sorted(edge(mapping[u], mapping[v]) for u, v in exact_edges)] == target_edges:
                matching_maps.append(dict(frame_D5_map=list(phi), roots_swapped=swap,
                                          full_graph_map={str(v): mapping[v] for v in sorted(mapping)}))
    assert matching_maps and source_controls[0]['independently_recomputed']['sigma_mask'] == 942
    controls = [image['actual_control'] for record in source_controls for image in record['all_D5_images']]
    counts = dict(AD_crit_orbit_representatives=len(source_controls), whole_graph_D5_transports=len(controls),
                  maximal_proper_edge_deletions=sum(c['L1_maximal_proper_edge_subgraph_count'] for c in controls),
                  L1_proper_edge_subgraphs_covered=sum(c['L1_all_proper_edge_subgraphs_covered'] for c in controls),
                  degree_valid_subgraphs_checked=sum(c['degree_valid_subgraph_count'] for c in controls),
                  root_omissions_checked=sum(len(c['root_omissions']) for c in controls),
                  zw_omissions_checked=len(controls),
                  actual_piece_shields_checked=sum(len(c['structural_checks']['pieces']) for c in controls),
                  actual_refused_component_pins_checked=sum(c['local_refusal_pin_count'] for c in controls),
                  fullB_touch_two_rejections_applicable=sum(c['structural_checks']['full_B_touch_two_rejections_applicable'] for c in controls),
                  fullB_touch_measured=sum(c['structural_checks']['full_B_touch_measured'] for c in controls),
                  L3_J2_actual_antecedent=sum(c['L3_J2_actual_antecedent'] for c in controls),
                  N_empty_actual_antecedents=sum(c['structural_checks']['N_empty_antecedent_count'] for c in controls),
                  m_three_actual_antecedents=sum(c['structural_checks']['m_three_antecedent'] for c in controls),
                  universal_spoke_redundancy_checks=sum(len(c['universal_spoke_redundancy_controls']) for c in controls),
                  G2_G3_long_unary_actual_antecedents=sum(c['G2_G3_long_unary_actual_antecedent'] for c in controls),
                  no_mixed_three_spoke_actual_antecedents=sum(c['no_mixed_three_spoke_actual_antecedents'] for c in controls),
                  selected_triple_applicable=0, controls_excluded=0)
    assert counts['AD_crit_orbit_representatives'] == 9 and counts['whole_graph_D5_transports'] == 90
    return dict(schema='c5-excess-two-e6-all-ad-controls-v1', base=BASE,
                four_colour_oracle_used=False, workers_used=1, source_key_enumeration=False,
                evidence_boundary='Actual finite controls only. All D5 images are independently solved. No finite loop proves arbitrary-size topology, Gallai, or source classification.',
                singleton_to_pattern_index=singletons, pattern_order=patterns,
                source_sha256={p: sha256(raw).hexdigest() for p, raw in sorted(raws.items())},
                summary=counts, AD_controls=source_controls,
                original_935=dict(source_path=archive_path, pointer=record_935['source_pointer'],
                                  record_sha256=record_935['record_sha256'], original_graph=graph_935,
                                  independently_recomputed=exact, complete_named_matches_to_942=matching_maps),
                applicability_notes=dict(
                    N_empty='All actual mixed supports are nonempty; no empty-support antecedent occurs.',
                    adjacent_m_three='All controls have m=1; m>=3 and the four-path contradiction are vacuous on this corpus.',
                    N_theta='The nonadjacent-root antecedent is absent from AD controls.',
                    L2='J2 mixed12 without U, J3 binary, and J3 ternary original incidence antecedents are absent.',
                    L6_L7='A mixed12 plus one unary with four root spokes is absent.',
                    L8='B mixed22 without unary is absent.',
                    triple_critical='Selected three-row rejection antecedent is absent; each saved nonframe edge is nevertheless verified Sigma-critical.',
                    proper_subgraphs='No all-key source census. Degree-valid graphs are exact subsets of the nine named controls. L1 on arbitrary proper edge subsets uses checked maximal deletions and monotonicity.'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output', type=Path)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    output = args.output or args.root / 'artifacts/c5_excess_two_e6/controls.json'
    raw = canonical(build(args.root)) + b'\n'
    if args.check:
        assert output.read_bytes() == raw, 'byte replay mismatch'
        print(f'CHECK OK: {output.relative_to(args.root) if output.is_relative_to(args.root) else output}; {len(raw)} bytes; 9 AD orbits, 90 D5 images')
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open('xb') as stream:
            stream.write(raw)
        print(f'GENERATED: {output}; {len(raw)} bytes; 9 AD orbits, 90 D5 images')


if __name__ == '__main__':
    main()
