#!/usr/bin/env python3
"""Independent reconstruction of C's common-H two-cap necessary screen.

No C checker is imported. Restricted-growth partitions and the original
literal R palette table are rebuilt here. This is not source realization.
"""
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
C = HERE.parent / 'C'
COLOURS = range(4)
EDGES = ((0,1),(1,2),(2,3),(3,4),(4,5),(5,0),(0,6),(6,7),(7,0))
PAIRS = (((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2)))
PATTERNS = ('ABABC','ABACB','ABACD','ABCAB','ABCAC','ABCAD',
            'ABCBC','ABCBD','ABCDB','ABCDC')
TABLE = {(0,1,0,1): {(2,3),(3,2)}, (0,1,0,2): set(),
         (0,1,2,1): {(1,3),(3,1),(2,3),(3,2)},
         (0,1,2,3): {(1,3),(3,1)}}


def canon(values):
    seen=[]
    out=[]
    for value in values:
        if value not in seen:
            seen.append(value)
        out.append(seen.index(value))
    return tuple(out)


def name(row):
    return ''.join('ABCD'[c] for c in row)


def lift_record(row):
    z,s,j,i,w,t,p,q=row
    result=[]
    for v in COLOURS:
        if v in (s,j,i,w):
            continue
        rr=[]
        for r in COLOURS:
            if r in (s,v,w,t):
                continue
            normalized=canon((z,s,r,t,p,q))
            rr.append((r,normalized[4:] in TABLE[normalized[:4]]))
        result.append((v,rr))
    return result


def bit(values):
    return 1 << PATTERNS.index(name(canon(values)))


@lru_cache(None)
def projections(row):
    z,s,j,i,w,t,p,q=row
    a=bit((z,s,i,w,t)) if s!=i else 0
    b=bit((z,s,j,w,t)) if j!=w else 0
    u=0
    for v,_ in lift_record(row):
        u |= bit((z,s,v,w,t))
    return a,b,u


def support(rows):
    out=[0,0,0]
    for row in rows:
        for i,value in enumerate(projections(row)):
            out[i] |= value
    return out


@lru_cache(None)
def component_partitions(vertices):
    # Generate set partitions via restricted-growth strings, independently
    # of C's insertion-of-first-vertex recursion.
    if not vertices:
        return ((),)
    result=[]
    def visit(labels):
        if len(labels)==len(vertices):
            by_vertex=dict(zip(vertices,labels))
            if any(by_vertex[a]!=by_vertex[b] for a,b in EDGES
                   if a in by_vertex and b in by_vertex):
                return
            result.append(tuple(tuple(v for v,k in by_vertex.items() if k==j)
                                for j in range(max(labels)+1)))
            return
        for value in range(max(labels)+2):
            visit(labels+(value,))
    visit((0,))
    return tuple(result)


@lru_cache(None)
def moves(row, pairing):
    possible=[]
    left=component_partitions(tuple(v for v,c in enumerate(row) if c in pairing[0]))
    right=component_partitions(tuple(v for v,c in enumerate(row) if c in pairing[1]))
    for a,b in product(left,right):
        blocks=a+b
        # Reject alternating boundary endpoints of any two distinct actual
        # components, using the literal six-vertex disk boundary only.
        bad=False
        for first,second in combinations(blocks,2):
            for x,y in combinations(sorted(v for v in first if v<6),2):
                if any(x<k<y for k in second if k<6) and any(
                    k<x or k>y for k in second if k<6):
                    bad=True
        if bad:
            continue
        labelled=[(block,pairing[0]) for block in a]+[(block,pairing[1]) for block in b]
        orbit=set()
        for bits in product((False,True),repeat=len(labelled)):
            transformed=list(row)
            for choose,(block,pair) in zip(bits,labelled):
                if choose:
                    for vertex in block:
                        transformed[vertex]=sum(pair)-transformed[vertex]
            orbit.add(canon(transformed))
        possible.append(frozenset(orbit))
    return tuple(possible)


def close(rows):
    rows=set(rows)
    stages=[]
    while True:
        following={row for row in rows if all(any(orbit<=rows for orbit in moves(row,p))
                                             for p in PAIRS)}
        stages.append([len(rows),len(rows-following)])
        if rows==following:
            return rows,stages
        rows=following


@lru_cache(None)
def nine_partitions(vertices):
    if not vertices:
        return ((),)
    result=[]
    def visit(labels):
        if len(labels)==len(vertices):
            by_vertex=dict(zip(vertices,labels))
            if any(by_vertex[a]!=by_vertex[b] for a,b in
                   ((i,(i+1)%9) for i in range(9))
                   if a in by_vertex and b in by_vertex):
                return
            result.append(tuple(tuple(v for v,k in by_vertex.items() if k==j)
                                for j in range(max(labels)+1)))
            return
        for value in range(max(labels)+2):
            visit(labels+(value,))
    visit((0,))
    return tuple(result)


@lru_cache(None)
def nine_moves(row,pairing):
    mapping=(0,1,2,3,4,5,0,6,7)
    split=tuple(row[v] for v in mapping)
    choices=[nine_partitions(tuple(i for i,c in enumerate(split) if c in pair))
             for pair in pairing]
    result=set()
    for first,second in product(*choices):
        partitions=first+second
        bad=False
        for a,b in combinations(partitions,2):
            for x,y in combinations(a,2):
                if any(x<k<y for k in b) and any(k<x or k>y for k in b):
                    bad=True
        if bad:
            continue
        glued=[]
        for groups,palette in zip((first,second),pairing):
            touches=[]
            others=[]
            for group in groups:
                mapped={mapping[v] for v in group}
                (touches if 0 in mapped else others).append(mapped)
            if touches:
                others.append(set.union(*touches))
            glued.extend((group,palette) for group in others)
        orbit=set()
        for selected in product((False,True),repeat=len(glued)):
            image=list(row)
            for yes,(group,palette) in zip(selected,glued):
                if yes:
                    for vertex in group:
                        image[vertex]=sum(palette)-image[vertex]
            orbit.add(canon(image))
        result.add(frozenset(orbit))
    return tuple(result)


def nine_close(rows):
    rows=set(rows)
    stages=[]
    while True:
        following={row for row in rows if all(any(orbit<=rows for orbit in nine_moves(row,p))
                                             for p in PAIRS)}
        stages.append([len(rows),len(rows-following)])
        if rows==following:
            return rows,stages
        rows=following


def main():
    cert=json.loads((C/'shared-caps-exploration.json').read_text())
    catalog=json.loads((C/'cells.json').read_text())
    need_hash='04650cea947a5086360e895c1a7350690f53da745314379a3328b97ee02d81b8'
    assert sha256((C/'cells.json').read_bytes()).hexdigest()==need_hash
    upper=set()
    total=0
    empty_v=0
    empty_r=0
    for row in product(COLOURS,repeat=8):
        total+=1
        if any(row[a]==row[b] for a,b in EDGES):
            continue
        lifts=lift_record(row)
        empty_v+=not lifts
        empty_r+=sum(not rr for _,rr in lifts)
        if all(ok for _,rr in lifts for _,ok in rr):
            upper.add(canon(row))
    live,stages=close(upper)
    assert sorted(name(r) for r in upper)==cert['upper_rows']
    assert sorted(name(r) for r in live)==cert['fixed_rows']
    assert stages==[[r['live'],r['removed']] for r in cert['fixed_rounds']]
    masks=sorted(int(x) for x in catalog['cells'] if int(x)&~support(live)[0]==0)
    reports=[]
    survivors=[]
    for a,b in product(masks,repeat=2):
        restricted={r for r in live if projections(r)[0]&~a==0 and projections(r)[1]&~b==0}
        remaining,rounds=close(restricted)
        ss=support(remaining)
        good=ss==[a,b,319]
        reports.append((a,b,len(remaining),ss,good))
        if good:
            survivors.append((a,b,len(remaining)))
    expected=[(x['cap_masks'][0],x['cap_masks'][1],x['stable_rows'],
               x['stable_supports'],x['necessary_possible']) for x in cert['pairs']]
    assert reports==expected
    assert survivors==[(1022,1022,81)]
    nine_cert=json.loads((C/'split-nine-exploration.json').read_text())
    nine_live,nine_stages=nine_close(upper)
    assert sorted(name(r) for r in nine_live)==nine_cert['fixed_rows']
    assert nine_stages==[[r['live'],len(r['removed'])] for r in nine_cert['rounds']]
    nine_survivors=[]
    for a,b in product(masks,repeat=2):
        restricted={r for r in nine_live if projections(r)[0]&~a==0 and projections(r)[1]&~b==0}
        remaining,_=nine_close(restricted)
        if support(remaining)==[a,b,319]:
            nine_survivors.append({'caps':[a,b],'rows':sorted(name(r) for r in remaining)})
    assert nine_survivors==nine_cert['survivors']
    result={'ok':True,'schema':'independent-common-H-two-cap-review-v1',
            'original_assignments':total,'proper_empty_v_fibres':empty_v,
            'proper_empty_r_fibres':empty_r,'upper_rows':len(upper),
            'closure_stages':stages,'stable_rows':len(live),
            'cap_mask_pairs':len(reports),'survivors':survivors,
            'split_nine':{'closure_stages':nine_stages,'stable_rows':len(nine_live),
                          'candidate_pairs':len(masks)**2,
                          'survivors':[(x['caps'],len(x['rows'])) for x in nine_survivors],
                          'split_copies_required_connected':False},
            'catalogue_sha256':need_hash,
            'source_instances':0,'source_coverage':'not triggered',
            'binding':{'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
                       'C_certificate_sha256':sha256((C/'shared-caps-exploration.json').read_bytes()).hexdigest(),
                       'C_nine_certificate_sha256':sha256((C/'split-nine-exploration.json').read_bytes()).hexdigest()}}
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':
    main()
