#!/usr/bin/env python3
"""Fixed controls for the short-support forbidden-color exclusion.

The unbounded two-hub Gallai lemma is a paper proof. These are explicit
nonplanar minor skeletons, not complete source graphs or a graph catalogue.
"""
import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_short_support_singleton/observations.json'


def edge(a, b):
    assert a != b
    return tuple(sorted((a, b)))


def connected(vertices, edges):
    vertices = set(vertices)
    if not vertices:
        return False
    seen, todo = set(), [min(vertices)]
    while todo:
        v = todo.pop()
        if v in seen:
            continue
        seen.add(v)
        todo.extend(b if a == v else a for a, b in edges
                    if v in (a, b) and {a, b} <= vertices)
    return seen == vertices


def k5_witness(edges, branch_sets):
    edges = set(map(tuple, edges))
    groups = [set(vs) for vs in branch_sets]
    assert len(groups) == 5 and all(connected(vs, edges) for vs in groups)
    assert all(not (a & b) for a, b in combinations(groups, 2))
    witnesses = []
    for i, j in combinations(range(5), 2):
        choices = sorted(e for e in edges if
                         (e[0] in groups[i] and e[1] in groups[j]) or
                         (e[1] in groups[i] and e[0] in groups[j]))
        assert choices, (i, j)
        witnesses.append(dict(branch_pair=[i, j], original_edge=choices[0]))
    return dict(branch_sets=[sorted(vs) for vs in groups],
                all_ten_adjacencies=witnesses)


def template(name, cycles, bridges):
    edges = {edge(a, b) for c in cycles for a, b in zip(c, c[1:] + c[:1])}
    edges.update(edge(a, b) for a, b in bridges)
    vertices = sorted(set().union(*(set(c) for c in cycles)))
    vertices = sorted(set(vertices) | {v for e in bridges for v in e})
    degrees = {v: sum(v in e for e in edges) for v in vertices}
    assert connected(vertices, edges) and all(2 <= d <= 4 for d in degrees.values())
    assert all(len(c) >= 3 and len(c) % 2 for c in cycles)
    # The supplied blocks themselves must form one incidence tree. This checks
    # that the hand-built motifs are cacti with exactly the specified blocks.
    blocks = cycles + [list(e) for e in bridges]
    offset = max(vertices) + 1
    incidence = {edge(v, offset + i) for i, block in enumerate(blocks) for v in block}
    incidence_vertices = vertices + list(range(offset, offset + len(blocks)))
    assert connected(incidence_vertices, incidence)
    assert len(incidence) == len(incidence_vertices) - 1
    leaf = next(c for c in cycles if sum(degrees[v] > 2 for v in c) <= 1)
    u, w = next((a, b) for a, b in zip(leaf, leaf[1:] + leaf[:1])
                if degrees[a] == degrees[b] == 2)
    remainder = sorted(set(vertices) - {u, w})
    assert connected(remainder, edges)
    witness = next(v for v in remainder if degrees[v] == 2)
    return dict(name=name, vertices=vertices, cycles=cycles, bridges=bridges,
        edges=sorted(edges), degrees=degrees, selected_leaf_cycle=leaf,
        adjacent_private_vertices=[u, w], remainder=remainder,
        remainder_original_degree_two_vertex=witness)


def templates():
    result = []
    for length in (3, 5, 7):
        result.append(template(f'one_cycle_{length}', [list(range(length))], []))
    for left, right in product((3, 5), repeat=2):
        first = list(range(left))
        shared = [0] + list(range(left, left + right - 1))
        result.append(template(f'shared_cycles_{left}_{right}', [first, shared], []))
        for distance in (1, 2, 3):
            second = list(range(left, left + right))
            path = [0] + list(range(left + right, left + right + distance - 1)) + [left]
            result.append(template(f'bridge_cycles_{left}_{right}_{distance}',
                [first, second], list(map(list, zip(path, path[1:])))))
    result.append(template('three_cycle_chain', [[0, 1, 2], [3, 4, 5], [6, 7, 8]],
                           [[0, 3], [4, 6]]))
    result.append(template('central_cycle_three_leaves',
        [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]], [[0, 3], [1, 6], [2, 9]]))
    return result


def two_hub_controls():
    motifs, records = templates(), []
    for ti, motif in enumerate(motifs):
        vertices = motif['vertices']
        x, y = max(vertices) + 1, max(vertices) + 2
        degree_three = [v for v in vertices if motif['degrees'][v] == 3]
        for choices in product((x, y), repeat=len(degree_three)):
            edges = set(map(tuple, motif['edges'])) | {edge(x, y)}
            for v in vertices:
                if motif['degrees'][v] == 2:
                    edges.update((edge(v, x), edge(v, y)))
            edges.update(edge(v, h) for v, h in zip(degree_three, choices))
            assert all(sum(v in e for e in edges) == 4 for v in vertices)
            u, w = motif['adjacent_private_vertices']
            witness = k5_witness(edges, [[x], [y], [u], [w], motif['remainder']])
            records.append(dict(template_index=ti, degree_three_vertices=degree_three,
                chosen_hubs=choices, hub_order=[x, y], edges=sorted(edges), **witness))
    return dict(templates=motifs, full_degree_four_two_hub_skeletons=records)


def original_lift_controls():
    records = []
    for a in range(5):
        for direction in (-1, 1):
            b = (a + direction) % 5
            for spoke, end, length in product(range(5), sorted(set(range(5)) - {a, b}), (2, 3)):
                for cycle_length in (3, 5):
                    # One named consecutive contact set of every cardinality;
                    # the theorem does not require consecutive contacts.
                    for contact_count in range(1, cycle_length + 1):
                        r = 5
                        cycle = list(range(6, 6 + cycle_length))
                        contacts = cycle[:contact_count]
                        inside_path = list(range(6 + cycle_length,
                                                 6 + cycle_length + length - 1))
                        path = [r] + inside_path + [end]
                        edges = {edge(j, (j + 1) % 5) for j in range(5)}
                        edges.add(edge(r, spoke))
                        edges.update(edge(u, v) for u, v in zip(path, path[1:]))
                        edges.update(edge(u, v) for u, v in zip(cycle, cycle[1:] + cycle[:1]))
                        for v in cycle:
                            edges.add(edge(v, b))
                            edges.add(edge(v, r if v in contacts else a))
                        assert all(sum(v in e for e in edges) == 4 for v in cycle)
                        x = [b]
                        y = sorted((set(range(5)) - {b}) | {r} | set(inside_path))
                        u, w = cycle[:2]
                        witness = k5_witness(edges, [x, y, [u], [w], cycle[2:]])
                        support = [b] if contact_count == cycle_length else sorted([a, b])
                        records.append(dict(support_envelope=[a, b], actual_support=support, original_root=r,
                            original_contacts=contacts, original_component_cycle=cycle,
                            original_spoke=[r, spoke], external_path=path,
                            seen_forbidden_color_at_boundary_vertex=a,
                            edges=sorted(edges), **witness))
    return records


def local_controls():
    # r and a receive color 0; b receives color 1. Tightness is equivalent to
    # having no duplicate external color, hence forbids merging parallel edges.
    tight = []
    for mask in range(8):
        outside = [j for j in range(3) if mask >> j & 1]
        colors = [0, 0, 1]
        internal_degree = 4 - len(outside)
        list_size = 4 - len({colors[j] for j in outside})
        no_collision = not (0 in outside and 1 in outside)
        assert (list_size == internal_degree) == no_collision
        if no_collision:
            assert len({0 if j < 2 else 1 for j in outside}) == len(outside)
        tight.append(dict(external_neighbor_order=['r', 'boundary_a', 'boundary_b'],
            present_indices=outside, internal_degree=internal_degree,
            list_size=list_size, tight=no_collision))
    # For two differently colored support vertices the stabilizer exchanges the
    # two unseen colors. Record all invariant subsets, with contacts capacity.
    invariant = []
    for mask in range(16):
        forbidden = {c for c in range(4) if mask >> c & 1}
        swapped = {3 if c == 2 else 2 if c == 3 else c for c in forbidden}
        if swapped == forbidden:
            surviving = not (forbidden & {0, 1})
            invariant.append(dict(forbidden=sorted(forbidden), survives_seen_color_lemma=surviving))
    assert [r['forbidden'] for r in invariant if r['survives_seen_color_lemma']] == [[], [2, 3]]
    return dict(tight_external_neighbor_cases=tight, support_stabilizer_cases=invariant)


def list_colorings(vertices, edges, lists):
    vertices = list(vertices)
    assigned = {}
    result = []
    def visit():
        if len(assigned) == len(vertices):
            result.append(dict(assigned))
            return
        v = min((v for v in vertices if v not in assigned),
                key=lambda v: (len(lists[v]), v))
        for color in sorted(lists[v]):
            if any(assigned.get(b if a == v else a) == color
                   for a, b in edges if v in (a, b)):
                continue
            assigned[v] = color
            visit()
            del assigned[v]
    visit()
    return result


def three_hub_controls():
    cases = [('edge', [], [(0, 1)]),
             ('path_three', [], [(0, 1), (1, 2)]),
             ('path_four', [], [(0, 1), (1, 2), (2, 3)]),
             ('triangle', [[0, 1, 2]], []),
             ('pentagon', [[0, 1, 2, 3, 4]], []),
             ('triangle_one_tail', [[0, 1, 2]], [(0, 3)]),
             ('triangle_two_tail', [[0, 1, 2]], [(0, 3), (3, 4)]),
             ('two_triangles_bridge', [[0, 1, 2], [3, 4, 5]], [(0, 3)]),
             ('two_triangles_shared', [[0, 1, 2], [0, 3, 4]], [])]
    records, summary = [], []
    for name, cycles, bridges in cases:
        inside_edges = {edge(a, b) for c in cycles for a, b in zip(c, c[1:] + c[:1])}
        inside_edges.update(edge(a, b) for a, b in bridges)
        vertices = sorted({v for e in inside_edges for v in e})
        degrees = {v: sum(v in e for e in inside_edges) for v in vertices}
        hubs = list(range(max(vertices) + 1, max(vertices) + 4))
        colors = dict(zip(hubs, range(3)))
        options = [list(combinations(hubs, 4 - degrees[v])) for v in vertices]
        checked, rejected = 0, 0
        for attachments in product(*options):
            lists = {v: set(range(4)) - {colors[h] for h in hs}
                     for v, hs in zip(vertices, attachments)}
            checked += 1
            if list_colorings(vertices, inside_edges, lists):
                continue
            rejected += 1
            edges = inside_edges | {edge(a, b) for a, b in combinations(hubs, 2)}
            edges |= {edge(v, h) for v, hs in zip(vertices, attachments) for h in hs}
            assert all(sum(v in e for e in edges) == 4 for v in vertices)
            leaves = [v for v in vertices if degrees[v] == 1]
            extra = {}
            if leaves:
                u = leaves[0]
                rest = sorted(set(vertices) - {u})
                neighbor, = [b if a == u else a for a, b in inside_edges if u in (a, b)]
                colorings = list_colorings(rest, inside_edges, lists)
                assert colorings and {f[neighbor] for f in colorings} == {3}
                assert all(any(edge(v, h) in edges for v in rest) for h in hubs)
                groups = [[h] for h in hubs] + [[u], rest]
                reason = 'leaf_bridge_with_forced_fourth_color'
                extra = dict(original_leaf=u, original_bridge_neighbor=neighbor,
                    bridge_deleted_rest_coloring=[[v, colorings[0][v]] for v in rest],
                    rest_endpoint_domain=[3])
            else:
                cycle = next(c for c in cycles if sum(degrees[v] > 2 for v in c) <= 1)
                private = [v for v in cycle if degrees[v] == 2]
                assert all(lists[v] == lists[private[0]] for v in private)
                u, w = next((a, b) for a, b in zip(cycle, cycle[1:] + cycle[:1])
                            if a in private and b in private)
                pair = [h for h in hubs if edge(u, h) in edges]
                third, = set(hubs) - set(pair)
                rest = sorted(set(vertices) - {u, w})
                third_touches = any(edge(v, third) in edges for v in rest)
                groups = [[h] for h in pair] + [[u], [w], rest + ([third] if third_touches else [])]
                reason = 'leaf_cycle_with_third_hub' if third_touches else 'two_hub_fallback'
                extra = dict(selected_leaf_cycle=cycle, adjacent_private_vertices=[u, w],
                    common_private_palette=sorted(lists[u]), third_hub=third,
                    third_hub_touches_component=third_touches)
            witness = k5_witness(edges, groups)
            records.append(dict(template=name, component_vertices=vertices,
                component_edges=sorted(inside_edges), hub_order=hubs,
                hub_colors=[0, 1, 2], lists=[sorted(lists[v]) for v in vertices],
                attachments=attachments, edges=sorted(edges), reason=reason, **extra, **witness))
        summary.append(dict(template=name, attachment_cases=checked,
                            rejected_cases=rejected, accepted_cases=checked - rejected))
    return dict(template_summary=summary, rejected_cases=records)


def unseen_original_lifts():
    records = []
    for a, direction, spoke, length, size in product(range(5), (-1, 1), range(5), (2, 3), (2, 4)):
        b = (a + direction) % 5
        for end in sorted(set(range(5)) - {a, b}):
            r = 5
            path = list(range(6, 6 + size))
            contacts = path[:]
            outside = list(range(6 + size, 6 + size + length - 1))
            external_path = [r] + outside + [end]
            edges = {edge(i, (i + 1) % 5) for i in range(5)} | {edge(r, spoke)}
            edges.update(edge(u, v) for u, v in zip(external_path, external_path[1:]))
            edges.update(edge(u, v) for u, v in zip(path, path[1:]))
            edges.update(edge(r, v) for v in path)
            edges.update(edge(a, v) for v in path)
            edges.update((edge(b, path[0]), edge(b, path[-1])))
            assert all(sum(v in e for e in edges) == 4 for v in path)
            third = sorted((set(range(5)) - {a, b}) | {r} | set(outside))
            witness = k5_witness(edges, [[a], [b], third, [path[0]], path[1:]])
            records.append(dict(actual_support=sorted([a, b]), original_root=r,
                original_contacts=contacts, original_component_path=path,
                original_spoke=[r, spoke], external_path=external_path,
                forbidden_unseen_pair=[2, 3], edges=sorted(edges), **witness))
    return records


def build():
    two_hub = two_hub_controls()
    originals = original_lift_controls()
    local = local_controls()
    three_hub = three_hub_controls()
    unseen_lifts = unseen_original_lifts()
    return dict(schema=1, source_sha256={'scripts/c5_short_support_singleton.py':
            sha256(Path(__file__).read_bytes()).hexdigest()},
        scope='short adjacent two-point support excludes every forbidden color for arbitrary contacts when an external root path exists',
        two_hub_controls=two_hub, original_lift_controls=originals, local_controls=local,
        three_hub_controls=three_hub, unseen_original_lift_controls=unseen_lifts,
        paper_dependencies=['degree-list characterization gives Gallai blocks',
            'connected original exterior excludes K4 blocks',
            'two-hub Gallai leaf-cycle K5 minor for arbitrary size',
            'three-hub tight Gallai leaf-cycle or leaf-bridge K5 minor for arbitrary size',
            'original exterior root path and tightness justify disjoint hub contraction'],
        summary=dict(gallai_templates=len(two_hub['templates']),
            two_hub_k5_skeletons=len(two_hub['full_degree_four_two_hub_skeletons']),
            original_c5_k5_skeletons=len(originals), local_tightness_cases=8,
            invariant_forbidden_sets=8, after_seen_color_lemma=[[], [2, 3]],
            three_hub_attachment_cases=sum(c['attachment_cases'] for c in three_hub['template_summary']),
            three_hub_rejected_k5_cases=len(three_hub['rejected_cases']),
            unseen_original_c5_k5_skeletons=len(unseen_lifts), surviving_forbidden_sets=[[]],
            graph_catalogue_search=False, source_realizability_claimed=False,
            new_lean_theorem=False))


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
