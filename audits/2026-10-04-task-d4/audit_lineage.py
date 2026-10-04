#!/usr/bin/env python3
"""Check previous delivery tables and concurrent documents without accepting them."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit_bundle import NEW, digest, write
from run_validation import NAMES


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo', type=Path, default=Path('.'))
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    root, out = a.repo.resolve(), a.output.resolve()
    assert not out.exists(), 'Preserve previous attempts'
    base = json.loads((root / 'audits/2026-10-04-task-d4/baseline.json').read_text())
    prior = {}
    for name in ('d2', 'd3'):
        d = root / ('audits/2026-10-04-task-' + name)
        delivery = json.loads((d / 'DELIVERY_SHA256.json').read_text())
        rows = [dict(path=rel, recorded_sha256=v['sha256'], actual_sha256=digest(d / rel))
                for rel, v in delivery.items()]
        mismatches = [r for r in rows if r['recorded_sha256'] != r['actual_sha256']]
        prior[name] = dict(files_checked=len(rows), mismatches=mismatches,
                           rows=rows, historical_report_rewritten=False)
    d3 = json.loads((root / 'audits/2026-10-04-task-d3/baseline.json').read_text())
    concurrent = [dict(path=rel, d3_start_sha256=v['sha256'],
                       returned_baseline_sha256=base['files'].get(rel, {}).get('sha256'),
                       independently_accepted_by_hash_comparison=False)
                  for rel, v in d3['files'].items()
                  if v['sha256'] != base['files'].get(rel, {}).get('sha256')]
    old = json.loads((root / 'audits/2026-10-04-task-d2/input_hash_audit.json').read_text())
    certs = sorted({r['artifact'] for r in old['records']} |
                   {'artifacts/' + name + '/observations.json' for name in NAMES})
    records = []
    for rel in certs:
        obj = json.loads((root / rel).read_text())
        for key in ('input_sha256', 'inputs_sha256', 'scripts_sha256', 'source_sha256'):
            for dep, expected in obj.get(key, {}).items():
                actual = digest(root / dep) if (root / dep).is_file() else None
                records.append(dict(artifact=rel, map=key, path=dep,
                       recorded_sha256=expected, returned_baseline_sha256=base['files'].get(dep, {}).get('sha256'),
                       current_sha256=actual, matches=expected == actual,
                       changed_during_integration=actual != base['files'].get(dep, {}).get('sha256')))
    drift = [r for r in records if not r['matches']]
    old_pairs = {(r['artifact'], r['path'], r['recorded_sha256']) for r in old['drift']}
    current_pairs = {(r['artifact'], r['path'], r['recorded_sha256']) for r in drift}
    non_document = [r for r in drift if not r['path'].startswith(('docs/', 'README'))]
    result = dict(previous_delivery_tables=prior,
                  concurrent_existing_changes_from_d3_start=concurrent,
                  concurrent_additions_from_d3_start=sorted(set(base['files']) - set(d3['files'])),
                  certificate_count=len(certs), declared_hash_count=len(records),
                  records=records, drift=drift, non_document_drift=non_document,
                  historical_four_drift_pairs_preserved=old_pairs == current_pairs,
                  scope='All declared direct hash maps of D2 28 certificates plus returned A3/B3/C3; not whole-repository certificate validity')
    result['all_checks_passed'] = not any(v['mismatches'] for v in prior.values()) and not non_document and old_pairs == current_pairs
    write(out, result)
    print(json.dumps(dict(passed=result['all_checks_passed'], previous_deliveries={k:v['files_checked'] for k,v in prior.items()},
                         concurrent_changes=len(concurrent), certificates=len(certs), hashes=len(records), drift=len(drift))))
    assert result['all_checks_passed']


if __name__ == '__main__':
    main()
