#!/usr/bin/env python3
"""Exact z--v attachment, complete fibres, and same-source Kempe transport.

No new planar row deletion is claimed. S4 representatives fix the original
triangle (x1,x2,z) to (0,1,2); all literal rows, including empties, are retained.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import subprocess

import four_color_three_step_relation_control as old
import four_color_three_step_source_invariant as source

ROOT = Path(__file__).resolve().parents[1]
COLORS = tuple(range(4))
PAIRS = tuple(combinations(COLORS, 2))
SPLITS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))
Y = (3, 4, 5, 6, 7, 8, 16)
U = tuple(range(3, 17))
CYCLE = (9, 10, 13, 12, 11, 14, 15, 16)


def canonical(c):
    mapping = {color: i for i, color in enumerate(c[:3])}
    for color in COLORS:
        if color not in mapping:
            mapping[color] = 3
    return tuple(mapping[color] for color in c)


def components(vertices, edges, c, pair):
    """Union-find, including isolated vertices; replay uses graph traversal."""
    parent = {v: v for v in vertices if c[v] in pair}
    def root(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v
    for a, b in edges:
        if a in parent and b in parent:
            parent[root(a)] = root(b)
    blocks = {}
    for v in parent:
        blocks.setdefault(root(v), []).append(v)
    return tuple(sorted(tuple(sorted(block)) for block in blocks.values()))


def enumerate_representatives(edges):
    neighbors = {v: set() for v in range(17)}
    for a, b in edges:
        neighbors[a].add(b)
        neighbors[b].add(a)
    coloring = {0: 0, 1: 1, 2: 2}
    result = []
    def visit():
        if len(coloring) == 17:
            result.append(tuple(coloring[v] for v in range(17)))
            return
        v = max((v for v in range(17) if v not in coloring),
                key=lambda v: (len(neighbors[v] & coloring.keys()), len(neighbors[v]), -v))
        forbidden = {coloring[w] for w in neighbors[v] if w in coloring}
        for color in COLORS:
            if color not in forbidden:
                coloring[v] = color
                visit()
        del coloring[v]
    visit()
    return sorted(result)


def projection_closure(fibres):
    support = [row for row, f in zip(product(COLORS, repeat=7), fibres) if f]
    tables = []
    for size in range(8):
        for indexes in combinations(range(7), size):
            tables.append(dict(ordered_scope=[Y[i] for i in indexes],
                               rows=sorted({tuple(row[i] for i in indexes) for row in support})))
    # Full relation is included. Check the entire 128-table semijoin family.
    for left in tables:
        for right in tables:
            overlap = sorted(set(left['ordered_scope']) & set(right['ordered_scope']))
            li = [left['ordered_scope'].index(v) for v in overlap]
            ri = [right['ordered_scope'].index(v) for v in overlap]
            supported = {tuple(r[i] for i in ri) for r in right['rows']}
            assert all(tuple(r[i] for i in li) in supported for r in left['rows'])
    return tables


def outer_counts(core_colorings):
    signature_counts = {}
    counts = []
    for word in product(COLORS, repeat=8):
        if any(word[i] == word[(i + 1) % 8] for i in range(8)):
            counts.append(0)
            continue
        a = dict(zip(CYCLE, word))
        signature = tuple(a[v] for v in (9, 13, 11, 15, 16))
        if signature not in signature_counts:
            signature_counts[signature] = sum(
                all(c[v] != a[p] for v, p in ((3, 9), (4, 13), (5, 11), (6, 15), (2, 16)))
                for c in core_colorings)
        counts.append(signature_counts[signature])
    positive = [n for n in counts if n]
    return dict(full_counts=counts, literal_proper_count=6564,
                accepted_count=len(positive), s4_pattern_count=274,
                min_lifts=min(positive), max_lifts=max(positive), total_lifts=sum(counts))


def feed(digest, record):
    digest.update(json.dumps(record, separators=(',', ':')).encode() + b'\n')


def cross_row_audit(edges, representatives):
    outside = [e for e in edges if min(e) >= 3]
    inside = [e for e in edges if min(e) < 3]
    interior_vertices = (0, 1, 2) + Y
    index = {c: i for i, c in enumerate(representatives)}
    partition_digest, transition_digest = sha256(), sha256()
    counts = dict(states=len(representatives), pair_partitions=0, joint_noncrossing_splits=0,
                  component_swaps=0, swaps_changing_outer_row=0,
                  swaps_preserving_outer_row=0, gluing_checks=0, core_outer_gluing_checks=0)
    outside_cache, ring_cache = {}, {}
    core_edges = [e for e in edges if max(e) < 9]
    ring_edges = [e for e in edges if min(e) >= 9]
    cut_edges = [e for e in edges if min(e) < 9 <= max(e)]
    assert cut_edges == [(2,16), (3,9), (4,13), (5,11), (6,15)]
    for i, c in enumerate(representatives):
        row = tuple(c[v] for v in U)
        if row not in outside_cache:
            outside_cache[row] = {p: components(U, outside, c, p) for p in PAIRS}
        outer_word = tuple(c[v] for v in CYCLE)
        if outer_word not in ring_cache:
            ring_cache[outer_word] = {p: components(CYCLE, ring_edges, c, p) for p in PAIRS}
        actual = {p: components(range(17), edges, c, p) for p in PAIRS}
        for p in PAIRS:
            exterior = outside_cache[row][p]
            interior = components(interior_vertices, inside, c, p)
            # Glue actual pieces along the SAME original interface vertices.
            links = [(block[0], v) for block in exterior + interior for v in block[1:]]
            assert components(range(17), links, c, p) == actual[p]
            counts['gluing_checks'] += 1
            core_blocks = components(range(9), core_edges, c, p)
            ring_blocks = ring_cache[outer_word][p]
            links = [(block[0], v) for block in core_blocks + ring_blocks for v in block[1:]]
            assert components(range(17), links + cut_edges, c, p) == actual[p]
            counts['core_outer_gluing_checks'] += 1
            feed(partition_digest, [i, p, actual[p], exterior])
            counts['pair_partitions'] += 1
            for block in actual[p]:
                target = list(c)
                for v in block:
                    target[v] = p[1] if c[v] == p[0] else p[0]
                assert all(target[a] != target[b] for a, b in edges)
                target = tuple(target)
                # Without relabelling, the exchanged and complementary pair
                # keep their exact components. Other pairs are recomputed at
                # the common target, never transported as independent choices.
                assert components(range(17), edges, target, p) == actual[p]
                complement = tuple(color for color in COLORS if color not in p)
                assert components(range(17), edges, target, complement) == actual[complement]
                j = index[canonical(target)]
                feed(transition_digest, [i, p, block, j, target[:3]])
                counts['component_swaps'] += 1
                changed = any(target[v] != c[v] for v in CYCLE)
                counts['swaps_changing_outer_row' if changed else 'swaps_preserving_outer_row'] += 1
        for left, right in SPLITS:
            blocks = [tuple(CYCLE.index(v) for v in block if v in CYCLE)
                      for block in actual[left] + actual[right]]
            assert old.kempe.noncrossing(blocks)
            counts['joint_noncrossing_splits'] += 1
    counts.update(partition_sha256=partition_digest.hexdigest(),
                  transition_sha256=transition_digest.hexdigest(),
                  distinct_anchored_remaining_rows=len(outside_cache),
                  distinct_anchored_outer_rows=len(ring_cache))
    return counts


def splice_control(edges):
    c = (0,1,2,1,2,2,3,3,0,0,1,0,1,0,1,0,1)
    target = (0,1,2,1,2,2,3,3,1,0,1,0,1,0,1,0,1)
    fake = (0,1,2,3,1,2,3,3,1,0,1,0,1,0,1,0,1)
    for row in (c, target, fake):
        assert all(row[a] != row[b] for a, b in edges)
    assert (8,) in components(range(17), edges, c, (0, 1))
    assert tuple(c[v] for v in CYCLE) == tuple(fake[v] for v in CYCLE)
    assert target != fake
    return dict(name='SWAP-TARGET-SPLICE-ZV', source_coloring=c, color_pair=(0,1),
                actual_component=(8,), true_target=target, forged_target=fake,
                illegal_changes=[v for v in range(17) if fake[v] != target[v]],
                all_three_colorings_proper=True,
                retained='All complete relations, fibres, six actual partitions at every lift, '
                         'and old C_alg/D inputs are unchanged; only one transport annotation is forged.',
                rejected_by='Target must change exactly the chosen actual component in the same literal frame.',
                new_solution_rows_deleted=0)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir', type=Path, required=True)
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=False)
    prior = source.outer_attachment_controls()['planar_outer_attachment_control']
    base_edges = list(map(tuple, prior['certificate']['original_edges']))
    edges = old.edges_canonical(base_edges + [(2, 16)])
    core = [e for e in base_edges if max(e) < 9]
    for v, required in [(0, {1,2,3,4,7}), (1, {0,2,5,6,7})]:
        assert {b if a == v else a for a, b in edges if v in (a,b)} == required
    # Split the original annular face at the actual new edge z--v.
    faces = prior['embedding']['prescribed_bounded_face_walks'][:-1] + [
        [3,2,16,9], [2,8,2,6,15,16], prior['embedding']['prescribed_exterior_walk']]
    embedding = source.rotation_from_faces(faces, source.nx.Graph(edges))
    history, remaining = old.exact_buckets(edges)
    h0, _ = old.exact_buckets(base_edges)
    assert history[:2] == h0[:2]
    assert tuple(history[2]['ordered_scope']) == Y
    assert (2,16) in map(tuple, history[2]['causal_original_edges'])
    assert all((2,16) not in map(tuple, r['causal_original_edges']) for r in history[:2])
    prior_fibres = old.direct_fibres(core)
    fibres = [[lift for lift in f if lift[2] != v] for f in prior_fibres for v in COLORS]
    # Reverse the entire bucket history only after a complete remaining row.
    relevant = [f for f in remaining if set(f['ordered_scope']) <= set(Y)]
    remaining_sets = [set(map(tuple, f['rows'])) for f in relevant]
    reconstructed = []
    for row in product(COLORS, repeat=7):
        a = dict(zip(Y, row))
        lifts = [a] if all(tuple(a[v] for v in f['ordered_scope']) in rows
                          for f, rows in zip(relevant, remaining_sets)) else []
        for record in reversed(history):
            extended = []
            for a in lifts:
                idx = 0
                for v in record['ordered_scope']:
                    idx = 4 * idx + a[v]
                extended.extend(a | {record['eliminated_vertex']: color}
                                for color in record['full_fibres'][idx])
            lifts = extended
        reconstructed.append(sorted(tuple(a[v] for v in range(3)) for a in lifts))
    assert reconstructed == fibres
    reps = enumerate_representatives(edges)
    core_colorings = [c for c in product(COLORS, repeat=9)
                      if all(c[a] != c[b] for a,b in core)]
    outer = outer_counts(core_colorings)
    assert len(reps)*24 == outer['total_lifts'] == 1529784
    cross = cross_row_audit(edges, reps)
    data = dict(contract=dict(name='ZV-17', vertices=list(range(17)),
                             labels=prior['labels'], original_edges=edges,
                             C_order=CYCLE, elimination_order=[0,1,2], shared_interface=Y,
                             new_edges=[(2,16)], base_core_edges=core,
                             exterior_edges=[e for e in edges if min(e)>=3],
                             oriented_faces=faces, rotation_system=embedding['rotation_system']),
                history=history,
                kernel=dict(full_fibres=fibres, remaining_factors=relevant,
                            projection_closure=projection_closure(fibres),
                            lifts=sum(map(len, fibres)), nonempty=sum(map(bool, fibres)),
                            empty=sum(not f for f in fibres),
                            old_cylinder_lifts=3744, old_cylinder_nonempty=2928),
                outer=outer,
                full_colorings=dict(triangle_anchor=[0,1,2], representatives=reps,
                                    literal_count=len(reps)*24),
                cross_row=cross, splice_control=splice_control(edges),
                old_control=dict(kernel_lifts=936, kernel_nonempty=732,
                                 d_control=old.inner_circle_control(core), outer_all_accept=True),
                claim='New original attachment changes the third bucket. Cross-row same-source '
                      'transport is verified; the Boolean outer table still accepts all proper C8. '
                      'No new solution-row exclusion, planar invariant sufficient for existence, or 4CT.')
    target = args.out_dir/'results.json'
    target.write_text(json.dumps(data,sort_keys=True,separators=(',', ':'))+'\n')
    dependencies = ['scripts/four_color_three_step_shared_exterior.py',
                    'scripts/four_color_three_step_shared_exterior_replay.py',
                    'scripts/four_color_three_step_relation_control.py',
                    'scripts/four_color_three_step_source_invariant.py',
                    'scripts/four_color_eight_cut_three_step_verification.py',
                    'scripts/four_color_seven_cut_verification.py', 'scripts/ck_kempe_obstruction.py']
    receipt = dict(baseline=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                   sources={p:sha256((ROOT/p).read_bytes()).hexdigest() for p in dependencies},
                   outputs={'results.json':sha256(target.read_bytes()).hexdigest()})
    (args.out_dir/'verification.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n')
    print(json.dumps(dict(kernel={k:v for k,v in data['kernel'].items() if k not in
                                 ('full_fibres','remaining_factors','projection_closure')},
                          history=[(r['nonempty_rows'],r['empty_rows']) for r in history],
                          outer={k:v for k,v in outer.items() if k!='full_counts'},cross_row=cross),sort_keys=True))


if __name__ == '__main__':
    main()
