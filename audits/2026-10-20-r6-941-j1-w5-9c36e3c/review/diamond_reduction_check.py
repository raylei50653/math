#!/usr/bin/env python3
"""Independent exact C10 full-cap certificate for n=5 C=(G-phRn)/(a=u1,b=L)."""
from pathlib import Path
from itertools import product
import argparse,gzip,hashlib,json
D=Path(__file__).resolve().parent
RIM=('a','u2','u1','L','q','c','s','v','w','t')
ROWS=('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
RIGHT=(('x','y'),('x','c'),('x','r'),('x','s'),('y','a'),('y','r'),('y','t'),('r','t'),('r','w'),('r','v'),('r','s'))
def canon(t):
 d={};return tuple(d.setdefault(c,len(d)) for c in t)
def states():
 def grow(t):
  if len(t)==10:
   if t[-1]!=t[0]:yield t
   return
  for c in range(min(3,max(t)+1)+1):
   if c!=t[-1]:yield from grow(t+(c,))
 return list(grow((0,)))
def packed(t):return json.dumps(t,sort_keys=True,separators=(',',':')).encode()
def compute():
 sourcepath=D/'diamond-certificate-v2.json.gz';source=json.load(gzip.open(sourcepath,'rt'));live=set(source['live']);sr=states();assert len(sr)==2461 and len(live)==1889
 assert [tuple(r['core']) for r in source['caps']]==sr
 mats=[[0]*2461 for _ in ROWS];records=[]
 for i,t in enumerate(sr):
  base=dict(zip(RIM,t));bs=[]
  for b in range(4):
   c=base|{'b':b}
   if all(c[u]!=c[v] for u,v in (('b','a'),('b','c'),('b','q'))) and c['a']==c['u1'] and c['b']==c['L']:bs.append(b)
  right=[]
  for x,y,r in product(range(4),repeat=3):
   c=base|{'x':x,'y':y,'r':r}
   if all(c[u]!=c[v] for u,v in RIGHT):right.append((x,y,r))
  for b in bs:
   for x,y,r in right:
    j=ROWS.index(''.join(map(str,canon((x,y,base['a'],b,base['c'])))));mats[j][i]+=1
  records.append({'core':t,'candidate_b_lifts':bs,'right_xyr':right,'ten_coefficients':[m[i] for m in mats]})
 excluded=[ROWS[j] for j in (1,4,6)]
 assert all(mats[j][i]==0 for j in (1,4,6) for i in live)
 # The two Kempe-residual witness cores have no candidate left lift.
 assert all(not records[w['canonical_id']]['candidate_b_lifts'] for w in source['witnesses'])
 # Literal original d_a restrictions: x,y and v,w independently permute 2,3.
 positive=[]
 for x,y in ((2,3),(3,2)):
  for v,w in ((2,3),(3,2)):
   literal=(0,2,0,1,2,0,1,v,w,1);i=sr.index(canon(literal))
   assert i in live
   assert literal[0]==literal[2] and literal[3]==1
   c=dict(zip(RIM,literal))|{'b':1,'x':x,'y':y,'r':0}
   assert all(c[u]!=c[z] for u,z in RIGHT+(('b','a'),('b','c'),('b','q')))
   assert ''.join(map(str,canon((x,y,0,1,0))))=='01232'
   assert mats[9][i]>0
   positive.append({'literal_core':literal,'literal_xyr':[x,y,0],'canonical_core_id':i})
 return {'status':'PASS; exact same-candidate four-row certificate in n=5 subcase','candidate':'C=(G-{p,h,R,n})/(a=u1,b=L)','ordered_original_frame':['x','y','a','b','c'],'completed_inner_vertices':'k-6','diamond_source_sha256':hashlib.sha256(sourcepath.read_bytes()).hexdigest(),'ordered_core_rim':RIM,'core_states':2461,'source_live_states':1889,'records':records,'matrices_sha256':hashlib.sha256(packed(mats)).hexdigest(),'complete_zero_rows':excluded,'every_zero_row_checked_over_all_live_core_states':True,'literal_d_a_positive_lifts':positive,'source_excluded_by_global_minimality':True,'full_W5_branch_excluded':False,'all_J1_J2_closed':False,'new_Lean':False}
def main():
 p=argparse.ArgumentParser();p.add_argument('--build',action='store_true');p.add_argument('--certificate',type=Path,default=D/'diamond-reduction-certificate.json.gz');a=p.parse_args();out=json.loads(packed(compute()))
 if a.build:
  with a.certificate.open('xb') as raw:
   with gzip.GzipFile(fileobj=raw,mode='wb',mtime=0) as f:f.write(packed(out)+b'\n')
 else:assert json.load(gzip.open(a.certificate,'rt'))==out
 print(json.dumps({k:out[k] for k in ('status','candidate','completed_inner_vertices','core_states','source_live_states','complete_zero_rows','source_excluded_by_global_minimality','full_W5_branch_excluded','all_J1_J2_closed')},sort_keys=True))
if __name__=='__main__':main()
