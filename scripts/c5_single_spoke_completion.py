#!/usr/bin/env python3
"""Replay exterior-path completion and refine the existing single-spoke table.

Arbitrary-size path extraction and disk coverage are paper arguments.  This
checks the inherited finite cover and named support implications, not sources.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from c5_single_spoke_cores import PI, Q, RHO, TARGETS, reflect
from c5_two_spoke_middle_21 import forbidden, relation

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_single_spoke_completion/observations.json'
SUPPORT_SOURCE = ROOT / 'artifacts/c5_single_spoke_cores/observations.json'
COMPLETION_SOURCE = ROOT / 'artifacts/c5_two_spoke_nonadjacent/observations.json'


def audit_completion(data):
    """Check exhaustive attachments and both full tuples in the inherited cover."""
    forms = (
        ('triangle', (6, 7), {(6, 7)}),
        ('two_triangles', tuple(range(6, 11)),
         {(6, 7), (6, 8), (8, 9), (8, 10), (9, 10)}),
    )
    expected = set()
    for name, vs, es in forms:
        options = [tuple(combinations((1, 2, 3, 4),
                   4 - sum(v in e for e in es) - int(v in (6, 7)))) for v in vs]
        expected.update((name, aa) for aa in product(*options))
    seen, counts = set(), Counter()
    for r in data['completion_forms']:
        vs, es = r['vertices'], {tuple(e) for e in r['edges']}
        name, template_vs, template_es = next(f for f in forms if f[0] == r['kind'])
        assert tuple(vs) == template_vs and es == template_es
        assert r['ordered_contacts'] == [6, 7]
        att = {int(v): ns for v, ns in r['attachments'].items()}
        key = (name, tuple(tuple(att[v]) for v in vs))
        assert key in expected and key not in seen
        seen.add(key)
        for row, prefix in ((Q, 'q'), (TARGETS[1], 'p')):
            rel = relation(vs, es, att, [6, 7], row)
            assert rel == [tuple(t) for t in r[prefix + '_tuples']]
            assert forbidden(rel) == r[prefix + '_forbidden']
            # Reversal acts on both coordinates of the whole relation.
            assert relation(vs, es, att, [7, 6], row) == sorted((y, x) for x, y in rel)
        assert not (r['q_forbidden'] in ([0], [3]) and r['p_forbidden'] == [0, 3])
        counts[name] += 1
    assert seen == expected and len(seen) == 3492
    return dict(counts)


def exterior_routes(r):
    """Two paths use distinct actual components, or the original spoke."""
    if 0 in r['supports'][0] or list(r['bans'][0]) not in ([0], [3]):
        return None
    choices = []
    for b in (1, 4):
        paths = ([dict(kind='spoke', boundary=b)] if r['spoke'] == b else [])
        paths += [dict(kind='component', component=j, boundary=b)
                  for j in (1, 2) if b in r['supports'][j]]
        choices.append(paths)
    for pair in product(*choices):
        components = [p['component'] for p in pair if p['kind'] == 'component']
        if len(components) == len(set(components)):
            return list(pair)
    return None


def verify_routes(r, paths):
    assert [p['boundary'] for p in paths] == [1, 4]
    used = set()
    for p in paths:
        if p['kind'] == 'spoke':
            assert p['boundary'] == r['spoke']
        else:
            j = p['component']
            assert j in (1, 2) and j not in used
            assert p['boundary'] in r['supports'][j]
            used.add(j)


def refine(r, target):
    old = r['targets'][target]
    # p1 is handled solely by the existing graph/relation reflection and
    # T(p1)=(0 2)p2; there is no reflected completion enumeration.
    frame = r if target == 1 else reflect(r)
    routes = exterior_routes(frame)
    excluded = ({0, 3} if target == 1 else {2, 3}) if routes else set()
    if routes:
        verify_routes(frame, routes)
    possible = set()
    bounds = []
    for item in old['known']:
        f = set(item['forbidden'])
        if item['component'] == 0:
            assert not f & excluded
        possible.update(f)
    for item in old['unknown_bounds']:
        bound = set(item['possible_forbidden'])
        if item['component'] == 0:
            bound -= excluded
        bounds.append(dict(component=item['component'], forbidden_upper_bound=sorted(bound)))
        possible.update(bound)
    allowed = sorted(set(old['available']) - possible)
    status = 'accept' if allowed else 'unresolved'
    assert old['status'] != 'reject'
    assert old['status'] != 'accept' or status == 'accept'
    return dict(row=old['row'], status=status, prior_status=old['status'],
                known=old['known'], bounds=bounds, guaranteed_z_colors=allowed,
                completion=None if routes is None else dict(
                    reflected=target == 0, component=0, routes=routes,
                    frame_spoke=frame['spoke'], frame_supports=frame['supports'],
                    frame_bans=frame['bans'], excluded_original_colors=sorted(excluded)))


def build():
    sigma = (2, 1, 0, 3)
    assert tuple(PI[Q[RHO[i]]] for i in range(5)) == Q
    assert tuple(PI[TARGETS[0][RHO[i]]] for i in range(5)) == tuple(sigma[c] for c in TARGETS[1])
    assert {PI[sigma[c]] for c in (0, 3)} == {2, 3}
    source = json.loads(SUPPORT_SOURCE.read_text())
    audit = audit_completion(json.loads(COMPLETION_SOURCE.read_text()))
    records, counts, groups, role_flags = [], Counter(), {}, {}
    new_queries = 0
    for index, r in enumerate(source['records']):
        if 'targets' not in r:
            continue
        targets = [refine(r, t) for t in (0, 1)]
        flags = tuple(e['status'] == 'accept' for e in targets)
        name = {(True, True): 'both', (True, False): 'p1_only',
                (False, True): 'p2_only', (False, False): 'neither'}[flags]
        counts[name] += 1
        new_queries += sum(e['status'] == 'accept' and e['prior_status'] != 'accept' for e in targets)
        records.append(dict(source_index=index, spoke=r['spoke'], bans=r['bans'],
                            supports=r['supports'], placements=r['placements'], targets=targets))
        ordered = sorted(zip(r['bans'], r['supports']))
        key = (r['spoke'], tuple(tuple(f) for f, _ in ordered),
               tuple(tuple(s) for _, s in ordered))
        role_key = (key, r['bans'][0][0])
        assert role_flags.setdefault(role_key, flags) == flags
        group = groups.setdefault(key, [set(), set()])
        for t in (0, 1):
            if flags[t]:
                group[t].add(r['bans'][0][0])
    assert len(records) == 114 and len(groups) == 19
    assert counts == {'both': 62, 'p1_only': 20, 'p2_only': 32}
    assert new_queries == 30
    table = [dict(spoke=k[0], bans=k[1], supports=k[2],
                  p1_two_contact_roles=sorted(v[0]), p2_two_contact_roles=sorted(v[1]))
             for k, v in sorted(groups.items())]
    paths = [SUPPORT_SOURCE, COMPLETION_SOURCE, Path(__file__),
             ROOT / 'scripts/c5_single_spoke_cores.py',
             ROOT / 'scripts/c5_two_spoke_middle_21.py']
    return dict(schema=1, scope='necessary support implications; source coverage is paper proof',
                source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths},
                completion_cover=audit, counts=dict(counts), new_accepted_queries=new_queries,
                support_table=table, records=records)


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
    print(json.dumps(dict(counts=result['counts'], new_queries=result['new_accepted_queries']), sort_keys=True))


if __name__ == '__main__':
    main()
