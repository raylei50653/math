#!/usr/bin/env python3
"""Check frozen boundary implications and fixed patches, not source realization."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json
D=Path(__file__).resolve().parent
ROOT=D.parent
F=ROOT/'frozen'
LAST='audits/2026-10-20-r6-941-last-rejection-f13eb4d/'
INPUTS=[LAST+'SOURCE_CONTRACT.md',LAST+'J1/certificate.json',LAST+'J1/PROOF.md',
        LAST+'frozen/audits/2026-10-19-r6-941-leakage-b89c591/B/CORE.md',
        LAST+'frozen/audits/2026-10-19-r6-941-leakage-b89c591/B/SOURCE_CONTRACT.md']
NAMES=('a','n','R','L','q','c','s','v','w','t')
def blocks(part):
 return frozenset(frozenset(NAMES[i] for i in range(10) if part[i]==b) for b in set(part))
def face_boundary(faces):
 edges=Counter(tuple(sorted((f[i],f[(i+1)%3]))) for f in faces for i in range(3))
 assert all(v in (1,2) for v in edges.values())
 return sorted([list(e) for e,v in edges.items() if v==1])
def make():
 manifest={r['path']:r['sha256'] for r in json.loads((ROOT/'INPUTS.json').read_text())}
 hashes={}
 for path in INPUTS:
  digest=hashlib.sha256((F/path).read_bytes()).hexdigest()
  assert digest==manifest[path]
  hashes[path]=digest
 data=json.loads((F/INPUTS[1]).read_text())
 targets=[(0,1,3,2,3,1,2,e0,e1,2) for e0,e1 in ((0,1),(1,0))]
 rows=[]
 for core in targets:
  row=next(z for z in data['component_records'] if tuple(z['core'])==core)
  z0=NAMES[core.index(0,7)];z1='w' if z0=='v' else 'v'
  expected=[]
  for typ,bs in [('I',[{'a'},{'R','q',z0},{'n','t'},{'L'},{'c','s'}]),
                 ('II',[{'a'},{'R',z0},{'q'},{'n','t'},{'L','c','s'}]),
                 ('III',[{'a'},{'R'},{'q',z0},{'n','L','t'},{'c','s'}])]:
   anchor='t' if z1=='w' else 's'
   next(b for b in bs if anchor in b).add(z1)
   expected.append((typ,frozenset(map(frozenset,bs))))
  actual=[blocks(p) for p in row['splits'][2]['partitions']]
  assert set(actual)=={p for _,p in expected}
  for part in row['splits'][0]['partitions']:
   assert part[0]==part[1]==part[5]
   if part[6]==part[9]:
    assert part[7]==part[8] and part[7]!=part[0]
    assert {NAMES[i] for i in range(10) if part[i]==part[6]}=={'s','t'}
  for _,p in expected:
   same=lambda x,y:any(x in b and y in b for b in p)
   assert same('q',z0)==(same('R','q') or same('n','L'))
   assert not(same('R','q') and same('n','L'))
   assert not same('n','c') and not same('a',z0)
  rows.append({'literal_core':list(core),'z0':z0,'z1':z1,
    '03_12_types':[{'type':typ,'blocks':sorted([sorted(b) for b in bs])} for typ,bs in expected],
    '01_23_partitions':[[list(b) for b in sorted(map(tuple,map(sorted,blocks(p))))] for p in row['splits'][0]['partitions']]})
 faces=[('a','b','p'),('b','p','q'),('p','q','h'),('p','h','n'),('p','n','a'),
        ('h','q','L'),('h','L','R'),('h','R','n'),('R','n','u2'),('R','u2','u1'),('R','u1','L')]
 rim=('a','b','q','L','u1','u2','n')
 boundary=face_boundary(faces)
 assert boundary==sorted([sorted((rim[i],rim[(i+1)%7])) for i in range(7)])
 for v,star in [('p',{'a','b','q','h','n'}),('h',{'p','q','L','R','n'}),('R',{'n','h','L','u1','u2'})]:
  assert {w for f in faces if v in f for w in f if w!=v}==star
 return {'status':'necessary geometry; OPEN','input_sha256':hashes,'residual_records':rows,
  'path_bounds':{'03_R_q':{'conditional':'type I','minimum_edges':4},
                 '23_s_t':{'conditional':'s~t in 23','minimum_edges':4},
                 '12_n_L':{'conditional':'type III','minimum_edges':3,
                   'three_edge_exception':'W5 with sole interior R and exact N_G(R)=(n,h,L,u1,u2)',
                   'otherwise_minimum_edges':5}},
  'exceptional_patch':{'rim':list(rim),'interior':['p','h','R'],'faces':[list(f) for f in faces],
                       'boundary_edges':boundary},
  'scope':{'same_complete_colouring':True,'source_realized':False,'source_excluded':False,
           'smaller_bad_constructed':False,'arbitrary_cross_pair_choices_realized':False,
           'geometric_proof_automatically_verified':False}}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--build',action='store_true');ap.add_argument('--certificate',type=Path,default=D/'certificate.json');args=ap.parse_args()
 out=make()
 if args.certificate.exists():assert json.loads(args.certificate.read_text())==out
 elif args.build:
  with args.certificate.open('x') as f:json.dump(out,f,indent=2,sort_keys=True);f.write('\n')
 else:raise FileNotFoundError(args.certificate)
 print(json.dumps({'status':'PASS','residual_fibres':2,'03_12_types_per_fibre':3,'W5_exception_retained':True,'source_excluded':False},sort_keys=True))
if __name__=='__main__':main()
