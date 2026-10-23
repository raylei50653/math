#!/usr/bin/env python3
"""Read-only checks of the paper contract, full wheel caps, and retained fibres."""
import argparse,copy,hashlib,itertools,json,random
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BASE='6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'
CAPS='audits/2026-10-23-941-gamma8-empty-m2-6b09cd4/K6_CAPS.json'
REL='audits/2026-10-23-941-types-wrong-side-6b09cd4/CAP_RELATION-v2.json'
def require(ok,msg):
 if not ok:raise ValueError(msg)
def load(p):return json.loads(p.read_text())
def edge(a,b):return tuple(sorted((a,b)))
def custody():
 m=load(HERE/'INPUTS.json');require(m['base']==BASE,'BASE custody')
 for row in m['authority']:
  for p in [ROOT/row['path'],HERE/row['snapshot']]:
   b=p.read_bytes();require((len(b),hashlib.sha256(b).hexdigest())==(row['bytes'],row['sha256']),'input drift '+str(p))
 return dict(authority_files=len(m['authority']),immutable_drift=0)
def wheel(k):
 n=['n'+str(i) for i in range(6)];q=['q'+str(i) for i in range(6)]
 faces=[['T',n[i],n[(i+1)%6]] for i in range(6)]+[[n[(i+1)%6],n[i],q[i]] for i in range(6)]
 boundary=[q[-1]]
 for i,extra in enumerate(k):
  arc=[q[(i-1)%6]]+['w'+str(i)+'_'+str(j) for j in range(extra)]+[q[i]]
  faces += [[n[i],a,b] for a,b in zip(arc,arc[1:])]
  boundary += arc[1:]
 boundary.pop()
 es={edge(a,b) for f in faces for a,b in zip(f,f[1:]+f[:1])}
 return dict(inner=['T']+n,boundary=boundary,edges=es,faces=faces)
def cap_check(cap):
 es=cap['edges'];faces=cap['faces'];boundary=cap['boundary'];inner=cap['inner'];darts={}
 for f in faces:
  require(len(set(f))==3,'triangle degeneracy')
  for a,b in zip(f,f[1:]+f[:1]):darts[a,b]=darts.get((a,b),0)+1
 require(set(es)=={edge(a,b) for a,b in darts},'cap edge/face mismatch')
 require(all(v==1 for v in darts.values()),'duplicate face dart')
 require({(a,b) for a,b in darts if (b,a) not in darts}==set(zip(boundary,boundary[1:]+boundary[:1])),'one shared oriented collar')
 verts=set(inner+boundary);require(len(verts)-len(es)+len(faces)==1,'disk Euler receipt')
 degrees=[]
 for v in inner:
  neighbors={b if a==v else a for a,b in es if v in (a,b)}
  link={edge(f[(i+1)%3],f[(i+2)%3]) for f in faces for i,x in enumerate(f) if x==v}
  adj={x:set() for x in neighbors}
  for a,b in link:adj[a].add(b);adj[b].add(a)
  require(all(len(vv)==2 for vv in adj.values()),'full interior link degree')
  seen=set();todo=[next(iter(neighbors))]
  while todo:
   x=todo.pop()
   if x in seen:continue
   seen.add(x);todo.extend(adj[x]-seen)
  require(seen==neighbors,'full interior link disconnected')
  require(len(neighbors)>=5,'full interior degree below five')
  degrees.append(len(neighbors))
 require(degrees[0]==6,'complete T6 star')
 return sorted(degrees[1:])
def calibrations(seed):
 rng=random.Random(seed);distributions=[]
 for a in range(6):
  for b in range(a,6):
   k=[0]*6;k[a]+=1;k[b]+=1;distributions.append(k)
 rng.shuffle(distributions);patterns={};sizes=set()
 for k in distributions:
  cap=wheel(k);p=tuple(cap_check(cap));patterns[p]=patterns.get(p,0)+1
  sizes.add((len(cap['inner'])+len(cap['boundary']),len(cap['edges']),len(cap['faces'])))
  colors={v:i%2*2 for i,v in enumerate(cap['boundary'])};colors['T']=0
  colors.update({'n'+str(i):1+2*(i%2) for i in range(6)})
  require(all(colors[a]!=colors[b] for a,b in cap['edges']),'one literal proper cap coloring')
 require(patterns=={(5,5,5,5,5,7):6,(5,5,5,5,6,6):15},'all two-slot compositions')
 require(sizes=={(15,34,20)},'sealed K8 size')
 # This is an abstract full-star calibration. Original Gamma source coverage
 # is the paper argument, and no K8 replacement or source realization follows.
 return dict(abstract_K8_caps=len(distributions),degree_pattern_counts={','.join(map(str,k)):v for k,v in sorted(patterns.items())},vertices=15,edges=34,actual_oriented_faces=20,full_inner_stars=7,source_realizability='not triggered')
def all_D_controls():
 out=[]
 for D in range(6,34,2):
  pairs=list(itertools.combinations(range(D),2));adjacent={tuple(sorted((i,(i+1)%D))) for i in range(D)}
  require(len(adjacent)==D and len(pairs)-len(adjacent)==D*(D-3)//2,'rim C4 pair coverage')
  # Any q meeting two distinct rim edges has at least three rim neighbors;
  # those contain a nonconsecutive pair, hence the forbidden T/q C4.
  for a,b in itertools.combinations(range(D),2):
   ns={a,(a+1)%D,b,(b+1)%D}
   require(any(tuple(sorted(p)) not in adjacent for p in itertools.combinations(ns,2)),'two face points may coincide')
  for alias in [False,True]:
   fixed=3 if alias else 4;minimum=2*D-3-fixed
   require(minimum==2*D-(6 if alias else 7),'all-D algebra')
   require(fixed+minimum-(D-3)==D,'sharp 02 resource budget')
   require(fixed+(minimum-1)-(D-3)<D,'below-bound resource shortage')
   out.append(dict(D=D,d_equals_U=alias,min_Z=minimum,min_X=minimum+1))
 return out
def extra_controls():
 rim=list(range(6));adjacent={tuple(sorted((i,(i+1)%6))) for i in rim};allowed=[]
 for size in range(7):
  for subset in itertools.combinations(rim,size):
   if all(tuple(sorted(p)) in adjacent for p in itertools.combinations(subset,2)):allowed.append(subset)
 require(max(map(len,allowed))==2,'outside non-T rim contacts')
 require(max(map(len,allowed))+1==3<5,'other-02 complete star contradiction')
 require([n for n in range(6,9) if n%2==0]==[6,8],'two-extra K collar parity')
 viable=[]
 for alias,c1,c2 in itertools.product([False,True],[0,2],[0,2]):
  old0=2 if alias else 3;old2=3
  if old0+(c1==0)+(c2==0)==4 and old2+(c1==2)+(c2==2)==4:viable.append((alias,c1,c2))
 require(viable==[(False,0,2),(False,2,0)],'K8 exact balanced colors/alias')
 return dict(non_T_allowed_rim_subsets=len(allowed),other_02_degree_upper_bound=3,other_02_minimum_degree=5,both_K_surviving_ordered_identities=viable)
def complete_lifts(cap,word):
 colors=dict(zip(cap['ordered_boundary'],word));out=[];inner=cap['ordered_inner'];adj={v:set() for v in cap['vertices']}
 for a,b in cap['edges']:adj[a].add(b);adj[b].add(a)
 def visit(i):
  if i==len(inner):out.append([colors[v] for v in inner]);return
  v=inner[i]
  for c in range(4):
   if all(colors.get(w)!=c for w in adj[v]):colors[v]=c;visit(i+1);del colors[v]
 visit(0);return out
def canonical(word):
 d={};out=[]
 for x in word:
  if x not in d:d[x]=len(d)
  out.append(d[x])
 return tuple(out)
def relations(c):
 old=load(HERE/'frozen'/REL);require(c['complete_retained_K6_relation']==old,'complete old relations changed')
 caps=load(HERE/'frozen'/CAPS)['caps'];tables={p['core']:{} for p in caps};generic=wheel([0]*6);cap_check(generic)
 mapping={'T':'T',**{'n'+str(i):x for i,x in enumerate(['r','tau','s','b','y','a'])}}
 for cap in caps:
  es={edge(*e) for e in cap['edges']}
  mp=dict(mapping)
  for i in range(6):
   pair={mapping['n'+str(i)],mapping['n'+str((i+1)%6)]}
   qs=[v for v in cap['ordered_boundary'] if all(edge(v,n) in es for n in pair)]
   require(len(qs)==1,'whole K6 graph mapping')
   mp['q'+str(i)]=qs[0]
  require(len(set(mp.values()))==13,'one whole cap bijection')
  require({edge(mp[a],mp[b]) for a,b in generic['edges']}==es,'all 30 old cap edges')
  require({tuple(sorted(mp[v] for v in f)) for f in generic['faces']}=={tuple(sorted(f)) for f in cap['oriented_actual_faces']},'all 18 old cap faces')
 for row in old['relations']:
  cap=next(x for x in caps if x['core']==row['core'])
  observed=complete_lifts(cap,row['word']);require(observed==row['complete_lifts'],'full seven-inner lifts')
  tables[row['core']][tuple(row['word'])]=bool(observed)
 require(all(len(t)==31 and sum(t.values())==19 for t in tables.values()),'all fibres including empties')
 ring={edge(i,(i+1)%6) for i in range(6)};models=[]
 for parity in [0,1]:
  p=list(range(parity,6,2));models.append((list(range(6)),ring|{edge(p[i],p[(i+1)%3]) for i in range(3)}))
 for parity in [0,1]:
  p=list(range(parity,6,2));mp=[p[0] if i in p else i for i in range(6)];models.append((mp,{edge(mp[a],mp[b]) for a,b in ring}))
 for word in itertools.product(range(4),repeat=6):
  proper=all(word[a]!=word[b] for a,b in ring);old_ok=proper and tables['L'][canonical(word)]
  require(not proper or tables['R'][canonical(word)]==old_ok,'one complete old relation')
  accepted=[]
  for mp,es in models:
   colors={};consistent=True
   for v,col in zip(mp,word):
    if v in colors and colors[v]!=col:consistent=False
    colors[v]=col
   accepted.append(consistent and all(colors[a]!=colors[b] for a,b in es))
  require(any(accepted)==old_ok,'four fixed same-H candidates full containment/cover')
 return dict(complete_fibres=62,empty_fibres=24,complete_lifts=sum(len(r['complete_lifts']) for r in old['relations']),literal_boundary_words=4096,whole_old_cap_graph_bijections=2)
def verify(c):
 require(c['schema']=='941-empty-seven-v1' and c['base']==BASE,'schema/BASE')
 require(c['source_contract']==dict(M2_empty=True,same_original_graph=True,same_rotation=True,same_literal_frame=True,complete_original_components=True,all_attachments_retained=True,arbitrary_spectators=True,K_sole_frame_contact='U'),'same-source authority')
 require(c['rim_faces']==dict(every_rim_edge_has_actual_opposite_face=True,q_original_colors=[0,2],q_pairwise_distinct=True,no_T_q_edge=True,no_K_assumption_for_general_q=True,available_non_Z_02=['d','x','zeta','U'],outside_T_link_N_count='D-3'),'complete actual rim face contract')
 require(c['all_D_bound']==dict(minimum_even_D=6,resource_lower_bound='2*D-7',alias_d_U_resource_lower_bound='2*D-6',spectator_lower_bound=1,D8_min_resource=9,D8_min_exterior=10,D8_alias_min_resource=10,D8_alias_min_exterior=11),'universal wheel bound')
 require(c['seven_resource_D6']==dict(extra_resources=2,forbidden_extra_02_outside_K=True,extra_02_max_rim_neighbors=2,extra_02_max_other_neighbors=1,extra_02_degree_upper_bound=3,minimum_original_degree=5,remaining_extra_identities=['K0','K2','N1','N3'],no_new_13_component=True),'seven-resource full-star bound')
 require(c['both_K']==dict(maximum_actual_K=8,possible_collar_lengths=[6,8],collar6='excluded by frozen same-H four-candidate reduction',remaining_collar_length=8,remaining_alias_d_U=False,remaining_extra_colors=[0,2],all_actual_K_on_collar=True,N_degree_patterns=[[5,5,5,5,5,7],[5,5,5,5,6,6]],sealed_inner_vertices=7,K8_edges=34,K8_faces=20),'joint K8 stopping point')
 require(c['same_candidate']==dict(choose_once_from_actual_01232=True,all_three_rejected_rows_one_H=True,rejected_rows=['01021','01202','01212'],all_same_original_exterior=True,quotient_pullback=True,k6_k_drops=[7,7,9,9]),'one same H/frame reduction')
 require(c['boundaries']==dict(finite_control='triggered and holds',full_source_realizability='not triggered',paper_D8_Z7_and_Z8='excluded',paper_D6_extra_other_02='excluded',paper_D6_bothK_same_color_or_d_equals_U='excluded',paper_D6_mixed_or_twoN='OPEN',paper_D6_bothK_K8='OPEN',empty_M2_min_exterior=8,full_eleven_types='OPEN',general_wrong_side='OPEN',common_k=23,new_Lean=False,new_matching=False,new_K8_replacement=False),'no authority promotion')
 return True
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--certificate',type=Path,default=HERE/'certificate.json');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--negative',action='store_true');args=ap.parse_args()
 custody_result=custody();c=load(args.certificate);verify(c);rel=relations(c);negative=[]
 if args.negative:
  muts=[('drop_frame',lambda d:d['source_contract'].__setitem__('same_literal_frame',False)),('forbid_spectators',lambda d:d['source_contract'].__setitem__('arbitrary_spectators',False)),('assume_q_in_K',lambda d:d['rim_faces'].__setitem__('no_K_assumption_for_general_q',False)),('lose_U_alias',lambda d:d['all_D_bound'].__setitem__('alias_d_U_resource_lower_bound','2*D-7')),('lower_D8',lambda d:d['all_D_bound'].__setitem__('D8_min_exterior',9)),('raise_other02_degree',lambda d:d['seven_resource_D6'].__setitem__('extra_02_degree_upper_bound',5)),('allow_same_K_colors',lambda d:d['both_K'].__setitem__('remaining_extra_colors',[0,0])),('reuse_d_U',lambda d:d['both_K'].__setitem__('remaining_alias_d_U',True)),('exclude_K8',lambda d:d['boundaries'].__setitem__('paper_D6_bothK_K8','excluded')),('invent_source',lambda d:d['boundaries'].__setitem__('full_source_realizability','triggered and holds')),('choose_H_per_row',lambda d:d['same_candidate'].__setitem__('all_three_rejected_rows_one_H',False)),('delete_fibre',lambda d:d['complete_retained_K6_relation']['relations'].pop()),('delete_full_lift',lambda d:d['complete_retained_K6_relation']['relations'][0]['complete_lifts'].pop())]
  for name,mutate in muts:
   bad=copy.deepcopy(c);mutate(bad)
   try:verify(bad);relations(bad)
   except (ValueError,KeyError,TypeError):negative.append(name)
   else:raise ValueError('negative accepted '+name)
 print(json.dumps(dict(status='PASS',seed=args.seed,custody=custody_result,all_D_controls=all_D_controls(),extra_resource_controls=extra_controls(),K8_abstract_full_star_controls=calibrations(args.seed),retained_full_relation=rel,negative_controls_rejected=negative),sort_keys=True,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
