#!/usr/bin/env python3
"""Exclusive-create replay logs for the declared finite domains."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prefix', required=True)
    args = parser.parse_args()
    rows = []

    def run(name, cmd, expected=0, seed=False):
        key = args.prefix + '-' + name
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
        if seed:
            env['PYTHONHASHSEED'] = '17'
        start = time.monotonic()
        with (HERE / 'logs' / (key + '.stdout')).open('xb') as out:
            with (HERE / 'logs' / (key + '.stderr')).open('xb') as err:
                result = subprocess.run(cmd, cwd=ROOT, env=env, stdout=out, stderr=err)
        rows.append({'name': key, 'command': cmd,
                     'environment': {'PYTHONHASHSEED': '17'} if seed else {},
                     'exit_code': result.returncode, 'expected_exit_code': expected,
                     'seconds': round(time.monotonic() - start, 3)})
        print(key, result.returncode, flush=True)
        return result.returncode == expected

    py = ['python3', '-B']
    a = str(HERE.relative_to(ROOT))
    ok = True
    for seed in (False, True):
        suffix = 'seed17' if seed else 'normal'
        ok &= run('matching-' + suffix, py + [a + '/matching_check.py', '--check',
                  a + '/matching_certificate-v2.json'], seed=seed)
        cmd = py + [a + '/check_geometry.py', '--check', a + '/geometry_certificate.json']
        if seed:
            cmd += ['--seed', '17']
        ok &= run('geometry-' + suffix, cmd, seed=seed)
    for kind in ('path-parity', 'missing-empty', 'odd-cycle-flag'):
        ok &= run('negative-matching-' + kind, py + [a + '/matching_check.py', '--check',
                  a + '/matching_certificate-v2.json', '--negative', kind], expected=1)
    original = json.loads((HERE / 'geometry_certificate.json').read_text())
    for kind in ('face', 'source'):
        value = json.loads(json.dumps(original))
        if kind == 'face':
            value['input']['faces'].pop()
        else:
            value['domain']['original_source_realization'] = True
        negative = HERE / ('negative-geometry-' + kind + '.json')
        with negative.open('x') as out:
            json.dump(value, out, sort_keys=True, indent=2)
            out.write('\n')
        ok &= run('negative-geometry-' + kind, py + [a + '/check_geometry.py', '--check',
                  str(negative.relative_to(ROOT))], expected=1)
    ok &= run('exclusive-matching', py + [a + '/matching_check.py', '--write',
              a + '/matching_certificate-v2.json'], expected=1)
    ok &= run('exclusive-geometry', py + [a + '/check_geometry.py', '--write',
              a + '/geometry_certificate.json'], expected=1)
    prior = 'audits/2026-10-16-r6-double-w5-101-0b639cf'
    chord = 'audits/2026-10-16-r6-chorded-five-c4c3d99'
    for seed in (False, True):
        suffix = 'seed17' if seed else 'normal'
        ok &= run('prior-double-w5-' + suffix, py + [prior + '/check.py', '--check',
                  prior + '/certificate.json'], seed=seed)
        ok &= run('prior-chorded-five-' + suffix, py + [chord + '/check.py', '--check',
                  chord + '/certificate.json'], seed=seed)
    cap = 'audits/2026-10-16-r6-cap-barriers-c4c3d99'
    ok &= run('prior-curvature', py + [cap + '/A/check.py'])
    ok &= run('prior-complete-w5', py + [cap + '/C/check.py', '--check',
              cap + '/C/certificate.json'])
    ok &= run('prior-saturation', py + [cap + '/B/check.py', '--verify',
              cap + '/B/certificate-v2.json'])
    for name in ('matching', 'geometry'):
        lhs = (HERE / 'logs' / (args.prefix + '-' + name + '-normal.stdout')).read_bytes()
        rhs = (HERE / 'logs' / (args.prefix + '-' + name + '-seed17.stdout')).read_bytes()
        ok &= lhs == rhs
    record = {'status': 'PASS' if ok else 'FAIL', 'runs': rows,
              'normal_seed17_outputs_identical': all(
                  (HERE / 'logs' / (args.prefix + '-' + n + '-normal.stdout')).read_bytes()
                  == (HERE / 'logs' / (args.prefix + '-' + n + '-seed17.stdout')).read_bytes()
                  for n in ('matching', 'geometry'))}
    with (HERE / (args.prefix + '-verification.json')).open('x') as out:
        json.dump(record, out, indent=2)
        out.write('\n')
    raise SystemExit(0 if ok else 1)


if __name__ == '__main__':
    main()
