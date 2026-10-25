"""Necessary same-exterior Kempe envelope; no source realization claim."""
import argparse,itertools,json,time
from functools import lru_cache
from pathlib import Path
HERE=Path(__file__).resolve().parent
SOURCE=HERE/'frozen/audits/2026-10-23-941-types-wrong-side-round7-6b09cd4/certificate.json'
PAIRS=tuple(itertools.combinations(range(4),2))
OUTER=(0,1,2,3,2)
REJECT={(0,1,0,2,1),(0,1,2,0,2),(0,1,2,1,2)}
def canon(w):
 d={};return tuple(d.setdefault(x,len(d)) for x in w)
def join(parts):
 blocks=[]
 for p in parts:
  for b in p:
   b=set(b)
   hit=[s for s in blocks if s&b]
   for s in hit:blocks.remove(s);b|=s
   blocks.append(b)
 return tuple(sorted(tuple(sorted(b)) for b in blocks))
@lru_cache(None)
def partitions(n):
 if n==0:return ((),)
 ans=[]
 for p in partitions(n-1):
  ans.append(p+((n-1,),))
  for i in range(len(p)):ans.append(p[:i]+(p[i]+(n-1,),)+p[i+1:])
 return tuple(ans)
def noncrossing(p,cycle):
 labels={v:i for i,b in enumerate(p) for v in b}
 seq=[labels[v] for v in cycle if v in labels]
 for a,b,c,d in itertools.combinations(range(len(seq)),4):
  if seq[a]==seq[c] and seq[b]==seq[d] and seq[a]!=seq[b]:return False
 return True
@lru_cache(None)
def exterior_partitions(word,pair):
 colors=word+OUTER
 active=[(v,) for v,c in enumerate(colors) if c in pair]
 edges=[(i,(i+1)%8) for i in range(8)]+[(8+i,8+(i+1)%5) for i in range(5)]
 forced=join([active,[(a,b) for a,b in edges if colors[a] in pair and colors[b] in pair]])
 result=[]
 for p in partitions(len(forced)):
  blocks=tuple(tuple(sorted(v for j in block for v in forced[j])) for block in p)
  if noncrossing(blocks,range(8)) and noncrossing(blocks,range(8,13)):result.append(blocks)
 return tuple(result)
def cap_connections(cap,word,lift,pair):
 vertices=cap['ordered_boundary']+cap['ordered_inner'];mp={v:i for i,v in enumerate(vertices)}
 colors=word+tuple(lift)
 p=join([[(v,) for v,c in enumerate(colors) if c in pair],[(mp[a],mp[b]) for a,b in cap['edges'] if colors[mp[a]] in pair and colors[mp[b]] in pair]])
 return tuple(tuple(v for v in b if v<8) for b in p if any(v<8 for v in b))
def targets(word,pair,full):
 ans=set();colors=word+OUTER;a,b=pair
 for bits in range(1<<len(full)):
  flip={v for i,block in enumerate(full) if bits>>i&1 for v in block}
  swapped=tuple(a+b-c if i in flip else c for i,c in enumerate(colors))
  q=canon(swapped[8:])
  if q in REJECT:return None
  if q==OUTER:
   palette={}
   for c in swapped[8:]:palette.setdefault(c,len(palette))
   ans.add(tuple(palette[c] for c in swapped[:8]))
 return frozenset(ans)
def precompute(cap):
 fibres={tuple(f['word']):f['full_lifts'] for f in cap['complete_fibres']}
 table={}
 words=sorted({tuple(p[c] for c in w) for w in cap['residual_accepting_words'] for p in itertools.permutations(range(4))})
 for word in words:
  canonical=canon(word);palette={c:word[canonical.index(c)] for c in set(canonical)}
  unused=sorted(set(range(4))-set(palette.values()))
  for c in sorted(set(range(4))-set(palette)):palette[c]=unused.pop(0)
  literal_lifts=[tuple(palette[c] for c in lift) for lift in fibres[canonical]]
  row=[]
  for pair in PAIRS:
   inner=set(cap_connections(cap,word,lift,pair) for lift in literal_lifts);allowed=[]
   for p in exterior_partitions(word,pair):
    outcomes=set();ok=True
    for local in inner:
     ts=targets(word,pair,join([p,local]))
     if ts is None:ok=False;break
     outcomes.update(ts)
    if ok:allowed.append((p,frozenset(outcomes)))
   row.append(allowed)
  table[word]=row
 return table
def annular_necessary(partition):
 if not noncrossing(partition,range(8)) or not noncrossing(partition,range(8,13)):return False
 # Used only as a necessary planar obstruction, never a realization test.
 through={i for i,b in enumerate(partition) if any(v<8 for v in b) and any(v>=8 for v in b)}
 if not through:return True
 labels={v:i for i,b in enumerate(partition) for v in b}
 orders=[]
 for circle in (list(range(8)),list(range(8,13))):
  for i,b in enumerate(partition):
   pos=[j for j,v in enumerate(circle) if v in b]
   if len(pos)<2:continue
   occupied=[]
   for k,start in enumerate(pos):
    end=pos[(k+1)%len(pos)];j=(start+1)%len(circle);hit=False
    while j!=end:
     hit|=labels.get(circle[j]) in through-{i};j=(j+1)%len(circle)
    if hit:occupied.append(k)
   if len(occupied)>1:return False
  seq=[]
  for v in circle:
   label=labels.get(v)
   if label in through and (not seq or seq[-1]!=label):seq.append(label)
  if len(seq)>1 and seq[0]==seq[-1]:seq.pop()
  if len(seq)!=len(through):return False
  orders.append(seq)
 a,b=orders
 return any(a==b[i:]+b[:i] or a==list(reversed(b[i:]+b[:i])) for i in range(len(b)))
def analyze(cap,strong=False):
 table=precompute(cap);current=set(table);rounds=[];witnesses={}
 while True:
  removed=[];stats=[];witnesses={}
  for word in sorted(current):
   allowed=[[p for p,ts in ps if ts<=current] for ps in table[word]]
   combinations=[]
   for i in range(3):
    j=5-i
    compatible=[(a,b) for a in allowed[i] for b in allowed[j] if (annular_necessary(a+b) if strong else noncrossing(a+b,range(8)) and noncrossing(a+b,range(8,13)))]
    combinations.append(compatible)
   stats.append(dict(word=word,individual=[len(p) for p in allowed],complementary=[len(c) for c in combinations]))
   if all(combinations):witnesses[word]=[c[0] for c in combinations]
   else:removed.append(word)
  rounds.append(dict(before=len(current),removed=removed,stats=stats))
  if not removed:break
  current.difference_update(removed)
 return dict(distribution=cap['distribution'],initial=len(table),remaining=sorted(current),rounds=rounds,necessary_controls=[dict(word=w,complementary_pairs=p) for w,p in sorted(witnesses.items())])
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--strong',action='store_true');parser.add_argument('--indices',nargs='*',type=int);parser.add_argument('--output',default='EXPLORATION-literal.json');args=parser.parse_args()
 source=json.loads(SOURCE.read_text());rows=[];start=time.monotonic()
 for index,cap in enumerate(source['caps']):
  if args.indices is not None and index not in args.indices:continue
  r=analyze(cap,args.strong);rows.append(r)
  print(cap['distribution'],r['initial'],'->',len(r['remaining']),'rounds',len(r['rounds']),'seconds',round(time.monotonic()-start,2),flush=True)
 with (HERE/args.output).open('x') as f:json.dump(dict(schema='k8-exterior-literal-necessary-v2',strong=args.strong,caps=rows),f,indent=2);f.write('\n')
if __name__=='__main__':main()
