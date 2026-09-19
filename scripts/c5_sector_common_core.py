#!/usr/bin/env python3
"""Audit common-core quotients for old x/d and new y/d in a single swap."""
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
from c5_sector_marked_incidence import project, packed

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / 'artifacts/c5_sector_marked_incidence/observations.json'
CROSS = ROOT / 'artifacts/c5_sector_cross_row/observations.json'
SOURCE = ROOT / 'artifacts/c5_sector_positive_control/observations.json'
OUT = ROOT / 'artifacts/c5_sector_common_core/observations.json'


def restrict(partition, vertices):
    return tuple(sorted(tuple(v for v in block if v in vertices)
                        for block in partition if any(v in vertices for v in block)))


def refines(left, right):
    return all(any(set(a) <= set(b) for b in right) for a in left)


def common_core(g, c, selected, x, y, d):
    core = g.subgraph(v for v in g if c[v] == d or (v in selected and c[v] == x))
    blocks = components(core)
    q = nx.Graph()
    owner = {}
    for i, block in enumerate(blocks):
        q.add_node(f'r{i}', marks=[v for v in block if v < 5],
                   stars=[v for v in block if v in selected],
                   d_vertices=[v for v in block if c[v] == d])
        owner.update((v, f'r{i}') for v in block)
    result = dict(old_pair=[x, d], new_pair=[y, d], core=packed(q),
                  core_partition=project(q), extensions=[])
    for color in (x, y):
        extension = q.copy()
        outsiders = sorted(v for v in g if v not in selected and c[v] == color)
        for v in outsiders:
            neighbors = sorted(g[v])
            # No edges to core stars: properness for x, maximality for y.
            assert all(c[w] == d for w in neighbors if w in core)
            extension.add_node(f'o{v}', marks=[v] if v < 5 else [], vertex=v)
            extension.add_edges_from((f'o{v}', owner[w]) for w in neighbors if c[w] == d)
        result['extensions'].append(dict(color=color, outside_vertices=outsiders,
                                        quotient=packed(extension), partition=project(extension)))
    return result


def candidate(states):
    source, target = states[397], states[330]
    selected = {0, 1, 2}
    raw = tuple(1-source['row'][v] if v in selected else source['row'][v] for v in range(5))
    row, mapping = relabel(raw)
    assert tuple(target['row']) == row
    rows = []
    for x, y in ((0, 1), (1, 0)):
        for d in (2, 3):
            terminals = {v for v in range(5) if source['row'][v] == d or
                         (v in selected and source['row'][v] == x)}
            old = restrict(source['partitions'][PAIRS.index(tuple(sorted((x, d))))], terminals)
            new = restrict(target['partitions'][PAIRS.index(tuple(sorted((mapping[y], mapping[d]))))], terminals)
            meet = tuple(sorted(tuple(sorted(set(a) & set(b))) for a in old for b in new if set(a) & set(b)))
            rows.append(dict(old_pair=[x, d], new_raw_pair=[y, d], terminals=sorted(terminals),
                             source_bound=old, target_bound=new, common_core_bound=meet))
    assert all(r['source_bound'] == r['target_bound'] for r in rows)
    return dict(source=397, action=2, target=330, rows=rows,
                source_bounds_unchanged=True, excludes_transition=False)


def build():
    upstream = json.loads(UPSTREAM.read_text())
    for name, expected in upstream['input_sha256'].items():
        assert sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
    saved = json.loads(CROSS.read_text())
    records = {r['source_index']: r for r in json.loads(SOURCE.read_text())['proper_hits']}
    requirement = next(w for w in saved['abstract']['closed_successors'] if w['state'] == 397)
    assert requirement['successors'][2] == 330
    audits, witnesses = [], {}
    total = Counter()
    for control in saved['controls']:
        index = control['source_index']
        g = nx.Graph(records[index]['sector_edges'])
        g.remove_edges_from([(0, 1), (0, 4)])
        assert sorted(g) == control['vertices']
        trace, counts = [], Counter()
        for ci, colors in enumerate(control['colorings']):
            c = dict(zip(control['vertices'], colors, strict=True))
            assert all(c[u] != c[v] for u, v in g.edges())
            moves = control['moves'][ci]
            expected = {(p, tuple(b)) for p in PAIRS for b in components(g.subgraph(v for v in g if c[v] in p))}
            assert {(tuple(m['pair']), tuple(m['component'])) for m in moves} == expected
            assert len(moves) == len(expected)
            for mi, move in enumerate(moves):
                a, b = move['pair']
                selected = set(move['component'])
                raw = {v: (b if c[v] == a else a) if v in selected else c[v] for v in g}
                assert normalize(tuple(raw[v] for v in control['vertices'])) == tuple(control['colorings'][move['target']])
                items = []
                for x, y in ((a, b), (b, a)):
                    for d in range(4):
                        if d in (a, b):
                            continue
                        item = common_core(g, c, selected, x, y, d)
                        terminals = {v for block in item['core_partition'] for v in block}
                        old = observed_partition(g, c, (x, d))
                        new = observed_partition(g, raw, (y, d))
                        assert item['extensions'][0]['partition'] == old
                        assert item['extensions'][1]['partition'] == new
                        for side, actual in (('old', old), ('new', new)):
                            bound = restrict(actual, terminals)
                            assert refines(item['core_partition'], bound)
                            if item['core_partition'] != bound:
                                counts[f'{side}_outside_detours'] += 1
                                witnesses.setdefault(side, dict(source_index=index, coloring_id=ci, move_id=mi,
                                    vertices=control['vertices'], coloring=colors,
                                    edges=sorted(sorted(e) for e in g.edges()), move=move, interface=item))
                        items.append(item)
                        counts['common_cores'] += 1
                        counts['extension_projections'] += 2
                trace.append([ci, mi, items])
                counts['moves'] += 1
        audits.append(dict(source_index=index, **counts, trace_sha256=digest(trace)))
        total.update(counts)
    assert set(witnesses) == {'old', 'new'}
    inputs = {UPSTREAM, CROSS, SOURCE, Path(__file__).resolve()}
    inputs.update(ROOT / p for p in upstream['input_sha256'])
    return dict(schema=1, baseline='3aaca0b',
                scope='Common-core extension lemma and fixed-corpus audit; no realizability or new closure claim.',
                input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in sorted(inputs)},
                summary=dict(controls=len(audits), **total), control_audits=audits,
                outside_detour_witnesses=witnesses, candidate=candidate(saved['abstract']['states']),
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
    print(json.dumps(dict(summary=result['summary'], candidate=result['candidate']), indent=2))


if __name__ == '__main__':
    main()
