#!/usr/bin/env python3
"""AB-only closure, signed blocker predicates, and a fixed Errera disk control.

python3 scripts/c5_ab_swap_cube.py [--check]
No graph catalogue search. Finite replay and paper topology, not Lean proofs.
"""
import argparse
from collections import deque
from hashlib import sha256
import json
from pathlib import Path

from c5_kempe_connectivity import (
    CAT, CYCLE, THREE, adjacency, colorings, component, components,
    escape, pair_components, swap,
)
from c5_kempe_screen import normalize
from c5_kempe_class_counts import classes

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_cells/ab_swap_cube.json'
BOUNDARY = (0, 1, 0, 2, 3)
SOURCE = 'https://raw.githubusercontent.com/sagemath/sage/10.6/src/sage/graphs/generators/smallgraphs.py'
# Edge data from Sage 10.6 ErreraGraph. Delete old vertex 0; keep cyclic order.
ERRERA = {0: [1, 7, 14, 15, 16], 1: [2, 9, 14, 15], 2: [3, 8, 9, 10, 14],
          3: [4, 9, 10, 11], 4: [5, 10, 11, 12], 5: [6, 11, 12, 13],
          6: [7, 8, 12, 13, 16], 7: [13, 15, 16], 8: [10, 12, 14, 16],
          9: [11, 13, 15], 10: [12], 11: [13], 13: [15], 14: [16]}
NEW_TO_OLD = (1, 14, 16, 7, 15, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13)
START = (0, 1, 0, 2, 3, 2, 3, 0, 3, 1, 3, 1, 1, 2, 2, 0)
FACES = ((0, 1, 5), (0, 4, 11), (0, 5, 11), (1, 2, 10), (1, 5, 10),
         (2, 3, 9), (2, 9, 10), (3, 4, 15), (3, 9, 15), (4, 11, 15),
         (5, 6, 11), (5, 6, 12), (5, 10, 12), (6, 7, 12), (6, 7, 13),
         (6, 11, 13), (7, 8, 13), (7, 8, 14), (7, 12, 14), (8, 9, 14),
         (8, 9, 15), (8, 13, 15), (9, 10, 14), (10, 12, 14), (11, 13, 15))


def path(adj, allowed, source, target):
    if source not in allowed or target not in allowed:
        return None
    previous = {source: None}
    queue = deque([source])
    while queue:
        u = queue.popleft()
        if u == target:
            result = []
            while u is not None:
                result.append(u)
                u = previous[u]
            return result[::-1]
        for v in sorted(adj[u] & allowed):
            if v not in previous:
                previous[v] = u
                queue.append(v)
    return None


def observe(adj, c):
    assert c[:5] == BOUNDARY
    blockers = [path(adj, {v for v, color in enumerate(c) if color in (1, r)}, 1, t)
                for r, t in ((2, 3), (3, 4))]
    result = dict(coloring=c, blocker_paths=blockers, blockers=all(blockers),
                  interface=[], new_links=[False, False], gate=False, full=False)
    if not all(blockers):
        return result
    s, t = component(adj, c, (0, 2), 0), component(adj, c, (0, 3), 2)
    assert s & set(range(5)) == {0} and t & set(range(5)) == {2}
    interface = sorted((u, v) for u in s if c[u] == 2
                       for v in adj[u] & t if c[v] == 3)
    cs, ct = swap(c, s, (0, 2)), swap(c, t, (0, 3))
    links = [4 in component(adj, cs, (0, 3), 2),
             3 in component(adj, ct, (0, 2), 0)]
    link_paths = [path(adj, {v for v, color in enumerate(cs) if color in (0, 3)}, 2, 4),
                  path(adj, {v for v, color in enumerate(ct) if color in (0, 2)}, 0, 3)]
    assert links == [p is not None for p in link_paths]
    if any(links):
        assert interface
    result.update(S=sorted(s), T=sorted(t), interface=interface,
                  new_links=links, new_link_paths=link_paths,
                  gate=bool(interface), full=all(links))
    return result


def cube(adj, start, pairs=((0, 1),)):
    """Full labeled split orbit, quotient only by one global color permutation.

    Components stay unchanged under swaps within these disjoint color pairs.
    Exhausting bit subsets therefore covers sequences of arbitrary length.
    """
    entries = [(pair, s) for pair in pairs
               for s in sorted(pair_components(adj, start, pair), key=lambda s: min(s))]
    raw = set()
    for bits in range(1 << len(entries)):
        c = start
        selected = {v for j, (_, s) in enumerate(entries) if bits >> j & 1 for v in s}
        for j, (pair, s) in enumerate(entries):
            if bits >> j & 1:
                assert s in pair_components(adj, c, pair)
                c = swap(c, s, pair)
        assert all(c[u] != c[v] for u in range(len(adj)) for v in adj[u])
        for pair in pairs:
            assert pair_components(adj, c, pair) == pair_components(adj, start, pair)
        if pairs == ((0, 1),):
            # Exact signed vertex-activation predicates, using the ORIGINAL graph.
            active_b = {v for v, color in enumerate(start)
                        if color in (0, 1) and (color ^ int(v in selected)) == 1}
            for r in (2, 3):
                allowed = active_b | {v for v, color in enumerate(start) if color == r}
                assert components(adj, allowed) == pair_components(adj, c, (1, r))
        raw.add(c)
    assert len(raw) == 1 << len(entries)
    normalized = sorted({normalize(c) for c in raw})
    assert all(c[:5] == BOUNDARY for c in normalized)
    assert len(raw) == len(normalized) * (1 << len(pairs))
    return dict(components=[dict(pair=p, vertices=sorted(s)) for p, s in entries],
                raw_size=len(raw), normalized_size=len(normalized),
                states=[observe(adj, c) for c in normalized])


def orient_and_verify(n, edges, faces):
    """Verify an orientable connected triangulated 2-manifold, one C5 boundary, chi=1.

    Its interpretation as a disk uses the standard surface theorem on paper.
    This is a fixed-complex certificate, not a general planarity oracle.
    """
    def arcs(f):
        return [(f[i], f[(i + 1) % 3]) for i in range(3)]
    oriented = {0: faces[0]}
    pending = [0]
    for i in pending:
        for u, v in arcs(oriented[i]):
            for j, f in enumerate(faces):
                if j in oriented or u not in f or v not in f:
                    continue
                oriented[j] = f if (v, u) in arcs(f) else (f[0], f[2], f[1])
                pending.append(j)
    assert len(oriented) == len(faces)
    result = [oriented[i] for i in range(len(faces))]
    directed = [e for f in result for e in arcs(f)]
    assert len(directed) == len(set(directed))
    assert {tuple(sorted(e)) for e in directed} == set(edges)
    assert {e for e in directed if e[::-1] not in directed} == set(CYCLE)
    assert n - len(edges) + len(faces) == 1
    for v in range(n):
        link_edges = [tuple(u for u in f if u != v) for f in faces if v in f]
        link = adjacency(n, link_edges)
        active = {u for e in link_edges for u in e}
        assert len(components(link, active)) == 1
        degrees = sorted(len(link[u]) for u in active)
        expected = [1, 1] + [2] * (len(active) - 2) if v < 5 else [2] * len(active)
        assert degrees == expected
    return result


def verify_route(adj, start, moves):
    c = start
    result = []
    for pair, vertices in moves:
        s = frozenset(vertices)
        assert s in pair_components(adj, c, pair)
        c = swap(c, s, pair)
        assert all(c[u] != c[v] for u in range(len(adj)) for v in adj[u])
        result.append(dict(pair=pair, component=sorted(s), coloring=c))
    b = c[:5]
    assert len(set(b)) == 3
    singleton = next(i for i in range(5) if b.count(b[i]) == 1)
    assert singleton not in (0, 2)
    return dict(singleton=singleton, moves=result)


def report():
    index = {old: new for new, old in enumerate(NEW_TO_OLD)}
    edges = sorted(tuple(sorted((index[u], index[v])))
                   for u, vs in ERRERA.items() for v in vs if u != 0 and v != 0)
    assert len(edges) == 40 and len(set(edges)) == 40
    adj = adjacency(16, edges)
    faces = orient_and_verify(16, edges, FACES)
    ab = cube(adj, START)
    assert ab['raw_size'] == 4 and ab['normalized_size'] == 2
    assert all(s['blockers'] and s['gate'] and s['full'] for s in ab['states'])
    assert sorted(len(s['interface']) for s in ab['states']) == [1, 3]
    fixed_paths = []
    for r, target in ((2, 3), (3, 4)):
        persistent = set.intersection(*({v for v, color in enumerate(s['coloring'])
                                        if color in (1, r)} for s in ab['states']))
        common_path = path(adj, persistent, 1, target)
        assert common_path is None
        fixed_paths.append(dict(pair=(1, r), persistent_vertices=sorted(persistent),
                                source_component=sorted(next(s for s in components(adj, persistent)
                                                             if 1 in s)),
                                target=target, common_path=None))
    split = cube(adj, START, ((0, 1), (2, 3)))
    assert split['raw_size'] == 16 and split['normalized_size'] == 4
    assert all(s['blockers'] for s in split['states'])
    assert sum(s['full'] for s in split['states']) == 2
    # CD first, then the prior two-move escape from an empty interface.
    cd_escape = verify_route(adj, START, [((2, 3), (5, 6, 8, 10, 13, 14)),
                                          ((0, 2), (0,)), ((0, 3), (2,))])
    shortest = escape(adj, START)
    assert shortest is not None and len(shortest['moves']) == 3
    verified = verify_route(adj, START, [(m['pair'], m['component']) for m in shortest['moves']])
    assert verified == shortest
    cs = classes(11, edges)
    assert len(cs) == 1 and cs[0]['size'] == 100
    support = sorted(i for i, j in THREE.items() if cs[0]['counts'][j])
    assert support == list(range(5))
    # Reuse the fixed existing witnesses; enumerate their AB cubes, not new graphs.
    catalog = json.loads(CAT.read_text())
    replay = []
    for mask, entry in sorted(catalog['cells'].items(), key=lambda p: int(p[0])):
        es = sorted({tuple(sorted(e)) for e in (*CYCLE, *entry['edges'])})
        ad = adjacency(5 + entry['k_eff'], es)
        seen = set()
        records = []
        for c in colorings(entry['k_eff'], es):
            if c[:5] != BOUNDARY or c in seen:
                continue
            orbit = cube(ad, c)
            seen.update(s['coloring'] for s in orbit['states'])
            records.append(dict(representative=c, states=orbit['normalized_size'],
                                all_blockers=all(s['blockers'] for s in orbit['states']),
                                all_gate=all(s['blockers'] and s['gate'] for s in orbit['states']),
                                all_full=all(s['blockers'] and s['full'] for s in orbit['states'])))
        replay.append(dict(mask=int(mask), extensions=len(seen), cubes=records))
    assert sum(r['extensions'] for r in replay) == 176
    assert not any(c['all_full'] for r in replay for c in r['cubes'])
    # Only toggling the boundary component misses relative states when r=3.
    small_adj = adjacency(7, [*CYCLE, (3, 5), (4, 6)])
    small_start = (*BOUNDARY, 0, 1)
    small = cube(small_adj, small_start)
    boundary_only = {normalize(small_start),
                     normalize(swap(small_start, component(small_adj, small_start, (0, 1), 0), (0, 1)))}
    assert len(boundary_only) == 2 and small['normalized_size'] == 4
    rejected_face = False
    try:
        orient_and_verify(16, edges, FACES[:-1])
    except AssertionError:
        rejected_face = True
    assert rejected_face
    files = [Path(__file__), CAT, ROOT / 'scripts/c5_kempe_connectivity.py',
             ROOT / 'scripts/c5_kempe_class_counts.py',
             ROOT / 'scripts/c5_adjacent_singleton_counts.py',
             ROOT / 'scripts/c5_kempe_screen.py']
    return dict(trust='Finite fixed-graph certificates plus paper cube and disk arguments; not Lean. AB-local invariance is not the global independent-singleton hypothesis.',
                hashes={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in files},
                fixed_graph=dict(source=SOURCE, source_function='ErreraGraph', deleted_vertex=0,
                                 new_to_old=NEW_TO_OLD, edges=edges, oriented_disk_faces=faces,
                                 start=START, ab_cube=ab, common_path_controls=fixed_paths,
                                 complementary_cube=split, cd_first_escape=cd_escape,
                                 shortest_escape=shortest, classes=cs, singleton_support=support),
                catalogue_replay=replay,
                negative_controls=dict(boundary_only_states=len(boundary_only),
                                       full_relative_states=small['normalized_size'],
                                       missing_face_rejected=rejected_face))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = report()
    encoded = json.dumps(result, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == encoded, 'Certificate differs; inspect before regeneration.'
    else:
        OUT.write_text(encoded)
    rows = result['catalogue_replay']
    print(json.dumps(dict(witnesses=len(rows), extensions=sum(r['extensions'] for r in rows),
                          cubes=sum(len(r['cubes']) for r in rows),
                          all_blockers_cubes=sum(c['all_blockers'] for r in rows for c in r['cubes']),
                          all_gate_cubes=sum(c['all_gate'] for r in rows for c in r['cubes']),
                          all_full_cubes=sum(c['all_full'] for r in rows for c in r['cubes']),
                          errera_ab_states=result['fixed_graph']['ab_cube']['normalized_size'],
                          errera_split_states=result['fixed_graph']['complementary_cube']['normalized_size'],
                          shortest_escape=len(result['fixed_graph']['shortest_escape']['moves'])), sort_keys=True))


if __name__ == '__main__':
    main()
