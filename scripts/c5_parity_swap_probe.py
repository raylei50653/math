"""Exploratory probe for docs/tasks/c5_parity_relaxation_tasks.md (not frozen evidence).

python3 scripts/c5_parity_swap_probe.py [seed] [graphs]

Parity-free exposability and single alternating-swap repair.

Networks: duals of random C5 near-triangulations (leaves t0..t4 for e0..e4).
PM(ij)  : perfect matchings of Q - t_i - t_j (no parity condition).
GOOD(ij): those whose complement cycles are all even (= M_ij of (M)).
Questions:
 Q1 is PM(ij) nonempty for all 10 pairs?
 Q2 one-swap: for alpha in GOOD(14), gamma in GOOD(02) or GOOD(03), does some
    alpha xor (P u S) with P a path of alpha^gamma at t1/t4 and S a subset of
    its cycles land in GOOD(target), target in {23,01,04}?
"""
import importlib.util, random, sys, itertools
from collections import Counter
from pathlib import Path
spec = importlib.util.spec_from_file_location("m", Path(__file__).resolve().parent / "c5_equivalent_forms_check.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

TARGETS = [frozenset(p) for p in ((2, 3), (0, 1), (0, 4))]


def network(faces):
    fid = {f: j for j, f in enumerate(faces)}
    edges = []
    for e in m.edges_of(faces):
        inc = [fid[f] for f in faces if e[0] in f and e[1] in f]
        if len(inc) == 2:
            edges.append((inc[0], inc[1]))
        else:
            i = e[0] if (e[0] + 1) % 5 == e[1] else e[1]
            edges.append((inc[0], ('t', i)))
    return len(faces), edges


def all_pms(n, edges, exposed):
    verts = list(range(n)) + [('t', i) for i in range(5) if i not in exposed]
    out = []

    def go(cov, chosen):
        free = [v for v in verts if v not in cov]
        if not free:
            out.append(frozenset(chosen)); return
        v = free[0]
        for k, (a, b) in enumerate(edges):
            if v in (a, b):
                w = b if a == v else a
                if w in verts and w not in cov:
                    go(cov | {v, w}, chosen | {k})
    go(frozenset(), frozenset())
    return out


def exposed_of(M, edges):
    hit = {edges[k][1][1] for k in M if isinstance(edges[k][1], tuple)}
    return frozenset(i for i in range(5) if i not in hit)


def odd_cycles(M, n, edges):
    adj = {}
    for k, (a, b) in enumerate(edges):
        if k in M: continue
        adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
    seen, odd = set(), 0
    for s in range(n):
        if s in seen: continue
        comp, st = set(), [s]
        while st:
            v = st.pop()
            if v in comp: continue
            comp.add(v); st += adj.get(v, [])
        seen |= comp
        if any(isinstance(v, tuple) for v in comp): continue
        odd += len([v for v in comp if not isinstance(v, tuple)]) % 2
    return odd


def components(edge_ids, edges):
    adj = {}
    for k in edge_ids:
        a, b = edges[k]
        adj.setdefault(a, []).append((b, k)); adj.setdefault(b, []).append((a, k))
    seen, comps = set(), []
    for s in adj:
        if s in seen: continue
        vs, ks, st = set(), set(), [s]
        while st:
            v = st.pop()
            if v in vs: continue
            vs.add(v)
            for w, k in adj[v]:
                ks.add(k); st.append(w)
        seen |= vs; comps.append((vs, frozenset(ks)))
    return comps


def main():
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 5)
    stats = Counter()
    for _ in range(int(sys.argv[2]) if len(sys.argv) > 2 else 200):
        nv, faces = m.random_near_triangulation(rng, rng.randrange(2, 12))
        n, edges = network(faces)
        pm = {frozenset(p): all_pms(n, edges, set(p)) for p in itertools.combinations(range(5), 2)}
        good = {p: [M for M in L if odd_cycles(M, n, edges) == 0] for p, L in pm.items()}
        stats['graphs'] += 1
        stats['pm_full'] += all(pm.values())
        stats['good_full'] += all(good.values())
        if pm[frozenset((1, 4))] and (pm[frozenset((0, 2))] or pm[frozenset((0, 3))]):
            stats['pf_lemma_triggered'] += 1
            stats['pf_lemma_holds'] += any(pm[t] for t in TARGETS)
        A = good[frozenset((1, 4))]
        G = good[frozenset((0, 2))] + good[frozenset((0, 3))]
        if not A or not G: continue
        stats['pairs_tested'] += len(A) * len(G)
        stats['graphs_with_AG'] += 1
        graph_ok = False
        for alpha in A:
            ok_alpha = False
            for gamma in G:
                diff = alpha ^ gamma
                comps = components(diff, edges)
                paths = [ks for vs, ks in comps if any(isinstance(v, tuple) for v in vs)]
                cycles = [ks for vs, ks in comps if not any(isinstance(v, tuple) for v in vs)]
                ok_path_only = ok_any = False
                for P in paths:
                    for r in range(len(cycles) + 1):
                        for S in itertools.combinations(cycles, r):
                            N = alpha ^ P
                            for c in S: N = N ^ c
                            if exposed_of(N, edges) in TARGETS and odd_cycles(N, n, edges) == 0:
                                ok_any = True
                                if r == 0: ok_path_only = True
                stats['swap_any_ok'] += ok_any
                stats['swap_path_only_ok'] += ok_path_only
                ok_alpha |= ok_any
            stats['alpha_total'] += 1
            stats['alpha_some_gamma_ok'] += ok_alpha
            graph_ok |= ok_alpha
        stats['graphs_some_alpha_ok'] += graph_ok
        if not graph_ok:
            stats['one_swap_failures'] += 1
            stats['failures_with_good_target'] += any(good[t] for t in TARGETS)
    print(dict(stats))


main()
