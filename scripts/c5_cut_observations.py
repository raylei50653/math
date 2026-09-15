#!/usr/bin/env python3
"""Audit coarse cut observations on the fixed 196 Errera transitions."""
import argparse
from collections import defaultdict
from hashlib import sha256
import json
from itertools import combinations
from pathlib import Path

from c5_cut_interfaces import SOURCE, ROOT, EdgeModel, Move, check_transition
from c5_complementary_cube import encode

OUT = ROOT / 'artifacts/c5_cells/cut_observations.json'


def report():
    source = json.loads(SOURCE.read_text())
    model = EdgeModel(source['graph'])
    rows = []
    for index, event in enumerate(source['transition_table']):
        c = tuple(event['before'])
        action = Move(tuple(event['pair']), tuple(event['component']))
        d = model.apply(c, action)
        assert d == tuple(event['after'])
        selected = set(action.component)
        cut = {i for i, (u, v) in enumerate(model.edges)
               if (u in selected) != (v in selected)}
        assert sorted(cut) == event['cut_edges']
        systems = model.dual.systems(c)
        # Paths are identified by ordered terminal labels; cycles are an
        # unordered multiset. No arbitrary cross-witness cycle identity.
        counts = [sorted((terminals, len(cut & set(edges)))
                         for terminals, edges in system) for system in systems]
        sizes = [sorted((terminals, len(edges), len(cut & set(edges)))
                        for terminals, edges in system) for system in systems]
        base = dict(boundary=c[:5], state=model.dual.state(c, True), pair=action.pair)
        length = dict(base, cut_length=len(cut))
        observations = dict(base=base, cut_length=length,
                            cut_counts=dict(length, component_cut_counts=counts),
                            component_sizes=dict(length, component_sizes_and_cuts=sizes))
        reconstructed = check_transition(model, c, action)
        rows.append(dict(index=index, source=c, action=dict(pair=action.pair,
            component=action.component), cut_edges=sorted(cut), observations=observations,
            target=d, target_state=model.dual.state(d, True),
            target_boundary=d[:5], target_compatible=model.compatible(d),
            interface_predictions=[r['prediction'] for r in reconstructed]))
    analyses = {}
    for name in rows[0]['observations']:
        groups = defaultdict(list)
        for row in rows:
            groups[encode(row['observations'][name])].append(row)
        classes, collisions = [], []
        for key, group in sorted(groups.items()):
            outputs = defaultdict(list)
            for row in group:
                outcome = dict(boundary=row['target_boundary'], state=row['target_state'],
                               compatible=row['target_compatible'])
                outputs[encode(outcome)].append(row['index'])
            item = dict(observation=json.loads(key),
                        outcomes=[dict(target=json.loads(k), transitions=v)
                                  for k, v in sorted(outputs.items())])
            classes.append(item)
            if len(outputs) > 1:
                collisions.append([item['outcomes'][0]['transitions'][0],
                                   item['outcomes'][1]['transitions'][0]])
        analyses[name] = dict(groups=len(groups),
            repeated_groups=sum(len(g) > 1 for g in groups.values()),
            distinct_source_groups=sum(len({r['source'] for r in g}) > 1
                                       for g in groups.values()),
            collision_groups=len(collisions), witnesses=collisions, classes=classes)
    # The base has genuine collisions, including different target pairings.
    assert analyses['base']['collision_groups'] > 0
    # Use the same rooted selection rule and target boundary, so the witness
    # is not merely two different components of a single coloring.
    pairing_witness = next((a['index'], b['index']) for a, b in combinations(rows, 2)
        if a['source'] != b['source']
        and a['observations']['base'] == b['observations']['base']
        and min(a['action']['component']) == min(b['action']['component'])
        and a['target_boundary'] == b['target_boundary']
        and a['target_state'][1:4] != b['target_state'][1:4])
    assert all(analyses[k]['collision_groups'] == 0
               for k in ('cut_length', 'cut_counts', 'component_sizes'))
    a, b = pairing_witness
    assert rows[a]['observations']['base'] == rows[b]['observations']['base']
    assert len(rows[a]['cut_edges']) != len(rows[b]['cut_edges'])
    files = {SOURCE, Path(__file__).resolve(), ROOT / 'scripts/c5_cut_interfaces.py'}
    files.update(ROOT / p for p in source['hashes'] if p.startswith('scripts/'))
    return dict(trust='Finite exact Python replay; no general sufficiency or Lean theorem.',
        scope='Exactly the existing transition table; no new actions or graphs enumerated.',
        graph=source['graph'], summary=dict(transitions=len(rows),
            audited_systems=3 * len(rows), observations={k: {x: v[x] for x in (
                'groups', 'repeated_groups', 'distinct_source_groups', 'collision_groups')}
                for k, v in analyses.items()}),
        pairing_witness=pairing_witness, rows=rows, analyses=analyses,
        hashes={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                for p in sorted(files)})


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
