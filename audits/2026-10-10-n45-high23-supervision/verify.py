#!/usr/bin/env python3
"""Read-only validation of sealed evidence and the permitted adoption state.

This checks artifact custody and actual receipts; it does not prove the paper.
Original current-origin pins are intentionally not reinterpreted after adoption.
"""
import argparse
import hashlib
import json
from pathlib import Path
import stat
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
AUDIT = 'N45-HIGH23-SUPERVISION'
META = {'manifest.json', 'delivery.json', 'receipt.json'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def require(value, message):
    if not value:
        raise ValueError(message)


def read(path):
    return json.loads(path.read_text())


def inventory(path, exclusions=()):
    result = {}
    for p in sorted(path.rglob('*')):
        if p.is_dir() and not p.is_symlink():
            continue
        relative = p.relative_to(path).as_posix()
        if relative in exclusions:
            continue
        require(p.is_file() and not p.is_symlink(), 'unexpected nonregular file: '+relative)
        data = p.read_bytes()
        result[relative] = {'kind': 'regular', 'bytes': len(data),
                            'mode': stat.S_IMODE(p.stat().st_mode), 'sha256': sha(data)}
    return result


def verify_manifest(manifest):
    require(manifest['audit_id'] == AUDIT, 'manifest audit ID')
    require(manifest['exact_top_level_metadata_exclusions'] == sorted(META), 'exact metadata exclusion set')
    actual = inventory(HERE, META)
    require(manifest['payload'] == actual, 'immutable payload inventory/hash/mode mismatch; nested metadata remains payload')


def verify_trees():
    for name, key in [('intake.json', 'workers'), ('reviewer-intake.json', 'reviews')]:
        for path, info in read(HERE/name)[key].items():
            require(inventory(ROOT/path) == info['fulltree'], 'original immutable tree drift: '+path)
            require(inventory(HERE/info['frozen']) == info['fulltree'], 'frozen fulltree drift: '+path)
    return sum(len(info['fulltree']) for name, key in [('intake.json', 'workers'), ('reviewer-intake.json', 'reviews')] for info in read(HERE/name)[key].values())


def verify_documentation():
    state = read(HERE/'documentation-state.json')
    for path, info in state['after'].items():
        data = (ROOT/path).read_bytes()
        require(sha(data) == info['sha256'] and len(data) == info['bytes'], 'adopted document drift: '+path)
    for path, info in state['reviewed_unchanged'].items():
        require(sha((ROOT/path).read_bytes()) == info['sha256'], 'reviewed route changed: '+path)
    for path in state['shared_before']:
        require((HERE/'draft'/path).read_bytes() == (ROOT/path).read_bytes(), 'reviewed draft/adopted document mismatch: '+path)
    return len(state['after'])


def verify_actual_replays():
    first = read(HERE/'initial-replays.json')['actual_commands']
    for run in first:
        require(run['exit'] == 0, 'initial actual replay failed')
        for channel in ['stdout', 'stderr']:
            path = HERE/'logs'/(run['name']+'.'+channel+'.txt')
            require(sha(path.read_bytes()) == run[channel+'_sha256'], 'initial actual stream binding')
    for a, b in zip(first[::2], first[1::2]):
        require(a['stdout_sha256'] == b['stdout_sha256'] and a['stderr_sha256'] == b['stderr_sha256'], 'initial seed comparison')
    second = read(HERE/'reviewer-parent-replays.json')['runs']
    for run in second:
        require(run['exit_code'] == 0, 'reviewer actual replay failed')
        for channel in ['stdout', 'stderr']:
            require(sha((HERE/run[channel]).read_bytes()) == run[channel+'_sha256'], 'reviewer actual stream binding')
    for a, b in zip(second[::2], second[1::2]):
        require(a['stdout_sha256'] == b['stdout_sha256'] and a['stderr_sha256'] == b['stderr_sha256'], 'reviewer seed comparison')
    require(len(first) == 10 and len(second) == 6, 'exact pre-adoption replay count')
    return len(first)+len(second)


def verify_boundaries():
    decision = read(HERE/'acceptance.json')
    require(decision['authority'] == 'parent scoped adoption', 'acceptance authority')
    require(len(decision['HIGH2']['full_H1_H13']) == 13 and len(decision['HIGH2']['claims']) == 12, 'complete HIGH2 domain')
    require(decision['HIGH2']['raw_all_twelve_PASS'] is False, 'raw quantifier finding retained')
    require(decision['HIGH2']['qualification_changes_source_domain'] is False, 'no source premise added')
    require(decision['HIGH3']['adopted'] is True and decision['coverage']['adopted'] is True, 'scoped conclusion adoption')
    require(decision['artifact_acceptance']['new_finite_source'] is False and decision['artifact_acceptance']['new_Lean'] is False, 'source and Lean boundaries')
    checks = read(HERE/'documentation-checks.json')
    require(checks['status'] == 'actual checks recorded', 'documentation checks unfinished')
    for run in checks['executions']:
        for channel in ['stdout', 'stderr']:
            require(sha((HERE/run[channel]).read_bytes()) == run[channel+'_sha256'], 'documentation actual stream binding')
        require(run['exit_code'] == run['expected_exit'], 'unexpected documentation check result: '+run['name'])
    require(checks['whole_docgraph_duplicate_ids'] == 62, 'known global duplicate count preserved')


def verify_delivery_if_present():
    if not (HERE/'delivery.json').exists():
        return
    delivery = read(HERE/'delivery.json')
    require(delivery['audit_id'] == AUDIT, 'delivery audit ID')
    manifest_sha = sha((HERE/'manifest.json').read_bytes())
    require(delivery['manifest_sha256'] == manifest_sha, 'delivery manifest binding')
    require(delivery['receipt_sha256'] == sha((HERE/'receipt.json').read_bytes()), 'delivery receipt binding')
    require(delivery['verifier_sha256'] == sha((HERE/'verify.py').read_bytes()), 'delivery verifier binding')
    receipt = read(HERE/'receipt.json')
    require(receipt['manifest_sha256'] == manifest_sha and receipt['verifier_sha256'] == delivery['verifier_sha256'], 'receipt manifest/verifier binding')
    runs = receipt['executions']
    require([r['name'] for r in runs] == ['normal', 'seed17', 'negative-nested-omission'], 'exact parent receipt execution set')
    for run in runs:
        require(sha(run['stdout'].encode()) == run['stdout_sha256'] and sha(run['stderr'].encode()) == run['stderr_sha256'], 'parent receipt stream binding')
        require(run['exit_code'] == (2 if run['name'].startswith('negative') else 0), 'parent actual exit')
    require(runs[0]['stdout'] == runs[1]['stdout'] and runs[0]['stderr'] == runs[1]['stderr'], 'parent seed comparison')
    require(runs[2]['stdin_sha256'] == sha(runs[2]['stdin'].encode()), 'negative formal manifest binding')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest-stdin', action='store_true', help='Read a formal inventory probe from stdin without any mutation')
    args = parser.parse_args()
    try:
        manifest = json.load(sys.stdin) if args.manifest_stdin else read(HERE/'manifest.json')
        verify_manifest(manifest)
        base = read(HERE/'intake.json')['BASE']
        require(subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip() == base, 'BASE head changed')
        files = verify_trees()
        documents = verify_documentation()
        commands = verify_actual_replays()
        verify_boundaries()
        verify_delivery_if_present()
        print(json.dumps({'audit_id': AUDIT, 'status': 'scoped adoption artifact checks hold',
                          'original_and_frozen_regular_files': files, 'adopted_documents': documents,
                          'pre_adoption_commands': commands, 'new_finite_source': False,
                          'new_Lean': False, 'whole_worktree_custody': 'not claimed'}, sort_keys=True))
    except (ValueError, KeyError, OSError, AssertionError, subprocess.CalledProcessError) as exc:
        print('REJECT: '+str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
