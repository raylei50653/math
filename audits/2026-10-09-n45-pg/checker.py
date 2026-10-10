#!/usr/bin/env python3
"""Fixed named shield/minor templates only. No source search or colouring replacement.
Generate exclusively; --check rebuilds in memory and never writes.
"""
import argparse,collections,hashlib,itertools,json,sys
from pathlib import Path
D=Path(__file__).resolve().parent

def edge(a,b):return tuple(sorted((a,b)))
def edges_base():
 return set([edge('b'+str(i),'b'+str((i+1)%5)) for i in range(5)]+[edge('U','b'+str(i)) for i in [0,1,2]]+[edge('L','b'+str(i)) for i in [2,3,4]]+[edge('S','b'+str(i)) for i in [4,0]]+[edge('r',p) for p in ['U','L','S']]+[edge('s',p) for p in ['L','S']])
BASE=edges_base()
TEMPLATES=[
 ('r-b4',('r','b4'),[['U'],['b4'],['L','s']],[['S','b0'],['b2','b3'],['r']]),
 ('s-b0',('s','b0'),[['U','b0'],['L'],['S']],[['r'],['s'],['b4']]),
 ('s-b2',('s','b2'),[['U','b2'],['L'],['S']],[['r'],['s'],['b3','b4']])]
FACES=[['b0','b1','U'],['b1','b2','U'],['b2','b3','L'],['b3','b4','L'],['b4','b0','S'],['U','b2','L','r'],['U','r','S','b0'],['L','b4','S','s'],['L','s','S','r']]
POS={'b0':(160,80),'b1':(60,240),'b2':(160,400),'b3':(470,400),'b4':(520,80),'U':(150,240),'L':(390,300),'S':(360,100),'r':(230,215),'s':(400,190)}
def connected_bag(bag,edges):
 reached={bag[0]};tree=[]
 while len(reached)<len(bag):
  options=sorted((a,b) for a in reached for b in bag if b not in reached and edge(a,b) in edges)
  assert options,('disconnected',bag)
  a,b=options[0];reached.add(b);tree.append([a,b])
 return tree

def verify_minor(name,assumed,A,C,edges):
 bags=A+C;assert len(set(sum(bags,[])))==sum(map(len,bags))
 trees=[connected_bag(b,edges) for b in bags]
 joins=[]
 for i,a in enumerate(A):
  for j,b in enumerate(C):
   choices=sorted(edge(x,y) for x in a for y in b if edge(x,y) in edges)
   assert choices,(name,i,j)
   joins.append({'A':i+1,'B':j+1,'retained_edge':list(choices[0])})
 return {'name':name,'assumed_spoke':list(assumed),'A_bags':A,'B_bags':C,'bag_spanning_trees':trees,'nine_original_quotient_edges':joins,'meaning':'U/L/S denote whole connected original pieces; theorem instantiation supplies actual named attachment/contact edges'}

def verify_faces(faces,edges):
 # Give every bounded face the same orientation, outer face the opposite one.
 def area(f):return sum(POS[f[i]][0]*POS[f[(i+1)%len(f)]][1]-POS[f[(i+1)%len(f)]][0]*POS[f[i]][1] for i in range(len(f)))
 fs=[]
 for f in faces:
  fs.append(f if area(f)>0 else list(reversed(f)))
 outer=['b0','b1','b2','b3','b4'];outer=outer if area(outer)<0 else list(reversed(outer));fs.append(outer)
 darts=collections.Counter((f[i],f[(i+1)%len(f)]) for f in fs for i in range(len(f)))
 assert set(darts)==set((a,b) for e in edges for a,b in [e,e[::-1]]) and all(n==1 for n in darts.values())
 rotation={v:{} for v in POS}
 for f in fs:
  for i,b in enumerate(f):rotation[b][f[i-1]]=f[(i+1)%len(f)]
 cycles={}
 for v,rot in rotation.items():
  a=min(rot);seq=[];q=a
  while q not in seq:seq.append(q);q=rot[q]
  assert q==a and len(seq)==len(rot),(v,rot)
  cycles[v]=seq
 assert len(POS)-len(edges)+len(fs)==2
 return {'faces':fs,'rotation':cycles,'Euler_characteristic':2,'B_is_designated_outer_face':True}

def build():
 partitions=[];minors=[]
 for start in range(5):
  for direction in [1,-1]:
   image=lambda i:(start+direction*i)%5
   partitions.append({'start':start,'direction':direction,'U_support':[image(i) for i in [0,1,2]],'L_support':[image(i) for i in [2,3,4]],'S_support':[image(i) for i in [4,0]],'U_shield':[list(edge('b'+str(image(i)),'b'+str(image(i+1)))) for i in [0,1]],'L_shield':[list(edge('b'+str(image(i)),'b'+str(image(i+1)))) for i in [2,3]],'S_shield':[list(edge('b'+str(image(4)),'b'+str(image(0))))]})
   for swap in [False,True]:
    def tr(x):return 'b'+str(image(int(x[1:]))) if x.startswith('b') else ({'r':'s','s':'r'}.get(x,x) if swap else x)
    e={edge(tr(a),tr(b)) for a,b in BASE}
    for name,assumed,A,C in TEMPLATES:
     ae=tuple(map(tr,assumed));m=verify_minor(name,ae,[list(map(tr,b)) for b in A],[list(map(tr,b)) for b in C],e|{edge(*ae)})
     m.update({'frame_start':start,'frame_direction':direction,'whole_root_swap':swap});minors.append(m)
 assert len({tuple(x['U_support']+x['L_support']+x['S_support']) for x in partitions})==10
 profiles=[];embeddings=[]
 for R in [[],['b0'],['b2'],['b0','b2']]:
  for T in [[],['b4']]:
   fs=[f[:] for f in FACES];es=BASE.copy()
   for root,b in [('r',b) for b in R]+[('s',b) for b in T]:
    es.add(edge(root,b));idx=next(i for i,f in enumerate(fs) if root in f and b in f);f=fs.pop(idx)
    ir=f.index(root);f=f[ir:]+f[:ir];ib=f.index(b)
    fs.extend([f[:ib+1],[root]+f[ib:]])
   em=verify_faces(fs,es);em.update({'r_spokes':R,'s_spokes':T});embeddings.append(em)
   mr=4-len(R);ms=5-len(T)
   for krL in range(1,mr):
    for ksL in range(1,ms):
     profiles.append({'r_spokes':R,'s_spokes':T,'U_root_incidence':1,'L_incidence':[krL,ksL],'S_incidence':[mr-krL,ms-ksL],'r_degree':5,'s_degree':5,'meaning':'necessary integer data only; no full graph, attachments, rotation or relations supplied'})
 assert len(profiles)==56
 unary_oracle=[]
 for c0,c4 in itertools.permutations(range(4),2):
  palette=[c for c in range(4) if c not in [c0,c4]]
  full_lifts={str(a)+','+str(b):[c for c in palette if c!=a and c!=b] for a in range(4) for b in range(4)}
  assert all(full_lifts[str(a)+','+str(c0)] for a in range(4))
  unary_oracle.append({'b0_colour':c0,'b4_colour':c4,'single_vertex_S_palette':palette,'complete_16_pin_lifts':full_lifts,'column_s_equals_b0_forbidden_r':[],'antecedent':'only a one-vertex edge-pair-supported S; fails positive column saturation'})
 return {'task':'N45-PG','BASE':'dc8e9aa7d6fccb51f63d30aa3f9c132296d44744','evidence_layer':'finite symbolic topology templates and one-vertex local lifts; no target sources','named_partitions':partitions,'whole_D5_and_root_swap_minor_templates':minors,'abstract_contracted_disk_embeddings':embeddings,'necessary_incidence_profiles':profiles,'single_vertex_S_negative_oracles':unary_oracle,'counts':{'named_shield_partitions':10,'minor_templates_with_whole_root_swap':60,'abstract_spoke_embeddings':8,'necessary_integer_profiles':56,'single_vertex_local_colour_oracles':12,'complete_target_sources':0},'scope':'Paper theorem supplies all original bag edges and arbitrary connected piece bags; these finite checks do not prove source existence or whole LP exclusion.'}

def main():
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
 b=(json.dumps(build(),sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode();target=D/'certificate.json'
 if a.check:
  assert target.read_bytes()==b,'certificate drift'
  print('PASS: read-only exact-byte replay; '+str(len(b))+' bytes; SHA256 '+hashlib.sha256(b).hexdigest())
 else:
  with target.open('xb') as f:f.write(b)
  print('Created certificate exclusively: '+str(len(b))+' bytes; SHA256 '+hashlib.sha256(b).hexdigest())
if __name__=='__main__':main()
