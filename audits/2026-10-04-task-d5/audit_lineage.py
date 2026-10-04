#!/usr/bin/env python3
"""Verify preserved deliveries, historical hash drift, and artifact registration."""
import argparse
import json
from pathlib import Path
import subprocess

from audit_bundle import digest, write
from run_validation import NAMES


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path('.'))
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root, output = args.repo.resolve(), args.output.resolve()
    base = json.loads((root / 'audits/2026-10-04-task-d5/baseline.json').read_text())
    prior = {}
    for name in ('d2', 'd3', 'd4'):
        directory = root / ('audits/2026-10-04-task-' + name)
        delivery = json.loads((directory / 'DELIVERY_SHA256.json').read_text())
        rows = [{'path': rel, 'recorded_sha256': val['sha256'],
                 'actual_sha256': digest(directory / rel)} for rel, val in delivery.items()]
        prior[name] = {'files_checked': len(rows), 'mismatches': [r for r in rows
                      if r['recorded_sha256'] != r['actual_sha256']], 'rows': rows}
    old = json.loads((root / 'audits/2026-10-04-task-d2/input_hash_audit.json').read_text())
    certificates = sorted({r['artifact'] for r in old['records']} |
                          {'artifacts/' + name + '/observations.json' for name in NAMES})
    records = []
    for rel in certificates:
        payload = json.loads((root / rel).read_text())
        for key in ('input_sha256', 'inputs_sha256', 'scripts_sha256', 'source_sha256'):
            for dependency, expected in payload.get(key, {}).items():
                actual = digest(root / dependency) if (root / dependency).is_file() else None
                records.append({'artifact': rel, 'map': key, 'path': dependency,
                                'recorded_sha256': expected, 'current_sha256': actual,
                                'baseline_sha256': base['files'].get(dependency, {}).get('sha256'),
                                'matches': actual == expected})
    drift = [r for r in records if not r['matches']]
    historical = {(r['artifact'], r['path'], r['recorded_sha256']) for r in old['drift']}
    actual_drift = {(r['artifact'], r['path'], r['recorded_sha256']) for r in drift}
    old_baseline = json.loads((root / 'audits/2026-10-04-task-d4/baseline.json').read_text())
    d4_docs = json.loads((root / 'audits/2026-10-04-task-d4/document_changes.json').read_text())
    old_manifest = json.loads((root / 'audits/2026-10-04-task-d4/snapshot/artifacts/MANIFEST.json').read_text())
    manifest = json.loads((root / 'artifacts/MANIFEST.json').read_text())
    registration = []
    for name in NAMES[-1:] + (NAMES[3], NAMES[7]):
        rel = 'artifacts/' + name + '/observations.json'
        size = (root / rel).stat().st_size
        item = manifest['files'].get(rel)
        ignored = subprocess.run(['git', 'check-ignore', '--no-index', rel], cwd=root,
                                 capture_output=True, text=True)
        registration.append({'path': rel, 'bytes': size, 'sha256': digest(root / rel),
                             'manifest_entry': item, 'ignore_exit_code': ignored.returncode,
                             'ignore_stdout': ignored.stdout,
                             'correct': (item is not None and item['bytes'] == size
                                         and item['sha256'] == digest(root / rel)
                                         and ignored.returncode == 0) if size >= 1000000 else
                                        item is None and ignored.returncode == 1})
    unchanged_entries = all(manifest['files'].get(k) == v for k, v in old_manifest['files'].items())
    result = {'previous_delivery_tables': prior, 'certificate_count': len(certificates),
              'declared_hash_count': len(records), 'records': records, 'drift': drift,
              'historical_four_drift_pairs_preserved': historical == actual_drift,
              'non_document_drift': [r for r in drift if not r['path'].startswith(('docs/', 'README'))],
              'changes_since_d4_capture': [{'path': p, 'd4_capture_sha256': v['sha256'],
                                          'd5_capture_sha256': base['files'].get(p, {}).get('sha256')}
                                         for p, v in old_baseline['files'].items()
                                         if v != base['files'].get(p)],
              'd4_document_changes_metadata': d4_docs,
              'manifest_existing_entries_preserved': unchanged_entries,
              'manifest_added_paths_since_d4': sorted(set(manifest['files']) - set(old_manifest['files'])),
              'new_artifact_registration': registration,
              'scope': 'D2 28 direct-map certificates plus A3/B3/C3 and A4/B4/C4; historical drift retained, not repaired'}
    result['all_checks_passed'] = (not any(v['mismatches'] for v in prior.values())
                                  and historical == actual_drift and not result['non_document_drift']
                                  and unchanged_entries and all(r['correct'] for r in registration))
    write(output, result)
    print(json.dumps({'passed': result['all_checks_passed'], 'certificates': len(certificates),
                      'hash_records': len(records), 'historical_document_drift': len(drift),
                      'previous_deliveries': {k: v['files_checked'] for k, v in prior.items()}}))
    assert result['all_checks_passed']


if __name__ == '__main__':
    main()
