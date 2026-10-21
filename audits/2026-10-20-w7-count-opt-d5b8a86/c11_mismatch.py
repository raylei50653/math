#!/usr/bin/env python3
"""Full mismatch of the direct C11 deletion pullback on the W7 cone (discovery only).

Same pullback as counting/tensor_control.py: delete u4,u3 (positions 2,3) from each
C13 half-row, take the frozen 132-term lambda on proper C11 projections, 0 elsewhere.
Column side r_j = 4 * sum of pulled lambda over column j (all 307,197 columns).
Z side w_s = sum of pulled lambda over the three half-rows of live state s.
Nonzero r_j are classified by the (u4,u3) colours and proper flags of their half-rows.
"""
import gzip
import importlib.util
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
CNT = HERE.parents[0] / '2026-10-20-r6-941-j1-five-edge-417732f/counting'
sp = importlib.util.spec_from_file_location('orbits', CNT / 'orbits.py')
o = importlib.util.module_from_spec(sp)
sp.loader.exec_module(o)
F = CNT.parent / 'frozen/audits/2026-10-20-r6-941-j1-c11-1148ce0'
cert = json.loads((F / 'reduction/reduced-orbit-certificate.json').read_text())
hrows = sorted(o.rowmap(list(o.c.proper_growth(11))))
lam = {hrows[h]: v for h, v in cert['live_half_row_multipliers']}
K = json.load(gzip.open(CNT / 'orbits.json.gz', 'rt'))
live = set(K['live'])


def decode(x, n):
    out = [0] * n
    for i in range(n - 1, -1, -1):
        out[i] = x & 3
        x >>= 2
    return tuple(out)


pulled, tag, state = {}, {}, {}
for row, s in K['rowids']:
    t = decode(row, 13)
    p = t[:2] + t[4:]
    prop = o.c.m.proper(p)
    pulled[row] = lam.get(o.encode(o.half(p)), 0) if prop else 0
    tag[row] = (t[2], t[3], int(prop), int(pulled[row] != 0))
    state[row] = s

r = [4 * sum(pulled[h] for h in col) for col in K['columns']]
w = Counter()
for row, s in K['rowids']:
    if s in live:
        w[s] += pulled[row]
nz = [j for j, v in enumerate(r) if v]
classes = Counter()
for j in nz:
    classes[(r[j], tuple(sorted(Counter(tag[h] for h in K['columns'][j]).items())))] += 1
touch = Counter(any(pulled[h] for h in col) for col in K['columns'])
out = {
    'columns': len(r), 'nonzero_columns': len(nz),
    'value_histogram': sorted(Counter(r[j] for j in nz).items()),
    'columns_touching_nonzero_lambda': touch[True],
    'nonzero_states_in_mismatch': len({state[h] for j in nz for h in K['columns'][j]}),
    'z_side_nonzero_live_states': sum(1 for s in live if w[s]),
    'z_side_histogram': sorted(Counter(w[s] for s in live if w[s]).items()),
    'z_side_targets': {str(s): w[s] for s in (44459, 44466)},
    'mismatch_classes': len(classes),
    'top_classes': [[v, [list(k) + [c] for k, c in pat], n]
                    for (v, pat), n in classes.most_common(15)],
}
(HERE / 'logs/c11-mismatch.json').write_text(json.dumps(out, indent=1) + '\n')
print(json.dumps({k: v for k, v in out.items() if k != 'top_classes'}, indent=1))
for v, pat, n in out['top_classes']:
    print(n, v, pat)
