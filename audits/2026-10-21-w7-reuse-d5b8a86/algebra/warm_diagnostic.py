#!/usr/bin/env python3
"""Read-only diagnostics of the original-coordinate cuOpt warm vector; no solve."""
import hashlib,json,sys
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.dont_write_bytecode=True
OPT=ROOT/'audits/2026-10-20-w7-count-opt-d5b8a86'
sys.path.insert(0,str(OPT))
from model import Model,LABELS
m=Model();path=OPT/'runs/all-cu-pdlp/vectors.npz';data=np.load(path)
ref=m.reference('mindeg');D=m.difference(ref);Q=m.positivity_rows(ref)
x=np.asarray(data['x']);y=np.asarray(data['y']);saved_ref=np.asarray(data['ref'])
assert x.shape==(m.nx,) and y.shape==(2*m.ns+10,) and np.array_equal(saved_ref,ref)
assert np.isfinite(x).all() and np.isfinite(y).all()
metrics=[]
for name,z in [('original',x),('clipped_nonnegative',np.maximum(x,0))]:
 dx=D@z;q=Q@z
 metrics.append({'vector':name,'min_x':float(z.min()),'max_x':float(z.max()),'sum_x':float(z.sum()),
  'negative_coordinates':int(np.count_nonzero(z<0)),'support_gt1e-9':int(np.count_nonzero(z>1e-9)),
  'D_residual_inf':float(np.max(abs(dx))),'D_residual_l2':float(np.linalg.norm(dx)),
  'D_residual_l2_per_sqrt_rowcount':float(np.linalg.norm(dx)/np.sqrt(len(dx))),
  'Q_values':q.tolist(),'PZ_values':(q/2).tolist(),'minimum_Q_minus2':float((q-2).min()),
  'positivity_violation_inf':float(np.maximum(2-q,0).max()),
  'combined_feasibility_violation_inf':float(max(np.max(abs(dx)),np.maximum(2-q,0).max(),max(0,-z.min())))})
# cuOpt y uses row-dual/KKT convention c-A^T y>=0. The sign test is
# diagnostic, not a certificate and not reused for feasibility c=0.
aty=D.T@y[:2*m.ns]+Q.T@y[2*m.ns:]
old_rc=1-aty
report={'status':'input diagnostics only; no new solve','warm_path':str(path.relative_to(ROOT)),
 'warm_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'keys':data.files,
 'shape_x':list(x.shape),'shape_y':list(y.shape),'saved_reference_matches_mindeg':True,
 'labels':LABELS,'scale':'Q_l X=2P_l Z; all ten lower bounds Q_l X>=2',
 'primal':metrics,
 'old_dual':{'saved_objective':'min sum(X)','min_y':float(y.min()),'max_y':float(y.max()),
  'positive_row_duals':y[2*m.ns:].tolist(),
  'min_reduced_cost_c_minus_ATy':float(old_rc.min()),
  'max_reduced_cost_c_minus_ATy':float(old_rc.max()),
  'saved_rc_max_abs_difference':float(np.max(abs(old_rc-data['reduced_costs']))) if 'reduced_costs' in data.files else None},
 'recommended_warm':'Use original x clipped to nonnegative (clipping is a no-op here); do not rescale; set all feasibility-PDHG dual coordinates to zero.',
 'why_no_old_dual':'Old y optimizes c=ones, while feasibility uses c=zero. For standard saddle F(Ax), lower-bound row duals have nonpositive sign, opposite the saved cuOpt lower-bound duals.',
 'recommended_metrics':['initial and final unscaled ||D X||_inf','minimum X and negative-coordinate count','all ten Q values and min(Q-2)','combined violation max(||D X||_inf,max(2-Q,0),max(-X,0))','last iterate and ergodic/best iterate separately','iterations, walltime and operator matvec count'],
 'scope':'A 60 s approximate feasibility trial may improve or worsen the warm residual. No cone/source verdict and no exact certificate.'}
(HERE/'warm-diagnostic.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
