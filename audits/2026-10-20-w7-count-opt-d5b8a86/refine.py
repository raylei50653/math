#!/usr/bin/env python3
"""Colour refinement of the full W7 feasibility LP (discovery only; never a verdict).

Grohe-Kersting-Mladenov-Selman 2013, Lemma 7.1: refine rows and columns of
[A | b] jointly until the partition is equitable (every row class sees, for each
column class and coefficient, the same count, and vice versa).  c = 0.

Full system (no Z elimination): rows are the 183,924 half-row equations
2 Z_s - S_h X = 0 plus the ten positivity rows P_l Z >= 1; columns are the 61,308
Z and 307,197 X.  Initial colours: row kind (equation / positivity, rhs), column
kind (Z / X).  Multiset hashing uses random 64-bit keys; a final exact pass
recomputes every class signature as a sorted tuple and asserts equitability.

--sums follows the paper exactly: a vertex's signature is, per class of the other
side, the SUM of its coefficients into that class (not the multiset of single
coefficients), and the initial column partition is one class (all columns have
c = 0, lb = 0, ub = inf).  Rows start by (sense, rhs) only.  Hash collisions can
only merge classes, and a discrete result has nothing left to merge.
"""
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from model import Model  # noqa: E402

MASK = np.uint64(0xFFFFFFFFFFFFFFFF)


def mix(a):
    a = (a ^ (a >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9)
    a = (a ^ (a >> np.uint64(27))) * np.uint64(0x94D049BB133111EB)
    return a ^ (a >> np.uint64(31))


def triplets(m, split_target):
    nh, ns, nx = m.nh, m.ns, m.nx
    col_x = np.repeat(np.arange(nx), np.diff(m.cptr))
    rows = [m.cidx, np.arange(nh)]
    cols = [ns + col_x, m.hstate]
    vals = [-np.ones(len(m.cidx), np.int64), np.full(nh, 2, np.int64)]
    for l in range(10):
        s = np.nonzero(m.P[l])[0]
        rows.append(np.full(len(s), nh + l))
        cols.append(s)
        vals.append(m.P[l][s])
    r, c, v = (np.concatenate(a).astype(np.int64) for a in (rows, cols, vals))
    rcol = np.r_[np.zeros(nh, np.int64), np.full(10, 1, np.int64)]
    if split_target:
        rcol[nh + 9] = 2
    ccol = np.r_[np.zeros(ns, np.int64), np.ones(nx, np.int64)]
    return r, c, v, rcol, ccol


def step(src_col, dst, other, vals, n_dst, own):
    key = mix(other.astype(np.uint64) * np.uint64(1000003) + (vals + 64).astype(np.uint64))
    acc = np.zeros(n_dst, np.uint64)
    np.add.at(acc, dst, key)
    sig = mix(acc ^ mix(own.astype(np.uint64) + np.uint64(7)))
    _, new = np.unique(np.stack([own.astype(np.uint64), sig], 1), axis=0, return_inverse=True)
    return new.reshape(-1).astype(np.int64)


def step_sums(dst, other, vals, n_dst, own):
    order = np.lexsort((other, dst))
    d, o, x = dst[order], other[order], vals[order]
    start = np.r_[0, np.nonzero((np.diff(d) != 0) | (np.diff(o) != 0))[0] + 1]
    s = np.add.reduceat(x, start)
    keep = s != 0
    d, o, s = d[start][keep], o[start][keep], s[keep]
    key = mix(o.astype(np.uint64) * np.uint64(1000003) + (s + (1 << 20)).astype(np.uint64))
    acc = np.zeros(n_dst, np.uint64)
    np.add.at(acc, d, key)
    sig = mix(acc ^ mix(own.astype(np.uint64) + np.uint64(7)))
    _, new = np.unique(np.stack([own.astype(np.uint64), sig], 1), axis=0, return_inverse=True)
    return new.reshape(-1).astype(np.int64)


def refine(r, c, v, rcol, ccol, sums=False):
    nr, nc = len(rcol), len(ccol)
    for it in range(200):
        if sums:
            nrc = step_sums(r, ccol[c], v, nr, rcol)
            ncc = step_sums(c, nrc[r], v, nc, ccol)
        else:
            nrc = step(None, r, ccol[c], v, nr, rcol)
            ncc = step(None, c, nrc[r], v, nc, ccol)
        done = nrc.max() == rcol.max() and ncc.max() == ccol.max()
        rcol, ccol = nrc, ncc
        print(json.dumps({'iter': it, 'row_classes': int(rcol.max() + 1),
                          'col_classes': int(ccol.max() + 1)}), flush=True)
        if done:
            return rcol, ccol, it
    raise RuntimeError('no fixpoint')


def exact_equitable(r, c, v, rcol, ccol):
    """Exact check: per vertex, sorted (other class, coef) counts equal within a class."""
    def sigs(dst, other_cls, n):
        order = np.lexsort((v, other_cls, dst))
        out = [Counter() for _ in range(n)]
        for d, o, x in zip(dst[order], other_cls[order], v[order]):
            out[d][(int(o), int(x))] += 1
        return out
    for dst, oc, own in ((r, ccol[c], rcol), (c, rcol[r], ccol)):
        s = sigs(dst, oc, len(own))
        rep = {}
        for i, k in enumerate(own):
            t = tuple(sorted(s[i].items()))
            assert rep.setdefault(int(k), t) == t, 'not equitable'


def main():
    m = Model()
    split = '--split-target' in sys.argv
    sums = '--sums' in sys.argv
    r, c, v, rcol, ccol = triplets(m, split)
    if sums:
        ccol = np.zeros_like(ccol)
    rcol, ccol, it = refine(r, c, v, rcol, ccol, sums)
    if not sums:
        exact_equitable(r, c, v, rcol, ccol)
    zc, xc = ccol[:m.ns], ccol[m.ns:]
    tz = sorted({int(zc[m.state_of[t]]) for t in (44459, 44466)})
    out = {
        'split_target_row': split, 'coefficient_sums': sums, 'iterations': it + 1,
        'rows': len(rcol), 'cols': len(ccol), 'nnz': len(v),
        'row_classes': int(rcol.max() + 1), 'col_classes': int(ccol.max() + 1),
        'z_classes': len(np.unique(zc)), 'x_classes': len(np.unique(xc)),
        'largest_col_class': int(np.bincount(ccol).max()),
        'singleton_col_classes': int((np.bincount(ccol) == 1).sum()),
        'target_z_classes': tz,
        'target_class_sizes': [int((zc == k).sum()) for k in tz],
        'exact_equitable': None if sums else True,
    }
    tag = ('split' if split else 'joint') + ('-sums' if sums else '')
    np.savez_compressed(HERE / f'cache/refine-{tag}.npz', rcol=rcol, ccol=ccol)
    (HERE / f'logs/refine-{tag}.json').write_text(json.dumps(out, indent=1) + '\n')
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
