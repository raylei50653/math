#!/usr/bin/env python3
"""Capture actual navigation checks without editing source or old artifacts."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def run(spec):
    name, argv, cwd, expected = spec
    result = subprocess.run(argv, cwd=cwd, capture_output=True, check=False)
    for stream in ('stdout', 'stderr'):
        with (HERE / f'logs/{name}.{stream}.log').open('xb') as output:
            output.write(getattr(result, stream))
    return dict(id=name, argv=argv, cwd=str(cwd), exit_code=result.returncode,
                expected_exit=expected, exit_matches_expectation=result.returncode == expected,
                stdout=f'logs/{name}.stdout.log', stderr=f'logs/{name}.stderr.log')


def main():
    base = HERE / 'base-source'
    specs = [
        ('fresh-base-docs', ['python3', '-B', 'scripts/check_docs.py'], base, 1),
        ('fresh-base-formal-docgraph', ['python3', '-B', 'tools/docgraph', '--include', 'docs/**/*.md', 'check'], base, 0),
        ('current-docs', ['python3', '-B', 'scripts/check_docs.py'], ROOT, 0),
        ('current-formal-docgraph', ['python3', '-B', 'tools/docgraph', '--include', 'docs/**/*.md', 'check'], ROOT, 0),
        ('current-whole-docgraph', ['python3', '-B', 'tools/docgraph', 'check'], ROOT, 1),
        ('tracked-diff-check', ['git', 'diff', '--check'], ROOT, 0),
        ('cached-diff-check', ['git', 'diff', '--cached', '--check'], ROOT, 0),
    ]
    with ThreadPoolExecutor(max_workers=3) as pool:
        commands = list(pool.map(run, specs))
    base_text = (HERE / 'logs/fresh-base-docs.stdout.log').read_text() + (HERE / 'logs/fresh-base-docs.stderr.log').read_text()
    whole = (HERE / 'logs/current-whole-docgraph.stdout.log').read_text() + (HERE / 'logs/current-whole-docgraph.stderr.log').read_text()
    results = dict(task='N45-S-LOW1', commands=commands,
                   fresh_base_missing_paths=[line for line in base_text.splitlines() if 'missing path:' in line],
                   whole_worktree_duplicate_id_lines=sum('duplicate' in line.lower() for line in whole.splitlines()),
                   historical_E4_provenance='Prior byte-replay FAIL retained, not rerun in this task',
                   postseal_actual_results='seal-checks/commands.json',
                   no_mathematical_checker_replay=True,
                   source_controls='not performed; no trigger count',
                   not_run=['new graph/k enumeration', 'upstream source/control checkers', 'PC LP schema',
                            'U1-U4', 'LP/SS reproof', 'Lean build/axiom audit', 'remote CI'],
                   doc_failures_preserved=True)
    with (HERE / 'checks.json').open('x') as output:
        json.dump(results, output, ensure_ascii=False, sort_keys=True, indent=2)
        output.write('\n')
    print(json.dumps(dict(exits={c['id']:c['exit_code'] for c in commands},
                          fresh_base_missing_paths=results['fresh_base_missing_paths'],
                          whole_worktree_duplicate_id_lines=results['whole_worktree_duplicate_id_lines']), sort_keys=True))
    if not all(c['exit_matches_expectation'] for c in commands):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
