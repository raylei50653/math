#!/usr/bin/env python3
"""Certify terminal-preserving pruning of one-step mixed Kempe incidences."""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

import networkx as nx
from boundary_relations import normalize
from c5_sector_cross_row import relabel
from c5_sector_forced_connectivity import PAIRS, observed_partition
from c5_sector_mixed_transition import components, digest

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / 'artifacts/c5_sector_mixed_transition/observations.json'
CROSS = ROOT / 'artifacts/c5_sector_cross_row/observations.json'
SOURCE = ROOT / 'artifacts/c5_sector_positive_control/observations.json'
OUT = ROOT / 'artifacts/c5_sector_marked_incidence/observations.json'


def marked_quotient(g, c, selected, a, b, d):
    """OLD coloring only. Retained interiors are absent from the interface."""
    blocks = components(g.subgraph(v for v in g
                                   if c[v] == d or (c[v] == a and v not in selected)))
    q = nx.Graph()
    owner = {}
    for i, block in enumerate(blocks):
        node = f'r{i}'
        q.add_node(node, kind='retained', marks=[v for v in block if v < 5])
        owner.update((v, node) for v in block)
    for v in sorted(selected):
        if c[v] != b:
            continue
        node = f's{v}'
        q.add_node(node, kind='star', vertex=v, marks=[v] if v < 5 else [])
        q.add_edges_from((node, owner[w]) for w in g[v] if c[w] == d)
    return q


def project(q):
    return tuple(sorted(tuple(sorted(v for n in block for v in q.nodes[n]['marks']))
                        for block in nx.connected_components(q)
                        if any(q.nodes[n]['marks'] for n in block)))


def packed(q):
    return dict(nodes=[dict(id=n, **q.nodes[n]) for n in sorted(q)],
                edges=sorted(sorted(e) for e in q.edges()))


def prune(q):
    """Remove terminal-free components, then unmarked degree <= 1 vertices."""
    q = q.copy()
    discarded = sorted(n for block in nx.connected_components(q)
                       if not any(q.nodes[n]['marks'] for n in block) for n in block)
    q.remove_nodes_from(discarded)
    rounds = []
    while True:
        leaves = sorted(n for n in q if not q.nodes[n]['marks'] and q.degree[n] <= 1)
        if not leaves:
            break
        rounds.append(leaves)
        q.remove_nodes_from(leaves)
    return q, dict(terminal_free=discarded, leaf_rounds=rounds)


def build():
    upstream = json.loads(UPSTREAM.read_text())
    for name, expected in upstream['input_sha256'].items():
        assert sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
    saved = json.loads(CROSS.read_text())
    records = {r['source_index']: r for r in json.loads(SOURCE.read_text())['proper_hits']}
    audits, negatives, collision = [], {}, []
    total = Counter()
    maxima = Counter()
    for control in saved['controls']:
        index = control['source_index']
        g = nx.Graph(records[index]['sector_edges'])
        g.remove_edges_from([(0, 1), (0, 4)])
        assert sorted(g) == control['vertices']
        traces, count = [], Counter()
        for ci, colors in enumerate(control['colorings']):
            c = dict(zip(control['vertices'], colors, strict=True))
            assert all(c[u] != c[v] for u, v in g.edges())
            expected = {(p, tuple(block)) for p in PAIRS
                        for block in components(g.subgraph(v for v in g if c[v] in p))}
            moves = control['moves'][ci]
            assert {(tuple(e['pair']), tuple(e['component'])) for e in moves} == expected
            assert len(moves) == len(expected)
            for ei, move in enumerate(moves):
                a, b = move['pair']
                selected = set(move['component'])
                raw = {v: (b if c[v] == a else a) if v in selected else c[v] for v in g}
                assert all(raw[u] != raw[v] for u, v in g.edges())
                assert normalize(tuple(raw[v] for v in control['vertices'])) == tuple(
                    control['colorings'][move['target']])
                row, mapping = relabel(tuple(raw[v] for v in range(5)))
                predicted = [None] * 6
                complement = tuple(d for d in range(4) if d not in (a, b))
                for pair in ((a, b), complement):
                    predicted[PAIRS.index(tuple(sorted(mapping[x] for x in pair)))] = (
                        observed_partition(g, c, pair))
                interfaces = []
                for x, y in ((a, b), (b, a)):
                    for d in complement:
                        q = marked_quotient(g, c, selected, x, y, d)
                        small, proof = prune(q)
                        actual = observed_partition(g, raw, (x, d))
                        assert project(q) == project(small) == actual
                        assert packed(prune(small)[0]) == packed(small)
                        k = PAIRS.index(tuple(sorted((mapping[x], mapping[d]))))
                        predicted[k] = project(small)
                        item = dict(pair=[x, d], full=packed(q), reduced=packed(small),
                                    deletion=proof, frame_partition=project(small))
                        interfaces.append(item)
                        count['mixed_interfaces'] += 1
                        count['full_nodes'] += len(q)
                        count['reduced_nodes'] += len(small)
                        count['full_edges'] += q.number_of_edges()
                        count['reduced_edges'] += small.number_of_edges()
                        count['terminal_free_nodes_removed'] += len(proof['terminal_free'])
                        count['leaf_nodes_removed'] += sum(map(len, proof['leaf_rounds']))
                        count['strict_reductions'] += len(q) != len(small)
                        maxima['full_nodes'] = max(maxima['full_nodes'], len(q))
                        maxima['reduced_nodes'] = max(maxima['reduced_nodes'], len(small))
                        # Reject two tempting but unsound frame-only projections.
                        for kind in ('retained', 'star'):
                            naive = q.copy()
                            removed = sorted(n for n in q if q.nodes[n]['kind'] == kind
                                             and not q.nodes[n]['marks'])
                            naive.remove_nodes_from(removed)
                            if project(naive) != actual:
                                count[f'unsafe_unmarked_{kind}_deletions'] += 1
                                negatives.setdefault(kind, dict(source_index=index, coloring_id=ci,
                                    move_id=ei, vertices=control['vertices'], coloring=colors,
                                    edges=sorted(sorted(e) for e in g.edges()), move=move,
                                    interface=item, removed=removed, wrong_partition=project(naive)))
                actual_profile = [None] * 6
                for pair in PAIRS:
                    k = PAIRS.index(tuple(sorted(mapping[x] for x in pair)))
                    actual_profile[k] = observed_partition(g, raw, pair)
                assert predicted == actual_profile
                count['moves'] += 1
                traces.append([ci, ei, interfaces, predicted])
                if index == 41 and ci in (19, 24) and (a, b) == (0, 1) and selected == {0, 1, 2, 9}:
                    collision.append(dict(coloring_id=ci, interfaces=interfaces,
                                          target_row=row, target_profile=predicted))
        total.update(count)
        audits.append(dict(source_index=index, **count, trace_sha256=digest(traces)))
    assert set(negatives) == {'retained', 'star'}
    assert len(collision) == 2 and collision[0]['target_profile'] != collision[1]['target_profile']
    assert collision[0]['interfaces'][0]['reduced'] != collision[1]['interfaces'][0]['reduced']
    inputs = {UPSTREAM, CROSS, SOURCE, Path(__file__).resolve()}
    inputs.update(ROOT / name for name in upstream['input_sha256'])
    return dict(schema=1, baseline='3aaca0b',
        scope='One-step frame connectivity only; joint interfaces extracted from one proper coloring and one maximal component. No new graph, closure or Lean theorem.',
        input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in sorted(inputs)},
        summary=dict(controls=len(audits), colorings=sum(len(c['colorings']) for c in saved['controls']),
                     **total, maxima=dict(maxima)),
        control_audits=audits, unsafe_projection_witnesses=negatives, collision=collision,
        closure_effect=dict(profile_deletions=0, inherited_profiles=603, fixed_point_recomputed=False))


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
