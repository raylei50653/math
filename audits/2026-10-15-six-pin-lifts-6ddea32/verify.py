#!/usr/bin/env python3
import copy
import hashlib
import itertools
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
checker = ROOT / 'check.py'
certificate = ROOT / 'certificate.json'
baseline = hashlib.sha256(certificate.read_bytes()).hexdigest()
data = json.loads(certificate.read_text())
receipts = []


def run(name, args=(), seed=None, expected=0):
    env = os.environ.copy()
    if seed is not None:
        env['PYTHONHASHSEED'] = str(seed)
    proc = subprocess.run([sys.executable, '-B', str(checker), *map(str, args)],
                          cwd=REPO, env=env, capture_output=True, text=True)
    for suffix, text in [('stdout', proc.stdout), ('stderr', proc.stderr)]:
        with (ROOT / 'logs' / (name + '.' + suffix)).open('x') as f:
            f.write(text)
    assert (proc.returncode == 0) == (expected == 0), name
    receipts.append({'name': name, 'returncode': proc.returncode,
                     'expected': 'accept' if expected == 0 else 'reject'})
    return proc.stdout


normal = run('normal')
assert run('seed17', seed=17) == normal
for name in ('missing-full-lift', 'missing-empty-fibre', 'wrong-return-side'):
    bad = copy.deepcopy(data)
    if name == 'missing-full-lift':
        bad['controls'][0]['U']['all_equal_s_t_full_lifts'].pop()
    elif name == 'missing-empty-fibre':
        fibres = bad['controls'][0]['six_pin_fibres_all_4^6_including_empties']
        del fibres[next(k for k, v in fibres.items() if not v)]
    else:
        checks = bad['controls'][1]['all_failed_state_pair_checks']
        ret = next(c['all_single_cycle_returns'][0] for c in checks if c['all_single_cycle_returns'])
        ret['side_vertices'] = []
    path = ROOT / 'negative' / (name + '.json')
    with path.open('x') as f:
        json.dump(bad, f, separators=(',', ':'), sort_keys=True)
        f.write('\n')
    run(name, ('--certificate', path), expected=1)
run('exclusive-create', ('--write',), expected=1)
assert hashlib.sha256(certificate.read_bytes()).hexdigest() == baseline

# An independent, direct ordinary vertex-Kempe replay on the first full graph.
# This uses the stored graph but not the dual-cycle checker or its routines.
c = data['controls'][0]
vertices, edges, pins = c['vertices'], c['edges'], c['pins']
rows = {tuple(r) for r in c['all_full_J_colourings']}
index = {v: i for i, v in enumerate(vertices)}
event = lambda r: not {r[index[pins[x]]] for x in 'pq'} & {r[index[pins[x]]] for x in 'vw'}
moves = 0
for row in sorted(rows):
    if event(row):
        continue
    for pair in itertools.combinations(range(4), 2):
        active = {v for v in vertices if row[index[v]] in pair}
        while active:
            seen, stack = set(), [min(active)]
            while stack:
                v = stack.pop()
                if v in seen:
                    continue
                seen.add(v)
                for a, b in edges:
                    w = b if a == v else a if b == v else None
                    if w in active and w not in seen:
                        stack.append(w)
            active -= seen
            changed = tuple(pair[0] + pair[1] - x if v in seen else x
                            for v, x in zip(vertices, row))
            assert changed in rows and not event(changed)
            moves += 1
triangles = {tuple(t) for t in itertools.combinations(vertices, 3)
             if all(sorted(e) in edges for e in itertools.combinations(t, 2))}
assert triangles == {tuple(sorted(f)) for f in c['faces']}
seal = json.loads((REPO / 'audits/2026-10-15-route-round3-6ddea32/BASE.json').read_text())
drift = [p for p, expected in seal['prior_file_hashes'].items()
         if hashlib.sha256((REPO / p).read_bytes()).hexdigest() != expected]
assert not drift
report = {'receipts': receipts, 'certificate_sha256': baseline,
          'icosahedral_direct_ordinary_Kempe_moves_from_E_free': moves,
          'icosahedral_E_free_states': 216, 'icosahedral_triangle_count': len(triangles),
          'prior_files_checked': len(seal['prior_file_hashes']), 'prior_file_drift': drift,
          'source_status': 'not triggered', 'general_319_exclusion': 'OPEN'}
with (ROOT / 'VERIFICATION.json').open('x') as f:
    json.dump(report, f, indent=2, sort_keys=True)
    f.write('\n')
print(json.dumps(report, sort_keys=True))
