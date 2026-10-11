#!/usr/bin/env python3
"""Native read-only runs for returned q2/D; write only fresh review outputs."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

REPO = Path(__file__).resolve().parents[2]
BASE = 'f2692089ad4259808e27d9b7e882ac09505b180a'
KINDS = {'q2': '2026-10-11-n45-s-long-s-t2-q2-restore',
         'block': '2026-10-11-n45-s-long-s-block-transfer'}


def write(root, name, obj):
    with (root / name).open('x') as stream:
        stream.write(json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + '\n')


def pin(path):
    assert stat.S_ISREG(path.lstat().st_mode), str(path)
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def tree(root):
    result = {}
    todo = [root]
    while todo:
        d = todo.pop()
        for p in sorted(d.iterdir()):
            mode = p.lstat().st_mode
            key = p.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                result[key + '/'] = {'type': 'directory'}
                todo.append(p)
            elif stat.S_ISREG(mode):
                result[key] = {'type': 'regular'} | pin(p)
            else:
                raise ValueError('symlink or special original entry: ' + key)
    return result


def snapshot(kind):
    target = REPO / 'audits' / KINDS[kind]
    if kind == 'q2':
        records = json.loads((target / 'custody-before.json').read_bytes())['files']
        expected = {}
        for rec in records:
            assert rec['path'] not in expected or expected[rec['path']] == rec['sha256']
            expected[rec['path']] = rec['sha256']
    else:
        expected = json.loads((target / 'logs/custody-certificate-before.stdout').read_bytes())['files']
    live = {name: pin(REPO / name) for name in sorted(expected)}
    assert all(live[name]['sha256'] == value for name, value in expected.items()), 'original custody input drift'
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO, text=True).strip()
    diff = subprocess.check_output(['git', 'diff', '--binary', 'HEAD'], cwd=REPO)
    assert head == BASE and diff == b''
    return {'target_tree': tree(target), 'guarded_original_files': live,
            'head': head, 'tracked_diff_sha256': hashlib.sha256(diff).hexdigest()}


def run(root, name, argv, overrides=None, expected=0):
    overrides = overrides or {}
    proc = subprocess.run(argv, cwd=REPO, env=os.environ | overrides, capture_output=True)
    for suffix, raw in [('stdout.log', proc.stdout), ('stderr.log', proc.stderr)]:
        with (root / 'logs' / (name + '.' + suffix)).open('xb') as stream:
            stream.write(raw)
    record = {'name': name, 'argv': argv, 'cwd': str(REPO), 'environment_override': overrides,
              'exit': proc.returncode, 'expected_exit': expected,
              'expected_exit_observed': proc.returncode == expected,
              'stdout': 'logs/' + name + '.stdout.log', 'stderr': 'logs/' + name + '.stderr.log',
              'stdout_sha256': hashlib.sha256(proc.stdout).hexdigest(),
              'stderr_sha256': hashlib.sha256(proc.stderr).hexdigest()}
    write(root, 'logs/' + name + '.command.json', record)
    print(json.dumps({'run': name, 'exit': proc.returncode, 'expected': expected}), flush=True)
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--kind', choices=KINDS, required=True)
    args = parser.parse_args()
    kind = args.kind
    target = REPO / 'audits' / KINDS[kind]
    root = REPO / 'audits' / (KINDS[kind] + '-review')
    before = snapshot(kind)
    write(root, 'custody-before.json', before)
    command = [sys.executable, '-B', str(target / 'checker.py'), '--check']
    specs = [('normal', command, {}, 0), ('seed17', command, {'PYTHONHASHSEED': '17'}, 0)]
    if kind == 'q2':
        specs.extend([(name, command + ['--certificate', str(target / 'negative-controls' / filename)], {}, 1)
                      for name, filename in [('wrong-L-map', 'wrong-L-map.json'), ('missing-diagonal', 'missing-diagonal.json')]])
        specs.append(('manifest', [sys.executable, '-B', str(target / 'validate_delivery.py'), '--manifest'], {}, 0))
    else:
        direct = [sys.executable, '-B', str(target / 'direct_enumerator.py'), '--check']
        specs.extend([('direct-normal', direct + ['--certificate', str(target / 'certificate.json')], {}, 0),
                      ('direct-seed17', direct + ['--certificate', str(target / 'certificate.json')], {'PYTHONHASHSEED': '17'}, 0)])
        for name, filename in [('r-colour', 'negative-r-colour.json'), ('empty-cell', 'negative-empty-cell.json'),
                               ('missing-branch', 'negative-missing-branch.json')]:
            specs.append((name, command + ['--certificate', str(target / filename)], {}, 1))
            specs.append(('direct-' + name, direct + ['--certificate', str(target / filename)], {}, 1))
    with ThreadPoolExecutor(max_workers=len(specs)) as pool:
        runs = list(pool.map(lambda s: run(root, *s), specs))
    after = snapshot(kind)
    write(root, 'custody-after.json', after)
    assert before == after, 'readonly replay drift'
    pairs = [('normal', 'seed17')]
    if kind == 'block':
        pairs.append(('direct-normal', 'direct-seed17'))
    equality = {left + '/' + right: all((root / ('logs/' + left + '.' + suffix + '.log')).read_bytes()
                                       == (root / ('logs/' + right + '.' + suffix + '.log')).read_bytes()
                                       for suffix in ('stdout', 'stderr')) for left, right in pairs}
    good = all(r['expected_exit_observed'] for r in runs) and all(equality.values())
    write(root, 'checks.json', {'base': BASE, 'checks_pass': good, 'runs': runs,
                               'normal_seed17_byte_equality': equality, 'original_custody_and_tree_zero_drift': True,
                               'guarded_distinct_original_files': len(before['guarded_original_files']),
                               'reviewed_delivery': pin(target / 'delivery.json'),
                               'scope': 'bounded literal/pin calibration' if kind == 'q2' else 'named C fragment interface calibration; no actual U/G'})
    assert good, 'unexpected native result'
    print(json.dumps({'kind': kind, 'checks_pass': good, 'zero_drift': True}), flush=True)


if __name__ == '__main__':
    main()
