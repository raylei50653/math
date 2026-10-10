#!/usr/bin/env python3
"""Read-only verification of this independent audit and its frozen worker."""
import argparse
import json
from pathlib import Path
import sys

import checker

HERE = Path(__file__).resolve().parent
LOGS = {f'receipt/{name}.{stream}.log' for name in ('normal', 'seed17') for stream in ('stdout', 'stderr')}
EXCLUDED = {'MANIFEST.sha256', 'delivery.json', 'receipt.json'} | LOGS


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--payload-only', action='store_true')
    args = parser.parse_args()
    try:
        files, links = checker.inventory(HERE, EXCLUDED)
        checker.require(not links, 'reviewer unexpected symlink')
        records = checker.manifest_records(HERE / 'MANIFEST.sha256')
        checker.require(sorted(records) == files, 'reviewer exact payload inventory differs')
        for relative, digest in records.items():
            checker.require(checker.digest(HERE / relative) == digest, 'reviewer payload digest differs: ' + relative)
        inputs = checker.check_full_capture()
        checker.check_worker_manifest(checker.WORKER / 'MANIFEST.sha256')
        checker.check_frozen_inputs(inputs)
        checker.check_coverage()
        checker.check_receipt(checker.WORKER / 'receipt.json')
        checks = checker.read(HERE / 'checks.json')
        expected_names = ['normal', 'seed17'] + list(checker.STAGES) + ['missing-nested-receipt']
        checker.require([r['name'] for r in checks['commands']] == expected_names, 'reviewer control names differ')
        for run in checks['commands']:
            expected = 0 if run['name'] in ('normal', 'seed17') else 2
            checker.require(run['actual_exit_code'] == run['expected_exit_code'] == expected, 'reviewer actual exit differs')
            if expected == 2:
                checker.require(run['stage_matches'] is True and run['expected_rejection_stage'] in
                                (HERE / run['stderr']).read_text(), 'reviewer negative stage differs')
        checker.require((HERE / 'checks/normal.stdout.log').read_bytes() ==
                        (HERE / 'checks/seed17.stdout.log').read_bytes(), 'reviewer normal/seed stdout differs')
        judgment = checker.read(HERE / 'independent-judgment.json')
        checker.require(judgment['tool_verdict'] == 'ACCEPT_SCOPED_ARTIFACT_INTEGRITY' and
                        judgment['mathematical_verdict'] == 'not evaluated by this audit', 'judgment scope differs')
        if not args.payload_only:
            delivery = checker.read(HERE / 'delivery.json')
            checker.require(delivery['excluded_exact_paths'] == sorted(EXCLUDED), 'reviewer excluded paths differ')
            checker.require(delivery['manifest_sha256'] == checker.digest(HERE / 'MANIFEST.sha256'), 'reviewer manifest binding differs')
            checker.require(delivery['receipt_sha256'] == checker.digest(HERE / 'receipt.json'), 'reviewer receipt binding differs')
            checker.require(delivery['payload_regular_files'] == len(records) and delivery['payload_symlinks'] == 0,
                            'reviewer payload counts differ')
            receipt = checker.read(HERE / 'receipt.json')
            checker.require(set(receipt['metadata']) == LOGS, 'reviewer receipt exact log inventory differs')
            for relative, digest in receipt['metadata'].items():
                checker.require(checker.digest(HERE / relative) == digest, 'reviewer receipt log digest differs')
            checker.require([r['name'] for r in receipt['commands']] == ['normal', 'seed17'], 'reviewer seal run names differ')
            checker.require(all(r['exit_code'] == 0 for r in receipt['commands']), 'reviewer seal exit differs')
            checker.require((HERE / 'receipt/normal.stdout.log').read_bytes() ==
                            (HERE / 'receipt/seed17.stdout.log').read_bytes(), 'reviewer seal stdout differs')
            checker.require(receipt['payload_before'] == receipt['payload_after'] == delivery['manifest_sha256'],
                            'reviewer readonly payload identity differs')
        print(json.dumps({'status': 'independent_audit_integrity_holds', 'payload_regular_files': len(records),
                          'payload_symlinks': 0, 'own_receipt_checked': not args.payload_only,
                          'frozen_worker_regular_files': 85, 'worker_payload_files': 66,
                          'tool_verdict': 'ACCEPT_SCOPED_ARTIFACT_INTEGRITY',
                          'mathematical_verdict': 'not evaluated by this audit',
                          'source_controls': 'not established; not executed; no trigger count'}, sort_keys=True))
    except (OSError, ValueError, KeyError) as error:
        print('reviewer integrity rejection: ' + str(error), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
