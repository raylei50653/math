#!/usr/bin/env python3
"""Exclusive-create process receipts and independent worker-orbit comparison."""
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
    with path.open('xb') as f:
        f.write(data)


def run(name, args, seed17=False, expected=0):
    env = dict(os.environ)
    if seed17:
        env['PYTHONHASHSEED'] = '17'
    command = [sys.executable, '-B'] + (['-O'] if seed17 else []) + [str(HERE / 'check.py')] + args
    p = subprocess.run(command, cwd=ROOT, env=env, capture_output=True)
    write_new(HERE / 'runs' / (name + '.stdout'), p.stdout)
    write_new(HERE / 'runs' / (name + '.stderr'), p.stderr)
    if p.returncode != expected:
        raise ValueError(f'{name}: expected {expected}, got {p.returncode}: {p.stdout!r}')
    return dict(command=command, exit_code=p.returncode, stdout_sha256=sha256(p.stdout).hexdigest(), result=json.loads(p.stdout))


def main():
    (HERE / 'runs').mkdir(exist_ok=False)
    normal = run('normal', [])
    seeded = run('seed17', ['--seed', '17'], True)
    a, b = deepcopy(normal['result']), deepcopy(seeded['result']); a.pop('seed'); b.pop('seed')
    if a != b:
        raise ValueError('normal and seed17 differ')
    negative = run('semantic-negative', ['--negative'])
    c = json.loads((HERE / 'certificate-v2.json').read_text())
    worker = json.loads((HERE / 'workers/stars/orbit.json').read_text())
    normalized = [dict(id=cell['id'], rows=[dict(M02=int(r['M02']), N13=int(r['N13']), K02=int(r['same_K02']),
        colors=r['colors'], six_palette_components=r['full_local_palette_components']) for r in cell['rows']])
        for cell in worker['rows']]
    if normalized != c['complete_local_orbits']:
        raise ValueError('independent worker complete orbit differs')
    c['paper_contract']['full_M2_separator_not_single_T_neighbor'] = False
    bad = HERE / 'runs/corrupt-certificate.json'
    write_new(bad, (json.dumps(c, sort_keys=True) + '\n').encode())
    corrupted = run('corrupt-negative', ['--certificate', str(bad)], expected=1)
    malformed = HERE / 'runs/malformed-certificate.json'
    write_new(malformed, b'{"schema":"941-gamma8-exterior-v1"}\n')
    missing = run('malformed-negative', ['--certificate', str(malformed)], expected=1)
    m = json.loads((HERE / 'INPUTS.json').read_text())
    drift = [r['path'] for r in m['inputs'] + m['preserved_prior_outputs']
             if sha256((ROOT / r['path']).read_bytes()).hexdigest() != r['sha256']]
    if drift:
        raise ValueError('post-run predecessor drift')
    receipt = dict(status='PASS', normal=normal, seed17=seeded, normal_seed17_equal_except_seed=True,
        semantic_negative=negative, semantic_negative_count=len(negative['result']['semantic_negatives']),
        external_corrupt_certificate=corrupted, malformed_certificate=missing,
        independent_worker_full_local_orbits_equal=True, immutable_and_prior_drift=drift,
        frozen_input_count=len(m['inputs']), prior_output_count=len(m['preserved_prior_outputs']),
        finite_scope='1056 literal endpoint rows; 88 complete local graph restrictions; no exterior completion search',
        paper_authority='L/R4 O5 strict exterior private lower bounds; arbitrary-j Gamma8 complete swaps and separators',
        source_realizability='not triggered', eleven_type_exclusions=0, initial_pair_exclusions=0,
        full_original_caps='byte/SHA custody; predecessor local replay; not all original caps recomputed')
    write_new(HERE / 'VERIFICATION.json', (json.dumps(receipt, sort_keys=True, indent=2) + '\n').encode())
    print(json.dumps(dict(status='PASS', normal_seed17_equal=True,
        semantic_negatives=receipt['semantic_negative_count'], external_negatives=2,
        worker_orbit_equal=True, predecessor_drift=0)))


if __name__ == '__main__':
    main()
