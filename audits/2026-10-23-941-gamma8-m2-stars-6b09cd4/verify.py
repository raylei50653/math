#!/usr/bin/env python3
"""Exclusive-create replay/negative/custody receipts for this narrow audit."""
from copy import deepcopy
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PREV = ROOT / 'audits/2026-10-23-941-gamma8-exterior-6b09cd4/check.py'


def write_new(path, data):
    with path.open('xb') as f:
        f.write(data)


def run(name, args, seed17=False, expected=0, checker=None):
    env = dict(os.environ)
    if seed17:
        env['PYTHONHASHSEED'] = '17'
    command = [sys.executable, '-B'] + (['-O'] if seed17 else [])
    command += [str(checker or HERE / 'check.py')] + args
    p = subprocess.run(command, cwd=ROOT, env=env, capture_output=True)
    write_new(HERE / 'runs' / (name + '.stdout'), p.stdout)
    write_new(HERE / 'runs' / (name + '.stderr'), p.stderr)
    if p.returncode != expected:
        raise ValueError(f'{name}: expected {expected}, got {p.returncode}: {p.stdout!r} {p.stderr!r}')
    return dict(command=command, exit_code=p.returncode,
                stdout_sha256=sha256(p.stdout).hexdigest(), result=json.loads(p.stdout))


def main():
    (HERE / 'runs').mkdir(exist_ok=False)
    normal = run('normal', [])
    seeded = run('seed17', ['--seed', '17'], seed17=True)
    a, b = deepcopy(normal['result']), deepcopy(seeded['result'])
    a.pop('seed'); b.pop('seed')
    if a != b:
        raise ValueError('normal and seed17 differ')
    negative = run('semantic-negative', ['--negative'])
    bad = json.loads((HERE / 'certificate.json').read_text())
    bad['paper_contract']['full_M2_set_retained'] = False
    path = HERE / 'runs/corrupt-certificate.json'
    write_new(path, (json.dumps(bad, sort_keys=True) + '\n').encode())
    corrupt = run('external-corrupt', ['--certificate', str(path)], expected=1)
    path = HERE / 'runs/malformed-certificate.json'
    write_new(path, b'{"schema":"941-gamma8-m2-stars-v1"}\n')
    malformed = run('external-malformed', ['--certificate', str(path)], expected=1)
    previous = run('predecessor-normal', [], checker=PREV)
    previous17 = run('predecessor-seed17', ['--seed', '17'], seed17=True, checker=PREV)
    a, b = deepcopy(previous['result']), deepcopy(previous17['result'])
    a.pop('seed'); b.pop('seed')
    if a != b:
        raise ValueError('predecessor normal and seed17 differ')
    previous_negative = run('predecessor-negative', ['--negative'], checker=PREV)
    manifest = json.loads((HERE / 'INPUTS.json').read_text())
    drift = [r['path'] for r in manifest['inputs'] + manifest['preserved_prior_outputs']
             if sha256((ROOT / r['path']).read_bytes()).hexdigest() != r['sha256']]
    if drift:
        raise ValueError('post-run predecessor drift: ' + repr(drift))
    result = dict(status='PASS', normal=normal, seed17=seeded,
        normal_seed17_equal_except_seed=True, semantic_negative=negative,
        semantic_negative_count=len(negative['result']['semantic_negatives']),
        external_corrupt=corrupt, external_malformed=malformed,
        predecessor_normal=previous, predecessor_seed17=previous17,
        predecessor_normal_seed17_equal_except_seed=True, predecessor_negative=previous_negative,
        predecessor_semantic_negative_count=len(previous_negative['result']['semantic_negatives']),
        immutable_and_prior_drift=drift,
        finite_scope='104 necessary four-face/T-star prefixes; 832 local actions; 4992 palette restrictions',
        paper_scope='j=2, original T degree5, protected external stars and full opposite-side M2 nonempty cut',
        source_realizability='not triggered', eleven_type_exclusions=0,
        caps='complete predecessor fibres including empties and full lifts kept byte-for-byte; not all original caps recomputed')
    write_new(HERE / 'VERIFICATION.json', (json.dumps(result, indent=2, sort_keys=True) + '\n').encode())
    print(json.dumps(dict(status='PASS', normal_seed17_equal=True,
        semantic_negatives=result['semantic_negative_count'], external_negatives=2,
        predecessor_replay='normal/seed17/negative PASS', immutable_drift=0)))


if __name__ == '__main__':
    main()
