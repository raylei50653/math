#!/usr/bin/env python3
"""Read-only independent audit of one-anchor locality for retained C5 supports."""
import argparse
import json
from collections import Counter
from hashlib import sha256
from itertools import permutations, combinations, product
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
Q=(0,1,0,1,2)
TARGETS=((0,1,0,2,1),(0,1,2,1,2))
PERMS=tuple(permutations(range(4)))
FAMILIES={'AA':'t2_path_palettes','AB':'t2_t1_endpoints','AC':'t2_t0_pairs','AE':'t2_t0_singles','BB':'bb','BC':'bc','BE':'be'}
EXPECTED={'AA':322,'AB':560,'AC':24,'AE':120,'BB':888,'BC':24,'BE':144}
EXTRA_GEO={'AA':'t2'}
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--out',type=Path,default=ROOT / 'artifacts/c5_no_mixed_hypothesis_audit/anchor.json')
parser.add_argument('--check',action='store_true')
args=parser.parse_args()
hashes={}
def read(suffix):
 p=ROOT/f'artifacts/c5_adjacent_degree5_no_mixed_{suffix}/observations.json'
 raw=p.read_bytes();hashes[str(p.relative_to(ROOT))]=sha256(raw).hexdigest();return json.loads(raw)
def flatten(rec):
 while 'original_record' in rec or 'inherited_record' in rec:
  rec=rec.get('original_record',rec.get('inherited_record'))
 return rec

def parse(rec,source):
 comps=[];spokes=[];names=[];offset=0
 for root in ('z','w'):
  side=source[root]
  for i,(k,F) in enumerate(zip(side['ports'],side['forbidden'],strict=True)):
   name='CDE'[i]+root
   comps.append(dict(name=name,root=root,support_index=offset,support=rec['supports'][offset],ports=k,Fq=F))
   names.append(name);offset+=1
  for i,h in enumerate(side['root_boundary']):
   assert rec['supports'][offset]==[h]
   spokes.append(dict(name=root+str(i),root=root,h=h,support_index=offset));names.append(root+str(i));offset+=1
 assert offset==len(rec['supports'])
 return comps,spokes,names

def mask(lift,anchor):
 return sum(1<<((anchor+i)%5) for i in range(min(lift),max(lift)))

def check_placement(rec,comps,spokes,names,pl):
 lifts=pl['lifts'];a=pl['anchor']
 assert len(lifts)==len(rec['supports'])
 for ss,ll in zip(rec['supports'],lifts,strict=True):
  assert sorted({(a+i)%5 for i in ll})==ss
  assert len(set(ll))==len(ss) and 0<=min(ll)<=max(ll)<=5
 order=[names.index(n) for n in pl['order']]
 assert sorted(order)==list(range(len(lifts)))
 for x,y in zip(order,order[1:]):assert max(lifts[x])<=min(lifts[y])
 roots={c['name']:c['root'] for c in comps}|{s['name']:s['root'] for s in spokes}
 rr=[roots[n] for n in pl['order']]
 assert sum(rr[j]!=rr[(j+1)%len(rr)] for j in range(len(rr)))==2
 masks=[]
 for c in comps:
  ll=lifts[c['support_index']]
  assert 0<max(ll)-min(ll)<5
  masks.append(mask(ll,a))
 for x,y in combinations(masks,2):assert not x&y
 for c in comps:
  lo,hi=min(lifts[c['support_index']]),max(lifts[c['support_index']])
  for s in spokes:assert not lo<lifts[s['support_index']][0]<hi
 # All supports, not only nontransportable ones, satisfy the incidence bound.
 for h in range(5):
  hit=[c for c in comps if h in c['support']]
  assert len(hit)<=2
  if len(hit)==2:
   used=[]
   for c in hit:
    ll=lifts[c['support_index']];lo,hi=min(ll),max(ll)
    x=next(v for v in ll if (a+v)%5==h)
    assert x in (lo,hi)
    used.append('right' if x==lo else 'left')
   assert set(used)=={'left','right'}
 return True

def options(qF,support,k,p):
 trans=[pi for pi in PERMS if all(pi[Q[h]]==p[h] for h in support)]
 by_partition=all((Q[i]==Q[j])==(p[i]==p[j]) for i,j in combinations(support,2))
 assert bool(trans)==by_partition
 if trans:
  images={tuple(sorted(pi[d] for d in qF)) for pi in trans}
  assert len(images)==1
  return True,[list(next(iter(images)))]
 stab=[pi for pi in PERMS if all(pi[p[h]]==p[h] for h in support)]
 out=[]
 for n in range(k+1):
  for F in combinations(range(4),n):
   if all(set(pi[d] for d in F)==set(F) for pi in stab):out.append(list(F))
 return False,out

rows=[];family_counts={};allbad=Counter();allhit=Counter();two_layout=Counter();two_hit_layout=Counter();failure_by_bad=Counter();summary_fail=0;placement_count=0
for cell,suffix in FAMILIES.items():
 d=read(suffix);geos=(read(EXTRA_GEO[cell]) if cell in EXTRA_GEO else d)['geometries']
 sources=d.get('original_records',d.get('original_frontier'))
 c_bad=Counter();c_hit=Counter();kept=0;queries=0;candidate_failures=0
 for final in d['records']:
  rec=flatten(final)
  if rec.get('status') in ('excluded','source_excluded'):continue
  kept+=1;source=sources[rec['source_id']];comps,spokes,names=parse(rec,source)
  common=source['z']['common'];assert common==source['w']['common']
  if 'common' in rec:assert common==rec['common']
  for root in ('z','w'):
   used={Q[h] for h in source[root]['root_boundary']}
   for F in source[root]['forbidden']:used.update(F)
   assert set(range(4))-used=={common}
  geo=geos[rec['geometry_id']];assert geo['supports']==rec['supports']
  for pl in geo['placements']:
   assert check_placement(rec,comps,spokes,names,pl);placement_count+=1
  targets=final.get('final_targets',final.get('targets'));assert len(targets)==2
  for ti,p in enumerate(TARGETS):
   assert targets[ti]['row']==list(p) and targets[ti]['status']=='accept'
   h=(1,2)[ti];sigma=((0,2,1,3),(0,1,2,3))[ti]
   qb=tuple(sigma[c] for c in Q);assert [i for i in range(5) if qb[i]!=p[i]]==[h]
   queries+=1;hit=[c['name'] for c in comps if h in c['support']]
   op=[options(c['Fq'],c['support'],c['ports'],p) for c in comps]
   bad=[c['name'] for c,(exact,_) in zip(comps,op) if not exact]
   assert set(bad)<=set(hit) and len(hit)<=2
   c_bad[len(bad)]+=1;c_hit[len(hit)]+=1;allbad[len(bad)]+=1;allhit[len(hit)]+=1
   if len(hit)==2:two_hit_layout['same_root' if hit[0][-1]==hit[1][-1] else 'opposite_roots']+=1
   if len(bad)==2:two_layout['same_root' if bad[0][-1]==bad[1][-1] else 'opposite_roots']+=1
   # Common-sigma anchor interface; outside the anchor, whole relations transport exactly.
   anchor_base={r:set(range(4))-{p[s['h']] for s in spokes if s['root']==r} for r in ('z','w')}
   for c in comps:
    if c['name'] not in hit:
     transported={sigma[d] for d in c['Fq']}
     exact,opts=op[comps.index(c)];assert exact and transported==set(opts[0])
     anchor_base[c['root']]-=transported
   # Literal fixed-frame interface: erase bad-component bans, keep every original spoke.
   base={r:set(range(4))-{p[s['h']] for s in spokes if s['root']==r} for r in ('z','w')}
   for c,(exact,opts) in zip(comps,op):
    if exact:base[c['root']]-=set(opts[0])
   failures=[]
   bad_comps=[(c,opts) for c,(exact,opts) in zip(comps,op) if not exact]
   for Fs in product(*(opts for _,opts in bad_comps)):
    E={r:set(base[r]) for r in base}
    for (c,_),F in zip(bad_comps,Fs):E[c['root']]-=set(F)
    full_F={c['name']:set(opts[0]) for c,(exact,opts) in zip(comps,op) if exact}
    full_F.update({c['name']:set(F) for (c,_),F in zip(bad_comps,Fs)})
    anchored_E={r:set(anchor_base[r]) for r in anchor_base}
    direct_E={r:set(range(4))-{p[s['h']] for s in spokes if s['root']==r} for r in ('z','w')}
    for c in comps:
     direct_E[c['root']]-=full_F[c['name']]
     if c['name'] in hit:anchored_E[c['root']]-=full_F[c['name']]
    assert E==anchored_E==direct_E
    pairs=[(a,b) for a in E['z'] for b in E['w'] if a!=b]
    if not pairs:failures.append(dict(Fs=Fs,residuals={r:sorted(E[r]) for r in E}))
   candidate_failures+=len(failures);failure_by_bad[len(bad)]+=len(failures)
   rows.append(dict(cell=cell,record_id=rec['id'],source_id=rec['source_id'],target=ti+1,anchor=h,common=common,hit=hit,bad=bad,anchor_spokes=[s['name'] for s in spokes if s['h']==h],fixed_base={r:sorted(base[r]) for r in base},anchor_base={r:sorted(anchor_base[r]) for r in anchor_base},candidate_failures=failures))
 assert kept==EXPECTED[cell]
 assert queries==d['summary']['target_queries']
 family_counts[cell]=dict(retained_supports=kept,queries=queries,nontransportable=dict(sorted(c_bad.items())),anchor_incident=dict(sorted(c_hit.items())),failing_candidate_joins=candidate_failures)
 summary_fail+=candidate_failures
# Exhaust the elementary edge-mask lemma independently of saved geometry.
arcs=[]
for a in range(5):
 for length in range(1,5):
  vertices={(a+i)%5 for i in range(length+1)}
  edges=sum(1<<((a+i)%5) for i in range(length))
  arcs.append((a,length,vertices,edges))
interval_controls=Counter()
for h in range(5):
 for selected in combinations([a for a in arcs if h in a[2]],3):
  assert any(x[3]&y[3] for x,y in combinations(selected,2))
  interval_controls['triples_checked']+=1
 for x,y in combinations([a for a in arcs if h in a[2]],2):
  if not x[3]&y[3]:
   assert h in {x[0],(x[0]+x[1])%5} and h in {y[0],(y[0]+y[1])%5}
   assert ((h==x[0]) != (h==y[0]))
   interval_controls['disjoint_pairs_checked']+=1
summary=dict(interval_controls=dict(interval_controls),retained_supports=sum(EXPECTED.values()),queries=len(rows),nontransportable=dict(sorted(allbad.items())),anchor_incident=dict(sorted(allhit.items())),two_nontransportable_roots=dict(two_layout),two_anchor_incident_roots=dict(two_hit_layout),failing_candidate_joins=summary_fail,failing_candidate_joins_by_nontransportable=dict(sorted(failure_by_bad.items())),saved_placements_checked=placement_count)
assert summary['queries']==4164
assert summary['nontransportable']=={0:2936,1:1184,2:44}
out=dict(frame=list(range(5)),q=Q,targets=TARGETS,anchor_changes=[dict(target=1,sigma=[0,2,1,3],anchor=1,old_color=2,new_color=1),dict(target=2,sigma=[0,1,2,3],anchor=2,old_color=0,new_color=2)],script_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),scope='one-anchor locality and exact fixed-frame interface; finite necessary supports, not disk realizability or local repair completeness',summary=summary,families=family_counts,inputs_sha256=hashes,queries=rows)
output_bytes=(json.dumps(out,indent=2,sort_keys=True)+'\n').encode()
if args.check:
 assert args.out.read_bytes()==output_bytes, f'stale output: {args.out}'
else:
 args.out.parent.mkdir(parents=True,exist_ok=True)
 args.out.write_bytes(output_bytes)
print(json.dumps(dict(summary=summary,families=family_counts),indent=2,sort_keys=True))
