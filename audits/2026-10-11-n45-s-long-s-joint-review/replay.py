#!/usr/bin/env python3
"""Independent custody snapshots and read-only replays of the delivered C task."""
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TARGET = ROOT / 'audits/2026-10-11-n45-s-long-s-joint'
BASE = 'f2692089ad4259808e27d9b7e882ac09505b180a'


def write(name, value):
    with (HERE / name).open('xb') as stream:
        stream.write((json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2) + '\n').encode())


def snapshot():
    tree = {}
    for path in sorted(TARGET.rglob('*')):
        relative = str(path.relative_to(TARGET))
        if path.is_symlink():
            tree[relative] = {'type': 'symlink', 'target': os.readlink(path)}
        elif path.is_file():
            data = path.read_bytes()
            tree[relative] = {'type': 'regular', 'bytes': len(data), 'sha256': sha256(data).hexdigest()}
        elif path.is_dir():
            tree[relative + '/'] = {'type': 'directory'}
        else:
            tree[relative] = {'type': 'other'}
    manifest = json.loads((TARGET / 'inputs.json').read_bytes())
    inputs = {}
    for item in manifest['inputs']:
        path = ROOT / item['path']
        data = path.read_bytes()
        inputs[item['path']] = {'bytes': len(data), 'sha256': sha256(data).hexdigest()}
    return {'target_tree': tree, 'live_inputs': inputs,
            'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
            'tracked_diff': subprocess.check_output(['git', 'diff', '--name-only', 'HEAD'], cwd=ROOT, text=True)}


def run(spec):
    name, argv, overrides, expected_exit = spec
    proc = subprocess.run(argv, cwd=ROOT, env=os.environ | overrides, capture_output=True)
    for suffix, data in [('stdout.log', proc.stdout), ('stderr.log', proc.stderr)]:
        with (HERE / 'logs' / (name + '.' + suffix)).open('xb') as stream:
            stream.write(data)
    record = {'name': name, 'argv': argv, 'cwd': str(ROOT), 'environment_override': overrides,
              'exit': proc.returncode, 'expected_exit': expected_exit,
              'expected_exit_observed': proc.returncode == expected_exit,
              'stdout': 'logs/' + name + '.stdout.log', 'stderr': 'logs/' + name + '.stderr.log',
              'stdout_sha256': sha256(proc.stdout).hexdigest(), 'stderr_sha256': sha256(proc.stderr).hexdigest()}
    write('logs/' + name + '.command.json', record)
    print(json.dumps({'run': name, 'exit': proc.returncode, 'expected_exit_observed': record['expected_exit_observed']}), flush=True)
    return record


def main():
    (HERE / 'logs').mkdir()
    before = snapshot()
    if before['head'] != BASE or before['tracked_diff']:
        raise ValueError('BASE or tracked worktree differs; do not refresh pins')
    write('custody-before.json', before)
    command = [sys.executable, '-B', str(TARGET / 'checker.py'), '--check']
    specs = [
        ('normal', command, {}, 0),
        ('seed17', command, {'PYTHONHASHSEED': '17'}, 0),
        ('bad-C-r-colour', command + ['--certificate', str(TARGET / 'bad-C-r-colour.json')], {}, 1),
        ('missing-empty-ambient', command + ['--certificate', str(TARGET / 'missing-empty-ambient.json')], {}, 1),
        ('delivery', [sys.executable, '-B', str(TARGET / 'seal_delivery.py'), '--check'], {}, 0),
    ]
    with ThreadPoolExecutor(max_workers=4) as pool:
        runs = list(pool.map(run, specs))
    after = snapshot()
    write('custody-after.json', after)
    drift = {section: before[section] != after[section] for section in before}
    negative_details = {}
    for name, fragment in [('bad-C-r-colour', 'C_assignments[0][0]: value differs'),
                           ('missing-empty-ambient', 'all_ambient_C_r_tuple_fibres: length differs')]:
        log = (HERE / 'logs' / (name + '.stderr.log')).read_text()
        negative_details[name] = {'expected_rejection_stage': fragment, 'observed': fragment in log}
    normal_seed_equal = (HERE / runs[0]['stdout']).read_bytes() == (HERE / runs[1]['stdout']).read_bytes()
    result = {'task_id': 'N45-S-LONG-S-JOINT-REVIEW', 'base': BASE,
              'reviewed_delivery_sha256': sha256((TARGET / 'delivery.json').read_bytes()).hexdigest(),
              'reviewed_certificate_sha256': sha256((TARGET / 'certificate.json').read_bytes()).hexdigest(),
              'runs': runs, 'normal_seed17_stdout_byte_equal': normal_seed_equal,
              'custody_drift': drift, 'negative_rejection_stages': negative_details,
              'scope': 'read-only finite-interface replay; no source-exclusion or private-cover acceptance'}
    good = all(z['expected_exit_observed'] for z in runs) and not any(drift.values()) and normal_seed_equal and all(z['observed'] for z in negative_details.values())
    result['checks_pass'] = good
    write('checks.json', result)
    print(json.dumps({'checks_pass': good, 'normal_seed17_stdout_byte_equal': normal_seed_equal, 'custody_drift': drift}), flush=True)
    return 0 if good else 1


if __name__ == '__main__':
    raise SystemExit(main())
