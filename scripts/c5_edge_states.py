#!/usr/bin/env python3
"""Fixed-corpus dual pairing and Kempe transition audit; no new graph search.

uv run --with networkx==3.5 python scripts/c5_edge_states.py [--check]
NetworkX only recovers embeddings of old catalogue controls. Every cubic dual
uses an independently checked oriented triangulated disk. Nontriangular controls
are retained for the XOR audit, but are not silently completed.
"""
import argparse
from collections import Counter, defaultdict
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path

import networkx as nx

from c5_kempe_connectivity import CYCLE, PAIRS, adjacency, pair_components, swap, escape
from c5_kempe_screen import normalize
from c5_ab_swap_cube import orient_and_verify
from c5_complementary_cube import singleton_distances, singleton_of, route, encode, PATTERNS

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_cells/edge_states.json'
TYPE_PAIRS = ((1, 2), (1, 3), (2, 3))


def catalogue_faces(n, edges):
    g = nx.Graph()
    g.add_nodes_from(range(n + 1))
    g.add_edges_from(edges)
    g.add_edges_from((n, i) for i in range(5))
    ok, emb = nx.check_planarity(g)
    assert ok
    seen, faces = set(), []
    for u, v in emb.edges():
        if (u, v) not in seen:
            f = emb.traverse_face(u, v, seen)
            if n not in f:
                faces.append(tuple(f))
    if any(len(f) != 3 for f in faces):
        return None
    # Choose the boundary orientation 0,1,2,3,4.
    arcs = {(f[i], f[(i + 1) % 3]) for f in faces for i in range(3)}
    if (0, 1) not in arcs:
        faces = [tuple(reversed(f)) for f in faces]
    return orient_and_verify(n, edges, faces)


def corpus():
    corner = json.loads((ROOT / 'artifacts/c5_cells/corner_disks.json').read_text())
    for s in corner['survivors']:
        yield dict(name=f"survivor-{s['disk']}", n=s['n'], edges=s['edges'],
                   faces=s['oriented_faces'], starts=[x['coloring'] for x in s['states']])
    comp = json.loads((ROOT / 'artifacts/c5_cells/complementary_cube.json').read_text())
    for j, d in enumerate(comp['errera_family']['disks']):
        edges = [tuple(e) for e in d['edges']]
        yield dict(name=f'errera-{j}', n=16, edges=edges,
                   faces=catalogue_faces(16, edges), starts=[])
    cat = json.loads((ROOT / 'artifacts/c5_cells/cells.json').read_text())
    for m, d in sorted(cat['cells'].items(), key=lambda kv: int(kv[0])):
        edges = sorted({tuple(sorted(e)) for e in [*CYCLE, *d['edges']]})
        n = d['k_eff'] + 5
        yield dict(name=f'catalogue-{m}', n=n, edges=edges,
                   faces=catalogue_faces(n, edges), starts=[])


class Dual:
    def __init__(self, n, edges, faces):
        self.edges = edges
        self.faces = orient_and_verify(n, edges, faces)
        self.f = len(faces)
        incidence = defaultdict(list)
        for j, face in enumerate(faces):
            for i in range(3):
                incidence[tuple(sorted((face[i], face[(i + 1) % 3])))].append(j)
        for i, e in enumerate(CYCLE):
            incidence[tuple(sorted(e))].append(self.f + i)
        self.ends = [tuple(incidence[e]) for e in edges]
        assert all(len(e) == 2 for e in self.ends)

    @lru_cache(None)
    def systems(self, c):
        types = tuple(c[u] ^ c[v] for u, v in self.edges)
        assert all({c[f[0]] ^ c[f[1]], c[f[1]] ^ c[f[2]],
                    c[f[2]] ^ c[f[0]]} == {1, 2, 3} for f in self.faces)
        answer = []
        for a, b in TYPE_PAIRS:
            adj = [[] for _ in range(self.f + 5)]
            for j, (u, v) in enumerate(self.ends):
                if types[j] in (a, b):
                    adj[u].append((v, j))
                    adj[v].append((u, j))
            assert all(len(adj[v]) == 2 for v in range(self.f))
            unseen = {v for v in range(self.f + 5) if adj[v]}
            parts = []
            while unseen:
                root = min(unseen)
                unseen.remove(root)
                queue, es = [root], set()
                for u in queue:
                    for v, e in adj[u]:
                        es.add(e)
                        if v in unseen:
                            unseen.remove(v)
                            queue.append(v)
                terminals = tuple(sorted(v - self.f for v in queue if v >= self.f))
                assert len(terminals) in (0, 2)
                if not terminals:
                    assert len(es) % 2 == 0
                parts.append((terminals, tuple(sorted(es))))
            pairings = sorted(t for t, _ in parts if t)
            for i, j in pairings:
                for k, l in pairings:
                    assert not (i < k < j < l)
            answer.append(tuple(sorted(parts)))
        return tuple(answer)

    def state(self, c, cycles=False):
        systems = self.systems(c)
        w = tuple(c[i] ^ c[(i + 1) % 5] for i in range(5))
        assert sorted(Counter(w).values()) == [1, 1, 3]
        t = (w, *(tuple(t for t, _ in s if t) for s in systems))
        return (*t, tuple(sum(not t for t, _ in s) for s in systems)) if cycles else t

    def boundary_partition(self, c, missing):
        s = self.systems(c)[TYPE_PAIRS.index(tuple(x for x in (1, 2, 3) if x != missing))]
        arcs = [t for t, _ in s if t]
        # Terminal i is on primal edge i--i+1. The open arc i..j contains
        # boundary vertices i+1,...,j; only this ordered side convention is used.
        sides = [tuple(i < v <= j for i, j in arcs) for v in range(5)]
        return {frozenset(v for v in range(5) if sides[v] == x) for x in sides}


def audit_graph(g):
    edges = sorted(tuple(e) for e in g['edges'])
    adj = adjacency(g['n'], edges)
    colours, dist, step = singleton_distances(adj, g['n'])
    colours = sorted(colours)
    index = {c: j for j, c in enumerate(colours)}
    dual = Dual(g['n'], edges, g['faces']) if g['faces'] else None
    counts, cut_shapes = Counter(), Counter()
    groups, enriched = defaultdict(list), defaultdict(list)
    successors, records = {}, []
    multi_cut = None
    trace_hash = sha256()
    fibre_states = defaultdict(set)
    for c in colours:
        if dual:
            groups[dual.state(c)].append(c)
            enriched[dual.state(c, True)].append(c)
            if len(set(c[:5])) == 4:
                fibre_states[(c[:5], dist.get(c) != 1)].add(dual.state(c))
            # Independent primal check of the boundary partition read off the
            # dual noncrossing arcs, for all three complementary splits.
            predicted_forbidden = False
            for k in (1, 2, 3):
                actual = set()
                for p in PAIRS:
                    if p[0] ^ p[1] == k:
                        actual |= {frozenset(s & set(range(5)))
                                   for s in pair_components(adj, c, p) if s & set(range(5))}
                predicted = dual.boundary_partition(c, k)
                assert actual == predicted
                for trace in predicted:
                    v = min(trace)
                    p = (c[v], c[v] ^ k)
                    assert all(c[u] in p for u in trace)
                    predicted_forbidden |= singleton_of(swap(c[:5], trace, p)) in (1, 3, 4)
                counts['boundary_partition_checks'] += 1
            if singleton_of(c) not in (1, 3, 4):
                assert predicted_forbidden == (dist.get(c) == 1)
        outcomes = set()
        for p in PAIRS:
            for block in sorted(pair_components(adj, c, p), key=min):
                d = swap(c, block, p)
                cut = {j for j, (u, v) in enumerate(edges) if (u in block) != (v in block)}
                k = p[0] ^ p[1]
                before = tuple(c[u] ^ c[v] for u, v in edges)
                after = tuple(d[u] ^ d[v] for u, v in edges)
                assert after == tuple(t ^ k if j in cut else t for j, t in enumerate(before))
                assert all(before[j] != k for j in cut)
                counts['swaps'] += 1
                trace_hash.update((json.dumps([c, p, sorted(block), d, sorted(cut)],
                                              separators=(',', ':')) + '\n').encode())
                if not dual:
                    continue
                # Cut is a union of WHOLE components of the other-two-type system.
                si = TYPE_PAIRS.index(tuple(x for x in (1, 2, 3) if x != k))
                parts = dual.systems(c)[si]
                selected = [j for j, (_, es) in enumerate(parts) if set(es) & cut]
                assert set().union(*(set(parts[j][1]) for j in selected)) == cut
                assert dual.state(c)[si + 1] == dual.state(d)[si + 1]
                counts['dual_swaps'] += 1
                shape = (sum(bool(parts[j][0]) for j in selected),
                         sum(not parts[j][0] for j in selected))
                cut_shapes[str(shape)] += 1
                if len(selected) > 1 and multi_cut is None:
                    multi_cut = dict(coloring=c, pair=p, component=sorted(block),
                                     cut_edges=[edges[j] for j in sorted(cut)],
                                     paths=shape[0], cycles=shape[1])
                outcomes.add(dual.state(d))  # actual colors: NO normalization here
                if g['name'].startswith('survivor'):
                    nd = normalize(d)
                    # Exact raw output can be reconstructed from canonical target
                    # and its global color map. Thus no alignment is discarded.
                    palette = tuple(next(d[v] for v in range(len(d)) if nd[v] == t)
                                    if t in nd else -1 for t in range(4))
                    records.append([index[c], list(p), sorted(block), index[nd], palette,
                                    selected, [i for i in range(3)
                                               if dual.state(c)[i + 1] != dual.state(d)[i + 1]]])
        successors[c] = frozenset(outcomes)

    def collision(grouping, observation):
        for state, cs in sorted(grouping.items()):
            first = cs[0]
            other = next((c for c in cs[1:] if observation(c) != observation(first)), None)
            if other is not None:
                result = dict(state=state, colorings=[first, other],
                              distances=[dist.get(first), dist.get(other)])
                if observation is not distance:
                    a, b = successors[first], successors[other]
                    result['successor_only_first'] = sorted(a - b)
                    result['successor_only_second'] = sorted(b - a)
                return result
        return None

    def distance(c):
        return dist.get(c)

    collisions = dict(distance=collision(groups, distance),
                      successors=collision(groups, lambda c: successors[c]),
                      cycle_counts_distance=collision(enriched, distance),
                      cycle_counts_successors=collision(enriched, lambda c: successors[c])) if dual else {}
    # Boundary arcs must determine whether a one-step forbidden singleton exists.
    if dual:
        assert all(len({dist.get(c) == 1 for c in cs}) == 1 for cs in groups.values())
    escapes = []
    for start in g['starts']:
        c = tuple(start)
        rows = []
        for move in route(adj, c, dist, step)['moves']:
            # Stored BFS routes use a normalized frame at each step. Translate
            # their named pair back into the continuous raw frame of this route.
            nc = normalize(c)
            palette = {nc[v]: c[v] for v in range(len(c))}
            p = tuple(palette[t] for t in move['pair'])
            block = set(move['component'])
            assert frozenset(block) in pair_components(adj, c, p)
            d = swap(c, block, p)
            assert normalize(tuple(move['coloring'])) == normalize(d)
            rows.append(dict(before=c, pair=p, component=sorted(block), after=d,
                             state_before=dual.state(c), state_after=dual.state(d),
                             changed_pairings=[i for i in range(3)
                                               if dual.state(c)[i + 1] != dual.state(d)[i + 1]],
                             distance_before=dist[normalize(c)], distance_after=dist[normalize(d)]))
            c = d
        escapes.append(dict(start=start, moves=rows, singleton=singleton_of(c)))
    result = dict(name=g['name'], n=g['n'], edges=edges, faces=g['faces'],
                  colorings=len(colours), states=len(groups), counts=dict(counts),
                  transition_trace_sha256=trace_hash.hexdigest(),
                  four_fibre_states=[dict(boundary=b, no_one_step_escape=safe,
                                          states=sorted(states))
                                     for (b, safe), states in sorted(fibre_states.items())],
                  cut_shapes=dict(sorted(cut_shapes.items())), multi_cut=multi_cut,
                  collisions=collisions, escapes=escapes)
    if records:
        result.update(coloring_table=colours, transitions=records)
    if dual:
        dual.systems.cache_clear()
    return result


def boundary_obligations():
    """Exact forbidden component traces for all five four-color boundary fibres.

    A trace is the intersection of one maximal primal two-color component with
    the boundary. We list both complementary traces when they have the same
    effect up to a global transposition; we do not assume traces realizable.
    """
    rows = []
    for b in PATTERNS:
        if len(set(b)) != 4:
            continue
        forbidden = []
        for p in PAIRS:
            vertices = [i for i in range(5) if b[i] in p]
            for mask in range(1, 1 << len(vertices)):
                trace = {v for j, v in enumerate(vertices) if mask >> j & 1}
                d = swap(b, trace, p)
                if (all(d[u] != d[v] for u, v in CYCLE)
                        and singleton_of(d) in (1, 3, 4)):
                    forbidden.append(dict(pair=p, trace=sorted(trace),
                                          singleton=singleton_of(d)))
        rows.append(dict(boundary=b, repeated_pair=[i for i in range(5) if b.count(b[i]) == 2],
                         forbidden_component_traces=forbidden))
    assert len(rows) == 5
    return rows


def report():
    graphs = [audit_graph(g) for g in corpus()]
    # Recheck the decisive same-class witness with the earlier, fully labeled
    # single-source BFS, independently of the normalized multi-source distances.
    errera = next(g for g in graphs if g['name'] == 'errera-0')
    witness = errera['collisions']['cycle_counts_distance']
    c, d = map(tuple, witness['colorings'])
    adj = adjacency(16, errera['edges'])
    block = frozenset((5, 6, 8, 10, 13, 14))
    assert block in pair_components(adj, c, (2, 3))
    assert swap(c, block, (2, 3)) == d
    raw_routes = [escape(adj, x) for x in (c, d)]
    assert [len(r['moves']) for r in raw_routes] == witness['distances'] == [3, 2]
    totals = Counter()
    for g in graphs:
        totals.update(g['counts'])
    summary = dict(graphs=len(graphs), cubic_graphs=sum(g['faces'] is not None for g in graphs),
                   colorings=sum(g['colorings'] for g in graphs), **totals,
                   collisions={k: [g['name'] for g in graphs if g['collisions'].get(k)]
                               for k in ('distance', 'successors', 'cycle_counts_distance',
                                         'cycle_counts_successors')})
    files = [Path(__file__), *(ROOT / 'scripts' / f for f in
             ('c5_kempe_connectivity.py', 'c5_kempe_screen.py', 'c5_ab_swap_cube.py',
              'c5_complementary_cube.py', 'c5_adjacent_singleton_counts.py')),
             *(ROOT / 'artifacts/c5_cells' / f for f in
               ('cells.json', 'corner_disks.json', 'complementary_cube.json'))]
    return dict(trust='Finite fixed-corpus audit; disk topology and general lemmas are paper arguments, not Lean.',
                networkx=nx.__version__,
                hashes={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in files},
                types={'1': 'alpha=AB|CD', '2': 'beta=AC|BD', '3': 'gamma=AD|BC'},
                state_columns=['boundary_edge_word', 'alpha_beta', 'alpha_gamma', 'beta_gamma'],
                transition_columns=['source_coloring_index', 'pair', 'component',
                                    'normalized_target_index', 'raw_target_palette',
                                    'selected_cut_system_components', 'changed_pairing_indices'],
                boundary_obligations=boundary_obligations(),
                same_class_regression=dict(graph='errera-0', colorings=[c, d],
                                           pair=[2, 3], component=sorted(block),
                                           independently_labeled_bfs_routes=raw_routes),
                summary=summary, graphs=graphs)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = report()
    content = encode(result) + '\n'
    if args.check:
        assert OUT.read_text() == content, 'Certificate differs; inspect before regenerating.'
    else:
        OUT.write_text(content)
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__':
    main()
