#!/usr/bin/env python3
import hashlib,itertools,json
from pathlib import Path
import sympy as sp
R=Path(__file__).resolve().parent
F=R.parent/'frozen/audits/2026-10-18-smaller-bad-e1617a2/kempe-consistency.json'
d=json.loads(F.read_text());ts=d['tuples']
def parts(p=(0,)):
 if len(p)==8:yield p;return
 for x in range(max(p)+2):yield from parts(p+(x,))
cols=[]
for p in parts():
 if any(p[a]==p[c] and p[b]==p[e] and p[a]!=p[b] for a,b,c,e in itertools.combinations(range(8),4)):continue
 col=[int(all(p[i]!=p[j] or t[i]==t[j] for i in range(8) for j in range(i))) for t in ts]
 if any(col):cols.append(col)
A=sp.Matrix(cols).T
probes=json.loads((R/'941-counted-candidate-probes.json').read_text())
results=[]
for rec in probes['results']:
 coeff,params=A.gauss_jordan_solve(sp.Matrix(rec['counts']))
 assert params.rows==0
 assert A*coeff==sp.Matrix(rec['counts'])
 print(rec['candidate'],'in signedspan',flush=True)
 results.append({'candidate':rec['candidate'],'coefficient_vector':[str(v) for v in coeff]})
out={'scope':'same941counted vectors also in planar signed span; not graph realization',
 'inputs':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'941-counted-candidate-probes.json',R/'cone-triangulated.json')},'results':results}
with (R/'941-counted-span.json').open('x') as f:f.write(json.dumps(out,indent=2)+'\n')
