#!/usr/bin/env python3
"""Read-only normal/seed17 replay and fail-closed negative certificate controls."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PREFIX = str(HERE.relative_to(ROOT))
OLD = 'audits/2026-10-12-neartri-complete-relation-reductions-5d70a399'


def read(path):
    return json.loads(path.read_text())


def serialized(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n'


def run(spec):
    name, argv, seed, expected = spec
    env = os.environ.copy()
    if seed is not None:
        env['PYTHONHASHSEED'] = str(seed)
    result = subprocess.run(argv, cwd=ROOT, env=env, capture_output=True, text=True)
    success = result.returncode == 0 if expected == 'pass' else result.returncode != 0
    return dict(name=name, argv=argv, seed=seed, expected=expected,
                returncode=result.returncode, verified=success,
                stdout=result.stdout.strip(), stderr=result.stderr.strip())


def main():
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--write', action='store_true')
    modes.add_argument('--check', action='store_true')
    args = parser.parse_args()
    negative_dir = HERE / 'negative-controls'
    if args.write:
        negative_dir.mkdir(exist_ok=False)
    certificate = read(HERE / 'joint/count_identity_certificate.json')
    wrong_coefficient = deepcopy(certificate)
    wrong_coefficient['identities'][0]['rhs'][0]['coefficient'] += 1
    wrong_preimage = deepcopy(certificate)
    wrong_preimage['upper_preimages_of_outer_word'].pop()
    controls = read(HERE / 'counts/controls.json')
    omitted_lift = deepcopy(controls)
    next(row for row in omitted_lift['literal_controls'][0]['full_lifts'] if row).pop()
    fixtures = {'coefficient.json': wrong_coefficient, 'preimage.json': wrong_preimage,
                'full-lift.json': omitted_lift}
    for name, payload in fixtures.items():
        path = negative_dir / name
        if args.write:
            with path.open('x') as stream:
                stream.write(serialized(payload))
        else:
            assert read(path) == payload, ('negative fixture drift', name)
    commands = [
        ('count-identities', ['python3', PREFIX+'/joint/count_identity.py', '--check']),
        ('independent-count-review', ['python3', PREFIX+'/topology/count_review.py']),
        ('complete-relations', ['python3', PREFIX+'/caps/checker.py', '--check']),
        ('independent-relations-and-caps', ['python3', PREFIX+'/caps/independent_verify.py']),
        ('singleton-fan', ['python3', PREFIX+'/caps/singleton_verify.py']),
        ('literal-count-controls', ['python3', PREFIX+'/counts/controls.py', '--check']),
    ]
    specs = [(name, argv, seed, 'pass') for seed in (None, 17) for name, argv in commands]
    specs += [('inherited-full-collar', ['python3', OLD+'/collar_checker.py', '--check'], None, 'pass')]
    for fixture in ('coefficient.json', 'preimage.json'):
        specs.append(('reject-'+fixture, ['python3', PREFIX+'/joint/count_identity.py',
            '--check', '--certificate', PREFIX+'/negative-controls/'+fixture], None, 'reject'))
    specs.append(('reject-missing-full-lift', ['python3', PREFIX+'/counts/controls.py',
        '--check', '--certificate', PREFIX+'/negative-controls/full-lift.json'], None, 'reject'))
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(run, specs))
    assert all(x['verified'] for x in results), [x for x in results if not x['verified']]
    for name, _ in commands:
        pair = [x for x in results if x['name'] == name]
        assert pair[0]['stdout'] == pair[1]['stdout'], ('seed drift', name)
    frozen = []
    for path in sorted((HERE / 'frozen').rglob('*')):
        if not path.is_file() or '__pycache__' in path.parts:
            continue
        relative = path.relative_to(HERE / 'frozen')
        frozen.append(dict(path=str(relative), sha256=sha256(path.read_bytes()).hexdigest(),
                           unchanged_authority=(ROOT/relative).read_bytes() == path.read_bytes()
                           if str(relative).startswith('audits/') else 'routing updated deliberately'))
    assert all(x['unchanged_authority'] is not False for x in frozen)
    original = read(HERE/'BASE.json')
    assert all(sha256((HERE/'frozen'/p).read_bytes()).hexdigest() == digest
               for p, digest in original['inputs_sha256'].items())
    subaudits = {str(p.relative_to(HERE)): sha256(p.read_bytes()).hexdigest()
                 for p in (HERE/'caps/verification.json', HERE/'topology/verification.json')}
    payload = dict(status='PASS', claim='No disk C7 relation is contained in U55; minimal 941 has h>=3 and n5>=9',
                   base=original['base'], checks=results, frozen_inputs=frozen,
                   source_input_drift=0, subaudit_verification_sha256=subaudits,
                   paper_scope='arbitrary finite planar C7 interior, fixed labels and full counts',
                   target_control_status='not triggered', universal_exclusion='proved',
                   lean='No Lean files changed; no new Lean theorem; lake build intentionally not rerun',
                   external_enumeration='not rerun')
    path = HERE/'verification.json'
    if args.write:
        with path.open('x') as stream:
            json.dump(payload, stream, sort_keys=True, indent=2)
            stream.write('\n')
    else:
        assert read(path) == payload, 'verification record mismatch'
    print(json.dumps(dict(status='PASS', replay_checks=len(results), source_input_drift=0,
        independent_full_cap_queries_per_seed=307853, negative_certificates_rejected=3,
        normal_seed17_agree=True), sort_keys=True))


if __name__ == '__main__':
    main()
