#!/usr/bin/env python3
"""Fresh verification record, immutable inputs and corruption control."""
import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run(argv):
    p = subprocess.run([sys.executable, '-B', *map(str, argv)], capture_output=True,
                       text=True, env=dict(os.environ, PYTHONHASHSEED='17'))
    return {'command': list(map(str, argv)), 'exit_code': p.returncode,
            'stdout': p.stdout, 'stderr': p.stderr}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    assert not args.output.exists(), 'refuse overwrite'
    manifest = json.loads((ROOT/'INPUTS.json').read_text())
    for record in manifest['inputs']:
        assert digest(ROOT/'frozen'/record['path']) == record['sha256']
    cert = ROOT/'forest/certificate.json.gz'
    before = digest(cert)
    good = run([ROOT/'forest/check.py', '--check'])
    assert good['exit_code'] == 0, good
    # Delete one actual full lift inside a supported H cell; keep valid gzip/JSON.
    with tempfile.TemporaryDirectory(prefix='forest-negative-') as temp:
        data = json.loads(gzip.decompress(cert.read_bytes()))
        cell = next(c for row in data['graphs'][0]['rows'] for c in row['cells'] if c)
        removed = cell.pop()
        corrupt = Path(temp)/'corrupt.json.gz'
        corrupt.write_bytes(gzip.compress(json.dumps(data, sort_keys=True,
                           separators=(',', ':')).encode(), mtime=0))
        bad = run([ROOT/'forest/check.py', '--check', '--certificate', corrupt])
        assert bad['exit_code'] != 0 and 'certificate mismatch' in bad['stderr'], bad
    assert digest(cert) == before
    child = json.loads((ROOT/'representatives/review_checks.json').read_text())
    assert all(v['normal_seed17']['exit_code'] == 0 and
               v['corrupted_copy']['exit_code'] != 0 and
               v['original_hashes_unchanged'] for v in child.values())
    result = {'forest_seed17': good, 'forest_deleted_lift_negative': bad,
              'removed_lift': removed, 'forest_certificate_sha256': before,
              'frozen_inputs_unchanged': True, 'original_forest_certificate_unchanged': True,
              'three_subpackage_checks': 'representatives/review_checks.json',
              'three_subpackage_checks_sha256': digest(ROOT/'representatives/review_checks.json'),
              'initial_generation_note': 'Start/end face orientations corrected before first certificate creation; final directed-dart and rotation checks pass.',
              'scope': 'Finite controls and frozen inputs; actual minimum source not triggered.'}
    with args.output.open('x') as f:
        json.dump(result, f, indent=2)
        f.write('\n')
    print('PASS: forest seed17, deleted-lift rejection, immutable evidence; three subpackage controls recorded')


if __name__ == '__main__':
    main()
