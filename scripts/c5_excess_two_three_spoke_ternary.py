#!/usr/bin/env python3
"""Three spokes, original (3): a capacity obstruction in the named C5 frame.

The capacity bound is a paper K5 lemma; this checks its finite consequence
and complete ordered seven-port gluing, without generating source graphs.
"""
import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from c5_independent_support_capacity import ROWS, U
from c5_excess_two_three_unary import orbit

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_three_spoke_ternary/observations.json'


def source_controls():
    singleton_rows = tuple(i for i, q in enumerate(ROWS) if len(set(q)) == 3)
    targets = sorted(set(orbit(933) + orbit(941)))
    geometry, queries = [], []
    for spokes in combinations(range(5), 3):
        rainbow = [i for i in singleton_rows if len({ROWS[i][s] for s in spokes}) == 3]
        gid = len(geometry)
        geometry.append(dict(original_spokes=spokes,
                             singleton_rows_with_three_spoke_colors=rainbow))
        for target in targets:
            rejected = [i for i in singleton_rows if not (target >> i & 1)]
            failures = [i for i in rejected if i not in rainbow]
            assert failures
            i = failures[0]
            seen = {ROWS[i][s] for s in spokes}
            # Enumerate every allowed capacity-zero/one forbidden set. Even
            # these independently chosen row values cannot reject this row.
            options = [(), *((c,) for c in range(4))]
            lifts = [dict(ternary_forbidden=f,
                          remaining_root_colors=sorted(U - seen - set(f)))
                     for f in options]
            assert all(lift['remaining_root_colors'] for lift in lifts)
            queries.append(dict(geometry_id=gid, target=target,
                rejected_singleton_rows=rejected, all_capacity_failure_rows=failures,
                first_failure_row=i, literal_boundary_row=ROWS[i],
                literal_spoke_colors=sorted(seen), capacity_one_root_controls=lifts))
    assert len(geometry) == 10 and len(queries) == 100
    t4_spoke_obstructions = []
    for n in (4, 5):
        for spokes in combinations(range(5), n):
            failures = [i for i, q in enumerate(ROWS)
                        if len(set(q)) == 4 and {q[s] for s in spokes} == U]
            assert failures
            t4_spoke_obstructions.append(dict(original_spokes=spokes,
                all_rejected_T4_rows=failures, first_boundary_witness=ROWS[failures[0]]))
    assert len(t4_spoke_obstructions) == 6
    return dict(original_contact_order=['C_x', 'C_y', 'C_z'],
        target_orbits={str(m): orbit(m) for m in (933, 941)},
        singleton_row_indices=singleton_rows, named_spoke_geometry=geometry,
        target_queries=queries, surviving_target_queries=0,
        T4_spoke_obstructions=t4_spoke_obstructions,
        scope='Capacity-one necessary consequences only; no source realizability claim.')


def relation_controls():
    contacts = tuple(product(range(4), repeat=3))
    spoke_tuples = tuple(product(range(4), repeat=3))
    digest = sha256()
    singleton_count = pair_count = 0
    non_cartesian = None
    for spokes in spoke_tuples:
        fibers = {}
        for p in contacts:
            fiber = tuple((a,) + spokes + p for a in range(4)
                          if a not in spokes + p)
            independent = tuple((a,) + spokes + p
                                for a in sorted(U - set(spokes) - set(p)))
            assert fiber == independent
            fibers[p] = fiber
            singleton_count += 1
            digest.update(json.dumps([spokes, p, fiber]).encode())
        for p, q in combinations(contacts, 2):
            relation = (p, q)
            joined = tuple(sorted(fibers[p] + fibers[q]))
            direct = tuple(sorted((a,) + spokes + t
                for a, t in product(range(4), relation) if a not in spokes + t))
            assert joined == direct
            forbidden = set(p) & set(q)
            assert {t[0] for t in joined} == U - set(spokes) - forbidden
            marginals = tuple(tuple(sorted({p[k], q[k]})) for k in range(3))
            extra = sorted(set(product(*marginals)) - set(relation))
            if non_cartesian is None and len(forbidden) <= 1 and extra and joined:
                non_cartesian = dict(literal_spoke_tuple=spokes,
                    original_ordered_ternary_relation=relation,
                    full_seven_port_relation=joined,
                    forbidden_colors=sorted(forbidden),
                    marginal_product_tuples_absent_from_original_relation=extra)
            pair_count += 1
            digest.update(json.dumps([spokes, relation, joined]).encode())
    assert singleton_count == 4096 and pair_count == 129024
    assert non_cartesian is not None
    return dict(port_order=['r', 'b_s', 'b_t', 'b_u', 'C_x', 'C_y', 'C_z'],
        all_ordered_contact_tuples=contacts,
        all_literal_ordered_spoke_color_tuples=spoke_tuples,
        singleton_relation_spoke_tuple_checks=singleton_count,
        two_element_relation_spoke_tuple_checks=pair_count,
        full_relation_sha256=digest.hexdigest(), non_cartesian_witness=non_cartesian,
        arbitrary_relation_coverage='For every nonempty original relation, the '
            'complete join is the union of its ordered-tuple fibers. A root color '
            'occurs precisely when some complete tuple avoids that color.',
        scope='Abstract exact relation controls; the capacity-one source bound '
              'is a separate arbitrary-size paper K5 argument.')


def build():
    sources = [Path(__file__).resolve(), ROOT / 'scripts/c5_independent_support_capacity.py',
               ROOT / 'scripts/c5_excess_two_three_unary.py']
    return dict(schema=1, scope='t=3 original (3) whole-source exclusion',
        source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                       for p in sources},
        pattern_order=ROWS, source_controls=source_controls(),
        complete_relation_controls=relation_controls(),
        paper_dependencies=['slack gives a nonempty complete original ternary relation',
            'two forbidden root colors force the original active triangle and three arms',
            'the original three tethers and any one original spoke give a K5 minor',
            'therefore each proper row has ternary forbidden capacity at most one'],
        summary=dict(named_spoke_triples=10, target_queries=100, remaining=0,
            T4_four_or_five_spoke_controls=6,
            singleton_seven_port_checks=4096, two_element_seven_port_checks=129024,
            graph_enumeration=False, disk_realizability_claim=False, new_Lean_theorem=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    payload = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.check:
        assert OUT.read_text() == payload, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
