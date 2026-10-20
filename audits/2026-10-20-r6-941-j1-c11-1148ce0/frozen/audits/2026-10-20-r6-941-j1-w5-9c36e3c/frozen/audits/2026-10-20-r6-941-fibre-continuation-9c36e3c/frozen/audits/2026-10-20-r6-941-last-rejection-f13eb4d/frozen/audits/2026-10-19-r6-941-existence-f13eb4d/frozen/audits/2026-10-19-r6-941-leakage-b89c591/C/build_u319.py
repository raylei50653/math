#!/usr/bin/env python3
"""Discovery-only evidence writer; check.py independently rebuilds these data."""
import itertools,json
from pathlib import Path
D=Path(__file__).resolve().parent
ROWS=('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
def canonical(t):
    d={}; return tuple(d.setdefault(x,len(d)) for x in t)
def proper(t):return all(t[i]!=t[(i+1)%len(t)] for i in range(len(t)))
def tuples(n):
    return sorted({canonical(t) for t in itertools.product(range(4),repeat=n) if proper(t)})
def lifts(t):
    a,n,R,L,q,c,s,v,w,tau=t
    return [[p,h] for p,h in itertools.product(range(4),repeat=2)
            if p not in {a,q,n,h} and h not in {p,q,L,R,n}]
ts=tuples(10);index={t:i for i,t in enumerate(ts)};rowindex={tuple(map(int,r)):i for i,r in enumerate(ROWS)}
records=[];forbidden=[]
for i,t in enumerate(ts):
    a,n,R,L,q,c,s,v,w,tau=t
    if a==c:
        j=rowindex[canonical((a,s,v,w,tau))]; ls=lifts(t)
        records.append([i,j,ls])
        if ls and not (319>>j)&1:forbidden.append(i)
M=[[0]*len(ts) for row in ROWS]
for j,row in enumerate(ROWS):
    z,s,v,w,tau=map(int,row)
    for n,R,L,q in itertools.product(range(4),repeat=4):
        t=(z,n,R,L,q,z,s,v,w,tau)
        if proper(t):M[j][index[canonical(t)]]+=len(lifts(t))
data={'pin_order':['a','n','R','L','q','c','s','v','w','t'],'tuple_count':len(ts),'rows':list(ROWS),
      'scope':'actual U from same completed original core: a=c=z; add p,h; no r-lift prerequisite',
      'source_U_mask':319,'forbidden_ids':forbidden,'all_equal_ac_records_schema':['tuple_id','U_row_id','all_p_h_lifts'],
      'all_equal_ac_records':records,'literal_U_count_matrix':M}
with (D/'u319-core.json').open('x') as f:json.dump(data,f,separators=(',',':'));f.write('\n')
print(json.dumps({'tuple_count':len(ts),'equal_ac_records':len(records),'forbidden_ids':len(forbidden),
                  'matrix_shape':[len(M),len(ts)],'forbidden_by_row':{ROWS[j]:sum(bool(M[j][i]) for i in range(len(ts))) for j in (6,7,9)}}))
# Additional complete cap count evidence for the universal factor-two inequality.
from collections import Counter
Gbad=[[0]*len(ts) for _ in range(2)]
for i,t in enumerate(ts):
    a,n,R,L,q,c,s,v,w,tau=t
    if a!=c:continue
    left=[(b,p,h) for b,p,h in itertools.product(range(4),repeat=3)
          if b not in {a,c,q,p} and p not in {a,q,n,h} and h not in {q,L,R,n}]
    right=[(x,y,r) for x,y,r in itertools.product(range(4),repeat=3)
           if x not in {y,c,r,s} and y not in {a,r,tau} and r not in {s,v,w,tau}]
    hist=Counter(rowindex[canonical((x,y,a,b,c))] for b,p,h in left for x,y,r in right)
    divisor=2 if len(set(t))==2 else 1
    for j,k in enumerate((4,6)):
        assert hist[k]%divisor==0
        Gbad[j][i]=hist[k]//divisor
slack=[Gbad[0][i]+Gbad[1][i]-2*sum(M[j][i] for j in (6,7,9)) for i in range(len(ts))]
assert min(slack)==0
extra={'source_G_rows':['01202','01212'],'source_G_literal_count_matrix':Gbad,
       'slack_G_rejects_minus_twice_U_rejects':slack,
       'U_rows':['01212','01213','01232'],
       'normalized_right_lifts_at_r_equals_z':{'01212':[[2,1,0],[2,3,0],[3,1,0]],
           '01213':[[2,1,0],[3,1,0],[3,2,0]],'01232':[[2,1,0],[2,3,0],[3,1,0]]}}
with (D/'u319-inequality.json').open('x') as f:json.dump(extra,f,separators=(',',':'));f.write('\n')
