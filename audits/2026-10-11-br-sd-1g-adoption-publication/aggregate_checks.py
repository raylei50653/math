#!/usr/bin/env python3
"""Collect captured receipts without changing original execution results."""
import hashlib
import json
from pathlib import Path

AUDIT = Path(__file__).resolve().parent
ROOT = AUDIT.parents[1]
BASE = 'c15a635e17d4be814e19aeeeeb765f3d6024099a'

def main():
    if (AUDIT / 'SEAL.json').exists() or (AUDIT / 'proof/ACCEPTANCE.json').exists():
        raise SystemExit('final review/seal exists; aggregate is immutable')
    successful, failures = [], []
    for path in sorted((AUDIT / 'logs').glob('*/receipt.json')):
        row = json.loads(path.read_text())
        for kind in ('stdout', 'stderr'):
            actual = hashlib.sha256((ROOT / row[kind + '_path']).read_bytes()).hexdigest()
            if actual != row[kind + '_sha256']:
                raise SystemExit('receipt drift: ' + str(path))
        row['receipt_path'] = str(path.relative_to(ROOT))
        row['receipt_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
        (successful if row['exit_code'] == row['expected_exit_code'] else failures).append(row)
    permitted_failures = {'docs', 'logger-controls'}
    if {r['name'] for r in failures} - permitted_failures:
        raise SystemExit('unresolved command failure')
    if failures and not any(r['name'] == 'docs-final' and r['exit_code'] == 0 for r in successful):
        raise SystemExit('documentation retry has not passed')
    for row in failures:
        row['superseded_by'] = row['name'] + '-final'
        row['superseded_reason'] = ('First check ran before mapping/REVIEW.md was delivered; identical command passed after delivery.'
                                    if row['name'] == 'docs' else
                                    'Disposable positive fixture omitted its required logs parent; original harness retained as logs/logger-controls/harness.v1.py; corrected harness passed.')
        if not any(r['name'] == row['superseded_by'] and r['argv'] == row['argv'] and r['exit_code'] == 0 for r in successful):
            raise SystemExit('retained failure has no successful identical-command retry: ' + row['name'])
    for prefix in ('fresh-finite', 'old-independent', 'old-primary', 'mapping-degrees'):
        rows = [r for r in successful if r['name'].startswith(prefix + '-')]
        if len(rows) != 2 or rows[0]['stdout_sha256'] != rows[1]['stdout_sha256']:
            raise SystemExit('normal/seed17 drift or missing pair: ' + prefix)
    result = dict(schema='br-sd-1g-adoption-checks-v1', base=BASE,
                  commands=successful, retained_failed_commands=failures,
                  all_final_expectations_met=True, parent_status='OPEN',
                  actual_source_status='not triggered', new_Lean_theorem=False,
                  new_unconditional_closures=0,
                  scope='Exact scoped adoption, named synthetic controls, docs and immutable custody; no source realization',
                  historical_publication_exception='exit1 immutable two-directory whitelist; preserved, not PASS',
                  postseal_receipt_location='External /tmp session receipts; sealed bytes unchanged')
    (AUDIT / 'CHECKS.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'successful_or_expected': len(successful), 'retained_failures': len(failures)}, sort_keys=True))

if __name__ == '__main__':
    main()
