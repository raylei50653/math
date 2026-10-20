#!/usr/bin/env python3
"""Read-only stdlib independent replay: complete fibres, U injection and controls."""
import argparse,copy,hashlib,itertools,json
from collections import Counter
from fractions import Fraction
from math import gcd,lcm
from pathlib import Path
D=Path(__file__).resolve().parent
ROOT=D.parents[2]
ROWS=('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
NAMES=('G','Q1','Q2','GB')
RI={tuple(map(int,row)):j for j,row in enumerate(ROWS)}
COLOURS=range(4)
EDGE_LEFT=(('b','a'),('b','c'),('b','q'),('b','p'),('p','a'),('p','q'),('p','h'),('p','n'),('h','q'),('h','L'),('h','R'),('h','n'))
EDGE_RIGHT=(('x','y'),('x','c'),('x','r'),('x','s'),('y','a'),('y','r'),('y','t'),('r','t'),('r','w'),('r','v'),('r','s'))
def canonical(t):
    seen={};return tuple(seen.setdefault(x,len(seen)) for x in t)
def proper(t):return all(t[i]!=t[(i+1)%len(t)] for i in range(len(t)))
def tuples(n):
    def extend(t=(0,)):
        if len(t)==n:
            if t[0]!=t[-1]:yield t
        else:
            for c in range(min(3,max(t)+1)+1):
                if c!=t[-1]:yield from extend(t+(c,))
    return list(extend())
def valid(f,edges):return all(f[a]!=f[b] for a,b in edges)
def mv(M,z):return [sum(a*b for a,b in zip(row,z)) for row in M]
def mask(v):return sum(1<<j for j,x in enumerate(v) if x)
def canonical_row(t):return RI[canonical(t)]
T8=tuples(8);I8={t:i for i,t in enumerate(T8)}
T10=tuples(10);I10={t:i for i,t in enumerate(T10)}
assert len(T8)==274 and len(T10)==2461

def reconstruct_joint():
    records=[];M={n:[[0]*274 for _ in ROWS] for n in NAMES}
    sectors={'h_equals_a':[0]*274,'h_equals_b':[0]*274}
    for j,row in enumerate(ROWS):
        x,y,a,b,c=map(int,row)
        for n,R,L,q in itertools.product(COLOURS,repeat=4):
            t=(a,n,R,L,q,c,x,y);base={'x':x,'y':y,'a':a,'b':b,'c':c,'n':n,'R':R,'L':L,'q':q}
            good=proper(t) and valid(base,(('b','a'),('b','c'),('b','q')))
            ls=[]
            if good:
                for p,h in itertools.product(COLOURS,repeat=2):
                    if valid(dict(base,p=p,h=h),EDGE_LEFT):ls.append([p,h])
            flags=[int(good and n==b and R==q),int(good and n==b and L==b),int(good and valid(base,(('b','n'),('b','R'),('b','L'))))]
            i=I8[canonical(t)] if proper(t) else -1
            records.append([j,n,R,L,q,i,int(good),ls,flags])
            if good:
                M['G'][j][i]+=len(ls)
                for name,v in zip(NAMES[1:],flags):M[name][j][i]+=v
                if j==9:
                    for name,col in [('h_equals_a',a),('h_equals_b',b)]:sectors[name][i]+=sum(h==col for p,h in ls)
                if flags[0]:assert bool(ls)==(L!=a),'Q1 complete lift equivalence'
                if flags[1]:assert bool(ls)==(a==q or R!=a),'Q2 a=q branch'
    return records,M,sectors

EXPECTED_JOINT,EXPECTED_M,EXPECTED_SECTORS=reconstruct_joint()
def verify_joint(data):
    assert data['pin_order']==['a','n','R','L','q','c','x','y'] and data['rows']==list(ROWS),'joint coordinates'
    assert data['tuple_count']==274,'joint tuple domain'
    assert data['all_literal_records']==EXPECTED_JOINT,'complete literal fibre domain or old lifts'
    assert data['literal_count_matrices']==EXPECTED_M,'complete matrix projection'
    assert data['original_alpha_sector_count_rows']==EXPECTED_SECTORS,'original accepted sector rows'

def reconstruct_u():
    records=[];forbidden=[];M=[[0]*2461 for row in ROWS]
    for i,t in enumerate(T10):
        a,n,R,L,q,c,s,v,w,tau=t
        if a!=c:continue
        f=dict(zip(('a','n','R','L','q','c','s','v','w','t'),t))
        # In U the edges to a and b have become one pz edge. b is absent.
        es=(('p','a'),('p','q'),('p','h'),('p','n'),('h','q'),('h','L'),('h','R'),('h','n'))
        ls=[[p,h] for p,h in itertools.product(COLOURS,repeat=2) if valid(dict(f,p=p,h=h),es)]
        j=canonical_row((a,s,v,w,tau));records.append([i,j,ls])
        if ls and not (319>>j)&1:forbidden.append(i)
    for j,row in enumerate(ROWS):
        z,s,v,w,tau=map(int,row)
        for n,R,L,q in itertools.product(COLOURS,repeat=4):
            f={'a':z,'q':q,'n':n,'L':L,'R':R}; t=(z,n,R,L,q,z,s,v,w,tau)
            if not proper(t):continue
            ls=[[p,h] for p,h in itertools.product(COLOURS,repeat=2) if valid(dict(f,p=p,h=h),es)]
            M[j][I10[canonical(t)]]+=len(ls)
    return records,forbidden,M
EXPECTED_UREC,EXPECTED_UZERO,EXPECTED_U=reconstruct_u()
def verify_u(data):
    assert data['pin_order']==['a','n','R','L','q','c','s','v','w','t'] and data['rows']==list(ROWS),'U coordinates'
    assert data['tuple_count']==2461 and data['source_U_mask']==319,'U domain'
    assert data['all_equal_ac_records']==EXPECTED_UREC,'all U complete local lifts'
    assert data['forbidden_ids']==EXPECTED_UZERO,'U forbidden domain'
    assert data['literal_U_count_matrix']==EXPECTED_U,'U fixed literal projection'
    assert len(EXPECTED_UREC)==600 and len(EXPECTED_UZERO)==108

def original_reject_matrix():
    # Independent direct fixed-row calculation; no orbit or stabilizer division.
    out=[[0]*2461 for _ in range(2)]
    for j,row_id in enumerate((4,6)):
        x,y,a,b,c=map(int,ROWS[row_id])
        for n,R,L,q,s,v,w,t in itertools.product(COLOURS,repeat=8):
            core=(a,n,R,L,q,c,s,v,w,t)
            if not proper(core):continue
            base=dict(zip(('a','n','R','L','q','c','s','v','w','t'),core));base.update(x=x,y=y,b=b)
            left=sum(valid(dict(base,p=p,h=h),EDGE_LEFT) for p,h in itertools.product(COLOURS,repeat=2))
            right=sum(valid(dict(base,r=r),EDGE_RIGHT) for r in COLOURS)
            out[j][I10[canonical(core)]]+=left*right
    return out
EXPECTED_GBAD=original_reject_matrix()
def verify_inequality(data):
    assert data['source_G_rows']==['01202','01212'] and data['U_rows']==['01212','01213','01232'],'inequality row domain'
    assert data['source_G_literal_count_matrix']==EXPECTED_GBAD,'independent G fixed-row cap matrix'
    slack=[sum(g[i] for g in EXPECTED_GBAD)-2*sum(EXPECTED_U[j][i] for j in (6,7,9)) for i in range(2461)]
    assert data['slack_G_rejects_minus_twice_U_rejects']==slack and all(v>=0 for v in slack),'factor-two inequality'
    for j in (6,7,9):
        z,s,v,w,t=map(int,ROWS[j]);f={'a':z,'c':z,'s':s,'v':v,'w':w,'t':t,'r':z}
        rights=[[x,y,z] for x,y in itertools.product(COLOURS,repeat=2) if valid(dict(f,x=x,y=y),EDGE_RIGHT)]
        assert data['normalized_right_lifts_at_r_equals_z'][ROWS[j]]==rights,'all direct injection right lifts'
        assert len(rights)==3
        for b in (1,2,3):
            chosen=[r for r in rights if b in r[:2]]
            assert len(chosen)==2,'two images of each source colouring'
            targets=[canonical_row((x,y,z,b,z)) for x,y,r in chosen]
            assert all(i in (4,6) for i in targets),'image rejection rows'
    assert all(EXPECTED_GBAD[0][i]+EXPECTED_GBAD[1][i]>0 for i in EXPECTED_UZERO),'U zero redundancy'

def rref(a):
    a=[[Fraction(x) for x in r] for r in a];pivots=[]
    for col in range(len(a[0])):
        k=next((i for i in range(len(pivots),len(a)) if a[i][col]),None)
        if k is None:continue
        r=len(pivots);a[r],a[k]=a[k],a[r];q=a[r][col];a[r]=[x/q for x in a[r]]
        for i in range(len(a)):
            if i!=r and a[i][col]:
                q=a[i][col];a[i]=[x-q*y for x,y in zip(a[i],a[r])]
        pivots.append(col)
    return a,pivots

def noncrossing_partitions(n,p=(0,)):
    if len(p)==n:
        if not any(p[i]==p[k] and p[j]==p[l] and p[i]!=p[j] for i,j,k,l in itertools.combinations(range(n),4)):yield p
    else:
        for v in range(max(p)+2):yield from noncrossing_partitions(n,p+(v,))

def verify_gb941(data):
    rel='audits/2026-10-18-smaller-bad-e1617a2/kempe-consistency.json'
    raw=(ROOT/rel).read_bytes();manifest=json.loads((D.parent/'INPUTS.json').read_text())
    assert hashlib.sha256(raw).hexdigest()==manifest['inputs'][rel],'necessary Kempe support SHA'
    src=json.loads(raw);assert list(map(tuple,src['tuples']))==T8,'necessary support coordinate order'
    live=set(next(r for r in src['results'] if r['source_mask']==941)['surviving_ids'])
    cols=[]
    for pi in noncrossing_partitions(8):
        col=[int(all(pi[i]!=pi[j] or t[i]==t[j] for i in range(8) for j in range(i))) for t in T8]
        if any(col):cols.append(col)
    A=list(map(list,zip(*cols)));assert len(cols)==len(rref(A)[1])==91,'full planar span rank'
    reduced,pivots=rref([r for i,r in enumerate(A) if i not in live]);free=[i for i in range(91) if i not in pivots]
    assert len(live)==225 and len(free)==44,'full restricted planar dimension'
    basis=[]
    for f in free:
        v=[Fraction(0)]*91;v[f]=1
        for k,p in enumerate(pivots):v[p]=-reduced[k][f]
        basis.append(mv(A,v))
    Aa=EXPECTED_SECTORS['h_equals_a'];M=EXPECTED_M['GB'];zsum=[int(i in (17,118,179)) for i in range(274)]
    residuals=[
        [a-t-2*r for a,t,r in zip(Aa,M[1],M[4])],
        [a-t-r for a,t,r in zip(M[6],M[1],M[4])],
        [a-b for a,b in zip(M[1],zsum)],
        [2*r-a-z for r,a,z in zip(M[6],Aa,zsum)]
    ]
    assert data['source_mask']==941 and data['planar_span_rank']==91 and data['restricted_space_dimension']==44 and data['necessary_C8_live_count']==225,'GB identity domain'
    assert data['identities']==['A_a=N_01021(GB)+2*N_01202(GB)','N_01212(GB)=N_01021(GB)+N_01202(GB)','N_01021(GB)=z_17+z_118+z_179','2*N_01212(GB)=A_a+z_17+z_118+z_179'],'GB identity statement domain'
    assert data['exterior_coordinate_ids']==[17,118,179] and data['exterior_coordinate_tuples']==[''.join(map(str,T8[i])) for i in (17,118,179)],'GB literal coordinate domain'
    assert all(sum(x*y for x,y in zip(d,b))==0 for d in residuals for b in basis),'exact GB identity'
    assert all(residuals[2][i]==0 for i in live),'literal tau identity'
    assert data['all_GB_supports_in_K132_proved'] is False and data['source_realized'] is False,'GB scope boundary'
    return {'planar_rank':91,'restricted_dimension':44,'identities':len(residuals),'GB_accepts01212_given_Aa_positive':True}

def same_candidate_claim(claim,projections):
    name=claim['candidate'];assert name in ('Q1','Q2','GB'),'candidate identity'
    assert claim['acceptance_candidate']==name and set(claim['refusal_candidates'])=={name},'mixed candidate refusals'
    v=projections[name];assert v[9]>0 and all(v[i]==0 for i in (1,4,6)),'same candidate complete four-row certificate'

def verify_old_controls(data):
    rel=data['source'];manifest=json.loads((D.parent/'INPUTS.json').read_text())
    raw=(ROOT/rel).read_bytes();assert hashlib.sha256(raw).hexdigest()==manifest['inputs'][rel],'old control SHA'
    old=json.loads(raw)['results'];assert len(data['results'])==3 and [r['specified_candidate'] for r in data['results']]==['Q1','Q2','GB'],'control domain'
    out=[]
    for r,c in zip(data['results'],old):
        z=c['counts'];assert len(z)==274 and all(isinstance(v,int) and v>=0 for v in z),'old complete vector'
        projections={name:mv(M,z) for name,M in EXPECTED_M.items()};assert r['counts']==projections,'same exterior count projection'
        masks={name:mask(v) for name,v in projections.items()};assert r['masks']==masks and masks['G']==941,'same exterior support projection'
        sectors={name:sum(a*b for a,b in zip(vec,z)) for name,vec in EXPECTED_SECTORS.items()}
        assert r['original_alpha_sectors']==sectors,'old original sector counts'
        claim={'candidate':c['candidate'],'acceptance_candidate':c['candidate'],'refusal_candidates':[c['candidate']]*3}
        same_candidate_claim(claim,projections)
        assert not all(sectors.values()),'archived controls violate a mandatory positive sector'
        out.append({'specified_candidate':c['candidate'],'masks':masks,'sectors':sectors})
    return out

parser=argparse.ArgumentParser();parser.add_argument('--negative-controls',action='store_true');args=parser.parse_args()
joint=json.loads((D/'joint-fibres.json').read_text());u=json.loads((D/'u319-core.json').read_text());ineq=json.loads((D/'u319-inequality.json').read_text());old=json.loads((D/'old-controls-projected.json').read_text())
verify_joint(joint);verify_u(u);verify_inequality(ineq);summary=verify_old_controls(old)
gbdata=json.loads((D/'gb941-identities.json').read_text());gbsummary=verify_gb941(gbdata)
negative=[]
if args.negative_controls:
    mutations=[]
    bad=copy.deepcopy(joint);i=next(i for i,r in enumerate(bad['all_literal_records']) if r[6] and not r[7]);del bad['all_literal_records'][i];mutations.append(('erase_empty_fibre',lambda:verify_joint(bad)))
    badq=copy.deepcopy(joint);r=next(r for r in badq['all_literal_records'] if r[8][1] and r[2]==r[4]==int(ROWS[r[0]][2]));assert r[7];r[7]=[];mutations.append(('drop_Q2_a_equals_q_branch',lambda:verify_joint(badq)))
    badu=copy.deepcopy(u);badu['forbidden_ids']=badu['forbidden_ids'][:-1];mutations.append(('truncate_U_zero_domain',lambda:verify_u(badu)))
    badi=copy.deepcopy(ineq);badi['source_G_literal_count_matrix'][0][EXPECTED_UZERO[0]]+=1;mutations.append(('alter_G_inequality_count',lambda:verify_inequality(badi)))
    badgb=copy.deepcopy(gbdata);badgb['exterior_coordinate_ids'][-1]=180;mutations.append(('alter_GB_identity_coordinate',lambda:verify_gb941(badgb)))
    mixed={'candidate':'Q1','acceptance_candidate':'Q1','refusal_candidates':['Q1','Q2','GB']};mutations.append(('mix_different_candidates',lambda:same_candidate_claim(mixed,old['results'][0]['counts'])))
    for name,verify in mutations:
        try:verify()
        except AssertionError as e:negative.append({'mutation':name,'rejected':True,'reason':str(e)})
        else:raise AssertionError('negative control accepted: '+name)
print(json.dumps({'pass':True,'literal_C8_records':2560,'proper_retained_cases':407,'empty_old_lift_cases':239,
 'C10_U_records':600,'U_forbidden_ids':108,'universal_factor_two_count_inequality':True,'U_upper319_zeros_redundant_given_G941':True,
 'GB941_count_identities':gbsummary,'old_941_controls':summary,'negative_controls':negative},sort_keys=True))
