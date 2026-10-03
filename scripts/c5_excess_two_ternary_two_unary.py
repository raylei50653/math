#!/usr/bin/env python3
"""Single spoke, original (3,1,1): same-frame support-profile exclusion.

Profiles are necessary S4-equivariant forbidden-set envelopes, not fabricated
source relations. Full ordered six-port gluing is checked separately.
"""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from c5_independent_support_capacity import ROWS
from c5_excess_two_three_unary import orbit

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_ternary_two_unary/observations.json'
U = set(range(4))


def shape(colors):
    names = {}
    return tuple(names.setdefault(c, len(names)) for c in colors)


@lru_cache(None)
def profile_domain(interval):
    support = tuple(i % 5 for i in range(interval[0], interval[1] + 1))
    shapes, representatives, infos = [], [], []
    for ri, row in enumerate(ROWS):
        colors = tuple(row[i] for i in support)
        key = shape(colors)
        if key not in shapes:
            shapes.append(key)
            representatives.append((ri, colors))
        infos.append((shapes.index(key), colors))
    choices = []
    for ri, colors in representatives:
        stabilizers = [p for p in permutations(range(4)) if all(p[c] == c for c in colors)]
        options = [-1] + [c for c in range(4) if all(p[c] == c for p in stabilizers)]
        assert options == [-1] + sorted(set(colors) if len(set(colors)) <= 2 else U)
        choices.append(options)
    transports = []
    for sid, colors in infos:
        base = representatives[sid][1]
        p = dict(zip(base, colors))
        p.update(zip(sorted(U - set(p)), sorted(U - set(p.values()))))
        assert sorted(p.values()) == list(range(4))
        transports.append((sid, p))
    profiles = []
    for selected in product(*choices):
        if all(c == -1 for c in selected):
            continue
        f = tuple(-1 if selected[sid] == -1 else p[selected[sid]] for sid, p in transports)
        profiles.append(f)
    assert len(set(profiles)) == len(profiles)
    # Independence of the chosen completion on unseen colours, including all
    # 24 colour maps. This verifies the actual necessary S4 condition.
    for ri, (sid, colors) in enumerate(infos):
        base = representatives[sid][1]
        maps = [p for p in permutations(range(4)) if tuple(p[c] for c in base) == colors]
        assert maps
        for c in choices[sid]:
            if c >= 0:
                assert len({p[c] for p in maps}) == 1
    record = dict(interval=interval, envelope_boundary_indices=support,
        local_shapes=[dict(shape=key, representative_row=ri, literal_colors=colors,
                           allowed_forbidden_colors=options)
                      for key, (ri, colors), options in zip(shapes, representatives, choices)],
        row_transports=[dict(local_shape=sid, color_permutation=[p[c] for c in range(4)])
                        for sid, p in transports],
        profile_code_key='- means empty; 0,1,2,3 mean that literal singleton forbidden colour',
        profile_codes=[''.join('-' if c == -1 else str(c) for c in f) for f in profiles])
    return tuple(profiles), record


def source_controls():
    arcs = [(a, b) for a in range(6) for b in range(a + 1, 6)]
    triples = [t for t in product(arcs, repeat=3)
               if t[0][1] <= t[1][0] and t[1][1] <= t[2][0]]
    assert len(triples) == 28
    used = sorted({a for t in triples for a in t})
    target_masks = sorted(set(orbit(933) + orbit(941)))
    records, digest, comparisons = [], sha256(), 0
    all_histogram = Counter()
    for tid, intervals in enumerate(triples):
        for factor_slots in permutations(range(3)):
            placed = tuple(intervals[slot] for slot in factor_slots)
            pools = [profile_domain(arc)[0] for arc in placed]
            histogram, witnesses = Counter(), {}
            for indices in product(*(range(len(pool)) for pool in pools)):
                fs = [pool[i] for pool, i in zip(pools, indices)]
                mask = sum(1 << ri for ri, row in enumerate(ROWS)
                           if len({row[0]} | {f[ri] for f in fs if f[ri] != -1}) < 4)
                assert mask not in target_masks, (placed, indices, mask)
                histogram[mask] += 1
                witnesses.setdefault(mask, indices)
                digest.update(json.dumps([tid, factor_slots, indices, mask]).encode())
                comparisons += 1
            records.append(dict(ordered_interval_triple=tid, factor_slot_indices=factor_slots,
                factor_intervals=placed, profile_domain_sizes=list(map(len, pools)),
                sigma_histogram=[dict(sigma=m, count=n, first_profile_indices=witnesses[m])
                                 for m, n in sorted(histogram.items())]))
            all_histogram.update(histogram)
    assert len(records) == 168 and comparisons == 146496
    return dict(factor_order=['original_ternary_C', 'original_unary_U', 'original_unary_V'],
        fixed_spoke_boundary_index=0, slit_boundary_indices=[0, 1, 2, 3, 4, 0],
        ordered_interval_triples=triples, profile_domains=[profile_domain(a)[1] for a in used],
        placements=records, target_orbits={str(m): orbit(m) for m in (933, 941)},
        all_profile_comparisons=comparisons, comparisons_sha256=digest.hexdigest(),
        global_sigma_histogram=sorted(all_histogram.items()), surviving_target_profiles=0)


def gluing_controls():
    pairs = list(product(range(4), repeat=3))
    domains = [tuple(c for c in range(4) if bits >> c & 1) for bits in range(1, 16)]
    operator = [t for t in product(range(4), repeat=6) if t[0] not in t[1:]]
    assert len(operator) == 972
    digest, single_checks, pair_checks = sha256(), 0, 0
    cap_one_pairs = 0
    for du, dv in product(domains, repeat=2):
        fibers = []
        unary_forbidden = (set(du) if len(du) == 1 else set()) | (set(dv) if len(dv) == 1 else set())
        for p in pairs:
            fiber = tuple(t for t in operator if t[1:4] == p and t[4] in du and t[5] in dv)
            direct = tuple((a,) + p + (u, v) for a, u, v in product(range(4), du, dv)
                           if a not in p and a != u and a != v)
            assert fiber == direct
            for e in range(4):
                joined = tuple(t for t in fiber if t[0] != e)
                assert {t[0] for t in joined} == U - set(p) - unary_forbidden - {e}
                digest.update(json.dumps([p, du, dv, e, joined]).encode())
                single_checks += 1
            fibers.append(fiber)
        for i, j in combinations(range(64), 2):
            relation = (pairs[i], pairs[j])
            union = tuple(sorted(fibers[i] + fibers[j]))
            direct = tuple(sorted((a,) + p + (u, v)
                for p, a, u, v in product(relation, range(4), du, dv)
                if a not in p and a != u and a != v))
            assert union == direct
            forbidden = set(pairs[i]) & set(pairs[j])
            assert {t[0] for t in union} == U - forbidden - unary_forbidden
            cap_one_pairs += len(forbidden) <= 1
            pair_checks += 1
            digest.update(json.dumps([i, j, du, dv, union]).encode())
    assert single_checks == 57600 and pair_checks == 453600
    return dict(ordered_six_port_operator=operator,
        port_order=['r', 'original_C_x', 'original_C_y', 'original_C_z', 'original_U_u', 'original_V_v'],
        ordered_ternary_tuples=pairs, unary_domains=domains,
        singleton_relation_spoke_checks=single_checks, two_tuple_relation_checks=pair_checks,
        cap_at_most_one_two_tuple_checks=cap_one_pairs, complete_joins_sha256=digest.hexdigest(),
        arbitrary_relation_coverage='For the same literal frame, J(R,S,T) is the union '
            'of J({p},S,T) over all original ordered p in R. Its root projection is '
            'U minus the intersection of set(p), unary singleton forbiddens and the spoke colour.',
        scope='Complete ordered relation algebra; abstract relations are not disk realizations.')


def build():
    source = source_controls()
    joins = gluing_controls()
    paths = [Path(__file__).resolve(), ROOT / 'scripts/c5_independent_support_capacity.py',
             ROOT / 'scripts/c5_excess_two_three_unary.py',
             ROOT / 'scripts/c5_single_spoke_three_one.py']
    return dict(schema=1, scope='t=1 original (3,1,1) whole-source exclusion', pattern_order=ROWS,
        source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths},
        source_controls=source, complete_relation_gluing=joins,
        paper_dependencies=['three original contacts and two forbidden colours imply an actual K5',
            'edge-minimal private witnesses and the two-boundary-point support bound',
            'same-embedding spoke slit and compatible original support lifts',
            'same-source local S4 equivariance in an enlarged support envelope'],
        summary=dict(ordered_interval_triples=28, named_placements=168,
            all_profile_comparisons=146496, target_orbits=10, surviving_target_profiles=0,
            complete_six_port_operator_tuples=972,
            singleton_relation_spoke_checks=joins['singleton_relation_spoke_checks'],
            two_tuple_relation_checks=joins['two_tuple_relation_checks'],
            cap_at_most_one_two_tuple_checks=joins['cap_at_most_one_two_tuple_checks'],
            graph_enumeration=False, disk_realizability_claim=False, new_Lean_theorem=False))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    payload = json.dumps(result, sort_keys=True, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == payload, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
