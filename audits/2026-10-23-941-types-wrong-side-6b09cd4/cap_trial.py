#!/usr/bin/env python3
"""Exploration only: complete ordered C6 relation of the fixed seven-point cap."""
from itertools import product
from functools import lru_cache
import json
from pathlib import Path
H=Path(__file__).resolve().parent

def norm(w):
    d={};return tuple(d.setdefault(x,len(d)) for x in w)
words=sorted({norm(w) for w in product(range(4),repeat=6) if all(w[i]!=w[(i+1)%6] for i in range(6))})

def full_lifts(w):
    # Inner i touches boundary i and i+1; inner six-cycle; hub touches all inner.
    lists=[tuple(c for c in range(4) if c not in {w[i],w[(i+1)%6]}) for i in range(6)]
    out=[]
    def rec(a):
        if len(a)==6:
            if a[0]==a[-1]:return
            for hub in range(4):
                if hub not in a:out.append((*a,hub))
            return
        for c in lists[len(a)]:
            if not a or a[-1]!=c:rec(a+[c])
    rec([]);return out

@lru_cache(None)
def triangulations(v):
    if len(v)<3:return (frozenset(),)
    result=[]
    for j in range(1,len(v)-1):
        edges=frozenset({tuple(sorted((v[0],v[j]))),tuple(sorted((v[j],v[-1]))),tuple(sorted((v[0],v[-1])))})
        for a in triangulations(v[:j+1]):
            for b in triangulations(v[j:]):result.append(a|b|edges)
    return tuple(set(result))
tris=sorted(triangulations(tuple(range(6))),key=lambda x:sorted(x))
old={w:full_lifts(w) for w in words}
relations=[{w for w in words if all(w[i]!=w[j] for i,j in t)} for t in tris]
relations.append({w for w in words if len(set(w))<4})
unsafe=[i for i,r in enumerate(relations) if not r<= {w for w,l in old.items() if l}]
safe=[i for i in range(len(relations)) if i not in unsafe]
covered=set().union(*(relations[i] for i in safe))
result=dict(scope='EXPLORATION ONLY, fixed C6 cap; no source or replacement theorem', normalized_boundary_words=len(words), old_relation_size=sum(bool(l) for l in old.values()),triangulations=len(tris), safe_caps=safe, unsafe_caps=unsafe,uncovered=[w for w,l in old.items() if l and w not in covered], rows=[dict(word=w,lift_count=len(l)) for w,l in old.items()])
(H/'cap-trial.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
