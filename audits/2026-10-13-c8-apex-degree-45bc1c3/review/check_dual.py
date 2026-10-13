from pathlib import Path
import json,itertools
from fractions import Fraction as F
from collections import Counter
from transfer import transfer
import sys
package=Path(__file__).resolve().parent.parent
root=package/'frozen/audits/2026-10-13-c8-struct-243a125'
result=json.loads((root/'RESULTS.json').read_text())
cone=json.loads((root/'kempe/cone.triangulated.json').read_text())
old=root/'frozen/audits/2026-10-13-c8-joint-count-3097ef5'
E=json.loads((old/'counts/certificate.v2.json').read_text())['equality_rows']
cert=json.loads((package/sys.argv[1]).read_text())
q=next(q for q in result['queries'] if q['query_id']==cert['query_id'])
rows=[tuple(x) for x in result['pattern_order']]
T=transfer(q, rows, result['outer_pattern_order'])
lookup={p:i for i,p in enumerate(rows)}
def norm(p):
 d={}
 return tuple(d.setdefault(x,len(d)) for x in p)
a=q['boundary_order'].index(cert['apex'])
assert a==cert['apex_position']
positions=[i for i in range(8) if i!=a]
triples=set()
contexts=0
for values in itertools.product(range(4),repeat=7):
 p=dict(zip(positions,values))
 if p[(a-1)%8]!=p[(a+1)%8]:continue
 if any(i!=a and (i+1)%8!=a and p[i]==p[(i+1)%8] for i in range(8)):continue
 contexts+=1
 ts=[]
 for c in range(4):
  if c==p[(a-1)%8]:continue
  p[a]=c
  ts.append(lookup[norm([p[i] for i in range(8)])])
 triples.add(tuple(sorted(ts)))
zero=[i for i in range(274) if not (q['support']>>i)&1]
assert cert['zero_rows']==zero
assert cert['target_outer_index']==9 and (q['target']>>9)&1
z=dict((i,F(x)) for i,x in cert['normalizer_dual'])
az=dict((i,F(x)) for i,x in cert['zero_dual'])
assert set(az)<=set(zero)
assert all(0<=i<821 for i in z)
rp=cone['row_to_pattern']
coeff=[F(0)]*274
for i,v in z.items():coeff[rp[i]]+=v
for i,v in az.items():coeff[i]+=v
for ts,p,v in cert['degree3_dual']:
 assert tuple(ts) in triples and p in ts
 v=F(v)
 assert v>=0
 for i in ts:coeff[i]+=v
 coeff[p]-=2*v
for j in range(91):
 assert sum(coeff[i]*E[i][j] for i in range(274))==-sum(T[9][i]*E[i][j] for i in range(274))
keep=[i for i,c in enumerate(cone['columns']) if all((q['support']>>rp[row])&1 for row,v in c['entries'])]
assert keep==cert['kept_orbits']
dots={i:sum(z.get(row,F(0))*v for row,v in cone['columns'][i]['entries']) for i in keep}
assert min(dots.values())>=0
assert {i:v for i,v in dots.items() if v}=={i:F(v) for i,v in cert['orbit_nonnegative_coefficients']}
print(json.dumps({'status':'PASS','literal_contexts':contexts,'degree3_triples':len(triples),'query':q['query_id'],'apex':cert['apex'],'exact_span_coordinates':91,'allowed_orbits':len(keep),'minimum_dual_on_allowed_orbits':str(min(dots.values()))},sort_keys=True))
