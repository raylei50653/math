#!/usr/bin/env python3
"""Small dual discovery; only exact integer postchecks can prove anything."""
from pathlib import Path
from collections import defaultdict
from fractions import Fraction
from functools import reduce
from math import gcd, lcm
import argparse, gzip, importlib.util, json, pickle, time


def main():
    import numpy as np
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix, vstack
    p = argparse.ArgumentParser()
    p.add_argument('--depth', type=int, default=1)
    p.add_argument('--targets', type=int, nargs='+', default=[44459, 44466])
    p.add_argument('--seconds', type=float, default=50)
    p.add_argument('--c11-defect', action='store_true')
    p.add_argument('--state-slacks', action='store_true')
    p.add_argument('--full', action='store_true', help='explicitly authorized full dual search')
    p.add_argument('--prefix', type=Path, required=True)
    p.add_argument('--source', type=Path, default=Path(__file__).resolve().parents[2] /
                   '2026-10-20-r6-941-j1-five-edge-417732f/counting')
    a = p.parse_args()
    start = time.monotonic()
    k = json.load(gzip.open(a.source/'orbits.json.gz', 'rt'))
    rowids = dict(k['rowids'])
    live = set(k['live'])
    byrow, bystate = defaultdict(list), defaultdict(list)
    for r, i in rowids.items():
        if i in live:
            bystate[i].append(r)
    for j, col in enumerate(k['columns']):
        for r in col:
            byrow[r].append(j)
    states = set(a.targets)
    if a.full:
        states = set(live)
    if a.c11_defect:
        sp = importlib.util.spec_from_file_location('old_orbits', a.source/'orbits.py')
        old = importlib.util.module_from_spec(sp)
        sp.loader.exec_module(old)
        hrows = sorted(old.rowmap(list(old.c.proper_growth(11))))
        cert = json.loads((a.source.parent/'frozen/audits/2026-10-20-r6-941-j1-c11-1148ce0/reduction/reduced-orbit-certificate.json').read_text())
        lam = {hrows[h]:v for h,v in cert['live_half_row_multipliers']}
        pulled = {}
        for r, i in rowids.items():
            if i not in live:
                continue
            x, t = r, [0]*13
            for q in range(12,-1,-1):t[q]=x&3;x>>=2
            projection = tuple(t[:2]+t[4:])
            if old.c.m.proper(projection):
                value = lam.get(old.encode(old.half(projection)),0)
                if value:
                    pulled[r] = value
                    states.add(i)
        for col in k['columns']:
            if sum(pulled.get(r,0) for r in col):
                states |= {rowids[r] for r in col}
    for _ in range(a.depth):
        touched = {j for i in states for r in bystate[i] for j in byrow[r]}
        states |= {rowids[r] for j in touched for r in k['columns'][j]}
    states = sorted(states)
    rows = sorted(r for i in states for r in bystate[i])
    assert a.full or len(rows) < 20000, 'this script is restricted to small local LPs'
    ri = {r: i for i, r in enumerate(rows)}
    touched = sorted({j for r in rows for j in byrow[r]})
    si = {s: i for i, s in enumerate(states)}
    er = [si[rowids[r]] for r in rows]
    E = coo_matrix((np.ones(len(rows)), (er, list(range(len(rows))))),
                   shape=(len(states),len(rows))).tocsr()
    ur, uc = [], []
    for jj, j in enumerate(touched):
        for r in k['columns'][j]:
            if r in ri:
                ur.append(jj)
                uc.append(ri[r])
    U = coo_matrix((np.ones(len(ur)),(ur,uc)),shape=(len(touched),len(rows))).tocsr()
    rhs = np.array([int(s in a.targets) for s in states], dtype=float)
    print(json.dumps({'states':len(states),'halfrows':len(rows),'columns':len(touched),
                      'nnz':U.nnz,'seconds':time.monotonic()-start}),flush=True)
    if a.state_slacks:
        ans = linprog(np.zeros(len(rows)), A_ub=vstack([U,-E]).tocsr(),
                      b_ub=np.r_[np.zeros(len(touched)),-rhs], bounds=(None,None),
                      method='highs-ds',options={'time_limit':a.seconds,'threads':1})
    else:
        ans = linprog(np.zeros(len(rows)), A_eq=E, b_eq=rhs, A_ub=U,
                      b_ub=np.zeros(len(touched)), bounds=(None,None), method='highs-ds',
                      options={'time_limit':a.seconds,'threads':1})
    out = {'targets':a.targets,'depth':a.depth,'c11_defect_support':a.c11_defect,'full':a.full,
           'state_slacks':a.state_slacks,
           'states':len(states),'halfrows':len(rows),
           'columns':len(touched),'status':ans.status,'message':ans.message,
           'seconds':time.monotonic()-start,'exact_certificate':False}
    with Path(str(a.prefix)+'.pickle').open('xb') as f:
        pickle.dump((rows,states,touched,ans),f)
    if ans.success:
        fractions = [Fraction(float(v)).limit_denominator(1000000) for v in ans.x]
        scale = 1
        for v in fractions:
            scale = lcm(scale,v.denominator)
            if scale.bit_length()>512:
                break
        if scale.bit_length()>512:
            out['rationalization_stop'] = 'common denominator exceeds 512 bits; raw solution retained'
            with Path(str(a.prefix)+'.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
            print(json.dumps(out,sort_keys=True))
            return
        y = {r:int(v*scale) for r,v in zip(rows,fractions) if v}
        divisor = reduce(gcd,(abs(v) for v in y.values()))
        y = {r:v//divisor for r,v in y.items()}
        zsum = defaultdict(int)
        for r,v in y.items():zsum[rowids[r]] += v
        colsum = [sum(y.get(r,0) for r in col) for col in k['columns']]
        exact = all((v>=0 if a.state_slacks else v==0)
                    for i,v in zsum.items() if i not in a.targets)
        exact &= all(zsum[i]>0 for i in a.targets) and max(colsum)<=0
        out.update({'exact_certificate':bool(exact),'nonzero_y':len(y),
                    'maximum_column_pairing':max(colsum),
                    'target_pairings':[[i,zsum[i]] for i in a.targets]})
        if exact:
            with Path(str(a.prefix)+'.certificate.json').open('x') as f:
                json.dump({'multipliers':sorted(y.items()),'target_pairings':out['target_pairings'],
                           'convention':'sum_h y_h*(2Z_i(h)-sum_j X_j)=0; column sums <=0'},f,indent=2)
                f.write('\n')
    with Path(str(a.prefix)+'.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
    print(json.dumps(out,sort_keys=True))


if __name__=='__main__':main()
