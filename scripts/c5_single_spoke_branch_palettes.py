#!/usr/bin/env python3
"""Local palette audit; no source-graph enumeration or disk-realizability claim."""
import argparse
import json
from itertools import combinations_with_replacement, permutations
from pathlib import Path

from c5_single_spoke_bridge_path import audit as path_audit

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_single_spoke_branch_palettes/observations.json'
Q = (0, 1, 0, 1, 2)
P = (0, 1, 0, 2, 1)


def mask(colors):
    return sum(1 << c for c in set(colors))


def transport(bits, perm):
    return mask(perm[c] for c in range(4) if bits & (1 << c))


def disjoint_unions(children):
    q = p = 0
    for cq, cp in children:
        if q & cq or p & cp:
            return None
        q |= cq
        p |= cp
    return q, p


def audit():
    # The paper induction preserves membership of 0 and 3 in each block.
    pairs = [(q, p) for q in range(1, 16) for p in range(1, 16)
             if q.bit_count() == p.bit_count() in (1, 2)
             and q & 9 == p & 9]
    assert len(pairs) == 16
    closure = []
    for row in path_audit()['tight_rows']:
        if row['contact']:
            continue
        lq, lp = map(mask, row['lists'][:2])
        for count in range(4):
            for children in combinations_with_replacement(pairs, count):
                unions = disjoint_unions(children)
                if unions is None:
                    continue
                q, p = unions
                if q & ~lq or p & ~lp:
                    continue
                residual = (lq ^ q, lp ^ p)
                if residual[0].bit_count() == residual[1].bit_count() in (1, 2):
                    assert residual in pairs
                    closure.append([row['support'], children, residual])
    path_rows = []
    for row in path_audit()['path_rows']:
        lq, lp2, lp3 = map(mask, row['lists'])
        r2, r3 = (8, 4) if row['contact'] else (12, 12)
        for count in range(3):
            for children in combinations_with_replacement(pairs, count):
                unions = disjoint_unions(children)
                if unions is None:
                    continue
                q, p = unions
                if q & ~lq or p & ~lp2 or p & ~lp3:
                    continue
                if lp2 ^ p != r2 or lp3 ^ p != r3:
                    continue
                residual = lq ^ q
                assert residual in ((2, 4) if row['contact'] else (10, 12))
                assert all(cp & 12 == 0 for _, cp in children)
                path_rows.append(dict(contact=row['contact'], support=row['support'],
                                      children=children, q_residual=residual))
    root_pairs = [(q, p) for q, p in pairs if p & 12 == 0]
    assert root_pairs == [(1, 1), (2, 2), (3, 3), (4, 2), (5, 3)]
    # Rooted palette uniqueness makes every compatible row permutation act on
    # the entire rooted branch palette. Enumerate only necessary support tests.
    supports = []
    for q, p in root_pairs:
        candidates = []
        for support_mask in range(1, 16):
            support = [i for i in range(1, 5) if support_mask & (1 << (i-1))]
            valid = True
            for perm in permutations(range(4)):
                for row, palette in ((Q, q), (P, p)):
                    if all(perm[row[i]] == row[i] for i in support):
                        valid &= transport(palette, perm) == palette
                if all(perm[Q[i]] == P[i] for i in support):
                    valid &= transport(q, perm) == p
            if valid:
                # Boundary 2 supplies palette color 0; boundary 1 supplies
                # q/p color 1; boundary 4 supplies q color 2 / p color 1.
                required = ({2} if q & 1 else set())
                required |= ({1} if q & 2 else set())
                required |= ({4} if q & 4 else set())
                assert required <= set(support)
                candidates.append(support)
        assert candidates
        supports.append(dict(q_palette=q, p_palette=p, allowed_supports=candidates))
    # A q bridge alternates 3/non-3 at each internal path vertex.
    transitions = [[a, b] for a in (1, 2, 3) for b in (1, 2, 3)
                   if a != b and (a == 3) != (b == 3)]
    assert len(transitions) == 4
    return dict(scope='necessary local palette constraints, not realizability',
                palette_encoding='bit c represents color c; pairs ordered q,p1',
                invariant_pairs=pairs, closure=closure, path_rows=path_rows,
                root_supports=supports, q_transitions=transitions)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = audit()
    normalized = json.loads(json.dumps(result))
    if args.check:
        assert json.loads(OUT.read_text()) == normalized
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(result, indent=2) + '\n')
    print(f"branch palettes: 16 pairs, {len(result['closure'])} closure cases, "
          f"{len(result['path_rows'])} path cases, 5 rooted support types verified")


if __name__ == '__main__':
    main()
