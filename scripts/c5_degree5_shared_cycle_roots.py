#!/usr/bin/env python3
"""Shared odd-cycle four-row acceptance interfaces; no graph minor claim."""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
from c5_degree5_long_triangle_roots import U, D, PAIRS, TRIPLES, colors, singleton, roots, brute, arm_states

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_degree5_shared_cycle_roots/observations.json'
root = lru_cache(None)(lambda ls: roots(list(ls)))


def build():
    counts, digest = Counter(), sha256()
    def record(kind, data):
        counts[kind] += 1
        digest.update((json.dumps([kind, data], separators=(',', ':'))+'\n').encode())
    # Independent exhaustive coloring oracle for all >=2 private lists on C5.
    for private in product(PAIRS + TRIPLES + (U,), repeat=4):
        ls = (U, *private)
        actual = root(ls)
        assert actual == brute(list(ls))
        assert actual.bit_count() >= 2
        uniform = len(set(private)) == 1 and private[0] in PAIRS
        assert (actual.bit_count() == 2) == uniform
        if uniform:
            assert actual == U ^ private[0]
        record('arbitrary_c5', [ls, actual])
    for private in product(PAIRS, repeat=6):
        actual = root((U, *private))
        assert actual.bit_count() >= 2
        assert (actual.bit_count() == 2) == (len(set(private)) == 1)
        if len(set(private)) == 1:
            assert actual == U ^ private[0]
        record('pair_c7', [private, actual])
    paths = arm_states()
    controls = {}
    forbiddens = Counter()
    for s in PAIRS:
        t = U ^ s
        for case in ('same_cycle', 'split_cycles', 'same_point'):
            other = s if case != 'split_cycles' else t
            for c, d in product(colors(U ^ s), colors(U ^ other)):
                if case == 'same_point' and c == d:
                    continue
                left = [st for st in paths if st[D] == 1 << c]
                right = [st for st in paths if st[D] == 1 << d]
                for st, tt in product(left, right):
                    for n in (3, 5, 7, 9):
                        positions = combinations(range(1, n), 2) if case == 'same_cycle' else ((p, p) for p in range(1, n))
                        for p, q in positions:
                            rows, short_rows = [], []
                            for a in range(4):
                                ls = [U] + [s] * (n-1)
                                if case == 'same_point':
                                    ls[p] = U & ~singleton(st[a]) & ~singleton(tt[a])
                                    short = [U, ls[p], s]
                                    rr = s
                                else:
                                    ls[p] = (s | (1 << c)) & ~singleton(st[a])
                                    lp = (other | (1 << d)) & ~singleton(tt[a])
                                    if case == 'same_cycle':
                                        ls[q] = lp
                                        short = [U, ls[p], lp]
                                        rr = s
                                    else:
                                        short = [U, ls[p], s]
                                        rs = [U] + [t]*(n-1)
                                        rs[q] = lp
                                        rr = root(tuple(rs))
                                        # Compare the actual joint queries, not side marginals.
                                lr, sr = root(tuple(ls)), root(tuple(short))
                                short_rr = root((U, lp, t)) if case == 'split_cycles' else rr
                                joined, short_joined = lr & rr, sr & short_rr
                                rows.append(joined); short_rows.append(short_joined)
                                assert bool(joined) == bool(short_joined)
                                if lr != sr and 'changed_side_root' not in controls:
                                    controls['changed_side_root'] = dict(case=case, palette=s, arm_paths=[paths[st], paths[tt]], z_color=a, source_lists=ls, target_lists=short, source_root=lr, target_root=sr)
                                if joined != short_joined and 'changed_joint_root' not in controls:
                                    controls['changed_joint_root'] = dict(case=case, palette=s, arm_paths=[paths[st], paths[tt]], z_color=a, source_lists=ls, target_lists=short, other_root=rr, source_joint=joined, target_joint=short_joined)
                            assert rows[D] == short_rows[D] == 0
                            if case != 'same_point':
                                assert all(rows[a] for a in range(3))
                            mask = sum(1 << a for a in range(4) if not rows[a])
                            forbiddens[(case, mask)] += 1
                            record(case, [s, st, tt, n, p, q, rows, short_rows])
    assert set(controls) == {'changed_side_root', 'changed_joint_root'}
    files = [Path(__file__), ROOT/'scripts/c5_degree5_long_triangle_roots.py']
    return dict(schema=1, scope='Fixed-q shared-cycle list acceptance only; neither full root preservation nor graph/topology certificate.', source_sha256={str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in files}, summary=dict(counts, arm_profiles=len(paths)), query_sha256=digest.hexdigest(), forbidden_masks={f'{case}:{mask}':v for (case,mask),v in sorted(forbiddens.items())}, negative_controls=controls)


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
