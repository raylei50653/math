#!/usr/bin/env python3
"""Independent boundary-preserving whole-cap isomorphism reconstruction."""
import collections,json,hashlib,itertools,argparse,copy
from pathlib import Path
from analyze_caps import inspect,edge
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
NEW='audits/2026-10-23-941-gamma8-nonempty-k-stars-6b09cd4/explore.json'
OLD='audits/2026-10-23-941-gamma8-chi-seven-6b09cd4/certificate.json'
def read(name):return json.loads((HERE/'frozen'/name).read_text())
def require(ok,msg):
 if not ok:raise ValueError(msg)
def isomorphism(new,old):
 A=new['vertices'];B=old['inner']+old['boundary'];ea=set(map(tuple,new['edges']));eb={edge(*e) for e in old['edges']}
 aa={v:{b if a==v else a for a,b in ea if v in (a,b)} for v in A};ab={v:{b if a==v else a for a,b in eb if v in (a,b)} for v in B}
 newbd=new['boundary'];oldbd=old['boundary'];interior=[v for v in A if v not in newbd]
 for rev in [False,True]:
  order=oldbd[::-1] if rev else oldbd[:]
  for shift in range(6):
   dest=order[shift:]+order[:shift];mp=dict(zip(newbd,dest))
   def rec():
    if len(mp)==len(A):
     return dict(mp) if {edge(mp[a],mp[b]) for a,b in ea}==eb else None
    options=[]
    for v in interior:
     if v in mp:continue
     can=[w for w in old['inner'] if w not in mp.values() and len(aa[v])==len(ab[w]) and all((z in aa[v])==(mz in ab[w]) for z,mz in mp.items())]
     if not can:return None
     options.append((len(can),v,can))
    _,v,can=min(options)
    for w in can:
     mp[v]=w;got=rec()
     if got:return got
     del mp[v]
    return None
   got=rec()
   if got:
    require({tuple(sorted(got[v] for v in f)) for f in new['faces']}=={tuple(sorted(f)) for f in old['faces']},'face bijection')
    return got
 return None
def side_obstruction(row):
 co=dict(r=1,T=0,s=1,x=0,h=1,W=3,e=1,d=0,tau=3,zeta=2,m=2,n=3,u=1,v=3,p_d=2,p_x=2,U=0,omega=int(row['omega_type'][-1]))
 K={'d','x','zeta','p_d','p_x','U','omega'}
 psi={v:(c^2 if v in K else c) for v,c in co.items()}
 es={tuple(e) for e in row['edges']};vertices=set().union(*map(set,es));adj={v:set() for v in vertices if psi[v] in {1,2}}
 for a,b in es:
  if a in adj and b in adj:adj[a].add(b);adj[b].add(a)
 C={'r','d','e','U'};E={'s','x','h'}
 unseen=set(adj)
 while unseen:
  start=min(unseen);seen={start};todo=[start];unseen.remove(start)
  while todo:
   for w in adj[todo.pop()]&unseen:unseen.remove(w);seen.add(w);todo.append(w)
  if seen&C and seen&E:return sorted(seen)
 return None
def reconstruct():
 rows=read(NEW);caps=read(OLD)['caps'];out=[]
 for i,r in enumerate(rows):
  obstruction=side_obstruction(r)
  if obstruction is not None:
   out.append(dict(row=i,kind='forbidden_common_C_E_component',component=obstruction));continue
  cap=inspect(r)
  if cap['status']!='disk':
   require(r['omega_type']=='K2' and edge('x','p_d') in set(map(tuple,r['edges'])),'uncovered non-disk star join')
   out.append(dict(row=i,kind='forbidden_d_x_exterior_common_neighbor',witness='p_d'));continue
  match=None
  for old in caps:
   mp=isomorphism(cap,old)
   if mp:match=dict(row=i,kind='old_cap',old_cap=old['id'],mapping=mp,boundary=cap['boundary']);break
  require(match is not None,'new cap not covered '+str(i));out.append(match)
 return out
def custody():
 for r in json.loads((HERE/'CAP_TRANSFER_INPUTS.json').read_text()):
  for p in [HERE/r['snapshot'],ROOT/r['path']]:
   raw=p.read_bytes();require(len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256'],'transfer input drift '+str(p))
def verify(cert,expected):
 require(cert['schema']=='941-nonempty-k-cap-transfer-v1','schema')
 require(cert['entries']==expected,'literal complete-cap transfer')
 require(cert['authority']==dict(source_realizability='not triggered',finite_control='triggered and holds',general_wrong_side='OPEN',all_eleven_types='OPEN',one_candidate_for_all_four_rows=True),'authority')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--produce',action='store_true');ap.add_argument('--negative',action='store_true');ap.add_argument('--certificate',type=Path,default=HERE/'cap-transfer-certificate.json');a=ap.parse_args();custody();out=reconstruct()
 cert=dict(schema='941-nonempty-k-cap-transfer-v1',entries=out,authority=dict(source_realizability='not triggered',finite_control='triggered and holds',general_wrong_side='OPEN',all_eleven_types='OPEN',one_candidate_for_all_four_rows=True))
 if a.produce:
  with a.certificate.open('x') as f:json.dump(cert,f,sort_keys=True,indent=2);f.write('\n')
 got=json.loads(a.certificate.read_text());verify(got,out);negative=[]
 if a.negative:
  for label,fn in [('omit_source_row',lambda x:x['entries'].pop()),('wrong_old_cap',lambda x:x['entries'][0].update(old_cap=-1)),('break_vertex_bijection',lambda x:x['entries'][0]['mapping'].update(T='not_a_vertex')),('claim_source',lambda x:x['authority'].update(source_realizability='triggered and holds')),('independent_row_candidates',lambda x:x['authority'].update(one_candidate_for_all_four_rows=False))]:
   bad=copy.deepcopy(got);fn(bad)
   try:verify(bad,out)
   except ValueError:negative.append(label)
   else:raise ValueError('negative unexpectedly accepted '+label)
 print(json.dumps(dict(status='PASS',rows=len(out),kinds=dict(collections.Counter(r['kind'] for r in out)),old_caps=sorted({r['old_cap'] for r in out if r['kind']=='old_cap'}),negative_rejected=negative),sort_keys=True))
if __name__=='__main__':main()
