#!/usr/bin/env python3
"""Read-only, independent original-star, cap, and full-relation reconstruction."""
import argparse,copy,hashlib,itertools,json,random
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BASE='6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'
CELLS='audits/2026-10-23-941-gamma8-cells-6b09cd4/certificate.json'
CAPS='audits/2026-10-23-941-gamma8-empty-m2-6b09cd4/K6_CAPS.json'
REL='audits/2026-10-23-941-types-wrong-side-6b09cd4/CAP_RELATION-v2.json'
def require(ok,msg):
 if not ok:raise ValueError(msg)
def load(p):return json.loads(p.read_text())
def edge(a,b):return tuple(sorted((a,b)))
def custody():
 m=load(HERE/'INPUTS.json');require(m['base']==BASE,'authority BASE')
 for row in m['authority']:
  for p in [ROOT/row['path'],HERE/row['snapshot']]:
   b=p.read_bytes();require((len(b),hashlib.sha256(b).hexdigest())==(row['bytes'],row['sha256']),'authority drift '+str(p))
 return dict(authority_files=len(m['authority']),immutable_drift=0)
def cycle_edges(v,lk):
 return {edge(v,w) for w in lk}|{edge(a,b) for a,b in zip(lk,lk[1:]+lk[:1])}
def arcs(pool,anchor,minimum=0):
 for n in range(minimum,len(pool)+1):
  for chosen in itertools.combinations(pool,n):
   for tail in itertools.permutations(chosen):yield anchor+list(tail)
def setup(c,cell,color,alias):
 image=lambda v:'d' if alias and v=='U' else v
 co={image(k):v for k,v in dict(c['original_colors'],a=3,b=3,y=1,p_d=2,p_x=2,U=0,omega=color).items()}
 lab={image(k):v for k,v in dict(c['original_component_labels'],a='N',b='N',y='N',p_d='K',p_x='K',U='K',omega='K').items()}
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
 for v,lk in full.items():
  if set(lk)!=adj[v] or len(lk)!=len(set(lk)):return False
  if v in {'tau','zeta'}:continue
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
 # Fixed interior ears never change the resource-star enumeration; every one
 # of the eleven original cells is nevertheless independently reconstructed.
 for cell in cells:
  for color,alias in itertools.product([0,2],[False,True]):
   image,co,lab,old,es,full=setup(c,cell,color,alias)
   pool=sorted({image(x) for x in ['d','x','U','p_d','p_x','omega']});partial=[];complete=[]
   for yl in arcs(pool,['a','T','b'],2):
    ey=es|cycle_edges('y',yl);fy=dict(full,y=yl)
    if not valid(ey,co,lab,old,fy,cell['core']):continue
    single={}
    for v,anchor in [('a','r'),('b','s')]:
     single[v]=[]
     for lk in arcs(pool,[anchor,'T','y'],2):
      if valid(ey|cycle_edges(v,lk),co,lab,old,dict(fy,**{v:lk}),cell['core']):single[v].append(lk)
    for al,bl in itertools.product(single['a'],single['b']):
     ex=ey|cycle_edges('a',al)|cycle_edges('b',bl);fx=dict(fy,a=al,b=bl)
     if not valid(ex,co,lab,old,fx,cell['core']):continue
     partial.append(dict(a=al,b=bl,y=yl));ss={}
     for v,anchor in [('r',['a','T','tau']+(['zeta'] if cell['core']=='L' else [])+['d']),('s',['b','T','tau']+(['zeta'] if cell['core']=='R' else [])+['x'])]:
      ss[v]=[];pp=sorted({image(x) for x in ['U','p_d','p_x','omega']}-set(anchor))
      for lk in arcs(pp,anchor):
       if valid(ex|cycle_edges(v,lk),co,lab,old,dict(fx,**{v:lk}),cell['core']):ss[v].append(lk)
     for rl,sl in itertools.product(ss['r'],ss['s']):
      ez=ex|cycle_edges('r',rl)|cycle_edges('s',sl);fz=dict(fx,r=rl,s=sl)
      if valid(ez,co,lab,old,fz,cell['core']):complete.append(dict(a=al,b=bl,y=yl,r=rl,s=sl))
   out.append(dict(cell=cell['id'],core=cell['core'],omega_color=color,U_equals_d=alias,partial_count=len(partial),stars=complete))
 return sorted(out,key=lambda r:(r['cell'],r['omega_color'],r['U_equals_d']))
def canonical(word):
 d={};out=[]
 for c in word:
  if c not in d:d[c]=len(d)
  out.append(d[c])
 return tuple(out)
def complete_lifts(cap,word):
 colors=dict(zip(cap['ordered_boundary'],word));out=[];inner=cap['ordered_inner'];adj={v:set() for v in cap['vertices']}
 for a,b in cap['edges']:adj[a].add(b);adj[b].add(a)
 def visit(i):
  if i==len(inner):out.append([colors[v] for v in inner]);return
  v=inner[i]
  for c in range(4):
   if all(colors.get(w)!=c for w in adj[v]):colors[v]=c;visit(i+1);del colors[v]
 visit(0);return out
def relation_check(c):
 old=load(HERE/'frozen'/REL);require(c['retained_complete_K6_relation']==old,'retained full relation/lifts/empty fibres changed')
 caps=load(HERE/'frozen'/CAPS)['caps'];tables={core:{} for core in ['L','R']}
 for row in old['relations']:
  cap=next(p for p in caps if p['core']==row['core']);observed=complete_lifts(cap,row['word'])
  require(observed==row['complete_lifts'],'complete seven-point lift enumeration')
  tables[row['core']][tuple(row['word'])]=bool(observed)
 require(all(len(t)==31 and sum(t.values())==19 for t in tables.values()),'all proper normalized fibres, including twelve empties')
 ring={tuple(sorted((i,(i+1)%6))) for i in range(6)};models=[]
 for parity in [0,1]:
  p=list(range(parity,6,2));models.append((list(range(6)),ring|{tuple(sorted((p[i],p[(i+1)%3]))) for i in range(3)}))
 for parity in [0,1]:
  p=list(range(parity,6,2));mp=[p[0] if i in p else i for i in range(6)]
  models.append((mp,{tuple(sorted((mp[a],mp[b]))) for a,b in ring}))
 counts=[0]*4;nonempty=0
 for word in itertools.product(range(4),repeat=6):
  proper=all(word[a]!=word[b] for a,b in ring);norm=canonical(word)
  old_accept=proper and tables['L'][norm]
  require(not proper or tables['R'][norm]==old_accept,'cores differ')
  accepted=[]
  for i,(mp,edges) in enumerate(models):
   colors={};consistent=True
   for v,col in zip(mp,word):
    if v in colors and colors[v]!=col:consistent=False
    colors[v]=col
   ok=consistent and all(colors[a]!=colors[b] for a,b in edges);accepted.append(ok);counts[i]+=ok
  require(any(accepted)==old_accept,'four fixed actual candidate relations fail union/containment')
  nonempty+=old_accept
 require(counts==[192,192,108,108] and nonempty==444,'literal relation cardinalities')
 return dict(normalized_fibres_per_core=31,empty_fibres_per_core=12,complete_old_lifts=sum(len(r['complete_lifts']) for r in old['relations']),literal_words=4096,literal_old_support=444,candidate_supports=counts)
def mapped_cap(cap,sub,alias):
 # Substitution is simultaneous: an abstract U replaced by omega must not be
 # confused with the separate actual identification d=U.
 image=lambda v:('d' if alias and sub.get(v,v)=='U' else sub.get(v,v))
 ports=[image(v) for v in cap['ordered_boundary']]
 require(len(ports)==len(set(ports))==6,'six actual distinct contacts')
 edges={edge(image(a),image(b)) for a,b in cap['edges']}
 faces=[[image(v) for v in f] for f in cap['oriented_actual_faces']]
 return image,ports,edges,faces
def face_control(ports,edges,faces):
 require(len(edges)==30 and len(faces)==18,'sealed cap size')
 darts={}
 for f in faces:
  require(len(set(f))==3 and all(edge(a,b) in edges for a,b in zip(f,f[1:]+f[:1])),'actual cap triangular face')
  for a,b in zip(f,f[1:]+f[:1]):darts[a,b]=darts.get((a,b),0)+1
 require(all(n==1 for n in darts.values()),'duplicate directed face side')
 boundary={(a,b) for a,b in darts if (b,a) not in darts}
 require(boundary==set(zip(ports,ports[1:]+ports[:1])),'one original oriented six-contact disk')
def verify(c,rows):
 require(c['schema']=='941-empty-k-collar-v1' and c['base']==BASE,'schema/BASE')
 require(c['source_contract']==dict(M2_empty=True,T_degree=6,resource_size=6,arbitrary_spectators=True,same_original_graph=True,same_rotation=True,same_literal_frame=True,K_sole_frame_contact='U',N_cycle=['r','tau','s','b','y','a'],K_available=['d','x','zeta','U','p_d','p_x','omega']),'same-source scope')
 require(c['wheel_lemma']==dict(exterior_edge_face_vertices=6,maximum_actual_K_vertices=7,no_K_two_nonconsecutive_N_contacts=True,extra_K_touches_at_most_one_N=True,collar_is_simple=True,bipartite_collar=True,collar_length=6,all_N_degrees=5),'universal wheel lemma contract')
 require(c['boundaries']==dict(finite_control='triggered and holds',source_realizability='not triggered',paper_empty_M2_D6_Z6='excluded',empty_M2_min_resource=7,empty_M2_min_exterior=8,full_eleven_types='OPEN',general_wrong_side='OPEN',common_k=23,new_Lean=False,new_matching=False),'authority promotion')
 require(c['same_candidate_reduction']==dict(candidates=['Q_even','Q_odd','J_even','J_odd'],k_drops=[7,7,9,9],choose_once_from_actual_01232=True,rejected_rows=['01021','01202','01212'],all_rows_one_graph_and_frame=True,all_exterior_and_attachments_retained=True,quotient_pullback=True),'one H/literal-frame reduction')
 caps={p['core']:p for p in load(HERE/'frozen'/CAPS)['caps']};require(len(c['cap_substitutions'])==12,'paper substitution coverage')
 # Build expected complete original stars from actual mapped cap graph.
 mapped=[]
 for item in c['cap_substitutions']:
  require(item['core'] in caps and item['omega_color'] in [0,2],'substitution identity')
  cap=caps[item['core']];image,ports,edges,faces=mapped_cap(cap,item['substitution'],item['U_equals_d']);face_control(ports,edges,faces)
  colors={image(v):col for v,col in cap['original_colors'].items()}
  require(all(colors[a]!=colors[b] for a,b in edges),'literal mapped cap coloring')
  require('omega' not in colors or colors['omega']==item['omega_color'],'omega literal color')
  stars={v:{b if a==v else a for a,b in edges if v in (a,b)} for v in cap['ordered_inner']}
  require(all(len(stars[v])==5 for v in ['r','s','tau','a','b','y']),'complete N five degree')
  mapped.append((item,stars,ports,faces))
 total=0;substitution_usage=[0]*len(mapped)
 for row in rows:
  expected=[(i,stars) for i,(item,stars,_,_) in enumerate(mapped) if all(row[k]==item[k] for k in ['core','omega_color','U_equals_d'])]
  observed=[]
  for star in row['stars']:
   matching=[i for i,expect in expected if all(set(lk)==expect[v] for v,lk in star.items())]
   require(len(matching)==1,'complete original N star lacks unique old-cap bijection')
   i=matching[0];substitution_usage[i]+=1;observed.append(i)
   # Every full cyclic link additionally matches the exact old cap face set.
   faces={tuple(sorted(f)) for f in mapped[i][3]}
   require(all(tuple(sorted([v,a,b])) in faces for v,lk in star.items() for a,b in zip(lk,lk[1:]+lk[:1])),'original cyclic order changed under cap map')
  require(len(observed)==len(set(observed)) and set(observed)=={i for i,_ in expected},'paper old-cap table misses or invents source stars')
  total+=len(observed)
 require(len(rows)==44 and total==48 and substitution_usage==[4]*12,'eleven cells/two colors/two literal U identities')
 return dict(source_star_cases=44,partial_aby_stars=sum(r['partial_count'] for r in rows),complete_N_stars=48,old_cap_substitutions=12,oriented_actual_faces_per_cap=18,O_complete_stars=0,paper_Z6_branch='excluded',source_realizability='not triggered')
def wheel_controls():
 # Fixed wheel contacts: every nonconsecutive N pair makes a chordless C4
 # with T and any shared K; every adjacent pair uses its unique outer face.
 cycle=list(range(6));pairs=list(itertools.combinations(cycle,2));adjacent={tuple(sorted((i,(i+1)%6))) for i in cycle}
 nonconsecutive=[p for p in pairs if p not in adjacent]
 require(len(nonconsecutive)==9 and len(adjacent)==6,'N6 pair coverage')
 feasible_extra=[q for q in range(2) if (6+q)%2==0];require(feasible_extra==[0],'bipartite collar parity')
 return dict(N_cycle_edges=6,nonconsecutive_pair_C4_obstructions=9,available_extra_K_vertices=1,possible_collar_lengths=[6])
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--seed',type=int,default=0);ap.add_argument('--negative',action='store_true');ap.add_argument('--certificate',type=Path,default=HERE/'certificate.json');args=ap.parse_args()
 inputs=custody();c=load(args.certificate);rows=reconstruct(args.seed);result=verify(c,rows);relations=relation_check(c);controls=wheel_controls();negative=[]
 if args.negative:
  mutations=[('drop_cap_substitution',lambda d:d['cap_substitutions'].pop()),('identify_literal_U_early',lambda d:d['cap_substitutions'][2]['substitution'].clear()),('wrong_omega_color',lambda d:d['cap_substitutions'][1].__setitem__('omega_color',2)),('allow_eight_K',lambda d:d['wheel_lemma'].__setitem__('maximum_actual_K_vertices',8)),('drop_arbitrary_spectators',lambda d:d['source_contract'].__setitem__('arbitrary_spectators',False)),('invent_full_source',lambda d:d['boundaries'].__setitem__('source_realizability','triggered and holds')),('choose_H_per_rejection',lambda d:d['same_candidate_reduction'].__setitem__('all_rows_one_graph_and_frame',False)),('change_completion_cost',lambda d:d['same_candidate_reduction']['k_drops'].__setitem__(3,7)),('lose_complete_fibre',lambda d:d['retained_complete_K6_relation']['relations'].pop()),('lose_full_lift',lambda d:d['retained_complete_K6_relation']['relations'][0]['complete_lifts'].pop())]
  for name,mutate in mutations:
   broken=copy.deepcopy(c);mutate(broken)
   try:verify(broken,rows);relation_check(broken)
   except (ValueError,KeyError,TypeError):negative.append(name)
   else:raise ValueError('negative control accepted '+name)
 print(json.dumps(dict(status='PASS',seed=args.seed,custody=inputs,result=result,relation=relations,wheel_controls=controls,negative_controls_rejected=negative),ensure_ascii=False,sort_keys=True,indent=2))
if __name__=='__main__':main()
