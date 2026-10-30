#!/usr/bin/env python3
"""Replay the marked K4-minus-edge insertion on a complete non-target control.

The general insertion preserves the full six-leaf lift with multiplier two
and gives an outer marked edge in no two-edge cut.  This finite control does
not realize the target lift, so it is not an unconditional target counterexample.
All arithmetic and graph checks use the Python standard library.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

from ck_bernhart_marked_separation import (
    CONTROL, PAIRS, SOURCE, complete_colorings, components, observation,
)
from four_color_counts_cone_verification import compatible, signatures

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / 'audits/2026-10-30-bernhart-marked-bond-obstruction/verification.json'


def faces(edges, rotations):
    """Walk the actual original-edge darts, using the fixed cyclic rotations."""
    for v, row in rotations.items():
        assert sorted(row) == [e for e, uv in enumerate(edges) if v in uv]
    pending = {(e, v) for e, uv in enumerate(edges) for v in uv}
    result = []
    while pending:
        root = min(pending)
        dart, face = root, []
        while True:
            assert dart in pending
            pending.remove(dart)
            e, v = dart
            face.append([v, e])
            a, b = edges[e]
            w = a if b == v else b
            row = rotations[w]
            dart = row[(row.index(e) - 1) % len(row)], w
            if dart == root:
                break
        result.append(face)
    assert len(rotations) - len(edges) + len(result) == 2
    return result


def outer_face(edges, rotations, leaves, marked):
    ff = faces(edges, rotations)
    outer = [f for f in ff if set(leaves) <= {v for v, _ in f}]
    assert len(outer) == 1
    outer = outer[0]
    assert marked in {e for _, e in outer}
    order = [v for v, _ in outer if v in leaves]
    start = order.index(leaves[0])
    assert order[start:] + order[:start] == leaves
    return ff, outer


def insert_diamond(fixture):
    old = fixture['edges']
    f = fixture['marked_edge']
    u, v = old[f]
    p, q, r, s = range(1 + max(sum(old, [])), 5 + max(sum(old, [])))
    keep = [e for e in range(len(old)) if e != f]
    edge_map = {e: i for i, e in enumerate(keep)}
    edges = [old[e] for e in keep]
    base = len(edges)
    up, qv, pr, ps, qr, qs, rs = range(base, base + 7)
    edges += [[u, p], [q, v], [p, r], [p, s], [q, r], [q, s], [r, s]]
    rotations = {}
    for vertex, row in fixture['rotations'].items():
        vertex = int(vertex)
        rotations[vertex] = [edge_map[e] if e != f else up if vertex == u else qv
                             for e in row]
    local = {p: [up, ps, pr], q: [qv, qr, qs],
             r: [pr, rs, qr], s: [qs, rs, ps]}
    # Both reflected local disks preserve all old rotation slots.  Select the
    # one whose p-r-q arc lies on the same outer face as the old marked edge.
    for reflected in (False, True):
        trial = rotations | {z: row[::-1] if reflected else row for z, row in local.items()}
        try:
            ff, outer = outer_face(edges, trial, fixture['boundary_order'], pr)
        except AssertionError:
            continue
        assert all(len(row) == (1 if z in fixture['boundary_order'] else 3)
                   for z, row in trial.items())
        return dict(edges=edges, rotations=trial, marked_edge=pr,
                    boundary_order=fixture['boundary_order'],
                    original_edge_map=edge_map, source_endpoints=[u, v],
                    gadget_vertices=dict(p=p, q=q, r=r, s=s),
                    gadget_edges=dict(up=up, qv=qv, pr=pr, ps=ps, qr=qr, qs=qs, rs=rs),
                    reflected=reflected, sphere_faces=ff, outer_face=outer)
    raise AssertionError('Neither mirrored local insertion preserves the marked outer face')


def vertex_components(edges, removed=()):
    vertices = set(sum(edges, []))
    adjacency = defaultdict(list)
    for e, (u, v) in enumerate(edges):
        if e not in removed:
            adjacency[u].append(v)
            adjacency[v].append(u)
    result = []
    while vertices:
        seen, todo = {min(vertices)}, [min(vertices)]
        for v in todo:
            for w in adjacency[v]:
                if w not in seen:
                    seen.add(w)
                    todo.append(w)
        vertices -= seen
        result.append(sorted(seen))
    return result


def all_vertices_connected(edges, removed=()):
    return len(vertex_components(edges, removed)) == 1


def source_path(edges, u, v, removed):
    adjacency = defaultdict(list)
    for e, (a, b) in enumerate(edges):
        if e != removed:
            adjacency[a].append((b, e))
            adjacency[b].append((a, e))
    parents = {u: None}
    todo = deque([u])
    while todo and v not in parents:
        a = todo.popleft()
        for b, e in adjacency[a]:
            if b not in parents:
                parents[b] = (a, e)
                todo.append(b)
    assert v in parents
    path, w = [], v
    while w != u:
        previous, e = parents[w]
        path.append(e)
        w = previous
    return path[::-1]


def verify_paths(edges, paths, a, b):
    sets = [set(path) for path in paths]
    assert all(not x.intersection(y) for i, x in enumerate(sets) for y in sets[i + 1:])
    for path in paths:
        v, vertices = a, [a]
        for e in path:
            assert v in edges[e]
            u, w = edges[e]
            v = u if v == w else w
            vertices.append(v)
        assert v == b and len(set(vertices)) == len(vertices)


def local_extensions():
    # Vertices 0 and 1 are terminal leaves; p,q,r,s are 2,3,4,5.
    edges = [(0, 2), (3, 1), (2, 4), (2, 5), (3, 4), (3, 5), (4, 5)]
    full = complete_colorings(edges)
    assert len(full) == 6
    by_terminal = defaultdict(list)
    for phi in full:
        x, y, z = phi[0], phi[2], phi[3]
        assert set((x, y, z)) == {1, 2, 3}
        assert phi == (x, x, y, z, z, y, x)
        by_terminal[x].append(phi)
    assert set(by_terminal) == {1, 2, 3}
    assert {len(row) for row in by_terminal.values()} == {2}
    return dict(edge_names=['up', 'qv', 'pr', 'ps', 'qr', 'qs', 'rs'],
                edges=edges, full_extensions=full,
                extensions_by_terminal_color=by_terminal, extension_multiplier=2)


def lift_tables(edges, colorings, leaves):
    n, counts, words, observations = Counter(), Counter(), defaultdict(list), []
    for i, phi in enumerate(colorings):
        word, sigs = observation(edges, phi, leaves)
        observations.append((word, sigs))
        n[word] += 1
        words[word].append(i)
        for pair, sig in zip(PAIRS, sigs):
            counts[word, pair, sig] += 1
    yy = []
    for sig in signatures(6):
        values = {counts[word, pair, sig] for word in product((1, 2, 3), repeat=6)
                  for pair in PAIRS if compatible(word, pair, sig)}
        assert len(values) == 1
        yy.append(dict(signature=sig, count=values.pop()))
    nn = [dict(word=word, count=n[word], complete_coloring_ids=words[word])
          for word in product((1, 2, 3), repeat=6)]
    return nn, yy, observations


def report():
    fixture = json.loads(CONTROL.read_text())
    old_edges = fixture['edges']
    leaves, f = fixture['boundary_order'], fixture['marked_edge']
    old_rotations = {int(z): row for z, row in fixture['rotations'].items()}
    old_faces, old_outer = outer_face(old_edges, old_rotations, leaves, f)
    assert all_vertices_connected(old_edges)
    new = insert_diamond(fixture)
    edges, marked = new['edges'], new['marked_edge']
    edge_map, gg, vv = new['original_edge_map'], new['gadget_edges'], new['gadget_vertices']
    assert all_vertices_connected(edges)

    old_full = complete_colorings(old_edges)
    new_full = complete_colorings(edges)
    assert len(old_full) == 576 and len(new_full) == 1152
    old_index = {phi: i for i, phi in enumerate(old_full)}
    old_n, old_y, old_obs = lift_tables(old_edges, old_full, leaves)
    new_n, new_y, new_obs = lift_tables(edges, new_full, leaves)
    fibres = defaultdict(list)
    projection = []
    cycle_checks = []
    for i, phi in enumerate(new_full):
        x = phi[gg['up']]
        assert x == phi[gg['qv']] == phi[gg['rs']]
        psi = tuple(x if e == f else phi[edge_map[e]] for e in range(len(old_edges)))
        assert psi in old_index
        j = old_index[psi]
        fibres[j].append(i)
        projection.append(j)
        assert new_obs[i] == old_obs[j]
        cycles = []
        for other in (1, 2, 3):
            if other == phi[marked]:
                continue
            ends, ee = next(part for part in components(edges, phi, (phi[marked], other))
                            if marked in part[1])
            assert not ends
            cycles.append(dict(pair=sorted((phi[marked], other)), edge_ids=ee))
        cycle_checks.append(dict(complete_coloring_id=i, cycles=cycles))
    assert set(fibres) == set(range(len(old_full)))
    assert {len(row) for row in fibres.values()} == {2}
    assert all(a['word'] == b['word'] and b['count'] == 2 * a['count']
               for a, b in zip(old_n, new_n))
    assert len(old_n) == len(new_n) == 729
    assert all(a['signature'] == b['signature'] and b['count'] == 2 * a['count']
               for a, b in zip(old_y, new_y))
    assert len(old_y) == len(new_y) == 191
    assert Counter(new_obs) == Counter({obs: count * 2 for obs, count in Counter(old_obs).items()})

    # Independent exhaustive connectivity, plus the general proof certificate.
    assert all_vertices_connected(edges, {marked})
    cut_checks = []
    for other in range(len(edges)):
        if other == marked:
            continue
        parts = vertex_components(edges, {marked, other})
        together = any(set(edges[marked]) <= set(part) for part in parts)
        assert together
        other_is_bridge = not all_vertices_connected(edges, {other})
        assert (len(parts) == 1) == (not other_is_bridge)
        cut_checks.append(dict(removed=[marked, other], components=parts,
                               marked_endpoints_in_one_component=together,
                               other_edge_is_bridge=other_is_bridge))
    u, v = new['source_endpoints']
    path = source_path(old_edges, u, v, f)
    paths = [[marked], [gg['ps'], gg['rs']],
             [gg['up']] + [edge_map[e] for e in path] + [gg['qv'], gg['qr']]]
    verify_paths(edges, paths, vv['p'], vv['r'])

    saved_target = json.loads(SOURCE.read_text())
    target_h = {tuple(row['six_word']): row['three_cap_colors'][0]
                for row in saved_target['word_factorization']['rows']}
    actual_n = {tuple(row['word']): row['count'] for row in new_n}
    mismatch = next(word for word, value in sorted(target_h.items()) if value and not actual_n[word])
    assert sum(value > 0 for value in target_h.values()) == 81
    assert sum(row['count'] > 0 for row in new_n) == 48
    assert sum(row['count'] > 0 for row in new_y) == 13
    positive_indices = [row['six_signature_index']
                        for row in saved_target['signature_factorization']['pairs']]
    assert len(positive_indices) == 23

    paths_data = [dict(edge_ids=row) for row in paths]
    result = dict(
        scope='Finite complete non-target control; not an unconditional target counterexample.',
        general_conditional_theorem=(
            'Every target source, if one exists, gives a target source at scale 2*mu '
            'with an outer marked edge in no two-edge cut, by this insertion. '
            'Universal target bond existence is therefore equivalent to target-source emptiness.'),
        conclusions=dict(target_bond_existence='OPEN', target_source_existence='OPEN',
                         r2_exclusion='OPEN', new_forced_zero_coordinates=0,
                         target_counterexample=False, new_Lean=False),
        source_sha256={str(path.relative_to(ROOT)): sha256(path.read_bytes()).hexdigest()
                       for path in (CONTROL, SOURCE, Path(__file__),
                                    ROOT / 'scripts/ck_bernhart_marked_separation.py',
                                    ROOT / 'scripts/four_color_counts_cone_verification.py')},
        local_two_pole=local_extensions(),
        original=dict(name=fixture['name'], edges=old_edges, rotations=old_rotations,
                      marked_edge=f, boundary_order=leaves,
                      sphere_faces=old_faces, outer_face=old_outer,
                      complete_colorings=[''.join(map(str, phi)) for phi in old_full],
                      n=old_n, y=old_y),
        transformed=dict(name=fixture['name'] + '-K4-MARK', **new,
                         complete_colorings=[''.join(map(str, phi)) for phi in new_full],
                         n=new_n, y=new_y,
                         projection_to_original_coloring_ids=projection,
                         full_projection_fibres=[dict(original_coloring_id=i, transformed_coloring_ids=fibres[i])
                                                 for i in range(len(old_full))],
                         all_three_signed_signature_tuples_preserved=True,
                         multiplier=2, marked_cycle_checks=cycle_checks,
                         marked_edge_pair_deletions=cut_checks,
                         original_f_avoiding_path=path,
                         three_edge_disjoint_marked_endpoint_paths=paths_data),
        not_target=dict(actual_positive_words=48, target_positive_words=81,
                        actual_positive_signatures=13, target_positive_signatures=23,
                        positive_target_empty_actual_word=mismatch,
                        target_h=target_h[mismatch], actual_n=actual_n[mismatch]))
    return json.loads(json.dumps(result, sort_keys=True))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=DEFAULT)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    result = report()
    if args.check:
        assert json.loads(args.check.read_text()) == result
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    transformed = result['transformed']
    print(json.dumps(dict(original_complete_colorings=len(result['original']['complete_colorings']),
                         transformed_complete_colorings=len(transformed['complete_colorings']),
                         projection_fibres=len(transformed['full_projection_fibres']),
                         multiplier=2, literal_word_coordinates=len(transformed['n']),
                         signed_signature_coordinates=len(transformed['y']),
                         marked_cycle_checks=2 * len(transformed['complete_colorings']),
                         marked_edge_pair_deletions=len(transformed['marked_edge_pair_deletions']),
                         edge_disjoint_paths=len(transformed['three_edge_disjoint_marked_endpoint_paths']),
                         target_counterexample=False, excluded_rays=[], new_forced_zero_coordinates=0),
                     sort_keys=True))


if __name__ == '__main__':
    main()
