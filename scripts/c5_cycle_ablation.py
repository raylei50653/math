#!/usr/bin/env python3
"""Cycle-count ablation on the frozen radius-two corpus; three-step source rule."""
import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

import networkx as nx

from c5_behavior_refinement import Explorer, GRAMMAR, ROOT
from c5_behavior_radius2 import pair_orbit, PERMS, recolor
from c5_complementary_cube import encode, singleton_of
from c5_cut_interfaces import check_transition
from c5_edge_choices import EdgeModel, Move
from c5_kempe_connectivity import component, components, PAIRS

SOURCE = ROOT / 'artifacts/c5_cells/behavior_radius2.json'
OUT = ROOT / 'artifacts/c5_cells/cycle_ablation.json'


def source_rule(model, c):
    """Source sets only; no swap or Explorer.step call. None is inapplicable."""
    a, b, spectator, repeat, d = c[:5]
    if a != repeat or len({a, b, spectator, d}) != 4:
        return None
    va, vb, vc, vd = ({v for v, t in enumerate(c) if t == color}
                       for color in (a, b, spectator, d))
    k = component(model.adj, c, tuple(sorted((a, d))), 0)
    if k & set(range(5)) != {0, 3, 4}:
        return None
    a1 = (va - k) | (vd & k)
    h = a1 | vb
    l = next(block for block in components(model.adj, h) if 1 in block)
    if l & set(range(5)) != {1}:
        return None
    u = vc | (a1 - l) | (vb & l)
    blocks = sorted(map(sorted, components(model.adj, u)))
    m = next(block for block in blocks if 1 in block)
    connected = 4 in m
    # A path or the entire disconnected component gives a replayable diagnostic.
    induced = nx.Graph()
    induced.add_nodes_from(u)
    induced.add_edges_from((v, w) for v, w in model.edges if v in u and w in u)
    path = nx.shortest_path(induced, 1, 4) if connected else None
    word = tuple((tuple(sorted(pair)), root)
                 for pair, root in [((a, d), 0), ((a, b), 1), ((a, spectator), 1)])
    return dict(frame=(a, b, spectator, d), connected=connected, word=word,
                first_component=sorted(k), first_a_vertices=sorted(a1),
                second_induced_vertices=sorted(h), second_component=sorted(l),
                final_induced_vertices=sorted(u), final_blocks=blocks,
                final_component=m, connection_path=path)


def ablated(ex, c):
    obs, p = ex.observation(c, 'full'), ex.framed_predicate(c)
    return (obs[:2], None if p is None else p['connected'])


def boundary_traces(model, c):
    return [dict(pair=p, traces=sorted(sorted(block & set(range(5)))
            for block in components(model.adj, {v for v, t in enumerate(c) if t in p})
            if block & set(range(5)))) for p in PAIRS]


def independent_outcome(graph, c, word):
    """Independent NetworkX transitions and boundary multiplicity observable."""
    c = list(c)
    for pair, root in word:
        if c[root] not in pair:
            return 'illegal'
        selected = nx.node_connected_component(graph.subgraph(
            [v for v, t in enumerate(c) if t in pair]), root)
        for v in selected:
            c[v] = pair[1] if c[v] == pair[0] else pair[0]
    counts = Counter(c[:5])
    return sorted(counts.values()) == [1, 2, 2] and any(
        counts[c[i]] == 1 for i in (1, 3, 4))


def report():
    data = json.loads(SOURCE.read_text())
    for path, digest in data['hashes'].items():
        assert sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    model = EdgeModel(data['graph'])
    ex = Explorer(model)
    corpus = [tuple(r['coloring']) for r in data['corpus']]
    assert len(corpus) == len(set(corpus)) == 106
    buckets = defaultdict(list)
    for c in corpus:
        model.validate(c)
        buckets[encode(ablated(ex, c))].append(c)
    pairs = []
    for bucket in buckets.values():
        for x, y in combinations(bucket, 2):
            word = ex.distinguish(x, y, 3, 'escape')
            replays = None if word is None else [ex.replay(c, word, 'escape') for c in (x, y)]
            if replays:
                assert replays[0]['outcome'] != replays[1]['outcome']
            pairs.append(dict(sources=(x, y), cycles=[ex.observation(c, 'full')[2] for c in (x, y)],
                word=word, depth=None if word is None else len(word), replays=replays,
                distinction=None if word is None else ('legality' if any(
                    r['outcome'] == 'illegal' for r in replays) else 'escape'),
                global_recoloring_equivalent=any(recolor(x, p) == y for p in PERMS)))
    candidates = [p for p in pairs if p['depth'] == 3 and p['distinction'] == 'escape']
    chosen = candidates[0]
    x, y = chosen['sources']
    rule_records = {c: source_rule(model, c) for c in corpus}
    chosen_rules = [rule_records[c] for c in (x, y)]
    assert [r['connected'] for r in chosen_rules] == [True, False]
    word = chosen_rules[0]['word']
    assert word == chosen_rules[1]['word'] == chosen['word']
    audits = []
    for c, rule in rule_records.items():
        if rule is None:
            continue
        p, q, r = rule['word']
        c1 = ex.step(c, p)
        c2 = ex.step(c1, q)
        c3 = ex.step(c2, r)
        a, b, spectator, d = rule['frame']
        assert rule['second_induced_vertices'] == [v for v, t in enumerate(c1) if t in (a, b)]
        assert rule['second_component'] == sorted(component(model.adj, c1, q[0], q[1]))
        assert rule['final_induced_vertices'] == [v for v, t in enumerate(c2) if t in (a, spectator)]
        assert rule['final_component'] == sorted(component(model.adj, c2, r[0], r[1]))
        assert c1[:5] == (d, b, spectator, d, a)
        assert c2[:5] == (d, a, spectator, d, a)
        assert singleton_of(c3) == (2 if rule['connected'] else 1)
        audits.append(dict(source=c, rule=rule, replay=ex.replay(c, rule['word'], 'escape')))
    graph = nx.Graph()
    graph.add_nodes_from(range(model.n))
    graph.add_edges_from(model.edges)
    independent_words = 0
    for depth in range(3):
        for w in product(GRAMMAR, repeat=depth):
            assert independent_outcome(graph, x, w) == independent_outcome(graph, y, w)
            independent_words += 1
    assert [independent_outcome(graph, c, word) for c in (x, y)] == [False, True]
    mechanism = []
    for c in (x, y):
        history = next(r['histories'] for r in data['corpus'] if tuple(r['coloring']) == c)
        states, transitions = [], []
        for step in range(4):
            states.append(dict(coloring=c, observation=ex.observation(c, 'full'),
                               boundary_traces=boundary_traces(model, c)))
            if step < 3:
                pair, root = word[step]
                move = Move(pair, tuple(sorted(component(model.adj, c, pair, root))))
                transitions.append(dict(action=word[step], component=move.component,
                                        interfaces=check_transition(model, c, move)))
                c = ex.step(c, word[step])
        mechanism.append(dict(histories=history, states=states, transitions=transitions))
    assert all(mechanism[0]['states'][i]['boundary_traces'] ==
               mechanism[1]['states'][i]['boundary_traces'] for i in (0, 1))
    assert mechanism[0]['states'][2]['boundary_traces'] != mechanism[1]['states'][2]['boundary_traces']
    induced_sets = [set(r['final_induced_vertices']) for r in chosen_rules]
    common = induced_sets[0] & induced_sets[1]
    parts = sorted(map(sorted, components(model.adj, common)))
    extras = [sorted(u - common) for u in induced_sets]
    assert extras == [[12], [8]]
    local = dict(common_vertices=sorted(common), common_blocks=parts,
                 added_vertices=extras, neighbors_in_common=[
                     sorted(model.adj[vertices[0]] & common) for vertices in extras])
    for rule, neighbors in zip(chosen_rules, local['neighbors_in_common']):
        left = next(set(b) for b in parts if 1 in b)
        right = next(set(b) for b in parts if 4 in b)
        assert left != right
        assert rule['connected'] == (bool(set(neighbors) & left) and bool(set(neighbors) & right))
    refined = defaultdict(list)
    for c in corpus:
        rule = rule_records[c]
        refined[encode((ablated(ex, c), None if rule is None else rule['connected']))].append(c)
    residual = []
    for bucket in refined.values():
        for a, b in combinations(bucket, 2):
            residual.append(next(i for i, p in enumerate(pairs) if p['sources'] == (a, b)))
    files = {SOURCE, Path(__file__).resolve(), ROOT / 'scripts/c5_cut_interfaces.py',
             *(ROOT / p for p in data['hashes'])}
    return dict(trust='Bounded Python evidence; general three-step iff proved on paper, not in Lean.',
        grammar=GRAMMAR, corpus_radius=2, continuation_depth=3,
        summary=dict(colorings=len(corpus), buckets=len(buckets),
            bucket_sizes=dict(sorted(Counter(map(len, buckets.values())).items())),
            pairs=len(pairs), shortest_depths=dict(sorted(Counter(p['depth'] for p in pairs).items())),
            depth3_escape=len(candidates), depth3_legality=sum(p['depth']==3 and p['distinction']=='legality' for p in pairs),
            depth3_pair_color_orbits=len({pair_orbit(*p['sources']) for p in pairs if p['depth']==3}),
            depth3_escape_pair_color_orbits=len({pair_orbit(*p['sources']) for p in candidates}),
            rule_applicable=len(audits), rule_true=sum(a['rule']['connected'] for a in audits),
            refined_buckets=len(refined), refined_pairs=len(residual),
            residual_depths=dict(sorted(Counter(pairs[i]['depth'] for i in residual).items())),
            independent_shorter_words=independent_words),
        pairs=pairs, selected_pair_index=pairs.index(chosen), mechanism=mechanism,
        local_bridge=local,
        source_rule_audits=audits, refined_residual_pair_indices=residual,
        hashes={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in sorted(files)})


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
