#!/usr/bin/env python3
"""Freeze D3 inputs and verify preservation without refreshing old certificates."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess


PREFIX = 'audits/2026-10-04-task-d3'
INPUTS = (
    'scripts/c5_mixed_p3_common_endpoint.py',
    'scripts/c5_mixed_p3_one_color_ternary_unary.py',
    'scripts/c5_mixed_capacity_contacts.py',
    'scripts/c5_adjacent_degree5_interfaces.py',
    'artifacts/c5_mixed_p3_common_endpoint/observations.json',
    'artifacts/c5_mixed_p3_common_endpoint/rotation_controls.json',
    'artifacts/c5_mixed_p3_one_color_ternary_unary/observations.json',
    'artifacts/c5_mixed_capacity_contacts/observations.json',
    'docs/c5_mixed_p3_common_endpoint.md',
    'docs/c5_mixed_p3_one_color_ternary_unary.md',
    'docs/c5_weak_deletion_guide.md',
    'docs/c5_kempe_guide.md',
    'docs/HANDOFF.md', 'docs/STATUS.md', 'docs/DOCUMENTATION.md',
    'audits/2026-10-04-task-d/REPORT.md',
    'audits/2026-10-04-task-d2/REPORT.md',
    'audits/2026-10-04-task-d2/FINAL_STATE.json',
    'audits/2026-10-04-task-d2/DELIVERY_SHA256.json',
    'audits/2026-10-04-task-d2/input_hash_audit.json',
)


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def git(root, *args):
    return subprocess.check_output(['git', *args], cwd=root, text=True).strip()


def inventory(root):
    paths = [root / 'README.md', root / '.gitignore']
    for name in ('docs', 'scripts', 'tools', 'artifacts', 'audits'):
        paths.extend((root / name).rglob('*'))
    return {
        str(p.relative_to(root)): dict(sha256=digest(p), size=p.stat().st_size)
        for p in sorted(set(paths))
        if p.is_file() and '__pycache__' not in p.parts
        and p.suffix != '.pyc' and not str(p.relative_to(root)).startswith(PREFIX + '/')
    }


def capture(root, out):
    target = out / 'baseline.json'
    assert not target.exists(), 'Refusing to replace a captured baseline'
    current = inventory(root)
    d2 = root / 'audits/2026-10-04-task-d2'
    expected = json.loads((d2 / 'baseline.json').read_text())['files']
    for row in json.loads((d2 / 'integrity_results.json').read_text())['changed_baseline_files']:
        expected[row['path']] = dict(sha256=row['after_sha256'])
    expected.update(json.loads((d2 / 'successor_baseline_final.json').read_text())['new_files'])
    mismatches = [dict(path=p, d2_sha256=v['sha256'], current_sha256=current.get(p, {}).get('sha256'))
                  for p, v in expected.items() if current.get(p, {}).get('sha256') != v['sha256']]
    delivery = json.loads((d2 / 'DELIVERY_SHA256.json').read_text())
    delivery_mismatches = [p for p, v in delivery.items() if digest(d2 / p) != v['sha256']]
    for rel in INPUTS:
        dst = out / 'snapshot' / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root / rel, dst)
    write(target, dict(timestamp_utc=datetime.now(timezone.utc).isoformat(),
                       head=git(root, 'rev-parse', 'HEAD'),
                       tracking_head=git(root, 'rev-parse', 'origin/main'),
                       git_status=git(root, 'status', '--short'), files=current,
                       input_paths=list(INPUTS), d2_expected_file_count=len(expected),
                       d2_final_snapshot_mismatches=mismatches,
                       d2_delivery_files_checked=len(delivery),
                       d2_delivery_mismatches=delivery_mismatches))
    print(json.dumps(dict(files=len(current), frozen_inputs=len(INPUTS),
                          d2_files_compared=len(expected), d2_snapshot_mismatches=len(mismatches),
                          d2_delivery_mismatches=len(delivery_mismatches))))
    assert not mismatches and not delivery_mismatches


def verify(root, out, destination, scope):
    assert not destination.exists(), 'Choose a fresh result path to retain prior attempts'
    baseline = json.loads((out / 'baseline.json').read_text())
    current = inventory(root)
    changes = [dict(path=p, before_sha256=v['sha256'], after_sha256=current.get(p, {}).get('sha256'))
               for p, v in baseline['files'].items() if current.get(p, {}).get('sha256') != v['sha256']]
    additions = sorted(set(current) - set(baseline['files']))
    frozen_changes = [p for p in INPUTS if digest(out / 'snapshot' / p) != baseline['files'][p]['sha256']]
    direct_hashes = []
    for rel in INPUTS:
        if not rel.startswith('artifacts/') or not rel.endswith('.json'):
            continue
        obj = json.loads((out / 'snapshot' / rel).read_text())
        for key in ('scripts_sha256', 'input_sha256', 'inputs_sha256', 'source_sha256'):
            for dep, expected in obj.get(key, {}).items():
                actual = digest(root / dep) if (root / dep).is_file() else None
                direct_hashes.append(dict(artifact=rel, map=key, path=dep,
                                          recorded_sha256=expected, current_sha256=actual,
                                          matches=expected == actual))
    historical = json.loads((root / 'audits/2026-10-04-task-d2/input_hash_audit.json').read_text())
    historical_drift = []
    for row in historical['drift']:
        actual = digest(root / row['path'])
        historical_drift.append(dict(artifact=row['artifact'], path=row['path'],
                                     recorded_sha256=row['recorded_sha256'],
                                     d2_current_sha256=row['d2_after_sha256'],
                                     current_sha256=actual, remains_drifted=actual != row['recorded_sha256'],
                                     unchanged_since_d2=actual == row['d2_after_sha256']))
    head = git(root, 'rev-parse', 'HEAD')
    tracking = git(root, 'rev-parse', 'origin/main')
    protected = [p for p in baseline['files'] if p != 'artifacts/MANIFEST.json'
                 and p.startswith(('scripts/', 'tools/', 'artifacts/', 'docs/history/', 'audits/'))]
    protected_changes = [r for r in changes if r['path'] in protected]
    manifest_before = json.loads((out / 'baseline_control_files/artifacts/MANIFEST.json').read_text())
    manifest_after = json.loads((root / 'artifacts/MANIFEST.json').read_text())
    manifest_changed_existing = [p for p, v in manifest_before['files'].items()
                                 if manifest_after['files'].get(p) != v]
    manifest_added = sorted(set(manifest_after['files']) - set(manifest_before['files']))
    passed = not frozen_changes and all(r['matches'] for r in direct_hashes)
    passed &= not protected_changes and not manifest_changed_existing
    if scope == 'strict':
        passed &= not changes
    passed &= head == baseline['head'] and tracking == baseline['tracking_head']
    passed &= all(r['remains_drifted'] and r['unchanged_since_d2'] for r in historical_drift)
    result = dict(timestamp_utc=datetime.now(timezone.utc).isoformat(), all_checks_passed=passed,
                  verification_scope=scope, strict_baseline_unchanged=not changes,
                  baseline_file_count=len(baseline['files']), changed_existing_files=changes,
                  protected_file_count=len(protected), changed_protected_files=protected_changes,
                  manifest_changed_existing_entries=manifest_changed_existing,
                  manifest_added_entries=manifest_added,
                  added_files_outside_d3=additions, frozen_input_changes=frozen_changes,
                  direct_input_hashes=direct_hashes, historical_hash_drift_preserved=historical_drift,
                  head_before=baseline['head'], head_after=head,
                  tracking_head_before=baseline['tracking_head'], tracking_head_after=tracking,
                  shared_document_sync_performed=False, committed_by_d3=False, pushed_by_d3=False,
                  scope='Existing file bytes and local Git refs; outside-D3 concurrent document/control changes are recorded, not adopted; no remote fetch or historical checker rerun')
    write(destination, result)
    print(json.dumps(dict(all_checks_passed=passed, baseline_files=len(baseline['files']),
                          changes=len(changes), frozen_input_changes=len(frozen_changes),
                          direct_hashes=len(direct_hashes), historical_drift=len(historical_drift),
                          protected_changes=len(protected_changes), strict_baseline_unchanged=not changes,
                          additions_outside_d3=len(additions))))
    assert passed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('capture', 'verify'))
    parser.add_argument('--repo', type=Path, default=Path('.'))
    parser.add_argument('--output', type=Path)
    parser.add_argument('--result', type=Path)
    parser.add_argument('--scope', choices=('strict', 'protected'), default='strict')
    args = parser.parse_args()
    root = args.repo.resolve()
    out = args.output.resolve() if args.output else root / PREFIX
    if args.action == 'capture':
        capture(root, out)
    else:
        verify(root, out, args.result or out / 'integrity_results.json', args.scope)


if __name__ == '__main__':
    main()
