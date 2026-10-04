#!/usr/bin/env python3
"""Read-only D2 replays; logs and result JSON go only to this audit directory."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--scope', choices=('historical', 'integration', 'navigation'), required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    specs = []
    if args.scope == 'historical':
        for name in ('c5_excess_two_mixed_core_single_spoke',
                     'c5_excess_two_mixed_core_four_spoke_singles'):
            for seed in (None, '17'):
                command = ['uv', 'run', '--with', 'networkx==3.5', 'python']
                specs.append((name + '.seed-' + (seed or 'default'),
                              command + ['scripts/' + name + '.py', '--check'], seed))
    else:
        specs = [
            ('c_check_seed17', ['python3', 'scripts/c5_mixed_p3_common_endpoint.py', '--check'], '17'),
            ('c2_check_seed17', ['python3', 'scripts/c5_mixed_p3_one_color_ternary_unary.py', '--check'], '17'),
            ('lake_build', ['lake', 'build'], None),
            ('check_docs', ['python3', 'scripts/check_docs.py'], None),
            ('audit_links', ['python3', 'audits/2026-10-04-task-d2/check_audit_links.py', '--repo', '.'], None),
            ('docgraph', ['python3', 'tools/docgraph', 'check'], None),
            ('artifact_status', ['python3', 'tools/artifacts.py', 'status'], None),
            ('diff_check', ['git', 'diff', '--check'], None),
        ]
        if args.scope == 'navigation':
            specs=[spec for spec in specs if spec[0] not in ('c_check_seed17','c2_check_seed17','lake_build')]
    results = []
    for name, command, seed in specs:
        env = os.environ.copy()
        env.pop('PYTHONHASHSEED', None)
        if seed is not None:
            env['PYTHONHASHSEED'] = seed
        started = time.monotonic()
        run = subprocess.run(command, cwd=repo, env=env, capture_output=True, text=True)
        result = dict(name=name, command=command, cwd=str(repo), hashseed=seed or 'default',
                      exit_code=run.returncode, elapsed_seconds=time.monotonic()-started,
                      stdout=run.stdout, stderr=run.stderr)
        results.append(result)
        (out/(name+'.log')).write_text(run.stdout+run.stderr)
        print(json.dumps(dict(name=name, exit_code=run.returncode), sort_keys=True), flush=True)
    (out/(args.scope+'_checks.json')).write_text(json.dumps(results, indent=2, ensure_ascii=False)+'\n')
    if args.scope in ('integration','navigation'):
        assert all(r['exit_code'] == 0 for r in results)
    else:
        assert all(r['exit_code'] != 0 and 'certificate differs' in r['stderr'] for r in results)


if __name__ == '__main__':
    main()
