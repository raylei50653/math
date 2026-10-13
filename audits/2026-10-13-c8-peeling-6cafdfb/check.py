#!/usr/bin/env python3
"""Read-only frozen-input and complete-fibre replay for C8 peeling."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def verify_inputs():
    data = json.loads((ROOT / 'INPUTS.json').read_text())
    for name, entry in data['inputs'].items():
        payload = (ROOT / entry['frozen']).read_bytes()
        assert len(payload) == entry['bytes'], name
        assert hashlib.sha256(payload).hexdigest() == entry['sha256'], name
    return len(data['inputs'])


def verify_manifest():
    data = json.loads((ROOT / 'MANIFEST.json').read_text())
    for name, digest in data['sha256'].items():
        payload = (ROOT / name).read_bytes()
        assert hashlib.sha256(payload).hexdigest() == digest, name
    return len(data['sha256'])


def replay(relative, negative):
    command = [sys.executable, '-B', str(ROOT / relative), '--check']
    if negative:
        command.append('--negative')
    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode:
        sys.stderr.write(result.stdout)
        sys.stderr.write(result.stderr)
        raise SystemExit(result.returncode)
    lines = result.stdout.strip().splitlines()
    assert lines, f'no replay result from {relative}'
    return json.loads(lines[-1])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--negative', action='store_true')
    args = parser.parse_args()
    inputs = verify_inputs()
    sealed = verify_manifest()
    primary = replay('calibration/check.py', args.negative)
    independent = replay('independent/check.py', args.negative)
    independent_calibration = replay('independent/check_calibration.py', args.negative)
    print(json.dumps({
        'frozen_inputs': inputs,
        'sealed_files': sealed,
        'primary': primary,
        'independent': independent,
        'independent_calibration': independent_calibration,
        'evidence': 'paper arbitrary-size structure; bounded complete-fibre replay',
        'target_source_status': 'not triggered',
        'remaining_unbounded_contracts': 'OPEN',
    }, sort_keys=True))


if __name__ == '__main__':
    main()
