#!/usr/bin/env python3
"""Read-only exact support closure for two specific smaller candidates."""
import importlib.util,json,hashlib,argparse
from pathlib import Path
from itertools import product
D=Path(__file__).resolve().parent;F=D.parent/'frozen'
ap=argparse.ArgumentParser();ap.add_argument('--build',action='store_true');ap.add_argument('--certificate',type=Path,default=D/'comparisons.json');args=ap.parse_args()
spec=importlib.util.spec_from_file_location('frozen_model',F/'audits/2026-10-19-r6-941-quotients-13dc5ff/A/model.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
I=m.interfaces();K=m.kempe(10,I['ten']);ix={t:i for i,t in enumerate(I['eight'])}
cat=set(map(int,json.loads((F/'audits/2026-10-18-smaller-bad-counts-e1617a2/frozen/artifacts/c5_cells/cells.json').read_text())['cells']))
matrices={}
for graph in ('J1','J2'):
 M=[[0]*274 for _ in range(10)]
 for j,row in enumerate(m.ROWS):
  x,y,a,b,c=map(int,row)
  for n,R,L,q in product(range(4),repeat=4):
   e=(a,n,R,L,q,c,x,y)
   if not m.proper(e) or b in (a,c,q):continue
   good=(b==L and a!=R) if graph=='J1' else (a!=L and a!=R and b!=L)
   if good:M[j][ix[m.canonical(e)]]+=1
 C=[[0]*2461 for _ in range(10)]
 for j,row in enumerate(M):
  for e,v in enumerate(row):
   if v:
    for i,w in I['T'][e]:C[j][i]+=v*w
 matrices[graph]={'E':M,'F':C}
zeroG={i for i in range(2461) if any(I['C']['G'][j][i] for j in (1,4,6))}
positiveG=[j for j in range(10) if 941>>j&1]
records=[]
for branch,graph in (('Q1','J1'),('Q2','J2')):
 C=matrices[graph]['F'];basezero=zeroG|{i for i,v in enumerate(I['C'][branch][9]) if v}
 survivors=[];failures=[]
 for mask in sorted(cat):
  zero=basezero|{i for i in range(2461) if any(C[j][i] for j in range(10) if not mask>>j&1)}
  live,rounds=m.close(K,set(range(2461))-zero)
  failed=[['G',j] for j in positiveG if not any(I['C']['G'][j][i] for i in live)]+[[graph,j] for j in range(10) if mask>>j&1 and not any(C[j][i] for i in live)]
  entry={'mask':mask,'live':live,'round_sizes':[len(r) for r in rounds],'failed_positive_rows':failed}
  if failed:failures.append(entry)
  else:survivors.append(entry)
 records.append({'zero_acceptance':branch,'candidate':graph,'survivors':survivors,'failures':failures})
 print(json.dumps({'branch':branch,'candidate':graph,'surviving_masks':[e['mask'] for e in survivors],'excluded':len(failures)},sort_keys=True),flush=True)
out={'source_realized':False,'status':'necessary support closure only','candidates':{'J1':'(G-{p,h})/(b=L), add aR','J2':'G-{p,h}, add aL,aR,bL'},'matrices':matrices,'records':records,'family_sha256':hashlib.sha256(json.dumps(K['columns'],separators=(',',':')).encode()).hexdigest()}
path=args.certificate
if path.exists():assert json.loads(path.read_text())==out
elif args.build:
 with path.open('x') as f:json.dump(out,f,separators=(',',':'));f.write('\n')
else:raise FileNotFoundError('Missing comparisons.json; use --build only to create a new certificate.')
