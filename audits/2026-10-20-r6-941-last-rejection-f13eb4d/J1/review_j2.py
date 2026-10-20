#!/usr/bin/env python3
"""Independent literal cap and printed unique-block review of sibling J2."""
from pathlib import Path
from itertools import product
from collections import Counter
import hashlib,json
D=Path(__file__).resolve().parent;J2=D.parent/'J2';p=J2/'certificate.json';data=json.loads(p.read_text())
def canonical(t):
 names={};return tuple(names.setdefault(x,len(names)) for x in t)
def growth(n,t=(0,)):
 if len(t)==n:yield t;return
 for c in range(min(3,max(t)+1)+1):yield from growth(n,t+(c,))
states=[t for t in growth(10) if all(t[i]!=t[(i+1)%10] for i in range(10))];ix={t:i for i,t in enumerate(states)}
literal=[[] for _ in states]
for n,R,L,q,s,v,w,t in product(range(4),repeat=8):
 u=(0,n,R,L,q,1,s,v,w,t)
 if any(u[i]==u[(i+1)%10] for i in range(10)):continue
 if q in(1,2) or L in(0,2) or R==0:continue
 for r in range(4):
  if any(a==b for a,b in ((0,s),(1,t),(r,0),(r,1),(r,s),(r,v),(r,w),(r,t))):continue
  literal[ix[canonical(u)]].append([list(u),r])
assert literal==data['all_T_literal_lifts_including_empties']
assert list(map(len,literal))==data['J2_matrices']['F'][1]
selected=[i for i in data['live'] if literal[i]];assert selected==[f['core_index'] for f in data['forms']]
assert all(len(literal[i])==1 for i in selected) and len(selected)==12
names=('a','n','R','L','q','c','s','v','w','t')
review=[]
for f in data['forms']:
 u=f['literal_core'];a,n,R,L,q,c,s,v,w,t=u
 left=[(b,p,h) for b,p,h in product(range(4),repeat=3)
       if all(x!=y for x,y in ((b,a),(b,c),(b,q),(b,p),(p,a),(p,q),(p,n),(p,h),(h,q),(h,L),(h,R),(h,n)))]
 assert not left
 fam=f['family'];d=s;assert s==t
 if fam not in(2,3):continue
 z0='v' if v==0 else 'w';z1='v' if v==1 else 'w'
 if fam==2 and d==2:
  expected=[{'a'},{'q',z0},{'n','R','L','t'}|({z1} if z1=='w' else set()),{'c','s'}|({z1} if z1=='v' else set())]
 elif fam==2 and d==3:
  expected=[{'a','t'}|({z0} if z0=='w' else set()),{'q','s'}|({z0} if z0=='v' else set()),{'n','R','L',z1},{'c'}]
 elif fam==3 and d==2:
  expected=[{'a','t'}|({z0} if z0=='w' else set()),{'R','s'}|({z0} if z0=='v' else set()),{'q'},{'n',z1},{'L','c'}]
 else:
  expected=[{'a'},{'R',z0},{'q'},{'n','t'}|({z1} if z1=='w' else set()),{'L','c','s'}|({z1} if z1=='v' else set())]
 rec=f['pair_records'][2 if fam==2 else 1];assert len(rec['partitions'])==1
 actual={frozenset(b) for b in rec['partitions'][0]['blocks']}
 assert actual=={frozenset(b) for b in expected}
 assert set().union(*expected)==set(names) and sum(map(len,expected))==10
 review.append({'core_index':f['core_index'],'family':fam,'d':d,'all_blocks_match':True})
out={'status':'PASS','certificate_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'literal_cap_rebuilt':True,'twelve_coefficients_all_one':True,'all_original_left_lifts_empty':True,'eight_unique_partition_tables_checked':review,'source_realized':False,'last_rejection':'OPEN'}
print(json.dumps(out,sort_keys=True))
