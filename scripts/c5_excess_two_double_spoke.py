#!/usr/bin/env python3
"""Restore two named spokes at one degree-six root over a degree-four core.

This is a conditional source exclusion, not coverage of all excess-two sources.
Keep the original ordered four-port relation, attachments and omission identities.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

from c5_independent_support_capacity import B, FRAME, ROWS, T4, U, components
from c5_941_two_spoke import (
    Q4, base_record, component_record, relabel_mask, search, singleton_positions,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_double_spoke/observations.json'
CORES = ROOT / 'artifacts/c5_941_two_spoke/observations.json'


def literal(value):
    return json.loads(json.dumps(value))


def marked_record(base, old, target_orbits):
    """Reconstruct all original component tuples, then restore both spokes."""
    n, r = base['vertices'], old['root']
    edges = set(map(tuple, base['edges']))
    interior = set(range(5, n))
    neighbors = {v: {b if a == v else a for a, b in edges if v in (a, b)}
                 for v in range(n)}
    spoke, = sorted(neighbors[r] & B)
    parts = components(interior - {r}, edges)
    binary, = [vs for vs in parts if len(set(vs) & neighbors[r]) == 2]
    unary, = [vs for vs in parts if len(set(vs) & neighbors[r]) == 1]
    x, y = sorted(set(binary) & neighbors[r])
    u, = sorted(set(unary) & neighbors[r])
    assert len(parts) == 2 and (x, y) in edges
    assert old['port_order'] == [r, x, y, u]
    assert old['existing_spoke'] == [spoke, r]
    assert old['binary_vertices'] == binary and old['binary_contacts'] == [x, y]
    assert old['unary_vertices'] == unary and old['unary_contact'] == u
    ports = old['port_order']
    rows = []
    for row, saved in zip(ROWS, old['rows'], strict=True):
        assert saved['row'] == list(row)
        c = component_record(binary, [x, y], edges, row)
        unit = component_record(unary, [u], edges, row)
        assert saved['binary'] == literal(c) and saved['unary'] == literal(unit)
        expected = {(a, cx, cy, cu[0]) for a in U - {row[spoke]}
                    for cx, cy in c['ordered_relation']
                    for cu in unit['ordered_relation'] if a not in {cx, cy, cu[0]}}
        actual = {tuple(f[v] for v in ports)
                  for f in search(interior, edges, dict(enumerate(row)))}
        assert actual == expected == set(map(tuple, saved['ordered_port_relation']))
        for t, witness in zip(saved['ordered_port_relation'], saved['tuple_witnesses'], strict=True):
            assert len(witness) == n and witness[:5] == list(row)
            assert all(c in U for c in witness)
            assert [witness[v] for v in ports] == t
            assert all(witness[a] != witness[b] for a, b in edges)
        rows.append(saved)

    additions = []
    for pair in combinations(sorted(B - {spoke}), 2):
        extended = edges | {(b, r) for b in pair}
        spokes = [spoke, *pair]
        assert sum(r in e for e in extended) == 6
        result_rows = []
        for row, saved in zip(ROWS, rows, strict=True):
            relation = list(map(tuple, saved['ordered_port_relation']))
            retained = [i for i, t in enumerate(relation)
                        if all(t[0] != row[b] for b in pair)]
            actual = {tuple(f[v] for v in ports)
                      for f in search(interior, extended, dict(enumerate(row)))}
            assert actual == {relation[i] for i in retained}
            intermediate = []
            for b in pair:
                indices = [i for i, t in enumerate(relation) if t[0] != row[b]]
                exact = {tuple(f[v] for v in ports) for f in search(
                    interior, edges | {(b, r)}, dict(enumerate(row)))}
                assert exact == {relation[i] for i in indices}
                intermediate.append(indices)
            assert retained == sorted(set(intermediate[0]) & set(intermediate[1]))
            factors = [{row[b]} for b in spokes] + [
                set(saved['binary']['forbidden']), set(saved['unary']['forbidden'])]
            assert U - set.union(*factors) == {t[0] for t in actual}
            # All five original factors; component deletion removes the whole
            # original component, never just one endpoint or its color mask.
            factor_deletions = []
            for i in range(5):
                removed_vertices = (set(binary) if i == 3 else
                                    set(unary) if i == 4 else set())
                removed = ({(spokes[i], r)} if i < 3 else
                           {e for e in extended if set(e) & removed_vertices})
                child = next(search(interior - removed_vertices, extended - removed,
                                    dict(enumerate(row))), None)
                omitted_rejects = set.union(*(f for j, f in enumerate(factors) if j != i)) == U
                assert (child is None) == omitted_rejects
                factor_deletions.append(omitted_rejects)
            # Save all pairs of original spoke identities, including pairs
            # other than the two just added. The relation can then grow beyond
            # the base relation, so recompute from the original components.
            pair_deletions = []
            for omitted in combinations(range(3), 2):
                child_edges = extended - {(spokes[i], r) for i in omitted}
                expected = {(a, cx, cy, cu[0]) for a in U
                    if all(a != row[b] for i, b in enumerate(spokes) if i not in omitted)
                    for cx, cy in saved['binary']['ordered_relation']
                    for cu in saved['unary']['ordered_relation'] if a not in {cx, cy, cu[0]}}
                choices = list(search(interior, child_edges, dict(enumerate(row))))
                exact = {tuple(f[v] for v in ports) for f in choices}
                assert exact == expected
                if omitted == (1, 2):
                    assert exact == set(relation)
                tuples = sorted(exact)
                witnesses = [[next(f for f in choices if tuple(f[v] for v in ports) == t)[v]
                              for v in range(n)] for t in tuples]
                pair_deletions.append(dict(omitted_spoke_indices=omitted,
                    ordered_port_relation=tuples, tuple_witnesses=witnesses))
            result_rows.append(dict(retained_port_tuple_indices=retained,
                single_restoration_port_tuple_indices=intermediate,
                omitted_factor_indices=[i for i, rejects in enumerate(factor_deletions) if rejects],
                spoke_pair_deletions=pair_deletions))
        sigma = sum(1 << i for i, row in enumerate(result_rows) if row['retained_port_tuple_indices'])
        assert all(sigma not in orbit for orbit in target_orbits.values())
        t4, rejected = sigma & T4 == T4, singleton_positions(sigma)
        if t4:
            assert len(rejected) == 1 or (len(rejected) == 2 and
                                         (rejected[0] - rejected[1]) % 5 in (1, 4))
        additions.append(dict(added_spokes=[[b, r] for b in pair], sigma=sigma,
            accepts_T4=t4, rejected_singleton_positions=rejected,
            factor_order=[dict(kind='spoke', edge=[b, r]) for b in spokes] + [
                dict(kind='binary', vertices=binary, contacts=[x, y]),
                dict(kind='unary', vertices=unary, contacts=[u])], rows=result_rows))
    record = {key: value for key, value in old.items() if key not in ('additions', 'factor_order')}
    for kind, vertices in [('binary', binary), ('unary', unary)]:
        record[kind + '_boundary_attachments'] = [
            dict(vertex=v, neighbors=sorted(neighbors[v] & B)) for v in vertices]
        assert record[kind + '_support'] == sorted(set.union(*(neighbors[v] & B for v in vertices)))
    record['additions'] = additions
    return record


def build():
    source = json.loads(CORES.read_text())
    for path, digest in source['source_sha256'].items():
        assert sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    assert source['pattern_order'] == literal(ROWS)
    target_orbits = {str(mask): sorted({relabel_mask(mask, [(s*j + t) % 5 for j in range(5)])
                                      for s in (-1, 1) for t in range(5)}) for mask in (933, 941)}
    bases = source['bases']
    for base in bases:
        assert literal(base_record(base['family'], base['input_index'], base)) == base
    # Reconstruct the complete set of degree-three markings from the saved
    # original edges; an omitted or duplicated marked core cannot pass.
    expected_marks = {(bi, r) for bi, base in enumerate(bases)
                      for r in range(5, base['vertices'])
                      if sum(r in e and min(e) >= 5 for e in base['edges']) == 3}
    marks = [(m['base_id'], m['root']) for m in source['marked_models']]
    assert len(marks) == len(set(marks)) and set(marks) == expected_marks
    marked = [marked_record(bases[m['base_id']], m, target_orbits) for m in source['marked_models']]
    additions = [a for m in marked for a in m['additions']]
    histogram = Counter(a['sigma'] for a in additions)
    family_histograms = {family: dict(sorted(Counter(a['sigma'] for m in marked
        if bases[m['base_id']]['family'] == family for a in m['additions']).items()))
        for family in sorted({base['family'] for base in bases})}
    assert len(bases) == 82 and len(marked) == 148 and len(additions) == 888
    assert sum(a['accepts_T4'] for a in additions) == 432
    assert {s: count for s, count in histogram.items() if s & T4 == T4} == {
        958: 76, 1020: 76, 1022: 280}
    dependencies = [Path(__file__).resolve(), ROOT / 'scripts/c5_941_two_spoke.py',
                    ROOT / 'scripts/c5_independent_support_capacity.py', CORES]
    return dict(schema=1,
        scope='conditional degree-six source with two original spokes omitted to a degree-four rejected-row core',
        source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in dependencies},
        inherited_source_sha256=source['source_sha256'], pattern_order=ROWS,
        normalized_omitted_row=Q4, target_D5_orbits=target_orbits,
        bases=bases, marked_models=marked,
        tuple_index_semantics='both restoration orders index the same complete original (r,x,y,u) tuples and full coloring witnesses',
        summary=dict(bases=len(bases), marked_roots=len(marked), restored_spoke_pair_models=len(additions),
            full_ten_row_checks=10*len(additions), single_restoration_queries=20*len(additions),
            factor_deletion_queries=50*len(additions), spoke_pair_deletion_queries=30*len(additions),
            T4_accepting_models=432, sigma_histogram=dict(sorted(histogram.items())),
            family_sigma_histograms=family_histograms, candidate_933_models=0, candidate_941_models=0,
            T4_models_have_at_most_two_adjacent_singleton_rejections=True,
            covers_all_excess_two_sources=False, arbitrary_size_coverage_is_paper=True,
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
