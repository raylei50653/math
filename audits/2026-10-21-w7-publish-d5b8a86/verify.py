#!/usr/bin/env python3
"""Portable publication custody verification. Stdlib by default; no files written.

Restore ARCHIVE first. --numerical additionally checks the saved one-run trial
with NumPy/SciPy against original-coordinate matrices, never running a solver.
The historical absolute warm path is accepted only as exact recorded provenance;
its bytes are always read from this checkout's corresponding relative path.
"""
import argparse,gzip,hashlib,json,stat,sys
from pathlib import Path,PurePosixPath
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]
CONE=ROOT/'audits/2026-10-20-w7-count-cone-d5b8a86'
REUSE=ROOT/'audits/2026-10-21-w7-reuse-d5b8a86'
OPT=ROOT/'audits/2026-10-20-w7-count-opt-d5b8a86'
def require(ok,why):
 if not ok:raise ValueError(why)
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def path(rel):
 q=PurePosixPath(rel)
 require(not q.is_absolute() and '..' not in q.parts,'unsafe relative path '+str(rel))
 p=ROOT/rel;require(p.resolve().is_relative_to(ROOT),'path escapes checkout '+str(rel));return p
def match(p,rec,mode=False):
 require(p.is_file(),'missing '+str(p.relative_to(ROOT)))
 require(p.stat().st_size==rec.get('bytes',rec.get('size',p.stat().st_size)),'byte drift '+str(p))
 require(sha(p)==rec['sha256'],'SHA drift '+str(p))
 if mode:require(stat.S_IMODE(p.stat().st_mode)==rec['mode'],'mode drift '+str(p))
def seal(root,records):
 for r in records:match(root/r['path'],r)
 return len(records)
def routing_input(rec):
 snapshot=HERE/'routing-before'/rec['path']
 if snapshot.is_file():
  match(snapshot,rec)
  return sha(path(rec['path']))!=rec['sha256']
 match(path(rec['path']),rec);return False

def custody(controls):
 inventory=read(HERE/'dependency/inventory.json')
 require(len(inventory['files'])==251,'connected inventory count drift')
 for r in inventory['files']:match(path(r['path']),r,True)
 cb=read(CONE/'BASE.json');rb=read(REUSE/'BASE.json');pub=read(HERE/'BASE.json')
 for r in cb['inputs']:match(path(r['path']),r)
 drift=[]
 for r in rb['inputs']:
  if routing_input(r):drift.append(r['path'])
 for r in pub['pins']:routing_input(r)
 cs=read(CONE/'OUTPUTS.json');rs=read(REUSE/'OUTPUTS.json')['files']
 if isinstance(rs,dict):rs=[dict(path=k,**v) for k,v in rs.items()]
 require(len(cs)==88 and len(rs)==69,'sealed record count drift')
 seal(CONE,cs);seal(REUSE,rs)
 before=json.loads(gzip.decompress((HERE/'ARCHIVE.before.json.gz').read_bytes()))
 after=read(ROOT/'audits/ARCHIVE.json');additions=read(HERE/'archive-additions.json')
 require(hashlib.sha256(gzip.decompress((HERE/'ARCHIVE.before.json.gz').read_bytes())).hexdigest()==additions['old_metadata_sha256'],'prior ARCHIVE snapshot hash mismatch')
 require(additions['prior_records_unchanged'] is True,'prior archive preservation flag mismatch')
 added={'files':additions['files'],'blobs':additions['new_blobs']}
 for kind in ('files','blobs'):
  for k,v in before[kind].items():require(after[kind].get(k)==v,'old ARCHIVE record changed '+k)
  require(set(after[kind])-set(before[kind])==set(added[kind]),'unexpected ARCHIVE additions '+kind)
  for k,v in added[kind].items():require(after[kind].get(k)==v,'addition record mismatch '+k)
 require(len(added['files'])==35 and len(added['blobs'])==32,'archive addition count drift')
 raw=compressed=0
 for source,r in added['files'].items():match(path(source),r,True);raw+=r['bytes']
 for uncompressed,r in added['blobs'].items():
  blob=path(r['path']);match(blob,r);compressed+=r['bytes'];h=hashlib.sha256();size=0
  with gzip.open(blob,'rb') as stream:
   for chunk in iter(lambda:stream.read(1048576),b''):h.update(chunk);size+=len(chunk)
  require(h.hexdigest()==uncompressed,'gzip payload drift '+r['path'])
  expected={x['bytes'] for x in added['files'].values() if x['sha256']==uncompressed}
  require(expected=={size},'gzip uncompressed size mismatch '+r['path'])
 control=None
 if controls:
  bad=dict(cs[0]);bad['sha256']='0'*64
  try:seal(CONE,[bad])
  except ValueError:control='PASS: altered seal SHA rejected in memory'
  require(control is not None,'negative control unexpectedly passed')
 return {'status':'PASS','connected_files':251,'cone_BASE_inputs':len(cb['inputs']),
  'reuse_BASE_inputs':len(rb['inputs']),'cone_sealed_files':len(cs),'reuse_sealed_files':len(rs),
  'authorized_routing_drift_checked_against_before_snapshot':drift,
  'old_ARCHIVE_file_records_preserved':len(before['files']),'old_ARCHIVE_blob_records_preserved':len(before['blobs']),
  'new_archive_paths':35,'new_archive_blobs':32,'new_raw_bytes':raw,'new_compressed_bytes':compressed,
  'negative_control':control,'uses_git_metadata':False}

def numerical():
 import numpy as np
 from scipy.sparse import csr_matrix,vstack
 sys.path.insert(0,str(OPT))
 from model import Model
 run=REUSE/'specialized/runs/feasibility-60s';inp=read(run/'input.json');result=read(run/'result.json')
 rel='audits/2026-10-20-w7-count-opt-d5b8a86/runs/all-cu-pdlp/vectors.npz'
 recorded='/home/ray/developer/ai/math/'+rel
 require(inp['warm']==recorded,'unexpected recorded absolute warm path')
 warm_path=path(rel);require(sha(warm_path)==inp['warm_sha256'],'warm SHA mismatch')
 for n,h in inp['source_sha256'].items():
  require(Path(n).name==n,'unsafe recorded source name');require(sha(REUSE/'specialized'/n)==h,'trial source SHA mismatch '+n)
 m=Model();ref=m.reference('mindeg');D=m.difference(ref);Q=m.positivity_rows(ref)
 A=vstack([D,csr_matrix(Q)],format='csr');warm=np.load(warm_path);vectors=np.load(run/'vectors.npz')
 require(np.array_equal(ref,warm['ref']) and np.array_equal(ref,vectors['ref']),'reference mismatch')
 def metrics(x):
  require(x.shape==(m.nx,) and np.isfinite(x).all() and x.min()>=0,'invalid primal vector')
  ax=A@x;d=ax[:2*m.ns];q=ax[2*m.ns:];balance=float(abs(d).max());pos=float(np.maximum(2-q,0).max())
  return {'balance_inf':balance,'balance_l2':float(np.linalg.norm(d)),'positivity_violation':pos,
   'primal_residual_inf':max(balance,pos,float(max(0,-x.min()))),'PZ_ten':(q/2).tolist(),
   'sum_x':float(x.sum()),'min_x':float(x.min()),'support_1e-9':int(np.count_nonzero(x>1e-9))}
 checked={}
 for label,x in [('initial',np.maximum(warm['x'],0)),('final',vectors['x']),('best',vectors['best_x'])]:
  actual=metrics(x)
  for k,v in actual.items():require(np.allclose(v,result[label][k],rtol=1e-12,atol=1e-11),'trial metric mismatch '+label+'/'+k)
  checked[label]=actual
 # Independently form the nonnegative majorant |L|C without importing the
 # compiled operator, then verify every coefficient and recorded bound.
 C=m.incidence().tocsr();other=np.array([[p for p in range(3) if p!=r] for r in ref])
 rr=(3*np.arange(m.ns)[:,None]+other).reshape(-1)
 refs=np.repeat(3*np.arange(m.ns)+ref,2)
 B=vstack([C[rr]+C[refs],csr_matrix(Q)],format='csr')
 diff=abs(A)-B;require(not diff.nnz or diff.data.max()<=0,'invalid |A| majorant')
 row=np.asarray(B.sum(axis=1)).reshape(-1);col=np.asarray(B.sum(axis=0)).reshape(-1)
 scaling=inp['scaling'];eta=scaling['eta'];require(0<eta<1 and row.min()>0 and col.min()>0,'invalid scaling bounds')
 require(np.allclose([row.min(),row.max()],scaling['row_bound_min_max'],rtol=1e-12),'row bound mismatch')
 require(np.allclose([col.min(),col.max()],scaling['column_bound_min_max'],rtol=1e-12),'column bound mismatch')
 require(np.isfinite(vectors['y']).all() and vectors['y'][2*m.ns:].max()<=0,'invalid feasibility dual')
 require(result['stop']=='time limit' and result['seconds']>=inp['requested_seconds'],'trial stop mismatch')
 require(result['necessary_cone']=='OPEN' and result['no_source_or_feasibility_verdict'] is True,'trial authority drift')
 require(checked['best']['primal_residual_inf']<=checked['initial']['primal_residual_inf']+1e-11,'best candidate drift')
 return {'status':'PASS: saved numerical trial independently recomputed; no solver',
  'warm_resolved_under_current_checkout':rel,'recorded_absolute_path_used_only_as_provenance':recorded,
  'majorant_and_diagonal_norm_bound_verified':True,'matrix_shape':list(A.shape),'matrix_nnz':int(A.nnz),
  'iterations':result['iterations'],'seconds':result['seconds'],'checks':checked,'necessary_cone':'OPEN'}

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--numerical',action='store_true');p.add_argument('--controls',action='store_true');args=p.parse_args()
 out={'custody':custody(args.controls)}
 if args.numerical:out['numerical']=numerical()
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
