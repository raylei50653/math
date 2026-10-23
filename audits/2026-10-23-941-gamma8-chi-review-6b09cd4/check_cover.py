#!/usr/bin/env python3
"""Literal-tuple independent review of the selected same-candidate cap covers."""
import argparse
from copy import deepcopy
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import random

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PARENT = 'audits/2026-10-23-941-types-wrong-side-round3-6b09cd4/'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def canon(word):
    names = {}
    return tuple(names.setdefault(c, len(names)) for c in word)


def accepts(graph, word):
    if any(word[i] == word[(i + 1) % 6] for i in range(6)):
        return False
    for (a, b), different in graph['constraints']:
        if (word[a] != word[b]) != bool(different):
            return False
    return not graph['spokes'] or len({word[i] for i in graph['spokes']}) < 4


def validate(cert, old, seed=0):
    words = list(product(range(4), repeat=6))
    random.Random(seed).shuffle(words)
    proper = [w for w in words if all(w[i] != w[(i + 1) % 6] for i in range(6))]
    need(len(proper) == 732, 'literal proper domain')
    need(len(cert['candidates']) == 34 and len(cert['caps']) == 16, 'family domain')
    graph_by_id = {g['id']: g for g in cert['candidates']}
    need(len(graph_by_id) == 34, 'candidate identity')
    for graph in cert['candidates']:
        constraints = graph['constraints']
        diagonals = [tuple(e) for e, _ in constraints]
        need(len(set(diagonals)) == len(diagonals), 'duplicate drawn chord')
        for a, b in diagonals:
            need(0 <= a < b < 6 and b - a not in (1, 5), 'chord endpoints')
        for (a, b), (c, d) in combinations(diagonals, 2):
            if len({a, b, c, d}) == 4:
                need(((a < c < b) == (a < d < b)), 'alternating chord endpoints')
        if graph['spokes']:
            need(graph['spokes'] == [0, 1, 2, 3, 4] and
                 constraints == [[[0, 4], 1]], 'unproved hub drawing')
        classes = {i: {i} for i in range(6)}
        for (a, b), different in constraints:
            need(type(different) is int and different in (0, 1), 'edge mode')
            if not different:
                group = classes[a] | classes[b]
                for i in group:
                    classes[i] = group
        expected_map = [min(classes[i]) for i in range(6)]
        need(graph['vertex_map'] == expected_map, 'equivalence closure')
        saving = 8 + 6 - len({tuple(sorted(v)) for v in classes.values()}) - bool(graph['spokes'])
        need(graph['completed_interior_saving'] == saving, 'completed size')
        stored = {tuple(r['word']): r['full_lifts'] for r in graph['relations']}
        need(len(stored) == 31, 'complete candidate rows')
        for word in words:
            need(accepts(graph, word) == bool(stored.get(canon(word))), 'literal candidate relation')
    literal_backfills = 0
    same_choice_rows = 0
    for record in cert['caps']:
        cap = old['caps'][record['cap_id']]
        need(record['relations'] == cap['relations'], 'original complete relations changed')
        support = {tuple(r['word']) for r in cap['relations'] if r['full_lifts']}
        selected = [graph_by_id[i] for i in record['candidates']]
        need(len(selected) == len({g['id'] for g in selected}), 'repeated selection')
        for graph in selected:
            for word in proper:
                if accepts(graph, word):
                    need(canon(word) in support, 'literal unsafe backfill')
                    literal_backfills += 1
        for word in proper:
            choices = [g for g in selected if accepts(g, word)]
            need(bool(choices) == (canon(word) in support), 'literal accepted witness coverage')
            if choices:
                fixed = choices[0]
                # Hold the accepted choice fixed while replaying every other row.
                for rejection in proper:
                    need(not accepts(fixed, rejection) or canon(rejection) in support,
                         'same candidate changed across rows')
                    same_choice_rows += 1
    return dict(status='PASS', all_literal_tuples=4096, literal_proper_tuples=732,
                candidates=34, caps=16, literal_candidate_backfills=literal_backfills,
                same_fixed_choice_literal_row_checks=same_choice_rows,
                all_drawn_chords_noncrossing=True, all_quotient_classes_checked=True,
                hub_drawings=1, savings=sorted({g['completed_interior_saving'] for g in cert['candidates']}),
                source_controls='not triggered', exclusions_from_control_pass=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--negative', action='store_true')
    args = parser.parse_args()
    manifest = json.loads((HERE / 'INPUTS-COVER.json').read_text())
    for row in manifest['sources']:
        snapshot = (HERE / 'frozen' / row['path']).read_bytes()
        need(sha256(snapshot).hexdigest() == row['sha256'], 'cover snapshot drift')
        if row['authority'] == 'immutable certificate':
            need((ROOT / row['path']).read_bytes() == snapshot, 'live cover drift')
    cert = json.loads((HERE / 'frozen' / PARENT / 'reduction-certificate.json').read_text())
    old = json.loads((HERE / 'frozen/audits/2026-10-23-941-gamma8-joint-bpaths-6b09cd4/EXACT_CAPS.json').read_text())
    if args.negative:
        tests = [('drop_candidate_cover', lambda c: c['caps'][0].update(candidates=[])),
                 ('change_cost', lambda c: c['candidates'][0].update(completed_interior_saving=20)),
                 ('crossed_diagonals', lambda c: c['candidates'][0].update(constraints=[[[0, 3], 1], [[1, 4], 1]])),
                 ('change_hub_side', lambda c: next(g for g in c['candidates'] if g['spokes']).update(spokes=[0, 1, 2, 3, 5]))]
        rejected = []
        for name, mutate in tests:
            damaged = deepcopy(cert)
            mutate(damaged)
            try:
                validate(damaged, old, args.seed)
            except ValueError:
                rejected.append(name)
            else:
                raise ValueError('negative accepted: ' + name)
        print(json.dumps(dict(status='PASS', rejected=rejected), sort_keys=True))
    else:
        print(json.dumps(validate(cert, old, args.seed), sort_keys=True))


if __name__ == '__main__':
    main()
