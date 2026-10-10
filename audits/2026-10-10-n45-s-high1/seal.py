#!/usr/bin/env python3
"""Exact payload inventory and delivery/receipt binding; artifact scope only."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
EXCLUDED = {'manifest.json', 'delivery.json', 'receipt.json'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def inventory():
    files = []
    for path in sorted(HERE.rglob('*')):
        require(not path.is_symlink(), 'symlink in payload: ' + str(path))
        if path.is_file():
            rel = path.relative_to(HERE).as_posix()
            if rel not in EXCLUDED:
                files.append({'path': rel, 'sha256': sha(path), 'bytes': path.stat().st_size})
    return files


def payload(path):
    doc = json.loads(sys.stdin.read()) if path is None else json.loads(path.read_bytes())
    require(doc['task'] == 'N45-S-HIGH1', 'manifest task identity')
    require(doc['excluded_exact_top_level'] == sorted(EXCLUDED), 'exact exclusions')
    current = inventory()
    saved_names = {x['path'] for x in doc['payload']}
    current_names = {x['path'] for x in current}
    require(doc['payload'] == current, 'payload inventory/hash mismatch; missing=' + repr(sorted(current_names - saved_names)) + '; extra=' + repr(sorted(saved_names - current_names)))
    return doc


def delivery(receipt_path):
    doc = json.loads((HERE / 'delivery.json').read_bytes())
    require(doc['task'] == 'N45-S-HIGH1' and doc['paper_status'] == 'candidate pending independent adoption', 'delivery identity/scope')
    require(doc['manifest_sha256'] == sha(HERE / 'manifest.json'), 'manifest metadata binding')
    require(doc['receipt_sha256'] == sha(receipt_path), 'receipt metadata binding')
    require(doc['excluded_exact_top_level'] == sorted(EXCLUDED), 'delivery exclusion binding')
    manifest = payload(HERE / 'manifest.json')
    receipt = json.loads(receipt_path.read_bytes())
    require(receipt['manifest_sha256'] == doc['manifest_sha256'], 'receipt manifest identity')
    require(receipt['task'] == doc['task'], 'receipt task identity')
    require(receipt['input_index_sha256'] == sha(HERE / 'inputs.json'), 'receipt input index binding')
    require(receipt['certificate_sha256'] == sha(HERE / 'certificate.json'), 'receipt certificate binding')
    checks = json.loads((HERE / 'checks-final.json').read_bytes())
    require(receipt['checks_sha256'] == sha(HERE / 'checks-final.json'), 'receipt checks binding')
    require(receipt['logs'] == checks['runs'], 'receipt exact command/log coverage')
    require(receipt['payload_check_normal']['exit'] == 0 and receipt['payload_check_seed17']['exit'] == 0, 'payload replay exits')
    require(receipt['payload_check_normal']['stdout'] == receipt['payload_check_seed17']['stdout'], 'payload replay agreement')
    for name, environment in [('payload_check_normal', {}), ('payload_check_seed17', {'PYTHONHASHSEED': '17'})]:
        run = receipt[name]
        require(run['command'] == ['python3', '-B', 'audits/2026-10-10-n45-s-high1/seal.py', '--check-payload'], 'payload replay command')
        require(run['cwd'] == str(HERE.parents[1]), 'payload replay cwd')
        require(run['environment'] == environment and run['stderr'] == '', 'payload replay environment/stderr')
    expected = {'normal', 'seed17', 'bad-certificate', 'bad-input-index', 'exclusive-create',
                'local-links-whitespace', 'git-diff-check', 'check-docs-current',
                'docgraph-formal', 'docgraph-whole', 'input-custody',
                'bad-manifest-nested-omission'}
    require({r['id'] for r in checks['runs']} == expected, 'required actual log coverage')
    for run in checks['runs']:
        for stream in ('stdout', 'stderr'):
            require(sha(HERE / run[stream + '_file']) == run[stream + '_sha256'], 'command log binding')
        require(run['actual_exit'] == run['expected_exit'], 'unexpected check exit: ' + run['id'])
    normal = next(r for r in checks['runs'] if r['id'] == 'normal')
    seeded = next(r for r in checks['runs'] if r['id'] == 'seed17')
    require(normal['stdout_sha256'] == seeded['stdout_sha256'] and normal['stderr_sha256'] == seeded['stderr_sha256'], 'checker seed byte agreement')
    require(seeded['environment'].get('PYTHONHASHSEED') == '17', 'seed environment')
    require(doc['payload_files'] == len(manifest['payload']), 'delivery payload count')
    return doc


def main():
    p = argparse.ArgumentParser(description=__doc__)
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument('--check-payload', action='store_true')
    group.add_argument('--check-delivery', action='store_true')
    p.add_argument('--manifest', type=Path, default=HERE / 'manifest.json')
    p.add_argument('--manifest-stdin', action='store_true')
    p.add_argument('--receipt', type=Path, default=HERE / 'receipt.json')
    args = p.parse_args()
    stage = 'payload inventory' if args.check_payload else 'delivery/receipt exact binding'
    try:
        if args.check_payload:
            doc = payload(None if args.manifest_stdin else args.manifest)
            count = len(doc['payload'])
        else:
            count = delivery(args.receipt)['payload_files']
        print(json.dumps({'status': 'PASS: artifact custody only', 'payload_files': count,
                          'exact_top_level_exclusions': sorted(EXCLUDED)}, sort_keys=True))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as e:
        print(json.dumps({'status': 'REJECT', 'stage': stage, 'reason': str(e)}, sort_keys=True), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
