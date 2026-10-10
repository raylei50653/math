#!/usr/bin/env python3
"""Read-only exact artifact verifier; no mathematical or source acceptance oracle."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SEAL_FILES = ('seal-checks/before.json', 'seal-checks/after.json',
              'seal-checks/normal.stdout.log', 'seal-checks/normal.stderr.log',
              'seal-checks/seed17.stdout.log', 'seal-checks/seed17.stderr.log',
              'seal-checks/corrupt.stdout.log', 'seal-checks/corrupt.stderr.log',
              'seal-checks/corrupt.sha256', 'seal-checks/commands.json', 'seal-checks/receipt.json')
EXCLUDED = {'MANIFEST.sha256', 'delivery.json', *SEAL_FILES}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def payload(manifest):
    rows = []
    for line in manifest.read_text().splitlines():
        digest, name = line.split('  ', 1)
        p = Path(name)
        need(not p.is_absolute() and '..' not in p.parts and name == p.as_posix(), 'unsafe manifest path')
        need(len(digest) == 64 and all(c in '0123456789abcdef' for c in digest), 'unsafe digest')
        need(name not in EXCLUDED, 'excluded metadata in manifest')
        rows.append((digest, name))
    need(len(rows) == len({name for _, name in rows}), 'duplicate manifest path')
    actual = {p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if p.is_file()}
    need(not any(p.is_symlink() for p in HERE.rglob('*')), 'symlink artifact')
    need(actual - EXCLUDED == {name for _, name in rows}, 'exact payload inventory')
    for digest, name in rows:
        need(sha((HERE / name).read_bytes()) == digest, 'payload digest differs: ' + name)
    return len(rows)


def check(manifest, payload_only):
    count = payload(manifest)
    judgment = json.loads((HERE / 'independent-judgment.json').read_bytes())
    need(judgment['decision'] == 'accept_HIGH1_full_contract_paper_with_BASE_and_external_trust', 'judgment identity')
    need(len(judgment['claims']) == 10 and all(len(c['full_source_contract']) == 13 for c in judgment['claims']),
         'judgment complete scope')
    need(not judgment['machine_proves_arbitrary_size'] and not judgment['new_Lean'], 'evidence boundary')
    need(judgment['finite_source'] == {'established': False, 'executed': False,
                                     'status': 'not triggered', 'trigger_count': None}, 'source boundary')
    run = subprocess.run([sys.executable, '-B', str(HERE / 'checker.py'), '--check'],
                         cwd=ROOT, capture_output=True)
    need(run.returncode == 0, 'independent checker rejected: ' + run.stderr.decode())
    checks = json.loads((HERE / 'checks.json').read_bytes())
    need(all(r['actual_exit'] == r['expected_exit'] for r in checks['commands']), 'recorded command exit')
    need((HERE / 'logs/normal.stdout.log').read_bytes() == (HERE / 'logs/seed17.stdout.log').read_bytes(),
         'normal seed17 bytes differ')
    negative = next(r for r in checks['commands'] if r['label'] == 'bad-certificate')
    need(negative['actual_exit'] == 2 and 'calibration bytes differ' in
         (HERE / 'logs/bad-certificate.stderr.log').read_text(), 'calibration negative stage')
    for r in checks['commands']:
        for stream in ('stdout', 'stderr'):
            p = HERE / 'logs' / (r['label'] + '.' + stream + '.log')
            need(sha(p.read_bytes()) == r[stream + '_sha256'], 'command stream digest')
    if not payload_only:
        delivery = json.loads((HERE / 'delivery.json').read_bytes())
        need(delivery['manifest_sha256'] == sha((HERE / 'MANIFEST.sha256').read_bytes()), 'delivery manifest binding')
        need(delivery['payload_files'] == count, 'payload count')
        need(set(delivery['seal_files']) == set(SEAL_FILES), 'precise seal metadata coverage')
        for name, digest in delivery['seal_files'].items():
            need(sha((HERE / name).read_bytes()) == digest, 'delivery seal digest: ' + name)
        receipt = json.loads((HERE / 'seal-checks/receipt.json').read_bytes())
        need(receipt['manifest_sha256'] == delivery['manifest_sha256'], 'receipt manifest binding')
        need(set(receipt['files']) == set(SEAL_FILES) - {'seal-checks/receipt.json'}, 'receipt exact coverage')
        for name, digest in receipt['files'].items():
            need(sha((HERE / name).read_bytes()) == digest, 'receipt digest: ' + name)
        commands = json.loads((HERE / 'seal-checks/commands.json').read_bytes())
        need([r['actual_exit'] for r in commands['commands']] == [0, 0, 2], 'actual seal exits')
        need((HERE / 'seal-checks/normal.stdout.log').read_bytes() ==
             (HERE / 'seal-checks/seed17.stdout.log').read_bytes(), 'seal seed bytes differ')
        need('payload digest differs' in (HERE / 'seal-checks/corrupt.stderr.log').read_text(), 'corrupt manifest stage')
        need(json.loads((HERE / 'seal-checks/before.json').read_bytes()) ==
             json.loads((HERE / 'seal-checks/after.json').read_bytes()), 'seal payload mutated')
    return {'task': 'N45-H1R', 'artifact_verification': 'PASS', 'payload_files': count,
            'calibration_sha256': sha((HERE / 'calibration.json').read_bytes()),
            'scope': 'artifact and fixed calibration only; no arbitrary-size machine proof or finite source'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--payload-only', action='store_true')
    parser.add_argument('--manifest', type=Path, default=HERE / 'MANIFEST.sha256')
    args = parser.parse_args()
    try:
        print(json.dumps(check(args.manifest, args.payload_only), sort_keys=True))
        return 0
    except (OSError, ValueError, KeyError, TypeError, AssertionError) as error:
        print('REJECT: ' + str(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
