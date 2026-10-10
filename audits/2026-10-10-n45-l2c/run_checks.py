#!/usr/bin/env python3
"""Exclusive actual subprocess recordings for independent artifact controls."""
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
NAMES = ('normal', 'seed17', 'bad-digest', 'missing-nested-delivery',
         'duplicate-path', 'unsafe-path', 'missing-payload', 'bad-receipt', 'missing-nested-receipt')
STAGES = {'bad-digest': 'manifest digest differs',
          'missing-nested-delivery': 'manifest payload inventory differs',
          'duplicate-path': 'manifest duplicate path',
          'unsafe-path': 'manifest unsafe path',
          'missing-payload': 'manifest payload inventory differs',
          'bad-receipt': 'delivery receipt binding differs',
          'missing-nested-receipt': 'manifest payload inventory differs'}


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as target:
        target.write(data)


def main():
    primary = (HERE / 'frozen/worker/MANIFEST.sha256').read_text()
    nested = 'frozen/current/audits/2026-10-10-n45-s-low1/seal-final-v4/commands.json'
    rows = primary.splitlines(keepends=True)
    filtered = [line for line in rows if not line.endswith('  ' + nested + '\n')]
    assert len(filtered) == len(rows) - 1
    fixture = HERE / 'negative/missing-nested-receipt.sha256'
    write(fixture, ''.join(filtered).encode())
    records = []
    for name in NAMES:
        command = [sys.executable, '-B', str(HERE / 'checker.py')]
        expected = 0 if name in NAMES[:2] else 2
        if name == 'bad-receipt':
            command += ['--receipt', str(HERE / 'frozen/worker/negative/bad-receipt.json')]
        elif name == 'missing-nested-receipt':
            command += ['--manifest', str(fixture)]
        elif expected == 2:
            command += ['--manifest', str(HERE / 'frozen/worker/negative' / (name + '.sha256'))]
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
        env.pop('PYTHONHASHSEED', None)
        if name == 'seed17':
            env['PYTHONHASHSEED'] = '17'
        result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True)
        for stream in ('stdout', 'stderr'):
            write(HERE / f'checks/{name}.{stream}.log', getattr(result, stream))
        record = {'name': name, 'command': command, 'cwd': str(ROOT), 'PYTHONHASHSEED': env.get('PYTHONHASHSEED'),
                  'actual_exit_code': result.returncode, 'expected_exit_code': expected,
                  'stdout': f'checks/{name}.stdout.log', 'stderr': f'checks/{name}.stderr.log',
                  'evidence_layer': 'synthetic artifact control; not a LOW2 source control',
                  'control_classification': 'triggered and holds' if result.returncode == expected else 'counterexample'}
        if expected == 2:
            record['expected_rejection_stage'] = STAGES[name]
            record['stage_matches'] = STAGES[name].encode() in result.stderr
        records.append(record)
        print(json.dumps({'name': name, 'actual_exit_code': result.returncode, 'expected_exit_code': expected}, sort_keys=True), flush=True)
    assert (HERE / 'checks/normal.stdout.log').read_bytes() == (HERE / 'checks/seed17.stdout.log').read_bytes()
    data = {'task': 'N45-L2C', 'commands': records, 'normal_seed17_stdout_byte_equal': True,
            'bad_receipt_boundary': 'Independent checker uses actual frozen final delivery and persisted invalid receipt, without a read_json override.',
            'source_controls': 'not established; not executed; no trigger count',
            'mathematical_verdict': 'not evaluated by this tool'}
    write(HERE / 'checks.json', (json.dumps(data, sort_keys=True, indent=2) + '\n').encode())
    assert all(r['actual_exit_code'] == r['expected_exit_code'] and r.get('stage_matches', True) for r in records)


if __name__ == '__main__':
    main()
