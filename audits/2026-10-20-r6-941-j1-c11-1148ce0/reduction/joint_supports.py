#!/usr/bin/env python3
"""K132 domain closure for all generated left and right relations."""
from right_contractions import *
from collections import Counter
ROWS=('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
CAT=OLD/'frozen/audits/2026-10-20-r6-941-fibre-continuation-9c36e3c/frozen/audits/2026-10-20-r6-941-last-rejection-f13eb4d/frozen/audits/2026-10-19-r6-941-existence-f13eb4d/frozen/artifacts/c5_cells/cells.json'
def compute():
 inter=json.load(gzip.open(OLD/'interface/certificate-v4.json.gz','rt'));left={int(k):v for k,v in json.load(gzip.open(D/'left-relations.json.gz','rt')).items()}
 rstates,ridx,right,counts=right_relations(2)
 cats=set(map(int,json.loads(CAT.read_text())['cells']));pairs=defaultdict(int)
 for i in inter['live']:
  a,n,u2,u1,L,q,c,s,v,w,t=inter['caps'][i]['core']
  for x,y in product(range(4),repeat=2):
   if x in (c,s,y) or y in (a,t):continue
   rj=ridx[p.canonical((s,x,y,t,w,v))]
   for b in range(4):
    if b in (a,c,q):continue
    row=''.join(map(str,p.canonical((x,y,a,b,c))))
    lj=p.INDEX[p.canonical((a,b,q,L,u1,u2,n))]
    pairs[lj,rj]|=1<<ROWS.index(row)
 hist=Counter();bad=[];improve=[];strict=0
 for ls,lc in left.items():
  local=[0]*len(rstates)
  for rj in range(len(rstates)):
   for lj in lc['support_ids']:local[rj]|=pairs.get((lj,rj),0)
  for rs,rc in right.items():
   delta=lc['completed_delta']+1+rc['delta']
   if delta>=0:continue
   strict+=1;mask=0
   for rj in rc['support_ids']:mask|=local[rj]
   hist[mask]+=1
   if mask not in cats:
    bad.append({'left':lc,'right':rc,'mask':mask,'delta':delta})
    envelope=0
    for k in cats:
     if k&mask==k:envelope|=k
    if envelope!=mask:improve.append({'left':lc,'right':rc,'mask':mask,'K132_envelope':envelope,'delta':delta})
 return {'strict_candidate_pairs':strict,'histogram':dict(hist),'maximal_mask_not_K132_count':len(bad),'prunable_candidate_count':len(improve),'prunable':improve,'noncatalogue_examples':bad[:5]}
if __name__=='__main__':
 out=compute()
 with (D/'joint-supports.json').open('x') as f:json.dump(out,f,indent=2,sort_keys=True);f.write('\n')
 print(json.dumps({k:v for k,v in out.items() if k not in ('prunable','noncatalogue_examples')}))
 print(json.dumps(out['prunable'][:2]))
