#!/usr/bin/env python3
"""Optional primal search among chord-only maximal outerplanar disks."""
import gzip,json,time
from pathlib import Path
from functools import lru_cache
P=Path(__file__).resolve().parent;S=P.parents[1]/'2026-10-20-r6-941-j1-five-edge-417732f/counting'
cap=json.load(gzip.open(S/'caps.json.gz','rt'));orb=json.load(gzip.open(S/'orbits.json.gz','rt'));states=cap['states'];live=set(orb['live']);bad=[states[i] for i in range(len(states)) if i not in live]
chords=[(i,j) for i in range(13) for j in range(i+2,13) if (i,j)!=(0,12)];masks={}
for e in chords:
 masks[e]=sum(1<<k for k,s in enumerate(bad) if s[e[0]]==s[e[1]])
full=(1<<len(bad))-1
@lru_cache(None)
def triangles(lo,hi):
 if hi-lo<=1:return [((),0)]
 out=[]
 for mid in range(lo+1,hi):
  additions=tuple(e for e in ((lo,mid),(mid,hi)) if e in masks)
  mask=0
  for e in additions:mask|=masks[e]
  for le,lm in triangles(lo,mid):
   for re,rm in triangles(mid,hi):out.append((le+re+additions,lm|rm|mask))
 return out
start=time.monotonic();alltri=triangles(0,12);res={}
for target in (44459,44466):
 t=states[target];valid=[(es,m) for es,m in alltri if all(t[i]!=t[j] for i,j in es)]
 best=min(valid,key=lambda x:(full^x[1]).bit_count());uncovered=(full^best[1]).bit_count();beststates=[i for i in range(len(states)) if i not in live and all(states[i][a]!=states[i][b] for a,b in best[0])]
 res[str(target)]={'target_compatible_triangulations':len(valid),'best_uncovered_zero_states':uncovered,'best_chords':best[0],'uncovered_state_ids':beststates}
print(json.dumps({'total_triangulations':len(alltri),'bad_states':len(bad),'targets':res,'seconds':time.monotonic()-start},indent=2))
(P/'triangulation-search.json').write_text(json.dumps({'total_triangulations':len(alltri),'bad_states':len(bad),'targets':res,'seconds':time.monotonic()-start},indent=2)+'\n')
