from pathlib import Path
import importlib.util,itertools,json
D=Path(__file__).parent
path=D/'frozen/audits/2026-10-14-c4-c5-recursion-fdd3e22/degree4/check_transfer.py'
s=importlib.util.spec_from_file_location('helper',path); h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
# Cut boundary: z_left,s,v,w,t,z_right,p,q. Original z=0.
MAP={1:1,2:2,3:3,4:4,5:6,6:7}
CUT_EDGES=((0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,0))
def nc(parts):
 labels={v:i for i,b in enumerate(parts) for v in b}
 return all(not (labels[a]==labels[c] and labels[b]==labels[d] and labels[a]!=labels[b]) for a,b,c,d in itertools.combinations(range(8),4))
def cut_options(row,parts):
 blocks=parts[0]+parts[1]
 zb=next(b for b in blocks if 0 in b)
 other=tuple(tuple(MAP[v] for v in b) for b in blocks if 0 not in b)
 rest=tuple(v for v in zb if v!=0)
 cutrow=row[:5]+(row[0],)+row[5:]
 for flags in itertools.product((0,1),repeat=len(rest)):
  lr=((0,)+tuple(MAP[v] for v,f in zip(rest,flags) if not f),(5,)+tuple(MAP[v] for v,f in zip(rest,flags) if f))
  pp=other+lr
  labels={v:i for i,b in enumerate(pp) for v in b}
  if all(labels[a]==labels[b] for a,b in CUT_EDGES if cutrow[a] in (row[0],row[next(v for v in range(7) if row[v]!=row[0])]) and False): pass
  # edge equality of components required only if endpoints belong to a single pair
  if any(cutrow[a]!=cutrow[b] and any(cutrow[a] in pair and cutrow[b] in pair for pair in CURRENT_PAIRING) and labels[a]!=labels[b] for a,b in CUT_EDGES):continue
  if nc(pp):yield pp
 # original component stays connected between z halves
 pp=other+(tuple(sorted((0,5)+tuple(MAP[v] for v in rest))),)
 if nc(pp):yield pp

def opts(row,pairing,edges):
 global CURRENT_PAIRING
 CURRENT_PAIRING=pairing
 out=[]
 for parts in itertools.product(*(h.pair_partitions(row,pair,edges) for pair in pairing)):
  if not h.noncrossing(parts[0]+parts[1]):continue
  cuts=list(cut_options(row,parts))
  if cuts:out.append((parts,h.switch_orbit(row,parts,pairing),cuts))
 return out
rows=sorted({h.canonical(row) for row in itertools.product(range(4),repeat=7) if h.allowed(row)})
options={r:[opts(r,p,h.EDGES) for p in h.PAIRINGS] for r in rows}
live=set(rows)
while True:
 dead={r for r in live if any(not any(o<=live for parts,o,cuts in x) for x in options[r])}
 print('live',len(live),'dead',[h.name(r) for r in sorted(dead)])
 if not dead:break
 live-=dead
print('live',[h.name(r) for r in sorted(live)])
removed=[]
for row in rows:
 for pair in h.PAIRINGS:
  old=h.options(row,pair,h.EDGES);new=opts(row,pair,h.EDGES)
  a={pp for pp,o in old};b={pp for pp,o,c in new}
  if a!=b:removed.append({'row':h.name(row),'pair':pair,'old':len(a),'new':len(b)})
print('options reductions',removed)
for word in ['ABABCBC','ABACBCD','ABACDBD','ABCACBC','ABCDBCD']:
 row=tuple('ABCD'.index(c) for c in word)
 print('\nROW',word)
 for pairing in h.PAIRINGS:
  good=[parts for parts,o in h.options(row,pairing,h.EDGES) if o<=live]
  print(pairing,len(good),good)
proper=sorted({h.canonical(row) for row in itertools.product(range(4),repeat=7) if all(row[a]!=row[b] for a,b in h.EDGES)})
diffs=[]
for row in proper:
 for pairing in h.PAIRINGS:
  old=h.options(row,pairing,h.EDGES);new=opts(row,pairing,h.EDGES)
  if len(old)!=len(new):diffs.append((h.name(row),pairing,len(old),len(new)))
print('all proper rows',len(proper),'diffs',diffs)
