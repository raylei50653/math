#!/usr/bin/env python3
"""Record fresh M2 commands, input bytes, output logs and final immutability."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
CANDIDATE = 'ba0b447f09617591d9f2ba81c988f537af771791'
INPUTS = [
    'docs/c5_excess_two_no_mixed_core44.md',
    'scripts/c5_excess_two_no_mixed_core44.py',
    'artifacts/c5_excess_two_no_mixed_core44/observations.json',
    'artifacts/c5_excess_two_mixed_omission/observations.json',
    'artifacts/MANIFEST.json', 'audits/ARCHIVE.json',
    'artifacts/c5_excess_two_c44pp/REPORT.md',
    'artifacts/c5_excess_two_c44/REPORT.md',
    'artifacts/c5_excess_two_e6/REPORT.md',
    'docs/c5_excess_two_mixed_omission.md',
    'docs/c5_excess_two_path_edge.md',
    'docs/c5_triangle_branches.md',
    'docs/c5_triangle_path_reduction.md',
    'artifacts/c5_triangle_branches/observations.json',
    'artifacts/c5_triangle_path_reduction/observations.json',
    'docs/c5_triangle_forks.md',
    'docs/c5_tree_cores.md',
    'docs/c5_k4_blocks.md',
    'docs/c5_weak_list_cores.md',
    'docs/c5_multi_odd_cycles.md',
    'docs/history/2026-10-07-merge-readiness-tasks.md',
    'docs/c5_degree4_guide.md',
    'docs/c5_independent_support_capacity.md',
    'docs/c5_two_triangle_blocks.md',
    'docs/c5_unary_shield_budget.md',
    'docs/c5_excess_two_root_deletions.md',
    'audits/2026-10-07-c44pp-mixed-audit/REPORT.md',
    'audits/2026-10-07-c44pp-mixed-audit/verify.py',
    'audits/2026-10-07-c44pp-mixed-audit/validation.json',
    'audits/2026-10-06-task-d9/REPORT.md',
    'audits/2026-10-06-task-d9/audit_e5.md',
    'audits/2026-10-06-task-d9/audit_e6.md',
]


def digest(path):
    raw = path.read_bytes()
    return dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def inventory():
    records = {rel: digest(ROOT / rel) for rel in INPUTS}
    manifest = json.loads((ROOT / 'artifacts/MANIFEST.json').read_text())['files']
    for rel in INPUTS:
        if rel in manifest:
            assert records[rel] == {key: manifest[rel][key] for key in ('bytes', 'sha256')}
    return records


def run(label, argv, seed=None):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    env.pop('PYTHONHASHSEED', None)
    if seed is not None:
        env['PYTHONHASHSEED'] = str(seed)
    start = time.monotonic()
    result = subprocess.run(argv, cwd=ROOT, env=env, capture_output=True)
    duration = time.monotonic() - start
    stdout, stderr = HERE / 'logs' / (label + '.stdout.log'), HERE / 'logs' / (label + '.stderr.log')
    stdout.write_bytes(result.stdout)
    stderr.write_bytes(result.stderr)
    entry = dict(label=label, argv=argv, cwd=str(ROOT),
                 env_overrides={'PYTHONDONTWRITEBYTECODE': '1', **({'PYTHONHASHSEED': str(seed)} if seed is not None else {})},
                 exit_code=result.returncode, elapsed_seconds=round(duration, 6),
                 stdout={**digest(stdout), 'path': str(stdout.relative_to(HERE))},
                 stderr={**digest(stderr), 'path': str(stderr.relative_to(HERE))})
    print(json.dumps(entry, sort_keys=True), flush=True)
    return entry


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--phase', choices=('restore', 'finite', 'finish'), required=True)
    args = parser.parse_args()
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == CANDIDATE
    (HERE / 'logs').mkdir(exist_ok=True)
    log_path = HERE / 'commands.json'
    entries = json.loads(log_path.read_text()) if log_path.exists() else []
    if args.phase == 'restore':
        assert not log_path.exists(), 'Use a fresh audit directory'
        entries.append(run('restore-input', [sys.executable, str(HERE / 'restore_input.py')]))
        assert entries[-1]['exit_code'] == 0
        (HERE / 'input-before.json').write_text(json.dumps(inventory(), sort_keys=True, indent=2) + '\n')
    elif args.phase == 'finite':
        before = json.loads((HERE / 'input-before.json').read_text())
        assert inventory() == before
        for label, seed in [('independent-default', None), ('independent-seed17', 17)]:
            entries.append(run(label, [sys.executable, str(HERE / 'verify.py'), '--root', str(ROOT),
                                      '--output', str(HERE / (label + '.json'))], seed))
    else:
        after = inventory()
        before = json.loads((HERE / 'input-before.json').read_text())
        (HERE / 'input-after.json').write_text(json.dumps(after, sort_keys=True, indent=2) + '\n')
        assert after == before
        entries.append(run('candidate-tracked-diff', ['git', 'diff', '--exit-code', CANDIDATE, '--']))
        entries.append(run('candidate-whitespace', ['git', 'diff', '--check']))
    log_path.write_text(json.dumps(entries, sort_keys=True, indent=2) + '\n')


if __name__ == '__main__':
    main()
