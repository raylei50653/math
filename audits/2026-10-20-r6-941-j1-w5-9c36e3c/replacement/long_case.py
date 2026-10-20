#!/usr/bin/env python3
"""Two actual n>=6 same-source candidates, complete residual fibres and cost."""
from pathlib import Path
from itertools import product
from collections import Counter
import gzip,json,hashlib,argparse
D=Path(__file__).resolve().parent;ROWS=('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
def canonical(t):
 d={};return tuple(d.setdefault(x,len(d)) for x in t)
def packed(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def compute():
 path=D.parent/'interface/certificate-v4.json.gz';inter=json.load(gzip.open(path,'rt'));ans=[]
 for chosen,slot in (('u1',3),('u2',2)):
  mats=[[0]*7381 for _ in ROWS];res={row:Counter() for row in ('01021','01202','01212')}
  for i,cap in enumerate(inter['caps']):
   t=cap['core'];a,n,u2,u1,L,q,c,s,v,w,tt=t
   if a!=t[slot] or L in (a,c,q):continue
   for x,y,r in cap['right_xyr']:
    frame=(x,y,a,L,c);z=''.join(map(str,canonical(frame)));j=ROWS.index(z);mats[j][i]+=1
    if z not in res or i not in inter['live']:continue
    perm=dict(zip(frame,map(int,z)))
    for cc,nn in zip(set(range(4))-set(perm),set(range(4))-set(perm.values())):perm[cc]=nn
    literal=tuple(perm[cc] for cc in t);res[z][literal]+=1
  rows={z:[{'literal_core':t,'coefficient':n} for t,n in sorted(cs.items())] for z,cs in res.items()}
  # A literal proper C5 fixes all four colour names. No orbit-size factor
  # remains in these full-fibre formulas, and every cap r is counted.
  ans.append({'candidate':f'C{0 if chosen=="u1" else 1}', 'definition':f'(G-{{p,h,R}})/(a={chosen},b=L)','completed_k_delta':-5,'ordered_C5_frame':['x','y','a','b','c'],'ordered_core_rim':inter['ordered_rim'],'negative_complete_fibres':rows,'negative_fibre_counts':{z:len(v) for z,v in rows.items()},'matrix_sha256':hashlib.sha256(packed(mats)).hexdigest(),'alpha_d_a_u1_u2':([0,2] if chosen=='u1' else [2,0]),'three_negative_zero_proved':False})
 return {'status':'exact residual full-fibre formulas; n>=6 source branch remains OPEN','interface_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'source_live':len(inter['live']),'candidates':ans,'source_excluded':False,'smaller_bad_constructed':False}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--build',action='store_true');a=ap.parse_args();out=json.loads(packed(compute()));path=D/'long-case-certificate.json.gz'
 if a.build:
  with path.open('xb') as raw:
   with gzip.GzipFile(fileobj=raw,mode='wb',mtime=0) as f:f.write(packed(out)+b'\n')
 else:assert json.load(gzip.open(path,'rt'))==out
 print(json.dumps({k:v for k,v in out.items() if k!='candidates'}|{'candidates':[{k:v for k,v in c.items() if k!='negative_complete_fibres'} for c in out['candidates']]}))
if __name__=='__main__':main()
