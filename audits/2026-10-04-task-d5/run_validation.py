#!/usr/bin/env python3
"""Read-only D5 replays and integration checks with immutable attempt outputs."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import time

NAMES = (
    'c5_excess_two_mixed_core_four_spoke_mixed12',
    'c5_excess_two_mixed_core_four_spoke_mixed12_01_12',
    'c5_excess_two_mixed_core_four_spoke_mixed12_01_01',
    'c5_excess_two_mixed_core_four_spoke_mixed12_04_04',
    'c5_excess_two_mixed_core_four_spoke_mixed22',
    'c5_excess_two_mixed_core_four_spoke_mixed22_short_face',
    'c5_excess_two_mixed_core_four_spoke_mixed22_long_face',
    'c5_excess_two_mixed_core_four_spoke_mixed22_shared4',
    'c5_mixed_p3_common_endpoint',
    'c5_mixed_p3_one_color_ternary_unary',
    'c5_mixed_p3_two_frame_ternary_unary',
    'c5_mixed_p3_two_frame_two_unary',
)
HELPERS = ('c5_excess_two_four_spoke_mixed12_04_04_joint_controls',)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path('.'))
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--scope', choices=('original', 'navigation', 'lake'), required=True)
    args = parser.parse_args()
    root, out = args.repo.resolve(), args.output.resolve()
    assert not out.exists(), 'Use a new path; preserve all failures'
    out.mkdir(parents=True)
    base = root / 'audits/2026-10-04-task-d5'
    if args.scope == 'original':
        cwd = base / 'snapshot'
        specs = []
        for name in NAMES + HELPERS:
            for seed in (None, '17'):
                label = name + '.seed-' + (seed or 'default')
                command = ['python3', str(base / 'trace_runtime.py'), '--repo', str(cwd),
                           '--script', name + '.py', '--output', str(out / (label + '.runtime.json'))]
                specs.append((label, command, seed))
    elif args.scope == 'navigation':
        cwd = root
        specs = [('check_docs', ['python3', 'scripts/check_docs.py'], None),
                 ('docgraph', ['python3', 'tools/docgraph', 'check'], None),
                 ('artifact_status', ['uv', 'run', '--with-requirements', 'requirements.txt',
                                      'python', 'tools/artifacts.py', 'status'], None),
                 ('diff_check', ['git', 'diff', '--check'], None)]
    else:
        cwd, specs = root, [('lake_build', ['lake', 'build'], None)]

    def run(spec):
        name, command, seed = spec
        env = os.environ.copy()
        env.pop('PYTHONHASHSEED', None)
        env['PYTHONDONTWRITEBYTECODE'] = '1'
        if seed:
            env['PYTHONHASHSEED'] = seed
        start = time.monotonic()
        proc = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True)
        result = {'name': name, 'command': command, 'cwd': str(cwd),
                  'hashseed': seed or 'default', 'exit_code': proc.returncode,
                  'elapsed_seconds': time.monotonic() - start,
                  'stdout': proc.stdout, 'stderr': proc.stderr}
        (out / (name + '.log')).write_text(proc.stdout + proc.stderr)
        (out / (name + '.json')).write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        print(json.dumps({'name': name, 'exit_code': proc.returncode}), flush=True)
        return result

    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(run, specs))
    (out / 'results.json').write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n')
    assert all(r['exit_code'] == 0 for r in results)


if __name__ == '__main__':
    main()
