#!/usr/bin/env python3
"""Exclude the triangle-root three-spoke-plus-unary omission branch.

The original unary V stays arbitrary. Four-port kernels are gluing operators,
not graphs asserted to realize V. Shared omissions use the same original V
and binary component in every row; arbitrary-size coverage is a paper step.
"""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

from c5_independent_support_capacity import B, ROWS, T4, U, components
from c5_941_two_spoke import Q4, base_record, component_record, relabel_mask, search
from c5_941_three_spoke import bare_triangles

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_three_spoke_unary/observations.json'
CORES = ROOT / 'artifacts/c5_941_three_spoke/observations.json'
DOUBLE_SPOKE = ROOT / 'artifacts/c5_excess_two_double_spoke/observations.json'


def literal(value):
    return json.loads(json.dumps(value))


def verified_source(path):
    source = json.loads(path.read_text())
    for name, digest in source['source_sha256'].items():
        assert sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
    assert source['pattern_order'] == literal(ROWS)
    return source


def marked_record(base, old, target_orbits):
    n, r = base['vertices'], old['root']
    edges = set(map(tuple, base['edges']))
    interior = set(range(5, n))
    neighbors = {v: {b if a == v else a for a, b in edges if v in (a, b)}
                 for v in range(n)}
    spokes = sorted(neighbors[r] & B)
    binary, = components(interior - {r}, edges)
    x, y = sorted(set(binary) & neighbors[r])
    ports = [r, x, y]
    assert len(spokes) == 2 and (x, y) in edges
    assert old['port_order'] == ports
    assert old['existing_spokes'] == [[b, r] for b in spokes]
    assert old['binary_vertices'] == binary and old['binary_contacts'] == [x, y]
    attachments = [dict(vertex=v, neighbors=sorted(neighbors[v] & B)) for v in binary]
    assert old['binary_boundary_attachments'] == attachments
    assert old['binary_support'] == sorted(set.union(*(neighbors[v] & B for v in binary)))
    rows = []
    for row, saved in zip(ROWS, old['rows'], strict=True):
        assert saved['row'] == list(row)
        c = component_record(binary, [x, y], edges, row)
        assert saved['binary'] == literal(c)
        joined = {(a, cx, cy) for a in U - {row[b] for b in spokes}
                  for cx, cy in c['ordered_relation'] if a not in {cx, cy}}
        actual = {tuple(f[v] for v in ports)
                  for f in search(interior, edges, dict(enumerate(row)))}
        assert actual == joined == set(map(tuple, saved['ordered_port_relation']))
        for t, witness in zip(saved['ordered_port_relation'], saved['tuple_witnesses'], strict=True):
            assert len(witness) == n and witness[:5] == list(row)
            assert all(c in U for c in witness) and [witness[v] for v in ports] == t
            assert all(witness[a] != witness[b] for a, b in edges)
        rows.append(saved)

    additions = []
    assert [a['added_spoke'] for a in old['additions']] == [[b, r] for b in sorted(B - set(spokes))]
    for old_addition in old['additions']:
        added, other = old_addition['added_spoke']
        assert other == r
        all_spokes = sorted(spokes + [added])
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
            # n labels the free unary endpoint variable, never an actual V.
            kernel = sorted(t + (d,) for t in exact for d in U if t[0] != d)
            operator_edges = extended | {(r, n)}
            operator = {tuple(f[v] for v in ports + [n])
                        for f in search(interior | {n}, operator_edges, dict(enumerate(row)))}
            assert set(kernel) == operator
            roots = sorted({t[0] for t in exact})
            by_endpoint = [[i for i, t in enumerate(kernel) if t[-1] == d] for d in range(4)]
            assert all(by_endpoint) == (len(roots) >= 2)
            lookup = {t: i for i, t in enumerate(relation)}
            witness_indices = [lookup[t[:3]] for t in kernel]
            for t, wi in zip(kernel, witness_indices, strict=True):
                witness = saved['tuple_witnesses'][wi] + [t[-1]]
                assert all(witness[a] != witness[b] for a, b in operator_edges)
                assert tuple(witness[v] for v in ports + [n]) == t
            audits = []
            for mask in range(1, 16):
                values = {d for d in U if mask >> d & 1}
                indices = [i for i, t in enumerate(kernel) if t[-1] in values]
                exact_join = {t + (d,) for t in exact for d in values if t[0] != d}
                assert exact_join == {kernel[i] for i in indices}
                forbidden = values if len(values) == 1 else set()
                assert bool(exact_join) == bool(set(roots) - forbidden)
                # A nonempty core with a unique root color can be blocked
                # only by the same singleton complete endpoint relation.
                if roots and not indices:
                    assert len(roots) == 1 and values == set(roots)
                audits.append(dict(endpoint_relation=sorted(values), joined_tuple_indices=indices))

            # Remove the same complete C_2: only r, its spokes and original
            # unary V remain. This operator keeps V's endpoint variable.
            binary_omission = sorted((a, d) for a in U - {row[b] for b in all_spokes}
                                     for d in U if a != d)
            star_edges = {(b, r) for b in all_spokes} | {(r, n)}
            star_actual = {tuple(f[v] for v in [r, n])
                           for f in search({r, n}, star_edges, dict(enumerate(row)))}
            assert set(binary_omission) == star_actual

            # Each pair refers to original spokes; after deleting them,
            # recompute all tuples rather than filtering the smaller core.
            pair_omissions = []
            for kept in all_spokes:
                removed = [(b, r) for b in all_spokes if b != kept]
                child_edges = extended - set(removed)
                child = sorted((a, cx, cy, d) for a in U - {row[kept]}
                               for cx, cy in saved['binary']['ordered_relation']
                               if a not in {cx, cy} for d in U if a != d)
                child_actual = {tuple(f[v] for v in ports + [n]) for f in search(
                    interior | {n}, child_edges | {(r, n)}, dict(enumerate(row)))}
                assert set(child) == child_actual
                binary_lookup = {tuple(t): i for i, t in enumerate(saved['binary']['ordered_relation'])}
                binary_witness_indices = [binary_lookup[t[1:3]] for t in child]
                for t, wi in zip(child, binary_witness_indices, strict=True):
                    witness = list(row) + [None] * (n - 5) + [t[-1]]
                    witness[r] = t[0]
                    for vertex, color in zip(binary, saved['binary']['tuple_witnesses'][wi], strict=True):
                        witness[vertex] = color
                    assert all(c in U for c in witness)
                    assert tuple(witness[v] for v in ports + [n]) == t
                    assert all(witness[a] != witness[b] for a, b in child_edges | {(r, n)})
                pair_omissions.append(dict(removed_spokes=removed, retained_spoke=[kept, r],
                    ordered_four_port_kernel=child, kernel_binary_witness_indices=binary_witness_indices))
            result_rows.append(dict(retained_core_tuple_indices=retained, root_colors=roots,
                ordered_four_port_kernel=kernel, kernel_core_witness_indices=witness_indices,
                kernel_indices_by_endpoint_color=by_endpoint,
                nonempty_unary_relation_audits=audits,
                binary_omission_two_port_kernel=binary_omission,
                double_spoke_omissions=pair_omissions))

        sigma = sum(1 << i for i, row in enumerate(result_rows) if row['root_colors'])
        assert sigma == old_addition['sigma']
        universal = sum(1 << i for i, row in enumerate(result_rows) if len(row['root_colors']) >= 2)
        exclusions = []
        for candidate, orbit in target_orbits.items():
            for target in orbit:
                lost = [i for i in range(10) if target >> i & 1 and not (sigma >> i & 1)]
                forced = [i for i in range(10) if universal >> i & 1 and not (target >> i & 1)]
                certificate = dict(candidate=candidate, target=target)
                if lost:
                    certificate.update(reason='core_already_rejects_required_acceptance', row_index=lost[0])
                elif forced:
                    i = forced[0]
                    certificate.update(reason='unary_cannot_block_two_root_colors', row_index=i,
                        endpoint_color_witness_indices=[ids[0] for ids in
                            result_rows[i]['kernel_indices_by_endpoint_color']])
                else:
                    demands, binary_rows, pairs = [], [], []
                    for i, row in enumerate(result_rows):
                        if target >> i & 1 or not row['root_colors']:
                            continue
                        d, = row['root_colors']
                        assert len(set(ROWS[i])) == 3
                        demands.append(dict(row_index=i, original_V_endpoint_relation=[d]))
                        if not any(t[-1] == d for t in row['binary_omission_two_port_kernel']):
                            binary_rows.append(i)
                        for pi, pair in enumerate(row['double_spoke_omissions']):
                            if not any(t[-1] == d for t in pair['ordered_four_port_kernel']):
                                pairs.append(dict(row_index=i, pair_index=pi,
                                    removed_spokes=pair['removed_spokes']))
                    certificate['same_original_V_demands'] = demands
                    if len(binary_rows) >= 2:
                        certificate.update(reason='same_binary_omission_rejects_two_rows',
                            row_indices=binary_rows[:2], omitted_component_vertices=binary)
                    else:
                        assert pairs, (old['base_id'], r, added, target, demands)
                        certificate.update(reason='double_spoke_omission_still_rejects', **pairs[0])
                exclusions.append(certificate)
        additions.append(dict(added_spoke=[added, r], original_spokes=[[b, r] for b in all_spokes],
            intermediate_sigma=sigma, universal_acceptance_mask=universal,
            accepts_T4=sigma & T4 == T4, rows=result_rows, exclusions=exclusions))
    record = {key: value for key, value in old.items() if key != 'additions'}
    record.update(four_port_order=ports + ['original_omitted_endpoint_v'],
        omission_identity=dict(spoke='added_spoke', component='original_V'),
        factor_order=['original_spokes', 'original_C_2', 'original_V'], additions=additions)
    return record


def build():
    source = verified_source(CORES)
    prior = verified_source(DOUBLE_SPOKE)
    target_orbits = {str(mask): sorted({relabel_mask(mask, [(s*j+t) % 5 for j in range(5)])
                                      for s in (-1, 1) for t in range(5)}) for mask in (933, 941)}
    assert prior['target_D5_orbits'] == target_orbits
    bare = bare_triangles()
    assert source['bare_triangle_controls'] == literal(bare)
    bases = source['bases']
    assert bases[:36] == literal([b for b in bare if b['accepts_T4']])
    for base in bases[36:]:
        assert literal(base_record(base['family'], base['input_index'], base)) == base
    expected = set()
    for bi, base in enumerate(bases):
        edges = set(map(tuple, base['edges']))
        for r in range(5, base['vertices']):
            contacts = sorted(v for v in range(5, base['vertices']) if tuple(sorted((v, r))) in edges)
            if len(contacts) == 2 and tuple(contacts) in edges:
                expected.add((bi, r))
    marks = [(m['base_id'], m['root']) for m in source['marked_models']]
    assert len(marks) == len(set(marks)) and set(marks) == expected
    marked = [marked_record(bases[m['base_id']], m, target_orbits) for m in source['marked_models']]
    additions = [a for m in marked for a in m['additions']]
    counts = {c: dict(sorted(Counter(e['reason'] for a in additions for e in a['exclusions']
                                    if e['candidate'] == c).items())) for c in target_orbits}
    assert len(bases) == 118 and len(marked) == 398 and len(additions) == 1194
    assert sum(a['accepts_T4'] for a in additions) == 1114
    assert counts == {
        '933': {'core_already_rejects_required_acceptance': 1556,
                'unary_cannot_block_two_root_colors': 3940,
                'same_binary_omission_rejects_two_rows': 456,
                'double_spoke_omission_still_rejects': 18},
        '941': {'core_already_rejects_required_acceptance': 2703,
                'unary_cannot_block_two_root_colors': 2487,
                'same_binary_omission_rejects_two_rows': 744,
                'double_spoke_omission_still_rejects': 36}}
    dependencies = [Path(__file__).resolve(), ROOT / 'scripts/c5_941_three_spoke.py',
                    ROOT / 'scripts/c5_941_two_spoke.py',
                    ROOT / 'scripts/c5_independent_support_capacity.py', CORES, DOUBLE_SPOKE]
    return dict(schema=1,
        scope='conditional excess-two unique degree-six three-spoke source; spoke and original unary omitted to a rejected degree-four core with the original root on a triangle',
        source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in dependencies},
        inherited_source_sha256=source['source_sha256'],
        prior_double_spoke_source_sha256=prior['source_sha256'], pattern_order=ROWS,
        normalized_omitted_row=Q4, target_D5_orbits=target_orbits, bases=bases, marked_models=marked,
        kernel_semantics='four-port gluing operator; restrict endpoint to actual original V relation and glue a full original V coloring; no unary graph is substituted or enumerated',
        paper_dependencies=['unary endpoint slack', 'original triangle relation preserving tail transfer',
                            'connected all-degree-four T4 disk source rejects at most one singleton row',
                            'candidate unique degree-six double-spoke omission accepts all rows'],
        summary=dict(bases=len(bases), marked_roots=len(marked), spoke_restorations=len(additions),
            T4_accepting_intermediates=1114, core_ten_row_checks=10*len(marked),
            restored_ten_row_checks=10*len(additions), four_port_kernel_checks=10*len(additions),
            nonempty_unary_relation_checks=150*len(additions),
            binary_omission_kernel_checks=10*len(additions), double_spoke_omission_kernel_checks=30*len(additions),
            candidate_comparisons=10*len(additions), exclusion_counts=counts,
            residual_after_two_root_color_screen=1254, surviving_candidate_comparisons=0,
            arbitrary_size_coverage_is_paper=True, omitted_unary_graph_enumerated=False,
            full_source_disk_realizability_checked=False, covers_path_or_tail_roots=False,
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
