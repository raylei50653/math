import importlib.util,json,itertools
from pathlib import Path
R=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('old',R/'audits/2026-10-23-941-gamma8-chi-six-6b09cd4/check.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
c=json.loads((R/m.CELLS).read_text())
for core in ['L','R','O']:
 cell=next(x for x in c['candidates'] if x['classification']=='local_necessary_type' and x['core']==core)
 for alias in [False,True]:
  image,co,la,es,old,fu=m.setup(cell,c,2,alias)
  co['omega']=3;la['omega']='N'
  pool=sorted({image(x) for x in ['d','x','U','p_d','p_x','omega']})
  ys=[];j=[]
  for yl in m.link_options(['a','T','b'],pool):
   ey=m.with_star(es,'y',yl);fy=dict(fu,y=yl)
   if not m.valid(ey,co,la,cell,old,fy):continue
   ys.append(yl);alinks=[];blinks=[]
   for ce,anchor,links in [('a','r',alinks),('b','s',blinks)]:
    for lk in m.link_options([anchor,'T','y'],pool):
     ex=m.with_star(ey,ce,lk);fx=dict(fy,**{ce:lk})
     if m.valid(ex,co,la,cell,old,fx):links.append(lk)
   for al,bl in itertools.product(alinks,blinks):
    ex=m.with_star(m.with_star(ey,'a',al),'b',bl);fx=dict(fy,a=al,b=bl)
    if not m.valid(ex,co,la,cell,old,fx):continue
    j.append(dict(y=yl,a=al,b=bl));continue
    # complete omega cycle, canonical at min neighbor; no forced anchor
    opool=sorted({image(x) for x in ['r','s','y','d','x','U','p_d','p_x']})
    for n in range(5,len(opool)+1):
     for cho in itertools.combinations(opool,n):
      for perm in itertools.permutations(cho[1:]):
       ol=[cho[0],*perm]
       if ol[1]>ol[-1]:continue
       eo=m.with_star(ex,'omega',ol);fo=dict(fx,omega=ol)
       if m.valid(eo,co,la,cell,old,fo):j.append(dict(y=yl,a=al,b=bl,omega=ol))
  print(core,alias,'ylinks',len(ys),'joins',len(j),flush=True)
  (Path(__file__).resolve().parent/f'partial-{core}-{alias}.json').write_text(json.dumps(j,indent=2)+'\n')
