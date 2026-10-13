#!/usr/bin/env python3
"""Exact independent replay of conditional degree3 exclusions, Python standard library."""
import argparse,itertools,json,hashlib
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

HERE=Path(__file__).resolve().parent
BASE_MANIFEST=json.loads((HERE/'BASE.json').read_text())
SOURCES={k:HERE/BASE_MANIFEST['inputs'][k]['frozen'] for k in ['results','cone','counts']}

def norm(p):
 d={};return tuple(d.setdefault(c,len(d)) for c in p)

def transfer(query, words, outer_words):
 """Rebuild original collar transfer from all distinct literal lifts."""
 order=query['boundary_order'];edges=query['collar_edges']
 color_permutations=list(itertools.permutations(range(4)))
 lifts=[sorted({tuple(g[c] for c in p) for g in color_permutations}) for p in words]
 matrix=[]
 for outer in outer_words:
  row=[]
  for orbit in lifts:
   total=0
   for inner in orbit:
    colors={f'b{i}':c for i,c in enumerate(outer)}
    colors.update(zip(order,inner))
    total+=all(colors[u]!=colors[v] for u,v in edges)
   row.append(total)
  matrix.append(row)
 return matrix

def check(generate=False, certificate_path=None, dual_dir=None):
 certificate_path=certificate_path or HERE/'certificate.json';dual_dir=dual_dir or HERE
 for item in BASE_MANIFEST['inputs'].values():
  p=HERE/item['frozen'];assert p.stat().st_size==item['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256']
 data={k:json.loads(p.read_text()) for k,p in SOURCES.items()};r=data['results'];cone=data['cone'];E=data['counts']['equality_rows'];rp=cone['row_to_pattern'];words=list(map(tuple,r['pattern_order']));wi={p:i for i,p in enumerate(words)}
 assert len(words)==274 and len(rp)==821 and len(E)==274 and all(len(e)==91 for e in E)
 assert all(words[p]==norm(row) for p,row in zip(rp,cone['rows']))
 triples=[]
 for a in range(8):
  ts=set()
  for p in words:
   if p[(a-1)%8]!=p[(a+1)%8]:continue
   row=[]
   for c in range(4):
    if c==p[(a-1)%8]:continue
    q=list(p);q[a]=c;row.append(wi[norm(q)])
   assert len(row)==3;ts.add(tuple(sorted(row)))
  triples.append(sorted(ts))
 result={'schema':'c8-apex-degree3-exclusion-v1','input_sha256':{str(p.relative_to(HERE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in SOURCES.values()},'queries':[]}
 for q in r['queries']:
  if q['result']!='source not excluded':continue
  assert len(q['boundary_order'])==8
  T=transfer(q,words,r['outer_pattern_order'])
  for a,name in enumerate(q['boundary_order']):
   if not name.startswith('a'):continue
   S={i for i in range(274) if q['support']>>i&1};steps=[]
   while True:
    orig=S.copy();lost=set()
    for ts in triples[a]:
     present=[i for i in ts if i in S]
     if len(present)==1:lost.add(present[0])
    if lost:steps.append({'rule':'degree3','removed':sorted(lost)});S-=lost
    keep=[j for j,c in enumerate(cone['columns']) if all(rp[i] in S for i,v in c['entries'])]
    touched={i for j in keep for i,v in cone['columns'][j]['entries']}
    lost={rp[i] for i in range(len(rp)) if rp[i] in S and i not in touched}
    if lost:steps.append({'rule':'orbit','removed':sorted(lost)});S-=lost
    if S==orig:break
   missing=[j for j in range(10) if q['target']>>j&1 and not any(T[j][i] for i in S)]
   out={'query_id':q['query_id'],'apex':name,'apex_position':a,'initial_support_size':q['support'].bit_count(),'steps':steps,'final_support':sorted(S),'missing_accepted_outer_indices':missing}
   if missing:out['method']='support closure'
   else:
    fn={'c04-941':'dual-c04-a1.json','c07-941':'dual-c07-a4.json'}[q['query_id']];d=json.loads((dual_dir/fn).read_text())
    assert (d['query_id'],d['apex'],d['apex_position'])==(q['query_id'],name,a)
    rejected=[i for i in range(274) if not q['support']>>i&1]
    keep=[j for j,c in enumerate(cone['columns']) if all(q['support']>>rp[i]&1 for i,v in c['entries'])]
    assert d['zero_rows']==rejected and d['kept_orbits']==keep
    z=[F(0)]*821
    for i,c in d['normalizer_dual']:assert not z[i];z[i]=F(c)
    az={p:F(c) for p,c in d['zero_dual']};assert set(az)<=set(rejected)
    G=[]
    for ts,p,c in d['degree3_dual']:
     assert tuple(ts) in triples[a] and p in ts and F(c)>=0
     coeff=Counter(ts);coeff[p]-=2;G.append((coeff,F(c)))
    target=d['target_outer_index'];assert target==9 and q['target']>>target&1
    for j in range(91):
     lhs=sum(E[rp[i]][j]*z[i] for i in range(821))+sum(E[p][j]*c for p,c in az.items())+sum(c*sum(n*E[p][j] for p,n in coeff.items()) for coeff,c in G)
     rhs=-sum(T[target][p]*E[p][j] for p in range(274));assert lhs==rhs,(q['query_id'],name,j,lhs,rhs)
    orbit_coeff=[(j,sum(z[i]*v for i,v in cone['columns'][j]['entries'])) for j in keep]
    assert all(c>=0 for j,c in orbit_coeff)
    assert [[j,str(c)] for j,c in orbit_coeff if c]==d['orbit_nonnegative_coefficients']
    out.update(method='exact count dual',dual=fn,missing_accepted_outer_indices=[target])
   assert out['missing_accepted_outer_indices'];result['queries'].append(out)
 assert len(result['queries'])==40
 result['conclusions']={'all_eight_remaining_C8_sources_have_apex_H_degree_at_least':4,'apex_original_degree_at_least':6,'strict_C8_inner_degree5_vertices_at_least':6,'h3_original_inner_vertices_at_least':14,'h_lower_bound':3,'global_n5_lower_bound':9,'new_whole_C8_queries_excluded':0}
 output=certificate_path
 if generate:output.write_text(json.dumps(result,indent=2)+'\n')
 else:assert json.loads(output.read_text())==result
 print('PASS: 40 conditional apex-degree3 exclusions (38 support, 2 exact count duals); h=3 implies at least 14 original inner vertices.')
 return result
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--generate',action='store_true');ap.add_argument('--check',action='store_true');args=ap.parse_args();check(args.generate)
