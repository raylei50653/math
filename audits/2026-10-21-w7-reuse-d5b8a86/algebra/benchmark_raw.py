#!/usr/bin/env python3
"""Fair output-allocation CPU benchmark of independent raw float64 kernel calls.
SciPy float32 baselines are separately labeled; no cross-dtype speed claim.
"""
import ctypes,json,sys,time,statistics
from pathlib import Path
import numpy as np
from scipy.sparse import csr_matrix,vstack
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT/'audits/2026-10-20-w7-count-opt-d5b8a86'))
from model import Model
m=Model(); ref=np.ascontiguousarray(m.reference('mindeg'),dtype=np.int32)
C=m.incidence().tocsr(); CT=C.T.tocsr(); D=m.difference(ref); P=csr_matrix(m.P)
A=vstack([D,csr_matrix(m.positivity_rows(ref))],format='csr'); AT=A.T.tocsr()
lib=ctypes.CDLL(str(HERE/'libkernels-review.so')); I=ctypes.POINTER(ctypes.c_int32); F=ctypes.POINTER(ctypes.c_double)
lib.unit_sum.argtypes=[ctypes.c_int,I,I,F,F]
lib.project.argtypes=[ctypes.c_int,I,F,ctypes.c_int,I,I,I,F]
lib.lift_adjoint.argtypes=[ctypes.c_int,I,F,ctypes.c_int,I,I,I,F]
def ip(a):return a.ctypes.data_as(I)
def fp(a):return a.ctypes.data_as(F)
cp,ci,tp,ti,pp,pi,pv=[np.ascontiguousarray(a,dtype=np.int32) for a in
 (C.indptr,C.indices,CT.indptr,CT.indices,P.indptr,P.indices,P.data)]
hscratch=np.empty(m.nh)
def unit_C(x):
 y=np.empty(m.nh);lib.unit_sum(m.nh,ip(cp),ip(ci),fp(x),fp(y));return y
def unit_CT(x):
 y=np.empty(m.nx);lib.unit_sum(m.nx,ip(tp),ip(ti),fp(x),fp(y));return y
def unit_A(x):
 y=np.empty(A.shape[0]);lib.unit_sum(m.nh,ip(cp),ip(ci),fp(x),fp(hscratch));lib.project(m.ns,ip(ref),fp(hscratch),10,ip(pp),ip(pi),ip(pv),fp(y));return y
def unit_AT(x):
 y=np.empty(m.nx);lib.lift_adjoint(m.ns,ip(ref),fp(x),10,ip(pp),ip(pi),ip(pv),fp(hscratch));lib.unit_sum(m.nx,ip(tp),ip(ti),fp(hscratch),fp(y));return y
rng=np.random.default_rng(17)
x=rng.standard_normal(m.nx);h=rng.standard_normal(m.nh);v=rng.standard_normal(A.shape[0])
ops={'C':(C,x,unit_C),'CT':(CT,h,unit_CT),'A_all10':(A,x,unit_A),'AT_all10':(AT,v,unit_AT)}
def measure(f):
 for _ in range(8):f()
 times=[]
 for _ in range(5):
  t=time.perf_counter()
  for _ in range(60):f()
  times.append((time.perf_counter()-t)/60)
 return {'median_ms':1000*statistics.median(times),'batch_ms':[1000*t for t in times]}
report={'dtype_target':'float64','thread_policy':'OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=MKL_NUM_THREADS=1',
 'timing_policy':'setup excluded; every timed call allocates its returned output; reusable operator scratch preallocated; 8 warmups then 5 batches of60 calls',
 'operations':{}}
for name,(B,w,native) in ops.items():
 B64=B.astype(np.float64);B32=B.astype(np.float32);w32=w.astype(np.float32)
 assert np.allclose(native(w),B64@w,rtol=1e-12,atol=1e-9)
 sci=measure(lambda:B64@w);unit=measure(lambda:native(w));sci32=measure(lambda:B32@w32)
 report['operations'][name]={'scipy_float64':sci,'unit_float64':unit,
  'unit_speedup_same_dtype':sci['median_ms']/unit['median_ms'],'scipy_float32_separate':sci32}
(HERE/'raw-benchmark.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
