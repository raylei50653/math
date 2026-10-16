#!/usr/bin/env python3
"""Positive calibration of the forbidden unequal two-palette W fibre."""
import argparse
import gzip
import json
from pathlib import Path
import check as core

HERE = Path(__file__).resolve().parent


def build():
    inputs = json.loads((HERE / 'INPUTS.json').read_text())
    for item in inputs['entries']:
        assert core.digest(HERE / item['frozen_path']) == item['sha256']
        assert core.digest(core.REPO / item['path']) == item['sha256']
    patch = core.patch(5, 6, 6, 7)
    assert patch['degrees']['m'] == 8 and patch['degrees']['z'] == 6
    obstructions = []
    for fibre in patch['all_proper_boundary_fibres_including_empty']:
        a, b = fibre['A_m'], fibre['A_z']
        if len(a) != 2 or len(b) != 2 or a == b:
            continue
        row = dict(zip(patch['boundary'], fibre['boundary_row']))
        assert row[patch['alpha']] == row[patch['beta']]
        assert len(fibre['all_full_lifts']) == 3
        differences = sorted(x ^ y for x, y in fibre['all_hub_pairs_including_empty'])
        assert differences == [1, 2, 3]
        e, f = row['v'] ^ row['w'], row['p'] ^ row['q']
        assert e == a[0] ^ a[1] and f == b[0] ^ b[1] and e != f
        bad = [lift for lift in fibre['all_full_lifts'] if not lift['all_r_source_allowed']]
        assert len(bad) == 1
        x, y = bad[0]['hub_pair']
        assert x ^ y == e
        obstructions.append({'boundary_row': fibre['boundary_row'], 'A_m': a, 'A_z': b,
                             'all_three_hub_differences': differences,
                             'unique_forbidden_full_lift': bad[0]})
    assert len(obstructions) == 24
    return {'base': core.BASE, 'core_checker_sha256': core.digest(HERE / 'check.py'),
            'checker_sha256': core.digest(Path(__file__)),
            'inputs_sha256': core.digest(HERE / 'INPUTS.json'),
            'complete_patch': patch, 'all_unequal_two_palette_obstructions': obstructions,
            'obstruction_count': 24, 'source_status': 'not triggered',
            'scope': 'local interface calibration, no claim that W realizes such a boundary row'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--certificate', type=Path, default=HERE / 'two-palette.json.gz')
    args = ap.parse_args()
    result = json.loads(json.dumps(build()))
    if args.write:
        raw = json.dumps(result, sort_keys=True, separators=(',', ':')).encode()
        with args.certificate.open('xb') as f:
            f.write(gzip.compress(raw, mtime=0))
    else:
        assert json.loads(gzip.decompress(args.certificate.read_bytes())) == result, 'certificate mismatch'
    print(json.dumps({'status': 'PASS', 'complete_patch_colourings': result['complete_patch']['full_count'],
                      'empty_boundary_fibres': result['complete_patch']['empty_fibre_count'],
                      'forbidden_unequal_two_palette_fibres': 24,
                      'source_status': 'not triggered'}, sort_keys=True))


if __name__ == '__main__':
    main()
