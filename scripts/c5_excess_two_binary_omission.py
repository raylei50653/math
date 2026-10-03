#!/usr/bin/env python3
"""Fixed necessary support envelopes for t=3, (2,1), binary omission.

No graph enumeration or realizability assertion; see the companion report.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from c5_independent_support_capacity import ROWS, U
from c5_excess_two_three_unary import orbit

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_binary_omission/observations.json'
SINGLETONS = tuple(i for i, q in enumerate(ROWS) if len(set(q)) == 3)
FORBIDDEN = tuple(tuple(f) for n in range(3) for f in combinations(range(4), n))


def options(q, spokes, v_arc, c_arc, omitted_rejects, accepts, omissions=True):
    """A relaxation of the exact root projection, never an endpoint relation."""
    seen_v, seen_c = {q[b] for b in v_arc}, {q[b] for b in c_arc}
    unseen_c = U - seen_c
    spoke_colors = {q[b] for b in spokes}
    result = []
    for d in (False, True):
        fv = {3} if d else set()
        if d and len(seen_v) != 3:
            continue
        if (spoke_colors | fv == U) != omitted_rejects:
            continue
        for colors in FORBIDDEN:
            fc = set(colors)
            if fc & unseen_c and not unseen_c <= fc:
                continue
            if (spoke_colors | fv | fc != U) != accepts:
                continue
            if omissions:
                if any({q[s]} | fv | fc == U for s in spokes):
                    continue
                if any({q[s] for s in pair} | fc == U
                       for pair in combinations(spokes, 2)):
                    continue
            result.append([int(d), list(colors)])
    return result


def evaluate(mask, q0, spokes, v_arc, c_arc, omissions=True):
    return [(i, options(ROWS[i], spokes, v_arc, c_arc, i == q0,
                        bool(mask >> i & 1), omissions)) for i in SINGLETONS]


def geometry():
    result = []
    for spokes in combinations(range(5), 3):
        sectors = [tuple((s+k) % 5 for k in range((spokes[(j+1) % 3]-s) % 5+1))
                   for j, s in enumerate(spokes)]
        for av, ac in product(range(3), repeat=2):
            for va, vb in combinations(range(len(sectors[av])), 2):
                if vb-va < 2:
                    continue
                for ca in range(len(sectors[ac])):
                    for cb in range(ca, len(sectors[ac])):
                        if av == ac and not (vb <= ca or cb <= va):
                            continue
                        result.append(dict(spokes=spokes, sectors=sectors,
                            sector_ids=[av, ac], offsets=[va, vb, ca, cb],
                            V_envelope=sectors[av][va:vb+1],
                            C2_envelope=sectors[ac][ca:cb+1]))
    return result


def controls():
    # All nonempty ordered binary relations, with literal x/y positions.
    pairs = tuple(product(range(4), repeat=2))
    avoids = [sum(1 << j for j, p in enumerate(pairs) if a not in p) for a in range(4)]
    count, digest = 0, sha256()
    for bits in range(1, 1 << 16):
        relation = [p for j, p in enumerate(pairs) if bits >> j & 1]
        forbidden = set.intersection(*(set(p) for p in relation))
        assert len(forbidden) <= 2
        # A bit at 16*r+4*x+y records the complete triple, before unary gluing.
        by_root = [sum(1 << (16*a+4*x+y) for x, y in relation if a not in (x, y))
                   for a in range(4)]
        assert {a for a in range(4) if bits & avoids[a]} == U-forbidden
        for unary in range(1, 16):
            domain = [v for v in range(4) if unary >> v & 1]
            # Four 64-bit slices indexed by the literal v colour encode every
            # (r,x,y,v) tuple, without replacing R by endpoint marginals.
            joined = sum(sum(by_root[a] for a in range(4) if a != v) << (64*v)
                         for v in domain)
            roots = {a for a in range(4) if any(
                joined & (((1 << 16)-1) << (64*v+16*a)) for v in domain)}
            fv = set(domain) if len(domain) == 1 else set()
            assert roots == U-forbidden-fv
            digest.update(joined.to_bytes(32, 'little'))
            count += 1
    # Independent direct tuple construction for representative correlated R,
    # every unary domain, all root-spoke masks and their omission filters.
    direct = 0
    for relation in (((0, 1), (1, 0)), ((0, 0), (1, 1)),
                     ((0, 1),), pairs):
        fc = set.intersection(*(set(p) for p in relation))
        for unary in range(1, 16):
            domain = [v for v in range(4) if unary >> v & 1]
            fv = set(domain) if len(domain) == 1 else set()
            for spoke_mask in range(16):
                sp = {a for a in range(4) if spoke_mask >> a & 1}
                tuples = [(a, x, y, v) for a in range(4) for x, y in relation for v in domain
                          if a not in sp and a not in (x, y, v)]
                assert {t[0] for t in tuples} == U-sp-fc-fv
                direct += 1
    # Check the envelope stabilizer test against all 24 colour permutations.
    stabilizers = 0
    for support in range(16):
        seen = {a for a in range(4) if support >> a & 1}
        unseen = U-seen
        for colors in FORBIDDEN:
            fc = set(colors)
            explicit = all({p[a] for a in fc} == fc for p in permutations(range(4))
                           if all(p[a] == a for a in seen))
            assert explicit == (not fc & unseen or unseen <= fc)
            stabilizers += 1
    return dict(binary_relations=65535, full_four_port_joins=count,
                full_tuples_sha256=digest.hexdigest(), direct_tuple_controls=direct,
                stabilizer_controls=stabilizers,
                marginal_collision={'R1': [[0, 1], [1, 0]], 'R2': [[0, 0], [1, 1]],
                                    'same_marginals': [[0, 1], [0, 1]],
                                    'F1': [0, 1], 'F2': []})


def build():
    placements = geometry()
    records, coarse, counts = [], [], Counter()
    # Whole-sector relaxation: each component may see its whole sector, but
    # the necessary V span 2 is charged and C2 is allowed span zero.
    coarse_keys = set()
    for gid, g in enumerate(placements):
        spokes = g['spokes']
        av, ac = g['sector_ids']
        for candidate in (933, 941):
            for mask in orbit(candidate):
                for q0 in SINGLETONS:
                    if mask >> q0 & 1 or len({ROWS[q0][s] for s in spokes}) != 3:
                        continue
                    key = (candidate, mask, spokes, av, ac, q0)
                    if key not in coarse_keys:
                        coarse_keys.add(key)
                        rows = evaluate(mask, q0, spokes, g['sectors'][av], g['sectors'][ac])
                        if all(opts for _, opts in rows):
                            coarse.append(dict(candidate=candidate, mask=mask, spokes=spokes,
                                sector_ids=[av, ac], omitted_row=q0, row_options=rows))
                            counts[f'{candidate}_whole_sector_survivors'] += 1
                    if len({ROWS[q0][s] for s in g['V_envelope']}) != 3:
                        continue
                    baseline = evaluate(mask, q0, spokes, g['V_envelope'], g['C2_envelope'], False)
                    rows = evaluate(mask, q0, spokes, g['V_envelope'], g['C2_envelope'])
                    counts[f'{candidate}_envelope_comparisons'] += 1
                    counts[f'{candidate}_before_omission_survivors'] += all(o for _, o in baseline)
                    empty = [i for i, opts in rows if not opts]
                    assert empty, (g, candidate, mask, q0, rows)
                    records.append([gid, candidate, mask, q0, empty[0],
                                    [len(o) for _, o in baseline], [len(o) for _, o in rows]])
    assert len(records) == 2030
    assert len(coarse) == 30
    sources = [Path(__file__).resolve(), ROOT / 'scripts/c5_independent_support_capacity.py',
               ROOT / 'scripts/c5_excess_two_three_unary.py']
    return dict(schema=1, scope='necessary original support envelopes; no graph enumeration',
        source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in sources},
        pattern_order=ROWS, singleton_row_indices=SINGLETONS,
        target_orbits={str(m): orbit(m) for m in (933, 941)}, geometry=placements,
        whole_sector_survivors=coarse,
        record_columns=['geometry_id', 'candidate', 'target', 'omitted_C2_row', 'first_empty_row',
                        'row_option_counts_before_omissions', 'row_option_counts_after_omissions'],
        exclusions=records, controls=controls(),
        paper_dependencies=['original binary/unary exact gluing and slack',
            'all-degree-four single-missing classification', 'unary D conservation',
            'common-root support lifts in fixed spoke sectors',
            'double-spoke and t=3 spoke-unary omission acceptance'],
        summary=dict(sorted(counts.items()), geometry_envelopes=len(placements),
                     envelope_comparisons=len(records), remaining=0,
                     disk_realizability_claimed=False, new_lean_theorem=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    payload = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.check:
        assert OUT.read_bytes() == payload.encode(), f'certificate differs: {OUT}'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(result['summary'], sort_keys=True))
    print(json.dumps(result['controls'], sort_keys=True))


if __name__ == '__main__':
    main()
