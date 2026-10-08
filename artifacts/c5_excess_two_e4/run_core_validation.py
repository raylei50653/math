#!/usr/bin/env python3
"""One-shot E4 validation; exclusive creates its own validation and replay."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[2]
PYTHON = '/home/ray/developer/ai/math/.venv/bin/python'
HERE = ROOT / 'artifacts/c5_excess_two_e4'
OUT = HERE / 'core_validation.json'
EXTERNAL = ('scripts/c5_excess_two_e4_control.py',
    'scripts/c5_excess_two_e4_reductions.py',
    'artifacts/c5_excess_two_e4/control.json',
    'artifacts/c5_excess_two_e4/reductions.json',
    'artifacts/c5_excess_two_e4/REPORT.md',
    'artifacts/c5_excess_two_e4/validation.json')


def record_files(names):
    return {name: {'bytes': (ROOT/name).stat().st_size,
        'sha256': hashlib.sha256((ROOT/name).read_bytes()).hexdigest()}
        for name in names if (ROOT/name).is_file()}


def execute(args, additions=None):
    env = dict(os.environ)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    if additions:
        env.update(additions)
    started = time.monotonic()
    result = subprocess.run(args, cwd=ROOT, env=env,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    record = dict(argv=args, cwd=str(ROOT),
        environment={'PYTHONDONTWRITEBYTECODE': '1'} | (additions or {}),
        exit_code=result.returncode, output=result.stdout,
        seconds=round(time.monotonic()-started, 3))
    print('exit', result.returncode, ' '.join(args), flush=True)
    if result.stdout:
        print(result.stdout[:1200], flush=True)
    return record


def main():
    initial_external = record_files(EXTERNAL)
    # The file exists during check_docs, but JSON bytes are written only once.
    with OUT.open('x') as final_stream:
        commands = []
        commands.append(execute([PYTHON,
            'scripts/c5_excess_two_e4_core_constraints.py', '--output',
            'artifacts/c5_excess_two_e4/replay_core/core_constraints.json']))
        for source in ('scripts/c5_excess_two_e4_core_constraints.py',
                'scripts/c5_excess_two_e4_control.py',
                'scripts/c5_excess_two_e4_reductions.py',
                'artifacts/c5_excess_two_e4/control_probe/split_hub_probe.py',
                'artifacts/c5_excess_two_e4/control_probe/m2_probe.py',
                'artifacts/c5_excess_two_e4/control_probe/m2_binary_probe.py'):
            commands.append(execute([PYTHON, source, '--check']))
            commands.append(execute([PYTHON, source, '--check'], {'PYTHONHASHSEED': '17'}))
        commands.append(execute([PYTHON, 'scripts/check_docs.py']))
        commands.append(execute([PYTHON, 'tools/docgraph', 'check']))
        commands.append(execute(['git', 'diff', '--check']))
        commands.append(execute(['git', 'diff', '--name-only', '2ac279b', '--']))
        new = subprocess.run(['git', 'ls-files', '--others', '--exclude-standard'],
            cwd=ROOT, text=True, check=True, stdout=subprocess.PIPE).stdout.splitlines()
        whitespace = []
        for name in new:
            file = ROOT / name
            if not file.is_file() or name == str(OUT.relative_to(ROOT)):
                continue
            if not (name.startswith('artifacts/c5_excess_two_e4/') or
                    name.startswith('scripts/c5_excess_two_e4_')):
                continue
            result = subprocess.run(['git', 'diff', '--no-index', '--check',
                '/dev/null', name], cwd=ROOT, text=True,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            whitespace.append(dict(path=name, exit_code=result.returncode,
                output=result.stdout,
                whitespace_diagnostics=bool(result.stdout.strip()),
                interpretation='exit1 without diagnostics is the expected new-file difference' if result.returncode == 1 and not result.stdout.strip() else 'inspect actual diagnostics'))
        assert all(not rec['whitespace_diagnostics'] for rec in whitespace)
        current_external = record_files(EXTERNAL)
        same_external = current_external == initial_external
        assert same_external, 'Parallel artifact changed during read-only validation; retain observations.'
        probe_validation = json.loads((HERE/'control_probe/validation.json').read_text())
        result = dict(schema_version=1, task='E4 independent core validation',
            baseline_commit='2ac279b', worktree=str(ROOT), python=PYTHON,
            command_records=commands,
            own_original_generation_observation=dict(
                argv=[PYTHON, 'scripts/c5_excess_two_e4_core_constraints.py'],
                exit_code=0,
                output='GENERATED core_constraints.json: bytes=158854 sha256=34885728aa6cacde211b2b68e65c9c0ccbc2e4d3b6b6f7daf307fd7855c6bfbd',
                observation='Actual tool execution earlier in this task; generation above separately uses exclusive fresh replay output.'),
            inherited_probe_generation_records=[rec for rec in probe_validation['commands']
                if '--check' not in rec['command'] and '.py' in rec['command']],
            inherited_probe_validation_sha256=hashlib.sha256((HERE/'control_probe/validation.json').read_bytes()).hexdigest(),
            report_collision=dict(attempted='artifacts/c5_excess_two_e4/REPORT.md',
                mode='x', actual_exit_code=1,
                error='FileExistsError: [Errno 17] File exists',
                result='No overwrite; CORE_CONSTRAINTS.md and core_validation.json exclusively created.'),
            parallel_artifacts_before=initial_external,
            parallel_artifacts_after=current_external,
            parallel_artifacts_unchanged_during_validation=same_external,
            parallel_authorship='The four control/reductions files and canonical REPORT/validation are another concurrent producer; read-only replays do not merge source provenance.',
            own_sources_and_reviews=record_files((
                'scripts/c5_excess_two_e4_core_constraints.py',
                'artifacts/c5_excess_two_e4/core_constraints.json',
                'artifacts/c5_excess_two_e4/CORE_CONSTRAINTS.md',
                'artifacts/c5_excess_two_e4/ROOT_REVIEW.md',
                'artifacts/c5_excess_two_e4/independent_review.md',
                'artifacts/c5_excess_two_e4/run_core_validation.py')),
            new_file_whitespace=whitespace,
            known_archive_missing_paths_not_restored=[
                'audits/2026-10-04-task-d5/scope_ledger.json',
                'audits/2026-10-04-task-d2/integration_live.diff.txt'],
            no_lean_build='No new Lean source; arbitrary-size paper topology remains unformalized.',
            positive_control='No requested realizable nonadjacent Sigma-critical control found; finite failures not a theorem.',
            publication='No commit or push; baseline tracked files unchanged.')
        final_stream.write(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2)+'\n')
    print('EXCLUSIVE CREATED', OUT, flush=True)


if __name__ == '__main__':
    main()
