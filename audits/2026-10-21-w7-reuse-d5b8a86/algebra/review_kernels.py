#!/usr/bin/env python3
"""Independent raw-kernel checks against frozen Model; no LP runs.
Run with opt/py -B from repo root. Writes only algebra/ review artifacts.
"""
import ctypes,hashlib,json,subprocess,sys,time
from pathlib import Path
import numpy as np
from scipy.sparse import csr_matrix,vstack
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT/'audits/2026-10-20-w7-count-opt-d5b8a86'))
from model import Model
source=HERE.parent/'specialized/kernels.cpp'
raw=source.read_bytes(); snapshot=HERE/'kernels-review-snapshot.cpp'
snapshot.write_bytes(raw)
libpath=HERE/'libkernels-review.so'
subprocess.run(['c++','-O3','-std=c++17','-shared','-fPIC',str(snapshot),'-o',str(libpath)],check=True)
lib=ctypes.CDLL(str(libpath)); I=ctypes.POINTER(ctypes.c_int32); F=ctypes.POINTER(ctypes.c_double)
lib.unit_sum.argtypes=[ctypes.c_int,I,I,F,F]
lib.project.argtypes=[ctypes.c_int,I,F,ctypes.c_int,I,I,I,F]
lib.lift_adjoint.argtypes=[ctypes.c_int,I,F,ctypes.c_int,I,I,I,F]
def ip(a): return a.ctypes.data_as(I)
def fp(a): return a.ctypes.data_as(F)
def i32(a): return np.ascontiguousarray(a,dtype=np.int32)
m=Model(); ref=i32(m.reference('mindeg')); C=m.incidence().tocsr().astype(np.int64)
CT=C.T.tocsr(); D=m.difference(ref).astype(np.int64); Q=csr_matrix(m.positivity_rows(ref).astype(np.int64))
A=vstack([D,Q],format='csr'); P=csr_matrix(m.P)
pp,pi,pv=map(i32,(P.indptr,P.indices,P.data))
cp,ci=map(i32,(C.indptr,C.indices)); tp,ti=map(i32,(CT.indptr,CT.indices))
rng=np.random.default_rng(17); checks=[]
for trial in range(3):
 x=rng.integers(0,8,size=m.nx,dtype=np.int64); v=rng.integers(-4,5,size=A.shape[0],dtype=np.int64)
 xf=x.astype(float); vf=v.astype(float)
 h=np.empty(m.nh); out=np.empty(A.shape[0]); adj=np.empty(m.nh); xt=np.empty(m.nx)
 lib.unit_sum(m.nh,ip(cp),ip(ci),fp(xf),fp(h))
 assert np.array_equal(h,C@x)
 lib.project(m.ns,ip(ref),fp(h),10,ip(pp),ip(pi),ip(pv),fp(out))
 assert np.array_equal(out,A@x)
 lib.lift_adjoint(m.ns,ip(ref),fp(vf),10,ip(pp),ip(pi),ip(pv),fp(adj))
 lib.unit_sum(m.nx,ip(tp),ip(ti),fp(adj),fp(xt))
 assert np.array_equal(xt,A.T@v)
 assert np.dot(out,vf)==np.dot(xf,xt)
 checks.append({'trial':trial,'integer_forward_exact':True,'integer_transpose_exact':True,'adjoint_exact':True})
# Floating test distinguishes rounding-order differences from structural errors.
x=rng.standard_normal(m.nx); v=rng.standard_normal(A.shape[0])
lib.unit_sum(m.nh,ip(cp),ip(ci),fp(x),fp(h)); lib.project(m.ns,ip(ref),fp(h),10,ip(pp),ip(pi),ip(pv),fp(out))
lib.lift_adjoint(m.ns,ip(ref),fp(v),10,ip(pp),ip(pi),ip(pv),fp(adj)); lib.unit_sum(m.nx,ip(tp),ip(ti),fp(adj),fp(xt))
forward=float(np.max(np.abs(out-A@x))); transpose=float(np.max(np.abs(xt-A.T@v)))
adjoint=float(abs(out@v-x@xt)); scale=float(max(1,abs(out@v),abs(x@xt)))
assert np.allclose(out,A@x,atol=1e-9,rtol=1e-12)
assert np.allclose(xt,A.T@v,atol=1e-9,rtol=1e-12)
assert adjoint<=1e-11*scale
report={'status':'raw C/CT plus projection kernel independent review passed; no solver',
 'source_sha256':hashlib.sha256(raw).hexdigest(),'all_ten_positivities':True,
 'dtype':'float64 CPU','integer_trials':checks,
 'normal_forward_max_abs_error':forward,'normal_transpose_max_abs_error':transpose,
 'normal_adjoint_abs_error':adjoint,'normal_adjoint_relative_error':adjoint/scale}
(HERE/'kernel-review.json').write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps(report,indent=2))
