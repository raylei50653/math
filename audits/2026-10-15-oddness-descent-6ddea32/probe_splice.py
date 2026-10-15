exec(open('audits/2026-10-15-oddness-descent-6ddea32/probe_named.py').read().split("for name in ('truncated_tetrahedron_graph'")[0])
def splice(g1,g2):
 # Remove endpoints of one edge, identify four dangling stubs in reverse cyclic hole order.
 out=[]
 for g in (g1,g2):
  ok,emb=nx.check_planarity(g);u,v=sorted(g.edges())[0];near=[x for x in emb.neighbors_cw_order(u) if x!=v]+[x for x in emb.neighbors_cw_order(v) if x!=u]
  # Evaluate finite four possible cyclic matchings below with explicit planarity acceptance.
  h=g.copy();h.remove_nodes_from([u,v]);out.append((h,near))
 h1,a=out[0];h2,b=out[1];mapping={v:i for i,v in enumerate(sorted(h1))};mapping2={v:i+len(h1) for i,v in enumerate(sorted(h2))};G=nx.relabel_nodes(h1,mapping);G.update(nx.relabel_nodes(h2,mapping2));a=[mapping[x] for x in a];b=[mapping2[x] for x in b]
 for perm in itertools.permutations(b):
  H=G.copy();H.add_edges_from(zip(a,perm));ok,emb=nx.check_planarity(H)
  if ok:return H
 raise ValueError
for name,gs in [('dodecahedron_4sum',(nx.dodecahedral_graph(),nx.dodecahedral_graph())),('dodecahedron_cube_4sum',(nx.dodecahedral_graph(),nx.cubical_graph()))]:
 g=splice(*gs);ed=sorted(tuple(sorted(x)) for x in g.edges());n=len(g);ms=list(map(frozenset,c.all_matchings(n,ed)));od=[sum(len(z)%2 for z in c.cycle_components(n,ed,M)) for M in ms];t=time.time();print(name,n,len(ms),flush=True)
 ok,emb=nx.check_planarity(g);used=set();faces=[]
 for u in sorted(g):
  for v in emb.neighbors_cw_order(u):
   if (u,v) not in used:faces.append(emb.traverse_face(u,v,used))
 print('faces',sorted(map(len,faces)),flush=True)
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
     data={'name':name,'n':n,'edges':ed,'faces':faces,'M':sorted(M),'matching_index':i,'e':e,'f':f,'good':sorted(ms[goods[0]])}
     Path('audits/2026-10-15-oddness-descent-6ddea32/probe-splice-trap.json').write_text(json.dumps(data,indent=2)+'\n');found=True;break
   if found:break
  if found:break
 print(name,'trap?',found,'sec',time.time()-t,flush=True)
 if found:break
