#!/usr/bin/env python3
"""First trial run for docs/stepwise_state_sufficiency.md on the C5 test bed.

python scripts/stepwise_sufficiency.py            # writes artifacts/stepwise/first_run.json

Scope of this run (all choices are recorded in the output):
  * inside patch      = one of the 87 disk patches in artifacts/fan_pentagon/states.json
  * continuation X    = another patch of the same family glued from outside along the
                        C5, with any of the 10 dihedral alignments of the boundary
  * history H         = (inside patch, colours already committed to b0..b_{n-1})
  * "H + X completable" = the ring colouring extends to a proper 4-colouring of the glued
                        graph, decided exactly from the two boundary relations
                        (some completion of the prefix lies in Sigma_in meet Sigma_out)
  * stepwise tree     = colour b0, b1, b2, b3, b4 one at a time, forward only, no
                        recolouring.

Sigma of every patch is recomputed here from its edge list and cross-checked against the
stored bits. Everything is colour-semantics only: planarity of the glued graph is not
re-verified beyond the recorded apex evidence of each patch.
"""
from collections import Counter, defaultdict
from itertools import combinations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FAN = ROOT / 'artifacts/fan_pentagon'
OUT = ROOT / 'artifacts/stepwise'
RING = 5


def normalize(pattern):
    names = {}
    return tuple(names.setdefault(c, len(names)) for c in pattern)


def sigma_from_edges(edges):
    """Exact boundary relation: normalized C5 patterns extendable to the interior."""
    adj = defaultdict(set)
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    interior = sorted(v for v in adj if v >= RING)
    accepted = set()
    for pattern in set(normalize(p) for p in product(range(4), repeat=RING)):
        colour = dict(enumerate(pattern))

        def extend(i):
            if i == len(interior):
                return True
            v = interior[i]
            for c in range(4):
                if all(colour.get(w) != c for w in adj[v]):
                    colour[v] = c
                    if extend(i + 1):
                        return True
                    del colour[v]
            return False

        if all(colour[u] != colour[v] for u, v in edges if u < RING and v < RING) and extend(0):
            accepted.add(pattern)
    return frozenset(accepted)


def dihedral():
    rot = [tuple((i + k) % RING for i in range(RING)) for k in range(RING)]
    return rot + [tuple((-i) % RING for i in g) for g in rot]


def align(sigma, g):
    """Outside patch whose port g[i] sits on ring position i."""
    return frozenset(normalize(tuple(p[g[i]] for i in range(RING))) for p in sigma)


def canonical(value):
    """Order-independent key: frozensets are sorted, tuples recursed."""
    if isinstance(value, frozenset):
        return ('set',) + tuple(sorted(canonical(v) for v in value))
    if isinstance(value, tuple):
        return tuple(canonical(v) for v in value)
    return value


class Bits:
    """Relations and prefix-completion sets as bitmasks over the ordered pattern list."""

    def __init__(self, pattern_order):
        self.order = pattern_order
        self.index = {p: j for j, p in enumerate(pattern_order)}
        self.prefixes = {n: sorted(set(normalize(p) for p in product(range(4), repeat=n)))
                         for n in range(1, RING)}
        self.completion = {}
        for n, ps in self.prefixes.items():
            for p in ps:
                mask = 0
                for rest in product(range(4), repeat=RING - n):
                    full = normalize(p + rest)
                    if full in self.index:
                        mask |= 1 << self.index[full]
                self.completion[p] = mask

    def mask(self, sigma):
        return sum(1 << self.index[p] for p in sigma)


def three_profile(sigma):
    return frozenset(p for p in sigma if max(p) <= 2)


def compressions(sigma):
    return {
        'sigma': sigma,
        'size': len(sigma),
        'three_profile': three_profile(sigma),
        'pairs': tuple(frozenset(normalize((p[i], p[j])) for p in sigma)
                       for i, j in combinations(range(RING), 2)),
        'all_windows': tuple(frozenset(normalize((p[i - 1], p[i], p[(i + 1) % RING])) for p in sigma)
                             for i in range(RING)),
        'windows+three': (tuple(frozenset(normalize((p[i - 1], p[i], p[(i + 1) % RING])) for p in sigma)
                                for i in range(RING)), three_profile(sigma)),
    }


# ---------- part A: uncoloured whole history (patch only) ----------

def part_a(sigmas, aligned):
    """Is 'glued graph 4-colourable' ever false?  (Expected never: the union is planar.)"""
    completable = sum(bool(s & out) for s in sigmas for out in aligned.values())
    return dict(pairs=len(sigmas) * len(aligned), completable=completable,
                note='an uncoloured inside patch can never be distinguished from another by a '
                     'planar outside patch: every glued graph is planar, hence 4-colourable')


# ---------- part B: coloured prefix, fixed outside ----------

def part_b(bits, in_masks, out_masks):
    """Compressions of the inside relation, tested against coloured prefixes.

    Two inside patches with the same compressed state but different Sigma: is there a
    prefix colouring and an outside patch where one extends and the other does not?
    """
    report = {}
    comp = [compressions(s) for s in in_masks['sigmas']]
    outs = list(out_masks.items())
    for name in comp[0]:
        classes = defaultdict(list)
        for k, c in enumerate(comp):
            classes[canonical(c[name])].append(k)
        conflicting = [(a, b) for cls in classes.values() for a, b in combinations(cls, 2)
                       if in_masks['masks'][a] != in_masks['masks'][b]]
        distinguished, undistinguished, example, depth_hist = 0, [], None, Counter()
        for a, b in conflicting:
            ma, mb = in_masks['masks'][a], in_masks['masks'][b]
            found = None
            for n in range(1, RING):
                for p in bits.prefixes[n]:
                    cp = bits.completion[p]
                    for (x, g), out in outs:
                        wa, wb = bool(cp & ma & out), bool(cp & mb & out)
                        if wa != wb:
                            found = dict(depth=n, prefix=p, inside_ok=a if wa else b,
                                         inside_dead=b if wa else a, outside=x, alignment=g)
                            break
                    if found:
                        break
                if found:
                    break
            if found:
                distinguished += 1
                depth_hist[found['depth']] += 1
                example = example or found
            else:
                undistinguished.append((a, b))
        report[name] = dict(classes=len(classes), pairs_same_state_different_sigma=len(conflicting),
                            distinguished=distinguished, not_distinguished=len(undistinguished),
                            shallowest_distinguishing_depth=dict(sorted(depth_hist.items())),
                            example=example, undistinguished_pairs=undistinguished[:20])
    return report


# ---------- part C: stepwise tree, window states and pruning conditions ----------

def part_c(bits, in_masks, out_masks):
    windows = [1, 2, 3, 4]
    window_counter = {k: Counter() for k in windows}
    prune = Counter()
    graphs = 0
    example = {}
    for i, m_in in enumerate(in_masks['masks']):
        for (x, g), out in out_masks.items():
            feasible = m_in & out
            if not feasible:
                continue
            graphs += 1
            for n in range(1, RING):
                # tree nodes are legal prefixes only: no equal colours on a ring edge
                w = {p: bool(bits.completion[p] & feasible) for p in bits.prefixes[n]
                     if all(p[j] != p[j + 1] for j in range(n - 1))}
                for p, ok in w.items():
                    if ok:
                        prune[(n, 'alive')] += 1
                        continue
                    b_in = not bits.completion[p] & m_in
                    b_out = not bits.completion[p] & out
                    label = ('seen_by_both' if b_in and b_out else
                             'seen_by_inside_only' if b_in else
                             'seen_by_outside_only' if b_out else
                             'unseen_by_either')
                    prune[(n, label)] += 1
                for k in windows:
                    groups = defaultdict(set)
                    for p, ok in w.items():
                        groups[normalize(p[-k:])].add(ok)
                    bad = [key for key, vals in groups.items() if len(vals) == 2]
                    window_counter[k][(n, 'insufficient' if bad else 'sufficient')] += 1
                    if bad and k not in example:
                        example[k] = dict(inside=i, outside=x, alignment=g, depth=n, window=k,
                                          colliding_window=bad[0],
                                          prefixes={str(p): ok for p, ok in w.items()
                                                    if normalize(p[-k:]) == bad[0]})
    return dict(
        glued_graphs=graphs,
        window_sufficiency={k: {f'depth{n}': dict(sufficient=c[(n, 'sufficient')],
                                                  insufficient=c[(n, 'insufficient')])
                                for n in range(1, RING)} for k, c in window_counter.items()},
        dead_branch_detection={f'depth{n}': {key[1]: v for key, v in sorted(prune.items())
                                             if key[0] == n} for n in range(1, RING)},
        example_per_window=example)


# ---------- part D: scope of the outside (fixed / exists / for all) ----------

def part_d(bits, in_masks, out_masks):
    union = 0
    inter = (1 << len(bits.order)) - 1
    for out in out_masks.values():
        union |= out
        inter &= out
    rows = []
    for n in range(1, RING):
        for p in bits.prefixes[n]:
            cp = bits.completion[p]
            rows.append(dict(depth=n, prefix=p,
                             insides_alive_for_some_outside=sum(bool(cp & m & union) for m in in_masks['masks']),
                             insides_alive_for_every_outside=sum(
                                 all(cp & m & out for out in out_masks.values()) for m in in_masks['masks']),
                             insides_alive_by_inside_alone=sum(bool(cp & m) for m in in_masks['masks'])))
    return dict(outsides=len(out_masks), library_union_patterns=bin(union).count('1'),
                library_intersection_patterns=bin(inter).count('1'), prefixes=rows)


def main():
    data = json.loads((FAN / 'states.json').read_text())
    pattern_order = [tuple(p) for p in data['pattern_order']]
    bits = Bits(pattern_order)
    sigmas = []
    for s in data['states']:
        sigma = sigma_from_edges([tuple(e) for e in s['edges']])
        assert bits.mask(sigma) == s['sigma_bits'], (s['mask'], bits.mask(sigma), s['sigma_bits'])
        sigmas.append(sigma)
    aligned = {(x, g): align(sigmas[x], g) for x in range(len(sigmas)) for g in dihedral()}
    in_masks = dict(sigmas=sigmas, masks=[bits.mask(s) for s in sigmas])
    out_masks = {key: bits.mask(s) for key, s in aligned.items()}
    result = dict(
        scope=dict(inside='87 fan-pentagon disk patches, Sigma recomputed from edges',
                   continuation='same 87 patches glued from outside, 10 dihedral alignments',
                   history='inside patch plus colours committed to b0..b_{n-1}, forward only',
                   completable='some completion of the prefix lies in Sigma_in meet aligned Sigma_out'),
        part_a_uncoloured=part_a(sigmas, aligned),
        part_b_compressed_inside_state=part_b(bits, in_masks, out_masks),
        part_c_stepwise=part_c(bits, in_masks, out_masks),
        part_d_outside_scope=part_d(bits, in_masks, out_masks),
    )
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'first_run.json').write_text(json.dumps(result, indent=1, default=repr) + '\n')

    a = result['part_a_uncoloured']
    print(f"part A (uncoloured): {a['completable']}/{a['pairs']} glued graphs 4-colourable")
    print('part B (coloured prefix): state -> classes / conflicting pairs / distinguished / not / depth hist')
    for name, r in result['part_b_compressed_inside_state'].items():
        print(f"  {name:15s} {r['classes']:3d} {r['pairs_same_state_different_sigma']:5d} "
              f"{r['distinguished']:5d} {r['not_distinguished']:5d} {r['shallowest_distinguishing_depth']}")
    c = result['part_c_stepwise']
    print('part C (stepwise): glued graphs', c['glued_graphs'])
    for k, rows in c['window_sufficiency'].items():
        print(f"  window {k}: insufficient in", {d: v['insufficient'] for d, v in rows.items()})
    for d, row in c['dead_branch_detection'].items():
        print(f"  {d}: {row}")
    d = result['part_d_outside_scope']
    print('part D (outside scope): union', d['library_union_patterns'], 'intersection',
          d['library_intersection_patterns'])
    for row in d['prefixes']:
        if row['depth'] >= 3:
            print(f"  depth {row['depth']} prefix {row['prefix']}: inside-alone {row['insides_alive_by_inside_alone']:2d}"
                  f"  some-outside {row['insides_alive_for_some_outside']:2d}"
                  f"  every-outside {row['insides_alive_for_every_outside']:2d}")


if __name__ == '__main__':
    main()
