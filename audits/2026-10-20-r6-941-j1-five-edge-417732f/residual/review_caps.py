#!/usr/bin/env python3
"""Independent literal whole-cap enumeration on deterministic C13 samples."""
from pathlib import Path
from itertools import product, permutations
from hashlib import sha256
import argparse, importlib.util, json
D=Path(__file__).resolve().parent
P=D.parent/'counting/check.py'
spec=importlib.util.spec_from_file_location('reviewed_caps',P)
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
ROWS=('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')

def canonical(t):
    names={};out=[]
    for x in t:
        if x not in names:names[x]=len(names)
        out.append(names[x])
    return ''.join(map(str,out))

def compute():
    states=list(p.proper_growth(13))
    tests={states[i] for i in (0,1,7,23,101,700,4000,10000,22000,44000,56000,66429)}
    for e0,e1 in ((0,1),(1,0)):
        t=(0,1,2,1,2,1,2,3,1,2,e0,e1,2)
        for perm in permutations(range(4)):tests.add(tuple(perm[x] for x in t))
    records=[]
    common=(('x','y'),('x','c'),('x','s'),('y','a'),('y','t'),
            ('r','s'),('r','v'),('r','w'),('r','t'),('r','x'),('r','y'))
    rstar=tuple(('R',v) for v in ('n','u4','u3','u2','u1','L'))
    baseleft=(('b','a'),('b','c'),('b','q'))
    gleft=baseleft+(('b','p'),('p','a'),('p','q'),('p','n'),('p','h'),
                    ('h','q'),('h','L'),('h','R'),('h','n'))+rstar
    for state in sorted(tests):
        c=dict(zip(p.RIM,state));out={k:[0]*10 for k in ('G','Q1','J1')};sectors=[0,0]
        for kind,names,edges in (('G',('b','p','h','R','x','y','r'),gleft+common),
                                 ('Q1',('b','R','x','y','r'),baseleft+rstar+common),
                                 ('J1',('b','R','x','y','r'),baseleft+rstar+common+(('a','R'),))):
            for values in product(range(4),repeat=len(names)):
                f=c|dict(zip(names,values))
                if kind=='Q1' and (f['b']!=f['n'] or f['R']!=f['q']):continue
                if kind=='J1' and f['b']!=f['L']:continue
                if not all(f[u]!=f[v] for u,v in edges):continue
                row=ROWS.index(canonical(tuple(f[v] for v in ('x','y','a','b','c'))))
                out[kind][row]+=1
                if kind=='G' and row==9:
                    sectors[0]+=f['h']==f['a'];sectors[1]+=f['h']==f['b']
        a,n,u4,u3,u2,u1,L,q,c0,s,v,w,t=state
        mask=sum(1<<x for x in set((n,u4,u3,u2,u1,L)))
        expected,es=p.cap_counts(a,n,L,q,c0,s,v,w,t,mask)
        assert out==expected and sectors==es,(state,out,expected,sectors,es)
        records.append({'literal':state,'counts':out,'accept_sectors':sectors})
    return {'status':'PASS','scope':'independent direct whole-cap enumeration; sampled literal C13 states, including every S4 image of both named targets',
            'sample_states':len(tests),'reviewed_check_py_sha256':sha256(P.read_bytes()).hexdigest(),
            'records':records,'source_excluded':False}

ap=argparse.ArgumentParser();ap.add_argument('--build',action='store_true');args=ap.parse_args()
a=json.loads(json.dumps(compute()));target=D/'review-caps.json'
if args.build:
    with target.open('x') as f:json.dump(a,f,indent=2);f.write('\n')
else:assert a==json.loads(target.read_text())
print(json.dumps({k:a[k] for k in ('status','scope','sample_states','source_excluded')}))
