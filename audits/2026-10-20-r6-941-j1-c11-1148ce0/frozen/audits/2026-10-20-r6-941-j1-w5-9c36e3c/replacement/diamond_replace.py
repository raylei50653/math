#!/usr/bin/env python3
"""Exact six-rim diamond replacements with bounded new interiors; no realization."""
from pathlib import Path
from itertools import product,combinations
from collections import defaultdict,Counter
import json,gzip,argparse,hashlib,time
import combined as cm
D=Path(__file__).resolve().parent
RIM=('a','b','q','L','u1','u2');ROWS=('01021','01202','01212')
BOUND={tuple(sorted((i,(i+1)%6))) for i in range(6)}
ST=[t for t in cm.p.growth(6) if all(t[i]!=t[(i+1)%6] for i in range(6))];IX={t:i for i,t in enumerate(ST)}
ALPHA=IX[cm.p.canonical((0,1,2,1,0,2))]
OFACES=cm.p.OFACES+[('n','a','u2')];OE={tuple(sorted(e)) for f in OFACES for e in combinations(f,2)}
OL=[]
for t in ST:
 c=dict(zip(RIM,t));li=[]
 for ex in product(range(4),repeat=4):
  c.update(zip(('p','h','R','n'),ex))
  if all(c[u]!=c[v] for u,v in OE):li.append(ex)
 OL.append(li)
OS=sum(1<<i for i,li in enumerate(OL) if li)
def tris(k):
 fs=[(0,j,j+1) for j in range(1,5)]
 for v in range(6,6+k):
  f=fs.pop(0);fs.extend(tuple(sorted((v,*e))) for e in combinations(f,2))
 first=tuple(sorted(fs));seen={first};queue=[first]
 for fs in queue:
  yield fs
  ef=defaultdict(list)
  for f in fs:
   for e in combinations(f,2):ef[e].append(f)
  for e,fl in ef.items():
   if len(fl)!=2:continue
   a=next(v for v in fl[0] if v not in e);b=next(v for v in fl[1] if v not in e)
   if tuple(sorted((a,b))) in ef:continue
   new=tuple(sorted(set(fs)-set(fl)|{tuple(sorted((a,b,e[0]))),tuple(sorted((a,b,e[1])))}))
   if new not in seen:seen.add(new);queue.append(new)
def cls(k,es,sig):
 par=list(range(6+k))
 def find(x):
  while par[x]!=x:x=par[x]
  return x
 for j,(u,v) in enumerate(es):
  if sig&(1<<j):par[find(u)]=find(v)
 return tuple(tuple(i for i in range(6+k) if find(i)==r) for r in sorted({find(i) for i in range(6+k)}))
def compute(maxint,progress=False):
 path=D.parent/'review/diamond-certificate-v2.json.gz'
 with gzip.open(path,'rt') as f:inter=json.load(f)
 righttris=cm.triangulate(tuple(range(6)));Ts=[0]*15
 for i in inter['live']:
  cap=inter['caps'][i];a,u2,u1,L,q,c,s,v,w,t=cap['core']
  for b in range(4):
   if b in (a,c,q):continue
   ri=IX[cm.p.canonical((a,b,q,L,u1,u2))]
   if any(''.join(map(str,cm.p.canonical((x,y,a,b,c)))) in ROWS for x,y,r in cap['right_xyr']):Ts[0]|=1<<ri
   for x,y in product(range(4),repeat=2):
    if x in (c,s,y) or y in (a,t) or ''.join(map(str,cm.p.canonical((x,y,a,b,c)))) not in ROWS:continue
    rr=(s,x,y,t,w,v)
    for j,tri in enumerate(righttris,1):
     if all(rr[u]!=rr[vv] for u,vv in tri):Ts[j]|=1<<ri
 alpha_right=[True]
 for tri in righttris:
  alpha_right.append(any(all((1,x,y,1,w,v)[u]!=(1,x,y,1,w,v)[vv] for u,vv in tri) for x,y in ((2,3),(3,2)) for v,w in ((2,3),(3,2))))
 summary=[];relations={};hits=[]
 for k in range(maxint+1):
  stats=Counter();start=time.monotonic()
  for fs in tris(k):
   stats['triangulations']+=1
   if progress and stats['triangulations']%2000==0:print(json.dumps({'interior':k,'triangulations':stats['triangulations'],'elapsed':round(time.monotonic()-start,1)}),flush=True)
   es=sorted({e for f in fs for e in combinations(f,2)}-BOUND);sigs=defaultdict(int)
   for i,t in enumerate(ST):
    bit=1<<i
    for ex in product(range(4),repeat=k):
     c=t+ex;sig=sum(1<<j for j,(u,v) in enumerate(es) if c[u]==c[v]);sigs[sig]|=bit
   stats['nonempty_tagged_relations']+=len(sigs)
   for sig,sup in sigs.items():
    if not sup&(1<<ALPHA):continue
    stats['alpha_relations']+=1
    if not sup&~OS:stats['universal_sound_hits']+=1
    cl=cls(k,es,sig);delta=len(cl)-10
    # All nonconsecutive outer six-rim edges are nonedges by the exact source geometry;
    # contractions of each new arc are tested from the one actual face disk.
    ca={'interior':k,'faces':fs,'new_edges':es,'equal_signature':sig,'classes':cl,'completed_delta':delta,'support_ids':[i for i in range(len(ST)) if sup&(1<<i)]}
    if sup not in relations or delta<relations[sup]['completed_delta']:relations[sup]=ca
    for j,T in enumerate(Ts):
     if alpha_right[j] and not sup&T:hits.append(ca|{'right_kind':'original' if j==0 else righttris[j-1],'completed_delta':delta-(j>0)})
  summary.append({'interior':k,'stats':dict(stats),'seconds':round(time.monotonic()-start,3)})
  if progress:print(json.dumps(summary[-1]),flush=True)
 return {'status':'bounded marked triangulation comparison; no actual source constructed','interface_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'ordered_rim':RIM,'states':ST,'original_full_lifts_phRn':OL,'alpha_id':ALPHA,'live_source_states':len(inter['live']),'source_forbidden_rim_ids':[[i for i in range(len(ST)) if T&(1<<i)] for T in Ts],'right_order':['original']+righttris,'right_d_a_accepts':alpha_right,'summary':summary,'distinct_alpha_relations':len(relations),'hits':hits,'relations':list(relations.values()),'source_excluded':False,'smaller_bad_constructed':False}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--max-interior',type=int,default=2);ap.add_argument('--build',action='store_true');ap.add_argument('--certificate',type=Path);a=ap.parse_args();out=compute(a.max_interior,True);path=a.certificate or D/f'diamond-search-{a.max_interior}.json.gz'
 if a.build:
  with path.open('xb') as raw:
   with gzip.GzipFile(fileobj=raw,mode='wb',mtime=0) as f:f.write(json.dumps(out,sort_keys=True,separators=(',',':')).encode()+b'\n')
 else:
  with gzip.open(path,'rt') as f:old=json.load(f)
  for r in out['summary']:r.pop('seconds',None)
  for r in old['summary']:r.pop('seconds',None)
  assert json.loads(json.dumps(out))==old
 print(json.dumps({k:v for k,v in out.items() if k not in ('original_full_lifts_phRn','states','relations','source_forbidden_rim_ids','right_order','hits')}|{'hit_count':len(out['hits'])}))
if __name__=='__main__':main()
