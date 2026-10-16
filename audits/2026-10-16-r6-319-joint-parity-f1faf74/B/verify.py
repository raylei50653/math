#!/usr/bin/env python3
"""Complete fixed-graph control of the proposed joint oddness implication.

No imports from previous checkers; all colour fibres and all vertex cuts are
reconstructed. This graph is explicitly not a complete Sigma319 source.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import itertools
import json
from pathlib import Path
import random


def components(vertices, edges):
    adj = {v: set() for v in vertices}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    left = set(vertices)
    result = []
    while left:
        todo = [min(left)]
        seen = set()
        while todo:
            v = todo.pop()
            if v not in seen:
                seen.add(v)
                todo.extend(adj[v] - seen)
        left -= seen
        result.append(sorted(seen))
    return sorted(result)


def reconstruct(graph, seed):
    rng = random.Random(seed)
    vertices = graph['J_vertices']
    edges = [tuple(x) for x in graph['J_edges']]
    faces = graph['J_faces']
    edge_index = {uv: i for i, uv in enumerate(edges)}
    incidence = defaultdict(list)
    for i, face in enumerate(faces):
        assert len(set(face)) == 3
        for uv in itertools.combinations(face, 2):
            incidence[tuple(sorted(uv))].append(i)
    assert set(incidence) == set(edges)
    assert all(len(fs) == 2 for fs in incidence.values())
    assert len(vertices) - len(edges) + len(faces) == 2
    # Check every primal vertex link is one cycle, retaining all faces.
    for v in vertices:
        link_edges = [tuple(x for x in f if x != v) for f in faces if v in f]
        link_vertices = sorted({x for uv in link_edges for x in uv})
        assert len(components(link_vertices, link_edges)) == 1
        assert all(sum(x in uv for uv in link_edges) == 2 for x in link_vertices)
    dual = [tuple(incidence[uv]) for uv in edges]
    n = len(faces)
    assert len(components(range(n), dual)) == 1
    assert all(sum(v in uv for uv in dual) == 3 for v in range(n))

    adj = {v: set() for v in vertices}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    ties = {v: rng.random() for v in vertices}
    order = sorted(vertices, key=lambda v: (-len(adj[v]), ties[v]))
    full = []
    current = {}
    def colour(k):
        if k == len(order):
            full.append([current[v] for v in vertices])
            return
        v = order[k]
        banned = {current[u] for u in adj[v] if u in current}
        palette = list(range(4))
        rng.shuffle(palette)
        for c in palette:
            if c not in banned:
                current[v] = c
                colour(k + 1)
        current.pop(v, None)
    colour(0)
    full.sort()
    differences = [[c[a] ^ c[b] for a, b in edges] for c in full]
    fibres = defaultdict(list)
    for ci, d in enumerate(differences):
        fibres[tuple(i for i, a in enumerate(d) if a == 1)].append(ci)

    incident = defaultdict(list)
    for i, (a, b) in enumerate(dual):
        incident[a].append((i, b))
        incident[b].append((i, a))
    for options in incident.values():
        rng.shuffle(options)
    pms = []
    def match(left, chosen):
        if not left:
            pms.append(tuple(sorted(chosen)))
            return
        a = min(left)
        for i, b in incident[a]:
            if b in left:
                match(left - {a, b}, chosen + [i])
    match(set(range(n)), [])
    pms.sort()
    assert len(pms) == len(set(pms))
    rows = []
    for pm in pms:
        cs = components(range(n), [uv for i, uv in enumerate(dual) if i not in pm])
        oddness = sum(len(c) % 2 for c in cs)
        fibre = fibres[pm]
        assert len(fibre) == (0 if oddness else 4 * 2 ** len(cs))
        rows.append({'matching': list(pm), 'complement_cycles': cs,
                     'oddness': oddness, 'complete_fixed_alpha_fibre': fibre})
    assert set(fibres) <= set(pms)

    # Enumerate every nontrivial bipartition, with dual vertex zero on one side.
    # All cuts are literal edge boundaries, not five-edge deletion supersets.
    masks = [sum(1 << b for _, b in incident[a]) for a in range(n)]
    cut_size = bytearray(1 << n)
    cuts = {4: [], 5: []}
    for side in range(1, 1 << n):
        bit = side & -side
        v = bit.bit_length() - 1
        rest = side ^ bit
        cut_size[side] = cut_size[rest] + 3 - 2 * (masks[v] & rest).bit_count()
        k = cut_size[side]
        if not side & 1 or k not in cuts:
            continue
        sides = [[v for v in range(n) if bool(side & (1 << v)) == flag]
                 for flag in (True, False)]
        if not all(sides):
            continue
        cyclic = []
        for vs in sides:
            vv = set(vs)
            es = [uv for uv in dual if set(uv) <= vv]
            cyclic.append(any(sum(a in C and b in C for a, b in es) >= len(C)
                              for C in components(vs, es)))
        if all(cyclic):
            boundary = [i for i, (a, b) in enumerate(dual)
                        if bool(side & (1 << a)) != bool(side & (1 << b))]
            assert len(boundary) == k
            cuts[k].append({'sides': sides, 'boundary': boundary})
    for k in cuts:
        cuts[k].sort(key=lambda r: r['boundary'])

    e, f, g = graph['marks']
    assert graph['marked_original_edges'] == [list(edges[i]) for i in (e, f, g)]
    assert 'pins' not in graph, 'weak control must not inherit a different named marking'
    assert len({u for i in (e, f, g) for u in edges[i]}) == 6
    assert len({u for i in (e, f, g) for u in dual[i]}) == 6
    assert all((d[e] == d[f]) == (d[e] == d[g]) for d in differences)
    assert any(d[e] == d[f] == d[g] for d in differences)
    assert any(len({d[e], d[f], d[g]}) == 3 for d in differences)
    assert all(not ({e, f} & set(c['boundary'])) for c in cuts[4])
    assert all(len({e, f, g} & set(c['boundary'])) <= 1 for c in cuts[5])
    joint = [i for i, r in enumerate(rows) if e in r['matching'] and
             ((f in r['matching']) != (g in r['matching']))]
    assert joint and min(rows[i]['oddness'] for i in joint) == 2
    assert all(g in rows[i]['matching'] and f not in rows[i]['matching'] for i in joint)
    weights = Counter()
    ordinary = Counter()
    for r in rows:
        status = ''.join('1' if i in r['matching'] else '0' for i in (e, f, g))
        ordinary[status] += 1
        if not r['oddness']:
            weights[status] += 2 ** len(r['complement_cycles'])
    for bits in itertools.product('01', repeat=3):
        ordinary[''.join(bits)] += 0
        weights[''.join(bits)] += 0

    # Exact same graph: all named layouts with literal triangular faces mvw,zpq
    # and g=mz. No independent terminal assignments are combined.
    layouts = defaultdict(list)
    for g0, mz in enumerate(edges):
        for m, z in (mz, mz[::-1]):
            for F in faces:
                if m not in F:
                    continue
                vw = tuple(sorted(set(F) - {m}))
                for H in faces:
                    if z not in H:
                        continue
                    pq = tuple(sorted(set(H) - {z}))
                    if len({m, z, *vw, *pq}) != 6:
                        continue
                    marks = (edge_index[vw], edge_index[pq], g0)
                    layouts[marks].append({'m': m, 'z': z, 'v': vw[0], 'w': vw[1],
                                           'p': pq[0], 'q': pq[1]})
    signatures = sorted(set(tuple(d) for d in differences))
    pm_sets = [set(pm) for pm in pms]
    cut4 = [set(c['boundary']) for c in cuts[4]]
    cut5 = [set(c['boundary']) for c in cuts[5]]
    layers = Counter()
    surviving_marks = []
    layout_candidates = []
    for ee, ff, gg in itertools.permutations(range(len(edges)), 3):
        states = {(d[ee] == d[ff], d[ee] == d[gg], len({d[ee], d[ff], d[gg]}))
                  for d in signatures}
        if not (all(a == b for a, b, _ in states) and
                (True, True, 1) in states and (False, False, 3) in states):
            continue
        layers['FJ_111_all_distinct'] += 1
        js = [i for i, pm in enumerate(pm_sets) if ee in pm and ((ff in pm) != (gg in pm))]
        if not js:
            continue
        layers['plus_ordinary_joint'] += 1
        four_ok = all(not ({ee, ff} & c) for c in cut4)
        five_ok = all(len({ee, ff, gg} & c) <= 1 for c in cut5)
        if four_ok:
            layers['plus_cyclic4_avoid_e_f'] += 1
            if five_ok:
                layers['plus_cyclic5_at_most_one_mark'] += 1
                surviving_marks.append([ee, ff, gg])
                if (ee, ff, gg) in layouts:
                    layers['plus_literal_two_faces_and_bridge'] += 1
        for pins in layouts.get((ee, ff, gg), []):
            m, z = pins['m'], pins['z']
            v, w, p, q = (pins[k] for k in ('v', 'w', 'p', 'q'))
            cross = sorted([sorted((a, b)) for a in (v, w) for b in (p, q)
                            if b in adj[a]])
            common = {str(x): sorted(adj[z] & adj[x]) for x in (v, w)}
            layout_candidates.append({'marks': [ee, ff, gg], 'pins': pins,
                                      'cyclic4_condition': four_ok,
                                      'cyclic5_condition': five_ok,
                                      'forbidden_cross_edges': cross,
                                      'common_neighbors_with_z': common})
    for label in ('FJ_111_all_distinct', 'plus_ordinary_joint',
                  'plus_cyclic4_avoid_e_f', 'plus_cyclic5_at_most_one_mark',
                  'plus_literal_two_faces_and_bridge'):
        layers[label] += 0
    assert not layouts.get((e, f, g))
    assert layers['plus_literal_two_faces_and_bridge'] == 0
    assert layout_candidates and all(r['forbidden_cross_edges'] for r in layout_candidates)
    return {
        'source_authority': 'not triggered; finite graph fails literal source layout',
        'dual_edges': [list(x) for x in dual],
        'all_complete_J_colourings': full,
        'all_matching_rows': rows,
        'ordinary_counts': dict(sorted(ordinary.items())),
        'even_weights': dict(sorted(weights.items())),
        'joint_matching_indices': joint,
        'joint_minimum_oddness': 2,
        'all_cyclic4_cuts': cuts[4],
        'all_cyclic5_cuts': cuts[5],
        'fixed_mark_literal_layouts': [],
        'all_marking_layer_counts': dict(sorted(layers.items())),
        'all_markings_passing_small_cut_conditions': surviving_marks,
        'all_FJ_nonempty_joint_literal_layouts': sorted(layout_candidates,
                                                       key=lambda r: (r['marks'], str(r['pins']))),
    }


def main():
    p = argparse.ArgumentParser()
    modes = p.add_mutually_exclusive_group(required=True)
    modes.add_argument('--output', type=Path)
    modes.add_argument('--check', type=Path)
    p.add_argument('--seed', type=int, default=0)
    p.add_argument('--input', type=Path)
    args = p.parse_args()
    source = args.input or Path(__file__).with_name('input_graph.json')
    result = {'input_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
              'result': reconstruct(json.loads(source.read_text()), args.seed)}
    if args.output:
        with args.output.open('x') as stream:
            json.dump(result, stream, sort_keys=True, indent=2)
            stream.write('\n')
    elif json.loads(args.check.read_text()) != result:
        raise SystemExit('FAIL: certificate differs from independent complete reconstruction')
    r = result['result']
    print(json.dumps({'status': 'PASS', 'colourings': len(r['all_complete_J_colourings']),
                      'PMs': len(r['all_matching_rows']),
                      'joint_PM_count': len(r['joint_matching_indices']),
                      'omega_e': r['joint_minimum_oddness'],
                      'cyclic4_cuts': len(r['all_cyclic4_cuts']),
                      'cyclic5_cuts': len(r['all_cyclic5_cuts']),
                      'layers': r['all_marking_layer_counts']}, sort_keys=True))


if __name__ == '__main__':
    main()
