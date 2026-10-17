#!/usr/bin/env python3
"""Independent labelled expansion of the root count-cone compression.

Reconstructs actual pin-level component cubes, then verifies the supplied
compressed feasible solution on all 24 labelled rows per canonical row.
It does not establish realization of those component cubes by a graph.
"""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import importlib.util
from itertools import combinations, permutations, product
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent/'integration'
PAIRS=(((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2)))
KEYS=tuple(frozenset(frozenset(p) for p in q) for q in PAIRS)
PERMS=tuple(permutations(range(4)))
FIXED=KEYS[0]
STAB=tuple(p for p in PERMS if frozenset(frozenset(p[c] for c in a) for a in PAIRS[0])==FIXED)
assert len(STAB)==8


def canonical(row):
    used=[]
    for c in row:
        if c not in used:used.append(c)
    used += [c for c in range(4) if c not in used]
    inv={c:i for i,c in enumerate(used)}
    return tuple(inv[c] for c in row),inv


def coordinate(row):
    cc,inv=canonical(row)
    key=frozenset(frozenset(inv[c] for c in a) for a in PAIRS[0])
    return cc,KEYS.index(key)


@lru_cache(None)
def groups(vertices):
    # Independent set-partition recursion, represented as vertex blocks.
    if not vertices:return ((),)
    first=vertices[0];result=[]
    for pp in groups(vertices[1:]):
        result.append(((first,),)+pp)
        for i in range(len(pp)):
            result.append(pp[:i]+(tuple(sorted((first,)+pp[i])),)+pp[i+1:])
    output=[]
    for pp in result:
        which={v:i for i,b in enumerate(pp) for v in b}
        if any(v in which and (v+1)%9 in which and which[v]!=which[(v+1)%9] for v in range(9)):continue
        output.append(pp)
    return tuple(output)


def planar(blocks):
    # Direct endpoint alternation; no root helper is imported.
    for aa,bb in combinations(blocks,2):
        for a,c in combinations(aa,2):
            for b,d in combinations(bb,2):
                if (a<b<c)!=(a<d<c):return False
    return True


def whole_cube(row,pairing,blocks):
    out=[]
    marked=[(b,pairing[side]) for side in range(2) for b in blocks[side]]
    for mask in range(1<<len(marked)):
        image=list(row)
        for j,(block,pal) in enumerate(marked):
            if mask>>j&1:
                for v in block:image[v]=sum(pal)-image[v]
        out.append(tuple(image))
    assert len(set(out))==len(out)
    return tuple(sorted(out))


def relabel(row,p):return tuple(p[c] for c in row)


def run(mask):
    cert=json.loads((ROOT/f'counts{mask}.json').read_text())
    rows=tuple(tuple('ABCD'.index(c) for c in s) for s in cert['canonical_rows'])
    ix={r:i for i,r in enumerate(rows)}
    # All rows use at least three colours, so the S4 action is free.
    labels=tuple(sorted({relabel(r,p) for r in rows for p in PERMS}))
    assert len(labels)==24*len(rows)
    for r in rows:
        per=Counter(coordinate(relabel(r,p))[1] for p in PERMS)
        assert per=={0:8,1:8,2:8}
    witnessed={}
    actual_orbits=set()
    for row in rows:
        for pi,pairing in enumerate(PAIRS):
            cc=[groups(tuple(i for i,c in enumerate(row) if c in pal)) for pal in pairing]
            trans=next(p for p in PERMS if frozenset(frozenset(p[c] for c in a) for a in pairing)==FIXED)
            for left,right in product(*cc):
                if not planar(left+right):continue
                cube=whole_cube(row,pairing,(left,right))
                if any(canonical(member)[0] not in ix for member in cube):continue
                cube=tuple(sorted(relabel(member,trans) for member in cube))
                counter=Counter((ix[coordinate(member)[0]],coordinate(member)[1]) for member in cube)
                vector=tuple(sorted((3*i+p,multiplicity) for (i,p),multiplicity in counter.items()))
                witnessed.setdefault(vector,cube)
                for sym in STAB:
                    actual_orbits.add(tuple(sorted(relabel(member,sym) for member in cube)))
    vectors=tuple(sorted(witnessed))
    assert len(vectors)==cert['orbit_vectors']
    # Expand compressed columns to literal cubes and count all 24 frames.
    reconstructed=Counter()
    weights=Counter()
    for j,raw in cert['nonzero_cube_weights']:
        weight=Fraction(raw)/8
        cube=witnessed[vectors[j]]
        for sym in STAB:
            orbit=tuple(sorted(relabel(member,sym) for member in cube))
            assert orbit in actual_orbits
            weights[orbit]+=weight
            for member in orbit:reconstructed[member]+=weight
    common=tuple(Fraction(v)/8 for v in cert['common_counts'])
    for member in labels:
        assert reconstructed[member]==common[ix[canonical(member)[0]]]
    assert all(v>=0 for v in common) and all(w>0 for w in weights.values())
    assert sum(reconstructed.values())==24*sum(common)
    return {'source_mask':mask,'canonical_rows':len(rows),'literal_rows':len(labels),
            'coordinate_rows':3*len(rows),'compressed_vectors':len(vectors),
            'full_labelled_orbits':len(actual_orbits),
            'nonzero_expanded_orbits':len(weights),'literal_count_total':str(sum(common)),
            'root_count_total':cert['total_count'],
            'exact_full_labelled_equations_verified':True,
            'source_realizability':'not triggered'}


def main():
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--source-mask',type=int,default=932)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();result=run(args.source_mask)
    result['binding']={'reviewer_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
                       'root_checker_sha256':sha256((ROOT/'full_count_cone.py').read_bytes()).hexdigest(),
                       'root_certificate_sha256':sha256((ROOT/f'counts{args.source_mask}.json').read_bytes()).hexdigest()}
    with args.output.open('x') as out:json.dump(result,out,indent=2);out.write('\n')
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':main()
