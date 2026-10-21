#!/usr/bin/env python3
"""Independent template_sum metadata construction, correctness, and CPU timing.
Build-only review artifact; no solver. Intended with one CPU thread.
"""
import collections,ctypes,gzip,hashlib,json,statistics,sys,time
from pathlib import Path
import numpy as np
from scipy.sparse import csr_matrix,vstack
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]; AUD=HERE.parent
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT/'audits/2026-10-20-w7-count-opt-d5b8a86'))
from model import Model
setup_start=time.perf_counter()
def gz(name):return json.loads(gzip.decompress((AUD/'templates'/name).read_bytes()))
T=gz('templates.json.gz'); R=gz('row_map.json.gz')['rows']; J=gz('column_map.json.gz')['original_column_order']
m=Model(); hk={int(h):i for i,h in enumerate(m.hrow)}
byrow=collections.defaultdict(dict); bycol=collections.defaultdict(dict); kval={}
for h,s,q,k,r,live in R:
 if live:
  assert r not in byrow[q];byrow[q][r]=hk[h];kval[q]=k
for j,(q,k,t) in enumerate(J):
 assert t not in bycol[q];bycol[q][t]=j;assert kval[q]==k
patterns=collections.defaultdict(list)
for q,rr in byrow.items(): patterns[(kval[q],tuple(sorted(rr)),tuple(sorted(bycol[q])))].append(q)
rptr=[];rind=[];cptr=[];cind=[];rows=[];cols=[];meta=[]
for (k,rr,jj),qq in sorted(patterns.items()):
 qq.sort();ri={r:i for i,r in enumerate(rr)}
 br=[];bc=[]
 for j,t in enumerate(jj):
  for r in T[str(k)][t]:
   assert r in ri;br.append(ri[r]);bc.append(j)
 B=csr_matrix((np.ones(len(br),dtype=np.int32),(br,bc)),shape=(len(rr),len(jj)))
 BT=B.T.tocsr()
 meta.append([len(rr),len(jj),len(qq),len(rptr),len(rind),len(cptr),len(cind),len(rows),len(cols)])
 rptr.extend(B.indptr);rind.extend(B.indices);cptr.extend(BT.indptr);cind.extend(BT.indices)
 rows.extend(byrow[q][r] for r in rr for q in qq)
 cols.extend(bycol[q][j] for j in jj for q in qq)
arrays=[np.ascontiguousarray(a,dtype=np.int32) for a in (meta,rptr,rind,cptr,cind,rows,cols)]
meta,rptr,rind,cptr,cind,rows,cols=arrays
assert np.array_equal(np.sort(rows),np.arange(m.nh))
assert np.array_equal(np.sort(cols),np.arange(m.nx))
assert meta.shape[1]==9
C=m.incidence().tocsr();CT=C.T.tocsr();ref=np.ascontiguousarray(m.reference('mindeg'),dtype=np.int32)
D=m.difference(ref); Q=csr_matrix(m.positivity_rows(ref)); A=vstack([D,Q],format='csr');AT=A.T.tocsr();P=csr_matrix(m.P)
pp,pi,pv=[np.ascontiguousarray(a,dtype=np.int32) for a in (P.indptr,P.indices,P.data)]
lib=ctypes.CDLL(str(HERE/'libkernels-review.so'));I=ctypes.POINTER(ctypes.c_int32);F=ctypes.POINTER(ctypes.c_double)
lib.template_sum.argtypes=[ctypes.c_int]+[I]*7+[ctypes.c_int]+[F]*4
lib.project.argtypes=[ctypes.c_int,I,F,ctypes.c_int,I,I,I,F]
lib.lift_adjoint.argtypes=[ctypes.c_int,I,F,ctypes.c_int,I,I,I,F]
def ip(a):return a.ctypes.data_as(I)
def fp(a):return a.ctypes.data_as(F)
space=max(int(max(nr,nc))*int(ng) for nr,nc,ng,*_ in meta)
packed=np.empty(space);sums=np.empty(space);hscratch=np.empty(m.nh)
params=[len(meta)]+[ip(a) for a in arrays]
def multiply(x,transpose=False):
 out=np.empty(m.nx if transpose else m.nh)
 lib.template_sum(*params,int(transpose),fp(x),fp(out),fp(packed),fp(sums));return out
def forward(x):
 h=multiply(x);out=np.empty(A.shape[0]);lib.project(m.ns,ip(ref),fp(h),10,ip(pp),ip(pi),ip(pv),fp(out));return out
def adjoint(x):
 lib.lift_adjoint(m.ns,ip(ref),fp(x),10,ip(pp),ip(pi),ip(pv),fp(hscratch));return multiply(hscratch,True)
setup=time.perf_counter()-setup_start
rng=np.random.default_rng(17)
for trial in range(3):
 x=rng.integers(0,8,size=m.nx,dtype=np.int64);h=rng.integers(-4,5,size=m.nh,dtype=np.int64);v=rng.integers(-4,5,size=A.shape[0],dtype=np.int64)
 assert np.array_equal(multiply(x.astype(float)),C.astype(np.int64)@x)
 assert np.array_equal(multiply(h.astype(float),True),CT.astype(np.int64)@h)
 assert np.array_equal(forward(x.astype(float)),A.astype(np.int64)@x)
 assert np.array_equal(adjoint(v.astype(float)),AT.astype(np.int64)@v)
x=rng.standard_normal(m.nx);h=rng.standard_normal(m.nh);v=rng.standard_normal(A.shape[0])
errors={};ops={'C':(C,x,lambda:multiply(x)), 'CT':(CT,h,lambda:multiply(h,True)),
 'A_all10':(A,x,lambda:forward(x)), 'AT_all10':(AT,v,lambda:adjoint(v))}
for name,(B,w,f) in ops.items():
 errors[name]=float(np.max(np.abs(f()-B@w)));assert np.allclose(f(),B@w,atol=1e-9,rtol=1e-12)
adjerr=float(abs(forward(x)@v-x@adjoint(v)));adjscale=float(max(1,abs(forward(x)@v),abs(x@adjoint(v))))
assert adjerr<=1e-11*adjscale
def measure(f):
 for _ in range(8):f()
 batches=[]
 for _ in range(5):
  t=time.perf_counter()
  for _ in range(60):f()
  batches.append((time.perf_counter()-t)*1000/60)
 return {'median_ms':statistics.median(batches),'batch_ms':batches}
timings={}
for name,(B,w,f) in ops.items():
 B=B.astype(np.float64)
 scipy=measure(lambda:B@w);native=measure(f)
 timings[name]={'scipy_float64':scipy,'template_float64':native,'speedup':scipy['median_ms']/native['median_ms']}
out={'status':'independent template kernel metadata and exact outputs pass; no solver',
 'source_snapshot_sha256':hashlib.sha256((HERE/'kernels-review-snapshot.cpp').read_bytes()).hexdigest(),
 'patterns':len(meta),'scatter_rows_cover_once':True,'scatter_columns_cover_once':True,
 'metadata_int32_bytes':sum(a.nbytes for a in arrays),'scratch_doubles':space,
 'three_integer_trials_exact_all_four_operations':True,'all_ten_positivities':True,
 'float64_max_abs_errors':errors,'adjoint_relative_error':adjerr/adjscale,
 'setup_seconds':setup,'timing_policy':'one thread; each timed operation allocates output; template A also allocates h intermediate; shared packed/sums scratch; 8 warmups then5x60',
 'timings':timings}
(HERE/'template-kernel-review.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
