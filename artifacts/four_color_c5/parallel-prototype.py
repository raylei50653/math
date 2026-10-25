import sys,time,random,statistics,json,heapq,multiprocessing
from concurrent.futures import ProcessPoolExecutor,ThreadPoolExecutor
sys.path.insert(0,'/home/ray/developer/ai/math/scripts')
from four_color_c5 import find_induced_c5
from four_color_lab import normalize_graph
from four_color_examples import random_triangulation

def pack(g):
 g=normalize_graph(g);vs=tuple(g['vertices']);idx={v:i for i,v in enumerate(vs)};adj=[0]*len(vs)
 for u,v in g['edges']:adj[idx[u]]|=1<<idx[v];adj[idx[v]]|=1<<idx[u]
 return vs,tuple(adj)

def endpoints(packed,endpoint_us):
 vs,adj=packed;n=len(vs);out=[]
 for u in endpoint_us:
  nu=adj[u];belowu=(1<<u)-1
  for v in range(u+1,n):
   if nu&(1<<v):continue
   nv=adj[v];centers=nu&nv&belowu
   if not centers:continue
   ys=nu&~nv
   while ys:
    bit=ys&-ys;ys^=bit;y=bit.bit_length()-1
    choices=centers&~adj[y]&((1<<y)-1)
    if not choices:continue
    firstx=(choices&-choices).bit_length()-1
    zs=adj[y]&nv&~nu&~((1<<(firstx+1))-1)
    while zs:
     bit=zs&-zs;zs^=bit;z=bit.bit_length()-1
     xs=choices&~adj[z]&((1<<z)-1)
     while xs:
      bit=xs&-xs;xs^=bit;x=bit.bit_length()-1
      out.append((x,u,y,z,v))
 out.sort()
 return out

def minimums(packed,starts):
 vs,adj=packed;out=[]
 for s in starts:
  ns=adj[s];after=~((1<<(s+1))-1);firsts=ns&after
  while firsts:
   bit=firsts&-firsts;firsts^=bit;a=bit.bit_length()-1;na=adj[a];aftera=~((1<<(a+1))-1)
   seconds=na&after&~ns
   while seconds:
    bit=seconds&-seconds;seconds^=bit;b=bit.bit_length()-1;nb=adj[b]
    thirds=nb&after&~(ns|na)
    while thirds:
     bit=thirds&-thirds;thirds^=bit;c=bit.bit_length()-1
     lasts=ns&adj[c]&aftera&~(na|nb)
     while lasts:
      bit=lasts&-lasts;lasts^=bit;d=bit.bit_length()-1
      out.append((s,a,b,c,d))
 return out

def run_serial(g,method):
 p=pack(g);rows=(endpoints if method=='endpoint' else minimums)(p,range(len(p[0])))
 return [tuple(p[0][v] for v in r) for r in rows]

def worker(job):
 method,p,starts=job
 return (endpoints if method=='endpoint' else minimums)(p,starts)

def run_parallel(g,method,pool,workers):
 p=pack(g);n=len(p[0]);jobs=[(method,p,tuple(range(i,n,workers))) for i in range(workers)]
 pieces=list(pool.map(worker,jobs,chunksize=1))
 return [tuple(p[0][v] for v in row) for row in heapq.merge(*pieces)]

def graph_worker(g):
 return find_induced_c5(g,10**9,10**9)['cycles']

def er(n,p,seed):
 r=random.Random(seed)
 return {'name':f'er_{n}_{p}_{seed}','vertices':list(range(n)),'edges':[[a,b] for a in range(n) for b in range(a+1,n) if r.random()<p]}

def measure(fn,reps=5):
 times=[];ans=None
 for _ in range(reps):
  t=time.perf_counter();ans=fn();times.append(time.perf_counter()-t)
 return {'median_s':statistics.median(times),'samples_s':times},ans

def main():
 # Complete n=5 family verifies the endpoint uniqueness and both frames.
 from itertools import combinations
 es=list(combinations(range(5),2))
 for mask in range(1<<len(es)):
  g={'vertices':list(range(5)),'edges':[e for i,e in enumerate(es) if mask>>i&1]}
  wanted=graph_worker(g)
  assert run_serial(g,'endpoint')==wanted
  assert run_serial(g,'minimum')==wanted
 print('n5 exact family passed',flush=True)
 graphs30=[random_triangulation(30,s) for s in range(100)]
 large=[er(160,.12,0),er(240,.07,1),er(400,.04,2)]
 results={}
 ctx=multiprocessing.get_context('spawn');workers=4
 # Startup test includes construction, transfer, and shutdown.
 def startup(g,method):
  with ProcessPoolExecutor(max_workers=workers,mp_context=ctx) as pool:
   return run_parallel(g,method,pool,workers)
 for g in [graphs30[8],large[0]]:
  row={};wanted=graph_worker(g)
  for method in ['endpoint','minimum']:
   row[method],actual=measure(lambda:startup(g,method),3);assert actual==wanted
  results['startup_'+g.get('name','n30')]=row
  print('STARTUP',g.get('name'),len(wanted),json.dumps(row),flush=True)
 with ProcessPoolExecutor(max_workers=workers,mp_context=ctx) as pool:
  # Force workers to start before reused-pool timing.
  list(pool.map(worker,[('minimum',pack(graphs30[0]),tuple(range(30)))]*workers))
  row={}
  row['serial_production'],wanted=measure(lambda:[graph_worker(g) for g in graphs30])
  row['parallel_across_graphs'],actual=measure(lambda:list(pool.map(graph_worker,graphs30,chunksize=5)));assert actual==wanted
  row['serial_endpoint'],actual=measure(lambda:[run_serial(g,'endpoint') for g in graphs30]);assert actual==wanted
  row['serial_minimum_core'],actual=measure(lambda:[run_serial(g,'minimum') for g in graphs30]);assert actual==wanted
  row['parallel_inside_each_minimum'],actual=measure(lambda:[run_parallel(g,'minimum',pool,workers) for g in graphs30],3);assert actual==wanted
  row['parallel_inside_each_endpoint'],actual=measure(lambda:[run_parallel(g,'endpoint',pool,workers) for g in graphs30],3);assert actual==wanted
  results['n30_100']=row;print('N30_BATCH',json.dumps(row),flush=True)
  for g in large:
   row={};name=g['name']
   row['production'],wanted=measure(lambda:graph_worker(g),3)
   for method in ['endpoint','minimum']:
    row['serial_'+method],actual=measure(lambda:run_serial(g,method),3);assert actual==wanted
    row['pool_'+method],actual=measure(lambda:run_parallel(g,method,pool,workers),3);assert actual==wanted
   row['cycles']=len(wanted);row['edges']=len(g['edges']);results[name]=row
   print('LARGE',name,json.dumps(row),flush=True)
 with ThreadPoolExecutor(max_workers=workers) as pool:
  g=large[0];r,actual=measure(lambda:run_parallel(g,'minimum',pool,workers),3);assert actual==graph_worker(g)
  results['threads_minimum_'+g['name']]=r
  print('THREADS',g['name'],json.dumps(r),flush=True)
 open('/tmp/c5_parallel_results.json','w').write(json.dumps(results,indent=2))
if __name__=='__main__':main()
