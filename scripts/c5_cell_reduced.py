#!/usr/bin/env python3
"""Reduced C5 cell enumeration: only interiors that no syntactic reduction removes.

uv run --with rustworkx==0.17.1 python scripts/c5_cell_reduced.py --k 6 --jobs 30

Same universe as c5_cell_enumerator.py (ordered C5, k private vertices, chords allowed, apex-planar),
but the DFS keeps only graphs in which

  R1  every interior vertex has degree >= 4   (a vertex with <= 3 neighbours is coloured last, so
                                              Σ(G) = Σ(G - v) and Σ(G) already lies in K_{k-1});
  SYM the five-bit boundary-attachment masks of x_1..x_k are non-increasing
      (every interior graph can be relabelled that way, so each unlabelled graph is still visited).

Edges are ordered chords, then one block per interior vertex (its five attachments, then its edges to
earlier interior vertices), so a vertex's degree and attachment mask are final when its block ends and
R1/SYM prune the DFS as soon as they fail.  The result is complete for the *new* Σ at level k:
K_k = K_{k-1} ∪ Σ(survivors).  Coverage of the edge universe is no longer asserted; the check is that
for k <= 5 the survivors' new Σ equal the exact catalogue's Σ with k_eff = k.

--r2 additionally tests every survivor for the non-monotone reduction

  R2  a cycle of length 3/4/5 separating a nonempty set S of interior vertices from the boundary,
      whose inside relation (on the cycle, all edges among cycle ∪ S) is realised by a disk patch with
      fewer than |S| interior vertices (C3: always 0; C4: small catalogue built here; C5: cells.json).
      Replacing the inside by that patch keeps Σ (Lean `replacement`) and planarity, so Σ ∈ K_{k-1}.

Observed for k <= 5: survivors with an old Σ are exactly the R2-reducible ones, and no survivor with a
new Σ is R2-reducible.
"""
import argparse
from collections import Counter
import itertools
import json
from multiprocessing import Pool
import os
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
import c5_cell_enumerator as C  # noqa: E402
from boundary_relations import normalize  # noqa: E402

ROOT = C.ROOT
OUT_DIR = ROOT / 'artifacts/c5_cells'
_W = {}


def block_edge_order(k):
    edges = list(C.CHORDS)
    blocks = []                       # per interior vertex: (first edge index, att sub-block end, last edge index)
    for m in range(k):
        x = 5 + m
        first = len(edges)
        edges += [(i, x) for i in range(5)]
        att_end = len(edges)
        edges += [(5 + l, x) for l in range(m)]
        blocks.append((first, att_end, len(edges) - 1))
    return tuple(edges), blocks


def _setup(k, keep=False):
    import rustworkx as rx
    edges, blocks = block_edge_order(k)
    tables, full = C.compat_tables(k, edges)
    graph = rx.PyGraph(multigraph=False)
    graph.add_nodes_from(range(5 + k + 1))
    graph.add_edges_from_no_data(list(C.CYCLE) + [(5 + k, i) for i in range(5)])
    block_of = [None] * len(edges)
    for m, (first, att_end, last) in enumerate(blocks):
        for e in range(first, last + 1):
            block_of[e] = m
    touch = [sum(1 << j for j, (u, v) in enumerate(edges) if 5 + m in (u, v)) for m in range(k)]
    att = [sum(1 << j for j in range(first, att_end)) for first, att_end, _ in blocks]
    _W.update(k=k, edges=edges, E=len(edges), blocks=blocks, block_of=block_of, tables=tables, full=full,
              graph=graph, rx=rx, touch=touch, att=att, keep=keep)


def att_value(mask, m):
    first, att_end, _ = _W['blocks'][m]
    return (mask >> first) & ((1 << (att_end - first)) - 1)


def viable(mask, e):
    """Can some continuation adding only bits >= e satisfy R1 and SYM?  (bits < e are final)"""
    k, blocks, touch = _W['k'], _W['blocks'], _W['touch']
    for m in range(k):
        first = blocks[m][0]
        if e <= first:
            break                                       # block m and later are still entirely open
        undecided = bin(touch[m] >> e).count('1')       # x_m's edges not yet decided, in any block
        if bin(mask & touch[m]).count('1') + undecided < 4:
            return False
        if m >= 1 and att_value(mask, m) > att_value(mask, m - 1):
            return False                                # undecided attachment bits can only grow it
    return True


def _record(mask, surviving, per_sigma):
    if not viable(mask, _W['E']):
        return False
    bits = sum(1 << j for j, s in enumerate(surviving) if s)
    cell = per_sigma.get(bits)
    if cell is None:
        cell = per_sigma[bits] = dict(count=0, witness=None)
    cell['count'] += 1
    key = (bin(mask).count('1'), mask)
    if cell['witness'] is None or key < cell['witness']:
        cell['witness'] = key
    if _W.get('keep'):
        cell.setdefault('masks', []).append(mask)
    return True


def _dfs(mask, start, stop, surviving, per_sigma, stats):
    edges, tables, graph, rx = _W['edges'], _W['tables'], _W['graph'], _W['rx']
    stats['nodes'] += 1
    stats['survivors'] += _record(mask, surviving, per_sigma)
    for e in range(start, stop):
        if not viable(mask, e):
            stats['pruned'] += 1
            return
        u, v = edges[e]
        graph.add_edge(u, v, None)
        stats['calls'] += 1
        if rx.is_planar(graph):
            _dfs(mask | 1 << e, e + 1, stop, tuple(a & b for a, b in zip(surviving, tables[e])), per_sigma, stats)
        else:
            stats['rejected'] += 1
        graph.remove_edge(u, v)


def _task(args):
    mask, prefix = args
    edges, tables, graph, full, E = _W['edges'], _W['tables'], _W['graph'], _W['full'], _W['E']
    surviving = (full,) * 10
    for j in range(prefix):
        if mask >> j & 1:
            graph.add_edge(*edges[j], None)
            surviving = tuple(a & b for a, b in zip(surviving, tables[j]))
    per_sigma, stats = {}, dict(nodes=0, survivors=0, pruned=0, calls=0, rejected=0)
    _dfs(mask, prefix, E, surviving, per_sigma, stats)
    for j in range(prefix):
        if mask >> j & 1:
            graph.remove_edge(*edges[j])
    return per_sigma, stats


def _merge(into, per_sigma):
    for bits, cell in per_sigma.items():
        mine = into.get(bits)
        if mine is None:
            into[bits] = cell
        else:
            mine['count'] += cell['count']
            mine['witness'] = min(mine['witness'], cell['witness'])
            if 'masks' in cell:
                mine.setdefault('masks', []).extend(cell['masks'])


def enumerate_reduced(k, jobs, log=print, keep=False):
    _setup(k, keep)
    E, full, blocks = _W['E'], _W['full'], _W['blocks']
    prefix = blocks[min(1, k - 1)][2] + 1 if k >= 1 else E       # chords + blocks of x_1, x_2
    started = time.monotonic()
    nodes = []
    stats = dict(nodes=0, survivors=0, pruned=0, calls=0, rejected=0)
    per_sigma = {}

    def dfs_prefix(mask, start, surviving):
        if prefix == E:
            stats['nodes'] += 1
            stats['survivors'] += _record(mask, surviving, per_sigma)
        nodes.append((mask, prefix))
        for e in range(start, prefix):
            if not viable(mask, e):
                return
            u, v = _W['edges'][e]
            _W['graph'].add_edge(u, v, None)
            if _W['rx'].is_planar(_W['graph']):
                dfs_prefix(mask | 1 << e, e + 1, tuple(a & b for a, b in zip(surviving, _W['tables'][e])))
            _W['graph'].remove_edge(u, v)

    dfs_prefix(0, 0, (full,) * 10)
    nodes = [n for n in nodes if viable(n[0], prefix)]           # prefix nodes that can still complete
    if prefix < E:
        nodes.sort(key=lambda n: bin(n[0]).count('1'))
        with Pool(jobs, initializer=_setup, initargs=(k, keep)) as pool:
            for i, (ps, st) in enumerate(pool.imap_unordered(_task, nodes, chunksize=1), 1):
                _merge(per_sigma, ps)
                for key in stats:
                    stats[key] += st[key]
                if i % 500 == 0 or i == len(nodes):
                    log(f"k={k} tasks={i}/{len(nodes)} nodes={stats['nodes']} survivors={stats['survivors']} "
                        f"sigma={len(per_sigma)} seconds={time.monotonic() - started:.1f}", flush=True)
    stats['seconds'] = round(time.monotonic() - started, 1)
    stats['jobs'] = jobs
    stats['prefix_tasks'] = len(nodes)
    return per_sigma, stats


# ---------------------------------------------------------------- R2: separating short cycles

def cycle_patterns(L):
    return sorted({normalize(b) for b in itertools.product(range(4), repeat=L)
                   if all(b[i] != b[(i + 1) % L] for i in range(L))})


PATS = {L: cycle_patterns(L) for L in (3, 4, 5)}
assert PATS[5] == list(C.REPS)


def inside_relation(adj, cyc, inside):
    """Patterns on the ordered cycle that extend to `inside`, using every edge among cycle ∪ inside."""
    L, pos, order, bits = len(cyc), {v: i for i, v in enumerate(cyc)}, sorted(inside), 0
    for j, b in enumerate(PATS[L]):
        col = {v: b[pos[v]] for v in cyc}
        if any(col[u] == col[v] for u in cyc for v in adj[u] if v in col):
            continue

        def bt(i):
            if i == len(order):
                return True
            v = order[i]
            for c in range(4):
                if all(col.get(u) != c for u in adj[v] if u in col):
                    col[v] = c
                    if bt(i + 1):
                        return True
                    del col[v]
            return False
        if bt(0):
            bits |= 1 << j
    return bits


def c4_catalogue(kmax=3):
    """Fewest interior vertices realising each relation on an ordered C4 by an apex-planar disk patch."""
    import rustworkx as rx
    best = {}
    cyc = [(i, (i + 1) % 4) for i in range(4)]
    for k in range(kmax + 1):
        n = 4 + k
        edges = ([(0, 2), (1, 3)] + [(i, 4 + m) for m in range(k) for i in range(4)]
                 + [(4 + l, 4 + m) for m in range(k) for l in range(m)])
        for mask in range(1 << len(edges)):
            es = [edges[j] for j in range(len(edges)) if mask >> j & 1]
            if any(all(4 + m not in e for e in es) for m in range(k)):
                continue                                  # unused vertex: already counted at k-1
            g = rx.PyGraph(multigraph=False)
            g.add_nodes_from(range(n + 1))
            g.add_edges_from_no_data(cyc + es + [(n, i) for i in range(4)])
            if not rx.is_planar(g):
                continue
            adj = [set() for _ in range(n)]
            for u, v in cyc + es:
                adj[u].add(v)
                adj[v].add(u)
            best.setdefault(inside_relation(adj, [0, 1, 2, 3], set(range(4, n))), k)
    return best


def r2_reduction(mask):
    """(cycle, |S|, smaller realisation size) for the first separating short cycle that reduces mask, else None."""
    edges, k, c4, c5 = _W['edges'], _W['k'], _W['c4'], _W['c5']
    n = 5 + k
    adj = [set() for _ in range(n)]
    for u, v in list(C.CYCLE) + [edges[j] for j in range(len(edges)) if mask >> j & 1]:
        adj[u].add(v)
        adj[v].add(u)
    inner = set(range(5, n))
    for L in (3, 4, 5):
        for cut in itertools.combinations(range(n), L):
            cs, order = set(cut), None
            for perm in itertools.permutations(cut[1:]):
                cyc = (cut[0],) + perm
                if all(cyc[(i + 1) % L] in adj[cyc[i]] for i in range(L)):
                    order = cyc
                    break
            if order is None:
                continue
            seen = {i for i in range(5) if i not in cs}
            stack = list(seen)
            while stack:
                a = stack.pop()
                for b in adj[a]:
                    if b not in cs and b not in seen:
                        seen.add(b)
                        stack.append(b)
            S = {v for v in inner if v not in cs and v not in seen}
            if not S:
                continue
            rel = inside_relation(adj, list(order), S)
            need = 0 if L == 3 else c4.get(rel, 99) if L == 4 else c5.get(rel, 99)
            if need < len(S):
                return order, len(S), need
    return None


def _r2_setup(k, c4, c5):
    _setup(k)
    _W.update(c4=c4, c5=c5)


def _r2_task(item):
    bits, masks = item
    return bits, [r2_reduction(m) is not None for m in masks]


def r2_verify(k, per_sigma, known, jobs, log=print):
    c4 = c4_catalogue(3)
    items = [(bits, cell['masks']) for bits, cell in per_sigma.items()]
    counts = Counter()
    unreduced = {}
    started = time.monotonic()
    with Pool(jobs, initializer=_r2_setup, initargs=(k, c4, known)) as pool:
        for i, (bits, flags) in enumerate(pool.imap_unordered(_r2_task, items), 1):
            new = known.get(bits, 99) >= k
            for f in flags:
                counts[(new, f)] += 1
            if not new and not all(flags):
                unreduced[bits] = sum(1 for f in flags if not f)
            if i % 20 == 0 or i == len(items):
                log(f"r2 k={k} sigma={i}/{len(items)} seconds={time.monotonic() - started:.1f}", flush=True)
    return dict(
        c4_catalogue={str(rel): need for rel, need in sorted(c4.items())},
        old_sigma_reducible=counts[(False, True)], old_sigma_unreduced=counts[(False, False)],
        new_sigma_reducible=counts[(True, True)], new_sigma_irreducible=counts[(True, False)],
        old_sigma_with_unreduced_survivors={str(b): c for b, c in sorted(unreduced.items())},
        complete=(counts[(False, False)] == 0 and counts[(True, True)] == 0))



def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--k', type=int, required=True)
    parser.add_argument('--jobs', type=int, default=max(1, (os.cpu_count() or 2) // 2))
    parser.add_argument('--r2', action='store_true', help='test every survivor for the separating-cycle reduction')
    args = parser.parse_args()
    exact = json.loads((OUT_DIR / 'cells.json').read_text())
    known = {int(b): c['k_eff'] for b, c in exact['cells'].items()}
    per_sigma, stats = enumerate_reduced(args.k, args.jobs, keep=args.r2)
    edges = _W['edges']
    new = sorted(b for b in per_sigma if known.get(b, 99) >= args.k)
    old = sorted(b for b in per_sigma if known.get(b, 99) < args.k)
    expected = sorted(b for b, ke in known.items() if ke == args.k) if args.k <= exact['k'] else None
    result = dict(
        k=args.k, search=stats, edge_order=[list(e) for e in edges],
        survivors=stats['survivors'], distinct_sigma=len(per_sigma),
        new_sigma=len(new), old_sigma_realised=len(old),
        old_sigma_survivor_graphs=sum(per_sigma[b]['count'] for b in old),
        new_sigma_survivor_graphs=sum(per_sigma[b]['count'] for b in new),
        matches_exact_catalogue=(new == expected) if expected is not None else 'beyond exact range',
        catalogue_size=len(set(known) | set(per_sigma)),
        r2=r2_verify(args.k, per_sigma, known, args.jobs) if args.r2 else 'not run',
        cells={str(b): dict(count=c['count'], new=b in new,
                            edges=[list(edges[j]) for j in range(len(edges)) if c['witness'][1] >> j & 1])
               for b, c in sorted(per_sigma.items())})
    path = OUT_DIR / f'reduced_k{args.k}.json'
    path.write_text(json.dumps(result, indent=1) + '\n')
    for key in ('search', 'survivors', 'distinct_sigma', 'new_sigma', 'old_sigma_realised',
                'old_sigma_survivor_graphs', 'new_sigma_survivor_graphs', 'matches_exact_catalogue', 'catalogue_size', 'r2'):
        print(key, json.dumps(result[key]))


if __name__ == '__main__':
    main()
