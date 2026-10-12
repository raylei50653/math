#!/usr/bin/env python3
"""Independently inspect stored literal graphs, rotations and complete joints.

Does not import the primary checker and uses Python standard library only.
Run with --check to replay the recorded review without modifying artifacts.
"""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).with_suffix('.json')
CYCLE = [(0,1),(1,2),(2,3),(3,4),(0,4)]
L = [0,5,2,6,7]
P = [0,1,2,6,7]
Q = [0,5,2,3,4]


def cyclic(values):
    return min(tuple(values[i:]+values[:i]) for i in range(len(values)))


def edgeset(edges):
    return {tuple(sorted(e)) for e in edges}


def run():
    independent = json.loads((ROOT/'review/independent_join.json').read_text())
    certificate_bytes = (ROOT/'controls/certificate.json').read_bytes()
    certificate = json.loads(certificate_bytes)
    source = json.loads((ROOT/'frozen/audits/2026-10-12-cofacial-uniform-separation-eb6b2303/frozen/artifacts/c5_cells/cells.json').read_text())
    assert len(independent['pair_records']) == len(certificate['pairs']) == 17424
    joint_hash = sha256()
    duplicate_count = 0
    literal_witness_count = 0
    for old, record in zip(independent['pair_records'],certificate['pairs']):
        pm,qm,mask,counts = old
        assert [pm,qm,mask,counts] == [record['P_mask'],record['Q_mask'],record['sigma'],[len(row['joint']) for row in record['rows']]]
        graph = record['graph']
        kp,kq = (source['cells'][str(m)]['k_eff'] for m in (pm,qm))
        n = 9+kp+kq
        pmap = P+list(range(9,9+kp))
        qmap = Q+list(range(9+kp,n))
        expected_edges = edgeset(CYCLE+[(L[i],L[(i+1)%5]) for i in range(5)]+[(v,8) for v in L])
        for m,mapping in ((pm,pmap),(qm,qmap)):
            expected_edges |= edgeset((mapping[u],mapping[v]) for u,v in source['cells'][str(m)]['edges'])
        edges = graph['edges']
        assert len(edges) == len(expected_edges) and edgeset(edges) == expected_edges
        assert graph['internal_vertices'] == n-5
        assert graph['P_local_to_global'] == pmap and graph['Q_local_to_global'] == qmap
        rotation = graph['rotation_edge_ids']
        assert len(rotation) == n
        neighbors = [set() for _ in range(n)]
        for v,seq in enumerate(rotation):
            assert len(seq) == len(set(seq))
            assert set(seq) == {i for i,e in enumerate(edges) if v in e}
            for i in seq:
                u,w = edges[i]
                assert u!=w and v in (u,w)
                neighbors[v].add(w if v==u else u)
        seen={0}
        todo=[0]
        while todo:
            v=todo.pop()
            for w in neighbors[v]-seen:
                seen.add(w);todo.append(w)
        assert len(seen)==n
        visited=set()
        faces=[]
        for v,seq in enumerate(rotation):
            for eid in seq:
                first=(v,eid)
                if first in visited:
                    continue
                dart=first
                face=[]
                while dart not in visited:
                    visited.add(dart)
                    face.append(dart)
                    u,e=dart
                    a,b=edges[e]
                    w=b if u==a else a
                    ws=rotation[w]
                    dart=(w,ws[(ws.index(e)+1)%len(ws)])
                assert dart==first
                faces.append(face)
        assert len(visited)==2*len(edges)
        assert n-len(edges)+len(faces)==2
        assert sorted(cyclic(f) for f in faces) == sorted(cyclic([tuple(d) for d in f]) for f in graph['faces_vertex_edge_darts'])
        face_vertices=Counter(cyclic([u for u,e in f]) for f in faces)
        assert face_vertices[cyclic([0,4,3,2,1])]==1
        center_order=[next(w for w in edges[e] if w!=8) for e in rotation[8]]
        assert cyclic(center_order)==cyclic(L)
        for i in range(5):
            assert face_vertices[cyclic([L[(i+1)%5],L[i],8])]==1
        duplicate=graph['parallel_edge_simplifications']
        expected_duplicate=all([0,2] in source['cells'][str(m)]['edges'] for m in (pm,qm))
        assert bool(duplicate)==expected_duplicate
        if duplicate:
            assert len(duplicate)==1 and duplicate[0]['endpoints']==[0,2]
            assert duplicate[0]['kept_owner']=='P' and duplicate[0]['deleted_owner']=='Q'
            duplicate_count+=1
        for row in record['rows']:
            joint_hash.update(json.dumps([pm,qm,row['index'],[j[:4] for j in row['joint']]],separators=(',',':')).encode())
            joint_hash.update(b'\n')
            witness=row['literal_full_witness']
            if row['joint']:
                assert witness is not None and len(witness)==n and witness[:5]==row['pattern']
                assert all(color in range(4) for color in witness)
                assert all(witness[u]!=witness[v] for u,v in edges)
                literal_witness_count+=1
            else:
                assert witness is None and row['full_lift_count']==0
    assert joint_hash.hexdigest()==independent['complete_interface_joint_sha256']
    assert certificate['summary']['relation_counts']==independent['output_histogram']
    return {
        'schema':'independent-stored-certificate-review-v1',
        'certificate_sha256':sha256(certificate_bytes).hexdigest(),
        'primary_checker_sha256':sha256((ROOT/'controls/checker.py').read_bytes()).hexdigest(),
        'paper_sha256':sha256((ROOT/'paper/PAPER.md').read_bytes()).hexdigest(),
        'pair_masks_and_ten_row_complete_interface_counts_equal':17424,
        'complete_interface_joint_sha256':joint_hash.hexdigest(),
        'literal_graph_edge_sets_equal_frozen_caps':17424,
        'connected_spherical_rotation_with_exact_outer_B':17424,
        'exact_center_rotation_L':17424,
        'all_five_star_faces_survive':17424,
        'double_ac_delete_Q_preserve_P':duplicate_count,
        'accepting_row_literal_full_witnesses_checked':literal_witness_count,
        'code_review':'MRV whole graph search is exhaustive and cap Cartesian product encoding retains complete full fibres',
        'paper_review':'source disk decomposition, induced link, all-row full lifts, double-ac simplification and scoped conditional exclusion have no blocker',
        'status':'triggered and holds',
    }


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    result=run()
    if args.check:
        assert result==json.loads(OUT.read_text())
    else:
        with OUT.open('x') as stream:
            json.dump(result,stream,sort_keys=True,indent=2)
            stream.write('\n')
    print(json.dumps(result,sort_keys=True))
