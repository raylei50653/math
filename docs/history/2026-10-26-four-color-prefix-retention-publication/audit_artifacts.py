#!/usr/bin/env python3
"""Read saved prefix/retention evidence; write only the requested audit receipt.

Checks custody and complete saved outputs, without running the solver or timing
experiments. Historical seed-17 runs are receipts, not fresh replay results.
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


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()


def graph_hash(graph):
    source = {'vertices': graph['vertices'],
              'edges': [list(e) for e in sorted(tuple(sorted(e)) for e in graph['edges'])],
              'fixed': graph.get('fixed', [])}
    return sha(json.dumps(source, separators=(',', ':')).encode())


def semantic(record):
    counters = {'checks', 'candidate_checks', 'relation_checks'}
    result = dict(record)
    result.pop('bucket_method', None)
    result['stats'] = {k: v for k, v in record['stats'].items() if k not in counters}
    result['events'] = [dict(event, stats={k: v for k, v in event['stats'].items()
                                         if k not in counters}) for event in record['events']]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    logic = root / 'artifacts/four_color_logic_optimization'
    retention = root / 'artifacts/four_color_retention_audit'
    checks, errors = Counter(), []
    snapshots, records = set(), set()
    reports, outputs, raw_outputs = {}, {}, {}

    def require(condition, label, detail=''):
        checks[label] += 1
        if not condition:
            errors.append({'kind': label, 'detail': str(detail)})

    def load(path):
        return json.loads(path.read_bytes())

    def check_file(path, expected, label):
        require(path.is_file() and sha(path.read_bytes()) == expected, label,
                path.relative_to(root))

    def source_snapshot(path, expected):
        check_file(path, expected, 'snapshot_hash_bindings')
        snapshots.add(path)

    final = load(logic / 'final-source-manifest.json')
    for rel, expected in final.items():
        source_snapshot(logic / 'final-source' / rel, expected)
    baseline = load(logic / 'baseline-manifest.json')
    for rel, expected in baseline['files'].items():
        candidate = logic / 'exploration-sources/baseline' / rel
        source_snapshot(candidate if candidate.is_file() else logic / 'final-source' / rel,
                        expected)
    check_file(logic / 'inputs.json', baseline['inputs_sha256'], 'input_hash_bindings')
    inputs = {case['name']: case for case in load(logic / 'inputs.json')}
    exploration = load(logic / 'exploration.json')
    for mode, row in exploration['modes'].items():
        for rel, expected in row['sources'].items():
            candidate = logic / 'exploration-sources' / mode / rel
            source_snapshot(candidate if candidate.is_file() else logic / 'final-source' / rel,
                            expected)
    independent = load(logic / 'independent-checks/receipt.json')
    check_file(logic / 'independent-checks/check_independent.py',
               independent['driver_sha256'], 'independent_driver_hash')
    for mode, expected in independent['receipt_sha256'].items():
        check_file(logic / 'independent-checks' / (mode + '.json'), expected,
                   'independent_receipt_hash')
    for mode, row in independent['modes'].items():
        for rel, expected in row['source_hashes'].items():
            source_snapshot(logic / 'exploration-sources' / mode / 'scripts' / rel, expected)

    summary, verification = load(retention / 'summary.json'), load(retention / 'verification.json')
    source_snapshot(retention / verification['baseline_solver'], verification['baseline_solver_sha256'])
    require(verification['baseline_solver_sha256'] == final['scripts/four_color_constraints.py'],
            'retention_baseline_matches_prefix')
    for rel, expected in summary['sources_sha256'].items():
        check_file(root / rel, expected, 'current_script_hash_bindings')
    for rel, expected in summary['frozen_sources'].items():
        check_file(root / rel, expected, 'retention_report_current_source_bindings')
    check_file(retention / 'summary.json', verification['retention_summary_sha256'],
               'retention_summary_hash')

    for label, directory in [('anchor', logic / 'comparison/anchor'),
                             ('prefix', logic / 'comparison/prefix'),
                             ('mask', retention / 'complete-run')]:
        report = load(directory / 'report.json')
        reports[label], outputs[label], raw_outputs[label] = report, {}, {}
        check_file(directory / report['input_file'], report['inputs_sha256'], 'report_input_hash')
        check_file(directory / report['baseline_manifest_file'], report['baseline_manifest_sha256'],
                   'report_baseline_manifest_hash')
        require(report['inputs_sha256'] == baseline['inputs_sha256'], 'common_frozen_inputs')
        bound = dict(report['sources'])
        bound['scripts/four_color_flow_experiment.py'] = report['driver_sha256']
        if label == 'mask':
            for rel, expected in bound.items():
                check_file(root / rel, expected, 'mask_current_source_hash_bindings')
            require(report['sources'] == summary['frozen_sources'], 'retention_report_sources')
        else:
            require(bound == final, 'prefix_report_frozen_sources', label)
        for case in report['cases']:
            row = case['results']['combined-contexts']
            path = directory / row['full_record']
            check_file(path, row['compressed_record_sha256'], 'full_record_hash')
            raw = path.read_bytes()
            record = json.loads(gzip.decompress(raw))
            records.add(path)
            checks['gzip_json_integrity'] += 1
            require(record['status'] == case['reference_status'] and record['status'] != 'limit',
                    'record_reference_status', case['name'])
            require(record['graph_sha256'] == case['graph_sha256'] ==
                    graph_hash(inputs[case['name']]['graph']) == graph_hash(record['graph']),
                    'original_graph_identity', case['name'])
            require(not record['trace_truncated'], 'untruncated_saved_record', case['name'])
            require(record['bucket_method'] == ('prefix' if label == 'mask' else label),
                    'executed_method_metadata', case['name'])
            outputs[label][case['name']], raw_outputs[label][case['name']] = record, raw

    comparison = load(logic / 'comparison/comparison.json')
    require(comparison == load(retention / 'prefix-comparison.json'), 'retention_prefix_comparison_copy')
    require(comparison['inputs_sha256'] == baseline['inputs_sha256'], 'comparison_input_binding')
    for mode in ['anchor', 'prefix']:
        require(comparison['sources'] == reports[mode]['sources'], 'comparison_source_binding', mode)
        require(comparison['totals'][mode] == reports[mode]['totals']['all'], 'comparison_totals', mode)
        require(comparison['options'] == {k: v for k, v in reports[mode]['options'].items()
                                         if k != 'bucket_method'}, 'comparison_options', mode)
    for field in ['selected_cases', 'oracle_max_rows', 'python', 'networkx', 'driver_sha256']:
        require(reports['anchor'][field] == reports['prefix'][field],
                'comparison_environment_identity', field)
    exploration_cases = {row['name']: row for row in exploration['cases']}
    for case in comparison['cases']:
        name = case['name']
        left, right = outputs['anchor'][name], outputs['prefix'][name]
        require(semantic(left) == semantic(right), 'saved_full_semantic_pairs', name)
        require(sha(json.dumps(semantic(left), ensure_ascii=False, sort_keys=True,
                               separators=(',', ':')).encode()) == case['semantic_sha256'],
                'comparison_semantic_hash', name)
        for mode, prototype in [('anchor', 'baseline'), ('prefix', 'prefix')]:
            record = dict(outputs[mode][name])
            record.pop('bucket_method')
            require(sha(gzip.compress(canonical(record), mtime=0)) ==
                    exploration_cases[name]['modes'][prototype]['original_record_sha256'],
                    'frozen_prototype_output_hash', name)
            require(sha(raw_outputs[mode][name]) == case['modes'][mode]['record_sha256'],
                    'comparison_record_hash', name)
        require(raw_outputs['prefix'][name] == raw_outputs['mask'][name],
                'saved_mask_prefix_exact_gzip_pairs', name)

    for row in verification['complete_record_comparisons']:
        mode = 'anchor' if row['before'].endswith('/anchor') else 'prefix'
        require(row['case_count'] == len(row['cases']) == 40 and
                row['all_full_gzip_records_byte_equal'], 'historical_comparison_shape')
        for case in row['cases']:
            require(sha(raw_outputs[mode][case['name']]) == case['full_record_sha256'],
                    'historical_before_after_record_receipt_bindings', case['name'])

    stored = verification['report_storage']
    original = gzip.decompress((retention / stored['original_bytes_archive']).read_bytes())
    require(sha(original) == stored['raw_report_sha256'] == summary['frozen_report_sha256'],
            'retention_original_report_hash')
    require(json.loads(original) == reports['mask'], 'retention_original_compact_report_equal')
    check_file(retention / 'complete-run/report.json', stored['compact_report_sha256'],
               'retention_compact_report_hash')
    for row in load(logic / 'archive-format.json')['files']:
        path = logic / row['path']
        check_file(path, row['archived_sha256'], 'prefix_compact_report_hash')
        pretty = canonical(load(path))
        require(len(pretty) == row['original_bytes'] and sha(pretty) == row['original_sha256'],
                'prefix_original_report_reconstruction', row['path'])
    saved = load(logic / 'verification.json')
    for rel, key in [('comparison/comparison.json', 'final_comparison_sha256'),
                     ('independent-checks/receipt.json', 'independent_receipt_sha256'),
                     ('tests.log', 'tests_log_sha256')]:
        check_file(logic / rel, saved[key], 'prefix_verification_hash')
    require(saved['final_source_files_verified'] == len(final) == 49,
            'frozen_final_source_count')
    require(len(records) == 120, 'distinct_saved_gzip_count')
    bundles = []
    for directory in [logic, retention]:
        names = subprocess.check_output(['git', '-C', str(root), 'ls-files', '--cached',
                                         '--others', '--exclude-standard', '-z', str(directory)])
        paths = {root / name.decode() for name in names.split(b'\0') if name}
        large = [str(p.relative_to(root)) for p in paths if p.suffix.lower() in
                 {'.json', '.jsonl', '.ndjson', '.json5', '.bin'} and p.stat().st_size >= 1_000_000]
        require(not large, 'no_large_publishable_generated_files', large)
        bundles.append({'name': directory.name, 'publishable_files': len(paths),
                        'publishable_bytes': sum(p.stat().st_size for p in paths)})
    result = dict(schema='four-color-prefix-retention-publication-audit/v1',
                  status='PASS' if not errors else 'FAIL',
                  scope='Saved evidence custody, dependency closure and complete-output comparison; no benchmark or solver rerun. Historical seed-17 receipts are bound to saved hashes, not freshly replayed.',
                  root=str(root), recorded_at_utc=datetime.now(timezone.utc).isoformat(),
                  command=shlex.join([sys.executable, str(Path(__file__).resolve()),
                                      '--root', str(root), '--out', str(args.out.resolve())]),
                  script_sha256=sha(Path(__file__).read_bytes()), checks=dict(sorted(checks.items())),
                  distinct_counts={'gzip_records': len(records), 'snapshot_files': len(snapshots),
                                   'final_snapshot_files': len(final)}, bundles=bundles, errors=errors)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    print(json.dumps(result, sort_keys=True))
    return bool(errors)


if __name__ == '__main__':
    sys.exit(main())
