#!/usr/bin/env python3
"""U4: restore an original mixed11 at nonadjacent roots.

Reconstruct the marked single-/double-triangle necessary domain from three
small immutable inputs. Keep the marked roots and the complete contact joint.
The paper supplies unbounded coverage; this checker uses no planarity oracle,
historical producer imports, or independent component color normalization.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_nonadjacent_two_mixed_core44/observations.json'
INPUTS = [ROOT / 'artifacts/c5_triangle_branches/observations.json',
          ROOT / 'artifacts/c5_triangle_path_reduction/observations.json',
          ROOT / 'artifacts/c5_two_triangle_blocks/observations.json',
          ROOT / 'artifacts/c5_excess_two_nonadjacent_two_mixed_core44/control_input.json']
B = set(range(5))
FRAME = {tuple(sorted((i, (i + 1) % 5))) for i in range(5)}
PINS = tuple(product(range(4), repeat=2))


def normalize(values):
    labels = {}
    return tuple(labels.setdefault(c, len(labels)) for c in values)


ROWS = tuple(sorted({normalize(r) for r in product(range(4), repeat=5)
                     if all(r[a] != r[b] for a, b in FRAME)}))
Q = (0, 1, 0, 1, 2)


def colorings(edges, row, ports, first_only=False):
    vertices = B | set().union(*map(set, edges))
    adjacent = {v: set() for v in vertices}
    for a, b in edges:
        adjacent[a].add(b)
        adjacent[b].add(a)
    fixed, found = dict(enumerate(row)), {}

    def visit():
        remaining = vertices - fixed.keys()
        if not remaining:
            found.setdefault(tuple(fixed[v] for v in ports),
                             tuple(fixed[v] for v in sorted(vertices)))
            return
        choices = {v: set(range(4)) - {fixed[u] for u in adjacent[v] if u in fixed}
                   for v in remaining}
        v = min(remaining, key=lambda u: (len(choices[u]), -len(adjacent[u]), u))
        for c in sorted(choices[v]):
            fixed[v] = c
            visit()
            if first_only and found:
                break
        fixed.pop(v, None)

    visit()
    return found


def components(vertices, edges):
    todo, result = set(vertices), []
    while todo:
        reached, pending = set(), [min(todo)]
        while pending:
            v = pending.pop()
            if v in reached:
                continue
            reached.add(v)
            pending.extend(b if a == v else a for a, b in edges
                           if v in (a, b) and {a, b} <= todo)
        todo -= reached
        result.append(sorted(reached))
    return result


def rotation_check(edges, rotation):
    apex = len(rotation) - 1
    augmented = edges | {(b, apex) for b in B}
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
            dart = (b, ns[(ns.index(a) - 1) % len(ns)])
            if dart == start:
                break
        faces.append(face)
    assert len(rotation) - len(augmented) + len(faces) == 2
    return faces


def pieces(edges, roots):
    interior = set().union(*map(set, edges)) - B
    result = []
    for group in components(interior - set(roots), edges):
        contacts = [[v for v in group if tuple(sorted((r, v))) in edges] for r in roots]
        attachments = [[b for b in sorted(B) if (b, v) in edges] for v in group]
        result.append(dict(vertices=group, root_contacts=contacts,
            owners=[r for r, cs in zip(roots, contacts, strict=True) if cs],
            contact_order=sorted(set().union(*map(set, contacts))),
            boundary_attachments=attachments,
            actual_support=sorted(set().union(*map(set, attachments))),
            incident_edges=sorted(e for e in edges if set(e).intersection(group))))
    return result


def single_forms():
    branches, switches = [json.loads(p.read_text()) for p in INPUTS[:2]]
    contexts = [(0, i, f) for i, f in enumerate(branches['disk_templates'])]
    contexts += [(1, i, f) for i, f in enumerate(switches['normal_forms'])]
    forms = []
    for family, input_id, base in contexts:
        edges = set(map(tuple, base['edges']))
        triangle = {5, 6, 7}
        rotation = base['apex_rotation'] if family == 0 else base['topology']['apex_rotation']
        rotation_check(edges, rotation)
        tails = []
        for group in components(set().union(*map(set, edges)) - B - triangle, edges):
            start, = [v for v in group if any(tuple(sorted((v, t))) in edges for t in triangle)]
            parent, = [t for t in triangle if tuple(sorted((t, start))) in edges]
            path, prior, current = [], None, start
            while True:
                path.append(current)
                nxt = [v for v in group if v != prior and tuple(sorted((v, current))) in edges]
                if not nxt:
                    break
                assert len(nxt) == 1
                prior, current = current, nxt[0]
            assert set(path) == set(group)
            tails.append((parent, path))
        for tail_id, (parent, path) in enumerate(tails):
            X = sorted(b for b in B if (b, path[0]) in edges)
            leaf = sorted(b for b in B if (b, path[-1]) in edges)
            specs = []
            if family == 0:
                for p, s in ((0, 0), (0, 2), (2, 0), (2, 2), (1, 1)):
                    specs.append(('uniform_nonleaf', p, s, [X] * (p + 1 + s) + [leaf], p))
                specs.append(('uniform_leaf', 0, 0, [X, leaf], 1))
            else:
                Y = sorted(b for b in B if (b, path[1]) in edges)
                specs.append(('two_run_X', 0, 2, [X, Y, Y, leaf], 0))
                for p, s in ((0, 1), (1, 0), (1, 2), (2, 1)):
                    specs.append(('two_run_Y', p, s, [X] + [Y] * (p + 1 + s) + [leaf], 1 + p))
                specs.append(('two_run_leaf', 0, 2, [X, Y, Y, leaf], 3))
            for w in sorted(triangle - {parent}):
                for kind, p, s, supports, marker in specs:
                    other = sorted(set().union(*map(set, edges)) - B - set(path))
                    remap = {v: v for v in B}
                    remap.update({v: 5 + j for j, v in enumerate(other)})
                    newpath = list(range(5 + len(other), 5 + len(other) + len(supports)))
                    marked = {tuple(sorted((remap[a], remap[b]))) for a, b in edges
                              if a not in path and b not in path}
                    marked |= {(b, v) for v, ns in zip(newpath, supports, strict=True) for b in ns}
                    marked |= set(zip(newpath, newpath[1:]))
                    marked.add(tuple(sorted((remap[parent], newpath[0]))))
                    roots = [newpath[marker], remap[w]]
                    regions = pieces(marked, roots)
                    mixed, = [r for r in regions if len(r['owners']) == 2]
                    assert list(map(len, mixed['root_contacts'])) == [1, 2]
                    if len(regions) > 2:
                        continue
                    forms.append(dict(family='single_triangle_uniform' if family == 0 else 'single_triangle_two_run',
                        input_origin=[family, input_id], marker=dict(tail=tail_id, kind=kind,
                            prefix=p, suffix=s, path=newpath, marker_offset=marker,
                            triangle_parent=remap[parent]),
                        original_edges=sorted(marked), original_root_order=roots))
    assert len(forms) == 316
    return forms


def double_forms():
    saved = json.loads(INPUTS[2].read_text())['disk_templates']
    forms, bases = [], 0
    for input_id, base in enumerate(saved):
        edges = set(map(tuple, base['edges']))
        sigma = sum(1 << i for i, row in enumerate(ROWS)
                    if colorings(edges, row, (), first_only=True))
        assert sigma == base['sigma']
        if sigma != 1022:
            continue
        bases += 1
        rotation_check(edges, base['apex_rotation'])
        interior = sorted(set().union(*map(set, edges)) - B)
        assert len(interior) == 6
        for roots in combinations(interior, 2):
            if roots in edges:
                continue
            regions = pieces(edges, roots)
            assert sum(len(r['owners']) == 2 for r in regions) == 1
            assert len(regions) <= 2
            forms.append(dict(family='double_triangle', input_origin=[2, input_id],
                marker=dict(), original_edges=sorted(edges), original_root_order=list(roots)))
    assert bases == 64 and len(forms) == 512
    return forms


def collision(pairs):
    return next(([list(a), list(b)] for a, b in combinations(pairs, 2)
                 if a[0] == b[0] or a[1] == b[1]), None)


def expand_marked_tail(form):
    """Add two points to every positive unmarked equal-attachment segment.

    Each retained root and triangle point is a singleton branch set. Quotient
    edges and ten whole-root relations are checked; full contact relations of
    the two actual graphs are retained separately.
    """
    edges = set(map(tuple, form['original_edges']))
    roots = form['original_root_order']
    path = form['marker']['path']
    groups, current = [], []
    for v in path:
        ns = tuple(b for b in sorted(B) if (b, v) in edges)
        if v in roots or len(ns) == 3:
            if current:
                groups.append(current)
                current = []
            continue
        if current and ns != tuple(b for b in sorted(B) if (b, current[-1]) in edges):
            groups.append(current)
            current = []
        current.append(v)
    if current:
        groups.append(current)
    expanded = set(edges)
    order = sorted(B | set().union(*map(set, edges)))
    bags = {v: [v] for v in order}
    nextv = max(order) + 1
    for segment in groups:
        anchor = segment[0]
        position = path.index(anchor)
        previous = form['marker']['triangle_parent'] if position == 0 else path[position - 1]
        original_edge = tuple(sorted((anchor, previous)))
        assert original_edge in expanded
        expanded.remove(original_edge)
        a, b = nextv, nextv + 1
        nextv += 2
        expanded |= {tuple(sorted((previous, a))), (a, b), tuple(sorted((b, anchor)))}
        expanded |= {(bd, v) for bd in B if (bd, anchor) in edges for v in (a, b)}
        bags[anchor] += [a, b]
    image = {u: v for v, bag in bags.items() for u in bag}
    quotient = {tuple(sorted((image[a], image[b]))) for a, b in expanded if image[a] != image[b]}
    assert quotient == edges and all(bags[r] == [r] for r in roots)
    for bag in bags.values():
        assert components(bag, expanded) == [sorted(bag)]
    assert all(sum(v in e for e in expanded) == 4 for v in set(image) - B)
    regions = pieces(expanded, roots)
    ports = list(roots) + sorted({v for r in regions for v in r['contact_order']})
    triangle, = [t for t in combinations(order, 3) if t[0] >= 5
                 and all(e in edges for e in combinations(t, 2))]
    anchors = list(roots) + sorted(set(triangle) - set(roots))
    rows = []
    for ri, row in enumerate(ROWS):
        joint = colorings(expanded, row, ports)
        tuples = sorted(joint)
        pins = sorted({t[:2] for t in tuples})
        assert pins == list(map(tuple, form['rows'][ri]['root_pairs']))
        anchor_joint = colorings(expanded, row, anchors)
        assert set(anchor_joint) == set(colorings(edges, row, anchors))
        rows.append(dict(joint_port_tuples=tuples, root_pairs=pins,
            full_coloring_witnesses=[joint[t] for t in tuples],
            anchor_joint_tuples=sorted(anchor_joint),
            full_anchor_coloring_witnesses=[anchor_joint[t] for t in sorted(anchor_joint)]))
    return dict(original_edges=sorted(expanded), original_root_order=roots,
        coloring_vertex_order=sorted(image), branch_sets=[bags[v] for v in order],
        quotient_vertex_order=order, retained_original_pieces=regions,
        port_order=ports, anchor_order=anchors, rows=rows, positive_segments_expanded=len(groups))


def original_control():
    source = json.loads(INPUTS[3].read_text())
    edges, core = [set(map(tuple, source[k])) for k in ('edges', 'M_edges')]
    roots = source['roots_in_z_w_order']
    assert [sum(r in e for e in edges) for r in roots] == [5, 5]
    assert all(sum(v in e for e in edges) == 4
               for v in set().union(*map(set, edges)) - B - set(roots))
    faces = rotation_check(edges, source['original_apex_rotation'])
    rows, masks = [], []
    for graph in (core, edges):
        graph_rows = []
        ports = list(roots) + sorted(set().union(*map(set, graph)) - B - set(roots))
        for row in ROWS:
            joint = colorings(graph, row, ports)
            ts = sorted(joint)
            graph_rows.append(dict(joint_port_tuples=ts,
                full_coloring_witnesses=[joint[t] for t in ts]))
        rows.append(dict(port_order=ports, coloring_vertex_order=sorted(B | set().union(*map(set, graph))),
                         rows=graph_rows))
        masks.append(sum(1 << i for i, r in enumerate(graph_rows) if r['joint_port_tuples']))
    assert masks == [1022, 1018]
    assert all(bool(rows[0]['rows'][i]['joint_port_tuples']) ==
               bool(rows[1]['rows'][i]['joint_port_tuples'])
               for i, row in enumerate(ROWS) if len(set(row)) == 3)
    critical = []
    for edge in sorted(edges - FRAME):
        for ri, row in enumerate(ROWS):
            if masks[1] >> ri & 1:
                continue
            witness = colorings(edges - {edge}, row, (), first_only=True)
            if witness:
                critical.append(dict(edge=edge, newly_accepted_row_index=ri,
                                     coloring=next(iter(witness.values()))))
                break
        else:
            raise AssertionError('Historical actual control lost Sigma-criticality')
    return dict(id=source['id'], original_edges=sorted(edges), core_edges=sorted(core),
        original_root_order=roots, sigma_M=masks[0], sigma_G=masks[1],
        full_target_source_premise='not_triggered', core_and_source_relations=rows,
        verified_apex_faces=faces, source_edge_deletion_witnesses=critical,
        limitation='four-color row 01023 is lost; equality of all ten rows is false')


def build():
    index = {r: i for i, r in enumerate(ROWS)}
    orbits = {str(mask): sorted({sum(1 << index[normalize(
        [row[(s*j+t) % 5] for j in range(5)])]
        for ri, row in enumerate(ROWS) if mask >> ri & 1)
        for s in (-1, 1) for t in range(5)}) for mask in (933, 941)}
    targets = sorted(set().union(*map(set, orbits.values())))
    counts, forms = Counter(), single_forms() + double_forms()
    for form in forms:
        edges, roots = set(map(tuple, form['original_edges'])), form['original_root_order']
        order = sorted(B | set().union(*map(set, edges)))
        interior = set(order) - B
        assert tuple(sorted(roots)) not in edges
        assert all(sum(v in e for e in edges) == 4 for v in interior)
        assert components(interior, edges) == [sorted(interior)]
        regions = pieces(edges, roots)
        ports = list(roots) + sorted({v for r in regions for v in r['contact_order']})
        form.update(coloring_vertex_order=order, retained_original_pieces=regions, port_order=ports)
        form['q_critical_witnesses'] = []
        for edge in sorted(edges - FRAME):
            witness = colorings(edges - {edge}, Q, (), first_only=True)
            assert witness
            form['q_critical_witnesses'].append(dict(edge=edge, coloring=next(iter(witness.values()))))
            counts['q_edge_deletion_witnesses'] += 1
        rows = []
        for row in ROWS:
            joint = colorings(edges, row, ports)
            tuples = sorted(joint)
            pins = sorted({t[:2] for t in tuples})
            assert pins == sorted(colorings(edges, row, roots))
            record = dict(joint_port_tuples=tuples, root_pairs=pins,
                full_coloring_witnesses=[joint[t] for t in tuples],
                root_fibres_by_pin_order=[[i for i, t in enumerate(tuples) if t[:2] == pin] for pin in PINS])
            if len(set(row)) == 3 and row != Q:
                pair = collision(pins)
                assert pair is not None
                record['three_color_capacity_collision'] = pair
                counts['non_q_three_color_row_collisions'] += 1
            rows.append(record)
            counts['full_joint_row_checks'] += 1
        assert sum(1 << i for i, row in enumerate(rows) if row['root_pairs']) == 1022
        form['rows'] = rows
        tests = []
        for target in targets:
            test = dict(target_mask=target)
            empty = next((i for i, r in enumerate(rows) if target >> i & 1 and not r['root_pairs']), None)
            if empty is not None:
                test.update(exclusion='target_accepts_empty_core_row', row_index=empty)
                counts['accepted_empty_exclusions'] += 1
            else:
                ri = next(i for i, r in enumerate(rows)
                          if not (target >> i & 1) and collision(r['root_pairs']) is not None)
                pair = collision(rows[ri]['root_pairs'])
                js = rows[ri]['joint_port_tuples']
                test.update(exclusion='mixed11_same_coordinate_capacity', row_index=ri,
                    collision_pairs=pair,
                    collision_joint_indices=[next(i for i, t in enumerate(js) if list(t[:2]) == p) for p in pair])
                counts['capacity_exclusions'] += 1
            tests.append(test)
            counts['target_comparisons'] += 1
        form['target_comparisons'] = tests
        counts['marked_cores'] += 1
    long_controls = []
    for fi, form in enumerate(forms):
        if form['family'] != 'double_triangle':
            long_controls.append(dict(form_index=fi, expanded=expand_marked_tail(form)))
    counts.update(single_triangle_markers=316, double_triangle_markers=512,
        root_fibres=16 * len(ROWS) * len(forms), long_controls=len(long_controls),
        long_root_pair_comparisons=10 * len(long_controls),
        long_triangle_marker_joint_comparisons=10 * len(long_controls), residuals=0)
    assert counts['marked_cores'] == 828 and counts['target_comparisons'] == 8280
    assert counts['accepted_empty_exclusions'] == 2484 and counts['capacity_exclusions'] == 5796
    assert counts['non_q_three_color_row_collisions'] == 3312
    return dict(schema=1,
        scope='U4 two-root44 only: complete Sigma933/941 and whole-source D5 images',
        source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                       for p in INPUTS + [Path(__file__).resolve()]},
        pattern_order=ROWS, normalized_rejected_row=Q, root_pin_order=PINS,
        target_D5_orbits=orbits, forms=forms, marked_tail_long_controls=long_controls,
        named_original_control=original_control(),
        summary=dict(sorted(counts.items())),
        trust_boundary='paper unbounded classification and marker transfer; finite graph/control evidence; no new Lean theorem or target source realization')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    encoded = json.dumps(result, sort_keys=True, separators=(',', ':')) + '\n'
    if args.check:
        assert OUT.read_text() == encoded, 'Certificate differs; preserve historical inputs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(encoded)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
