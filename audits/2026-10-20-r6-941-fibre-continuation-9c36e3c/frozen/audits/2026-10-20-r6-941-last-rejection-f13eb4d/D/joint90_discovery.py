from pathlib import Path
D=Path(__file__).resolve().parent
exec((D/'joint_discovery.py').read_text().split('out=[]')[0])
from functools import lru_cache
close=lru_cache(maxsize=50000)(close)
c=json.loads((OLD/'C/certificate.json').read_text());unique={v['signature_id']:v for v in c['candidates']}
for k,v in unique.items():
 g='P'+str(k);E=[[0]*274 for _ in range(10)];sig=list(map(len,v['lifts']))
 for j,n,R,L,q,ei,ri,good in c['exterior_records']:
  if good:E[j][ei]+=sig[ri]
 mat=[[0]*2461 for _ in range(10)]
 for j,row in enumerate(E):
  for e,w in enumerate(row):
   if w:
    for i,t in I['T'][e]:mat[j][i]+=w*t
 M[g]=mat;bits[g]=[sum(1<<i for i,v in enumerate(r) if v) for r in mat]
 zeros[g]={mask:full^sum(1<<i for i in range(2461) if any(mat[j][i] for j in range(10) if not mask>>j&1)) for mask in cat}
print('90 matrices ready',flush=True)
out=[]
for branch,g,target in [('a1','Q1','J1'),('a2','Q2','J2')]:
 seed=close(base&~bits[g][9]);gs=['J1','J2','Q1','Q2','GB']+['P'+str(k) for k in sorted(unique)]
 force={target:[935,942,943] if target=='J1' else [943]}
 other='Q2' if g=='Q1' else 'Q1';force[other]=[mask for mask in cat if mask>>9&1]
 force['GB']=[mask for mask in cat if mask>>9&1 and mask>>6&1]
 live,ds=domains(seed,gs,force)
 out.append({'branch':branch,'live':[i for i in range(2461) if live>>i&1],'domains':ds})
 print(branch,'END',live.bit_count(),close.cache_info(),flush=True)
(D/'joint90_discovery.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
