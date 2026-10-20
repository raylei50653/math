#!/usr/bin/env python3
"""Read-only, exact connected replay of the named 941 audit."""
import hashlib
import copy
import json
from pathlib import Path
import subprocess
import sys

D = Path(__file__).resolve().parent
ROOT = D.parents[1]
BASE = 'b89c5913cea9df2305845be0f65fa6f1c1aaf55f'
manifest = json.loads((D / 'INPUTS.json').read_text())
assert manifest['base'] == manifest['start_head'] == BASE
assert manifest['initial_status'] == 'clean'
assert manifest['exclusive_audit'] == D.relative_to(ROOT).as_posix()
expected = {'docs/HANDOFF.md', 'docs/STATUS.md', 'docs/DOCUMENTATION.md',
            'docs/c5_kempe_guide.md'}
for name in ('2026-10-18-smaller-bad-e1617a2',
             '2026-10-18-smaller-bad-counts-e1617a2',
             '2026-10-19-c5-pr-disk-semantics-ed59843'):
    paths = subprocess.check_output(
        ['git', 'ls-tree', '-r', '--name-only', BASE, 'audits/' + name],
        cwd=ROOT, text=True).splitlines()
    expected.update(paths)
assert set(manifest['inputs']) == expected and len(expected) == 238, 'frozen input domain'
assert manifest['routing_drift_allowed'] == ['docs/c5_kempe_guide.md', 'docs/STATUS.md']
for path, digest in manifest['inputs'].items():
    if path in manifest['routing_drift_allowed']:
        raw = subprocess.check_output(['git', 'show', BASE + ':' + path], cwd=ROOT)
    else:
        raw = (ROOT / path).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == digest, ('frozen input drift', path)

# Freeze mathematical outputs before running any child checker. Logs, review
# receipts and routing files are deliberately outside this immutable domain.
sealed = json.loads((D / 'OUTPUTS.json').read_text())
assert sealed['base'] == BASE
assert sealed['source_realized'] is False
assert sealed['whole_three_candidate_route_excluded'] is False
assert sealed['GB_four_row_route_excluded'] is True
for path, digest in sealed['outputs'].items():
    assert hashlib.sha256((D / path).read_bytes()).hexdigest() == digest, ('audit drift', path)

def verify_costs(costs):
    assert costs['boundary'] == ['x', 'y', 'a', 'b', 'c']
    assert costs['deleted'] == ['p', 'h']
    assert costs['new_vertices'] == costs['reconstruction_vertices'] == 0
    assert costs['changed_boundary'] is False
    classes = {'Q1': [['n', 'b'], ['R', 'q']],
               'Q2': [['n', 'L', 'b']], 'GB': []}
    assert set(costs['candidates']) == set(classes)
    for name, record in costs['candidates'].items():
        assert record['classes'] == classes[name]
        change = -len(costs['deleted']) - sum(len(c) - 1 for c in record['classes'])
        assert record['completed_inner_change'] == change, 'completed size includes every identification'

costs = json.loads((D / 'costs.json').read_text())
verify_costs(costs)
bad_cost = copy.deepcopy(costs)
bad_cost['candidates']['Q1']['completed_inner_change'] = -2
try:
    verify_costs(bad_cost)
except AssertionError:
    cost_negative_rejected = True
else:
    raise AssertionError('omitted quotient cost was accepted')

results = []
commands = [
    (ROOT / 'audits/2026-10-18-smaller-bad-e1617a2/A/verify_kempe.py', []),
    (ROOT / 'audits/2026-10-18-smaller-bad-e1617a2/B/check.py', ['--negative-control']),
    (D / 'B/check_core.py', []),
    (D / 'C/check.py', ['--negative-controls']),
    (D / 'A/check.py', ['--negative-controls']),
]
for path, args in commands:
    run = subprocess.run([sys.executable, '-B', str(path), *args], cwd=ROOT,
                         capture_output=True, text=True)
    if run.returncode:
        sys.stderr.write(run.stdout + run.stderr)
        raise SystemExit(run.returncode)
    results.append({'checker': path.relative_to(ROOT).as_posix(),
                    'exit_code': run.returncode, 'stdout': run.stdout.strip()})
for path, digest in sealed['outputs'].items():
    assert hashlib.sha256((D / path).read_bytes()).hexdigest() == digest, ('checker wrote output', path)
print(json.dumps({'pass': True, 'base': BASE, 'frozen_inputs': len(expected),
                  'frozen_drift': 0, 'output_drift': 0,
                  'GB941_accepts01232_and01212': True,
                  'GB941_four_row_route_excluded': True,
                  'whole_three_candidate_route_excluded': False,
                  'all_GB_supports_in_K132_proved': False,
                  'Q1_Q2_source_four_row_route': 'OPEN',
                  'omitted_completed_cost_negative_rejected': cost_negative_rejected,
                  'smaller_bad_constructed': False, 'checks': results}, sort_keys=True))
