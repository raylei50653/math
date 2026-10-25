#!/usr/bin/env python3
"""Read-only publication custody audit for the three finite four-color bundles.

Writes only the explicitly supplied result path; never changes repository files.
This checks saved evidence custody and closure, not solver completeness or speed.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import shlex
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    errors = []
    checks = Counter()
    snapshot_paths = set()
    baseline_optimized_paths = set()
    incremental_paths = set()
    record_paths = set()
    worker_paths = set()
    bundles = []

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def check(path, expected, kind):
        checks[kind] += 1
        if not path.is_file():
            errors.append({'kind': 'missing_file', 'path': str(path.relative_to(root))})
        elif digest(path) != expected:
            errors.append({'kind': 'sha256_mismatch', 'path': str(path.relative_to(root))})

    def snapshot(path, expected, kind):
        check(path, expected, kind)
        snapshot_paths.add(path)
        if 'incremental-source' in path.parts:
            incremental_paths.add(path)
        else:
            baseline_optimized_paths.add(path)

    for name in ['four_color_flow_optimization', 'four_color_memory_optimization',
                 'four_color_ram_indexes']:
        bundle = root / 'artifacts' / name
        verification = json.loads((bundle / 'verification.json').read_text())
        baseline = json.loads((bundle / 'baseline-manifest.json').read_text())
        before = len(snapshot_paths)
        for rel, sha in baseline.get('source_sha256', baseline.get('sources', {})).items():
            snapshot(bundle / 'baseline-source' / rel, sha, 'baseline_snapshot_bindings')
        for rel, sha in verification['source_sha256'].items():
            snapshot(bundle / 'optimized-source' / rel, sha, 'optimized_snapshot_bindings')
        for key, base in [('full_record_sha256', bundle),
                          ('complete_record_sha256', bundle / 'comparison')]:
            for rel, sha in verification.get(key, {}).items():
                check(base / rel, sha, 'receipt_record_hash_bindings')
        for rel, sha in verification['documentation_checks']['logs_sha256'].items():
            check(bundle / rel, sha, 'documentation_log_hash_bindings')
        check(bundle / 'tests.log', verification['tests']['log_sha256'], 'test_log_hash_bindings')
        if 'comparison_report_sha256' in verification:
            check(bundle / 'comparison/report.json', verification['comparison_report_sha256'],
                  'comparison_report_hash_bindings')
        if 'timings_sha256' in verification:
            check(bundle / 'comparison/timings.json', verification['timings_sha256'],
                  'timings_hash_bindings')
        for rel, phase in verification.get('phase_summaries', {}).items():
            check(bundle / rel / 'report.json', phase['report_sha256'], 'phase_report_hash_bindings')

        if name == 'four_color_flow_optimization':
            check(bundle / 'prior-inputs.json', baseline['frozen_input_sha256'], 'input_hash_bindings')
            check(bundle / 'prior-report.json', baseline['prior_report_sha256'], 'prior_report_hash_bindings')
            reports = [bundle / phase / 'report.json'
                       for phase in ['baseline', 'incremental', 'optimized']]
        else:
            check(bundle / 'inputs.json', baseline['inputs_sha256'], 'input_hash_bindings')
            check(root / baseline['prior_report'], baseline['prior_report_sha256'], 'prior_report_hash_bindings')
            reports = [bundle / 'comparison/report.json']

        for report_path in reports:
            report = json.loads(report_path.read_text())
            check(report_path.parent / report['input_file'], report['inputs_sha256'],
                  'report_input_hash_bindings')
            check(report_path.parent / report['baseline_manifest_file'], report['baseline_manifest_sha256'],
                  'report_manifest_hash_bindings')
            if name == 'four_color_flow_optimization':
                for rel, sha in report['sources'].items():
                    snapshot(bundle / (report_path.parent.name + '-source') / rel,
                             sha, 'flow_phase_snapshot_bindings')
            else:
                # source_hashes excludes the executing flow driver, whose hash
                # is stored separately in the report and included in receipts.
                bound_sources = dict(report['sources'])
                bound_sources['scripts/four_color_flow_experiment.py'] = report['driver_sha256']
                checks['report_source_receipt_bindings'] += 1
                if bound_sources != verification['source_sha256']:
                    errors.append({'kind': 'report_receipt_sources_mismatch',
                                   'path': str(report_path.relative_to(root))})
            for case in report['cases']:
                for result in case['results'].values():
                    record_path = report_path.parent / result['full_record']
                    check(record_path, result['compressed_record_sha256'], 'report_record_hash_bindings')
                    try:
                        json.loads(gzip.decompress(record_path.read_bytes()))
                    except (OSError, EOFError, ValueError) as error:
                        errors.append({'kind': 'gzip_json_integrity',
                                       'path': str(record_path.relative_to(root)),
                                       'error': str(error)})
                    checks['gzip_json_integrity'] += 1
                    record_paths.add(record_path)
                    if 'worker_report' in result:
                        worker_path = report_path.parent / result['worker_report']
                        check(worker_path, result['worker_report_sha256'], 'worker_report_hash_bindings')
                        worker_paths.add(worker_path)

        represented = {path for path in snapshot_paths if path.is_relative_to(bundle)}
        discovered = {path for directory in bundle.glob('*-source')
                      for path in directory.rglob('*')
                      if path.is_file() and '__pycache__' not in path.parts}
        if represented != discovered:
            errors.append({'kind': 'snapshot_manifest_coverage', 'bundle': name,
                           'unbound': sorted(str(x.relative_to(root)) for x in discovered - represented),
                           'missing': sorted(str(x.relative_to(root)) for x in represented - discovered)})
        names = subprocess.check_output(['git', '-C', str(root), 'ls-files', '--cached',
                                         '--others', '--exclude-standard', '-z', str(bundle)])
        publishable = {root / rel.decode() for rel in names.split(b'\0') if rel}
        large = []
        for path in sorted(publishable):
            if (path.suffix.lower() in {'.json', '.jsonl', '.ndjson', '.json5', '.bin'}
                    and path.stat().st_size >= 1_000_000):
                large.append({'path': str(path.relative_to(root)), 'bytes': path.stat().st_size,
                              'sha256': digest(path)})
        bundles.append({'name': name, 'distinct_snapshot_files': len(snapshot_paths) - before,
                        'publishable_files': len(publishable),
                        'publishable_bytes': sum(path.stat().st_size for path in publishable),
                        'large_json_frozen_exceptions': large})

    latest = json.loads((root / 'artifacts/four_color_ram_indexes/verification.json').read_text())
    for rel, sha in latest['source_sha256'].items():
        check(root / rel, sha, 'current_source_hash_bindings')
    expected_counts = {'distinct_gzip_records': (len(record_paths), 280),
                       'distinct_worker_reports': (len(worker_paths), 160),
                       'distinct_snapshot_files': (len(snapshot_paths), 309),
                       'distinct_baseline_optimized_snapshot_files': (len(baseline_optimized_paths), 267),
                       'distinct_incremental_snapshot_files': (len(incremental_paths), 42),
                       'current_source_hash_bindings': (checks['current_source_hash_bindings'], 47)}
    for label, (actual, expected) in expected_counts.items():
        if actual != expected:
            errors.append({'kind': 'unexpected_count', 'label': label,
                           'actual': actual, 'expected': expected})
    result = {
        'schema': 'four-color-publication-artifact-audit/v1',
        'status': 'PASS' if not errors else 'FAIL',
        'scope': 'Read-only custody, hash consistency, saved-record integrity and dependency closure; not a solver theorem or benchmark rerun.',
        'root': str(root),
        'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
        'command': shlex.join([sys.executable, str(Path(__file__).resolve()),
                               '--root', str(root), '--out', str(args.out.resolve())]),
        'script_sha256': digest(Path(__file__)),
        'checks': dict(sorted(checks.items())),
        'distinct_counts': {label: actual for label, (actual, _) in expected_counts.items()},
        'snapshot_count_interpretation': '267 distinct baseline/optimized files plus 42 distinct incremental files equals 309 distinct snapshot files. The 131 baseline, 136 optimized and 126 flow phase manifest checks total 393 snapshot hash bindings; baseline and optimized flow files are checked twice against independent bindings.',
        'bundles': bundles,
        'errors': errors,
    }
    args.out.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'result': str(args.out),
                      'distinct_counts': result['distinct_counts'], 'checks': result['checks'],
                      'errors': errors}, sort_keys=True))
    return bool(errors)


if __name__ == '__main__':
    sys.exit(main())
