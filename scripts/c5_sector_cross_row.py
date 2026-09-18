#!/usr/bin/env python3
"""Finite cross-row partition closure and fixed-corpus actual Kempe orbits."""
import argparse
from collections import Counter, deque
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

import networkx as nx
from boundary_relations import normalize
from c5_sector_forced_connectivity import (
    FRAME, PAIRS, QUERIES, REJECTED, SOURCE, crossing, extract,
    observed_partition, path_certificate,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_sector_cross_row/observations.json'
ROWS = tuple(sorted({normalize(c) for c in product(range(4), repeat=5)
                     if all(c[u] != c[v] for u, v in FRAME)}))


def relabel(row):
    order = list(dict.fromkeys(row))
    order += [c for c in range(4) if c not in order]
    mapping = {c: i for i, c in enumerate(order)}
    return tuple(mapping[c] for c in row), mapping


def actions(row, profile):
    """Each result is an existential successor requirement, not an exact update."""
    for j, pair in enumerate(PAIRS):
        for bits in product((0, 1), repeat=len(profile[j])):
            target = list(row)
            for block, bit in zip(profile[j], bits):
                if bit:
                    for v in block:
                        target[v] = pair[1] if row[v] == pair[0] else pair[0]
            target, mapping = relabel(target)
            k = PAIRS.index(tuple(sorted(mapping[c] for c in pair)))
            yield (target, k, profile[j], profile[5-j])


def global_swap(row, profile, pair):
    """Swapping ALL components of one pair is an exact color permutation."""
    trans = {c: pair[1] if c == pair[0] else pair[0] if c == pair[1] else c
             for c in range(4)}
    target, mapping = relabel(tuple(trans[c] for c in row))
    result = [None] * 6
    for j, old_pair in enumerate(PAIRS):
        k = PAIRS.index(tuple(sorted(mapping[trans[c]] for c in old_pair)))
        result[k] = profile[j]
    return target, tuple(result)


def abstract_closure():
    states = []
    for row in ROWS:
        if row in REJECTED:
            continue
        allowed = [extract(row, pair)['allowed'] for pair in PAIRS]
        for p in product(*allowed):
            if any(crossing(s, s) for s in p):
                continue
            if any(crossing(p[j], p[5-j]) for j in range(3)):
                continue
            states.append((row, p))
    ids = {s: i for i, s in enumerate(states)}
    requirements = [list(actions(*s)) for s in states]
    exact = [[ids[global_swap(*s, pair)] for pair in PAIRS] for s in states]
    alive = set(range(len(states)))
    rounds = []
    while True:
        index = {}
        for i in sorted(alive):
            row, p = states[i]
            for j in range(6):
                index.setdefault((row, j, p[j], p[5-j]), i)
        dead = []
        for i in sorted(alive):
            missing = next((j for j, a in enumerate(requirements[i]) if a not in index), None)
            missing_exact = next((j for j, t in enumerate(exact[i]) if t not in alive), None)
            if missing is not None or missing_exact is not None:
                dead.append(dict(state=i, missing_action=missing, missing_global=missing_exact))
        if not dead:
            break
        rounds.append(dead)
        alive.difference_update(d['state'] for d in dead)
    # Independently validate the saved successor selection against the final set.
    witnesses = []
    for i in sorted(alive):
        successors = [index[a] for a in requirements[i]]
        for a, t in zip(requirements[i], successors, strict=True):
            row, j, p, q = a
            tr, tp = states[t]
            assert t in alive and tr == row and tp[j] == p and tp[5-j] == q
        assert all(t in alive for t in exact[i])
        witnesses.append(dict(state=i, successors=successors, global_successors=exact[i]))
    counts = {''.join(map(str, r)): [sum(s[0] == r for s in states),
                                    sum(states[i][0] == r for i in alive)] for r in ROWS}
    assert all(counts[''.join(map(str, r))][1] for r in QUERIES if r not in REJECTED)
    return dict(states=[dict(row=r, partitions=p) for r, p in states],
                deletion_rounds=rounds, closed_successors=witnesses, per_row=counts,
                initial_states=len(states), final_states=len(alive))


def swap_component(vertices, colors, pair, component):
    return normalize(tuple((pair[1] if colors[v] == pair[0] else pair[0])
                           if v in component else colors[v] for v in vertices))


def audit_control(record):
    graph = nx.Graph(record['sector_edges'])
    graph.remove_edges_from([(0, 1), (0, 4)])
    vertices = sorted(graph)
    assert vertices[:5] == list(range(5))
    colorings = set()
    for row in ROWS:
        for cs in product(range(4), repeat=len(vertices)-5):
            c = row + cs
            colors = dict(zip(vertices, c))
            if all(colors[u] != colors[v] for u, v in graph.edges()):
                colorings.add(normalize(c))
    colorings = sorted(colorings)
    ids = {c: i for i, c in enumerate(colorings)}
    adjacency = [[] for _ in colorings]
    witnesses = {}
    for i, c in enumerate(colorings):
        colors = dict(zip(vertices, c))
        if c[:5] in QUERIES:
            assert c[:5] not in REJECTED
            # Direct paths, not just an abstract crossing test.
            witness = path_certificate(graph, colors)
            if witness is not None:
                witnesses[i] = witness
        for pair in PAIRS:
            sub = graph.subgraph(v for v in vertices if colors[v] in pair)
            for component in sorted(tuple(sorted(s)) for s in nx.connected_components(sub)):
                target = swap_component(vertices, colors, pair, set(component))
                assert target in ids
                # Same/complementary induced graphs are literally unchanged before relabeling.
                raw = {v: (pair[1] if colors[v] == pair[0] else pair[0])
                       if v in component else colors[v] for v in vertices}
                complement = tuple(c for c in range(4) if c not in pair)
                for p in (pair, complement):
                    assert observed_partition(graph, colors, p) == observed_partition(graph, raw, p)
                adjacency[i].append(dict(pair=pair, component=component, target=ids[target]))
    mask = sum(1 << j for j, r in enumerate(QUERIES) if any(c[:5] == r for c in colorings))
    assert mask == 3903
    # Global color quotient preserves reachability; every move has an inverse after relabeling.
    for i, edges in enumerate(adjacency):
        for edge in edges:
            assert any(e['target'] == i for e in adjacency[edge['target']])
    distance = {i: 0 for i in witnesses}
    next_step = {}
    queue = deque(sorted(witnesses))
    while queue:
        target = queue.popleft()
        for edge in adjacency[target]:
            i = edge['target']
            if i not in distance:
                distance[i] = distance[target] + 1
                next_step[i] = next(e for e in adjacency[i] if e['target'] == target)
                queue.append(i)
    orbit = nx.Graph()
    orbit.add_nodes_from(range(len(colorings)))
    orbit.add_edges_from((i, e['target']) for i, edges in enumerate(adjacency) for e in edges)
    assert len(distance) == len(colorings)
    for i, edge in next_step.items():
        assert distance[edge['target']] == distance[i] - 1
    query_counts = Counter(QUERIES.index(c[:5]) for c in colorings if c[:5] in QUERIES)
    return dict(source_index=record['source_index'], vertices=vertices, mask=mask,
                colorings=colorings, moves=adjacency,
                orbit_count=nx.number_connected_components(orbit),
                path_witnesses={str(i): w for i, w in sorted(witnesses.items())},
                distance_to_queried_witness=[distance[i] for i in range(len(colorings))],
                next_step={str(i): e for i, e in sorted(next_step.items())},
                query_colorings=dict(sorted(query_counts.items())),
                maximum_distance=max(distance.values()))


def build():
    abstract = abstract_closure()
    source = json.loads(SOURCE.read_text())
    controls = [audit_control(r) for r in source['proper_hits']]
    inputs = [SOURCE] + [ROOT / 'scripts' / (name + '.py') for name in
                         ('c5_sector_cross_row', 'c5_sector_forced_connectivity',
                          'c5_sector_targets', 'boundary_relations',
                          'c5_cell_enumerator', 'c5_k4_blocks')]
    return dict(schema=1,
                scope='Partition-closure relaxation on all 19 rows; actual Kempe orbits only for 22 saved graphs. No general graph-realizability claim.',
                input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in inputs},
                abstract=abstract, controls=controls,
                summary=dict(initial_profiles=abstract['initial_states'],
                             closed_profiles=abstract['final_states'],
                             removed_per_round=[len(r) for r in abstract['deletion_rounds']],
                             controls=len(controls),
                             canonical_colorings=sum(len(c['colorings']) for c in controls),
                             queried_witness_colorings=sum(len(c['path_witnesses']) for c in controls),
                             orbit_counts=[c['orbit_count'] for c in controls],
                             maximum_distance=max(c['maximum_distance'] for c in controls)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    data = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == data, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__':
    main()
