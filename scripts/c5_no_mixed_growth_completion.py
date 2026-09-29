#!/usr/bin/env python3
"""Replay explicit arc recipes for the paper no-mixed growth completion.

No support catalogue is generated. Old acceptance and exclusion flags are not
used. Complete original records remain bound by pointers and hashes. The new
screen deliberately keeps some harmless pairs excluded by the stronger screen.
"""

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import sys

from c5_no_mixed_no_growth import Q, U, TARGETS, options, geometry, digest, invariant_options
from c5_adjacent_degree5_no_mixed_t2_t1_bridge import external_routes, minor_control as bridge_control
from c5_adjacent_degree5_no_mixed_t2_t1_endpoints import minor_control as endpoint_control

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'artifacts/c5_no_mixed_root_transport/observations.json'
OUT = ROOT / 'artifacts/c5_no_mixed_growth_completion/observations.json'
P = TARGETS[1]
RHO = (3, 2, 1, 0, 4)
IDENTITY = tuple(range(4))
# Whole-row maps, not independent component permutations.
SOURCE_MAP = (1, 0, 2, 3)
TARGET_MAP = (1, 2, 0, 3)
PARTS = {
    '01': ((0,), (1,), (2, 3, 4)),
    '04': ((0,), (4,), (1, 2, 3)),
    '014': ((0, 1), (4,), (2, 3)),
    '23': ((2,), (3,), (4, 0, 1)),
    '34': ((3,), (4,), (0, 1, 2)),
    '4_123': ((4,), (1, 2, 3), (0,)),
}


def normalize(record, ti):
    vertex = RHO if ti == 0 else tuple(range(5))
    source_color = SOURCE_MAP if ti == 0 else IDENTITY
    target_color = TARGET_MAP if ti == 0 else IDENTITY
    assert tuple(source_color[Q[vertex[i]]] for i in range(5)) == Q
    assert tuple(target_color[TARGETS[ti][vertex[i]]] for i in range(5)) == P
    ctx = dict(record_id=record['record_id'], root_boundary={
        r: sorted(vertex[h] for h in hs) for r, hs in record['root_boundary'].items()},
        components=[dict(name=c['name'], root=c['root'],
                         support=sorted(vertex[h] for h in c['support']),
                         contacts=c['contacts'],
                         source_forbidden=sorted(source_color[a] for a in c['Fq']))
                    for c in record['components']])
    return ctx, vertex, source_color, target_color


def residuals(ctx, row, Fs, omit=None):
    return {r: U - {row[h] for h in ctx['root_boundary'][r]}
            - set().union(*(set(F) for k, (c, F) in enumerate(zip(ctx['components'], Fs, strict=True))
                            if c['root'] == r and k != omit)) for r in ('z', 'w')}


def pairs(E):
    return sorted([a, b] for a, b in product(E['z'], E['w']) if a != b)


def bags(S, d, beta, D):
    # For a pair and a three-color row, invariance says that the row sees
    # the pair if it omits 3, and its complement if it contains 3.
    source_need = {d, beta} if 3 not in (d, beta) else U - {d, beta}
    target_need = set(D) if 3 not in D else U - set(D)
    return [list(T) for n in range(len(S) + 1) for T in combinations(S, n)
            if source_need <= {Q[h] for h in T} and target_need <= {P[h] for h in T}]


def frame(ctx, k, family, key, mode, landing):
    if not family:
        return dict(reason='empty_bag_family', supports=[])
    X, Y, outside = PARTS[key]
    assert all(set(T) & set(X) and set(T) & set(Y) for T in family)
    routes = [route for route in external_routes(ctx, k)
              if route['landing'] in outside and route['landing'] == landing]
    assert routes, (ctx, key)
    witness = dict(frame_arcs=[list(X), list(Y), list(outside)], route=routes[0])
    control = endpoint_control if mode == 'endpoints' else bridge_control
    lengths = (1, 3, 5) if mode == 'endpoints' else (1,)
    skeletons = [dict(length=n, sha256=digest(control(ctx, k, witness, length=n))) for n in lengths]
    return dict(reason='fixed_frame_original_path', supports=family, partition=key,
                witness=witness, skeleton_controls=skeletons)


def recipe(ctx, k, D, window):
    c = ctx['components'][k]
    S, d = c['support'], c['source_forbidden'][0]
    assert 2 in S and ({0, 4} & set(S))
    assert window in ('234', '1234', '4012')
    K = {a for a in U if all((Q[h] == a) == (P[h] == a) for h in S)}
    assert K == {1, 3}
    conserved = d in K
    exterior = {route['landing'] for route in external_routes(ctx, k)}
    landing = (3 if window == '4012' else 0 if window == '1234'
               else min(exterior & {0, 1}))
    assert landing in exterior
    result = dict(component=c['name'], root=c['root'], support=S, source_ban=[d],
                  target_pair=list(D), window=window, fixed_colors=sorted(K), conserved=conserved)
    if window == '4012':
        assert d in (1, 3)
    if window == '234':
        assert S == [2, 3, 4] and d in (1, 3)
    if window == '1234' and 1 in S:
        assert set(ctx['root_boundary'][c['root']]) == {1, 4} and d in (0, 3)
    if conserved and d not in D:
        return result | dict(reason='conserved_color_absent', excluded=True)
    cases = [(b, bags(S, d, b, D)) for b in sorted(U - {d})
             if {d, b} & K == set(D) & K]
    if not conserved:
        assert window == '1234' and d in (0, 2)
        assert set(D) in ({0, 3}, {1, 2})
        if set(D) == {1, 2}:
            return result | dict(reason='harmless_seen_pair', excluded=False)
        family = sorted({tuple(T) for b, Ts in cases for T in Ts})
        assert [b for b, Ts in cases] == [3]
        key = '4_123' if d == 0 else '23'
        ev = frame(ctx, k, family, key, 'endpoints', landing)
        return result | dict(reason='nonconserved_endpoints', excluded=True, endpoint_frame=ev)
    evidence, surviving = [], []
    for b, family in cases:
        key = None
        if window == '4012':
            if set(D) in ({0, 1}, {2, 3}):
                key = '01'
            elif set(D) == {1, 3}:
                key = '04'
            else:
                assert set(D) in ({1, 2}, {0, 3})
                if {d, b} in ({1, 2}, {0, 3}):
                    key = '014'
        elif set(S) <= {2, 3, 4}:
            key = '23' if {d, b} in ({0, 1}, {2, 3}) else '34'
        else:
            assert window == '1234' and d == 3 and set(D) == {0, 3}
            if b == 0:
                key = '4_123'
        ev = dict(beta=b, supports=family)
        if key is not None or not family:
            ev['frame'] = frame(ctx, k, family, key, 'odd_bridge', landing)
        else:
            surviving.append(b)
        evidence.append(ev)
    assert len(surviving) <= 1
    return result | dict(reason='unique_beta_palette_switch' if surviving else 'all_odd_betas_excluded',
                         excluded=True, beta_cases=evidence, surviving_betas=surviving)


def algebra_controls():
    count = 0
    for row in (Q, P):
        for D in combinations(range(4), 2):
            for n in range(6):
                for S in combinations(range(5), n):
                    need = set(D) if 3 not in D else U - set(D)
                    assert (need <= {row[h] for h in S}) == (
                        D in invariant_options(tuple(sorted({row[h] for h in S})), 2))
                    count += 1
    return dict(pair_stabilizer_controls=count)


def build():
    raw = SOURCE.read_bytes()
    data = json.loads(raw)
    inputs = {str(SOURCE.relative_to(ROOT)): sha256(raw).hexdigest(), **data['inputs_sha256']}
    for path, expected in inputs.items():
        assert sha256((ROOT / path).read_bytes()).hexdigest() == expected, path
    controls = algebra_controls()
    counts, families, rules, queries, anchors = Counter(), {}, [], [], {}
    for ri, record in enumerate(data['records']):
        geos = [geometry(record, pl) for pl in record['placements']]
        for ti, row in enumerate(TARGETS):
            ctx, vertex, source_color, target_color = normalize(record, ti)
            source_Fs = [c['source_forbidden'] for c in ctx['components']]
            Eq = residuals(ctx, Q, source_Fs)
            assert len(Eq['z']) == 1 and Eq['z'] == Eq['w']
            for r in ('z', 'w'):
                assert len(ctx['root_boundary'][r]) + sum(
                    len(c['source_forbidden']) for c in ctx['components'] if c['root'] == r) == 3
            original_domains = [options(tuple(c['support']), tuple(c['Fq']), c['ports'], row)
                                for c in record['components']]
            domains = [tuple(tuple(sorted(target_color[a] for a in F)) for F in domain)
                       for domain in original_domains]
            saved = [tuple(tuple(j['F_by_component'][c['name']]) for c in record['components'])
                     for j in record['targets'][ti]['candidates']]
            assert len(saved) == len(set(saved)) and set(saved) == set(product(*original_domains))
            local = {}
            for k, c in enumerate(ctx['components']):
                for D in domains[k]:
                    if len(D) <= len(c['source_forbidden']):
                        continue
                    assert len(D) == 2 and len(c['source_forbidden']) == 1 and len(c['contacts']) == 2
                    # Verify the classification in every saved common lift.
                    witnesses = []
                    for geo in geos:
                        lo, hi = geo['side_intervals'][c['root']]
                        arc = {vertex[(geo['anchor'] + x) % 5] for x in range(lo, hi + 1)}
                        window = next(w for w in ('234', '1234', '4012') if arc == set(map(int, w)))
                        ll = next(u['lifts'] for u in geo['ordered_units'] if u['name'] == c['name'])
                        assert max(ll) - min(ll) >= 2
                        assert record['family'][('z', 'w').index(c['root'])] in ('A', 'B')
                        if hi - lo == 3:
                            other = 'w' if c['root'] == 'z' else 'z'
                            other_actual = set(ctx['root_boundary'][other]).union(*(
                                set(cc['support']) for cc in ctx['components'] if cc['root'] == other))
                            assert ({2, 3, 4} if window == '4012' else {4, 0, 1}) <= other_actual
                        ev = recipe(ctx, k, D, window)
                        ev['owner_side_arc'] = sorted(arc)
                        ev['component_span'] = max(ll) - min(ll)
                        witnesses.append(ev)
                    ev = witnesses[0]
                    assert all(w['excluded'] == ev['excluded'] for w in witnesses)
                    if not ev['excluded']:
                        assert all(len(domain) == 1 for j, domain in enumerate(domains) if j != k)
                        Fs = [domain[0] for domain in domains]
                        R = residuals(ctx, P, Fs, omit=k)
                        root, other = c['root'], 'w' if c['root'] == 'z' else 'z'
                        assert R[root] == {0, 3} and R[other] == {3} and not set(D) & R[root]
                        ev['harmless_gate'] = dict(R={r: sorted(v) for r, v in R.items()},
                                                   all_other_components_transported=True)
                    idx = len(rules)
                    rules.append(dict(family=record['family'], record_id=record['record_id'], target=ti+1,
                        input_record_pointer=f'/records/{ri}', input_record_sha256=digest(record),
                        source_color_map=source_color, target_color_map=target_color, vertex_map=vertex,
                        evidence=ev, all_common_lifts_sha256=digest(witnesses)))
                    local[k, D] = idx
                    counts['growth_cases'] += 1
                    counts[ev['reason']] += 1
            kept, excluded = [], []
            for ji, original_Fs in enumerate(saved):
                Fs = [tuple(sorted(target_color[a] for a in F)) for F in original_Fs]
                hits = [local[k, D] for k, D in enumerate(Fs) if (k, D) in local]
                bad = [i for i in hits if rules[i]['evidence']['excluded']]
                E = residuals(ctx, P, Fs)
                canonical_pairs = pairs(E)
                if bad:
                    excluded.append([ji, bad[0]])
                else:
                    assert canonical_pairs
                    inv = {a: i for i, a in enumerate(target_color)}
                    actual_pair = [inv[a] for a in canonical_pairs[0]]
                    original_ctx = normalize(record, 1)[0]
                    actual_E = residuals(original_ctx, row, original_Fs)
                    assert actual_pair in pairs(actual_E)
                    kept.append([ji, actual_pair])
                    counts['kept_growth_joins' if hits else 'no_growth_joins'] += 1
                if not canonical_pairs:
                    assert bad
                    counts['old_bad_joins_recomputed'] += 1
                if (record['family'], record['record_id'], ti + 1, ji) in (
                        ('AA', 54, 1, 4), ('AB', 22, 2, 4)):
                    assert bad
                    anchors[record['family'] + str(record['record_id'])] = dict(
                        join=ji, target=ti+1, excluding_rules=bad)
            counts.update(queries=1, joins=len(saved), excluded_joins=len(excluded), kept_joins=len(kept))
            fc = families.setdefault(record['family'], Counter())
            fc.update(queries=1, joins=len(saved), excluded_joins=len(excluded), kept_joins=len(kept))
            queries.append(dict(family=record['family'], record_id=record['record_id'], target=ti+1,
                input_pointer=f'/records/{ri}/targets/{ti}', original_domain_sha256=digest(saved),
                local_rules=sorted(local.values()), excluded_joins_and_rule=excluded,
                kept_joins_and_original_root_pair=kept))
    assert counts['growth_cases'] == 2240 and counts['queries'] == 4164 and counts['joins'] == 11096
    assert counts['no_growth_joins'] == 7848 and counts['old_bad_joins_recomputed'] == 434
    assert counts['harmless_seen_pair'] == counts['kept_growth_joins'] == 230
    assert counts['kept_joins'] == 8078 and counts['excluded_joins'] == 3018
    assert any(rules[i]['evidence']['reason'] == 'unique_beta_palette_switch'
               for i in anchors['AA54']['excluding_rules'])
    assert any(rules[i]['evidence']['reason'] == 'nonconserved_endpoints'
               for i in anchors['AB22']['excluding_rules'])
    frames = [f for rule in rules for ev in [rule['evidence']] for f in
              ([b['frame'] for b in ev.get('beta_cases', []) if 'frame' in b] +
               ([ev['endpoint_frame']] if 'endpoint_frame' in ev else []))]
    counts['minor_skeleton_controls'] = sum(len(f.get('skeleton_controls', [])) for f in frames)
    for path, expected in inputs.items():
        assert sha256((ROOT / path).read_bytes()).hexdigest() == expected
    scripts = {}
    for module in tuple(sys.modules.values()):
        path = Path(getattr(module, '__file__', '') or '/nonexistent').resolve()
        if path.is_file() and path.is_relative_to(ROOT / 'scripts'):
            scripts[str(path.relative_to(ROOT))] = sha256(path.read_bytes()).hexdigest()
    scripts[str(Path(__file__).resolve().relative_to(ROOT))] = sha256(Path(__file__).read_bytes()).hexdigest()
    return dict(schema=1, scope='explicit paper arc recipes; finite replay, no new accepts or source exclusions; '
                'not a coloring-level repair, realizability, full Sigma, general exit or Lean theorem',
                inputs_sha256=inputs, scripts_sha256=scripts, summary=dict(counts), families=families,
                algebra_controls=controls, controls=anchors, local_rules=rules, queries=queries)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build()
    raw = (json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()
    if args.check:
        assert OUT.read_bytes() == raw, f'stale artifact: {OUT}'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_bytes(raw)
    print(json.dumps(dict(summary=data['summary'], families=data['families'],
                          algebra_controls=data['algebra_controls']), sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
