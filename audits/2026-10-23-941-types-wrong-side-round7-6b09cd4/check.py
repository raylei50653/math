#!/usr/bin/env python3
"""Read-only independent star catalogs, full lifts, and actual quotient graphs."""
import argparse,copy,hashlib,itertools,json,random,sys
from pathlib import Path
import stars_independent
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BASE='6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'
KINDS=[('N1','N1'),('N1','N3'),('N3','N3'),('N1','K0'),('N1','K2'),('N3','K0'),('N3','K2')]
CONTRACT=dict(same_original_G_F=True,same_rotation_attachments_B14_literal_frame=True,complete_original_components=True,
 arbitrary_spectators=True,M2_empty=True,T_degree=6,resource_count=7,K_sole_F_frame_contact='U',
 U_F_link_not_complete_original_star=True,all_rootless_stars_minimum_original_degree=5,rootless_neighbor_closure=True,
 choose_once_from_actual_01232=True,three_rejected_rows_one_H=True,pullback_to_same_original_exterior=True,all_eight_ports_original_C5_inner=True)
BOUNDARIES=dict(finite_control='triggered and holds',source_realizability='not triggered',
 paper_seven_resource_NN_NK='excluded_by_complete_finite_star_certificate',K8_full_safe_replacement='OPEN',
 K8_accepting_witness_outside_safe_library='necessary',empty_min_X=8,nonempty_min_X=9,non_single_M2_min_X=10,
 eleven_entire_type_exclusions=0,common_k=23,general_wrong_side='OPEN',new_Lean=False,new_matching=False)
def require(ok,msg):
 if not ok:raise ValueError(msg)
def load(p):return json.loads(p.read_text())
def edge(a,b):return tuple(sorted((a,b)))
def custody():
 inputs=load(HERE/'INPUTS.json')['inputs']+[load(HERE/'INPUTS_STARS.json')]+load(HERE/'INPUTS_COVERAGE.json');total=0
 for r in inputs:
  for p in [HERE/r['snapshot']]+([] if r.get('authority')=='routing-entry' else [ROOT/r['path']]):
   b=p.read_bytes();require((len(b),hashlib.sha256(b).hexdigest())==(r['bytes'],r['sha256']),'authority drift '+str(p))
 routing=0
 for r in load(HERE/'PREDECESSOR_REPLAY.json')['entries']:
  is_routing=r['path'] in ('docs/STATUS.md','docs/c5_kempe_guide.md')
  p=(HERE/'entry'/r['path']) if is_routing else ROOT/r['path']
  b=p.read_bytes();require((len(b),hashlib.sha256(b).hexdigest())==(r['bytes'],r['sha256']),'predecessor drift '+r['path']);total+=1;routing+=is_routing
 return dict(direct_inputs=len(inputs),predecessor_files=total,predecessor_immutable_files=total-routing,predecessor_routing_snapshots=routing,immutable_drift=0)
def header(c):
 require(c['schema']=='941-round7-empty-seven-v1' and c['base']==BASE,'schema/BASE')
 require(c['contract']==CONTRACT,'same-source/same-H contract changed')
 require(c['boundaries']==BOUNDARIES,'authority boundary changed')
 require(len(c['caps'])==21 and len(c['source_star_contexts'])==154 and len(c['independent_DFS_contexts'])==154,'domain incomplete')
def canonical(w):
 mapping={};return tuple(mapping.setdefault(x,len(mapping)) for x in w)
def domain():
 # Restricted-growth words: one common S4 action on the entire ordered tuple.
 words=[]
 def visit(w):
  if len(w)==8:
   if w[-1]!=w[0]:words.append(tuple(w))
   return
  for col in range(min(3,max(w)+1)+1):
   if col!=w[-1]:visit(w+[col])
 visit([0]);require(len(words)==274,'complete ordered eight-port domain');return words
def graph(dist):
 faces=[];boundary=[]
 for i in range(6):faces.append(['T','n'+str(i),'n'+str((i+1)%6)])
 for i in range(6):faces.append(['n'+str((i+1)%6),'n'+str(i),'q'+str(i)])
 for i in range(6):
  arc=['q'+str((i-1)%6)]+['w'+str(i)+'_'+str(j) for j in range(dist[i])]+['q'+str(i)]
  boundary.extend(arc[:-1])
  faces.extend([['n'+str(i),a,b] for a,b in zip(arc,arc[1:])])
 es={edge(a,b) for f in faces for a,b in zip(f,f[1:]+f[:1])}
 return ['T']+['n'+str(i) for i in range(6)],boundary,es,faces
def lifts(inner,boundary,edges,word):
 adj={v:set() for v in inner+boundary}
 for a,b in edges:adj[a].add(b);adj[b].add(a)
 colors=dict(zip(boundary,word));out=[]
 def visit(todo):
  if not todo:out.append([colors[v] for v in inner]);return
  v=min(todo,key=lambda v:(len({c for c in range(4) if all(colors.get(w)!=c for w in adj[v])}),v))
  for col in range(4):
   if all(colors.get(w)!=col for w in adj[v]):colors[v]=col;visit(todo-{v});del colors[v]
 visit(set(inner));return sorted(out)
def library(words):
 diagonals=[(a,b) for a,b in itertools.combinations(range(8),2) if b-a not in (1,7)]
 def cross(x,y):
  a,b=x;c,d=y;return a<c<b<d or c<a<d<b
 triangles=[tri for tri in itertools.combinations(diagonals,5) if not any(cross(a,b) for a,b in itertools.combinations(tri,2))]
 require(len(triangles)==132,'all octagon triangulations')
 relations=set()
 for tri in triangles:
  bins={}
  for i,w in enumerate(words):
   label=tuple(w[a]==w[b] for a,b in tri);bins[label]=bins.get(label,0)|(1<<i)
  relations.update(bins.values())
 require(len(relations)==398,'all nonempty labeled-triangulation relations')
 return relations
def quotient(q,words):
 equal=[tuple(e) for e in q['equal']];different=[tuple(e) for e in q['different']]
 require(all((a-b)%2==0 for a,b in equal),'original K parity nonedge for contraction')
 allchords=equal+different
 require(len(allchords)==len(set(allchords))==5,'five labeled diagonals')
 require(all(0<=a<b<8 and b-a not in (1,7) for a,b in allchords),'diagonal domain')
 require(not any(a<c<b<d or c<a<d<b for (a,b),(c,d) in itertools.combinations(allchords,2)),'crossing contraction/chord')
 blocks=[{v} for v in range(8)]
 for a,b in equal:
  aa=next(s for s in blocks if a in s);bb=next(s for s in blocks if b in s)
  if aa is not bb:blocks.remove(aa);blocks.remove(bb);blocks.append(aa|bb)
 mp=[min(next(s for s in blocks if v in s)) for v in range(8)]
 es={edge(mp[a],mp[b]) for a,b in [(i,(i+1)%8) for i in range(8)]+different}
 require(all(a!=b for a,b in es),'quotient loop')
 require(q['port_map']==mp and q['vertices']==sorted(set(mp)) and q['edges']==[list(x) for x in sorted(es)],'actual quotient graph')
 require(q['k_drop']==7+8-len(set(mp)),'completed cost')
 result=[]
 for w in words:
  assigned={};proper=True
  for v,col in zip(mp,w):
   if v in assigned and assigned[v]!=col:proper=False
   assigned[v]=col
  if proper and all(assigned[a]!=assigned[b] for a,b in es):result.append(list(w))
 require(q['normalized_relation']==result,'whole quotient coloring relation')
 return sum(1<<i for i,w in enumerate(words) if list(w) in result)
def validate(c,seed):
 header(c);words=domain();lib=library(words);require(c['library']==dict(triangulations=132,diagonal_labelings=4224,distinct_nonempty_relations=398),'library domain')
 contract=load(HERE/'entry/audits/2026-10-23-941-gamma8-cells-6b09cd4/certificate.json')
 cells=[x for x in contract['candidates'] if x['classification']=='local_necessary_type']
 contexts=[(cell,kinds,alias) for cell in cells for kinds in KINDS for alias in (False,True)]
 expectedkeys=[(cell['id'],list(kinds),alias) for cell,kinds,alias in contexts]
 for table in [c['source_star_contexts'],c['independent_DFS_contexts']]:
  require([(r['cell'],r['kinds'],r['d_equals_U']) for r in table]==expectedkeys,'all 154 labeled source contexts including aliases')
 order=list(range(154));random.Random(seed).shuffle(order)
 for i in order:
  cell,kinds,alias=contexts[i];actual=stars_independent.audit(contract,cell,kinds,alias)
  require(actual==c['source_star_contexts'][i],'independent full-cycle catalog/join mismatch')
  require(actual['complete_join_count']==0,'full N star exists in necessary envelope')
  dfs=c['independent_DFS_contexts'][i]
  require(dfs['rows']==[] and dfs['stage_counts'][:6]==actual['stage_counts'][:6] and dfs['stage_counts'][-1]==0,'independent DFS prefix/final mismatch')
 distributions=[]
 for a in range(6):
  for b in range(a,6):
   d=[0]*6;d[a]+=1;d[b]+=1;distributions.append(d)
 require([r['distribution'] for r in c['caps']]==distributions,'21 full cap distributions')
 totals=dict(complete_fibres=0,empty_fibres=0,nonempty_fibres=0,full_lifts=0,safe_candidates=0,safely_covered_fibres=0,residual_fibres=0,literal_lifts_checked=0)
 capstats=[]
 for row in c['caps']:
  inner,boundary,es,faces=graph(row['distribution'])
  require(row['ordered_inner']==inner and row['ordered_boundary']==boundary and row['edges']==[list(x) for x in sorted(es)] and row['oriented_actual_faces']==faces,'whole cap edges/rotation')
  require(len(es)==34 and len(faces)==20,'K8 sealed size')
  darts=[(a,b) for f in faces for a,b in zip(f,f[1:]+f[:1])]
  require(len(set(darts))==60 and {(a,b) for a,b in darts if (b,a) not in darts}==set(zip(boundary,boundary[1:]+boundary[:1])),'common actual face orientation')
  require([r['word'] for r in row['complete_fibres']]==[list(w) for w in words],'all fibres including empties')
  support=0
  for i,(w,f) in enumerate(zip(words,row['complete_fibres'])):
   actual=lifts(inner,boundary,es,w);require(sorted(f['full_lifts'])==actual,'complete seven-point lift reconstruction')
   totals['complete_fibres']+=1;totals['full_lifts']+=len(actual)
   if actual:support|=1<<i;totals['nonempty_fibres']+=1
   else:totals['empty_fibres']+=1
   # Inverse one common literal palette on every vertex, including unused colors.
   for perm in itertools.permutations(range(4)):
    for lift in actual:
     col=dict(zip(boundary,[perm[x] for x in w]));col.update(zip(inner,[perm[x] for x in lift]))
     require(all(col[a]!=col[b] for a,b in es),'full literal lift edge failure');totals['literal_lifts_checked']+=1
  safe={mask for mask in lib if not mask&~support};observed=set();union=0
  for q in row['safe_candidates']:
   mask=quotient(q,words);require(mask in safe,'candidate leaks an original empty fibre');observed.add(mask);union|=mask
  require(observed==safe and len(observed)==len(row['safe_candidates']),'complete safe sublibrary')
  residual=[list(w) for i,w in enumerate(words) if support>>i&1 and not union>>i&1]
  require(residual==row['residual_accepting_words'],'residual accepting witness relation')
  totals['safe_candidates']+=len(safe);totals['safely_covered_fibres']+=union.bit_count();totals['residual_fibres']+=len(residual)
  capstats.append(dict(distribution=row['distribution'],nonempty=support.bit_count(),full_lifts=sum(len(f['full_lifts']) for f in row['complete_fibres']),safe=len(safe),covered=union.bit_count(),residual=len(residual)))
 require(totals==dict(complete_fibres=5754,empty_fibres=3003,nonempty_fibres=2751,full_lifts=4236,safe_candidates=72,safely_covered_fibres=1041,residual_fibres=1710,literal_lifts_checked=101664),'complete relation totals')
 return dict(source_contexts=154,source_full_star_joins=0,**totals,cap_stats=capstats)
def negatives(c):
 # Compare mutations to a certificate already independently reconstructed above.
 mutations=[('drop_empty_fibre',lambda x:next(r for r in x['caps'][0]['complete_fibres'] if not r['full_lifts']).update(full_lifts=[[0]*7])),
  ('lose_full_lift',lambda x:next(r for r in x['caps'][0]['complete_fibres'] if r['full_lifts'])['full_lifts'].pop()),
  ('drop_NN_context',lambda x:x['source_star_contexts'].pop(0)),('drop_d_U_alias',lambda x:x['source_star_contexts'][1].update(d_equals_U=False)),
  ('invent_complete_star',lambda x:x['source_star_contexts'][0].update(complete_join_count=1)),
  ('change_quotient',lambda x:x['caps'][0]['safe_candidates'][0]['port_map'].__setitem__(0,7)),
  ('claim_full_K8_cover',lambda x:x['caps'][0].update(residual_accepting_words=[])),
  ('choose_H_per_row',lambda x:x['contract'].update(three_rejected_rows_one_H=False)),
  ('seal_U_original_star',lambda x:x['contract'].update(U_F_link_not_complete_original_star=False)),
  ('forbid_spectators',lambda x:x['contract'].update(arbitrary_spectators=False)),
  ('invent_source',lambda x:x['boundaries'].update(source_realizability='triggered and holds')),
  ('raise_common_X',lambda x:x['boundaries'].update(empty_min_X=9)),
  ('exclude_eleven',lambda x:x['boundaries'].update(eleven_entire_type_exclusions=1)),
  ('raise_k',lambda x:x['boundaries'].update(common_k=24))]
 out=[]
 def replay_cached(candidate):
  header(candidate)
  require(candidate==c,'semantic disagreement with independently reconstructed complete certificate')
 for name,mutate in mutations:
  bad=copy.deepcopy(c);mutate(bad)
  try:replay_cached(bad)
  except (ValueError,KeyError,TypeError,IndexError):out.append(dict(name=name,status='rejected_against_independently_reconstructed_certificate'))
  else:raise ValueError('negative accepted '+name)
 return out
def main():
 p=argparse.ArgumentParser();p.add_argument('--certificate',type=Path,default=HERE/'certificate.json');p.add_argument('--seed',type=int,default=0);p.add_argument('--negative',action='store_true');a=p.parse_args()
 c=load(a.certificate);header(c);auth=custody();result=validate(c,a.seed)
 print(json.dumps(dict(status='PASS',seed=a.seed,custody=auth,**result,negative_controls=negatives(c) if a.negative else []),sort_keys=True))
if __name__=='__main__':
 try:main()
 except (ValueError,KeyError,TypeError,IndexError,OSError,json.JSONDecodeError) as e:
  print(json.dumps(dict(status='REJECT',reason=str(e))));sys.exit(1)
