#!/usr/bin/env python3
"""Exact, read-only structural probe of the frozen W7 X-only system.

Run from repo root:
  audits/2026-10-20-w7-count-opt-d5b8a86/py audits/2026-10-21-w7-reuse-d5b8a86/algebra/probe.py
No solver is called. All arithmetic on the constraint entries is integer.
"""
import collections
import gzip
import hashlib
import json
import math
import sys
import time
from pathlib import Path
import numpy as np
from scipy.sparse import csr_matrix, vstack
from scipy.sparse.csgraph import connected_components

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OPT = ROOT / 'audits/2026-10-20-w7-count-opt-d5b8a86'
BASE = json.loads((HERE.parent / 'BASE.json').read_text())

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def hist(a):
    return {str(int(k)):int(v) for k,v in sorted(collections.Counter(map(int,a)).items())}

def normalized_groups(A, allow_negative=False):
    """Primitive sparse vectors, grouped with exact tuple equality after hashing.
    Return only nontrivial groups; signs are retained separately when allowed.
    """
    out = collections.defaultdict(list)
    zero = []
    for i in range(A.shape[0]):
        s,e = A.indptr[i:i+2]
        idx = A.indices[s:e]
        dat = A.data[s:e]
        if not len(dat):
            zero.append(i)
            continue
        g = math.gcd(*map(int,dat))
        sign = -1 if allow_negative and dat[0] < 0 else 1
        key = (tuple(map(int,idx)), tuple(int(x)//g*sign for x in dat))
        out[key].append((i,g*sign))
    groups = [v for v in out.values() if len(v)>1]
    return groups,zero

start=time.monotonic()
checks=[]
for item in BASE['inputs']:
    p=ROOT/item['path']
    actual=sha(p)
    if actual != item['sha256']:
        raise RuntimeError('frozen input SHA mismatch: '+str(p))
    checks.append({'path':item['path'],'sha256':actual})
# Importing Model only loads an existing cache. Verify every cache array directly
# against the frozen gzip JSONs before computing any derived matrix.
sys.path.insert(0,str(OPT))
sys.dont_write_bytecode = True
from model import Model
m=Model()
SRC=ROOT/'audits/2026-10-20-r6-941-j1-five-edge-417732f/counting'
orb=json.loads(gzip.decompress((SRC/'orbits.json.gz').read_bytes()))
caps=json.loads(gzip.decompress((SRC/'caps.json.gz').read_bytes()))
live=np.asarray(orb['live'],dtype=np.int64)
li={int(s):i for i,s in enumerate(live)}
per=collections.defaultdict(list)
for r,s in orb['rowids']:
    if s in li: per[li[s]].append(r)
tri=np.asarray([sorted(per[i]) for i in range(len(live))],dtype=np.int64)
hrow=tri.reshape(-1)
hk={int(r):k for k,r in enumerate(hrow)}
cols=orb['columns']
cptr=np.r_[0,np.cumsum([len(c) for c in cols],dtype=np.int64)]
cidx=np.fromiter((hk[r] for c in cols for r in c),dtype=np.int64,count=int(cptr[-1]))
P=np.asarray([[caps['matrices']['G'][j][int(s)] for s in live] for j in (0,2,3,5,7,8,9)] +
             [[p[int(s)] for s in live] for p in caps['sectors']] +
             [[int(int(s) in (44459,44466)) for s in live]],dtype=np.int64)
expected={'live':live,'tri':tri,'hrow':hrow,'hstate':np.repeat(np.arange(len(live)),3),
          'cptr':cptr,'cidx':cidx,'P':P}
for k,v in expected.items():
    if not np.array_equal(getattr(m,k),v): raise RuntimeError('cache mismatch '+k)
del orb,caps,cols,expected,per,hk
ref=m.reference('mindeg')
D=m.difference(ref).astype(np.int64)
D.sort_indices()
Q=m.positivity_rows(ref).astype(np.int64)
A=vstack([D,csr_matrix(Q)],format='csr')
Dc=D.tocsc()
Ac=A.tocsc()
print('verified inputs and built integer matrices',flush=True)
report={'base':BASE['base'],'verified_inputs':checks,'cache_rebuilt_arrays_equal':True,
        'model':{'states':m.ns,'half_rows':m.nh,'columns':m.nx,'D_shape':list(D.shape),
                 'D_nnz':int(D.nnz),'Q_shape':list(Q.shape),'Q_nnz':int(np.count_nonzero(Q)),
                 'D_entry_histogram':hist(D.data),
                 'row_degree_histogram':hist(np.diff(D.indptr)),
                 'column_degree_histogram':hist(np.diff(Dc.indptr))}}
# Equalities may be scaled by any nonzero scalar; variables only by a positive
# scalar, since X >= 0. Column equality includes all ten positivity forms Q.
rg,rz=normalized_groups(D,True)
cg,cz=normalized_groups(Ac.T.tocsr(),False)
dg,dz=normalized_groups(Dc.T.tocsr(),False)
sg,sz=normalized_groups(Dc.T.tocsr(),True)
report['proportional_rows']={'groups':len(rg),'redundant':sum(len(g)-1 for g in rg),
                            'zero_rows':rz,'examples':rg[:8]}
report['positive_proportional_columns_all_positivities']={
    'groups':len(cg),'reduction':sum(len(g)-1 for g in cg),'zero_columns':cz,'examples':cg[:8]}
report['positive_proportional_columns_D_only']={
    'groups':len(dg),'reduction':sum(len(g)-1 for g in dg),'zero_columns':dz,'examples':dg[:8]}
report['signed_proportional_columns_D_only']={
    'groups':len(sg),'reduction':sum(len(g)-1 for g in sg),'zero_columns':sz,'examples':sg[:8]}
# Cheap exact facial and equality tests, distinct from float support probing.
monos=[]
twos=[]
nonnegative=[]
for i in range(D.shape[0]):
    s,e=D.indptr[i:i+2]
    val=D.data[s:e]
    if len(val)==1: monos.append(i)
    if len(val)==2: twos.append(i)
    if len(val) and (np.all(val>0) or np.all(val<0)): nonnegative.append(i)
report['low_degree_rows']={'singleton':monos,'two_term':twos,'one_sign':nonnegative,
                         'degree_2_columns':int(np.count_nonzero(np.diff(Dc.indptr)==2))}
# Components of exact D incidence. The ten Q forms add across components, so
# each component may be processed independently before adding cone witnesses.
from scipy.sparse import coo_matrix
rr,cc=D.nonzero()
nr,nc=D.shape
G=coo_matrix((np.ones(2*len(rr),dtype=np.int8),
    (np.r_[rr,nr+cc],np.r_[nr+cc,rr])),shape=(nr+nc,nr+nc)).tocsr()
ncomp,labels=connected_components(G,directed=False)
sizes=collections.Counter(map(int,labels))
comp=[]
for k,size in sizes.most_common():
    r=np.flatnonzero(labels[:nr]==k)
    c=np.flatnonzero(labels[nr:]==k)
    comp.append({'label':k,'rows':len(r),'columns':len(c),
                 'positivities_hit':[i for i in range(10) if np.any(Q[i,c])],
                 'row_example':r[:3].tolist(),'column_example':c[:3].tolist()})
report['components']={'number':ncomp,'components':comp}
np.savez_compressed(HERE/'maps.npz',ref=ref,component_row=labels[:nr],component_column=labels[nr:])
report['elapsed_seconds']=time.monotonic()-start
(HERE/'result.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('verified_inputs',)},indent=2),flush=True)
