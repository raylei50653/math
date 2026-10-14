#!/usr/bin/env python3
"""Full-fibre controls on seven explicit plane disks, not target sources."""
import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
TYPES = ((0, 1, 0, 1), (0, 1, 0, 2), (0, 1, 2, 1), (0, 1, 2, 3))
NAMES = ('ABAB', 'ABAC', 'ABCB', 'ABCD')


def need(condition, message):
    if not condition:
        raise ValueError(message)


def edges_of(faces):
    return sorted({tuple(sorted((f[i], f[(i + 1) % len(f)])))
                   for f in faces for i in range(len(f))})


def validate(faces):
    edges = edges_of(faces)
    vertices = sorted({v for edge in edges for v in edge})
    darts = Counter((f[i], f[(i + 1) % len(f)])
                    for f in faces for i in range(len(f)))
    need(darts == Counter({d: 1 for u, v in edges for d in ((u, v), (v, u))}),
         'oriented sphere incidence')
    need(len(vertices) - len(edges) + len(faces) == 2, 'sphere Euler')
    for v in vertices:
        links = [(f[(i - 1) % len(f)], f[(i + 1) % len(f)])
                 for f in faces for i in range(len(f)) if f[i] == v]
        successor = dict(links)
        neighbors = {w for e in edges if v in e for w in e if w != v}
        need(len(successor) == len(links) and set(successor) == neighbors
             and set(successor.values()) == neighbors, 'vertex-link darts')
        seen, at = set(), min(neighbors)
        while at not in seen:
            seen.add(at)
            at = successor[at]
        need(at == min(neighbors) and seen == neighbors, 'one vertex-link cycle')
    return vertices, edges


def all_fibres(vertices, edges):
    adj = {v: set() for v in vertices}
    for v, w in edges:
        adj[v].add(w)
        adj[w].add(v)
    result = []
    for boundary in TYPES:
        f = dict(enumerate(boundary))
        rows = []

        def visit():
            if len(f) == len(vertices):
                rows.append(tuple(f[v] for v in vertices))
                return
            v = max((v for v in vertices if v not in f),
                    key=lambda v: (len({f[w] for w in adj[v] if w in f}), len(adj[v]), -v))
            forbidden = {f[w] for w in adj[v] if w in f}
            for c in range(4):
                if c not in forbidden:
                    f[v] = c
                    visit()
                    del f[v]

        visit()
        result.append(set(rows))
    return adj, result


def component(adj, f, root, colors):
    seen, todo = {root}, [root]
    while todo:
        for w in sorted(adj[todo.pop()]):
            if w not in seen and f[w] in colors:
                seen.add(w)
                todo.append(w)
    return seen


def switch(adj, f, root, colors):
    comp = component(adj, f, root, colors)
    a, b = colors
    return tuple(b if c == a and v in comp else a if c == b and v in comp else c
                 for v, c in enumerate(f))


def models():
    # The outer face is (0,3,2,1), so named Q=(0,1,2,3) is counterclockwise.
    base = [(0, 3, 2, 1), (0, 1, 4), (1, 2, 5), (2, 3, 5),
            (3, 0, 4), (1, 5, 4), (3, 4, 5)]
    yield 'base-mask13', base, None
    # Stellar insertion preserves the full Q relation. The final z-p-q face
    # has two strictly internal named vertices. These controls have low degrees.
    for side, first in enumerate(((0, 1, 4), (3, 0, 4))):
        faces = list(base)
        face = first
        for depth in range(1, 4):
            new = 5 + depth
            faces.remove(face)
            added = [(face[i], face[(i + 1) % 3], new) for i in range(3)]
            faces.extend(added)
            face = next(f for f in added if 0 in f and 4 in f)
            yield f'side{side}-stack{depth}', list(faces), (4, new)


def local_r_table():
    # R'=z,s,v,t. Restore r adjacent to s,v,t; old Q=z,s,r,t.
    rows = []
    support_image = []
    for new_q in TYPES:
        lifts = []
        for r in range(4):
            if r in new_q[1:]:
                continue
            old_q = (new_q[0], new_q[1], r, new_q[3])
            rename = {}
            normalized = tuple(rename.setdefault(c, len(rename)) for c in old_q)
            old_type = TYPES.index(normalized)
            lifts.append({'r': r, 'old_Q': old_q, 'old_type': NAMES[old_type]})
        rows.append({'Q_prime': new_q, 'lifts': lifts})
        support_image.append(sum(1 << i for i in
                                 {NAMES.index(l['old_type']) for l in lifts}))
    seven = (7, 10, 11, 12, 13, 14, 15)
    matches = []
    for mask in seven:
        image = 0
        for i in range(4):
            if mask & (1 << i):
                image |= support_image[i]
        if image == 13:
            matches.append(mask)
    need(matches == [7], 'unique smaller support')
    # Intersect all same-row r lifts with the refined old six-pin conditions.
    refined = {0: ({2, 3},), 1: (), 2: ({1, 3}, {2, 3}), 3: ({1, 3},)}
    expected = (((2, 3), (3, 2)), ((1, 2), (2, 1)), ((2, 3), (3, 2)), ())
    for i, row in enumerate(rows):
        allowed = []
        for pq in itertools.permutations((1, 2, 3), 2):
            good = True
            for lift in row['lifts']:
                rename = {}
                for c in lift['old_Q']:
                    rename.setdefault(c, len(rename))
                for c in range(4):
                    rename.setdefault(c, len(rename))
                palette = {rename[c] for c in pq}
                if palette not in refined[NAMES.index(lift['old_type'])]:
                    good = False
            if good:
                allowed.append(pq)
        need(tuple(allowed) == expected[i], 'refined smaller joint relation')
        row['allowed_pq'] = allowed
    return {'rows': rows, 'support_images': support_image, 'preimage_of_13': matches}


def calculate():
    records = []
    total = 0
    bad_abcb_examples = []
    for name, faces, pq in models():
        vertices, edges = validate(faces)
        adj, fibres = all_fibres(vertices, edges)
        need(sum(1 << i for i, rows in enumerate(fibres) if rows) == 13,
             'explicit graph mask13')
        ac_separate = {f for f in fibres[2] if 0 not in component(adj, f, 2, (0, 2))}
        ac_connected = fibres[2] - ac_separate
        mapped_abab = {switch(adj, f, 2, (0, 2)) for f in fibres[0]}
        mapped_abcd = {switch(adj, f, 3, (1, 3)) for f in fibres[3]}
        need(mapped_abab == ac_separate, 'ABAB full-set bijection')
        need(mapped_abcd == ac_connected, 'ABCD full-set bijection')
        for i, target, root, pair in ((0, ac_separate, 2, (0, 2)),
                                      (3, ac_connected, 3, (1, 3))):
            need({switch(adj, f, root, pair) for f in target} == fibres[i], 'inverse')
            for f in fibres[i] | target:
                need(switch(adj, switch(adj, f, root, pair), root, pair) == f, 'involution')
        conditions = None
        if pq is not None:
            p, q = pq
            need({0, p, q} in [set(face) for face in faces[1:]], 'literal marked face')
            conditions = [all({f[p], f[q]} == {2, 3} for f in fibres[0]),
                          all({f[p], f[q]} == {1, 3} for f in fibres[3])]
            # Every sampled graph has actual successful cap lifts. They are
            # countercontrols, not asserted realizations of target failure.
            need(not all(conditions), 'control accidentally target failure')
            examples = [f for f in fibres[2] if {f[p], f[q]} == {1, 2}]
            if examples:
                bad_abcb_examples.append({'graph': name, 'pq': pq, 'full_coloring': min(examples),
                                          'failure_conditions': conditions})
        total += sum(map(len, fibres))
        records.append({'name': name, 'edges': edges, 'oriented_faces': faces, 'pq': pq,
                        'counts': list(map(len, fibres)), 'failure_conditions': conditions,
                        'fibres': {n: sorted(fs) for n, fs in zip(NAMES, fibres)},
                        'ABCB_AC_separate': sorted(ac_separate),
                        'ABCB_AC_connected': sorted(ac_connected)})
    need(bad_abcb_examples, 'need actual graph negative control for dropped hypotheses')
    # A marginal equality is insufficient: deliberately drop a full target lift.
    victim = set(tuple(f) for f in records[0]['ABCB_AC_separate'])
    altered = victim - {min(victim)}
    base_vertices, base_edges = validate(records[0]['oriented_faces'])
    base_adj, base_fibres = all_fibres(base_vertices, base_edges)
    actual_image = {switch(base_adj, f, 2, (0, 2)) for f in base_fibres[0]}
    try:
        need(actual_image == altered, 'ABAB full-set bijection')
    except ValueError as error:
        missing_lift_rejection = str(error)
    else:
        raise ValueError('accepted missing full lift')
    return {'status': 'PASS', 'graphs': len(records), 'complete_fixed_Q_colorings': total,
            'full_set_bijections': 2 * len(records), 'actual_target_sources': 0,
            'records': records, 'dropped_hypothesis_negative_controls': bad_abcb_examples,
            'missing_full_lift_rejection': missing_lift_rejection,
            'r_degree5_table': local_r_table(),
            'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = calculate()
    payload = json.dumps(result, indent=2) + '\n'
    output = HERE / 'fibres.json'
    if args.check:
        need(output.read_text() == payload, 'certificate differs')
    else:
        with output.open('x') as handle:
            handle.write(payload)
    print(json.dumps({k: result[k] for k in ('status', 'graphs', 'complete_fixed_Q_colorings',
                                           'full_set_bijections', 'actual_target_sources')}))


if __name__ == '__main__':
    main()
