#!/usr/bin/env python3
"""Read-only reconstruction from original ten-point edges and full cyclic stars."""
import argparse,copy,hashlib,itertools,json,random
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BASE='6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'
CELLS='audits/2026-10-23-941-gamma8-cells-6b09cd4/certificate.json'
def require(ok,msg):
 if not ok:raise ValueError(msg)
def edge(a,b):return tuple(sorted((a,b)))
def load(path):return json.loads(path.read_text())
def custody():
 m=load(HERE/'INPUTS.json');require(m['base']==BASE,'BASE')
 for row in m['authority']:
  for p in [HERE/row['snapshot'],ROOT/row['path']]:
   raw=p.read_bytes();require((len(raw),hashlib.sha256(raw).hexdigest())==(row['bytes'],row['sha256']),'authority drift '+str(p))
 extra=load(HERE/'INPUTS-CUSTODY.json')
 raw=(HERE/extra['snapshot']).read_bytes();require(hashlib.sha256(raw).hexdigest()==extra['sha256'],'frozen final-manifest drift')
 manifest=json.loads(raw);n=0;route={x['path']:x for x in load(HERE/'ROUTING-ENTRY.json')['routing']}
 for row in manifest['entries']:
  p=HERE/route[row['path']]['snapshot'] if row['path'] in route else ROOT/row['path']
  b=p.read_bytes();require((len(b),hashlib.sha256(b).hexdigest())==(row['bytes'],row['sha256']),'round3 retained artifact drift '+row['path']);n+=1
 return dict(direct_authorities=len(m['authority']),retained_round3_artifacts=n,routing_snapshots=len(route),drift=0)
def cycle_edges(center,link):
 return {edge(center,v) for v in link}|{edge(a,b) for a,b in zip(link,link[1:]+link[:1])}
def anchored(pool,anchor):
 for n in range(2,len(pool)+1):
  for chosen in itertools.combinations(pool,n):
   for rest in itertools.permutations(chosen):yield [*anchor,*rest]
def setup(c,cell,alias):
 image=lambda z:'d' if alias and z=='U' else z
 co={image(k):v for k,v in dict(c['original_colors'],a=3,b=3,y=1,p_d=2,p_x=2,U=0,omega=3).items()}
 lab={image(k):v for k,v in dict(c['original_component_labels'],a='N',b='N',y='N',p_d='K',p_x='K',U='K',omega='N').items()}
 old={edge(*e) for e in cell['edges']}
 es=old|{edge(*e) for e in [('T','a'),('T','y'),('T','b'),('r','a'),('a','y'),('y','b'),('b','s'),('d','p_d'),('x','p_x')]}
 full={'T':['r','tau','s','b','y','a']}
 for v in ['tau','zeta']:full[v]=[b if a==v else a for a,b in old if v in (a,b)]
 return image,co,lab,old,es,full
def valid(es,co,lab,old,full,core):
 adj={v:set() for v in co};orig={'r','T','s','x','h','W','e','d','tau','zeta'}
 for a,b in es:
  if a==b or co[a]==co[b]:return False
  if {a,b}<=orig and edge(a,b) not in old:return False
  if {a,b}&{'tau','zeta'} and not {a,b}<=orig:return False
  if {co[a],co[b]}<={0,2} and lab[a]!=lab[b]:return False
  if {co[a],co[b]}<={1,3} and lab[a]!=lab[b]:return False
  if lab[a]!='K' and lab[b]!='K' and ((lab[a] in {'M','N'})!=(lab[b] in {'M','N'})):return False
  adj[a].add(b);adj[b].add(a)
 for center,lk in full.items():
  if set(lk)!=adj[center] or len(lk)!=len(set(lk)):return False
  if center in {'tau','zeta'}:continue
  if len(lk)<5:return False
  if any(edge(a,b) not in es for a,b in zip(lk,lk[1:]+lk[:1])):return False
  if any(edge(lk[i],lk[j]) in es for i in range(len(lk)) for j in range(i+1,len(lk)) if j-i not in {1,len(lk)-1}):return False
 for a,b in itertools.combinations(co,2):
  if co[a]==co[b] and len(adj[a]&adj[b])>2:return False
 ext={'a','b','y','p_d','p_x','U','omega'}
 forbidden=[('r','s'),('d','x')]+([('T','x')] if core in {'L','O'} else [])+([('T','d')] if core in {'R','O'} else [])
 if any(adj[a]&adj[b]&ext for a,b in forbidden):return False
 psi={v:(co[v]^2 if lab[v]=='K' else co[v]) for v in co}
 unseen={v for v in co if psi[v] in {1,2}}
 while unseen:
  start=min(unseen);unseen.remove(start);seen={start};todo=[start]
  while todo:
   v=todo.pop()
   for w in adj[v]&unseen:unseen.remove(w);seen.add(w);todo.append(w)
  if seen&{'r','d','e','U'} and seen&{'s','x','h'}:return False
 return True
def reconstruct(seed):
 c=load(HERE/'frozen'/CELLS);cells=[x for x in c['candidates'] if x['classification']=='local_necessary_type'];random.Random(seed).shuffle(cells)
 out=[]
 for cell in cells:
  for alias in [False,True]:
   image,co,lab,old,es,full=setup(c,cell,alias);pool=sorted({image(x) for x in ['d','x','U','p_d','p_x','omega']});partial=[];complete=[]
   for yl in anchored(pool,['a','T','b']):
    ey=es|cycle_edges('y',yl);fy=dict(full,y=yl)
    if not valid(ey,co,lab,old,fy,cell['core']):continue
    singles={}
    for v,anchor in [('a','r'),('b','s')]:
     singles[v]=[]
     for lk in anchored(pool,[anchor,'T','y']):
      if valid(ey|cycle_edges(v,lk),co,lab,old,dict(fy,**{v:lk}),cell['core']):singles[v].append(lk)
    for al,bl in itertools.product(singles['a'],singles['b']):
     ex=ey|cycle_edges('a',al)|cycle_edges('b',bl);fx=dict(fy,a=al,b=bl)
     if not valid(ex,co,lab,old,fx,cell['core']):continue
     row=dict(core=cell['core'],y=yl,a=al,b=bl);partial.append(row)
     op=sorted({image(x) for x in ['r','s','y','d','x','U','p_d','p_x']})
     # A source omega has exactly one full cyclic star, modulo global reversal.
     for degree in range(5,len(op)+1):
      for chosen in itertools.combinations(op,degree):
       for rest in itertools.permutations(chosen[1:]):
        ol=[chosen[0],*rest]
        if ol[1]>ol[-1]:continue
        if valid(ex|cycle_edges('omega',ol),co,lab,old,dict(fx,omega=ol),cell['core']):complete.append(dict(row,omega=ol))
   out.append(dict(cell=cell['id'],core=cell['core'],U_equals_d=alias,partial=partial,complete=complete))
 return sorted(out,key=lambda x:(x['cell'],x['U_equals_d']))
def owner_controls():
 # Independent subset capacity reconstruction of the paper N1 argument.
 pool=['a','b','d','x','U','p_d','p_x'];large=[]
 for n in range(5,len(pool)+1):
  for chosen in itertools.combinations(pool,n):
   s=set(chosen)
   if len(s&{'a','b'})>1 or len(s&{'d','x'})>1:continue
   large.append(s)
 require(len(large)==4 and all(len(s)==5 and {'U','p_d','p_x'}<=s for s in large),'N1 full-star capacity')
 for s in large:
  for p in ['p_d','p_x']:
   v=next(iter(s&{'a','b'}));require({v,'U',p}<=s,'N1 third common neighbor')
 r02_pool=['r','s','a','y','b']
 r02_sets=[set(t) for n in range(len(r02_pool)+1) for t in itertools.combinations(r02_pool,n) if not {'r','s'}<=set(t)]
 max_degree=max(map(len,r02_sets));require(max_degree<5,'new R02 minimum degree contradiction')
 # Distinct N13 cannot use an N edge; T full star excludes its M contact.
 new_13_J_minus_K_neighbors=set(['M','N'])-{'M','N'}
 require(not new_13_J_minus_K_neighbors,'new13 component could join R')
 return dict(R02_max_neighbors=max_degree,R13_new_component_contacts=len(new_13_J_minus_K_neighbors),N1_degree_five_sets=len(large),N1_three_common_neighbor_obstructions=2*len(large))
def verify(c,rows):
 scope=load(HERE/'CERTIFICATE-SCOPE.json')
 require(scope==dict(schema='941-empty-resource-certificate-scope-v1',elimination_domain='M2_empty_D6_Z6_arbitrary_spectators',K_star_envelope_additional_premise='X7_with_X_minus_Z_equal_chi',frame13='complete_actual_B14_vertices_with_original_phi_color_1_or_3_after_literal_aliases',K_star_envelopes_are_complete_necessary_neighbor_sets=True,K_cyclic_stars='OPEN'),'K envelope coverage scope')
 require(c['schema']=='941-empty-resource-stars-v1' and c['base']==BASE,'certificate contract')
 require(c['eliminated_owners']==['R02_outside_M','R13_outside_N','N1','N3'] and c['remaining_owners']==['K0','K2'],'owner coverage')
 require(c['contract']==dict(D=6,M2_empty=True,resource_size=6,extra_resource='omega',same_original_source=True,complete_original_stars=True,U_is_boundary_exception=True),'source contract')
 require(c['boundaries']==dict(source_realizability='not triggered',finite_control='triggered and holds',empty_M2_X7='OPEN',all_eleven_types='OPEN',general_wrong_side='OPEN',common_k=23,D_at_least_8='unchanged'),'authority boundary')
 patterns=c['partial_N3_star_patterns'];require(len(patterns)==5,'paper pattern count')
 fields=['core','y','a','b']
 expected=[{k:p[k] for k in fields} for p in patterns]
 for r in rows:
  want=[] if r['U_equals_d'] else [p for p in expected if p['core']==r['core']]
  require(sorted(r['partial'],key=lambda x:json.dumps(x,sort_keys=True))==sorted(want,key=lambda x:json.dumps(x,sort_keys=True)),'partial source-star coverage '+r['cell'])
  require(r['complete']==[],'N3 complete star survived')
 require(len(rows)==22,'eleven core-ear types and two U identities')
 require(c['K_star_envelopes']==dict(K0=['r','s','a','y','b','p_d','p_x','e','h','W','frame13','chi_if_color3'],K2=['r','s','a','y','b','d','x','U','e','h','W','frame13','chi_if_color3']),'complete K envelopes')
 return dict(source_star_cases=len(rows),partial_N3_stars=sum(len(r['partial']) for r in rows),complete_N3_stars=0,owners_remaining=['K0','K2'],source_realizability='not triggered')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--seed',type=int,default=0);ap.add_argument('--negative',action='store_true');ap.add_argument('--certificate',type=Path,default=HERE/'certificate.json');args=ap.parse_args()
 frozen=custody();c=load(args.certificate);rows=reconstruct(args.seed);result=verify(c,rows);controls=owner_controls()
 if args.negative:
  mutations=[('drop_N3_pattern',lambda x:x['partial_N3_star_patterns'].pop()),('invent_R02_owner',lambda x:x['remaining_owners'].append('R02')),('invent_complete_source',lambda x:x['boundaries'].update(source_realizability='triggered and holds')),('promote_general_wrong_side',lambda x:x['boundaries'].update(general_wrong_side='excluded')),('wrong_K0_complete_envelope',lambda x:x['K_star_envelopes']['K0'].append('T')),('invent_U_complete_star',lambda x:x['contract'].update(U_is_boundary_exception=False))]
  passed=[]
  for label,fn in mutations:
   bad=copy.deepcopy(c);fn(bad)
   try:verify(bad,rows)
   except ValueError:passed.append(label)
   else:raise ValueError('negative accepted '+label)
  result['negative_rejected']=passed
 print(json.dumps(dict(status='PASS',seed=args.seed,custody=frozen,verification=result,owner_controls=controls),ensure_ascii=False,sort_keys=True,indent=2))
if __name__=='__main__':main()
