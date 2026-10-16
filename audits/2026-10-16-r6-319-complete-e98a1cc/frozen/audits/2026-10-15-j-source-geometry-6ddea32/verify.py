#!/usr/bin/env python3
import copy
import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
receipts = []
hashes = {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
          for name in ('certificate.json', 'two-palette.json.gz')}


def run(name, script='check.py', args=(), seed=None, accept=True):
    env = os.environ.copy()
    if seed is not None:
        env['PYTHONHASHSEED'] = str(seed)
    p = subprocess.run([sys.executable, '-B', str(HERE / script), *map(str, args)],
                       cwd=REPO, env=env, capture_output=True, text=True)
    for ext, value in [('stdout', p.stdout), ('stderr', p.stderr)]:
        with (HERE / 'logs' / (name + '.' + ext)).open('x') as f:
            f.write(value)
    assert (p.returncode == 0) == accept, name
    receipts.append({'name': name, 'script': script, 'exit_code': p.returncode,
                     'expected': 'accept' if accept else 'reject'})
    return p.stdout


assert run('normal') == run('seed17', seed=17)
assert run('two-palette-normal', 'check_two_palette.py') == run('two-palette-seed17', 'check_two_palette.py', seed=17)
data = json.loads((HERE / 'certificate.json').read_text())
for name in ('missing-full-lift', 'missing-empty-fibre', 'wrong-source-palette'):
    bad = copy.deepcopy(data)
    fibres = bad['patch_controls'][0]['all_proper_boundary_fibres_including_empty']
    if name == 'missing-full-lift':
        next(f for f in fibres if f['all_full_lifts'])['all_full_lifts'].pop()
    elif name == 'missing-empty-fibre':
        fibres.remove(next(f for f in fibres if not f['all_full_lifts']))
    else:
        row = bad['all_proper_six_pin_rows'][0]
        row['source_all_r_allowed'] = not row['source_all_r_allowed']
    path = HERE / 'negative' / (name + '.json')
    with path.open('x') as f:
        json.dump(bad, f, sort_keys=True, separators=(',', ':'))
    run(name, args=('--certificate', path), accept=False)
bad = json.loads(gzip.decompress((HERE / 'two-palette.json.gz').read_bytes()))
bad['all_unequal_two_palette_obstructions'][0]['unique_forbidden_full_lift']['hub_pair'] = [0, 0]
path = HERE / 'negative' / 'wrong-hub-return.json.gz'
with path.open('xb') as f:
    f.write(gzip.compress(json.dumps(bad, sort_keys=True, separators=(',', ':')).encode(), mtime=0))
run('wrong-hub-return', 'check_two_palette.py', ('--certificate', path), accept=False)
run('exclusive-create', args=('--write',), accept=False)
run('two-palette-exclusive-create', 'check_two_palette.py', ('--write',), accept=False)
assert hashes == {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest() for name in hashes}
seal = json.loads((REPO / 'audits/2026-10-15-route-round4-6ddea32/BASE.json').read_text())
drift = [p for p, wanted in seal['prior_file_hashes'].items()
         if hashlib.sha256((REPO / p).read_bytes()).hexdigest() != wanted]
assert not drift
report = {'receipts': receipts, 'certificate_hashes_unchanged': hashes,
          'prior_files_checked': len(seal['prior_file_hashes']), 'prior_file_drift': drift,
          'source_status': 'not triggered', 'complete_319_exclusion': 'OPEN'}
with (HERE / 'VERIFICATION.json').open('x') as f:
    json.dump(report, f, indent=2, sort_keys=True)
    f.write('\n')
print(json.dumps(report, sort_keys=True))
