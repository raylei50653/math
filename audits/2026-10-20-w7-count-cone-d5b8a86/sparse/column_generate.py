#!/usr/bin/env python3
"""Numerical sparse column generation; restrictions never exclude full cone."""
import argparse,gzip,json,pickle,time
from pathlib import Path
import numpy as np
import highspy
from scipy.sparse import coo_matrix,csr_matrix,vstack
P=Path(__file__).resolve().parent; SOURCE=P.parents[1]/'2026-10-20-r6-941-j1-five-edge-417732f/counting'

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--name',required=True);ap.add_argument('--max-cols',type=int,default=15000);ap.add_argument('--batch',type=int,default=250);ap.add_argument('--seconds',type=float,default=300);ap.add_argument('--target',type=int,default=44459); args=ap.parse_args()
 out=P/args.name;out.mkdir(exist_ok=False);start=time.monotonic()
 orb=json.load(gzip.open(SOURCE/'orbits.json.gz','rt'));live=orb['live'];li={s:i for i,s in enumerate(live)};rowids=dict(orb['rowids']);sr={s:[] for s in live}
 for r,s in orb['rowids']:
  if s in sr:sr[s].append(r)
 for rs in sr.values():rs.sort()
 # Use each state's last row as reference, including targets' singleton rows.
 rowcoef={}
 for s,rs in sr.items():
  i=li[s]
  rowcoef[rs[2]]=[(2*i,-1.),(2*i+1,-1.)]
  rowcoef[rs[0]]=[(2*i,1.)];rowcoef[rs[1]]=[(2*i+1,1.)]
 rr=[];cc=[];vv=[];targetrow=sr[args.target][2]
 for j,col in enumerate(orb['columns']):
  for r in col:
   for x,v in rowcoef[r]:rr.append(x);cc.append(j);vv.append(v)
   if r==targetrow:rr.append(2*len(live));cc.append(j);vv.append(1.)
 A=coo_matrix((vv,(rr,cc)),shape=(2*len(live)+1,len(orb['columns']))).tocsc();A.sum_duplicates();A.eliminate_zeros()
 selected={j for j,c in enumerate(orb['columns']) if any(rowids[r]==args.target for r in c)}
 history=[];last=None
 while len(selected)<=args.max_cols and time.monotonic()-start<args.seconds:
  js=np.array(sorted(selected),dtype=int);m=A[:,js].tocsr();rows=np.flatnonzero(np.diff(m.indptr));m=m[rows,:];b=np.zeros(len(rows));b[np.where(rows==2*len(live))[0]]=1.
  lp=highspy.HighsLp();lp.num_col_=len(js);lp.num_row_=len(rows);lp.col_cost_=np.ones(len(js));lp.col_lower_=np.zeros(len(js));lp.col_upper_=np.full(len(js),highspy.kHighsInf);lp.row_lower_=b;lp.row_upper_=b;lp.a_matrix_.format_=highspy.MatrixFormat.kRowwise;lp.a_matrix_.start_=m.indptr;lp.a_matrix_.index_=m.indices;lp.a_matrix_.value_=m.data
  h=highspy.Highs();h.setOptionValue('solver','simplex');h.setOptionValue('presolve','off');h.setOptionValue('output_flag',False);h.setOptionValue('threads',1);h.setOptionValue('time_limit',min(40.,args.seconds-(time.monotonic()-start)));h.passModel(lp);h.run()
  st=h.getModelStatus();info=h.getInfo();rec={'iteration':len(history),'columns':len(js),'rows':len(rows),'status':str(st),'elapsed':time.monotonic()-start,'simplex_iterations':info.simplex_iteration_count}
  if st==highspy.HighsModelStatus.kOptimal:
   sol=h.getSolution();vals=np.array(sol.col_value);r=m@vals-b;rec.update({'objective':info.objective_function_value,'residual':float(abs(r).max()),'support':int((vals>1e-9).sum())});last={'columns':js.tolist(),'values':vals.tolist(),'rows':rows.tolist(),'row_dual':sol.row_dual};history.append(rec);print(json.dumps(rec),flush=True);break
  if st!=highspy.HighsModelStatus.kInfeasible:
   last={'selected_columns':js.tolist(),'rows':rows.tolist(),'status':str(st)};history.append(rec);print(json.dumps(rec),flush=True);break
  status,exists,ray=h.getDualRay()
  if not exists:
   rec['ray']='absent';history.append(rec);print(json.dumps(rec),flush=True);break
  ray=np.array(ray);prod=float(ray@b)
  if prod>0:ray=-ray;prod=-prod
  dual=np.zeros(A.shape[0]);dual[rows]=ray;prices=A.T@dual;prices[js]=np.inf
  neg=np.flatnonzero(prices < -1e-8);rec.update({'ray_rhs':prod,'minimum_price':float(prices.min()),'negative_prices':len(neg)})
  history.append(rec);print(json.dumps(rec),flush=True)
  if not len(neg):
   last={'rows':rows.tolist(),'dual_ray':ray.tolist()};break
  chosen=neg[np.argsort(prices[neg],kind='stable')[:args.batch]];selected.update(chosen.tolist())
 (out/'history.json').write_text(json.dumps({'arguments':vars(args),'history':history,'elapsed':time.monotonic()-start},indent=2)+'\n')
 if last is None:last={'selected_columns':sorted(selected)}
 if last:
  with (out/'result.pickle').open('wb') as f:pickle.dump(last,f)

if __name__=='__main__':main()
