#!/usr/bin/env python3
"""Independent stdlib-only positive cut-support verifier; imports no producer."""
from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import combinations,product
import json
from pathlib import Path

PAIRS=(((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2)))


def norm(row):
    seen={}
    return tuple(seen.setdefault(c,len(seen)) for c in row)


def proper(row):
    return all(row[i]!=row[(i+1)%len(row)] for i in range(len(row)))


def replay(path):
    obj=json.loads(path.read_text())
    boundaries=[tuple(s['boundary_order']) for s in obj['sides']]
    assert boundaries==[(2,6,7,8,4,5,0,1),(2,3,4,8,7,6)]
    sep=tuple(obj['separator_order'])
    assert sep==(2,6,7,8,4)
    expected_d16={tuple(map(int,s)) for s in (
        '010201','010212','010213','010231','012012','012021','012102','012121',
        '012123','012132','012301','012302','012312','012313','012321','012323')}
    assert set(map(tuple,obj['d16_patterns']))==expected_d16
    patterns=[]
    supports=[]
    for s,boundary in zip(obj['sides'],boundaries):
        ps=sorted({norm(row) for row in product(range(4),repeat=len(boundary)) if proper(row)})
        assert list(map(list,ps))==s['pattern_order']
        patterns.append(ps)
        selected=set(s['support_indices'])
        assert len(selected)==len(s['support_indices'])
        assert [list(ps[i]) for i in sorted(selected)]==s['support_patterns']
        supports.append(selected)
        witnesses={(w['pattern_index'],w['split']):w for w in s['complete_orbit_witnesses']}
        assert len(witnesses)==len(s['complete_orbit_witnesses'])==3*len(selected)
        for i in selected:
            row=ps[i]
            for split,pairs in enumerate(PAIRS):
                w=witnesses[i,split]
                blocks=w['blocks']
                owner={v:j for j,block in enumerate(blocks) for v in block}
                assert sum(map(len,blocks))==len(row) and set(owner)==set(range(len(row)))
                assert all(block and any(all(row[v] in pair for v in block) for pair in pairs) for block in blocks)
                assert all(not(row[v] in pair and row[(v+1)%len(row)] in pair)
                           or owner[v]==owner[(v+1)%len(row)]
                           for v in range(len(row)) for pair in pairs)
                assert not any(owner[a]==owner[c] and owner[b]==owner[d] and owner[a]!=owner[b]
                               for a,b,c,d in combinations(range(len(row)),4))
                mate={a:b for pair in pairs for a,b in (pair,pair[::-1])}
                orbit=set()
                for bits in product((False,True),repeat=len(blocks)):
                    target=tuple(mate[c] if bits[owner[v]] else c for v,c in enumerate(row))
                    assert proper(target)
                    orbit.add(ps.index(norm(target)))
                assert orbit<=selected and sorted(orbit)==w['orbit_indices']
    indices=[{p:i for i,p in enumerate(ps)} for ps in patterns]
    edges={tuple(sorted((a,b))) for boundary in boundaries
           for a,b in zip(boundary,boundary[1:]+boundary[:1])}
    compatible=set()
    forbidden=set()
    joins=[]
    outer=set()
    selected_pairs=set()
    fibres={ell:[] for ell in product(range(4),repeat=5)}
    for f in product(range(4),repeat=9):
        if any(f[a]==f[b] for a,b in edges):
            continue
        pair=tuple(indices[s][norm(tuple(f[v] for v in b))] for s,b in enumerate(boundaries))
        compatible.add(pair)
        if norm(f[:6]) not in expected_d16:
            forbidden.add(pair)
        if all(pair[s] in supports[s] for s in range(2)):
            assert norm(f[:6]) in expected_d16
            joins.append(f)
            outer.add(norm(f[:6]))
            selected_pairs.add(pair)
            fibres[tuple(f[v] for v in sep)].append(f)
    assert sorted(compatible)==list(map(tuple,obj['full_domain_compatible_pairs']))
    assert sorted(forbidden)==list(map(tuple,obj['full_domain_forbidden_pairs']))
    assert joins==list(map(tuple,obj['join_rows']))
    assert outer==expected_d16==set(map(tuple,obj['outer_projection_patterns']))
    assert list(obj['seed_union_row'])==[0,1,2,1,2,1,3,2,3]
    assert tuple(obj['seed_union_row']) in joins
    assert len(obj['complete_separator_fibres'])==4**5
    for entry,(ell,rows) in zip(obj['complete_separator_fibres'],fibres.items()):
        assert tuple(entry['separator_word'])==ell
        assert list(map(tuple,entry['joint_rows']))==rows
    nonempty=sum(bool(f) for f in fibres.values())
    counts=dict(side_patterns=list(map(len,patterns)),selected_side_patterns=list(map(len,supports)),
        compatible_pairs=len(compatible),forbidden_pairs=len(forbidden),
        selected_compatible_pairs=len(selected_pairs),joint_literal_rows=len(joins),
        nonempty_separator_fibres=nonempty,empty_separator_fibres=4**5-nonempty)
    assert counts==obj['counts']
    data=json.dumps(joins,sort_keys=True,separators=(',',':')).encode()
    assert sha256(data).hexdigest()==obj['join_sha256']
    return dict(status='pass',scope='positive support-only relaxation certificate',counts=counts,
                results_sha256=sha256(path.read_bytes()).hexdigest())


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--results',type=Path,required=True)
    p.add_argument('--out',type=Path)
    args=p.parse_args()
    result=replay(args.results)
    rendered=json.dumps(result,indent=2)+'\n'
    if args.out:
        args.out.write_text(rendered)
    print(rendered,end='')
