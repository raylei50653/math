#!/usr/bin/env python3
"""Read-only replay of the 19 early audit reports and two extra checkers.

Writes receipts only beside this runner. Original audit files and certificates
are never generated, edited, or replaced. Expected semantic-negative commands
return PASS after rejecting damaged in-memory copies.
"""
import concurrent.futures
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = HERE.parent.parent / 'BASE.json'
TIMEOUT_SECONDS = 180
EXCLUDED = {
    'gamma8-empty-k-stars', 'gamma8-empty-resource-stars',
    'gamma8-empty-seven', 'gamma8-k-star-review', 'gamma8-n-stars',
    'gamma8-n7-review', 'gamma8-nonempty-k-stars',
    'gamma8-nonempty-resource-stars', 'gamma8-resource-review',
    'types-wrong-side-round4', 'types-wrong-side-round5',
    'types-wrong-side-round6', 'types-wrong-side-round7',
}


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def integrity(base):
    drift = []
    for row in base['entries']:
        p = ROOT / row['path']
        if not p.is_file():
            drift.append({'path': row['path'], 'reason': 'missing'})
            continue
        raw = p.read_bytes()
        sha = hashlib.sha256(raw).hexdigest()
        if len(raw) != row['bytes'] or sha != row['sha256']:
            drift.append({'path': row['path'], 'bytes': len(raw), 'sha256': sha})
    return {'checked_files': len(base['entries']), 'drift': drift}


def commands(base):
    result = []
    for directory in base['directories']:
        short = directory.split('2026-10-23-941-', 1)[1].removesuffix('-6b09cd4')
        if short in EXCLUDED:
            continue
        report = ROOT / directory / 'REPORT.md'
        blocks = re.findall(r'```(?:sh|bash)?\n(.*?)```', report.read_text(), re.S)
        lines = [line.strip() for block in blocks for line in block.splitlines()
                 if line.strip()]
        if len(lines) != 3:
            raise ValueError(f'Expected documented normal/seed17/negative triple: {report}')
        for mode, line in zip(('normal', 'seed17', 'negative'), lines):
            argv = shlex.split(line)
            env = {'PYTHONDONTWRITEBYTECODE': '1'}
            if argv[0] == 'PYTHONHASHSEED=17':
                env['PYTHONHASHSEED'] = '17'
                argv.pop(0)
            if argv[0] != 'python3' or any('produce' in arg for arg in argv):
                raise ValueError(f'Unexpected mutating command: {line}')
            result.append({'id': f'{short}--{mode}', 'directory': directory,
                           'group': short, 'mode': mode, 'argv': argv,
                           'environment_overrides': env, 'documented_command': line,
                           'authority': f'{directory}/REPORT.md'})
    directory = 'audits/2026-10-23-941-gamma8-chi-review-6b09cd4'
    script = f'{directory}/check_cover.py'
    for mode, opts in [('normal', []), ('seed17', ['--seed', '17']),
                       ('negative', ['--negative'])]:
        env = {'PYTHONDONTWRITEBYTECODE': '1'}
        argv = ['python3', '-B']
        if mode == 'seed17':
            argv += ['-O']
            env['PYTHONHASHSEED'] = '17'
        result.append({'id': f'gamma8-chi-review-cover--{mode}',
                       'directory': directory, 'group': 'gamma8-chi-review-cover',
                       'mode': mode, 'argv': argv + [script] + opts,
                       'environment_overrides': env,
                       'authority': f'{directory}/REPORT.md and inspected checker CLI'})
    directory = 'audits/2026-10-23-941-wrong-side-general-6b09cd4'
    for mode in ('normal', 'seed17'):
        env = {'PYTHONDONTWRITEBYTECODE': '1'}
        if mode == 'seed17':
            env['PYTHONHASHSEED'] = '17'
        result.append({'id': f'wrong-side-general-empty-m2-review--{mode}',
                       'directory': directory, 'group': 'wrong-side-general-empty-m2-review',
                       'mode': mode,
                       'argv': ['python3', '-B', f'{directory}/review_empty_m2.py'],
                       'environment_overrides': env,
                       'authority': f'{directory}/REVIEW_EMPTY_M2.md and inspected checker',
                       'optimization_note': 'No -O: this supplementary topology checker uses assert.'})
    return result


def run_one(spec):
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    before = time.monotonic()
    env = os.environ.copy()
    env.update(spec['environment_overrides'])
    receipt = dict(spec, cwd='repository root', started_utc=started,
                   timeout_seconds=TIMEOUT_SECONDS)
    try:
        proc = subprocess.run(spec['argv'], cwd=ROOT, env=env, text=True,
                              capture_output=True, timeout=TIMEOUT_SECONDS)
        receipt.update(exit_code=proc.returncode, timed_out=False,
                       stdout=proc.stdout, stderr=proc.stderr)
    except subprocess.TimeoutExpired as error:
        def txt(value):
            return value.decode(errors='replace') if isinstance(value, bytes) else value or ''
        receipt.update(exit_code=None, timed_out=True,
                       stdout=txt(error.stdout), stderr=txt(error.stderr))
    receipt['elapsed_seconds'] = round(time.monotonic() - before, 6)
    try:
        receipt['payload'] = json.loads(receipt['stdout'])
    except (json.JSONDecodeError, KeyError):
        receipt['payload'] = None
    payload = receipt['payload']
    explicit_pass = isinstance(payload, dict) and payload.get('status') == 'PASS'
    # The joint-bpaths and u-link checkers document custody/validation output
    # without a top-level status. Their semantic checks raise on failure.
    validated_custody = (isinstance(payload, dict) and 'status' not in payload
                         and isinstance(payload.get('validation'), dict)
                         and isinstance(payload.get('custody'), dict)
                         and payload['custody'].get('immutable_drift') == 0)
    receipt['success_evidence'] = ('explicit PASS' if explicit_pass else
                                    'zero exit with documented custody/validation schema'
                                    if validated_custody else 'unrecognized or failed output')
    receipt['passed'] = receipt['exit_code'] == 0 and (explicit_pass or validated_custody)
    dump(HERE / (spec['id'] + '.json'), receipt)
    print(json.dumps({'id': spec['id'], 'passed': receipt['passed'],
                      'elapsed_seconds': receipt['elapsed_seconds']}, sort_keys=True), flush=True)
    return receipt


def strip_seed(payload):
    if isinstance(payload, dict):
        return {key: strip_seed(value) for key, value in payload.items()
                if key != 'seed'}
    if isinstance(payload, list):
        return [strip_seed(value) for value in payload]
    return payload


def main():
    base = json.loads(BASE.read_text())
    initial = integrity(base)
    specs = commands(base)
    dump(HERE / 'COMMANDS.json', specs)
    receipts = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(run_one, spec) for spec in specs]
        for future in concurrent.futures.as_completed(futures):
            receipts.append(future.result())
    groups = {}
    for receipt in receipts:
        groups.setdefault(receipt['group'], {})[receipt['mode']] = receipt
    equality = []
    for group, modes in sorted(groups.items()):
        a, b = modes['normal'], modes['seed17']
        equality.append({'group': group,
                         'both_passed': a['passed'] and b['passed'],
                         'payloads_equal_excluding_seed': strip_seed(a['payload']) == strip_seed(b['payload']),
                         'excluded_fields': ['seed']})
    final = integrity(base)
    failed = [receipt['id'] for receipt in receipts if not receipt['passed']]
    summary = {
        'base': base['base'], 'scope': '19 early audit directories and two supplementary checkers',
        'directories': sorted({spec['directory'] for spec in specs}),
        'commands': len(specs), 'passed': len(specs) - len(failed),
        'failed': failed, 'normal_seed17_comparisons': equality,
        'source_integrity_before': initial, 'source_integrity_after': final,
        'all_passed': not failed and not initial['drift'] and not final['drift']
                      and all(row['both_passed'] and row['payloads_equal_excluding_seed'] for row in equality),
        'controls_scope': 'Finite calibration only; no source realization or general exclusion is inferred.',
        'original_audits_mutated': False,
        'supplementary_topology_note': 'review_empty_m2.py ran without -O so its assertions remain active.',
    }
    dump(HERE / 'SUMMARY.json', summary)
    print(json.dumps({'commands': len(specs), 'passed': summary['passed'],
                      'failed': failed, 'all_passed': summary['all_passed']}, sort_keys=True))


if __name__ == '__main__':
    main()
