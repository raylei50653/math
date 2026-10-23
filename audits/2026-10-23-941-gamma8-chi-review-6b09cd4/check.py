#!/usr/bin/env python3
"""Independent custody, sealed-star and oriented-face review; no source search."""
import argparse
from collections import Counter, defaultdict, deque
from copy import deepcopy
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import random

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def need(condition, message):
    if not condition:
        raise ValueError(message)


def edge(a, b):
    return tuple(sorted((a, b)))


def topology(boundary, inner, raw_edges, raw_faces):
    vertices = set(boundary + inner)
    edges = {edge(*e) for e in raw_edges}
    faces = [tuple(f) for f in raw_faces]
    need(len(vertices) == len(boundary) + len(inner), 'ownership alias')
    need(len(edges) == len(raw_edges), 'duplicate edge')
    need(len({tuple(sorted(f)) for f in faces}) == len(faces), 'duplicate face')
    need(all(len(set(f)) == 3 and set(f) <= vertices for f in faces), 'bad face')
    need(all(set(f) & set(inner) for f in faces), 'face lacks sealed interior owner')
    boundary_edges = {edge(boundary[i], boundary[(i + 1) % len(boundary)])
                      for i in range(len(boundary))}
    incidence = defaultdict(list)
    for i, f in enumerate(faces):
        for j in range(3):
            a, b = f[j], f[(j + 1) % 3]
            need(edge(a, b) in edges, 'face edge absent')
            incidence[edge(a, b)].append((i, 1 if a < b else -1))
    need(set(incidence) == edges, 'edge has no actual face')
    need(all(len(v) == (1 if e in boundary_edges else 2)
             for e, v in incidence.items()), 'face incidence')
    need(len(vertices) - len(edges) + len(faces) == 1, 'disk Euler')
    triangles = {tuple(sorted((a, b, c))) for a, b, c in combinations(vertices, 3)
                 if {edge(a, b), edge(b, c), edge(c, a)} <= edges}
    need(triangles == {tuple(sorted(f)) for f in faces}, 'nonface triangle')
    dual = defaultdict(list)
    for v in incidence.values():
        if len(v) == 2:
            (a, x), (b, y) = v
            dual[a].append((b, -x * y))
            dual[b].append((a, -x * y))
    signs = {0: 1}
    queue = deque([0])
    while queue:
        i = queue.popleft()
        for j, relation in dual[i]:
            wanted = signs[i] * relation
            if j in signs:
                need(signs[j] == wanted, 'incompatible face rotation')
            else:
                signs[j] = wanted
                queue.append(j)
    need(len(signs) == len(faces), 'disconnected face disk')
    oriented_boundary = Counter()
    for e, row in incidence.items():
        if len(row) == 1:
            i, direction = row[0]
            oriented_boundary[e if signs[i] * direction == 1 else tuple(reversed(e))] += 1
    expected = Counter((boundary[i], boundary[(i + 1) % len(boundary)])
                       for i in range(len(boundary)))
    need(oriented_boundary in (expected, Counter((b, a) for a, b in expected)),
         'oriented boundary mismatch')
    degrees = {}
    for v in vertices:
        neighbors = {b if a == v else a for a, b in edges if v in (a, b)}
        link_edges = {edge(*(x for x in f if x != v)) for f in faces if v in f}
        link_adj = {x: set() for x in neighbors}
        for a, b in link_edges:
            link_adj[a].add(b)
            link_adj[b].add(a)
        reached = set()
        queue = [next(iter(neighbors))]
        while queue:
            x = queue.pop()
            if x not in reached:
                reached.add(x)
                queue.extend(link_adj[x] - reached)
        need(reached == neighbors, 'disconnected vertex link')
        histogram = Counter(len(link_adj[x]) for x in neighbors)
        if v in inner:
            need(histogram == Counter({2: len(neighbors)}), 'unsealed interior star')
            need(len(neighbors) >= 5, 'interior original minimum degree')
            degrees[v] = len(neighbors)
        else:
            need(histogram == Counter({2: len(neighbors) - 2, 1: 2}), 'boundary link not path')
    return dict(vertices=len(vertices), edges=len(edges), faces=len(faces),
                sealed_stars=degrees, every_face_has_sealed_owner=True,
                common_orientation=True, boundary_link_paths=6)


def review(seed=0):
    inputs = json.loads((HERE / 'INPUTS.json').read_text())
    for row in inputs['sources']:
        data = (HERE / 'frozen' / row['path']).read_bytes()
        need(sha256(data).hexdigest() == row['sha256'], 'frozen source drift')
        need(sha256((ROOT / row['path']).read_bytes()).hexdigest() == row['sha256'],
             'live mathematical source drift')
    nonempty = json.loads((HERE / 'frozen/audits/2026-10-23-941-gamma8-joint-bpaths-6b09cd4/EXACT_CAPS.json').read_text())
    empty = json.loads((HERE / 'frozen/audits/2026-10-23-941-gamma8-empty-m2-6b09cd4/K6_CAPS.json').read_text())
    rows = []
    caps = [(f'nonempty-{c["id"]}', c['boundary'], c['inner'], c['edges'], c['faces'])
            for c in nonempty['caps']]
    caps += [(f'empty-{c["core"]}', c['ordered_boundary'], c['ordered_inner'], c['edges'], c['oriented_actual_faces'])
             for c in empty['caps']]
    random.Random(seed).shuffle(caps)
    for name, boundary, inner, edges, faces in caps:
        rows.append(dict(id=name, **topology(boundary, inner, edges, faces)))
    need(len(rows) == 18, 'cap domain coverage')
    # Validate the stored complete relation representation, never replace it by marginals.
    full_lifts = empty_fibres = 0
    for cap in nonempty['caps']:
        relations = cap['relations']
        need([r['word'] for r in relations] == nonempty['proper_S4_words'], 'ordered complete rows')
        for row in relations:
            lifts = row['full_lifts']
            need(len(lifts) == len({tuple(a) for a in lifts}), 'duplicate complete lift')
            empty_fibres += not lifts
            for lift in lifts:
                need(len(lift) == 8, 'truncated full lift')
                coloring = dict(zip(cap['boundary'] + cap['inner'], row['word'] + lift))
                need(all(coloring[a] != coloring[b] for a, b in cap['edges']), 'invalid full lift')
                full_lifts += 1
    return dict(status='PASS', frozen_inputs=len(inputs['sources']), mathematical_drift=0,
                cap_topology=sorted(rows, key=lambda r: r['id']),
                preserved_complete_boundary_rows=16 * 31,
                checked_saved_full_lifts=full_lifts, preserved_empty_fibres=empty_fibres,
                full_relation_exhaustiveness='inherited authority, not re-enumerated',
                source_realizability='not triggered', source_exclusion_from_controls=False)


def negative():
    path = HERE / 'frozen/audits/2026-10-23-941-gamma8-joint-bpaths-6b09cd4/EXACT_CAPS.json'
    cap = json.loads(path.read_text())['caps'][0]
    mutations = [('drop_actual_face', lambda c: c['faces'].pop()),
                 ('identify_boundary', lambda c: c['boundary'].__setitem__(0, 'd')),
                 ('lose_interior_owner', lambda c: c['inner'].remove('u')),
                 ('extra_sealed_star_edge', lambda c: c['edges'].append(['u', 'x']))]
    rejected = []
    for name, mutate in mutations:
        damaged = deepcopy(cap)
        mutate(damaged)
        try:
            topology(damaged['boundary'], damaged['inner'], damaged['edges'], damaged['faces'])
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('negative accepted: ' + name)
    return dict(status='PASS', semantic_rejections=rejected)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--negative', action='store_true')
    args = parser.parse_args()
    print(json.dumps(negative() if args.negative else review(args.seed), sort_keys=True))
