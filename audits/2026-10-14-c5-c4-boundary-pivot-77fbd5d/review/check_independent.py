#!/usr/bin/env python3
"""Independent literal cap/fibre audit; standard library, no primary-checker imports."""
import argparse
from collections import Counter
from itertools import combinations, product
import gzip
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
B5 = ((0,1,0,1,2),(0,1,0,2,1),(0,1,0,2,3),(0,1,2,0,1),(0,1,2,0,2),
      (0,1,2,0,3),(0,1,2,1,2),(0,1,2,1,3),(0,1,2,3,1),(0,1,2,3,2))
Q4 = ((0,1,0,1),(0,1,0,2),(0,1,2,1),(0,1,2,3))
B_EDGES = {(i,(i+1)%5) for i in range(5)}
EXPECTED = ((0,0,0,0,0,0,0,0,0,2),(0,1,1,0,0,0,0,0,1,0),
            (0,0,0,0,1,0,1,0,0,0),(1,1,0,1,0,0,0,0,0,0))

def normal(t):
    d = {}
    return tuple(d.setdefault(c,len(d)) for c in t)

def edge(a,b): return tuple(sorted((a,b)))

def cap_fibres(r, drop=None):
    q_vertices = (5,(r-1)%5,r,(r+1)%5)
    qs = [q for q in product(range(4),repeat=4) if all(q[i]!=q[(i+1)%4] for i in range(4))]
    fibres = {q:[] for q in qs}
    for c in product(range(4),repeat=6):
        if any(c[a]==c[b] for a,b in B_EDGES): continue
        if any(c[5]==c[i] for i in range(5) if i!=r and i!=drop): continue
        q = tuple(c[v] for v in q_vertices)
        fibres[q].append((c,B5.index(normal(c[:5]))))
    return fibres

def colorings(n, edges, pinned):
    adj = [set() for _ in range(n)]
    for a,b in edges: adj[a].add(b); adj[b].add(a)
    c = [-1]*n
    for v,col in pinned.items(): c[v] = col
    if any(c[a]>=0 and c[a]==c[b] for a,b in edges): return []
    out=[]
    def rec():
        todo = [v for v in range(n) if c[v]<0]
        if not todo: out.append(tuple(c)); return
        v = max(todo,key=lambda v:(len({c[w] for w in adj[v]}-{-1}),len(adj[v]),-v))
        for col in sorted(set(range(4))-{c[w] for w in adj[v]}):
            c[v]=col; rec()
        c[v]=-1
    rec()
    return out

def icosahedron_root_disk():
    # Two pentagonal rings with poles; delete the north pole and label its rim 0..4.
    old_edges=set(); faces=set()
    U=lambda i:1+i%5
    L=lambda i:6+i%5
    for i in range(5):
        for f in [(0,U(i),U(i+1)),(11,L(i),L(i+1)),(U(i),U(i+1),L(i)),(U(i),L(i-1),L(i))]:
            faces.add(tuple(sorted(f)))
            old_edges.update(edge(a,b) for a,b in combinations(f,2))
    mapping={old:old-1 for old in range(1,12)}
    return 11,{edge(mapping[a],mapping[b]) for a,b in old_edges if a and b}

def positive_control(name,n,edges):
    edges={edge(a,b) for a,b in edges}
    fibres=cap_fibres(3)
    g_by_literal={}
    for p in product(range(4),repeat=5):
        if all(p[a]!=p[b] for a,b in B_EDGES):
            g_by_literal[p]=colorings(n,edges,dict(enumerate(p)))
    counts=[len(g_by_literal[p]) for p in B5]
    g_mask=sum(1<<j for j,x in enumerate(counts) if x)
    h_edges=edges|{edge(n,b) for b in (0,1,2,4)}
    q_vertices=(n,2,3,4)
    complete_h_fibres={}
    for q,cap_rows in fibres.items():
        direct=set(colorings(n+1,h_edges,dict(zip(q_vertices,q))))
        joined={g+(q[0],) for c,j in cap_rows for g in g_by_literal[c[:5]]}
        assert direct==joined, (name,q)
        complete_h_fibres[''.join(map(str,q))]=sorted(direct)
    direct_counts=[len(complete_h_fibres[''.join(map(str,q))]) for q in Q4]
    predicted=[sum(a*b for a,b in zip(row,counts)) for row in EXPECTED]
    assert direct_counts==predicted
    degrees=Counter(v for e in h_edges for v in e)
    return dict(name=name,g_vertices=n,g_edges=sorted(edges),g_counts=counts,g_mask=g_mask,
                h_vertices=n+1,h_edges=sorted(h_edges),h_counts=direct_counts,
                h_mask=sum(1<<j for j,x in enumerate(direct_counts) if x),
                h_min_internal_degree=min(degrees[v] for v in range(n+1) if v not in q_vertices),
                full_g_fibres={''.join(map(str,p)):c for p,c in g_by_literal.items()},
                full_h_fibres=complete_h_fibres,
                full_h_lifts=sum(map(len,complete_h_fibres.values())))

def build():
    rotations=[]
    for r in range(5):
        fibres=cap_fibres(r)
        assert len(fibres)==84 and sum(map(len,fibres.values()))==216
        matrix=tuple(tuple(Counter(j for c,j in fibres[q])[i] for i in range(10)) for q in Q4)
        shift=(r-3)%5
        column_move=[B5.index(normal(tuple(p[(i-shift)%5] for i in range(5)))) for p in B5]
        for q in range(4):
            for j in range(10): assert matrix[q][column_move[j]]==EXPECTED[q][j]
        maps=[]
        for mask in range(1024):
            output=sum(1<<i for i in range(4) if any(a and mask>>j&1 for j,a in enumerate(matrix[i])))
            for q,full in fibres.items():
                assert any(mask>>j&1 for c,j in full)==bool(output>>Q4.index(normal(q))&1)
            maps.append(output)
        target_maps={}
        for mask in (932,933,941):
            rotated=sum(1<<column_move[j] for j in range(10) if mask>>j&1)
            target_maps[str(mask)]=dict(rotated_mask=rotated,output_mask=maps[rotated])
        assert [target_maps[str(m)]['output_mask'] for m in (932,933,941)]==[3,11,11]
        rotations.append(dict(omitted_spoke=r,ordered_q=(5,(r-1)%5,r,(r+1)%5),matrix=matrix,
                              all_1024_maps=maps,target_maps=target_maps,
                              complete_cap_fibres={''.join(map(str,q)):c for q,c in fibres.items()}))
    broken=cap_fibres(3,drop=0)[Q4[2]]
    negative_witness=next(c for c,j in broken if 941>>j&1)
    ico_n,ico_e=icosahedron_root_disk()
    controls=[positive_control('W5_scope_and_empty_fibre_control',6,B_EDGES|{(i,5) for i in range(5)}),
              positive_control('icosahedron_minus_degree5_root',ico_n,ico_e)]
    assert controls[1]['h_min_internal_degree']==5
    return dict(scope='Independent finite cap identity and complete positive-control fibres; no target source is realized and no external enumeration is rerun.',
                pattern_order=B5,q_order=Q4,rotations=rotations,
                same_frame_mask_queries=5*1024*84,cap_literal_lifts=5*216,
                positive_controls=controls,
                negative_drop_original_spoke_u_b0=dict(detected=True,literal_six_vertex_coloring=negative_witness),
                actual_target_sources=0)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    result=build();raw=json.dumps(result,sort_keys=True,indent=2)+'\n';path=HERE/'result.json.gz'
    if args.check:
        assert gzip.decompress(path.read_bytes()).decode()==raw, 'Saved independent result differs.'
        assert path.read_bytes()==gzip.compress(raw.encode(),mtime=0), 'Saved gzip is not deterministic.'
    else:path.write_bytes(gzip.compress(raw.encode(),mtime=0))
    print(json.dumps(dict(PASS=True,queries=result['same_frame_mask_queries'],cap_lifts=result['cap_literal_lifts'],
                         control_summary=[{k:c[k] for k in ('name','g_counts','g_mask','h_counts','h_mask','full_h_lifts')} for c in result['positive_controls']],
                         negative_control=True,actual_target_sources=0)))
if __name__=='__main__': main()
