#!/usr/bin/env python3
"""Native read-only replay and custody guard for the delivered q0 restoration."""
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
TARGET = REPO / 'audits/2026-10-11-n45-s-long-s-t2-q0-restore'
BASE = 'f2692089ad4259808e27d9b7e882ac09505b180a'
EXTRA_SOURCES = ['artifacts/c5_excess_two_e4/REPORT.md',
                 'docs/c5_phase_b_common_lemmas.md', 'docs/c5_short_support_singleton.md']


def write(name, data):
    with (HERE / name).open('xb') as stream:
        stream.write((json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode())


def pin(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': sha256(raw).hexdigest()}


def snapshot():
    tree = {}
    for path in sorted(TARGET.rglob('*')):
        name = path.relative_to(TARGET).as_posix()
        if path.is_symlink():
            tree[name] = {'type': 'symlink', 'target': os.readlink(path)}
        elif path.is_file():
            tree[name] = {'type': 'regular'} | pin(path)
        elif path.is_dir():
            tree[name + '/'] = {'type': 'directory'}
        else:
            tree[name] = {'type': 'other'}
    recorded = json.loads((TARGET / 'custody-before.json').read_bytes())['files']
    files = {name: pin(REPO / name) for name in sorted(set(recorded) | set(EXTRA_SOURCES))}
    return {'target_tree': tree, 'authority_and_old_certificate_files': files,
            'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO, text=True).strip(),
            'tracked_diff': subprocess.check_output(['git', 'diff', '--name-only', 'HEAD'], cwd=REPO, text=True)}


def freeze_extra_sources():
    items = []
    for name in EXTRA_SOURCES:
        raw = subprocess.check_output(['git', 'show', BASE + ':' + name], cwd=REPO)
        if raw != (REPO / name).read_bytes():
            raise ValueError('live extra authority differs from BASE: ' + name)
        frozen = 'authority/' + name
        path = HERE / frozen
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as stream:
            stream.write(raw)
        items.append({'path': name, 'frozen_path': frozen, 'base': BASE, 'authority': 'BASE Git blob',
                      'git_blob': subprocess.check_output(['git', 'rev-parse', BASE + ':' + name], cwd=REPO, text=True).strip(),
                      **pin(path)})
    write('extra-authority-inputs.json', {'base': BASE, 'scope': 'independent N-diagonal dependency inspection',
                                        'inputs': items})


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
        raise ValueError('HEAD/BASE or tracked files changed; refusing to refresh pins')
    write('custody-before.json', before)
    freeze_extra_sources()
    command = [sys.executable, '-B', str(TARGET / 'audit.py'), 'check']
    specs = [
        ('normal', command, {}, 0),
        ('seed17', command, {'PYTHONHASHSEED': '17'}, 0),
        ('bad-q2-column', command + ['--certificate', str(TARGET / 'negative-controls/bad-q2-column.json')], {}, 1),
        ('missing-diagonal', command + ['--coverage', str(TARGET / 'negative-controls/missing-diagonal.json')], {}, 1),
        ('delivery', [sys.executable, '-B', str(TARGET / 'audit.py'), 'verify-delivery'], {}, 0),
    ]
    with ThreadPoolExecutor(max_workers=5) as pool:
        runs = list(pool.map(run, specs))
    after = snapshot()
    write('custody-after.json', after)
    drift = {section: before[section] != after[section] for section in before}
    seed_equal = all((HERE / ('logs/normal.' + suffix + '.log')).read_bytes()
                     == (HERE / ('logs/seed17.' + suffix + '.log')).read_bytes()
                     for suffix in ['stdout', 'stderr'])
    stages = {name: fragment in (HERE / ('logs/' + name + '.stderr.log')).read_text()
              for name, fragment in [('bad-q2-column', 'calibration certificate mismatch'),
                                     ('missing-diagonal', 'coverage mismatch')]}
    good = all(run['expected_exit_observed'] for run in runs) and seed_equal and all(stages.values()) and not any(drift.values())
    write('checks.json', {'base': BASE, 'checks_pass': good, 'runs': runs,
                         'normal_seed17_stdout_stderr_byte_equal': seed_equal,
                         'negative_rejection_stages': stages, 'custody_drift': drift,
                         'recorded_target_custody_files': 60,
                         'guarded_authority_union': len(before['authority_and_old_certificate_files']),
                         'reviewed_delivery_sha256': pin(TARGET / 'delivery.json')['sha256'],
                         'scope': 'bounded metadata/algebra calibration only; no target source validation'})
    print(json.dumps({'checks_pass': good, 'normal_seed17_stdout_stderr_byte_equal': seed_equal,
                      'custody_drift': drift}), flush=True)
    return 0 if good else 1


if __name__ == '__main__':
    raise SystemExit(main())
