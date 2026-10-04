#!/usr/bin/env python3
"""Compare final independent replays and assemble complete scoped ledgers."""
import argparse
import copy
import json
from pathlib import Path

from audit_bundle import digest, write

SPECS = {
    'a4': ('a4/attempts/0004-default', 'a4/attempts/0005-seed17',
           ('rebuilt_complete_relations.json', 'counterexamples.json', 'scope_ledger.json', 'audit_source_versions.json')),
    'b4': ('b4/default-final', 'b4/seed17-final',
           ('relations.json', 'scope_ledger.json', 'exact_lists.json', 'audit_source_versions.json')),
    'c4': ('c4/attempt3-default', 'c4/attempt4-seed17',
           ('relations.json', 'scope_ledger.json', 'audit_source_versions.json')),
}


def semantic_result(path, owner):
    data = json.loads(path.read_text())
    if owner == 'a4':
        data.pop('elapsed_seconds')
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path('.'))
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--a4-default', default=SPECS['a4'][0])
    parser.add_argument('--a4-seed', default=SPECS['a4'][1])
    parser.add_argument('--a4-replay', default='checks/a4-final-root-replay/audit')
    args = parser.parse_args()
    root = args.repo.resolve()
    base = root / 'audits/2026-10-04-task-d5'
    output = args.output.resolve()
    assert not output.exists(), 'Preserve earlier comparisons'
    output.mkdir(parents=True)
    comparisons, ledgers, audits = {}, {}, {}
    for owner, (default_rel, seed_rel, files) in SPECS.items():
        if owner == 'a4':
            default_rel, seed_rel = args.a4_default, args.a4_seed
        default, seed = base / default_rel, base / seed_rel
        replay = base / 'checks' / (owner + '-final-root-replay') / 'audit'
        if owner == 'a4':
            replay = base / args.a4_replay
        execution = json.loads((replay.parent / 'execution.json').read_text())
        data = semantic_result(default / 'results.json', owner)
        passed = data.get('all_checks_passed', data.get('status') == 'pass')
        rows = []
        for name in files:
            row = {'file': name, 'default_sha256': digest(default / name),
                   'seed17_sha256': digest(seed / name), 'root_replay_sha256': digest(replay / name)}
            row['byte_identical'] = len({row[k] for k in ('default_sha256', 'seed17_sha256', 'root_replay_sha256')}) == 1
            rows.append(row)
        results_equal = data == semantic_result(seed / 'results.json', owner) == semantic_result(replay / 'results.json', owner)
        comparisons[owner] = {'all_checks_passed': passed and execution['all_checks_passed']
                              and results_equal and all(r['byte_identical'] for r in rows),
                              'default_path': default_rel, 'seed17_path': seed_rel,
                              'root_replay_path': str(replay.relative_to(base)), 'files': rows,
                              'results_equal': results_equal,
                              'results_ignored_fields': ['elapsed_seconds'] if owner == 'a4' else [],
                              'source_stable': execution['sources_stable_during_replay']}
        ledgers[owner] = {'path': str((replay / 'scope_ledger.json').relative_to(root)),
                          'sha256': digest(replay / 'scope_ledger.json'),
                          'complete_ledger': json.loads((replay / 'scope_ledger.json').read_text())}
        audits[owner] = copy.deepcopy(data)
    result = {'all_checks_passed': all(v['all_checks_passed'] for v in comparisons.values()),
              'comparisons': comparisons,
              'scope': 'Full results, complete relations, every ledger and source version; only A4 elapsed time excluded'}
    write(output / 'replay_comparison.json', result)
    write(output / 'SCOPE_LEDGER.json', {'all_checks_passed': result['all_checks_passed'],
         'scope': 'Accepted A4 original04/04/root swap; B4 one conditional attachment branch; C4 only one newly closed key',
         'complete_ledgers': ledgers, 'audit_results': audits,
         'evidence_boundaries': {'arbitrary_size': 'Separate reviewed paper arguments under stated original-source hypotheses',
            'external_theorems': 'A4 Dvorak Lemma7/Theorem10; B4 ancillary connected slack only; C4 none required',
            'python': 'Fixed full relations/empty fibres/original-edge models/witnesses only',
            'lean': 'No new theorem; successful existing lake build does not formalize these paper arguments'},
         'no_research_expansion': True, 'no_commit_push': True})
    print(json.dumps({k: v['all_checks_passed'] for k, v in comparisons.items()}))
    assert result['all_checks_passed']


if __name__ == '__main__':
    main()
