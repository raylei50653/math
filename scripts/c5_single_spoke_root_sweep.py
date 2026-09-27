#!/usr/bin/env python3
"""Sweep the single-root unused-colour condition over the 114 named rows.

For a single-contact component C with F_C(q)={a} and target p, every colour
d != a that neither q nor p shows on the actual support S_C is not in F_C(p)
(report c5_single_spoke_root_conservation.md, section 2).  This removes such d
from the inherited upper bounds; the arbitrary-size proof is on paper.
"""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

from c5_single_spoke_cores import PI, Q, RHO, reflect

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_single_spoke_root_sweep/observations.json'
TABLE = ROOT / 'artifacts/c5_single_spoke_root_conservation/observations.json'
COMPLETION = ROOT / 'artifacts/c5_single_spoke_completion/observations.json'
NAMES = {(True, True): 'both', (True, False): 'p1_only',
         (False, True): 'p2_only', (False, False): 'neither'}


def root_exclusions(r, j, p):
    """Colours excluded from F_Cj(p) by the single-root lemma."""
    assert j in (1, 2)  # component 0 is the two-contact block
    a, = r['bans'][j]
    seen = {Q[i] for i in r['supports'][j]} | {p[i] for i in r['supports'][j]}
    return {d for d in range(4) if d != a and d not in seen}


def sweep(r, c, t):
    target = c['targets'][t]
    p = target['row']
    available = set(range(4)) - {p[r['spoke']]}
    possible, bounds = set(), []
    for item in target['known']:
        possible.update(item['forbidden'])
    for item in target['bounds']:
        j = item['component']
        old = set(item['forbidden_upper_bound'])
        cut = root_exclusions(r, j, p) & old if j != 0 else set()
        possible.update(old - cut)
        bounds.append(dict(component=j, inherited_upper_bound=sorted(old),
                           root_excluded=sorted(cut), forbidden_upper_bound=sorted(old - cut)))
    return dict(row=p, known=target['known'], bounds=bounds,
                guaranteed_z_colors=sorted(available - possible))


def build():
    table = json.loads(TABLE.read_text())['table']['records']
    completion = {r['source_index']: r for r in json.loads(COMPLETION.read_text())['records']}
    assert len(table) == 114
    records, counts, new = [], Counter(), {0: [], 1: []}
    for r in table:
        c = completion[r['source_index']]
        assert (r['spoke'], r['bans'], r['supports']) == (c['spoke'], c['bans'], c['supports'])
        prior = r['accepted_targets']
        flags, targets = [], []
        for t in (0, 1):
            e = sweep(r, c, t)
            swept = bool(e['guaranteed_z_colors'])
            if not prior[t] and swept:
                new[t].append(r['source_index'])
            e.update(prior_accept=prior[t], sweep_accept=swept, accept=prior[t] or swept)
            flags.append(e['accept'])
            targets.append(e)
        counts[NAMES[tuple(flags)]] += 1
        records.append(dict(source_index=r['source_index'], spoke=r['spoke'], bans=r['bans'],
                            supports=r['supports'], placements=r['placements'],
                            targets=targets))
    # The sweep alone re-derives every earlier acceptance except the two
    # branch-minor p1 queries, which rest on the separate K5 argument.
    lost = [(r['source_index'], t) for r in records for t in (0, 1)
            if r['targets'][t]['prior_accept'] and not r['targets'][t]['sweep_accept']]
    assert lost == [(24, 0), (29, 0)]
    assert new == {0: [61, 72, 78, 88, 154, 172, 181, 202], 1: [14, 18, 112, 131, 193, 212]}
    assert counts == {'both': 80, 'p1_only': 12, 'p2_only': 22}
    # Reflection consistency: T fixes q, swaps the two targets, maps s=4 to s=4.
    key = {(r['spoke'], tuple(map(tuple, r['bans'])), tuple(map(tuple, r['supports']))): r
           for r in records}
    checked = 0
    for r in records:
        m = reflect(r)
        image = key.get((m['spoke'], tuple(m['bans']), tuple(m['supports'])))
        if image is None:
            assert r['spoke'] in (0, 1)  # reflected sides s=3, 2 are transport only
            continue
        assert [e['accept'] for e in r['targets']] == [e['accept'] for e in image['targets']][::-1]
        checked += 1
    assert checked == 72
    # Role table: which two-contact roles now accept each target, per support type.
    groups = {}
    for r in records:
        ordered = sorted(zip(r['bans'], r['supports']))
        k = (r['spoke'], tuple(tuple(f) for f, _ in ordered), tuple(tuple(s) for _, s in ordered))
        g = groups.setdefault(k, [set(), set(), set()])
        g[2].add(r['bans'][0][0])
        for t in (0, 1):
            if r['targets'][t]['accept']:
                g[t].add(r['bans'][0][0])
    assert len(groups) == 19
    roles = [dict(spoke=k[0], bans=k[1], supports=k[2], two_contact_roles=sorted(v[2]),
                  p1_accepted_roles=sorted(v[0]), p2_accepted_roles=sorted(v[1]))
             for k, v in sorted(groups.items())]
    open_queries = [dict(source_index=r['source_index'], target=('p1', 'p2')[t])
                    for r in records for t in (0, 1) if not r['targets'][t]['accept']]
    assert len(open_queries) == 34
    paths = [TABLE, COMPLETION, Path(__file__), ROOT / 'scripts/c5_single_spoke_cores.py']
    return dict(scope='necessary upper bounds on named rows; arbitrary-size lemma in report',
                source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                               for p in paths},
                counts=dict(counts), newly_accepted=dict(p1=new[0], p2=new[1]),
                reflection_pairs_checked=checked, role_table=roles,
                open_queries=open_queries, records=records)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    payload = json.dumps(result, sort_keys=True, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == payload, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(dict(counts=result['counts'], newly_accepted=result['newly_accepted'],
                          reflection_pairs=result['reflection_pairs_checked']), sort_keys=True))


if __name__ == '__main__':
    main()
