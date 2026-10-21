#!/usr/bin/env python3
"""Exact helpers for candidate certificates.  Only check.py decides.

rational_solve: exact solution of a square nonsingular integer system B x = r,
via float LU, exact integer residual refinement (x = sum_k d_k 2^{-s k}) and
rational reconstruction with a common denominator.  The final equality is
re-verified in Python integers; any failure returns None.
"""
from fractions import Fraction
import json
from math import gcd, lcm
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
CHECKER = HERE.parent / '2026-10-20-w7-count-cone-d5b8a86/independent/check.py'
BASE = 'd5b8a8605bcbcef7aebbcf1934dad7ba255ccf02'


def int_matvec(B, x):
    """B (scipy, integer-valued) times a list of Python ints, exactly."""
    B = B.tocsr()
    ind, ptr = B.indices, B.indptr
    dat = [int(v) for v in B.data]
    out = []
    for i in range(B.shape[0]):
        s = 0
        for t in range(ptr[i], ptr[i + 1]):
            s += dat[t] * x[ind[t]]
        out.append(s)
    return out


def reconstruct(acc, den_acc, max_den_bits):
    """Common-denominator rational reconstruction of acc/den_acc, or None."""
    Q = 1
    bound = 1 << max_den_bits
    half = 1 << (den_acc.bit_length() // 2)
    for a in sorted(range(len(acc)), key=lambda i: -abs(acc[i])):
        v = Fraction(acc[a] * Q, den_acc)
        w = v.limit_denominator(max(1, half // Q))
        Q *= w.denominator
        if Q > bound or Q * Q > den_acc:
            return None
    num = [(2 * acc[i] * Q + den_acc) // (2 * den_acc) for i in range(len(acc))]
    g = Q
    for v in num:
        g = gcd(g, v)
    return [v // g for v in num], Q // g


def rational_solve(B, r, bits=24, max_rounds=400, every=4, max_den_bits=6000):
    """Return (numerators, denominator) with B num = den r exactly, or None.

    The dyadic expansion acc/2^(bits*k) satisfies B acc = 2^(bits*k) r - res_k
    exactly; reconstruction is attempted every few rounds and accepted only
    after an exact integer verification."""
    from scipy.sparse.linalg import splu
    lu = splu(B.tocsc().astype(float), permc_spec='COLAMD')
    Bi = B.tocsr().astype(np.int64)
    n = B.shape[0]
    target = [int(v) for v in r]
    res = np.array(target, dtype=object)
    acc = [0] * n
    scale = 1 << bits
    for k in range(1, max_rounds + 1):
        f = lu.solve(np.array([float(v) for v in res]))
        d = np.rint(f * scale)
        if not np.all(np.isfinite(d)) or np.abs(d).max() > 2 ** 62:
            return None
        d = d.astype(np.int64)
        acc = [a * scale + int(v) for a, v in zip(acc, d)]
        res = res * scale - (Bi @ d).astype(object)
        if max(abs(int(v)) for v in res).bit_length() > 2 * bits + 64:
            return None                              # refinement diverges
        if k % every and any(res):
            continue
        den_acc = scale ** k
        if not any(res):                             # exact dyadic solution
            g = den_acc
            for v in acc:
                g = gcd(g, v)
            return [v // g for v in acc], den_acc // g
        out = reconstruct(acc, den_acc, max_den_bits)
        if out is not None and int_matvec(B, out[0]) == [out[1] * v for v in target]:
            return out
    return None


def integer_scale(fracs):
    """Fractions -> common positive integer multiple, gcd-reduced."""
    den = 1
    for f in fracs:
        den = lcm(den, f.denominator)
    ints = [int(f * den) for f in fracs]
    g = 0
    for v in ints:
        g = gcd(g, v)
    return [v // g for v in ints] if g else ints


def write_primal(path, model, z_by_state, x_by_col, meta):
    """z_by_state: {canonical_id: int>0}; x_by_col: {column: int>0}."""
    cert = {'base': BASE, 'kind': 'primal', **meta,
            'z': [[int(s), int(v)] for s, v in sorted(z_by_state.items()) if v],
            'x': [[int(j), int(v)] for j, v in sorted(x_by_col.items()) if v]}
    _write(path, cert)


def write_dual(path, y_by_halfrow, lam, meta):
    cert = {'base': BASE, 'kind': 'dual', **meta,
            'y': [[int(h), int(v)] for h, v in sorted(y_by_halfrow.items()) if v],
            'lambda': [int(v) for v in lam]}
    _write(path, cert)


def _write(path, cert):
    path = Path(path)
    with path.open('x') as f:
        json.dump(cert, f, separators=(',', ':'))
        f.write('\n')


def load_checker():
    import importlib.util
    spec = importlib.util.spec_from_file_location('w7_independent_check', CHECKER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
