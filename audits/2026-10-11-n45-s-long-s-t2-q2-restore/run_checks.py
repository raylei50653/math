#!/usr/bin/env python3
"""Capture native bounded checks, writing only the exclusive task directory."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent
BASE = 'f2692089ad4259808e27d9b7e882ac09505b180a'


def save(path, value):
    with path.open('x') as f:
        json.dump(value, f, indent=2, sort_keys=True)
        f.write('\n')


def capture(label, argv, env_updates=None):
    prefix = ROOT / 'logs' / label
    env_updates = env_updates or {}
    save(prefix.with_suffix('.command.json'), {'argv': argv, 'cwd': str(REPO),
                                             'env_updates': env_updates})
    env = dict(os.environ)
    env.update(env_updates)
    start = time.monotonic()
    p = subprocess.run(argv, cwd=REPO, env=env, capture_output=True)
    for suffix, data in [('.stdout', p.stdout), ('.stderr', p.stderr)]:
        with prefix.with_suffix(suffix).open('xb') as f:
            f.write(data)
    save(prefix.with_suffix('.result.json'), {'exit_code': p.returncode,
                                            'elapsed_seconds': time.monotonic() - start,
                                            'stdout_sha256': hashlib.sha256(p.stdout).hexdigest(),
                                            'stderr_sha256': hashlib.sha256(p.stderr).hexdigest()})
    return p


def main():
    assert (ROOT / 'calibration-plan.json').is_file()
    dispatch = REPO / 'audits/2026-10-11-n45-s-long-s-rfibre-dispatch/check_dispatch.py'
    p = capture('dispatch-check', [sys.executable, '-B', str(dispatch), '--check'])
    assert p.returncode == 0
    findings = []
    for label, path in [('missing-no-spoke', 'artifacts/c5_no_spoke_exterior/observations.json'),
                        ('missing-locality', 'artifacts/c5_single_spoke_residual_locality/observations.json')]:
        p = capture(label, ['git', 'cat-file', 'blob', BASE + ':' + path])
        assert p.returncode == 128
        findings.append({'path': path, 'base': BASE, 'native_exit': p.returncode,
                         'authority_admitted': False, 'dependent_finite_replay_executed': False,
                         'status': 'not triggered'})
    checker = str(ROOT / 'checker.py')
    p = capture('calibration-generate', [sys.executable, '-B', checker, '--print-certificate'])
    assert p.returncode == 0
    with (ROOT / 'calibration.json').open('xb') as f:
        f.write(p.stdout)
    normal = capture('calibration-normal', [sys.executable, '-B', checker, '--check'])
    seeded = capture('calibration-seed17', [sys.executable, '-B', checker, '--check'],
                     {'PYTHONHASHSEED': '17'})
    assert normal.returncode == seeded.returncode == 0
    assert normal.stdout == seeded.stdout
    negative = ROOT / 'negative-controls'
    negative.mkdir(exist_ok=False)
    bad_map = json.loads((ROOT / 'calibration.json').read_text())
    bad_map['proof_transports'][1]['L_colour_map'] = [0, 2, 1, 3]
    save(negative / 'wrong-L-map.json', bad_map)
    bad_cell = json.loads((ROOT / 'calibration.json').read_text())
    bad_cell['schedules'][0]['ambient_cells'][0]['pins'].remove([3, 3])
    save(negative / 'missing-diagonal.json', bad_cell)
    negatives = []
    for label in ['wrong-L-map', 'missing-diagonal']:
        p = capture('negative-' + label, [sys.executable, '-B', checker, '--check',
                                         '--certificate', str(negative / (label + '.json'))])
        assert p.returncode != 0
        assert b'calibration certificate mismatch' in p.stderr
        negatives.append({'id': label, 'native_exit': p.returncode,
                          'status': 'triggered and holds', 'bad_certificate_retained': True,
                          'scope': 'fail-closed calibration certificate comparison'})
    save(ROOT / 'checks.json', {'adoption_status': '待獨立驗收',
                              'calibration': {'status': 'triggered and holds',
                                              'normal_exit': normal.returncode,
                                              'seed17_exit': seeded.returncode,
                                              'stdout_byte_equal': True},
                              'negative_controls': negatives, 'missing_BASE_blobs': findings,
                              'old_19_controls_rerun': False,
                              'target_source': {'executed': False, 'trigger_count': None,
                                                'status': 'not triggered'}})
    print(json.dumps({'calibration': 'triggered and holds', 'seed17_byte_equal': True,
                      'negative_controls_rejected': len(negatives), 'missing_BASE_blobs': len(findings),
                      'target_source_executed': False, 'target_trigger_count': None}, sort_keys=True))


if __name__ == '__main__':
    main()
