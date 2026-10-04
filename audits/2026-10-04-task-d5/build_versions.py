#!/usr/bin/env python3
"""Bind final returned inputs and observed runtime dependencies to captured bytes."""
import argparse
import json
from pathlib import Path

from audit_bundle import digest, write

TARGETS = {
    'A4': 'c5_excess_two_mixed_core_four_spoke_mixed12_04_04',
    'B4': 'c5_excess_two_mixed_core_four_spoke_mixed22_shared4',
    'C4': 'c5_mixed_p3_two_frame_two_unary',
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path('.'))
    parser.add_argument('--traces', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root, out = args.repo.resolve(), args.output.resolve()
    assert not out.exists(), 'Use a fresh version output'
    out.mkdir(parents=True)
    base = root / 'audits/2026-10-04-task-d5'
    baseline = json.loads((base / 'baseline.json').read_text())
    records, observed, external, trace_records = {}, {}, {}, []
    for path in sorted(args.traces.resolve().glob('*.runtime.json')):
        trace = json.loads(path.read_text())
        label = trace['script'] + ':' + trace['hashseed']
        trace_records.append({'path': str(path.relative_to(root)), 'sha256': digest(path),
                              'exit_code': trace['exit_code'],
                              'repository_writes': trace['repository_writes']})
        for rel, record in trace['repository_read_dependencies'].items():
            assert record == baseline['files'][rel], f'Runtime input differs from capture: {rel}'
            observed.setdefault(rel, []).append(label)
        for name, record in trace['imported_external_modules'].items():
            external.setdefault(name, {})[record['path']] = record['sha256']
    for rel, uses in sorted(observed.items()):
        records[rel] = {**baseline['files'][rel], 'observed_by': uses, 'declared_by': []}
    target_records = {}
    for label, name in TARGETS.items():
        paths = ['docs/' + name + '.md', 'scripts/' + name + '.py',
                 'artifacts/' + name + '/observations.json']
        payload = json.loads((base / 'snapshot' / paths[-1]).read_text())
        for key in ('input_sha256', 'inputs_sha256', 'scripts_sha256', 'source_sha256'):
            for rel, expected in payload.get(key, {}).items():
                assert expected == baseline['files'][rel]['sha256'], f'Stale final declaration: {rel}'
                records.setdefault(rel, {**baseline['files'][rel], 'observed_by': [], 'declared_by': []})
                records[rel]['declared_by'].append({'target': label, 'map': key})
                paths.append(rel)
        for rel in paths:
            records.setdefault(rel, {**baseline['files'][rel], 'observed_by': [], 'declared_by': []})
        target_records[label] = {'name': name, 'files': sorted(set(paths)), 'artifact_schema': payload.get('schema')}
    for rel in ('requirements.txt', 'lean-toolchain', 'lakefile.toml', 'lake-manifest.json',
                'artifacts/MANIFEST.json', '.gitignore'):
        records.setdefault(rel, {**baseline['files'][rel], 'observed_by': [], 'declared_by': []})
    missing = [p for p in records if p not in baseline['input_paths']]
    changed = [p for p in records if digest(base / 'snapshot' / p) != records[p]['sha256']]
    result = {'all_checks_passed': not missing and not changed and
              all(r['exit_code'] == 0 and not r['repository_writes'] for r in trace_records),
              'baseline_head': baseline['head'], 'targets': target_records,
              'versions': dict(sorted(records.items())), 'runtime_trace_records': trace_records,
              'external_imported_module_versions': external,
              'missing_snapshot_dependencies': missing, 'changed_snapshot_dependencies': changed,
              'scope': 'All actual read dependencies of 12 producer and one helper --check executions, both seeds; direct declarations of A4/B4/C4; source SHA256 names immutable snapshot version'}
    write(out / 'VERSION_TABLE.json', result)
    rows = ['# D₅ 固定成果版本表', '',
            'SHA256 綁定起始最終返回 bytes；整合後的文件版本另見文件變更表。', '',
            '| 成果 | 檔案 | bytes | SHA256 |', '| --- | --- | ---: | --- |']
    for label, name in TARGETS.items():
        for rel in ('docs/' + name + '.md', 'scripts/' + name + '.py',
                    'artifacts/' + name + '/observations.json'):
            entry = records[rel]
            rows.append(f'| {label} | `{rel}` | {entry["size"]} | `{entry["sha256"]}` |')
    rows += ['', '[完整版本／實際執行依賴表](VERSION_TABLE.json)逐份列出 imports、runtime inputs、',
             'declared inputs、兩 seed 的讀取者與外部 Python module hashes。',
             '[執行環境](../environment_versions.json)另列 Python、Lean／Lake、Git、uv 及 package 版本。',
             '複製完整既有 artifacts 僅確保依賴可重播，不擴大數學驗收範圍。', '']
    (out / 'VERSION_TABLE.md').write_text('\n'.join(rows))
    print(json.dumps({'passed': result['all_checks_passed'], 'versioned_files': len(records),
                      'runtime_traces': len(trace_records), 'observed_repository_dependencies': len(observed)}))
    assert result['all_checks_passed']


if __name__ == '__main__':
    main()
