"""Necessary Kempe closure for any planar disk with original simple C6.
Enumerates noncrossing component partitions, not inner source graphs.
"""
import itertools,json
from pathlib import Path
from probe import canon
N=6
ROWS=sorted({canon(w) for w in itertools.product(range(4),repeat=N) if all(w[i]!=w[(i+1)%N] for i in range(N))})
PAIRS=(((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2)))

def partitions(n):
 def rec(p,m):
  if len(p)==n:yield tuple(p);return
  for x in range(m+2):yield from rec(p+[x],max(m,x))
 yield from rec([0],0)

def noncrossing(p):
 return not any(p[a]==p[c] and p[b]==p[d] and p[a]!=p[b] for a,b,c,d in itertools.combinations(range(len(p)),4))

PARTS=[p for p in partitions(N) if noncrossing(p)]

def options(row,split):
 colors=tuple(map(int,row));pairs=PAIRS[split]
 group={c:g for g,p in enumerate(pairs) for c in p}
 swap={c:p[1-i] for p in pairs for i,c in enumerate(p)}
 out=[]
 for p in PARTS:
  blocks=[[i for i,x in enumerate(p) if x==b] for b in range(max(p)+1)]
  if any(len({group[colors[i]] for i in b})!=1 for b in blocks):continue
  if any(group[colors[i]]==group[colors[(i+1)%N]] and p[i]!=p[(i+1)%N] for i in range(N)):continue
  orbit=set()
  for sw in itertools.product((0,1),repeat=len(blocks)):
   w=[swap[c] if sw[p[i]] else c for i,c in enumerate(colors)]
   assert all(w[i]!=w[(i+1)%N] for i in range(N))
   orbit.add(canon(w))
  out.append((p,tuple(sorted(orbit))))
 return out
OPTIONS={(r,s):options(r,s) for r in ROWS for s in range(3)}

def prune(initial):
 S=set(initial); steps=[]
 while True:
  for r in sorted(S):
   for s in range(3):
    opt=OPTIONS[r,s]
    if not any(set(o)<=S for _,o in opt):
     steps.append({'row':r,'split':s,'witnesses':[{'partition':p,'missing':min(set(o)-S)} for p,o in opt]})
     S.remove(r);break
   else:continue
   break
  else:return S,steps

def run():
 data=json.loads(Path(__file__).with_name('outer_cut_results.json').read_text())
 R=[]
 for r in data['records']:
  if r['excluded']:continue
  masks={q:r['masks'].get(q,0) for q in ROWS}; tau=r['target']
  initial={q for q,m in masks.items() if not m & ~tau}
  S,steps=prune(initial)
  possible=0
  for q in S:possible|=masks[q]
  result={k:r[k] for k in ('kind','pair','side','query','target')}
  result.update(initial=sorted(initial),final=sorted(S),steps=steps,possible=possible,missing=tau & ~possible,excluded=possible!=tau)
  R.append(result)
  print(result['query'],r['pair'],r['side'],'nonzero',len(r['masks']),'initial',len(initial),'final',len(S),'possible',possible,'excluded',possible!=tau,flush=True)
 Path(__file__).with_name('kempe_results.json').write_text(json.dumps({'rows':ROWS,'noncrossing_partitions':PARTS,'records':R},indent=2))
 print('ALL',len(R),sum(r['excluded'] for r in R))
if __name__=='__main__':run()
