#!/usr/bin/env python3
"""Run existing read-only checks against an isolated repository snapshot."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import time

PURE = [
    'c5_excess_two_mixed_core_four_spoke_short_face',
    'c5_excess_two_mixed_core_four_spoke_long_face',
    'c5_excess_two_mixed_core_four_spoke_crosscut',
    'c5_excess_two_mixed_core_four_spoke_short_arc',
    'c5_excess_two_mixed_core_four_spoke_disjoint_pairs',
    'c5_excess_two_mixed_core_four_spoke_equal_pair',
    'c5_short_support_singleton',
    'c5_excess_two_mixed_core_leaf_fibers',
    'c5_excess_two_four_spoke_binary_star',
    'c5_excess_two_four_spoke_binary_hubs',
    'c5_excess_two_mixed_core_four_spoke_ternary',
    'c5_excess_two_mixed_core_four_spoke_quaternary',
    'c5_single_spoke_three_one',
]
NETWORKX = [
    'c5_excess_two_mixed_core_single_spoke',
    'c5_excess_two_mixed_core_four_spoke_singles',
    'c5_excess_two_mixed_core_four_spoke_binary',
    'c5_excess_two_four_spoke_progress_audit',
]
EPSILON_ONE = [
    'c5_941_single_spoke', 'c5_941_two_spoke', 'c5_941_three_spoke',
    'c5_excess_one_subcovers', 'c5_independent_support_capacity',
]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--jobs', type=int, default=3)
    parser.add_argument('--scope', choices=('latest-and-prerequisites', 'epsilon-one', 'all'),
                        default='latest-and-prerequisites')
    args = parser.parse_args()
    repo, out = args.repo.resolve(), args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)

    def run(name, nx, seed):
        argv = (['uv', 'run', '--with', 'networkx==3.5', 'python'] if nx
                else ['python3']) + [f'scripts/{name}.py', '--check']
        env = os.environ.copy()
        env.pop('PYTHONHASHSEED', None)
        env['PYTHONDONTWRITEBYTECODE'] = '1'
        if seed is not None:
            env['PYTHONHASHSEED'] = str(seed)
        label = f'{name}.seed-{seed if seed is not None else "default"}'
        start = datetime.now(timezone.utc).isoformat()
        t0 = time.monotonic()
        process = subprocess.run(argv, cwd=repo, env=env, capture_output=True, text=True)
        result = dict(name=name, argv=argv, pythonhashseed=seed, cwd=str(repo),
                      started_utc=start, elapsed_seconds=round(time.monotonic()-t0, 3),
                      returncode=process.returncode, stdout=process.stdout,
                      stderr=process.stderr, historical_artifacts_written=False)
        (out/f'{label}.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
        (out/f'{label}.log').write_text(process.stdout + process.stderr)
        print(json.dumps({k:result[k] for k in ('name','pythonhashseed','returncode','elapsed_seconds')}, sort_keys=True), flush=True)
        return result

    results=[]
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        names = ([(n,False) for n in PURE]+[(n,True) for n in NETWORKX]
                 if args.scope != 'epsilon-one' else [])
        if args.scope in ('epsilon-one','all'):
            names += [(n,False) for n in EPSILON_ONE]
        futures=[pool.submit(run,name,nx,seed) for name,nx in names
                 for seed in (None,17)]
        for future in as_completed(futures):
            results.append(future.result())
            (out/'results.json').write_text(json.dumps(sorted(results,key=lambda r:(r['name'], -1 if r['pythonhashseed'] is None else r['pythonhashseed'])),ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(replay_count=len(results),pass_count=sum(r['returncode']==0 for r in results),failure_count=sum(r['returncode']!=0 for r in results)),sort_keys=True),flush=True)

if __name__=='__main__':
    main()
