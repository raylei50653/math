"""Direct integer check of the reduced 132-term orbit cancellation."""
from pathlib import Path
import pickle,gzip,json,hashlib
D=Path(__file__).resolve().parent;A=D.parent
with (A/'counting/discovery.pickle').open('rb') as f:K,*ignored=pickle.load(f)
I=json.load(gzip.open(A/'frozen/audits/2026-10-20-r6-941-j1-w5-9c36e3c/interface/certificate-v4.json.gz','rt'));live=set(I['live']);p=D/'reduced-orbit-certificate.json';cert=json.loads(p.read_text());lam=dict(cert['live_half_row_multipliers']);assert len(lam)==132==len(cert['live_half_row_multipliers']);assert set(lam.values())=={-1,1};assert sum(v==1 for v in lam.values())==64
assert all(K['rowids'][h] in live for h in lam)
co=[0]*len(K['states'])
for h,v in lam.items():co[K['rowids'][h]]+=v*K['hsize'][h]
assert {i:co[i] for i in live if co[i]}=={5093:-16,5100:-16}
good=[]
for j,col in enumerate(K['columns']):
 if all(K['rowids'][h] in live for h,v in col):
  good.append(j);assert sum(lam.get(h,0)*v for h,v in col)==0
assert len(good)==20794 and cert['live_columns']==good and cert['nonnegative_column_slacks']==[]
assert cert['witness_ids']==[5093,5100] and cert['positive_coefficient']==16
out={'status':'PASS; exact 132-term count cancellation','live_core_states':len(live),'live_half_rows':sum(i in live for i in K['rowids']),'live_columns':len(good),'positive_multiplier':16,'positive_half_rows':64,'negative_half_rows':68,'surviving_column_pairings_all_zero':True,'source_witness_count_forced_zero':True,'certificate_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
print(json.dumps(out,sort_keys=True))
