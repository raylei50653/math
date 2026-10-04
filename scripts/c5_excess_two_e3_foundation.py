#!/usr/bin/env python3
"""E3 finite reduction and exact E1 positive controls; no graph search or 4CT.

Generation exclusively creates its output. --check is read-only byte replay.
Control graphs are the two extracted E1 minimum representatives, with original
ordered vertices, attachments, rotations and critical witnesses preserved.
"""
from __future__ import annotations
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import networkx as nx

FRAME=tuple(range(5))
CYCLE=tuple(sorted(tuple(sorted((i,(i+1)%5))) for i in FRAME))
T4=(2,5,7,8,9)
TRIPLE=(0,1,3)
E1_SHA='23a92b56f325bd4bd496d7e8dfb14714d8481618253f88243df4cb7916ca999e'

def canonical(obj):
    return json.dumps(obj,sort_keys=True,separators=(',',':')).encode()

def edge(u,v):
    return tuple(sorted((u,v)))

def components(verts,edges):
    left=set(verts); out=[]
    adj={v:set() for v in left}
    for u,v in edges:
        if u in left and v in left:adj[u].add(v);adj[v].add(u)
    while left:
        todo=[min(left)]; seen=set(todo)
        while todo:
            for w in adj[todo.pop()]:
                if w not in seen:seen.add(w);todo.append(w)
        left-=seen;out.append(tuple(sorted(seen)))
    return tuple(out)

def assignments(verts,edges,row):
    private=tuple(v for v in verts if v not in FRAME)
    answer=[]
    for colours in product(range(4),repeat=len(private)):
        f=dict(zip(FRAME,row));f.update(zip(private,colours))
        if all(f[u]!=f[v] for u,v in edges):answer.append(tuple(f[v] for v in verts))
    return tuple(answer)

def mask_for(verts,edges,patterns):
    return sum(1<<i for i,p in enumerate(patterns) if assignments(verts,edges,p))

def singleton_map(patterns):
    return {i:next(v for v in FRAME if row.count(row[v])==1)
            for i,row in enumerate(patterns) if len(set(row))==3}

def q_profile(mask, singles):
    q=tuple(sorted(v for i,v in singles.items() if not(mask>>i&1)))
    e=sum(u in q and v in q for u,v in CYCLE)
    c=len(q)-e if len(q)<5 else 1
    return q,c

def pair_isolated(q):
    return len(q)==3 and sum(u in q and v in q for u,v in CYCLE)==1

def reduction(cells,patterns,singles):
    rows={v:list(patterns[i]) for i,v in singles.items()}
    triples=[q for q in combinations(FRAME,3) if pair_isolated(q)]
    four=[]
    for key,cell in sorted(cells['cells'].items(),key=lambda kv:int(kv[0])):
        q,c=q_profile(int(key),singles)
        if len(q)==4:
            contained=[list(t) for t in triples if set(t)<=set(q)]
            assert c==1 and len(contained)==2
            four.append(dict(cell_mask=int(key),Q=list(q),contained_triples=contained,
                             only_Q_shape_used=True,T4_accepted=int(key)&932==932))
    assert {tuple(x['Q']) for x in four}==set(combinations(FRAME,4))
    allsets=[]
    for n in range(6):
        for q in combinations(FRAME,n):
            mask=sum(1<<i for i in T4)+sum(1<<i for i,v in singles.items() if v not in q)
            _,c=q_profile(mask,singles)
            bad=len(q)+c>4
            included=[list(t) for t in triples if set(t)<=set(q)]
            assert bad==bool(included)
            allsets.append(dict(Q=list(q),c=c,bad=bad,contained_triples=included))
    transports=[]
    for sign in (-1,1):
        for shift in FRAME:
            phi=[(shift+sign*v)%5 for v in FRAME]
            target=sorted(phi[v] for v in TRIPLE)
            assert pair_isolated(target)
            transported_rows=[]
            for v in TRIPLE:
                row=[None]*5
                for j,c in enumerate(rows[v]):row[phi[j]]=c
                assert all(row[u]!=row[w] for u,w in CYCLE)
                assert row.count(row[phi[v]])==1
                transported_rows.append(dict(original_singleton=v,target_singleton=phi[v],
                                             literal_row=row))
            transports.append(dict(phi=phi,target_Q=target,rows=transported_rows))
    possible=[m for m in range(1024) if m&932==932 and all(not(m>>i&1) for i,v in singles.items() if v in TRIPLE)]
    assert possible==[932,933,940,941]
    return dict(canonical_Q=list(TRIPLE),canonical_rejected_rows=[dict(singleton=v,index=i,row=list(patterns[i]))
                  for v in TRIPLE for i,s in singles.items() if s==v],
                catalogue_four_arcs=four,all_32_subsets=allsets,common_D5_transports=transports,
                permitted_complete_masks=possible,acceptance_of_indices_0_and_3_unrestricted=True)

def shield(verts,edges,rotation,piece):
    plane=nx.PlanarEmbedding();plane.set_data({int(v):ns for v,ns in rotation.items()});plane.check_structure()
    marked=set(); faces=[]; dart={}
    for u,v in sorted(plane.edges()):
        if (u,v) in marked:continue
        face=plane.traverse_face(u,v,marked); idx=len(faces);faces.append(face)
        for a,b in zip(face,face[1:]+face[:1]):dart[(a,b)]=idx
    keep=set(CYCLE)|{e for e in edges if all(v in set(FRAME)|set(piece) for v in e)}
    parent=list(range(len(faces)))
    def find(a):
        while parent[a]!=a:parent[a]=parent[parent[a]];a=parent[a]
        return a
    def union(a,b):parent[find(a)]=find(b)
    for u,v in edges:
        if (u,v) not in keep:union(dart[u,v],dart[v,u])
    others=set(verts)-set(FRAME)-set(piece)
    groups={find(i) for i,f in enumerate(faces) if set(f)&others}
    assert len(groups)==1
    region=next(iter(groups))
    visible={edge(u,v) for u,v in CYCLE if find(dart[u,v])==region or find(dart[v,u])==region}
    sigma=set(CYCLE)-visible
    support={u for u,v in edges if u in FRAME and v in piece}|{v for u,v in edges if v in FRAME and u in piece}
    sigma_vertices={v for e in sigma for v in e}
    if len(support)>=2:assert support==sigma_vertices
    outside_support={u for u,v in edges if u in FRAME and v in others}|{v for u,v in edges if v in FRAME and u in others}
    count=Counter(v for e in sigma for v in e)
    if sigma and len(sigma)<5:assert not(outside_support&{v for v,n in count.items() if n==2})
    return dict(piece=list(piece),support=sorted(support),shield_edges=[list(e) for e in sorted(sigma)],
                complement_frame_edges=[list(e) for e in sorted(visible)],
                containing_original_faces=[faces[i] for i in range(len(faces)) if find(i)==region])

def control(source,patterns,singles):
    rec=source['graph'];assert sha256(canonical(rec)).hexdigest()==source['record_sha256']
    verts=tuple(rec['vertices']); nonframe=tuple(map(tuple,rec['nonframe_edges']));edges=tuple(sorted(CYCLE+nonframe))
    assert tuple(map(tuple,rec['all_edges']))==edges
    private=tuple(v for v in verts if v not in FRAME)
    d=Counter(v for e in edges for v in e)
    assert all(d[v]>=4 for v in private)
    assert sum(d[v]-4 for v in private)==2
    assert len(components(private,edges))==1
    assert {u for u,v in nonframe if u in FRAME and v in private}==set(FRAME)
    roots=tuple(v for v in private if d[v]>4)
    assert sorted(d[v] for v in private)==rec['private_degree_sequence']
    assert all(sum(edge(v,b) in edges for b in FRAME)<=3 for v in private)
    sigma=mask_for(verts,edges,patterns);assert sigma==rec['sigma_mask'] and sigma&932==932
    q,c=q_profile(sigma,singles);assert list(q)==rec['Q']
    assert not any(set(t)<=set(q) for t in combinations(FRAME,3) if pair_isolated(t))
    full=[]
    for i,p in enumerate(patterns):
        rows=assignments(verts,edges,p)
        if str(i) in rec['accepted_colourings']:
            f=rec['accepted_colourings'][str(i)]
            assert tuple(f[str(v)] for v in verts) in rows
        full.append(dict(pattern_index=i,boundary=list(p),private_roles=list(private),
                         complete_private_tuples=[list(row[5:]) for row in rows]))
    critical=[]
    for old in rec['critical_edges']:
        e=tuple(old['edge']);deleted=tuple(f for f in edges if f!=e)
        new=mask_for(verts,deleted,patterns); assert new==old['sigma_after_deletion'] and new!=sigma
        added=[i for i in range(10) if new>>i&1 and not(sigma>>i&1)]
        assert added==old['newly_accepted_indices']
        f=old['colouring'];row=tuple(f[str(v)] for v in verts)
        assert row in assignments(verts,deleted,patterns[old['pattern_index']])
        assert f[str(e[0])]==f[str(e[1])]
        critical.append(old)
    pieces=components(set(private)-set(roots),edges)
    shield_records=[];relations=[];omissions=[];reject_witnesses=[]
    for piece in pieces:
        owner=tuple(r for r in roots if any(edge(r,v) in edges for v in piece))
        one_sided=len(components(set(private)-set(piece),edges))==1
        assert one_sided
        s=shield(verts,edges,rec['embedding']['disk_rotation'],piece)
        s['owners']=list(owner); s['original_root_incidences']=[list(e) for e in edges if
           any(v in piece for v in e) and any(v in roots for v in e)]
        if len(owner)==1:assert len(s['shield_edges'])>=2
        shield_records.append(s)
        contacts=tuple(v for v in piece if any(edge(v,r) in edges for r in roots))
        for i,p in enumerate(patterns):
            subverts=FRAME+piece
            subedges=tuple(e for e in edges if all(v in subverts for v in e))
            rs=assignments(subverts,subedges,p)
            relations.append(dict(piece=list(piece),owners=list(owner),contacts=list(contacts),
                                  pattern_index=i,roles=list(piece),complete_tuples=[list(r[5:]) for r in rs]))
            outside=tuple(v for v in verts if v not in piece)
            outedges=tuple(e for e in edges if all(v in outside for v in e))
            for outrow in assignments(outside,outedges,p):
                f=dict(zip(outside,outrow));lists={v:set(range(4))-{f[w] for e in edges if v in e for w in e if w!=v and w in f} for v in piece}
                def can_extend():
                    for colours in product(range(4),repeat=len(piece)):
                        g=dict(zip(piece,colours))
                        if all(g[v] in lists[v] for v in piece) and all(g[u]!=g[v] for u,v in edges if u in g and v in g):return True
                    return False
                if can_extend():continue
                assert all(len(lists[v])==sum(v in e and all(w in piece for w in e) for e in edges) for v in piece)
                used_root_colours={f[r] for r in owner}
                if len(s['shield_edges'])<=1:assert len(used_root_colours)>=2
                if len(owner)==2 and len(s['shield_edges'])<=1 and len(contacts)==1:
                    assert len(piece)==1
                    assert len(s['support'])==2 and tuple(s['support']) in CYCLE
                    outside_colours={f[w] for e in edges if piece[0] in e for w in e if w!=piece[0]}
                    assert len(outside_colours)==4
                reject_witnesses.append(dict(piece=list(piece),pattern_index=i,
                    complete_outside_colouring={str(v):f[v] for v in outside},lists={str(v):sorted(lists[v]) for v in piece}))
        remaining=tuple(v for v in verts if v not in piece)
        remaining_edges=tuple(e for e in edges if all(v in remaining for v in e))
        omissions.append(dict(omit_piece=list(piece),sigma=mask_for(remaining,remaining_edges,patterns)))
    assert len([s for s in shield_records if len(s['owners'])==1])<=2
    assert sum(len(s['shield_edges']) for s in shield_records)<=5
    assert all(not(set(map(tuple,a['shield_edges']))&set(map(tuple,b['shield_edges']))) for a,b in combinations(shield_records,2))
    # Complete piece joins: enumerate actual entire-piece relations together with roots.
    for i,p in enumerate(patterns):
        per_piece=[next(r['complete_tuples'] for r in relations if r['piece']==list(piece) and r['pattern_index']==i) for piece in pieces]
        joined=set()
        for rootcols in product(range(4),repeat=len(roots)):
            for tuples in product(*per_piece):
                f=dict(zip(FRAME,p));f.update(zip(roots,rootcols))
                for piece,cols in zip(pieces,tuples):f.update(zip(piece,cols))
                if all(f[u]!=f[v] for u,v in edges):joined.add(tuple(f[v] for v in private))
        assert sorted(joined)==sorted(map(tuple,full[i]['complete_private_tuples']))
    root_deletions=[]
    for absent in roots:
        kept=tuple(v for v in verts if v!=absent); es=tuple(e for e in edges if absent not in e)
        other_roots=tuple(r for r in roots if r!=absent)
        unary=[piece for piece in pieces if not any(edge(absent,v) in edges for v in piece)]
        side=tuple(sorted(set(FRAME)|set(other_roots)|{v for piece in unary for v in piece}))
        se=tuple(e for e in edges if all(v in side for v in e))
        deleted_mask=mask_for(kept,es,patterns);side_mask=mask_for(side,se,patterns)
        assert deleted_mask==side_mask
        root_deletions.append(dict(omit_root=absent,side_vertices=list(side),side_sigma=side_mask,deleted_sigma=deleted_mask))
    # Fixed positive-control subgraphs only, not a source-graph enumeration.
    valid=[]
    for bits in range(1<<len(nonframe)):
        es=tuple(e for i,e in enumerate(nonframe) if bits>>i&1)
        ds=Counter(v for e in CYCLE+es for v in e)
        effective=tuple(v for v in private if ds[v])
        if any(ds[v]<4 for v in effective):continue
        eps=sum(ds[v]-4 for v in effective);assert eps<=2
        if eps==2:assert es==nonframe
        valid.append(dict(nonframe_edges=[list(e) for e in es],epsilon=eps,effective_vertices=list(effective),
                          sigma=mask_for(FRAME+effective,CYCLE+es,patterns)))
    pair=edge(*roots) if len(roots)==2 else None
    zw=mask_for(verts,tuple(e for e in edges if e!=pair),patterns) if pair in edges else None
    return dict(source_pointer=source['pointer'],source_record_sha256=source['record_sha256'],
                vertices=list(verts),nonframe_edges=[list(e) for e in nonframe],sigma=sigma,Q=list(q),
                degrees={str(v):d[v] for v in verts},epsilon=2,roots=list(roots),root_edge=pair in edges,
                all_common_hypotheses_verified=True,selected_triple_hypothesis=False,
                general_lemma_controls={'degree_floor':'pass','connected_H_full_B_touch':'pass',
                   'spokes_at_most_three':'pass','same_excess_saturation':'pass',
                   'complete_same_frame_piece_joins':'pass','unary_shields_and_five_edge_budget':'pass',
                   'rejection_lists_tightness':'pass','short_mixed_monochromatic_roots_impossible':'pass',
                   'shared_contact_short_mixed_singleton':'pass' if len(roots)==2 else 'not_applicable_no_mixed',
                   'C_W_common_endpoint_P3':'not_applicable_no_original_P3_mixed',
                   'every_edge_critical_for_selected_triple':'not_applicable_selected_triple_absent'},
                complete_ordered_relations=full,complete_piece_relations=relations,critical_witnesses=critical,
                original_shields=shield_records,rejection_witnesses_with_tight_lists=reject_witnesses,
                piece_omissions=omissions,root_deletions=root_deletions,root_edge_omission_sigma=zw,
                saturation_control=dict(edge_subsets_checked=1<<len(nonframe),degree_valid_subgraphs=valid,
                                        full_excess_subgraphs=1))

def build(root):
    cellpath=root/'artifacts/c5_cells/cells.json'; raw=cellpath.read_bytes();cells=json.loads(raw)
    patterns=tuple(map(tuple,cells['pattern_order']));singles=singleton_map(patterns)
    assert singles=={0:4,1:3,3:2,4:1,6:0}
    path=root/'artifacts/c5_excess_two_e3/positive_control_inputs.json'; inputs=json.loads(path.read_text())
    assert inputs['source_sha256']==E1_SHA
    return dict(schema='e3-foundation-v1',base='2ddc6b4a4e412ab2cb7917fe4fb6fdeef2e86090',
                sources={str(cellpath.relative_to(root)):sha256(raw).hexdigest(),str(path.relative_to(root)):sha256(path.read_bytes()).hexdigest()},
                evidence_boundary='finite row/set arithmetic and two fixed graph controls; paper saturation/E2 dependency not proved by Python',
                reduction=reduction(cells,patterns,singles),positive_controls=[control(r,patterns,singles) for r in inputs['records']])

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);parser.add_argument('--output',type=Path);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    output=args.output or args.root/'artifacts/c5_excess_two_e3/foundation.json'
    result=build(args.root); raw=(json.dumps(result,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode()
    if args.check:
        assert output.read_bytes()==raw,'artifact byte mismatch'
        print('CHECK OK: all five four-arcs, 32 subsets, ten common D5 transports; exact E1 951/935 controls preserved')
    else:
        output.parent.mkdir(parents=True,exist_ok=True)
        with output.open('xb') as f:f.write(raw)
        print('CREATED',output)
    print('sha256',sha256(raw).hexdigest(),'bytes',len(raw))
if __name__=='__main__':main()
