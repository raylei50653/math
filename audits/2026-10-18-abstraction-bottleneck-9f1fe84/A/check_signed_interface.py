#!/usr/bin/env python3
"""Exhaustive observation certificates against the frozen K<=5 mask catalogue.

This does not prove existence of a smaller disk graph or replay catalogue
enumeration. It uses only the frozen catalogue's literal mask keys.
"""
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent


def calculate():
    manifest = json.loads((HERE / 'INPUTS.json').read_text())
    for entry in manifest['inputs']:
        data = (HERE / entry['frozen']).read_bytes()
        assert hashlib.sha256(data).hexdigest() == entry['sha256']
    data = json.loads((HERE / 'frozen/artifacts/c5_cells/cells.json').read_text())
    masks = sorted(map(int, data['cells']))
    rows = [''.join(map(str, row)) for row in data['pattern_order']]
    assert len(masks) == len(set(masks)) == data['distinct_sigma'] == 132
    assert rows == ['01012', '01021', '01023', '01201', '01202',
                    '01203', '01212', '01213', '01231', '01232']
    target_results = {}
    for target in (932, 933, 941):
        separating = []
        small_witnesses = []
        for scope in range(1024):
            compatible = [known for known in masks if not (known ^ target) & scope]
            if not compatible:
                separating.append(scope)
            if scope.bit_count() <= 3:
                assert compatible
                small_witnesses.append({'scope': scope, 'known_mask': compatible[0]})
        minimum = min(scope.bit_count() for scope in separating)
        minimal_scopes = [scope for scope in separating if scope.bit_count() == minimum]
        assert minimum == 4
        assert len(small_witnesses) == 176
        target_results[str(target)] = {
            'minimum_observations': minimum,
            'minimum_scopes': minimal_scopes,
            'all_at_most_three_observation_countermodels': small_witnesses,
        }
    scope, accept = 594, 512
    assert all((target & scope) == accept for target in (932, 933, 941))
    assert target_results['941']['minimum_scopes'] == [scope]
    assert len(target_results['933']['minimum_scopes']) == 2
    assert len(target_results['932']['minimum_scopes']) == 5
    compatible_masks = [mask for mask in range(1024) if (mask & scope) == accept]
    assert len(compatible_masks) == 64
    assert not set(compatible_masks) & set(masks)
    removal_controls = {}
    for bit in (1, 4, 6, 9):
        reduced = scope ^ (1 << bit)
        compatible = [mask for mask in masks if (mask & reduced) == (accept & reduced)]
        assert compatible
        removal_controls[rows[bit]] = compatible
    return {
        'base': manifest['base'],
        'evidence_scope': 'finite catalogue separation, not source realization or reduction',
        'catalogue_masks': 132,
        'pattern_order': rows,
        'targets': target_results,
        'common_interface': {
            'query_mask': scope,
            'accepted_query_mask': accept,
            'accept': ['01232'],
            'reject': ['01021', '01202', '01212'],
            'compatible_raw_masks': compatible_masks,
            'known_mask_count': 0,
            'one_query_removed_controls': removal_controls,
        },
    }


def main():
    result = calculate()
    certificate = HERE / 'signed_interface_certificate.json'
    if sys.argv[1:] == ['--write']:
        with certificate.open('x') as handle:
            json.dump(result, handle, indent=2, sort_keys=True)
            handle.write('\n')
    elif not sys.argv[1:]:
        assert json.loads(certificate.read_text()) == result
    else:
        raise SystemExit('usage: check_signed_interface.py [--write]')
    print('PASS: 132 masks; 3 x 1024 scopes; 528 <=3-query countermodels; '
          'common four-query interface has 64 raw masks and zero catalogue matches')


if __name__ == '__main__':
    main()
