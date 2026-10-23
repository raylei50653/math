#!/usr/bin/env python3
"""Exact, read-only 933 candidate audit.  Build exclusively with --build."""
import argparse
import copy
from fractions import Fraction as F
import hashlib
import itertools
import json
import math
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
BASE='cb8f8593e273a7426ecadd59797a6e643cc4768e'
ROWS=('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
SOURCE='audits/2026-10-18-smaller-bad-counts-e1617a2/frozen/audits/2026-10-18-smaller-bad-e1617a2/kempe-consistency.json'
CAT='audits/2026-10-18-smaller-bad-counts-e1617a2/frozen/artifacts/c5_cells/cells.json'
RULES='audits/2026-10-19-r6-941-acceptance-13dc5ff/C/certificate.json'
OLD='audits/2026-10-18-smaller-bad-counts-e1617a2/C/certificate.json'
NAMES=('G','Q1','Q2','GB')


def canonical(word):
    names={}
    return tuple(names.setdefault(c,len(names)) for c in word)


def rref(matrix):
    if not matrix:return [],[]
    a=[[F(x) for x in row] for row in matrix];pivots=[]
    for col in range(len(a[0])):
        i=next((i for i in range(len(pivots),len(a)) if a[i][col]),None)
        if i is None:continue
        j=len(pivots);a[j],a[i]=a[i],a[j];d=a[j][col]
        a[j]=[x/d for x in a[j]]
        for i in range(len(a)):
            if i!=j and a[i][col]:
                d=a[i][col];a[i]=[x-d*y for x,y in zip(a[i],a[j])]
        pivots.append(col)
    return a,pivots


def kernel(matrix,width):
    if not matrix:return [[int(i==j) for j in range(width)] for i in range(width)]
    reduced,pivots=rref(matrix);vectors=[]
    for col in range(width):
        if col in pivots:continue
        v=[F(0)]*width;v[col]=F(1)
        for j,p in enumerate(pivots):v[p]=-reduced[j][col]
        m=math.lcm(*(x.denominator for x in v));v=[int(x*m) for x in v]
        d=math.gcd(*v);vectors.append([x//d for x in v])
    return list(map(list,zip(*vectors))) if vectors else [[] for _ in range(width)]


def mv(matrix,vector):
    return [sum(a*b for a,b in zip(row,vector)) for row in matrix]


def mm(a,b):
    cols=list(zip(*b))
    return [[sum(x*y for x,y in zip(row,col)) for col in cols] for row in a]


def partitions(word=(0,)):
    if len(word)==8:yield word;return
    for c in range(max(word)+2):yield from partitions(word+(c,))


def inputs():
    manifest=json.loads((HERE/'INPUTS.json').read_text());assert manifest['base']==BASE
    for entry in manifest['files']:
        rel=entry['path'];data=(HERE/'frozen'/rel).read_bytes()
        assert len(data)==entry['bytes'] and hashlib.sha256(data).hexdigest()==entry['sha256'],'frozen bytes: '+rel
        assert (ROOT/rel).read_bytes()==data,'authority input drift: '+rel
    return manifest


def local_relations(tuples):
    index={t:i for i,t in enumerate(tuples)}
    matrices={n:[[0]*274 for _ in ROWS] for n in NAMES};records=[]
    E=('a','n','R','L','q','c','x','y')
    exterior_edges=list(zip(E,E[1:]+E[:1]))
    base_edges=exterior_edges+[('a','b'),('b','c'),('b','q')]
    original_edges=base_edges+[('p',v) for v in ('a','b','q','h','n')]+[('h',v) for v in ('q','L','R','n')]
    def proper(colors,edges):return all(colors[u]!=colors[v] for u,v in edges)
    for ri,word in enumerate(ROWS):
        x,y,a,b,c=map(int,word)
        for n,right,left,q in itertools.product(range(4),repeat=4):
            boundary=(a,n,right,left,q,c,x,y);colors=dict(zip(E,boundary));colors['b']=b
            eid=index[canonical(boundary)] if proper(colors,exterior_edges) else None
            lifts=[]
            for p,h in itertools.product(range(4),repeat=2):
                full=dict(colors,p=p,h=h)
                if proper(full,original_edges):lifts.append([p,h])
            flags=[int(proper(colors,base_edges) and n==b and right==q),
                   int(proper(colors,base_edges) and n==b and left==b),
                   int(proper(colors,base_edges+[('b',v) for v in ('n','L','R')]))]
            # Independent direct local formulas retain the complete p,h relation.
            expected=[[p,h] for p,h in itertools.product(range(4),repeat=2)
                      if eid is not None and b not in {a,c,q} and p not in {a,b,q,n,h}
                      and h not in {p,q,left,right,n}]
            assert lifts==expected
            records.append([ri,n,right,left,q,eid,lifts,flags])
            if eid is not None:
                matrices['G'][ri][eid]+=len(lifts)
                for name,flag in zip(NAMES[1:],flags):matrices[name][ri][eid]+=flag
    assert len(records)==2560
    return matrices,records


def all_prime_rules(catalogue):
    def hits(mask,p,z):return mask&p==p and mask&z==0
    rules=[]
    for state in itertools.product((0,1,2),repeat=10):
        p=sum(1<<i for i,x in enumerate(state) if x==1)
        z=sum(1<<i for i,x in enumerate(state) if x==2)
        if any(hits(m,p,z) for m in catalogue):continue
        if all(any(hits(m,p&~(1<<i),z&~(1<<i)) for m in catalogue)
               for i,x in enumerate(state) if x):
            rules.append({'required_mask':p,'absent_mask':z,
                          'required_rows':[ROWS[i] for i in range(10) if p>>i&1],
                          'absent_rows':[ROWS[i] for i in range(10) if z>>i&1]})
    return rules


def close_zeros(B,initial):
    """Exact sign propagation in bases whose coordinates are actual nonnegative z's."""
    zeros=set(initial);steps=[];width=len(B[0])
    while True:
        K=kernel([B[j] for j in sorted(zeros) if any(B[j])],width)
        if not K[0]:return [],steps,sorted(zeros)
        S=mm(B,K)
        rr,pivots=rref(list(map(list,zip(*S))))
        T=list(map(list,zip(*rr[:len(pivots)])))
        assert [T[j] for j in pivots]==[[F(int(i==j)) for j in range(len(pivots))] for i in range(len(pivots))]
        witnesses=[];forced=set()
        for row_id,row in enumerate(T):
            if any(row) and all(x<=0 for x in row):
                terms=[[pivots[k],str(x)] for k,x in enumerate(row) if x]
                new={j for j,_ in terms}-zeros
                if not new:continue
                # z_row = sum c_k z_pivot, modulo the already certified zeros.
                residual=[x-sum(F(c)*B[j][k] for j,c in terms) for k,x in enumerate(B[row_id])]
                assert not any(mm([residual],K)[0]),'zero-propagation exact relation'
                witnesses.append({'row_id':row_id,'terms':terms});forced|=new
        if not forced:return S,steps,sorted(zeros)
        steps.append({'dimension':len(S[0]),'witnesses':witnesses,'new_zero_ids':sorted(forced)})
        zeros|=forced


def compute():
    manifest=inputs();src=json.loads((HERE/'frozen'/SOURCE).read_text())
    tuples=[tuple(t) for t in src['tuples']]
    expected=sorted({canonical(t) for t in itertools.product(range(4),repeat=8)
                     if all(t[j]!=t[(j+1)%8] for j in range(8))})
    assert tuples==expected and len(tuples)==274
    assert src['pin_order']==['a','n','R','L','q','c','x','y']
    fours=list(itertools.combinations(range(8),4))
    nc=[p for p in partitions() if not any(p[i]==p[k] and p[j]==p[l] and p[i]!=p[j] for i,j,k,l in fours)]
    columns=[]
    for p in nc:
        col=[int(all(p[i]!=p[j] or t[i]==t[j] for i in range(8) for j in range(i))) for t in tuples]
        if any(col):columns.append(col)
    A=list(map(list,zip(*columns)))
    assert len(nc)==1430 and len(columns)==91 and len(rref(A)[1])==91
    live=set(next(r['surviving_ids'] for r in src['results'] if r['source_mask']==933))
    B=mm(A,kernel([row for j,row in enumerate(A) if j not in live],91))
    assert len(B[0])==18
    assert [i for i in sorted(live) if not any(B[i])]==[176,192]
    M,records=local_relations(tuples)
    old=json.loads((HERE/'frozen'/OLD).read_text())
    control=next(w for w in old['maximal_support_witnesses'] if w['source_mask']==933)
    z=mv(A,control['coefficient_vector']);assert z==control['exterior_counts'] and all(x>=0 for x in z)
    assert mv(M['G'],z)==control['source_counts']
    assert sum(1<<i for i,x in enumerate(mv(M['G'],z)) if x)==933
    # New equalities and nonnegative decompositions.
    main=[]
    residual_ids={'Q1':[51,273],'Q2':[172,212],'GB':[34,61,101,121,155,182]}
    distinguished={'Q1':131,'Q2':30,'GB':20}
    for name in NAMES[1:]:
        j=distinguished[name]
        residual=[x-(4 if k==j else 0) for k,x in enumerate(M['G'][9])]
        assert not any(mm([residual],B)[0]),'new 4z identity'
        terms=[j]+residual_ids[name]
        residual=[x-int(k in terms) for k,x in enumerate(M[name][8])]
        assert not any(mm([residual],B)[0]),'complete 01231 projection'
        factor=4 if name=='GB' else 2
        residual=[4*x-y-(factor if k==17 else 0) for k,(x,y) in enumerate(zip(M[name][6],M[name][9]))]
        assert not any(mm([residual],B)[0]),'old 01212 leakage'
        main.append({'candidate':name,'source_acceptance_row':'01232','source_acceptance_factor':4,
                     'distinguished_exterior_id':j,'distinguished_literal_word':list(tuples[j]),
                     'candidate_positive_row':'01231','other_nonnegative_exterior_ids':residual_ids[name],
                     'old_leakage_residual_factor':factor})
    catalogue=set(map(int,json.loads((HERE/'frozen'/CAT).read_text())['cells']))
    rules=all_prime_rules(catalogue);assert len(rules)==56
    frozen_rules=json.loads((HERE/'frozen'/RULES).read_text())['rules']
    assert rules==[{k:r[k] for k in ('required_mask','absent_mask','required_rows','absent_rows')} for r in frozen_rules]
    assert {i for i in range(1024) if not any(i&r['required_mask']==r['required_mask'] and i&r['absent_mask']==0 for r in rules)}==catalogue
    screens=[];summaries={}
    for name in NAMES[1:]:
        counts={};survivors=[]
        for ri,rule in enumerate(rules):
            absent=[i for i in range(10) if rule['absent_mask']>>i&1]
            positive=[i for i in range(10) if rule['required_mask']>>i&1]
            initial=[j for j in range(274) if any(M[name][i][j] for i in absent)]
            S,steps,zeros=close_zeros(B,initial)
            G=mm(M['G'],S) if S else [[] for _ in ROWS]
            H=mm(M[name],S) if S else [[] for _ in ROWS]
            killed_source=[i for i in range(10) if 933>>i&1 and not any(G[i])]
            killed_candidate=[i for i in positive if not any(H[i])]
            status='source_positive_killed' if killed_source else 'candidate_positive_killed' if killed_candidate else 'unresolved'
            if status=='unresolved':survivors.append(ri)
            counts[status]=counts.get(status,0)+1
            screens.append({'candidate':name,'rule_id':ri,'initial_zero_ids':initial,'propagation_steps':steps,
                            'final_known_zero_ids':zeros,'final_dimension':len(S[0]) if S else 0,
                            'killed_source_positive_rows':killed_source,'killed_candidate_positive_rows':killed_candidate,'status':status})
        summaries[name]={'counts':counts,'surviving_rule_ids':survivors}
    assert summaries=={
        'Q1':{'counts':{'source_positive_killed':54,'unresolved':2},'surviving_rule_ids':[49,55]},
        'Q2':{'counts':{'source_positive_killed':49,'candidate_positive_killed':5,'unresolved':2},'surviving_rule_ids':[49,55]},
        'GB':{'counts':{'source_positive_killed':55,'candidate_positive_killed':1},'surviving_rule_ids':[]}}
    assert all(not any(mm([M[name][1]],B)[0]) for name in ('Q1','Q2')),'whole 01021 fibre empty'
    return {'base':BASE,'input_manifest_sha256':hashlib.sha256((HERE/'INPUTS.json').read_bytes()).hexdigest(),
            'rows':list(ROWS),'pin_order':src['pin_order'],'original_mask':933,
            'same_exterior_dimension':18,'complete_cap_fibres':records,'complete_cap_fibre_count':len(records),
            'count_matrices':M,'source_positive_rows':[i for i in range(10) if 933>>i&1],
            'new_01231_decompositions':main,'prime_rules':rules,'screens':screens,'screen_summaries':summaries,
            'GB_full_support_in_K132':True,'all_alpha_single_positive_certificates_ruled_out':True,
            'Q1_Q2_smaller_bad_constructed':False,'source_realization_claimed':False,
            'unresolved_rule_feasibility_claimed':False,'general_933_exclusion_claimed':False,
            'control_status':{'algebra_and_complete_local_relations':'triggered and holds',
                              'actual_complete_933_original_source':'not triggered',
                              'remaining_rules_actual_source_realizability':'not triggered'}}


def verify(cert,expected):
    assert cert==expected,'complete exact certificate mismatch'


def negatives(cert,expected):
    cases=[]
    def reject(name,change):
        bad=copy.deepcopy(cert);change(bad)
        try:verify(bad,expected)
        except AssertionError:cases.append({'name':name,'rejected':True})
        else:raise AssertionError('accepted negative: '+name)
    reject('change-source-acceptance-factor',lambda c:c['new_01231_decompositions'][0].__setitem__('source_acceptance_factor',2))
    reject('independently-normalize-contact-frame',lambda c:c['pin_order'].__setitem__(1,'L'))
    reject('drop-a-full-p-h-lift',lambda c:next(r[6] for r in c['complete_cap_fibres'] if r[6]).pop())
    reject('drop-an-empty-fibre',lambda c:c['complete_cap_fibres'].pop(next(i for i,r in enumerate(c['complete_cap_fibres']) if not r[6])))
    reject('drop-one-of-the-56-rules',lambda c:c['prime_rules'].pop())
    reject('truncate-168-same-candidate-screens',lambda c:c['screens'].pop())
    def flip_trace_sign(c):
        term=next(term for s in c['screens'] for step in s['propagation_steps']
                  for w in step['witnesses'] for term in w['terms'])
        term[1]=str(-F(term[1]))
    reject('reverse-a-zero-propagation-negative-sign',flip_trace_sign)
    reject('omit-a-strict-original-positive-row',lambda c:c['source_positive_rows'].pop())
    reject('delete-a-killed-original-positive-witness',
           lambda c:next(s['killed_source_positive_rows'] for s in c['screens'] if s['killed_source_positive_rows']).pop())
    reject('turn-unresolved-rule-into-realized-source',lambda c:c.__setitem__('source_realization_claimed',True))
    reject('claim-general-933-exclusion',lambda c:c.__setitem__('general_933_exclusion_claimed',True))
    return cases


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--build',action='store_true');parser.add_argument('--negative',action='store_true')
    parser.add_argument('--certificate',type=Path,default=HERE/'certificate.json');args=parser.parse_args()
    expected=compute()
    if args.build:
        with args.certificate.open('x') as f:json.dump(expected,f,sort_keys=True,separators=(',',':'));f.write('\n')
    cert=json.loads(args.certificate.read_text());verify(cert,expected)
    summary={'ok':True,'base':BASE,'complete_full_lift_records':2560,'dimension':18,
             'prime_rules':56,'same_candidate_screens':168,'screen_summaries':cert['screen_summaries'],
             'new_01231_lower_bound':'4 N01231(H) >= N01232(G) > 0 for Q1,Q2,GB',
             'GB_full_support_in_K132':True,'all_alpha_single_positive_certificates_ruled_out':True,
             'frozen_input_drift':0,'new_smaller_bad':False,'general_933_exclusion':False}
    if args.negative:summary['negative_controls']=negatives(cert,expected)
    print(json.dumps(summary,sort_keys=True))

if __name__=='__main__':main()
