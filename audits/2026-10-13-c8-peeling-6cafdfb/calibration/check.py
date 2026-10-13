#!/usr/bin/env python3
"""Paper-bounded m=10 calibration: complete fixed-frame fibres and full joins."""
from pathlib import Path
import argparse
from collections import defaultdict, deque
import gzip
import hashlib
import itertools
import json

ROOT = Path(__file__).resolve().parent
C = tuple(f'c{i}' for i in range(8))
T = tuple(f't{i}' for i in range(8))
I = T + ('r', 's')
B = tuple(f'b{i}' for i in range(5))
B_ROWS = ('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
QUERIES = (
 ('c15-933',(0,1,2,0,0),933), ('c18-933',(0,2,1,0,0),933),
 ('c04-941',(0,0,1,0,2),941), ('c07-941',(0,0,2,0,1),941),
 ('c15-941',(0,1,2,0,0),941), ('c18-941',(0,2,1,0,0),941),
 ('c20-941',(1,0,0,0,2),941), ('c30-941',(2,0,0,0,1),941),
)

def canonical(word):
 names = {}
 return ''.join(str(names.setdefault(c,len(names))) for c in word)

ALL_T_ROWS = tuple(''.join(map(str,w)) for w in itertools.product(range(4),repeat=8)
                   if all(w[i] != w[(i+1)%8] for i in range(8)))
C_ROWS = tuple(w for w in ALL_T_ROWS if canonical(w)==w)
assert len(ALL_T_ROWS)==6564 and len(C_ROWS)==274


def edge(a,b):
 return tuple(sorted((a,b)))


def assemble(vertices, outer, faces):
 edges = sorted({edge(a,b) for f in faces for a,b in zip(f,f[1:]+f[:1])})
 adj = {v:set() for v in vertices}
 for a,b in edges:
  adj[a].add(b); adj[b].add(a)
 assert len(set(vertices))==len(vertices)
 assert len(vertices)-len(edges)+len(faces)==1
 assert len(edges)==3*(len(vertices)-len(outer))+2*len(outer)-3
 darts={}
 for fid,f in enumerate(faces):
  assert len(set(f))==3
  for a,b in zip(f,f[1:]+f[:1]):
   assert (a,b) not in darts
   darts[a,b]=fid
 outer_edges={edge(a,b) for a,b in zip(outer,outer[1:]+outer[:1])}
 for a,b in edges:
  assert int((a,b) in darts)+int((b,a) in darts)==(1 if (a,b) in outer_edges else 2)
 for a,b in zip(outer,outer[1:]+outer[:1]):
  assert (a,b) in darts and (b,a) not in darts
 # Vertex links are single cycles internally and single paths on the outer rim.
 for v in vertices:
  link=defaultdict(set)
  for f in faces:
   if v in f:
    a,b=[w for w in f if w!=v]
    link[a].add(b);link[b].add(a)
  assert set(link)==adj[v]
  assert all(len(z) in (1,2) for z in link.values())
  assert sum(len(z)==1 for z in link.values())==(2 if v in outer else 0)
  reached={next(iter(link))};pending=list(reached)
  while pending:
   for w in link[pending.pop()]:
    if w not in reached:reached.add(w);pending.append(w)
  assert reached==set(link)
 return {'vertices':tuple(vertices),'outer':tuple(outer),'edges':edges,'faces':tuple(faces),'adj':adj}


def kinds():
 for a in range(4):yield 'CHORD-55',a,4
 for a in range(8):yield 'EDGE-35',a,3
 for a in range(4):yield 'EDGE-44',a,4


def core_graph(kind,a,d):
 b=(a+d)%8
 r_arc=[(a+j)%8 for j in range(d)]
 faces=[(T[i],T[(i+1)%8],'r' if i in r_arc else 's') for i in range(8)]
 if kind=='CHORD-55':faces += [(T[b],T[a],'r'),(T[a],T[b],'s')]
 else:faces += [('r',T[b],'s'),('s',T[a],'r')]
 return assemble(I,T,faces)


def inner_graph(core):
 faces=[]
 for i in range(8):
  faces += [(C[i],C[(i+1)%8],T[i]),(C[i],T[i],T[(i-1)%8])]
 faces += list(core['faces'])
 return assemble(C+I,C,faces)


def collar_faces(e):
 faces=[]
 names=['a0']
 for i in range(1,5):names += [f'y{i}_{j}' for j in range(1,e[i]+1)]+[f'a{i}']
 names += [f'y0_{j}' for j in range(1,e[0]+1)]
 rename=dict(zip(names,C))
 for i in range(5):
  faces.append((B[i],B[(i+1)%5],rename[f'a{i}']))
  fan=[f'a{(i-1)%5}']+[f'y{i}_{j}' for j in range(1,e[i]+1)]+[f'a{i}']
  for a,b in zip(fan,fan[1:]):faces.append((B[i],rename[b],rename[a]))
 return faces,names


def whole_graph(h,e):
 faces,names=collar_faces(e)
 return assemble(B+C+I,B,faces+list(h['faces'])),names


def full_lifts(g,pinned=None):
 vertices=g['vertices'];adj=g['adj'];colors=dict(pinned or {})
 assert all(colors.get(a)!=colors.get(b) for a,b in g['edges'] if a in colors and b in colors)
 result=[]
 def visit():
  if len(colors)==len(vertices):
   result.append(''.join(str(colors[v]) for v in vertices));return
  candidates=[]
  for index,v in enumerate(vertices):
   if v in colors:continue
   legal=tuple(c for c in range(4) if all(colors.get(w)!=c for w in adj[v]))
   candidates.append((len(legal),-sum(w in colors for w in adj[v]),index,v,legal))
  _,_,_,v,legal=min(candidates)
  for c in legal:
   colors[v]=c;visit();del colors[v]
 visit()
 return sorted(result)


def simple_small_cycles(g):
 adj=g['adj'];result=set()
 def walk(start,path):
  for w in sorted(adj[path[-1]]):
   if w==start and len(path)>=3:
    if path[1]<path[-1]:result.add(tuple(path))
   elif len(path)<5 and w>start and w not in path:walk(start,path+[w])
 for v in sorted(adj):walk(v,[v])
 return sorted(result)


def cap_check(g):
 faces=g['faces'];outer=g['outer'];edges=g['edges']
 incident=defaultdict(list)
 for i,f in enumerate(faces):
  for a,b in zip(f,f[1:]+f[:1]):incident[edge(a,b)].append(i)
 for a,b in zip(outer,outer[1:]+outer[:1]):incident[edge(a,b)].append(-1)
 dual=defaultdict(list)
 for e,fl in incident.items():
  assert len(fl)==2
  dual[fl[0]].append((fl[1],e));dual[fl[1]].append((fl[0],e))
 counts=defaultdict(int)
 for cyc in simple_small_cycles(g):
  barrier={edge(a,b) for a,b in zip(cyc,cyc[1:]+cyc[:1])}
  reached={-1};q=deque([-1])
  while q:
   for f,e in dual[q.popleft()]:
    if e not in barrier and f not in reached:reached.add(f);q.append(f)
  inside_faces=[f for i,f in enumerate(faces) if i not in reached]
  inside=set().union(*map(set,inside_faces))-set(cyc)
  n=len(cyc)
  if n in (3,4):assert not inside,(cyc,inside)
  else:
   assert len(inside)<=1,(cyc,inside)
   if inside:
    z=next(iter(inside))
    assert all(v in g['adj'][z] for v in cyc)
    assert len(inside_faces)==5
  counts[f'C{n}_{"W5" if inside else "empty"}']+=1
 return dict(sorted(counts.items()))


def core_fibres(core):
 result={row:[] for row in ALL_T_ROWS}
 for lift in full_lifts(core):result[lift[:8]].append(lift)
 return result


def c_transfer(core_f, row):
 result=[]
 for trow,lifts in core_f.items():
  if lifts and all(trow[i]!=row[i] and trow[i]!=row[(i+1)%8] for i in range(8)):
   result.extend(row+lift for lift in lifts)
 return sorted(result)


def raw_c_transfer(representatives,row):
 # One single color permutation acts on the entire H lift, with unused colors
 # completed by increasing order. No Q, C, or I piece gets a separate frame.
 names={};inv={}
 for c in row:
  if c not in names:names[c]=str(len(names));inv[names[c]]=c
 for c in '0123':
  if c not in inv:inv[c]=next(x for x in '0123' if x not in inv.values())
 return sorted(''.join(inv[c] for c in lift) for lift in representatives[canonical(row)])


def b_transfer(hfib,g,row):
 # Enumerate only the actual B-C collar, then take the full H fibre in the
 # SAME literal C row. Empty collar or H fibres remain empty.
 collar_edges=[e for e in g['edges'] if not (e[0] in I or e[1] in I)]
 adj={v:set() for v in B+C}
 for a,b in collar_edges:adj[a].add(b);adj[b].add(a)
 collar={'vertices':B+C,'edges':collar_edges,'adj':adj}
 result=[]
 for lift in full_lifts(collar,dict(zip(B,map(int,row)))):
  crow=lift[5:]
  result.extend(row+h for h in raw_c_transfer(hfib,crow))
 return sorted(result)


def public_graph(g,rename=None):
 rename=rename or {}
 def name(v):return rename.get(v,v)
 return {'vertices':tuple(map(name,g['vertices'])),'outer':tuple(map(name,g['outer'])),
   'edges':sorted(edge(name(a),name(b)) for a,b in g['edges']),
   'oriented_inner_faces':tuple(tuple(map(name,f)) for f in g['faces'])}


def calculate(progress=False):
 frozen_inputs_check()
 cases=[];sources=[]
 for kind,a,d in kinds():
  identifier=f'{kind}-t{a}-t{(a+d)%8}'
  core=core_graph(kind,a,d);h=inner_graph(core)
  assert all(len(h['adj'][v])>=4 for v in C)
  assert all(len(h['adj'][v])>=5 for v in I)
  assert all(set(h['adj'][T[i]])&set(C)=={C[i],C[(i+1)%8]} for i in range(8))
  assert not any(set(h['adj'][v])&set(C) for v in ('r','s'))
  assert all(edge(a,b) in {edge(C[i],C[(i+1)%8]) for i in range(8)} for a,b in h['edges'] if a in C and b in C)
  caps=cap_check(h)
  cf=core_fibres(core)
  hf={}
  for row in C_ROWS:
   direct=full_lifts(h,dict(zip(C,map(int,row))))
   transfer=c_transfer(cf,row)
   assert direct==transfer,(identifier,row,'C transfer')
   hf[row]=direct
  cases.append({'id':identifier,'type':kind,'clockwise_arc_length':d,'endpoints':[T[a],T[(a+d)%8]],
    'H':public_graph(h),'Q':public_graph(core),'cap_counts':caps,
    'core_literal_row_order':ALL_T_ROWS,'core_complete_fibres':cf,
    'C_normalized_row_order':C_ROWS,'H_complete_fibres':hf,
    'H_fibre_counts':[len(hf[row]) for row in C_ROWS]})
  for query,e,target in QUERIES:
   g,names=whole_graph(h,e)
   bf={}
   for row in B_ROWS:
    direct=full_lifts(g,dict(zip(B,map(int,row))))
    transfer=b_transfer(hf,g,row)
    assert direct==transfer,(identifier,query,row,'B transfer')
    bf[row]=direct
   counts=[len(bf[row]) for row in B_ROWS]
   sigma=sum(1<<i for i,v in enumerate(counts) if v)
   sources.append({'id':identifier+'__'+query,'H_id':identifier,'contract':query,'e':e,
     'target':target,'original_C_names':names,'graph':public_graph(g,dict(zip(C,names))),
     'B_row_order':B_ROWS,'complete_fibres':bf,'counts':counts,'sigma':sigma})
  if progress:print(json.dumps({'case_complete':identifier,'H_lifts':sum(map(len,hf.values())),
      'Q_lifts':sum(map(len,cf.values())),'source_sigmas':[s['sigma'] for s in sources[-8:]]}),flush=True)
 return {'base':'6cafdfb02fe5892a49eee21f92aea2369a25c022',
   'scope':'complete m=10 H classification under stated source contract, then complete literal colouring controls; not larger-size enumeration',
   'source_realizability':'not triggered','C_rows':len(C_ROWS),'literal_C_rows':len(ALL_T_ROWS),
   'types':{'CHORD-55':4,'EDGE-35':8,'EDGE-44':4},'H_cases':cases,'B_source_controls':sources,
   'transfer_validation':'direct whole graph equals same-row full join in every saved fibre, including empty fibres'}


def stable(value):return json.loads(json.dumps(value))


def frozen_inputs_check():
 # Fail closed on every frozen enclosing-audit input, including the literal
 # former source graphs. Reconstruct their B-C collars from actual named edges
 # and original oriented faces, independently of the former constructor code.
 root_manifest=json.loads((ROOT.parent/'INPUTS.json').read_text())
 for name,entry in root_manifest['inputs'].items():
  contents=(ROOT.parent/entry['frozen']).read_bytes()
  assert hashlib.sha256(contents).hexdigest()==entry['sha256'],name
 p=ROOT.parent/'frozen/audits/2026-10-13-c8-followup-6cafdfb/check.py'
 expected=ROOT/'INPUTS.json'
 manifest=json.loads(expected.read_text())
 assert hashlib.sha256(p.read_bytes()).hexdigest()==manifest['old_checker_sha256']
 frozen_certificate=ROOT.parent/'frozen/audits/2026-10-13-c8-followup-6cafdfb/certificate.json.gz'
 original=json.loads(gzip.decompress(frozen_certificate.read_bytes()))
 assert [(c['id'],tuple(c['e']),c['target']) for c in original['cases']]==list(QUERIES)
 for c in original['cases']:
  generated_faces,names=collar_faces(tuple(c['e']))
  rename=dict(zip(C,names));named_faces=[tuple(rename.get(v,v) for v in f) for f in generated_faces]
  old_names=c['outer_B']+c['collar_C']
  assert old_names==list(B)+names
  old_set=set(old_names)
  original_edges={tuple(e) for e in c['edges'] if set(e)<=old_set}
  original_faces=[tuple(f) for f in c['oriented_inner_faces'] if set(f)<=old_set]
  assert {edge(a,b) for f in named_faces for a,b in zip(f,f[1:]+f[:1])}==original_edges
  assert named_faces==original_faces


def validate(data,progress=False):
 frozen_inputs_check()
 expected=stable(calculate(progress))
 compare_certificate(data,expected)
 return expected


def compare_certificate(data,expected):
 assert data==expected, 'literal graph, cap, row, or complete fibre mismatch'


def main():
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true')
 p.add_argument('--negative',action='store_true');args=p.parse_args()
 path=ROOT/'certificate.json.gz'
 if args.write:
  data=calculate(True)
  with path.open('xb') as f:f.write(gzip.compress((json.dumps(data,sort_keys=True,separators=(',',':'))+'\n').encode(),mtime=0))
  expected=stable(data)
 else:
  data=json.loads(gzip.decompress(path.read_bytes()));expected=validate(data,True)
 if args.negative:
  for name,mutate in (
   ('deleted full lift',lambda d:d['B_source_controls'][0]['complete_fibres']['01012'].pop()),
   ('changed literal edge',lambda d:d['H_cases'][0]['H']['edges'].pop()),
   ('deleted empty core fibre',lambda d:d['H_cases'][0]['core_complete_fibres'].pop(next(r for r,f in d['H_cases'][0]['core_complete_fibres'].items() if not f))),
   ('deleted empty C fibre',lambda d:d['H_cases'][0]['H_complete_fibres'].pop(next(r for r,f in d['H_cases'][0]['H_complete_fibres'].items() if not f))),
  ):
   damaged=stable(data);mutate(damaged)
   # Recompute once above; compare every literal saved field to the verified
   # object. The controls target loss of witnesses, geometry, or empty rows.
   try:compare_certificate(damaged,expected)
   except AssertionError:pass
   else:raise AssertionError('negative control was accepted: '+name)
 counts={}
 for s in data['B_source_controls']:counts[str(s['sigma'])]=counts.get(str(s['sigma']),0)+1
 summary={'H_cases':len(data['H_cases']),'source_controls':len(data['B_source_controls']),
  'C_rows_per_H':len(C_ROWS),'core_literal_rows_per_H':len(ALL_T_ROWS),'type_counts':data['types'],
  'source_sigma_counts':counts,'C_fibres':sum(len(c['H_complete_fibres']) for c in data['H_cases']),
  'C_nonempty_fibres':sum(bool(f) for c in data['H_cases'] for f in c['H_complete_fibres'].values()),
  'C_full_lifts':sum(len(f) for c in data['H_cases'] for f in c['H_complete_fibres'].values()),
  'B_fibres':sum(len(c['complete_fibres']) for c in data['B_source_controls']),
  'B_full_lifts':sum(len(f) for c in data['B_source_controls'] for f in c['complete_fibres'].values()),
  'caps':'pass C3/C4 empty and C5 empty or W5 by original-face dual flood',
  'direct_vs_layered_transfer':'pass, every complete fixed-frame fibre'}
 if args.write:(ROOT/'RESULTS.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
 print(json.dumps(dict(summary,negative_controls=args.negative),sort_keys=True))

if __name__=='__main__':main()
