#!/usr/bin/env python3
"""Exact quotient by identical original half-row sum expressions.

Requires probe.py to have verified pinned inputs. This script calls no solver.
For a quotient state t, every original Z_s in its DSU class is z_t.
T is the matrix of unique half-row sums; E maps each template to its class.
All equations are T_k X=2 z_{E(k)}. Choose a minimum-degree template r(t),
eliminate z_t=T_{r(t)}X/2, and retain T_k-T_{r(E(k))}=0 for k!=r(E(k)).
Q_t = sum_{s in class t} P_s, so all ten positivity forms are retained.
"""
import collections, hashlib,json,sys,time
from pathlib import Path
import numpy as np
from scipy.sparse import csr_matrix
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]
BASE=json.loads((HERE.parent/'BASE.json').read_text())
for item in BASE['inputs']:
 p=ROOT/item['path']
 if hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256']:
  raise RuntimeError('frozen input SHA mismatch '+str(p))
sys.path.insert(0,str(ROOT/'audits/2026-10-20-w7-count-opt-d5b8a86'))
sys.dont_write_bytecode = True
from model import Model
m=Model(); C=m.incidence().tocsr().astype(np.int64); C.sort_indices()
parent=np.arange(m.ns)
def find(x):
 while parent[x]!=x:
  parent[x]=parent[parent[x]]; x=parent[x]
 return int(x)
def union(a,b):
 a,b=find(a),find(b)
 if a!=b: parent[max(a,b)]=min(a,b)
keys={}; template_of_half=np.empty(m.nh,dtype=np.int64); reps=[]
for k in range(m.nh):
 s,e=C.indptr[k:k+2]; key=tuple(map(int,C.indices[s:e]))
 if key not in keys:
  keys[key]=len(reps); reps.append(k)
 tid=keys[key]; template_of_half[k]=tid
 union(k//3,reps[tid]//3)
roots=np.array([find(i) for i in range(m.ns)],dtype=np.int64)
_,state_class=np.unique(roots,return_inverse=True)
nsq=int(state_class.max())+1
T=C[reps]
template_state=state_class[np.array(reps)//3]
ref=np.empty(nsq,dtype=np.int64)
classes=collections.defaultdict(list)
for i,t in enumerate(template_state): classes[int(t)].append(i)
for t,tt in classes.items(): ref[t]=min(tt,key=lambda i:(T.indptr[i+1]-T.indptr[i],i))
keep=np.flatnonzero(np.arange(len(reps))!=ref[template_state])
Dq=(T[keep]-T[ref[template_state[keep]]]).tocsr(); Dq.eliminate_zeros(); Dq.sort_indices()
Pq=np.zeros((10,nsq),dtype=np.int64)
for i in range(10): np.add.at(Pq[i],state_class,m.P[i])
R=T[ref]
Q=np.asarray((R.T@Pq.T).T)
# An exact symbolic check of the lift: original rows are literally T template
# rows, and every grouped state/half-row belongs to one common quotient state.
assert (C-T[template_of_half]).nnz==0
assert np.array_equal(state_class[m.hstate],template_state[template_of_half])
# A comparison of matrix-free and materialized operations on deterministic
# integer vectors exercises transpose and all ten positivity forms.
rng=np.random.default_rng(21261021)
x=rng.integers(0,8,size=m.nx,dtype=np.int64)
u=T@x
assert np.array_equal(Dq@x,u[keep]-u[ref[template_state[keep]]])
assert np.array_equal(Q@x,Pq@u[ref])
v=rng.integers(-4,5,size=len(keep),dtype=np.int64)
w=np.zeros(len(reps),dtype=np.int64)
np.add.at(w,keep,v); np.add.at(w,ref[template_state[keep]],-v)
assert np.array_equal(Dq.T@v,T.T@w)
# Store all exact maps, reconstruct the matrices from frozen C rather than
# storing another several-megabyte coefficient copy.
np.savez_compressed(HERE/'quotient_maps.npz',state_class=state_class,
 template_of_half=template_of_half,template_representative_half=np.array(reps),
 template_state=template_state,reference_template=ref,equality_template=keep,Pq=Pq)
original_D=m.difference(m.reference('mindeg'))
report={'base':BASE['base'],'original_states':m.ns,'quotient_states':nsq,
 'state_reduction':m.ns-nsq,'state_class_size_histogram':dict(sorted(collections.Counter(map(int,np.bincount(state_class))).items())),
 'original_half_rows':m.nh,'unique_half_sum_templates':len(reps),'half_row_reduction':m.nh-len(reps),
 'original_C_nnz':int(C.nnz),'unique_template_T_nnz':int(T.nnz),
 'original_D_shape':list(original_D.shape),'original_D_nnz':int(original_D.nnz),
 'quotient_D_shape':list(Dq.shape),'quotient_D_nnz':int(Dq.nnz),
 'equality_row_reduction':original_D.shape[0]-Dq.shape[0],
 'difference_nnz_reduction':int(original_D.nnz-Dq.nnz),
 'Q_nnz':int(np.count_nonzero(Q)),
 'minimum_template_degree':int(np.diff(T.indptr).min()),
 'matrix_free_D_nonzeros':int(T.nnz+2*len(keep)),
 'symbolic_lift_checks':True,'integer_matvec_transpose_checks':True,
 'nonnegativity_preserved':'z_t = T_reference(t) X / 2 >= 0; X unchanged >= 0',
 'positivity_preserved':'Pq_l[t] = sum_{s: state_class[s]=t} P_l[s] for each of all ten rows'}
(HERE/'quotient.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
