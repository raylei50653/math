#!/usr/bin/env python3
"""Independent cross-check of the reduced C5 cell enumeration (K_6 = K_5) along a different search path.

uv run --with rustworkx==0.17.1 python scripts/c5_k6_crosscheck.py --k 5 --sym none --order attach_first
uv run --with rustworkx==0.17.1 --with networkx==3.5 python scripts/c5_k6_crosscheck.py --k 6 --sym count \
    --order within_first --jobs 30 --nx-verify --out artifacts/c5_cells/k6_independent_crosscheck.json

Same universe as c5_cell_reduced.py (ordered C5, k private interior vertices, chords allowed, apex-planar),
but nothing of the production DFS is reused: the edge order, the prefix split, the viability test and the
Σ evaluator are written here from scratch.  Σ is computed by plain backtracking over the interior colours
of each of the ten boundary patterns (no bitset compatibility tables).

Pruning is configurable so that the search path differs from production while staying lossless:

  R1  (always) every interior vertex ends with degree >= 4        -- same lemma as production
  --sym none          no relabelling canonicalisation at all (every labelled graph is visited)
  --sym count         attachment *counts* of x_1..x_k non-increasing   (coarser than production)
  --sym nonincreasing attachment masks non-increasing                 (production's condition)
  --sym nondecreasing attachment masks non-decreasing                 (mirror image of production)

Each of these is intersected by every relabelling orbit (sort the vertices by the key), so the survivors'
Σ still cover every new Σ at level k.  --order changes the position of each edge in the DFS:

  production    chords, then per vertex: five attachments, then edges to earlier interior vertices
  within_first  chords, then per vertex: edges to earlier interior vertices, then five attachments
  attach_first  chords, then all attachments (vertex by vertex), then all interior-interior edges
  reversed      production order with the interior vertices' blocks in reverse and attachments 4..0

The check reported is: the set of distinct Σ of the survivors, compared with the exact catalogue K_5
(artifacts/c5_cells/cells.json).  `new_vs_K5 == []` reproduces K_k = K_5 along this search path.
--nx-verify re-tests every Σ witness's apex-planarity with NetworkX (independent of the rustworkx test
used inside the DFS) and recomputes its Σ a second time from the edge list.

--from-cpp FILE skips the Python DFS and ingests the output of scripts/cpp/c5_crosscheck.cpp (the same
search in C++ with Boost's Boyer–Myrvold planarity test and std::thread), then performs the same K_5
comparison and witness re-verification and writes the artifact with provenance (commit, source hashes).
The C++ binary reproduces the Python DFS exactly (nodes, survivors, Σ counts) for k <= 5.
"""
import argparse
import hashlib
import itertools
import json
from multiprocessing import Pool
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
CELLS = ROOT / 'artifacts/c5_cells/cells.json'
CYCLE = tuple((i, (i + 1) % 5) for i in range(5))
CHORDS = ((0, 2), (0, 3), (1, 3), (1, 4), (2, 4))


def normalize(pattern):
    names = {}
    return tuple(names.setdefault(c, len(names)) for c in pattern)


REPS = tuple(sorted({normalize(b) for b in itertools.product(range(4), repeat=5)
                     if all(b[i] != b[(i + 1) % 5] for i in range(5))}))
assert len(REPS) == 10


# ---------------------------------------------------------------- edge orders

def edge_order(k, order):
    inner = [5 + m for m in range(k)]
    if order == 'production':
        return tuple(CHORDS) + tuple(e for m in range(k) for e in
                                     [(i, inner[m]) for i in range(5)] + [(inner[l], inner[m]) for l in range(m)])
    if order == 'within_first':
        return tuple(CHORDS) + tuple(e for m in range(k) for e in
                                     [(inner[l], inner[m]) for l in range(m)] + [(i, inner[m]) for i in range(5)])
    if order == 'attach_first':
        return (tuple(CHORDS) + tuple((i, inner[m]) for m in range(k) for i in range(5))
                + tuple((inner[l], inner[m]) for m in range(k) for l in range(m)))
    if order == 'reversed':
        return tuple(CHORDS) + tuple(e for m in reversed(range(k)) for e in
                                     [(i, inner[m]) for i in (4, 3, 2, 1, 0)] + [(inner[m], inner[l]) for l in range(m + 1, k)])
    raise ValueError(order)


# ---------------------------------------------------------------- worker state and viability

_W = {}


def _setup(k, order, sym):
    import rustworkx as rx
    edges = edge_order(k, order)
    E = len(edges)
    touch = [sum(1 << j for j, (u, v) in enumerate(edges) if 5 + m in (u, v)) for m in range(k)]
    attpos = [[next(j for j, e in enumerate(edges) if e in ((i, 5 + m), (5 + m, i))) for i in range(5)] for m in range(k)]
    attmask = [sum(1 << j for j in attpos[m]) for m in range(k)]
    graph = rx.PyGraph(multigraph=False)
    graph.add_nodes_from(range(5 + k + 1))
    graph.add_edges_from_no_data(list(CYCLE) + [(5 + k, i) for i in range(5)])
    adj = [[] for _ in range(5 + k)]
    _W.update(k=k, edges=edges, E=E, touch=touch, attpos=attpos, attmask=attmask, sym=sym, graph=graph, rx=rx)


def popcount(x):
    return bin(x).count('1')


def att_bounds(mask, e, m):
    """(lower, upper) for the attachment value / count of x_m given bits < e are final."""
    attpos = _W['attpos'][m]
    lo = sum(1 << i for i, j in enumerate(attpos) if j < e and mask >> j & 1)
    hi = lo | sum(1 << i for i, j in enumerate(attpos) if j >= e)
    return lo, hi


def viable(mask, e):
    """Can some continuation deciding only bits >= e satisfy R1 and the chosen SYM condition?"""
    k, touch, sym = _W['k'], _W['touch'], _W['sym']
    undecided_all = ~((1 << e) - 1)
    for m in range(k):
        if popcount(mask & touch[m]) + popcount(touch[m] & undecided_all) < 4:
            return False
    if sym == 'none':
        return True
    for m in range(1, k):
        lo1, hi1 = att_bounds(mask, e, m - 1)
        lo2, hi2 = att_bounds(mask, e, m)
        if sym == 'count':
            if popcount(lo2) > popcount(hi1):
                return False
        elif sym == 'nonincreasing':
            if lo2 > hi1:
                return False
        elif sym == 'nondecreasing':
            if hi2 < lo1:
                return False
        else:
            raise ValueError(sym)
    return True


# ---------------------------------------------------------------- independent Σ evaluator

def adjacency(k, edge_list):
    adj = [set() for _ in range(5 + k)]
    for u, v in list(CYCLE) + list(edge_list):
        adj[u].add(v)
        adj[v].add(u)
    return adj


def sigma_backtrack(k, adj):
    """Ten-bit Σ: pattern j is set iff REPS[j] on the boundary extends to a proper 4-colouring of the interior."""
    order = sorted(range(5, 5 + k), key=lambda v: -len(adj[v]))
    bits = 0
    for j, pat in enumerate(REPS):
        col = list(pat) + [-1] * k
        if any(col[u] == col[v] for u in range(5) for v in adj[u] if v < 5):
            continue

        def extend(i):
            if i == k:
                return True
            v = order[i]
            for c in range(4):
                if all(col[u] != c for u in adj[v]):
                    col[v] = c
                    if extend(i + 1):
                        return True
                    col[v] = -1
            return False
        if extend(0):
            bits |= 1 << j
    return bits


def sigma_of_mask(mask):
    edges = _W['edges']
    return sigma_backtrack(_W['k'], adjacency(_W['k'], [edges[j] for j in range(_W['E']) if mask >> j & 1]))


# ---------------------------------------------------------------- DFS

def _leaf(mask, per_sigma, stats):
    if not viable(mask, _W['E']):
        return
    stats['survivors'] += 1
    s = sigma_of_mask(mask)
    cell = per_sigma.get(s)
    if cell is None:
        cell = per_sigma[s] = dict(count=0, witness=None)
    cell['count'] += 1
    key = (popcount(mask), mask)
    if cell['witness'] is None or key < cell['witness']:
        cell['witness'] = key


def _dfs(mask, start, per_sigma, stats):
    edges, graph, rx, E = _W['edges'], _W['graph'], _W['rx'], _W['E']
    stats['nodes'] += 1
    _leaf(mask, per_sigma, stats)
    for e in range(start, E):
        if not viable(mask, e):
            stats['pruned'] += 1
            return
        u, v = edges[e]
        graph.add_edge(u, v, None)
        if rx.is_planar(graph):
            _dfs(mask | 1 << e, e + 1, per_sigma, stats)
        else:
            stats['nonplanar'] += 1
        graph.remove_edge(u, v)


def _task(args):
    mask, start = args
    edges, graph = _W['edges'], _W['graph']
    for j in range(start):
        if mask >> j & 1:
            graph.add_edge(*edges[j], None)
    per_sigma, stats = {}, dict(nodes=0, survivors=0, pruned=0, nonplanar=0)
    _dfs(mask, start, per_sigma, stats)
    for j in range(start):
        if mask >> j & 1:
            graph.remove_edge(*edges[j])
    return per_sigma, stats


def prefix_nodes(depth):
    """Every planar, viable edge subset of bits < depth, each the root of one disjoint subtree."""
    edges, graph, rx = _W['edges'], _W['graph'], _W['rx']
    out = []

    def rec(mask, start):
        if viable(mask, depth):
            out.append((mask, depth))
        for e in range(start, depth):
            if not viable(mask, e):
                return
            u, v = edges[e]
            graph.add_edge(u, v, None)
            if rx.is_planar(graph):
                rec(mask | 1 << e, e + 1)
            graph.remove_edge(u, v)
    rec(0, 0)
    return out


def enumerate_crosscheck(k, order, sym, jobs, depth, log=print):
    _setup(k, order, sym)
    E = _W['E']
    depth = min(depth, E)
    started = time.monotonic()
    nodes = prefix_nodes(depth)
    nodes.sort(key=lambda n: -popcount(n[0]))
    per_sigma, stats = {}, dict(nodes=0, survivors=0, pruned=0, nonplanar=0)
    with Pool(jobs, initializer=_setup, initargs=(k, order, sym)) as pool:
        for i, (ps, st) in enumerate(pool.imap_unordered(_task, nodes, chunksize=1), 1):
            for s, cell in ps.items():
                mine = per_sigma.get(s)
                if mine is None:
                    per_sigma[s] = cell
                else:
                    mine['count'] += cell['count']
                    mine['witness'] = min(mine['witness'], cell['witness'])
            for key in st:
                stats[key] += st[key]
            if i % 500 == 0 or i == len(nodes):
                log(f"k={k} sym={sym} order={order} tasks={i}/{len(nodes)} nodes={stats['nodes']} "
                    f"survivors={stats['survivors']} sigma={len(per_sigma)} seconds={time.monotonic() - started:.1f}",
                    flush=True)
    stats.update(seconds=round(time.monotonic() - started, 1), jobs=jobs, prefix_depth=depth, prefix_tasks=len(nodes))
    return per_sigma, stats


# ---------------------------------------------------------------- NetworkX re-verification of witnesses

def nx_verify(k, edge_lists):
    import networkx as nx
    checked = 0
    for s, es in edge_lists:
        g = nx.Graph()
        g.add_nodes_from(range(5 + k + 1))
        g.add_edges_from(list(CYCLE) + [tuple(e) for e in es] + [(5 + k, i) for i in range(5)])
        assert nx.check_planarity(g)[0], es
        assert sigma_backtrack(k, adjacency(k, [tuple(e) for e in es])) == s, es
        checked += 1
    return checked


def from_cpp(args):
    cpp = json.loads(args.from_cpp.read_text())
    assert cpp['k'] == args.k and cpp['sym'] == args.sym and cpp['order'] == args.order, 'configuration mismatch'
    _setup(args.k, args.order, args.sym)
    assert [list(e) for e in _W['edges']] == cpp['edges'], 'edge order mismatch between C++ and Python'
    exact = json.loads(CELLS.read_text())
    known = {int(b): c['k_eff'] for b, c in exact['cells'].items()}
    assert exact['k'] == 5 and len(known) == 132
    cells = {int(s): c for s, c in cpp['cells'].items()}
    found = sorted(cells)
    new = [s for s in found if s not in known]
    at_level = sorted(s for s in found if known.get(s, 99) == args.k)
    expected = sorted(s for s, ke in known.items() if ke == args.k) if args.k <= 5 else None
    witnesses = [(s, [list(e) for e in cells[s]['edges']]) for s in found]
    for s, es in witnesses:                       # the witness edge list must be the decoded witness mask
        m = cells[s]['witness_mask']
        assert es == [list(_W['edges'][j]) for j in range(_W['E']) if m >> j & 1]
    src = ROOT / 'scripts/cpp/c5_crosscheck.cpp'
    sha = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    result = dict(
        purpose='independent reproduction of K_k = K_5 along a search path different from c5_cell_reduced.py',
        source_commit=sha,
        enumerator='scripts/cpp/c5_crosscheck.cpp (Boost Boyer-Myrvold planarity, std::thread)',
        enumerator_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),
        verifier='scripts/c5_k6_crosscheck.py --from-cpp (NetworkX planarity + backtracking Σ on every witness)',
        verifier_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        boost_version=cpp['boost_version'], planarity_test=cpp['planarity'],
        configuration=dict(k=args.k, pruning=['R1'] + ([] if args.sym == 'none' else [f'SYM:{args.sym}']),
                           sym=args.sym, edge_order=args.order, edges=cpp['edges'],
                           prefix_depth=cpp['prefix_depth'], prefix_tasks=cpp['prefix_tasks'], threads=cpp['threads']),
        search=cpp['search'], wall_seconds=cpp['search']['seconds'],
        survivors=cpp['search']['survivors'], distinct_sigma=len(found),
        sigma_at_level_k=len(at_level), matches_exact_catalogue=(at_level == expected) if expected is not None else 'beyond exact range',
        new_vs_K5=new, missing_vs_K5=sorted(set(known) - set(found)), catalogue_size=len(set(known) | set(found)),
        nx_verified_witnesses=nx_verify(args.k, witnesses),
        cells={str(s): dict(count=cells[s]['count'], k_eff_in_K5=known.get(s), edges=es) for s, es in witnesses})
    out = args.out or ROOT / f'artifacts/c5_cells/crosscheck_k{args.k}_{args.sym}_{args.order}.json'
    out.write_text(json.dumps(result, indent=1) + '\n')
    for key in ('configuration', 'search', 'survivors', 'distinct_sigma', 'sigma_at_level_k', 'matches_exact_catalogue',
                'new_vs_K5', 'missing_vs_K5', 'catalogue_size', 'nx_verified_witnesses'):
        val = result[key]
        if key == 'configuration':
            val = {a: b for a, b in val.items() if a != 'edges'}
        print(key, json.dumps(val))
    print('written', out)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--k', type=int, required=True)
    parser.add_argument('--sym', choices=('none', 'count', 'nonincreasing', 'nondecreasing'), default='none')
    parser.add_argument('--order', choices=('production', 'within_first', 'attach_first', 'reversed'), default='within_first')
    parser.add_argument('--jobs', type=int, default=max(1, (os.cpu_count() or 2) - 2))
    parser.add_argument('--prefix-depth', type=int, default=None, help='edge bits split across tasks (default: chords + 2 blocks)')
    parser.add_argument('--nx-verify', action='store_true', help='re-test every Σ witness with NetworkX planarity')
    parser.add_argument('--from-cpp', type=Path, default=None, help='ingest scripts/cpp/c5_crosscheck output instead of searching')
    parser.add_argument('--out', type=Path, default=None)
    args = parser.parse_args()
    if args.from_cpp:
        return from_cpp(args)

    exact = json.loads(CELLS.read_text())
    known = {int(b): c['k_eff'] for b, c in exact['cells'].items()}
    assert exact['k'] == 5 and len(known) == 132
    depth = args.prefix_depth if args.prefix_depth is not None else 5 + 2 * 5 + 1 + (0 if args.order != 'attach_first' else 0)
    per_sigma, stats = enumerate_crosscheck(args.k, args.order, args.sym, args.jobs, depth)
    edges = _W['edges']
    found = sorted(per_sigma)
    new = [s for s in found if s not in known]
    at_level = sorted(s for s in found if known.get(s, 99) == args.k)
    expected = sorted(s for s, ke in known.items() if ke == args.k) if args.k <= 5 else None
    witnesses = [(s, [list(edges[j]) for j in range(len(edges)) if per_sigma[s]['witness'][1] >> j & 1]) for s in found]
    sha = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    result = dict(
        purpose='independent reproduction of K_k = K_5 along a search path different from c5_cell_reduced.py',
        source_commit=sha,
        evaluator_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        rustworkx=_W['rx'].__version__,
        configuration=dict(k=args.k, pruning=['R1'] + ([] if args.sym == 'none' else [f'SYM:{args.sym}']),
                           sym=args.sym, edge_order=args.order, edges=[list(e) for e in edges],
                           prefix_depth=stats['prefix_depth'], prefix_tasks=stats['prefix_tasks'], jobs=args.jobs),
        search=stats, wall_seconds=stats['seconds'],
        survivors=stats['survivors'], distinct_sigma=len(found),
        sigma_at_level_k=len(at_level), matches_exact_catalogue=(at_level == expected) if expected is not None else 'beyond exact range',
        new_vs_K5=new, catalogue_size=len(set(known) | set(found)),
        nx_verified_witnesses=nx_verify(args.k, witnesses) if args.nx_verify else 'not run',
        cells={str(s): dict(count=per_sigma[s]['count'], k_eff_in_K5=known.get(s), edges=es) for s, es in witnesses})
    out = args.out or ROOT / f'artifacts/c5_cells/crosscheck_k{args.k}_{args.sym}_{args.order}.json'
    out.write_text(json.dumps(result, indent=1) + '\n')
    for key in ('configuration', 'search', 'survivors', 'distinct_sigma', 'sigma_at_level_k', 'matches_exact_catalogue',
                'new_vs_K5', 'catalogue_size', 'nx_verified_witnesses'):
        val = result[key]
        if key == 'configuration':
            val = {a: b for a, b in val.items() if a != 'edges'}
        print(key, json.dumps(val))
    print('written', out)


if __name__ == '__main__':
    main()
