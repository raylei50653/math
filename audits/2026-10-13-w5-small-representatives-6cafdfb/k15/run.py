#!/usr/bin/env python3
"""Read-only K15 replay; writes receipts only in this isolated audit."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib
import json
import os
import subprocess
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PREFIX = 'audits/2026-10-13-k15-sphere-6cafdfb/'
COMMANDS = {
    'main-normal': (['python3', '-B', PREFIX + 'check.py', '--check'], None),
    'main-seed17': (['python3', '-B', PREFIX + 'check.py', '--check'], '17'),
    'independent-normal': (['python3', '-B', PREFIX + 'independent/compare.py'], None),
    'independent-seed17': (['python3', '-B', PREFIX + 'independent/compare.py'], '17'),
}


def run(name):
    command, seed = COMMANDS[name]
    env = os.environ.copy()
    if seed is not None:
        env['PYTHONHASHSEED'] = seed
    started = time.monotonic()
    result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True)
    for suffix, payload in [('stdout.log', result.stdout), ('stderr.log', result.stderr)]:
        with (HERE / 'logs' / (name + '.' + suffix)).open('xb') as stream:
            stream.write(payload)
    receipt = {'command': command, 'cwd': str(ROOT), 'PYTHONHASHSEED': seed,
               'elapsed_seconds': time.monotonic() - started, 'returncode': result.returncode,
               'stdout_sha256': hashlib.sha256(result.stdout).hexdigest(),
               'stderr_sha256': hashlib.sha256(result.stderr).hexdigest()}
    with (HERE / 'logs' / (name + '.receipt.json')).open('x') as stream:
        json.dump(receipt, stream, sort_keys=True, indent=2)
        stream.write('\n')
    print(name, json.dumps(receipt, sort_keys=True), flush=True)
    return result.returncode


if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(run, COMMANDS))
    raise SystemExit(max(results))
