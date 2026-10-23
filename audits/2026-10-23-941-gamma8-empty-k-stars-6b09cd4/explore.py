#!/usr/bin/env python3
import importlib.util,itertools,json,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
spec=importlib.util.spec_from_file_location('old',ROOT/'audits/2026-10-23-941-gamma8-empty-resource-stars-6b09cd4/check.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
c=m.load(ROOT/m.CELLS)
def candidates(core,color,alias):
 cell=next(x for x in c['candidates'] if x['classification']=='local_necessary_type' and x['core']==core)
 image,co,lab,old,es,full=m.setup(c,cell,alias)
 co['omega']=color;lab['omega']='K'
 pool=sorted({image(x) for x in ['d','x','U','p_d','p_x','omega']})
 out=[];ny=0
 for yl in m.anchored(pool,['a','T','b']):
  ey=es|m.cycle_edges('y',yl);fy=dict(full,y=yl)
  if not m.valid(ey,co,lab,old,fy,core):continue
  ny+=1;single={}
  for v,anchor in [('a','r'),('b','s')]:
   single[v]=[]
   for lk in m.anchored(pool,[anchor,'T','y']):
    if m.valid(ey|m.cycle_edges(v,lk),co,lab,old,dict(fy,**{v:lk}),core):single[v].append(lk)
  for al,bl in itertools.product(single['a'],single['b']):
   ex=ey|m.cycle_edges('a',al)|m.cycle_edges('b',bl);fx=dict(fy,a=al,b=bl)
   if m.valid(ex,co,lab,old,fx,core):out.append(dict(y=yl,a=al,b=bl))
 return dict(core=core,color=color,alias=alias,y_count=ny,partial=out)
if __name__=='__main__':
 for core,color,alias in itertools.product(['L','R','O'],[0,2],[False,True]):
  t=time.time();row=candidates(core,color,alias)
  print(core,color,alias,row['y_count'],len(row['partial']),time.time()-t,flush=True)
  with (HERE/f'explore-{core}-{color}-{alias}.json').open('x') as f:json.dump(row,f,indent=2);f.write('\n')
