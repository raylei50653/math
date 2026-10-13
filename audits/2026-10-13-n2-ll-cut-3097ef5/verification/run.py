#!/usr/bin/env python3
"""Local read-only replay receipt; exclusive creation, no historical writes."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

HERE = Path(__file__).resolve().parents[1]
REPO = HERE.parents[1]
REL = HERE.relative_to(REPO)
scripts = ['profiles/domain.py', 'profiles/independent_contacts.py', 'checker.py',
           'controls/checker.py', 'controls/supplemental_minor_checker.py',
           'controls/same_h_minor_checker.py', 'paper/topology_checker.py']
records = []
before = {str(p.relative_to(HERE)): hashlib.sha256(p.read_bytes()).hexdigest()
          for p in HERE.rglob('*.json') if 'verification' not in p.parts and 'entrypoints-before' not in p.parts}
for script in scripts:
    outputs = []
    for seed in (None, '17'):
        env = dict(os.environ)
        if seed is not None: env['PYTHONHASHSEED'] = seed
        argv = ['python3', '-B', str(REL / script), '--check']
        start = time.monotonic()
        result = subprocess.run(argv, cwd=REPO, env=env, capture_output=True, text=True)
        rec = {'argv': argv, 'seed': seed or 'normal', 'exit_code': result.returncode,
               'seconds': round(time.monotonic() - start, 3),
               'stdout': result.stdout, 'stderr': result.stderr}
        records.append(rec)
        outputs.append(result.stdout)
        print(script, seed or 'normal', result.returncode, flush=True)
        if result.returncode: raise RuntimeError(rec)
    if outputs[0] != outputs[1]: raise RuntimeError('hash-seed output drift: ' + script)

source = json.loads((HERE / 'profiles/profiles.json').read_bytes())
negative = []
for mutation in ('capacity-bound', 'fixed-cell'):
    bad = copy.deepcopy(source)
    row_id = bad['profiles'][0]['row_certificates'][0]
    row = bad['row_catalog'][row_id]
    if mutation == 'capacity-bound': row['row_bounds'][0] += 1
    else:
        cell = [row['rows'][0], row['columns'][0]]
        if cell in row['S_P']: row['S_P'].remove(cell)
        else: row['S_P'].append(cell)
    path = HERE / 'verification' / (mutation + '.corrupt.json')
    with path.open('x') as out: json.dump(bad, out, sort_keys=True, separators=(',', ':'))
    argv = ['python3', '-B', str(REL / 'checker.py'), '--check', '--profiles', str(path)]
    result = subprocess.run(argv, cwd=REPO, capture_output=True, text=True)
    if result.returncode == 0: raise RuntimeError('corrupt mathematical certificate accepted')
    negative.append({'mutation': mutation, 'argv': argv, 'exit_code': result.returncode,
                     'stdout': result.stdout, 'stderr': result.stderr,
                     'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
for path, sha in before.items():
    if hashlib.sha256((HERE / path).read_bytes()).hexdigest() != sha:
        raise RuntimeError('replay modified input ' + path)
receipt = {'base': '3097ef5be241b7777451a5ef8a663f3987d6b866',
           'status': 'mathematical finite replay passed', 'checks': records,
           'normal_seed17_equal_for_all_seven': True, 'read_only_input_drift': 0,
           'standalone_corrupt_profiles_rejected': negative,
           'artifact_hashes': before,
           'other_negative_records': ['controls/verification.json', 'controls/supplemental_verification.json',
                                      'controls/same_h_verification.json', 'paper/topology_verification.json'],
           'documentation_record': 'verification/documentation.json',
           'new_Lean_theorem': False, 'Lean_build': 'not run; no Lean edits, paper theorem not formalized',
           'full_target_finite_status': 'not triggered',
           'not_run': ['source graph census', 'upstream broad source enumerations', 'whole-tree DocGraph historical duplicate-ID cleanup',
                       'commit', 'push', 'PR', 'issue', 'external messages']}
with (HERE / 'verification.json').open('x') as out:
    json.dump(receipt, out, ensure_ascii=False, indent=2); out.write('\n')
print('receipt written; all read-only hashes unchanged', flush=True)
