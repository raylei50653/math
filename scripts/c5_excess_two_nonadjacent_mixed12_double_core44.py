#!/usr/bin/env python3
"""U3 mixed12: exact six-vertex double-triangle core restoration controls.

Use inherited actual disk cores without path compression. Every restored-spoke
relation is recomputed by full graph coloring. A capacity-one omitted unary
can forbid at most one w color per row, which already excludes every full
Sigma933/941 D5 image here; fixed-support and topology stages are not triggered.
Deterministic certificate generation and replay use only the standard library.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'artifacts/c5_two_triangle_blocks/observations.json'
OUT = ROOT / 'artifacts/c5_excess_two_nonadjacent_mixed12_double_core44/observations.json'
B = set(range(5))
INTERIOR = tuple(range(5, 11))
FRAME = {tuple(sorted((b, (b+1) % 5))) for b in B}
COLORS = set(range(4))
PAIRS = tuple(product(range(4), repeat=2))


def normalize(values):
    labels = {}
    return tuple(labels.setdefault(c, len(labels)) for c in values)


ROWS = tuple(sorted({normalize(r) for r in product(range(4), repeat=5)
                     if all(r[a] != r[b] for a, b in FRAME)}))
Q = (0, 1, 0, 1, 2)


def adjacency(edges):
    result = {v: set() for v in range(11)}
    for a, b in edges:
        assert 0 <= a < b < 11
        result[a].add(b)
        result[b].add(a)
    return result


def complete_colorings(edges, row):
    """Enumerate all six interior colors by a fixed vertex-order search."""
    adjacent = adjacency(edges)
    fixed = dict(enumerate(row))
    answer = []

    def visit(index):
        if index == len(INTERIOR):
            answer.append(tuple(fixed[v] for v in INTERIOR))
            return
        v = INTERIOR[index]
        for color in range(4):
            if any(fixed.get(u) == color for u in adjacent[v]):
                continue
            fixed[v] = color
            visit(index+1)
        fixed.pop(v, None)

    visit(0)
    assert answer == sorted(set(answer))
    return answer


def valid_witness(edges, row, witness):
    assert len(witness) == 11 and tuple(witness[:5]) == row
    assert all(c in COLORS for c in witness)
    assert all(witness[a] != witness[b] for a, b in edges)


def rotation_faces(edges, rotation):
    """Verify the actual saved exterior-apex sphere embedding."""
    assert len(rotation) == 12
    augmented = edges | {(b, 11) for b in B}
    for v, ns in enumerate(rotation):
        assert len(ns) == len(set(ns))
        assert set(ns) == {b if a == v else a for a, b in augmented if v in (a, b)}
    todo = {(a, b) for a, b in augmented} | {(b, a) for a, b in augmented}
    faces = []
    while todo:
        start = min(todo)
        dart, face = start, []
        while True:
            assert dart in todo
            todo.remove(dart)
            a, b = dart
            face.append(a)
            ns = rotation[b]
            dart = (b, ns[(ns.index(a)-1) % len(ns)])
            if dart == start:
                break
        faces.append(face)
    assert len(rotation)-len(augmented)+len(faces) == 2
    return faces


def target_orbits():
    index = {row: i for i, row in enumerate(ROWS)}
    return {str(mask): sorted({sum(1 << index[normalize(
        [row[(s*j+t) % 5] for j in range(5)])]
        for ri, row in enumerate(ROWS) if mask >> ri & 1)
        for s in (-1, 1) for t in range(5)}) for mask in (933, 941)}


def row_fibres(base_colors, retained, roots, row, edges):
    """Literal sixteen root fibres, all complete tuples, and whole witnesses."""
    slots = [INTERIOR.index(v) for v in roots]
    fibres = [[] for _ in PAIRS]
    for ci in retained:
        pair = tuple(base_colors[ci][slot] for slot in slots)
        fibres[PAIRS.index(pair)].append(ci)
        valid_witness(edges, row, row + base_colors[ci])
    relation = [pair for pair, fibre in zip(PAIRS, fibres, strict=True) if fibre]
    witnesses = [fibres[PAIRS.index(pair)][0] for pair in relation]
    return dict(ordered_root_pair_relation=relation,
        root_fibres_by_pin_order=fibres,
        retained_complete_core_coloring_indices=retained,
        ordered_root_pair_witness_coloring_indices=witnesses)


def piece(edges, vertices, roots):
    adjacent = adjacency(edges)
    contacts = [sorted(adjacent[r] & set(vertices)) for r in roots]
    attachments = [dict(vertex=v, boundary_neighbors=sorted(adjacent[v] & B))
                   for v in vertices]
    return dict(vertices=vertices, ordered_root_contacts=contacts,
        owner_roots=[r for r, cs in zip(roots, contacts, strict=True) if cs],
        contact_order=sorted(set().union(*map(set, contacts))),
        actual_boundary_attachments=attachments,
        actual_support=sorted(set().union(*(set(a['boundary_neighbors']) for a in attachments))),
        incident_original_edges=sorted(e for e in edges if set(e) & set(vertices)))


def exact_base(input_index, old):
    edges = set(map(tuple, old['edges']))
    adjacent = adjacency(edges)
    assert FRAME <= edges and all(len(adjacent[v]) == 4 for v in INTERIOR)
    assert [sorted(adjacent[v] & B) for v in INTERIOR] == [
        sorted(s) for s in old['neighborhoods']]
    h_edges = {e for e in edges if set(e) <= set(INTERIOR)}
    triangles = [tuple(t) for t in combinations(INTERIOR, 3)
                 if all(e in h_edges for e in combinations(t, 2))]
    assert len(triangles) == 2 and not set(triangles[0]) & set(triangles[1])
    bridges = sorted(h_edges - {e for t in triangles for e in combinations(t, 2)})
    assert len(bridges) == 1 and len(h_edges) == 7
    colors = [complete_colorings(edges, row) for row in ROWS]
    sigma = sum(1 << ri for ri, cs in enumerate(colors) if cs)
    assert sigma == old['sigma'] == 1022 and not colors[ROWS.index(Q)]
    q_witnesses = []
    for edge in sorted(edges-FRAME):
        cs = complete_colorings(edges-{edge}, Q)
        assert cs, 'inherited q core is not edge critical'
        witness = Q+cs[0]
        valid_witness(edges-{edge}, Q, witness)
        q_witnesses.append(dict(deleted_original_edge=edge, whole_graph_coloring=witness))
    return dict(source_input_index=input_index, original_edges=sorted(edges),
        original_vertex_order=list(range(11)), complete_core_coloring_order=INTERIOR,
        boundary_attachments=[dict(vertex=v, neighbors=sorted(adjacent[v] & B))
                              for v in INTERIOR],
        triangles=triangles, direct_original_bridge=bridges[0],
        inherited_apex_rotation=old['apex_rotation'],
        verified_apex_faces=rotation_faces(edges, old['apex_rotation']),
        sigma=sigma, rows=[dict(row=row, complete_interior_colorings=cs)
                          for row, cs in zip(ROWS, colors, strict=True)],
        q_edge_critical_whole_graph_witnesses=q_witnesses)


def unary_target_check(rows, target, counts):
    """Necessary K minus at most one forbidden w color; retain both pins."""
    accepted_empty = [ri for ri, r in enumerate(rows)
                      if target >> ri & 1 and not r['ordered_root_pair_relation']]
    if accepted_empty:
        ri = accepted_empty[0]
        counts['unary_target_accepts_empty_kernel'] += 1
        return dict(target_mask=target, exclusion='target_accepts_empty_whole_kernel',
                    deciding_row_index=ri, literal_kernel_relation=[])
    for ri, row in enumerate(rows):
        relation = row['ordered_root_pair_relation']
        w_colors = sorted({p[1] for p in relation})
        if not (target >> ri & 1) and len(w_colors) > 1:
            pins = [next(p for p in relation if p[1] == c) for c in w_colors[:2]]
            witnesses = [row['ordered_root_pair_witness_coloring_indices'][relation.index(p)]
                         for p in pins]
            counts['unary_singleton_capacity_exclusions'] += 1
            return dict(target_mask=target, exclusion='rejected_row_requires_two_forbidden_w_colors',
                deciding_row_index=ri, required_w_colors=w_colors,
                two_distinct_w_color_root_pins=pins, kernel_witness_coloring_indices=witnesses,
                omitted_original_unary_forbidden_w_color_capacity=1)
    raise AssertionError('unresolved target must retain one fixed actual unary support before further work')


def double_spoke_mask_check(sigma, target):
    assert sigma != target
    ri = next(i for i in range(len(ROWS)) if (sigma >> i & 1) != (target >> i & 1))
    accepts = bool(sigma >> ri & 1)
    return dict(target_mask=target, deciding_row_index=ri,
        original_graph_accepts=accepts, target_accepts=bool(target >> ri & 1))


KERNEL_ROW_COLUMNS = ['retained_complete_core_coloring_indices',
    'ordered_root_pair_relation', 'root_fibres_by_pin_order',
    'ordered_root_pair_witness_coloring_indices']
UNARY_CHECK_COLUMNS = ['target_mask', 'exclusion_code', 'deciding_row_index',
    'required_w_colors', 'two_distinct_w_color_root_pins',
    'kernel_witness_coloring_indices']


def compact_kernel_row(row):
    return [row[name] for name in KERNEL_ROW_COLUMNS]


def compact_unary_check(check):
    empty = check['exclusion'] == 'target_accepts_empty_whole_kernel'
    return [check['target_mask'], 0 if empty else 1, check['deciding_row_index'],
        check.get('required_w_colors', []),
        check.get('two_distinct_w_color_root_pins', []),
        check.get('kernel_witness_coloring_indices', [])]


def mark_and_restore(base, roots, targets, counts, sigma_histogram):
    edges = set(map(tuple, base['original_edges']))
    adjacent = adjacency(edges)
    z, w = roots
    assert w not in adjacent[z]
    uz = sorted(adjacent[z] & set(INTERIOR)-set(roots)-set(adjacent[w]))
    c = sorted(set(INTERIOR)-set(roots)-set(uz))
    assert len(uz) == len(c) == 2
    uz_piece, c_piece = piece(edges, uz, roots), piece(edges, c, roots)
    assert list(map(len, uz_piece['ordered_root_contacts'])) == [2, 0]
    assert list(map(len, c_piece['ordered_root_contacts'])) == [1, 2]
    assert tuple(uz) in edges and tuple(c) in edges
    core_rows = [row_fibres(r['complete_interior_colorings'],
        list(range(len(r['complete_interior_colorings']))), roots, row, edges)
        for row, r in zip(ROWS, base['rows'], strict=True)]
    z_restorations = []
    for b_z in sorted(B-adjacent[z]):
        z_spoke = (b_z, z)
        ze = edges | {z_spoke}
        assert [len(adjacency(ze)[v]) for v in roots] == [5, 4]
        k_rows, k_colors = [], []
        for row, saved in zip(ROWS, base['rows'], strict=True):
            full = saved['complete_interior_colorings']
            retained = [ci for ci, cs in enumerate(full) if cs[z-5] != row[b_z]]
            direct = complete_colorings(ze, row)
            assert direct == [full[ci] for ci in retained]
            k_colors.append(direct)
            k_rows.append(row_fibres(full, retained, roots, row, ze))
            counts['z_spoke_full_graph_row_recomputations'] += 1
        tests = [unary_target_check(k_rows, target, counts) for target in targets]
        restorations = []
        for b_w in sorted(B-adjacent[w]):
            w_spoke = (b_w, w)
            original = ze | {w_spoke}
            assert [len(adjacency(original)[v]) for v in INTERIOR] == [
                5 if v in roots else 4 for v in INTERIOR]
            original_colors, complete_indices = [], []
            for ri, (row, saved) in enumerate(zip(ROWS, base['rows'], strict=True)):
                full = saved['complete_interior_colorings']
                retained = [ci for ci in k_rows[ri]['retained_complete_core_coloring_indices']
                            if full[ci][w-5] != row[b_w]]
                direct = complete_colorings(original, row)
                assert direct == [full[ci] for ci in retained]
                original_colors.append(direct)
                complete_indices.append(retained)
                counts['double_spoke_full_graph_row_recomputations'] += 1
            sigma = sum(1 << ri for ri, cs in enumerate(original_colors) if cs)
            assert sigma not in targets
            sigma_histogram[sigma] += 1
            restorations.append(dict(restored_original_w_spoke=w_spoke,
                full_sigma=sigma, full_original_graph_coloring_indices_by_row=complete_indices))
            counts['double_spoke_restorations'] += 1
        z_restorations.append(dict(restored_original_z_spoke=z_spoke,
            whole_kernel_rows=[compact_kernel_row(r) for r in k_rows],
            omitted_unary_target_checks=[compact_unary_check(t) for t in tests],
            double_spoke_restorations=restorations))
        counts['z_spoke_kernels'] += 1
    counts['ordered_mixed12_markings'] += 1
    return dict(original_root_order=roots, roots_nonadjacent=True,
        original_sole_mixed_incidence=[1, 2],
        literal_retained_original_Uz=uz_piece, literal_original_sole_mixed_C=c_piece,
        retained_core_root_degrees=[4, 4], retained_core_root_spoke_counts=[1, 2],
        retained_core_rows=[compact_kernel_row(r) for r in core_rows],
        z_spoke_restorations=z_restorations)


def build():
    source = json.loads(SOURCE.read_text())
    assert len(source['disk_templates']) == 128
    selected = [(i, old) for i, old in enumerate(source['disk_templates']) if old['sigma'] == 1022]
    assert len(selected) == 64
    orbits = target_orbits()
    targets = sorted(set().union(*map(set, orbits.values())))
    assert len(targets) == 10
    counts, sigma_histogram, cores = Counter(), Counter(), []
    for input_index, old in selected:
        base = exact_base(input_index, old)
        bridge = base['direct_original_bridge']
        adjacent = adjacency(set(map(tuple, base['original_edges'])))
        marks = []
        for z, opposite_bridge_endpoint in (bridge, bridge[::-1]):
            for w in sorted(adjacent[opposite_bridge_endpoint] & set(INTERIOR)-set(bridge)):
                marks.append(mark_and_restore(base, [z, w], targets, counts, sigma_histogram))
        assert len(marks) == 4
        base['marked_cores'] = marks
        cores.append(base)
    counts.update(exact_six_vertex_q_disk_cores=len(cores),
        inherited_core_full_graph_row_recomputations=10*len(cores),
        complete_core_interior_colorings=sum(len(r['complete_interior_colorings'])
            for c in cores for r in c['rows']),
        double_spoke_full_target_comparisons=counts['double_spoke_restorations']*len(targets),
        omitted_unary_full_target_comparisons=counts['z_spoke_kernels']*len(targets),
        unary_fixed_actual_support_stage_triggered=0, topology_stage_triggered=0,
        double_spoke_residuals=0, omitted_capacity_one_unary_residuals=0)
    assert dict(counts) == dict(exact_six_vertex_q_disk_cores=64,
        inherited_core_full_graph_row_recomputations=640,
        complete_core_interior_colorings=8480, ordered_mixed12_markings=256,
        z_spoke_kernels=1024, z_spoke_full_graph_row_recomputations=10240,
        double_spoke_restorations=3072, double_spoke_full_graph_row_recomputations=30720,
        double_spoke_full_target_comparisons=30720,
        omitted_unary_full_target_comparisons=10240,
        unary_target_accepts_empty_kernel=5248, unary_singleton_capacity_exclusions=4992,
        unary_fixed_actual_support_stage_triggered=0, topology_stage_triggered=0,
        double_spoke_residuals=0, omitted_capacity_one_unary_residuals=0), dict(counts)
    assert sigma_histogram == {1022: 1920, 830: 384, 1016: 384, 958: 192, 1020: 192}
    return dict(schema=1,
        scope='U3 mixed12 exact six-interior-vertex directly bridged double-triangle core44 only; full Sigma933/941 D5 images; no source realizability or general epsilon theorem',
        source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                       for p in (SOURCE, Path(__file__).resolve())},
        pattern_order=ROWS, omitted_q_row=Q, ordered_root_pair_pin_order=PAIRS,
        target_D5_orbits=orbits,
        compact_kernel_row_columns=KERNEL_ROW_COLUMNS,
        compact_unary_target_check_columns=UNARY_CHECK_COLUMNS,
        unary_exclusion_codes={'0': 'target_accepts_empty_whole_kernel',
            '1': 'rejected_row_requires_two_forbidden_w_colors'},
        witness_semantics='Every core row lists all complete interior colorings in literal vertex order 5..10. Every index, including relation witnesses, refers to that same core and same row; prepend the actual row 0..4. All sixteen fibres are literal arrays in ordered_root_pair_pin_order, including []. The kernel row column schema makes every relation and whole witness explicit without repeating colorings.',
        restoration_edge_semantics='Every kernel graph is precisely the same core original_edges plus its restored_original_z_spoke. Every double-spoke original graph adds that same z spoke and its restored_original_w_spoke. All full coloring sets are independently recomputed and checked against the saved same-core indices. The target deciding-row table is shared by full_sigma; an accepting-row whole witness is the first coloring index saved for that same original graph and deciding row, while a rejecting-row full index list is literally [].',
        double_spoke_mask_target_comparisons={str(mask): [double_spoke_mask_check(mask, target)
            for target in targets] for mask in sorted(sigma_histogram)},
        omission_scope=dict(z='one original spoke restores bridge endpoint z from degree4 to degree5',
            w_spoke='one original spoke restores opposite nonbridge w from degree4 to degree5',
            w_unary='one omitted original capacity-one unary Uw restores w from degree4 to degree5; no independently chosen row schedule or realization is asserted'),
        degree_and_spoke_semantics=dict(retained_core_root_degrees=[4, 4],
            retained_core_root_spoke_counts=[1, 2], G_minus_Uw_root_degrees=[5, 4],
            original_root_degrees=[5, 5], double_spoke_original_spoke_counts=[2, 3],
            omitted_Uw_original_spoke_counts=[2, 2], omitted_original_Uw_incidence=1),
        omitted_unary_necessary_operator=dict(original_fixed_actual_support_required=True,
            root_pin='w, second coordinate of the ordered whole kernel K_beta',
            forbidden_root_color_set_cardinality_at_most=1,
            acceptance='there exists (a,b) in the complete whole graph kernel K_beta with b outside F_U(beta)',
            fixed_support_and_S4_transport='If the rowwise necessity survived, one actual S would be fixed for all ten rows; equal boundary restrictions on S must transport F_U by the same color permutation, including every stabilizer.',
            support_scope='Under the source shield theorem, actual S is a continuous boundary arc with at least three vertices.',
            fixed_support_stage='not triggered: every target already violates empty-kernel or singleton-capacity necessity',
            topology_stage='not triggered'),
        cores=cores, double_spoke_Sigma_histogram=dict(sorted(sigma_histogram.items())),
        summary=dict(sorted(counts.items())),
        trust_boundary='The inherited all-degree-four q-core classification supplies exact six-vertex double-triangle coverage. This script verifies only those literal saved cores, root markings and restorations; arbitrary-size classification, minimal-source premises and unary capacity bounds are paper dependencies. No graph compression, Lean theorem, or source realization is certified.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build()
    encoded = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(',', ':'))+'\n'
    if args.check:
        assert OUT.read_text() == encoded, 'certificate differs; preserve historical inputs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(encoded)
    print(json.dumps(dict(status='checked' if args.check else 'written', **data['summary']), sort_keys=True))


if __name__ == '__main__':
    main()
