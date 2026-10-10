#!/usr/bin/env python3
"""Seal this supervisor delivery; original outputs remain untouched."""
import hashlib
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


records = [json.loads(p.read_text()) for p in sorted((OUT / 'logs').glob('*.json'))]
assert len(records) == 14, len(records)
for p, row in zip(sorted((OUT / 'logs').glob('*.json')), records, strict=True):
    expected = 1 if p.stem == 'whole-docgraph' else 0
    assert row['exit_code'] == expected, p.name
    row['expected_exit'] = expected
    row['stdout_sha256'] = sha(OUT / row['stdout'])
    row['stderr_sha256'] = sha(OUT / row['stderr'])
post = json.loads((OUT / 'post-integration-final.json').read_text())
assert not post['worker_byte_mtime_drift']
assert post['worker_files_unchanged'] == 6012
checks = {'BASE': post['BASE'], 'actual_HEAD': post['BASE'],
          'commands': records, 'adoption': 'Fourteen S/U paper claims within their stated hypotheses; narrow subtypes only.',
          'paper': {'S': 6, 'U': 8, 'new_proof_gap': 0, 'Lean': 'no new proof or build'},
          'finite': {'distinct_graph_pin_cases': 7952, 'piece_relations': 690, 'piece_lifts': 2986,
                     'capacity_columns': 102, 'target_source_triggered': 0},
          'final_immutable_verification': 'post-integration-final.json',
          'shared_docs': (OUT / 'logs/docs-final.stdout.log').read_text().strip(),
          'formal_docs': (OUT / 'logs/formal-docgraph.stdout.log').read_text().strip(),
          'whole_worktree_DocGraph': {'exit': 1, 'duplicates': 62, 'copies_retained': True},
          'retained_history': {'fresh_BASE_docs': 'FAIL; two missing historical targets; SU-A and SU-J logs retained, not rerun here.',
                               'E4_byte_replays': 'Four BASE frozen historical exit1 logs retained; source field drift is not a mathematical counterexample.'},
          'propagation': {'updated': ['N45 canonical', 'E4 dated follow-up', 'Phase B direct consumer',
                                     'Kempe relevant paragraph', 'STATUS relevant index', 'N45 first-batch history'],
                          'reviewed_unchanged': ['E4 historical three-row body and original stop', 'CORE_CONSTRAINTS identity classification',
                                                 'E3 N2 reduction', 'U1-U4 44 domain'],
                          'stop': 'L2; parent N2/E OPEN, common language and HANDOFF/README unchanged'},
          'next_batch': {'residual': 'N45-U-LP', 'tasks': ['N45-PG', 'N45-PR', 'N45-PC'],
                         'status': 'ready for user publication; not started', 'geometry_control_triggered': 0},
          'not_run': ['whole upstream enumerations', 'broad graph/k search', 'Lean build or axioms audit',
                      'historical E4 replays (retained)', 'fresh BASE docs again (frozen worker evidence retained)'],
          'publication': 'no commit/push/PR/external messages/sub-agents'}
with (OUT / 'checks.json').open('x') as f:
    json.dump(checks, f, ensure_ascii=False, sort_keys=True, indent=2)
    f.write('\n')
for path in sorted(OUT.rglob('*')):
    if not path.is_file():
        continue
    if path.suffix == '.json':
        json.loads(path.read_text())
    if path.suffix in ('.py', '.md', '.json'):
        text = path.read_text()
        assert text.endswith('\n') and all(line == line.rstrip() for line in text.splitlines()), path
files = [p for p in sorted(OUT.rglob('*')) if p.is_file()]
with (OUT / 'MANIFEST.sha256').open('x') as f:
    for path in files:
        f.write(sha(path) + '  ' + str(path.relative_to(OUT)) + '\n')
for line in (OUT / 'MANIFEST.sha256').read_text().splitlines():
    digest, rel = line.split('  ', 1)
    assert sha(OUT / rel) == digest, rel
assert {str(p.relative_to(OUT)) for p in OUT.rglob('*') if p.is_file()} == {
    str(p.relative_to(OUT)) for p in files} | {'MANIFEST.sha256'}
assert (OUT / 'checks.json').exists()
print(json.dumps({'status': 'sealed', 'files_excluding_manifest': len(files),
                  'manifest_sha256': sha(OUT / 'MANIFEST.sha256'), 'worker_files_unchanged': 6012}, sort_keys=True))
