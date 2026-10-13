import importlib.util,sys,time,json,gzip,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent

def imp(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
i=imp('ind',ROOT/'frozen/audits/2026-10-13-w5-rank3-essential-45bc1c3/independent/check.py')

def domains():
 answer=set()
 def visit(w,s,b,u,d):
  if len(w)==s:
   if b==u==0:
    for f in (0,1):answer.add((s+3,d,f,w))
   return
  for l,(db,du) in i.INCREMENT.items():
   if len(w)>=2 and db==du==0:continue
   if db<=b and du<=u:visit(w+l,s,b-db,u-du,d)
 for r in range(8,14):
  for d in (0,1):visit('',r-3,5-d,3,d)
 return answer

def neighbours(w,d,f):
 s=len(w);n=s+13;qs=n-3;q0=n-2;q1=n-1;ed=set();b=u=0
 def add(x,y):
  if f:x=x+5 if x<5 else x-5 if x<10 else x;y=y+5 if y<5 else y-5 if y<10 else y
  assert x!=y;ed.add(tuple(sorted((x,y))))
 for off in (0,5):
  for z in range(5):add(off+z,off+(z+1)%5)
 for z,l in enumerate(w):
  db,du=i.INCREMENT[l];x=10+z
  for y in {b%5,(b+db)%5,5+u%5,5+(u+du)%5}:add(x,y)
  b+=db;u+=du
  if z==0:
   for y in {b%5,(b+d)%5}:add(qs,y)
   for y in {5+u%5,5+(u+1)%5}:add(q0,y)
   for y in {5+(u+1)%5,5+(u+2)%5}:add(q1,y)
   for a,z1 in [(10,qs),(10,q0),(qs,q0),(qs,q1),(q0,q1),(11,qs),(11,q1)]:add(a,z1)
   b+=d;u+=2
  else:add(x,10+(z+1)%s)
 assert b==u==5
 return n,sorted(ed)


DOMAIN=domains()

def verify(g):
 r,d,f,w=g['key'].split(':');r,d,f=int(r),int(d),int(f)
 assert (r,d,f,w) in DOMAIN,'parameter outside domain'
 n,ed=neighbours(w,d,f);assert n-10==r==g['r']
 assert g['vertices']==list(range(n));assert g['B']==list(range(5));assert g['U']==list(range(5,10));assert g['private']==list(range(10,n))
 assert g['edges']==[list(e) for e in ed],'original edge mismatch'
 assert i.canonical_cycle(g['faces'][0])==i.canonical_cycle([0,4,3,2,1]) and i.canonical_cycle(g['faces'][-1])==i.canonical_cycle(list(range(5,10)))
 assert all(len(face)==3 for face in g['faces'][1:-1]);i.rotation_faces(n,ed,g['faces'],g['rotation'])
 wed=sorted(ed+[(u,n) for u in range(5,10)]);assert g['wheel_edges']==[list(e) for e in wed]
 i.rotation_faces(n+1,wed,g['wheel_faces'],g['wheel_rotation'])
 assert i.Counter(map(i.canonical_cycle,g['wheel_faces']))==i.Counter(map(i.canonical_cycle,g['faces'][:-1]+[[5+j,5+(j+1)%5,n] for j in range(5)]))
 private=[e for e in ed if min(e)>=10];df=[sum(v in e for e in private) for v in range(10,n)];dg=[sum(v in e for e in wed) for v in range(n+1)]
 assert g['degree_F']==df and g['degree_G']==dg
 assert all(dg[v]>=5 for v in range(10,n));assert sorted(df)==[2]*(r-5)+[3]*4+[4];assert sum(dg[10:n])==4*r+13
 assert len(private)-r+1==4 and len(ed)==3*r+20
 assert sum(all(v>=10 for v in face) for face in g['faces'][1:-1])==3
 assert not any(x<5<=y<10 for x,y in ed)
 assert g['counts']=={'r':r,'c':1,'rho':4,'t_P':3,'a':0,'p':0,'M':0}
 assert g['ownership']=={'outer_face':0,'empty_U_face':len(g['faces'])-1,'centre_after_restoration':n,'pin_map':list(range(10)),'backbone_order':list(range(10,n-3)),'ear_x':10,'ear_y':11,'short_apex':n-3,'long_vertices':[n-2,n-1],'short_ring':'U' if f else 'B','short_increment':d}
 assert g['source_degree_flags']=={'B_ge4':all(dg[x]>=4 for x in range(5)),'U_ge5':all(dg[x]>=5 for x in range(5,10))}
 for v in range(10,n):
  for off in (0,5):
   ns=[x-off for x in range(off,off+5) if tuple(sorted((v,x))) in ed]
   assert len(ns)<=2
   if len(ns)==2:assert (ns[1]-ns[0])%5 in (1,4)
 counts=i.verify_rows(g,n,ed);assert g['Sigma']==1023
 return counts

def coverage(seen):
 assert seen==DOMAIN,'missing or extra template'

def run():
 keys=domains();assert len(keys)==2872;seen=set();stats={'templates':0,'cells':0,'empty_cells':0,'A_full_lifts':0,'G_full_lifts':0};start=time.time();h=hashlib.sha256()
 with gzip.open(ROOT/'controls/certificate.jsonl.gz','rb') as cert:
  raw=cert.readline();h.update(raw);head=json.loads(raw)
  assert head['type']=='header' and head['base']=='acd2b1beea6c909edade565a00eeeeac05d2b3a7'
  assert head['beta_order']==[list(b) for b in i.BETAS] and head['tau_order']==[list(t) for t in i.TAUS]
  for raw in cert:
   h.update(raw);g=json.loads(raw);r,d,f,w=g['key'].split(':');key=(int(r),int(d),int(f),w)
   assert key not in seen;seen.add(key);counts=verify(g);stats['templates']+=1
   for k,v in counts.items():stats[k]+=v
   if stats['templates']%200==0:print(json.dumps({'checked':stats['templates'],'elapsed':time.time()-start}),flush=True)
 coverage(seen)
 summary=json.loads((ROOT/'controls/summary.json').read_text())
 for k,v in stats.items():assert summary[k]==v
 assert h.hexdigest()==summary['mathematical_sha256']
 stats['mathematical_sha256']=h.hexdigest();print(json.dumps(stats,sort_keys=True),flush=True)
if __name__=='__main__':run()
