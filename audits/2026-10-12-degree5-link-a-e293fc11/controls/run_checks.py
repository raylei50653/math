#!/usr/bin/env python3
"""Replay the certificate twice and require rejection of corrupt copies."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
CHECKER = HERE / 'check.py'
CERTIFICATE = HERE / 'certificate.v2.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def command(path, seed):
    return [sys.executable, str(CHECKER), '--check', str(path), '--seed', str(seed)]


def mutate(data, kind):
    controls = data['controls']
    if kind == 'missing_outer_row':
        controls[0]['relations']['all_ten_rows'].pop()
    elif kind == 'wrong_named_label':
        controls[1]['L'][0] = 'wrong_boundary_pin'
    elif kind == 'wrong_full_lift':
        controls[0]['relations']['all_ten_rows'][0]['full_lifts'][0][-1] = 9
    elif kind == 'missing_empty_fiber':
        masks = controls[0]['relations']['all_ten_rows'][0]['center_color_masks']
        masks.pop(masks.index(0))
    elif kind == 'wrong_rotation':
        rotation = controls[0]['rotations']['v']
        rotation[0], rotation[1] = rotation[1], rotation[0]
    elif kind == 'wrong_global_transport':
        data['contact_enumeration']['records'][0]['transport']['global_vertex_map']['a'] = 'b'
    elif kind == 'missing_orientation_record':
        data['contact_enumeration']['records'].pop()
    else:
        raise ValueError(kind)


def main():
    before = sha(CERTIFICATE)
    payload = json.loads(CERTIFICATE.read_text())
    results = []
    for seed in (0, 17):
        result = subprocess.run(command(CERTIFICATE, seed), capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError(result.stdout + result.stderr)
        results.append({'case': f'canonical_seed_{seed}', 'returncode': result.returncode,
                        'stdout': result.stdout.strip(), 'stderr': result.stderr.strip(),
                        'status': 'triggered and holds'})
    cases = ('missing_outer_row', 'wrong_named_label', 'wrong_full_lift', 'missing_empty_fiber',
             'wrong_rotation', 'wrong_global_transport', 'missing_orientation_record')
    with tempfile.TemporaryDirectory(prefix='negative-', dir=HERE) as tmp:
        for kind in cases:
            damaged = copy.deepcopy(payload)
            mutate(damaged, kind)
            path = Path(tmp) / f'{kind}.json'
            with path.open('x') as output:
                output.write(json.dumps(damaged, sort_keys=True, separators=(',', ':')) + '\n')
            initial = sha(path)
            result = subprocess.run(command(path, 17), capture_output=True, text=True)
            if result.returncode != 1 or 'certificate differs from complete replay' not in result.stderr:
                raise RuntimeError(f'negative control did not reject properly: {kind}: {result.stdout} {result.stderr}')
            if initial != sha(path):
                raise RuntimeError('read-only checker mutated a negative certificate')
            results.append({'case': kind, 'corrupt_sha256': initial, 'returncode': result.returncode,
                            'stdout': result.stdout.strip(), 'stderr': result.stderr.strip(),
                            'input_unchanged': True, 'status': 'triggered and holds'})
    if before != sha(CERTIFICATE):
        raise RuntimeError('read-only checker mutated canonical certificate')
    record = {'checker_sha256': sha(CHECKER), 'certificate_sha256': before,
              'canonical_certificate_unchanged': True, 'python': sys.version,
              'results': results, 'scope': 'Nine finite topology skeletons only; no unknown minimal source was tested.'}
    target = HERE / 'verification.v2.json'
    with target.open('x') as output:
        json.dump(record, output, indent=2, sort_keys=True)
        output.write('\n')
    print(f'PASS: 2 normal replays and {len(cases)} corrupted copies rejected; {target}')


if __name__ == '__main__':
    main()
