#!/usr/bin/env python3
"""Semantic bridge: the ten-bit mask of `c5_cell_enumerator.py` ≡ the specification Σ.

uv run --with networkx==3.5 --with rustworkx==0.17.1 python scripts/c5_sigma_bridge.py --quick
uv run --with networkx==3.5 --with rustworkx==0.17.1 python scripts/c5_sigma_bridge.py \
  --cases --product --catalogue --random 60 \
  --all-masks 0 --all-masks 1 --all-masks 2 --all-masks 3 --dfs 2 --dfs 3 --dfs 4

------------------------------------------------------------------------------
SPECIFICATION (everything in this block is definitional; no production code)
------------------------------------------------------------------------------
A *C5 cell graph* is a pair (k, E) where k ≥ 0 counts sealed private interior
vertices X = {5, …, 4+k} and E is a set of edges drawn from the universe

    U(k) = chords(5) ∪ boundary–interior(5k) ∪ interior–interior(C(k,2)),

with the boundary C5 = 0-1-2-3-4-0 always present.  Index the edges of U(k) by
their position 0 … |U(k)|-1 in that fixed order; a *mask* is a subset of U(k)
written as a little-endian bitmap over that index.

Write `proper(C5)` for the proper four-colourings of the boundary cycle and

    S4 = the global colour renamings {0,1,2,3} → {0,1,2,3}.

`orbit_rep(b)` is the representative of the S4 orbit of b, computed as the
lexicographically least relabelling of b.  `PATTERN_ORDER` is the sorted list of
the ten orbit representatives of `proper(C5)`.

    Σ(k, E)  :=  { orbit_rep(b) : b ∈ proper(C5) ∧ ∃ x : X → {0,1,2,3},
                                    proper on C5 ∪ E and x|boundary = b }

    bit_j(k, E) = 1  ⟺  PATTERN_ORDER[j] ∈ Σ(k, E)          (0 ≤ j < 10)
    mask(k, E)  =  Σ_j bit_j(k, E) · 2^j

Semantic reading of one bit: bit j = 1 means the boundary colour-class (S4
orbit) PATTERN_ORDER[j] has at least one proper extension to the sealed interior
that also respects every chord, attachment and interior edge of E.  bit j = 0
means no such extension exists.  Colours are *global*: one renaming is applied
to boundary and interior simultaneously, which is exactly why the ten orbit bits
are a lossless interface (see docs/c5_cell_enumerator.md §0–§1).

This file checks that the production enumerator's mask is that function:

  * `PATTERN_ORDER` is re-derived here from the definition and compared with
    the production `REPS` and with both published libraries' `pattern_order`.
  * `orbit_rep` is re-derived by a different algorithm and compared with
    `boundary_relations.normalize`.
  * `ref_bits` enumerates boundary colourings first and then interior
    colourings (constraint search); `ref_bitwise` tests each of the ten orbits
    independently from its representative; `ref_bits_product` brute-forces all
    4^(5+k) colourings.  All three are written from the definition only.
  * `prod_bits` reads the mask out of the production code path: the production
    `compat_tables` fold plus the production `_record` bit encoder.
  * `dfs_sweep` runs the production DFS itself and captures, through a spy on
    `_record`, every accepted node's mask, so the fold is production code too.

Trust level of the result: **computationally verified** on the domains printed
in the report (exhaustive over all DFS-accepted graphs for the k values swept,
exhaustive over the whole k ≤ 5 catalogue, plus curated extremes).  It is not a
Lean proof, it says nothing about k ≥ 6, and it does not touch geometry: apex
planarity decides which graphs enter the catalogue, not what Σ is.
"""
import argparse
from itertools import permutations, product
import hashlib
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import c5_cell_enumerator as prod            # noqa: E402  (code under test)
from boundary_relations import normalize     # noqa: E402  (second opinion only)

CELLS = ROOT / 'artifacts/c5_cells/cells.json'
LIBRARY = ROOT / 'artifacts/boundary_relations/library.json'
FAN = ROOT / 'artifacts/fan_pentagon/states.json'
REPORT = ROOT / 'artifacts/c5_cells/sigma_bridge.json'
QUICK_REPORT = ROOT / 'artifacts/c5_cells/sigma_bridge_quick.json'

COLOUR_COUNT = 4
CYCLE = tuple((i, (i + 1) % 5) for i in range(5))
CHORDS = ((0, 2), (0, 3), (1, 3), (1, 4), (2, 4))
PROPER_BOUNDARY = tuple(b for b in product(range(COLOUR_COUNT), repeat=5)
                        if all(b[i] != b[(i + 1) % 5] for i in range(5)))
assert len(PROPER_BOUNDARY) == 240, len(PROPER_BOUNDARY)


# ---------------------------------------------------------------- specification
def edge_universe(k):
    """U(k) in index order: chords, then boundary–interior, then interior–interior."""
    inner = [5 + m for m in range(k)]
    return (tuple(CHORDS) + tuple((i, x) for x in inner for i in range(5))
            + tuple((inner[m], inner[l]) for m in range(k) for l in range(m + 1, k)))


def orbit_rep(b):
    """S4 representative: least relabelling over all global colour renamings."""
    return min(tuple(perm[c] for c in b) for perm in permutations(range(COLOUR_COUNT)))


PATTERN_ORDER = tuple(sorted({orbit_rep(b) for b in PROPER_BOUNDARY}))
PATTERN_INDEX = {p: j for j, p in enumerate(PATTERN_ORDER)}
assert len(PATTERN_ORDER) == 10


def canon_agrees():
    """`orbit_rep` (min over S4) vs `normalize` (first-appearance) on *all* 4^5 tuples."""
    bad = [b for b in product(range(COLOUR_COUNT), repeat=5) if orbit_rep(b) != normalize(b)]
    proper_bad = [b for b in PROPER_BOUNDARY if orbit_rep(b) != normalize(b)]
    return dict(all_5tuples=4 ** 5, all_agree=not bad, proper_agree=not proper_bad,
                counterexample=bad[0] if bad else None)


def orbit_members(p):
    """Every colouring with representative p — the S4 orbit, listed explicitly."""
    return {tuple(perm[c] for c in p) for perm in permutations(range(COLOUR_COUNT))}


# --------------------------------------------------- reference Σ (spec-only code)
def _popcount(x):
    return bin(x).count('1')


def _extend(remaining, dom, cols, adj):
    """Backtracking over interior vertices with minimum-remaining-values order."""
    if not remaining:
        return True
    v = min(remaining, key=lambda x: _popcount(dom[x]))
    if dom[v] == 0:
        return False
    rest = tuple(x for x in remaining if x != v)
    d = dom[v]
    while d:
        bit = d & -d
        d ^= bit
        c = bit.bit_length() - 1
        ndom, ncols, ok = list(dom), list(cols), True
        ndom[v], ncols[v] = 0, c
        for w in adj[v]:
            if ncols[w] >= 0:
                if ncols[w] == c:
                    ok = False
                    break
            else:
                ndom[w] &= ~bit
                if ndom[w] == 0:
                    ok = False
                    break
        if ok and _extend(rest, ndom, ncols, adj):
            return True
    return False


def ref_feasible(k, edges, boundary):
    """∃ interior colouring proper on C5 ∪ edges and agreeing with `boundary`?"""
    for u, v in edges:                                   # chords constrain the boundary
        if u < 5 and v < 5 and boundary[u] == boundary[v]:
            return False
    dom, adj = [0b1111] * k, [[] for _ in range(k)]
    for u, v in edges:
        if u >= 5 and v >= 5:
            a, b = u - 5, v - 5
            adj[a].append(b)
            adj[b].append(a)
        elif u < 5 <= v:
            dom[v - 5] &= ~(1 << boundary[u])
        elif v < 5 <= u:
            dom[u - 5] &= ~(1 << boundary[v])
    if any(d == 0 for d in dom):
        return False
    return _extend(tuple(range(k)), dom, [-1] * k, adj)


def ref_sigma(k, edges):
    """Σ as a set of orbit representatives, by enumerating boundary then interior."""
    return {orbit_rep(b) for b in PROPER_BOUNDARY if ref_feasible(k, edges, b)}


def ref_bits(k, edges):
    return sum(1 << PATTERN_INDEX[p] for p in ref_sigma(k, edges))


def ref_bitwise(k, edges):
    """Bit j tested on its own from representative PATTERN_ORDER[j]; no orbit reasoning."""
    return sum(1 << j for j, p in enumerate(PATTERN_ORDER) if ref_feasible(k, edges, p))


def ref_bits_product(k, edges):
    """Brute force over all 4^(5+k) colourings of boundary + interior."""
    full = CYCLE + tuple(edges)
    found = set()
    for c in product(range(COLOUR_COUNT), repeat=5 + k):
        if all(c[u] != c[v] for u, v in full):
            found.add(orbit_rep(c[:5]))
    return sum(1 << PATTERN_INDEX[p] for p in found)


def orbit_invariance(k, edges, j):
    """All members of orbit j must be equally (in)feasible — validates S4 compression."""
    verdicts = {ref_feasible(k, edges, b) for b in orbit_members(PATTERN_ORDER[j])}
    return len(verdicts) == 1


# ------------------------------------------------- production code under test
REAL_RECORD = prod._record


def prod_setup(k, force=False):
    """Enter the production worker state for k (`_W` is one shared dict, so track its k)."""
    assert prod.edge_universe(k) == edge_universe(k), 'edge universe drifted'
    if force or prod._W.get('k') != k:
        prod._setup(k)                  # production tables for this k
    return prod._W


def prod_bits(k, mask):
    """Production Σ at one edge set: production tables folded, production `_record` encodes."""
    w = prod_setup(k)
    surviving = (w['full'],) * 10
    for j in range(len(w['edges'])):
        if mask >> j & 1:
            surviving = tuple(a & b for a, b in zip(surviving, w['tables'][j]))
    probe = {}
    REAL_RECORD(mask, surviving, probe)          # production bit encoder
    assert len(probe) == 1
    return next(iter(probe))


def mask_of(k, edges):
    index = {e: j for j, e in enumerate(edge_universe(k))}
    mask = 0
    for e in edges:
        u, v = e
        mask |= 1 << index[(u, v) if (u, v) in index else (v, u)]
    return mask


def edges_of(k, mask):
    return [e for j, e in enumerate(edge_universe(k)) if mask >> j & 1]


def compare(k, edges, label):
    """One graph, both directions: production mask vs the three reference readings."""
    mask = mask_of(k, edges)
    got = prod_bits(k, mask)
    by_orbit = ref_bits(k, edges)
    by_bit = ref_bitwise(k, edges)
    row = dict(label=label, k=k, edges=[list(e) for e in edges], mask=mask,
               prod_bits=got, ref_bits=by_orbit, ref_bits_per_bit=by_bit,
               bits=[(got >> j) & 1 for j in range(10)],
               ref_bits_list=[(by_bit >> j) & 1 for j in range(10)],
               orbit_invariant=all(orbit_invariance(k, edges, j) for j in range(10)),
               match=(got == by_orbit == by_bit))
    return row


# ---------------------------------------------------------------- curated cases
def star(m):
    """The five attachment edges of interior vertex 5+m."""
    return [(i, 5 + m) for i in range(5)]


def case_list():
    cases = [
        ('k=0 empty interior (boundary C5 only)', 0, []),
        ('k=0 single chord [0,2]', 0, [(0, 2)]),
        ('k=0 two chords sharing endpoint [0,2],[0,3]', 0, [(0, 2), (0, 3)]),
        ('k=0 boundary K4 chords [0,2],[0,3],[1,3] (minimal BAD side)', 0, [(0, 2), (0, 3), (1, 3)]),
        ('k=0 three chords [0,2],[0,3],[2,4]', 0, [(0, 2), (0, 3), (2, 4)]),
        ('k=0 all five chords (boundary K5, not 4-colourable)', 0, list(CHORDS)),
        ('k=1 isolated interior vertex (k_eff=0 in production wording)', 1, []),
        ('k=1 full attachment star (5 edges)', 1, star(0)),
        ('k=1 degree-4 attachment star, no chord [0,2]', 1, [(i, 5) for i in range(1, 5)]),
        ('k=1 degree-3 attachment star', 1, [(0, 5), (1, 5), (2, 5)]),
        ('k=2 two attachment stars', 2, star(0) + star(1)),
        ('k=2 attachment stars plus interior edge', 2, star(0) + star(1) + [(5, 6)]),
        ('k=2 isolated pair (no edges at all)', 2, []),
        ('k=3 interior triangle + one attachment each', 3,
         [(5, 6), (6, 7), (5, 7)] + [(0, 5), (1, 6), (2, 7)]),
        ('k=3 interior path + chords', 3,
         [(0, 2), (5, 6), (6, 7), (0, 5), (1, 5), (2, 6), (3, 7)]),
        ('k=4 interior K4 (needs 4 colours, boundary pinned)', 4,
         [(5, 6), (5, 7), (5, 8), (6, 7), (6, 8), (7, 8)]),
        ('k=4 interior K4 + full stars', 4,
         [(5, 6), (5, 7), (5, 8), (6, 7), (6, 8), (7, 8)]
         + [e for m in range(4) for e in star(m)]),
        ('k=5 interior K5 (5-chromatic, only reachable unplanarly)', 5,
         [(5 + a, 5 + b) for a in range(5) for b in range(a + 1, 5)]),
        ('k=5 five interior vertices, each attached to all five boundary vertices', 5,
         [e for m in range(5) for e in star(m)]),
        ('k=5 interior 5-cycle + one attachment each', 5,
         [(5 + m, 5 + (m + 1) % 5) for m in range(5)] + [(m, 5 + m) for m in range(5)]),
    ]
    out = []
    for label, k, edges in cases:
        universe = {tuple(sorted(e)) for e in edge_universe(k)}
        assert all(tuple(sorted(e)) in universe for e in edges), label
        assert len({tuple(sorted(e)) for e in edges}) == len(edges), label
        out.append((label, k, edges))
    return out


# --------------------------------------------------------------------- modes
def mode_alignment():
    """Ordering / canonicalization claims the bit semantics depends on."""
    lib = json.loads(LIBRARY.read_text())
    fan = json.loads(FAN.read_text())
    cells = json.loads(CELLS.read_text())
    orders = dict(
        bridge=[list(p) for p in PATTERN_ORDER],
        production=[list(p) for p in prod.REPS],
        boundary_library=lib['pattern_order'],
        fan_pentagon=fan['pattern_order'],
        cells_json=cells['pattern_order'],
    )
    return dict(patterns=orders,
                all_identical=all(v == orders['bridge'] for v in orders.values()),
                canonicalization=canon_agrees(),
                universe_k2=[list(e) for e in edge_universe(2)],
                universe_k2_matches_production=prod.edge_universe(2) == edge_universe(2),
                universe_k5_matches_cells_json=[list(e) for e in edge_universe(5)] == cells['edge_universe'])


def mode_cases(with_product=False):
    rows = []
    for label, k, edges in case_list():
        row = compare(k, edges, label)
        if with_product:
            row['ref_bits_full_product'] = ref_bits_product(k, edges)
            row['match'] = row['match'] and row['ref_bits_full_product'] == row['prod_bits']
        rows.append(row)
    return rows


def mode_catalogue(check_planarity=True):
    data = json.loads(CELLS.read_text())
    assert [list(p) for p in PATTERN_ORDER] == data['pattern_order']
    rows, k_effs = [], {}
    for key, cell in sorted(data['cells'].items(), key=lambda kv: int(kv[0])):
        k, edges = cell['k_eff'], [tuple(e) for e in cell['edges']]
        row = compare(k, edges, f'catalogue bits={key}')
        row['stored_bits'] = int(key)
        row['stored_bits_match'] = int(key) == row['prod_bits'] == row['ref_bits']
        row['match'] = row['match'] and row['stored_bits_match']
        if check_planarity:
            row['apex_planar'] = apex_planar(k, edges)
        rows.append(row)
        k_effs[int(key)] = k
    nested = {level: sum(1 for k in k_effs.values() if k <= level) for level in range(6)}
    new = {level: nested[level] - nested.get(level - 1, 0) for level in nested}
    return dict(rows=rows, mismatches=[r['label'] for r in rows if not r['match']],
                nested_by_k_eff={str(a): b for a, b in nested.items()},
                nested_matches_stored=all(data['nested_by_k_eff'][str(a)] == b for a, b in nested.items()),
                new_by_k_eff={str(a): b for a, b in new.items()},
                new_matches_stored=all(data['new_sigma_by_k_eff'][str(a)] == b for a, b in new.items()),
                distinct_sigma_recomputed=len(k_effs), distinct_sigma_stored=data['distinct_sigma'],
                cells_sha256=hashlib.sha256(CELLS.read_bytes()).hexdigest())


def apex_planar(k, edges):
    """Is C5 ∪ interior a disk patch (C5 a face once an apex joins all five)?"""
    import networkx as nx
    g = nx.Graph(list(CYCLE) + [tuple(e) for e in edges] + [(5 + k, i) for i in range(5)])
    planar, _ = nx.check_planarity(g)
    return bool(planar)


def dfs_sweep(k, jobs=1, sample=0, orbit_sample=200, log=print):
    """Run the production DFS itself and compare accepted nodes with Σ.

    Every accepted node is an edge set the enumerator deems a cell candidate.  Bitwise
    comparison uses `ref_bitwise` (ten independent feasibility tests).  A prefix of the
    nodes is additionally compared with `ref_bits` and checked for S4 orbit invariance,
    which is what licenses the ten-orbit compression in the first place.
    """
    prod_setup(k, force=True)
    stride = sample if sample else 1
    state = dict(accepted=0, checked=0, masks=set(), mismatches=[], orbit_checked=0, orbit_fail=[])
    keep_masks = sample == 0
    MASK_CAP = 1 << 20

    def spy(mask, surviving, per_sigma):
        probe = {}
        REAL_RECORD(mask, surviving, probe)          # production bit encoder
        got = next(iter(probe))
        REAL_RECORD(mask, surviving, per_sigma)      # the real recording, unchanged
        state['accepted'] += 1
        n = state['accepted']
        if n % stride:
            return
        state['checked'] += 1
        if keep_masks and len(state['masks']) < MASK_CAP:
            state['masks'].add(mask)
        edges = edges_of(k, mask)
        by_bit = ref_bitwise(k, edges)
        if got != by_bit:
            state['mismatches'].append(dict(mask=mask, prod_bits=got, ref_bits_per_bit=by_bit,
                                            edges=[list(e) for e in edges]))
        if state['orbit_checked'] < orbit_sample:
            state['orbit_checked'] += 1
            if ref_bits(k, edges) != by_bit:
                state['orbit_fail'].append(dict(mask=mask, reason='orbit union differs'))
            elif not all(orbit_invariance(k, edges, j) for j in range(10)):
                state['orbit_fail'].append(dict(mask=mask, reason='orbit not rename-invariant'))

    prod._record = spy
    try:
        _, per_sigma, stats = prod.enumerate_cells(k, jobs=jobs, log=log)
    finally:
        prod._record = REAL_RECORD
    return dict(k=k, edge_universe=len(edge_universe(k)), accepted_nodes=state['accepted'],
                checked=state['checked'], sampled=bool(sample),
                distinct_masks=len(state['masks']) if keep_masks else None,
                distinct_masks_capped=keep_masks and len(state['masks']) >= MASK_CAP,
                distinct_sigmas=len(per_sigma), orbit_checked=state['orbit_checked'],
                orbit_failures=state['orbit_fail'][:20], search=stats,
                mismatches=state['mismatches'][:20], mismatch_count=len(state['mismatches']))


def mode_all_masks(k, log=print, report_every=1 << 21):
    """Every graph on U(k), planarity aside: all 2^|U(k)| edge subsets, mask vs Σ.

    This is stronger than the DFS sweep (which only sees apex-planar prefixes) and
    weaker in k, since 2^40 is out of reach; it exists to close k ≤ 3 completely.
    """
    w = prod_setup(k, force=True)
    universe = w['edges']
    total = 1 << len(universe)
    mismatches, checked = [], 0
    for mask in range(total):
        got = prod_bits(k, mask)
        ref = ref_bitwise(k, [universe[j] for j in range(len(universe)) if mask >> j & 1])
        checked += 1
        if got != ref:
            mismatches.append(dict(mask=mask, prod_bits=got, ref_bits_per_bit=ref,
                                   edges=[list(e) for e in edges_of(k, mask)]))
        if report_every and mask and mask % report_every == 0:
            log(f"  all-masks k={k}: {mask}/{total} graphs, {len(mismatches)} mismatches")
    return dict(k=k, edge_universe=len(universe), graphs=total, checked=checked,
                mismatches=mismatches[:20], mismatch_count=len(mismatches))


def mode_random(count=60, seed=7):
    """Random graphs: cross-validate the three reference readings against production."""
    rng = random.Random(seed)
    rows = []
    for i in range(count):
        k = rng.choice([0, 1, 2, 3])
        universe = edge_universe(k)
        edges = [e for e in universe if rng.random() < rng.choice([0.15, 0.3, 0.5])]
        row = compare(k, edges, f'random#{i} k={k}')
        row['ref_bits_full_product'] = ref_bits_product(k, edges)
        row['match'] = row['match'] and row['ref_bits_full_product'] == row['prod_bits']
        rows.append(row)
    return dict(rows=rows, mismatches=[r['label'] for r in rows if not r['match']])


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--cases', action='store_true', help='curated extreme cases')
    parser.add_argument('--catalogue', action='store_true', help='all stored k<=5 witnesses')
    parser.add_argument('--dfs', type=int, action='append', default=[],
                        help='exhaustive DFS sweep at this k (repeatable)')
    parser.add_argument('--all-masks', type=int, action='append', default=[],
                        help='check every one of the 2^|U(k)| edge subsets (repeatable, k<=3)')
    parser.add_argument('--sample', type=int, default=0, help='compare every N-th DFS node')
    parser.add_argument('--stride', action='append', default=[], metavar='K=N',
                        help='per-k DFS stride, overrides --sample for that k (repeatable)')
    parser.add_argument('--orbit-sample', type=int, default=200,
                        help='nodes per k checked for S4 orbit invariance / orbit-level Σ')
    parser.add_argument('--seed', type=int, default=1)
    parser.add_argument('--random', type=int, default=0, help='random reference cross-checks')
    parser.add_argument('--product', action='store_true', help='also brute force 4^(5+k) per case')
    parser.add_argument('--jobs', type=int, default=1, help='jobs for the DFS sweep (capture needs 1)')
    parser.add_argument('--no-planarity', action='store_true')
    parser.add_argument('--quick', action='store_true',
                        help='fast routine preset: cases + catalogue + random + all-masks 0..2 + dfs 2,3')
    parser.add_argument('--out', type=Path,
                        default=None, help='report path (default: sigma_bridge.json, or '
                                           'sigma_bridge_quick.json for --quick)')
    parser.add_argument('--quiet', action='store_true')
    args = parser.parse_args()
    log = (lambda *a, **kw: None) if args.quiet else print

    if args.quick:
        args.cases = args.catalogue = args.product = True
        args.random = args.random or 30
        args.all_masks = sorted(set(args.all_masks) | {0, 1, 2})
        args.dfs = sorted(set(args.dfs) | {2, 3})

    if not (args.cases or args.catalogue or args.dfs or args.random or args.all_masks):
        args.cases = args.catalogue = True

    strides = {}
    for item in args.stride:
        key, _, value = item.partition('=')
        strides[int(key)] = int(value)

    report = dict(spec=dict(
        colours=COLOUR_COUNT, cycle=[list(e) for e in CYCLE], chords=[list(e) for e in CHORDS],
        pattern_order=[list(p) for p in PATTERN_ORDER],
        bit_meaning='bit j = 1 iff orbit PATTERN_ORDER[j] has a proper extension to the sealed interior',
        canonicalization='orbit_rep = least global S4 renaming; D5 acts only at composition time'),
        status='computationally verified (finite domains listed below); not a Lean proof')
    report['alignment'] = mode_alignment()
    ok = (report['alignment']['all_identical']
          and report['alignment']['canonicalization']['proper_agree']
          and report['alignment']['universe_k2_matches_production']
          and report['alignment']['universe_k5_matches_cells_json'])
    log(f"alignment: all pattern orders identical = {report['alignment']['all_identical']}, "
        f"orbit_rep == normalize = {report['alignment']['canonicalization']['proper_agree']}")

    if args.cases:
        rows = mode_cases(with_product=args.product)
        report['cases'] = dict(rows=rows, mismatches=[r['label'] for r in rows if not r['match']])
        ok &= not report['cases']['mismatches']
        log(f"cases: {len(rows)} graphs, {len(report['cases']['mismatches'])} mismatches")

    if args.random:
        report['random'] = mode_random(args.random, seed=args.seed)
        ok &= not report['random']['mismatches']
        log(f"random: {len(report['random']['rows'])} graphs (seed {args.seed}), "
            f"{len(report['random']['mismatches'])} mismatches")

    if args.catalogue:
        cat = mode_catalogue(check_planarity=not args.no_planarity)
        report['catalogue'] = cat
        ok &= not cat['mismatches'] and cat['nested_matches_stored'] and cat['new_matches_stored']
        log(f"catalogue: {len(cat['rows'])} cells, {len(cat['mismatches'])} mismatches, "
            f"nested={cat['nested_by_k_eff']} (stored match: {cat['nested_matches_stored']})")

    if args.dfs and args.jobs != 1:
        parser.error('the DFS capture is in-process: run the sweep with --jobs 1 '
                     '(a worker pool would silently return an unchecked sweep)')

    if args.all_masks:
        report['all_masks'] = []
        for k in sorted(set(args.all_masks)):
            res = mode_all_masks(k, log=log)
            report['all_masks'].append(res)
            ok &= not res['mismatches']
            log(f"all-masks k={k}: {res['checked']}/{res['graphs']} graphs, "
                f"{res['mismatch_count']} mismatches")

    if args.dfs:
        report['dfs'] = []
        for k in sorted(set(args.dfs)):
            res = dfs_sweep(k, jobs=args.jobs, sample=strides.get(k, args.sample),
                            orbit_sample=args.orbit_sample, log=log)
            report['dfs'].append(res)
            ok &= not res['mismatches'] and not res['orbit_failures']
            log(f"dfs k={k}: accepted={res['accepted_nodes']} checked={res['checked']} "
                f"orbit_checked={res['orbit_checked']} distinct_sigma={res['distinct_sigmas']} "
                f"mismatches={res['mismatch_count']} orbit_failures={len(res['orbit_failures'])}")

    domains = []
    if 'all_masks' in report:
        for res in report['all_masks']:
            domains.append(f"k={res['k']}: every one of the {res['graphs']} edge subsets of U({res['k']}); "
                           f"{res['mismatch_count']} mismatches")
    if 'dfs' in report:
        for res in report['dfs']:
            domains.append(f"k={res['k']}: {res['checked']} of {res['accepted_nodes']} DFS-accepted "
                           f"graphs ({'sampled' if res['sampled'] else 'exhaustive'}); "
                           f"{res['mismatch_count']} mismatches")
    if 'catalogue' in report:
        domains.append(f"k<=5: all {len(report['catalogue']['rows'])} catalogue witnesses; "
                       f"{len(report['catalogue']['mismatches'])} mismatches")
    if 'cases' in report:
        domains.append(f"curated: {len(report['cases']['rows'])} hand-built graphs; "
                       f"{len(report['cases']['mismatches'])} mismatches")
    if 'random' in report:
        domains.append(f"random: {len(report['random']['rows'])} graphs, reference cross-checked "
                       f"against full 4^(5+k) enumeration; {len(report['random']['mismatches'])} mismatches")
    report['domains'] = domains
    report['answer'] = ('yes: on every domain checked here the production ten-bit mask equals '
                        'the specification Σ bit by bit') if ok else 'NO — mismatch found'
    report['all_checks_passed'] = bool(ok)
    out = args.out or (QUICK_REPORT if args.quick else REPORT)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=1) + '\n')
    log(f"answer: {report['answer']}\nreport: {out}")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
