#!/usr/bin/env python3
"""Exact stdlib replay of the planar-span certificate; no LP or graph search."""
import argparse
import copy
from fractions import Fraction as F
import hashlib
import itertools
import json
import math
from pathlib import Path

D=Path(__file__).resolve().parent
R=D.parent
SOURCE=R/'frozen/audits/2026-10-18-smaller-bad-e1617a2/kempe-consistency.json'
CATALOGUE=R/'frozen/artifacts/c5_cells/cells.json'
ROWS=('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
NAMES=('G','Q1','Q2','GB')

def canonical(t):
    d={}
    return tuple(d.setdefault(x,len(d)) for x in t)

def partitions(p=(0,)):
    if len(p)==8:
        yield p
        return
    for x in range(max(p)+2):
        yield from partitions(p+(x,))

def rref(a):
    a=[[F(x) for x in row] for row in a]
    width=len(a[0]); pivots=[]
    for col in range(width):
        pivot=next((i for i in range(len(pivots),len(a)) if a[i][col]),None)
        if pivot is None:
            continue
        j=len(pivots)
        a[j],a[pivot]=a[pivot],a[j]
        d=a[j][col]
        a[j]=[x/d for x in a[j]]
        for i in range(len(a)):
            if i!=j and a[i][col]:
                d=a[i][col]
                a[i]=[x-d*y for x,y in zip(a[i],a[j])]
        pivots.append(col)
    return a,pivots

def kernel(a):
    reduced,pivots=rref(a)
    width=len(a[0]); vectors=[]
    for col in range(width):
        if col in pivots:
            continue
        v=[F(0)]*width;v[col]=F(1)
        for j,p in enumerate(pivots):
            v[p]=-reduced[j][col]
        multiple=math.lcm(*(x.denominator for x in v))
        v=[int(x*multiple) for x in v]
        divisor=math.gcd(*v)
        vectors.append([x//divisor for x in v])
    return list(map(list,zip(*vectors)))

def mv(a,v):
    assert a and all(len(row)==len(v) for row in a),'matrix-vector dimensions'
    return [sum(x*y for x,y in zip(row,v)) for row in a]

def mm(a,b):
    assert a and b and all(len(row)==len(b) for row in a),'matrix-product dimensions'
    assert all(len(row)==len(b[0]) for row in b),'matrix column dimensions'
    columns=list(zip(*b))
    return [[sum(x*y for x,y in zip(row,col)) for col in columns] for row in a]

def support(v):
    return sum(1<<i for i,x in enumerate(v) if x>0)

src=json.loads(SOURCE.read_text())
tuples=[tuple(t) for t in src['tuples']]
ind={t:i for i,t in enumerate(tuples)}
expected=sorted({canonical(t) for t in itertools.product(range(4),repeat=8)
                 if all(t[i]!=t[(i+1)%8] for i in range(8))})
assert tuples==expected and len(tuples)==274
fours=list(itertools.combinations(range(8),4))
noncrossing=[p for p in partitions() if not any(p[i]==p[k] and p[j]==p[l] and p[i]!=p[j] for i,j,k,l in fours)]
columns=[]
for p in noncrossing:
    col=[int(all(p[i]!=p[j] or t[i]==t[j] for i in range(8) for j in range(i))) for t in tuples]
    if any(col):
        columns.append(col)
A=list(map(list,zip(*columns)))
assert len(noncrossing)==1430 and len(columns)==91
assert len(rref(A)[1])==91
M={name:[[0]*274 for _ in ROWS] for name in NAMES}
for ri,row in enumerate(ROWS):
    x,y,a,b,c=map(int,row)
    for n,right,left,q in itertools.product(range(4),repeat=4):
        t=(a,n,right,left,q,c,x,y)
        if any(t[j]==t[(j+1)%8] for j in range(8)) or b in {a,q,c}:
            continue
        i=ind[canonical(t)]
        M['G'][ri][i]+=sum(p not in {a,b,q,n,h} and h not in {q,left,right,n}
                           for p,h in itertools.product(range(4),repeat=2))
        M['Q1'][ri][i]+=int(n==b and right==q)
        M['Q2'][ri][i]+=int(n==b and left==b)
        M['GB'][ri][i]+=int(b not in {n,left,right})
lives={r['source_mask']:set(r['surviving_ids']) for r in src['results']}
bases={mask:mm(A,kernel([row for i,row in enumerate(A) if i not in live]))
       for mask,live in lives.items()}
K=set(map(int,json.loads(CATALOGUE.read_text())['cells']))

def verify(cert):
    assert set(cert['input_sha256'])=={str(SOURCE.relative_to(R)),str(CATALOGUE.relative_to(R))},'input hash domain'
    assert len(cert['maximal_support_witnesses'])==3 and {w['source_mask'] for w in cert['maximal_support_witnesses']}=={932,933,941},'source domain'
    for rel,digest in cert['input_sha256'].items():
        assert hashlib.sha256((R/rel).read_bytes()).hexdigest()==digest,'input hash'
    assert cert['pin_order']==src['pin_order'] and cert['rows']==list(ROWS)
    assert (cert['noncrossing_partitions'],cert['nonzero_columns'],cert['rank'])==(1430,91,91)
    assert cert['source_realized'] is False and cert['smaller_bad_source_constructed'] is False
    for w in cert['maximal_support_witnesses']:
        mask=w['source_mask'];live=lives[mask];B=bases[mask]
        assert w['dimension']==len(B[0]),'kernel dimension'
        zeros=[i for i in sorted(live) if not any(B[i])]
        assert w['extra_zero_ids']==zeros,'forced zeros'
        z=mv(A,w['coefficient_vector'])
        assert z==w['exterior_counts'] and all(x>=0 for x in z),'maximal witness'
        assert {i for i,x in enumerate(z) if x>0}==live-set(zeros),'maximal support'
        assert mv(M['G'],z)==w['source_counts'] and support(w['source_counts'])==mask,'original full support'
    r=cert['source932'];ids=r['coordinate_ids'];rays=r['exterior_rays']
    assert ids==[11,17,132] and r['coordinate_tuples']==[list(tuples[i]) for i in ids]
    assert len(bases[932][0])==3 and mm(A,r['coefficient_rays'])==rays,'ray span'
    assert all(all(x>=0 for x in row) for row in rays),'nonnegative rays'
    assert [rays[i] for i in ids]==[[1,0,0],[0,1,0],[0,0,1]],'coordinate normalization'
    assert all(not any(row) for i,row in enumerate(rays) if i not in lives[932]),'ray support'
    for name in NAMES:
        assert mm(M[name],rays)==r['projected_rays'][name],'full count projection'
    expected_cases=[]
    for bits in itertools.product((0,1),repeat=3):
        if not any(bits):
            continue
        masks={name:support(mv(matrix,bits)) for name,matrix in r['projected_rays'].items()}
        assert masks['G']==932
        assert all(masks[name] in K for name in ('Q1','Q2','GB')),'catalogue pattern'
        expected_cases.append({'positive_coordinates':list(bits),'masks':masks})
    assert r['seven_support_patterns']==expected_cases
    assert len(cert['identities'])==6 and {(r['source_mask'],r['candidate']) for r in cert['identities']}==set(itertools.product((932,933),('Q1','Q2','GB'))),'identity domain'
    for claim in cert['identities']:
        mask=claim['source_mask'];name=claim['candidate'];factor=claim['factor'];i=claim['residual_exterior_id'];c=claim['residual_factor']
        assert mask in (932,933) and name in ('Q1','Q2','GB')
        assert (factor,i,c)==(4,17,4 if name=='GB' else 2)
        assert (claim['acceptance_row'],claim['rejection_row'])==('01232','01212')
        d=[factor*r-a-(c if j==i else 0) for j,(r,a) in enumerate(zip(M[name][6],M[name][9]))]
        assert all(x==0 for x in mm([d],bases[mask])[0]),'count identity'
    assert len(cert['source941_separate_candidate_controls'])==3 and {w['name'] for w in cert['source941_separate_candidate_controls']}=={'Q1','Q2','GB'},'941 domain'
    for w in cert['source941_separate_candidate_controls']:
        z=mv(A,w['coefficient_vector'])
        assert z==w['exterior_counts'] and all(x>=0 for x in z)
        assert all(x==0 for i,x in enumerate(z) if i not in lives[941])
        assert mv(M['G'],z)==w['source_counts'] and support(w['source_counts'])==941
        q=mv(M[w['name']],z)
        assert q==w['candidate_counts'] and q[9]>0 and all(q[i]==0 for i in (1,4,6)),'941 separate candidate'

parser=argparse.ArgumentParser()
parser.add_argument('--certificate',type=Path,default=D/'certificate.json')
parser.add_argument('--negative-controls',action='store_true')
parser.add_argument('--check',action='store_true',help='Compatibility flag; all runs verify the certificate.')
args=parser.parse_args()
cert=json.loads(args.certificate.read_text())
verify(cert)
summary={'pass':True,'rank':91,'dimensions':{str(m):len(b[0]) for m,b in bases.items()},'source932_933_candidate01212_obstruction':True,'source932_all_candidate_masks_in_K132':True,'source941_control_count':3}
if args.negative_controls:
    controls=[]
    for name in ('projected_acceptance','ray_coordinate','941_false_empty','truncated_domain'):
        changed=copy.deepcopy(cert)
        if name=='projected_acceptance':changed['source932']['projected_rays']['Q1'][9][0]+=1
        elif name=='ray_coordinate':changed['source932']['exterior_rays'][11][0]+=1
        elif name=='941_false_empty':changed['source941_separate_candidate_controls'][0]['candidate_counts'][4]=1
        else:changed['identities']=changed['identities'][:3]+changed['identities'][:3]
        try:
            verify(changed)
        except AssertionError as err:
            controls.append({'mutation':name,'rejected':True,'reason':str(err)})
        else:
            raise AssertionError('negative control was accepted')
    summary['negative_controls']=controls
print(json.dumps(summary,sort_keys=True))
