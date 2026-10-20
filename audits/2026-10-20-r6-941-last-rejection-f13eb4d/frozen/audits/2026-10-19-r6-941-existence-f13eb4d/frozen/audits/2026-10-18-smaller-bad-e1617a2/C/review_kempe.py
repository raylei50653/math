#!/usr/bin/env python3
"""Independent candidate projections using C's local full-lift evaluator."""
import argparse
import contextlib
import hashlib
import io
import json
from pathlib import Path
import runpy
import sys
ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--check', action='store_true')
args = parser.parse_args()
saved = sys.argv
sys.argv = [str(ROOT / 'check.py'), '--check']
with contextlib.redirect_stdout(io.StringIO()):
    local = runpy.run_path(str(ROOT / 'check.py'))
sys.argv = saved
source = ROOT.parent / 'kempe-consistency.json'
data = json.loads(source.read_text())
assert hashlib.sha256((ROOT.parent / 'kempe_consistency.py').read_bytes()).hexdigest() == data['script_sha256']
projections = []
for i, values in enumerate(data['tuples']):
    chi = dict(zip(data['pin_order'], values))
    state = tuple(chi[v] for v in local['PINS'])
    support = local['state_support'](state)
    assert support[0] == data['old_lift_masks'][i]
    projections.append(support)
results = []
expected = {932: (932, 1021, 1023, 509, 1021, 1021, 1021),
            933: (933, 1021, 1023, 509, 1021, 1021, 1021),
            941: (941, 1023, 1023, 511, 1023, 1023, 1023)}
for record in data['results']:
    target = record['source_mask']
    support = local['union'](projections[i] for i in record['surviving_ids'])
    assert support == expected[target]
    assert support[0] == record['surviving_old_projection']
    assert all(mask in local['K'] for mask in support[1:])
    accepted = [i for i in record['surviving_ids'] if projections[i][0] & 512]
    assert accepted == record['accepted_tuple_ids']
    results.append({'source_mask': target, 'initial_states': len(record['initial_ids']),
                    'surviving_states': len(record['surviving_ids']),
                    'accepted_states': len(accepted), 'support_order': local['NAMES'],
                    'joint_supports': support, 'all_six_candidates_in_K132': True})
result = {'scope': 'independent full-local-lift projections of supplied surviving states; does not audit partition fixed point or claim graph realization',
          'kempe_certificate_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
          'kempe_script_sha256': data['script_sha256'],
          'C_script_sha256': hashlib.sha256((ROOT / 'check.py').read_bytes()).hexdigest(),
          'C_certificate_sha256': hashlib.sha256((ROOT / 'certificate.json').read_bytes()).hexdigest(),
          'review_script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'all_274_old_projection_masks_match': len(projections) == 274,
          'results': results}
path = ROOT / 'REVIEW-KEMPE.json'
if args.check:
    assert json.loads(path.read_text()) == json.loads(json.dumps(result)), 'review differs'
else:
    with path.open('x') as stream:
        stream.write(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
