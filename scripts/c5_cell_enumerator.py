#!/usr/bin/env python3
"""C5 cell enumerator: ordered C5 boundary + sealed disk interior, exposed only as its ten-bit Σ.

uv run --with rustworkx==0.17.1 --with networkx==3.5 python scripts/c5_cell_enumerator.py --k 4 --jobs 16
uv run --with networkx==3.5 python scripts/c5_cell_enumerator.py --check

A *cell* is (ordered C5 b0..b4, interior graph on k private vertices, apex-planar so that
the C5 is a face of the interior side).  The only thing the enumerator exposes outward is
Σ(cell) = the set of proper C5 patterns (S4 orbits, ten bits in the library pattern order)
that extend to the interior.  Exterior structure is never enumerated against the raw interior:
composition is `Σ_in & g·Σ_out` (g ∈ D5 realigns the two boundary labellings), conditioning on
committed boundary colours is a filter on patterns, and the residual states of a cell under a
committed-colour reader are the distinct filtered masks.

Trust: the inner enumeration is a DFS over the full edge universe with apex-planarity pruning
(rustworkx Left–Right test, nonplanar prefixes pruned as in fan_pentagon.py; `--jobs` splits the
DFS by the first PREFIX_BITS edge bits across processes, every subtree accounted once); `--check` replays
every stored witness with NetworkX planarity and an independent brute-force Σ over all colourings.
Everything here is computationally observed; no Lean certificate is produced by this script.
"""
import argparse
from collections import Counter
from multiprocessing import Pool
import os
from itertools import permutations, product
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_cells/cells.json'
sys.path.insert(0, str(ROOT / 'scripts'))
from boundary_relations import normalize  # noqa: E402

CYCLE = tuple((i, (i + 1) % 5) for i in range(5))
CHORDS = ((0, 2), (0, 3), (1, 3), (1, 4), (2, 4))
REPS = tuple(sorted({normalize(b) for b in product(range(4), repeat=5)
                     if all(b[i] != b[(i + 1) % 5] for i in range(5))}))
assert len(REPS) == 10
THREE = tuple(j for j, p in enumerate(REPS) if max(p) == 2)          # patterns using three colours
FOUR = tuple(j for j, p in enumerate(REPS) if max(p) == 3)
SINGLETON = {j: next(i for i in range(5) if list(REPS[j]).count(REPS[j][i]) == 1) for j in THREE}
T4 = sum(1 << j for j in FOUR)


def d5_index_maps():
    """Pattern-index permutation for every boundary relabelling in D5 (rotation^a · reflection^s)."""
    maps = {}
    for s in (0, 1):
        for a in range(5):
            def act(p, a=a, s=s):
                q = tuple(p[(-i) % 5] for i in range(5)) if s else p
                return normalize(tuple(q[(i + a) % 5] for i in range(5)))
            maps[f'r{a}s{s}'] = tuple(REPS.index(act(p)) for p in REPS)
    return maps


D5 = d5_index_maps()


def act_mask(bits, index_map):
    return sum(1 << index_map[j] for j in range(10) if bits >> j & 1)


def edge_universe(k):
    inner = [5 + m for m in range(k)]
    att = [(i, x) for x in inner for i in range(5)]
    within = [(inner[m], inner[l]) for m in range(k) for l in range(m + 1, k)]
    return tuple(CHORDS) + tuple(att) + tuple(within)


def compat_tables(k, edges):
    """Per edge, per pattern: bitset over the 4^k interior assignments compatible with that edge."""
    assigns = list(product(range(4), repeat=k))
    full = (1 << len(assigns)) - 1
    tables = []
    for u, v in edges:
        row = []
        for b in REPS:
            if u < 5 and v < 5:
                row.append(full if b[u] != b[v] else 0)
            elif u < 5:
                row.append(sum(1 << t for t, a in enumerate(assigns) if a[v - 5] != b[u]))
            else:
                row.append(sum(1 << t for t, a in enumerate(assigns) if a[u - 5] != a[v - 5]))
        tables.append(tuple(row))
    return tuple(tables), full


def interior_perm_maps(k, edges):
    """Mask permutations induced by relabelling the k interior vertices."""
    index = {e: j for j, e in enumerate(edges)}
    maps = []
    for perm in permutations(range(k)):
        if perm == tuple(range(k)):
            continue
        rel = {5 + m: 5 + perm[m] for m in range(k)}
        img = []
        for u, v in edges:
            a, b = rel.get(u, u), rel.get(v, v)
            img.append(index[(a, b) if (a, b) in index else (b, a)])
        maps.append(tuple(img))
    return maps


PREFIX_BITS = 12          # edge bits explored by the parent; each accepted prefix node is one task
_W = {}                   # per-process worker state


def _setup(k):
    import rustworkx as rx
    edges = edge_universe(k)
    tables, full = compat_tables(k, edges)
    graph = rx.PyGraph(multigraph=False)
    graph.add_nodes_from(range(5 + k + 1))
    graph.add_edges_from_no_data(list(CYCLE) + [(5 + k, i) for i in range(5)])
    _W.update(k=k, edges=edges, E=len(edges), tables=tables, full=full, graph=graph, rx=rx,
              perm_maps=interior_perm_maps(k, edges) if k <= 3 else [],
              touch=[sum(1 << j for j, (u, v) in enumerate(edges) if 5 + m in (u, v)) for m in range(k)])


def _record(mask, surviving, per_sigma):
    k, E, touch, perm_maps = _W['k'], _W['E'], _W['touch'], _W['perm_maps']
    bits = sum(1 << j for j, s in enumerate(surviving) if s)
    k_eff = sum(1 for m in range(k) if mask & touch[m])
    canonical = k <= 3 and all(sum(1 << pm[j] for j in range(E) if mask >> j & 1) >= mask for pm in perm_maps)
    cell = per_sigma.get(bits)
    if cell is None:
        cell = per_sigma[bits] = dict(labeled=0, canonical=0, by_k_eff=Counter(), witness=None)
    cell['labeled'] += 1
    cell['canonical'] += canonical
    cell['by_k_eff'][k_eff] += 1
    key = (k_eff, bin(mask).count('1'), mask)
    if cell['witness'] is None or key < cell['witness']:
        cell['witness'] = key


def _dfs(mask, start, stop, surviving, per_sigma, stats):
    """Explore edge bits start..stop-1 below `mask`; bits >= stop are left to the caller's tasks."""
    edges, tables, graph, rx, E = _W['edges'], _W['tables'], _W['graph'], _W['rx'], _W['E']
    stats['accepted'] += 1
    _record(mask, surviving, per_sigma)
    for e in range(start, stop):
        u, v = edges[e]
        graph.add_edge(u, v, None)
        stats['calls'] += 1
        if rx.is_planar(graph):
            _dfs(mask | 1 << e, e + 1, stop, tuple(a & b for a, b in zip(surviving, tables[e])), per_sigma, stats)
        else:
            stats['rejected'] += 1
            stats['covered'] += 1 << (E - 1 - e)       # every superset adding only higher bits
        graph.remove_edge(u, v)


def _task(mask):
    """Full subtree of one accepted prefix node: bits >= PREFIX_BITS, the node itself not re-counted."""
    edges, tables, graph, full, E = _W['edges'], _W['tables'], _W['graph'], _W['full'], _W['E']
    surviving = (full,) * 10
    for j in range(PREFIX_BITS):
        if mask >> j & 1:
            graph.add_edge(*edges[j], None)
            surviving = tuple(a & b for a, b in zip(surviving, tables[j]))
    per_sigma, stats = {}, dict(accepted=0, rejected=0, calls=0, covered=0)
    _dfs(mask, PREFIX_BITS, E, surviving, per_sigma, stats)      # records the prefix node itself
    for j in range(PREFIX_BITS):
        if mask >> j & 1:
            graph.remove_edge(*edges[j])
    return per_sigma, stats


def _merge(into, per_sigma):
    for bits, cell in per_sigma.items():
        mine = into.get(bits)
        if mine is None:
            into[bits] = cell
            continue
        mine['labeled'] += cell['labeled']
        mine['canonical'] += cell['canonical']
        mine['by_k_eff'].update(cell['by_k_eff'])
        mine['witness'] = min(mine['witness'], cell['witness'])


def enumerate_cells(k, jobs=1, log=print):
    _setup(k)
    E, full = _W['E'], _W['full']
    prefix = min(PREFIX_BITS, E)
    stats = dict(accepted=0, rejected=0, calls=0, covered=0)
    per_sigma = {}
    started = time.monotonic()
    # parent explores bits < prefix; every accepted node there owns the subtree over bits >= prefix
    nodes = []
    orig_record = _record

    def dfs_prefix(mask, start, surviving):
        if prefix == E:                       # no tasks: the parent owns every node
            stats['accepted'] += 1
            orig_record(mask, surviving, per_sigma)
        nodes.append(mask)
        for e in range(start, prefix):
            u, v = _W['edges'][e]
            _W['graph'].add_edge(u, v, None)
            stats['calls'] += 1
            if _W['rx'].is_planar(_W['graph']):
                dfs_prefix(mask | 1 << e, e + 1, tuple(a & b for a, b in zip(surviving, _W['tables'][e])))
            else:
                stats['rejected'] += 1
                stats['covered'] += 1 << (E - 1 - e)
            _W['graph'].remove_edge(u, v)

    dfs_prefix(0, 0, (full,) * 10)
    if prefix < E:
        nodes.sort(key=lambda m: bin(m).count('1'))            # sparse prefixes = big subtrees first
        if jobs > 1:
            with Pool(jobs, initializer=_setup, initargs=(k,)) as pool:
                results = pool.imap_unordered(_task, nodes, chunksize=1)
                for i, (ps, st) in enumerate(results, 1):
                    _merge(per_sigma, ps)
                    for key in stats:
                        stats[key] += st[key]
                    if i % 200 == 0 or i == len(nodes):
                        log(f"k={k} tasks={i}/{len(nodes)} accepted={stats['accepted']} "
                            f"sigma={len(per_sigma)} seconds={time.monotonic() - started:.1f}", flush=True)
        else:
            for i, mask in enumerate(nodes, 1):
                ps, st = _task(mask)
                _merge(per_sigma, ps)
                for key in stats:
                    stats[key] += st[key]
                if i % 200 == 0:
                    log(f"k={k} tasks={i}/{len(nodes)} accepted={stats['accepted']} "
                        f"sigma={len(per_sigma)} seconds={time.monotonic() - started:.1f}", flush=True)
    stats['covered'] += stats['accepted']
    assert stats['covered'] == 1 << E, 'DFS intervals must tile the whole edge universe'
    stats['seconds'] = round(time.monotonic() - started, 1)
    stats['jobs'] = jobs
    stats['prefix_tasks'] = len(nodes)
    return _W['edges'], per_sigma, stats


def profile(bits):
    return [SINGLETON[j] for j in THREE if bits >> j & 1]


def residual_states(bits):
    """Distinct filtered masks when b0,b1,... are committed in order (prefix normalised)."""
    states = {}
    dead = []
    live_prefixes = {normalize(p[:n]) for p in REPS for n in range(6)}
    for n in range(6):
        for p in REPS:
            pre = normalize(p[:n])
            residual = sum(1 << j for j, q in enumerate(REPS) if bits >> j & 1 and normalize(q[:n]) == pre)
            states[(n, pre)] = residual
    for (n, pre), residual in states.items():
        if residual == 0 and pre in live_prefixes:
            dead.append((n, pre))
    return states, sorted(dead)


def analyse(k, per_sigma, edges):
    cat = {bits: cell for bits, cell in per_sigma.items()}
    nested = {}
    for level in range(k + 1):
        nested[level] = sorted(bits for bits, cell in cat.items() if cell['witness'][0] <= level)
    prof = {bits: profile(bits) for bits in cat}
    size2 = [bits for bits, p in prof.items() if len(p) == 2]
    adjacent2 = all((p[0] - p[1]) % 5 in (1, 4) for bits in size2 for p in [prof[bits]])
    lib = json.loads((ROOT / 'artifacts/boundary_relations/library.json').read_text())
    lib_ids = sorted(int(e['id']) for e in lib['entries'])
    k3_ids = sorted(int(e['id']) for e in lib['entries'] if not e['new_vs_triangle'])
    fan = json.loads((ROOT / 'artifacts/fan_pentagon/states.json').read_text())
    assert [list(p) for p in REPS] == fan['pattern_order'], 'pattern order must match the libraries'
    fan_ids = sorted(s['sigma_bits'] for s in fan['states'])
    # separating C5: both sides are cells, any D5 realignment of the second boundary labelling
    meets, bad, exact_t4 = set(), {}, set()
    for b1 in sorted(cat):
        for name, im in D5.items():
            for b2 in sorted(cat):
                m = b1 & act_mask(b2, im)
                meets.add(m)
                if m and not any(m >> j & 1 for j in THREE):
                    cost = cat[b1]['witness'][0] + cat[b2]['witness'][0]
                    if m not in bad or (cost, b1, name, b2) < bad[m]:
                        bad[m] = (cost, b1, name, b2)
                if m == T4:
                    exact_t4.add((b1, name, b2))
    states_all, dead_all = {}, {}
    for bits in cat:
        st, dead = residual_states(bits)
        states_all[bits] = st
        dead_all[bits] = dead
    distinct_residual = {r for st in states_all.values() for r in st.values()}
    return dict(
        pattern_order=[list(p) for p in REPS],
        three_colour_patterns=list(THREE), singleton_of_three_colour=SINGLETON,
        edge_universe=[list(e) for e in edges],
        distinct_sigma=len(cat),
        nested_by_k_eff={str(level): len(v) for level, v in nested.items()},
        new_sigma_by_k_eff={str(level): len(set(nested[level]) - set(nested.get(level - 1, [])))
                            for level in nested},
        empty_sigma=sum(1 for bits in cat if bits == 0),
        no_three_colour=sum(1 for bits in cat if bits and not prof[bits]),
        min_three_profile=min(len(p) for p in prof.values()),
        profile_size_counts={str(n): sum(1 for p in prof.values() if len(p) == n) for n in range(6)},
        size2_profiles_adjacent=adjacent2,
        d5_orbits=len({min(act_mask(bits, im) for im in D5.values()) for bits in cat}),
        libraries=dict(
            fan_pentagon_states=len(fan_ids),
            fan_pentagon_in_catalogue=sum(1 for b in fan_ids if b in cat),
            fan_pentagon_missing=[b for b in fan_ids if b not in cat],
            library_entries=len(lib_ids), library_in_catalogue=sum(1 for b in lib_ids if b in cat),
            triangle_grammar_states=len(k3_ids),
            triangle_grammar_in_catalogue=sum(1 for b in k3_ids if b in cat)),
        separating_c5=dict(
            distinct_meets=len(meets), empty_meets=int(0 in meets),
            bad_meets=len(bad), exact_T4_pairs=len(exact_t4),
            min_bad_interior_vertices=(min(v[0] for v in bad.values()) if bad else None),
            cheapest_bad=[dict(meet=m, sides=[v[1], v[3]], alignment=v[2], interior_vertices=v[0])
                          for m, v in sorted(bad.items(), key=lambda kv: (kv[1][0], kv[0]))[:5]]),
        residual=dict(
            distinct_residual_masks=len(distinct_residual),
            cells_with_dead_prefix=sum(1 for d in dead_all.values() if d),
            max_dead_prefixes=max(len(d) for d in dead_all.values()),
            earliest_dead_prefix_length=min((n for d in dead_all.values() for n, _ in d), default=None)),
        cells={str(bits): dict(
            k_eff=cell['witness'][0], edges=[list(edges[j]) for j in range(len(edges)) if cell['witness'][2] >> j & 1],
            labeled_masks=cell['labeled'], canonical_masks=cell['canonical'],
            three_profile=prof[bits], dead_prefixes=[[n, list(p)] for n, p in dead_all[bits]])
            for bits, cell in sorted(cat.items())},
    )


def brute_sigma(k_eff, edges):
    """Independent Σ: every proper colouring of the witness graph, boundary pattern normalised."""
    n = 5 + k_eff
    used = sorted({v for e in edges for v in e} | set(range(5)))
    assert used == list(range(n)), used
    all_edges = list(CYCLE) + [tuple(e) for e in edges]
    found = set()
    for c in product(range(4), repeat=n):
        if all(c[u] != c[v] for u, v in all_edges):
            found.add(normalize(c[:5]))
    return sum(1 << REPS.index(p) for p in found)


def check():
    import networkx as nx
    data = json.loads(OUT.read_text())
    assert data['pattern_order'] == [list(p) for p in REPS]
    bad = 0
    for bits, cell in data['cells'].items():
        edges = [tuple(e) for e in cell['edges']]
        k_eff = cell['k_eff']
        relabel = {v: i for i, v in enumerate(sorted({v for e in edges for v in e} | set(range(5))))}
        edges = [(relabel[u], relabel[v]) for u, v in edges]
        g = nx.Graph(list(CYCLE) + edges + [(5 + k_eff, i) for i in range(5)])
        planar, _ = nx.check_planarity(g)
        sigma = brute_sigma(k_eff, edges)
        ok = planar and sigma == int(bits)
        bad += not ok
        if not ok:
            print(f'MISMATCH bits={bits} planar={planar} brute={sigma}')
    print(f"{len(data['cells'])} cells replayed, {bad} mismatches; "
          f"distinct_sigma={data['distinct_sigma']} nested={data['nested_by_k_eff']}")
    sys.exit(1 if bad else 0)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--k', type=int, default=3, help='interior vertex budget (3 ≈ 1 min)')
    parser.add_argument('--check', action='store_true', help='replay stored witnesses independently')
    parser.add_argument('--jobs', type=int, default=max(1, (os.cpu_count() or 2) // 2),
                        help='worker processes for the subtree tasks (default: physical cores)')
    args = parser.parse_args()
    if args.check:
        check()
        return
    edges, per_sigma, stats = enumerate_cells(args.k, args.jobs)
    result = dict(k=args.k, search=stats, **analyse(args.k, per_sigma, edges))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=1) + '\n')
    for key in ('search', 'distinct_sigma', 'nested_by_k_eff', 'new_sigma_by_k_eff', 'min_three_profile',
                'profile_size_counts', 'size2_profiles_adjacent', 'd5_orbits', 'libraries',
                'separating_c5', 'residual'):
        print(key, json.dumps(result[key]))


if __name__ == '__main__':
    main()
