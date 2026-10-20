#!/usr/bin/env python3
"""Seven-rim <=2 replacement with fourteen fixed original right-hole fillings."""
import probe as p
from itertools import product,combinations
from collections import defaultdict,Counter
from pathlib import Path
import gzip,json,time,hashlib,argparse
D=p.ROOT
ROWS=('01021','01202','01212')
def triangulate(poly):
 if len(poly)==3:return [()]
 ans=[]
 for j in range(1,len(poly)-1):
  left=poly[:j+1];right=poly[j:]
  ls=[()] if len(left)<3 else triangulate(left)
  rs=[()] if len(right)<3 else triangulate(right)
  extras=[]
  if j>1:extras.append(tuple(sorted((poly[0],poly[j]))))
  if j<len(poly)-2:extras.append(tuple(sorted((poly[j],poly[-1]))))
  for l in ls:
   for r in rs:ans.append(tuple(sorted(set(l+r+tuple(extras)))))
 return sorted(set(ans))
def classes(k,es,sig):
 par=list(range(7+k))
 def find(x):
  while par[x]!=x:x=par[x]
  return x
 for j,(u,v) in enumerate(es):
  if sig&(1<<j):par[find(u)]=find(v)
 return tuple(tuple(i for i in range(7+k) if find(i)==r) for r in sorted({find(i) for i in range(7+k)}))
def relations():
 ans={}
 for k in range(3):
  for fs in p.all_triangulations(k):
   es=sorted({e for f in fs for e in combinations(f,2)}-p.BOUND);sigs=defaultdict(int)
   for i,t in enumerate(p.STATES):
    for ex in product(range(4),repeat=k):
     c=t+ex;sig=sum(1<<j for j,(u,v) in enumerate(es) if c[u]==c[v]);sigs[sig]|=1<<i
   for sig,sup in sigs.items():
    al=[a for a in p.ALPHA_IDS if sup&(1<<a)]
    if not al:continue
    cl=classes(k,es,sig)
    if any(0 in g and 5 in g for g in cl):continue
    delta=len(cl)-11 # -3 original left + k new - contractions - original r
    if sup in ans and ans[sup]['completed_delta']<=delta:continue
    ans[sup]={'interior':k,'faces':fs,'new_edges':es,'equal_signature':sig,'classes':cl,'completed_delta':delta,'alpha_ids':al,'support_ids':[i for i in range(91) if sup&(1<<i)]}
 return ans

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--interface',type=Path,default=D.parent/'interface/certificate.json.gz');ap.add_argument('--output',type=Path,default=D/'combined.json');ap.add_argument('--n5',action='store_true');args=ap.parse_args();start=time.monotonic()
 with gzip.open(args.interface,'rt') as f:inter=json.load(f)
 if args.n5:
  profile=next(d for d in inter['conditional_chord_profiles'] if d['present_chords']==[['a','u2']])
  inter['live']=profile['live_ids']
 tris=triangulate(tuple(range(6)));assert len(tris)==14
 forbidden=[0]*14;inc=[[defaultdict(set) for row in ROWS] for tri in tris]
 for i in inter['live']:
  a,n,u2,u1,L,q,c,s,v,w,t=inter['caps'][i]['core']
  for x,y in product(range(4),repeat=2):
   if x in (c,s,y) or y in (a,t):continue
   rr=(s,x,y,t,w,v)
   which=[j for j,tri in enumerate(tris) if all(rr[u]!=rr[vv] for u,vv in tri)]
   if not which:continue
   for b in range(4):
    if b in (a,c,q):continue
    row=''.join(map(str,p.canonical((x,y,a,b,c))))
    if row not in ROWS:continue
    rid=ROWS.index(row);rimid=p.INDEX[p.canonical((a,b,q,L,u1,u2,n))]
    frame=(x,y,a,b,c);perm=dict(zip(frame,map(int,row)))
    for z,znew in zip(set(range(4))-set(perm),set(range(4))-set(perm.values())):perm[z]=znew
    lit=tuple(perm[z] for z in inter['caps'][i]['core'])
    for j in which:forbidden[j]|=1<<rimid;inc[j][rid][rimid].add(lit)
 rel=relations();hits=[];near=[];coverage=set();records=[]
 for j,tri in enumerate(tris):
  vw=[]
  for v,w in ((2,3),(3,2)):
   lifts=[(x,y) for x,y in ((2,3),(3,2)) if all((1,x,y,1,w,v)[u]!=(1,x,y,1,w,v)[vv] for u,vv in tri)]
   if lifts:vw.append({'v_w':[v,w],'x_y_lifts':lifts})
  records.append({'triangles_index':j,'diagonals':tri,'d_a_vw_lifts':vw,'forbidden_rim_ids':[i for i in range(91) if forbidden[j]&(1<<i)]})
  for sup,ca in rel.items():
   if not vw:continue
   if args.n5 and p.ALPHA_IDS[0] not in ca['alpha_ids']:continue
   bad=sup&forbidden[j]
   c=dict(ca)|{'right_tri_index':j,'right_diagonals':tri,'right_d_a_vw_lifts':vw,'remaining_forbidden_rim_ids':[i for i in range(91) if bad&(1<<i)]}
   rs=[set().union(*(d.get(i,set()) for i in ca['support_ids'])) for d in inc[j]]
   sizes=tuple(len(x) for x in rs);c['negative_fibre_counts']=dict(zip(ROWS,sizes))
   if not bad:
    hits.append(c)
    for al in ca['alpha_ids']:
     for rec in vw:coverage.add((al,*rec['v_w']))
   score=(sum(x>0 for x in sizes),sum(sizes),len(c['remaining_forbidden_rim_ids']),ca['completed_delta'])
   if len(near)<30 or score<near[-1][0]:
    c['complete_negative_literal_fibres']=dict(zip(ROWS,[sorted(s) for s in rs]));near.append((score,len(near),c));near.sort(key=lambda z:z[:2]);near=near[:30]
 data={'status':'bounded expanded interface control, not source realization','interface_sha256':hashlib.sha256(args.interface.read_bytes()).hexdigest(),'n5_profile':args.n5,'source_live_states':len(inter['live']),'left_distinct_relations':len(rel),'right_triangulations':records,'hits':hits,'d_a_joint_coverage':sorted(coverage),'near':[c for score,n,c in near],'seconds':time.monotonic()-start}
 with args.output.open('x') as f:json.dump(data,f,sort_keys=True,indent=2);f.write('\n')
 print(json.dumps({k:v for k,v in data.items() if k not in ('right_triangulations','hits','near')}))
 for c in (hits[:4] if hits else [c for score,n,c in near[:5]]):print(json.dumps({k:v for k,v in c.items() if k!='complete_negative_literal_fibres'}))
if __name__=='__main__':main()
