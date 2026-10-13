#!/usr/bin/env python3
"""Literal-source control replay with independent numeric-order exhaustive DFS.

No repository colouring/planarity code is imported. --generate exclusively writes
this audit's controls. Every fibre contains ALL full lifts, including empty cells.
Minimal cores are enumerated only as edge-subgraphs of the two fixed old graphs;
this is not a graph/source search and supplies no target-source exclusion.
"""
from __future__ import annotations
import argparse
from collections import Counter
from copy import deepcopy
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DEFAULT = HERE / 'controls/graphs.json'
FRAME = {tuple(sorted((i, (i + 1) % 5))) for i in range(5)}
ROWS = [(0,1,0,1,2),(0,1,0,2,1),(0,1,0,2,3),(0,1,2,0,1),
        (0,1,2,0,2),(0,1,2,0,3),(0,1,2,1,2),(0,1,2,1,3),
        (0,1,2,3,1),(0,1,2,3,2)]
Q_INDEX = {0:6, 1:4, 2:3, 3:1, 4:0}
T4 = (2,5,7,8,9)
SELECTED = [
 ('SIGMA956-AD3', 'artifacts/c5_excess_two_independent_search/AD_k3/q_orbits/chunk_0001.json', 1, [0,4]),
 ('SIGMA1013-NA6', 'artifacts/c5_excess_two_independent_search/NA_k6/q_orbits/chunk_0001.json', 5, [2,3]),
]


def canonical_edges(edges):
    result = tuple(sorted(tuple(sorted(e)) for e in edges))
    assert len(result) == len(set(result)) and all(a < b for a,b in result)
    return result


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n').encode()


def reject(mask):
    return [q for q,index in Q_INDEX.items() if not (mask >> index & 1)]


def enumerate_lifts(vertices, edges, boundary):
    """Exhaustive fixed ascending vertex and ascending colour order; no MRV/DP."""
    adjacency = {v: [] for v in vertices}
    for a,b in edges:
        adjacency[a].append(b)
        adjacency[b].append(a)
    assignment = list(boundary) + [-1] * (len(vertices)-5)
    assert vertices == list(range(len(vertices)))
    assert all(assignment[a] != assignment[b] for a,b in edges if b < 5)
    result = []
    def visit(v):
        if v == len(vertices):
            result.append(assignment.copy())
            return
        unavailable = {assignment[w] for w in adjacency[v] if assignment[w] >= 0}
        for color in range(4):
            if color not in unavailable:
                assignment[v] = color
                visit(v+1)
        assignment[v] = -1
    visit(5)
    return result


def relation(vertices, edges, roots):
    rows = []
    for index,boundary in enumerate(ROWS):
        lifts = enumerate_lifts(vertices, edges, boundary)
        fibres = [{'root_colors': [a,b],
                   'lifts': [c for c in lifts if [c[roots[0]],c[roots[1]]] == [a,b]]}
                  for a,b in product(range(4), repeat=2)]
        rows.append({'index':index, 'boundary':list(boundary),
                     'accepted':bool(lifts), 'lift_count':len(lifts),
                     'root_relation':[f['root_colors'] for f in fibres if f['lifts']],
                     'fibres':fibres})
    mask = sum(1 << r['index'] for r in rows if r['accepted'])
    return {'sigma_mask':mask, 'Q':reject(mask), 'rows':rows}


def faces(rotation):
    darts = {(int(a),b) for a,ns in rotation.items() for b in ns}
    remaining = set(darts)
    result = []
    while remaining:
        first = min(remaining)
        current, face = first, []
        while True:
            assert current in remaining
            remaining.remove(current)
            a,b = current
            face.append(a)
            around = rotation[str(b)]
            current = (b, around[(around.index(a)-1) % len(around)])
            if current == first:
                break
        result.append(face)
    return result


def validate_embedding(vertices, edges, rotation, augmented):
    assert set(rotation) == {str(v) for v in vertices}
    adj = {v:set() for v in vertices}
    for a,b in edges:
        adj[a].add(b); adj[b].add(a)
    for v in vertices:
        assert len(rotation[str(v)]) == len(set(rotation[str(v)]))
        assert set(rotation[str(v)]) == adj[v]
    f = faces(rotation)
    assert len(vertices) - len(edges) + len(f) == 2
    assert any(len(c)==5 and all(tuple(sorted((c[i],c[(i+1)%5]))) in FRAME for i in range(5)) for c in f)
    apex = len(vertices)
    assert set(augmented) == {str(v) for v in range(apex+1)}
    assert set(augmented[str(apex)]) == set(range(5))
    assert all([w for w in augmented[str(v)] if w!=apex] == rotation[str(v)] for v in vertices)
    augmented_edges = canonical_edges(list(edges) + [(b,apex) for b in range(5)])
    assert {(min(int(v),w),max(int(v),w)) for v,ns in augmented.items() for w in ns} == set(augmented_edges)
    assert all(len(ns)==len(set(ns)) for ns in augmented.values())
    assert apex+1-len(augmented_edges)+len(faces(augmented)) == 2
    return {'rotation_faces':f, 'euler_characteristic':2,
            'ordered_B_is_facial':True, 'augmented_apex':apex}


def geometry(vertices, edges):
    degree = Counter(v for e in edges for v in e)
    internal = [v for v in vertices if v>=5 and degree[v]>0]
    adj = {v:set() for v in internal}
    for a,b in edges:
        if a>=5 and b>=5:
            adj[a].add(b); adj[b].add(a)
    def components(remaining):
        unseen, answer = set(remaining), []
        while unseen:
            found, todo = set(), [min(unseen)]
            while todo:
                v=todo.pop()
                if v in found: continue
                found.add(v); todo.extend((adj[v]&unseen)-found)
            unseen -= found; answer.append(sorted(found))
        return answer
    roots = [v for v in internal if degree[v]>4]
    remainder = components(set(internal)-set(roots))
    pieces=[]
    for c in remainder:
        attachments = {str(r):sorted(v for v in c if r in adj[v]) for r in roots}
        pieces.append({'vertices':c, 'root_attachments':attachments,
                       'boundary_attachments':[[v,b] for v in c for b in range(5) if tuple(sorted((v,b))) in edges]})
    mixed_count = sum(all(p['root_attachments'][str(r)] for r in roots) for p in pieces)
    return {'degrees':[[v,degree[v]] for v in vertices], 'effective_internal':internal,
            'epsilon':sum(degree[v]-4 for v in internal), 'internal_components':components(internal),
            'surplus_roots':roots, 'roots_adjacent':tuple(roots) in edges if len(roots)==2 else None,
            'pieces_after_roots':pieces, 'mixed_count':mixed_count}


def analyze_graph(vertices, edges, roots, selected):
    cache={}
    def result(e):
        e=canonical_edges(e)
        if e not in cache: cache[e]=relation(vertices,e,roots)
        return cache[e]
    original=result(edges)
    assert original['sigma_mask'] & 932 == 932
    assert set(selected) <= set(original['Q'])
    deletions=[]
    for edge in edges:
        if edge in FRAME: continue
        child=result([e for e in edges if e!=edge])
        newly=sorted(set(original['Q'])-set(child['Q']))
        deletions.append({'edge':list(edge), 'result':child,
                          'newly_accepted_q':newly,
                          'sigma_critical':child['sigma_mask']!=original['sigma_mask'],
                          'selected_critical':bool(set(newly)&set(selected))})
    minimal=[]
    traversal_counts={}
    for q in original['Q']:
        visited=set(); found=set()
        def descend(e):
            if e in visited: return
            visited.add(e)
            rejected_children=[]
            for edge in e:
                if edge in FRAME: continue
                child=tuple(x for x in e if x!=edge)
                if q in result(child)['Q']: rejected_children.append(child)
            if not rejected_children: found.add(e)
            for child in rejected_children: descend(child)
        descend(edges)
        traversal_counts[str(q)]=len(visited)
        for core in sorted(found):
            g=geometry(vertices,core)
            assert all(d>=4 for v,d in g['degrees'] if v in g['effective_internal'])
            core_deletions=[]
            for edge in core:
                if edge in FRAME: continue
                child=result(tuple(e for e in core if e!=edge))
                assert q not in child['Q']
                core_deletions.append({'edge':list(edge), 'result':child})
            minimal.append({'q':q, 'edges':[list(e) for e in core],
                            'geometry':g, 'result':result(core),
                            'minimality_deletions':core_deletions})
    z=sorted({c['q'] for c in minimal if c['geometry']['epsilon']==0})
    pair_unions=[]
    for first,second in combinations(minimal,2):
        if first['q']==second['q']: continue
        pair_unions.append({'q_pair':[first['q'],second['q']],
                           'union_equals_original':set(map(tuple,first['edges']))|set(map(tuple,second['edges']))==set(edges)})
    return {'original':original, 'deletions':deletions, 'minimal_cores':minimal,
            'core_search_rejection_preserving_subgraphs':traversal_counts,
            'Z':z, 'sigma_critical':all(d['sigma_critical'] for d in deletions),
            'selected_critical':all(d['selected_critical'] for d in deletions),
            'proper_subgraph_at_most_one_rejection':all(len(d['result']['Q'])<=1 for d in deletions),
            'core_pair_unions':pair_unions,
            'unique_coloring_queries':len(cache),
            'canonical_triple_rejected':{0,1,3} <= set(original['Q'])}


def build():
    inputs=[]; graphs=[]
    old_path=ROOT/'artifacts/c5_excess_two_arc_pair_critical/observations.json'
    old_raw=old_path.read_bytes(); old=json.loads(old_raw)
    inputs.append({'path':str(old_path.relative_to(ROOT)), 'sha256':sha256(old_raw).hexdigest()})
    for name,path,ordinal,selected in SELECTED:
        raw=(ROOT/path).read_bytes(); source=json.loads(raw)['q_orbits'][ordinal-1]
        inputs.append({'path':path,'sha256':sha256(raw).hexdigest()})
        edges=canonical_edges(source['canonical_edges'])
        vertices=list(range(max(v for e in edges for v in e)+1))
        geo=geometry(vertices,edges); roots=geo['surplus_roots']
        assert roots==[5,6] and geo['epsilon']==2
        augmented=source['augmented_rotation']
        rotation={str(v):[w for w in augmented[str(v)] if w in vertices] for v in vertices}
        embedding=validate_embedding(vertices,edges,rotation,augmented)
        analysis=analyze_graph(vertices,edges,roots,selected)
        saved=next(r for r in old['records'] if r['source']==path and r['ordinal']==ordinal)
        assert source['sigma_mask']==analysis['original']['sigma_mask']==saved['sigma_mask']
        assert analysis['Z']==saved['zero_core_rows']
        actual_cores={(c['q'],canonical_edges(c['edges'])) for c in analysis['minimal_cores']}
        saved_cores={(c['q'],canonical_edges(c['edges'])) for c in saved['cores']}
        assert actual_cores==saved_cores
        graphs.append({'id':name, 'source':path, 'ordinal':ordinal,
                       'vertices':vertices, 'ordered_B':list(range(5)),
                       'edges':[list(e) for e in edges], 'roots':roots,
                       'selected_rejections':selected, 'rotation':rotation,
                       'augmented_rotation':augmented, 'embedding':embedding,
                       'geometry':geo, 'analysis':analysis})
    assert graphs[0]['analysis']['sigma_critical'] and not graphs[0]['analysis']['selected_critical']
    assert graphs[0]['analysis']['Z']==[0,3,4]
    assert graphs[1]['analysis']['sigma_critical'] and graphs[1]['analysis']['selected_critical']
    assert graphs[1]['analysis']['Z']==[]
    return {'schema':'n2-bridge-literal-controls-v1', 'inputs':inputs,
            'row_order':[list(r) for r in ROWS], 'q_to_row_index':Q_INDEX,
            'T4_indices':list(T4), 'graphs':graphs,
            'source_exclusion_evidence':False,
            'canonical_N2_target_status':'not triggered',
            'minimal_core_completeness':'exhaustive rejection-preserving edge-subgraph DFS on these two fixed graphs only'}


def validate(data):
    assert data['schema']=='n2-bridge-literal-controls-v1'
    assert data['row_order']==[list(r) for r in ROWS]
    assert {int(q):i for q,i in data['q_to_row_index'].items()}==Q_INDEX
    assert data['T4_indices']==list(T4)
    assert data['source_exclusion_evidence'] is False
    assert data['canonical_N2_target_status']=='not triggered'
    assert len(data['graphs'])==2
    for item in data['inputs']:
        assert sha256((ROOT/item['path']).read_bytes()).hexdigest()==item['sha256']
    for g in data['graphs']:
        assert g['ordered_B']==list(range(5))
        edges=canonical_edges(g['edges']); vertices=g['vertices']
        assert g['embedding']==validate_embedding(vertices,edges,g['rotation'],g['augmented_rotation'])
        assert g['geometry']==geometry(vertices,edges)
        assert g['analysis']==analyze_graph(vertices,edges,g['roots'],g['selected_rejections'])
        assert not g['analysis']['canonical_triple_rejected']
    assert data['graphs'][0]['analysis']['sigma_critical']
    assert not data['graphs'][0]['analysis']['selected_critical']
    assert data['graphs'][1]['analysis']['proper_subgraph_at_most_one_rejection']


def negatives(data):
    cases=[]
    def test(name, mutate):
        bad=deepcopy(data); mutate(bad)
        try: validate(bad)
        except (AssertionError, ValueError, KeyError, IndexError):
            cases.append({'name':name,'status':'rejected'})
        else: raise AssertionError('mutation accepted: '+name)
    test('false_sigma_critical_implies_selected_critical',lambda d:d['graphs'][0]['analysis'].__setitem__('selected_critical',True))
    test('false_Z_at_most_one',lambda d:d['graphs'][0]['analysis'].__setitem__('Z',[]))
    test('delete_empty_fibre',lambda d:d['graphs'][0]['analysis']['original']['rows'][0]['fibres'].pop())
    def corrupt_lift(d):
        row=next(r for r in d['graphs'][0]['analysis']['original']['rows'] if r['accepted'])
        fibre=next(f for f in row['fibres'] if f['lifts'])
        fibre['lifts'][0][5]=fibre['lifts'][0][6]
    test('false_full_lift_on_original_edge_56',corrupt_lift)
    test('independent_B_relabel',lambda d:d['graphs'][0]['ordered_B'].__setitem__(0,1))
    def corrupt_rotation(d):
        ns=d['graphs'][0]['rotation']['5']; ns[0],ns[1]=ns[1],ns[0]
    test('rotation_swap',corrupt_rotation)
    test('target_not_triggered_as_exclusion',lambda d:d.__setitem__('source_exclusion_evidence',True))
    test('silently_force_q2_acceptance',lambda d:d['graphs'][1]['analysis']['original']['rows'][3].__setitem__('accepted',True))
    return cases


def summary(data,negative_results):
    return {'status':'PASS', 'checker':'independent numeric-order exhaustive DFS',
            'graphs':len(data['graphs']),
            'nonframe_edge_deletions':sum(len(g['analysis']['deletions']) for g in data['graphs']),
            'minimal_cores':sum(len(g['analysis']['minimal_cores']) for g in data['graphs']),
            'core_minimality_deletions':sum(len(c['minimality_deletions']) for g in data['graphs'] for c in g['analysis']['minimal_cores']),
            'unique_coloring_queries':sum(g['analysis']['unique_coloring_queries'] for g in data['graphs']),
            'canonical_N2_target_status':'not triggered',
            'negative_tests':negative_results}



def build_u4():
    """Replay fixed marked cores without reading any target masks/comparisons."""
    relative='artifacts/c5_excess_two_nonadjacent_two_mixed_core44/observations.json'
    raw=(HERE/'frozen'/relative).read_bytes(); primary=json.loads(raw)
    assert primary['pattern_order']==[list(r) for r in ROWS]
    assert primary['normalized_rejected_row']==list(ROWS[0])
    assert len(primary['forms'])==828
    counts=Counter(); records=[]; fingerprints=set()
    for fi,form in enumerate(primary['forms']):
        edges=canonical_edges(form['original_edges'])
        vertices=form['coloring_vertex_order']; roots=form['original_root_order']
        ports=form['port_order']
        assert vertices==list(range(max(v for e in edges for v in e)+1))
        assert ports[:2]==roots and len(ports)==len(set(ports))
        assert tuple(sorted(roots)) not in edges
        fingerprint=(edges,tuple(roots)); assert fingerprint not in fingerprints
        fingerprints.add(fingerprint)
        degree=Counter(v for e in edges for v in e)
        assert all(degree[v]==4 for v in vertices if v>=5)
        assert set(e for e in edges if e[1]<5)==FRAME
        witnesses=form['q_critical_witnesses']
        assert {tuple(w['edge']) for w in witnesses}==set(edges)-FRAME
        assert len(witnesses)==len(set(edges)-FRAME)
        for witness in witnesses:
            coloring=witness['coloring']; removed=tuple(witness['edge'])
            assert len(coloring)==len(vertices) and coloring[:5]==list(ROWS[0])
            assert all(0<=c<4 for c in coloring)
            assert all(coloring[a]!=coloring[b] for a,b in edges if (a,b)!=removed)
            counts['q_minimality_full_lifts']+=1
        rows=[]
        for ri,boundary in enumerate(ROWS):
            lifts=enumerate_lifts(vertices,edges,boundary)
            joint=sorted({tuple(c[v] for v in ports) for c in lifts})
            saved=form['rows'][ri]
            assert joint==list(map(tuple,saved['joint_port_tuples']))
            assert len(saved['full_coloring_witnesses'])==len(joint)
            for values,coloring in zip(joint,saved['full_coloring_witnesses']):
                assert len(coloring)==len(vertices) and coloring[:5]==list(boundary)
                assert all(0<=c<4 for c in coloring)
                assert all(coloring[a]!=coloring[b] for a,b in edges)
                assert tuple(coloring[v] for v in ports)==values
                counts['saved_full_lifts']+=1
            pins=sorted({values[:2] for values in joint})
            assert pins==list(map(tuple,saved['root_pairs']))
            fibres=[[i for i,values in enumerate(joint) if values[:2]==pin]
                    for pin in product(range(4),repeat=2)]
            assert fibres==saved['root_fibres_by_pin_order']
            counts['empty_fibres']+=sum(not f for f in fibres)
            counts['nonempty_fibres']+=sum(bool(f) for f in fibres)
            record={'index':ri,'boundary':list(boundary),'root_pairs':[list(p) for p in pins],
                    'joint_port_tuples':[list(t) for t in joint],
                    'root_fibres_by_pin_order':fibres,'all_full_lifts':lifts}
            assert bool(lifts)==(ri!=0)
            if len(set(boundary))==3 and ri!=0:
                collision=next((pair for pair in combinations(pins,2)
                                if pair[0][0]==pair[1][0] or pair[0][1]==pair[1][1]),None)
                assert collision is not None
                chosen=[next(c for c in lifts if tuple(c[v] for v in roots)==pin) for pin in collision]
                record['collision']={'root_pairs':[list(p) for p in collision],
                                     'full_lifts':chosen}
                counts['non_q_T3_collisions']+=1
            counts['full_rows']+=1; counts['all_full_lifts']+=len(lifts)
            rows.append(record)
        records.append({'form_index':fi,'family':form['family'],
                        'original_edges':[list(e) for e in edges],
                        'ordered_B':list(range(5)),'coloring_vertex_order':vertices,
                        'original_root_order':roots,'port_order':ports,'rows':rows})
        counts['marked_cores']+=1
    assert counts['marked_cores']==828 and counts['full_rows']==8280
    assert counts['non_q_T3_collisions']==3312 and counts['q_minimality_full_lifts']==15460
    assert counts['empty_fibres']+counts['nonempty_fibres']==132480
    return {'schema':'n2-bridge-u4-mask-free-v1',
            'input':{'path':relative,'sha256':sha256(raw).hexdigest()},
            'row_order':[list(r) for r in ROWS],
            'normalized_core_rejected_row':list(ROWS[0]),
            'claim':'Every other T3 row has two distinct root pins sharing one coordinate',
            'target_masks_used':False,
            'scope':'Fixed 828 marked necessary cores; arbitrary-size marked reduction inherited from U4 paper',
            'counts':dict(sorted(counts.items())),'forms':records}


def check_u4_negatives(data):
    """Semantic witness checks, independent of equality against rebuilt artifact."""
    def witness_valid(record,row,pin,coloring):
        assert len(coloring)==len(record['coloring_vertex_order'])
        assert coloring[:5]==row['boundary']
        assert all(0<=c<4 for c in coloring)
        assert all(coloring[a]!=coloring[b] for a,b in record['original_edges'])
        assert [coloring[v] for v in record['original_root_order']]==pin
    record=data['forms'][0]
    row=next(r for r in record['rows'] if 'collision' in r)
    pair=row['collision']['root_pairs']; lifts=row['collision']['full_lifts']
    assert pair[0]!=pair[1] and (pair[0][0]==pair[1][0] or pair[0][1]==pair[1][1])
    for pin,coloring in zip(pair,lifts):witness_valid(record,row,pin,coloring)
    results=[]
    bad=lifts[0].copy(); a,b=next(e for e in record['original_edges'] if e[0]>=5)
    bad[a]=bad[b]
    try:witness_valid(record,row,pair[0],bad)
    except AssertionError:results.append({'name':'U4_collision_full_lift_breaks_original_edge','status':'rejected'})
    else:raise AssertionError('corrupt full lift accepted')
    badpin=pair[0].copy(); badpin[0]=(badpin[0]+1)%4
    try:witness_valid(record,row,badpin,lifts[0])
    except AssertionError:results.append({'name':'U4_independently_recolored_root_pin','status':'rejected'})
    else:raise AssertionError('corrupt pin accepted')
    try:
        assert len(row['root_fibres_by_pin_order'][:-1])==16
    except AssertionError:results.append({'name':'U4_missing_empty_fibre','status':'rejected'})
    else:raise AssertionError('truncated fibres accepted')
    return results



def build_u4_t3_negative():
    relative='artifacts/c5_excess_two_nonadjacent_two_mixed_core44/control_input.json'
    raw=(HERE/'frozen'/relative).read_bytes(); source=json.loads(raw)
    edges=canonical_edges(source['edges']); core=canonical_edges(source['M_edges'])
    vertices=list(range(max(v for e in edges for v in e)+1))
    roots=source['roots_in_z_w_order']
    augmented={str(v):ns for v,ns in enumerate(source['original_apex_rotation'])}
    rotation={str(v):[w for w in augmented[str(v)] if w in vertices] for v in vertices}
    embedding=validate_embedding(vertices,edges,rotation,augmented)
    original=relation(vertices,edges,roots); retained=relation(vertices,core,roots)
    assert original['sigma_mask']==1018 and retained['sigma_mask']==1022
    assert original['Q']==retained['Q']==[4]
    deletions=[]
    for edge in edges:
        if edge in FRAME:continue
        smaller=relation(vertices,tuple(e for e in edges if e!=edge),roots)
        assert smaller['sigma_mask']!=original['sigma_mask']
        deletions.append({'edge':list(edge),'result':smaller})
    return {'schema':'n2-bridge-u4-t3-only-v1','id':source['id'],
            'input':{'path':relative,'sha256':sha256(raw).hexdigest()},
            'ordered_B':list(range(5)), 'vertices':vertices,'roots':roots,
            'edges':[list(e) for e in edges], 'M_edges':[list(e) for e in core],
            'rotation':rotation,'augmented_rotation':augmented,'embedding':embedding,
            'geometry':geometry(vertices,edges),'original':original,'M':retained,
            'nonframe_deletions':deletions, 'Sigma_critical':True,
            'T3_preservation':'triggered and holds',
            'all_ten_row_preservation':'counterexample',
            'T4_source':'not triggered', 'canonical_N2_target':'not triggered',
            'scope':'Counterexample only to strengthening omitted-mixed11 T3 preservation to equality of all ten rows'}



def build_arithmetic():
    qrows={q:ROWS[i] for q,i in Q_INDEX.items()}
    nonedges=[pair for pair in combinations(range(5),2) if pair not in FRAME]
    repetitions=[{'boundary_pair':list(pair),
                  'rows':[q for q,row in qrows.items() if row[pair[0]]==row[pair[1]]]}
                 for pair in nonedges]
    assert all(len(r['rows'])==2 for r in repetitions)
    signatures=[]
    for excluded in range(5):
        qset=[q for q in range(5) if q!=excluded]
        v_signatures=[tuple(qrows[q][v] for q in qset) for v in range(5)]
        e_signatures=[tuple(tuple(sorted((qrows[q][a],qrows[q][b]))) for q in qset)
                      for a,b in sorted(FRAME)]
        assert len(set(v_signatures))==5 and len(set(e_signatures))==5
        signatures.append({'excluded_q':excluded,'retained_rows':qset,
                           'vertex_signatures':[list(v) for v in v_signatures],
                           'boundary_edge_order':[list(e) for e in sorted(FRAME)],
                           'edge_signatures':[[list(pair) for pair in e] for e in e_signatures]})
    spectrum=[]
    for bits in product((False,True),repeat=5):
        accepted_q=[q for q in range(5) if bits[q]]
        mask=932+sum(1<<Q_INDEX[q] for q in accepted_q)
        rejected_q=sorted(set(range(5))-set(accepted_q))
        within_arc=any(set(rejected_q)<={start,(start+1)%5,(start+2)%5} for start in range(5))
        nonconsecutive=[list(t) for t in combinations(rejected_q,3)
                        if not any(set(t)=={start,(start+1)%5,(start+2)%5} for start in range(5))]
        spectrum.append({'mask':mask,'Q':rejected_q,'E_domain':1<=len(rejected_q)<=4,
                         'contained_in_consecutive_three_arc':within_arc,
                         'nonconsecutive_triples':nonconsecutive,
                         'canonical_triple_rejected':{0,1,3}<=set(rejected_q)})
    spectrum.sort(key=lambda r:r['mask'])
    assert [r['mask'] for r in spectrum if r['canonical_triple_rejected']]==[932,933,940,941]
    assert all(r['contained_in_consecutive_three_arc']==(not r['nonconsecutive_triples']) for r in spectrum)
    def normalize(row):
        labels={}; return tuple(labels.setdefault(c,len(labels)) for c in row)
    def transformed_mask(mask,direction,offset):
        return sum(1<<ROWS.index(normalize([row[(direction*j+offset)%5] for j in range(5)]))
                   for ri,row in enumerate(ROWS) if mask>>ri&1)
    orbits={str(mask):sorted({transformed_mask(mask,s,t) for s in (-1,1) for t in range(5)})
            for mask in (933,941)}
    assert transformed_mask(940,-1,1)==933
    outside_arcs={r['mask'] for r in spectrum if r['E_domain'] and not r['contained_in_consecutive_three_arc']}
    assert outside_arcs==set(orbits['933'])|set(orbits['941'])
    return {'schema':'n2-bridge-boundary-arithmetic-v1',
            'literal_q_rows':{str(q):list(row) for q,row in qrows.items()},
            'nonadjacent_repetitions':repetitions,'any_four_signatures':signatures,
            'all_T4_accepting_spectra':spectrum,'bad_arc_E_domain_D5_orbits':orbits,
            'whole_frame_reflection_940_to_933':{'index_map':[1,0,4,3,2],'result_mask':933},
            'canonical_three_rejection_masks':[932,933,940,941]}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--arithmetic',action='store_true')
    p.add_argument('--u4',action='store_true')
    p.add_argument('--u4-t3-negative',action='store_true')
    p.add_argument('--generate',action='store_true')
    p.add_argument('--check',action='store_true')
    p.add_argument('--artifact',type=Path,default=DEFAULT)
    p.add_argument('--negative-tests',action='store_true')
    args=p.parse_args()
    if args.arithmetic:
        artifact=(HERE/'controls/boundary_arithmetic.json') if args.artifact==DEFAULT else args.artifact
        data=build_arithmetic(); raw=encoded(data)
        if args.generate:
            with artifact.open('xb') as f:f.write(raw)
        else:
            assert artifact.read_bytes()==raw, 'Boundary arithmetic replay differs'
        print(json.dumps({'status':'PASS','spectra':32,'any_four_signature_sets':5,
                          'canonical_three_rejection_masks':data['canonical_three_rejection_masks'],
                          'artifact_sha256':sha256(raw).hexdigest()},sort_keys=True)); return
    if args.u4_t3_negative:
        artifact=(HERE/'controls/u4_t3_negative.json') if args.artifact==DEFAULT else args.artifact
        data=build_u4_t3_negative(); raw=encoded(data)
        if args.generate:
            with artifact.open('xb') as f:f.write(raw)
        else:
            assert artifact.read_bytes()==raw, 'U4 T3 negative replay differs'
        print(json.dumps({'status':'PASS','id':data['id'],
                          'artifact_sha256':sha256(raw).hexdigest(),
                          'M_mask':data['M']['sigma_mask'],'G_mask':data['original']['sigma_mask'],
                          'nonframe_deletions':len(data['nonframe_deletions']),
                          'all_ten_row_preservation':'counterexample',
                          'T3_preservation':'triggered and holds','canonical_N2_target':'not triggered'},sort_keys=True)); return
    if args.u4:
        artifact=(HERE/'controls/u4_mask_free.json') if args.artifact==DEFAULT else args.artifact
        data=build_u4(); raw=encoded(data)
        if args.generate:
            with artifact.open('xb') as f:f.write(raw)
        else:
            assert artifact.read_bytes()==raw, 'U4 mask-free replay differs'
        result={'status':'PASS','checker':'independent numeric-order mask-free DFS',
                'artifact_sha256':sha256(raw).hexdigest(),**data['counts']}
        if args.negative_tests:result['negative_tests']=check_u4_negatives(data)
        print(json.dumps(result,sort_keys=True)); return
    if args.generate:
        data=build(); raw=encoded(data)
        with args.artifact.open('xb') as f:f.write(raw)
        data=json.loads(raw)
    else:
        data=json.loads(args.artifact.read_bytes())
    validate(data)
    results=negatives(data) if args.negative_tests else []
    out=summary(data,results); out['artifact_sha256']=sha256(args.artifact.read_bytes()).hexdigest()
    print(json.dumps(out,sort_keys=True))

if __name__=='__main__':main()
