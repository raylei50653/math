#!/usr/bin/env python3
"""Independent stdlib integer replay of the C11 separating functional.

No scipy, pickle, sparse solver matrix, or frozen Kempe generator is imported.
Noncrossing partitions use decomposition at the block containing the first point.
"""
from pathlib import Path
from functools import lru_cache
from itertools import combinations,product,permutations
from collections import Counter,defaultdict
import argparse,gzip,hashlib,importlib.util,json,time
D=Path(__file__).resolve().parent
A=D.parent/'frozen/audits/2026-10-20-r6-941-j1-w5-9c36e3c'
IP=A/'interface/certificate-v4.json.gz'
SPEC=importlib.util.spec_from_file_location('independent_caps',D/'check.py')
capsmod=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(capsmod)
H=tuple(p for p in permutations(range(4)) if p[0]//2==p[1]//2 and p[2]//2==p[3]//2)
REPS=((0,1,2,3),(0,2,1,3),(0,3,2,1))
def packed(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
@lru_cache(maxsize=None)
def hc(t):return min(tuple(p[v] for v in t) for p in H)
def canonical(t):return capsmod.canon(t)
def proper(t):return all(t[i]!=t[(i+1)%len(t)] for i in range(len(t)))
@lru_cache(None)
def noncrossing_partitions(n):
 if n==0:return ((),)
 ans=[]
 for mask in range(1<<(n-1)):
  block=(0,)+tuple(i for i in range(1,n) if mask&(1<<(i-1)))
  ends=block+(n,)
  intervals=[tuple(range(ends[k]+1,ends[k+1])) for k in range(len(block))]
  for inner in product(*(noncrossing_partitions(len(interval)) for interval in intervals)):
   row=[0]*n;nextlabel=1
   for interval,part in zip(intervals,inner):
    for i,label in zip(interval,part):row[i]=nextlabel+label
    if part:nextlabel+=max(part)+1
   ans.append(tuple(row))
 return tuple(sorted(ans))
@lru_cache(maxsize=1)
def build_columns(states):
 index={t:i for i,t in enumerate(states)}
 hrows=sorted({hc(tuple(p[v] for v in t)) for t in states for p in REPS})
 assert len(hrows)==22143 and len(H)==8
 hi={t:i for i,t in enumerate(hrows)}
 rowids=[index[canonical(t)] for t in hrows]
 nc=noncrossing_partitions(11);assert len(nc)==58786 and len(set(nc))==58786
 parts=[p for p in nc if proper(p)];assert len(parts)==1585
 sideparts=defaultdict(list)
 for p in nc:
  b=max(p)+1
  edges=Counter(tuple(sorted((p[i],p[(i+1)%11]))) for i in range(11) if p[i]!=p[(i+1)%11])
  # A noncrossing boundary walk around a tree traverses every tree edge twice.
  if len(edges)!=b-1 or any(mult!=2 for mult in edges.values()):continue
  adjacency=[[] for _ in range(b)]
  for u,v in edges:adjacency[u].append(v);adjacency[v].append(u)
  colours={0:0};pending=[0]
  while pending:
   u=pending.pop()
   for v in adjacency[u]:
    if v not in colours:colours[v]=1-colours[u];pending.append(v)
    else:assert colours[u]!=colours[v]
  assert len(colours)==b
  side=tuple(colours[v] for v in p)
  sideparts[side].append(p);sideparts[tuple(1-v for v in side)].append(p)
 columns=set()
 for t in hrows:
  for p in sideparts[tuple(v//2 for v in t)]:
   counts=Counter()
   for chosen in range(1<<(max(p)+1)):
    switched=tuple(v^(1 if chosen&(1<<p[i]) else 0) for i,v in enumerate(t))
    counts[hi[hc(switched)]]+=1
   columns.add(tuple(sorted(counts.items())))
 cols=sorted(columns);assert len(cols)==36487
 inter=json.load(gzip.open(IP,'rt'))
 assert hashlib.sha256(packed(cols)).hexdigest()==inter['kempe']['columns_sha256']
 return hrows,rowids,cols,parts

def sparse_vector(items,size,label):
 assert isinstance(items,list)
 out=[0]*size;seen=set()
 for i,v in items:
  assert type(i) is int and 0<=i<size and i not in seen,(label,i)
  assert type(v) is int and v!=0,(label,i,v)
  seen.add(i);out[i]=v
 return out

def verify(certificate):
 start=time.monotonic();ind=capsmod.compute();states=tuple(tuple(c['core']) for c in ind['caps'])
 inter=json.load(gzip.open(IP,'rt'));live=set(inter['live'])
 hrows,rowids,columns,parts=build_columns(states);n=len(states);nh=len(hrows);nc=len(columns)
 print(json.dumps({'stage':'independent columns regenerated','elapsed_seconds':round(time.monotonic()-start,2),'states':n,'half_rows':nh,'columns':nc,'span_columns':len(parts)}),flush=True)
 ray=json.loads(certificate.read_text());eq=sparse_vector(ray['equality_multipliers'],nh+n,'equalities')
 posweights=sparse_vector(ray['positive_row_multipliers'],10,'positive rows')
 assert all(v>=0 for v in posweights) and sum(posweights)>0
 assert sum(posweights)==ray['positive_weight_sum']
 rows=[0,2,3,5,7,8,9]
 pos=[[rec['ten_coefficients']['G'][j] for rec in ind['caps']] for j in rows]
 sectors=[[0]*n for _ in range(2)]
 for i,rec in enumerate(ind['caps']):
  cc=dict(zip(capsmod.NAMES,rec['core']))
  for b,p,h,R in rec['G_bphR']:
   for x,y,r in rec['right_xyr']:
    if capsmod.rownum((x,y,cc['a'],b,cc['c']))==9:
     sectors[0][i]+=h==cc['a'];sectors[1][i]+=h==b
 pos+=sectors
 witness=[0]*n
 for rec in inter['witnesses']:witness[rec['canonical_id']]=1
 pos.append(witness)
 zcoef=eq[nh:].copy()
 for r,i in enumerate(rowids):zcoef[i]+=8*eq[r]
 for weight,pr in zip(posweights,pos):
  if weight:
   for i,v in enumerate(pr):zcoef[i]+=weight*v
 assert all(zcoef[i]<=0 for i in live),'positive coefficient on nonnegative core variable'
 orbitcoef=[-sum(eq[r]*v for r,v in col) for col in columns]
 assert all(v<=0 for v in orbitcoef),'positive coefficient on nonnegative Kempe orbit variable'
 span_residuals=[]
 for p in parts:
  eqpairs=[(j,i) for i in range(11) for j in range(i) if p[i]==p[j]]
  val=sum(eq[nh+i] for i,t in enumerate(states) if eq[nh+i] and all(t[u]==t[v] for u,v in eqpairs))
  span_residuals.append(val)
 assert not any(span_residuals),'signed planar-span coordinate was not cancelled'
 slacks=[[i,-zcoef[i]] for i in sorted(live) if zcoef[i]]+[[n+j,-v] for j,v in enumerate(orbitcoef) if v]
 assert slacks==ray['nonnegative_slacks'],'nonnegative slack manifest differs'
 out={'status':'PASS independent exact integer separating functional','certificate_sha256':hashlib.sha256(certificate.read_bytes()).hexdigest(),'states':n,'half_rows':nh,'kempe_columns':nc,'proper_noncrossing_span_columns':len(parts),'live_nonnegative_core_coordinates':len(live),'positive_row_names':['N01012(G)','N01023(G)','N01201(G)','N01203(G)','N01213(G)','N01231(G)','N01232(G)','A_a','A_b','short_W5_witness_sum'],'positive_weights':posweights,'positive_weight_sum':sum(posweights),'nonzero_slacks':len(slacks),'same_source_contradiction_under_frozen_contract':True,'arbitrary_necessary_model_realized':False,'new_Lean':False}
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--certificate',type=Path,default=D.parent/'geometry/orbit-farkas-certificate.json');args=ap.parse_args()
 print(json.dumps(verify(args.certificate),sort_keys=True))
if __name__=='__main__':main()
