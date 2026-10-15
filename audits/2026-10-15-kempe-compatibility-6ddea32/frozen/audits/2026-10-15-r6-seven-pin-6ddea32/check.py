#!/usr/bin/env python3
"""Two finite method controls; never a source-realizability checker."""
import argparse, hashlib, importlib.util, itertools, json, math
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PINS=('z','s','v','w','t','p','q')
CUT_PINS=('z_left','s','v','w','t','z_right','p','q')
SOURCE=HERE/'frozen/audits/2026-10-14-c4-c5-recursion-fdd3e22/degree4/check_transfer.py'
spec=importlib.util.spec_from_file_location('frozen_transfer',SOURCE)
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
CUT_EDGES=tuple((i,(i+1)%8) for i in range(8))
CUT_TO_ORIGINAL=(0,1,2,3,4,0,5,6)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(parts):return tuple(sorted(tuple(sorted(b)) for b in parts))
def need(ok,msg):
 if not ok:raise ValueError(msg)
def custody():
 manifest=json.loads((HERE/'INPUTS.json').read_text())
 for item in manifest['inputs']:
  need(digest(HERE/'frozen'/item['path'])==item['sha256'],'frozen input drift: '+item['path'])
  need(digest(ROOT/item['path'])==item['sha256'],'live input drift: '+item['path'])
 return manifest

def independent_partitions(vertices):
 # Restricted-growth strings, separate from the frozen recursive insertion code.
 if not vertices:
  yield ();return
 labels=[0]*len(vertices)
 def rec(i,maximum):
  if i==len(vertices):
   yield tuple(tuple(v for v,j in zip(vertices,labels) if j==b) for b in range(maximum+1));return
  for label in range(maximum+2):
   labels[i]=label;yield from rec(i+1,max(maximum,label))
 yield from rec(1,0)
def crossing(parts,n):
 labels={v:i for i,block in enumerate(parts) for v in block}
 for a,b,c,d in itertools.combinations(range(n),4):
  if labels[a]==labels[c] and labels[b]==labels[d] and labels[a]!=labels[b]:return (a,b,c,d)
 return None

def project(parts):
 # The two pieces containing copies of z merge when the copies are identified.
 zs=[];other=[]
 for block in parts:
  image=set(CUT_TO_ORIGINAL[v] for v in block)
  if 0 in image:zs.append(image)
  else:other.append(tuple(sorted(image)))
 if zs:other.append(tuple(sorted(set().union(*zs))))
 return norm(other)
def independent_cut_options(row,pairing):
 cutrow=tuple(row[v] for v in CUT_TO_ORIGINAL)
 domains=[]
 for pair in pairing:
  vertices=tuple(i for i,c in enumerate(cutrow) if c in pair)
  good=[]
  for part in independent_partitions(vertices):
   blocks={v:i for i,b in enumerate(part) for v in b}
   if any(blocks[a]!=blocks[b] for a,b in CUT_EDGES if a in vertices and b in vertices):continue
   good.append(part)
  domains.append(good)
 result={}
 for left,right in itertools.product(*domains):
  if crossing(left+right,8):continue
  key=(project(left),project(right))
  result.setdefault(key,(left,right))
 return result

def partition_control():
 rows=sorted({h.canonical(row) for row in itertools.product(range(4),repeat=7)
              if all(row[a]!=row[b] for a,b in h.EDGES)})
 need(len(rows)==60,'proper orbit domain')
 records=[];total=0;allowed_count=0;filtered={}
 for row in rows:
  allowed=h.allowed(row)
  for pairing in h.PAIRINGS:
   old={tuple(norm(x) for x in parts):orbit for parts,orbit in h.options(row,pairing,h.EDGES)}
   cut=independent_cut_options(row,pairing)
   need(set(old)==set(cut),'cut relaxation differs: '+h.name(row))
   total+=len(old)
   if allowed:allowed_count+=len(old)
   records.append({'row':h.name(row),'pairing':pairing,'all_r_lifts_allowed':allowed,
    'partitions':[{'original_parts':key,'cut_witness':cut[key],
      'canonical_switch_successors':[h.name(s) for s in sorted(old[key])]}
      for key in sorted(old)]})
  if allowed:filtered[row]=[h.options(row,pair,h.EDGES) for pair in h.PAIRINGS]
 live=set(filtered);rounds=[]
 while True:
  dead={r for r in live if any(not any(orb<=live for part,orb in choices) for choices in filtered[r])}
  rounds.append({'live':[h.name(r) for r in sorted(live)],'removed':[h.name(r) for r in sorted(dead)]})
  if not dead:break
  live-=dead
 need(len(filtered)==26 and len(live)==22,'old fixed-point regression')
 # Bad shortcut: forbidding a cut of the z component rejects realizable abstract options.
 examples=[]
 for record in records:
  for part in record['partitions']:
   zpair=next(g for g in part['cut_witness'] if any(0 in b for b in g))
   if not any(0 in b and 5 in b for b in zpair):
    examples.append({'row':record['row'],'pairing':record['pairing'],**part});break
  if examples:break
 need(bool(examples),'missing split witness')
 return {'pins':PINS,'cut_boundary':CUT_PINS,'cut_edges':CUT_EDGES,
  'proper_canonical_rows':len(rows),'proper_labelled_rows':len(rows)*24,
  'row_pairing_cases':len(records),'old_partition_options':total,
  'old_all_r_allowed_partition_options':allowed_count,'newly_rejected_options':0,
  'records':records,'fixed_point_rounds':rounds,'split_z_witness':examples[0]}

def adjacency(edges,n):
 out=[set() for _ in range(n)]
 for a,b in edges:out[a].add(b);out[b].add(a)
 return out

def enumerate_full(adj,prefix):
 colors=list(prefix)+[-1]*(len(adj)-len(prefix));answers=[]
 if any(colors[a]>=0 and colors[a]==colors[b] for a in range(len(adj)) for b in adj[a]):return []
 def rec():
  empty=[i for i,c in enumerate(colors) if c<0]
  if not empty:answers.append(tuple(colors));return
  domains={v:set(range(4))-{colors[w] for w in adj[v]} for v in empty}
  v=min(empty,key=lambda x:(len(domains[x]),x))
  for c in sorted(domains[v]):colors[v]=c;rec()
  colors[v]=-1
 rec();return sorted(answers)

def true_graph_control():
 cells=json.loads((HERE/'frozen/artifacts/c5_cells/cells.json').read_text())
 edges={tuple(sorted(e)) for e in cells['cells']['319']['edges']}
 edges|={tuple(sorted((i,(i+1)%5))) for i in range(5)};edges=sorted(edges)
 n=8;adj=adjacency(edges,n)
 coords=((0,4),(-4,1),(-3,-3),(3,-3),(4,1),(0,0),(2,1),(-2,1))
 def orient(a,b,c):
  x,y=coords[a];xx,yy=coords[b];xxx,yyy=coords[c]
  return (xx-x)*(yyy-y)-(yy-y)*(xxx-x)
 # Strict crossing and collinearity are independently rejected for nonincident edges.
 for (a,b),(c,d) in itertools.combinations(edges,2):
  if len({a,b,c,d})<4:continue
  need(not(orient(a,b,c)*orient(a,b,d)<0 and orient(c,d,a)*orient(c,d,b)<0),'drawing crosses')
  for x,y,v in ((a,b,c),(a,b,d),(c,d,a),(c,d,b)):
   if orient(x,y,v)==0:
    need(not(all(min(coords[x][j],coords[y][j])<=coords[v][j]<=max(coords[x][j],coords[y][j]) for j in (0,1))), 'vertex on nonincident edge')
 rotation=[sorted(adj[v],key=lambda w:math.atan2(coords[w][1]-coords[v][1],coords[w][0]-coords[v][0])) for v in range(n)]
 seen=set();faces=[]
 for edge in [(a,b) for a,b in edges for a,b in ((a,b),(b,a))]:
  if edge in seen:continue
  face=[];a,b=edge
  while (a,b) not in seen:
   seen.add((a,b));face.append(a);ns=rotation[b];a,b=b,ns[(ns.index(a)-1)%len(ns)]
  faces.append(face)
 need(n-len(edges)+len(faces)==2,'Euler')
 outer=[f for f in faces if len(f)==5]
 need(len(outer)==1 and set(outer[0])==set(range(5)),'outer C5')
 triangles={tuple(vs) for vs in itertools.combinations(range(n),3) if all(tuple(sorted(e)) in edges for e in itertools.combinations(vs,2))}
 facial={tuple(sorted(f)) for f in faces if len(f)==3}
 need(triangles==facial and len(facial)==9,'all triangles facial')
 need(tuple(sorted((0,6,5))) in facial,'named inner triangle missing')
 full=enumerate_full(adj,())
 brute=[row for row in itertools.product(range(4),repeat=n) if all(row[a]!=row[b] for a,b in edges)]
 need(full==brute,'independent exhaustive full-colouring mismatch')
 patterns=[tuple(w) for w in cells['pattern_order']]
 outer_fibres={h.name(w):[h.name(f) for f in full if f[:5]==w] for w in patterns}
 counts=[len(outer_fibres[h.name(w)]) for w in patterns]
 need(counts==[1,2,1,2,1,1,0,0,1,0],'319 graph count vector')
 mask=sum(1<<i for i,c in enumerate(counts) if c)
 pin_vertices=(0,1,2,3,4,6,5)
 proper=sorted({h.canonical(r) for r in itertools.product(range(4),repeat=7)
                if all(r[a]!=r[b] for a,b in h.EDGES)})
 joint={h.name(r):[h.name(f) for f in full if tuple(f[v] for v in pin_vertices)==r] for r in proper}
 violations=[]
 for row in proper:
  fs=joint[h.name(row)]
  if fs and not h.allowed(row):
   for color in h.lifts(row):
    if not h.old_allowed((row[0],row[1],color,row[4]),row[5:]):
     violations.append({'seven_pin_row':h.name(row),'r_color':'ABCD'[color],
                        'full_U_lifts':fs})
 need(bool(violations),'graph should violate source all-r condition')
 return {'claim':'counterexample to 319 plus facial zpq forcing a nonfacial triangle',
  'vertex_order':['z','s','v','w','t','q','p','h'], 'pins':PINS,'pin_vertices':pin_vertices,
  'edges':edges,'coordinates':coords,'rotation_ccw':rotation,'faces':faces,
  'all_triangle_vertex_sets':sorted(triangles),'nonfacial_triangles':[],
  'degrees':list(map(len,adj)),'outer_mask':mask,'outer_count_vector':counts,
  'all_fixed_outer_fibres':outer_fibres,'all_sixty_seven_pin_fibres':joint,
  'all_global_full_U_lifts':[h.name(f) for f in full],
  'all_r_violation_witnesses':violations,
  'failed_source_necessary_conditions':{
   's_t_U_degree_at_least_four':False,'z_U_degree_at_least_seven':False,
   'pv_pw_qv_qw_all_absent':False,'all_r_lifts_respect_joint6':False},
  'genuine_minimum_source':False}

def build():
 manifest=custody()
 return {'schema':'r6-seven-pin-method-boundary-v1','base':manifest['BASE'],
  'binding':{'inputs_sha256':digest(HERE/'INPUTS.json'),'checker_sha256':digest(Path(__file__))},
  'partition_relaxation':partition_control(),'graph_control':true_graph_control(),
  'target_source_status':'not triggered; no source exclusion or realization',
  'general_K_infinity_status':'OPEN','new_Lean':False}

def main():
 ap=argparse.ArgumentParser();m=ap.add_mutually_exclusive_group(required=True)
 m.add_argument('--write',action='store_true');m.add_argument('--check',action='store_true')
 ap.add_argument('--certificate',type=Path,default=HERE/'certificate.json');a=ap.parse_args()
 result=build();payload=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
 if a.write:
  with a.certificate.open('x') as f:f.write(payload)
 else:need(a.certificate.read_text()==payload,'certificate differs from complete recomputation')
 p=result['partition_relaxation'];g=result['graph_control']
 print(json.dumps({'status':'PASS finite method controls; target source not triggered',
  'proper_orbits':p['proper_canonical_rows'],'row_pairings':p['row_pairing_cases'],
  'partition_options':p['old_partition_options'],'newly_rejected':p['newly_rejected_options'],
  'graph_mask':g['outer_mask'],'global_lifts':len(g['all_global_full_U_lifts']),
  'nonfacial_triangles':len(g['nonfacial_triangles'])},sort_keys=True))
if __name__=='__main__':main()
