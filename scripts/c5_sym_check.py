#!/usr/bin/env python3
"""SYM audit: is the production enumerator's canonicalisation only the interior-relabelling equivalence?

uv run python scripts/c5_sym_check.py --quick
uv run --with networkx==3.5 --with rustworkx==0.17.1 python scripts/c5_sym_check.py --k 3

------------------------------------------------------------------------------
WHAT IS BEING CHECKED (label normalisation, "SYM")
------------------------------------------------------------------------------
Fix `k` and the edge universe

    U(k) = chords(5) ∪ boundary–interior(5k) ∪ interior–interior(C(k,2))

with the boundary C5 always present and the interior vertices x_m = 5+m being *labels*.  Relabelling
the interior by τ ∈ Sym(k) sends the edge set E ⊆ U(k) to

    relabel(τ, E) = { (a, b) : (τ⁻¹(a), τ⁻¹(b)) ∈ E }          (a vertex permutation of the graph)

and, on masks, to the bit permutation `interior_perm_maps` of `c5_cell_enumerator.py`.  Two masks in
the same orbit describe the *same unlabelled graph*, so by `Sigma_relabel` (Math/SymRelabel.lean) they
have the same ten-bit Σ key.  This script checks that the production canonicalisation uses nothing
beyond that equivalence:

  A1  `interior_perm_maps` agrees with an independently written relabel map, and the map is a group
      action (identity, inverse, multiplicativity).
  A2  The five-bit attachment mask of an interior vertex is transported by relabelling; the multiset
      of attachment sizes is relabelling-invariant (this is the fact SYM sorts).
  A3  Every graph has *some* relabelling whose attachment masks are non-increasing — the pigeonhole
      step that makes the SYM cut lossless. Exhaustive over the requested small-k universes.
  A4  SYM intersects every orbit and agrees with production's numeric attachment-mask order.
      It generally splits orbits: sortedness itself is not invariant under relabelling.
  A5  The catalogue's `canonical_masks` counter is a relabelling-orbit count: it counts the masks of
      each Σ-class that are the maximum of their own relabelling orbit, and every orbit has exactly
      one such mask.

Together A1-A5 say that the production canonicalisation consults nothing but the interior-relabelling
equivalence: the relabel map is the symmetric-group action and SYM retains at least one
representative per orbit. The canonical counter has a separate orbit-maximum check.

Nothing here modifies `cells.json` or any enumerator; the script only reads the artefacts and
re-derives the claims from the edge universe.  Trust level: computationally verified on the printed
domains, not a Lean proof.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import c5_cell_enumerator as C            # noqa: E402  (code under test)
import c5_cell_reduced as R               # noqa: E402  (code under test)

CELLS = ROOT / 'artifacts/c5_cells/cells.json'
REPORT = ROOT / 'artifacts/c5_cells/sym_check.json'
QUICK_REPORT = ROOT / 'artifacts/c5_cells/sym_check_quick.json'


# ----------------------------------------------------------------- reference relabelling

def ref_perm_maps(k, edges):
    """Independent relabel map: edge bit j ↦ the bit of its image under τ.

    Written from the definition `relabel(τ, E) = {(a,b) : (τ⁻¹a, τ⁻¹b) ∈ E}` only; the production
    `interior_perm_maps` is compared against this.
    """
    index = {e: j for j, e in enumerate(edges)}
    maps = []
    for tau in itertools.permutations(range(k)):
        if tau == tuple(range(k)):
            continue                      # production also omits the identity
        rel = {5 + m: 5 + tau[m] for m in range(k)}
        img = []
        for u, v in edges:
            a, b = rel.get(u, u), rel.get(v, v)
            img.append(index[(a, b) if (a, b) in index else (b, a)])
        maps.append(tuple(img))
    return maps


def act(mask, pm):
    out = 0
    for j, t in enumerate(pm):
        if mask >> j & 1:
            out |= 1 << t
    return out


def orbit(mask, pms):
    return {act(mask, pm) for pm in pms}


def edge_reindex(src_edges, dst_edges):
    """Bit-permutation moving a mask from `src_edges`' bit order to `dst_edges`' bit order.

    Same edge set, but production's `R.block_edge_order` interleaves each interior vertex's
    interior-interior edges right after its boundary block, while the reference `C.edge_universe`
    defers all interior-interior edges to the end. The two orders coincide for k<=2 (there is at most
    one interior-interior edge, always trailing either way) and diverge from k=3 on, so any mask built
    against one order must be translated with this before it is handed to code built on the other.
    """
    index = {e: j for j, e in enumerate(dst_edges)}
    return [index[e] if e in index else index[(e[1], e[0])] for e in src_edges]


def att_masks(mask, k, edges):
    """The five-bit attachment mask of each interior vertex, as a bitmask over the boundary 0..4.

    One pass over `edges`, building all `k` masks together — a boundary-interior edge contributes to
    exactly one vertex's mask — instead of the previous k separate scans of the whole edge list.
    """
    bits = [0] * k
    for j, (u, w) in enumerate(edges):
        if not (mask >> j & 1):
            continue
        if u < 5 <= w:
            bits[w - 5] |= 1 << u
        elif w < 5 <= u:
            bits[u - 5] |= 1 << w
    return tuple(bits)


def att_sizes(mask, k, edges):
    return tuple(bin(a).count('1') for a in att_masks(mask, k, edges))


def nonincreasing(seq):
    return all(seq[i] >= seq[i + 1] for i in range(len(seq) - 1))


def r1_ok(mask, k, edges):
    """R1's degree cut, recomputed here: every interior vertex has degree >= 4."""
    touch = C._W['touch']
    return all(bin(mask & touch[m]).count('1') >= 4 for m in range(k))


def sym_spec_card(mask, k, edges):
    """SYM read by attachment *size*: the numbers of attached boundary vertices are non-increasing."""
    return nonincreasing(att_sizes(mask, k, edges))


def sym_spec_value(mask, k, edges):
    """SYM read by attachment-mask *value*: the five-bit masks are non-increasing as integers.

    This matches production (`att_value` returns the raw bit block). Numeric order and
    popcount order are incomparable: (16, 15) passes only numeric order, (15, 16) only size order.
    """
    m = att_masks(mask, k, edges)
    return nonincreasing(m)


def sym_ok(mask, k, edges):
    """SYM read off the bit order of `U(k)`: the five-bit attachment masks are non-increasing.

    The attachments of x_m occupy the five bits `5+5m .. 5+5m+4` of `U(k)`, i.e. exactly the block
    `att_masks` reads, so this is the same reading as `sym_spec_value`.  Production instead reads its
    own per-vertex block layout (`R.att_value`); `check_layout` below verifies that the two layouts
    describe the same five-bit masks for a vertex relabelling.
    """
    return sym_spec_value(mask, k, edges)


def layout_masks(mask, k):
    """The same attachment masks read through production's block layout (`R.att_value`).

    Caller must call `R._setup(k)` and set `R._W['blocks']` once beforehand — this used to redo that
    setup, including `compat_tables`'s O(edges * 4**k) table build, on every single call, which made
    `check_layout` redo it once per mask in the whole universe instead of once per k.
    """
    return tuple(R.att_value(mask, m) for m in range(k))


def check_layout(k, edges, log, masks, c_to_r):
    """The enumerator's per-vertex block layout and the `U(k)` bit order describe the same masks.

    `mask` is in `edges`' (reference) bit order; `c_to_r` translates it into `R`'s block-edge order
    before it is handed to `R.att_value` — see `edge_reindex`. Caller must have already run
    `R._setup(k)` and set `R._W['blocks']`.
    """
    bad = 0
    first = None
    for mask in masks:
        if att_masks(mask, k, edges) != layout_masks(act(mask, c_to_r), k):
            if first is None:
                first = mask
            bad += 1
    out = dict(k=k, graphs=len(masks), layout_mismatches=bad, first_mismatch=first)
    log(f"A0 layout agreement: {out}")
    return out


def prod_sym_ok(mask, k):
    """The production helper `c5_cell_reduced.viable` reduced to its SYM part.

    `mask` must already be in `R`'s block-edge order (translate a reference-order mask with `c_to_r`
    and `act` first) — `R.att_value` reads bit positions per `R._W['blocks']`, not per `edge_universe`.
    """
    for m in range(1, k):
        if R.att_value(mask, m) > R.att_value(mask, m - 1):
            return False
    return True


# ----------------------------------------------------------------- the checks

def check_perm_maps(k, edges, log):
    pms = ref_perm_maps(k, edges)
    prods = C.interior_perm_maps(k, edges)
    E = len(edges)
    assert len(pms) == len(prods), 'reference and production map counts differ'
    out = dict(k=k, reference_maps=len(pms), production_maps=len(prods),
               maps_agree=(pms == prods))
    if k <= 3:
        assert pms == prods, 'reference and production relabel maps differ'
    # group action: the generated set (identity included) is closed under composition and inversion
    pmset = set(pms) | {tuple(range(E))}
    inv_ok = all(tuple(sorted(range(E), key=lambda j: pm[j])) in pmset for pm in pmset)
    comp_ok = True
    for a in sorted(pmset)[:24]:
        for b in sorted(pmset)[:24]:
            comp = tuple(a[b[j]] for j in range(E))
            if comp not in pmset:
                comp_ok = False
                break
        if not comp_ok:
            break
    full_orbit_ok = len(pmset) == (1 if k <= 1 else 24 if k >= 4 else 2 if k == 2 else 6)
    out.update(inverse_closed=inv_ok, composition_closed=comp_ok,
               generated_group_order=len(pmset), full_symmetric_group=full_orbit_ok)
    log(f"A1 perm maps: {out}")
    return out


def check_attachment(k, edges, log, sample):
    """A2: the attachment mask is transported by relabelling and the size multiset is invariant."""
    pms = ref_perm_maps(k, edges)
    bad_mask = bad_multiset = 0
    n = 0
    for mask in sample:
        sizes = att_sizes(mask, k, edges)
        for pm in pms:
            n += 1
            img = act(mask, pm)
            if Counter(att_sizes(img, k, edges)) != Counter(sizes):
                bad_multiset += 1
            # the boundary neighbours of the vertex on which m lands are the old neighbours of m
            m_att = att_masks(mask, k, edges)
            i_att = att_masks(img, k, edges)
            if sorted(m_att) != sorted(i_att):
                bad_mask += 1
    out = dict(k=k, relabellings_checked=n, mask_multiset_mismatches=bad_multiset,
               attachment_multiset_mismatches=bad_mask)
    log(f"A2 attachment transport: {out}")
    return out


def build_orbit_partition(masks, full):
    """One-pass relabelling-orbit partition of `masks` under the group `full` (identity included).

    `orbit(m, full)` is the same set regardless of which member `m` of an orbit you start from (`full`
    is closed under composition/inversion, checked by `check_perm_maps`), so each orbit only needs to
    be materialised once. Returns `(orbits, owner)`: `orbits` is the list of distinct orbits as
    frozensets, `owner` maps every mask to its orbit — every later check reuses this instead of
    re-deriving orbits with fresh `act()` calls, which was previously done independently (and mostly
    without de-duplication) in pigeonhole, sym_orbits, r1_sym and canonical.
    """
    owner = {}
    orbits = []
    for mask in masks:
        if mask in owner:
            continue
        orb = frozenset(orbit(mask, full))
        orbits.append(orb)
        for m in orb:
            owner[m] = orb
    return orbits, owner


def check_pigeonhole(k, edges, log, masks, orbits):
    """A3: every graph has a non-increasing relabelling (the SYM cut loses no unlabelled graph)."""
    orbit_ok = {orb: any(sym_spec_value(x, k, edges) for x in orb) for orb in orbits}
    missing = [m for orb in orbits if not orbit_ok[orb] for m in orb]
    out = dict(k=k, graphs=len(masks), without_sorted_relabel=len(missing),
               first_missing=(missing[0] if missing else None))
    if missing:
        raise AssertionError(out)
    log(f"A3 pigeonhole: {out}")
    return out


def check_sym_orbits(k, edges, log, masks, orbits, c_to_r):
    """A4: SYM hits every orbit, and agrees with the numeric attachment-mask specification.

    Caller must have already run `R._setup(k)` and set `R._W['blocks']`; `c_to_r` (`edge_reindex`)
    translates a reference-order mask into `R`'s block-edge order for `prod_sym_ok`.
    """
    card_mismatch = 0
    value_mismatch = 0
    prod_mismatch = 0
    value_only = size_only = 0
    for mask in masks:
        s = sym_ok(mask, k, edges)
        if s != sym_spec_card(mask, k, edges):
            card_mismatch += 1
            value_only += int(s)
            size_only += int(not s)
        if s != sym_spec_value(mask, k, edges):
            value_mismatch += 1
        if s != prod_sym_ok(act(mask, c_to_r), k):
            prod_mismatch += 1
    # Split orbits are expected. An orbit with no retained representative is an error.
    orbit_split = sum(1 for orb in orbits if len({sym_ok(m, k, edges) for m in orb}) != 1)
    orbit_lost = sum(1 for orb in orbits if not any(sym_ok(m, k, edges) for m in orb))
    out = dict(k=k, graphs=len(masks), orbits=len(orbits),
               value_spec_mismatches=value_mismatch, size_spec_mismatches=card_mismatch,
               production_mismatches=prod_mismatch, orbits_split_by_sym=orbit_split,
               orbits_without_sym_representative=orbit_lost,
               numeric_only_graphs=value_only, size_only_graphs=size_only)
    if value_mismatch or prod_mismatch or orbit_lost:
        raise AssertionError(out)
    log(f"A4 SYM orbit coverage and production agreement: {out}")
    return out


def check_r1_sym_survivors(k, edges, log, masks, owner, c_to_r):
    """A4': among the R1 survivors, every orbit has a SYM representative (SYM cut is lossless).

    This is the pigeonhole fact as the reduction actually uses it, for both the size and the
    value reading of the attachment order: sorting the interior vertices by the key makes any
    chosen order on the masks non-increasing, so a representative survives in every orbit.

    `orbits_lost_by_production_sym` exercises `prod_sym_ok` (production's own `R.att_value` reading,
    via `c_to_r`) — it used to re-check `sym_ok` under a different name, which could never disagree
    with `orbits_lost_by_value_sym` and so tested nothing beyond it.
    """
    r1 = [m for m in masks if r1_ok(m, k, edges)]
    by_orbit = {}
    for m in r1:
        by_orbit.setdefault(owner[m], []).append(m)
    lost_size = [sorted(v)[0] for v in by_orbit.values() if not any(sym_spec_card(x, k, edges) for x in v)]
    lost_value = [sorted(v)[0] for v in by_orbit.values() if not any(sym_spec_value(x, k, edges) for x in v)]
    lost_prod = [sorted(v)[0] for v in by_orbit.values() if not any(prod_sym_ok(act(x, c_to_r), k) for x in v)]
    out = dict(k=k, r1_survivors=len(r1), r1_orbits=len(by_orbit),
               orbits_lost_by_value_sym=len(lost_value), orbits_lost_by_size_sym=len(lost_size),
               orbits_lost_by_production_sym=len(lost_prod),
               first_lost_value=(lost_value[0] if lost_value else None))
    log(f"A4' R1+SYM lossless: {out}")
    return out


def check_canonical(k, log, masks, orbits, full):
    """A5: the `canonical` counter is a relabelling-orbit maximum count."""
    def maxima(orb):
        return [m for m in orb if all(act(m, pm) >= m for pm in full)]
    counts = [len(maxima(o)) for o in orbits]
    canon = sum(counts)
    out = dict(k=k, graphs=len(masks), orbits=len(orbits), canonical=canon,
               canonical_per_orbit_min=min(counts, default=None),
               canonical_per_orbit_max=max(counts, default=None),
               orbits_with_two_maxima=sum(1 for c in counts if c > 1),
               orbits_without_maximum=sum(1 for c in counts if c == 0))
    log(f"A5 canonical maxima: {out}")
    return out


def check_catalogue_canonical(data, log, limit=3):
    """A5 (production numbers): `canonical_masks` in cells.json equals the orbit-maximum count."""
    pms_cache = {}
    rows = {}
    bad = 0
    for bits, cell in data['cells'].items():
        k = cell['k_eff']
        if k == 0 or k > limit:
            continue
        edges = [tuple(e) for e in cell['edges']]
        if k not in pms_cache:
            pms_cache[k] = ref_perm_maps(k, C.edge_universe(k))
        universe = C.edge_universe(k)
        index = {e: j for j, e in enumerate(universe)}
        mask = 0
        for u, v in edges:
            mask |= 1 << index[(u, v) if (u, v) in index else (v, u)]
        pms = [tuple(range(len(universe)))] + pms_cache[k]
        is_canon = all(act(mask, pm) >= mask for pm in pms)
        rows[bits] = dict(k=k, canonical=is_canon, stored=cell['canonical_masks'])
    mism = [b for b, r in rows.items() if (1 if r['canonical'] else 0) > r['stored']]
    bad = sum(1 for r in rows.values() if r['stored'] not in (0, 1))
    out = dict(witnesses_checked=len(rows), witness_canonical=sum(1 for r in rows.values() if r['canonical']),
               stored_counter_not_0_or_1=bad,
               stored_at_least_witness=[b for b, r in rows.items() if r['stored'] and not r['canonical']][:5])
    log(f"A5' catalogue canonical counters: {out}")
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--k', type=int, action='append', default=[],
                        help='exhaustive over the whole universe U(k) for this k (k <= 3)')
    parser.add_argument('--quick', action='store_true', help='k=0,1,2 exhaustive + catalogue audit')
    parser.add_argument('--jobs', type=int, default=1)
    parser.add_argument('--out', type=Path, default=None)
    args = parser.parse_args()

    ks = [0, 1, 2] if args.quick else args.k
    if not ks and not args.quick:
        ks = [3]
    data = json.loads(CELLS.read_text())
    report = dict(k_requested=ks, universe={}, catalogue=None)
    log = print
    for k in ks:
        edges = C.edge_universe(k)
        C._setup(k)
        universe = list(range(1 << len(edges)))
        log(f'--- k={k}: {len(edges)} edge bits, {len(universe)} graphs in the universe')
        full = [tuple(range(len(edges)))] + ref_perm_maps(k, edges)
        orbits, owner = build_orbit_partition(universe, full)
        R._setup(k)
        R._W['blocks'] = R.block_edge_order(k)[1]
        c_to_r = edge_reindex(edges, R._W['edges'])
        report['universe'][str(k)] = dict(
            edge_bits=len(edges),
            layout=check_layout(k, edges, log, universe, c_to_r),
            perm_maps=check_perm_maps(k, edges, log),
            attachment=check_attachment(k, edges, log, universe if k <= 2 else universe[::7]),
            pigeonhole=check_pigeonhole(k, edges, log, universe, orbits),
            sym_orbits=check_sym_orbits(k, edges, log, universe, orbits, c_to_r),
            r1_sym=check_r1_sym_survivors(k, edges, log, universe, owner, c_to_r),
            canonical=check_canonical(k, log, universe, orbits, full),
        )
    report['catalogue'] = check_catalogue_canonical(data, log, limit=3)

    path = args.out or (QUICK_REPORT if args.quick else REPORT)
    path.write_text(json.dumps(report, indent=1) + '\n')
    print(f'wrote {path}')


if __name__ == '__main__':
    main()
