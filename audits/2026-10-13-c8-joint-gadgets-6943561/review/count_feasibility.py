#!/usr/bin/env python3
"""Exact full-support common-count controls on the eight frozen C8 residuals.

Discovery uses the frozen rational reconstruction utility and SciPy. Checking
reconstructs the NC equality matrix and all joins without importing a producer.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as Q
from itertools import combinations
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / 'frozen/audits'
INTERFACE = BASE / '2026-10-13-c8-joint-count-3097ef5/interface.json'
UPPERS = BASE / '2026-10-13-c5-no4ct-c8-6cafdfb/RESULTS.json'
CERT = HERE / 'count_feasibility.json'


def partitions(n, prefix=()):
    if len(prefix) == n:
        yield prefix
    else:
        for c in range(max(prefix, default=-1) + 2):
            yield from partitions(n, prefix+(c,))


def algebra(words):
    nc = [p for p in partitions(8) if not any(p[a] == p[c] and p[b] == p[d] and p[a] != p[b]
                                             for a,b,c,d in combinations(range(8),4))]
    matrix = [[int(all(part[i] != part[j] or row[i] == row[j]
                       for i,j in combinations(range(8),2))) for part in nc] for row in words]
    active = [i for i in range(len(nc)) if any(row[i] for row in matrix)]
    return nc, active, [[row[i] for i in active] for row in matrix]


def inputs():
    interface = json.loads(INTERFACE.read_text())
    queries = [q for q in json.loads(UPPERS.read_text())['queries']
               if q['status'] == 'necessary_condition_residual']
    assert len(queries) == 8
    return interface, queries


def rank(matrix):
    basis={}
    for row in matrix:
        v=list(map(Q,row))
        for pivot,r in sorted(basis.items()):
            z=v[pivot]
            if z:v=[a-z*b for a,b in zip(v,r)]
        if any(v):
            pivot=next(i for i,x in enumerate(v) if x)
            z=v[pivot];basis[pivot]=[x/z for x in v]
    return len(basis)


def build():
    import numpy as np
    from scipy.optimize import linprog
    sys.path.insert(0, str(BASE/'2026-10-13-c8-joint-count-3097ef5/counts'))
    from generate import nullspace, reconstruct
    interface, queries = inputs()
    _, active, rows = algebra(interface['pattern_order'])
    cases = {c['id']:c for c in interface['cases']}
    result = {'schema':'c8-full-support-common-count-v1','active_partition_indices':active,'queries':[]}
    for q in queries:
        mask = q['support']
        allowed = [i for i in range(274) if mask >> i & 1]
        kernel = nullspace([r for i,r in enumerate(rows) if not mask >> i & 1],len(active))
        values = [[sum(Q(a)*b for a,b in zip(row,v)) for v in kernel] for row in rows]
        constraints = [values[i] for i in allowed]
        lp = linprog(np.zeros(len(kernel)),A_ub=-np.array(constraints,float),
                     b_ub=-np.ones(len(allowed)),bounds=(None,None),method='highs')
        assert lp.success, (q['query_id'],lp.message)
        pars = reconstruct(lp.x,constraints,[Q(1)]*len(allowed))
        cs = [sum(v[j]*c for v,c in zip(kernel,pars)) for j in range(len(active))]
        counts = [sum(Q(c)*a for c,a in zip(row,cs)) for row in rows]
        outer = [sum(Q(a)*b for a,b in zip(row,counts)) for row in cases[q['case_id']]['transfer']]
        result['queries'].append({'query_id':q['query_id'],'support':mask,
            'counts':list(map(str,counts)),'partition_coefficients':list(map(str,cs)),
            'outer_counts':list(map(str,outer)),'kernel_dimension':len(kernel)})
        print(q['query_id'], 'full support',len(allowed),'dim',len(kernel),flush=True)
    return result


def check(result):
    interface, queries = inputs()
    words = interface['pattern_order']
    assert words == [list(p) for p in partitions(8) if max(p)<4 and all(p[i]!=p[(i+1)%8] for i in range(8))]
    nc, active, rows = algebra(words)
    assert len(nc)==1430 and len(active)==91 and result['active_partition_indices']==active
    assert rank(rows)==91
    assert [q['query_id'] for q in queries] == [q['query_id'] for q in result['queries']]
    cases = {c['id']:c for c in interface['cases']}
    for expected, q in zip(queries,result['queries']):
        mask = expected['support']; assert q['support']==mask
        assert q['kernel_dimension']==91-rank([row for i,row in enumerate(rows) if not mask>>i&1])
        counts = list(map(Q,q['counts'])); cs = list(map(Q,q['partition_coefficients']))
        assert len(counts)==274 and len(cs)==91
        assert all(x>0 if mask>>i&1 else x==0 for i,x in enumerate(counts))
        assert counts == [sum(Q(c)*a for c,a in zip(row,cs)) for row in rows]
        case = cases[expected['case_id']]
        outer = [sum(Q(a)*b for a,b in zip(row,counts)) for row in case['transfer']]
        assert list(map(str,outer))==q['outer_counts']
        assert all(x>0 if expected['target']>>i&1 else x==0 for i,x in enumerate(outer))
        assert all(any(o & ~mask == 0 for o in opts) for i in range(274) if mask>>i&1
                   for opts in interface['kempe_obligations'][i])
    return {'status':'PASS','queries':8,'full_support_sizes':[q['support'].bit_count() for q in result['queries']],
            'NC_partitions':len(nc),'active_columns':len(active),'arithmetic':'int/Fraction'}


def main():
    p=argparse.ArgumentParser(); p.add_argument('--write',action='store_true'); p.add_argument('--check',action='store_true');p.add_argument('--negative',action='store_true')
    args=p.parse_args()
    if args.write:
        result=build();check(result)
        with CERT.open('x') as f: json.dump(result,f,sort_keys=True,separators=(',',':'));f.write('\n')
    else: result=json.loads(CERT.read_text())
    receipt=check(result)
    if args.negative:
        for key in ('counts','partition_coefficients','outer_counts'):
            bad=json.loads(json.dumps(result));bad['queries'][0][key][0]=str(Q(bad['queries'][0][key][0])+1)
            try:check(bad)
            except AssertionError:pass
            else:raise AssertionError('negative control accepted: '+key)
        receipt['negative_controls_rejected']=3
    print(json.dumps(receipt,sort_keys=True))

if __name__=='__main__':main()
