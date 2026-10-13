#!/usr/bin/env python3
"""Independent finite check of annulus chi 3 -> 4, not colouring counts."""
import json


def edge(a, b):
    return tuple(sorted((a, b)))


def count_three(vertices, edges):
    adj = {v: set() for v in vertices}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    colors = {0: 0}
    total = 0

    def dfs():
        nonlocal total
        if len(colors) == len(vertices):
            total += 1
            return
        v = max((v for v in vertices if v not in colors),
                key=lambda v: (len({colors[w] for w in adj[v] if w in colors}), len(adj[v]), v))
        blocked = {colors[w] for w in adj[v] if w in colors}
        for c in range(3):
            if c not in blocked:
                colors[v] = c
                dfs()
                del colors[v]

    dfs()
    return total


def main():
    prism = {edge(i, (i + 1) % 5) for i in range(5)}
    prism |= {edge(5 + i, 5 + (i + 1) % 5) for i in range(5)}
    prism |= {edge(i, 5 + i) for i in range(5)}
    source = prism | {edge(10, v) for v in (0, 1, 6)}
    target = prism | {edge(i, 5 + (i + 1) % 5) for i in range(5)}
    three_source = tuple(map(int, '01012201012'))
    four_target = tuple(map(int, '0101212323'))
    assert set(three_source) == {0, 1, 2}
    assert all(three_source[a] != three_source[b] for a, b in source)
    assert set(four_target) == {0, 1, 2, 3}
    assert all(four_target[a] != four_target[b] for a, b in target)
    ns, nt = count_three(list(range(11)), source), count_three(list(range(10)), target)
    assert ns > 0 and nt == 0
    print(json.dumps({'status': 'PASS', 'source': {'chi': 3, 'literal_witness': list(three_source),
          'three_colorings_with_b0_fixed_0': ns},
          'target': {'chi': 4, 'literal_witness': list(four_target),
          'three_colorings_with_b0_fixed_0': nt},
          'capped_complete_Sigma': '1023 on both sides by the all-m prism proof',
          'source_minimality': 'not triggered'}, indent=2))


if __name__ == '__main__':
    main()
