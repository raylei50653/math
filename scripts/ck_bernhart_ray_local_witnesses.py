#!/usr/bin/env python3
"""Exact local plane controls for Bernhart's two selected full-lift rays.

A control realizes one ray-supported complete Tait state and its actual cuts.
Its full counting vector is NOT asserted proportional to either ray. An actual
successor outside a ray rejects this control as a realization, not all sources.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from functools import cmp_to_key
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import ck_bernhart_benchmark as benchmark
import c5_dual_path_surgery as surgery
import ck_retained_intersection_parity as parity
from four_color_counts_cone_verification import compatible, integrate

SOURCE = ROOT / 'audits/2026-10-29-bernhart-cross-split-e1a90fe/verification.json'
DEFAULT = ROOT / 'audits/2026-10-29-bernhart-retained-parity/ray-local.json'
PAIRS = ((1, 2), (1, 3), (2, 3))
F = 14
ATTACHMENTS = (0, 2, 4, 5, 7, 10, 11, 13)


def name(v):
    return f'v{v}' if v < F else f'e{v-F}'


def orient(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])


def graph(shift):
    edges = [(i, (i+1) % F) for i in range(F)] + [(3, 6), (1, 8), (9, 12)]
    edges += [(v, F+(i+shift) % 8) for i, v in enumerate(ATTACHMENTS)]
    labels = [2 if i % 2 == 0 else 3 for i in range(F)] + [1]*11
    points = {i: (14*i-91, 14*i*i-819) for i in range(F)}
    for i, v in enumerate(ATTACHMENTS):
        points[F+(i+shift) % 8] = tuple(100*x for x in points[v])
    outer = [(F+i, F+(i+1) % 8) for i in range(8)]
    all_edges = edges + outer
    # Exact straight-line disk embedding, including the terminal boundary.
    for u, v in outer:
        assert all(orient(points[u], points[v], points[w]) > 0 for w in range(F))
    for i, (a, b) in enumerate(all_edges):
        for c, d in all_edges[i+1:]:
            if len({a, b, c, d}) < 4:
                continue
            x = [orient(points[a], points[b], points[v]) for v in (c, d)]
            y = [orient(points[c], points[d], points[v]) for v in (a, b)]
            separated = x[0]*x[1] > 0 or y[0]*y[1] > 0
            if not separated and x == [0, 0] and y == [0, 0]:
                separated = any(max(points[a][j], points[b][j]) < min(points[c][j], points[d][j])
                                or max(points[c][j], points[d][j]) < min(points[a][j], points[b][j])
                                for j in range(2))
            assert separated
    adjacency = defaultdict(list)
    for u, v in all_edges:
        adjacency[u].append(v); adjacency[v].append(u)
    def order_at(v):
        def compare(a, b):
            ax, ay = (points[a][j]-points[v][j] for j in range(2))
            bx, by = (points[b][j]-points[v][j] for j in range(2))
            ha, hb = int(ay < 0 or ay == 0 and ax < 0), int(by < 0 or by == 0 and bx < 0)
            if ha != hb:
                return ha-hb
            z = ax*by-ay*bx
            assert z != 0
            return -1 if z > 0 else 1
        return sorted(adjacency[v], key=cmp_to_key(compare))
    rotation = {v: order_at(v) for v in adjacency}
    pending = {(u, v) for a, b in all_edges for u, v in ((a, b), (b, a))}
    faces = []
    while pending:
        root = min(pending); dart = root; face = []
        while True:
            assert dart in pending
            pending.remove(dart); u, v = dart; face.append(u)
            order = rotation[v]; dart = (v, order[(order.index(u)-1) % len(order)])
            if dart == root:
                break
        faces.append(face)
    assert len(points)-len(all_edges)+len(faces) == 2
    assert any(len(face) == 8 and set(face) == set(range(F, F+8)) for face in faces)
    for v in range(F):
        assert sorted(labels[e] for e, uv in enumerate(edges) if v in uv) == [1, 2, 3]
    assert all(sum(v in uv for uv in edges) == 1 for v in range(F, F+8))
    return edges, labels, dict(
        construction='A fourteen-cycle with three interior noncrossing color-1 chords; leaves on its exterior.',
        vertices=[name(v) for v in range(F+8)],
        edges=[dict(index=e, ends=[name(v) for v in uv], color=labels[e]) for e, uv in enumerate(edges)],
        integer_positions={name(v): xy for v, xy in sorted(points.items())},
        terminal_order=[f'e{i}' for i in range(8)],
        boundary_closure_edges=[[name(v) for v in uv] for uv in outer],
        closure_counterclockwise_rotations={name(v): [name(w) for w in ws] for v, ws in sorted(rotation.items())},
        closure_oriented_sphere_faces=[[name(v) for v in face] for face in faces],
        exact_disk_geometry_checked=True)


def observe(edges, labels, signature_index):
    signatures, cycles = [], []
    for pair in PAIRS:
        parts = surgery.pair_strands(edges, labels, pair)
        sig = tuple(sorted((p['ends'][0]-F, p['ends'][1]-F,
                            -1 if len(p['edges']) % 2 else 1)
                           for p in parts if p['ends']))
        signatures.append(signature_index[sig]); cycles.append(sum(not p['ends'] for p in parts))
    word = tuple(labels[next(e for e, uv in enumerate(edges) if F+i in uv)] for i in range(8))
    return dict(word=word, signatures=signatures, cycles=cycles)


def common_sides(ends, ports, retained):
    start, end = ends
    arcs = [list(reversed(range(start+1, end))), list(range(end+1, 8))+list(range(start))]
    feasible, rejected = [], []
    for bits in product((0, 1), repeat=len(ports)):
        sides = {f't{i}': b for i, b in enumerate(bits)}
        for side, arc in enumerate(arcs):
            sides.update({f'e{i}': side for i in arc})
        orders = [[f't{i}' for i, b in enumerate(bits) if b == side] + [f'e{i}' for i in arc]
                  for side, arc in enumerate(arcs)]
        witness = None
        for system, row in enumerate(retained):
            for p in row['paths']:
                u, v = p['ends']
                if sides[u] != sides[v]:
                    witness = dict(kind='opposite_sides', system=system, ends=[u, v]); break
            if witness:
                break
            for side, order in enumerate(orders):
                pairs = [tuple(sorted(order.index(v) for v in p['ends'])) for p in row['paths']
                         if sides[p['ends'][0]] == side]
                for (a, b), (c, d) in combinations(pairs, 2):
                    if a < c < b < d or c < a < d < b:
                        witness = dict(kind='interleaving', system=system, side=side, pairs=[[a, b], [c, d]])
                        break
                if witness:
                    break
            if witness:
                break
        if witness:
            rejected.append(dict(bits=bits, witness=witness))
        else:
            feasible.append(dict(bits=bits, side_orders=orders))
    assert feasible
    return dict(boundary_arcs=arcs, feasible=feasible, rejected=rejected, tested=2**len(ports))


def action(edges, labels, path, sig_index, sigs, ray_y):
    pair = (1, 2); removed = set(path['edges'])
    ports = path['vertices'][1:-1]
    assert len(set(ports)) == len(ports)
    names = {v: f't{i}' for i, v in enumerate(ports)}
    names.update({F+i: f'e{i}' for i in range(8)})
    retained, glue_observations = [], []
    for old, new in ((1, 2), (2, 1)):
        parts = surgery.pair_strands(edges, labels, (old, 3), removed)
        paths = [dict(ends=[names[v] for v in p['ends']],
                      original_vertices=[name(v) for v in p['vertices']], original_edges=p['edges'])
                 for p in parts if p['ends']]
        loops = [dict(original_vertices=[name(v) for v in p['vertices']], original_edges=p['edges'])
                 for p in parts if not p['ends']]
        local = {color: [dict(ends=[names[v] for v in edges[e]], original_edge=e)
                         for e in path['edges'] if labels[e] == color] for color in pair}
        row = dict(pair=[old, 3], paths=paths, untouched_cycles=loops,
                   old_local_links=local[old], new_local_links=local[new])
        retained.append(row)
        def glue(color):
            links = [p['ends'] for p in paths] + [q['ends'] for q in local[color]]
            lengths = [len(p['original_edges']) for p in paths] + [1]*len(local[color])
            glued = surgery.strands(links)
            signature = tuple(sorted((int(p['ends'][0][1:]), int(p['ends'][1][1:]),
                                      -1 if sum(lengths[e] for e in p['edges']) % 2 else 1)
                                     for p in glued if p['ends']))
            return sig_index[signature], len(loops)+sum(not p['ends'] for p in glued)
        glue_observations.append((old, glue(old), glue(new)))
    third_edges = []
    for i, v in enumerate(ports):
        ee = [e for e, uv in enumerate(edges) if v in uv and e not in removed]
        assert len(ee) == 1 and labels[ee[0]] == 3
        e = ee[0]
        third_edges.append(dict(port=f't{i}', vertex=name(v), original_edge=e,
                                edge_ends=[name(w) for w in edges[e]]))
    # A common third edge whose two endpoints are cut ports occurs verbatim in BOTH retained systems.
    for e in {p['original_edge'] for p in third_edges}:
        uv = edges[e]
        if all(v in ports for v in uv):
            expected = {names[v] for v in uv}
            assert all(any(set(p['ends']) == expected and p['original_edges'] == [e] for p in row['paths'])
                       for row in retained)
    changed = labels.copy()
    for e in removed:
        changed[e] = 3-changed[e]
    before = observe(edges, labels, sig_index); after = observe(edges, changed, sig_index)
    for old, previous, prediction in glue_observations:
        j = PAIRS.index((old, 3))
        assert previous == (before['signatures'][j], before['cycles'][j])
        assert prediction == (after['signatures'][j], after['cycles'][j])
    allowed = [[s for s in sorted(ray_y) if compatible(after['word'], cp, sigs[s])] for cp in PAIRS]
    rejected = [dict(pair=cp, actual_signature=after['signatures'][j], allowed_signatures=allowed[j])
                for j, cp in enumerate(PAIRS) if after['signatures'][j] not in allowed[j]]
    return dict(pair=pair, source_path=dict(ends=[v-F for v in path['ends']],
                original_vertices=[name(v) for v in path['vertices']], original_edges=path['edges']),
                ordered_ports=[dict(port=f't{i}', vertex=name(v)) for i, v in enumerate(ports)],
                common_third_color_edges=third_edges, retained=retained,
                common_cut_sides=common_sides([v-F for v in path['ends']], ports, retained),
                successor=after, successor_original_edge_colors=changed,
                ray_allowed_successor_signatures=allowed,
                successor_in_ray_signature_support=not rejected,
                forbidden_successor_systems=rejected,
                exact_ordered_gluing_checked=True)


def report():
    receipt = SOURCE.parent / 'RECEIPT.json'
    assert sha256(SOURCE.read_bytes()).hexdigest() == json.loads(receipt.read_text())['sources_sha256'][str(SOURCE.relative_to(ROOT))]
    saved = json.loads(SOURCE.read_text())
    words, sigs, states, rows, columns = benchmark.cone_data()
    sig_index = {s: i for i, s in enumerate(sigs)}
    results = []
    for ray_index, shift in ((0, 4), (1, 0)):
        ray = saved['exact_nonextremality']['parts'][ray_index]
        ray_y = {r['index']: r['weight'] for r in ray['signature_weights']}
        ray_n = {r['index']: r['count'] for r in ray['pattern_counts']}
        actual = [0]*len(rows)
        for s, value in ray_y.items():
            assert value == 1
            for r in columns[s]:
                actual[r] += value
        assert all(actual[r] == ray_n.get(states[wi], 0) for r, (wi, _) in enumerate(rows))
        assert ray_y[0] == ray_n[0] == 1
        assert sum(ray_n.get(states[wi], 0) for wi in range(len(words))) == 261
        edges, labels, drawing = graph(shift)
        by_name = {name(v): v for v in range(F+8)}
        rotations = {v: [e for z in drawing['closure_counterclockwise_rotations'][name(v)]
                         for e, uv in enumerate(edges) if set(uv) == {v, by_name[z]}]
                     for v in range(F+8)}
        drawing['original_edge_id_rotations'] = {name(v): rr for v, rr in rotations.items()}
        drawing['numeric_vertex_names'] = {str(v): name(v) for v in range(F+8)}
        assert parity.ribbon_faces(edges, rotations)['genus'] == 0
        obs = observe(edges, labels, sig_index)
        assert obs['word'] == (1,)*8
        assert all(s in ray_y for s in obs['signatures'])
        paths = surgery.pair_strands(edges, labels, (1, 2))
        selected = [{(0+shift) % 8, (7+shift) % 8}, {(1+shift) % 8, (4+shift) % 8}]
        actions = [action(edges, labels, p, sig_index, sigs, ray_y) for ends in selected for p in paths
                   if {v-F for v in p['ends']} == ends]
        selected_paths = [p for ends in selected for p in paths if {v-F for v in p['ends']} == ends]
        for row, path in zip(actions, selected_paths):
            row['retained_intersection_parity'] = parity.cut_action(edges, labels, rotations, F, 8, (1, 2), path)
        cut = actions[0]['retained_intersection_parity']
        target = next(q for q in cut['parity_checks'] if q.get('shared_edges') == [3, 5] and q['status'] == 'checked')
        first = cut['retained'][0]['components'][target['first_component']]
        second = cut['retained'][1]['components'][target['second_component']]
        order = next(rr for rr in cut['cut_side_vertex_orders'] if set(first['ends']+second['ends']) <= set(rr))
        assert 3 not in selected_paths[0]['vertices']
        changed_rotations = {v: rr.copy() for v, rr in rotations.items()}
        changed_rotations[3].reverse()
        bad = parity.intersection_parity(edges, labels, changed_rotations, first, second, 1, 2, 3, order)
        assert target['passed'] and not bad['passed']
        negative = dict(changed_vertex='v3', original_rotation=rotations[3], changed_rotation=changed_rotations[3],
                        retained_component_indices=[target['first_component'], target['second_component']],
                        positive=target, negative=bad,
                        changed_ribbon_topology=parity.ribbon_faces(edges, changed_rotations),
                        graph_colors_paths_third_edges_retained_wirings_and_cut_sides_unchanged=True,
                        limitation='Rejects this fixed original-rotation extension; the underlying graph has the valid plane rotation already given.')
        assert len(actions) == 2
        assert actions[0]['successor_in_ray_signature_support']
        assert not actions[1]['successor_in_ray_signature_support']
        used = set(obs['signatures'])
        for row in actions:
            used.update(row['successor']['signatures'])
            used.update(s for ss in row['ray_allowed_successor_signatures'] for s in ss)
        results.append(dict(ray=ray_index+1, ray_rows=len(ray['pattern_counts']),
                            source=drawing, initial=obs, actions=actions,
                            primitive_lift=dict(full_incidence_equations_checked=len(rows),
                                                positive_y=len(ray_y), all_positive_y_equal_one=True,
                                                monochrome_count=1, empty_signature_weight=1,
                                                literal_word_mass=261,
                                                positive_scale_for_actual_counts='An integer, because the monochrome count equals the scale.'),
                            offcut_rotation_negative_control=negative,
                            signature_dictionary={str(s): sigs[s] for s in sorted(used)},
                            full_count_ray_realization=False,
                            limitation='A plane local state and selected cuts only. A forbidden actual successor rejects this control; it does not quantify over other sources or positive scales.'))
    deps = [Path(__file__), SOURCE, receipt, ROOT/'scripts/ck_bernhart_benchmark.py',
            ROOT/'scripts/c5_dual_path_surgery.py', ROOT/'scripts/four_color_counts_cone_verification.py',
            ROOT/'scripts/ck_retained_intersection_parity.py', ROOT/'scripts/ck_kempe_obstruction.py',
            ROOT/'scripts/c5_kempe_connectivity.py', parity.CONFIG]
    return dict(scope='Two explicit connected plane local Tait witnesses; neither realizes its target full-lift ray.',
                rays=results,
                local_necessary_condition='For every actual selected path, glue the two complete retained systems to the swapped local edges. Every resulting signed signature must be positive in the same source lift. Both systems retain each common third edge with its original identity.',
                excluded_positive_scale_rays=[], excluded_coordinates=[],
                source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in deps})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    result = report()
    payload = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2)+'\n'
    if args.check:
        assert args.check.read_text() == payload, 'Local witness certificate differs'
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload)
    print(json.dumps(dict(rays=len(result['rays']), actual_actions=sum(len(r['actions']) for r in result['rays']),
                          excluded_positive_scale_rays=[], excluded_coordinates=[]), sort_keys=True))


if __name__ == '__main__':
    main()
