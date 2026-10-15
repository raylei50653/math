#!/usr/bin/env python3
"""Complete-colouring controls for a three-edge return obstruction; no 4CT."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
BASE = "6ddea32a81349821ad3724ae1652bddb9c6a7b04"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edge(a, b):
    return tuple(sorted((a, b)))


def edges_of(faces):
    return sorted({edge(a, b) for f in faces for a, b in itertools.combinations(f, 2)})


def colourings(vertices, edges):
    adj = {v: set() for v in vertices}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    out, f = [], {}

    def visit():
        if len(f) == len(vertices):
            out.append(tuple(f[v] for v in vertices))
            return
        v = min((v for v in vertices if v not in f),
                key=lambda v: (-len({f[w] for w in adj[v] if w in f}),
                               -len(adj[v]), v))
        avoid = {f[w] for w in adj[v] if w in f}
        for c in range(4):
            if c not in avoid:
                f[v] = c
                visit()
                del f[v]
    visit()
    return sorted(out)


def components(vertices, edges):
    adj = {v: set() for v in vertices}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    todo, out = set(vertices), []
    while todo:
        seed = min(todo)
        seen, frontier = {seed}, [seed]
        while frontier:
            a = frontier.pop()
            for b in sorted(adj[a] - seen):
                seen.add(b)
                frontier.append(b)
        todo -= seen
        out.append(sorted(seen))
    return sorted(out)


def verify_sphere(vertices, faces):
    """Connected orientable closed triangulated surface with Euler 2."""
    assert len(faces) == len({tuple(sorted(f)) for f in faces})
    inc = {}
    for i, f in enumerate(faces):
        assert len(set(f)) == 3
        for a, b in zip(f, f[1:] + f[:1]):
            inc.setdefault(edge(a, b), []).append((i, 1 if a < b else -1))
    assert all(len(v) == 2 for v in inc.values())
    orientation = {0: 1}
    todo = [0]
    dual = []
    for entries in inc.values():
        (i, x), (j, y) = entries
        dual.append((i, j))
    assert len(components(list(range(len(faces))), dual)) == 1
    while todo:
        i = todo.pop()
        for entries in inc.values():
            if entries[0][0] == i:
                (_, x), (j, y) = entries
            elif entries[1][0] == i:
                (j, y), (_, x) = entries
            else:
                continue
            want = -orientation[i] * x * y
            if j in orientation:
                assert orientation[j] == want
            else:
                orientation[j] = want
                todo.append(j)
    for v in vertices:
        link = [tuple(x for x in f if x != v) for f in faces if v in f]
        ls = sorted({x for e in link for x in e})
        assert len(components(ls, link)) == 1
        assert all(sum(x in e for e in link) == 2 for x in ls)
    assert len(vertices) - len(inc) + len(faces) == 2
    return {e: tuple(i for i, _ in entries) for e, entries in inc.items()}


def event(f, pins):
    return not {f[pins['p']], f[pins['q']]} & {f[pins['v']], f[pins['w']]}


def cycles_for(labels, dual, pair):
    chosen = [e for e in sorted(dual) if labels[e] in pair]
    cs = components(sorted({v for e in chosen for v in dual[e]}), [dual[e] for e in chosen])
    out = []
    for c in cs:
        es = [e for e in chosen if dual[e][0] in c]
        assert all(sum(v in dual[e] for e in es) == 2 for v in c)
        assert len(es) == len(c)
        out.append(es)
    return sorted(out)


def safe_formula(values, partition, pair):
    a, b, c = values
    same = lambda i, j: partition[i] is not None and partition[i] == partition[j]
    if a == b:
        assert c == a  # initial state is E-free
        return a not in pair or same(2, 0) or same(2, 1)
    if set(pair) != {a, b}:
        return True
    if c == a:
        return same(0, 1) or same(0, 2)
    if c == b:
        return same(1, 0) or same(1, 2)
    return same(0, 1)


def all_partitions(n):
    def rec(row):
        if len(row) == n:
            yield tuple(row)
        else:
            for x in range(max(row, default=-1) + 2):
                yield from rec(row + [x])
    yield from rec([])


def abstract_cubes():
    records = []
    for values in itertools.product((1, 2, 3), repeat=3):
        if values[0] == values[1] != values[2]:
            continue
        for pair in itertools.combinations((1, 2, 3), 2):
            active = [i for i, v in enumerate(values) if v in pair]
            for blocks in all_partitions(len(active)):
                part = [None] * 3
                for i, block in zip(active, blocks):
                    part[i] = block
                masks = range(1 << (max(blocks, default=-1) + 1))
                hits, single = [], []
                for mask in masks:
                    after = tuple(v ^ (pair[0] ^ pair[1])
                                  if part[i] is not None and mask >> part[i] & 1 else v
                                  for i, v in enumerate(values))
                    if after[0] == after[1] != after[2]:
                        hits.append(mask)
                        if mask.bit_count() == 1:
                            single.append(mask)
                safe = safe_formula(values, part, pair)
                assert safe == (not hits)
                assert bool(hits) == bool(single)
                records.append({'values': values, 'pair': pair, 'partition': part,
                                'E_masks': hits, 'single_cycle_E_masks': single, 'safe': safe})
    return records


def controls():
    # Two pentagonal caps joined by the explicitly triangulated annulus.
    A, B = lambda i: 2 + i % 5, lambda i: 7 + i % 5
    faces = [f for i in range(5) for f in
             [(0, A(i), A(i + 1)), (1, B(i), B(i + 1)),
              (A(i), A(i + 1), B(i)), (A(i), B(i - 1), B(i))]]
    yield 'icosahedral', list(range(12)), faces, dict(m=0, v=2, w=3, z=4, p=5, q=9)
    # Flip original edge 0--5; its opposite face vertices 4 and 6 are a nonedge.
    old = [f for f in faces if 0 in f and 5 in f]
    assert len(old) == 2 and (4, 6) not in edges_of(faces)
    flipped = [f for f in faces if f not in old] + [(0, 4, 6), (5, 4, 6)]
    yield 'flipped_icosahedral_return', list(range(12)), flipped, dict(m=0, v=2, w=3, z=4, p=5, q=9)
    # Stellar insertion in four specified faces; one fixed K4 colouring
    # extends uniquely at each insertion.  Final p,q have no v,w cross edge.
    faces = [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]
    for new, face in [(4, (1, 2, 3)), (5, (1, 4, 3)),
                      (6, (1, 4, 5)), (7, (1, 5, 6))]:
        old = next(f for f in faces if set(f) == set(face))
        faces.remove(old)
        a, b, c = face
        faces.extend([(a, b, new), (b, c, new), (c, a, new)])
    yield 'stacked_E_empty', list(range(8)), faces, dict(m=0, v=2, w=3, z=1, p=6, q=7)


def split_u(vertices, edges, faces, pins):
    m, v, w, z = [pins[x] for x in ('m', 'v', 'w', 'z')]
    link = [tuple(x for x in f if x != m) for f in faces if m in f]
    adj = {x: [] for e in link for x in e}
    for a, b in link:
        if {a, b} != {v, w}:
            adj[a].append(b)
            adj[b].append(a)
    path, previous = [v], None
    while path[-1] != w:
        choices = [x for x in adj[path[-1]] if x != previous]
        assert len(choices) == 1
        previous, nxt = path[-1], choices[0]
        path.append(nxt)
    zi = path.index(z)
    left, right = set(path[:zi + 1]), set(path[zi:])
    s, t = max(vertices) + 1, max(vertices) + 2
    ue = [e for e in edges if m not in e]
    ue += [edge(s, x) for x in left] + [edge(t, x) for x in right]
    uv = sorted(set(vertices) - {m} | {s, t})
    up = {x: pins[x] for x in 'zvwpq'} | {'s': s, 't': t}
    return uv, sorted(ue), up, path


def graph_control(name, vertices, faces, pins):
    edges = edges_of(faces)
    dual = verify_sphere(vertices, faces)
    assert set((pins['m'], pins['v'], pins['w'])) in [set(f) for f in faces]
    assert set((pins['z'], pins['p'], pins['q'])) in [set(f) for f in faces]
    assert edge(pins['m'], pins['z']) in edges
    assert all(edge(pins[a], pins[b]) not in edges for a in 'pq' for b in 'vw')
    marked = [edge(pins[a], pins[b]) for a, b in [('v', 'w'), ('p', 'q'), ('m', 'z')]]
    rows = colourings(vertices, edges)
    rowset = set(rows)
    six_order = 'mvwzpq'
    six_fibres = {''.join(map(str, row)): [] for row in itertools.product(range(4), repeat=6)}
    steps, n_E, unsafe = [], 0, 0
    for row in rows:
        f = dict(zip(vertices, row))
        labels = {e: f[e[0]] ^ f[e[1]] for e in edges}
        values = tuple(labels[e] for e in marked)
        hit = event(f, pins)
        assert hit == (values[0] == values[1] != values[2])
        n_E += hit
        six_fibres[''.join(str(f[pins[x]]) for x in six_order)].append(row)
        if hit:
            continue
        for pair in itertools.combinations((1, 2, 3), 2):
            cycles = cycles_for(labels, dual, pair)
            part = [next((i for i, c in enumerate(cycles) if e in c), None) for e in marked]
            safe = safe_formula(values, part, pair)
            returns = []
            for i, cycle in enumerate(cycles):
                sides = components(vertices, [e for e in edges if e not in cycle])
                assert len(sides) == 2
                side = next(s for s in sides if vertices[0] not in s)
                after = tuple(f[x] ^ (pair[0] ^ pair[1]) if x in side else f[x] for x in vertices)
                assert after in rowset
                af = dict(zip(vertices, after))
                for e in edges:
                    assert af[e[0]] ^ af[e[1]] == (labels[e] ^ (pair[0] ^ pair[1]) if e in cycle else labels[e])
                if event(af, pins):
                    returns.append({'cycle_index': i, 'side_vertices': side, 'full_return': after})
            assert safe == (not returns)
            unsafe += not safe
            steps.append({'full_colouring': row, 'pair': pair, 'cycles_as_original_edges': cycles,
                          'marked_cycle_partition': part, 'safe': safe, 'all_single_cycle_returns': returns})
    uv, ue, up, path = split_u(vertices, edges, faces, pins)
    urows = colourings(uv, ue)
    u_index = {x: i for i, x in enumerate(uv)}
    u_fibres = {''.join(map(str, r)): [] for r in itertools.product(range(4), repeat=7)}
    equal_rows, r_lifts = [], []
    for row in urows:
        f = dict(zip(uv, row))
        key = ''.join(str(f[up[x]]) for x in 'zsvwtpq')
        u_fibres[key].append(row)
        lifts = sorted(set(range(4)) - {f[up[x]] for x in 'svwt'})
        r_lifts.append({'full_U_colouring': row, 'all_r_lifts': lifts})
        if f[up['s']] == f[up['t']]:
            equal_rows.append(row)
    pulled = []
    for row in rows:
        f = dict(zip(vertices, row))
        pulled.append(tuple(f[pins['m']] if x in (up['s'], up['t']) else f[x] for x in uv))
    assert sorted(pulled) == equal_rows
    if name == 'stacked_E_empty':
        assert n_E == 0 and len(rows) == 24 and unsafe == 0
    elif name == 'icosahedral':
        assert len(rows) == 240 and n_E == 24 and unsafe == 0
    else:
        assert len(rows) == 288 and n_E == 96 and unsafe == 96
    return {'name': name, 'scope': 'plane_control_not_minimum_source', 'vertices': vertices,
            'edges': edges, 'faces': faces, 'pins': pins, 'marked_edges_e_f_g': marked,
            'all_full_J_colourings': rows, 'full_J_count': len(rows), 'E_count': n_E,
            'six_pin_fibres_all_4^6_including_empties': six_fibres,
            'all_failed_state_pair_checks': steps, 'unsafe_state_pairs': unsafe,
            'U': {'vertices': uv, 'edges': ue, 'pins': up, 'm_link_path_v_to_w_via_z': path,
                  'all_full_colourings': urows, 'full_count': len(urows),
                  'all_equal_s_t_full_lifts': equal_rows,
                  'seven_pin_fibres_all_4^7_including_empties': u_fibres,
                  'all_r_lifts_including_empties': r_lifts}}


def compute():
    inputs = json.loads((ROOT / 'INPUTS.json').read_text())
    assert inputs['base'] == BASE
    for item in inputs['entries']:
        assert sha(ROOT / item['frozen_path']) == item['sha256']
        assert sha(REPO / item['path']) == item['sha256']
    return {'base': BASE, 'checker_sha256': sha(Path(__file__)),
            'inputs_sha256': sha(ROOT / 'INPUTS.json'), 'input_drift': 0,
            'genuine_source_count': 0, 'genuine_source_status': 'not triggered',
            'abstract_cubes': abstract_cubes(),
            'controls': [graph_control(*args) for args in controls()]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--certificate', type=Path, default=ROOT / 'certificate.json')
    args = ap.parse_args()
    result = compute()
    # Roundtrip makes tuple/list comparison literal.
    result = json.loads(json.dumps(result))
    if args.write:
        with args.certificate.open('x') as f:
            json.dump(result, f, separators=(',', ':'), sort_keys=True)
            f.write('\n')
    else:
        assert json.loads(args.certificate.read_text()) == result, 'certificate mismatch'
    print(json.dumps({'status': 'PASS', 'abstract_cube_count': len(result['abstract_cubes']),
                      'controls': [{k: c[k] for k in ('name', 'full_J_count', 'E_count', 'unsafe_state_pairs')}
                                   | {'full_U_count': c['U']['full_count']} for c in result['controls']],
                      'input_drift': 0, 'genuine_source_status': 'not triggered'}, sort_keys=True))


if __name__ == '__main__':
    main()
