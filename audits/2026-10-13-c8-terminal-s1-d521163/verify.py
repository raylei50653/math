#!/usr/bin/env python3
"""Read-only custody and integration check; full mathematical replays are separate."""
import argparse
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def check():
    authority = module('s1_authority', ROOT / 'authority.py')
    inputs = json.loads((ROOT / 'AUTHORITY.json').read_text())
    authority.verify(inputs)
    with gzip.open(ROOT / 'transfer/certificate.json.gz', 'rt') as source:
        primary = json.load(source)
    independent = json.loads((ROOT / 'review/independent_transfer.json').read_text())
    checks = json.loads((ROOT / 'VERIFICATION.json').read_text())
    assert checks['status'] == 'PASS'
    assert checks['claim_status'] == 'PROVED_WITH_COMPLETE_FINITE_EXTERIOR_CERTIFICATE'
    names = {f'{kind}-{i}-{side}-{slot}-{q["query"]}'
             for kind in ('PINCH', 'BRIDGE') for i in range(4)
             for side in range(2) for slot in range(5) for q in inputs['queries']}
    pmap = {row['name']: row for row in primary['exteriors']}
    imap = {row['name']: row for row in independent['records']}
    assert set(pmap) == set(imap) == names and len(names) == 640
    assert primary['B_rows'] == independent['B_rows'] == inputs['B_rows']
    lift_count = 0
    zero_unions = 0
    for name in sorted(names):
        p, i = pmap[name], imap[name]
        assert p['target'] == i['target']
        assert p['graph']['D'] == i['D']
        masks = p['D_orbit_B_masks']
        assert masks == i['masks'] and len(masks) == 31
        allowed = {q: m for q, m in masks.items() if not m & ~p['target']}
        possible = 0
        for mask in allowed.values():
            possible |= mask
        assert allowed == p['allowed_D_orbits'] == i['allowed']
        assert possible == p['maximal_allowed_B_mask'] == i['possible']
        missing = p['target'] & ~possible
        assert missing == p['missing_target_mask'] == i['missing'] and missing
        assert [p['row_full_lift_counts'][b] for b in inputs['B_rows']] == i['direct_P_B_lift_counts']
        lift_count += sum(p['row_full_lift_counts'].values())
        zero_unions += possible == 0
    assert lift_count == 2515696 and zero_unions == 498
    assert primary['summary']['explicit_empty_B_D_fibres'] == 25659554
    assert len(primary['chord_calibrations']) == 256
    digest = hashlib.sha256()
    with gzip.open(ROOT / 'transfer/full_lifts.jsonl.gz', 'rb') as source:
        while chunk := source.read(1024 * 1024):
            digest.update(chunk)
    assert digest.hexdigest() == primary['archive_uncompressed_sha256']
    for entry in checks['checks']:
        assert entry['exit_code'] == 0
        assert (ROOT / entry['log']).is_file()
        if 'checker_sha256' in entry:
            assert sha(ROOT / entry['checker']) == entry['checker_sha256']
    manifest = json.loads((ROOT / 'MANIFEST.json').read_text())
    for entry in manifest['files']:
        path = ROOT / entry['path']
        assert path.stat().st_size == entry['bytes']
        assert sha(path) == entry['sha256'], ('output drift', entry['path'])
    print(json.dumps(dict(status='PASS', scope='custody and certificate integration; see VERIFICATION.json for full replays',
                          frozen_inputs=inputs['input_files'],
                          named_exteriors=640, all_source_targets_excluded=True,
                          remaining_C6_interior_size_bound=None,
                          full_P_lifts=lift_count, literal_B_D_fibres=26214400,
                          frozen_input_drift=0, output_manifest_files=len(manifest['files'])), sort_keys=True))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    parser.parse_args()
    check()
