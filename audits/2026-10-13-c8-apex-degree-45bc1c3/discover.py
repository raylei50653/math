#!/usr/bin/env python3
"""Optional SciPy discovery only. Exact acceptance is exclusively check.py."""
import argparse,json,itertools
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix,hstack
import check

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,required=True);args=ap.parse_args();args.output_dir.mkdir(parents=True,exist_ok=True)
 data={k:json.loads(p.read_text()) for k,p in check.SOURCES.items()};r=data['results'];cone=data['cone'];E=np.array(data['counts']['equality_rows']);rp=np.array(cone['row_to_pattern']);words=list(map(tuple,r['pattern_order']));wi={p:i for i,p in enumerate(words)}
 rows=[];cols=[];values=[]
 for j,c in enumerate(cone['columns']):
  for i,v in c['entries']:rows.append(i);cols.append(j);values.append(v)
 V=csr_matrix((values,(rows,cols)),shape=(821,len(cone['columns'])))
 for qid,name in [('c04-941','a1'),('c07-941','a4')]:
  q=next(q for q in r['queries'] if q['query_id']==qid);a=q['boundary_order'].index(name);upper=q['support'];rejected=[i for i in range(274) if not upper>>i&1];keep=[j for j,c in enumerate(cone['columns']) if all(upper>>int(rp[i])&1 for i,v in c['entries'])];W=V[:,keep]
  ts=set()
  for p in words:
   if p[(a-1)%8]!=p[(a+1)%8]:continue
   triple=[]
   for c in range(4):
    if c==p[(a-1)%8]:continue
    word=list(p);word[a]=c;triple.append(wi[check.norm(word)])
   ts.add(tuple(sorted(triple)))
  G=[];gs=[]
  for triple in sorted(ts):
   for p in sorted(set(triple)):
    d=Counter(triple);d[p]-=2;G.append(sum(n*E[i] for i,n in d.items()));gs.append((triple,p))
  G=np.array(G);T=np.array(check.transfer(q,words,r['outer_pattern_order']));target=T[9]@E
  D=hstack([csr_matrix(E[rp].T),csr_matrix(E[rejected].T),csr_matrix(G.T)]);Dub=hstack([W.T,csr_matrix((len(keep),len(rejected)+len(G)))])
  lp=linprog(np.zeros(D.shape[1]),A_eq=D,b_eq=-target,A_ub=-Dub,b_ub=np.zeros(len(keep)),bounds=[(None,None)]*(821+len(rejected))+[(0,None)]*len(G),method='highs');assert lp.success
  v=[F(float(x)).limit_denominator(1000000) for x in lp.x];z=v[:821];az=v[821:821+len(rejected)];b=v[821+len(rejected):]
  for j in range(91):assert sum(F(int(E[rp[i],j]))*z[i] for i in range(821))+sum(F(int(E[p,j]))*c for p,c in zip(rejected,az))+sum(F(int(G[i,j]))*b[i] for i in range(len(G)))==-int(target[j])
  assert all(c>=0 for c in b);co=[sum(z[i]*v for i,v in cone['columns'][k]['entries']) for k in keep];assert all(c>=0 for c in co)
  out={'query_id':qid,'apex':name,'apex_position':a,'target_outer_index':9,'zero_rows':rejected,'kept_orbits':keep,'normalizer_dual':[[i,str(c)] for i,c in enumerate(z) if c],'zero_dual':[[p,str(c)] for p,c in zip(rejected,az) if c],'degree3_dual':[[list(gs[i][0]),gs[i][1],str(c)] for i,c in enumerate(b) if c],'orbit_nonnegative_coefficients':[[k,str(c)] for k,c in zip(keep,co) if c]}
  fn=f'dual-{qid[:3]}-{name}.json';(args.output_dir/fn).write_text(json.dumps(out,indent=2)+'\n');print(qid,name,'candidate exact identity checked; validate package with check.py')
if __name__=='__main__':main()
