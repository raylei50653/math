#!/usr/bin/env python3
"""Exclusive logs and certificate probes; writes only this audit directory."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def write(path, data):
    with path.open('xb') as f:
        f.write(data)


def encode(data):
    return (json.dumps(data, sort_keys=True, ensure_ascii=False, indent=2) + '\n').encode()


def run(name, argv, env=None):
    task_env = os.environ.copy()
    if env:
        task_env.update(env)
    process = subprocess.run(argv, cwd=ROOT, env=task_env, capture_output=True)
    prefix = HERE / 'logs' / name
    write(prefix.with_suffix('.stdout.log'), process.stdout)
    write(prefix.with_suffix('.stderr.log'), process.stderr)
    result = {'command': argv, 'cwd': str(ROOT), 'environment_override': env or {},
              'exit': process.returncode, 'stdout': str(prefix.with_suffix('.stdout.log').relative_to(HERE)),
              'stderr': str(prefix.with_suffix('.stderr.log').relative_to(HERE))}
    write(prefix.with_suffix('.command.json'), encode(result))
    print(json.dumps({'run': name, 'exit': process.returncode}), flush=True)
    return result, process.stdout


def snapshot():
    manifest = json.loads((HERE / 'inputs.json').read_bytes())
    result = {}
    for item in manifest['inputs']:
        for path in (ROOT / item['path'], HERE / item['frozen_path']):
            result[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
    for name in ('inputs.json', 'checker.py', 'certificate.json'):
        p = HERE / name
        if p.exists():
            result[str(p)] = hashlib.sha256(p.read_bytes()).hexdigest()
    return result


def tree_snapshot():
    return {str(p.relative_to(HERE)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in HERE.rglob('*') if p.is_file()}


def main():
    checker = str(HERE / 'checker.py')
    command = [sys.executable, '-B', checker]
    before = snapshot()
    write(HERE / 'custody-before.json', encode(before))
    runs = []
    result, _ = run('generation-attempt1', command)
    runs.append(result)
    if result['exit']:
        write(HERE / 'checks-attempt1.json', encode({'status': 'failed generation; logs retained', 'runs': runs}))
        return 1
    certificate = HERE / 'certificate.json'
    canonical = certificate.read_bytes()
    replay_results = []
    for name, env in [('normal', None), ('seed17', {'PYTHONHASHSEED': '17'})]:
        # Snapshot the entire new directory before --check; compare before writing its logs.
        tree_before = tree_snapshot()
        process = subprocess.run(command + ['--check'], cwd=ROOT, env=os.environ | (env or {}), capture_output=True)
        read_only = tree_before == tree_snapshot()
        prefix = HERE / 'logs' / name
        write(prefix.with_suffix('.stdout.log'), process.stdout)
        write(prefix.with_suffix('.stderr.log'), process.stderr)
        result = {'command': command + ['--check'], 'cwd': str(ROOT), 'environment_override': env or {},
                  'exit': process.returncode, 'read_only_full_audit_tree': read_only,
                  'stdout': str(prefix.with_suffix('.stdout.log').relative_to(HERE)),
                  'stderr': str(prefix.with_suffix('.stderr.log').relative_to(HERE))}
        write(prefix.with_suffix('.command.json'), encode(result))
        runs.append(result)
        replay_results.append(process.stdout)
        print(json.dumps({'run': name, 'exit': process.returncode, 'read_only': read_only}), flush=True)
    obj = json.loads(canonical)
    bad_r = json.loads(canonical)
    graph = bad_r['graphs'][0]
    r = graph['root_order'][0]
    row = graph['cases'][0]['rows'][0]
    rpos = graph['C_vertices'].index(r)
    row['C_assignments'][0][rpos] = (row['C_assignments'][0][rpos] + 1) % 4
    bad_empty = json.loads(canonical)
    fibres = bad_empty['graphs'][0]['cases'][0]['rows'][0]['all_ambient_C_r_tuple_fibres']
    empty_index = next(i for i, cell in enumerate(fibres) if not cell['C_assignment_indices'])
    removed_cell = fibres.pop(empty_index)
    probes = []
    for name, bad in [('bad-C-r-colour', bad_r), ('missing-empty-ambient', bad_empty)]:
        path = HERE / (name + '.json')
        write(path, encode(bad))
        result, _ = run(name, command + ['--check', '--certificate', str(path)])
        runs.append(result)
        probes.append({'name': name, 'status': 'triggered and holds' if result['exit'] != 0 else 'counterexample',
                       'certificate': path.name, 'certificate_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                       'rejected': result['exit'] != 0})
    result, _ = run('exclusive-create-existing', command)
    runs.append(result)
    after = snapshot()
    write(HERE / 'custody-after.json', encode(after))
    drift = {p: {'before': digest, 'after': after.get(p)} for p, digest in before.items() if after.get(p) != digest}
    summary = {'task_id': obj['task_id'], 'base': obj['base'], 'runs': runs,
               'finite_interface': obj['finite_interface'], 'target_source': obj['target_source'],
               'private_cover': obj['private_cover'], 'normal_seed17_stdout_byte_equal': replay_results[0] == replay_results[1],
               'negative_controls': probes, 'removed_empty_ambient_cell': removed_cell,
               'exclusive_create_rejected': result['exit'] != 0,
               'canonical_certificate_unchanged': certificate.read_bytes() == canonical,
               'frozen_and_old_inputs_drift': drift,
               'replay_checks_read_only': all(z.get('read_only_full_audit_tree', True) for z in runs),
               'independent_acceptance': 'pending'}
    good = (all(z['exit'] == 0 for z in runs[0:3]) and not drift and
            all(z['rejected'] for z in probes) and summary['normal_seed17_stdout_byte_equal'] and
            summary['exclusive_create_rejected'] and summary['canonical_certificate_unchanged'] and
            summary['replay_checks_read_only'])
    summary['fixed_calibration_checks_pass'] = good
    write(HERE / 'checks.json', encode(summary))
    print(json.dumps({'fixed_calibration_checks_pass': good, 'counts': obj['finite_interface']['counts']}), flush=True)
    return 0 if good else 1


if __name__ == '__main__':
    raise SystemExit(main())
