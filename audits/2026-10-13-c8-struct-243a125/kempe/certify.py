#!/usr/bin/env python3
"""SciPy discovery followed by exact rational validation before serialization."""
from discover import *
from fractions import Fraction as Q

def rat(v):return [Q(float(x)).limit_denominator(10000000) for x in v]
def sparse(v):return [[i,str(a)] for i,a in enumerate(v) if a]
def exact_primal(v,keep,data,E):
 a=rat(v);ls=a[:len(keep)];cs=a[len(keep):]
 x=[sum(Q(e)*c for e,c in zip(row,cs)) for row in E]
 z=[Q(0)]*len(data['rows'])
 for j,l in zip(keep,ls):
  for i,c in data['columns'][j]['entries']:z[i]+=l*c
 assert all(l>=0 for l in ls)
 assert all(z[i]==x[p] for i,p in enumerate(data['row_to_pattern'])),'exact primal failed'
 return ls,cs,x

def main():
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('--input-dir',type=Path,default=HERE);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
 data=json.loads((args.input_dir/'cone.triangulated.json').read_text());V=matrix(data);rp=np.array(data['row_to_pattern']);
 cert=json.loads((OLD/'counts/certificate.v2.json').read_text());E=np.array(cert['equality_rows']);
 interface=json.loads((OLD/'interface.json').read_text());cases={c['id']:c for c in interface['cases']}
 discovery=json.loads((args.input_dir/'discovery.triangulated.json').read_text());sparse_discovery=json.loads((args.input_dir/'discovery.triangulated.sparse.json').read_text())
 qs={(q['case_id'],q['target']):q for q in cert['queries'] if q['status']=='necessary_condition_residual'}
 out={'schema':'c8-struct-fixed-split-count-v1','pattern_order':cert['pattern_order'],'color_frame':[0,1,2,3],'queries':[]}
 for d,sd in zip(discovery,sparse_discovery):
  q=qs[d['case_id'],d['target']];upper=q['final_upper_mask'];allowed=[i for i in range(274) if upper>>i&1];rejected=[i for i in range(274) if not upper>>i&1]
  keep=d['allowed_columns'];W=V[:,keep];T=np.array(cases[q['case_id']]['transfer']);acc=[i for i in range(10) if q['target']>>i&1]
  r={'boundary_order':cases[q['case_id']]['boundary_order'],'supports':cases[q['case_id']]['supports'],'extras':cases[q['case_id']]['extras'],'case_id':q['case_id'],'target':q['target'],'status':'necessary-condition residual','old_upper':upper,'allowed_columns':keep}
  init=d['joint_float'] if d['joint_status']==0 else sd['joint_float']
  ls,cs,x=exact_primal(init,keep,data,E)
  forced=[]
  if d['joint_status']!=0:
   Aeq=vstack([hstack([W,csr_matrix(-E[rp])]),hstack([csr_matrix((len(rejected),len(keep))),csr_matrix(E[rejected])])]);beq=np.zeros(Aeq.shape[0])
   for i in allowed:
    if x[i]:continue
    positive=np.vstack([T[acc]@E,E[i]])
    Aub=hstack([csr_matrix((len(positive),len(keep))),csr_matrix(-positive)])
    lp=linprog(np.zeros(len(keep)+91),A_eq=Aeq,b_eq=beq,A_ub=Aub,b_ub=-np.ones(len(positive)),bounds=[(0,None)]*len(keep)+[(None,None)]*91,method='highs')
    if lp.success:
     al,ac,ax=exact_primal(lp.x,keep,data,E)
     ls=[a+b for a,b in zip(ls,al)];cs=[a+b for a,b in zip(cs,ac)];x=[a+b for a,b in zip(x,ax)]
     print(q['case_id'],'add support',i,flush=True)
    else:
     assert lp.status==2
     # 0 = sum lambda_j*(W^T z)_j + x_i; hence x_i=0.
     Deq=hstack([csr_matrix(-E[rp].T),csr_matrix(E[rejected].T)])
     Dub=hstack([W.T,csr_matrix((len(keep),len(rejected)))])
     dual=linprog(np.zeros(821+len(rejected)),A_eq=Deq,b_eq=E[i],A_ub=-Dub,b_ub=np.zeros(len(keep)),bounds=(None,None),method='highs')
     assert dual.success
     dv=rat(dual.x);z=dv[:821];a=dv[821:]
     assert all(sum(Q(e)*c for e,c in zip(-E[rp,j],z))+sum(Q(e)*c for e,c in zip(E[rejected,j],a))==E[i,j] for j in range(91))
     assert all(sum(z[r]*v for r,v in data['columns'][k]['entries'])>=0 for k in keep)
     forced.append({'pattern':i,'word':cert['pattern_order'][i],'normalizer_dual':sparse(z),'zero_count_dual':[[p,str(v)] for p,v in zip(rejected,a) if v]})
     print(q['case_id'],'forced zero',i,flush=True)
  support=sum(1<<i for i,v in enumerate(x) if v)
  assert set(allowed)-{i for i,v in enumerate(x) if v}=={f['pattern'] for f in forced}
  outer=[sum(Q(v)*c for v,c in zip(row,x)) for row in T]
  assert all(v>0 if i in acc else v==0 for i,v in enumerate(outer))
  r.update(counts=list(map(str,x)),partition_coefficients=list(map(str,cs)),orbit_coefficients=[[j,str(v)] for j,v in zip(keep,ls) if v],outer_counts=list(map(str,outer)),support=support,forced_zeros=forced)
  oldx=[Q(v) for v in q['counts']]
  if d['original_status']==0:
   oldls=rat(d['original_lambda_float']);zz=[Q(0)]*821
   for j,l in zip(keep,oldls):
    for i,v in data['columns'][j]['entries']:zz[i]+=l*v
   assert all(zz[i]==oldx[p] for i,p in enumerate(rp))
   r['old_vector']={'status':'passes new necessary condition','orbit_coefficients':[[j,str(v)] for j,v in zip(keep,oldls) if v]}
  else:
   dual=linprog(np.array([float(oldx[p]) for p in rp]),A_ub=-V.T,b_ub=np.zeros(V.shape[1]),bounds=(-1,1),method='highs')
   assert dual.success and dual.fun < -1e-6
   z=rat(dual.x)
   assert all(sum(z[i]*v for i,v in c['entries'])>=0 for c in data['columns'])
   dot=sum(oldx[p]*z[i] for i,p in enumerate(rp));assert dot<0
   r['old_vector']={'status':'counterexample to weakened claim','normalizer_dual':sparse(z),'dot':str(dot)}
  out['queries'].append(r)
  print(q['case_id'],q['target'],'support',support.bit_count(),'forced',len(forced),'exact PASS',flush=True)
 args.output.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n')
if __name__=='__main__':main()
