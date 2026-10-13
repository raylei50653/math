#!/usr/bin/env python3
import itertools as it, json, math
from collections import Counter
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix, hstack, vstack
HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'frozen/audits/2026-10-13-c8-joint-count-3097ef5'

def norm(p):
 d={}; return tuple(d.setdefault(c,len(d)) for c in p)

def partitions(n,w=()):
 if len(w)==n: yield w
 else:
  for c in range(max(w,default=-1)+2): yield from partitions(n,w+(c,))

def nc(w):
 return not any(w[a]==w[c] and w[b]==w[d] and w[a]!=w[b] for a,b,c,d in it.combinations(range(8),4))

def build(triangulated=False, output_dir=HERE):
 cert=json.loads((OLD/'counts/certificate.v2.json').read_text())
 words=list(map(tuple,cert['pattern_order'])); wi={p:i for i,p in enumerate(words)}
 group=[p for p in it.permutations(range(4)) if {p[0]//2,p[1]//2} in ({0},{1})]
 literal=[p for p in it.product(range(4),repeat=8) if all(p[i]!=p[(i+1)%8] for i in range(8))]
 canonical={p:min(tuple(g[c] for c in p) for g in group) for p in literal}
 reps=sorted(set(canonical.values())); ri={p:i for i,p in enumerate(reps)}
 rid={p:ri[q] for p,q in canonical.items()}
 row_sizes=Counter(rid.values()); ncparts=[q for q in partitions(8) if nc(q)]
 columns={}
 for r,p in enumerate(reps):
  for part in ncparts:
   if triangulated and max(part)+1 != sum(p[i]//2 != p[(i+1)%8]//2 for i in range(8))//2+1: continue
   blocks=[[i for i,c in enumerate(part) if c==b] for b in range(max(part)+1)]
   if any(len({p[i]//2 for i in b})>1 for b in blocks): continue
   if any(p[i]//2==p[(i+1)%8]//2 and part[i]!=part[(i+1)%8] for i in range(8)): continue
   counts=Counter(rid[tuple(c^(bits>>part[i]&1) for i,c in enumerate(p))] for bits in range(1<<len(blocks)))
   v={i:n*8//row_sizes[i] for i,n in counts.items()}
   d=math.gcd(*v.values()); col=tuple(sorted((i,n//d) for i,n in v.items()))
   columns.setdefault(col,(r,part,d))
 print('reps',len(reps),'columns',len(columns),flush=True)
 out={'group':group,'rows':reps,'row_sizes':[row_sizes[i] for i in range(len(reps))], 'row_to_pattern':[wi[norm(p)] for p in reps], 'columns':[{'seed_row':r,'partition':part,'gcd':d,'entries':col} for col,(r,part,d) in sorted(columns.items())]}
 (output_dir/('cone.triangulated.json' if triangulated else 'cone.generic.json')).write_text(json.dumps(out,separators=(',',':'),sort_keys=True)+'\n')
 return out,cert

def matrix(data):
 rows=[]; cols=[]; vals=[]
 for j,c in enumerate(data['columns']):
  for i,v in c['entries']: rows.append(i);cols.append(j);vals.append(v)
 return csr_matrix((vals,(rows,cols)),shape=(len(data['rows']),len(data['columns'])))

def main():
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('--triangulated',action='store_true');ap.add_argument('--sparse-support',action='store_true');ap.add_argument('--output-dir',type=Path,required=True);args=ap.parse_args()
 args.output_dir.mkdir(parents=True,exist_ok=True)
 triangulated=args.triangulated
 data,cert=build(triangulated,args.output_dir); V=matrix(data); rp=np.array(data['row_to_pattern']); E=np.array(cert['equality_rows'])
 interface=json.loads((OLD/'interface.json').read_text()); cases={c['id']:c for c in interface['cases']}
 results=[]
 for q in cert['queries']:
  if q['status']!='necessary_condition_residual':continue
  from fractions import Fraction as Q
  x=np.array([float(Q(a)) for a in q['counts']]); upper=q['final_upper_mask']
  allowed=[i for i in range(274) if upper>>i&1]; rejected=[i for i in range(274) if not upper>>i&1]
  keep=[j for j,c in enumerate(data['columns']) if all(upper>>data['row_to_pattern'][i]&1 for i,v in c['entries'])]
  W=V[:,keep]
  lp=linprog(np.zeros(len(keep)),A_eq=W,b_eq=x[rp],bounds=(0,None),method='highs')
  print(q['case_id'],q['target'],'old vector',lp.status,'columns',len(keep),flush=True)
  Aeq=hstack([W,csr_matrix(-E[rp])]);beq=np.zeros(len(rp))
  Zeq=hstack([csr_matrix((len(rejected),len(keep))),csr_matrix(E[rejected])]);
  Aeq=vstack([Aeq,Zeq]);beq=np.r_[beq,np.zeros(len(rejected))]
  T=np.array(cases[q['case_id']]['transfer']); acc=[i for i in range(10) if q['target']>>i&1]
  positive=T[acc]@E if args.sparse_support else np.vstack([T[acc]@E,E[allowed]])
  Aub=hstack([csr_matrix((len(positive),len(keep))),csr_matrix(-positive)]);
  joint=linprog(np.zeros(len(keep)+91),A_eq=Aeq,b_eq=beq,A_ub=Aub,b_ub=-np.ones(len(positive)),bounds=[(0,None)]*len(keep)+[(None,None)]*91,method='highs')
  print(q['case_id'],q['target'],'joint',joint.status,flush=True)
  r={'case_id':q['case_id'],'target':q['target'],'original_status':lp.status,'joint_status':joint.status,'allowed_columns':keep}
  if lp.success:r['original_lambda_float']=lp.x.tolist()
  if joint.success:r['joint_float']=joint.x.tolist()
  else:r['message']=joint.message
  results.append(r)
 (args.output_dir/('discovery.'+('triangulated' if triangulated else 'generic')+('.sparse' if args.sparse_support else '')+'.json')).write_text(json.dumps(results,separators=(',',':'),sort_keys=True)+'\n')
if __name__=='__main__':main()
