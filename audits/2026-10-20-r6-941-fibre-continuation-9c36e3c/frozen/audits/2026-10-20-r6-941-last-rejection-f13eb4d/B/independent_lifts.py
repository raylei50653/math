#!/usr/bin/env python3
"""Independent graph-edge/quotient replay of all 20 complete cap tables, stdlib."""
import gzip,json
from itertools import product
from math import factorial
from pathlib import Path
H=Path(__file__).resolve().parent
PINS=('a','n','R','L','q','u','s','v','w','t')
ROWS=('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
RIGHT=(('x','y'),('x','r'),('x','s'),('y','a'),('y','r'),('y','t'),('r','t'),('r','w'),('r','v'),('r','s'))
BASE=tuple((PINS[i],PINS[(i+1)%10]) for i in range(10))+(('b','a'),('b','q'))+RIGHT
HS=(('q',(('q','s'),('q','x'))),('q',(('q','x'),('u','x'))),('u',(('b','u'),('u','x'))),('s',(('b','s'),('b','u'))),('s',(('b','s'),('q','s'))))
LEFTS=((('b','n'),('q','R')), (('b','n','L'),), (('b','L'),), ())
ADDS=((),(),(('a','R'),),(('a','L'),('a','R'),('b','L')))
def canon(t):
 d={};return tuple(d.setdefault(v,len(d)) for v in t)
def graph(frame,extra,groups,added):
 classes=[];taken=set()
 for g in groups:classes.append(g);taken.update(g)
 classes += [(v,) for v in PINS+('b','x','y','r') if v not in taken]
 rep={v:g[0] for g in classes for v in g}
 edges=set(tuple(sorted((rep[v],rep[w]))) for v,w in BASE+extra+added)
 assert all(v!=w for v,w in edges)
 boundary=tuple(rep[v] for v in ('x','y','a','b',frame));assert len(set(boundary))==5
 return classes,sorted(edges),boundary,len(classes)-17

def main():
 cert=json.loads(gzip.decompress((H/'certificate.json.gz').read_bytes()));caps=json.loads(gzip.decompress((H/'complete-lifts.json.gz').read_bytes()))
 assert tuple(cert['core_order'])==PINS and tuple(cert['literal_rows'])==ROWS
 graphs=[graph(frame,extra,LEFTS[j],ADDS[j]) for frame,extra in HS for j in range(4)]
 assert [g[3] for g in graphs]==[-5,-5,-4,-3]*5
 assert [o['completed_inner_delta'] for o in cert['operations']]==[g[3] for g in graphs]
 matrices=[[[0]*len(caps) for r in ROWS] for g in graphs];total=0;empty=0
 for i,rec in enumerate(caps):
  f=dict(zip(PINS,rec['core']));all_lifts=[[] for g in graphs]
  for b,x,y,r in product(range(4),repeat=4):
   ff=dict(f,b=b,x=x,y=y,r=r)
   if any(ff[u]==ff[v] for u,v in BASE):continue
   for j,(classes,edges,boundary,cost) in enumerate(graphs):
    if any(any(ff[v]!=ff[g[0]] for v in g) for g in classes):continue
    if any(ff[u]==ff[v] for u,v in edges):continue
    all_lifts[j].append([b,x,y,r]);ri=ROWS.index(''.join(map(str,canon(tuple(ff[v] for v in boundary)))))
    matrices[j][ri][i]+=1;total+=1
  assert all_lifts==rec['complete_lifts'],('joint full graph lift mismatch',i)
  empty+=sum(not v for v in all_lifts)
  fac=factorial(4-len(set(rec['core'])))
  for M in matrices:
   for row in M:assert row[i]%fac==0;row[i]//=fac
 assert matrices==cert['matrices'],'all ten fixed-literal matrix rows'
 print(json.dumps({'independent_graph_replay':True,'candidates':len(graphs),'core_states':len(caps),'complete_cap_assignments':total,'empty_candidate_fibres':empty,'completed_costs':[-5,-5,-4,-3]},sort_keys=True))
if __name__=='__main__':main()
