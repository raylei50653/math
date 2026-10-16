#!/usr/bin/env python3
"""Replay and meaningful corrupted-complete-fibre negative controls."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
CHECKER = ROOT / 'matching_check.py'
CERT = ROOT / 'matching_certificate-v3.json'


def run(extra):
    command = [sys.executable, str(CHECKER)] + extra
    process = subprocess.run(command, text=True, capture_output=True)
    return {'command_arguments': extra, 'returncode': process.returncode,
            'stdout': process.stdout, 'stderr': process.stderr}


def main():
    normal = run([])
    seed17 = run(['--seed', '17'])
    if normal['returncode'] or seed17['returncode']:
        raise ValueError('normal or seed17 replay failed')
    baseline = json.loads(CERT.read_text())
    variants = []
    changed = copy.deepcopy(baseline)
    states = changed['patches'][0]['all_1206_state_fibres']
    empty = next(key for key, value in states.items() if not value)
    del states[empty]
    variants.append(('missing_empty_state', changed, {'removed_state': empty}))
    changed = copy.deepcopy(baseline)
    witness = next(r for r in changed['controls'][0]['all_exterior_matching_lifts'] if r['mark_pattern'] == '111')
    witness['paths'][0]['parity'] ^= 1
    variants.append(('outside_even_parity_corrupted', changed, {'exterior_lift': witness['id']}))
    changed = copy.deepcopy(baseline)
    witness = next(r for r in changed['controls'][0]['all_exterior_matching_lifts'] if r['mark_pattern'] == '111')
    path = next(q for q in witness['paths'] if q['length'] == 0)
    path['length'] = 2
    variants.append(('zero_path_length_corrupted', changed, {'ports': path['ports']}))
    changed = copy.deepcopy(baseline)
    witness = next(r for r in changed['controls'][2]['all_global_pm_lifts'] if r['mark_pattern'] == '111' and r['all_labelled_tait_lifts'])
    del witness['all_labelled_tait_lifts'][0]
    variants.append(('missing_complete_tait_lift', changed, {'global_matching': witness['id']}))
    negatives = []
    with tempfile.TemporaryDirectory(prefix='seven-disk-matching-') as tmp:
        for name, payload, mutation in variants:
            path = Path(tmp) / (name+'.json')
            raw = json.dumps(payload, indent=2)+'\n'
            path.write_text(raw)
            result = run(['--certificate', str(path)])
            if result['returncode'] == 0 or 'complete certificate exact replay' not in result['stderr']:
                raise ValueError('negative control was not rejected as expected: '+name)
            result['command_arguments'] = ['--certificate', '<temporary corrupted certificate>']
            negatives.append({'name': name, 'mutation': mutation, 'mutated_sha256': hashlib.sha256(raw.encode()).hexdigest(), **result})
    result = {'status': 'PASS', 'certificate': CERT.name, 'normal': normal, 'seed17': seed17,
              'negative_controls': negatives, 'source_realizability': 'not triggered'}
    destination = ROOT / 'matching_verification.json'
    with destination.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(json.dumps({'status': 'PASS', 'normal': 0, 'seed17': 0,
                      'negative_controls_rejected': len(negatives)}))


if __name__ == '__main__':
    main()
