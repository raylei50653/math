#!/usr/bin/env python3
"""Independent finite geometric calibration of the all-size seven-defect lemma."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
ROOT = AUDIT.parent.parent
FROZEN = AUDIT / 'frozen'
INPUT = Path('audits/2026-10-16-r6-319-joint-parity-f1faf74/B/input_graph.json')
AUTHORITIES = [
 Path('audits/2026-10-16-r6-319-continuation-f1faf74/C/PROOF.md'),
 Path('audits/2026-10-16-r6-319-complete-e98a1cc/C/PROOF.md'),
 Path('audits/2026-10-16-r6-101-nonwheel-seven-cut-120aae9/GEOMETRY.md'),
 Path('audits/2026-10-16-r6-joint-zero-c4c3d99/C/PROOF.md'),
 INPUT,
]

def sha(p):
 return hashlib.sha256(p.read_bytes()).hexdigest()

def edge(u,v): return tuple(sorted((u,v)))

def comp(vertices, edges):
 rem=set(vertices); out=[]; adj={u:set() for u in rem}
 for u,v in edges:
  if u in rem and v in rem: adj[u].add(v);adj[v].add(u)
 while rem:
  s=min(rem); todo=[s]; seen={s}
  while todo:
   u=todo.pop()
   for v in adj[u]-seen:seen.add(v);todo.append(v)
  out.append(sorted(seen)); rem-=seen
 return out

def cycle_order(vertices, edges):
 a={u:[] for u in vertices}
 for u,v in edges:a[u].append(v);a[v].append(u)
 assert all(len(x)==2 for x in a.values())
 s=min(a); p=None;u=s; out=[]
 while u not in out:
  out.append(u); v=min(x for x in a[u] if x!=p);p,u=u,v
 assert u==s and set(out)==set(vertices)
 return out

def analyse(name, faces):
 faces=[tuple(sorted(f)) for f in faces]
 assert len(set(faces))==len(faces)
 vs=sorted(set(itertools.chain.from_iterable(faces)))
 es=sorted({edge(u,v) for f in faces for u,v in itertools.combinations(f,2)})
 ad={u:{v for e in es if u in e for v in e if v!=u} for u in vs}
 assert len(vs)-len(es)+len(faces)==2
 assert len(comp(vs,es))==1 and min(map(len,ad.values()))>=4
 # Every link is one cycle: this is the complete simplicial sphere input.
 for u in vs:
  le=[tuple(v for v in f if v!=u) for f in faces if u in f]
  cycle_order(ad[u],le)
 triangles={t for t in itertools.combinations(vs,3) if all(edge(u,v) in es for u,v in itertools.combinations(t,2))}
 assert triangles==set(faces)
 de=[tuple(i for i,f in enumerate(faces) if set(e)<=set(f)) for e in es]
 assert all(len(e)==2 and e[0]!=e[1] for e in de)
 assert len(set(de))==len(de)
 dv=list(range(len(faces))); da={u:[] for u in dv}
 for i,(u,v) in enumerate(de):da[u].append((v,i));da[v].append((u,i))
 assert all(len(x)==3 for x in da.values())
 assert not any(all(edge(u,v) in {edge(*x) for x in de} for u,v in itertools.combinations(t,2)) for t in itertools.combinations(dv,3))
 cuts3=[]
 for k in range(1,4):
  for gone in itertools.combinations(range(len(es)),k):
   cs=comp(dv,[e for i,e in enumerate(de) if i not in gone])
   if len(cs)==1:continue
   assert k==3 and len(cs)==2 and min(map(len,cs))==1
   cuts3.append(list(gone))
 def pms(rem, chosen=()):
  if not rem:
   yield tuple(sorted(chosen));return
  u=min(rem)
  for v,i in sorted(da[u]):
   if v in rem:yield from pms(rem-{u,v},chosen+(i,))
 records=[]; stats={'PMs':0,'facial5':0,'facial7':0,'nonfacial7':0}
 for M0 in sorted(pms(set(dv))):
  M=set(M0);fe=[e for i,e in enumerate(de) if i not in M]
  cycles=[]
  for cv in comp(dv,fe):
   ordered=cycle_order(cv,[(u,v) for u,v in fe if u in cv])
   ci=sorted(i for i,e in enumerate(de) if i not in M and set(e)<=set(cv))
   facial=[u for u in vs if {i for i,e in enumerate(es) if u in e}==set(ci)]
   ch=sorted(i for i in M if set(de[i])<=set(cv))
   rec={'vertices':ordered,'edges':ci,'length':len(cv),'facial_centres':facial,'matching_chords':ch}
   if len(cv)==5:assert len(facial)==1 and not ch;stats['facial5']+=1
   if len(cv)==7:
    if facial:
     assert len(facial)==1 and not ch;stats['facial7']+=1
    else:
     stats['nonfacial7']+=1;assert len(ch)==1
     ab=es[ch[0]];assert sorted(len(ad[u]) for u in ab)==[4,5]
     boundary={i for i,e in enumerate(es) if ab[0] in e}^{i for i,e in enumerate(es) if ab[1] in e}
     assert boundary==set(ci)
     spokes=sorted(i for i,(u,v) in enumerate(de) if (u in cv)!=(v in cv))
     assert len(spokes)==5 and set(spokes)<=M
     outer=set(dv)-set(cv);assert outer
     assert all(any(set(e)<=set(c) and i not in M for i,e in enumerate(de)) for c in comp(outer,[e for i,e in enumerate(de) if i not in M]))
     qe=[es[i] for i in spokes];qv=set(itertools.chain.from_iterable(qe));qo=cycle_order(qv,qe)
     assert len(qo)==5
     assert {e for e in es if set(e)<=qv}==set(qe)
     rec.update({'two_centres':list(ab),'centre_degrees':[len(ad[u]) for u in ab],'cyclic_five_cut':spokes,'induced_primal_C5':qo})
   cycles.append(rec)
  records.append({'matching':list(M0),'complement_cycles':sorted(cycles,key=lambda c:c['vertices'])})
 stats['PMs']=len(records)
 return {'name':name,'vertices':vs,'primal_edges':es,'primal_faces':faces,'dual_edges':de,'trivial_three_cuts':cuts3,'stats':stats,'all_matchings':records}

def build():
 base=json.loads((AUDIT/'BASE.json').read_text())
 bindings={x['path']:x['sha256'] for x in base['inputs']}
 added=json.loads((AUDIT/'ADDITIONAL_GEOMETRY_INPUTS.json').read_text())
 assert added['base']==base['base']
 bindings.update({x['path']:x['sha256'] for x in added['inputs']})
 for p in AUTHORITIES:
  assert (FROZEN/p).is_file(),str(p)
  assert str(p) in bindings,str(p)
  assert sha(FROZEN/p)==bindings[str(p)]
 raw=json.loads((FROZEN/INPUT).read_text())
 a=analyse('frozen_flipped_icosahedral',raw['J_faces'])
 faces=[]
 for u in range(7):faces.extend([(7,u,(u+1)%7),(8,u,(u+1)%7)])
 b=analyse('seven_bipyramid',faces)
 assert a['stats']['nonfacial7']>0 and a['stats']['facial5']>0
 assert b['stats']['facial7']>0
 return {'base':base['base'],'scope':'geometric calibration only; source not triggered; full source fibres retained as universal obligation','bindings':{str(p):sha(FROZEN/p) for p in AUTHORITIES},'local_bindings':{p:sha(HERE/p) for p in ['PROOF.md','check.py']},'controls':[a,b]}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--certificate',type=Path,default=HERE/'certificate-v3.json');ap.add_argument('--create',action='store_true');ap.add_argument('--seed',type=int,default=0);args=ap.parse_args()
 # Seed is accepted to calibrate order independence; canonical reconstruction
 # does not depend on hash seed or pseudo-random sampling.
 cert=json.loads(json.dumps(build()));data=json.dumps(cert,sort_keys=True,indent=2)+'\n'
 if args.create:
  with args.certificate.open('x') as f:f.write(data)
 else:
  assert json.loads(args.certificate.read_text())==cert,'certificate differs from full independent reconstruction'
 print(json.dumps({'ok':True,'seed':args.seed,'certificate_sha256':hashlib.sha256(data.encode()).hexdigest(),'stats':[c['stats'] for c in cert['controls']]},sort_keys=True))
if __name__=='__main__':main()
