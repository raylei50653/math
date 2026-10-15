exec(open('audits/2026-10-15-oddness-descent-6ddea32/probe_named.py').read().split("for name in ('truncated_tetrahedron_graph'")[0])
for file in ['probe-splice-trap.json','probe-trap.json']:
 d=json.loads(Path('audits/2026-10-15-oddness-descent-6ddea32/'+file).read_text());ed=d['edges'];n=d['n'];ms=list(map(frozenset,c.all_matchings(n,ed)));od=[sum(len(z)%2 for z in c.cycle_components(n,ed,N)) for N in ms]
 for i,M in enumerate(ms):
  if not od[i]:continue
  below=[j for j in range(len(ms)) if od[j]<od[i] and onecycle(n,ed,M^ms[j])]
  for e in sorted(M):
   candidates=set(range(len(ed)))-M
   for j in below:
    candidates=candidates&ms[j] if e in ms[j] else candidates-ms[j]
   for f in sorted(candidates):
    goods=[j for j,N in enumerate(ms) if not od[j] and (e in N)!=(f in N)]
    if goods:
     print('XOR TRAP',d['name'],i,e,f,od[i],goods[:5],flush=True)
     d.update(M=sorted(M),matching_index=i,e=e,f=f,good=sorted(ms[goods[0]]));Path('audits/2026-10-15-oddness-descent-6ddea32/probe-xor-trap.json').write_text(json.dumps(d,indent=2)+'\n');raise SystemExit
 print(d['name'],'no xor trap',flush=True)
