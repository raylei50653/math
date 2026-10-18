#!/usr/bin/env python3
"""Small graph controls, not enumeration of original research sources."""
import json
from itertools import product


def edge(u, v):
    return tuple(sorted((u, v)))


def fragments(vertices, edges):
    """All exact matching fragments; cut edges cover only their local end."""
    vertices = frozenset(vertices)
    incident = {v: [] for v in vertices}
    for e in edges:
        for v in set(e) & vertices:
            incident[v].append(e)

    def rec(uncovered, chosen):
        if not uncovered:
            yield frozenset(chosen)
            return
        v = min(uncovered)
        for e in sorted(incident[v]):
            covered = set(e) & vertices
            if covered <= uncovered:
                yield from rec(uncovered - covered, chosen + [e])

    return list(rec(set(vertices), []))


def components(edges, nodes=()):
    """Edges carry parity; return complete node and indexed-edge components."""
    adj = {v: [] for v in nodes}
    for i, (u, v, _) in enumerate(edges):
        adj.setdefault(u, []).append((v, i))
        adj.setdefault(v, []).append((u, i))
    unseen = set(adj)
    out = []
    while unseen:
        todo = [min(unseen, key=repr)]
        ns, es = set(), set()
        while todo:
            v = todo.pop()
            if v in ns:
                continue
            ns.add(v)
            for w, i in adj[v]:
                es.add(i)
                if w not in ns:
                    todo.append(w)
        unseen -= ns
        out.append((ns, es))
    return out


def summary(vertices, all_edges, matching, marks):
    vs = set(vertices)
    cut = {e for e in all_edges if len(set(e) & vs) == 1}
    selected = tuple(sorted(cut & matching))
    ce = []
    for e in all_edges:
        if e in matching:
            continue
        local = set(e) & vs
        if len(local) == 2:
            ce.append((e[0], e[1], 1))
        elif len(local) == 1:
            ce.append((next(iter(local)), ('port', e), 0))
    paths, odd = [], 0
    for ns, es in components(ce, vs):
        ports = sorted(v[1] for v in ns if isinstance(v, tuple))
        parity = sum(ce[i][2] for i in es) % 2
        if ports:
            assert len(ports) == 2
            paths.append((ports[0], ports[1], parity))
        else:
            odd += parity
    mu = tuple((e in matching) if set(e) & vs else None for e in marks)
    return (selected, tuple(sorted(paths)), mu), odd


def join_odd(left, right):
    assert left[0] == right[0]
    ce, ports = [], set()
    for side, s in enumerate((left, right)):
        for u, v, parity in s[1]:
            ce.append(((side, u), (side, v), parity))
            ports.update((u, v))
    for b in ports:
        ce.append(((0, b), (1, b), 1))
    return sum(sum(ce[i][2] for i in es) % 2 for _, es in components(ce))


def global_odd(vertices, edges, matching):
    ce = [(u, v, 1) for u, v in edges if (u, v) not in matching]
    return sum(len(es) % 2 for _, es in components(ce, vertices))


def joint(matching, marks):
    e, f, g = marks
    return e in matching and ((f in matching) != (g in matching))


def check_graph(name, vertices, edges, left_vertices):
    edges = sorted({edge(*e) for e in edges})
    vertices = set(vertices)
    assert all(sum(v in e for e in edges) == 3 for v in vertices)
    left_vertices = set(left_vertices)
    right_vertices = vertices - left_vertices
    whole = fragments(vertices, edges)
    # Pick literal marks with a nonempty joint family in each control.
    first_matching = sorted(whole[0])
    marks = (first_matching[0], first_matching[1],
             next(e for e in edges if e not in whole[0]))
    left = [(m, *summary(left_vertices, edges, m, marks))
            for m in fragments(left_vertices, edges)]
    right = [(m, *summary(right_vertices, edges, m, marks))
             for m in fragments(right_vertices, edges)]
    joined, all_pairs, joint_values = [], 0, []
    left_table, right_table = {}, {}
    for _, s, c in left:
        left_table[s] = min(left_table.get(s, float('inf')), c)
    for _, t, c in right:
        right_table[t] = min(right_table.get(t, float('inf')), c)
    for (m, s, c), (n, t, d) in product(left, right):
        if s[0] != t[0]:
            continue
        both = m | n
        value = c + d + join_odd(s, t)
        assert value == global_odd(vertices, edges, both)
        assert all(sum(v in e for e in both) == 1 for v in vertices)
        joined.append(both)
        all_pairs += 1
        if joint(both, marks):
            joint_values.append(value)
    assert len(joined) == len(set(joined))
    assert set(joined) == set(whole)
    compressed = []
    for s, t in product(left_table, right_table):
        if s[0] != t[0]:
            continue
        mu = []
        for a, b in zip(s[2], t[2]):
            if a is not None and b is not None:
                assert a == b
            mu.append(a if a is not None else b)
        if mu[0] and (mu[1] != mu[2]):
            compressed.append(left_table[s] + right_table[t] + join_odd(s, t))
    assert min(compressed, default=None) == min(joint_values, default=None)
    assert min(joint_values, default=None) == min(
        (global_odd(vertices, edges, m) for m in whole if joint(m, marks)),
        default=None)
    return {'name': name, 'ports': sum(len(set(e) & left_vertices) == 1 for e in edges),
            'left_fragments': len(left), 'right_fragments': len(right),
            'compatible_pairs': all_pairs, 'whole_perfect_matchings': len(whole),
            'joint_minimum': min(joint_values, default=None)}


def signed(pairing, parities):
    return ((), tuple((u, v, p) for (u, v), p in zip(pairing, parities)), ())


def ladder_fragment(rungs):
    """Realize two paths in cyclic port order 0,1,2,3."""
    n = 2 * rungs
    vertices = set(range(n))
    rows = [edge(i, i + 1) for i in range(rungs - 1)]
    rows += [edge(i + rungs, i + rungs + 1) for i in range(rungs - 1)]
    matching = frozenset(edge(i, i + rungs) for i in range(rungs))
    boundary_vertices = (0, rungs - 1, n - 1, rungs)
    terminals = {edge(v, n + j): j for j, v in enumerate(boundary_vertices)}
    edges = rows + list(matching) + list(terminals)
    assert all(sum(v in e for e in edges) == 3 for v in vertices)
    s, c = summary(vertices, edges, matching, ())
    assert s[0] == () and c == 0
    paths = []
    for u, v, parity in s[1]:
        a, b = sorted((terminals[u], terminals[v]))
        paths.append((a, b, parity))
    return ((), tuple(sorted(paths)), ())


def negative_controls():
    same = ((0, 1), (2, 3))
    other = ((0, 3), (1, 2))
    exterior = signed(same, (1, 1))
    odd_paths = signed(same, (1, 1))
    even_paths = signed(same, (0, 0))
    alternate_pairing = signed(other, (0, 0))
    assert ladder_fragment(2) == odd_paths
    assert ladder_fragment(3) == even_paths
    assert join_odd(odd_paths, exterior) == 0
    assert join_odd(even_paths, exterior) == 2
    assert join_odd(alternate_pairing, exterior) == 0
    prism = sorted([edge(0, 1), edge(1, 2), edge(2, 0), edge(3, 4),
                    edge(4, 5), edge(5, 3), edge(0, 3), edge(1, 4), edge(2, 5)])
    rungs = {edge(0, 3), edge(1, 4), edge(2, 5)}
    twice = prism + [edge(u + 6, v + 6) for u, v in prism]
    two_rungs = rungs | {edge(u + 6, v + 6) for u, v in rungs}
    assert global_odd(range(6), prism, rungs) == 2
    assert global_odd(range(12), twice, two_rungs) == 4
    # A zero-length complementary path occurs on the singleton K4 piece.
    k4 = [edge(u, v) for u in range(4) for v in range(u + 1, 4)]
    state, cost = summary({0}, k4, frozenset({edge(0, 1)}), ())
    assert cost == 0 and len(state[1]) == 1 and state[1][0][2] == 0
    # Wrong dominance direction: the old prism with this fixed rung fibre
    # is bad (cost 2), the proposed smaller K4 fixed matching is good (0).
    k4_matching = frozenset({edge(0, 1), edge(2, 3)})
    assert global_odd(range(4), k4, k4_matching) == 0
    return {'forget_path_parity': [0, 2], 'forget_pairing': [2, 0],
            'replace_odd_count_by_bit': [2, 4], 'zero_length_path': 'checked',
            'ladder_path_realizations': [2, 3],
            'wrong_dominance_direction_fixed_fibres': {'old': 2, 'smaller': 0}}


def main():
    k4 = [edge(u, v) for u in range(4) for v in range(u + 1, 4)]
    prism = [edge(i, (i + 1) % 3) for i in range(3)]
    prism += [edge(i + 3, (i + 1) % 3 + 3) for i in range(3)]
    prism += [edge(i, i + 3) for i in range(3)]
    petersen = [edge(i, (i + 1) % 5) for i in range(5)]
    petersen += [edge(i + 5, (i + 2) % 5 + 5) for i in range(5)]
    petersen += [edge(i, i + 5) for i in range(5)]
    result = {'scope': 'fixed graph controls; original source not triggered',
              'graphs': [check_graph('K4 singleton', range(4), k4, {0}),
                         check_graph('K4 two vertices', range(4), k4, {0, 1}),
                         check_graph('triangular prism', range(6), prism, {0, 1, 2}),
                         check_graph('Petersen outer cycle', range(10), petersen, range(5))],
              'negative_controls': negative_controls()}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
