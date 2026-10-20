#!/usr/bin/env python3
"""Independent C13 cap reconstruction from original graph edges; stdlib."""
from pathlib import Path
from itertools import product
from functools import lru_cache
import argparse, hashlib, json
D=Path(__file__).resolve().parent
NAMES=('a','n','u4','u3','u2','u1','L','q','c','s','v','w','t')
ROWS=('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
LEFT=(('b','a'),('b','c'),('b','q'),('b','p'),('p','a'),('p','q'),('p','n'),('p','h'),('h','q'),('h','L'),('h','R'),('h','n'),('R','n'),('R','L'),('R','u1'),('R','u2'),('R','u3'),('R','u4'))
RIGHT=(('x','c'),('x','s'),('x','y'),('x','r'),('y','a'),('y','t'),('y','r'),('r','s'),('r','v'),('r','w'),('r','t'))

def canonical(t):
 d={};return tuple(d.setdefault(x,len(d)) for x in t)

def rim_states(t=(0,)):
 if len(t)==13:
  if t[-1]!=t[0]:yield t
  return
 for x in range(min(3,max(t)+1)+1):
  if x!=t[-1]:yield from rim_states(t+(x,))

def packed(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()

def lifts(boundary, variables, edges):
 # Derive each list from ORIGINAL boundary edges, then test remaining edges.
 bs=set(boundary); allowed=[]
 for v in variables:
  neighbours={w if u==v else u for u,w in edges if u==v or w==v}
  forbidden={boundary[w] for w in neighbours & bs}
  allowed.append(tuple(c for c in range(4) if c not in forbidden))
 inner=[(variables.index(u),variables.index(v)) for u,v in edges if u not in bs and v not in bs]
 for colours in product(*allowed):
  if all(colours[i]!=colours[j] for i,j in inner):yield colours

@lru_cache(None)
def right_caps(a,c,s,v,w,t):
 b=dict(zip(('a','c','s','v','w','t'),(a,c,s,v,w,t)))
 return tuple(lifts(b,('x','y','r'),RIGHT))

def compute():
 states=list(rim_states());assert len(states)==66430
 matrices={g:[[0]*len(states) for _ in ROWS] for g in ('G','Q1','J1')}
 left_counts={g:[] for g in matrices}; right_counts=[]
 for i,tup in enumerate(states):
  bdy=dict(zip(NAMES,tup)); a,n,u4,u3,u2,u1,L,q,c,s,v,w,t=tup
  ls=tuple(lifts(bdy,('b','p','h','R'),LEFT))
  # Q1 and J1 are complete pullbacks of the actual quotient; deleted p,h
  # remove all their incident edges, while new aR belongs only to J1.
  retained=tuple((u,v) for u,v in LEFT if u not in ('p','h') and v not in ('p','h'))
  pairs=tuple(lifts(bdy,('b','R'),retained))
  qs=tuple((b,R) for b,R in pairs if b==n and R==q)
  js=tuple((b,R) for b,R in pairs if b==L and a!=R)
  rs=right_caps(a,c,s,v,w,t);right_counts.append(len(rs))
  for g,ll in (('G',ls),('Q1',qs),('J1',js)):
   left_counts[g].append(len(ll))
   for lift in ll:
    b=lift[0]
    for x,y,r in rs:
     row=''.join(map(str,canonical((x,y,a,b,c))))
     matrices[g][ROWS.index(row)][i]+=1
 return {'states':len(states),'ordered_rim':NAMES,
  'state_sha256':hashlib.sha256(packed(states)).hexdigest(),
  'matrices_sha256':hashlib.sha256(packed(matrices)).hexdigest(),
  'left_counts_sha256':{g:hashlib.sha256(packed(v)).hexdigest() for g,v in left_counts.items()},
  'right_counts_sha256':hashlib.sha256(packed(right_counts)).hexdigest(),
  'original_edges_left':LEFT,'original_edges_right':RIGHT,
  'source_realizability_asserted':False,'new_Lean':False}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--build',action='store_true');ap.add_argument('--certificate',type=Path,default=D/'caps.json');a=ap.parse_args()
 data=json.loads(packed(compute()))
 if a.build:
  with a.certificate.open('x') as f:json.dump(data,f,indent=2);f.write('\n')
 else:assert json.loads(a.certificate.read_text())==data
 print(json.dumps({'status':'PASS independent full C13 caps',**data},sort_keys=True))
if __name__=='__main__':main()
