#!/usr/bin/env python3
"""Original three-spoke star screen of inherited named binary support domains.

Contract H-a only for a topology minor; retain complete inherited relations.
Explicit K3,3 subdivisions certify exclusions. Passing domains are necessary
domains, not source graphs or common ten-row coloring witnesses.
"""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_four_spoke_binary_star/observations.json'
SOURCE = ROOT / 'artifacts/c5_excess_two_mixed_core_four_spoke_binary/observations.json'
FRAME = {tuple(sorted((i, (i + 1) % 5))) for i in range(5)}
COLORS = set(range(4))
HUB, APEX = 7, 8


def edge(u, v):
    assert u != v
    return tuple(sorted((u, v)))


def sectors(spokes):
    ordered = sorted(spokes)
    return [tuple((u + k) % 5 for k in range((v - u) % 5 + 1))
            for u, v in zip(ordered, ordered[1:] + ordered[:1])]


def minor_edges(a, spokes, support):
    return (FRAME | {edge(a, i) for i in spokes} | {edge(a, HUB)}
            | {edge(HUB, i) for i in support} | {edge(APEX, i) for i in range(5)})


def verify_subdivision(edges, cert):
    left, right = cert['left'], cert['right']
    branches = set(left + right)
    assert len(branches) == 6 and len(left) == len(right) == 3
    assert len(cert['paths']) == 9
    internal, used_edges = set(), set()
    for (u, v), path in zip(product(left, right), cert['paths'], strict=True):
        assert path[0] == u and path[-1] == v and len(set(path)) == len(path)
        assert not branches & set(path[1:-1])
        assert not internal & set(path[1:-1])
        internal.update(path[1:-1])
        steps = {edge(x, y) for x, y in zip(path, path[1:])}
        assert steps <= edges and not used_edges & steps
        used_edges.update(steps)


@lru_cache(None)
def subdivision(edges):
    """Search only paths in this eight-vertex minor, then check all nine paths."""
    edges = set(edges)
    nodes = sorted({v for e in edges for v in e})
    adjacency = {v: sorted(w for w in nodes if v != w and edge(v, w) in edges)
                 for v in nodes}
    for chosen in combinations(nodes, 6):
        for rest in combinations(chosen[1:], 2):
            left = (chosen[0], *rest)
            right = tuple(v for v in chosen if v not in left)
            branches = set(chosen)
            choices = []
            for u, v in product(left, right):
                found = []

                def walk(path):
                    for w in adjacency[path[-1]]:
                        if w == v:
                            found.append(tuple(path + [w]))
                        elif w not in branches and w not in path:
                            walk(path + [w])

                walk([u])
                choices.append(sorted(found, key=lambda p: (len(p), p)))
            if not all(choices):
                continue
            order = sorted(range(9), key=lambda i: (len(choices[i]), i))

            def select(k, used, paths):
                if k == 9:
                    return paths
                i = order[k]
                for path in choices[i]:
                    inside = set(path[1:-1])
                    if not inside & used:
                        result = select(k + 1, used | inside, {**paths, i: path})
                        if result is not None:
                            return result
                return None

            paths = select(0, set(), {})
            if paths is not None:
                cert = dict(left=left, right=right, paths=[paths[i] for i in range(9)])
                verify_subdivision(edges, cert)
                return cert
    return None


def connected(vertices, edges):
    seen = {min(vertices)}
    while True:
        more = seen | {v for e in edges if set(e) & seen for v in e if v in vertices}
        if more == seen:
            return seen == vertices
        seen = more


def component_relation(vertices, edges, attachments, row, contacts):
    """Literal whole-component backtracking; equal contacts remain one vertex."""
    vertices = sorted(vertices)
    result = {}

    def visit(f):
        if len(f) == len(vertices):
            result.setdefault(tuple(f[v] for v in contacts), [f[v] for v in vertices])
            return
        v = vertices[len(f)]
        blocked = {row[b] for b in attachments[v]}
        blocked |= {f[w] for w in f if edge(v, w) in edges}
        for c in sorted(COLORS - blocked):
            visit({**f, v: c})

    visit({})
    for value, witness in result.items():
        f = dict(zip(vertices, witness, strict=True))
        assert tuple(f[v] for v in contacts) == value
        assert all(f[u] != f[v] for u, v in edges)
        assert all(f[v] != row[b] for v in vertices for b in attachments[v])
    return dict(vertex_order=vertices, ordered_contacts=contacts,
                complete_tuples=sorted(result),
                tuple_witnesses=[dict(tuple=t, coloring=result[t]) for t in sorted(result)])


def extracted_controls():
    """Full degree graphs testing both x=y and positive even C paths, no disk claim."""
    records = []
    q = [0, 1, 0, 2, 1]
    for length, u_length, swapped in product((0, 2, 4, 6), (1, 2, 4), (False, True)):
        a, b = (5, 6) if swapped else (6, 5)
        if length == 0:
            cv, x, y = [9, 10, 11, 12], 9, 9
            ce = {edge(9, 10), edge(10, 11), edge(10, 12), edge(11, 12)}
            ca = {9: [1], 10: [1], 11: [0, 1], 12: [1, 2]}
        else:
            cv = list(range(9, 10 + length))
            x, y = cv[0], cv[-1]
            ce = {edge(u, v) for u, v in zip(cv, cv[1:])}
            ca = {v: [1, 2] if i == 1 else [0, 1] for i, v in enumerate(cv)}
        uv = list(range(max(cv) + 1, max(cv) + 2 + u_length))
        u, v = uv[0], uv[-1]
        ue = {edge(w, z) for w, z in zip(uv, uv[1:])}
        ua = {w: [2, 3] if w == u else [3, 4] if w == v else [2, 4] for w in uv}
        original = FRAME | ce | ue | {edge(a, b), edge(a, x), edge(b, y), edge(b, u), edge(b, v)}
        original |= {edge(a, i) for i in (0, 1, 2)} | {edge(b, 0)}
        original |= {edge(w, i) for w, support in {**ca, **ua}.items() for i in support}
        interior = [a, b, *cv, *uv]
        assert all(sum(w in e for e in original) == (5 if w in (a, b) else 4) for w in interior)
        c_relation = component_relation(cv, ce, ca, q, (x, y))
        assert set(c_relation['complete_tuples']) == {(2, 2), (3, 3)}
        whole_bag = set(interior) - {a}
        assert connected(whole_bag, original) and connected(set(cv), original)
        augmented = original | {edge(APEX, i) for i in range(5)}
        direct_bags = [{a}, set(cv), {APEX}, {0}, {1}, {2}]
        assert all(connected(bag, augmented) for bag in direct_bags)
        assert sum(map(len, direct_bags)) == len(set.union(*direct_bags))
        adjacencies = []
        for i, j in product(range(3), range(3, 6)):
            witnesses = [e for e in sorted(augmented)
                         if (e[0] in direct_bags[i] and e[1] in direct_bags[j])
                         or (e[1] in direct_bags[i] and e[0] in direct_bags[j])]
            assert witnesses
            adjacencies.append(dict(bags=[i, j], original_edge=witnesses[0]))
        mapping = {w: HUB if w in whole_bag else w for w in range(max(interior) + 1)}
        contracted = {edge(mapping[w], mapping[z]) for w, z in augmented if mapping[w] != mapping[z]}
        expected = minor_edges(a, (0, 1, 2), tuple(range(5)))
        assert contracted == expected
        cert = subdivision(tuple(sorted(contracted)))
        assert cert is not None
        records.append(dict(control_index=len(records), a=a, b=b,
            C_path_length=length, U_path_length=u_length, original_edges=sorted(original),
            original_C_vertices=cv, original_U_vertices=uv, actual_attachments={**ca, **ua},
            C_contacts=[x, y], U_contacts=[u, v], literal_row=q,
            complete_C_relation=c_relation,
            complete_U_relation=component_relation(uv, ue, ua, q, (u, v)),
            original_H_minus_a_connected_bag=sorted(whole_bag),
            contracted_augmented_edges=sorted(contracted), subdivision=cert,
            direct_K33_connected_branch_sets=[sorted(bag) for bag in direct_bags],
            direct_K33_original_edge_witnesses=adjacencies,
            scope='Full degree graph, C diagonal pair, topology lifting control; no source Sigma/criticality/disk'))
    assert len(records) == 24
    return records


def build():
    source = json.loads(SOURCE.read_text())
    targets, root_swaps, symmetry_checks = [], 0, 0
    for target in source['marked_core_reduction']['targets']:
        counts, frames, keys = Counter(), [], {}
        for original_frame in target['frames']:
            frame = {k: v for k, v in original_frame.items() if k != 'same_source_domains'}
            sa, b_spoke = frame['original_a_spoke_support'], frame['original_b_spoke']
            arcs = sectors(sa)
            domains = []
            for original_domain in original_frame['same_source_domains']:
                if original_domain['status'] != 'necessary_residual_not_realization':
                    continue
                counts['inherited_necessary_domains'] += 1
                sc, su = map(set, original_domain['actual_original_supports'])
                sw = sc | su | {b_spoke}
                fits_c = [arc for arc in arcs if sc <= set(arc)]
                fits_w = [arc for arc in arcs if sw <= set(arc)]
                edges = minor_edges(frame['a'], sa, sw)
                cert = subdivision(tuple(sorted(edges)))
                assert bool(fits_w) == (cert is None)
                record = dict(original_domain=original_domain,
                    original_H_minus_a_support=sorted(sw), original_star_sectors=arcs,
                    sectors_containing_C=fits_c, sectors_containing_H_minus_a=fits_w,
                    topology_minor_bags=dict(a=[frame['a']], W=['original b', 'whole original C', 'whole original U']),
                    original_W_connectivity_edges=['by', 'bu', 'bv'],
                    original_a_W_edge='ab', augmented_minor_edges=sorted(edges))
                if cert is None:
                    record['status'] = 'necessary_residual_not_realization'
                    counts['remaining_necessary_domains'] += 1
                    schedules = {tuple(sorted({len(row['forbidden_colors'][0])
                        for row in assignment['same_literal_row_whole_relation_domains']}))
                        for assignment in original_domain['compatible_same_source_query_assignments']}
                    assert schedules == {(2,)}
                    counts['remaining_all_pair_domains'] += 1
                else:
                    record.update(status='excluded_by_original_star', subdivision=cert)
                    counts['excluded_domains'] += 1
                    if not fits_c:
                        c_edges = minor_edges(frame['a'], sa, sc)
                        c_cert = (dict(left=[frame['a'], HUB, APEX], right=sa,
                            paths=[[v, w] for v, w in product([frame['a'], HUB, APEX], sa)])
                            if len(sc & set(sa)) == 3 else subdivision(tuple(sorted(c_edges))))
                        assert c_cert is not None
                        verify_subdivision(c_edges, c_cert)
                        record['original_C_only_minor'] = dict(
                            contracted_bag='whole original C', original_a_C_edge='ax',
                            augmented_minor_edges=sorted(c_edges), subdivision=c_cert)
                    if len(sc & set(sa)) == 3:
                        counts['C_three_common_neighbors'] += 1
                    elif not fits_c:
                        counts['C_cyclic_interleaving'] += 1
                    else:
                        counts['H_minus_a_additional_sector_conflict'] += 1
                # D5 moves the entire named boundary; roots and the W bag retain identity.
                for sign, shift in product((-1, 1), range(5)):
                    move = {i: (sign * i + shift) % 5 for i in range(5)}
                    moved_sa, moved_sw = {move[i] for i in sa}, {move[i] for i in sw}
                    assert bool(fits_w) == any(moved_sw <= set(arc) for arc in sectors(moved_sa))
                    if cert is not None:
                        def moved(v):
                            return move.get(v, v)
                        transported = dict(left=[moved(v) for v in cert['left']],
                            right=[moved(v) for v in cert['right']],
                            paths=[[moved(v) for v in path] for path in cert['paths']])
                        verify_subdivision(minor_edges(frame['a'], moved_sa, moved_sw), transported)
                    symmetry_checks += 1
                key = (tuple(sa), b_spoke, tuple(sorted(sc)), tuple(sorted(su)), frame['a'], frame['b'])
                keys[key] = (record['status'], original_domain['compatible_same_source_query_assignments'])
                domains.append(record)
            if domains:
                frames.append(dict(original_frame_context=frame, domains=domains))
        for key, value in keys.items():
            swapped = (*key[:4], key[5], key[4])
            assert keys[swapped] == value
            root_swaps += 1
        expected = ({'inherited_necessary_domains': 116, 'excluded_domains': 84,
                     'C_three_common_neighbors': 68, 'C_cyclic_interleaving': 16,
                     'remaining_necessary_domains': 32, 'remaining_all_pair_domains': 32}
                    if target['source_sigma'] == 933 else
                    {'inherited_necessary_domains': 256, 'excluded_domains': 192,
                     'C_three_common_neighbors': 144, 'C_cyclic_interleaving': 40,
                     'H_minus_a_additional_sector_conflict': 8,
                     'remaining_necessary_domains': 64, 'remaining_all_pair_domains': 64})
        assert dict(counts) == expected
        targets.append(dict(source_sigma=target['source_sigma'], counts=dict(sorted(counts.items())), frames=frames))
    assert root_swaps == 372 and symmetry_checks == 3720
    named = []
    for target in targets:
        entries = []
        for spoke, sc, su, status in ((0, [0, 1, 2], [2, 3, 4], 'excluded_by_original_star'),
                                     (2, [0, 4], [2, 3, 4], 'necessary_residual_not_realization')):
            frame, = [f for f in target['frames'] if f['original_frame_context']['a'] == 6
                      and f['original_frame_context']['original_a_spoke_support'] == [0, 1, 2]
                      and f['original_frame_context']['original_b_spoke'] == spoke]
            domain, = [d for d in frame['domains'] if d['original_domain']['actual_original_supports'] == [sc, su]]
            assert domain['status'] == status
            entries.append(dict(original_frame_index=frame['original_frame_context']['frame_index'],
                original_domain_index=domain['original_domain']['domain_index'], a=6, b=5,
                a_spokes=[0, 1, 2], b_spoke=spoke, actual_C_support=sc, actual_U_support=su,
                status=status))
        named.append(dict(source_sigma=target['source_sigma'], excluded_original_entry=entries[0],
                          next_necessary_entry=entries[1]))
    paths = [Path(__file__), SOURCE, ROOT / 'scripts/c5_excess_two_mixed_core_four_spoke_binary.py']
    return dict(schema=1, scope=__doc__, pattern_order=source['pattern_order'],
        input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths},
        topology_contraction_scope='Minor only; no change to color relations or identification of contact colors',
        source_inherited_named_relation_records=source['marked_core_reduction']['inherited_named_records'],
        inherited_base_replay_audit=source['inherited_base_replay_audit'],
        targets=targets, named_entries=named, fixed_original_graph_controls=extracted_controls(),
        summary=dict(target_counts=[dict(source_sigma=t['source_sigma'], **t['counts']) for t in targets],
            explicit_K33_subdivisions=276, root_swap_domain_checks=root_swaps,
            simultaneous_D5_topology_checks=symmetry_checks, fixed_full_degree_graph_controls=24,
            selected_original_entry_excluded=True, selected_binary_subtype_excluded=False,
            cross_row_palette_theorem_proved=False, epsilon_three_proved=False, new_lean_theorem=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    payload = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=1) + '\n'
    if args.check:
        assert OUT.read_bytes() == payload.encode(), f'certificate differs: {OUT}'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
