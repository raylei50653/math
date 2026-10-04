#!/usr/bin/env python3
"""Read-only replays against the fixed snapshot; preserve each output attempt."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import time

NAMES = ('c5_excess_two_mixed_core_four_spoke_mixed12',
         'c5_excess_two_mixed_core_four_spoke_mixed12_01_12',
         'c5_excess_two_mixed_core_four_spoke_mixed12_01_01',
         'c5_excess_two_mixed_core_four_spoke_mixed22',
         'c5_excess_two_mixed_core_four_spoke_mixed22_short_face',
         'c5_excess_two_mixed_core_four_spoke_mixed22_long_face',
         'c5_mixed_p3_common_endpoint', 'c5_mixed_p3_one_color_ternary_unary',
         'c5_mixed_p3_two_frame_ternary_unary')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo', type=Path, default=Path('.'))
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--scope', choices=('original', 'navigation'), required=True)
    a = p.parse_args()
    root, out = a.repo.resolve(), a.output.resolve()
    assert not out.exists(), 'Use a new path; previous failures must remain'
    out.mkdir(parents=True)
    if a.scope == 'original':
        cwd = root / 'audits/2026-10-04-task-d4/snapshot'
        specs = [(name + '.seed-' + (seed or 'default'),
                  ['python3', 'scripts/' + name + '.py', '--check'], seed)
                 for name in NAMES for seed in (None, '17')]
    else:
        cwd = root
        specs = [('check_docs', ['python3', 'scripts/check_docs.py'], None),
                 ('docgraph', ['python3', 'tools/docgraph', 'check'], None),
                 ('artifact_status', ['python3', 'tools/artifacts.py', 'status'], None),
                 ('diff_check', ['git', 'diff', '--check'], None)]

    def run(spec):
        name, cmd, seed = spec
        env = os.environ.copy()
        env.pop('PYTHONHASHSEED', None)
        if seed:
            env['PYTHONHASHSEED'] = seed
        start = time.monotonic()
        proc = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
        result = dict(name=name, command=cmd, cwd=str(cwd), hashseed=seed or 'default',
                      exit_code=proc.returncode, elapsed_seconds=time.monotonic() - start,
                      stdout=proc.stdout, stderr=proc.stderr)
        (out / (name + '.log')).write_text(proc.stdout + proc.stderr)
        (out / (name + '.json')).write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        print(json.dumps(dict(name=name, exit_code=proc.returncode)), flush=True)
        return result

    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(run, specs))
    (out / 'results.json').write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n')
    assert all(r['exit_code'] == 0 for r in results)


if __name__ == '__main__':
    main()
