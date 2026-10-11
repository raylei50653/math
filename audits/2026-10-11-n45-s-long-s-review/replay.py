#!/usr/bin/env python3
"""Capture native read-only A/B replays, guarding all three delivered trees."""
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
BASE = 'f2692089ad4259808e27d9b7e882ac09505b180a'
TARGETS = {key: REPO / ('audits/2026-10-11-n45-s-long-s-' + suffix)
           for key, suffix in [('A', 'direct'), ('B', 'fibre'), ('C', 'joint')]}


def write(name, data):
    with (HERE / name).open('xb') as stream:
        stream.write((json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode())


def file_pin(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': sha256(raw).hexdigest()}


def snapshot():
    trees, inputs, authority_artifacts = {}, {}, {}
    for key, target in TARGETS.items():
        tree = {}
        for path in sorted(target.rglob('*')):
            name = path.relative_to(target).as_posix()
            if path.is_symlink():
                tree[name] = {'type': 'symlink', 'target': os.readlink(path)}
            elif path.is_file():
                tree[name] = {'type': 'regular'} | file_pin(path)
            elif path.is_dir():
                tree[name + '/'] = {'type': 'directory'}
            else:
                tree[name] = {'type': 'other'}
        trees[key] = tree
        source = json.loads((target / 'inputs.json').read_bytes())
        for item in source.get('inputs', source.get('entries', [])):
            inputs[item['path']] = file_pin(REPO / item['path'])
        authority_artifacts[key] = {'path': target.relative_to(REPO).as_posix(),
                                   'artifacts': {name: file_pin(target / name)
                                    for name in ['REPORT.md', 'claims.json', 'inputs.json', 'delivery.json']}}
        if (target / 'certificate.json').exists():
            authority_artifacts[key]['artifacts']['certificate.json'] = file_pin(target / 'certificate.json')
    return {'original_trees': trees, 'live_inputs': inputs,
            'authority_artifacts': authority_artifacts,
            'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO, text=True).strip(),
            'tracked_diff': subprocess.check_output(['git', 'diff', '--name-only', 'HEAD'], cwd=REPO, text=True)}


def run(spec):
    name, argv, overrides, expected_exit = spec
    proc = subprocess.run(argv, cwd=REPO, env=os.environ | overrides, capture_output=True)
    for suffix, data in [('stdout.log', proc.stdout), ('stderr.log', proc.stderr)]:
        with (HERE / 'logs' / (name + '.' + suffix)).open('xb') as stream:
            stream.write(data)
    record = {'name': name, 'argv': argv, 'cwd': str(REPO), 'environment_override': overrides,
              'exit': proc.returncode, 'expected_exit': expected_exit,
              'expected_exit_observed': proc.returncode == expected_exit,
              'stdout': 'logs/' + name + '.stdout.log', 'stderr': 'logs/' + name + '.stderr.log',
              'stdout_sha256': sha256(proc.stdout).hexdigest(), 'stderr_sha256': sha256(proc.stderr).hexdigest()}
    write('logs/' + name + '.command.json', record)
    print(json.dumps({'run': name, 'exit': proc.returncode,
                      'expected_exit_observed': record['expected_exit_observed']}), flush=True)
    return record


def main():
    before = snapshot()
    if before['head'] != BASE or before['tracked_diff']:
        raise ValueError('BASE/head or tracked files changed; refusing to refresh pins')
    write('custody-before.json', before)
    a, b = TARGETS['A'], TARGETS['B']
    command = [sys.executable, '-B', str(b / 'checker.py'), '--check']
    specs = [
        ('A-contents-manifest', [sys.executable, '-B', str(a / 'validate.py'),
                                '--contents', '--manifest', str(a / 'delivery.json')], {}, 0),
        ('B-normal', command, {}, 0),
        ('B-seed17', command, {'PYTHONHASHSEED': '17'}, 0),
        ('B-bad-C-assignment', command + ['--certificate', str(b / 'negative-corrupt-certificate.json')], {}, 1),
    ]
    with ThreadPoolExecutor(max_workers=4) as pool:
        runs = list(pool.map(run, specs))
    after = snapshot()
    write('custody-after.json', after)
    drift = {section: before[section] != after[section] for section in before}
    seed_equal = (HERE / 'logs/B-normal.stdout.log').read_bytes() == (HERE / 'logs/B-seed17.stdout.log').read_bytes()
    negative_stage = b'certificate mismatch' in (HERE / 'logs/B-bad-C-assignment.stderr.log').read_bytes()
    good = all(r['expected_exit_observed'] for r in runs) and not any(drift.values()) and seed_equal and negative_stage
    write('checks.json', {'task_id': 'N45-S-LONG-S-REVIEW', 'base': BASE, 'runs': runs,
                        'checks_pass': good, 'normal_seed17_stdout_byte_equal': seed_equal,
                        'negative_certificate_mismatch_observed': negative_stage,
                        'custody_drift': drift, 'live_input_union_count': len(before['live_inputs']),
                        'C_checks': '../2026-10-11-n45-s-long-s-joint-review/checks.json',
                        'scope': 'custody and fixed finite calibration; no finite target-source acceptance'})
    write('input-pins.json', {'base': BASE, 'reviewed_deliveries': before['authority_artifacts'],
                            'live_input_union_count': len(before['live_inputs']),
                            'C_independent_judgment': file_pin(REPO / 'audits/2026-10-11-n45-s-long-s-joint-review/independent-judgment.json')})
    print(json.dumps({'checks_pass': good, 'normal_seed17_stdout_byte_equal': seed_equal,
                      'custody_drift': drift, 'live_input_union_count': len(before['live_inputs'])}), flush=True)
    return 0 if good else 1


if __name__ == '__main__':
    raise SystemExit(main())
