#!/usr/bin/env python3
"""Stand-alone verifier for the broadened T1 candidate.
No producer imports. Rebuilds the shell from triangle fans, uses fixed-order
DFS, builds Kempe partitions by set-block recursion/gap noncrossing test,
and enumerates safe rectangles from the TRANSPOSED compatibility relation.
Only standard library dependencies. Runs entirely on local certificate files.
"""
import json,itertools,time,gzip,hashlib,copy,sys
from pathlib import Path
from collections import Counter,defaultdict
ROOT=Path(__file__).resolve().parent
BROWS=('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
QUERIES=(('c15-933',(0,1,2,0,0),933),('c18-933',(0,2,1,0,0),933),
 ('c04-941',(0,0,1,0,2),941),('c07-941',(0,0,2,0,1),941),
 ('c15-941',(0,1,2,0,0),941),('c18-941',(0,2,1,0,0),941),
 ('c20-941',(1,0,0,0,2),941),('c30-941',(2,0,0,0,1),941))

def normalize(seq):
 order=list(dict.fromkeys(seq))
 return ''.join(str(order.index(c)) for c in seq)
R=sorted({normalize(x) for x in itertools.product(range(4),repeat=6) if all(x[i]!=x[(i+1)%6] for i in range(6))})
assert len(R)==31
RI={r:i for i,r in enumerate(R)}
ALL=(1<<31)-1

def members(mask):return [i for i in range(31) if mask>>i&1]

def make_shell(kind,pair,e):
 names=['a0']
 for i in range(1,5):names.extend([f'y{i}_{j}' for j in range(1,e[i]+1)]+[f'a{i}'])
 names.extend([f'y0_{j}' for j in range(1,e[0]+1)])
 assert len(names)==8
 cmap={v:f'c{i}' for i,v in enumerate(names)}
 faces=[]
 for i in range(5):
  b=f'b{i}';faces.append((b,f'b{(i+1)%5}',cmap[f'a{i}']))
  path=[cmap[f'a{(i-1)%5}']]+[cmap[f'y{i}_{j}'] for j in range(1,e[i]+1)]+[cmap[f'a{i}']]
  faces += [(b,a,c) for a,c in zip(path,path[1:])]
 C=[f'c{i}' for i in range(8)]
 if kind=='BRIDGE':faces += [(C[pair],'x','y'),(C[(pair+4)%8],'y','x')]
 ends=['x'] if kind=='PINCH' else ['x','y']
 D=[[ends[s] if kind=='BRIDGE' else 'x']+[C[(pair+4*s+j)%8] for j in range(5)] for s in range(2)]
 def ed(a,b):return tuple(sorted((a,b)))
 E={ed(a,b) for f in faces for a,b in zip(f,f[1:]+f[:1])}
 for d in D:E |= {ed(a,b) for a,b in zip(d,d[1:]+d[:1])}
 V=[f'b{i}' for i in range(5)]+C+ends
 # Independent two-hole geometry check: fill each hole with its own cone.
 filled=faces+[(f'z{s}',d[i],d[(i+1)%6]) for s,d in enumerate(D) for i in range(6)]
 EF=Counter(ed(a,b) for f in filled for a,b in zip(f,f[1:]+f[:1]))
 outer={ed(f'b{i}',f'b{(i+1)%5}') for i in range(5)}
 assert all(n==(1 if edge in outer else 2) for edge,n in EF.items())
 assert len(V)+2-len(EF)+len(filled)==1
 # Each filled vertex link is a connected path (B) or cycle (other vertices).
 for v in V+['z0','z1']:
  le=[tuple(x for x in f if x!=v) for f in filled if v in f]
  ad=defaultdict(set)
  for a,b in le:ad[a].add(b);ad[b].add(a)
  seen=set();todo=[next(iter(ad))]
  while todo:
   u=todo.pop()
   if u not in seen:seen.add(u);todo.extend(ad[u]-seen)
  assert seen==set(ad)
  degrees=sorted(map(len,ad.values()))
  if v.startswith('b'):assert degrees[:2]==[1,1] and all(d==2 for d in degrees[2:])
  else:assert all(d==2 for d in degrees)
 return V,sorted(E),D,faces

def shell_colours(V,E,D):
 idx={v:i for i,v in enumerate(V)}
 earlier=[[] for _ in V]
 for a,b in E:
  a,b=sorted((idx[a],idx[b]));earlier[b].append(a)
 di=[[idx[v] for v in d] for d in D]
 M=[[0]*31 for _ in R];full={};counts=[]
 for bi,beta in enumerate(BROWS):
  colors=[int(c) for c in beta]+[-1]*(len(V)-5)
  for i in range(5):assert all(colors[i]!=colors[j] for j in earlier[i])
  lifts=[]
  def dfs(i):
   if i==len(V):
    a,b=[RI[normalize([colors[j] for j in d])] for d in di]
    M[a][b]|=1<<bi;lifts.append(''.join(map(str,colors)));return
   forbidden={colors[j] for j in earlier[i]}
   for c in range(4):
    if c not in forbidden:colors[i]=c;dfs(i+1)
   colors[i]=-1
  dfs(5);full[beta]=lifts;counts.append(len(lifts))
 return M,counts,full

def set_partitions(S):
 if not S:yield ();return
 first,*rest=S
 for size in range(len(rest)+1):
  for take in itertools.combinations(rest,size):
   block=(first,)+take;remaining=tuple(x for x in rest if x not in take)
   for tail in set_partitions(remaining):yield (block,)+tail

def nc(blocks):
 for X in blocks:
  if len(X)<2:continue
  gap={}
  for i,a in enumerate(X):
   z=(a+1)%6
   while z!=X[(i+1)%len(X)]:gap[z]=i;z=(z+1)%6
  for Y in blocks:
   if Y!=X and len({gap[y] for y in Y})>1:return False
 return True
PARTS=[p for p in set_partitions(tuple(range(6))) if nc(p)]
assert len(list(set_partitions(tuple(range(6)))))==203 and len(PARTS)==132
PAIRSETS=(((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2)))

def build_options():
 table=[]
 for r in R:
  colors=tuple(map(int,r));by_split=[]
  for pairs in PAIRSETS:
   group={c:i for i,pair in enumerate(pairs) for c in pair}
   swap={a:b for a,b in [*pairs,*[p[::-1] for p in pairs]]}
   options=set()
   for blocks in PARTS:
    if any(len({group[colors[x]] for x in block})!=1 for block in blocks):continue
    owner={x:b for b,block in enumerate(blocks) for x in block}
    if any(group[colors[i]]==group[colors[(i+1)%6]] and owner[i]!=owner[(i+1)%6] for i in range(6)):continue
    seen={colors};todo=[colors]
    while todo:
     state=todo.pop()
     for block in blocks:
      new=list(state)
      for x in block:new[x]=swap[state[x]]
      new=tuple(new)
      if new not in seen:seen.add(new);todo.append(new)
    orbit={RI[normalize(state)] for state in seen}
    options.add(sum(1<<x for x in orbit))
   assert options
   by_split.append(tuple(sorted(options)))
  table.append(by_split)
 return table
OPS=build_options()

def prune(mask):
 while True:
  removed=0
  for i in members(mask):
   if any(not any((orbit|mask)==mask for orbit in opts) for opts in OPS[i]):removed|=1<<i
  if not removed:return mask
  mask &= ~removed

def check_record(record):
 kind,pair=record['kind'],record['pair']
 q=next(q for q in QUERIES if q[0]==record['query'])
 assert list(q[1])==record['collar'] and q[2]==record['target']
 V,E,D,faces=make_shell(kind,pair,q[1])
 assert V==record['vertices'] and [list(e) for e in E]==record['edges'] and D==record['interfaces']
 M,counts,lifts=shell_colours(V,E,D)
 assert M==record['matrix'] and counts==record['shell_lift_counts']
 tau=q[2]
 # Positive control: literal shell plus ANY two disks with all proper C6
 # boundary rows yields the all-ten relation. The cycle C6 realizes this support.
 assert prune(ALL)==ALL
 covered=0
 for row in M:
  for m in row:covered|=m
 assert covered==1023
 # Dual enumeration: intersections of allowed LEFT neighbours of right rows.
 col=[sum(1<<a for a in range(31) if M[a][b]&~tau==0) for b in range(31)]
 domains={ALL}
 for nb in reversed(col):
  additions={x&nb for x in domains};domains.update(additions)
 rects=record['rectangles']
 index={row[0]:row for row in rects}
 assert len(index)==len(rects)==record['intersections']
 assert set(index)==domains
 cache={};masks=Counter()
 for aa in domains:
  bb=sum(1<<b for b in range(31) if (aa|col[b])==col[b])
  if aa not in cache:cache[aa]=prune(aa)
  if bb not in cache:cache[bb]=prune(bb)
  ap,bp=cache[aa],cache[bb]
  possible=0
  for a in members(ap):
   for b in members(bp):possible|=M[a][b]
  expected=[aa,bb,ap,bp,possible,tau & ~possible]
  assert expected==index[aa] and expected[-1]!=0
  masks[possible]+=1
 assert record['excluded'] and not record['incomplete']
 packed=json.dumps({'vertices':V,'interfaces':D,'fibres_by_B':lifts},sort_keys=True,separators=(',',':')).encode()
 return dict(kind=kind,pair=pair,query=q[0],target=tau,rectangles=len(domains),
             output_masks=dict(masks),shell_full_lifts=sum(counts),
             full_lifts_sha256=hashlib.sha256(packed).hexdigest()),packed

def disk_support(extra_vertices,extra_edges):
 # Independent actual disk positive controls, all colorings of a small graph.
 V=list(range(6+extra_vertices));E={tuple(sorted((i,(i+1)%6))) for i in range(6)}
 E|={tuple(sorted(x)) for x in extra_edges};adj=[[] for _ in V]
 for a,b in E:adj[max(a,b)].append(min(a,b))
 colors=[-1]*len(V);S=set()
 def dfs(i):
  if i==len(V):S.add(RI[normalize(colors[:6])]);return
  for c in range(4):
   if all(colors[j]!=c for j in adj[i]):colors[i]=c;dfs(i+1)
  colors[i]=-1
 dfs(0);return sum(1<<s for s in S)

def controls():
 examples=[('cycle',0,[]),('wheel',1,[(6,i) for i in range(6)]),
           ('fan',0,[(0,2),(0,3),(0,4)]),('triangle',0,[(0,2),(2,4),(4,0)]),
           ('split_quad',0,[(0,3)]),('split_triangle',0,[(0,2)]),
           ('stacked_fan',1,[(0,2),(0,3),(0,4),(6,0),(6,1),(6,2)])]
 results={}
 for name,n,E in examples:
  S=disk_support(n,E);assert S and prune(S)==S;results[name]=S.bit_count()
 # Every actual support is closed; damaged deleting options must violate a control.
 bad=copy.deepcopy(OPS);bad[0][0]=()
 assert all(OPS[i][s] for i in range(31) for s in range(3)) and not bad[0][0]
 return results

def run(kind,pair):
 start=time.monotonic();path=ROOT/f'twohole_{kind}_{pair}.json'
 data=json.loads(path.read_text());assert data['rows']==R
 reports=[];full=[]
 for record in data['records']:
  report,packed=check_record(record);reports.append(report);full.append(packed.decode())
  print('VERIFIED',kind,pair,record['query'],report['rectangles'],round(time.monotonic()-start,2),flush=True)
 assert [r['query'] for r in reports]==[q[0] for q in QUERIES]
 gz=ROOT/f'independent_full_lifts_{kind}_{pair}.jsonl.gz'
 with gz.open('wb') as f:
  with gzip.GzipFile(filename='',fileobj=f,mode='wb',mtime=0) as z:z.write(('\n'.join(full)+'\n').encode())
 out={'kind':kind,'pair':pair,'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
      'actual_disk_positive_controls':controls(),'records':reports,
      'full_lift_archive_sha256':hashlib.sha256(gz.read_bytes()).hexdigest(),
      'status':'PASS','scope':'independent finite kernel/rectangle/Kempe verification; source-cover proof still requires review'}
 (ROOT/f'independent_{kind}_{pair}.json').write_text(json.dumps(out,indent=2))
if __name__=='__main__':
 if len(sys.argv)>1:run(sys.argv[1],int(sys.argv[2]))
 else:
  for kind in ('PINCH','BRIDGE'):
   for pair in range(4):run(kind,pair)
