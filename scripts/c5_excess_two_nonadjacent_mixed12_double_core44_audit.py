#!/usr/bin/env python3
"""Independent full-graph replay of the U3 mixed12 double-triangle controls.

No producer modules are imported. Restricted-growth boundary words, target
orbits, graph inventories, whole colorings and all sixteen literal root fibres
are reconstructed here. The inherited classification remains a paper premise.
"""
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'artifacts/c5_two_triangle_blocks/observations.json'
PRIMARY = ROOT / 'artifacts/c5_excess_two_nonadjacent_mixed12_double_core44/observations.json'
OUT = PRIMARY.with_name('independent_audit.json')
PRIVATE = tuple(range(5, 11))
BOUNDARY = frozenset(range(5))
FRAME = frozenset(tuple(sorted((i, (i+1) % 5))) for i in range(5))
PINS = tuple(itertools.product(range(4), repeat=2))


def require(value, message):
    if not value:
        raise AssertionError(message)


def digest_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(word):
    seen = []
    result = []
    for color in word:
        if color not in seen:
            seen.append(color)
        result.append(seen.index(color))
    return tuple(result)


def boundary_words():
    answer = []
    def extend(word):
        if len(word) == 5:
            if word[-1] != word[0]:
                answer.append(tuple(word))
            return
        for color in range(min(3, max(word)+1)+1):
            if color != word[-1]:
                extend(word+[color])
    extend([0])
    return tuple(sorted(answer))


def targets_from_words(rows):
    index = {row: i for i, row in enumerate(rows)}
    orbits = {}
    for mask in (933, 941):
        masks = set()
        for offset in range(5):
            for direction in (1, -1):
                target = 0
                for i, row in enumerate(rows):
                    if mask & (1 << i):
                        moved = canonical(row[(offset+direction*j) % 5] for j in range(5))
                        target |= 1 << index[moved]
                masks.add(target)
        orbits[str(mask)] = sorted(masks)
    return orbits


def edges_from(entries):
    edges = frozenset(tuple(edge) for edge in entries)
    require(len(edges) == len(entries), 'edge inventory repeats an edge')
    require(all(0 <= a < b < 11 for a, b in edges), 'literal edge order/range')
    return edges


def neighbors(edges):
    result = {v: set() for v in range(11)}
    for a, b in edges:
        result[a].add(b)
        result[b].add(a)
    return result


def all_colorings(edges, row):
    """Static vertex order and boundary-derived domains, no producer filtering."""
    adjacent = neighbors(edges)
    domains = {v: tuple(c for c in range(4)
        if c not in {row[b] for b in adjacent[v] & BOUNDARY}) for v in PRIVATE}
    earlier = {v: tuple(u for u in adjacent[v] if 5 <= u < v) for v in PRIVATE}
    assigned = {}
    answer = []
    def visit(position):
        if position == len(PRIVATE):
            answer.append(tuple(assigned[v] for v in PRIVATE))
            return
        v = PRIVATE[position]
        for color in domains[v]:
            if any(assigned[u] == color for u in earlier[v]):
                continue
            assigned[v] = color
            visit(position+1)
        assigned.pop(v, None)
    visit(0)
    require(answer == sorted(set(answer)), 'complete coloring order')
    return answer


def whole_witness(values, edges, row, roots=(), pins=()):
    require(len(values) == 11 and tuple(values[:5]) == row, 'literal witness boundary/order')
    require(all(c in range(4) for c in values), 'witness color range')
    require(all(values[a] != values[b] for a, b in edges), 'witness violates actual edge')
    require(tuple(values[v] for v in roots) == tuple(pins), 'witness root pins')


def piece_inventory(edges, vertices, roots):
    adjacent = neighbors(edges)
    contacts = [sorted(adjacent[r] & set(vertices)) for r in roots]
    attachments = [dict(vertex=v, boundary_neighbors=sorted(adjacent[v] & BOUNDARY))
                   for v in vertices]
    return dict(vertices=vertices, ordered_root_contacts=contacts,
        owner_roots=[r for r, port in zip(roots, contacts) if port],
        contact_order=sorted(set().union(*map(set, contacts))),
        actual_boundary_attachments=attachments,
        actual_support=sorted(set().union(*(set(a['boundary_neighbors']) for a in attachments))),
        incident_original_edges=[list(e) for e in sorted(edges) if set(e) & set(vertices)])


def check_rotation(edges, rotation):
    require(len(rotation) == 12, 'exterior-apex rotation vertex count')
    augmented = set(edges) | {(b, 11) for b in BOUNDARY}
    for v, order in enumerate(rotation):
        actual = {b if a == v else a for a, b in augmented if v in (a, b)}
        require(len(order) == len(set(order)) and set(order) == actual, 'rotation actual darts')
    remaining = {(a, b) for a, b in augmented} | {(b, a) for a, b in augmented}
    faces = []
    while remaining:
        initial = min(remaining)
        a, b = initial
        face = []
        while True:
            require((a, b) in remaining, 'rotation repeats a dart')
            remaining.remove((a, b))
            face.append(a)
            around = rotation[b]
            a, b = b, around[(around.index(a)-1) % len(around)]
            if (a, b) == initial:
                break
        faces.append(face)
    require(12-len(augmented)+len(faces) == 2, 'rotation Euler sphere condition')
    require(all((b, (b+1) % 5) in augmented or ((b+1) % 5, b) in augmented
                for b in BOUNDARY), 'original outer cycle')
    return faces


def audit():
    primary = json.loads(PRIMARY.read_bytes())
    source = json.loads(SOURCE.read_bytes())
    rows = boundary_words()
    require(len(rows) == 10 and [list(r) for r in rows] == primary['pattern_order'], 'ten words')
    require(primary['ordered_root_pair_pin_order'] == [list(p) for p in PINS], 'all literal pins')
    q = (0, 1, 0, 1, 2)
    require(tuple(primary['omitted_q_row']) == q, 'inherited core refusal frame')
    orbits = targets_from_words(rows)
    require(orbits == primary['target_D5_orbits'], 'whole D5 target masks')
    targets = sorted(set().union(*map(set, orbits.values())))
    require(len(targets) == 10, 'ten target mask inventory')
    columns = ['retained_complete_core_coloring_indices', 'ordered_root_pair_relation',
               'root_fibres_by_pin_order', 'ordered_root_pair_witness_coloring_indices']
    require(primary['compact_kernel_row_columns'] == columns, 'compact literal fibre columns')
    require(primary['compact_unary_target_check_columns'] == ['target_mask', 'exclusion_code',
        'deciding_row_index', 'required_w_colors', 'two_distinct_w_color_root_pins',
        'kernel_witness_coloring_indices'], 'compact unary evidence columns')
    for path, expected in primary['source_sha256'].items():
        require(digest_file(ROOT/path) == expected, 'producer input hash '+path)

    counts = Counter()
    fibre_counts = Counter()
    fibre_stream = hashlib.sha256()
    sigma_histogram = Counter()
    all_inputs = []
    selected = []
    computed = {}
    require(len(source['disk_templates']) == 128, 'inherited template inventory')
    for input_index, old in enumerate(source['disk_templates']):
        edges = edges_from(old['edges'])
        require(FRAME <= edges, 'source includes literal boundary cycle')
        colorings = [all_colorings(edges, row) for row in rows]
        sigma = sum(1 << ri for ri, cs in enumerate(colorings) if cs)
        require(sigma == old['sigma'], 'independently reconstructed inherited Sigma')
        all_inputs.append(dict(source_input_index=input_index, independently_computed_sigma=sigma))
        computed[input_index] = (edges, colorings)
        if sigma == 1022:
            selected.append(input_index)
        counts['inherited_all_128_template_row_recomputations'] += 10
    require(len(selected) == 64, 'independent exact64 selection')
    require([c['source_input_index'] for c in primary['cores']] == selected, 'exact core input inventory')

    def fibres(base, direct, roots, row, edges, label, saved=None):
        index = {coloring: i for i, coloring in enumerate(base)}
        require(all(cs in index for cs in direct), 'restoration lost base identity')
        retained = [index[cs] for cs in direct]
        slots = tuple(v-5 for v in roots)
        bags = [[] for _ in PINS]
        for cs in direct:
            pin = tuple(cs[slot] for slot in slots)
            bags[PINS.index(pin)].append(index[cs])
        relation = [list(pin) for pin, bag in zip(PINS, bags) if bag]
        witness = [list(row+base[bag[0]]) for bag in bags if bag]
        witness_indices = [bag[0] for bag in bags if bag]
        if saved is not None:
            require(len(saved) == len(columns), 'complete compact row')
            saved = dict(zip(columns, saved))
            require(saved['retained_complete_core_coloring_indices'] == retained, 'complete retained indices')
            require(saved['root_fibres_by_pin_order'] == bags, 'all sixteen exact root fibres')
            require(saved['ordered_root_pair_relation'] == relation, 'whole root-pair relation')
            require(saved['ordered_root_pair_witness_coloring_indices'] == witness_indices, 'whole graph witness indices')
        for pin, bag in zip(PINS, bags):
            fibre_counts[label+'_all_literal_fibres'] += 1
            fibre_counts[label+('_nonempty_fibres' if bag else '_empty_fibres')] += 1
            for ci in bag:
                whole_witness(row+base[ci], edges, row, roots, pin)
                fibre_counts[label+'_whole_assignments'] += 1
        fibre_stream.update(json.dumps([label, roots, row, retained, bags, relation, witness],
            sort_keys=True, separators=(',', ':')).encode())
        return dict(indices=retained, relation=relation, witnesses=witness, witness_indices=witness_indices)

    for base in primary['cores']:
        input_index = base['source_input_index']
        old = source['disk_templates'][input_index]
        edges, colorings = computed[input_index]
        adjacent = neighbors(edges)
        require(edges_from(base['original_edges']) == edges, 'exact source edges retained')
        require(base['original_vertex_order'] == list(range(11)), 'core literal vertex order')
        require(base['complete_core_coloring_order'] == list(PRIVATE), 'core coloring order')
        require(all(len(adjacent[v]) == 4 for v in PRIVATE), 'core full degree four')
        attachments = [dict(vertex=v, neighbors=sorted(adjacent[v] & BOUNDARY)) for v in PRIVATE]
        require(base['boundary_attachments'] == attachments, 'all actual boundary attachments')
        require([a['neighbors'] for a in attachments] == [sorted(ns) for ns in old['neighborhoods']], 'inherited attachments')
        tri = [list(t) for t in itertools.combinations(PRIVATE, 3)
               if all(e in edges for e in itertools.combinations(t, 2))]
        h_edges = {e for e in edges if e[0] >= 5}
        tri_edges = set().union(*(set(itertools.combinations(t, 2)) for t in tri))
        bridge = sorted(h_edges-tri_edges)
        require(len(tri) == 2 and not set(tri[0]) & set(tri[1]), 'two disjoint actual triangles')
        require(len(bridge) == 1 and len(h_edges) == 7, 'one direct actual bridge; no tails')
        require(base['triangles'] == tri and base['direct_original_bridge'] == list(bridge[0]), 'saved blocks')
        require(base['inherited_apex_rotation'] == old['apex_rotation'], 'original rotation retained')
        require(check_rotation(edges, old['apex_rotation']) == base['verified_apex_faces'], 'actual disk faces')
        counts['verified_original_apex_rotations'] += 1
        require(base['sigma'] == 1022, 'core full Sigma')
        for row, direct, saved in zip(rows, colorings, base['rows']):
            require(tuple(saved['row']) == row and saved['complete_interior_colorings'] == [list(cs) for cs in direct],
                    'all inherited literal whole colorings')
            counts['complete_core_interior_colorings'] += len(direct)
        deletions = base['q_edge_critical_whole_graph_witnesses']
        require([d['deleted_original_edge'] for d in deletions] == [list(e) for e in sorted(edges-FRAME)],
                'every nonboundary q-critical edge')
        for deletion in deletions:
            smaller = edges-{tuple(deletion['deleted_original_edge'])}
            direct = all_colorings(smaller, q)
            require(direct and deletion['whole_graph_coloring'] == list(q+direct[0]), 'q-critical full recoloring')
            whole_witness(deletion['whole_graph_coloring'], smaller, q)
            counts['q_edge_critical_witnesses'] += 1
        marks = []
        for z, other in (bridge[0], bridge[0][::-1]):
            for w in sorted(adjacent[other] & set(PRIVATE)-set(bridge[0])):
                marks.append([z, w])
        require(len(marks) == 4 and [m['original_root_order'] for m in base['marked_cores']] == marks,
                'complete four ordered markings')
        for marked, roots in zip(base['marked_cores'], marks):
            z, w = roots
            require(w not in adjacent[z] and marked['roots_nonadjacent'], 'actual roots nonadjacent')
            uz = sorted(set(next(t for t in tri if z in t))-{z})
            c = sorted(set(next(t for t in tri if w in t))-{w})
            uz_inventory = piece_inventory(edges, uz, roots)
            c_inventory = piece_inventory(edges, c, roots)
            require(marked['literal_retained_original_Uz'] == uz_inventory, 'whole original Uz')
            require(marked['literal_original_sole_mixed_C'] == c_inventory, 'whole original C')
            require([len(cs) for cs in c_inventory['ordered_root_contacts']] == [1, 2], 'actual mixed12 contacts')
            require(marked['original_sole_mixed_incidence'] == [1, 2], 'mixed incidence label')
            require(marked['retained_core_root_degrees'] == [4, 4]
                and marked['retained_core_root_spoke_counts'] == [1, 2], 'core root degrees/spokes')
            for row, direct, saved in zip(rows, colorings, marked['retained_core_rows']):
                fibres(direct, direct, roots, row, edges, 'core', saved)
            require([k['restored_original_z_spoke'] for k in marked['z_spoke_restorations']]
                == [[b, z] for b in sorted(BOUNDARY-adjacent[z])], 'all four original z-spoke choices')
            for kernel in marked['z_spoke_restorations']:
                ze = edges | {tuple(kernel['restored_original_z_spoke'])}
                kernel_adjacent = neighbors(ze)
                require([len(kernel_adjacent[v]) for v in roots] == [5, 4], 'kernel root degrees')
                require([len(kernel_adjacent[v] & BOUNDARY) for v in roots] == [2, 2], 'kernel root spokes')
                require(piece_inventory(ze, uz, roots) == uz_inventory
                    and piece_inventory(ze, c, roots) == c_inventory, 'same whole original components in kernel')
                kernel_rows = []
                for row, full, saved in zip(rows, colorings, kernel['whole_kernel_rows']):
                    direct = all_colorings(ze, row)
                    kernel_rows.append(fibres(full, direct, roots, row, ze, 'kernel', saved))
                    counts['z_spoke_full_graph_row_recomputations'] += 1
                checks = kernel['omitted_unary_target_checks']
                require([test[0] for test in checks] == targets, 'all unary target checks')
                for target, test in zip(targets, checks):
                    empty = [i for i, r in enumerate(kernel_rows) if target & (1 << i) and not r['relation']]
                    if empty:
                        i = empty[0]
                        require(test == [target, 0, i, [], [], []], 'target acceptance requires nonempty kernel')
                        counts['unary_target_accepts_empty_kernel'] += 1
                    else:
                        impossible = [i for i, r in enumerate(kernel_rows) if not (target & (1 << i))
                            and len({p[1] for p in r['relation']}) > 1]
                        require(impossible, 'unresolved unary target: cannot claim exclusion')
                        i = impossible[0]
                        r = kernel_rows[i]
                        colors = sorted({p[1] for p in r['relation']})
                        two_pins = [next(p for p in r['relation'] if p[1] == color) for color in colors[:2]]
                        witnesses = [r['witnesses'][r['relation'].index(p)] for p in two_pins]
                        witness_indices = [r['witness_indices'][r['relation'].index(p)] for p in two_pins]
                        expected = [target, 1, i, colors, two_pins, witness_indices]
                        require(test == expected, 'literal two-w-color singleton-capacity evidence')
                        for pin, witness in zip(two_pins, witnesses):
                            whole_witness(witness, ze, rows[i], roots, pin)
                        counts['unary_singleton_capacity_exclusions'] += 1
                    counts['omitted_unary_full_target_comparisons'] += 1
                restorations = kernel['double_spoke_restorations']
                require([r['restored_original_w_spoke'] for r in restorations]
                    == [[b, w] for b in sorted(BOUNDARY-adjacent[w])], 'all three original w-spoke choices')
                for original in restorations:
                    restored = ze | {tuple(original['restored_original_w_spoke'])}
                    degrees = neighbors(restored)
                    require(all(len(degrees[v]) == (5 if v in roots else 4) for v in PRIVATE), 'full source degree identities')
                    require([len(degrees[v] & BOUNDARY) for v in roots] == [2, 3], 'restored roots/spokes')
                    relations = []
                    for ri, (row, full) in enumerate(zip(rows, colorings)):
                        direct = all_colorings(restored, row)
                        result = fibres(full, direct, roots, row, restored, 'restored')
                        require(result['indices'] == original['full_original_graph_coloring_indices_by_row'][ri],
                                'all complete restored coloring indices')
                        relations.append((direct, result))
                        counts['double_spoke_full_graph_row_recomputations'] += 1
                    sigma = sum(1 << i for i, (cs, _) in enumerate(relations) if cs)
                    require(sigma == original['full_sigma'] and sigma not in targets, 'independent restored complete Sigma')
                    sigma_histogram[sigma] += 1
                    tests = primary['double_spoke_mask_target_comparisons'][str(sigma)]
                    require([t['target_mask'] for t in tests] == targets, 'all restored target comparisons')
                    for target, test in zip(targets, tests):
                        i = next(i for i in range(10) if bool(sigma & (1 << i)) != bool(target & (1 << i)))
                        direct, result = relations[i]
                        expected = dict(target_mask=target, deciding_row_index=i,
                            original_graph_accepts=bool(direct), target_accepts=bool(target & (1 << i)))
                        require(test == expected, 'exact full Sigma mismatch evidence')
                        if direct:
                            first_index = original['full_original_graph_coloring_indices_by_row'][i][0]
                            require(colorings[i][first_index] == direct[0], 'same-row whole deciding witness index')
                            whole_witness(rows[i]+colorings[i][first_index], restored, rows[i])
                        counts['double_spoke_full_target_comparisons'] += 1
                    counts['double_spoke_restorations'] += 1
                counts['z_spoke_kernels'] += 1
            counts['ordered_mixed12_markings'] += 1
    counts['exact_six_vertex_q_disk_cores'] = len(selected)
    counts['inherited_core_full_graph_row_recomputations'] = len(selected)*10
    for key in ('double_spoke_residuals', 'omitted_capacity_one_unary_residuals',
                'unary_fixed_actual_support_stage_triggered', 'topology_stage_triggered'):
        counts[key] = 0
    for key, expected in primary['summary'].items():
        require(counts[key] == expected, 'producer summary '+key)
    require({str(k): v for k, v in sorted(sigma_histogram.items())}
        == primary['double_spoke_Sigma_histogram'], 'restored full Sigma histogram')
    require(fibre_counts['core_all_literal_fibres'] == 40960
        and fibre_counts['kernel_all_literal_fibres'] == 163840
        and fibre_counts['restored_all_literal_fibres'] == 491520, 'complete fibre inventories')
    hashes = {str(path.relative_to(ROOT)): digest_file(path)
              for path in (SOURCE, PRIMARY, Path(__file__).resolve(), ROOT/'scripts/c5_excess_two_nonadjacent_mixed12_double_core44.py')}
    return dict(schema=1, status='triggered_and_holds', source_sha256=hashes,
        independent_method='No producer imports; restricted-growth words, all128 source Sigma selection, fixed-order full-graph backtracking, all16 literal root fibres including empty, actual edge witnesses and sphere rotations.',
        pattern_order=rows, target_D5_orbits=orbits,
        inherited_source_inventory=all_inputs, selected_source_input_indices=selected,
        counts=dict(sorted(counts.items())), literal_root_fibre_counts=dict(sorted(fibre_counts.items())),
        complete_literal_root_fibre_stream_sha256=fibre_stream.hexdigest(),
        restored_complete_Sigma_histogram=dict(sorted(sigma_histogram.items())),
        not_triggered=['one fixed actual omitted-unary support across rows', 'restored source disk realization'],
        trust_boundary='Finite literal double-triangle controls only. All-degree-four arbitrary-size classification, source saturation and the arbitrary omitted-unary singleton-capacity lemma remain paper premises. No broad search, general epsilon theorem or new Lean proof.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = audit()
    encoded = json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(',', ':'))+'\n'
    if args.check:
        require(OUT.read_text() == encoded, 'independent certificate byte/hash drift; preserve historical output')
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(encoded)
    print(json.dumps(dict(status='checked' if args.check else 'written',
        **result['counts'], **result['literal_root_fibre_counts']), sort_keys=True))


if __name__ == '__main__':
    main()
