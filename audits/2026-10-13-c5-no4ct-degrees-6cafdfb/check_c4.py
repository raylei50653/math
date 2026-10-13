#!/usr/bin/env python3
"""Replay finite C4 witnesses under the new relative-size paper premise."""
import argparse
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent


def calculate():
    manifest = json.loads((HERE / 'INPUTS.json').read_text())
    for row in manifest['files']:
        actual = hashlib.sha256((HERE / 'frozen' / row['path']).read_bytes()).hexdigest()
        if actual != row['sha256']:
            raise ValueError('frozen input drift: ' + row['path'])
    source = HERE / 'frozen/audits/2026-10-12-c5-saturation-degree-bound/controls/check.py'
    spec = importlib.util.spec_from_file_location('frozen_degree', source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    catalogue = json.loads(module.CATALOGUE.read_text())
    result = module.c4_control(catalogue, seed=0)
    result.pop('universal_premise')
    result['paper_premise'] = (
        'k is globally minimal among all outside-K C5 disks; '
        'the tested C4 source has s<k interior vertices. '
        'Its dummy augmentation has s interiors, hence lies in K by minimality. '
        'This finite replay proves no universal C4 theorem.')
    summary = result['summary']
    summary['possible_C4_masks_under_relative_size_premise'] = summary.pop(
        'possible_C4_masks_under_external_premise')
    return json.loads(json.dumps(result))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--write', action='store_true')
    group.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = calculate()
    path = HERE / 'C4_CERTIFICATE.json.gz'
    if args.write:
        with path.open('xb') as stream:
            stream.write(gzip.compress((json.dumps(result, indent=2) + '\n').encode(), mtime=0))
    elif json.loads(gzip.decompress(path.read_bytes())) != result:
        raise ValueError('C4 certificate mismatch')
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
