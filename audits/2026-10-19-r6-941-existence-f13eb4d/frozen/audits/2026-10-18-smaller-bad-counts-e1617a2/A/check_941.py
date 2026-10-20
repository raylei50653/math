#!/usr/bin/env python3
"""Exact stdlib replay of the941same-vector counted and planar-span controls."""
import hashlib,itertools,json
from fractions import Fraction
from pathlib import Path
import count_cone
R=Path(__file__).resolve().parent
F=R.parent/'frozen/audits/2026-10-18-smaller-bad-e1617a2'
d=json.loads((F/'kempe-consistency.json').read_text())
p=json.loads((F/'candidate-projections.json').read_text())['complete_local_records']
c=json.loads((R/'cone-triangulated.json').read_text())
cert=json.loads((R/'941-counted-candidate-probes.json').read_text())
span=json.loads((R/'941-counted-span.json').read_text())
assert c==count_cone.build()
for name,h in span['inputs'].items():assert hashlib.sha256((R/name).read_bytes()).hexdigest()==h
for recs in (cert['results'],span['results']):
 assert len(recs)==3 and {r['candidate'] for r in recs}=={'Q1','Q2','GB'}
cols=[]
for part in count_cone.partitions():
 if any(part[a]==part[k] and part[b]==part[e] and part[a]!=part[b] for a,b,k,e in itertools.combinations(range(8),4)):continue
 col=[int(all(part[i]!=part[j] or t[i]==t[j] for i in range(8) for j in range(i))) for t in d['tuples']]
 if any(col):cols.append(col)
assert len(cols)==91
summary=[]
for rec in cert['results']:
 name=rec['candidate'];assert rec['feasible'] is True
 live=[i for i in d['results'][2]['surviving_ids'] if not (p[i]['local_candidate_masks'][name]&82)]
 assert rec['allowed_ids']==live
 allowed=[j for j,col in enumerate(c['columns']) if all(c['rows'][r]['tuple_id'] in live for r,v in col['entries'])]
 assert rec['allowed_columns']==allowed
 z=rec['counts'];assert len(z)==274 and all(isinstance(v,int) and v>=0 for v in z)
 assert all(not v for i,v in enumerate(z) if i not in live)
 residual=[-row['orbit_size']*z[row['tuple_id']] for row in c['rows']]
 for j,w in rec['orbit_weights']:
  assert j in allowed and isinstance(w,int) and w>0
  for r,v in c['columns'][j]['entries']:residual[r]+=v*w
 assert not any(residual)
 coeff=[Fraction(v) for v in next(r for r in span['results'] if r['candidate']==name)['coefficient_vector']]
 assert len(coeff)==91
 assert [sum(col[i]*v for col,v in zip(cols,coeff)) for i in range(274)]==z
 original=0;candidate=0;masks=dict.fromkeys(('Q1','Q2','GB'),0)
 for i,v in enumerate(z):
  if v:
   original|=d['old_lift_masks'][i]
   candidate|=p[i]['local_candidate_masks'][name]
   for n in masks:masks[n]|=p[i]['local_candidate_masks'][n]
 assert original==rec['original_mask']==941
 assert candidate==rec['candidate_mask']==932
 assert candidate&512 and not candidate&82
 summary.append({'specified_candidate':name,'positive_C8_states':sum(bool(v) for v in z),'original_mask':original,'all_candidate_masks':masks})
print(json.dumps({'pass':True,'exact_count_cone_and_same_vector_planar_span':True,'source_realized':False,'results':summary}))
