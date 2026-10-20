#!/usr/bin/env python3
"""Exact same-source J1 01021 fibre refinement; no source existence claim."""
from pathlib import Path
from itertools import product
from collections import Counter
import argparse,hashlib,importlib.util,json
D=Path(__file__).resolve().parent;F=D.parent/'frozen'
MODEL=F/'audits/2026-10-19-r6-941-quotients-13dc5ff/A/model.py'
spec=importlib.util.spec_from_file_location('frozen_model',MODEL)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
NAMES=('a','n','R','L','q','c','s','v','w','t')
SPLITS=((0,1,2,3),(0,2,1,3),(0,2,3,1))
def extend_right_partition(core,r,sep,part):
 colors=tuple(core)+(0,1,r);parent=list(range(13))
 def root(i):
  while parent[i]!=i:i=parent[i]
  return i
 def join(a,b):parent[root(a)]=root(b)
 for a in range(10):
  for b in range(a):
   if part[a]==part[b]:join(a,b)
 # x=10,y=11,r=12; all right cap edges, including its interfaces.
 for a,b in ((0,11),(11,10),(10,5),(10,6),(11,9),(12,10),(12,11),(12,6),(12,7),(12,8),(12,9)):
  if sep[colors[a]]//2==sep[colors[b]]//2:join(a,b)
 return tuple(root(i) for i in range(13))
def make():
 manifest={e['path']:e for e in json.loads((D.parent/'INPUTS.json').read_text())}
 model_name=MODEL.relative_to(F).as_posix();raw=MODEL.read_bytes()
 assert hashlib.sha256(raw).hexdigest()==manifest[model_name]['sha256'] and len(raw)==manifest[model_name]['bytes']
 I=m.interfaces();K=m.kempe(10,I['ten']);ix={t:i for i,t in enumerate(I['ten'])};i8={t:i for i,t in enumerate(I['eight'])}
 M=[[0]*274 for _ in m.ROWS]
 for j,row in enumerate(m.ROWS):
  x,y,a,b,c=map(int,row)
  for n,R,L,q in product(range(4),repeat=4):
   e=(a,n,R,L,q,c,x,y)
   if m.proper(e) and b not in (a,c,q) and b==L and a!=R:M[j][i8[m.canonical(e)]]+=1
 C=[[sum(M[j][e]*dict(I['T'][e]).get(i,0) for e in range(274) if M[j][e]) for i in range(2461)] for j in range(10)]
 initial=set(range(2461))-{i for i in range(2461) if any(I['C']['G'][j][i] for j in (1,4,6)) or I['C']['Q1'][9][i] or C[4][i] or C[6][i]}
 live,rounds=m.close(K,initial);live=set(live)
 assert len(live)==1973
 records=[];left=[]
 for n,R,L,q in product(range(4),repeat=4):
  e=(0,n,R,L,q,1,0,1);proper=m.proper(e) and 2 not in (0,1,q);j1=proper and L==2 and R!=0
  lifts=[(p,h) for p,h in product(range(4),repeat=2) if proper and p not in (0,2,q,n,h) and h not in (p,q,L,R,n)]
  records.append({'nRLq':[n,R,L,q],'E_proper_and_b_legal':proper,'J1':j1,'original_ph':lifts})
  if j1:left.append((n,R,L,q,lifts))
 right=[];right_empty=0
 for s,v,w,t,r in product(range(4),repeat=5):
  okay=(s!=1 and t!=0 and s!=v and v!=w and w!=t and r not in (s,v,w,t,0,1) and s!=0 and t!=1)
  if okay:right.append((s,v,w,t,r))
  else:right_empty+=1
 assert len(right)==4 and right_empty==1020
 cap=[];targets=[]
 for n,R,L,q,lifts in left:
  for s,v,w,t,r in right:
   core=(0,n,R,L,q,1,s,v,w,t);idx=ix[m.canonical(core)]
   row={'core':core,'r':r,'core_id':idx,'original_ph':lifts,'survives':idx in live}
   cap.append(row)
   if idx in live:targets.append(row)
 assert len(left)==8 and len(cap)==32 and len(targets)==8
 assert len([r for r in cap if not r['original_ph']])==12
 assert all(t['core'][1:5] in ((1,3,2,0),(1,3,2,3)) for t in targets)
 coeff=Counter(r['core_id'] for r in targets)
 assert all(C[1][i]==coeff.get(i,0) for i in live)
 good=[j for j,col in enumerate(K['columns']) if all(K['rowids'][r] in live for r,v in col)]
 covering={}
 for j in good:
  for r,v in K['columns'][j]:covering.setdefault(r,[]).append(j)
 hi={t:i for i,t in enumerate(K['hrows'])};part_records=[]
 for target in targets:
  core=target['core'];splits=[]
  for sep in SPLITS:
   ht=m.hc(tuple(sep[c] for c in core));row=hi[ht];cols=covering[row]
   parts=[K['descriptions'][j][1] for j in cols]
   # A full complementary-pair orbit keeps its boundary partition unchanged.
   assert all(tuple(sep[core[a]]//2==sep[core[b]]//2 for a in range(10) for b in range(10) if p[a]==p[b])==tuple(True for a in range(10) for b in range(10) if p[a]==p[b]) for p in parts)
   together=[(NAMES[a],NAMES[b]) for a in range(10) for b in range(a+1,10) if all(p[a]==p[b] for p in parts)]
   apart=[(NAMES[a],NAMES[b]) for a in range(10) for b in range(a+1,10) if sep[core[a]]//2==sep[core[b]]//2 and all(p[a]!=p[b] for p in parts)]
   extended=[extend_right_partition(core,target['r'],sep,p) for p in parts]
   splits.append({'extended_E_partitions':extended,'color_map':sep,'H_row':row,'columns':cols,'partitions':parts,'forced_together':together,'forced_apart':apart})
  assert ('a','c') in splits[0]['forced_together']
  assert ('a','L') in splits[1]['forced_apart']
  assert ('n','c') in splits[2]['forced_apart']
  assert all(p[1]==p[11] and p[1]!=p[5] and p[0]!=p[10] for p in splits[2]['extended_E_partitions'])
  part_records.append({'core':core,'r':target['r'],'core_id':target['core_id'],'splits':splits})
 # Fixed literal complete core counts have coefficient one, without S4 factors.
 out={'status':'necessary theorem; J1 last rejection remains OPEN','source_realized':False,
      'source_contract':'../SOURCE_CONTRACT.md','model_sha256':hashlib.sha256(MODEL.read_bytes()).hexdigest(),
      'family_sha256':hashlib.sha256(json.dumps(K['columns'],separators=(',',':')).encode()).hexdigest(),
      'all_256_left_records':records,'right_lifts':right,'empty_right_assignments':right_empty,
      'all_32_J1_T_cap_records':cap,'initial_live':sorted(initial),'deletion_rounds':rounds,'final_live':sorted(live),
      'eight_surviving_literal_fibres':targets,'exact_T_coefficients':sorted(coeff.items()),'component_records':part_records,
      'negative_controls':{'wrong_n_equals_R_rejected':any(r['core'][1]!=r['core'][2] for r in targets),
       'false_a_L_02_connection_rejected':all(('a','L') in z['splits'][1]['forced_apart'] for z in part_records),
       'false_n_c_12_connection_rejected':all(('n','c') in z['splits'][2]['forced_apart'] for z in part_records),
       'claim_T_forced_empty_rejected':bool(targets)}}
 return json.loads(json.dumps(out))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--build',action='store_true');ap.add_argument('--certificate',type=Path,default=D/'certificate.json');args=ap.parse_args()
 out=make()
 if args.certificate.exists():assert json.loads(args.certificate.read_text())==out
 elif args.build:
  with args.certificate.open('x') as f:json.dump(out,f,separators=(',',':'));f.write('\n')
 else:raise FileNotFoundError(args.certificate)
 print(json.dumps({'status':'PASS','core_live':len(out['final_live']),'J1_T_literal_fibres':len(out['eight_surviving_literal_fibres']),'source_realized':False,'last_rejection':'OPEN'},sort_keys=True))
if __name__=='__main__':main()
