#!/usr/bin/env python3
"""Read-only replay of the named C8 audit and inherited C7 exclusion.

--write saves a new verification log exclusively; --check also verifies the
sealed local payload. Neither mode changes certificates or frozen inputs.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frozen_inputs():
    base = json.loads((HERE/'BASE.json').read_text())
    assert base['base'] == '3097ef5be241b7777451a5ef8a663f3987d6b866'
    checked = []
    for row in base['inputs']:
        frozen = HERE/'frozen'/row['path']
        assert digest(frozen) == row['sha256']
        original = subprocess.check_output(['git', 'show', base['base']+':'+row['path']], cwd=REPO)
        assert original == frozen.read_bytes(), 'BASE mismatch: '+row['path']
        # The one current authority entry deliberately receives a dated update;
        # its BASE copy remains the exact authority for this mathematical audit.
        live_match = digest(REPO/row['path']) == row['sha256']
        if row['path'].startswith('audits/') and row['path'] != 'audits/README.md':
            assert live_match, 'unrelated authority changed: '+row['path']
        checked.append(dict(path=row['path'], frozen_matches_BASE=True, live_matches_BASE=live_match))
    return checked


def run(argv):
    start = time.monotonic()
    env = os.environ.copy()
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    process = subprocess.run(argv, cwd=REPO, env=env, text=True, capture_output=True)
    record = dict(argv=argv, returncode=process.returncode, stdout=process.stdout,
                  stderr=process.stderr, elapsed_seconds=time.monotonic()-start)
    assert process.returncode == 0, record
    return record


def main():
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--write', action='store_true')
    modes.add_argument('--check', action='store_true')
    args = parser.parse_args()
    sources = frozen_inputs()
    if args.check:
        manifest = json.loads((HERE/'MANIFEST.json').read_text())
        for row in manifest['audit_files']:
            path = HERE/row['path']
            assert path.stat().st_size == row['bytes'] and digest(path) == row['sha256'], row['path']
    rel = str(HERE.relative_to(REPO))
    commands = [
        ['python3', rel+'/interface.py', '--check'],
        ['python3', rel+'/controls/checker.py', '--check'],
        ['python3', rel+'/counts/checker.py', '--check'],
        ['python3', rel+'/count_review.py', '--check'],
        ['python3', 'audits/2026-10-12-neartri-complete-relation-reductions-5d70a399/collar_checker.py', '--check'],
        ['python3', 'audits/2026-10-13-c7-joint-kempe-19209f4c/joint/count_identity.py', '--check'],
        ['python3', 'audits/2026-10-13-c7-joint-kempe-19209f4c/topology/count_review.py'],
    ]
    checks = [run(command) for command in commands]
    compressed = json.loads((HERE/'counts/certificate.v2.json').read_text())
    matrix = json.loads((HERE/'equality_matrix.json').read_text())
    assert matrix['pattern_order'] == compressed['pattern_order']
    assert matrix['noncrossing_partitions'] == compressed['noncrossing_partitions']
    active = {j:k for k,j in enumerate(compressed['active_partition_indices'])}
    assert matrix['equality_rows'] == [[row[active[j]] if j in active else 0
                                      for j in range(len(compressed['noncrossing_partitions']))]
                                     for row in compressed['equality_rows']]
    subrecords = ['validation/interface_checks.json', 'controls/verification.json',
                  'counts/verification.json', 'validation/lean.json', 'documentation_checks.json']
    for path in subrecords:
        assert (HERE/path).is_file(), 'missing validation record: '+path
    payload = dict(status='PASS', frozen_inputs=sources, checks=checks,
                   validation_records={p:digest(HERE/p) for p in subrecords},
                   summary=dict(named_collars=35,queries=70,excluded_transfer_kempe=57,
                                excluded_count=3,necessary_condition_residual=10),
                   source_input_drift=0, adopted_bounds='h>=3, n5>=9 unchanged',
                   excluded_scope='Every finite planar inner disk compatible with the frozen source collar theorem',
                   not_executed=['larger source graph enumeration', 'external theorem computation',
                                 'new Lean formalization', 'global duplicate-ID repair',
                                 'commit/push/PR/issue/comment'])
    if args.write:
        with (HERE/'verification.json').open('x') as stream:
            json.dump(payload, stream, indent=2, sort_keys=True)
            stream.write('\n')
    else:
        recorded = json.loads((HERE/'verification.json').read_text())
        assert recorded['summary'] == payload['summary']
        assert recorded['validation_records'] == payload['validation_records']
    print(json.dumps(dict(status='PASS', **payload['summary'], frozen_source_drift=0), sort_keys=True))


if __name__ == '__main__':
    main()
