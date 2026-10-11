#!/usr/bin/env python3
"""Memory-only seal corruption controls; never mutate sealed payloads."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

AUDIT = Path(__file__).resolve().parent
ROOT = AUDIT.parents[1]

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()

def main():
    original = (AUDIT / 'SEAL.json').read_bytes()
    seal = json.loads(original)
    cases = []
    for name in ('decision-escalation', 'parent-closure', 'source-escalation', 'extra-metadata', 'missing-payload-rehashed', 'payload-hash-rehashed'):
        altered = copy.deepcopy(seal)
        if name == 'decision-escalation':
            altered['formal_adoption_executed'] = True
        elif name == 'parent-closure':
            altered['parent_status'] = 'CLOSED'
        elif name == 'source-escalation':
            altered['source_status'] = 'triggered and holds'
        elif name == 'extra-metadata':
            altered['unreviewed_general_theorem'] = True
        elif name == 'missing-payload-rehashed':
            altered['payloads'].pop()
            altered['payload_manifest_sha256'] = hashlib.sha256(canonical(altered['payloads'])).hexdigest()
        else:
            altered['payloads'][0]['sha256'] = '0' * 64
            altered['payload_manifest_sha256'] = hashlib.sha256(canonical(altered['payloads'])).hexdigest()
        fd = os.memfd_create('br-sd-1g-adopt-negative', 0)
        try:
            os.write(fd, json.dumps(altered).encode())
            argv = [sys.executable, '-B', str(AUDIT / 'verify.py'), '--check', '--seal-path', f'/proc/self/fd/{fd}']
            result = subprocess.run(argv, cwd=ROOT, capture_output=True, pass_fds=(fd,))
            cases.append({'name': name, 'argv': argv, 'exit_code': result.returncode, 'expected_exit_code': 1,
                          'stdout': result.stdout.decode(), 'stderr': result.stderr.decode()})
            if result.returncode != 1 or 'seal corruption' not in result.stderr.decode():
                raise ValueError('negative rejected for unexpected reason: ' + name)
        finally:
            os.close(fd)
    argv = [sys.executable, '-B', str(AUDIT / 'verify.py'), '--seal']
    result = subprocess.run(argv, cwd=ROOT, capture_output=True)
    cases.append({'name': 'exclusive-reseal', 'argv': argv, 'exit_code': result.returncode, 'expected_exit_code': 1,
                  'stdout': result.stdout.decode(), 'stderr': result.stderr.decode()})
    if result.returncode != 1 or not any(message in result.stderr.decode() for message in ('File exists', 'delivery exists before seal')):
        raise ValueError('reseal rejection missing')
    if (AUDIT / 'SEAL.json').read_bytes() != original:
        raise ValueError('seal bytes changed during negative controls')
    print(json.dumps({'status': 'triggered and holds', 'scope': 'seven memory-only custody controls',
                      'seal_unchanged': True, 'cases': cases}, sort_keys=True))

if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError) as exc:
        print('FAIL: ' + str(exc), file=sys.stderr)
        raise SystemExit(1)
