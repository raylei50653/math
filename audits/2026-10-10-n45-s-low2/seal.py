#!/usr/bin/env python3
"""One-shot exclusive seal; keep every failed output and use a new version."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import verify

HERE = Path(__file__).resolve().parent


def write(path, data):
    with path.open('xb') as f:
        f.write(data)


def json_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + '\n').encode()


def main():
    for name in ('MANIFEST.sha256', 'receipt.json', 'delivery.json', 'negative', 'receipt'):
        if (HERE / name).exists():
            raise ValueError('seal already exists; preserve it and create a new version: ' + name)
    (HERE / 'negative').mkdir()
    (HERE / 'receipt').mkdir()
    regular, links = verify.payload_inventory()
    verify.require(not links, 'unexpected payload symlink')
    # Add all probe paths before hashing: these are payload, never excluded by basename.
    probe_files = {name: HERE / 'negative' / (name + '.sha256') for name in verify.PROBES[:-1]}
    bad_receipt = HERE / 'negative/bad-receipt.json'
    all_files = sorted(regular + [p.relative_to(HERE).as_posix() for p in probe_files.values()] +
                       [bad_receipt.relative_to(HERE).as_posix()])
    fake = [f'{"0" * 64}  {p}\n' for p in all_files]
    nested = 'frozen/current/audits/2026-10-10-n45-s-low1/delivery.json'
    verify.require(nested in all_files, 'nested delivery probe missing input')
    for name, path in probe_files.items():
        content = fake[:]
        if name == 'missing-nested-delivery':
            content = [s for s in content if not s.endswith('  ' + nested + '\n')]
        elif name == 'duplicate-path':
            content.append(content[0])
        elif name == 'unsafe-path':
            content.append('0' * 64 + '  ../outside-audit\n')
        elif name == 'missing-payload':
            content = [s for s in content if not s.endswith('  claims.json\n')]
        write(path, ''.join(content).encode())
    write(bad_receipt, b'{"tampered_receipt": true}\n')
    manifest = ''.join(f'{verify.sha(HERE / p)}  {p}\n' for p in all_files).encode()
    write(HERE / 'MANIFEST.sha256', manifest)
    before = {p: verify.sha(HERE / p) for p in all_files}
    stages = {'bad-digest': 'manifest digest differs',
              'missing-nested-delivery': 'manifest payload inventory differs',
              'duplicate-path': 'manifest duplicate path',
              'unsafe-path': 'manifest unsafe path',
              'missing-payload': 'manifest payload inventory differs',
              'bad-receipt': 'delivery receipt binding differs'}
    records = []
    for name in verify.RUNS:
        command = [sys.executable, '-B', str(HERE / 'verify.py')]
        expected = 0 if name in ('normal', 'seed17') else 2
        if name == 'bad-receipt':
            # Bind an intentionally invalid receipt first. All previous negative probes
            # stop at manifest validation, so no valid receipt is needed yet.
            provisional = {'manifest_sha256': verify.sha(HERE / 'MANIFEST.sha256'),
                           'receipt_sha256': '0' * 64,
                           'paper_status': 'candidate_pending_independent_adoption'}
            # This probe uses a separately named delivery fixture through a subprocess
            # shim, without creating/overwriting the actual final delivery.
            shim = ('import sys; from pathlib import Path; '
                    'sys.path.insert(0, sys.argv[1]); import verify; '
                    'actual=verify.read_json; '
                    'verify.read_json=lambda p: ' + repr(provisional) +
                    ' if p == verify.HERE / "delivery.json" else actual(p); '
                    'sys.argv=["verify.py", "--receipt", sys.argv[2]]; '
                    'sys.exit(verify.main())')
            command = [sys.executable, '-B', '-c', shim, str(HERE), str(bad_receipt)]
        else:
            command.append('--payload-only')
            if name in probe_files:
                command += ['--manifest', str(probe_files[name])]
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
        if name == 'seed17':
            env['PYTHONHASHSEED'] = '17'
        result = subprocess.run(command, cwd=verify.ROOT, env=env, capture_output=True)
        for stream in ('stdout', 'stderr'):
            write(HERE / f'receipt/{name}.{stream}.log', getattr(result, stream))
        record = {'name': name, 'command': command, 'cwd': str(verify.ROOT),
                  'PYTHONHASHSEED': '17' if name == 'seed17' else env.get('PYTHONHASHSEED'),
                  'exit_code': result.returncode, 'expected_exit': expected,
                  'control_classification': 'triggered and holds' if result.returncode == expected else 'counterexample',
                  'evidence_layer': 'synthetic artifact control only; not a LOW2 source evaluation',
                  'stdout': f'receipt/{name}.stdout.log', 'stderr': f'receipt/{name}.stderr.log'}
        if name in stages:
            record['rejection_stage'] = stages[name]
        records.append(record)
        print(json.dumps({'name': name, 'exit_code': result.returncode, 'expected_exit': expected}), flush=True)
    after = {p: verify.sha(HERE / p) for p in all_files}
    receipt = {'commands': records,
               'metadata': {p: verify.sha(HERE / p) for p in sorted(verify.RECEIPT_LOGS)},
               'payload_before': hashlib.sha256(manifest).hexdigest(),
               'payload_after': hashlib.sha256(''.join(f'{after[p]}  {p}\n' for p in all_files).encode()).hexdigest(),
               'new_files_outside_audit': [], 'changed_preexisting_files': [],
               'workspace_scope_basis': 'Normal/seed17 verify complete preexisting Git-listed inventory and diffs; four nested directory entries only, without recursive hash.',
               'bad_receipt_probe_boundary': 'Actual verify.check_receipt with read_json override solely for absent final delivery; persisted bad receipt bytes and exact command included. This is a synthetic tool probe.'}
    write(HERE / 'receipt.json', json_bytes(receipt))
    delivery = {'task': 'N45-S-LOW2', 'BASE': verify.BASE,
                'manifest_sha256': verify.sha(HERE / 'MANIFEST.sha256'),
                'receipt_sha256': verify.sha(HERE / 'receipt.json'),
                'paper_status': 'candidate_pending_independent_adoption',
                'source_controls': 'not established; not executed; no trigger count',
                'source_realization': False, 'new_Lean': False,
                'excluded_exact_paths': sorted(verify.EXCLUDED),
                'external_messages_commit_push_PR_delegation': False}
    write(HERE / 'delivery.json', json_bytes(delivery))
    verify.require(before == after, 'read-only sealing changed payload')
    verify.check_receipt(HERE / 'receipt.json')
    verify.require(all(r['exit_code'] == r['expected_exit'] for r in records), 'unexpected exit; preserve failed seal')
    print(json.dumps({'sealed': True, 'payload_files': len(all_files),
                      'metadata_logs': len(verify.RECEIPT_LOGS), 'negative_probes': len(stages)}, sort_keys=True))


if __name__ == '__main__':
    main()
