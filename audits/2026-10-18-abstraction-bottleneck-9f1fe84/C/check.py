#!/usr/bin/env python3
"""Finite controls for the proved marked-region theorem; no source authority."""
from itertools import combinations
import json


def edge(a, b):
    return tuple(sorted((a, b)))


def components(n, edges):
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    unseen = set(range(n))
    out = []
    while unseen:
        stack = [min(unseen)]
        seen = set(stack)
        while stack:
            for v in adj[stack.pop()]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        unseen -= seen
        out.append(frozenset(seen))
    return out


def validate(n, edges):
    assert len(edges) * 2 == 3 * n
    assert all(a < b for a, b in edges)
    assert all(sum(v in e for e in edges) == 3 for v in range(n))
    assert len(components(n, edges)) == 1


def matchings(n, edges):
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    def recur(left, chosen):
        if not left:
            yield frozenset(chosen)
            return
        a = min(left)
        for b in sorted(adj[a] & left):
            yield from recur(left - {a, b}, chosen + [edge(a, b)])
    return list(recur(set(range(n)), []))


def oddness(n, edges, matching):
    assert len(matching) * 2 == n
    assert all(sum(v in e for e in matching) == 1 for v in range(n))
    return sum(len(c) % 2 for c in components(n, edges - matching))


def rank(vectors):
    basis = {}
    for v in vectors:
        while v:
            p = v.bit_length() - 1
            if p in basis:
                v ^= basis[p]
            else:
                basis[p] = v
                break
    return len(basis)


def xor(vectors):
    out = 0
    for v in vectors:
        out ^= v
    return out


def triangle_expand(base_n, base_edges):
    # Each base incidence is a vertex. Old matching consists of external edges.
    incidences = sorted((v, w) for a, b in base_edges for v, w in [(a, b), (b, a)])
    idx = {p: i for i, p in enumerate(incidences)}
    edges = {edge(idx[a, b], idx[b, a]) for a, b in base_edges}
    external = set(edges)
    for v in range(base_n):
        ports = [idx[p] for p in incidences if p[0] == v]
        assert len(ports) == 3
        edges |= {edge(a, b) for a, b in combinations(ports, 2)}
    return 3 * base_n, edges, external, idx


def cycle_control(k):
    # The base is an even Hamiltonian cycle plus a disjoint opposite matching.
    n = 2 * k
    cyc = {edge(v, (v + 1) % n) for v in range(n)}
    rung = {edge(v, v + k) for v in range(k)}
    assert not cyc & rung
    big_n, edges, old, idx = triangle_expand(n, cyc | rung)
    ref = {edge(idx[a, b], idx[b, a]) for a, b in rung}
    for v in range(n):
        cyc_ports = [idx[v, w] for w in [(v - 1) % n, (v + 1) % n]]
        ref.add(edge(*cyc_ports))
    return big_n, edges, frozenset(old), frozenset(ref), idx


def region_data(n, edges, old, ref, columns):
    out = []
    for region in components(n, edges - (old & ref)):
        diff = frozenset(e for e in old ^ ref if e[0] in region)
        assert all((a in region) == (b in region) for a, b in old ^ ref)
        cycles = [c for c in components(n, edges - old) if c <= region]
        gain = sum(len(c) % 2 for c in cycles)
        assert gain % 2 == 0
        syndrome = xor(columns.get(e, 0) for e in diff)
        out.append((region, diff, gain, syndrome))
    return out


def audit_graph(n, edges, columns):
    validate(n, edges)
    pms = matchings(n, edges)
    refs = [r for r in pms if oddness(n, edges, r) == 0]
    pair_count = batch_count = 0
    for old in pms:
        old_odd = oddness(n, edges, old)
        for ref in refs:
            data = region_data(n, edges, old, ref, columns)
            zero = [s for _, _, q, s in data if q == 0]
            pos = [s for _, _, q, s in data if q > 0]
            no_safe_positive = True
            for mask in range(1 << len(data)):
                chosen = [data[i] for i in range(len(data)) if mask >> i & 1]
                diff = frozenset().union(*(t for _, t, _, _ in chosen))
                new = old ^ diff
                gain = sum(q for _, _, q, _ in chosen)
                syn = xor(s for _, _, _, s in chosen)
                assert oddness(n, edges, new) == old_odd - gain
                assert syn == xor(columns.get(e, 0) for e in old ^ new)
                if syn == 0 and gain > 0:
                    no_safe_positive = False
                batch_count += 1
            independent = rank(zero + pos) == rank(zero) + len(pos)
            assert no_safe_positive == independent
            pair_count += 1
    return {"vertices": n, "perfect_matchings": len(pms),
            "even_references": len(refs), "pairs": pair_count,
            "full_region_batches": batch_count}


def sharp_rank_two():
    # Two expanded K4s are joined across a common old/reference matching edge.
    n, e0, old0, ref0, idx = cycle_control(2)
    def shift(edges):
        return {edge(a + n, b + n) for a, b in edges}
    shared = edge(idx[0, 2], idx[2, 0])
    a, b = shared
    cross = {edge(a, a + n), edge(b, b + n)}
    edges = (e0 | shift(e0)) - {shared, edge(a + n, b + n)} | cross
    ref = (set(ref0) | shift(ref0)) - {shared, edge(a + n, b + n)} | cross
    g = edge(a, a + n)
    f0 = edge(idx[0, 1], idx[0, 3])
    f1 = edge(f0[0] + n, f0[1] + n)
    # Constraints are f0 XOR g = 1 and f1 XOR g = 1.
    columns = {f0: 1, f1: 2, g: 3}
    pms = matchings(2 * n, edges)
    family = [m for m in pms if xor(columns.get(e, 0) for e in m) == 3]
    best = min(oddness(2 * n, edges, m) for m in family)
    assert best == 4
    old = next(m for m in family if oddness(2 * n, edges, m) == best)
    data = region_data(2 * n, edges, old, frozenset(ref), columns)
    pos = [(q, s) for _, _, q, s in data if q]
    assert sorted(pos) == [(2, 1), (2, 2)]
    validate(2 * n, edges)
    assert oddness(2 * n, edges, frozenset(ref)) == 0
    return {"vertices": 2 * n, "perfect_matchings": len(pms),
            "family_size": len(family), "global_minimum_oddness": best,
            "positive_region_gain_syndrome": pos,
            "edges": sorted(edges), "old": sorted(old), "reference": sorted(ref),
            "column_edges": [[list(e), s] for e, s in sorted(columns.items())]}


def main():
    n, edges, old, ref, idx = cycle_control(2)
    chosen = sorted(edges)[:4]
    report = {"authority": "finite graph controls only; no source realizability",
              "rank_two_all_pair_replay": audit_graph(n, edges, {e: s for e, s in zip(chosen, [1, 2, 3, 1])}),
              "sharp_rank_two": sharp_rank_two(), "concentration": []}
    for k in [2, 3, 4, 8, 16]:
        n, edges, old, ref, idx = cycle_control(k)
        validate(n, edges)
        assert oddness(n, edges, old) == 2 * k
        assert oddness(n, edges, ref) == 0
        data = region_data(n, edges, old, ref, {})
        assert len(data) == 1 and data[0][2] == 2 * k
        report["concentration"].append({"vertices": n, "odd_cycles": 2 * k, "regions": 1})
    # Negative control: parity fails for an odd-complement reference R=M.
    n, edges, old, _, _ = cycle_control(2)
    malformed = False
    try:
        region_data(n, edges, old, old, {})
    except AssertionError:
        malformed = True
    assert malformed
    report["odd_reference_premise_rejection"] = "PASS"
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
