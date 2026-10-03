#!/usr/bin/env python3
"""Necessary same-source constraints for three spokes and three unary factors.

This enumerates labelled set constraints, not graphs or realizable relations.
Arbitrary-size and disk arguments are in docs/c5_excess_two_three_unary.md.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from c5_independent_support_capacity import ROWS, U

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_three_unary/observations.json'
PAIRS = tuple(combinations(range(6), 2))
SINGLETONS = tuple(i for i, q in enumerate(ROWS) if len(set(q)) == 3)


def orbit(mask):
    lookup = {q: i for i, q in enumerate(ROWS)}
    result = set()
    for sign in (-1, 1):
        for shift in range(5):
            moved = 0
            for i, q in enumerate(ROWS):
                names = {}
                b = tuple(names.setdefault(q[(sign*j+shift) % 5], len(names))
                          for j in range(5))
                moved |= ((mask >> i) & 1) << lookup[b]
            result.add(moved)
    return sorted(result)


def row_options(q, spokes, types, sectors=None, assignment=None):
    choices = []
    for j, is_d in enumerate(types):
        seen = {q[b] for b in sectors[assignment[j]]} if sectors else {0, 1, 2}
        choices.append((-1, 3) if is_d and len(seen) == 3 else
                       (-1,) if is_d else (-1, *sorted(seen)))
    options = {}
    for colors in product(*choices):
        factors = [{q[b]} for b in spokes] + [set() if c < 0 else {c} for c in colors]
        if set.union(*factors) != U:
            continue
        omitted = [pi for pi, pair in enumerate(PAIRS)
                   if set.union(*(f for j, f in enumerate(factors) if j not in pair)) == U]
        # Any four-colour cover by six unit factors has a four-factor subcover.
        assert omitted
        # Keeping three distinct unary branches cannot be a degree-four core.
        if any(PAIRS[pi][1] < 3 for pi in omitted):
            continue
        bits = sum(1 << pi for pi in omitted)
        options.setdefault(bits, dict(unary_forbidden_colors=colors,
                                      omitted_pair_indices=omitted))
    return [(bits, options[bits]) for bits in sorted(options)]


def schedules(mask, spokes, types, sectors=None, assignment=None):
    states = {0: []}
    layers = []
    for i in SINGLETONS:
        if mask >> i & 1:
            continue
        options = row_options(ROWS[i], spokes, types, sectors, assignment)
        following = {}
        for used, witness in sorted(states.items()):
            for bits, option in options:
                if not used & bits:
                    following.setdefault(used | bits, witness + [dict(row_index=i, **option)])
        states = following
        layers.append(dict(row_index=i, option_count=len(options),
                           reachable_omission_masks=sorted(states)))
    return states, layers


def gluing_controls():
    """Check full (r,x,y,v) tuples against factor projection for every unary set.

    Free endpoint sets are algebraic inputs, never asserted to be graph sources.
    Include every proper three-spoke colour set possible on the five rows.
    """
    nonempty = [tuple(c for c in range(4) if bits >> c & 1) for bits in range(1, 16)]
    spoke_sets = sorted({tuple(sorted({q[b] for b in spokes}))
                        for q in ROWS for spokes in combinations(range(5), 3)})
    digest, checked = sha256(), 0
    for domains in product(nonempty, repeat=3):
        forbidden = set().union(*(set(s) if len(s) == 1 else set() for s in domains))
        for spoke_colors in spoke_sets:
            tuples = [(r, x, y, v) for r, x, y, v in product(range(4), *domains)
                      if r not in (*spoke_colors, x, y, v)]
            projected = {t[0] for t in tuples}
            assert projected == U - set(spoke_colors) - forbidden
            digest.update(json.dumps([domains, spoke_colors, tuples]).encode())
            checked += 1
    return dict(nonempty_unary_triples=15**3, spoke_color_sets=spoke_sets,
                full_four_port_checks=checked, tuples_sha256=digest.hexdigest())


def build():
    targets = {str(m): orbit(m) for m in (933, 941)}
    assert targets == {'933': [933, 934, 940, 948, 996],
                       '941': [941, 949, 950, 998, 1004]}
    records, geometry, counts = [], [], Counter()
    for spokes in combinations(range(5), 3):
        sectors = [tuple((s+k) % 5 for k in range((spokes[(j+1) % 3]-s) % 5 + 1))
                   for j, s in enumerate(spokes)]
        for types in product((0, 1), repeat=3):
            placements = [a for a in product(range(3), repeat=3)
                          if all(sum(1+types[j] for j in range(3) if a[j] == k)
                                 <= len(sectors[k])-1 for k in range(3))]
            geometry.append(dict(spokes=spokes, sectors=sectors, D_types=types,
                                 span_lower_bounds=[1+d for d in types],
                                 permitted_sector_assignments=placements))
            for candidate, masks in targets.items():
                for mask in masks:
                    states, layers = schedules(mask, spokes, types)
                    counts[f'{candidate}_abstract_cases'] += 1
                    counts[f'{candidate}_abstract_terminal_states'] += len(states)
                    if not states:
                        continue
                    if candidate == '933':
                        assert sum(types) == 2
                        assert sorted(len(s)-1 for s in sectors) == [1, 1, 3]
                    counts[f'{candidate}_surviving_cases_with_{sum(types)}_D_types'] += 1
                    witness = states[min(states)]
                    refinements = []
                    for assignment in placements:
                        remaining, refined_layers = schedules(mask, spokes, types, sectors, assignment)
                        assert not remaining, (mask, spokes, types, assignment, remaining)
                        refinements.append(dict(sector_assignment=assignment, layers=refined_layers))
                    counts[f'{candidate}_abstract_surviving_cases'] += 1
                    counts[f'{candidate}_sector_refinements'] += len(refinements)
                    counts[f'{candidate}_no_sector_placement'] += not bool(placements)
                    records.append(dict(candidate=int(candidate), target=mask, spokes=spokes,
                        D_types=types, layers=layers, abstract_witness=witness,
                        terminal_state_count=len(states), sector_refinements=refinements))
    # Independent global-placement count (including cases already excluded algebraically).
    assert sum(len(g['permitted_sector_assignments']) for g in geometry) == 365
    controls = gluing_controls()
    sources = [Path(__file__).resolve(), ROOT / 'scripts/c5_independent_support_capacity.py']
    return dict(schema=1, scope='necessary labelled constraints; three original unary components, no graph enumeration',
        source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in sources},
        pattern_order=ROWS, factor_order=['spoke_0', 'spoke_1', 'spoke_2', 'U_1', 'U_2', 'V'],
        omitted_factor_pairs=PAIRS, target_D5_orbits=targets, geometry=geometry,
        abstract_survivors=records, gluing_controls=controls,
        paper_dependencies=['unary slack and exact gluing', 'complete-Sigma edge minimality',
            'connected all-degree-four disk classification and single missing row',
            'unary unused-colour conservation', 'same-source sector lifts and support stabilizers'],
        summary=dict(**dict(sorted(counts.items())), geometry_scenarios=len(geometry),
            permitted_sector_assignments=365, candidate_comparisons=800,
            full_four_port_checks=controls['full_four_port_checks'], remaining=0,
            graph_enumeration=False, disk_realizability_claimed=False, new_lean_theorem=False))


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
