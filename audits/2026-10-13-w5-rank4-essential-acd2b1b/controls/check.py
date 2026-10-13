import importlib.util,itertools,json,hashlib,sys,time,gzip,argparse,random
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
p=ROOT/'frozen/audits/2026-10-13-w5-rank3-essential-45bc1c3/controls/check.py'
s=importlib.util.spec_from_file_location('prior',p); old=importlib.util.module_from_spec(s); s.loader.exec_module(old)
ST=old.STEPS

def words(r,d):
 s=r-3
 for w in itertools.product(*['OBUD' if i<2 else 'BUD' for i in range(s)]):
  if sum(ST[x][0] for x in w)==5-d and sum(ST[x][1] for x in w)==3: yield ''.join(w)

def make(w,d,flip=0):
 s=len(w);r=s+3;n=10+r;b=u=0;qS=n-3;q0=n-2;q1=n-1
 faces=[[0,4,3,2,1]]
 for i,l in enumerate(w):
  db,du=ST[l];x=10+i;y=10+(i+1)%s
  if db: faces.append([b%5,(b+1)%5,x])
  if du: faces.append([5+(u+1)%5,5+u%5,x])
  b+=db;u+=du
  if i:
   faces += [[b%5,y,x],[5+u%5,x,y]]
  else:
   faces += [[b%5,qS,x]]
   if d: faces += [[b%5,(b+1)%5,qS]]
   faces += [[(b+d)%5,y,qS],[5+u%5,x,q0],[5+(u+1)%5,5+u%5,q0],[5+(u+1)%5,q0,q1],[5+(u+2)%5,5+(u+1)%5,q1],[5+(u+2)%5,q1,y],[x,qS,q0],[qS,q1,q0],[y,q1,qS]]
   b+=d;u+=2
 assert b==u==5
 faces += [list(range(5,10))]
 if flip:
  def tf(f): return [v+5 if v<5 else v-5 if v<10 else v for v in reversed(f)]
  faces=[tf(faces[-1])]+[tf(f) for f in faces[1:-1]]+[tf(faces[0])]
 edges,rotation=old.embedding(n,faces)
 wfaces=faces[:-1]+[[5+i,5+(i+1)%5,n] for i in range(5)]
 wedges,wrotation=old.embedding(n+1,wfaces)
 deg=[sum(v in e for e in wedges) for v in range(n+1)]
 df=[sum(v in e and min(e)>=10 for e in wedges) for v in range(10,n)]
 assert all(deg[v]>=5 for v in range(10,n))
 assert len([e for e in edges if min(e)>=10])-r+1==4
 assert sum(all(v>=10 for v in f) for f in faces[1:-1])==3
 assert sorted(df)==[2]*(r-5)+[3]*4+[4]
 assert sum(deg[10:n])==4*r+13
 return {'vertices':list(range(n)),'key':f'{r}:{d}:{flip}:{w}','r':r,'edges':edges,'faces':faces,'rotation':rotation,'wheel_edges':wedges,'wheel_faces':wfaces,'wheel_rotation':wrotation,'degree_G':deg,'degree_F':df}


BASE='acd2b1beea6c909edade565a00eeeeac05d2b3a7'
def configure(seed):
 if seed is None:return
 def lifts(n,edges,beta):
  adj=[[] for _ in range(n)]
  for x,y in edges:adj[x].append(y);adj[y].append(x)
  rng=random.Random(seed);priority=list(range(n));rng.shuffle(priority);palette=list(range(4));rng.shuffle(palette)
  colors=list(beta)+[-1]*(n-5);answer=[]
  def visit(left):
   if not left:answer.append(''.join(map(str,colors)));return
   choices=[]
   for v in left:
    mask=15
    for w in adj[v]:
     if colors[w]>=0:mask &= ~(1<<colors[w])
    if not mask:return
    choices.append((mask.bit_count(),-len(adj[v]),priority[v],v,mask))
   _,_,_,v,mask=min(choices);tail=tuple(w for w in left if w!=v)
   for color in palette:
    if mask & (1<<color):colors[v]=color;visit(tail)
   colors[v]=-1
  visit(tuple(range(5,n)))
  return sorted(answer)
 old.lifts=lifts

def graph(r,d,f,w):
 g=make(w,d,f);n=len(g['vertices'])
 g.update(B=list(range(5)),U=list(range(5,10)),private=list(range(10,n)),counts={'r':r,'c':1,'rho':4,'t_P':3,'a':0,'p':0,'M':0},ownership={'outer_face':0,'empty_U_face':len(g['faces'])-1,'centre_after_restoration':n,'pin_map':list(range(10)),'backbone_order':list(range(10,n-3)),'ear_x':10,'ear_y':11,'short_apex':n-3,'long_vertices':[n-2,n-1],'short_ring':'U' if f else 'B','short_increment':d},source_degree_flags={'B_ge4':all(g['degree_G'][x]>=4 for x in range(5)),'U_ge5':all(g['degree_G'][x]>=5 for x in range(5,10))},status='triggered and holds: necessary template; minimum-source identity not triggered')
 return g

def header():
 return {'type':'header','base':BASE,'beta_order':old.BETAS,'tau_order':old.TAUS,'domain':'r8..13; d0/1; short ring B/U; s=r-3; tips O/B/U/D, others B/U/D; totals(5-d,3)','claim':'essential private rho=4 excluded by complete source classification and full Sigma=1023; not a smaller representative'}

def run(args):
 configure(args.seed);stats={'templates':0,'by_r':{},'masks':{},'cells':0,'empty_cells':0,'A_full_lifts':0,'G_full_lifts':0,'source_degree_flags':{}};digest=hashlib.sha256()
 cert=ROOT/'controls/certificate.jsonl.gz';summary=ROOT/'controls/summary.json';start=time.time()
 if args.write:
  assert not cert.exists() and not summary.exists(),'refuse overwrite'
  raw=cert.open('xb');stream=gzip.GzipFile(filename='',fileobj=raw,mode='wb',mtime=0)
 else:raw=None;stream=gzip.open(cert,'rb')
 def accept(g):
  bs=old.encoded(g);digest.update(bs)
  if args.write:stream.write(bs)
  else:assert stream.readline()==bs,'certificate mismatch: '+str(g.get('key','header'))
 try:
  accept(header())
  for r in range(8,14):
   count=0
   for d in (0,1):
    for f in (0,1):
     for w in sorted(words(r,d)):
      g=old.fill(graph(r,d,f,w));assert g['Sigma']==1023;accept(g);count+=1
      stats['masks'][g['Sigma']]=stats['masks'].get(g['Sigma'],0)+1
      stats['cells']+=10240;stats['empty_cells']+=sum(not c for row in g['rows'] for c in row['cells'])
      stats['A_full_lifts']+=sum(len(c) for row in g['rows'] for c in row['cells']);stats['G_full_lifts']+=sum(len(row['wheel_full_lifts']) for row in g['rows'])
      flag=str(g['source_degree_flags']);stats['source_degree_flags'][flag]=stats['source_degree_flags'].get(flag,0)+1
   stats['templates']+=count;stats['by_r'][r]=count;print(json.dumps({'r':r,'templates':stats['templates'],'elapsed':time.time()-start}),flush=True)
  if not args.write:assert not stream.read(1),'extra record'
 finally:
  stream.close()
  if raw:raw.close()
 assert stats['templates']==2872 and stats['by_r']=={8:96,9:408,10:840,11:912,12:504,13:112}
 stats['mathematical_sha256']=digest.hexdigest();stats=json.loads(json.dumps(stats))
 if args.write:
  with summary.open('x') as out:json.dump(stats,out,indent=2,sort_keys=True);out.write('\n')
 else:assert json.loads(summary.read_text())==stats,'summary mismatch'
 print(json.dumps(stats,sort_keys=True),flush=True)

if __name__=='__main__':
 parser=argparse.ArgumentParser();m=parser.add_mutually_exclusive_group(required=True);m.add_argument('--write',action='store_true');m.add_argument('--check',action='store_true');parser.add_argument('--seed',type=int);run(parser.parse_args())
