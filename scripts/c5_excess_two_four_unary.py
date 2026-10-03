#!/usr/bin/env python3
"""Four original unary components: fixed support and full five-port controls.

The arbitrary-size source exclusion is proved in the companion report.
This checks finite necessary conditions, never graph or disk realizability.
"""
import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from c5_independent_support_capacity import ROWS, U
from c5_excess_two_three_unary import orbit

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_four_unary/observations.json'
SINGLETONS = tuple(i for i, q in enumerate(ROWS) if len(set(q)) == 3)


def singleton_position(q):
    position, = (j for j, c in enumerate(q) if q.count(c) == 1)
    return position


def capacity_controls():
    checked, private_checks = 0, 0
    digest = sha256()
    for colors in product(range(-1, 4), repeat=6):
        if set(colors) - {-1} != U:
            continue
        covers = [ids for ids in combinations(range(6), 4)
                  if {colors[j] for j in ids} == U]
        assert covers
        private = [j for j, c in enumerate(colors) if c >= 0 and colors.count(c) == 1]
        assert all(j in ids for j in private for ids in covers)
        private_checks += len(private)
        digest.update(json.dumps([colors, covers, private]).encode())
        checked += 1
    return dict(six_unit_covers=checked, private_factor_checks=private_checks,
                all_four_factor_subcovers_sha256=digest.hexdigest())


def gluing_controls():
    domains = [tuple(c for c in range(4) if bits >> c & 1) for bits in range(1, 16)]
    operator = tuple(t for t in product(range(4), repeat=5) if t[0] not in t[1:])
    digest, checked = sha256(), 0
    for sets in product(domains, repeat=4):
        # Independent joins: restrict the literal star relation, or choose all
        # four original endpoint colours and then impose all four original edges.
        restricted = tuple(t for t in operator if all(t[j+1] in sets[j] for j in range(4)))
        direct = tuple(t for t in product(range(4), *sets) if t[0] not in t[1:])
        assert restricted == direct
        forbidden = set().union(*(set(s) if len(s) == 1 else set() for s in sets))
        for mask in range(16):
            spoke_colors = {c for c in range(4) if mask >> c & 1}
            joined = tuple(t for t in restricted if t[0] not in spoke_colors)
            assert {t[0] for t in joined} == U - spoke_colors - forbidden
            digest.update(bytes(c for t in joined for c in t) + b'\xff')
            checked += 1
    return dict(unary_domains=domains, unary_domain_quadruples=len(domains)**4,
                ordered_five_port_operator=operator, spoke_color_masks=list(range(16)),
                full_five_port_checks=checked, tuples_sha256=digest.hexdigest())


def build():
    spans = []
    for types in product((0, 1), repeat=4):
        lower = [1+d for d in types]
        feasible = 0 < sum(types) and sum(lower) <= 5
        assert feasible == (sum(types) == 1)
        spans.append(dict(D_types=types, span_lower_bounds=lower,
                          total=sum(lower), has_D=bool(sum(types)), feasible=feasible))
    arcs = [tuple((s+j) % 5 for j in range(3)) for s in range(5)]
    rows = []
    for i in SINGLETONS:
        q = ROWS[i]
        pos = singleton_position(q)
        rainbow = [j for j, arc in enumerate(arcs) if len({q[v] for v in arc}) == 3]
        assert rainbow == [j for j, arc in enumerate(arcs) if pos in arc]
        rows.append(dict(row_index=i, row=q, singleton_position=pos,
                         rainbow_arc_indices=rainbow))
    exclusions = []
    for candidate in (933, 941):
        for target in orbit(candidate):
            rejected = [i for i in SINGLETONS if not (target >> i & 1)]
            positions = sorted(singleton_position(ROWS[i]) for i in rejected)
            for aid, arc in enumerate(arcs):
                blocked = [i for i in rejected if len({ROWS[i][v] for v in arc}) < 3]
                assert blocked, (candidate, target, arc)
                exclusions.append(dict(candidate=candidate, target=target,
                    rejected_rows=rejected, rejected_positions=positions,
                    D_support_envelope_index=aid, blocked_rows=blocked))
    # Sharpness of this necessary screen: each consecutive triple survives its
    # own arc. These five controls are abstract, not realizable graph sources.
    surviving_triples = [dict(rejected_positions=p,
        containing_arc_indices=[j for j, a in enumerate(arcs) if set(p) <= set(a)])
        for p in combinations(range(5), 3) if any(set(p) <= set(a) for a in arcs)]
    assert len(surviving_triples) == 5
    capacity = capacity_controls()
    gluing = gluing_controls()
    paths = [Path(__file__).resolve(), ROOT / 'scripts/c5_independent_support_capacity.py',
             ROOT / 'scripts/c5_excess_two_three_unary.py']
    return dict(schema=1, scope='t=2 four original unary source exclusion; finite necessary controls',
        source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths},
        pattern_order=ROWS, port_order=['r', 'original_U0_x0', 'original_U1_x1',
            'original_U2_x2', 'original_U3_x3'],
        factor_order=['spoke_s', 'spoke_t', 'original_U0', 'original_U1', 'original_U2', 'original_U3'],
        span_cases=spans, D_support_envelopes=arcs, singleton_rows=rows,
        target_orbits={str(m): orbit(m) for m in (933, 941)}, exclusions=exclusions,
        abstract_consecutive_triple_controls=surviving_triples,
        capacity_controls=capacity, gluing_controls=gluing,
        paper_dependencies=['original-component slack and full ordered gluing',
            'complete-Sigma edge minimality and degree-four core saturation',
            'all-degree-four disk classification and K4-free Gallai components',
            'same original unary D conservation', 'common-root compatible support lifts'],
        summary=dict(D_identity_cases=16, feasible_D_identity_cases=4,
            rainbow_arc_row_checks=25, target_arc_comparisons=len(exclusions), remaining=0,
            consecutive_triple_controls=5, six_unit_covers=capacity['six_unit_covers'],
            full_five_port_checks=gluing['full_five_port_checks'], graph_enumeration=False,
            disk_realizability_claimed=False, new_lean_theorem=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    payload = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.check:
        assert OUT.read_bytes() == payload.encode(), f'certificate differs: {OUT}'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
