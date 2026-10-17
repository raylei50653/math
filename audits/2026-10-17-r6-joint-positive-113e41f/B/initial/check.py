#!/usr/bin/env python3
"""Local independent calibration; no finite source-realizability claim."""
from hashlib import sha256
from itertools import combinations, permutations, product
from pathlib import Path
import argparse, json
P=Path(__file__).resolve().parent
R=P.parent
F=R/'frozen'
C=F/'audits/2026-10-16-r6-319-joint-parity-f1faf74/C'
COL=range(4)
PAT=('ABABC','ABACB','ABACD','ABCAB','ABCAC','ABCAD','ABCBC','ABCBD','ABCDB','ABCDC')
def canon(row):
 d={};return tuple(d.setdefault(x,len(d)) for x in row)
def bit(row):return 1<<PAT.index(''.join('ABCD'[x] for x in canon(row)))
def edge(a,b):return tuple(sorted((a,b)))
def main():
 inputs=json.loads((P/'INPUTS.json').read_text())
 for f in inputs['inputs']:
  q=R/f['path']
  if sha256(q.read_bytes()).hexdigest()!=f['sha256']:raise ValueError('input hash changed: '+f['path'])
 base=json.loads((C/'certificate.json').read_text())
 for f in base['outputs']:
  if sha256((C/f['path']).read_bytes()).hexdigest()!=f['sha256']:raise ValueError('source worker seal changed: '+f['path'])
 final=json.loads((C/'final-step-certificate.json').read_text())
 compulsory=['ABACDBCD','ABACDBDC','ABCADBCD','ABCADBDC','ABCDABCD','ABCDABDC']
 assert final['mandatory_rows']==compulsory
 assert all(set(r[1:5])==set('ABCD') for r in compulsory)
 literal=sorted(set(compulsory)|{s.translate(str.maketrans('CD','DC')) for s in compulsory})
 assert len(literal)==12
 hnames=('z','s','j','i','w','t','p','q')
 nonedges=[]
 for a,b in [('i','p'),('i','q'),('j','p'),('j','q'),('z','i'),('z','j')]:
  ws=[s for s in literal if s[hnames.index(a)]==s[hnames.index(b)]]
  assert ws
  nonedges.append({'pair':[a,b],'complete_compulsory_witnesses':ws})
 # Independent complete nine-pin / five-restoration local table.
 source=json.loads((C/'full-source-local-fibres.json').read_text())
 names=('c','s','j','i','w','t','a','p','q','v','r','x','y','b')
 ext=tuple((k,(k+1)%9) for k in range(9))
 raw=[('v',x) for x in ('s','j','i','w','r')]
 raw += [('r',x) for x in ('s','w','t','x','y')]
 raw += [('x',x) for x in ('c','s','y')]
 raw += [('y',x) for x in ('t','a')]
 raw += [('b',x) for x in ('a','c','p','q')]
 attach=tuple((names.index(a),names.index(b)) for a,b in raw)
 proper={canon(r) for r in product(COL,repeat=9) if all(r[a]!=r[b] for a,b in ext)}
 stored={f['row']:f['all_lifts'] for f in source['fibres']}
 assert len(proper)==len(stored)==820
 empty=total=0
 for rr in sorted(proper):
  row=''.join('ABCD'[x] for x in rr); ll=[]
  for add in product(COL,repeat=5):
   r=rr+add
   if all(r[a]!=r[b] for a,b in attach):ll.append(list(add)+[bit((r[11],r[12],r[6],r[13],r[0]))])
  assert ll==stored[row],('original full fibre differs',row)
  empty+=not ll;total+=len(ll)
 assert (empty,total)==(475,648)
 full=json.loads((C/'full-source-exploration.json').read_text())
 combined=json.loads((C/'combined-source-exploration.json').read_text())
 fixed=[]
 for f,c in zip(full['results'],combined):
  assert f['source_mask']==c['source']
  assert f['source_lift_support']==f['source_mask']
  assert c['H_fixed']==final['input_rows']
  assert f['U_lift_support']==319
  S=f['source_mask']
  assert all(all(x[-1]&S for x in stored[row]) for row in f['fixed_rows'])
  fixed.append({'source_mask':S,'fixed_F_rows':len(f['fixed_rows']),'all_original_lifts_respected':True,'H_upper_rows':len(c['H_fixed'])})
 assert [x['source_mask'] for x in fixed]==[932,933,941]
 # Every possible local connector pattern for a marked six-cycle.
 vertices=('v','w','p','q','m','j','i','h')
 banned={edge(a,b) for a in ('v','w','i','j') for b in ('p','q')}
 banned|={edge('v',a) for a in vertices if a not in ('v','m','j','i','w')}
 cycles=set()
 for rest in permutations(tuple(x for x in vertices if x!='v'),5):
  r=('v',)+rest
  if not {'w','p','q'}<=set(r):continue
  es={edge(r[k],r[(k+1)%6]) for k in range(6)}
  if edge('v','w') not in es or edge('p','q') not in es or es&banned:continue
  cycles.add(min(r,('v',)+tuple(reversed(rest))))
 assert cycles=={('v','m','p','q','h','w'),('v','m','q','p','h','w')}
 # Enumerate ALL empty pentagon triangulations rather than choose one.
 boundary=('t','p','q','h','w')
 rim={edge(boundary[k],boundary[(k+1)%5]) for k in range(5)}
 diags=set(combinations(boundary,2))
 diags={edge(*e) for e in diags}-rim
 def crosses(e,f):
  if set(e)&set(f):return False
  a,b=sorted(boundary.index(x) for x in e)
  c,d=sorted(boundary.index(x) for x in f)
  return (a<c<b<d) or (c<a<d<b)
 triangulations=[set(ds) for ds in combinations(sorted(diags),2) if not crosses(*ds)]
 assert len(triangulations)==5
 banq={edge('t','q'),edge('p','w'),edge('q','w')}
 allowed=[ds for ds in triangulations if not ds&banq]
 assert allowed==[{edge('t','h'),edge('p','h')}]
 outside=[('t','p','a'),('a','p','b'),('b','p','q')]
 caps=[('empty',[('t','p','h'),('p','q','h'),('t','h','w')]),('W5',[(boundary[k],boundary[(k+1)%5],'u') for k in range(5)])]
 cap_records=[]
 for kind,inside in caps:
  faces=outside+inside
  adj={}
  for tri in faces:
   if 'p' in tri:
    a,b=[x for x in tri if x!='p']
    adj.setdefault(a,set()).add(b);adj.setdefault(b,set()).add(a)
  assert len(adj)==5 and all(len(n)==2 for n in adj.values())
  seen=set();stack=['t']
  while stack:
   x=stack.pop()
   if x in seen:continue
   seen.add(x);stack.extend(adj[x]-seen)
  assert seen==set(adj)
  cap_records.append({'kind':kind,'faces':inside,'p_neighbours':sorted(adj),'p_link_cycle':[[x,sorted(adj[x])] for x in sorted(adj)],'original_degree_p':5,'original_degree_a':4,'excluded_by_low_p':True})
 # A cyclic component costs >=4, every additional component >=3.
 side_cases=[{'components':k,'minimum_cut':4+3*(k-1),'six_cut_possible':4+3*(k-1)<=6} for k in range(1,4)]
 assert all(not c['six_cut_possible'] for c in side_cases[1:])
 return {'base':inputs['base'],'authority':'local calibration plus conditional arbitrary-size source proof; not source realization','pins':hnames,'mandatory_complete_H_rows':compulsory,'literal_complete_H_rows':literal,'nonedges':nonedges,'original_fibres':{'proper_normalized_rows':820,'empty_fibres':empty,'all_five_vertex_lifts':total,'fixed_masks':fixed},'six_cycle_connector_patterns':[list(x) for x in sorted(cycles)],'pentagon_triangulations':len(triangulations),'allowed_empty_cap_diagonals':[sorted(map(list,ds)) for ds in allowed],'cap_checks':cap_records,'cyclic_cut_side_component_lower_bounds':side_cases,'no_six_cycle_through_e_f':'PROVED conditional on original v5','v5_exclusion':'OPEN','W110_plus_W101_positive':'OPEN','source_instances':0,'source_coverage':'not triggered'}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--check',type=Path);ap.add_argument('--output',type=Path);args=ap.parse_args()
 result=json.loads(json.dumps(main()))
 if args.check:
  if result!=json.loads(args.check.read_text()):raise ValueError('certificate differs from independent recomputation')
  print(json.dumps({'status':'PASS','new_nonedges':6,'original_fibres':820,'connector_patterns':2,'cap_cases':2,'v5_exclusion':'OPEN','joint_positive':'OPEN'},sort_keys=True))
 elif args.output:
  with args.output.open('x') as f:f.write(json.dumps(result,indent=2,sort_keys=True)+'\n')
  print('created '+str(args.output))
 else:print(json.dumps(result,indent=2,sort_keys=True))
