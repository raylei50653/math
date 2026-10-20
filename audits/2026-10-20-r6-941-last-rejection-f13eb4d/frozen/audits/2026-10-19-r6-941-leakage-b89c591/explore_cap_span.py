#!/usr/bin/env python3
"""Discovery only: image of the C10 planar span through the actual r6 cap."""
import itertools
import json
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy import sparse
from scipy.optimize import linprog
import sympy as sp

D = Path(__file__).resolve().parent
ROOT = D.parents[1]


def canonical(t):
    d = {}
    return tuple(d.setdefault(x, len(d)) for x in t)


def growth(n, p=(0,)):
    if len(p) == n:
        yield p
    else:
        for x in range(max(p) + 2):
            yield from growth(n, p + (x,))


def proper(t):
    return all(t[i] != t[(i + 1) % len(t)] for i in range(len(t)))


def main():
    t8 = [t for t in growth(8) if max(t) < 4 and proper(t)]
    t10 = [t for t in growth(10) if max(t) < 4 and proper(t)]
    idx = {t: i for i, t in enumerate(t10)}
    q4 = list(itertools.combinations(range(10), 4))
    parts = [p for p in growth(10) if proper(p) and not any(
        p[i] == p[k] and p[j] == p[l] and p[i] != p[j]
        for i, j, k, l in q4)]
    print('basis', len(t8), len(t10), len(parts), flush=True)
    a = np.ones((len(t10), len(parts)), dtype=np.int64)
    ts = np.array(t10)
    for j, p in enumerate(parts):
        for i in range(10):
            old = next((k for k in range(i) if p[k] == p[i]), None)
            if old is not None:
                a[:, j] &= (ts[:, i] == ts[:, old])
    transfer = np.zeros((len(t8), len(t10)), dtype=np.int64)
    for i, (aa, n, rr, ll, q, c, x, y) in enumerate(t8):
        for s, v, w, t in itertools.product(range(4), repeat=4):
            core = (aa, n, rr, ll, q, c, s, v, w, t)
            if not proper(core) or s == x or t == y:
                continue
            lifts = sum(r not in {x, y, s, v, w, t} for r in range(4))
            transfer[i, idx[canonical(core)]] += lifts
    image = sparse.csr_matrix(transfer) @ a
    print('transfer nnz', np.count_nonzero(transfer), flush=True)
    # Select independent columns by modular Gaussian elimination, then verify
    # exact reconstruction using the old 91-dimensional planar basis.
    mat = sp.polys.matrices.DomainMatrix.from_Matrix(sp.Matrix(image.tolist()))
    den, denom, piv = mat.rref_den()
    print('rank image', len(piv), flush=True)
    basis = image[:, list(piv)]
    old = json.loads((ROOT/'audits/2026-10-18-smaller-bad-e1617a2/kempe-consistency.json').read_text())
    assert t8 == [tuple(t) for t in old['tuples']]
    live = set(next(r['surviving_ids'] for r in old['results'] if r['source_mask'] == 941))
    kill = sp.Matrix([list(basis[i]) for i in range(len(t8)) if i not in live])
    null = kill.nullspace()
    reduced = sp.Matrix(basis.tolist()) * sp.Matrix.hstack(*null)
    print('941 dimension', len(null), flush=True)
    controls=json.loads((ROOT/'audits/2026-10-18-smaller-bad-counts-e1617a2/A/941-counted-candidate-probes.json').read_text())
    tests=[]
    for control in controls['results']:
        fit=linprog(np.zeros(a.shape[1]),A_ub=-a,b_ub=np.zeros(len(t10)),
                    A_eq=image,b_eq=np.array(control['counts']),bounds=[(None,None)]*a.shape[1],method='highs')
        print('positive span preimage',control['candidate'],fit.success,fit.message,flush=True)
        tests.append({'candidate':control['candidate'],'feasible':fit.success})
    rows=('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
    m8={name:np.zeros((10,len(t8)),dtype=np.int64) for name in ['G','Q1','Q2','GB']}
    iu={t:i for i,t in enumerate(t8)}
    mu=np.zeros((10,len(t10)),dtype=np.int64)
    for ri,row in enumerate(rows):
        x,y,aa,b,c=map(int,row)
        for n,rr,ll,q in itertools.product(range(4),repeat=4):
            tp=(aa,n,rr,ll,q,c,x,y)
            if not proper(tp) or b in {aa,q,c}: continue
            j=iu[canonical(tp)]
            m8['G'][ri,j]+=sum(p not in {aa,b,q,n,h} and h not in {q,ll,rr,n}
                              for p,h in itertools.product(range(4),repeat=2))
            m8['Q1'][ri,j]+=int(n==b and rr==q)
            m8['Q2'][ri,j]+=int(n==b and ll==b)
            m8['GB'][ri,j]+=int(b not in {n,ll,rr})
        z,s,v,w,t=map(int,row)
        for n,rr,ll,q in itertools.product(range(4),repeat=4):
            tp=(z,n,rr,ll,q,z,s,v,w,t)
            if not proper(tp): continue
            lifts=sum(p not in {z,q,n,h} and h not in {q,ll,rr,n}
                      for p,h in itertools.product(range(4),repeat=2))
            mu[ri,idx[canonical(tp)]]+=lifts
    muimage=mu@a
    projections={name:m@image for name,m in m8.items()}
    kill=np.vstack([image[i] for i in range(len(t8)) if i not in live]+[muimage[i] for i in (6,7,9)])
    force_b=sum((a[idx[canonical((2,0,rr,ll,0,2,3,v,w,3))]] for rr,ll in [(1,2),(2,1)] for v,w in [(0,1),(1,0)]),start=np.zeros(a.shape[1],dtype=np.int64))
    force_a=sum((a[idx[canonical((2,3,rr,ll,0,2,3,v,w,3))]] for ll,rr in [(3,1),(3,0),(1,0)] for v,w in [(0,1),(1,0)]),start=np.zeros(a.shape[1],dtype=np.int64))
    positive=np.vstack([projections['G'][i] for i in range(10) if (941>>i)&1]+[muimage[i] for i in range(10) if (319>>i)&1]+[force_a,force_b])
    ub=np.vstack([-a,-positive]); rhs=np.concatenate([np.zeros(len(t10)),-np.ones(len(positive))])
    samples=[]
    for target in ['source','Q1','Q2','GB','all_full']:
        eq=kill
        aub=ub; bub=rhs
        if target=='all_full':
            aub=np.vstack([ub]+[-projections[name] for name in ('Q1','Q2','GB')])
            bub=np.concatenate([rhs,-np.ones(30)])
        elif target!='source':
            eq=np.vstack([kill,projections[target][[1,4,6]]])
            aub=np.vstack([ub,-projections[target][9]])
            bub=np.concatenate([rhs,[-1]])
        fit=linprog(np.zeros(a.shape[1]),A_ub=aub,b_ub=bub,A_eq=eq,b_eq=np.zeros(len(eq)),bounds=[(None,None)]*a.shape[1],method='highs')
        print('U319 plus source941 planar core',target,fit.success,fit.message,flush=True)
        item={'target':target,'feasible':fit.success}
        if fit.success:
            coeff=[Fraction(float(x)).limit_denominator(100000) for x in fit.x]
            item['coefficient_rationals']=[str(x) for x in coeff]
            item['candidate_masks']={name:sum(1<<i for i,x in enumerate(m@fit.x) if x>1e-6) for name,m in projections.items()}
            item['U_mask']=sum(1<<i for i,x in enumerate(muimage@fit.x) if x>1e-6)
            print('masks',item['candidate_masks'],'U',item['U_mask'],flush=True)
        samples.append(item)
    out = {'pin_order': ['a','n','R','L','q','c','s','v','w','t'],
           'tuple_count':len(t10), 'noncrossing_nonzero_columns':len(parts),
           'transfer_image_rank':len(piv), 'dimension_941':len(null),
           'positive_span_preimage_controls':tests,
           'U319_planar_core_tests':samples,
           'pivots':list(piv), 'image_basis':basis.tolist(),
           'restricted_basis':[[str(x) for x in row] for row in reduced.tolist()]}
    with (D/'cap-span-discovery-v5.json').open('x') as f:
        json.dump(out,f,indent=2); f.write('\n')


if __name__ == '__main__':
    main()
