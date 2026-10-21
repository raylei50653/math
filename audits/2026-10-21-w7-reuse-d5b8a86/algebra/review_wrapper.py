#!/usr/bin/env python3
"""Independent public-wrapper correctness/negative controls and fair CPU timing.
Build-only review artifacts; no solver. Intended with one CPU thread.
"""
import concurrent.futures,hashlib,json,statistics,sys,time
from pathlib import Path
import numpy as np
from scipy.sparse import csr_matrix,vstack
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];AUD=HERE.parent
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT/'audits/2026-10-20-w7-count-opt-d5b8a86'))
sys.path.insert(0,str(AUD/'specialized'))
from model import Model
from w7_operator import W7Operator
m=Model();rng=np.random.default_rng(17)
xi=rng.integers(0,8,size=m.nx,dtype=np.int64);x=xi.astype(float)
cases=[];saved={}
for reference in ('mindeg','h2'):
 ref=m.reference(reference);D=m.difference(ref).astype(np.int64);Q=m.positivity_rows(ref).astype(np.int64)
 for positive in ((),(9,),(9,0,7),tuple(range(10))):
  A=vstack([D,csr_matrix(Q[list(positive)])],format='csr').astype(np.int64)
  vi=rng.integers(-4,5,size=A.shape[0],dtype=np.int64);v=vi.astype(float)
  target=A@xi;adj=A.T@vi
  for backend in ('direct','template'):
   op=W7Operator(backend=backend,positive=positive,reference=reference);w=op.workspace()
   out=np.empty(A.shape[0]);ot=np.empty(m.nx)
   assert op.matvec_into(x,out,w) is out and np.array_equal(out,target)
   assert op.rmatvec_into(v,ot,w) is ot and np.array_equal(ot,adj)
   assert np.array_equal(op.matvec(x),target) and np.array_equal(op.rmatvec(v),adj)
   assert np.array_equal(op.recover_z(x),m.zmap(ref)@xi/2)
   assert np.dot(out,v)==np.dot(x,ot)
   L=op.aslinearoperator()
   assert np.array_equal(L@x,target) and np.array_equal(L.T@v,adj)
   assert np.array_equal(L.matvec(x.reshape(-1,1)).reshape(-1),target)
   cases.append({'backend':backend,'reference':reference,'positive':list(positive),'integer_forward_transpose_recovery_adjoint_exact':True})
   if reference=='mindeg' and positive==tuple(range(10)):saved[backend]=(op,A.astype(float),A.T.tocsr().astype(float))
negative=[]
def reject(name,fn):
 try:fn()
 except (ValueError,TypeError):negative.append(name)
 else:raise AssertionError('invalid input accepted: '+name)
for backend,(op,A,AT) in saved.items():
 w=op.workspace();out=np.empty(op.shape[0]);ot=np.empty(op.nx)
 reject(backend+':wrong_input_length',lambda:op.matvec(x[:-1]))
 reject(backend+':complex_input',lambda:op.matvec(x.astype(complex)))
 reject(backend+':float32_output',lambda:op.matvec_into(x,out.astype(np.float32),w))
 reject(backend+':noncontiguous_output',lambda:op.matvec_into(x,np.empty(2*len(out))[::2],w))
 readonly=out.copy();readonly.flags.writeable=False
 reject(backend+':readonly_output',lambda:op.matvec_into(x,readonly,w))
 reject(backend+':short_workspace',lambda:op.matvec_into(x,out,(np.empty(op.nh-1),*w[1:])))
 readonly_w=w[0].copy();readonly_w.flags.writeable=False
 reject(backend+':readonly_workspace',lambda:op.matvec_into(x,out,(readonly_w,*w[1:])))
 backing=np.empty(max(op.nh,op.nx));backing[:op.nx]=x
 reject(backend+':input_workspace_overlap',lambda:op.matvec_into(backing[:op.nx],out,(backing[:op.nh],*w[1:])))
 backing=np.empty(max(op.nx,op.shape[0]));backing[:op.nx]=x
 reject(backend+':input_output_overlap',lambda:op.matvec_into(backing[:op.nx],backing[:op.shape[0]],w))
 reject(backend+':rinput_output_overlap',lambda:op.rmatvec_into(backing[:op.shape[0]],backing[:op.nx],w))
 # The public claim of separate-workspace concurrency is checked directly.
 xs=[rng.standard_normal(op.nx) for _ in range(2)]
 ws=[op.workspace(),op.workspace()];os=[np.empty(op.shape[0]),np.empty(op.shape[0])]
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
  fs=[pool.submit(op.matvec_into,z,o,t) for z,o,t in zip(xs,os,ws)]
  for f,z in zip(fs,xs):assert np.allclose(f.result(),A@z,rtol=1e-12,atol=1e-9)
for kwargs in ({'backend':'bad'},{'reference':'bad'},{'positive':(9,9)},{'positive':(-1,)},{'positive':(True,)}):
 reject(str(kwargs),lambda kwargs=kwargs:W7Operator(**kwargs))
def measure(f):
 for _ in range(8):f()
 batches=[]
 for _ in range(5):
  t=time.perf_counter()
  for _ in range(60):f()
  batches.append((time.perf_counter()-t)*1000/60)
 return {'median_ms':statistics.median(batches),'batch_ms':batches}
xn=rng.standard_normal(m.nx);v=rng.standard_normal(2*m.ns+10)
A=saved['direct'][1];AT=saved['direct'][2]
bench={'scipy_forward':measure(lambda:A@xn),'scipy_transpose':measure(lambda:AT@v)}
for backend,(op,_,_) in saved.items():
 workspace=op.workspace()
 bench[backend+'_forward']=measure(lambda:op.matvec_into(xn,np.empty(op.shape[0]),workspace))
 bench[backend+'_transpose']=measure(lambda:op.rmatvec_into(v,np.empty(op.nx),workspace))
report={'status':'independent wrapper review passed; no solver',
 'wrapper_sha256':hashlib.sha256((AUD/'specialized/w7_operator.py').read_bytes()).hexdigest(),
 'cases':cases,'negative_controls_rejected':negative,'separate_workspace_concurrency_pass':True,
 'timing_policy':'float64 CPU one thread; persistent native workspace; every native/SciPy call allocates returned output; setup excluded;8warmups,5x60',
 'benchmark':bench}
(HERE/'wrapper-review.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
