#!/usr/bin/env python3
"""Frozen finite checks; no search for, or claim of, an outside-catalogue source.

--write uses exclusive creation. --check recomputes the entire certificate and
does not write. --seed only changes traversal order; JSON is canonicalized.
The complete ten-row lifts below concern the three explicitly named controls.
Catalogue rows are independently recoloured, but not asserted exhaustive by
this checker: exhaustiveness remains an input theorem/evidence boundary.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import random
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE = ROOT / 'frozen/artifacts/c5_cells/cells.json'
CYCLE = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)]


def need(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(colouring):
    names = {}
    return tuple(names.setdefault(c, len(names)) for c in colouring)


def patterns():
    return sorted({canonical(p) for p in itertools.product(range(4), repeat=5)
                   if all(p[u] != p[v] for u, v in CYCLE)})


def normalized(edges):
    return sorted({tuple(sorted(e)) for e in edges})


def lifts(n, edges, boundary):
    return [list(boundary + rest)
            for rest in itertools.product(range(4), repeat=n - 5)
            if all((boundary + rest)[u] != (boundary + rest)[v]
                   for u, v in edges)]


def relation(rows):
    return sum(1 << i for i, row in enumerate(rows) if row)


def transform_pattern(p, permutation):
    out = [None] * 5
    for old, new in enumerate(permutation):
        out[new] = p[old]
    return canonical(out)


def transform_mask(mask, action):
    return sum(1 << action[i] for i in range(10) if mask & (1 << i))


def mask_patterns(mask, pats):
    return [''.join(map(str, p)) for i, p in enumerate(pats)
            if mask & (1 << i)]


def orientation(a, b, c):
    return ((b[0] - a[0]) * (c[1] - a[1])
            - (b[1] - a[1]) * (c[0] - a[0]))


def on_segment(a, b, p):
    return (orientation(a, b, p) == 0
            and min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
            and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))


def embedding_check(coords, edges, pair):
    """Certify a convex C5 straight-line disk embedding, also after adding uv."""
    augmented = normalized(edges + [pair])
    need(len(set(map(tuple, coords))) == len(coords), 'distinct coordinates')
    for v in range(5, len(coords)):
        need(all(orientation(coords[i], coords[(i + 1) % 5], coords[v]) < 0
                 for i in range(5)), 'interior point is strictly in convex C5')
    for u, v in augmented:
        need(u != v, 'loop in embedding control')
        for w in range(len(coords)):
            if w not in (u, v):
                need(not on_segment(coords[u], coords[v], coords[w]),
                     'vertex on edge in embedding control')
    for (u, v), (x, y) in itertools.combinations(augmented, 2):
        if len({u, v, x, y}) != 4:
            continue
        a, b, c, d = (coords[t] for t in (u, v, x, y))
        cross = (orientation(a, b, c) * orientation(a, b, d) < 0
                 and orientation(c, d, a) * orientation(c, d, b) < 0)
        touch = (on_segment(a, b, c) or on_segment(a, b, d)
                 or on_segment(c, d, a) or on_segment(c, d, b))
        need(not cross and not touch, 'crossing in embedding control')
    return {'status': 'triggered and holds',
            'method': 'exact integer straight-line disk embedding of G+uv',
            'nonadjacent_cofacial_pair': list(pair),
            'coordinates': coords}


def quotient(n, edges, pair):
    u, v = sorted(pair)
    survivors = [x for x in range(n) if x != v]
    mapping = {x: survivors.index(u if x == v else x) for x in range(n)}
    result = normalized([(mapping[x], mapping[y]) for x, y in edges])
    need(all(x != y for x, y in result), 'pair identification creates loop')
    return n - 1, result, [mapping[x] for x in range(n)]


def pair_control(name, n, extra, pair, coords, pats):
    edges = normalized(CYCLE + extra)
    source_rows = [lifts(n, edges, p) for p in pats]
    u, v = pair
    eq_rows = [[c for c in row if c[u] == c[v]] for row in source_rows]
    diff_rows = [[c for c in row if c[u] != c[v]] for row in source_rows]
    quotient_n, quotient_edges, projection = quotient(n, edges, pair)
    quotient_rows = [lifts(quotient_n, quotient_edges, p) for p in pats]
    add_edges = normalized(edges + [pair])
    add_rows = [lifts(n, add_edges, p) for p in pats]
    for i in range(10):
        pulled_back = sorted([[c[projection[x]] for x in range(n)]
                              for c in quotient_rows[i]])
        need(pulled_back == eq_rows[i], name + ': full Eq quotient lift')
        need(add_rows[i] == diff_rows[i], name + ': full Diff edge lift')
        need(sorted(eq_rows[i] + diff_rows[i]) == source_rows[i],
             name + ': same-source complete partition of whole colourings')
    masks = {'sigma': relation(source_rows), 'eq': relation(eq_rows),
             'diff': relation(diff_rows),
             'overlap': relation(eq_rows) & relation(diff_rows)}
    need(masks['sigma'] == masks['eq'] | masks['diff'], name + ': union')
    need(masks['overlap'] != 0, name + ': Eq/Diff overlap control')
    return {
        'name': name, 'status': 'triggered and holds',
        'source': {'vertices': list(range(n)), 'boundary_order': list(range(5)),
                   'edges': [list(e) for e in edges]},
        'pair': list(pair), 'embedding': embedding_check(coords, edges, pair),
        'quotient': {'vertices': list(range(quotient_n)),
                     'edges': [list(e) for e in quotient_edges],
                     'projection': projection},
        'add_edge_graph': {'vertices': list(range(n)),
                           'edges': [list(e) for e in add_edges]},
        'masks': masks,
        'rows': [{'index': i, 'pattern': list(p),
                  'source_full_lifts': source_rows[i],
                  'eq_full_lifts': eq_rows[i],
                  'diff_full_lifts': diff_rows[i],
                  'quotient_full_lifts': quotient_rows[i],
                  'add_edge_full_lifts': add_rows[i]}
                 for i, p in enumerate(pats)]}


def catalogue_checks(data, pats, rng):
    masks = sorted(map(int, data['cells']))
    need(len(masks) == 132, 'catalogue cardinality')
    need(list(map(tuple, data['pattern_order'])) == pats,
         'independently enumerated pattern order differs')
    visits = masks[:]
    rng.shuffle(visits)
    checks = {}
    for mask in visits:
        cell = data['cells'][str(mask)]
        n = 5 + cell['k_eff']
        edges = normalized(CYCLE + [tuple(e) for e in cell['edges']])
        need(all(0 <= u < v < n for u, v in edges), 'catalogue vertex labels')
        rows = [lifts(n, edges, p) for p in pats]
        actual = relation(rows)
        need(actual == mask, 'catalogue witness recolouring ' + str(mask))
        checks[str(mask)] = {'internal_vertices': n - 5,
                             'sigma': actual,
                             'ten_row_lift_counts': list(map(len, rows))}
    pairs = list(itertools.combinations_with_replacement(masks, 2))
    need(len(pairs) == 8778, 'union pair count')
    bad = [[a, b, a | b] for a, b in pairs if (a | b) not in masks]
    need(not bad, 'catalogue union closure')
    actions = []
    for sign in (1, -1):
        for rotation in range(5):
            permutation = [(rotation + sign * i) % 5 for i in range(5)]
            pattern_action = [pats.index(transform_pattern(p, permutation))
                              for p in pats]
            need(sorted(pattern_action) == list(range(10)), 'D5 permutation')
            need(sorted(transform_mask(m, pattern_action) for m in masks) == masks,
                 'D5 closure of catalogue')
            actions.append({'rotation': rotation, 'sign': sign,
                            'boundary_old_to_new': permutation,
                            'pattern_old_to_new': pattern_action})
    transported = []
    for base in (933, 941):
        subrelations = [m for m in masks if m & base == m]
        expected = [165] if base == 933 else [165, 424, 429]
        need(subrelations == expected, 'base subrelation list')
        available = 0
        for m in subrelations:
            available |= m
        gap = base & ~available
        need(gap == (768 if base == 933 else 512), 'base uniform gap')
        for action in actions:
            p_action = action['pattern_old_to_new']
            target = transform_mask(base, p_action)
            subs = sorted(transform_mask(m, p_action) for m in subrelations)
            need(subs == [m for m in masks if m & target == m],
                 'transported subrelation list')
            gaps = transform_mask(gap, p_action)
            q = p_action[9]
            need(gaps & (1 << q) != 0, 'transported 01232 missing state')
            need(target not in masks, 'outside target unexpectedly in catalogue')
            transported.append({'base': base, 'action': action,
                                'target': target, 'catalogue_subrelations': subs,
                                'gap_mask': gaps,
                                'forced_separation_patterns': mask_patterns(gaps, pats),
                                'transported_01232_index': q,
                                'transported_01232': list(pats[q]),
                                'source_realizability_status': 'not triggered',
                                'minimum_outside_source_status': 'not triggered'})
    targets = sorted({row['target'] for row in transported})
    need(len(targets) == 10, 'ten distinct outside targets')
    return {'status': 'triggered and holds',
            'witness_recolouring': {str(m): checks[str(m)] for m in masks},
            'union_closure': {'pair_count': len(pairs), 'bad_pairs': bad,
                              'includes_diagonal': True},
            'd5_actions': actions, 'outside_targets': targets,
            'target_transports': transported,
            'exhaustiveness': 'input boundary; this checker does not enumerate all disk graphs'}


def certificate(seed):
    raw = SOURCE.read_bytes()
    source_hash = hashlib.sha256(raw).hexdigest()
    manifest = json.loads((ROOT / 'INPUTS.json').read_text())
    expected = next(x['sha256'] for x in manifest['inputs']
                    if x['path'] == 'artifacts/c5_cells/cells.json')
    need(source_hash == expected, 'frozen catalogue hash mismatch')
    data = json.loads(raw)
    pats = patterns()
    need(len(pats) == 10, 'boundary pattern count')
    rng = random.Random(seed)
    boundary_coords = [[0, 4], [4, 1], [2, -4], [-2, -4], [-4, 1]]
    safe = pair_control('safe_equality_with_overlap', 7,
                        [(0, 5), (1, 5), (1, 6), (2, 6)], (5, 6),
                        boundary_coords + [[1, 2], [2, 0]], pats)
    need(safe['masks']['sigma'] == safe['masks']['eq'] == 1023,
         'safe equality preserves all ten patterns')
    split = pair_control('proper_equality_subrelation_with_overlap', 7,
                         [(0, 5), (1, 5), (2, 6), (3, 6)], (5, 6),
                         boundary_coords + [[1, 2], [0, -2]], pats)
    need(split['masks']['eq'] == 255 and split['masks']['diff'] == 1023,
         'proper Eq subrelation and complete Diff')
    extra = [(0, 5), (0, 6), (0, 7), (5, 7)]
    neg_coords = boundary_coords + [[-1, 2], [0, 3], [1, 2]]
    first = pair_control('joint_negative_ab', 8, extra, (5, 6), neg_coords, pats)
    second = pair_control('joint_negative_bc', 8, extra, (6, 7), neg_coords, pats)
    joint_rows = [[c for c in row['source_full_lifts']
                   if c[5] == c[6] == c[7]] for row in first['rows']]
    need(first['masks']['eq'] == second['masks']['eq'] == 1023,
         'both pairs independently safe')
    need(relation(joint_rows) == 0, 'joint equalities conflict with ac edge')
    need([first['quotient']['projection'][6], first['quotient']['projection'][7]]
         in first['quotient']['edges'], 'second pair becomes adjacent')
    controls = [safe, split, first, second]
    try:
        import networkx as nx
    except ImportError:
        apex = {'status': 'not triggered', 'reason': 'networkx unavailable',
                'disk_planarity': 'certified by exact coordinates for all small controls'}
    else:
        apex_rows = []
        for control in controls:
            for kind in ('source', 'quotient', 'add_edge_graph'):
                graph = control[kind]
                apex_vertex = len(graph['vertices'])
                g = nx.Graph()
                g.add_nodes_from(graph['vertices'] + [apex_vertex])
                g.add_edges_from(graph['edges'] + [[i, apex_vertex] for i in range(5)])
                planar, _ = nx.check_planarity(g)
                need(planar, 'apex planarity ' + control['name'] + ' ' + kind)
                apex_rows.append({'control': control['name'], 'graph': kind,
                                  'apex_planar': planar})
        apex = {'status': 'triggered and holds', 'version': nx.__version__,
                'rows': apex_rows}
    return {
        'schema': 'cofacial-uniform-separation-controls-v1',
        'frozen_source': {'path': '../frozen/artifacts/c5_cells/cells.json',
                          'sha256': source_hash, 'base': manifest['base']},
        'pattern_order': [list(p) for p in pats],
        'catalogue': catalogue_checks(data, pats, rng),
        'pair_controls': controls,
        'joint_negative_control': {
            'status': 'counterexample',
            'claim_refuted': 'individually safe identifications can always be combined',
            'source_control': 'joint_negative_ab',
            'pairs': [[5, 6], [6, 7]], 'literal_ac_edge': [5, 7],
            'each_equality_mask': [1023, 1023], 'joint_equality_mask': 0,
            'joint_rows': [{'index': i, 'pattern': list(p), 'full_lifts': joint_rows[i]}
                           for i, p in enumerate(pats)],
            'joint_identification': 'creates a loop; is not a legal loopless disk reduction',
            'after_first_identification_second_pair': 'adjacent; safe rule not triggered'},
        'optional_apex_planarity': apex,
        'outside_target_source_control': {
            'status': 'not triggered', 'realized_sources_supplied': 0,
            'statement': 'No minimum outside-catalogue source was supplied or inferred.'},
        'boundaries': ['No new source realizability conclusion.',
                       'No universal adjacent-singleton lemma or <=5 theorem proved here.',
                       'Uniform separation is conditional on a global minimum outside source.',
                       'Each complete lift uses the same labelled graph and colour frame.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--write', type=Path, metavar='CERTIFICATE')
    modes.add_argument('--check', type=Path, metavar='CERTIFICATE')
    parser.add_argument('--seed', type=int, default=0)
    args = parser.parse_args()
    actual = certificate(args.seed)
    if args.write:
        target = args.write.resolve()
        need(target.parent == HERE, 'certificate output must remain in controls/')
        with target.open('x') as output:
            json.dump(actual, output, sort_keys=True, indent=2)
            output.write('\n')
        print('PASS: exclusively created ' + str(target))
    else:
        expected = json.loads(args.check.read_text())
        need(expected == actual, 'certificate does not equal complete recomputation')
        print('PASS: read-only recomputation matches ' + str(args.check))
    print('132 witnesses; 8778 unions; 10 targets; full ten-row pair lifts; '
          'joint negative counterexample; outside source not triggered')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, FileExistsError) as error:
        print('FAIL: ' + str(error), file=sys.stderr)
        raise SystemExit(1)
