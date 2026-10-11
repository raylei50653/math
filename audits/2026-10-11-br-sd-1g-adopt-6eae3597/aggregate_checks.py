#!/usr/bin/env python3
"""Aggregate only this round's root receipts; preserve prior failures separately."""
import hashlib
import json
from pathlib import Path

AUDIT = Path(__file__).resolve().parent
commands = []
retained_failed = []
superseded = {'audit-precheck-v1': 'Exit1: planned ROOT_TOOL_REVIEW.md had not yet been delivered; superseded only after actual v2 precheck passes.'}
for path in sorted((AUDIT / 'logs').glob('*.json')):
    record = json.loads(path.read_text())
    if isinstance(record, dict) and {'argv', 'exit_code', 'expected_exit_code', 'stdout_path', 'stderr_path'} <= set(record):
        enriched = record | {'receipt_path': path.relative_to(AUDIT).as_posix(),
                             'receipt_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
        if record['exit_code'] != record['expected_exit_code'] and path.stem in superseded:
            retained_failed.append(enriched | {'superseded_reason': superseded[path.stem]})
        else:
            commands.append(enriched)
value = {
    'schema': 'br-sd-1g-adopt-checks-v1',
    'base': 'c15a635e17d4be814e19aeeeeb765f3d6024099a',
    'scope': 'enumerated current root validation commands; preliminary failures and worker receipts are separate',
    'all_recorded_expectations_met': all(r['exit_code'] == r['expected_exit_code'] for r in commands),
    'commands': commands,
    'retained_failed_commands': retained_failed,
    'worker_receipt_manifests': ['agents/proof/READS.json', 'agents/proof/FETCH_REPLAY.json',
                                 'agents/mapping/READS.json', 'agents/mapping/CHECKS.json',
                                 'agents/custody/final-v2-COMMAND_RECEIPTS.json',
                                 'agents/custody/METADATA_RECEIPTS.json'],
    'retained_failure_evidence': ['logs/bootstrap-failures.txt',
                                  'agents/custody/COMMAND_RECEIPTS.json',
                                  'agents/proof/READS.json'],
    'historical_checker_exceptions': {
        'publication_normal_hashseed17': {'actual_exit_code': 1, 'classification': 'authorized new audit outside historical write whitelist',
                                          'receipt_manifest': 'agents/custody/final-v2-COMMAND_RECEIPTS.json'},
        'original_fresh': {'actual_exit_code': 1, 'classification': 'historical fresh BASE differs from fixed task HEAD',
                            'receipt_manifest': 'agents/custody/final-v2-COMMAND_RECEIPTS.json'}},
    'postseal_receipts': 'DELIVERY.json binds five exact command/env/exit0 receipts and independent reviewer readback',
    'actual_source_status': 'not triggered', 'new_Lean_theorem': False,
    'decision': 'ACCEPTABLE', 'formal_adoption_executed': False,
    'parent_status': 'OPEN', 'new_unconditional_closures': 0,
}
(AUDIT / 'CHECKS.json').write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')
print(json.dumps({'root_checks': len(commands), 'expectations_met': value['all_recorded_expectations_met']}, sort_keys=True))
