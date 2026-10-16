#!/usr/bin/env python3
"""Independent full-colouring, perfect-matching and primal-cycle replay."""
import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def calculate(path):
    data = path.read_bytes()
    graph = json.loads(data)
    edges = [tuple(x) for x in graph['J_edges']]
    faces = [tuple(sorted(x)) for x in graph['J_faces']]
    n = len(graph['J_vertices'])
    assert graph['J_vertices'] == list(range(n))
    assert len(set(edges)) == len(edges)
    assert all(a < b for a, b in edges)
    marks = graph['marks']
    assert len(set(marks)) == 3 and all(0 <= i < len(edges) for i in marks)
    assert [list(edges[i]) for i in marks] == graph['marked_original_edges']
    incident = defaultdict(list)
    for i, face in enumerate(faces):
        assert len(set(face)) == 3
        for a, b in ((face[0], face[1]), (face[0], face[2]), (face[1], face[2])):
            incident[(a, b)].append(i)
    assert set(incident) == set(edges)
    assert all(len(v) == 2 for v in incident.values())
    assert n - len(edges) + len(faces) == 2
    dual = [tuple(incident[e]) for e in edges]
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    root = faces[0]
    free = [v for v in range(n) if v not in root]
    normalized = []
    # Direct assignment enumeration, independent of the worker's DSATUR search.
    for values in product(range(4), repeat=len(free)):
        row = [0] * n
        for v, c in zip(root, range(3)):
            row[v] = c
        for v, c in zip(free, values):
            row[v] = c
        if all(row[a] != row[b] for a, b in edges):
            normalized.append(row)
    full = sorted({tuple(perm[c] for c in row)
                   for row in normalized for perm in permutations(range(4))})
    colour_fibres = Counter()
    types = Counter()
    for row in full:
        differences = [row[a] ^ row[b] for a, b in edges]
        colour_fibres[tuple(i for i, d in enumerate(differences) if d == 1)] += 1
        a, b, c = (differences[i] for i in marks)
        kind = ('111' if a == b == c else 'distinct' if len({a,b,c}) == 3
                else 'fg' if b == c else 'ef' if a == b else 'eg')
        types[kind] += 1
    d_adj = [[] for _ in faces]
    for i, (a, b) in enumerate(dual):
        d_adj[a].append((b, i))
        d_adj[b].append((a, i))

    def matching(left):
        if not left:
            yield ()
            return
        v = (left & -left).bit_length() - 1
        for u, edge in d_adj[v]:
            if left >> u & 1:
                for tail in matching(left ^ (1 << v) ^ (1 << u)):
                    yield tuple(sorted((edge,) + tail))

    pms = sorted(matching((1 << len(faces)) - 1))
    pm_records = []
    weights = Counter()
    counts = Counter()
    for pm in pms:
        remaining = set(range(len(faces)))
        cycles = []
        while remaining:
            todo = [min(remaining)]
            seen = set()
            while todo:
                v = todo.pop()
                if v in seen:
                    continue
                seen.add(v)
                todo.extend(u for u, edge in d_adj[v] if edge not in pm)
            remaining -= seen
            cycles.append(len(seen))
        cycles.sort()
        pattern = ''.join(str(int(i in pm)) for i in marks)
        oddness = sum(c % 2 for c in cycles)
        weight = 0 if oddness else 2 ** len(cycles)
        assert colour_fibres[pm] == 4 * weight
        counts[pattern] += 1
        weights[pattern] += weight
        pm_records.append({'matching': pm, 'pattern': pattern,
                           'cycle_lengths': cycles, 'oddness': oddness,
                           'full_fixed_alpha_fibre_size': colour_fibres[pm]})
    assert sum(colour_fibres.values()) == len(full)

    # Enumerate primal simple cycles; compare to the worker's dual vertex cuts.
    primal_cycles = set()
    for start in range(n):
        def walk(path):
            if len(path) in (4, 5) and start in adj[path[-1]]:
                cycle = tuple(path)
                primal_cycles.add(min(cycle, (start,) + tuple(reversed(path[1:]))))
            if len(path) == 5:
                return
            for v in sorted(adj[path[-1]]):
                if v > start and v not in path:
                    walk(path + [v])
        walk([start])
    edge_index = {e: i for i, e in enumerate(edges)}
    cuts = {'4': [], '5': []}
    for cycle in sorted(primal_cycles):
        cut = {edge_index[tuple(sorted((cycle[i], cycle[(i+1) % len(cycle)])))]
               for i in range(len(cycle))}
        remaining = set(range(len(faces)))
        sides = []
        while remaining:
            todo = [min(remaining)]
            seen = set()
            while todo:
                v = todo.pop()
                if v in seen:
                    continue
                seen.add(v)
                todo.extend(u for u, edge in d_adj[v] if edge not in cut)
            remaining -= seen
            sides.append(seen)
        assert len(sides) == 2
        if all(sum(a in side and b in side for a,b in dual) >= len(side)
               for side in sides):
            cuts[str(len(cycle))].append(sorted(cut))
    cuts = {k: sorted(v) for k, v in cuts.items()}
    layouts = []
    (v,w), (p,q), (g0,g1) = [edges[i] for i in marks]
    for m,z in ((g0,g1),(g1,g0)):
        if tuple(sorted((m,v,w))) in faces and tuple(sorted((z,p,q))) in faces:
            layouts.append({'m':m,'z':z,'v':v,'w':w,'p':p,'q':q})
    joint = [x for x in pm_records if x['pattern'] in ('110','101')]
    return {'input_sha256': sha256(data).hexdigest(),
            'checker_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
            'normalized_colourings': normalized, 'full_colourings': len(full),
            'colour_types': dict(sorted(types.items())),
            'pm_counts': dict(sorted(counts.items())),
            'weights': {format(i, '03b'): weights[format(i,'03b')] for i in range(8)},
            'all_pm_records': pm_records, 'joint_oddness': min(x['oddness'] for x in joint),
            'cyclic_cuts': cuts,
            'four_cut_avoids_e_f': all(not (set(c) & set(marks[:2])) for c in cuts['4']),
            'five_cut_at_most_one_mark': all(len(set(c) & set(marks)) <= 1 for c in cuts['5']),
            'source_two_face_layouts': layouts, 'original_minimum_source': 'not triggered'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, default=HERE.parent/'B/input_graph.json')
    parser.add_argument('--certificate', type=Path, default=HERE/'independent-control.json')
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = calculate(args.input)
    encoded = json.dumps(result, sort_keys=True, indent=2) + '\n'
    if args.write:
        with args.certificate.open('x') as f:
            f.write(encoded)
    else:
        assert args.certificate.read_text() == encoded, 'independent certificate differs'
    print(json.dumps({k:result[k] for k in ('full_colourings','colour_types','pm_counts',
                     'weights','joint_oddness','four_cut_avoids_e_f',
                     'five_cut_at_most_one_mark','source_two_face_layouts')}, sort_keys=True))


if __name__ == '__main__':
    main()
