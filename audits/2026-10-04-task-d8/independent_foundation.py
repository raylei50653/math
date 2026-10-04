#!/usr/bin/env python3
"""Independent 32-set audit; does not import repository checkers."""
from itertools import combinations
from pathlib import Path
import argparse, hashlib, json
OUT=Path(__file__).with_name('independent_foundation.json')
def connected_components(vertices,edges):
    unseen=set(vertices); answer=[]
    while unseen:
        seen={min(unseen)}; pending=list(seen)
        while pending:
            v=pending.pop()
            for a,b in edges:
                if v in (a,b):
                    n=b if a==v else a
                    if n in unseen and n not in seen: seen.add(n);pending.append(n)
        unseen-=seen;answer.append(sorted(seen))
    return answer

def build():
    frame=set(range(5)); edges={(i,(i+1)%5) for i in frame}
    triples=[set(t) for t in combinations(sorted(frame),3)
        if sum(a in t and b in t for a,b in edges)==1]
    subsets=[]
    for k in range(6):
        for selected in combinations(sorted(frame),k):
            q=set(selected); cc=connected_components(q,edges)
            included=[sorted(t) for t in triples if t<=q]
            assert (k+len(cc)>4)==bool(included)
            subsets.append(dict(Q=list(selected),components=cc,c=len(cc),bad=k+len(cc)>4,
                contained_941_triples=included))
    orbit=sorted({tuple(sorted((sign*v+shift)%5 for v in (0,1,3)))
        for sign in (-1,1) for shift in frame})
    assert orbit==sorted(tuple(sorted(t)) for t in triples)
    assert next(x for x in subsets if x['Q']==list(range(5)))['c']==1
    # Off-path hubs are actual consecutive intervals of one fixed external path.
    # All endpoint colors, including equal ones, remain in the same color frame.
    hubs=[]
    for n in range(3,8):
        path=list(range(5,5+n)); e=list(zip(path,path[1:]))
        for c0 in range(4):
            for c1 in range(4):
                bags=[path] if c0==c1 else [path[:-1],path[-1:]]
                assert all(len(connected_components(b,e))==1 for b in bags)
                assert len(set().union(*(set(b) for b in bags)))==sum(map(len,bags))
                if len(bags)==2:
                    assert all(len(set(b)&{path[0],path[-1]})==1 for b in bags)
                    assert any(a in bags[0] and b in bags[1] for a,b in e)
                hubs.append(dict(path=path,edges=e,root_colors=[c0,c1],bags=bags))
    return dict(scope='32 named C5 subsets and literal external-path hub bags; no Gallai or topology proof by finite search',
        subsets=subsets,D5_triple_orbit=[list(t) for t in orbit],
        bad_subsets=sum(x['bad'] for x in subsets),hub_bags=hubs)
p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');args=p.parse_args()
raw=(json.dumps(build(),ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
if args.check:assert OUT.read_bytes()==raw
else:
    with OUT.open('xb') as f:f.write(raw)
print(json.dumps(dict(subsets=32,bad_subsets=11,D5_triple_orbit=5,hub_bag_controls=80,sha256=hashlib.sha256(raw).hexdigest(),check=args.check),sort_keys=True))
