#!/usr/bin/env python3
"""Record actual independent checker replays and small corrupt-copy controls."""
from pathlib import Path
import copy
import hashlib
import json
import os
import subprocess

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]

def write_new(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(raw)

def fixture(name, obj):
    path = OUT / 'negative-controls' / (name + '.json')
    write_new(path, (json.dumps(obj, indent=2, sort_keys=True) + '\n').encode())
    return path

def main():
    commands = []
    def run(label, args, expect, seed=None, expected_error=None):
        argv = ['python3', '-B', str(OUT / 'checker.py'), *args]
        env = dict(os.environ)
        if seed is None:
            env.pop('PYTHONHASHSEED', None)
        else:
            env['PYTHONHASHSEED'] = seed
        process = subprocess.run(argv, cwd=ROOT, env=env, capture_output=True)
        stdout = 'logs/' + label + '.stdout.log'
        stderr = 'logs/' + label + '.stderr.log'
        write_new(OUT / stdout, process.stdout)
        write_new(OUT / stderr, process.stderr)
        matched = process.returncode == expect and (expected_error is None or expected_error.encode() in process.stderr)
        commands.append({'id': label, 'argv': argv, 'cwd': str(ROOT),
                         'env_override': {'PYTHONHASHSEED': seed}, 'exit_code': process.returncode,
                         'expected_exit_code': expect, 'expected_error': expected_error,
                         'expectation_matched': matched, 'stdout': stdout, 'stderr': stderr})
        if not matched:
            raise RuntimeError('unexpected checker result: ' + label)
        return process.stdout
    normal = run('independent-normal', [], 0)
    seeded = run('independent-seed17', [], 0, seed='17')
    if normal != seeded:
        raise RuntimeError('normal/seed17 output changed')
    source = json.loads((OUT / 'frozen/worker/claims.json').read_bytes())
    positive = fixture('claims-positive', source)
    run('claims-positive', ['--component', 'claims', '--fixture', str(positive)], 0)
    missing = copy.deepcopy(source)
    missing['claims'][0]['sufficient_premises'].pop()
    path = fixture('claims-missing-premise', missing)
    run('claims-missing-premise', ['--component', 'claims', '--fixture', str(path)], 1,
        expected_error='claim source premise missing: N45-SS-COST')
    cycle = copy.deepcopy(source)
    cycle['claims'][0]['dependencies'].append('N45-SS-EXCLUSION')
    path = fixture('claims-cycle', cycle)
    run('claims-cycle', ['--component', 'claims', '--fixture', str(path)], 1,
        expected_error='claim dependency cycle: N45-SS-COST')
    promoted = copy.deepcopy(source)
    promoted['claims'][0]['coverage']['finite_source_controls'] = 'SS zero triggers prove exclusion'
    path = fixture('claims-promoted-finite', promoted)
    run('claims-promoted-finite', ['--component', 'claims', '--fixture', str(path)], 1,
        expected_error='finite SS evidence has been promoted: N45-SS-COST')
    digest = hashlib.sha256(b'original bytes\n').hexdigest()
    good = {'manifest': digest + '  payload.txt\n', 'observed': {'payload.txt': digest}}
    path = fixture('manifest-positive', good)
    run('manifest-positive', ['--component', 'manifest-fixture', '--fixture', str(path)], 0)
    changed = copy.deepcopy(good)
    changed['observed']['payload.txt'] = hashlib.sha256(b'altered bytes\n').hexdigest()
    path = fixture('manifest-byte-drift', changed)
    run('manifest-byte-drift', ['--component', 'manifest-fixture', '--fixture', str(path)], 1,
        expected_error='manifest digest mismatch: payload.txt')
    extra = copy.deepcopy(good)
    extra['observed']['unexpected.txt'] = digest
    path = fixture('manifest-extra-file', extra)
    run('manifest-extra-file', ['--component', 'manifest-fixture', '--fixture', str(path)], 1,
        expected_error='manifest exact inventory mismatch')
    duplicate = copy.deepcopy(good)
    duplicate['manifest'] += duplicate['manifest']
    path = fixture('manifest-duplicate-path', duplicate)
    run('manifest-duplicate-path', ['--component', 'manifest-fixture', '--fixture', str(path)], 1,
        expected_error='duplicate manifest path: payload.txt')
    result = {'task': 'N45-SSC', 'normal_seed17_byte_equal': normal == seeded,
              'scope': 'Read-only artifact audit; six small corrupt-copy failures do not establish general validator soundness.',
              'commands': commands}
    write_new(OUT / 'checks.json', (json.dumps(result, indent=2, sort_keys=True) + '\n').encode())
    write_new(OUT / 'independent-judgment.json', normal)
    print(json.dumps({'normal_seed17_byte_equal': True, 'commands': len(commands),
                      'negative_controls_rejected': 6, 'all_expected_results_matched': True}, sort_keys=True))

if __name__ == '__main__':
    main()
