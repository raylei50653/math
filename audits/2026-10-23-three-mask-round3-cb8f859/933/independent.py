#!/usr/bin/env python3
"""Independent standard-library reconstruction, using E-word-first enumeration.

Also checks every full fibre on one genuine plane cone control. This control is
explicitly outside the complete original minimum r6/933 source contract.
"""
import argparse,copy,hashlib,itertools,json
from pathlib import Path
P=Path(__file__).resolve().parent
ROWS=('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
E=('a','n','R','L','q','c','x','y');H=('a','n','R','L','q','b')
def canon(t):
 d={};return tuple(d.setdefault(c,len(d)) for c in t)
def build():
 c=json.loads((P/'certificate.json').read_text());tuples=sorted({canon(t) for t in itertools.product(range(4),repeat=8) if all(t[i]!=t[(i+1)%8] for i in range(8))})
 diagonals=[tuple(sorted((H[i],H[j]))) for i in range(6) for j in range(i+2,6) if (i,j)!=(0,5)]
 def cross(e,f):
  a,b=sorted(H.index(v) for v in e);p,q=sorted(H.index(v) for v in f);return a<p<b<q or p<a<q<b
 tri=sorted(tuple(sorted(t)) for t in itertools.combinations(diagonals,3) if not any(cross(e,f) for e,f in itertools.combinations(t,2)))
 assert [[list(e) for e in t] for t in tri]==c['triangulations']
 base=list(zip(E,E[1:]+E[:1]))+[('a','b'),('b','c'),('b','q')];original=base+[('p',v) for v in ('a','b','q','h','n')]+[('h',v) for v in ('q','L','R','n')]
 def proper(colors,edges):return all(colors[u]!=colors[v] for u,v in edges)
 mats=[[[0]*274 for _ in ROWS] for _ in tri];G=[[0]*274 for _ in ROWS];seen=set();local={}
 # Reverse of the main checker's outer-row-first enumeration. A single colour
 # permutation simultaneously acts on E, b, the outer frame, and every lift.
 for eid,t in enumerate(tuples):
  for b in range(4):
   colors=dict(zip(E,t),b=b)
   if not proper(colors,base):continue
   outer=tuple(colors[v] for v in ('x','y','a','b','c'));word=canon(outer)
   if ''.join(map(str,word)) not in ROWS:continue
   permutation={}
   for color,k in zip(outer,word):permutation[color]=k
   for color,k in zip(sorted(set(range(4))-set(permutation)),sorted(set(range(4))-set(permutation.values()))):permutation[color]=k
   colors={v:permutation[k] for v,k in colors.items()};ri=ROWS.index(''.join(map(str,word)))
   key=(ri,colors['n'],colors['R'],colors['L'],colors['q'])
   if key in seen:continue  # unused colour names give the same common S4 orbit
   seen.add(key)
   lifts=[[p,h] for p,h in itertools.product(range(4),repeat=2) if proper(dict(colors,p=p,h=h),original)];flags=[int(proper(colors,base+list(ds))) for ds in tri]
   local[key]=(eid,lifts,flags);G[ri][eid]+=len(lifts)
   for M,flag in zip(mats,flags):M[ri][eid]+=flag
 assert G==c['original_count_matrix'] and mats==c['candidate_count_matrices']
 for ri,n,R,L,q,eid,lifts,flags in c['complete_local_fibres']:
  key=(ri,n,R,L,q)
  if key in local:assert local[key]==(eid,lifts,flags)
  else:assert not lifts and not any(flags)
 # Cone over the original E rim, preserving one actual graph and every vertex.
 cone_edges=[('r',v) for v in E];counts=[];candidate_fibres=[];original_fibres=[];source_counts=[]
 z=[4-len(set(t)) for t in tuples]
 for ri,word in enumerate(ROWS):
  fixed=dict(zip(('x','y','a','b','c'),map(int,word)));fibres=[[] for _ in tri];old=[]
  for n,R,L,q,r in itertools.product(range(4),repeat=5):
   colors=dict(fixed,n=n,R=R,L=L,q=q,r=r)
   if not proper(colors,base+cone_edges):continue
   for j,ds in enumerate(tri):
    if proper(colors,list(ds)):fibres[j].append([n,R,L,q,r])
   for p,h in itertools.product(range(4),repeat=2):
    if proper(dict(colors,p=p,h=h),original):old.append([n,R,L,q,r,p,h])
  candidate_fibres.append(fibres);original_fibres.append(old);source_counts.append(len(old))
 counts=[[len(candidate_fibres[ri][j]) for ri in range(10)] for j in range(14)]
 assert counts==[[sum(a*b for a,b in zip(row,z)) for row in M] for M in mats]
 assert source_counts==[sum(a*b for a,b in zip(row,z)) for row in G]
 mask=sum(1<<i for i,n in enumerate(source_counts) if n)
 assert mask!=933,'control must never be presented as an original933 source'
 return {'status':'PASS','independent_order':'canonical-E-word then b, one common literal colour permutation','candidate_count':14,'complete_count_matrices_match':True,'all_local_fibres_match':True,'whole_graph_control':{'E':'one cone over the same ordered C8','source_counts':source_counts,'source_support_mask':mask,'source_contract_status':'not triggered','candidate_counts':counts,'candidate_full_fibres_by_outer_row':candidate_fibres,'original_full_fibres_by_outer_row':original_fibres,'exterior_counts':z,'outer_row_order':list(ROWS)},'source_realization_claimed':False,'certificate_sha256':hashlib.sha256((P/'certificate.json').read_bytes()).hexdigest()}
def main():
 p=argparse.ArgumentParser();p.add_argument('--build',action='store_true');args=p.parse_args();expected=build();path=P/'independent-certificate.json'
 if args.build:
  with path.open('x') as f:json.dump(expected,f,indent=2);f.write('\n')
 assert json.loads(path.read_text())==expected
 print(json.dumps({k:v for k,v in expected.items() if k!='whole_graph_control'},sort_keys=True))
if __name__=='__main__':main()
