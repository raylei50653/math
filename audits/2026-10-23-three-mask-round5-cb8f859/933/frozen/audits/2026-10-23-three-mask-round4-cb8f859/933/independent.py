#!/usr/bin/env python3
"""Independent r-neighbour formula, separate-palette partitions, actual full maps."""
import argparse,itertools,json,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent
SRC='audits/2026-10-18-smaller-bad-counts-e1617a2/frozen/audits/2026-10-18-smaller-bad-e1617a2/kempe-consistency.json'
E=('a','n','R','L','q','c','x','y');D=('a','n','R','L','q','c','s','v','w','t')
def canon(t):
 names={};return tuple(names.setdefault(c,len(names)) for c in t)
def proper_cycle(t):return all(t[i]!=t[(i+1)%len(t)] for i in range(len(t)))
def restricted(n,t=()):
 if len(t)==n:yield t;return
 for c in range(max(t,default=-1)+2):yield from restricted(n,t+(c,))
def r_choices(d,x,y):
 a,n,R,L,q,c,s,v,w,t=d
 if not proper_cycle(d) or x in (y,c,s) or y in (a,t):return []
 return sorted(set(range(4))-{x,y,s,v,w,t})
def refills(d,index):
 return [(r,x,y,index[canon(tuple(d[:6])+(x,y))]) for x,y in itertools.product(range(4),repeat=2) for r in r_choices(d,x,y)]
def palette_partitions(t):
 groups=[[i for i,c in enumerate(t) if c in pair] for pair in ((0,2),(1,3))];ans=[]
 for left in restricted(len(groups[0])):
  for right in restricted(len(groups[1])):
   raw=[None]*10
   for i,c in zip(groups[0],left):raw[i]=c
   for i,c in zip(groups[1],right):raw[i]=c+max(left,default=-1)+1
   p=canon(raw)
   if any(t[i]%2==t[(i+1)%10]%2 and p[i]!=p[(i+1)%10] for i in range(10)):continue
   if any(p[a]==p[c] and p[b]==p[d] and p[a]!=p[b] for a,b,c,d in itertools.combinations(range(10),4)):continue
   ans.append(p)
 return sorted(ans)
def component(vertices,edges,colors,root):
 adj={v:set() for v in vertices}
 for a,b in edges:
  if colors[a] in (1,3) and colors[b] in (1,3):adj[a].add(b);adj[b].add(a)
 seen=set();todo=[root]
 while todo:
  v=todo.pop()
  if v not in seen:seen.add(v);todo.extend(adj[v]-seen)
 return seen

def compute():
 cert=json.loads((P/'certificate.json').read_text());src=json.loads((P/'frozen'/SRC).read_text());ts=[tuple(t) for t in src['tuples']];ei={t:i for i,t in enumerate(ts)};ds=[tuple(t) for t in cert['D_words']];di={t:i for i,t in enumerate(ds)};live=set(next(r['surviving_ids'] for r in src['results'] if r['source_mask']==933))
 kernels=[];empty=0
 for j,t in enumerate(ts):
  row={};records=[]
  for tail in itertools.product(range(4),repeat=4):
   d=t[:6]+tail;did=di[canon(d)] if proper_cycle(d) else None;choices=r_choices(d,t[6],t[7]);records.append([did,choices]);empty+=not choices
   if choices:row[str(did)]=row.get(str(did),0)+len(choices)
  assert records==cert['complete_274_by_256_tail_fibres'][j]
  assert row==cert['generic_E_to_D_sparse_kernel'][j];kernels.append(row)
 local=[]
 for tail in itertools.product(range(4),repeat=4):
  d=(0,1,0,2,3,0)+tail;fills=refills(d,ei);local.append((tail,fills))
 relevant=[(tail,fills) for tail,fills in local if any((x,y) in ((1,3),(3,1)) for r,x,y,e in fills)]
 killed=[tail for tail,fills in relevant if any(e not in live for r,x,y,e in fills)];survive=[tail for tail,fills in relevant if all(e in live for r,x,y,e in fills)]
 assert (len(relevant),len(killed),len(survive))==(24,18,6)
 assert set(survive)==set(map(tuple,cert['six_surviving_necessary_D_tails']))
 component_results=[]
 for lemma in cert['D_component_lemmas']:
  t=tuple(lemma['literal_D']);parts=palette_partitions(t);assert parts==[tuple(x['partition']) for x in lemma['all_compatible_component_options']]
  good=[]
  for part in parts:
   clean=True
   for bits in itertools.product((False,True),repeat=max(part)+1):
    word=tuple((c^2) if bits[part[i]] else c for i,c in enumerate(t))
    if any(e not in live for r,x,y,e in refills(word,ei)):clean=False;break
   if clean:good.append(list(part))
  assert good==lemma['surviving_necessary_partitions'];component_results.append({'target':lemma['target'],'all_options':len(parts),'surviving_necessary_partitions':len(good)})
 # Actual disk controls: the bare D rim with private pendant trees. They are
 # explicit whole colourings, not complete original minimum-source realizations.
 rim=list(zip(D,D[1:]+D[:1]));cap=[('x','y'),('x','c'),('x','s'),('x','r'),('y','a'),('y','t'),('y','r')]+[('r',v) for v in ('s','v','w','t')];pendants=[('s','S1'),('t','T1'),('L','O1'),('O1','O2')];edges=rim+cap+pendants;vertices=list(D)+['r','x','y','S1','T1','O1','O2'];controls=[]
 for i,tail in enumerate(cert['six_surviving_necessary_D_tails']):
  d=(0,1,0,2,3,0)+tuple(tail);colors=dict(zip(D,d),r=0 if i<2 else 2,x=1 if i<4 else 3,y=3 if i<4 else 1);colors.update(S1=4-colors['s'] if colors['s'] in (1,3) else 1,T1=4-colors['t'] if colors['t'] in (1,3) else 3,O1=1,O2=3)
  assert all(colors[a]!=colors[b] for a,b in edges)
  actual=component(vertices,edges,colors,'x');assert 'y' in actual and 'O1' not in actual and 'O2' not in actual
  changed={v:(4-c if v in actual and c in (1,3) else c) for v,c in colors.items()};assert all(changed[a]!=changed[b] for a,b in edges)
  assert tuple(changed[v] for v in E)==((0,1,0,2,3,0,3,1) if i<4 else (0,1,0,2,3,0,1,3))
  if i<2:assert actual=={'x','y'} and all(colors[v]==changed[v] for v in D)
  else:assert {'S1','T1'}<=actual
  controls.append({'target':i,'vertices':vertices,'edges':[list(e) for e in edges],'entire_source_colouring':[colors[v] for v in vertices],'entire_destination_colouring':[changed[v] for v in vertices],'one_complete_switched_E13_component':sorted(actual),'rootless_component_fixed':['O1','O2'],'bijection_status':'triggered and holds','full_original_r6_933_source':'not triggered'})
 return {'status':'PASS','complete_generic_tail_fibres_checked':274*256,'empty_generic_tail_fibres':empty,'all_generic_kernel_entries_match':True,'related_D_tuples':24,'forced_zero_D_tuples':18,'surviving_necessary_D_tails':[list(t) for t in survive],'component_reconstruction':component_results,'complete_whole_colouring_controls':controls,'source_realization_claimed':False,'certificate_sha256':hashlib.sha256((P/'certificate.json').read_bytes()).hexdigest()}
def main():
 p=argparse.ArgumentParser();p.add_argument('--build',action='store_true');args=p.parse_args();expected=compute();path=P/'independent-certificate.json'
 if args.build:
  with path.open('x') as f:json.dump(expected,f,indent=2);f.write('\n')
 assert json.loads(path.read_text())==expected
 print(json.dumps({k:v for k,v in expected.items() if k!='complete_whole_colouring_controls'},sort_keys=True))
if __name__=='__main__':main()
