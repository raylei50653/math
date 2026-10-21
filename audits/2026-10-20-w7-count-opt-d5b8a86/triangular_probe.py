#!/usr/bin/env python3
"""Negative probe (discovery only): greedy lower-triangular basis on support {x~>delta}.

Fix free columns in increasing x~; pivot any row with one free column left.  Rows
whose free count hits 0 are left unenforced.  Usage: ./gpy triangular_probe.py runs/all-cu-pdlp/vectors.npz 1e-9 1e-6
"""
import heapq, sys, numpy as np
sys.path.insert(0, '.')
from types import SimpleNamespace as N
from model import Model
from solve_lp import build
x = np.clip(np.load(sys.argv[1])['x'], 0, None)
m = Model(); ref, A, _, _ = build(m, N(ref='mindeg', positive=-1, objective='sum', seed=0))
for delta in map(float, sys.argv[2:]):
    T = np.flatnonzero(x > delta); xt = x[T]
    DT = A[:2*m.ns][:, T]
    R = DT.tocsr(); C = DT.tocsc(); nr, nc = DT.shape
    cnt = np.diff(R.indptr).copy()
    state = np.zeros(nc, np.int8)   # 0 free, 1 fixed, 2 basic
    rdone = cnt == 0                # untouched rows need nothing
    order = iter(np.argsort(xt, kind='stable'))
    q = [i for i in range(nr) if cnt[i] == 1]
    piv = []; viol = []
    def assign(j):
        for i in C.indices[C.indptr[j]:C.indptr[j+1]]:
            cnt[i] -= 1
            if not rdone[i]:
                if cnt[i] == 1: q.append(i)
                elif cnt[i] == 0: viol.append(i); rdone[i] = True
    while True:
        while q:
            i = q.pop()
            if rdone[i] or cnt[i] != 1: continue
            cols = R.indices[R.indptr[i]:R.indptr[i+1]]
            j = cols[state[cols] == 0][0]
            state[j] = 2; rdone[i] = True; piv.append((i, j)); assign(j)
        j = next(order, None)
        if j is None: break
        if state[j] == 0:
            state[j] = 1; assign(j)
    # float solve: basics in pivot order
    v = np.where(state == 1, xt, 0.0)
    for i, j in piv:
        s, e = R.indptr[i], R.indptr[i+1]
        cols, vals = R.indices[s:e], R.data[s:e]
        a = vals[cols == j][0]
        v[j] = -(vals @ v[cols] - a * v[j]) / a
    b = state == 2
    res = R @ v
    print(f'delta {delta:.0e}: cols {nc} pivots {len(piv)} fixed {(state==1).sum()} violated rows {len(viol)} '
          f'max|resid| {abs(res).max():.2e} min basic {v[b].min():.3e} negatives {(v[b]<0).sum()} '
          f'max|x_B-xt_B| {abs(v[b]-xt[b]).max():.2e}', flush=True)
