"""Independent direct integer arithmetic; does not use the discovery sparse E/U."""
from pathlib import Path
import pickle,gzip,json,hashlib
D=Path(__file__).resolve().parent;A=D.parent
with (A/'counting/discovery.pickle').open('rb') as f:K,*ignored=pickle.load(f)
C=A/'geometry/orbit-farkas-certificate.json';c=json.loads(C.read_text());I=json.load(gzip.open(A/'frozen/audits/2026-10-20-r6-941-j1-w5-9c36e3c/interface/certificate-v4.json.gz','rt'));n=len(K['states']);nh=len(K['hrows']);nc=len(K['columns']);live=set(I['live'])
assert c['positive_row_multipliers']==[[9,16]]
lam=dict(c['equality_multipliers']);assert len(lam)==len(c['equality_multipliers']);assert all(0<=r<nh for r in lam)
z=[0]*n
for h,(s,i) in enumerate(zip(K['hsize'],K['rowids'])):z[i]+=s*lam.get(h,0)
for w in I['witnesses']:z[w['canonical_id']]+=16
x=[-sum(lam.get(h,0)*v for h,v in col) for col in K['columns']]
assert all(z[i]<=0 for i in live);assert max(x)<=0
slacks=[[i,-z[i]] for i in sorted(live) if z[i]]+[[n+j,-v] for j,v in enumerate(x) if v]
assert slacks==c['nonnegative_slacks']
assert c['positive_weight_sum']==16
out={'status':'PASS; exact count-only identity independently recomputed','certificate_sha256':hashlib.sha256(C.read_bytes()).hexdigest(),'equality_multipliers':len(lam),'live_core_slacks':sum(z[i]<0 for i in live),'orbit_slacks':sum(v<0 for v in x),'strict_positive_quantity':'16*(z5093+z5100)','signed_span_multipliers':0,'uses_sparse_discovery_matrices':False}
print(json.dumps(out,sort_keys=True))
