#!/usr/bin/env python3
"""Five original unary components cannot reject a row in the t=1 case.

The arbitrary-size exclusion uses the existing all-degree-four disk
classification. This certificate checks labelled four-factor subcovers and
literal ordered gluing. It neither enumerates source graphs nor proves the
classification, disk topology, or realizability of abstract unary domains.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from c5_independent_support_capacity import ROWS, U
from c5_excess_two_three_unary import orbit

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_five_unary/observations.json'
FACTORS = ['original_spoke'] + [f'original_U{i}' for i in range(5)]
PORTS = ['r'] + [f'original_U{i}_x{i}' for i in range(5)]


def structural_cases():
    records = []
    for kept in combinations(range(6), 4):
        omitted = [j for j in range(6) if j not in kept]
        unary = [j - 1 for j in kept if j]
        spoke_count = int(0 in kept)
        interior_degree = len(unary)
        assert interior_degree + spoke_count == 4
        assert interior_degree in (3, 4)
        records.append(dict(kept_factor_indices=kept,
            omitted_factor_indices=omitted, retained_original_unaries=unary,
            retained_spoke_count=spoke_count, root_full_degree=4,
            root_interior_degree=interior_degree,
            all_root_interior_edges_are_bridges=True,
            classification_conflict='noncycle root has interior degree greater than two'))
    assert Counter(r['root_interior_degree'] for r in records) == {3: 10, 4: 5}
    return records


def capacity_controls(structures):
    records, incidence = [], Counter()
    for spoke in range(4):
        for unary in product(range(-1, 4), repeat=5):
            colors = (spoke,) + unary
            if set(colors) - {-1} != U:
                continue
            covers = [i for i, entry in enumerate(structures)
                      if {colors[j] for j in entry['kept_factor_indices']} == U]
            assert covers
            for i in covers:
                assert structures[i]['root_interior_degree'] > 2
                incidence[i] += 1
            records.append(dict(spoke_color=spoke,
                original_unary_forbidden_colors=unary,
                all_four_factor_subcover_indices=covers))
    assert set(incidence) == set(range(15))
    return dict(empty_factor_encoding=-1, all_covering_assignments=records,
        subcover_incidence=[incidence[i] for i in range(15)],
        covering_assignments=len(records), four_factor_subcovers=sum(incidence.values()))


def gluing_controls():
    # This complete transition table proves the root projection one literal
    # contact at a time. The paper join keeps every earlier tuple unchanged.
    domains = [tuple(c for c in range(4) if mask >> c & 1) for mask in range(1, 16)]
    transitions = []
    for mask in range(16):
        roots = tuple(c for c in range(4) if mask >> c & 1)
        for domain in domains:
            relation = tuple((a, c) for a in roots for c in domain if a != c)
            forbidden = set(domain) if len(domain) == 1 else set()
            assert {a for a, _ in relation} == set(roots) - forbidden
            transitions.append(dict(root_domain=roots, original_endpoint_domain=domain,
                ordered_relation=relation, root_projection=sorted({a for a, _ in relation})))
    # Full six-port checks over five literal representative domains. A domain
    # with >=2 colors is not replaced inside a tuple relation: its projection
    # behavior follows from the complete 240-entry transition table above.
    representatives = [(c,) for c in range(4)] + [tuple(range(4))]
    operator = tuple(t for t in product(range(4), repeat=6) if t[0] not in t[1:])
    digest, checks = sha256(), 0
    for sets in product(representatives, repeat=5):
        restricted = tuple(t for t in operator
                           if all(t[j + 1] in sets[j] for j in range(5)))
        direct = tuple(t for t in product(range(4), *sets) if t[0] not in t[1:])
        assert restricted == direct
        for spoke in range(4):
            joined = tuple(t for t in restricted if t[0] != spoke)
            sequential = U - {spoke}
            for domain in sets:
                sequential = {a for a in sequential if any(a != c for c in domain)}
            forbidden = {spoke} | set().union(*(set(s) for s in sets if len(s) == 1))
            assert {t[0] for t in joined} == sequential == U - forbidden
            digest.update(bytes(c for t in joined for c in t) + b'\xff')
            checks += 1
    assert len(transitions) == 240 and checks == 12500 and len(operator) == 972
    return dict(all_nonempty_unary_domains=domains,
        full_one_contact_transition_table=transitions,
        ordered_six_port_operator=operator,
        literal_representative_domains=representatives,
        representative_domain_quintuples=len(representatives)**5,
        full_six_port_checks=checks, ordered_relations_sha256=digest.hexdigest())


def build():
    structures = structural_cases()
    capacity = capacity_controls(structures)
    gluing = gluing_controls()
    targets = []
    for candidate in (933, 941):
        for target in orbit(candidate):
            rejected = [i for i in range(len(ROWS)) if not target >> i & 1]
            assert rejected and all(len(set(ROWS[i])) == 3 for i in rejected)
            targets.append(dict(candidate=candidate, target=target,
                rejected_row_indices=rejected,
                exclusion='every rejected row requires an impossible four-factor subcore'))
    paths = [Path(__file__).resolve(), ROOT / 'scripts/c5_independent_support_capacity.py',
             ROOT / 'scripts/c5_excess_two_three_unary.py']
    return dict(schema=1,
        scope='t=1 partition (1,1,1,1,1) entire source exclusion by required degree-four subcore',
        source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths},
        pattern_order=ROWS, factor_order=FACTORS, port_order=PORTS,
        structural_cases=structures, capacity_controls=capacity, gluing_controls=gluing,
        target_exclusions=targets,
        paper_dependencies=['nonempty original unary domains by endpoint slack',
            'full ordered same-boundary gluing of original components',
            'degree-four saturation of a minimal rejected-row subcore',
            'all-degree-four C5 disk classification: noncycle vertices have interior degree at most two'],
        summary=dict(named_omission_pairs=len(structures),
            root_degree_three_bridge_cases=10, root_degree_four_bridge_cases=5,
            covering_assignments=capacity['covering_assignments'],
            four_factor_subcovers=capacity['four_factor_subcovers'],
            full_one_contact_transition_checks=240,
            full_six_port_checks=gluing['full_six_port_checks'],
            target_orbits_checked=len(targets), remaining=0,
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
