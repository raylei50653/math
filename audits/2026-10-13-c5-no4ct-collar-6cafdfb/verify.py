#!/usr/bin/env python3
"""Read-only replay of the isolated no-4CT three-target collar audit."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
FROZEN = HERE / 'frozen'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', required=True, action='store_true')
    args = parser.parse_args()
    manifest = json.loads((HERE / 'INPUTS.json').read_text())
    for row in manifest['inputs']:
        content = (FROZEN / row['path']).read_bytes()
        if len(content) != row['bytes'] or hashlib.sha256(content).hexdigest() != row['sha256']:
            raise ValueError('frozen input drift: ' + row['path'])
    commands = [
        ('relative-C4', ['uv', 'run', '--with', 'networkx==3.5', 'python', '-B',
                        str(FROZEN / 'audits/2026-10-13-c5-no4ct-degrees-6cafdfb/check_c4.py'), '--check']),
        ('crosscut-finite', [sys.executable, '-B',
                            str(FROZEN / 'audits/2026-10-12-neartri-complete-relation-reductions-5d70a399/checker.py'), '--check']),
        ('three-target-collar', [sys.executable, '-B', str(HERE / 'collar/check.py'), '--check']),
        ('independent-review', [sys.executable, '-B', str(HERE / 'review/independent_review.py')]),
        ('independent-C7-count', [sys.executable, '-B',
                                 str(FROZEN / 'audits/2026-10-13-c7-joint-kempe-19209f4c/topology/count_review.py')]),
    ]
    results = []
    for name, command in commands:
        completed = subprocess.run(command, capture_output=True, text=True)
        if completed.returncode:
            sys.stderr.write(completed.stdout + completed.stderr)
            raise RuntimeError(f'{name} failed with exit code {completed.returncode}')
        output = completed.stdout.strip()
        try:
            output = json.loads(output)
            if isinstance(output, dict):
                output.pop('cases', None)  # Full table lives in review/verification.json.
        except json.JSONDecodeError:
            pass
        results.append({'name': name, 'output': output})
    print(json.dumps({'status': 'PASS', 'frozen_inputs': len(manifest['inputs']),
                      'checks': results,
                      'scope': 'Finite replay for the paper three-branch minimal-source collar reduction',
                      'actual_target_source_status': 'not triggered',
                      'general_theorem': 'OPEN'}, sort_keys=True))


if __name__ == '__main__':
    main()
