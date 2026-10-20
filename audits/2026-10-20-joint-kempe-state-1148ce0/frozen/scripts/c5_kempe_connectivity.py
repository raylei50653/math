#!/usr/bin/env python3
"""Exact connectivity surgery and existing-witness replay; no graph search.

python3 scripts/c5_kempe_connectivity.py [--check]
General surgery and disk gate soundness are paper proofs, not Lean proofs.
"""
import argparse
from collections import deque
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from c5_adjacent_singleton_counts import CAT, CYCLE, REPS, THREE

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_cells/kempe_connectivity.json'
PAIRS = tuple(combinations(range(4), 2))


def adjacency(n, edges):
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return adj


def components(adj, vertices):
    unseen = set(vertices)
    answer = []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        queue = [root]
        for u in queue:
            for v in sorted(adj[u] & unseen):
                unseen.remove(v)
                queue.append(v)
        answer.append(frozenset(queue))
    return frozenset(answer)


def pair_components(adj, c, pair):
    return components(adj, (v for v, color in enumerate(c) if color in pair))


def component(adj, c, pair, root):
    return next(s for s in pair_components(adj, c, pair) if root in s)


def swap(c, s, pair):
    return tuple(sum(pair) - color if v in s else color
                 for v, color in enumerate(c))


def surgery(adj, c, s, old, new, spectator):
    """Predict post-swap {old,spectator} components without reading new colors.

    Delete old-colored vertices in S, contract residual components, and attach
    each new-colored vertex in S as a separate star. Lift connectivity back.
    """
    residual = {v for v, color in enumerate(c)
                if color == spectator or (color == old and v not in s)}
    blocks = sorted(components(adj, residual), key=lambda block: min(block))
    inserted = sorted(v for v in s if c[v] == new)
    blocks += [frozenset([v]) for v in inserted]
    owner = {v: j for j, block in enumerate(blocks) for v in block}
    quotient = [set() for _ in blocks]
    for v in inserted:
        for w in adj[v] & residual:
            assert c[w] == spectator
            a, b = owner[v], owner[w]
            quotient[a].add(b)
            quotient[b].add(a)
    return frozenset(frozenset().union(*(blocks[j] for j in group))
                     for group in components(quotient, range(len(blocks))))


def colorings(k, edges):
    for b in REPS:
        for inner in product(range(4), repeat=k):
            c = b + inner
            if all(c[u] != c[v] for u, v in edges):
                yield c


def escape(adj, start):
    """Shortest actual-component route to a singleton outside {0,2}."""
    queue = deque([start])
    previous = {start: None}
    moves = {}
    while queue:
        c = queue.popleft()
        b = c[:5]
        if len(set(b)) == 3:
            singleton = next(i for i in range(5) if b.count(b[i]) == 1)
            if singleton not in (0, 2):
                path = []
                while previous[c] is not None:
                    path.append(dict(**moves[c], coloring=c))
                    c = previous[c]
                return dict(singleton=singleton, moves=list(reversed(path)))
        for pair in PAIRS:
            for s in sorted(pair_components(adj, c, pair), key=lambda s: min(s)):
                target = swap(c, s, pair)
                if target not in previous:
                    previous[target] = c
                    moves[target] = dict(pair=pair, component=sorted(s))
                    queue.append(target)
    return None


def report():
    catalog = json.loads(CAT.read_text())
    rows = []
    gates = []
    counts = dict(initial_fibre=0, both_initial_blockers=0,
                  left_new_link=0, right_new_link=0, both_new_links=0)
    for mask, entry in sorted(catalog['cells'].items(), key=lambda p: int(p[0])):
        edges = sorted({tuple(sorted(e)) for e in (*CYCLE, *entry['edges'])})
        adj = adjacency(5 + entry['k_eff'], edges)
        row = dict(mask=int(mask), colorings=0, swaps=0, mixed_checks=0)
        for c in colorings(entry['k_eff'], edges):
            row['colorings'] += 1
            before = {p: pair_components(adj, c, p) for p in PAIRS}
            for pair in PAIRS:
                other = tuple(v for v in range(4) if v not in pair)
                for s in sorted(before[pair], key=lambda s: min(s)):
                    target = swap(c, s, pair)
                    assert all(target[u] != target[v] for u, v in edges)
                    assert pair_components(adj, target, pair) == before[pair]
                    assert pair_components(adj, target, other) == before[other]
                    for old, new in (pair, pair[::-1]):
                        for spectator in other:
                            expected = surgery(adj, c, s, old, new, spectator)
                            assert expected == pair_components(adj, target, (old, spectator))
                            row['mixed_checks'] += 1
                    row['swaps'] += 1
            if c[:5] != (0, 1, 0, 2, 3):
                continue
            counts['initial_fibre'] += 1
            if (3 not in component(adj, c, (1, 2), 1)
                    or 4 not in component(adj, c, (1, 3), 1)):
                continue
            counts['both_initial_blockers'] += 1
            s = component(adj, c, (0, 2), 0)
            t = component(adj, c, (0, 3), 2)
            # Disk separation is a paper theorem; test its consequence on witnesses.
            assert s & set(range(5)) == {0}
            assert t & set(range(5)) == {2}
            cs, ct = swap(c, s, (0, 2)), swap(c, t, (0, 3))
            left = 4 in component(adj, cs, (0, 3), 2)
            right = 3 in component(adj, ct, (0, 2), 0)
            interface = sorted((u, v) for u in s if c[u] == 2
                               for v in adj[u] & t if c[v] == 3)
            if left or right:
                assert interface, 'A newly created linkage must exit via a C-D edge.'
            if not left:
                end = swap(cs, component(adj, cs, (0, 3), 2), (0, 3))
                assert end[:5] == (2, 1, 3, 2, 3)
                assert all(end[u] != end[v] for u, v in edges)
            if not right:
                end = swap(ct, component(adj, ct, (0, 2), 0), (0, 2))
                assert end[:5] == (2, 1, 3, 2, 3)
                assert all(end[u] != end[v] for u, v in edges)
            counts['left_new_link'] += left
            counts['right_new_link'] += right
            if left and right:
                counts['both_new_links'] += 1
                route = escape(adj, c)
                assert route is not None
                gates.append(dict(mask=int(mask), edges=edges, coloring=c,
                                  S=sorted(s), T=sorted(t), interface=interface,
                                  S_T_disjoint=not bool(s & t),
                                  T_after_S=sorted(component(adj, cs, (0, 3), 2)),
                                  S_after_T=sorted(component(adj, ct, (0, 2), 0)),
                                  singleton_support=sorted(i for i, j in THREE.items()
                                                           if int(mask) >> j & 1),
                                  shortest_escape=route))
        rows.append(row)
    # A-D-A cut: contracting the original component before deletion is unsound.
    adj = adjacency(3, [(0, 1), (1, 2)])
    c, s = (3, 0, 3), frozenset([1])
    assert component(adj, c, (0, 3), 0) == {0, 1, 2}
    target = swap(c, s, (0, 2))
    assert component(adj, target, (0, 3), 0) == {0}
    assert surgery(adj, c, s, 0, 2, 3) == pair_components(adj, target, (0, 3))
    assert len(gates) == 1 and gates[0]['mask'] == 935
    gate = gates[0]
    assert gate['S_T_disjoint'] and gate['T_after_S'] != gate['T']
    assert len(gate['shortest_escape']['moves']) == 2
    # Explicit oriented triangulated disk certificate for this fixed control.
    faces = [(0, 1, 6), (1, 2, 7), (2, 3, 7), (3, 4, 5), (4, 0, 6),
             (1, 7, 6), (3, 5, 7), (4, 6, 5), (5, 6, 7)]
    directed = [(face[i], face[(i + 1) % 3]) for face in faces for i in range(3)]
    assert len(directed) == len(set(directed))
    assert {tuple(sorted(e)) for e in directed} == set(gate['edges'])
    assert {e for e in directed if e[::-1] not in directed} == set(CYCLE)
    assert 8 - len(gate['edges']) + len(faces) == 1
    for v in range(8):
        link_edges = [tuple(u for u in face if u != v) for face in faces if v in face]
        link = adjacency(8, link_edges)
        active = {u for e in link_edges for u in e}
        assert len(components(link, active)) == 1
        degrees = sorted(len(link[u]) for u in active)
        assert degrees == ([1, 1] + [2] * (len(active) - 2) if v < 5
                           else [2] * len(active))
    gate['oriented_disk_faces'] = faces
    files = [Path(__file__), CAT, ROOT / 'scripts/c5_adjacent_singleton_counts.py',
             ROOT / 'scripts/c5_kempe_screen.py']
    return dict(trust='Paper surgery and disk-gate lemmas; exact replay of existing witnesses. Not Lean, not a realizability proof, no new graph catalogue search.',
                hashes={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                        for p in files}, witness_replay=rows, gate_counts=counts,
                local_gate_controls=gates,
                negative_controls=dict(delete_before_contract=True,
                                       disjoint_supports_do_not_preserve_components=True))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = report()
    encoded = json.dumps(result, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == encoded, 'Certificate differs; inspect before regeneration.'
    else:
        OUT.write_text(encoded)
    print(json.dumps(dict(witnesses=len(result['witness_replay']),
                          totals={key: sum(r[key] for r in result['witness_replay'])
                                  for key in ('colorings', 'swaps', 'mixed_checks')},
                          gate_counts=result['gate_counts']), sort_keys=True))


if __name__ == '__main__':
    main()
