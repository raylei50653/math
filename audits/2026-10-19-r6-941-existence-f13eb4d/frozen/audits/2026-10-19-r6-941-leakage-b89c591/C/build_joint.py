#!/usr/bin/env python3
"""Discovery-only full literal table writer; replay check.py writes nothing."""
import itertools,json
from pathlib import Path
D=Path(__file__).resolve().parent
ROWS=('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
NAMES=('G','Q1','Q2','GB')
def canonical(t):
    d={};return tuple(d.setdefault(x,len(d)) for x in t)
def proper(t):return all(t[i]!=t[(i+1)%len(t)] for i in range(len(t)))
T=sorted({canonical(t) for t in itertools.product(range(4),repeat=8) if proper(t)});I={t:i for i,t in enumerate(T)}
M={name:[[0]*274 for _ in ROWS] for name in NAMES};records=[]
for j,row in enumerate(ROWS):
    x,y,a,b,c=map(int,row)
    for n,R,L,q in itertools.product(range(4),repeat=4):
        t=(a,n,R,L,q,c,x,y); good=proper(t) and b not in {a,c,q}
        lift=[[p,h] for p,h in itertools.product(range(4),repeat=2)
              if good and p not in {a,b,q,n,h} and h not in {q,L,R,n}]
        flags=[int(good and n==b and R==q),int(good and n==L==b),int(good and b not in {n,R,L})]
        i=I[canonical(t)] if proper(t) else -1
        rec=[j,n,R,L,q,i,int(good),lift,flags];records.append(rec)
        if good:
            M['G'][j][i]+=len(lift)
            for name,flag in zip(NAMES[1:],flags):M[name][j][i]+=flag
sectors={'h_equals_a':[0]*274,'h_equals_b':[0]*274}
for r in records:
    if r[0]==9 and r[6]:
        for v,name in [(2,'h_equals_a'),(3,'h_equals_b')]:
            sectors[name][r[5]]+=sum(h==v for pp,h in r[7])
out={'original_alpha_sector_count_rows':sectors,'pin_order':['a','n','R','L','q','c','x','y'],'rows':list(ROWS),'tuple_count':274,
     'record_schema':['row_id','n','R','L','q','exterior_orbit_id_or_minus_1','retained_edges_proper','all_p_h_lifts','Q1_Q2_GB_flags'],
     'all_literal_records':records,'literal_count_matrices':M}
with (D/'joint-fibres.json').open('x') as f:json.dump(out,f,separators=(',',':'));f.write('\n')
print(json.dumps({'records':len(records),'proper_retained_cases':sum(r[6] for r in records),
                  'empty_old_lift_cases':sum(r[6] and not r[7] for r in records),
                  'original_local_lifts':sum(len(r[7]) for r in records),
                  'Q1_Q2_GB_local_assignments':[sum(r[8][j] for r in records) for j in range(3)]}))
