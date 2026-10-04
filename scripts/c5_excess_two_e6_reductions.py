#!/usr/bin/env python3
"""E6 literal field arithmetic and fixed adjacent parallel-path embeddings.

No source-key enumeration and no Four Color Theorem oracle. The universal
paper arguments and exact residual interfaces are in E6 REPORT.md. These
finite checks do not formalize Jordan separation or the Gallai theorem.
Creation is exclusive; --check is read-only, byte-for-byte replay.
"""
from __future__ import annotations
import argparse
from hashlib import sha256
from itertools import combinations, product
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_e6/reductions.json'
FRAME = tuple(range(5))
FRAME_EDGES = frozenset(tuple(sorted((i, (i+1)%5))) for i in FRAME)
SELECTED = frozenset((0, 1, 3))
BASE = 'd00aba4e10ea2d05ab216fedd94f5a166b2777ad'
SOURCES = ('artifacts/c5_cells/cells.json',
           'artifacts/c5_excess_two_e3/REPORT.md',
           'artifacts/c5_excess_two_e3/adjacent_notes.md',
           'artifacts/c5_excess_two_e4/REPORT.md',
           'artifacts/c5_excess_two_e5/REPORT.md',
           'docs/c5_unary_shield_budget.md')


def edge(a, b):
    assert a != b
    return tuple(sorted((a, b)))


def profile_ok(q):
    q = frozenset(q)
    return len(q) <= 1 or (len(q) == 2 and tuple(sorted(q)) in FRAME_EDGES)


def subsets(values):
    values = tuple(sorted(values))
    return [s for n in range(len(values)+1) for s in combinations(values, n)]


def arithmetic(rows, row_of_q):
    branch_records = []
    expected_general = {
        941: [(0,1,2),(0,1,3),(0,1,4),(0,3,4),(1,2,3),(2,3,4)],
        933: [(0,1,2),(0,1,4),(0,3,4),(1,2,3),(2,3,4)],
        940: [(0,1,2),(0,1,4),(0,3,4),(1,2,3),(2,3,4)],
        932: [(0,1,2),(0,1,4),(0,3,4),(1,2,3),(2,3,4)]}
    expected_l3 = {941:[(0,1,2),(0,1,4),(0,3,4),(1,2,3)],
                   933:[(0,1,2),(1,2,3)],
                   940:[(0,1,4),(0,3,4)], 932:[]}
    consecutive = {tuple(sorted(((i-1)%5,i,(i+1)%5))) for i in FRAME}
    for mask in (941, 933, 940, 932):
        qg = tuple(q for q in FRAME if not mask >> row_of_q[q] & 1)
        assert SELECTED <= set(qg) and mask & 932 == 932
        profiles = [s for s in subsets(qg) if profile_ok(s)]
        # L1 forbids all proper superprofiles; inclusion containment keeps
        # optional rejected rows literal, not prefilled as accepted.
        assert all(SELECTED - set(s) for s in profiles)
        tests, general, single = [], [], []
        for s in combinations(FRAME, 3):
            deletions = []
            for j in s:
                dq = tuple(q for q in qg if any(
                    rows[row_of_q[q]][j] == rows[row_of_q[q]][k]
                    for k in s if k != j))
                deletions.append(dict(deleted_original_spoke_endpoint=j,
                                      redundant_rejected_singletons=dq))
            l1 = all(profile_ok(d['redundant_rejected_singletons']) for d in deletions)
            l3 = all(len(d['redundant_rejected_singletons']) <= 1 for d in deletions)
            if l1: general.append(s)
            if l3: single.append(s)
            tests.append(dict(actual_spoke_set=s, deletion_tests=deletions,
                              universal_L1_necessary=l1, E5_L3_necessary=l3,
                              consecutive_three_point_set=s in consecutive))
        assert general == expected_general[mask] and single == expected_l3[mask]
        no_mixed_three = [s for s in general if s not in consecutive]
        assert no_mixed_three == ([(0,1,3)] if mask == 941 else [])
        branch_records.append(dict(mask=mask, rejected_singletons=qg,
            all_possible_L1_proper_subgraph_profiles=profiles,
            epsilon_zero_proper_profiles=[s for s in profiles if len(s)<=1],
            every_edge_releases_at_least=len(qg)-2,
            universal_three_spoke_necessary=general,
            E5_L3_three_spoke_necessary=single,
            no_mixed_three_spoke_necessary=no_mixed_three,
            all_ten_field_tests=tests))
    long_u_queries = []
    for s in sorted(consecutive & set(expected_l3[941])):
        gap = next(tuple((start+i)%5 for i in range(4)) for start in FRAME
                   if set(((start+3)%5,start)) <= set(s)
                   and not set(((start+1)%5,(start+2)%5)) & set(s))
        qs = [q for q in sorted(SELECTED)
              if rows[row_of_q[q]][gap[0]] == rows[row_of_q[q]][gap[-1]]]
        assert qs
        q = qs[0]; beta = rows[row_of_q[q]]
        c = beta[gap[0]]
        a_colors = tuple(x for x in range(4) if x not in {beta[j] for j in s})
        b_colors = tuple(x for x in range(4) if x != c)
        assert len(a_colors) == 2 and len(b_colors) == 3
        assert c not in a_colors
        covers = []
        for capacity in (1,2):
            for forbidden in subsets(range(4)):
                if len(forbidden)>capacity: continue
                admissible_b = tuple(x for x in b_colors if x not in forbidden)
                pairs = [(a,b) for a,b in product(a_colors,admissible_b) if a!=b]
                assert pairs
                covers.append(dict(unary_capacity=capacity, exact_query_forbidden_set=forbidden,
                                   admissible_root_pairs=pairs))
        long_u_queries.append(dict(actual_a_spokes=s, complementary_three_edge_gap=gap,
            selected_rejected_singleton=q, literal_row=beta,
            repeated_gap_endpoint_color=c, legal_a_colors=a_colors,
            legal_b_colors_before_U=b_colors, all_capacity_queries=covers,
            scope='Capacity is only an exact common-root avoidance-query bound on a full U relation.'))
    assert len(long_u_queries)==4
    guards=[]
    for a_domain,b_domain in product(subsets(range(4)),repeat=2):
        pairs=[(a,b) for a,b in product(a_domain,b_domain) if a!=b]
        if a_domain and b_domain and not pairs:
            assert a_domain==b_domain and len(a_domain)==1
            guards.append(dict(E_z=a_domain,E_w=b_domain))
    assert len(guards)==4
    return dict(branches=branch_records, long_unary_star_gap_queries=long_u_queries,
                no_mixed_full_relation_guard=dict(nonempty_rejecting_domain_pairs=guards,
                    domain_pairs_checked=256,
                    premise='E_r derived from complete original unary tuples with lifts; one common color frame.'))


def orientation(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])


def components(vertices,edges):
    todo=set(vertices); result=[]
    while todo:
        stack=[min(todo)]; found=set()
        while stack:
            v=stack.pop()
            if v in found: continue
            found.add(v)
            stack.extend(sorted({w for e in edges if v in e for w in e if w!=v} & todo-found))
        todo-=found; result.append(sorted(found))
    return result


def parallel_path_controls():
    records=[]
    for direct_outer in (True,False):
        pos={0:(-30,-25),1:(30,-25),2:(40,20),3:(0,40),4:(-40,20),
             5:(-8,0),6:(8,0)}
        heights=(6,12,18) if direct_outer else (-18,-6,12)
        pos.update({7+i:(0,h) for i,h in enumerate(heights)})
        pos[10]=(0,7) if direct_outer else (0,-5)
        twig_owner=7 if direct_outer else 8
        edges=set(FRAME_EDGES)|{edge(5,6),edge(twig_owner,10),edge(9,3)}
        edges|={edge(r,p) for r in (5,6) for p in (7,8,9)}
        edges|=({edge(5,0),edge(6,1)} if direct_outer else
                {edge(7,0),edge(5,4),edge(6,1)})
        for e,f in combinations(sorted(edges),2):
            if set(e)&set(f): continue
            a,b=(pos[v] for v in e);c,d=(pos[v] for v in f)
            signs=(orientation(a,b,c),orientation(a,b,d),orientation(c,d,a),orientation(c,d,b))
            assert not (signs[0]*signs[1]<0 and signs[2]*signs[3]<0),(e,f)
            for x,y,z,s in ((a,b,c,signs[0]),(a,b,d,signs[1]),(c,d,a,signs[2]),(c,d,b,signs[3])):
                assert not (s==0 and min(x[0],y[0])<=z[0]<=max(x[0],y[0]) and
                            min(x[1],y[1])<=z[1]<=max(x[1],y[1])),(e,f)
        rotation={v:sorted({w for e in edges if v in e for w in e if w!=v},
            key=lambda w:math.atan2(pos[w][1]-pos[v][1],pos[w][0]-pos[v][0])) for v in pos}
        todo={(a,b) for a,b in edges}|{(b,a) for a,b in edges};faces=[]
        while todo:
            start=min(todo);cur=start;walk=[]
            while True:
                assert cur in todo;todo.remove(cur);a,b=cur;walk.append(a)
                ns=rotation[b];cur=(b,ns[(ns.index(a)+1)%len(ns)])
                if cur==start: break
            faces.append(walk)
        assert len(pos)-len(edges)+len(faces)==2
        assert any(len(f)==5 and set(f)==set(FRAME) for f in faces)
        ps=components(set(pos)-set(FRAME)-{5,6},edges)
        jordan=[5,6,9] if direct_outer else [5,7,6,9]
        assert all(edge(a,b) in edges for a,b in zip(jordan,jordan[1:]+jordan[:1]))
        hidden=[]
        for piece in ps:
            if set(piece)&set(jordan): continue
            assert all(orientation(pos[a],pos[b],pos[v])>0 for v in piece
                       for a,b in zip(jordan,jordan[1:]+jordan[:1]))
            support=sorted({w for e in edges if set(e)&set(piece) for w in e if w in FRAME})
            assert support==[]
            hidden.append(dict(complete_original_component=piece,actual_B_support=support))
        assert len(hidden)==(2 if direct_outer else 1)
        assert any(10 in p['complete_original_component'] for p in hidden)
        records.append(dict(zw_on_exterior_parallel_path_face=direct_outer,
            vertices=sorted(pos),full_edges=sorted(edges),positions={str(v):p for v,p in pos.items()},
            rotation={str(v):ns for v,ns in rotation.items()},faces=faces,
            roots=[5,6],four_original_paths=[[5,6],[5,7,6],[5,8,6],[5,9,6]],
            all_original_components=ps,exterior_Jordan_cycle=jordan,hidden_whole_components=hidden,
            scope='Fixed topology illustration, including off-path original component vertex. Not a degree-valid critical source.'))
    return records


def build():
    raw={p:(ROOT/p).read_bytes() for p in SOURCES}
    cells=json.loads(raw[SOURCES[0]])
    rows=tuple(map(tuple,cells['pattern_order']))
    qi={int(q):int(i) for i,q in cells['singleton_of_three_colour'].items()}
    assert qi=={0:6,1:4,2:3,3:1,4:0}
    return dict(schema='e6-reductions-v1',base=BASE,
        source_sha256={p:sha256(v).hexdigest() for p,v in raw.items()},
        script_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        literal_arithmetic=arithmetic(rows,qi),
        fixed_parallel_path_embeddings=parallel_path_controls(),
        evidence_boundary='Finite arithmetic and two explicit drawings only. Universal topology, saturation and hub arguments are paper proofs in REPORT.md.',
        workers=1,no_four_colour_theorem_oracle=True,no_source_key_enumeration=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true');args=parser.parse_args()
    payload=(json.dumps(build(),ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
    if args.check:
        assert OUT.read_bytes()==payload,'E6 reductions byte mismatch'
        print('CHECK OK: literal L1/L3 branch fields, long-U queries and both adjacent outer-edge cases')
    else:
        OUT.parent.mkdir(parents=True,exist_ok=True)
        with OUT.open('xb') as f:f.write(payload)
        print('CREATED',OUT)
    print('bytes',len(payload),'sha256',sha256(payload).hexdigest())


if __name__=='__main__':main()
