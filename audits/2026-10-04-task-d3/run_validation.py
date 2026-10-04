#!/usr/bin/env python3
"""Run read-only checks, preserving each attempt under a fresh output path."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path('.'))
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--scope', choices=('original', 'navigation'), required=True)
    args = parser.parse_args()
    root, out = args.repo.resolve(), args.output.resolve()
    assert not out.exists(), 'Choose a new output path to preserve earlier attempts'
    out.mkdir(parents=True)
    if args.scope == 'original':
        cwd = root / 'audits/2026-10-04-task-d3/snapshot'
        specs = [(name + '.seed-' + (seed or 'default'),
                  ['python3', 'scripts/' + name + '.py', '--check'], seed)
                 for name in ('c5_mixed_p3_common_endpoint', 'c5_mixed_p3_one_color_ternary_unary')
                 for seed in (None, '17')]
    else:
        cwd = root
        specs = [
            ('lake_build', ['lake', 'build'], None),
            ('check_docs', ['python3', 'scripts/check_docs.py'], None),
            ('docgraph', ['python3', 'tools/docgraph', 'check'], None),
            ('artifact_status', ['python3', 'tools/artifacts.py', 'status'], None),
            ('diff_check', ['git', 'diff', '--check'], None),
        ]

    def run(spec):
        name, command, seed = spec
        env = os.environ.copy()
        env.pop('PYTHONHASHSEED', None)
        if seed is not None:
            env['PYTHONHASHSEED'] = seed
        started = time.monotonic()
        process = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True)
        result = dict(name=name, command=command, cwd=str(cwd), hashseed=seed or 'default',
                      exit_code=process.returncode, elapsed_seconds=time.monotonic() - started,
                      stdout=process.stdout, stderr=process.stderr)
        (out / (name + '.log')).write_text(process.stdout + process.stderr)
        (out / (name + '.json')).write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
        print(json.dumps(dict(name=name, exit_code=process.returncode)), flush=True)
        return result

    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(run, specs))
    (out / 'results.json').write_text(json.dumps(results, indent=2, ensure_ascii=False) + '\n')
    assert all(r['exit_code'] == 0 for r in results)


if __name__ == '__main__':
    main()
