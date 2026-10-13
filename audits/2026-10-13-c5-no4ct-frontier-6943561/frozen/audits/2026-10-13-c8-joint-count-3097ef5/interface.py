#!/usr/bin/env python3
"""Complete named h=3 collar, literal transfer, and necessary Kempe bound.

The frozen h<=2 implementation supplies the already audited combinatorial
Kempe rule. This producer extends only its interface length, not its rule.
controls/checker.py independently reconstructs the literal interface.
"""
import argparse
from collections import Counter
import importlib.util
from itertools import product
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
OLD = HERE / 'frozen/audits/2026-10-12-neartri-complete-relation-reductions-5d70a399/collar_checker.py'
spec = importlib.util.spec_from_file_location('frozen_collar', OLD)
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)


def compatible(inner, outer, supports):
    return all(inner[j] != outer[i] for j, support in enumerate(supports)
               for i in support)


def build():
    literal = tuple(p for p in product(range(4), repeat=8)
                    if all(p[i] != p[(i+1) % 8] for i in range(8)))
    pats = tuple(sorted({old.norm(p) for p in literal}))
    index = {p: i for i, p in enumerate(pats)}
    literal_index = [index[old.norm(p)] for p in literal]
    sizes = Counter(literal_index)
    by_colors = Counter(len(set(p)) for p in pats)
    # Computed by exhaustive enumeration, then compared with independent formulas.
    assert len(literal) == 3**8 + 3 == 6564
    assert len(pats) == 274 and by_colors == {2: 1, 3: 42, 4: 231}
    assert [sizes[i] for i, p in enumerate(pats) if len(set(p)) == 2] == [12]
    assert all(sizes[i] == 24 for i, p in enumerate(pats) if len(set(p)) >= 3)
    table = old.kempe_table(8)
    extras = list(old.compositions(3, 5))
    brute_extras = [t for t in product(range(4), repeat=5) if sum(t) == 3]
    assert extras == brute_extras and len(extras) == 35
    cases = []
    for case_index, t in enumerate(extras):
        supports = old.collar_supports(t)
        labels = []
        for i in range(5):
            labels.append('a'+str(i))
            labels.extend(f'y{(i+1)%5}_{j}' for j in range(1, t[(i+1)%5]+1))
        columns, lifts = old.columns(t)
        transfer = [[0]*len(pats) for _ in old.P5]
        # No normalization of independently glued pieces: both assignments
        # are literally compared in the common frame 0,1,2,3.
        for r, outer in enumerate(old.P5):
            for inner, pidx in zip(literal, literal_index):
                if compatible(inner, outer, supports):
                    transfer[r][pidx] += 1
        reverse = [[sum(old.norm(b) == outer for b in row_lifts)
                    for row_lifts in lifts] for outer in old.P5]
        for r in range(10):
            for p in range(len(pats)):
                assert 24*transfer[r][p] == sizes[p]*reverse[r][p]
                assert bool(transfer[r][p]) == bool(columns[p] >> r & 1)
        checks = []
        for target in (933, 941):
            check = old.prune(columns, table, target)
            check['accepted_preimages'] = {
                str(r): [p for p in range(len(pats))
                         if check['fixed_point'] >> p & 1 and transfer[r][p]]
                for r in range(10) if target >> r & 1}
            check['query_id'] = f'c{case_index:02d}-{target}'
            checks.append(check)
        edges = [(f'b{i}', f'b{(i+1)%5}') for i in range(5)]
        edges += [(labels[i], labels[(i+1)%8]) for i in range(8)]
        edges += [(f'b{i}', labels[j]) for j, support in enumerate(supports)
                  for i in support]
        cases.append(dict(id=f'c{case_index:02d}', extras=t,
                          boundary_order=labels, supports=supports,
                          collar_edges=edges, column_masks=columns,
                          transfer=transfer,
                          outer_lifts_for_each_named_inner_row=lifts,
                          full_preimages={str(r): [p for p in range(len(pats))
                                                  if transfer[r][p]] for r in range(10)},
                          targets=checks))
    return dict(schema='c8-joint-count-v1', color_frame=[0, 1, 2, 3],
                boundary_order=[f'b{i}' for i in range(5)],
                pattern_order=pats, outer_pattern_order=old.P5,
                orbit_sizes=[sizes[i] for i in range(len(pats))],
                orbit_counts_by_colors=dict(sorted(by_colors.items())),
                literal_assignments=literal, literal_to_pattern=literal_index,
                complementary_splits=[[[0, 1], [2, 3]], [[0, 2], [1, 3]], [[0, 3], [1, 2]]],
                kempe_obligations=table, cases=cases,
                symmetry='No reduction: all 35 named distributions times both targets. Identity label map for every query.',
                transfer_definition='T[r,p] counts literal C8 assignments in orbit p compatible with fixed canonical outer row r; y_r=sum_p T[r,p]*x_p, where x_p counts H extensions for one fixed literal inner row.',
                bound_status='Necessary upper bound only; neither an actual full relation nor an extension count vector.')


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--write', action='store_true')
    group.add_argument('--check', action='store_true')
    parser.add_argument('--certificate', type=Path, default=HERE/'interface.json')
    args = parser.parse_args()
    result = build()
    if args.write:
        with args.certificate.open('x') as f:
            json.dump(result, f, sort_keys=True, separators=(',', ':'))
            f.write('\n')
    else:
        assert json.loads(args.certificate.read_text()) == json.loads(json.dumps(result)), 'interface certificate mismatch'
    survivors = [dict(id=q['query_id'], extras=c['extras'], upper=q['fixed_point'].bit_count())
                 for c in result['cases'] for q in c['targets'] if not q['excluded']]
    print(json.dumps(dict(status='PASS', cases=len(result['cases']), queries=70,
                          rows=len(result['pattern_order']), literal=len(result['literal_assignments']),
                          kempe_survivors=survivors), sort_keys=True))


if __name__ == '__main__':
    main()
