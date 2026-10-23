"""Exclusive-create the round-seven finite certificate, retaining empty fibres."""
import itertools,json
from pathlib import Path
import explore_k8 as e
HERE=Path(__file__).resolve().parent
BASE='6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'
CONTRACT=dict(same_original_G_F=True,same_rotation_attachments_B14_literal_frame=True,
 complete_original_components=True,arbitrary_spectators=True,M2_empty=True,T_degree=6,
 resource_count=7,K_sole_F_frame_contact='U',U_F_link_not_complete_original_star=True,
 all_rootless_stars_minimum_original_degree=5,rootless_neighbor_closure=True,
 choose_once_from_actual_01232=True,three_rejected_rows_one_H=True,
 pullback_to_same_original_exterior=True,all_eight_ports_original_C5_inner=True)
BOUNDARIES=dict(finite_control='triggered and holds',source_realizability='not triggered',
 paper_seven_resource_NN_NK='excluded_by_complete_finite_star_certificate',
 K8_full_safe_replacement='OPEN',K8_accepting_witness_outside_safe_library='necessary',
 empty_min_X=8,nonempty_min_X=9,non_single_M2_min_X=10,eleven_entire_type_exclusions=0,
 common_k=23,general_wrong_side='OPEN',new_Lean=False,new_matching=False)
def quotient(model):
 parent=list(range(8))
 def find(v):
  while parent[v]!=v:v=parent[v]
  return v
 for a,b in model['equal']:
  a,b=find(a),find(b);parent[max(a,b)]=min(a,b)
 ports=[find(v) for v in range(8)]
 edges={tuple(sorted((ports[a],ports[b]))) for a,b in [(i,(i+1)%8) for i in range(8)]+model['different']}
 assert all(a!=b for a,b in edges)
 return dict(port_map=ports,vertices=sorted(set(ports)),edges=[list(x) for x in sorted(edges)],k_drop=7+8-len(set(ports)))
def main():
 words=e.words();library=e.models(words);caps=[]
 for a in range(6):
  for b in range(a,6):
   dist=[0]*6;dist[a]+=1;dist[b]+=1;cap=e.m.wheel(dist)
   graph=dict(vertices=cap['inner']+cap['boundary'],ordered_inner=cap['inner'],ordered_boundary=cap['boundary'],edges=sorted(cap['edges']))
   fibres=[dict(word=list(w),full_lifts=e.m.complete_lifts(graph,w)) for w in words]
   mask=sum(1<<i for i,row in enumerate(fibres) if row['full_lifts']);safe=[];union=0
   for sm,model in sorted(library.items()):
    if sm&~mask:continue
    union|=sm;safe.append(dict(**model,**quotient(model),normalized_relation=[list(w) for i,w in enumerate(words) if sm>>i&1]))
   caps.append(dict(distribution=dist,ordered_inner=cap['inner'],ordered_boundary=cap['boundary'],edges=[list(x) for x in sorted(cap['edges'])],
    oriented_actual_faces=cap['faces'],complete_fibres=fibres,safe_candidates=safe,
    residual_accepting_words=[list(w) for i,w in enumerate(words) if mask>>i&1 and not union>>i&1]))
 cert=dict(schema='941-round7-empty-seven-v1',base=BASE,contract=CONTRACT,boundaries=BOUNDARIES,
  source_star_contexts=json.loads((HERE/'INDEPENDENT_STARS.json').read_text()),
  independent_DFS_contexts=json.loads((HERE/'EXPLORATION_STARS.json').read_text()),
  library=dict(triangulations=132,diagonal_labelings=4224,distinct_nonempty_relations=398),caps=caps)
 with (HERE/'certificate.json').open('x') as f:json.dump(cert,f,sort_keys=True,indent=2);f.write('\n')
 print('created',len(caps),'caps',sum(len(c['complete_fibres']) for c in caps),'fibres',sum(len(c['safe_candidates']) for c in caps),'safe candidates')
if __name__=='__main__':main()
