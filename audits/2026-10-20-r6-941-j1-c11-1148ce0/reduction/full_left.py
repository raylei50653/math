#!/usr/bin/env python3
"""Complete <=2 original induced seven-rim family, including a=u2 quotients."""
from right_contractions import *
def left_relations():
 ans={};counts={}
 for k in range(3):
  counts[k]=0
  for fs in p.all_triangulations(k):
   counts[k]+=1;es=sorted({e for f in fs for e in combinations(f,2)}-p.BOUND);sigs=defaultdict(int)
   for i,t in enumerate(p.STATES):
    for ex in product(range(4),repeat=k):
     c=t+ex;sig=sum(1<<j for j,(u,v) in enumerate(es) if c[u]==c[v]);sigs[sig]|=1<<i
   for sig,sup in sigs.items():
    al=[a for a in p.ALPHA_IDS if sup&(1<<a)]
    if not al:continue
    cl=classes(7,k,es,sig)
    assert not any(0 in g and 1 in g for g in cl)
    delta=len(cl)-11
    if sup in ans and ans[sup]['completed_delta']<=delta:continue
    ans[sup]={'interior':k,'faces':fs,'new_edges':es,'equal_signature':sig,'classes':cl,'completed_delta':delta,'alpha_ids':al,'support_ids':[i for i in range(91) if sup&(1<<i)]}
 return ans,counts
if __name__=='__main__':
 ans,counts=left_relations()
 with (D/'full-left-relations.json.gz').open('xb') as f:
  with gzip.GzipFile(fileobj=f,mode='wb',mtime=0) as g:g.write(json.dumps(ans,sort_keys=True,separators=(',',':')).encode()+b'\n')
 print(json.dumps({'relations':len(ans),'triangulations':counts,'includes_a_u2_quotients':True}))
