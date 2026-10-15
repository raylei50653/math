from pathlib import Path
import json,time
H=Path(__file__).resolve().parent
exec((H/'probe_covers.py').read_text().split('for v in [0,Q[0],Q[1]]:')[0])
previous=json.load(open(H/'probe-all-covers.json'));out=[];start=time.time()
for old in previous:
 if not old['q_reached']:continue
 voltage=old['voltage'];run(voltage);sols,F,E,pins=LAST
 cubes={}
 for s in S:
  for j,p in enumerate(s['pairings']):
   arr=[]
   for mask in range(len(p['cube_targets_by_bitmask'])):
    cur=s['id'];e=0
    for bit in range(sum(map(len,p['terminal_parts']))):
     if mask>>bit&1:
      e^=(voltage>>index[edges[cur,j,bit]])&1;cur=byid[cur]['pairings'][j]['cube_targets_by_bitmask'][1<<bit]
    arr.append((cur,e))
   cubes[s['id'],j]=arr
 strict=[]
 for i,f in enumerate(F):
  okay=True
  for s in S:
   for e in range(2):
    for j,p in enumerate(s['pairings']):
     targets=cubes[s['id'],j];c=f[s['id'],e];bits=[pair for pair,blocks in zip(p['pairing'],p['terminal_parts']) for _ in blocks]
     changed=[bit for bit in range(len(bits)) if f[targets[1<<bit][0],e^targets[1<<bit][1]]!=c]
     if len(changed)!=1:okay=False;break
     bit=changed[0];pair=bits[bit]
     if any(f[t,e^d]!=(sum(pair)-c if mask>>bit&1 else c) for mask,(t,d) in enumerate(targets)):okay=False;break
    if not okay:break
   if not okay:break
  if okay:strict.append(i)
 alive=set(strict);EE=[(a,b) for a,b in E if a in alive and b in alive];adj={v:set() for v in alive}
 for a,b in EE:adj[a].add(b);adj[b].add(a)
 bad=None
 for s in S:
  for e in range(2):
   for j,p in enumerate(s['pairings']):
    for pair,blocks in zip(p['pairing'],p['terminal_parts']):
     for block in blocks:
      reach={pins[block[0]]};todo=list(reach)
      while todo:
       a=todo.pop()
       for b in adj[a]-reach:
        if F[b][s['id'],e] in pair:reach.add(b);todo.append(b)
      if any(pins[v] not in reach for v in block):bad={'state':s['id'],'sheet':e,'pair':pair,'block':block,'reached':sorted(reach)};break
     if bad:break
    if bad:break
   if bad:break
  if bad:break
 rec={'class':old['class'],'weak':len(F),'strict':len(strict),'edges':len(EE),'bad':bad};out.append(rec);print('class',old['class'],'strict',len(strict),'edges',len(EE),'bad',None if not bad else(bad['state'],bad['sheet'],bad['block']),flush=True)
(H/'probe-strict.json').write_text(json.dumps(out,indent=2)+'\n');print('DONE secs',time.time()-start,'survivors',sum(not r['bad'] for r in out),flush=True)
