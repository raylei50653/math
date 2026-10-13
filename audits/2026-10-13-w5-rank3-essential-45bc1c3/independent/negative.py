#!/usr/bin/env python3
"""Four concrete corruptions, rejected by two distinct record validators."""
import copy
import gzip
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    primary = module('primary', ROOT/'controls/check.py')
    independent = module('independent', ROOT/'independent/check.py')
    with gzip.open(ROOT/'controls/certificate.jsonl.gz', 'rt') as stream:
        next(stream)
        source = json.loads(next(stream))
    expected = primary.fill(primary.make(source['key']))
    assert expected == source
    n, edges = independent.geometry(source)
    independent.verify_rows(source, n, edges)
    bad = {}
    edge = copy.deepcopy(source)
    q = edge['ownership']['diamond']
    edge['edges'].remove(sorted([q['qB'], q['qU']]))
    bad['omitted_original_diamond_edge'] = edge
    pins = copy.deepcopy(source)
    pins['ownership']['pin_map'][5:7] = [6, 5]
    bad['wrong_U_pin_map'] = pins
    faces = copy.deepcopy(source)
    faces['faces'][-1].reverse()
    bad['reversed_U_face'] = faces
    lift = copy.deepcopy(source)
    next(cell for row in lift['rows'] for cell in row['cells'] if cell).pop()
    bad['omitted_full_A_lift'] = lift
    rejected = []
    for name, record in bad.items():
        for validator in ('primary', 'independent'):
            try:
                if validator == 'primary':
                    assert record == expected, 'recomputed record mismatch'
                else:
                    nr, er = independent.geometry(record)
                    independent.verify_rows(record, nr, er)
            except AssertionError as error:
                rejected.append({'case': name, 'validator': validator,
                                 'status': 'rejected', 'reason': str(error)})
            else:
                raise AssertionError(f'corruption accepted: {name} {validator}')
    assert len(rejected) == 8
    print(json.dumps({'status': 'PASS', 'positive_record': source['key'],
                      'negative_controls': rejected}, sort_keys=True))


if __name__ == '__main__':
    main()
