#!/usr/bin/env python3
"""Replay checks and meaningful corruption controls for C/check.py."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group()
    action.add_argument('--write', action='store_true')
    action.add_argument('--check', action='store_true')
    args = parser.parse_args()
    original = json.loads((HERE / 'certificate.json').read_text())
    rows = []

    def run(name, arguments, expected_success, environment=None):
        env = dict(os.environ)
        if environment:
            env.update(environment)
        result = subprocess.run([sys.executable, '-B', str(HERE / 'check.py'), *arguments],
                                capture_output=True, text=True, env=env)
        if (result.returncode == 0) != expected_success:
            raise ValueError(name + ' had wrong success/failure outcome: ' + result.stdout + result.stderr)
        rows.append({'case': name, 'expected_success': expected_success,
                     'returncode': result.returncode,
                     'stdout': result.stdout.strip(), 'stderr': result.stderr.strip()})

    run('normal replay', ['--check'], True)
    run('seed17 replay', ['--check', '--seed', '17'], True, {'PYTHONHASHSEED': '17'})
    with tempfile.TemporaryDirectory(prefix='r6-marked-six-C-') as directory:
        tmp = Path(directory)
        mutations = {}
        c = copy.deepcopy(original)
        c['all_matching_rows'].pop()
        mutations['omitted ordinary matching'] = c
        c = copy.deepcopy(original)
        c['all_matching_rows'][8]['complement_cycles'][0]['vertices'][0] = 99
        mutations['corrupted actual complement vertex'] = c
        c = copy.deepcopy(original)
        c['marked_simple_six_cycles'][1]['sides'][0]['E'] = 17
        mutations['corrupted cyclic-cut side edge count'] = c
        c = copy.deepcopy(original)
        c['marked_simple_six_cycles'].pop()
        mutations['omitted marked six-cycle'] = c
        c = copy.deepcopy(original)
        c['marks'][1]['edge_index'] = 28
        mutations['changed literal marked edge ID'] = c
        c = copy.deepcopy(original)
        c['source_authority'] = 'arbitrary source theorem proved'
        mutations['invented source authority'] = c
        for i, (name, corrupted) in enumerate(mutations.items()):
            path = tmp / ('certificate-' + str(i) + '.json')
            path.write_text(json.dumps(corrupted))
            run(name, ['--check', str(path)], False)
        source = HERE.parent / 'frozen' / original['input']['path'].removeprefix('frozen/')
        bad_graph = json.loads(source.read_text())
        bad_graph['marks'][1] = 28
        path = tmp / 'corrupted-graph.json'
        path.write_text(json.dumps(bad_graph))
        run('changed source input rejected by frozen hash', ['--check', '--input', str(path)], False)
        # Use a temporary existing path so the diagnostic contains no host path.
        path = tmp / 'existing.json'
        path.write_text('do not replace\n')
        before = path.read_bytes()
        result = subprocess.run([sys.executable, '-B', str(HERE / 'check.py'), '--write', str(path)],
                                capture_output=True, text=True)
        if result.returncode == 0 or path.read_bytes() != before:
            raise ValueError('exclusive certificate creation failed')
        rows.append({'case': 'exclusive creation refuses existing file and preserves bytes',
                     'expected_success': False, 'returncode': result.returncode,
                     'result': 'existing bytes preserved; File exists rejection'})
    result = {'schema': 'r6-marked-six-control-verification-v1',
              'base': original['base'],
              'checker_sha256': hashlib.sha256((HERE / 'check.py').read_bytes()).hexdigest(),
              'certificate_sha256': hashlib.sha256((HERE / 'certificate.json').read_bytes()).hexdigest(),
              'cases': rows, 'all_expected_outcomes': True}
    payload = json.dumps(result, indent=2, sort_keys=True) + '\n'
    target = HERE / 'VERIFICATION.json'
    if args.write:
        with target.open('x') as output:
            output.write(payload)
    if args.check and json.loads(target.read_text()) != result:
        raise ValueError('verification record mismatch')
    print('PASS: 2 successful replays; 7 corruption rejections; exclusive-create preservation')


if __name__ == '__main__':
    main()
