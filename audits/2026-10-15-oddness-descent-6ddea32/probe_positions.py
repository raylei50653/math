exec(open('audits/2026-10-15-oddness-descent-6ddea32/probe_named.py').read().split("for name in ('truncated_tetrahedron_graph'")[0])
d=json.loads(Path('audits/2026-10-15-oddness-descent-6ddea32/probe-splice-trap.json').read_text());ed=d['edges'];n=d['n'];faces=d['faces'];pe=[]
for u,v in ed:pe.append([i for i,f in enumerate(faces) if any({f[j],f[(j+1)%len(f)]}=={u,v} for j in range(len(f)))])
pes={tuple(sorted(x)) for x in pe};triangles=[[i for i,f in enumerate(faces) if v in f] for v in range(n)];poses={}
for e,f in itertools.permutations(range(len(ed)),2):
 if set(pe[e])&set(pe[f]):continue
 x,y=pe[e]
 for z,b in (pe[f],pe[f][::-1]):
  if len(faces[z])<7:continue
  if sorted([z,x,y]) not in sorted(sorted(t) for t in triangles):continue
  if tuple(sorted([b,x])) in pes or tuple(sorted([b,y])) in pes:continue
  poses[e,f]=(z,x,y,b)
print('valid T positions',len(poses),flush=True)
ms=list(map(frozenset,c.all_matchings(n,ed)));od=[sum(len(z)%2 for z in c.cycle_components(n,ed,M)) for M in ms]
for i,M in enumerate(ms):
 if not od[i]:continue
 below=[j for j in range(len(ms)) if od[j]<od[i] and onecycle(n,ed,M^ms[j])]
 for (e,f),roles in sorted(poses.items()):
  if (e in M)==(f in M):continue
  if any((e in ms[j])==(e in M) and (f in ms[j])==(f in M) for j in below):continue
  goods=[j for j,N in enumerate(ms) if not od[j] and (e in N)==(e in M) and (f in N)==(f in M)]
  if goods:
   print('POSITION TRAP',i,e,f,roles,od[i],goods[:5],flush=True)
   d.update(M=sorted(M),matching_index=i,e=e,f=f,roles_z_x_y_b=list(roles),good=sorted(ms[goods[0]]));Path('audits/2026-10-15-oddness-descent-6ddea32/probe-position-trap.json').write_text(json.dumps(d,indent=2)+'\n');raise SystemExit
print('no sourceposition trap')
