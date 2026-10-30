#!/usr/bin/env python3
"""Complete-O buffer controls on four fixed triangulated spheres.

No graph enumeration, truncation of the exterior, or assumption of a blocked
class. Canonical states represent full global S4 orbits; all original edges,
actual full-O components and complete joint fibres are retained.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

import networkx as nx

from c5_ab_swap_cube import ERRERA
from c5_blocked_transport_return import BOUNDARIES, INVERSE, STEPS
from ck_kempe_obstruction import patterns
from four_color_bond_perimeter_small_cuts import (
    capped_antiprism, original_faces, short_cycles,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'audits/2026-10-29-kempe-realizability/buffer/certificate.json'


def normalize(c):
    names = {}
    return tuple(names.setdefault(x, len(names)) for x in c)


def components(adj, allowed):
    unseen, answer = set(allowed), []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        todo = [root]
        for u in todo:
            for w in sorted(adj[u] & unseen):
                unseen.remove(w)
                todo.append(w)
        answer.append(tuple(sorted(todo)))
    return answer


def interface_order(graph, vertices):
    """Use the actual cycle when present; never call a general layer a ring."""
    layer = graph.subgraph(vertices)
    if len(vertices) >= 3 and nx.is_connected(layer) and all(d == 2 for _, d in layer.degree()):
        first = min(vertices)
        order = [first, min(layer[first])]
        while len(order) < len(vertices):
            order.append(next(v for v in layer[order[-1]] if v != order[-2]))
        assert layer.has_edge(order[-1], first) and len(set(order)) == len(vertices)
        return order, 'actual-induced-cycle'
    return sorted(vertices), 'general-distance-layer-not-assumed-cycle'


def colorings(adj):
    n, answer = len(adj), set()
    for boundary in patterns(5):
        c = list(boundary) + [-1] * (n - 5)
        def visit():
            todo = [v for v in range(n) if c[v] < 0]
            if not todo:
                answer.add(tuple(c))
                return
            avail = {v: set(range(4)) - {c[w] for w in adj[v]} for v in todo}
            v = min(todo, key=lambda v: (len(avail[v]), -len(adj[v]), v))
            for a in sorted(avail[v]):
                c[v] = a
                visit()
                c[v] = -1
        visit()
    assert all(normalize(c) == c for c in answer)
    return sorted(answer)


def labelled_colorings(adj):
    """Independent E enumeration: all literal colours, with no A restriction."""
    c, answer = [-1] * len(adj), []
    def visit():
        todo = [v for v in range(len(adj)) if c[v] < 0]
        if not todo:
            answer.append(tuple(c))
            return
        avail = {v: set(range(4)) - {c[w] for w in adj[v]} for v in todo}
        v = min(todo, key=lambda v: (len(avail[v]), -len(adj[v]), v))
        for a in sorted(avail[v]):
            c[v] = a
            visit()
            c[v] = -1
    visit()
    return sorted(answer)


def short_sides(graph, faces):
    owners = defaultdict(list)
    for j, face in enumerate(faces):
        for a, b in zip(face, face[1:] + face[:1]):
            owners[tuple(sorted((a, b)))].append(j)
    assert all(len(ids) == 2 for ids in owners.values())
    dual = nx.Graph()
    dual.add_nodes_from(range(len(faces)))
    dual.add_edges_from(owners.values())
    rows = []
    for cycle in short_cycles(graph):
        cut = dual.copy()
        for a, b in zip(cycle, cycle[1:] + cycle[:1]):
            cut.remove_edge(*owners[tuple(sorted((a, b)))])
        regions = sorted(map(sorted, nx.connected_components(cut)))
        assert len(regions) == 2
        sides = sorted(sorted(set().union(*(set(faces[j]) for j in ids)) - set(cycle))
                       for ids in regions)
        assert not set(sides[0]) & set(sides[1])
        assert set(sides[0]) | set(sides[1]) == set(graph) - set(cycle)
        rows.append(dict(cycle=cycle, sides=sides))
    return rows


def audit(name, graph, root=0):
    planar, embedding = nx.check_planarity(graph)
    assert planar and graph.degree[root] == 5 and min(dict(graph.degree).values()) >= 5
    embedding.check_structure()
    faces = original_faces(embedding)
    assert len(graph) - graph.number_of_edges() + len(faces) == 2
    boundary = list(embedding.neighbors_cw_order(root))
    assert all(graph.has_edge(boundary[i], boundary[(i + 1) % 5]) for i in range(5))
    exterior = graph.copy()
    exterior.remove_node(root)
    ids = boundary + sorted(set(exterior) - set(boundary))
    index = {v: i for i, v in enumerate(ids)}
    adj = [{index[w] for w in exterior[v]} for v in ids]
    original_edges = sorted(tuple(sorted(e)) for e in graph.edges())
    exterior_edges = sorted(tuple(sorted(e)) for e in exterior.edges())
    assert set(exterior_edges) | {tuple(sorted((root, v))) for v in boundary} == set(original_edges)
    assert len(exterior) == len(graph) - 1
    states = colorings(adj)
    lookup = {c: j for j, c in enumerate(states)}
    moves, neighbors = [], [set() for _ in states]
    for j, c in enumerate(states):
        for pair in combinations(range(4), 2):
            for comp in components(adj, {v for v, a in enumerate(c) if a in pair}):
                target = normalize(tuple(sum(pair) - a if v in comp else a
                                         for v, a in enumerate(c)))
                k = lookup[target]
                moves.append(dict(source=j, pair=pair, vertices=[ids[v] for v in comp], target=k))
                neighbors[j].add(k)
    unseen, classes = set(range(len(states))), []
    while unseen:
        first = min(unseen)
        unseen.remove(first)
        todo = [first]
        for j in todo:
            for k in sorted(neighbors[j] & unseen):
                unseen.remove(k)
                todo.append(k)
        classes.append(dict(states=sorted(todo),
                            three_colour_boundary_states=[j for j in sorted(todo)
                                                          if len(set(states[j][:5])) == 3]))
    assert all(row['three_colour_boundary_states'] for row in classes)
    distance = nx.single_source_shortest_path_length(graph, root)
    layers = {d: sorted(v for v in exterior if distance[v] == d) for d in range(1, max(distance.values()) + 1)}
    buffers = []
    for extra_rings in (1, 2):
        depth = extra_rings + 1
        outer, outer_shape = interface_order(exterior, layers.get(depth, []))
        kept = sorted(v for v in exterior if distance[v] <= depth)
        remote = sorted(set(exterior) - set(kept))
        joint_order = boundary + outer
        # R_A is computed independently, before any remote extension filter.
        a_order = boundary + sorted(set(kept) - set(boundary))
        a_index = {v: i for i, v in enumerate(a_order)}
        a_adj = [{a_index[w] for w in exterior[v] if w in a_index} for v in a_order]
        a_states = colorings(a_adj)
        a_lookup = {c: j for j, c in enumerate(a_states)}
        private = sorted(set(kept) - set(joint_order))
        local_joint = defaultdict(list)
        for j, c in enumerate(a_states):
            local_joint[tuple(c[a_index[v]] for v in joint_order)].append(j)
        # E keeps C=outer in common with A; all A--remote edges end at C.
        assert all(u in outer for u in kept for v in exterior[u] if v in remote)
        e_order = outer + remote
        e_index = {v: i for i, v in enumerate(e_order)}
        e_adj = [{e_index[w] for w in exterior[v] if w in e_index} for v in e_order]
        e_states = labelled_colorings(e_adj)
        e_fibres = defaultdict(list)
        for c in e_states:
            e_fibres[c[:len(outer)]].append(c[len(outer):])
        lifted = set()
        for ac in a_states:
            for remote_assignment in e_fibres.get(tuple(ac[a_index[v]] for v in outer), []):
                assignment = {v: ac[a_index[v]] for v in kept}
                assignment.update(zip(remote, remote_assignment))
                lifted.add(tuple(assignment[v] for v in ids))
        assert lifted == set(states), 'Independent complete A/E fibre join differs from full O'
        extendable_a = sorted({a_lookup[tuple(c[index[v]] for v in a_order)] for c in states})
        joint = defaultdict(list)
        kept_projection = defaultdict(list)
        for j, c in enumerate(states):
            joint[tuple(c[index[v]] for v in joint_order)].append(j)
            kept_projection[tuple(c[index[v]] for v in kept)].append(j)
        assert sorted(j for fibre in joint.values() for j in fibre) == list(range(len(states)))
        assert sorted(j for fibre in kept_projection.values() for j in fibre) == list(range(len(states)))
        reconnect, gluing = [], []
        kept_indices = {index[v] for v in kept}
        remote_indices = {index[v] for v in remote}
        for j, c in enumerate(states):
            for pair in combinations(range(4), 2):
                active = {v for v, a in enumerate(c) if a in pair}
                local = components(adj, active & kept_indices)
                full = components(adj, active)
                remote_components = components(adj, active & remote_indices)
                augmented = [set() for _ in range(len(ids) + len(remote_components))]
                for u in active & kept_indices:
                    augmented[u] = adj[u] & active & kept_indices
                stars = []
                for q, comp in enumerate(remote_components):
                    attachments = set().union(*(adj[v] for v in comp)) & active & kept_indices
                    aux = len(ids) + q
                    augmented[aux] = attachments
                    for u in attachments:
                        augmented[u].add(aux)
                    stars.append(dict(remote_component=[ids[v] for v in comp],
                                      actual_buffer_attachments=[ids[v] for v in sorted(attachments)]))
                aux_active = (active & kept_indices) | set(range(len(ids), len(augmented)))
                actual_projection = sorted(tuple(sorted(set(comp) & kept_indices)) for comp in full
                                           if set(comp) & kept_indices)
                composed_projection = sorted(tuple(sorted(set(comp) & kept_indices))
                                             for comp in components(augmented, aux_active)
                                             if set(comp) & kept_indices)
                assert composed_projection == actual_projection
                gluing.append(dict(state=j, pair=pair, remote_stars=stars,
                                   exact_full_component_intersections=[[ids[v] for v in p]
                                                                       for p in actual_projection]))
                for comp in full:
                    pieces = [p for p in local if set(p) <= set(comp)]
                    if len(pieces) >= 2:
                        reconnect.append(dict(state=j, pair=pair,
                            full_component=[ids[v] for v in comp],
                            buffer_pieces=[[ids[v] for v in p] for p in pieces],
                            remote_vertices=sorted(set(ids[v] for v in comp) & set(remote))))
        buffers.append(dict(extra_rings=extra_rings, depth=depth,
            inner_boundary_B0=boundary, outer_interface=outer, outer_interface_shape=outer_shape,
            kept_vertices=kept, remote_vertices=remote,
            joint_order=joint_order,
            local_A=dict(vertex_order=a_order,
                original_edges=sorted(tuple(sorted(e)) for e in exterior.subgraph(kept).edges()),
                canonical_full_A_states=a_states, private_vertex_order=private,
                complete_joint_fibres=[dict(row=k, full_A_state_ids=v,
                    all_private_assignments=[tuple(a_states[j][a_index[x]] for x in private) for j in v])
                    for k, v in sorted(local_joint.items())],
                closed_world='Domain: every proper literal B0/outer assignment. Canonicalize by one common S4 permutation beginning with B0; unlisted canonical rows have empty fibres. Apply the inverse common permutation to every private A assignment. All illegal interface assignments also have empty fibres.',
                E_extendable_A_state_ids=extendable_a,
                A_states_without_E_extension=sorted(set(range(len(a_states))) - set(extendable_a))),
            remote_E=dict(vertex_order=e_order, outer_interface=outer, private_vertex_order=remote,
                original_edges=sorted(tuple(sorted(e)) for e in exterior.subgraph(e_order).edges()),
                complete_literal_interface_fibres=[dict(row=k, all_remote_assignments=v)
                                                  for k, v in sorted(e_fibres.items())],
                closed_world='All 4^|outer| literal assignments are the query domain; unlisted rows have empty fibres, including improper interface rows.'),
            independent_A_E_join_equals_full_O=True,
            complete_joint_fibres=[dict(row=k, full_state_ids=v) for k, v in sorted(joint.items())],
            complete_buffer_fibres=[dict(row=k, full_state_ids=v) for k, v in sorted(kept_projection.items())],
            global_projection_closed_world='These two tables contain only E-extendable rows of full O. Their unlisted canonical rows are empty in the full-O projection; they are not the standalone local relation R_A above.',
            complete_remote_component_gluing=gluing,
            actual_remote_reconnections=reconnect))
    transfers = []
    for j, start in enumerate(states):
        if start[:5] != BOUNDARIES[0]:
            continue
        c, route = start, []
        for t, (pair, selected_root) in enumerate(STEPS):
            comp = next(p for p in components(adj, {v for v, a in enumerate(c) if a in pair})
                        if selected_root in p)
            changed = tuple(sum(pair) - a if v in comp else a for v, a in enumerate(c))
            if changed[:5] != BOUNDARIES[t + 1]:
                break
            assert set(comp) & set(range(5)) == {selected_root}
            route.append(dict(pair=pair, root=ids[selected_root], vertices=[ids[v] for v in comp],
                              before=c, after=changed))
            c = changed
        else:
            final = tuple(INVERSE[a] for a in c)
            k = lookup[final]
            assert final[:5] == start[:5] and final != start
            transfers.append(dict(source=j, target=k, steps=route,
                normalized_return=final,
                changed_original_vertices=[ids[v] for v, (a, b) in enumerate(zip(start, final)) if a != b],
                changed_by_layer={d: [v for v in vs if start[index[v]] != final[index[v]]] for d, vs in layers.items()}))
    h = {row['source']: row['target'] for row in transfers}
    cycles, covered = [], set()
    for j in sorted(h):
        if j in covered:
            continue
        todo, position, k = [], {}, j
        while k in h and k not in position:
            position[k] = len(todo)
            todo.append(k)
            k = h[k]
        if k == j:
            cycles.append(todo)
            covered.update(todo)
    sides = short_sides(graph, faces)
    bad34 = [row for row in sides if len(row['cycle']) <= 4 and min(map(len, row['sides'])) > 0]
    bad5 = [row for row in sides if len(row['cycle']) == 5 and min(map(len, row['sides'])) > 1]
    assert not bad34
    return dict(name=name, original_root=root, original_vertices=sorted(graph), original_edges=original_edges,
        rotation={v: list(embedding.neighbors_cw_order(v)) for v in sorted(graph)}, sphere_faces=faces,
        original_degrees=dict(sorted(graph.degree())), original_short_cycle_sides=sides,
        satisfies_S34=True, satisfies_S5=not bad5, separating_five_cycle_violations=bad5,
        ordered_boundary_B0=boundary, full_exterior_vertex_order=ids, full_exterior_edges=exterior_edges,
        layers=layers, canonical_full_exterior_states=states, all_actual_component_moves=moves,
        complete_kempe_classes=classes, buffers=buffers, valid_five_transfers=transfers, normalized_return_cycles=cycles)


def report():
    errera = nx.Graph((u, v) for u, vs in ERRERA.items() for v in vs)
    cases = [audit('icosahedron', nx.icosahedral_graph()),
             audit('capped-antiprism-6', capped_antiprism(6)),
             audit('capped-antiprism-7', capped_antiprism(7)),
             audit('Errera-v0', errera)]
    e = cases[-1]
    assert len(e['canonical_full_exterior_states']) == 100
    assert sorted(map(len, e['normalized_return_cycles'])) == [4]
    assert all(row['changed_by_layer'][2] for row in e['valid_five_transfers'])
    assert all(b['actual_remote_reconnections'] for b in e['buffers'])
    assert all(c['satisfies_S5'] for c in cases[:-1]) and not e['satisfies_S5']
    files = [Path(__file__), ROOT / 'scripts/c5_ab_swap_cube.py',
             ROOT / 'scripts/c5_blocked_transport_return.py', ROOT / 'scripts/ck_kempe_obstruction.py',
             ROOT / 'scripts/four_color_bond_perimeter_small_cuts.py']
    return dict(schema='complete-O-one-two-ring-buffer-v1',
        trust='Finite exact states/fibres and original-embedding checks. No 4CT, no graph census, no blocked class is assumed. Not Lean.',
        hashes={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in files},
        colour_quotient='Only one global S4 permutation: canonical full states begin with B0. Saturate each whole state by the 24 permutations to recover all labelled colourings. Component moves are computed in all of O.',
        fibre_contract='Each fibre lists every full canonical O state with the given joint row, including distinct buffer interiors and all remote assignments; full state arrays and original edges are saved.',
        cases=cases,
        exclusion_scope='Errera refutes boundary-restoration=>one/two-buffer-restoration and buffer-components-are-self-contained in the delta5/S34 sphere class. Errera violates S5 and has a three-colour state in its sole full Kempe class. It is not a blocked-class counterexample or a counterexample for the stronger S5 research class.',
        open='No new blocked component has been realized. No conclusion about all allowed I or the existence of buffer-invariant returns on S5 sources.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = report()
    encoded = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == encoded, 'Certificate differs; inspect before regeneration'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        with OUT.open('x') as target:
            target.write(encoded)
    print(json.dumps(dict(check='OK', cases=[dict(name=c['name'],
        full_states=len(c['canonical_full_exterior_states']), classes=len(c['complete_kempe_classes']),
        local_A_states=[len(b['local_A']['canonical_full_A_states']) for b in c['buffers']],
        local_A_without_E=[len(b['local_A']['A_states_without_E_extension']) for b in c['buffers']],
        valid_five_transfers=len(c['valid_five_transfers']), return_periods=list(map(len, c['normalized_return_cycles'])),
        remote_reconnections=[len(b['actual_remote_reconnections']) for b in c['buffers']],
        S5=c['satisfies_S5']) for c in result['cases']]), sort_keys=True))


if __name__ == '__main__':
    main()
