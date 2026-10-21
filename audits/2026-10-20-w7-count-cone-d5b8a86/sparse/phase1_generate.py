#!/usr/bin/env python3
"""Bounded-dual numerical column generation; no exact verdict on its own."""
import argparse,gzip,json,pickle,time
from pathlib import Path
import numpy as np
import highspy
from scipy.sparse import coo_matrix,csr_matrix,vstack,hstack
P=Path(__file__).resolve().parent;SOURCE=P.parents[1]/'2026-10-20-r6-941-j1-five-edge-417732f/counting'

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--name',required=True);ap.add_argument('--max-cols',type=int,default=18000);ap.add_argument('--batch',type=int,default=500);ap.add_argument('--seconds',type=float,default=280);ap.add_argument('--target',type=int,default=44459);ap.add_argument('--start',type=Path);args=ap.parse_args()
 out=P/args.name;out.mkdir(exist_ok=False);start=time.monotonic()
 orb=json.load(gzip.open(SOURCE/'orbits.json.gz','rt'));live=orb['live'];li={s:i for i,s in enumerate(live)};rowids=dict(orb['rowids']);sr={s:[] for s in live}
 for r,s in orb['rowids']:
  if s in sr:sr[s].append(r)
 for rs in sr.values():rs.sort()
 rowcoef={}
 for s,rs in sr.items():
  i=li[s];rowcoef[rs[2]]=[(2*i,-1.),(2*i+1,-1.)];rowcoef[rs[0]]=[(2*i,1.)];rowcoef[rs[1]]=[(2*i+1,1.)]
 rr=[];cc=[];vv=[];tr=2*len(live);targetrow=sr[args.target][2]
 for j,col in enumerate(orb['columns']):
  for r in col:
   for x,v in rowcoef[r]:rr.append(x);cc.append(j);vv.append(v)
   if r==targetrow:rr.append(tr);cc.append(j);vv.append(1.)
 A=coo_matrix((vv,(rr,cc)),shape=(tr+1,len(orb['columns']))).tocsc();A.sum_duplicates();A.eliminate_zeros()
 if args.start:
  data=pickle.load(args.start.open('rb'));selected=set(data.get('selected_columns',data.get('columns')))
 else:selected={j for j,c in enumerate(orb['columns']) if any(rowids[r]==args.target for r in c)}
 history=[];last={}
 while len(selected)<=args.max_cols and time.monotonic()-start<args.seconds:
  js=np.array(sorted(selected),dtype=int);m=A[:,js].tocsr();rows=np.flatnonzero(np.diff(m.indptr));m=m[rows,:];b=np.zeros(len(rows));b[np.where(rows==tr)[0]]=1.;nr=len(rows)
  mm=vstack([m,-m],format='csr');tcol=csr_matrix(-np.ones((2*nr,1)));mm=hstack([mm,tcol],format='csr');ub=np.r_[b,-b]
  lp=highspy.HighsLp();lp.num_col_=len(js)+1;lp.num_row_=2*nr;lp.col_cost_=np.r_[np.zeros(len(js)),1.];lp.col_lower_=np.zeros(len(js)+1);lp.col_upper_=np.full(len(js)+1,highspy.kHighsInf);lp.row_lower_=np.full(2*nr,-highspy.kHighsInf);lp.row_upper_=ub;lp.a_matrix_.format_=highspy.MatrixFormat.kRowwise;lp.a_matrix_.start_=mm.indptr;lp.a_matrix_.index_=mm.indices;lp.a_matrix_.value_=mm.data
  h=highspy.Highs();h.setOptionValue('solver','simplex');h.setOptionValue('presolve','on');h.setOptionValue('output_flag',False);h.setOptionValue('threads',1);h.setOptionValue('time_limit',min(50.,args.seconds-(time.monotonic()-start)));h.passModel(lp);h.run();st=h.getModelStatus();info=h.getInfo();sol=h.getSolution()
  rec={'iteration':len(history),'columns':len(js),'rows':nr,'status':str(st),'elapsed':time.monotonic()-start,'simplex_iterations':info.simplex_iteration_count,'objective':info.objective_function_value,'primal_infeasibility':info.max_primal_infeasibility,'dual_infeasibility':info.max_dual_infeasibility}
  last={'selected_columns':js.tolist(),'rows':rows.tolist(),'col_value':sol.col_value,'row_dual':sol.row_dual,'status':str(st),'target':args.target,'rowcoef_reference':'sorted halfrow index2','history':history}
  if st!=highspy.HighsModelStatus.kOptimal:
   history.append(rec);print(json.dumps(rec),flush=True);break
  vals=np.array(sol.col_value);du=np.array(sol.row_dual);y=du[:nr]-du[nr:];full_y=np.zeros(A.shape[0]);full_y[rows]=y;prices=A.T@full_y;prices[js]=-np.inf;neg=np.flatnonzero(prices>1e-9)
  rec.update({'target_dual':float(y[np.where(rows==tr)[0]][0]),'maximum_price':float(prices.max()),'improving_prices':len(neg),'support':int((vals[:-1]>1e-9).sum())});last['full_row_dual']=full_y.tolist();last['full_prices']=prices.tolist()
  history.append(rec);print(json.dumps(rec),flush=True)
  if vals[-1]<1e-8 or not len(neg):break
  chosen=neg[np.argsort(-prices[neg],kind='stable')[:args.batch]];selected.update(chosen.tolist())
  with (out/'checkpoint.pickle').open('wb') as f:pickle.dump(last,f)
 with (out/'result.pickle').open('wb') as f:pickle.dump(last,f)
 (out/'history.json').write_text(json.dumps({'arguments':{**vars(args),'start':str(args.start)},'history':history,'elapsed':time.monotonic()-start,'selected_columns':sorted(selected)},indent=2)+'\n')

if __name__=='__main__':main()
