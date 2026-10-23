#!/usr/bin/env python3
"""Exclusive-create process receipts, including malformed/external negatives."""
from copy import deepcopy
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def write_new(path, data):
    with path.open('xb') as stream:
        stream.write(data)


def run(name, arguments, seed17=False, expected=0):
    env = dict(os.environ)
    if seed17:
        env['PYTHONHASHSEED'] = '17'
    command = [sys.executable, '-B'] + (['-O'] if seed17 else []) + [str(HERE / 'check.py')] + arguments
    result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True)
    write_new(HERE / 'runs' / (name + '.stdout'), result.stdout)
    write_new(HERE / 'runs' / (name + '.stderr'), result.stderr)
    if result.returncode != expected:
        raise ValueError(f'{name}: expected {expected}, got {result.returncode}: {result.stdout!r}')
    return dict(command=command, exit_code=result.returncode,
                stdout_sha256=sha256(result.stdout).hexdigest(), result=json.loads(result.stdout))


def main():
    (HERE / 'runs').mkdir(exist_ok=False)
    normal = run('normal', [])
    seed17 = run('seed17', ['--seed', '17'], True)
    a, b = deepcopy(normal['result']), deepcopy(seed17['result'])
    a.pop('seed'); b.pop('seed')
    if a != b:
        raise ValueError('independent process replays differ')
    semantic = run('semantic-negative', ['--negative'])
    bad = json.loads((HERE / 'certificate.json').read_text())
    bad['paper_claims']['alpha_pair_allowed_two_shared_colors'].append([2, 3])
    bad_path = HERE / 'runs' / 'corrupt-certificate.json'
    write_new(bad_path, (json.dumps(bad, sort_keys=True) + '\n').encode())
    external = run('external-negative', ['--certificate', str(bad_path)], expected=1)
    malformed_path = HERE / 'runs' / 'malformed-certificate.json'
    write_new(malformed_path, b'{"schema":"941-patch-order-v1"}\n')
    malformed = run('malformed-negative', ['--certificate', str(malformed_path)], expected=1)
    manifest = json.loads((HERE / 'INPUTS.json').read_text())
    drift = [r['path'] for r in manifest['inputs']
             if sha256((ROOT / r['path']).read_bytes()).hexdigest() != r['sha256']]
    if drift:
        raise ValueError('immutable post-run drift: ' + repr(drift))
    receipt = dict(status='PASS', normal=normal, seed17=seed17,
                   normal_seed17_equal_except_seed=True, semantic_negative=semantic,
                   semantic_negative_count=len(semantic['result']['semantic_negatives']),
                   external_corrupt_certificate=external, malformed_certificate=malformed,
                   immutable_input_drift=drift,
                   inherited_full_lifts='byte and SHA custody; round5 local calibration replayed',
                   general_topology='paper proof; not established by finite calibration',
                   source_realizability='not triggered', new_initial_pair_exclusions=0)
    write_new(HERE / 'VERIFICATION.json', (json.dumps(receipt, sort_keys=True, indent=2) + '\n').encode())
    print(json.dumps(dict(status='PASS', independent_seed17_equal=True,
                         semantic_negatives=receipt['semantic_negative_count'], external_negatives=2,
                         immutable_input_drift=0)))


if __name__ == '__main__':
    main()
