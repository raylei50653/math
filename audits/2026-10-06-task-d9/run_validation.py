#!/usr/bin/env python3
"""D9 read-only replays and exact log records; outputs stay in this audit."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

HERE = Path(__file__).resolve().parent
ROOT = Path(os.environ.get('D9_REPO', str(HERE.parents[1])))
CHECKERS = (
    ('e4_reductions', 'python3'),
    ('e4_control', 'networkx'),
    ('e5_controls', 'python3'),
    ('e5_local', 'python3'),
    ('e5_branches', 'python3'),
    ('e6_reductions', 'python3'),
    ('e6_controls', 'networkx'),
    ('e6_local_controls', 'networkx'),
)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def run(command, name, overrides=None):
    env = os.environ.copy()
    env.pop('PYTHONHASHSEED', None)
    env.update(overrides or {})
    start = time.monotonic()
    result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True)
    record = dict(command=command, cwd=str(ROOT), environment=overrides or {},
                  exit_code=result.returncode, seconds=round(time.monotonic() - start, 3))
    for tag, data in [('stdout', result.stdout), ('stderr', result.stderr)]:
        log = HERE / 'logs' / f'{name}.{tag}.log'
        log.write_bytes(data)
        record[f'{tag}_log'] = str(log.relative_to(HERE))
        record[f'{tag}_sha256'] = sha(data)
    print(json.dumps(dict(name=name, exit_code=result.returncode,
                         seconds=record['seconds']), ensure_ascii=False), flush=True)
    return record


def restore_required():
    """Restore only a missing required input from its recorded archive blob."""
    archive = json.loads((ROOT / 'audits/ARCHIVE.json').read_text())
    manifest = json.loads((ROOT / 'artifacts/MANIFEST.json').read_text())
    outputs = []
    for relative in ['artifacts/c5_excess_rejection_law/observations.json']:
        entry = manifest['files'][relative]
        target = ROOT / relative
        blob = archive['blobs'][entry['sha256']]
        compressed = (ROOT / blob['path']).read_bytes()
        assert sha(compressed) == blob['sha256'] and len(compressed) == blob['bytes']
        data = gzip.decompress(compressed)
        assert sha(data) == entry['sha256'] and len(data) == entry['bytes']
        if target.exists():
            assert target.read_bytes() == data, relative
            action = 'already identical'
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open('xb') as stream:
                stream.write(data)
            action = 'restored exclusively'
        outputs.append(dict(path=relative, bytes=len(data), sha256=sha(data), action=action))
    dump(HERE / ('required_restore_verification.json' if (HERE / 'required_restore.json').exists() else 'required_restore.json'), outputs)
    print(json.dumps(outputs))


def replays():
    records, pairs = [], []
    for name, interpreter in CHECKERS:
        prefix = (['uv', 'run', '--with', 'networkx==3.5', 'python']
                  if interpreter == 'networkx' else ['python3'])
        command = prefix + [f'scripts/c5_excess_two_{name}.py', '--check']
        first = run(command, f'{name}_default')
        second = run(command, f'{name}_seed17', {'PYTHONHASHSEED': '17'})
        records.extend([first, second])
        pairs.append(dict(checker=name, default_exit=first['exit_code'],
                          seed17_exit=second['exit_code'],
                          stdout_matches=first['stdout_sha256'] == second['stdout_sha256'],
                          stderr_matches=first['stderr_sha256'] == second['stderr_sha256']))
        dump(HERE / 'original_replays.json', dict(commands=records, pairs=pairs))


def finalize():
    originals = json.loads((HERE / 'original_replays.json').read_text())
    records = [json.loads((HERE / 'setup_validation.json').read_text())]
    records.extend(originals['commands'])
    agent_manifests = {}
    for relative in ['e4_independent_validation.json', 'e5_independent_validation.json', 'validation_e6_independent.json']:
        manifest = json.loads((HERE / relative).read_text())
        agent_manifests[relative] = manifest
        for command_record in manifest['commands']:
            for tag in ['stdout', 'stderr']:
                log = command_record.get(f'{tag}_log')
                expected = command_record.get(f'{tag}_sha256')
                if 'logs' in command_record:
                    log = command_record['logs'][tag]['path']
                    expected = command_record['logs'][tag]['sha256']
                if log:
                    assert sha((HERE / log).read_bytes()) == expected, log
            if command_record.get('log'):
                assert sha((HERE / command_record['log']).read_bytes()) == command_record['log_sha256']
            records.append(command_record)
    records.append(run(['python3', str(HERE / 'run_validation.py'), 'restore-required'], 'required_restore_validation', {'D9_REPO': str(ROOT)}))
    records.append(run(['python3', str(HERE / 'inspect_original_replay.py')], 'historical_replay_diagnosis', {'D9_REPO': str(ROOT)}))
    # Run the audit tools ourselves so the integrated manifest has complete,
    # consistently structured command/log/hash records.
    for name in ['e4', 'e5', 'e6']:
        path = HERE / f'audit_{name}_controls.py'
        command = ['python3', str(path), '--root', str(ROOT), '--output', str(HERE / f'{name}_controls.json'), '--check']
        records.append(run(command, f'independent_{name}_default'))
        records.append(run(command, f'independent_{name}_seed17', {'PYTHONHASHSEED': '17'}))
    records.append(json.loads((HERE / 'permission_validation.json').read_text()))
    for command, name in [(['python3', 'scripts/check_docs.py'], 'check_docs'),
                          (['git', 'diff', '--check'], 'diff_check'),
                          (['git', 'diff', '--cached', '--check'], 'cached_diff_check')]:
        records.append(run(command, name))
    base = json.loads((HERE / 'baseline_sha256.json').read_text())
    drift = [p for p, old in base['files'].items()
             if not (ROOT / p).is_file() or sha((ROOT / p).read_bytes()) != old]
    invariance = dict(base_commit=base['base_commit'], baseline_files=len(base['files']),
                      changed_existing_tracked_files=drift,
                      head=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip())
    dump(HERE / 'invariance.json', invariance)
    dump(HERE / 'validation.json', dict(schema=1, base_commit=base['base_commit'],
         max_worker_jobs=4, commands=records, original_pairs=originals['pairs'], agent_command_manifests=agent_manifests,
         baseline_invariance=invariance, lean_build_run=False, pushed=False,
         staging_directory=str(HERE), delivery_write_permission=False,
         commit_sha=None, pending=['copy finalized audit into task worktree', 'stage and commit task branch']))
    output_check = run(['python3', str(HERE / 'check_audit_outputs.py'), '--root', str(ROOT)], 'audit_output_checks_final')
    data = json.loads((HERE / 'validation.json').read_text())
    data['commands'].append(output_check)
    dump(HERE / 'validation.json', data)
    assert output_check['exit_code'] == 0
    assert not drift, drift


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['restore-required', 'replays', 'finalize'])
    args = parser.parse_args()
    HERE.joinpath('logs').mkdir(exist_ok=True)
    {'restore-required': restore_required, 'replays': replays, 'finalize': finalize}[args.action]()
