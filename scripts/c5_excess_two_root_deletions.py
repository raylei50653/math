#!/usr/bin/env python3
"""Same-source two-root deletions and an exact double-triangle exclusion.

The original degree-four six-point bases are inherited, not compressed anew.
Adding a named internal edge filters the complete ordered root-pair relation.
Paper coverage and the remaining epsilon-two branches are in the report.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

from c5_independent_support_capacity import B, FRAME, ROWS, T4, U, components
from c5_941_two_spoke import Q4, check_rotation, relabel_mask, search
from c5_excess_two_root_deletion_controls import build as deletion_controls

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_root_deletions/observations.json'
DOUBLE = ROOT / 'artifacts/c5_two_triangle_blocks/observations.json'


def encoded(data):
    return json.dumps(data, ensure_ascii=False, sort_keys=True, indent=1) + '\n'


def relation_controls():
    """All ordered four-colour binary relations, including the empty one."""
    universe = tuple((a, b) for a in range(4) for b in range(4))
    diagonal = sum(1 << (4*a+a) for a in range(4))
    digest = sha256()
    for mask in range(1 << 16):
        relation = {t for i, t in enumerate(universe) if mask >> i & 1}
        joined = {t for t in relation if t[0] != t[1]}
        independent = {(a, b) for a in range(4) for b in range(4)
                       if mask >> (4*a+b) & 1 and a != b}
        actual = sum(1 << (4*a+b) for a, b in joined)
        assert joined == independent and actual == mask & ~diagonal
        digest.update(f'{mask}:{actual}\n'.encode())
    same = {(0, 0), (1, 1)}
    different = {(0, 1), (1, 0)}
    marginals = lambda relation: [sorted({t[j] for t in relation}) for j in (0, 1)]
    assert marginals(same) == marginals(different)
    assert not {t for t in same if t[0] != t[1]}
    assert {t for t in different if t[0] != t[1]} == different
    return dict(ordered_binary_relations=65536, enumeration_sha256=digest.hexdigest(),
        marginal_collision=dict(scope='abstract relation algebra, no graph or disk realization claim',
            diagonal_relation=sorted(same), off_diagonal_relation=sorted(different),
            equal_marginals=marginals(same), edge_join_sizes=[0, 2]))


def exact_base(index, old):
    edges = set(map(tuple, old['edges']))
    n = 5 + len(old['neighborhoods'])
    interior = set(range(5, n))
    assert n == 11 and FRAME <= edges
    assert all(a < b for a, b in edges)
    neighbors = {v: {b if a == v else a for a, b in edges if v in (a, b)}
                 for v in range(n)}
    assert all(len(neighbors[v]) == 4 for v in interior)
    assert [sorted(neighbors[v] & B) for v in sorted(interior)] == [
        sorted(support) for support in old['neighborhoods']]
    h_edges = {e for e in edges if set(e) <= interior}
    triangles = [list(t) for t in combinations(sorted(interior), 3)
                 if all(e in h_edges for e in combinations(t, 2))]
    assert len(triangles) == 2 and not set(triangles[0]) & set(triangles[1])
    bridges = sorted(h_edges - {e for t in triangles for e in combinations(t, 2)})
    assert len(bridges) == 1 and len(components(interior, edges)) == 1
    faces = check_rotation(n, edges, old['apex_rotation'])
    rows = []
    for row in ROWS:
        choices = list(search(interior, edges, dict(enumerate(row))))
        tuples = sorted(tuple(f[v] for v in sorted(interior)) for f in choices)
        assert len(tuples) == len(set(tuples))
        rows.append(dict(row=row, complete_interior_colorings=tuples))
    mask = sum(1 << i for i, data in enumerate(rows) if data['complete_interior_colorings'])
    assert mask == old['sigma'] and mask & T4 == T4
    return dict(input_index=index, vertices=n, boundary=list(range(5)),
        interior_order=sorted(interior), edges=sorted(edges), triangles=triangles,
        original_bridge=bridges[0], boundary_attachments=[
            dict(vertex=v, neighbors=sorted(neighbors[v] & B)) for v in sorted(interior)],
        apex_rotation=old['apex_rotation'], apex_faces=faces, sigma=mask, rows=rows)


def restore_pairs(base):
    edges = set(map(tuple, base['edges']))
    interior = set(base['interior_order'])
    n = base['vertices']
    critical = []
    for edge in sorted(edges - FRAME):
        witness = next(search(interior, edges - {edge}, dict(enumerate(Q4))), None)
        assert witness is not None
        critical.append(dict(edge=edge, coloring=[witness[v] for v in range(n)]))
    base['q4_critical_witnesses'] = critical
    models = []
    for pair in combinations(sorted(interior), 2):
        if pair in edges:
            continue
        extended = edges | {pair}
        assert [sum(v in e for e in extended) for v in sorted(interior)] == [
            5 if v in pair else 4 for v in sorted(interior)]
        parts = components(interior - set(pair), extended)
        neighbors = {v: {b if a == v else a for a, b in extended if v in (a, b)}
                     for v in range(n)}
        original_components = [dict(vertices=part,
            root_contacts=[sorted(set(part) & neighbors[r]) for r in pair],
            boundary_attachments=[dict(vertex=v, neighbors=sorted(neighbors[v] & B))
                                  for v in part]) for part in parts]
        rows = []
        for row, saved in zip(ROWS, base['rows'], strict=True):
            full = [tuple(t) for t in saved['complete_interior_colorings']]
            slots = [base['interior_order'].index(v) for v in pair]
            witnesses = {}
            for i, colors in enumerate(full):
                witnesses.setdefault(tuple(colors[j] for j in slots), i)
            relation = sorted(witnesses)
            retained = [i for i, t in enumerate(relation) if t[0] != t[1]]
            direct = sorted(tuple(f[v] for v in base['interior_order'])
                            for f in search(interior, extended, dict(enumerate(row))))
            filtered = [colors for colors in full if colors[slots[0]] != colors[slots[1]]]
            assert direct == filtered
            assert {tuple(t[j] for j in slots) for t in direct} == {
                relation[i] for i in retained}
            assert bool(retained) == bool(full)
            rows.append(dict(ordered_root_pair_relation=relation,
                pair_witness_coloring_indices=[witnesses[t] for t in relation],
                retained_pair_tuple_indices=retained,
                extension_witness_coloring_index=(witnesses[relation[retained[0]]]
                                                 if retained else None)))
        sigma = sum(1 << i for i, data in enumerate(rows) if data['retained_pair_tuple_indices'])
        assert sigma == base['sigma'] == 1022
        models.append(dict(added_original_edge=pair, port_order=pair,
            original_components=original_components, sigma=sigma,
            strict_Sigma_minimality=False,
            augmented_disk_realizability_checked=False, rows=rows))
    assert len(models) == 8
    base['edge_restorations'] = models
    return base


def build():
    source = json.loads(DOUBLE.read_text())
    # Reconstruct all 128 actual saved disk cores; no acceptance flag is an oracle.
    reconstructed = [exact_base(i, old) for i, old in enumerate(source['disk_templates'])]
    assert len(reconstructed) == 128
    histogram = Counter(base['sigma'] for base in reconstructed)
    assert histogram == {1021: 32, 1022: 64, 959: 32}
    bases = [restore_pairs(base) for base in reconstructed if base['sigma'] == 1022]
    assert len(bases) == 64
    target_orbits = {str(mask): sorted({relabel_mask(mask, [(s*j+t) % 5 for j in range(5)])
                                      for s in (-1, 1) for t in range(5)})
                     for mask in (933, 941)}
    assert all(model['sigma'] not in orbit for base in bases
               for model in base['edge_restorations'] for orbit in target_orbits.values())
    controls = deletion_controls()
    dependencies = [Path(__file__).resolve(),
        ROOT / 'scripts/c5_excess_two_root_deletion_controls.py',
        ROOT / 'scripts/c5_independent_support_capacity.py',
        ROOT / 'scripts/c5_941_two_spoke.py', DOUBLE]
    return dict(schema=1,
        scope='same-source root-deletion controls and exact six-point double-triangle edge restoration; arbitrary-size root-deletion lemmas and coverage are paper arguments',
        source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                       for p in dependencies}, pattern_order=ROWS, normalized_omitted_row=Q4,
        target_D5_orbits=target_orbits,
        source_domain=dict(saved_disk_bases=len(reconstructed),
            reconstructed_Sigma_histogram=dict(sorted(histogram.items())),
            coverage='inherited exact whole-graph classification, no marked path/tail compression'),
        tuple_witness_semantics='indices refer to the complete coloring of this original base in the same row; prepend the row in boundary order 0..4',
        binary_relation_controls=relation_controls(), root_deletion_controls=controls,
        double_triangle_bases=bases,
        summary=dict(exact_q4_bases=len(bases), original_edge_restorations=8*len(bases),
            full_ten_row_edge_queries=80*len(bases), all_restored_Sigma=1022,
            reconstructed_source_row_queries=10*len(reconstructed),
            complete_binary_relations=65536,
            root_deletion_control_graphs=len(controls['named_source_controls']),
            root_deletion_side_equalities=controls['root_deletion_unary_side_equality_checks'],
            conditioned_component_relations=controls['conditioned_component_relation_checks']))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build()
    result = encoded(data)
    if args.check:
        assert OUT.read_text() == result, 'certificate differs; regenerate intentionally'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(result)
    print(json.dumps(dict(status='checked' if args.check else 'written', **data['summary']),
                     sort_keys=True))


if __name__ == '__main__':
    main()
