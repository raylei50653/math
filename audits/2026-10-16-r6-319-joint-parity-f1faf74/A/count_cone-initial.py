#!/usr/bin/env python3
"""Labelled count-cone relaxation; exact rational verification is stdlib-only.

The three palette partitions share one count vector. Canonical orbit sets
are never used as multiplicity vectors. This does not test realizability.
"""
import argparse
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from review_c_independent import canon, nine_partitions, projections, PAIRS

HERE=Path(__file__).resolve().parent
INPUT=HERE.parent/'C'/'combined-source-exploration.json'
MAP=(0,1,2,3,4,5,0,6,7)
PAIR_KEYS=[frozenset(frozenset(p) for p in pairs) for pairs in PAIRS]


@lru_cache(None)
def labelled_moves(row,pairing):
    split=tuple(row[i] for i in MAP)
    pp=[nine_partitions(tuple(i for i,c in enumerate(split) if c in palette))
        for palette in pairing]
    result=set()
    for first,second in product(*pp):
        bad=False
        for aa,bb in combinations(first+second,2):
            for x,y in combinations(aa,2):
                if any(x<k<y for k in bb) and any(k<x or k>y for k in bb):
                    bad=True
        if bad:
            continue
        labelled=[]
        for groups,palette in zip((first,second),pairing):
            touched=[]
            kept=[]
            for group in groups:
                mapped={MAP[v] for v in group}
                (touched if 0 in mapped else kept).append(mapped)
            if touched:
                kept.append(set.union(*touched))
            labelled.extend((group,palette) for group in kept)
        orbit=set()
        for selected in product((False,True),repeat=len(labelled)):
            image=list(row)
            for flag,(group,palette) in zip(selected,labelled):
                if flag:
                    for vertex in group:
                        image[vertex]=sum(palette)-image[vertex]
            orbit.add(tuple(image))
        # Different visible component flip choices must give distinct rows.
        assert len(orbit)==2**len(labelled)
        result.add(tuple(sorted(orbit)))
    return tuple(sorted(result))


def build():
    inputs=json.loads(INPUT.read_text())
    rowlists=[r['survivors'][0]['rows'] for r in inputs]
    assert all(r==rowlists[0] for r in rowlists)
    canonical=tuple(tuple('ABCD'.index(c) for c in s) for s in rowlists[0])
    assert len(canonical)==58
    canon_index={row:i for i,row in enumerate(canonical)}
    perms=tuple(permutations(range(4)))
    rows=tuple(sorted({tuple(p[c] for c in row) for row in canonical for p in perms}))
    assert len(rows)==24*58
    row_index={row:i for i,row in enumerate(rows)}
    classes=tuple(canon_index[canon(row)] for row in rows)
    orbit_sets=[set() for _ in PAIRS]
    for row in canonical:
        for pairing in PAIRS:
            for orbit in labelled_moves(row,pairing):
                if any(canon(member) not in canon_index for member in orbit):
                    continue
                for perm in perms:
                    changed=frozenset(frozenset(perm[c] for c in pair) for pair in pairing)
                    target=PAIR_KEYS.index(changed)
                    indices=tuple(sorted(row_index[tuple(perm[c] for c in member)]
                                         for member in orbit))
                    orbit_sets[target].add(indices)
    orbits=tuple(tuple(sorted(s)) for s in orbit_sets)
    positivity=[]
    for projection,mask in ((0,1022),(1,1022),(2,319)):
        for bit in range(10):
            if mask>>bit&1:
                indices=tuple(i for i,row in enumerate(canonical)
                              if projections(row)[projection]>>bit&1)
                assert indices
                positivity.append((projection,bit,indices))
    assert len(positivity)==25
    return canonical,rows,classes,orbits,tuple(positivity)


def binding():
    return {'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'partition_helper_sha256':sha256((HERE/'review_c_independent.py').read_bytes()).hexdigest(),
            'source_rows_sha256':sha256(INPUT.read_bytes()).hexdigest()}


def verify(cert,model):
    canonical,rows,classes,orbits,positivity=model
    assert cert['binding']==binding()
    n=tuple(Fraction(v) for v in cert['shared_canonical_counts'])
    assert len(n)==len(canonical) and all(v>=0 for v in n)
    for family,weights in enumerate(cert['nonzero_orbit_weights']):
        reconstructed=[Fraction(0) for _ in rows]
        seen=set()
        for index,value in weights:
            assert index not in seen
            seen.add(index)
            value=Fraction(value)
            assert value>0
            for member in orbits[family][index]:
                reconstructed[member]+=value
        assert all(value==n[classes[i]] for i,value in enumerate(reconstructed)), family
    assert all(sum(n[i] for i in indices)>=1 for _,_,indices in positivity)
    assert cert['canonical_rows']==[''.join('ABCD'[c] for c in r) for r in canonical]
    assert cert['labelled_rows']==len(rows)
    assert cert['orbit_counts']==[len(o) for o in orbits]
    assert cert['source_realizability']=='not triggered'


def solve(model):
    import numpy as np
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix
    canonical,rows,classes,orbits,positivity=model
    nsize=len(canonical)
    rsize=len(rows)
    starts=[]
    count=nsize
    for family in orbits:
        starts.append(count)
        count+=len(family)
    rr=[];cc=[];vv=[]
    for family in range(3):
        for row,index in enumerate(classes):
            rr.append(family*rsize+row);cc.append(index);vv.append(-1)
        for index,orbit in enumerate(orbits[family]):
            for row in orbit:
                rr.append(family*rsize+row);cc.append(starts[family]+index);vv.append(1)
    eq=coo_matrix((vv,(rr,cc)),shape=(3*rsize,count)).tocsr()
    ur=[];uc=[]
    for j,(_,_,indices) in enumerate(positivity):
        for i in indices:
            ur.append(j);uc.append(i)
    ub=coo_matrix((-np.ones(len(ur)),(ur,uc)),shape=(len(positivity),count)).tocsr()
    objective=np.zeros(count);objective[:nsize]=1
    result=linprog(objective,A_eq=eq,b_eq=np.zeros(3*rsize),
                   A_ub=ub,b_ub=-np.ones(len(positivity)),
                   bounds=(0,None),method='highs')
    if not result.success:
        raise RuntimeError('LP did not return feasibility; no exclusion claim: '+result.message)
    exact=[Fraction(float(x)).limit_denominator(1000000) for x in result.x]
    cert={'schema':'source319-v5-labelled-common-count-cone-feasible-v1',
          'binding':binding(),
          'canonical_rows':[''.join('ABCD'[c] for c in r) for r in canonical],
          'labelled_rows':len(rows),'orbit_counts':[len(o) for o in orbits],
          'positivity_obligations':[[p,b,list(indices)] for p,b,indices in positivity],
          'shared_canonical_counts':[str(v) for v in exact[:nsize]],
          'nonzero_orbit_weights':[[[i,str(exact[start+i])] for i in range(len(family))
                                    if exact[start+i]>0]
                                   for start,family in zip(starts,orbits)],
          'floating_solver_message':result.message,
          'exact_total_count':str(sum(exact[:nsize])),
          'conclusion':'The common-count necessary relaxation is feasible; no source realization or exclusion follows.',
          'source_realizability':'not triggered','full319_exclusion':'OPEN'}
    verify(cert,model)
    return cert


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--solve',action='store_true')
    parser.add_argument('--certificate',type=Path,default=HERE/'count-cone-feasible.json')
    args=parser.parse_args()
    model=build()
    if args.solve:
        certificate=solve(model)
        with args.certificate.open('x') as handle:
            json.dump(certificate,handle,indent=2)
            handle.write('\n')
    else:
        certificate=json.loads(args.certificate.read_text())
        verify(certificate,model)
    print(json.dumps({'ok':True,'canonical_rows':len(model[0]),'labelled_rows':len(model[1]),
                      'orbit_counts':[len(x) for x in model[3]],
                      'positivity_obligations':len(model[4]),
                      'exact_total_count':certificate['exact_total_count'],
                      'conclusion':'exact rational feasible relaxation; source realizability not triggered'},
                     sort_keys=True))


if __name__=='__main__':
    main()
