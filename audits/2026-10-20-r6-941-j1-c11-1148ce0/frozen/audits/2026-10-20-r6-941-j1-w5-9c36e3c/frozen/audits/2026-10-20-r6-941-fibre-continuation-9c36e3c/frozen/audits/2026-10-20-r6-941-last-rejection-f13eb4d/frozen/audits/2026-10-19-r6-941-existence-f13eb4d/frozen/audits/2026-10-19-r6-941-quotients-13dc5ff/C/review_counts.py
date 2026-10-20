#!/usr/bin/env python3
"""Independent E fibre/matrix and signed-span identity review."""
from collections import Counter
from fractions import Fraction
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    out=importlib.util.module_from_spec(spec);spec.loader.exec_module(out);return out

cap=load('independent_caps_review',HERE/'check.py')
family=load('independent_component_review',HERE/'review_closure.py')

def canonical(t):
    d={};return tuple(d.setdefault(x,len(d)) for x in t)

def all_partitions(n,p=()):
    if len(p)==n:yield p;return
    for c in range(max(p,default=-1)+2):yield from all_partitions(n,p+(c,))

def verify():
    actual=json.loads((HERE.parent/'A/certificate.json').read_text())
    own=json.loads((HERE/'certificate-v2.json').read_text())
    eight=sorted({canonical(t) for t in cap.literal_cycle(8)})
    ix={t:i for i,t in enumerate(eight)}
    joint=[]
    for ri,row in enumerate(cap.ROWS):
        x,y,a,b,c=map(int,row)
        for n,R,L,q in itertools.product(range(4),repeat=4):
            e=(a,n,R,L,q,c,x,y);good=cap.proper(e) and b not in (a,c,q)
            lifts=cap.old_lifts(e,b) if good else []
            flags=[int(good and n==b and R==q),int(good and n==b and L==b),int(good and b not in (n,R,L))]
            joint.append([ri,n,R,L,q,ix[canonical(e)] if cap.proper(e) else -1,int(good),lifts,flags])
    assert joint==actual['all_joint_records']
    ownM={name:[[0]*274 for _ in cap.ROWS] for name in ('G','Q1','Q2','GB')}
    sectors={'Aa':[0]*274,'Ab':[0]*274}
    for ri,n,R,L,q,ei,good,lifts,flags in joint:
        if not good:continue
        ownM['G'][ri][ei]+=len(lifts)
        for name,flag in zip(('Q1','Q2','GB'),flags):ownM[name][ri][ei]+=flag
        if ri==9:
            a,b=map(int,(cap.ROWS[ri][2],cap.ROWS[ri][3]))
            sectors['Aa'][ei]+=sum(h==a for p,h in lifts)
            sectors['Ab'][ei]+=sum(h==b for p,h in lifts)
    assert ownM==actual['literal_E_count_matrices']
    assert sectors==actual['original_alpha_sectors']
    identities={
      'a1+a2=2Aa':[ownM['Q1'][9][i]+ownM['Q2'][9][i]-2*sectors['Aa'][i] for i in range(274)],
      'Ab=U1+V1+U2+V2':[sectors['Ab'][i]-sum(ownM[q][r][i] for q in ('Q1','Q2') for r in (4,6)) for i in range(274)],
      'Aa=TG+2UG':[sectors['Aa'][i]-ownM['GB'][1][i]-2*ownM['GB'][4][i] for i in range(274)],
      'VG=TG+UG':[ownM['GB'][6][i]-ownM['GB'][1][i]-ownM['GB'][4][i] for i in range(274)]}
    assert identities==actual['planar_count_proof']['identities']
    cores=own['cores'];othercaps=json.loads((HERE.parent/'A/cap-lifts.json').read_text())
    for a,b in zip(cores,othercaps):
        assert a['G']==b['left'] and a['right']==b['right']
        assert all([x[0] for x in a[q]]==b[q] for q in ('Q1','Q2','GB'))
    # A uses E->core transfer; C used direct literal full-core enumeration.
    for name in ('G','Q1','Q2','GB'):
        for ri,m in enumerate(actual['literal_E_count_matrices'][name]):
            reconstructed=Counter()
            for ei,mult in enumerate(m):
                for ci,weight in actual['complete_E_transfer'][ei]:
                    reconstructed[ci]+=mult*weight
            reconstructed={i:n for i,n in reconstructed.items() if n}
            assert reconstructed==dict(own['query_matrices'][name][ri])
    # Independently regenerate every C8 exchange column using cyclic side runs.
    lits=list(cap.literal_cycle(8));hnames={t:family.hcanonical(t) for t in lits}
    hrows=sorted(set(hnames.values()));hi={t:i for i,t in enumerate(hrows)}
    hindex={t:hi[hnames[t]] for t in lits};rowids=[ix[canonical(t)] for t in hrows]
    columns=set()
    for t in hrows:
        for p in family.templates(tuple(c//2 for c in t)):
            col=Counter()
            for mask in range(1<<(max(p)+1)):
                changed=tuple(c^1 if mask&(1<<p[i]) else c for i,c in enumerate(t))
                col[hindex[changed]]+=1
            columns.add(tuple(sorted(col.items())))
    columns=sorted(columns);assert len(columns)==981
    column_sha=hashlib.sha256(json.dumps(columns,separators=(',',':'),sort_keys=True).encode()).hexdigest()
    assert column_sha==actual['source_E_closure']['columns_sha256']
    G=actual['literal_E_count_matrices']['G']
    live={i for i in range(274) if all(not G[j][i] for j in (1,4,6))};initial=sorted(live);rounds=[]
    while True:
        covered={h for col in columns if all(rowids[h] in live for h,n in col) for h,n in col}
        missing={}
        for h,i in enumerate(rowids):
            if i in live and h not in covered:missing.setdefault(i,h)
        if not missing:break
        rounds.append([[i,missing[i]] for i in sorted(missing)]);live.difference_update(missing)
    assert initial==actual['source_E_closure']['initial']
    assert rounds==actual['source_E_closure']['rounds']
    assert sorted(live)==actual['source_E_closure']['live']
    # Eliminate on constraint rows, rather than constructing A's nullspace basis.
    parts=[p for p in all_partitions(8) if cap.proper(p) and not any(p[a]==p[c] and p[b]==p[d] and p[a]!=p[b] for a,b,c,d in itertools.combinations(range(8),4))]
    assert len(parts)==91
    span=[[int(all(p[i]!=p[j] or t[i]==t[j] for i in range(8) for j in range(i))) for p in parts] for t in eight]
    echelon=[]
    def reduce_vector(vector):
        v=list(map(Fraction,vector))
        for pivot,row in echelon:
            if v[pivot]:
                scale=v[pivot];v=[x-scale*y for x,y in zip(v,row)]
        return v
    for ei,row in enumerate(span):
        if ei in live:continue
        rem=reduce_vector(row)
        pivot=next((j for j,x in enumerate(rem) if x),None)
        if pivot is not None:
            scale=rem[pivot];echelon.append((pivot,[x/scale for x in rem]));echelon.sort()
    identities=actual['planar_count_proof']['identities']
    for name,vector in identities.items():
        functional=[sum(vector[i]*span[i][j] for i in range(274)) for j in range(91)]
        assert not any(reduce_vector(functional)),name
    return {'status':'PASS','complete_joint_fibres':len(joint),'complete_cap_interfaces':len(cores),'all_direct_core_matrix_comparisons':40,
            'E_exchange_columns':981,'E_columns_sha256':column_sha,'E_round_removed':[len(r) for r in rounds],
            'E_live':len(live),'signed_span_columns':91,'constraint_rank':len(echelon),'identity_count':len(identities),
            'identity_method':'exact rational constraint row-span reduction independent of A nullspace basis'}

if __name__=='__main__':print(json.dumps(verify(),sort_keys=True))
