import networkx as nx,importlib.util,itertools,json,time
from pathlib import Path
p=Path('audits/2026-10-15-tait-separation-6ddea32/check_controls.py');s=importlib.util.spec_from_file_location('c',p);c=importlib.util.module_from_spec(s);s.loader.exec_module(c)
def onecycle(n,ed,d):
 adj={}
 for k in d:
  u,v=ed[k];adj.setdefault(u,[]).append(v);adj.setdefault(v,[]).append(u)
 if not adj:return False
 todo=[next(iter(adj))];seen=set(todo)
 while todo:
  for v in adj[todo.pop()]:
   if v not in seen:seen.add(v);todo.append(v)
 return len(seen)==len(adj)
for name in ('truncated_tetrahedron_graph','truncated_cube_graph','tutte_graph'):
 g=getattr(nx,name)();ed=sorted(tuple(sorted(x)) for x in g.edges());n=len(g);ms=list(map(frozenset,c.all_matchings(n,ed)));od=[sum(len(z)%2 for z in c.cycle_components(n,ed,M)) for M in ms];t=time.time()
 found=False
 for i,M in enumerate(ms):
  if not od[i]:continue
  below=[j for j in range(len(ms)) if od[j]<od[i] and onecycle(n,ed,M^ms[j])]
  for e in sorted(M):
   candidates=set(range(len(ed)))-M
   for j in below:
    if e in ms[j]:candidates &= ms[j]
   for f in sorted(candidates):
    goods=[j for j,N in enumerate(ms) if not od[j] and e in N and f not in N]
    if goods:
     print('TRAP',name,'M',i,'odd',od[i],'e,f',e,f,'goods',goods[:10],'lowerneighbors',len(below),flush=True)
     data={'name':name,'n':n,'edges':ed,'M':sorted(M),'matching_index':i,'e':e,'f':f,'good':sorted(ms[goods[0]])}
     Path('audits/2026-10-15-oddness-descent-6ddea32/probe-trap.json').write_text(json.dumps(data,indent=2)+'\n');found=True;break
   if found:break
  if found:break
 print(name,'trap?',found,'sec',time.time()-t,flush=True)
 if found:break
