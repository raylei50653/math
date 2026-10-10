#!/usr/bin/env python3
"""Freeze delivered independent audits and record actual pre-adoption replays."""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import time
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def digest(data):
    return hashlib.sha256(data).hexdigest()


def inventory(path):
    result = {}
    for p in sorted(path.rglob('*')):
        if p.is_dir() and not p.is_symlink():
            continue
        assert p.is_file() and not p.is_symlink(), p
        data = p.read_bytes()
        result[p.relative_to(path).as_posix()] = {
            'kind': 'regular', 'bytes': len(data),
            'mode': stat.S_IMODE(p.stat().st_mode), 'sha256': digest(data),
        }
    return result


def write(name, value):
    with (HERE / name).open('x') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write('\n')


def run(job):
    name, command, seed = job
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0')
    if seed:
        env['PYTHONHASHSEED'] = '17'
    else:
        env.pop('PYTHONHASHSEED', None)
    started = datetime.now(timezone.utc).isoformat()
    clock = time.monotonic()
    p = subprocess.run(command, cwd=ROOT, env=env, capture_output=True)
    for channel, data in [('stdout', p.stdout), ('stderr', p.stderr)]:
        with (HERE / 'logs' / (name + '.' + channel + '.txt')).open('xb') as f:
            f.write(data)
    return {'name': name, 'command': command, 'cwd': str(ROOT),
            'environment': {'PYTHONDONTWRITEBYTECODE': '1', 'GIT_OPTIONAL_LOCKS': '0',
                            'PYTHONHASHSEED': '17' if seed else 'unset'},
            'start_UTC': started, 'elapsed_seconds': round(time.monotonic()-clock, 3),
            'exit_code': p.returncode,
            'stdout': 'logs/' + name + '.stdout.txt', 'stdout_sha256': digest(p.stdout),
            'stderr': 'logs/' + name + '.stderr.txt', 'stderr_sha256': digest(p.stderr)}


def main():
    intake = json.loads((HERE/'intake.json').read_text())
    for path, info in intake['workers'].items():
        assert inventory(ROOT/path) == info['fulltree'], path
        assert inventory(HERE/info['frozen']) == info['fulltree'], path
    for path, item in intake['shared_before'].items():
        expected = item['sha256'] if isinstance(item, dict) else item
        assert digest((ROOT/path).read_bytes()) == expected, path
    reviews = {}
    for suffix in ['h2a', 'h2r', 'h2c']:
        path = 'audits/2026-10-10-n45-' + suffix
        frozen = 'frozen/' + path
        before = inventory(ROOT/path)
        shutil.copytree(ROOT/path, HERE/frozen, copy_function=shutil.copy2)
        assert before == inventory(HERE/frozen) == inventory(ROOT/path)
        reviews[path] = {'frozen': frozen, 'fulltree': before}
    write('reviewer-intake.json', {'BASE': intake['BASE'], 'reviews': reviews})
    jobs = []
    for suffix in ['h2a', 'h2r', 'h2c']:
        command = ['python3', '-B', 'audits/2026-10-10-n45-' + suffix + '/verifier.py']
        if suffix != 'h2c':
            command.append('--check')
        for seed in [False, True]:
            jobs.append((suffix+'-parent-'+('seed17' if seed else 'normal'), command, seed))
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        runs = list(pool.map(run, jobs))
    pairs = []
    for a, b in zip(runs[::2], runs[1::2]):
        pairs.append({'pair': a['name'].removesuffix('-normal'),
                      'both_exit0': a['exit_code'] == b['exit_code'] == 0,
                      'stdout_identical': a['stdout_sha256'] == b['stdout_sha256'],
                      'stderr_identical': a['stderr_sha256'] == b['stderr_sha256']})
    write('reviewer-parent-replays.json', {'runs': runs, 'pairs': pairs})
    for path, info in reviews.items():
        assert inventory(ROOT/path) == info['fulltree'], path
    assert all(p['both_exit0'] and p['stdout_identical'] and p['stderr_identical'] for p in pairs)
    print(json.dumps({'reviewer_files': sum(len(v['fulltree']) for v in reviews.values()),
                      'runs': len(runs), 'pairs_identical': len(pairs)}, sort_keys=True))


if __name__ == '__main__':
    main()
