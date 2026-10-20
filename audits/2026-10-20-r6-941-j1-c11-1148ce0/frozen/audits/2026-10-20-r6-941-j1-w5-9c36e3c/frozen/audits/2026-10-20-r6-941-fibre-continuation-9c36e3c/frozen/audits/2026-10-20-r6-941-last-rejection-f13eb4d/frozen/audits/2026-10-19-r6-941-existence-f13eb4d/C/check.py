#!/usr/bin/env python3
"""All triangulated hexagon patches with zero/one internal vertex and contractions.
Exact common-exterior count projection; no graph realization claimed for controls.
"""
from pathlib import Path
from itertools import combinations, product
from collections import Counter
import json, hashlib, argparse
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
FROZEN=AUDIT/'frozen'
ROWS=('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
RIM=('a','b','q','L','R','n')

def canon(t):
 d={};return tuple(d.setdefault(c,len(d)) for c in t)
def proper(t):return all(t[i]!=t[(i+1)%len(t)] for i in range(len(t)))
def growth(n,t=(0,)):
 if len(t)==n:yield t;return
 for c in range(min(3,max(t)+1)+1):yield from growth(n,t+(c,))
def pair(a,b):return tuple(sorted((a,b)))
def tris(vertices):
 if len(vertices)<=3:return [()]
 edges=[pair(vertices[i],vertices[j]) for i in range(len(vertices)) for j in range(i+1,len(vertices)) if j-i not in (1,len(vertices)-1)]
 pos={v:i for i,v in enumerate(vertices)}
 def cross(e,f):
  a,b=sorted(pos[x] for x in e);c,d=sorted(pos[x] for x in f)
  return a<c<b<d or c<a<d<b
 return [tuple(sorted(es)) for es in combinations(edges,len(vertices)-3) if not any(cross(e,f) for e,f in combinations(es,2))]
def patches():
 zero=tris(tuple(range(6)));one=set()
 for degree in range(3,7):
  for spokes in combinations(range(6),degree):
   base={pair(6,v) for v in spokes};gap_options=[]
   for i,u in enumerate(spokes):
    v=spokes[(i+1)%degree];seq=tuple((u+j)%6 for j in range((v-u)%6+1))
    if len(seq)>2:base.add(pair(u,v))
    gap_options.append(tris(seq))
   for options in product(*gap_options):one.add(tuple(sorted(base.union(*(set(x) for x in options)))))
 return [(0,p) for p in zero]+[(1,p) for p in sorted(one)]
def relation(internal,edges,eqmask,states):
 # Contract exactly the equality edges; all six original rim edges stay inequalities.
 parent=list(range(6+internal))
 def root(x):
  while parent[x]!=x:x=parent[x]
  return x
 for i,(u,v) in enumerate(edges):
  if eqmask>>i&1:parent[root(u)]=root(v)
 classes=tuple(root(i) for i in range(len(parent)))
 inequalities=[(i,(i+1)%6) for i in range(6)]+[e for i,e in enumerate(edges) if not eqmask>>i&1]
 if any(classes[u]==classes[v] for u,v in inequalities):return None
 rel=[]
 for t in states:
  lifts=[]
  for color in range(4) if internal else (None,):
   z=t+(color,) if internal else t
   if all((z[u]==z[v])==bool(eqmask>>i&1) for i,(u,v) in enumerate(edges)):lifts.append(color)
  rel.append(lifts)
 return rel,len(set(classes)),classes

def calculate():
 manifest=json.loads((HERE/'INPUTS.json').read_text())
 assert manifest['base']=='f13eb4d0887d962021992ae7afe3323af4d79cd3'
 for relative,expected in manifest['files'].items():
  raw=(FROZEN/relative).read_bytes()
  assert len(raw)==expected['bytes'] and hashlib.sha256(raw).hexdigest()==expected['sha256']
 inputs={
 'positive':'audits/2026-10-19-r6-941-leakage-b89c591/A/source-positive-certificate.json',
 'zero':'audits/2026-10-19-r6-941-acceptance-13dc5ff/A/acceptance-zero-controls.json',
 'catalogue':'audits/2026-10-18-smaller-bad-counts-e1617a2/frozen/artifacts/c5_cells/cells.json'}
 data={k:json.loads((FROZEN/v).read_text()) for k,v in inputs.items()}
 controls=data['positive']['records']+data['zero']['records'];K=set(map(int,data['catalogue']['cells']))
 states=[t for t in growth(6) if proper(t)];index={t:i for i,t in enumerate(states)}
 eight=[t for t in growth(8) if proper(t)];index8={t:i for i,t in enumerate(eight)}
 # Every complete exterior colouring has all private colours; each coefficient
 # multiplies its complete fixed-representative count, not an orbit cardinality.
 records=[];weights={r['name']:[[0]*len(states) for _ in ROWS] for r in controls}
 for j,row in enumerate(ROWS):
  x,y,a,b,c=map(int,row)
  for n,R,L,q in product(range(4),repeat=4):
   e=(a,n,R,L,q,c,x,y);rim=(a,b,q,L,R,n)
   good=proper(e) and b not in (a,c,q)
   records.append([j,n,R,L,q,index8.get(canon(e),-1),index.get(canon(rim),-1),good])
   if good:
    ei=index8[canon(e)];ri=index[canon(rim)]
    for rec in controls:weights[rec['name']][j][ri]+=rec['exterior_counts'][ei]
 out=[];signatures={};skipped=0
 for internal,edges in patches():
  assert len(edges)==3+3*internal
  for eqmask in range(1<<len(edges)):
   result=relation(internal,edges,eqmask,states)
   if result is None:skipped+=1;continue
   lifts,classes,mapping=result;sig=tuple(map(len,lifts))
   assert any(sig)
   # Each generated candidate is a legal completed graph of this size;
   # equality classes containing rim nodes inherit original identities.
   cost=-2+internal-(6+internal-classes)
   counts={name:[sum(w*m for w,m in zip(row,sig)) for row in W] for name,W in weights.items()}
   masks={name:sum(1<<j for j,v in enumerate(ns) if v) for name,ns in counts.items()}
   key=str(len(signatures))
   if sig not in signatures:signatures[sig]=key
   key=signatures[sig]
   out.append({'internal':internal,'edges':[list(e) for e in edges],'equality_mask':eqmask,'classes':list(mapping),'completed_k_delta':cost,'signature_id':int(key),'lifts':lifts,'counts':counts,'masks':masks,'outside_catalogue':{n:m not in K for n,m in masks.items()}})
 summary={}
 for rec in controls:
  name=rec['name'];summary[name]={'support_histogram':dict(sorted(Counter(x['masks'][name] for x in out).items())), 'outside_count':sum(x['outside_catalogue'][name] for x in out),'target_count':sum(x['counts'][name][9]>0 and all(x['counts'][name][j]==0 for j in (1,4,6)) for x in out)}
 return {'base':'f13eb4d0887d962021992ae7afe3323af4d79cd3','source_realized':False,'source_contract_scope':'Full frozen r6 original p=h=5 minimal source, complete support 941; controls remain necessary models only.','input_sha256':{v:hashlib.sha256((FROZEN/v).read_bytes()).hexdigest() for v in inputs.values()},'rim':RIM,'rows':ROWS,'rim_states':states,'exterior_records':records,'patch_counts':dict(Counter(i for i,p in patches())),'raw_signed_patches':sum(1<<len(p) for i,p in patches()),'inconsistent_contractions':skipped,'candidate_count':len(out),'distinct_count_signatures':len(signatures),'summary':summary,'candidates':out}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--build',action='store_true');ap.add_argument('--certificate',type=Path,default=HERE/'certificate.json');args=ap.parse_args();d=calculate();p=args.certificate
 if args.build:
  with p.open('x') as f:json.dump(d,f,ensure_ascii=False,separators=(',',':'));f.write('\n')
 else:assert json.loads(p.read_text())==json.loads(json.dumps(d))
 print(json.dumps({k:d[k] for k in ('patch_counts','raw_signed_patches','inconsistent_contractions','candidate_count','distinct_count_signatures','summary')},sort_keys=True))
if __name__=='__main__':main()
