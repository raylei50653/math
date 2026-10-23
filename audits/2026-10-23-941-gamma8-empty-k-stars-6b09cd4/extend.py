#!/usr/bin/env python3
import importlib.util,itertools,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('explore',HERE/'explore.py')
q=importlib.util.module_from_spec(spec);spec.loader.exec_module(q)
m=q.m;c=q.c
def arcs(pool,anchor):
 for n in range(len(pool)+1):
  for chosen in itertools.combinations(pool,n):
   for tail in itertools.permutations(chosen):yield anchor+list(tail)
def extend(row):
 core,color,alias=row['core'],row['color'],row['alias']
 cell=next(x for x in c['candidates'] if x['classification']=='local_necessary_type' and x['core']==core)
 image,co,lab,old,es,full=m.setup(c,cell,alias)
 co['omega']=color;lab['omega']='K';out=[]
 for p in row['partial']:
  ex=set(es);fx=dict(full,**p)
  for v,lk in p.items():ex|=m.cycle_edges(v,lk)
  single={}
  for v,anchor in [('r',['a','T','tau']+(['zeta'] if core=='L' else [])+['d']),('s',['b','T','tau']+(['zeta'] if core=='R' else [])+['x'])]:
   pool=sorted({image(x) for x in ['U','p_d','p_x','omega']}-set(anchor));single[v]=[]
   for lk in arcs(pool,anchor):
    if m.valid(ex|m.cycle_edges(v,lk),co,lab,old,dict(fx,**{v:lk}),core):single[v].append(lk)
  for rl,sl in itertools.product(single['r'],single['s']):
   ey=ex|m.cycle_edges('r',rl)|m.cycle_edges('s',sl);fy=dict(fx,r=rl,s=sl)
   if m.valid(ey,co,lab,old,fy,core):out.append(dict(p,r=rl,s=sl))
 return dict(core=core,color=color,alias=alias,stars=out)
if __name__=='__main__':
 for core,color,alias in itertools.product(['L','R','O'],[0,2],[False,True]):
  r=extend(m.load(HERE/f'explore-{core}-{color}-{alias}.json'))
  print(core,color,alias,len(r['stars']),flush=True)
  with (HERE/f'full-N-{core}-{color}-{alias}.json').open('x') as f:json.dump(r,f,indent=2);f.write('\n')
