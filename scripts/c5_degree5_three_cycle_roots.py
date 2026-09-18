#!/usr/bin/env python3
"""Three shared-cycle chain: ordered interface and four-row list evidence only."""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
from c5_degree5_long_triangle_roots import U, D, PAIRS, TRIPLES, colors, singleton, step, roots, arm_states

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_degree5_three_cycle_roots/observations.json'


@lru_cache(None)
def relation(lists, p):
    """Bit 4*x+y represents the ordered endpoint assignment (x,y)."""
    result = 0
    for x, y in product(colors(lists[0]), colors(lists[p])):
        msg = 1 << x
        for i, allowed in enumerate(lists[1:], 1):
            msg = step(msg, (1 << y) if i == p else allowed)
        if msg & ~(1 << x):
            result |= 1 << (4*x+y)
    return result


def brute_relation(lists, p):
    result = 0
    for cs in product(*map(colors, lists)):
        if all(x != y for x, y in zip(cs, cs[1:] + cs[:1])):
            result |= 1 << (4*cs[0]+cs[p])
    return result


def restrict(rel, left, right):
    return rel & sum(1 << (4*x+y) for x, y in product(colors(left), colors(right)))


@lru_cache(None)
def end_rows(n, p, palette, extra, state):
    rows = []
    for a in range(4):
        ls = [U] + [palette]*(n-1)
        ls[p] = (palette | (1 << extra)) & ~singleton(state[a])
        rows.append(roots(ls))
    return tuple(rows)


def build():
    counts, digest, controls = Counter(), sha256(), {}
    def record(kind, data):
        counts[kind] += 1
        digest.update((json.dumps([kind, data], separators=(',', ':'))+'\n').encode())

    # Arbitrary middle C5 private lists; exact relation has independent oracle.
    allowed = PAIRS + TRIPLES + (U,)
    for p in range(1, 5):
        for private in product(allowed, repeat=3):
            it = iter(private)
            ls = tuple(U if i in (0, p) else next(it) for i in range(5))
            rel = relation(ls, p)
            assert rel == brute_relation(ls, p)
            # Every pair of possible terminal root sets (all have size >=2).
            for left, right in product(allowed, repeat=2):
                rejected = not restrict(rel, left, right)
                rigid = left == right and left in PAIRS and all(v == left for v in private)
                assert rejected == rigid
            record('middle_c5', [p, ls, rel])

    paths = arm_states()
    shapes = ((3, 3, 3), (5, 7, 9), (9, 5, 7), (7, 9, 5))
    for s in PAIRS:
        t = U ^ s
        for c, d in product(colors(s), repeat=2):
            for st, tt in product([x for x in paths if x[D] == 1 << c],
                                  [x for x in paths if x[D] == 1 << d]):
                for n, m, k in shapes:
                    for p, h, q in product(range(1, n), range(1, m), range(1, k)):
                        left = end_rows(n, p, t, c, st)
                        right = end_rows(k, q, t, d, tt)
                        short_left = end_rows(3, 1, t, c, st)
                        short_right = end_rows(3, 1, t, d, tt)
                        ls = tuple(U if i in (0, h) else s for i in range(m))
                        rel = relation(ls, h)
                        short_rel = relation((U, U, s), 1)
                        rows = [restrict(rel, left[a], right[a]) for a in range(4)]
                        short = [restrict(short_rel, short_left[a], short_right[a]) for a in range(4)]
                        assert [bool(x) for x in rows] == [True, True, True, False]
                        # All eight subsets of the three cycle replacements.
                        for bits in product((False, True), repeat=3):
                            ll = short_left if bits[0] else left
                            rr = short_right if bits[2] else right
                            mm = short_rel if bits[1] else rel
                            assert [bool(restrict(mm, ll[a], rr[a])) for a in range(4)] == [bool(x) for x in rows]
                        if rel != short_rel and 'changed_middle_relation' not in controls:
                            delta = rel ^ short_rel
                            bit = (delta & -delta).bit_length()-1
                            controls['changed_middle_relation'] = dict(source_lists=ls, source_position=h,
                                target_lists=[U,U,s], target_position=1, source_relation=rel,
                                target_relation=short_rel, distinguishing_pin=[bit//4,bit%4])
                        if rows != short and 'changed_joined_relation' not in controls:
                            a = next(a for a in range(4) if rows[a] != short[a])
                            controls['changed_joined_relation'] = dict(lengths=[n,m,k], positions=[p,h,q],
                                middle_palette=s, arm_paths=[paths[st],paths[tt]], z_color=a,
                                source=rows[a], target=short[a], source_end_roots=[left[a],right[a]],
                                target_end_roots=[short_left[a],short_right[a]])
                        record('chain_four_rows', [s,st,tt,n,m,k,p,h,q,rows,short])
    rel = relation((U, U, 3), 1)
    lproj = sum(1 << x for x in range(4) if any(rel & (1 << (4*x+y)) for y in range(4)))
    rproj = sum(1 << y for y in range(4) if any(rel & (1 << (4*x+y)) for x in range(4)))
    assert lproj == rproj == U and not restrict(rel, 3, 3)
    controls['independent_projections_false_positive'] = dict(middle_lists=[U,U,3],
        position=1, relation=rel, projections=[lproj,rproj], end_roots=[3,3],
        exact_accepts=False, projected_accepts=True, terminal_private_palette=12)
    assert len(controls) == 3
    files = [Path(__file__), ROOT/'scripts/c5_degree5_long_triangle_roots.py']
    return dict(schema=1, scope='Three shared odd-cycle chain, one arm on each terminal cycle: fixed-q lists only; no graph minor, minimality or topology claim.',
        source_sha256={str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in files},
        summary=dict(counts, middle_endpoint_restrictions=counts['middle_c5']*121, arm_profiles=len(paths), replacement_subsets=8),
        query_sha256=digest.hexdigest(), negative_controls=controls)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    data = json.dumps(result, ensure_ascii=False, indent=2)+'\n'
    if args.check:
        assert OUT.read_text() == data, 'certificate differs; rebuild explicitly'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(result['summary'], indent=2))

if __name__ == '__main__':
    main()
