#!/usr/bin/env python3
"""Exclude a spoke-plus-unary omission core at a degree-six, two-spoke root.

The five-port kernel is an exact gluing operator, not an invented unary source.
The original omitted component stays arbitrary and has a nonempty endpoint
relation by the paper slack argument. No unary graph census or disk oracle.
"""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

from c5_independent_support_capacity import B, FRAME, ROWS, T4, U, components
from c5_941_two_spoke import (
    Q4, base_record, component_record, relabel_mask, search, singleton_positions,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_spoke_unary/observations.json'
CORES = ROOT / 'artifacts/c5_941_two_spoke/observations.json'


def literal(value):
    return json.loads(json.dumps(value))


def marked_record(base, old, target_orbits):
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
    ports = [r, x, y, u]
    assert len(parts) == 2 and (x, y) in edges
    assert old['port_order'] == ports and old['existing_spoke'] == [spoke, r]
    assert old['binary_vertices'] == binary and old['binary_contacts'] == [x, y]
    assert old['unary_vertices'] == unary and old['unary_contact'] == u
    rows = []
    for row, saved in zip(ROWS, old['rows'], strict=True):
        assert saved['row'] == list(row)
        c = component_record(binary, [x, y], edges, row)
        unit = component_record(unary, [u], edges, row)
        assert saved['binary'] == literal(c) and saved['unary'] == literal(unit)
        joined = {(a, cx, cy, cu[0]) for a in U - {row[spoke]}
                  for cx, cy in c['ordered_relation'] for cu in unit['ordered_relation']
                  if a not in {cx, cy, cu[0]}}
        actual = {tuple(f[v] for v in ports)
                  for f in search(interior, edges, dict(enumerate(row)))}
        assert actual == joined == set(map(tuple, saved['ordered_port_relation']))
        assert len(saved['ordered_port_relation']) == len(saved['tuple_witnesses'])
        for t, witness in zip(saved['ordered_port_relation'], saved['tuple_witnesses'], strict=True):
            assert len(witness) == n and witness[:5] == list(row)
            assert all(a in U for a in witness) and [witness[v] for v in ports] == t
            assert all(witness[a] != witness[b] for a, b in edges)
        rows.append(saved)

    additions = []
    assert [a['added_spoke'] for a in old['additions']] == [[b, r] for b in sorted(B - {spoke})]
    for old_addition in old['additions']:
        added, = [b for b in old_addition['added_spoke'] if b != r]
        extended = edges | {(added, r)}
        assert sum(r in e for e in extended) == 5
        result_rows = []
        for row, saved, old_row in zip(ROWS, rows, old_addition['rows'], strict=True):
            relation = list(map(tuple, saved['ordered_port_relation']))
            retained = [i for i, t in enumerate(relation) if t[0] != row[added]]
            exact = {tuple(f[v] for v in ports)
                     for f in search(interior, extended, dict(enumerate(row)))}
            assert exact == {relation[i] for i in retained}
            assert retained == old_row['retained_port_tuple_indices']
            # The extra variable n is a free endpoint in the gluing operator,
            # not a degree-four graph claimed to realize the omitted V.
            kernel = sorted(t + (d,) for t in exact for d in U if t[0] != d)
            operator_edges = extended | {(r, n)}
            operator_choices = list(search(interior | {n}, operator_edges, dict(enumerate(row))))
            assert set(kernel) == {tuple(f[v] for v in ports + [n]) for f in operator_choices}
            roots = sorted({t[0] for t in exact})
            by_endpoint = [[i for i, t in enumerate(kernel) if t[-1] == d] for d in range(4)]
            universal = all(by_endpoint)
            assert universal == (len(roots) >= 2)
            relation_lookup = {t: i for i, t in enumerate(relation)}
            witness_indices = [relation_lookup[t[:4]] for t in kernel]
            for t, wi in zip(kernel, witness_indices, strict=True):
                witness = saved['tuple_witnesses'][wi] + [t[-1]]
                assert all(witness[a] != witness[b] for a, b in operator_edges)
                assert tuple(witness[v] for v in ports + [n]) == t
            # Every nonempty *complete* unary relation, including nonsingletons.
            # This is a local universal quantifier, not independent cross-row
            # graph realizability or a replacement for the actual V relation.
            audits = []
            for mask in range(1, 16):
                values = {d for d in U if mask >> d & 1}
                indices = [i for i, t in enumerate(kernel) if t[-1] in values]
                exact_join = {t + (d,) for t in exact for d in values if t[0] != d}
                assert exact_join == {kernel[i] for i in indices}
                factor_forbidden = values if len(values) == 1 else set()
                assert bool(exact_join) == bool(set(roots) - factor_forbidden)
                if universal:
                    assert indices
                audits.append(dict(endpoint_relation=sorted(values),
                    joined_tuple_indices=indices,
                    witness_tuple_index=indices[0] if indices else None))
            result_rows.append(dict(retained_core_tuple_indices=retained,
                root_colors=roots, ordered_five_port_kernel=kernel,
                kernel_core_witness_indices=witness_indices,
                kernel_indices_by_endpoint_color=by_endpoint,
                survives_every_nonempty_unary_relation=universal,
                nonempty_unary_relation_audits=audits))
        sigma = sum(1 << i for i, row in enumerate(result_rows) if row['retained_core_tuple_indices'])
        assert sigma == old_addition['sigma']
        universal_mask = sum(1 << i for i, row in enumerate(result_rows)
                             if row['survives_every_nonempty_unary_relation'])
        exclusions = []
        for candidate, orbit in target_orbits.items():
            for target in orbit:
                lost = [i for i in range(10) if target >> i & 1 and not (sigma >> i & 1)]
                if lost:
                    exclusions.append(dict(candidate=candidate, target=target,
                        reason='core_already_rejects_required_acceptance', row_index=lost[0]))
                else:
                    witnesses = [i for i in range(10) if universal_mask >> i & 1 and not (target >> i & 1)]
                    assert witnesses, (old['base_id'], r, added, target)
                    i = witnesses[0]
                    assert len(set(ROWS[i])) == 3
                    exclusions.append(dict(candidate=candidate, target=target,
                        reason='unary_cannot_block_two_root_colors', row_index=i,
                        endpoint_color_witness_indices=[indices[0] for indices in
                            result_rows[i]['kernel_indices_by_endpoint_color']]))
        # A deliberately enlarged row-wise model. These masks are bounds,
        # never claims that one same-graph unary V realizes all ten relations.
        possible = [mask for mask in range(1024) if mask & T4 == T4
                    and mask & sigma == mask and mask & universal_mask == universal_mask]
        assert not any(mask in orbit for orbit in target_orbits.values() for mask in possible)
        additions.append(dict(added_spoke=[added, r], intermediate_sigma=sigma,
            universal_acceptance_mask=universal_mask, accepts_T4=sigma & T4 == T4,
            enlarged_possible_full_masks=possible, exclusions=exclusions, rows=result_rows))
    record = {key: value for key, value in old.items() if key not in ('additions', 'factor_order')}
    for kind, vertices in [('binary', binary), ('unary', unary)]:
        record[kind + '_boundary_attachments'] = [dict(vertex=v, neighbors=sorted(neighbors[v] & B))
                                                for v in vertices]
        assert record[kind + '_support'] == sorted(set.union(*(neighbors[v] & B for v in vertices)))
    record['five_port_order'] = ports + ['original_omitted_endpoint_v']
    record['factor_order'] = ['existing_spoke', 'added_spoke', 'C_2', 'U', 'original_omitted_V']
    record['omission_identity'] = ['added_spoke', 'original_omitted_V']
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
    expected = {(bi, r) for bi, base in enumerate(bases) for r in range(5, base['vertices'])
                if sum(r in e and min(e) >= 5 for e in base['edges']) == 3}
    marks = [(m['base_id'], m['root']) for m in source['marked_models']]
    assert len(marks) == len(set(marks)) and set(marks) == expected
    marked = [marked_record(bases[m['base_id']], m, target_orbits) for m in source['marked_models']]
    additions = [a for m in marked for a in m['additions']]
    counts = {candidate: dict(sorted(Counter(e['reason'] for a in additions
                    for e in a['exclusions'] if e['candidate'] == candidate).items()))
              for candidate in target_orbits}
    possible_histogram = Counter(mask for a in additions for mask in a['enlarged_possible_full_masks'])
    interval_histogram = Counter((a['intermediate_sigma'], a['universal_acceptance_mask'] | T4)
                                for a in additions if a['accepts_T4'])
    assert len(bases) == 82 and len(marked) == 148 and len(additions) == 592
    assert sum(a['accepts_T4'] for a in additions) == 444
    assert counts == {
        '933': {'core_already_rejects_required_acceptance': 1264, 'unary_cannot_block_two_root_colors': 1696},
        '941': {'core_already_rejects_required_acceptance': 1788, 'unary_cannot_block_two_root_colors': 1172}}
    assert dict(possible_histogram) == {942: 6, 958: 218, 1006: 2, 1012: 6, 1014: 2, 1020: 218, 1022: 364}
    dependencies = [Path(__file__).resolve(), ROOT / 'scripts/c5_941_two_spoke.py',
                    ROOT / 'scripts/c5_independent_support_capacity.py', CORES]
    return dict(schema=1,
        scope='conditional excess-two unique degree-six two-spoke source, with a spoke and original unary component omitted to a rejected degree-four core',
        source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in dependencies},
        inherited_source_sha256=source['source_sha256'], pattern_order=ROWS,
        normalized_omitted_row=Q4, target_D5_orbits=target_orbits, bases=bases, marked_models=marked,
        kernel_semantics='five-port gluing operator; restrict the last coordinate to the actual original V endpoint relation, then glue its full coloring witness; V is never replaced by the free endpoint control graph',
        interval_histogram=[dict(intermediate_sigma=upper, forced_T4_acceptance_mask=lower,
                                 possible_rejected_singleton_positions=singleton_positions(lower), count=count)
                            for (upper, lower), count in sorted(interval_histogram.items())],
        summary=dict(bases=len(bases), marked_roots=len(marked), spoke_restorations=len(additions),
            T4_accepting_intermediates=444, core_ten_row_checks=10*len(marked),
            restored_ten_row_checks=10*len(additions), five_port_kernel_checks=10*len(additions),
            nonempty_unary_relation_checks=150*len(additions), candidate_comparisons=10*len(additions),
            exclusion_counts=counts, enlarged_mask_histogram=dict(sorted(possible_histogram.items())),
            surviving_candidate_comparisons=0, arbitrary_size_coverage_is_paper=True,
            omitted_unary_graph_enumerated=False, full_source_disk_realizability_checked=False,
            covers_all_excess_two_sources=False, new_lean_theorem=False))


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
