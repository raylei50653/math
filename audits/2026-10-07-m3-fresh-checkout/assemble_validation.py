#!/usr/bin/env python3
"""Assemble recorded M3 commands after all candidate checks finish."""
import gzip
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
REQUIRED = [
    'archive-restore', 'archive-verify', 'artifact-status', 'docs', 'docgraph-default', 'checkout-diff',
    'u1-default', 'u1-seed17', 'mixed-verifier',
    'd9-e4-default', 'd9-e4-seed17', 'd9-e5-default', 'd9-e5-seed17', 'd9-e6-default', 'd9-e6-seed17',
    'c44-input-audit', 'c44-small', 'c44-full-default', 'c44-full-seed17', 'c44-algorithm-audit',
    'c44p-screen-default', 'c44p-two-private-default', 'c44p-independent-default',
    'c44p-screen-seed17', 'c44p-two-private-seed17', 'c44p-independent-seed17',
    'lc-exporter', 'lean-build', 'lean-axioms',
]


def read(name):
    path = HERE / name
    return json.loads(path.read_bytes() if path.exists() else gzip.decompress((HERE / (name + '.gz')).read_bytes()))


def main():
    records = [json.loads(p.read_text()) for p in sorted((HERE / 'commands').glob('*.json'))]
    by_name = {r['name']: r for r in records}
    assert len(by_name) == len(records) and set(REQUIRED) <= by_name.keys()
    failures = [name for name in REQUIRED if by_name[name]['exit_code'] != 0]
    assert failures == ['c44-input-audit'], failures
    axioms = read('lean-axioms-summary.json')
    drift = read('sources-after.json')
    assert drift['zero_drift']
    provenance = read('provenance-summary.json')
    result = {
        'task': 'M3', 'execution_status': 'complete', 'acceptance_status': 'needs follow-up',
        'candidate_sha': 'ba0b447f09617591d9f2ba81c988f537af771791',
        'base_sha': '2ddc6b4a4e412ab2cb7917fe4fb6fdeef2e86090',
        'candidate_parent_sha': 'a1ca89db9c04c6e65ba0b1cb0928df9e8c163e42',
        'checkout': '/tmp/math-m3-ba0b447', 'new_commit': None,
        'required_checks': {'count': len(REQUIRED), 'passed': len(REQUIRED) - len(failures),
                            'failed': failures, 'names': REQUIRED},
        'commands': records, 'setup': 'setup.json', 'environment': 'environment.json',
        'lean_environment': 'lean-environment.json', 'lean_axioms': 'lean-axioms-summary.json',
        'source_inventory_before': 'sources-before.json.gz',
        'source_inventory_after': 'sources-after.json.gz',
        'zero_source_drift': drift['zero_drift'], 'source_entries': drift['entry_count'],
        'source_bytes': drift['file_bytes'],
        'summaries': ['controls-summary.json', 'c44-summary.json', 'provenance-summary.json'],
        'candidate_specific_findings': ['M3-C44-INPUT-AUDIT-001', 'M3-PROV-E5-BRANCHES'],
        'historical_byte_failures_preserved': ['E4 reductions', 'E5 controls', 'E4C'],
        'mathematical_payload_differences': [],
        'whitespace_exceptions': 'whitespace-comparison.json', 'not_rerun': provenance['not_rerun'],
        'limits': ['M2 paper audit is separate', 'no new k search, arbitrary-size theorem or source realization',
                   'LC is an explicit local target outside default CI', 'no commit, push, PR, CI dispatch or merge'],
    }
    (HERE / 'validation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    table = ['# M3 完整命令台帳', '',
             '每筆 JSON 保存完整 argv、cwd、環境、exit、耗時及 stdout／stderr bytes／SHA256。',
             'Clone／checkout 的兩筆命令另見 [setup.json](setup.json)。', '',
             '| 命令紀錄 | exit | 秒 | stdout | stderr |', '| --- | ---: | ---: | --- | --- |']
    for r in records:
        out, err = r['logs']
        table.append(f"| [{r['name']}](commands/{r['name']}.json) | {r['exit_code']} | {r['seconds']} | [log]({out['path']}) | [log]({err['path']}) |")
    table += ['', 'Helper 控制使用 Oct05 舊 log，只驗證本次統計工具；原控制 harness／parser 錯誤及封存跨 device 失敗均留存。',
              '這些紀錄與正式候選的 Lean build／axioms 命令分開，不充當 fresh LC 證據。', '']
    (HERE / 'COMMANDS.md').write_text('\n'.join(table))
    print(json.dumps({'required': len(REQUIRED), 'passed': len(REQUIRED) - len(failures),
                      'failures': failures, 'commands': len(records), 'axioms': axioms['declaration_count']}))


if __name__ == '__main__':
    main()
