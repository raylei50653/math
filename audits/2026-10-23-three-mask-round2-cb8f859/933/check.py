#!/usr/bin/env python3
"""Read-only exact replay of four inherited 933 residuals, on one actual E.

Only --build creates a certificate, with exclusive creation. No graph is generated.
"""
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
PREV='audits/2026-10-23-three-mask-methods-cb8f859/933'
SOURCE='audits/2026-10-18-smaller-bad-counts-e1617a2/frozen/audits/2026-10-18-smaller-bad-e1617a2/kempe-consistency.json'
ROWS=('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
PIN=('a','n','R','L','q','c','x','y')
SPLIT=((0,2),(1,3))


def digest(data):return hashlib.sha256(data).hexdigest()


def frozen(path):return (HERE/'frozen'/path).read_bytes()


def inputs():
    manifest=json.loads((HERE/'INPUTS.json').read_text())
    assert manifest['base']==BASE
    for entry in manifest['files']:
        data=frozen(entry['path'])
        assert len(data)==entry['bytes'] and digest(data)==entry['sha256'],'frozen bytes: '+entry['path']
        assert (ROOT/entry['path']).read_bytes()==data,'immutable authority drift: '+entry['path']
    return manifest


def canonical(word):
    names={}
    return tuple(names.setdefault(c,len(names)) for c in word)


def rref(matrix):
    if not matrix:return [],[]
    a=[[F(x) for x in row] for row in matrix];pivots=[]
    for col in range(len(a[0])):
        i=next((i for i in range(len(pivots),len(a)) if a[i][col]),None)
        if i is None:continue
        j=len(pivots);a[j],a[i]=a[i],a[j];d=a[j][col];a[j]=[x/d for x in a[j]]
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


def mm(a,b):
    cols=list(zip(*b))
    return [[sum(x*y for x,y in zip(row,col)) for col in cols] for row in a]


def partitions(word=(0,)):
    if len(word)==8:yield word;return
    for c in range(max(word)+2):yield from partitions(word+(c,))


def local_relations(tuples):
    index={t:i for i,t in enumerate(tuples)}
    matrices={name:[[0]*274 for _ in ROWS] for name in ('G','Q1','Q2','GB')};records=[]
    exterior_edges=list(zip(PIN,PIN[1:]+PIN[:1]))
    base_edges=exterior_edges+[('a','b'),('b','c'),('b','q')]
    edges=base_edges+[('p',v) for v in ('a','b','q','h','n')]+[('h',v) for v in ('q','L','R','n')]
    def proper(colors,es):return all(colors[u]!=colors[v] for u,v in es)
    for ri,word in enumerate(ROWS):
        x,y,a,b,c=map(int,word)
        for n,right,left,q in itertools.product(range(4),repeat=4):
            t=(a,n,right,left,q,c,x,y);colors=dict(zip(PIN,t));colors['b']=b
            eid=index[canonical(t)] if proper(colors,exterior_edges) else None
            lifts=[[p,h] for p,h in itertools.product(range(4),repeat=2) if proper(dict(colors,p=p,h=h),edges)]
            flags=[int(proper(colors,base_edges) and n==b and right==q),
                   int(proper(colors,base_edges) and n==b and left==b),
                   int(proper(colors,base_edges+[('b',v) for v in ('n','L','R')]))]
            formula=[[p,h] for p,h in itertools.product(range(4),repeat=2)
                     if eid is not None and b not in {a,c,q} and p not in {a,b,q,n,h}
                     and h not in {p,q,left,right,n}]
            assert lifts==formula,'whole original p,h lifts versus independent local formula'
            records.append([ri,n,right,left,q,eid,lifts,flags])
            if eid is not None:
                matrices['G'][ri][eid]+=len(lifts)
                for name,flag in zip(('Q1','Q2','GB'),flags):matrices[name][ri][eid]+=flag
    return matrices,records


def restrict_and_sign_close(B,initial):
    """Use only nonnegative actual z coordinates as sign-propagation variables."""
    zeros=set(initial);steps=[];width=len(B[0])
    while True:
        K=kernel([B[j] for j in sorted(zeros) if any(B[j])],width)
        assert K[0],'unexpected zero-dimensional restriction'
        S=mm(B,K)
        rr,pivots=rref(list(map(list,zip(*S))))
        T=list(map(list,zip(*rr[:len(pivots)])))
        assert [T[j] for j in pivots]==[[F(int(i==j)) for j in range(len(pivots))] for i in range(len(pivots))]
        witnesses=[];forced=set()
        for j,row in enumerate(T):
            if any(row) and all(x<=0 for x in row):
                terms=[[pivots[k],str(x)] for k,x in enumerate(row) if x]
                new={i for i,_ in terms}-zeros
                if not new:continue
                residual=[x-sum(F(c)*B[i][k] for i,c in terms) for k,x in enumerate(B[j])]
                assert not any(mm([residual],K)[0]),'signed zero identity'
                witnesses.append({'row_id':j,'nonpositive_terms':terms});forced|=new
        if not forced:
            linear_zeros=[j for j,row in enumerate(S) if not any(row)]
            return S,steps,sorted(zeros),linear_zeros
        steps.append({'dimension':len(S[0]),'witnesses':witnesses,'new_zero_ids':sorted(forced)})
        zeros|=forced


def all_actual_component_options(t,noncrossing,index):
    """All NC boundary component partitions for the fixed 02|13 palette split.

    Include every compatible partition, including partitions with identical
    orbits. The same original partition is used for every subset switch.
    """
    side={c:k for k,pair in enumerate(SPLIT) for c in pair}
    flip={pair[k]:pair[1-k] for pair in SPLIT for k in (0,1)}
    records=[]
    for part in noncrossing:
        blocks=[[i for i,v in enumerate(part) if v==b] for b in range(max(part)+1)]
        if any(len({side[t[i]] for i in block})!=1 for block in blocks):continue
        if any(side[t[i]]==side[t[(i+1)%8]] and part[i]!=part[(i+1)%8] for i in range(8)):continue
        lifts=[];orbit=set()
        for subset in range(1<<len(blocks)):
            changed=tuple(flip[c] if subset>>part[i]&1 else c for i,c in enumerate(t))
            assert all(changed[i]!=changed[(i+1)%8] for i in range(8))
            eid=index[canonical(changed)];orbit.add(eid)
            lifts.append([subset,list(changed),eid])
        records.append({'partition':list(part),'orbit':sorted(orbit),'all_boundary_switch_lifts':lifts})
    assert records
    return records


def compute():
    inputs();old=json.loads(frozen(PREV+'/certificate.json'));src=json.loads(frozen(SOURCE))
    assert old['base']==BASE and old['original_mask']==933
    assert old['screen_summaries']['GB']['surviving_rule_ids']==[]
    assert old['GB_full_support_in_K132'] is True
    assert all(old['screen_summaries'][name]['surviving_rule_ids']==[49,55] for name in ('Q1','Q2'))
    tuples=[tuple(t) for t in src['tuples']]
    expected=sorted({canonical(t) for t in itertools.product(range(4),repeat=8) if all(t[i]!=t[(i+1)%8] for i in range(8))})
    assert tuples==expected and len(tuples)==274 and src['pin_order']==list(PIN)
    fours=list(itertools.combinations(range(8),4))
    nc=[part for part in partitions() if not any(part[i]==part[k] and part[j]==part[l] and part[i]!=part[j] for i,j,k,l in fours)]
    columns=[]
    for part in nc:
        col=[int(all(part[i]!=part[j] or t[i]==t[j] for i in range(8) for j in range(i))) for t in tuples]
        if any(col):columns.append(col)
    A=list(map(list,zip(*columns)))
    assert len(nc)==1430 and len(columns)==91 and len(rref(A)[1])==91
    live=set(next(r['surviving_ids'] for r in src['results'] if r['source_mask']==933))
    B=mm(A,kernel([row for j,row in enumerate(A) if j not in live],91))
    assert len(B[0])==18
    M,cap=local_relations(tuples)
    assert M==old['count_matrices'] and cap==old['complete_cap_fibres'],'whole predecessor cap reconstruction'
    assert len(cap)==2560 and sum(len(r[6]) for r in cap)==175 and sum(not r[6] for r in cap)==2392
    assert [i for i in sorted(live) if not any(B[i])]==[176,192]
    simple_zero_ids=[0,5,26,47,127,152,168]
    assert all(not any(B[j]) for j in simple_zero_ids)
    simple_relations=[{'left':130,'terms':[[112,1],[125,1],[129,1]]},
                      {'left':130,'terms':[[11,1],[112,1],[125,1]]},
                      {'left':29,'terms':[[11,1],[24,1],[28,1]]}]
    for identity in simple_relations:
        assert all(x==sum(c*B[j][k] for j,c in identity['terms']) for k,x in enumerate(B[identity['left']]))
    for j in (30,131):
        residual=[v-int(i==j)*4 for i,v in enumerate(M['G'][9])]
        assert not any(mm([residual],B)[0]),'inherited source01232=4z identity'
    options={str(j):all_actual_component_options(tuples[j],nc,{t:i for i,t in enumerate(tuples)}) for j in (17,30,131)}
    cases=[]
    for name,rule_id,target in (('Q1',49,131),('Q1',55,131),('Q2',49,30),('Q2',55,17)):
        rule=old['prime_rules'][rule_id]
        assert rule['required_rows']==(['01203'] if rule_id==49 else ['01023'])
        assert rule['absent_rows']==(['01012','01201','01202'] if rule_id==49 else ['01012','01021','01202'])
        initial=sorted({j for i,row in enumerate(M[name]) if rule['absent_mask']>>i&1 for j,x in enumerate(row) if x})
        S,sign_steps,known,zeros=restrict_and_sign_close(B,initial)
        assert target not in zeros
        small_hit={131:[47,127,130],30:[5,26,29,168],17:[0,24,26,152]}[target]
        assert set(small_hit)<=set(zeros)
        blockers=[]
        for option in options[str(target)]:
            blocked=sorted(set(option['orbit'])&set(small_hit))
            assert blocked,'every actual compatible partition has a forced-empty orbit member'
            blockers.append(blocked[0])
        # This is the only Kempe-deleted coordinate needed for each case.
        final=mm(S,kernel([S[target]],len(S[0])))
        if name=='Q2' and rule_id==55:
            residual=[a-b for a,b in zip(mm([M[name][2]],S)[0],S[17])]
            assert not any(residual),'Q2 01023=z17 on this same restricted count space'
            assert not any(mm([M[name][2]],final)[0])
            contradiction={'kind':'candidate_required_positive_killed','row':'01023','factor':1,'target_id':17}
        else:
            assert not any(mm([M['G'][9]],final)[0])
            contradiction={'kind':'original_required_positive_killed','row':'01232','factor':4,'target_id':target}
        cases.append({'candidate':name,'rule_id':rule_id,'rule':rule,'initial_complete_fibre_zero_ids':initial,
                      'sign_steps':sign_steps,'known_zero_ids':known,'all_linear_zero_ids':zeros,
                      'restricted_dimension':len(S[0]),'restriction_basis':S,
                      'kempe_target_id':target,'kempe_target_word':list(tuples[target]),
                      'palette_split':[list(p) for p in SPLIT],
                      'small_forced_zero_hitting_set':small_hit,
                      'partition_blocker_ids':blockers,'contradiction':contradiction,
                      'status':'excluded_on_actual_source_necessary_domain'})
    return {'base':BASE,'input_manifest_sha256':digest((HERE/'INPUTS.json').read_bytes()),
            'scope':'complete original r6 two-star contract, original mask933, same actual E',
            'pin_order':list(PIN),'rows':list(ROWS),'source_positive_rows':[ROWS[i] for i in range(10) if 933>>i&1],
            'source_space_dimension':18,'complete_cap_fibres':cap,'count_matrices':M,
            'paper_zero_ids':simple_zero_ids,'paper_linear_identities':simple_relations,
            'component_options':options,'cases':cases,'Q1_full_support_in_K132':True,
            'Q2_full_support_in_K132':True,'GB_full_support_in_K132_inherited':True,
            'all_three_fixed_candidate_supports_in_K132':True,'source_realized':False,
            'smaller_bad_constructed':False,'general_933_exclusion':False,'new_Lean_theorem':False,
            'control_status':{'exact_cap_count_and_orbit_proof':'triggered and holds',
                              'actual_complete_original_source_control':'not triggered',
                              'strict_smaller_bad_construction':'not triggered'}}


def normalize(obj):return json.loads(json.dumps(obj))


def verify(cert,expected):
    assert cert==expected,'complete exact certificate mismatch'


def negatives(cert,expected):
    cases=[]
    def reject(name,change):
        bad=copy.deepcopy(cert);change(bad)
        try:verify(bad,expected)
        except AssertionError:cases.append({'name':name,'rejected':True})
        else:raise AssertionError('accepted negative: '+name)
    reject('change-original-contact-order',lambda c:c['pin_order'].__setitem__(1,'L'))
    reject('drop-nonempty-original-full-lift',lambda c:next(r[6] for r in c['complete_cap_fibres'] if r[6]).pop())
    reject('omit-empty-complete-cap-fibre',lambda c:c['complete_cap_fibres'].pop(next(i for i,r in enumerate(c['complete_cap_fibres']) if not r[6])))
    reject('drop-one-residual-rule',lambda c:c['cases'].pop())
    reject('omit-compatible-component-partition',lambda c:c['component_options']['17'].pop())
    reject('omit-one-subset-switch-lift',lambda c:c['component_options']['131'][0]['all_boundary_switch_lifts'].pop())
    reject('change-literal-switch-output',lambda c:c['component_options']['17'][0]['all_boundary_switch_lifts'][0][1].__setitem__(0,3))
    reject('omit-one-allowed-orbit-member',lambda c:c['component_options']['30'][0]['orbit'].pop())
    reject('replace-forced-empty-blocker-by-live-target',lambda c:c['cases'][0]['partition_blocker_ids'].__setitem__(0,131))
    reject('claim-Q2-rule55-kills-original-source',lambda c:c['cases'][3]['contradiction'].__setitem__('kind','original_required_positive_killed'))
    reject('change-Q2-01023-z17-factor',lambda c:c['cases'][3]['contradiction'].__setitem__('factor',2))
    def flip(c):
        term=next(term for case in c['cases'] for step in case['sign_steps'] for w in step['witnesses'] for term in w['nonpositive_terms'])
        term[1]=str(-F(term[1]))
    reject('reverse-required-nonpositive-sign',flip)
    reject('turn-necessary-domain-into-actual-source',lambda c:c.__setitem__('source_realized',True))
    reject('promote-family-no-go-to-general-933-exclusion',lambda c:c.__setitem__('general_933_exclusion',True))
    return cases


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--build',action='store_true');parser.add_argument('--negative',action='store_true')
    parser.add_argument('--certificate',type=Path,default=HERE/'certificate-v2.json');args=parser.parse_args()
    expected=normalize(compute())
    if args.build:
        with args.certificate.open('x') as f:json.dump(expected,f,sort_keys=True,separators=(',',':'));f.write('\n')
    cert=json.loads(args.certificate.read_text());verify(cert,expected)
    summary={'ok':True,'base':BASE,'immutable_input_drift':0,'same_E_dimension':18,
             'complete_cap_fibres':2560,'empty_cap_fibres':2392,'full_p_h_lifts':175,
             'residuals_excluded':4,'actual_component_partition_counts':{j:len(v) for j,v in cert['component_options'].items()},
             'Q1_Q2_GB_full_supports_in_K132':True,'actual_source_control':'not triggered',
             'smaller_bad_constructed':False,'general_933_exclusion':False}
    if args.negative:summary['negative_controls']=negatives(cert,expected)
    print(json.dumps(summary,sort_keys=True))


if __name__=='__main__':main()
