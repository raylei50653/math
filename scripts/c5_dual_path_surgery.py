#!/usr/bin/env python3
"""Ordered dual path surgery, replaying existing induced-C5 triangulations.

No graph catalogue search and no record-110 realizability claim. Standard library
only: oriented triangular faces are reconstructed and checked as a sphere map.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path

from c5_kempe_connectivity import colorings

ROOT = Path(__file__).resolve().parents[1]
CAT = ROOT / 'artifacts/c5_cells/cells.json'
OUT = ROOT / 'artifacts/c5_cells/dual_path_surgery.json'
PAIRS = ((1, 2), (1, 3), (2, 3))


def check_faces(n, edges, faces):
    """A connected oriented sphere map with the specified C5 face removed."""
    all_faces = list(faces) + [(4, 3, 2, 1, 0)]
    darts = [(f[j], f[(j + 1) % len(f)]) for f in all_faces for j in range(len(f))]
    assert Counter(darts) == Counter((u, v) for e in edges for u, v in (e, e[::-1]))
    rotation = {(v, f[j - 1]): f[(j + 1) % len(f)]
                for f in all_faces for j, v in enumerate(f)}
    for v in range(n):
        neighbors = {w for u, w in rotation if u == v}
        root = min(neighbors)
        seen, x = set(), root
        while x not in seen:
            seen.add(x)
            x = rotation[v, x]
        assert x == root and seen == neighbors
    reached = {0}
    while True:
        more = reached | {v for u, v in darts if u in reached}
        if more == reached:
            break
        reached = more
    assert reached == set(range(n)) and n - len(edges) + len(all_faces) == 2
    assert all(len(f) == 3 for f in faces)


def triangular_faces(n, edges):
    """Exact cover of darts of one fixed witness, not an enumeration of graphs."""
    outer = {(i, (i + 1) % 5) for i in range(5)}
    darts = {(u, v) for e in edges for u, v in (e, e[::-1])} - {(v, u) for u, v in outer}
    triangles = []
    for u, v, w in permutations(range(n), 3):
        ds = {(u, v), (v, w), (w, u)}
        if u == min(u, v, w) and ds <= darts:
            triangles.append(((u, v, w), ds))
    by_dart = {d: [i for i, (_, ds) in enumerate(triangles) if d in ds] for d in darts}

    def visit(todo, chosen):
        if not todo:
            try:
                check_faces(n, edges, chosen)
            except AssertionError:
                return None
            return sorted(chosen)
        options = min(([i for i in by_dart[d] if triangles[i][1] <= todo]
                       for d in sorted(todo)), key=len)
        for i in options:
            f, ds = triangles[i]
            answer = visit(todo - ds, chosen + [f])
            if answer is not None:
                return answer
        return None

    answer = visit(darts, [])
    assert answer is not None
    return answer


def dual(edges, faces):
    incidence = {e: [] for e in edges}
    for j, f in enumerate(faces):
        for u, v in zip(f, f[1:] + f[:1]):
            incidence[tuple(sorted((u, v)))].append(j)
    for i in range(5):
        incidence[tuple(sorted((i, (i + 1) % 5)))].append(len(faces) + i)
    assert all(len(vs) == 2 for vs in incidence.values())
    return [tuple(incidence[e]) for e in edges]


def strands(links):
    """Trace a degree <=2 multigraph, retaining parallel links and cycles."""
    adj = {}
    for e, (u, v) in enumerate(links):
        adj.setdefault(u, []).append((v, e))
        adj.setdefault(v, []).append((u, e))
    assert all(len(es) in (1, 2) for es in adj.values())
    pending = set(adj)
    result = []
    while pending:
        root = min(pending)
        component, queue = {root}, [root]
        for u in queue:
            for v, _ in adj[u]:
                if v not in component:
                    component.add(v)
                    queue.append(v)
        pending -= component
        ends = sorted(v for v in component if len(adj[v]) == 1)
        assert len(ends) in (0, 2)
        start = ends[0] if ends else min(component)
        order, edge_order, used, current = [start], [], set(), start
        while True:
            options = sorted((e, v) for v, e in adj[current] if e not in used)
            if not options:
                break
            e, v = options[0]
            used.add(e)
            edge_order.append(e)
            order.append(v)
            current = v
        assert len(used) == sum(len(adj[v]) for v in component) // 2
        result.append(dict(ends=ends, vertices=order, edges=edge_order))
    return result


def pair_strands(de, labels, pair, removed=()):
    selected = [e for e, c in enumerate(labels) if c in pair and e not in removed]
    return [dict(s, edges=[selected[j] for j in s['edges']])
            for s in strands([de[j] for j in selected])]


def matching(de, labels, pair, f):
    ss = pair_strands(de, labels, pair)
    pairs = tuple(sorted(tuple(v - f for v in s['ends']) for s in ss if s['ends']))
    assert all(0 <= v < 5 for p in pairs for v in p)
    for (a, b), (c, d) in combinations(pairs, 2):
        assert not (a < c < b < d or c < a < d < b)
    return pairs, sum(not s['ends'] for s in ss)


def boundary_state(de, labels, f):
    return tuple(matching(de, labels, p, f)[0] for p in PAIRS)


def integrate(n, edges, labels):
    values = [None] * n
    values[0] = 0
    while any(c is None for c in values):
        previous = values.count(None)
        for (u, v), label in zip(edges, labels):
            if values[u] is not None:
                if values[v] is None:
                    values[v] = values[u] ^ label
                else:
                    assert values[v] == values[u] ^ label
            elif values[v] is not None:
                values[u] = values[v] ^ label
        assert values.count(None) < previous
    assert all(values[u] ^ values[v] == label for (u, v), label in zip(edges, labels))
    return values


def ordered_surgery(de, labels, f, pair, strand):
    """Predict both mixed pairs from PRE-switch ordered cut data alone."""
    a, b = pair
    c = 6 - a - b
    switched_edges = set(strand['edges'])
    order = strand['vertices']
    internal = [v for v in order if v < f]
    if not strand['ends']:
        assert internal[-1] == internal[0]
        internal.pop()
    assert len(set(internal)) == len(internal)
    names = {v: f't{i}' for i, v in enumerate(internal)}
    names.update({f + i: f'e{i}' for i in range(5)})
    local = {x: [tuple(names[v] for v in de[e]) for e in strand['edges'] if labels[e] == x]
             for x in pair}
    prediction, cuts = {}, []
    for old, new in ((a, b), (b, a)):
        outside = pair_strands(de, labels, (old, c), switched_edges)
        segments = [dict(ends=tuple(names[v] for v in s['ends']), edges=s['edges'])
                    for s in outside if s['ends']]
        untouched_cycles = [s['edges'] for s in outside if not s['ends']]
        endpoint_list = [v for s in segments for v in s['ends']]
        assert len(endpoint_list) == len(set(endpoint_list))
        assert {names[v] for v in internal} <= set(endpoint_list)

        def glue(which):
            ss = strands([s['ends'] for s in segments] + local[which])
            ps = tuple(sorted(tuple(sorted(int(v[1:]) for v in s['ends']))
                              for s in ss if s['ends']))
            assert all(v.startswith('e') for s in ss for v in s['ends'])
            return ps, len(untouched_cycles) + sum(not s['ends'] for s in ss)

        # Reconstructing the old data is an independent guard on the cut.
        assert glue(old) == matching(de, labels, tuple(sorted((old, c))), f)
        prediction[tuple(sorted((old, c)))] = glue(new)
        cuts.append(dict(pair=sorted((old, c)), exterior_segments=segments,
                         untouched_cycles=untouched_cycles,
                         old_local_links=local[old], new_local_links=local[new],
                         predicted_matching=glue(new)[0], predicted_cycles=glue(new)[1]))
    return prediction, dict(ordered_vertices=order, ordered_path_edges=strand['edges'],
                            port_vertices=internal, local_links=local, cuts=cuts)


def check_cut_sides(edges, faces, strand, cut_data):
    """Use the SAME oriented drawing for both exterior matchings."""
    s, t = (v - len(faces) for v in strand['ends'])
    assert s < t
    sides = {}
    for i, v in enumerate(cut_data['port_vertices']):
        face = faces[v]
        rotation = [edges.index(tuple(sorted((face[j], face[(j + 1) % 3])))) for j in range(3)]
        incoming, outgoing = strand['edges'][i:i + 2]
        sides[f't{i}'] = int((rotation.index(outgoing) - rotation.index(incoming)) % 3 == 1)
    arcs = [list(reversed(range(s + 1, t))), list(range(t + 1, 5)) + list(range(s))]
    for side, arc in enumerate(arcs):
        sides.update({f'e{i}': side for i in arc})
    orders = [[f't{i}' for i in range(len(cut_data['port_vertices'])) if sides[f't{i}'] == side]
              + [f'e{i}' for i in arc] for side, arc in enumerate(arcs)]
    for cut in cut_data['cuts']:
        for segment in cut['exterior_segments']:
            u, v = segment['ends']
            assert sides[u] == sides[v]
        for side, order in enumerate(orders):
            pairs = [tuple(sorted(order.index(v) for v in segment['ends']))
                     for segment in cut['exterior_segments'] if sides[segment['ends'][0]] == side]
            for (a, b), (c, d) in combinations(pairs, 2):
                assert not (a < c < b < d or c < a < d < b)
    cut_data['cut_side_orders'] = orders


def record110_constraints():
    data = json.loads((ROOT / 'artifacts/c5_single_spoke_two_two/observations.json').read_text())
    r = data['records'][110]
    assert (r['id'], r['spoke'], r['supports'], r['bans']) == (110, 0, [[3, 4], [1, 2]], [[1, 2], [2, 3]])
    assert [t['status'] for t in r['targets']] == ['reject', 'reject']
    # A hypothetical source is 2-connected by minimality, so the paper's
    # color-preserving face completion retains the entire marked source.
    # This is not an assertion that the record has a source.
    word = (1, 1, 2, 1, 3)  # alpha = 01023
    forbidden = {(3, 4), (2, 3), (0, 4)}
    allowed = []
    for pair in PAIRS:
        ends = [i for i, c in enumerate(word) if c in pair]
        options = [[(ends[0], ends[1])]] if len(ends) == 2 else [
            [(ends[0], ends[1]), (ends[2], ends[3])],
            [(ends[0], ends[3]), (ends[1], ends[2])]]
        keep = []
        for option in options:
            outcomes = []
            for selected in range(1 << len(option)):
                new_word = list(word)
                for j, edge in enumerate(option):
                    if selected >> j & 1:
                        for end in edge:
                            new_word[end] = sum(pair) - new_word[end]
                minority = tuple(i for i, x in enumerate(new_word) if new_word.count(x) == 1)
                assert len(minority) == 2
                outcomes.append(minority)
            if not any(p in forbidden for p in outcomes):
                keep.append(option)
        assert len(keep) == 1
        allowed.append(dict(pair=pair, matching=keep[0]))
    return dict(record=110, alpha=[0, 1, 0, 2, 3], edge_word=word,
                forbidden_edge_pairs=sorted(forbidden), forced_matchings=allowed,
                after_minority_23_switch=[allowed[1]['matching'], allowed[0]['matching'], allowed[2]['matching']],
                scope='Necessary for every alpha-preserving completion of a hypothetical source; no source existence or exclusion claim.')


def report():
    catalogue = json.loads(CAT.read_text())['cells']
    rows, negative_records = [], []
    totals = Counter()
    for mask, entry in sorted(catalogue.items(), key=lambda item: int(item[0])):
        n = 5 + entry['k_eff']
        edges = sorted({tuple(sorted(e)) for e in entry['edges'] + [[i, (i + 1) % 5] for i in range(5)]})
        if len(edges) != 3 * n - 8 or any(u < 5 and v < 5 and (u - v) % 5 not in (1, 4) for u, v in edges):
            continue
        faces = triangular_faces(n, edges)
        check_faces(n, edges, faces)
        de, f = dual(edges, faces), len(faces)
        counts = Counter()
        for coloring in colorings(entry['k_eff'], edges):
            labels = tuple(coloring[u] ^ coloring[v] for u, v in edges)
            assert all({labels[e] for e, vs in enumerate(de) if v in vs} == {1, 2, 3} for v in range(f))
            before = boundary_state(de, labels, f)
            counts['colorings'] += 1
            for pair in PAIRS:
                for strand in pair_strands(de, labels, pair):
                    prediction, cut_data = ordered_surgery(de, labels, f, pair, strand)
                    if strand['ends']:
                        check_cut_sides(edges, faces, strand, cut_data)
                        counts['common_cut_order_checks'] += 1
                    selected = set(strand['edges'])
                    target = tuple(sum(pair) - x if j in selected else x for j, x in enumerate(labels))
                    assert all({target[e] for e, vs in enumerate(de) if v in vs} == {1, 2, 3} for v in range(f))
                    assert matching(de, target, pair, f) == matching(de, labels, pair, f)
                    assert tuple(sum(pair) - x if j in selected else x for j, x in enumerate(target)) == labels
                    integrate(n, edges, target)
                    counts['primal_integrations'] += 1
                    for p, expected in prediction.items():
                        assert matching(de, target, p, f) == expected
                        counts['mixed_updates'] += 1
                    counts['path_switches' if strand['ends'] else 'cycle_switches'] += 1
                    # Two specified complete colorings of the SAME induced-C5 disk.
                    if int(mask) == 701 and coloring in ((0, 1, 0, 2, 3, 1, 0, 3, 2), (0, 1, 0, 2, 3, 1, 2, 3, 3)) and pair == (2, 3) and strand['ends'] == [f + 2, f + 4]:
                        negative_records.append(dict(coloring=coloring, labels=labels,
                                                     before=before, after=boundary_state(de, target, f),
                                                     switched_labels=target, surgery=cut_data))
        row = dict(mask=int(mask), vertices=n, edges=edges, faces=faces, checks=dict(counts))
        if int(mask) == 701:
            negative_graph = dict(row, dual_edges=de)
        rows.append(row)
        totals.update(counts)
    assert len(rows) == 56 and len(negative_records) == 2
    x, y = negative_records
    assert x['coloring'][:5] == y['coloring'][:5] and x['before'] == y['before'] and x['after'] != y['after']
    r110 = record110_constraints()
    expected_before = tuple(tuple(map(tuple, p['matching'])) for p in r110['forced_matchings'])
    expected_after = tuple(tuple(map(tuple, p)) for p in r110['after_minority_23_switch'])
    assert x['before'] == expected_before
    assert x['after'] != expected_after and y['after'] == expected_after
    # Actual second dual path switch, without assuming a state transition.
    de, f = negative_graph['dual_edges'], len(negative_graph['faces'])
    second = next(s for s in pair_strands(de, x['switched_labels'], (1, 3)) if s['ends'] == [f, f + 1])
    final_labels = [4 - c if e in second['edges'] else c for e, c in enumerate(x['switched_labels'])]
    escape_coloring = integrate(negative_graph['vertices'], negative_graph['edges'], final_labels)
    boundary = escape_coloring[:5]
    assert boundary[0] == boundary[2] and boundary[1] == boundary[3] and len(set(boundary)) == 3
    # Parallel links must remain a closed component, not a single ordinary edge.
    assert strands([('t0', 't1'), ('t0', 't1')])[0]['ends'] == []
    inputs = [Path(__file__), CAT, ROOT / 'scripts/c5_kempe_connectivity.py',
              ROOT / 'scripts/c5_adjacent_singleton_counts.py', ROOT / 'scripts/c5_kempe_screen.py',
              ROOT / 'artifacts/c5_single_spoke_two_two/observations.json']
    return dict(evidence='Paper arbitrary-size surgery; finite replay and explicit state counterexample; not a record-110 exclusion.',
                source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in inputs},
                checks=dict(totals), existing_induced_triangulations=rows,
                boundary_state_counterexample=dict(graph=negative_graph, pair=[2, 3], ends=[2, 4], colorings=negative_records,
                                                   first_coloring_q_escape=dict(second_pair=[1, 3], second_ends=[0, 1],
                                                                               second_path_edges=second['edges'], coloring=escape_coloring)),
                record110=r110)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = report()
    encoded = json.dumps(data, indent=2, ensure_ascii=False) + '\n'
    if args.check:
        assert OUT.read_text() == encoded, 'Certificate mismatch; regenerate and review.'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(encoded)
    print('Dual path surgery:', json.dumps(data['checks'], sort_keys=True),
          '; 56 existing induced-C5 triangulations; same-graph boundary-state counterexample.')


if __name__ == '__main__':
    main()
