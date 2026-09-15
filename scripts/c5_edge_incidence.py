#!/usr/bin/env python3
"""Fixed-corpus counterexamples to compressed joint dual incidence states.

uv run --with networkx==3.5 python scripts/c5_edge_incidence.py [--check]
Cycle names are quotiented jointly, never independently in each matrix.
"""
import argparse
from collections import Counter, defaultdict
from functools import lru_cache
from hashlib import sha256
from itertools import permutations, product, combinations
import json
from pathlib import Path

from c5_edge_states import Dual, TYPE_PAIRS
from c5_kempe_connectivity import adjacency, PAIRS, pair_components, swap, escape
from c5_complementary_cube import singleton_distances, encode

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'artifacts/c5_cells/edge_states.json'
OUT = ROOT / 'artifacts/c5_cells/edge_incidence.json'
LEVELS = ('edge_support', 'edge_counts', 'face_counts')


def incidence_states(dual, c):
    systems = dual.systems(c)
    owners = [{e: j for j, (_, es) in enumerate(s) for e in es} for s in systems]
    matrices = {}
    for a, b in combinations(range(3), 2):
        counts = Counter((owners[a][e], owners[b][e]) for e in owners[a].keys() & owners[b].keys())
        matrices[a, b] = counts
    faces = Counter()
    face_edges = [{j for j, ends in enumerate(dual.ends) if f in ends} for f in range(dual.f)]
    for es in face_edges:
        ids = []
        for owner in owners:
            hits = {owner[e] for e in es if e in owner}
            assert len(hits) == 1
            ids.append(next(iter(hits)))
        faces[tuple(ids)] += 1
    # Each internal shared edge touches two faces, each boundary edge one.
    for (a, b), counts in matrices.items():
        marginal = Counter()
        for ids, count in faces.items():
            marginal[ids[a], ids[b]] += count
        boundary = Counter((owners[a][e], owners[b][e])
                           for e in owners[a].keys() & owners[b].keys()
                           if any(v >= dual.f for v in dual.ends[e]))
        assert marginal == Counter({ij: 2 * n - boundary[ij] for ij, n in counts.items()})
    orders = []
    for s in systems:
        cycles = [j for j, (t, _) in enumerate(s) if not t]
        paths = sorted((j for j, (t, _) in enumerate(s) if t), key=lambda j: s[j][0])
        orders.append([tuple(paths) + p for p in permutations(cycles)])
    best = [None] * 3
    # This minimum is over a SINGLE joint renaming of each system's cycles.
    for order in product(*orders):
        labels = tuple(tuple(systems[i][j][0] for j in order[i]) for i in range(3))
        weights = tuple(tuple(matrices[a, b][i, j] for i in order[a] for j in order[b])
                        for a, b in combinations(range(3), 2))
        triples = tuple(faces[i, j, k] for i in order[0] for j in order[1] for k in order[2])
        prefix = (dual.state(c)[0], labels)
        candidates = ((*prefix, tuple(tuple(int(n > 0) for n in m) for m in weights)),
                      (*prefix, weights), (*prefix, weights, triples))
        for level, candidate in enumerate(candidates):
            if best[level] is None or candidate < best[level]:
                best[level] = candidate
    return tuple(best)


def audit(g):
    edges = [tuple(e) for e in g['edges']]
    dual = Dual(g['n'], edges, g['faces'])
    adj = adjacency(g['n'], edges)
    colours, dist, _ = singleton_distances(adj, g['n'])
    groups = [defaultdict(list) for _ in LEVELS]
    successors = {}
    observe_states = lru_cache(None)(lambda c: incidence_states(dual, c))
    for c in sorted(colours):
        states = observe_states(c)
        for grouping, state in zip(groups, states):
            grouping[state].append(c)
        targets = [swap(c, block, pair) for pair in PAIRS for block in pair_components(adj, c, pair)]
        successors[c] = tuple(frozenset(observe_states(d)[i] for d in targets) for i in range(3))
    results = {}
    for li, (level, grouping) in enumerate(zip(LEVELS, groups)):
        collisions = {}
        for kind in ('distance', 'successors', 'safe_successors'):
            for state, cs in sorted(grouping.items()):
                if kind == 'safe_successors':
                    cs = [c for c in cs if dist.get(c) is None or dist[c] > 1]
                if not cs:
                    continue
                first = cs[0]
                observe = (lambda c: dist.get(c)) if kind == 'distance' else (lambda c: successors[c][li])
                other = next((c for c in cs[1:] if observe(c) != observe(first)), None)
                if other is not None:
                    assert first[:5] == other[:5]
                    collisions[kind] = dict(colorings=[first, other], state=state,
                                            distances=[dist.get(first), dist.get(other)],
                                            successor_only_first=sorted(successors[first][li] - successors[other][li]),
                                            successor_only_second=sorted(successors[other][li] - successors[first][li]))
                    break
        results[level] = dict(states=len(grouping), collisions=collisions)
    dual.systems.cache_clear()
    return dict(name=g['name'], n=g['n'], colorings=len(colours), levels=results)


def report():
    source = json.loads(SOURCE.read_text())
    graphs = [g for g in source['graphs'] if g['faces'] is not None]
    errera = next(g for g in graphs if g['name'] == 'errera-0')
    dual = Dual(errera['n'], [tuple(e) for e in errera['edges']], errera['faces'])
    cs = [tuple(c) for c in source['same_class_regression']['colorings']]
    states = [incidence_states(dual, c) for c in cs]
    regression = dict(graph=errera['name'], colorings=cs,
                      distinguished={k: states[0][i] != states[1][i] for i, k in enumerate(LEVELS)},
                      observations={k: [s[i] for s in states] for i, k in enumerate(LEVELS)})
    dual.systems.cache_clear()
    rows = [audit(g) for g in graphs]
    summary = dict(graphs=len(rows), colorings=sum(g['colorings'] for g in rows),
                   regression_distinguished=regression['distinguished'],
                   collision_graphs={level: {kind: sum(kind in g['levels'][level]['collisions'] for g in rows)
                                             for kind in ('distance', 'successors', 'safe_successors')}
                                     for level in LEVELS})
    witnesses = {}
    for level in LEVELS:
        witnesses[level] = {}
        for kind in ('distance', 'successors', 'safe_successors'):
            candidates = [r for r in rows if kind in r['levels'][level]['collisions']]
            if not candidates:
                continue
            r = min(candidates, key=lambda r: (r['n'], r['name']))
            g = next(g for g in graphs if g['name'] == r['name'])
            w = r['levels'][level]['collisions'][kind]
            adj = adjacency(g['n'], g['edges'])
            routes = [escape(adj, tuple(c)) for c in w['colorings']]
            assert [None if x is None else len(x['moves']) for x in routes] == w['distances']
            witnesses[level][kind] = dict(graph=g['name'], n=g['n'], edges=g['edges'],
                                         faces=g['faces'], **w, independent_labeled_routes=routes)
    files = [Path(__file__), SOURCE, *(ROOT / p for p in source['hashes'] if p.startswith('scripts/'))]
    return dict(trust='Exact fixed-corpus Python audit; no general sufficiency or minimality theorem, no new Lean.',
                hashes={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in files},
                successor_observation='Same candidate incidence state in the unchanged raw color frame; action names forgotten.',
                summary=summary, regression=regression, witnesses=witnesses, graphs=rows)


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
