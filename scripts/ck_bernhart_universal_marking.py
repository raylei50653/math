#!/usr/bin/env python3
"""A fixed planar two-pole universally creates an outer protected marking.

The local 40-cubic-vertex pole is extracted from the complete MC40 control.
It has twelve extensions per common terminal color. Its marked edge lies in
two closed bicolor components in every local extension, and its endpoints
have three edge-disjoint paths entirely inside the pole.

This does not construct a target source. The C6 replay is a non-target control.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path

from ck_bernhart_marked_separation import (
    CONTROL, SOURCE, complete_colorings, components, observation,
)
from ck_bernhart_marked_bond_obstruction import (
    all_vertices_connected, faces, lift_tables, outer_face,
    vertex_components, verify_paths,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / 'audits/2026-10-30-bernhart-universal-marking/verification.json'


def closed_mark_checks(edges, full, marked):
    checks = []
    for i, phi in enumerate(full):
        cycles = []
        for other in (1, 2, 3):
            if other == phi[marked]:
                continue
            ends, ee = next(part for part in components(edges, phi, (phi[marked], other))
                            if marked in part[1])
            assert not ends
            cycles.append(dict(pair=sorted((phi[marked], other)), edge_ids=ee))
        checks.append(dict(complete_coloring_id=i, cycles=cycles))
    return checks


def extract_pole():
    original = json.loads(CONTROL.read_text())
    interior = set(range(40))
    ids = [e for e, uv in enumerate(original['edges']) if set(uv).intersection(interior)]
    edges = [original['edges'][e] for e in ids]
    old_to_local = {e: i for i, e in enumerate(ids)}
    vertices = set(sum(edges, []))
    rotations = {int(v): [old_to_local[e] for e in row if e in old_to_local]
                 for v, row in original['rotations'].items() if int(v) in vertices}
    marked = old_to_local[original['marked_edge']]
    terminals = [40, 45]
    stems = [old_to_local[e] for e in (59, 64)]
    assert len(interior) == 40 and len(vertices) == 42 and len(edges) == 61
    assert all(len(row) == (1 if v in terminals else 3) for v, row in rotations.items())
    assert all_vertices_connected(edges)
    ff, outer = outer_face(edges, rotations, terminals, marked)
    full = complete_colorings(edges)
    assert len(full) == 36
    by_color = defaultdict(list)
    for i, phi in enumerate(full):
        assert phi[stems[0]] == phi[stems[1]]
        by_color[phi[stems[0]]].append(i)
    assert set(by_color) == {1, 2, 3} and {len(row) for row in by_color.values()} == {12}
    cycles = closed_mark_checks(edges, full, marked)
    # These original-edge paths lie entirely within the cubic interior, so
    # their cut obstruction is independent of any graph attached to the ports.
    original_paths = [[12], [11, 0, 13, 14], [30, 4, 2, 3, 51, 28, 54, 56]]
    paths = [[old_to_local[e] for e in row] for row in original_paths]
    verify_paths(edges, paths, *edges[marked])
    assert all(set(edges[e]) <= interior for path in paths for e in path)
    cut_checks = []
    for other in range(len(edges)):
        if other == marked:
            continue
        parts = vertex_components(edges, {marked, other})
        assert any(set(edges[marked]) <= set(part) for part in parts)
        cut_checks.append(dict(removed=[marked, other], components=parts,
                               marked_endpoints_in_one_component=True))
    return dict(original_name=original['name'], cubic_vertices=sorted(interior),
                terminals=terminals, stem_edges=stems, edges=edges, rotations=rotations,
                original_edge_ids=ids, original_to_local_edge_map=old_to_local,
                marked_edge=marked, sphere_faces=ff, outer_face=outer,
                complete_colorings=[''.join(map(str, phi)) for phi in full],
                complete_coloring_ids_by_terminal_color=by_color,
                multiplier=12, marked_cycle_checks=cycles,
                original_edge_disjoint_paths=original_paths,
                three_edge_disjoint_marked_endpoint_paths=paths,
                marked_edge_pair_deletions=cut_checks)


def cycle_control():
    edges = [[i, (i + 1) % 6] for i in range(6)] + [[i, 6 + i] for i in range(6)]
    leaves = list(range(6, 12))
    rotations = {i: [(i - 1) % 6, i, 6 + i] for i in range(6)}
    rotations |= {6 + i: [6 + i] for i in range(6)}
    for reflected in (False, True):
        trial = {v: row[::-1] if reflected else row for v, row in rotations.items()}
        try:
            ff, outer = outer_face(edges, trial, leaves, 0)
        except AssertionError:
            continue
        return dict(edges=edges, rotations=trial, boundary_order=leaves,
                    replaced_edge=0, sphere_faces=ff, outer_face=outer)
    raise AssertionError('No oriented C6 control found')


def insert_pole(core, pole):
    old, removed = core['edges'], core['replaced_edge']
    u, v = old[removed]
    keep = [e for e in range(len(old)) if e != removed]
    core_map = {e: i for i, e in enumerate(keep)}
    first_new = 1 + max(sum(old, []))
    vertex_map = {w: first_new + i for i, w in enumerate(pole['cubic_vertices'])}
    vertex_map |= {pole['terminals'][0]: u, pole['terminals'][1]: v}
    pole_map = {e: len(keep) + e for e in range(len(pole['edges']))}
    edges = [old[e] for e in keep] + [[vertex_map[a], vertex_map[b]] for a, b in pole['edges']]
    stems = [pole_map[e] for e in pole['stem_edges']]
    rotations = {w: [core_map[e] if e != removed else stems[0] if w == u else stems[1]
                     for e in row] for w, row in core['rotations'].items()}
    local = {vertex_map[w]: [pole_map[e] for e in pole['rotations'][w]]
             for w in pole['cubic_vertices']}
    marked = pole_map[pole['marked_edge']]
    for reflected in (False, True):
        trial = rotations | {w: row[::-1] if reflected else row for w, row in local.items()}
        try:
            ff, outer = outer_face(edges, trial, core['boundary_order'], marked)
        except AssertionError:
            continue
        return dict(edges=edges, rotations=trial, marked_edge=marked,
                    boundary_order=core['boundary_order'], source_edge_map=core_map,
                    pole_edge_map=pole_map, pole_vertex_map=vertex_map, stem_edges=stems,
                    reflected=reflected, sphere_faces=ff, outer_face=outer)
    raise AssertionError('No local reflection preserves the outer marked face')


def report():
    pole, core = extract_pole(), cycle_control()
    new = insert_pole(core, pole)
    base_full = complete_colorings(core['edges'])
    full = complete_colorings(new['edges'])
    assert len(base_full) == 66 and len(full) == 792
    assert all_vertices_connected(new['edges'])
    base_n, base_y, base_obs = lift_tables(core['edges'], base_full, core['boundary_order'])
    new_n, new_y, new_obs = lift_tables(new['edges'], full, core['boundary_order'])
    index = {phi: i for i, phi in enumerate(base_full)}
    fibres = defaultdict(list)
    projection = []
    for i, phi in enumerate(full):
        x = phi[new['stem_edges'][0]]
        assert x == phi[new['stem_edges'][1]]
        psi = tuple(x if e == core['replaced_edge'] else phi[new['source_edge_map'][e]]
                    for e in range(len(core['edges'])))
        j = index[psi]
        assert new_obs[i] == base_obs[j]
        projection.append(j)
        fibres[j].append(i)
    assert set(fibres) == set(range(len(base_full))) and {len(row) for row in fibres.values()} == {12}
    assert all(b['word'] == a['word'] and b['count'] == 12 * a['count']
               for a, b in zip(base_n, new_n))
    assert all(b['signature'] == a['signature'] and b['count'] == 12 * a['count']
               for a, b in zip(base_y, new_y))
    assert len(base_n) == len(new_n) == 729 and len(base_y) == len(new_y) == 191
    assert Counter(new_obs) == Counter({obs: 12 * value for obs, value in Counter(base_obs).items()})
    marked_checks = closed_mark_checks(new['edges'], full, new['marked_edge'])
    base_double_closed = 0
    for phi in base_full:
        statuses = [not next(part for part in components(core['edges'], phi,
                    (phi[core['replaced_edge']], other)) if core['replaced_edge'] in part[1])[0]
                    for other in (1, 2, 3) if other != phi[core['replaced_edge']]]
        base_double_closed += all(statuses)
    assert base_double_closed == 0
    paths = [[new['pole_edge_map'][e] for e in path]
             for path in pole['three_edge_disjoint_marked_endpoint_paths']]
    verify_paths(new['edges'], paths, *new['edges'][new['marked_edge']])
    cut_checks = []
    for other in range(len(new['edges'])):
        if other == new['marked_edge']:
            continue
        parts = vertex_components(new['edges'], {new['marked_edge'], other})
        assert any(set(new['edges'][new['marked_edge']]) <= set(part) for part in parts)
        cut_checks.append(dict(removed=[new['marked_edge'], other],
                               marked_endpoints_in_one_component=True))
    target = json.loads(SOURCE.read_text())
    h = {tuple(row['six_word']): row['three_cap_colors'][0]
         for row in target['word_factorization']['rows']}
    actual = {tuple(row['word']): row['count'] for row in new_n}
    mismatch = next(w for w in sorted(h) if h[w] and not actual[w])
    sources = [CONTROL, SOURCE, Path(__file__),
               ROOT / 'scripts/ck_bernhart_marked_separation.py',
               ROOT / 'scripts/ck_bernhart_marked_bond_obstruction.py',
               ROOT / 'scripts/four_color_counts_cone_verification.py']
    result = dict(
        scope='Universal finite marking gadget and non-target C6 insertion control; not a target counterexample.',
        conditional_theorem='Every unmarked connected plane six-leaf positive integer multiple of (k,h), if any exists, gives a marked target at twelve times the scale and with no two-edge cut containing its marking.',
        conclusions=dict(unmarked_target_source_existence='OPEN', marked_target_source_existence='OPEN',
                         universal_target_bond_existence='Equivalent to unmarked target-source emptiness; OPEN',
                         complete_target_counterexample=False, r2_exclusion='OPEN', new_forced_zero_coordinates=0),
        source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in sources},
        protected_two_pole=pole,
        control=dict(**core, complete_colorings=[''.join(map(str, phi)) for phi in base_full],
                     n=base_n, y=base_y, double_closed_replaced_edge_colorings=base_double_closed),
        transformed=dict(**new, complete_colorings=[''.join(map(str, phi)) for phi in full],
                         n=new_n, y=new_y, projection_to_source_coloring_ids=projection,
                         complete_projection_fibres=[dict(source_coloring_id=i, extension_coloring_ids=fibres[i])
                                                    for i in range(len(base_full))],
                         all_three_signed_signature_tuples_preserved=True, multiplier=12,
                         marked_cycle_checks=marked_checks,
                         three_edge_disjoint_marked_endpoint_paths=paths,
                         marked_edge_pair_deletions=cut_checks),
        not_target=dict(positive_target_empty_control_word=mismatch,
                        target_h=h[mismatch], transformed_n=actual[mismatch],
                        actual_positive_words=sum(v > 0 for v in actual.values()),
                        target_positive_words=sum(v > 0 for v in h.values())))
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
    print(json.dumps(dict(local_extensions=36, extensions_per_terminal_color=12,
                         local_marked_cycle_checks=72, local_marked_pair_deletions=60,
                         control_colorings=66, transformed_colorings=792, complete_projection_fibres=66,
                         multiplier=12, literal_word_coordinates=729, signed_signature_coordinates=191,
                         transformed_marked_cycle_checks=1584, transformed_marked_pair_deletions=71,
                         edge_disjoint_paths=3, target_counterexample=False,
                         excluded_rays=[], new_forced_zero_coordinates=0), sort_keys=True))


if __name__ == '__main__':
    main()
