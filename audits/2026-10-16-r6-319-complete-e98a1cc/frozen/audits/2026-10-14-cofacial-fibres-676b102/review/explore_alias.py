"""Finite necessary rows only; no source graph or new exclusion is asserted."""
from itertools import product, combinations
import json

def norm(row):
    colors = {}
    return tuple(colors.setdefault(c, len(colors)) for c in row)

def r_ok(z,s,r,t,p,q):
    row=(z,s,r,t)
    w=norm(row)
    if w==(0,1,0,2): return False
    missing=set(range(4))-set(row)
    pq={p,q}
    if w==(0,1,0,1): return pq==missing
    if w==(0,1,2,1): return bool(pq & missing)
    if w==(0,1,2,3): return pq=={s,t}
    raise AssertionError(row)

def h_ok(z,q,ell,t,x,y):
    row=(z,q,ell,t)
    w=norm(row)
    xy={x,y}
    if w==(0,1,0,1): return False
    if w in ((0,1,0,2),(0,1,2,1)):
        return xy==({q} | (set(range(4))-set(row)))
    if w==(0,1,2,3): return xy in ({q,ell},{q,t})
    raise AssertionError(row)

cycle=[(i,(i+1)%6) for i in range(6)]
rows=sorted({norm(row) for row in product(range(4),repeat=6)
             if all(row[i]!=row[j] for i,j in cycle)})
allowed=[]
for row in rows:
    z,s,r,t,ell,q=row
    if z==t:
        allowed.append(row)
        continue
    ps=[p for p in range(4) if p not in {z,q,ell,t}]
    xys=[(x,y) for x,y in product(range(4),repeat=2)
         if x not in {z,s,r} and y not in {z,r,t} and x!=y]
    if all(r_ok(z,s,r,t,p,q) for p in ps) and all(h_ok(z,q,ell,t,x,y) for x,y in xys):
        allowed.append(row)

# A partition is drawable by disjoint exterior identification trees iff
# no two distinct blocks have alternating boundary occurrences.
parts=sorted({norm(row) for row in product(range(6),repeat=6)})
legal=[]
for part in parts:
    if any(part[i]==part[j] for i,j in cycle): continue
    if any(part[a]==part[c] and part[b]==part[d] and part[a]!=part[b]
           for a,b,c,d in combinations(range(6),4)): continue
    survivors=[row for row in allowed if all(part[i]!=part[j] or row[i]==row[j]
                                            for i,j in combinations(range(6),2))]
    legal.append({'partition':part,'survivors':survivors})

out={'scope':'m=t alias; E=D-zt actual C6; necessary full restoration rows only',
     'pins':['z','s','r','t','ell','q'],
     'proper_c6_rows':len(rows),'allowed_rows':allowed,
     'allowed_z_eq_t':[r for r in allowed if r[0]==r[3]],
     'legal_noncrossing_loopless_partitions':len(legal),
     'zero_survivor_partitions':[p for p in legal if not p['survivors']],
     'partitions':legal}
print(json.dumps(out,indent=2))
