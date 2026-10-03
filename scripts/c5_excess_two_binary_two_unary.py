#!/usr/bin/env python3
"""Exclude original binary omission for t=2, partition (2,1,1).

Necessary same-embedding support envelopes, not a source graph enumeration.
All relations use literal ordered ports (r,x,y,u,v) and one color frame.
"""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from c5_independent_support_capacity import ROWS, U
from c5_excess_two_three_unary import orbit

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_binary_two_unary/observations.json'
SINGLETONS = tuple(i for i, q in enumerate(ROWS) if len(set(q)) == 3)
FORBIDDEN = tuple(tuple(f) for n in range(3) for f in combinations(range(4), n))
UNIT_PAIRS = tuple(combinations(range(4), 2))
TYPES = ((0, 1), (1, 0))


def singleton(c):
    return set() if c < 0 else {c}


@lru_cache(None)
def options(ri, spokes, types, omitted_row, target, arcs=None):
    """Necessary forbidden sets; these are not complete endpoint relations."""
    q = ROWS[ri]
    seen = [{q[b] for b in a} for a in arcs] if arcs else [{0, 1, 2}]*3
    choices = [(-1, 3) if d else (-1, 0, 1, 2) for d in types]
    result = []
    for u, v, colors in product(*choices, FORBIDDEN):
        fu, fv, fa = singleton(u), singleton(v), set(colors)
        if any(f and (len(s) < 3 if d else not f <= s)
               for f, s, d in zip((fu, fv), seen[:2], types, strict=True)):
            continue
        unseen = U - seen[2]
        if fa & unseen and not unseen <= fa:
            continue
        factors = [{q[s]} for s in spokes] + [fu, fv]
        units = set.union(*factors)
        if (units == U) != (ri == omitted_row):
            continue
        if (units | fa != U) != bool(target >> ri & 1):
            continue
        if any(fa | factors[j] | factors[k] == U for j, k in UNIT_PAIRS):
            continue
        result.append((u, v, colors))
    return tuple(result)


def geometry(spokes, types):
    sectors = [tuple((s+k) % 5 for k in range((spokes[(j+1) % 2]-s) % 5+1))
               for j, s in enumerate(spokes)]
    # A may have empty support or span zero. No positive span is imposed on A.
    choices = [[(sid, a, b, sector[a:b+1])
                for sid, sector in enumerate(sectors)
                for a in range(len(sector)) for b in range(a+minimum, len(sector))]
               for minimum in (1+types[0], 1+types[1], 0)]
    for placement in product(*choices):
        if any(i[0] == j[0] and not (i[2] <= j[1] or j[2] <= i[1])
               for i, j in combinations(placement, 2)):
            continue
        yield dict(spokes=spokes, D_types=types, sectors=sectors,
                   component_order=['original_U', 'original_V', 'original_A'],
                   sector_ids=[p[0] for p in placement],
                   offsets=[[p[1], p[2]] for p in placement],
                   envelopes=[p[3] for p in placement])


def gluing_controls():
    """Literal five-port operators; exhaustive binary projection and unary lifts.

Every nonempty ordered binary relation is checked at the three-port level.
For every attainable forbidden set, a representative complete relation is
then glued to every pair of nonempty unary domains and every spoke color set.
Two extra relations preserve the equal-marginal/different-forbidden collision.
These are algebraic controls, not witnesses of actual disk realizability.
"""
    pairs = tuple(product(range(4), repeat=2))
    representatives, binary_digest = {}, sha256()
    for bits in range(1, 1 << 16):
        relation = tuple(p for j, p in enumerate(pairs) if bits >> j & 1)
        fa = tuple(sorted(set.intersection(*(set(p) for p in relation))))
        triples = [(a, x, y) for a in range(4) for x, y in relation if a not in (x, y)]
        assert {t[0] for t in triples} == U-set(fa)
        representatives.setdefault(fa, relation)
        binary_digest.update(bytes(c for t in triples for c in t) + b'\xff')
    assert set(representatives) == set(FORBIDDEN)
    relations = sorted(set(representatives.values()) |
                       {((0, 1), (1, 0)), ((0, 0), (1, 1)), pairs})
    domains = [tuple(c for c in range(4) if bits >> c & 1) for bits in range(1, 16)]
    operators, digest, checked = [], sha256(), 0
    for relation in relations:
        fa = set.intersection(*(set(p) for p in relation))
        operator = [(r, x, y, u, v) for r, (x, y), u, v
                    in product(range(4), relation, range(4), range(4))
                    if r not in (x, y, u, v)]
        for su, sv in product(domains, repeat=2):
            fu = set(su) if len(su) == 1 else set()
            fv = set(sv) if len(sv) == 1 else set()
            restricted = [t for t in operator if t[3] in su and t[4] in sv]
            for mask in range(16):
                sc = {c for c in range(4) if mask >> c & 1}
                joined = [t for t in restricted if t[0] not in sc]
                direct = [(r, x, y, u, v) for r, (x, y), u, v
                          in product(range(4), relation, su, sv)
                          if r not in (*sc, x, y, u, v)]
                assert set(joined) == set(direct)
                assert {t[0] for t in joined} == U-sc-fa-fu-fv
                digest.update(bytes(c for t in sorted(joined) for c in t)+b'\xff')
                checked += 1
        operators.append(dict(binary_relation=relation, forbidden=sorted(fa),
                              ordered_five_port_operator=operator))
    stabilizers = 0
    for mask, colors in product(range(16), FORBIDDEN):
        seen = {c for c in range(4) if mask >> c & 1}
        unseen, f = U-seen, set(colors)
        explicit = all({p[c] for c in f} == f for p in permutations(range(4))
                       if all(p[c] == c for c in seen))
        assert explicit == (not f & unseen or unseen <= f)
        stabilizers += 1
    return dict(binary_relations=65535, binary_projection_sha256=binary_digest.hexdigest(),
                operators=operators, unary_domains=domains, full_five_port_checks=checked,
                five_port_sha256=digest.hexdigest(), stabilizer_checks=stabilizers,
                marginal_collision=dict(R1=[[0, 1], [1, 0]], R2=[[0, 0], [1, 1]],
                                        F1=[0, 1], F2=[]))


def build():
    counts, abstract, placements, exclusions = Counter(), [], [], []
    for spokes in combinations(range(5), 2):
        for types in TYPES:
            surviving = []
            for candidate in (933, 941):
                for target in orbit(candidate):
                    for q0 in SINGLETONS:
                        if target >> q0 & 1:
                            continue
                        rows = [options(i, spokes, types, q0, target) for i in SINGLETONS]
                        empty = [i for i, row in zip(SINGLETONS, rows, strict=True) if not row]
                        aid = len(abstract)
                        abstract.append(dict(spokes=spokes, D_types=types, candidate=candidate,
                            target=target, omitted_A_row=q0, row_options=rows,
                            first_empty_row=empty[0] if empty else None))
                        counts[f'{candidate}_abstract_comparisons'] += 1
                        if not empty:
                            surviving.append((aid, candidate, target, q0))
                            counts[f'{candidate}_abstract_survivors'] += 1
            for g in geometry(spokes, types):
                gid = len(placements)
                placements.append(g)
                arcs = tuple(g['envelopes'])
                for aid, candidate, target, q0 in surviving:
                    rows = [options(i, spokes, types, q0, target, arcs) for i in SINGLETONS]
                    empty = [i for i, row in zip(SINGLETONS, rows, strict=True) if not row]
                    assert empty, (g, candidate, target, q0, rows)
                    exclusions.append([gid, aid, empty[0], [len(row) for row in rows]])
                    counts[f'{candidate}_envelope_comparisons'] += 1
    assert len(abstract) == 700 and len(placements) == 2340
    assert len(exclusions) == 65100
    assert sum(a['first_empty_row'] is None for a in abstract) == 560
    controls = gluing_controls()
    paths = [Path(__file__).resolve(), ROOT / 'scripts/c5_independent_support_capacity.py',
             ROOT / 'scripts/c5_excess_two_three_unary.py']
    return dict(schema=1,
        scope='conditional t=2 (2,1,1) original binary omission; necessary envelopes only',
        source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths},
        pattern_order=ROWS, singleton_row_indices=SINGLETONS,
        target_orbits={str(m): orbit(m) for m in (933, 941)},
        port_order=['r', 'original_A_x', 'original_A_y', 'original_U_u', 'original_V_v'],
        unit_factor_order=['spoke_0', 'spoke_1', 'original_U', 'original_V'],
        retained_unit_pairs=UNIT_PAIRS,
        option_encoding='[U forbidden color, V forbidden color, A forbidden set]; -1 is empty',
        abstract_cases=abstract, geometry=placements,
        exclusion_columns=['geometry_id', 'abstract_case_id', 'first_empty_row', 'five_row_option_counts'],
        exclusions=exclusions, gluing_controls=controls,
        paper_dependencies=['original component slack and full ordered five-port gluing',
            'all-degree-four disk single-missing classification and saturation',
            'same original unary D conservation and positive support span',
            'same-embedding common-root support envelopes in two spoke sectors',
            'double-spoke, spoke-unary and two-unary omissions accept all rows'],
        summary=dict(sorted(counts.items()), abstract_comparisons=len(abstract),
            abstract_survivors=560, geometry_envelopes=len(placements),
            envelope_comparisons=len(exclusions), remaining=0,
            binary_relation_controls=controls['binary_relations'],
            full_five_port_checks=controls['full_five_port_checks'],
            graph_enumeration=False, new_lean_theorem=False, disk_realizability_claimed=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    payload = json.dumps(result, indent=1, sort_keys=True)+'\n'
    if args.check:
        assert OUT.read_bytes() == payload.encode(), f'certificate differs: {OUT}'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
