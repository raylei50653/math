#!/usr/bin/env python3
"""Check the literal deletion pullback of the frozen C11 132-term identity."""
from pathlib import Path
import argparse,gzip,importlib.util,json
D=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('orbits',D/'orbits.py')
o=importlib.util.module_from_spec(sp);sp.loader.exec_module(o)
F=D.parent/'frozen/audits/2026-10-20-r6-941-j1-c11-1148ce0'
cert=json.loads((F/'reduction/reduced-orbit-certificate.json').read_text())
hrows=sorted(o.rowmap(list(o.c.proper_growth(11))))
lam={hrows[h]:v for h,v in cert['live_half_row_multipliers']}
K=json.load(gzip.open(D/'orbits.json.gz','rt'))
def decode(x,n):
    out=[0]*n
    for i in range(n-1,-1,-1):out[i]=x&3;x>>=2
    return tuple(out)
pulled={}
for row,i in K['rowids']:
    t=decode(row,13);p=t[:2]+t[4:]
    if o.c.m.proper(p):pulled[row]=lam.get(o.encode(o.half(p)),0)
    else:pulled[row]=0
bad=[]
for j,col in enumerate(K['columns']):
    v=4*sum(pulled[r] for r in col)
    if v and len(bad)<4:bad.append({'column_id':j,'half_rows':col,'pullback_pairing':v})
assert bad
out={'status':'PASS; direct two-vertex deletion tensor is not a cancellation',
     'deleted_positions':[2,3],'deleted_names':['u4','u3'],
     'outside_proper_C11_projection_multiplier':0,
     'counterexample_surviving_columns':bad,
     'generalized_identity_excluded':False,'source_excluded':False}
ap=argparse.ArgumentParser();ap.add_argument('--build',action='store_true');args=ap.parse_args()
p=D/'tensor-control.json'
if args.build:
    with p.open('x') as f:json.dump(out,f,indent=2);f.write('\n')
else:assert out==json.loads(p.read_text())
print(json.dumps(out,sort_keys=True))
