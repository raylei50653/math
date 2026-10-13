#!/usr/bin/env python3
"""Read-only replay and expected-rejection tests; create new logs exclusively."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

AUDIT = Path(__file__).resolve().parent
ROOT = AUDIT.parents[1]
REL = AUDIT.relative_to(ROOT).as_posix()


def run(job):
    name, argv, expected, seed = job
    environment = dict(os.environ)
    environment['PYTHONDONTWRITEBYTECODE'] = '1'
    if seed:
        environment['PYTHONHASHSEED'] = '17'
    start = time.monotonic()
    result = subprocess.run(argv, cwd=ROOT, env=environment,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    log = 'logs/replay_' + name + '.log'
    with (AUDIT / log).open('x') as handle:
        handle.write(result.stdout)
    return dict(name=name, argv=argv, pythonhashseed=17 if seed else None,
                expected_exit=expected, exit_code=result.returncode,
                matches_expectation=result.returncode == expected,
                seconds=round(time.monotonic()-start, 3), log=log)


def main():
    if (AUDIT / 'verification.json').exists():
        raise SystemExit('Refusing to overwrite verification.json')
    primary = ['python3', '-B', REL + '/controls/check_three_color_support.py']
    independent = ['python3', '-B', REL + '/review/independent_check.py']
    supplementary = ['python3', '-B', REL + '/review/strict_support_check.py']
    jobs = [
        ('primary', primary + ['--check'], 0, False),
        ('primary_seed17', primary + ['--check', '--seed', '17'], 0, True),
        ('independent', independent, 0, False),
        ('supplementary', supplementary + ['--check', REL + '/review/strict_support.json'], 0, False),
        ('refuse_overwrite', primary + ['--write'], 1, False),
    ]
    fixture_metadata = json.loads((AUDIT / 'negative/fixtures.json').read_text())
    for fixture in fixture_metadata['fixtures']:
        path = REL + '/' + fixture['path']
        jobs.append(('bad_primary_' + fixture['name'], primary + ['--check', '--certificate', path], 1, False))
        jobs.append(('bad_independent_' + fixture['name'], independent + ['--primary', path], 1, False))
    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(run, jobs))
    inputs = json.loads((AUDIT / 'INPUTS.json').read_text())
    hashes = []
    for entry in inputs['entries']:
        frozen = hashlib.sha256((AUDIT / 'frozen' / entry['path']).read_bytes()).hexdigest()
        live = hashlib.sha256((ROOT / entry['path']).read_bytes()).hexdigest()
        hashes.append(dict(path=entry['path'], frozen_matches=frozen == entry['sha256'],
                           live_matches=live == entry['sha256']))
    repo_checks = [json.loads((AUDIT / ('logs/' + name + '.json')).read_text())
                   for name in ('docs', 'formal_docgraph', 'whole_docgraph', 'lean_regression', 'whitespace')]
    document = dict(base=inputs['base'], replay_results=results, input_hashes=hashes,
                    repo_checks=repo_checks,
                    whole_docgraph_status='FAIL: 62 retained historical duplicate-ID errors; no global PASS',
                    no_new_lean_theorem=True,
                    all_replay_expectations_met=all(r['matches_expectation'] for r in results),
                    frozen_input_drift=sum(not r['frozen_matches'] for r in hashes),
                    live_input_drift=sum(not r['live_matches'] for r in hashes),
                    scope='Only this audit was written. Other untracked concurrent audits are not touched.')
    with (AUDIT / 'verification.json').open('x') as handle:
        json.dump(document, handle, indent=2)
        handle.write('\n')
    print(json.dumps({k: document[k] for k in
                      ('all_replay_expectations_met', 'frozen_input_drift', 'live_input_drift')}))
    print(json.dumps({'replays': len(results), 'expected_rejections': sum(r['expected_exit'] != 0 for r in results),
                      'unexpected': [r for r in results if not r['matches_expectation']]}))
    if not document['all_replay_expectations_met'] or document['frozen_input_drift']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
