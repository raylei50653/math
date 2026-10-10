#!/usr/bin/env python3
"""Exclusive seal with exact inventory; self and delivery hashes are non-circular."""
import hashlib
import json
from pathlib import Path
import sys
import time

H = Path(__file__).resolve().parent
R = H.parent.parent
start = time.time()


def read(p):
    return json.loads(p.read_text())


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def save(p, value):
    with p.open('x') as f:
        json.dump(value, f, ensure_ascii=False, sort_keys=True, indent=2)
        f.write('\n')


assert not (H / 'checks.json').exists() and not (H / 'MANIFEST.sha256').exists() and not (H / 'delivery.json').exists()
records = [read(p) for p in sorted((H / 'logs').glob('*.json')) if p.name != 'setup.json']
expected = {'fresh-BASE-docs': 1, 'whole-docgraph-shared': 1, 'exclusive-create-guard': 1}
for item in records:
    assert item['exit'] == expected.get(item['id'], 0), item
    item['expected_exit'] = expected.get(item['id'], 0)
    item['log_sha256'] = sha(H / item['log'])
assert len(records) == 18, (len(records), [x['id'] for x in records])
assert not read(H / 'fingerprints.json')['authored_bytes_and_mtime_drift']
assert not read(H / 'supervisor-comparison.json')['semantic_differences']
assert sha(H / 'certificate.json') == 'a4b5b4c148f823f8df22a2672700eb40516bae0fd673edf8210a477af3b508ee'
result = {'id': 'finalize', 'command': ['python3', '-B', str(H / 'finalize.py')],
          'cwd': str(R), 'environment': {'PYTHONDONTWRITEBYTECODE': '1'}, 'exit': 0,
          'seconds': round(time.time() - start, 6), 'log': 'logs/finalize.log',
          'expected_exit': 0,
          'scope': 'Assertions above completed; exclusive seal and read-back verification below.'}
with (H / 'logs/finalize.log').open('x') as f:
    f.write('PASS: 18 command records have their expected exits; finite certificate and drift evidence match.\n')
save(H / 'logs/finalize.json', result)
result['log_sha256'] = sha(H / result['log'])
records.append(result)
save(H / 'checks.json', {
    'task': 'N45-SU-J', 'BASE': read(H / 'inputs.json')['BASE'],
    'preparation': {'record': 'logs/setup.json', 'exit': 0,
                    'commands': ['git rev-parse HEAD', 'git status --short --branch',
                                 'git show BASE:path for 71 unique authority paths and each S/U/J manifest entry',
                                 'git archive BASE (extract exclusively into fresh base-source directory)'],
                    'record_correction': 'setup.json literal 71? is an explanatory placeholder; actual BASE_unique_inputs is 71.'},
    'commands_and_logs': records,
    'expected_failures_are_preserved': expected,
    'historical_failures_not_rerun': [
        {'scope': 'E4 core constraints and reductions, normal and seed17', 'exit': 1,
         'evidence': '../2026-10-09-n45-batch-supervision/e4_core_constraints.log and e4_reductions.log',
         'reason': 'Historical source provenance mismatch; outside this incremental finite task. Original FAIL retained.'}],
    'not_run': [
        {'scope': 'S-01–06 and U arbitrary-size paper / Gallai primary-source applicability', 'reason': 'SU-A owns these obligations.'},
        {'scope': 'E3/E4/E4C whole enumeration, ES/ER, U1–U4, new graph generation', 'reason': 'Fixed incremental inputs only; no broader search authorized.'},
        {'scope': 'All minimal cores re-enumeration', 'reason': 'Supplied core edges/degrees and retained-edge lifts checked; no new core claim.'},
        {'scope': 'lake build / axioms audit / native_decide', 'reason': 'No new Lean and no formalization claim.'},
        {'scope': 'Original worker generation and full verify drivers', 'reason': 'Read-only --check used; preserve original logs and artifacts.'},
        {'scope': 'Supervisor review scripts replay', 'reason': 'Read only after independent computation for comparison; never imported or executed.'}],
    'input_drift': [], 'finite_discrepancies': [], 'formal_docs_PASS_is_not_whole_worktree_PASS': True,
})
excluded = {'MANIFEST.sha256', 'delivery.json'}
files = [p for p in sorted(H.rglob('*')) if p.is_file() and str(p.relative_to(H)) not in excluded]
with (H / 'MANIFEST.sha256').open('x') as f:
    for p in files:
        f.write(sha(p) + '  ' + str(p.relative_to(H)) + '\n')
save(H / 'delivery.json', {
    'task': 'N45-SU-J', 'BASE': read(H / 'inputs.json')['BASE'],
    'actual_HEAD': read(H / 'fingerprints.json')['HEAD_before_after'],
    'manifest_sha256': sha(H / 'MANIFEST.sha256'), 'manifest_entries': len(files),
    'BASE_archive_files': sum(p.relative_to(H).parts[0] == 'base-source' for p in files),
    'authored_files_in_manifest': sum(p.relative_to(H).parts[0] != 'base-source' for p in files),
    'excluded_from_manifest': {'MANIFEST.sha256': 'self hash in delivery.json',
                               'delivery.json': 'final receipt; own hash omitted to avoid circularity'},
    'original_authored_bytes_and_mtime_drift': [], 'source_input_bytes_and_mtime_drift': [],
    'finite_payload': 'PASS in specified domain', 'target_source': 'not triggered',
    'source_counterexamples': 0, 'paper_and_Lean': 'not checked',
    'fresh_BASE_docs': 'FAIL: two historical missing paths', 'whole_worktree_DocGraph': 'FAIL: 62 duplicate IDs',
    'formal_docs_DocGraph': 'PASS', 'shared_docs': 'PASS',
    'publication': 'No commit, push, PR or external message',
})
assert {str(p.relative_to(H)) for p in H.rglob('*') if p.is_file()} == {
    str(p.relative_to(H)) for p in files} | excluded
for line in (H / 'MANIFEST.sha256').read_text().splitlines():
    digest, rel = line.split('  ', 1)
    assert sha(H / rel) == digest, rel
for rel in read(H / 'output-validation.json')['pending_targets']:
    assert (H / rel).exists(), rel
assert sha(H / 'MANIFEST.sha256') == read(H / 'delivery.json')['manifest_sha256']
print(json.dumps({'status': 'sealed and verified', 'manifest_entries': len(files),
                  'manifest_sha256': sha(H / 'MANIFEST.sha256'),
                  'delivery_sha256': sha(H / 'delivery.json')}, sort_keys=True))
