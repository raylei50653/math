#!/usr/bin/env python3
"""Restore a third named spoke at an original degree-two triangle vertex.

The finite necessary domain uses saved cores and all bare-triangle supports.
Arbitrary-size coverage and relation-preserving tail reduction are paper steps.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from c5_independent_support_capacity import B, FRAME, ROWS, T4, U, colorings, components
from c5_941_two_spoke import (
    Q4, base_record, component_record,
    relabel_mask, search, singleton_positions, tail_controls,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_941_three_spoke/observations.json'
# Keep input paths explicit so the artifact tool records producer dependencies.
BRANCHES = ROOT / 'artifacts/c5_triangle_branches/observations.json'
PATHS = ROOT / 'artifacts/c5_triangle_path_reduction/observations.json'
DOUBLE = ROOT / 'artifacts/c5_two_triangle_blocks/observations.json'


def bare_triangles():
    """All q4-critical bare triangles; no planarity filter or size search."""
    records = []
    for missing in combinations(range(3), 2):
        options = [tuple(sorted((a, b))) for a in sorted(B) for b in sorted(B)
                   if Q4[a] == missing[0] and Q4[b] == missing[1]]
        for neighborhoods in product(options, repeat=3):
            edges = FRAME | {(5, 6), (5, 7), (6, 7)} | {
                (b, 5 + i) for i, support in enumerate(neighborhoods) for b in support}
            rows = []
            for row in ROWS:
                choices = list(search(range(5, 8), edges, dict(enumerate(row))))
                tuples = sorted(tuple(f[v] for v in range(5, 8)) for f in choices)
                assert tuples == sorted(tuple(f[v] for v in range(5, 8))
                    for f in colorings(range(5, 8), edges, dict(enumerate(row))))
                rows.append(dict(row=row, interior_order=[5, 6, 7],
                                 complete_interior_colorings=tuples))
            sigma = sum(1 << i for i, row in enumerate(rows)
                        if row['complete_interior_colorings'])
            assert not rows[ROWS.index(Q4)]['complete_interior_colorings']
            critical = []
            for edge in sorted(edges - FRAME):
                witness = next(search(range(5, 8), edges - {edge}, dict(enumerate(Q4))), None)
                assert witness is not None
                critical.append(dict(edge=edge, coloring=[witness[v] for v in range(8)]))
            assert all(sum(v in e for e in edges) == 4 for v in range(5, 8))
            t4 = sigma & T4 == T4
            if t4:
                assert sigma == 1022
            records.append(dict(family='bare_triangle', input_index=len(records),
                vertices=8, edges=sorted(edges), neighborhoods=neighborhoods,
                common_q4_palette=sorted(U - set(missing)), sigma=sigma,
                accepts_T4=t4, rows=rows, q4_critical_witnesses=critical,
                disk_realizability_checked=False))
    assert len(records) == 80 and sum(r['accepts_T4'] for r in records) == 36
    return records


def marked_record(base_id, base, r, target_orbit):
    n, edges = base['vertices'], set(map(tuple, base['edges']))
    neighbors = {v: {b if a == v else a for a, b in edges if v in (a, b)}
                 for v in range(n)}
    spokes = sorted(neighbors[r] & B)
    assert len(spokes) == 2
    interior = set(range(5, n))
    binary, = components(interior - {r}, edges)
    x, y = sorted(neighbors[r] & set(binary))
    assert (x, y) in edges
    ports = [r, x, y]
    rows = []
    for row in ROWS:
        c = component_record(binary, [x, y], edges, row)
        expected = sorted((a, cx, cy) for a in sorted(U - {row[b] for b in spokes})
                          for cx, cy in c['ordered_relation'] if a not in {cx, cy})
        choices = list(search(interior, edges, dict(enumerate(row))))
        relation = sorted({tuple(f[v] for v in ports) for f in choices})
        assert relation == expected
        witnesses = [[next(f for f in choices if tuple(f[v] for v in ports) == t)[v]
                      for v in range(n)] for t in relation]
        rows.append(dict(row=row, binary=c, ordered_port_relation=relation,
                         tuple_witnesses=witnesses))
    additions = []
    for added in sorted(B - set(spokes)):
        extended = edges | {(added, r)}
        factor_spokes = spokes + [added]
        result_rows = []
        for row, saved in zip(ROWS, rows):
            retained = [i for i, t in enumerate(saved['ordered_port_relation'])
                        if t[0] != row[added]]
            exact = {tuple(f[v] for v in ports)
                     for f in search(interior, extended, dict(enumerate(row)))}
            assert exact == {saved['ordered_port_relation'][i] for i in retained}
            factors = [{row[b]} for b in factor_spokes] + [set(saved['binary']['forbidden'])]
            assert U - set.union(*factors) == {t[0] for t in exact}
            omitted = [i for i in range(4) if set.union(
                *(f for j, f in enumerate(factors) if i != j)) == U]
            assert not omitted or not retained
            for i in range(4):
                removed = ({(factor_spokes[i], r)} if i < 3 else
                           {e for e in extended if set(e) & set(binary)})
                remaining = interior if i < 3 else {r}
                child = next(search(remaining, extended - removed, dict(enumerate(row))), None)
                assert (child is None) == (i in omitted)
            result_rows.append(dict(retained_port_tuple_indices=retained,
                                    omitted_factor_indices=omitted))
        sigma = sum(1 << i for i, data in enumerate(result_rows)
                    if data['retained_port_tuple_indices'])
        assert sigma not in target_orbit
        t4, rejected = sigma & T4 == T4, singleton_positions(sigma)
        additions.append(dict(added_spoke=[added, r], sigma=sigma, accepts_T4=t4,
            factor_order=[dict(kind='spoke', edge=[b, r]) for b in factor_spokes]
                         + [dict(kind='binary', vertices=binary, contacts=[x, y])],
            rejected_singleton_positions=rejected, rows=result_rows))
    return dict(base_id=base_id, root=r, existing_spokes=[[b, r] for b in spokes],
        binary_vertices=binary, binary_contacts=[x, y],
        binary_boundary_attachments=[dict(vertex=v, neighbors=sorted(neighbors[v] & B))
                                     for v in binary],
        binary_support=sorted(set.union(*(neighbors[v] & B for v in binary))),
        port_order=ports, rows=rows, additions=additions)


def build():
    branch_data = json.loads(BRANCHES.read_text())
    path_data = json.loads(PATHS.read_text())
    double_data = json.loads(DOUBLE.read_text())
    tails = tail_controls(branch_data['disk_templates'], path_data)
    target_orbit = sorted({relabel_mask(941, [(s*j + t) % 5 for j in range(5)])
                           for s in (-1, 1) for t in range(5)})
    bare = bare_triangles()
    bases = [dict(record) for record in bare if record['accepts_T4']]
    for family, data in [('single_triangle', branch_data), ('double_triangle', double_data)]:
        for index, base in enumerate(data['disk_templates']):
            if base['sigma'] == 1022:
                bases.append(base_record(family, index, base))
    marked, counts = [], Counter()
    for base_id, base in enumerate(bases):
        family, edges = base['family'], set(map(tuple, base['edges']))
        counts[family + '_bases'] += 1
        for r in range(5, base['vertices']):
            contacts = sorted(v for v in range(5, base['vertices'])
                              if tuple(sorted((v, r))) in edges)
            if len(contacts) != 2 or tuple(contacts) not in edges:
                continue
            marked.append(marked_record(base_id, base, r, target_orbit))
            counts[family + '_marked_roots'] += 1
    additions = [a for model in marked for a in model['additions']]
    histogram = Counter(a['sigma'] for a in additions)
    family_histograms = {family: dict(sorted(Counter(a['sigma']
        for model in marked if bases[model['base_id']]['family'] == family
        for a in model['additions']).items())) for family in sorted({b['family'] for b in bases})}
    assert len(bases) == 118 and len(marked) == 398 and len(additions) == 1194
    dependencies = [Path(__file__).resolve(), ROOT / 'scripts/c5_941_two_spoke.py',
                    ROOT / 'scripts/c5_independent_support_capacity.py', BRANCHES, PATHS, DOUBLE]
    return dict(schema=1,
        scope='finite necessary marked-core restoration; arbitrary-size coverage is inherited paper classification and tail transfer',
        source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in dependencies},
        pattern_order=ROWS, normalized_omitted_row=Q4, target_D5_orbit=target_orbit,
        bare_triangle_controls=bare, tail_root_controls=tails, bases=bases, marked_models=marked,
        tuple_index_semantics='addition rows index complete base (r,x,y) tuples and full coloring witnesses in one literal boundary frame',
        summary=dict(**dict(sorted(counts.items())), bare_support_models=len(bare),
            bare_models_rejected_by_T4=44, bases=len(bases), marked_roots=len(marked),
            restored_spoke_models=len(additions), full_ten_row_checks=10*len(additions),
            factor_deletion_queries=40*len(additions),
            T4_accepting_models=sum(a['accepts_T4'] for a in additions),
            sigma_histogram=dict(sorted(histogram.items())), family_sigma_histograms=family_histograms,
            candidate_941_models=0, remaining_941_excess_one_spokes=[],
            candidate_941_excess_lower_bound_with_prior_exclusions=2,
            uniform_tail_root_checks=tails['full_row_uniform_checks'],
            two_run_tail_root_checks=tails['full_row_two_run_checks'],
            restored_graph_disk_realizability_checked=False,
            new_source_graph_census=False, new_lean_theorem=False))


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
