#!/usr/bin/env python3
"""Audit the exact C2 exclusion key without changing any predecessor row."""
import argparse
import hashlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path('.'))
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root, out = args.repo.resolve(), args.output.resolve()
    assert not out.exists(), 'Use a fresh output path to preserve earlier attempts'
    out.mkdir(parents=True)
    paths = ['artifacts/c5_mixed_p3_common_endpoint/observations.json',
             'artifacts/c5_mixed_p3_one_color_ternary_unary/observations.json']
    raw = [(root / p).read_bytes() for p in paths]
    common, unary = map(json.loads, raw)
    target = ('CPP-134-1', 30, 20)
    case_by_id = {c['id']: c for c in common['local']['cases']}
    local_by_id = {c['id']: c for c in common['local']['configurations']}
    geometries = common['geometry']['retained_geometries']
    assert len(case_by_id) == len(common['local']['cases'])
    assert len({g['id'] for g in geometries}) == len(geometries)
    assert (unary['identity']['parent_entry']['case_name'],
            unary['identity']['parent_entry']['geometry_id'],
            unary['identity']['parent_entry']['side_join_id']) == target
    assert unary['identity']['case'] == case_by_id[86]
    assert unary['identity']['local'] == local_by_id[134]
    assert unary['identity']['geometry'] == next(g for g in geometries if g['id'] == 30)
    rows = []
    for g in geometries:
        c = case_by_id[g['case_id']]
        local = local_by_id[c['local_id']]
        a = str(local['a'])
        assert len(c['side_join_ids']) == len(set(c['side_join_ids'])) == 25
        for j in c['side_join_ids']:
            z_id, w_id = common['local']['joins_by_a'][a][j]
            key = (c['name'], g['id'], j)
            rows.append(dict(case_name=c['name'], case_id=c['id'], local_id=local['id'],
                             geometry_id=g['id'], side_join_id=j, side_ids=[z_id, w_id],
                             actual_supports=local['actual_supports'],
                             actual_side_supports=g['actual_side_supports'],
                             complete_P3_triples=local['complete_triples'],
                             z_role=common['local']['side_roles'][z_id],
                             w_role=common['local']['side_roles'][w_id],
                             c2_closed=key == target,
                             scope='necessary indexed candidate; no realization or new D3 source verdict'))
    keys = [(r['case_name'], r['geometry_id'], r['side_join_id']) for r in rows]
    assert len(keys) == len(set(keys)) == 3500
    closed = [r for r in rows if r['c2_closed']]
    assert len(closed) == 1 and closed[0]['side_ids'] == [8, 1]
    assert closed[0]['actual_side_supports'] == [[1], [2, 4]]
    target_case = [r for r in rows if r['case_name'] == target[0]]
    assert len(target_case) == 150
    assert len([r for r in target_case if r['geometry_id'] == 30 and not r['c2_closed']]) == 24
    assert len([r for r in target_case if not r['c2_closed']]) == 149
    following = unary['identity']['next_entry']
    assert (following['case_name'], following['geometry_id'], following['side_join_id']) == (target[0], 34, 20)
    assert any((r['case_name'], r['geometry_id'], r['side_join_id']) == (target[0], 34, 20)
               and not r['c2_closed'] for r in rows)
    negatives = []
    for name, predicate in (
        ('drop_whole_case', lambda r: r['case_name'] == target[0]),
        ('drop_whole_geometry30', lambda r: r['case_name'] == target[0] and r['geometry_id'] == 30),
        ('drop_join20_across_case_geometries', lambda r: r['case_name'] == target[0] and r['side_join_id'] == 20),
    ):
        wrong = [r for r in rows if predicate(r)]
        extras = [[r['case_name'], r['geometry_id'], r['side_join_id']] for r in wrong if not r['c2_closed']]
        assert extras
        negatives.append(dict(name=name, wrongly_removed_count=len(wrong),
                              extra_removed_count=len(extras), extra_keys=extras,
                              rejected_by_exact_key_audit=True))
    assert unary['summary']['predecessor_deletions'] == 0
    assert (unary['summary']['predecessor_cases'], unary['summary']['predecessor_geometries'],
            unary['summary']['predecessor_joins']) == (36, 140, 900)
    result = dict(all_checks_passed=True,
                  inputs_sha256={p: hashlib.sha256(b).hexdigest() for p, b in zip(paths, raw)},
                  predecessor_retained_cases=36, predecessor_geometries=140,
                  predecessor_case_side_joins=900, expanded_case_geometry_side_keys=len(rows),
                  c2_closed_keys=[list(target)], target_case_geometries=sorted({r['geometry_id'] for r in target_case}),
                  target_case_side_join_ids=case_by_id[86]['side_join_ids'],
                  target_case_rows_outside_c2_scope=149, geometry30_other_side_joins=24,
                  next_entry_preserved=[target[0], 34, 20],
                  source_arrays_changed=False, negative_controls=negatives,
                  note='3500 keys index 140 geometries times 25 case roles; no source enumeration, target query or broadened exclusion')
    (out / 'scope_ledger.json').write_text(json.dumps(rows, indent=1, ensure_ascii=False) + '\n')
    (out / 'results.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('inputs_sha256', 'negative_controls')}))


if __name__ == '__main__':
    main()
