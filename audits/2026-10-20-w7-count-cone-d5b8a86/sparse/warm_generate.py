#!/usr/bin/env python3
"""Incremental bounded-dual discovery; output requires an exact checker."""
import argparse,gzip,json,pickle,time
from pathlib import Path
import numpy as np
import highspy
from scipy.sparse import coo_matrix,csr_matrix,vstack,hstack
P=Path(__file__).resolve().parent;S=P.parents[1]/'2026-10-20-r6-941-j1-five-edge-417732f/counting'

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--name',required=True);ap.add_argument('--target',type=int,default=44459);ap.add_argument('--seconds',type=float,default=200);ap.add_argument('--max-cols',type=int,default=19000);ap.add_argument('--batch',type=int,default=500);ap.add_argument('--start',type=Path,required=True);args=ap.parse_args();out=P/args.name;out.mkdir(exist_ok=False);start=time.monotonic()
 o=json.load(gzip.open(S/'orbits.json.gz','rt'));live=o['live'];li={s:i for i,s in enumerate(live)};sr={s:[] for s in live}
 for r,s in o['rowids']:
  if s in sr:sr[s].append(r)
 for rs in sr.values():rs.sort()
 rc={}
 for s,rs in sr.items():
  i=li[s];rc[rs[0]]=[(2*i,1.)];rc[rs[1]]=[(2*i+1,1.)];rc[rs[2]]=[(2*i,-1.),(2*i+1,-1.)]
 tr=2*len(live);rr=[];cc=[];vv=[]
 for j,col in enumerate(o['columns']):
  for r in col:
   for t,v in rc[r]:rr.append(t);cc.append(j);vv.append(v)
   if r==sr[args.target][2]:rr.append(tr);cc.append(j);vv.append(1.)
 A=coo_matrix((vv,(rr,cc)),shape=(tr+1,len(o['columns']))).tocsc();A.sum_duplicates();A.eliminate_zeros();nr=A.shape[0]
 d=pickle.load(args.start.open('rb'));js=list(d['selected_columns']);selected=set(js);b=np.zeros(nr);b[tr]=1.;ub=np.r_[b,-b]
 m=vstack([A[:,js],-A[:,js]],format='csc');m=hstack([m,csr_matrix(-np.ones((2*nr,1)))],format='csc')
 lp=highspy.HighsLp();lp.num_col_=len(js)+1;lp.num_row_=2*nr;lp.col_cost_=np.r_[np.zeros(len(js)),1.];lp.col_lower_=np.zeros(len(js)+1);lp.col_upper_=np.full(len(js)+1,highspy.kHighsInf);lp.row_lower_=np.full(2*nr,-highspy.kHighsInf);lp.row_upper_=ub;lp.a_matrix_.format_=highspy.MatrixFormat.kColwise;lp.a_matrix_.start_=m.indptr;lp.a_matrix_.index_=m.indices;lp.a_matrix_.value_=m.data
 # First column list includes a fixed t at index len(initial js), added X follow t.
 tcol=len(js);model_columns=list(js)+[-1]
 h=highspy.Highs();h.setOptionValue('solver','simplex');h.setOptionValue('presolve','on');h.setOptionValue('output_flag',False);h.setOptionValue('threads',1);h.passModel(lp)
 history=[];last={}
 while time.monotonic()-start<args.seconds and len(js)<=args.max_cols:
  h.setOptionValue('time_limit',args.seconds);h.run();st=h.getModelStatus();info=h.getInfo();sol=h.getSolution()
  rec={'iteration':len(history),'columns':len(js),'full_difference_rows':nr,'status':str(st),'elapsed':time.monotonic()-start,'simplex_iterations':info.simplex_iteration_count,'objective':info.objective_function_value,'primal_infeasibility':info.max_primal_infeasibility,'dual_infeasibility':info.max_dual_infeasibility}
  vals=np.array(sol.col_value);du=np.array(sol.row_dual);y=du[:nr]-du[nr:];prices=A.T@y;prices[np.array(js)]=-np.inf;improving=np.flatnonzero(prices>1e-9)
  rec.update({'target_dual':float(y[tr]),'maximum_price':float(prices.max()),'improving_prices':len(improving),'dual_support':int((abs(y)>1e-10).sum()),'support':int((vals>1e-9).sum())});history.append(rec);print(json.dumps(rec),flush=True)
  last={'selected_columns':list(js),'model_columns':list(model_columns),'t_column':tcol,'target':args.target,'full_row_dual':y.tolist(),'full_prices':prices.tolist(),'col_value':sol.col_value,'status':str(st),'history':history}
  with (out/'checkpoint.pickle').open('wb') as f:pickle.dump(last,f)
  if st==highspy.HighsModelStatus.kOptimal:
   with (out/'last-optimal.pickle').open('wb') as f:pickle.dump(last,f)
  if st!=highspy.HighsModelStatus.kOptimal or vals[tcol]<1e-8 or not len(improving):break
  new=improving[np.argsort(-prices[improving],kind='stable')[:min(args.batch,args.max_cols-len(js))]];nn=len(new)
  if not nn:break
  add=vstack([A[:,new],-A[:,new]],format='csc');assert h.addCols(nn,np.zeros(nn),np.zeros(nn),np.full(nn,highspy.kHighsInf),add.nnz,add.indptr,add.indices,add.data)==highspy.HighsStatus.kOk
  js.extend(new.tolist());model_columns.extend(new.tolist());selected.update(new.tolist())
 with (out/'result.pickle').open('wb') as f:pickle.dump(last,f)
 (out/'history.json').write_text(json.dumps({'arguments':{**vars(args),'start':str(args.start)},'history':history,'elapsed':time.monotonic()-start},indent=2)+'\n')
if __name__=='__main__':main()
