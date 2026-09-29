#!/usr/bin/env python3
"""Uniform local growth screen over the existing no-mixed necessary supports.

Recompute local endpoint/palette evidence; never trust saved target acceptance
or exclusion flags. Original complete relations and geometries remain inputs.
This is finite coverage of conditional paper rules, not a table-free repair.
"""

import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path
import sys

from c5_adjacent_degree5_no_mixed_t2_t1_bridge import frame_evidence, minor_control as bridge_control
from c5_adjacent_degree5_no_mixed_t2_t1_endpoints import minor_control as endpoint_control
from c5_single_spoke_first_bridge import fixed_colors
from c5_single_spoke_frame_arc import admissible_supports

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'artifacts/c5_no_mixed_root_transport/observations.json'
OUT = ROOT / 'artifacts/c5_no_mixed_local_screen/observations.json'
Q = (0, 1, 0, 1, 2)
U = frozenset(range(4))
PERMS = tuple(permutations(range(4)))


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def subsets(values):
    return tuple(tuple(s) for n in range(len(values) + 1) for s in combinations(values, n))


@lru_cache(None)
def options(support, source_ban, ports, row):
    pp = [pi for pi in PERMS if all(pi[Q[h]] == row[h] for h in support)]
    if pp:
        images = {tuple(sorted(pi[a] for a in source_ban)) for pi in pp}
        assert len(images) == 1
        return tuple(sorted(images))
    stabilizer = [pi for pi in PERMS if all(pi[row[h]] == row[h] for h in support)]
    return tuple(F for F in subsets(tuple(range(4))) if len(F) <= ports
                 and all({pi[a] for a in F} == set(F) for pi in stabilizer))


def context(record):
    return dict(record_id=record['record_id'], root_boundary=record['root_boundary'],
                components=[dict(name=c['name'], root=c['root'], support=c['support'],
                                 contacts=c['contacts'], source_forbidden=c['Fq'])
                            for c in record['components']])


def residuals(ctx, row, Fs):
    return {r: U - {row[h] for h in ctx['root_boundary'][r]}
            - set().union(*(set(F) for c, F in zip(ctx['components'], Fs, strict=True)
                            if c['root'] == r)) for r in ('z', 'w')}


def root_pairs(E):
    return sorted([a, b] for a, b in product(E['z'], E['w']) if a != b)


def compact_frame(ctx, k, family, mode):
    """A fixed partition must work for ALL bags, before choosing a route."""
    family = sorted(set(family), key=lambda T: (len(T), sorted(T)))
    ev = frame_evidence(ctx, k, family)
    result = dict(supports=[sorted(T) for T in family], eliminated=ev['eliminated'],
                  reason=ev['reason'], witness_count=len(ev['witnesses']))
    if ev['witnesses']:
        witness = ev['witnesses'][0]
        # Both recipes retain the original path, contacts and exterior component.
        # The bridge control implements the two-bag recipe, valid at any odd edge.
        control = endpoint_control if mode == 'endpoints' else bridge_control
        lengths = (1, 3, 5) if mode == 'endpoints' else (1,)
        skeletons = [control(ctx, k, witness, length=n) for n in lengths]
        result.update(witness=witness, all_witnesses_sha256=digest(ev['witnesses']),
                      skeleton_controls=[dict(length=s['length'], sha256=digest(s)) for s in skeletons])
    return result


def local_rule(ctx, row, k, pair):
    comp = ctx['components'][k]
    assert len(comp['contacts']) == 2 and len(comp['source_forbidden']) == 1 and len(pair) == 2
    d = comp['source_forbidden'][0]
    support = tuple(comp['support'])
    K = fixed_colors(Q, row, support)
    result = dict(component=comp['name'], root=comp['root'], contacts=comp['contacts'],
                  support=comp['support'], source_ban=[d], target_pair=pair,
                  fixed_colors=sorted(K), conserved=d in K)
    if d in K and d not in pair:
        return result | dict(eliminated=True, reason='conserved_color_absent')
    target = admissible_supports(row, support, pair)
    cases, union, surviving = [], set(), []
    for beta in sorted(U - {d}):
        R = tuple(sorted((d, beta)))
        if set(R) & K != set(pair) & K:
            continue
        source = admissible_supports(Q, support, R)
        family = tuple(T for T in target if T in source)
        union.update(family)
        case = dict(beta=beta, source_endpoint_residual=R, supports=[sorted(T) for T in family])
        if d in K:
            case['frame'] = compact_frame(ctx, k, family, 'odd_bridge')
            if not case['frame']['eliminated']:
                surviving.append(beta)
        cases.append(case)
    result['beta_cases'] = cases
    if d in K:
        # Source tightness plus fixed-d induction applies on EVERY odd bridge.
        # A unique surviving beta permits the whole-path palette interchange.
        result.update(surviving_betas=surviving, eliminated=len(surviving) <= 1,
                      reason=('all_odd_betas_excluded' if not surviving else
                              'unique_beta_palette_switch' if len(surviving) == 1 else 'unresolved'))
    else:
        # Do not use the conserved odd-bridge induction for nonconserved d.
        # Both ORIGINAL endpoints belong to this union, with independent betas.
        frame = compact_frame(ctx, k, union, 'endpoints')
        result.update(endpoint_frame=frame, eliminated=frame['eliminated'],
                      reason='nonconserved_endpoints' if frame['eliminated'] else 'unresolved')
    return result


def build():
    raw = SOURCE.read_bytes()
    data = json.loads(raw)
    inputs = {str(SOURCE.relative_to(ROOT)): sha256(raw).hexdigest()}
    # Bind the same original schemas, placements, and support identities.
    for path, expected in data['inputs_sha256'].items():
        actual = sha256((ROOT / path).read_bytes()).hexdigest()
        assert actual == expected, path
        inputs[path] = actual
    rules, queries, counts, by_family = [], [], Counter(), {}
    harmless, failures = [], []
    controls = {}
    # Cardinality alone cannot rule out a shared singleton. This is an
    # abstract list control, without target-support compatibility or a disk.
    abstract_E = {r: U - {0, 1, 2} for r in ('z', 'w')}
    assert all(abstract_E.values()) and not root_pairs(abstract_E)
    for ri, record in enumerate(data['records']):
        ctx = context(record)
        family = record['family']
        fc = by_family.setdefault(family, Counter())
        for ti, target in enumerate(record['targets']):
            row = tuple(target['row'])
            domains = [options(tuple(c['support']), tuple(c['Fq']), c['ports'], row)
                       for c in record['components']]
            saved = [tuple(tuple(j['F_by_component'][c['name']]) for c in record['components'])
                     for j in target['candidates']]
            assert len(saved) == len(set(saved)) and set(saved) == set(product(*domains))
            lookup, query_rules = {}, []
            for k, comp in enumerate(record['components']):
                if comp['ports'] != 2 or len(comp['Fq']) != 1:
                    continue
                for pair in domains[k]:
                    if len(pair) != 2:
                        continue
                    rule = local_rule(ctx, row, k, pair)
                    rule.update(family=family, record_id=record['record_id'], target=ti + 1,
                                input_record_pointer=f'/records/{ri}', input_record_sha256=digest(record),
                                input_target_pointer=f'/records/{ri}/targets/{ti}')
                    idx = len(rules)
                    rules.append(rule)
                    lookup[k, pair] = idx
                    query_rules.append(idx)
                    counts['local_growth_cases'] += 1
                    fc['local_growth_cases'] += 1
                    counts['conserved_cases' if rule['conserved'] else 'nonconserved_cases'] += 1
                    counts[rule['reason']] += 1
                    if not rule['eliminated']:
                        harmless.append(idx)
            eliminated, kept, old_bad, no_growth = [], [], [], []
            for ji, (Fs, old) in enumerate(zip(saved, target['candidates'], strict=True)):
                assert old['original_join_index'] == ji
                E = residuals(ctx, row, Fs)
                assert {r: sorted(v) for r, v in E.items()} == old['E']
                pairs = root_pairs(E)
                growth = [lookup[k, F] for k, F in enumerate(Fs) if (k, F) in lookup]
                hits = [idx for idx in growth if rules[idx]['eliminated']]
                if not growth:
                    # The finite no-growth compatibility gate is checked, not assumed.
                    assert all(E.values())  # The paper capacity lemma.
                    assert pairs
                    no_growth.append(ji)
                if not pairs:
                    assert growth and hits
                    conserved_hits = [idx for idx in hits if rules[idx]['conserved']]
                    mechanism = 'conserved' if conserved_hits else 'nonconserved'
                    if mechanism == 'nonconserved':
                        assert (not E['z']) != (not E['w'])
                    counts['old_failures_' + mechanism] += 1
                    fc['old_failures_' + mechanism] += 1
                    old_bad.append(ji)
                    failure = dict(family=family, record_id=record['record_id'], target=ti + 1,
                                   join=ji, growth_rules=growth, excluding_rules=hits,
                                   group=mechanism, input_failure_index=old['failure_index'])
                    failures.append(failure)
                    if (family, record['record_id'], ti + 1) in [('AA', 54, 1), ('AB', 22, 2)]:
                        controls[family + str(record['record_id'])] = failure
                if hits:
                    eliminated.append([ji, hits[0]])
                else:
                    assert pairs
                    kept.append([ji, pairs[0]])
            # Each unresolved LOCAL pair is safe for all OTHER candidate bans,
            # even before using any local exclusions on the opposite root.
            for idx in query_rules:
                rule = rules[idx]
                if rule['eliminated']:
                    continue
                k = next(i for i, c in enumerate(record['components']) if c['name'] == rule['component'])
                root = rule['root']
                other = 'w' if root == 'z' else 'z'
                # These 32 pairs do not remove ANY available root color.
                # This supplies the simple paper sufficiency gate, not just a
                # saved PASS flag for one independently chosen join.
                assert target['D_p'][root] == [rule['component']] and not target['D_p'][other]
                assert len(target['R'][root]) == 2 and target['R'][other] == [3]
                assert not set(rule['target_pair']) & set(target['R'][root])
                rule['harmless_gate'] = dict(R=target['R'], unknown_by_root=target['D_p'],
                    reason='pair_disjoint_from_own_R_and_other_root_known_nonempty')
                containing = [(ji, root_pairs(residuals(ctx, row, Fs))) for ji, Fs in enumerate(saved)
                              if Fs[k] == rule['target_pair']]
                assert containing and all(pairs for _, pairs in containing)
                rule['all_containing_joins_have_root_pair'] = [[ji, pairs[0]] for ji, pairs in containing]
            entry = dict(family=family, record_id=record['record_id'], target=ti + 1,
                         input_pointer=f'/records/{ri}/targets/{ti}',
                         ordered_candidate_domain_sha256=digest(saved), local_rules=query_rules,
                         no_growth_joins=no_growth, old_failing_joins=old_bad,
                         excluded_joins_and_rule=eliminated, surviving_joins_and_root_pair=kept)
            queries.append(entry)
            metrics = dict(queries=1, joins=len(saved), old_failures=len(old_bad),
                           no_growth_joins=len(no_growth), excluded_joins=len(eliminated),
                           surviving_joins=len(kept))
            counts.update(metrics)
            fc.update(metrics)
    assert counts['queries'] == 4164 and counts['joins'] == 11096
    assert counts['old_failures'] == 434
    assert counts['local_growth_cases'] == 2240
    assert counts['conserved_cases'] == 1780 and counts['nonconserved_cases'] == 460
    assert counts['conserved_color_absent'] == 890
    assert counts['all_odd_betas_excluded'] == 850
    assert counts['unique_beta_palette_switch'] == 40
    assert counts['nonconserved_endpoints'] == 428 and len(harmless) == 32
    assert counts['old_failures_conserved'] == 204 and counts['old_failures_nonconserved'] == 230
    assert counts['no_growth_joins'] == 7848 and counts['surviving_joins'] == 7880
    assert counts['excluded_joins'] == 3216
    assert any(rules[i]['reason'] == 'unique_beta_palette_switch' for i in controls['AA54']['excluding_rules'])
    assert all(rules[i]['reason'] == 'nonconserved_endpoints' for i in controls['AB22']['excluding_rules'])
    # Explicit negative control to an overstrong screen: 32 unresolved pairs
    # remain admissible upper candidates. Their local realizability is unknown.
    counts['unresolved_local_pairs_with_unconditional_root_pair'] = len(harmless)
    counts['excluded_local_pairs'] = len(rules) - len(harmless)
    frames = [frame for rule in rules for frame in
              ([case['frame'] for case in rule.get('beta_cases', []) if 'frame' in case]
               + ([rule['endpoint_frame']] if 'endpoint_frame' in rule else []))]
    counts['minor_skeleton_controls'] = sum(len(f.get('skeleton_controls', [])) for f in frames)
    assert counts['minor_skeleton_controls'] == 2324
    for path, expected in inputs.items():
        assert sha256((ROOT / path).read_bytes()).hexdigest() == expected
    scripts = {}
    for module in tuple(sys.modules.values()):
        path = Path(getattr(module, '__file__', '') or '/nonexistent').resolve()
        if path.is_file() and path.is_relative_to(ROOT / 'scripts'):
            scripts[str(path.relative_to(ROOT))] = sha256(path.read_bytes()).hexdigest()
    scripts[str(Path(__file__).resolve().relative_to(ROOT))] = sha256(Path(__file__).read_bytes()).hexdigest()
    return dict(schema=1, scope='uniform conditional local rules plus finite necessary-support coverage; '
                'no table-free repair, new target accepts, source exclusions or realizability',
                inputs_sha256=inputs, scripts_sha256=scripts, summary=dict(counts),
                families=by_family, controls=controls, harmless_growth_rule_indices=harmless,
                abstract_capacity_negative_control=dict(E={r: sorted(v) for r, v in abstract_E.items()},
                    root_pairs=[], scope='abstract lists only; not target-support or disk evidence'),
                local_rules=rules, queries=queries, failures=failures)


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
    print(json.dumps(dict(summary=data['summary'], families=data['families']), sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
