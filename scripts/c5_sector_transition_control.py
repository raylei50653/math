#!/usr/bin/env python3
"""Explicit disk 397->330 control; replay checks saved rotations/colorings only."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_sector_transition_control/observations.json'
UPSTREAM = ROOT / 'artifacts/c5_sector_corner_gates/observations.json'
CROSS = ROOT / 'artifacts/c5_sector_cross_row/observations.json'
NAMES = ['0', '1', '2', '3', '4', 'w', 'b', 'a', 't3', 'c', 't2', 'd', 'q', 'r', 'p', 'x', 'u']
ID = {name: i for i, name in enumerate(NAMES)}
FRAME = set(range(5))
PAIRS = list(combinations(range(4), 2))


def edges(g):
    return sorted(sorted(e) for e in g.edges())


def normalize(row):
    names = {}
    return tuple(names.setdefault(c, len(names)) for c in row)


def seed(patched=False):
    g = nx.Graph()
    g.add_nodes_from(range(17 if patched else 16))
    for word in ['1 2 3 4', '0 w p', '0 b a t3 c t2 d 1',
                 '1 q w r t3 x 4', '3 t2 p 1'] + (['p u 1'] if patched else []):
        vs = [ID[v] for v in word.split()]
        g.add_edges_from(zip(vs, vs[1:]))
    colors = dict(enumerate([0, 1, 0, 2, 1, 1, 1, 0, 1, 0, 1, 0, 3, 3, 2, 3, 0][:len(g)]))
    return g, colors


def complete(base):
    g, gadgets = base.copy(), []
    for anchor in sorted(set(base) - FRAME):
        assert base.degree[anchor] in (2, 4)
        if base.degree[anchor] == 4:
            continue
        vs = list(range(len(g), len(g)+6))
        g.add_nodes_from(vs)
        local_edges = [(v, w) for i, v in enumerate(vs) for j, w in enumerate(vs)
                       if i < j and i//2 != j//2 and (i, j) != (0, 2)]
        g.add_edges_from(local_edges + [(anchor, vs[0]), (anchor, vs[2])])
        gadgets.append(dict(anchor=anchor, vertices=vs, edges=local_edges + [(anchor, vs[0]), (anchor, vs[2])]))
    return g, gadgets


def lift(colors, gadgets):
    result = dict(colors)
    for gadget in gadgets:
        palette = sorted(set(range(4)) - {result[gadget['anchor']]})
        result.update((v, palette[i//2]) for i, v in enumerate(gadget['vertices']))
    return result


def proper(g, colors):
    assert set(colors) == set(g) and set(colors.values()) <= set(range(4))
    assert all(colors[v] != colors[w] for v, w in g.edges())


def partition(g, colors, pair, frame_only=False):
    return sorted(sorted(set(cc) & FRAME if frame_only else cc)
                  for cc in nx.connected_components(g.subgraph(v for v in g if colors[v] in pair))
                  if not frame_only or set(cc) & FRAME)


def even_cycle(g, colors, raw, selected):
    j = g.subgraph(set(g)-{0, ID['w']})
    sprime = selected-{0, ID['w']}
    # Stop at the FIRST frame hit, so the joining segment is entirely internal.
    gamma = nx.shortest_path(j.subgraph(sprime), ID['b'], 1)
    stop = next(i for i, v in enumerate(gamma) if v in FRAME)
    gamma = gamma[:stop+1]
    assert gamma[-1] in (1, 2) and not set(gamma[:-1]) & FRAME
    rpath = nx.shortest_path(j.subgraph(v for v in j if colors[v] in (1, 3)), 4, ID['r'])
    ppath = nx.shortest_path(j.subgraph(v for v in j if raw[v] in (0, 2) and v != 1), 3, ID['p'])
    assert not set(rpath) & set(ppath)
    hits = [(i, 'R' if v in rpath else 'P') for i, v in enumerate(gamma) if v in rpath or v in ppath]
    assert {kind for _, kind in hits} == {'R', 'P'}
    left, right = next((x, y) for x, y in zip(hits, hits[1:]) if x[1] != y[1])
    middle = gamma[left[0]:right[0]+1]
    if left[1] == 'P':
        middle.reverse()
    tr, tp = middle[0], middle[-1]
    assert colors[tr] == colors[tp] == 1 and tr in selected and tp in selected
    arm_r = rpath[rpath.index(tr):] + [ID['w']]
    arm_p = ppath[ppath.index(tp):] + [ID['w']]
    cycle = middle + arm_p[1:] + list(reversed(arm_r))[1:-1]
    assert len(cycle) == len(set(cycle)) and not set(cycle) & FRAME
    assert all(g.has_edge(v, w) for v, w in zip(cycle, cycle[1:]+cycle[:1]))
    lengths = [len(path)-1 for path in (middle, arm_r, arm_p)]
    assert all(n >= 2 and n % 2 == 0 for n in lengths)
    assert len(cycle) == sum(lengths) and len(cycle) >= 6 and len(cycle) % 2 == 0
    return dict(first_frame_path=gamma, R=rpath, P=ppath, consecutive_hits=[tr, tp],
                middle=middle, R_to_w=arm_r, P_to_w=arm_p,
                even_segment_lengths=lengths, internal_even_cycle=cycle)


def transition(g, colors, states):
    proper(g, colors)
    assert edges(g.subgraph(FRAME)) == [[1, 2], [2, 3], [3, 4]]
    assert nx.is_connected(g.subgraph(set(g)-FRAME))
    assert set(g[0]) == {ID['w'], ID['b']}
    assert all(g.degree[v] <= 4 for v in set(g)-FRAME)
    selected = set(nx.node_connected_component(g.subgraph(v for v in g if colors[v] in (0, 1)), 0))
    assert selected & FRAME == {0, 1, 2}
    raw = {v: 1-colors[v] if v in selected else colors[v] for v in g}
    proper(g, raw)
    normalized = {v: {0: 1, 1: 0, 2: 2, 3: 3}[c] for v, c in raw.items()}
    for c, number in ((colors, 397), (normalized, 330)):
        assert [c[v] for v in range(5)] == states[number]['row']
        assert [partition(g, c, pair, True) for pair in PAIRS] == states[number]['partitions']
    h2 = g.subgraph(v for v in g if v != 1 and raw[v] in (0, 2))
    b3 = set(nx.node_connected_component(h2, 3))
    assert set(g[0]) & b3 == {ID['w']}
    assert set(g[ID['w']]) == {0, ID['p'], ID['q'], ID['r']}
    assert set(g[ID['w']]) & selected == {0}
    j = g.subgraph(set(g)-{0, ID['w']})
    sprime = selected - {0, ID['w']}
    assert nx.is_connected(j.subgraph(sprime))
    stars = {d: sorted(v for v in sprime-FRAME
                        if Counter(colors[n] for n in g[v]) == Counter([0, 0, d, d])) for d in (2, 3)}
    assert ID['t2'] in stars[2] and ID['t3'] in stars[3]
    for d in (2, 3):
        remainder = j.subgraph(sprime-set(stars[d]))
        assert ID['b'] not in remainder or not (set(nx.node_connected_component(remainder, ID['b'])) & {1, 2})
    # This control is in the frame-1 cut branch.
    assert not nx.has_path(j.subgraph(sprime-{1}), ID['b'], 2)
    new13 = partition(g, raw, (1, 3))
    assert not any(2 in cc and 4 in cc for cc in new13)
    return dict(selected=sorted(selected), old_colors=[colors[v] for v in sorted(g)],
                new_raw_colors=[raw[v] for v in sorted(g)],
                old_partitions=[partition(g, colors, p, True) for p in PAIRS],
                normalized_new_partitions=[partition(g, normalized, p, True) for p in PAIRS],
                B3=sorted(b3), stars=stars, new13_components=new13,
                even_cycle=even_cycle(g, colors, raw, selected))


def augmented(g):
    k = g.copy()
    k.add_edges_from([(0, 1), (0, 4)])
    apex = max(g)+1
    k.add_edges_from((apex, v) for v in range(5))
    return k, apex


def embedding(g, saved=None):
    k, apex = augmented(g)
    if saved is None:
        ok, emb = nx.check_planarity(k)
        assert ok
    else:
        emb = nx.PlanarEmbedding()
        emb.set_data({int(v): neighbors for v, neighbors in saved.items()})
    emb.check_structure()  # Rotation/Euler verification, not planarity search.
    assert set(emb) == set(k) and edges(emb.to_undirected()) == edges(k)
    rot = {v: list(emb.neighbors_cw_order(v)) for v in sorted(k)}
    # Restrict to K and then J; retain the exact corners of deleted edges.
    krot = {v: [w for w in ns if w != apex] for v, ns in rot.items() if v != apex}
    deleted = {0, ID['w']}
    jrot = {v: [w for w in ns if w not in deleted] for v, ns in krot.items() if v not in deleted}
    je = nx.PlanarEmbedding(); je.set_data(jrot); je.check_structure()
    if je.traverse_face(1, 2)[:4] != [1, 2, 3, 4]:
        krot = {v: list(reversed(ns)) for v, ns in krot.items()}
        jrot = {v: list(reversed(ns)) for v, ns in jrot.items()}
        je = nx.PlanarEmbedding(); je.set_data(jrot); je.check_structure()
    face = je.traverse_face(1, 2)
    assert face[:4] == [1, 2, 3, 4]
    markers = {}
    for name in ('1', '4', 'b', 'p', 'q', 'r'):
        v = ID[name]; removed = 0 if name in ('1', '4', 'b') else ID['w']
        ns = krot[v]; i = ns.index(removed)
        # Face successor uses the counterclockwise predecessor of the incoming edge.
        incoming = ns[(i+1) % len(ns)]
        assert incoming not in deleted
        markers[incoming, v] = name
    seen = []
    for v, w in zip(face, face[1:]+face[:1]):
        if (v, w) in markers:
            seen.append(markers[v, w])
    assert len(seen) == 6
    i = seen.index('1'); seen = seen[i:]+seen[:i]
    assert seen == ['1', '4', 'b', 'r', 'p', 'q']
    return dict(apex_rotation=rot, inherited_J_face=face, corner_order=seen,
                corner_incoming_darts={name: list(dart) for dart, name in markers.items()})


def find_coloring(g, row):
    colors = dict(enumerate(row))
    def visit():
        if len(colors) == len(g):
            return dict(colors)
        options = {v: sorted(set(range(4)) - {colors[w] for w in g[v] if w in colors})
                   for v in g if v not in colors}
        v = min(options, key=lambda w: (len(options[w]), w))
        for c in options[v]:
            colors[v] = c
            found = visit()
            if found is not None:
                return found
            del colors[v]
        return None
    return visit()


def build(saved=None):
    upstream = json.loads(UPSTREAM.read_text())
    for name, digest in upstream['input_sha256'].items():
        assert sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
    states = json.loads(CROSS.read_text())['abstract']['states']
    small, small_c = seed()
    base, base_c = seed(True)
    full, gadgets = complete(base)
    full_c = lift(base_c, gadgets)
    assert len(gadgets) == 8 and len(full)-5 == 60
    assert all(full.degree[v] == 4 for v in set(full)-FRAME)
    records = {}
    for name, g, c in [('seed', small, small_c), ('patched', base, base_c), ('degree4', full, full_c)]:
        emb = embedding(g, saved['graphs'][name]['embedding']['apex_rotation'] if saved else None)
        records[name] = dict(vertices=sorted(g), edges=edges(g), inner_vertices=len(g)-5,
                             embedding=emb, transition=transition(g, c, states))
    rows = sorted({normalize(row) for row in product(range(4), repeat=5)
                   if all(row[i] != row[i+1] for i in (1, 2, 3))})
    assert len(rows) == 19
    witnesses = []
    for i, row in enumerate(rows):
        c = dict(enumerate(saved['all_open_rows'][i]['patched_colors'])) if saved else find_coloring(base, row)
        assert c is not None and tuple(c[v] for v in range(5)) == row
        proper(base, c)
        proper(small, {v: c[v] for v in small})
        extension = lift(c, gadgets); proper(full, extension)
        witnesses.append(dict(row=row, patched_colors=[c[v] for v in sorted(base)],
                              degree4_colors=[extension[v] for v in sorted(full)]))
    subdivisions = []
    for bits in product((0, 1), repeat=3):
        g, c = seed()
        split = []
        for active, (a, b, new_colors) in zip(bits, [('t3', 'c', [0, 1]),
                                                    ('t3', 'r', [3, 1]),
                                                    ('t2', 'p', [2, 0])]):
            if not active:
                continue
            u, v = ID[a], ID[b]
            x, y = len(g), len(g)+1
            g.remove_edge(u, v); g.add_edges_from([(u, x), (x, y), (y, v)])
            c[x], c[y] = new_colors
            split.append(dict(old_edge=[u, v], replacement=[u, x, y, v], new_colors=new_colors))
        proper(g, c)
        selected = set(nx.node_connected_component(g.subgraph(v for v in g if c[v] in (0, 1)), 0))
        raw = {v: 1-c[v] if v in selected else c[v] for v in g}
        proper(g, raw)
        result = even_cycle(g, c, raw, selected)
        assert len(result['internal_even_cycle']) == 6+2*sum(bits)
        subdivisions.append(dict(scope='Even-cycle lemma only; subdivisions need not preserve profile 397.',
                                 subdivisions=split, edges=edges(g), old_colors=[c[v] for v in sorted(g)],
                                 selected=sorted(selected), even_cycle=result))
    # Exhaust all possible anchor colors for the universal one-vertex gadget.
    local_checks = []
    first = gadgets[0]
    local = full.subgraph([first['anchor'], *first['vertices']])
    for anchor_color in range(4):
        c = lift({first['anchor']: anchor_color}, [first]); proper(local, c)
        local_checks.append(dict(anchor_color=anchor_color, colors=[c[v] for v in sorted(local)]))
    inputs = {UPSTREAM, CROSS, Path(__file__).resolve()}
    inputs.update(ROOT / p for p in upstream['input_sha256'])
    return dict(schema=1, scope='Explicit disk realization of one 397->330 transition, not of sector mask 3903.',
                generation='Three NetworkX 3.5 apex rotations; 19 color witnesses on one explicit patched graph. Check mode performs neither search.',
                input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in sorted(inputs)},
                names=ID, graphs=records, gadgets=gadgets, gadget_color_controls=local_checks,
                all_open_rows=witnesses, subdivision_controls=subdivisions,
                summary=dict(seed_inner=11, patched_inner=12, degree4_inner=60,
                             degree_completion_gadgets=8, checked_apex_rotations=3,
                             even_cycle_subdivision_controls=8,
                             realized_transition=[397, 330], corner_order=['1', '4', 'b', 'r', 'p', 'q'],
                             accepted_open_rows=19, twelve_bit_mask=4095, is_3903=False,
                             profile_deletions=0, inherited_profiles=603, fixed_point_recomputed=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    saved = json.loads(OUT.read_text()) if args.check else None
    result = build(saved)
    data = json.dumps(result, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == data, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__':
    main()
