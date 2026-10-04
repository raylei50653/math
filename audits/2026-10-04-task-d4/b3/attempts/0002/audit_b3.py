#!/usr/bin/env python3
"""Independent B3 audit against the D4 immutable production snapshot.

Uses only Python stdlib and the D2 audit-local MRV solver, never production
enumerators, join helpers, or validators. Every run preserves its code, log,
result and exception under a fresh attempts directory.
"""
import argparse
from collections import Counter
from contextlib import redirect_stdout, redirect_stderr
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path
import shutil
import sys
import time
import traceback

sys.dont_write_bytecode = True
from independent_core import (B, U, FRAME, COUNTS, edge, edges, unique,
    normalize, powerset, connected, solve, witness, stored_relation,
    rotation_faces, walk)

REL = 'artifacts/c5_excess_two_mixed_core_four_spoke_mixed22_long_face/observations.json'
PREV = 'artifacts/c5_excess_two_mixed_core_four_spoke_mixed22/observations.json'
SHORT = 'artifacts/c5_excess_two_mixed_core_four_spoke_mixed22_short_face/observations.json'
ENVELOPE = {0, 3, 4}
OWNERS = {'none': (), 'a_only': (0,), 'b_only': (1,), 'shared_a_b': (0, 1)}
ALLOWED = {'none': {(), (0,), (3,), (4,), (0, 4), (3, 4)},
    'a_only': {(), (0,)}, 'b_only': {(), (3,)}, 'shared_a_b': {()}}
LEAVES = {'none04': ('none', (0, 4)), 'none34': ('none', (3, 4)),
    'a0': ('a_only', (0,)), 'b3': ('b_only', (3,)), 'sharedab': ('shared_a_b', ())}
SKELETON = FRAME | {edge(5, 6), edge(0, 5), edge(1, 5), edge(2, 6), edge(3, 6)}


def exact(beta, pair, owners, attachments):
    neighbors = [(h, beta[h]) for h in attachments] + [(5+j, pair[j]) for j in owners]
    deg = 4 - len(neighbors)
    palette = sorted(U - {c for _, c in neighbors})
    assert deg >= 1 and len(palette) >= deg
    return {'neighbors': neighbors, 'degree': deg, 'palette': palette,
        'slack': len(palette)-deg, 'distinct': len({c for _, c in neighbors}) == len(neighbors)}


def exact_serialized(item, beta, pair, owners, attachments):
    ex = exact(beta, pair, owners, attachments)
    assert item['original_root_colors'] == list(pair)
    assert [(x['original_neighbor'], x['literal_color']) for x in item['actual_external_neighbors']] == ex['neighbors']
    assert item['required_original_C_degree'] == ex['degree']
    assert item['exact_private_list'] == ex['palette']
    assert item['exact_list_size'] == len(ex['palette'])
    assert item['exact_degree_slack'] == ex['slack']
    assert item['all_actual_external_neighbor_colors_distinct'] == ex['distinct']
    COUNTS['serialized_exact_same_frame_lists_checked'] += 1
    return ex


def blocks(vs, es):
    """Audit-local Tarjan decomposition; edges are the original C edges."""
    adj = {v: set() for v in vs}
    for v, w in es:
        adj[v].add(w); adj[w].add(v)
    disc, low, stack, result = {}, {}, [], []
    def visit(v, parent=None):
        disc[v] = low[v] = len(disc)
        for w in sorted(adj[v]):
            if w == parent:
                continue
            if w not in disc:
                stack.append(edge(v,w)); visit(w,v); low[v] = min(low[v],low[w])
                if low[w] >= disc[v]:
                    found = set()
                    while True:
                        e = stack.pop(); found.update(e)
                        if e == edge(v,w): break
                    result.append(frozenset(found))
            elif disc[w] < disc[v]:
                stack.append(edge(v,w)); low[v] = min(low[v],disc[w])
    visit(min(vs))
    assert set(disc) == set(vs) and not stack
    return result


def audit(base):
    data = json.loads((base / REL).read_text())
    source = json.loads((base / PREV).read_text())
    short = json.loads((base / SHORT).read_text())
    rows = [tuple(q) for q in data['pattern_order']]
    assert rows == sorted({normalize(q) for q in product(range(4), repeat=5)
        if all(q[h] != q[(h+1)%5] for h in B)})
    assert rows == [tuple(q) for q in source['pattern_order']]
    result = {'schema': 1, 'scope': __doc__, 'read_only_snapshot': str(base),
        'input_sha256': {p: sha256((base/p).read_bytes()).hexdigest()
            for p in sorted({REL, PREV, SHORT, *data['input_sha256']})},
        'selected_frames': [], 'examples': {}, 'ledger': [],
        'claims_not_established_by_finite_checks': [
            'Arbitrary-size topology/Gallai leaf existence; assessed separately in notes.md',
            'Original B source spoke-omission/q-core theorem; inherited provenance checked',
            'Disk, target Sigma, criticality, or source realizability of fixed controls',
            'All mixed22, epsilon>=3, general exits, K_infinity=K_at_most_5, new Lean theorem']}
    for p, h in data['input_sha256'].items():
        assert sha256((base/p).read_bytes()).hexdigest() == h
        COUNTS['declared_input_hashes_checked'] += 1
    assert data['original_relation_contract'] == source['original_relation_contract']
    assert data['source_omission_and_q_core_conclusions'] == source['original_omission_q_core_identity']
    parts = {normalize(t) for t in product(range(4),repeat=4) if t[0]!=t[1] and t[2]!=t[3]}
    named = {}
    for p in parts:
        share = [(i,j-2) for i in range(2) for j in range(2,4) if p[i]==p[j]]
        name = 'D4' if not share else (f'S{share[0][0]}{share[0][1]}' if len(share)==1 else
            'Pstraight' if share==[(0,0),(1,1)] else 'Pcross')
        named[name] = p
    assert len(named) == 7
    assert unique([x['identity'] for x in data['contact_identity_table']]) == set(named)
    assert data['contact_identity_table'] == source['contact_identity_table']
    for x in data['contact_identity_table']:
        assert tuple(x['original_vertex_partition']) == named[x['identity']]
        assert x['original_vertex_classes'] == [[['x0','x1','y0','y1'][i]
            for i,c in enumerate(named[x['identity']]) if c==k] for k in sorted(set(named[x['identity']]))]
        COUNTS['independently_generated_contact_identities'] += 1

    for selected in data['selected_original_frames']:
        sigma = selected['source_sigma']; index = 101 if sigma==933 else 139
        target = next(t for t in source['targets'] if t['source_sigma']==sigma)
        frames = target['original_named_frames']
        f = next(f for f in frames if f['inherited_named_skeleton_index']==index)
        assert selected['named_source'] == f'W{sigma}-{index}'
        assert selected['inherited_original_named_frame'] == f
        assert f['original_spoke_supports'] == [[0,1],[2,3]]
        assert edges(f['original_root_and_boundary_edges']) == SKELETON
        face = selected['selected_original_long_face']
        assert face in f['retained_original_C_face_necessities']
        assert face['exact_actual_support_envelope'] == sorted(ENVELOPE)
        assert set(face['original_face']) == {0,3,4,5,6}
        assert all(edge(v,w) in SKELETON for v,w in zip(face['original_face'],face['original_face'][1:]+face['original_face'][:1]))
        assert {tuple(g['exact_actual_support_envelope']) for g in f['retained_original_C_face_necessities']} == {(1,2),(0,3,4)}
        for rr in f['fixed_original_skeleton_rotation_audit']['disk_rotations']:
            fs = rotation_faces({r['vertex']:r['ring'] for r in rr['rotation']}, SKELETON)
            assert {frozenset(g) for g in rr['mixed_capable_original_faces']} == {frozenset(g) for g in fs if {5,6}<=set(g)}
            assert {frozenset(g) for g in fs if {5,6}<=set(g)} == {frozenset([5,1,2,6]),frozenset([5,0,4,3,6])}
            COUNTS['inherited_fixed_disk_rotations_checked'] += 1
        s = next(x for x in short['selected_original_frames'] if x['source_sigma']==sigma)
        assert s['inherited_original_named_frame'] == f and s['named_short_face_residuals']==[]
        assert selected['named_long_face_residuals'] == []
        ids = selected['all_seven_original_contact_identity_results']
        assert unique([r['identity'] for r in ids]) == set(named)
        assert all(r['long_face_status']=='excluded_by_B3_arbitrary_size_original_K5_lemma' for r in ids)
        rejected = {i for i in range(10) if not sigma>>i&1}
        rps = {i:solve(B|{5,6},SKELETON,rows[i],[5,6]) for i in rejected}
        rr = face['rejected_rows_with_complete_original_root_pairs']
        assert unique([r['row_index'] for r in rr]) == rejected
        for r in rr:
            assert tuple(r['row']) == rows[r['row_index']]
            assert unique([tuple(p) for p in r['original_G_minus_C_root_pairs']]) == rps[r['row_index']]
            COUNTS['selected_face_complete_rejected_root_relations'] += 1
        for tab in face['per_original_vertex_attachment_necessities']:
            role = tab['original_vertex_role']; owners = OWNERS[role]
            allowed = {hs for hs in powerset(ENVELOPE) if 4-len(hs)-len(owners)>=1 and
                all(exact(rows[i],p,owners,hs)['slack']==0 for i in rejected for p in rps[i])}
            assert allowed == ALLOWED[role] == {tuple(t) for t in tab['permissible_actual_boundary_attachment_subsets']}
            assert face['necessary_minimum_C_degree_by_original_role'][role] == min(4-len(hs)-len(owners) for hs in allowed)==2
            for d in tab['internal_degree_for_subset']:
                assert d['required_original_C_degree'] == 4-len(d['actual_attachments'])-len(owners)
            COUNTS['all_rejected_row_actual_attachment_owner_intersections'] += 1
        retained = target['retained_named_skeleton_indices']
        assert len(unique(retained))==20 and index in retained
        rename = lambda v: 11-v if v in (5,6) else v
        swapped_edges = {edge(rename(v),rename(w)) for v,w in SKELETON}
        swapped = [g for g in frames if edges(g['original_root_and_boundary_edges'])==swapped_edges]
        assert len(swapped)==1
        partner = swapped[0]['inherited_named_skeleton_index']
        assert partner == (171 if sigma==933 else 279) and partner in retained
        result['ledger'].append({'source_sigma':sigma,'historical_retained_literal_rows':retained,
            'primary_named_source_excluded':index,'literal_primary_only_unjudged':[i for i in retained if i!=index],
            'literal_primary_only_unjudged_count':19,'exact_original_root_swap_correspondence':partner,
            'root_swap_counterpart_new_closure_registered':False,
            'original_historical_rows_rewritten':False})
        result['selected_frames'].append({'named_source':selected['named_source'],'long_envelope':sorted(ENVELOPE),
            'long_face_serialized_residuals':0,'distinct_B2_short_face_verified':True})

    fixed = data['fixed_complete_degree_and_original_K5_controls']
    palettes = fixed['exact_private_leaf_owner_palette_controls']
    subset_n = pair_n = 0
    for group in palettes['per_mask_actual_attachment_subset_audits']:
        sigma=group['source_sigma']; rejected={i for i in range(10) if not sigma>>i&1}
        rps={i:solve(B|{5,6},SKELETON,rows[i],[5,6]) for i in rejected}
        assert unique([r['row_index'] for r in group['all_rejected_rows']])==rejected
        for r in group['all_rejected_rows']:
            assert tuple(r['literal_boundary'])==rows[r['row_index']]
            assert unique([tuple(p) for p in r['complete_legal_root_pairs']])==rps[r['row_index']]
        assert unique([t['original_owner_role'] for t in group['original_owner_attachment_tables']])==set(OWNERS)
        for tab in group['original_owner_attachment_tables']:
            role=tab['original_owner_role']; owners=OWNERS[role]
            assert tab['original_root_owner_positions']==list(owners)
            permitted=set()
            candidates=tab['all_finite_attachment_subset_audits']
            expected={hs for hs in powerset(ENVELOPE) if 4-len(hs)-len(owners)>=1}
            assert unique([tuple(c['actual_boundary_attachment_subset']) for c in candidates])==expected
            for c in candidates:
                hs=tuple(c['actual_boundary_attachment_subset']); subset_n+=1
                computed={(i,p):exact(rows[i],p,owners,hs) for i in rejected for p in rps[i]}; pair_n+=len(computed)
                allowed=all(x['slack']==0 for x in computed.values())
                assert c['permissible_across_all_rejected_rows_and_all_legal_pairs']==allowed
                if allowed:
                    permitted.add(hs)
                    rr=c['all_rejected_row_exact_lists']; assert unique([r['row_index'] for r in rr])==rejected
                    assert c['actual_same_frame_slack_counterexample'] is None
                    for r in rr:
                        i=r['row_index']; assert tuple(r['literal_boundary'])==rows[i]
                        assert unique([tuple(p) for p in r['complete_legal_root_pairs']])==rps[i]
                        assert unique([tuple(e['original_root_colors']) for e in r['exact_same_frame_lists']])==rps[i]
                        for item in r['exact_same_frame_lists']: exact_serialized(item,rows[i],tuple(item['original_root_colors']),owners,hs)
                else:
                    assert c['all_rejected_row_exact_lists']==[]
                    failure=c['actual_same_frame_slack_counterexample']; i=failure['row_index']
                    assert i in rejected and tuple(failure['literal_boundary'])==rows[i]
                    item=failure['exact_same_frame_list']; p=tuple(item['original_root_colors']); assert p in rps[i]
                    assert exact_serialized(item,rows[i],p,owners,hs)['slack']>0
            assert permitted==ALLOWED[role]=={tuple(hs) for hs in tab['permissible_actual_boundary_attachment_subsets']}
            assert tab['minimum_necessary_original_C_degree']==2
    assert subset_n==palettes['all_finite_actual_attachment_subset_checks']==52
    assert pair_n==palettes['all_same_frame_row_root_pair_attachment_checks']==546
    COUNTS['independent_actual_attachment_subset_checks']=subset_n
    COUNTS['independent_rejected_row_pair_exact_list_checks']=pair_n
    sigs=palettes['five_degree_two_leaf_palette_signatures']; q=rows[1]; pairs=[(3,1),(2,3)]
    assert unique([s['original_leaf_type'] for s in sigs])==set(LEAVES)
    signatures={}
    for s in sigs:
        role,hs=LEAVES[s['original_leaf_type']]; owners=OWNERS[role]
        assert s['original_owner_role']==role and s['original_root_owner_positions']==list(owners)
        assert tuple(s['actual_boundary_attachments'])==hs
        assert [tuple(p) for p in s['exact_root_pair_order']]==pairs
        exacts=[exact_serialized(e,q,p,owners,hs) for e,p in zip(s['exact_same_frame_lists'],pairs,strict=True)]
        signatures[s['original_leaf_type']]=[e['palette'] for e in exacts]
        assert s['missing_color_membership']==[int(3 in e['palette']) for e in exacts]
        assert all(e['degree']==len(e['palette'])==2 for e in exacts)
        COUNTS['owner_and_actual_attachment_separating_leaf_signatures_checked']+=1
    assert len({tuple(map(tuple,x)) for x in signatures.values()})==5
    result['examples']['five_literal_leaf_signatures']=signatures
    result['examples']['single_row_shared_b0_hole']={'row':list(q),'all_row1_pairs_allow_shared_b0':
        all(exact(q,p,(0,1),(0,))['slack']==0 for p in solve(B|{5,6},SKELETON,q,[5,6])),
        'row6_has_strict_slack':exact(rows[6],(2,0),(0,1),(0,))}
    assert result['examples']['single_row_shared_b0_hole']['all_row1_pairs_allow_shared_b0']
    failures=palettes['shared_degree_one_actual_attachment_slack_counterexamples']
    assert unique([(x['source_sigma'],tuple(x['hypothetical_actual_boundary_attachment'])) for x in failures])==set(product((933,941),((0,),(3,),(4,))))
    for x in failures:
        i=x['rejected_row_index']; p=tuple(x['exact_same_frame_list']['original_root_colors']); hs=x['hypothetical_actual_boundary_attachment']
        assert not x['source_sigma']>>i&1 and p in solve(B|{5,6},SKELETON,rows[i],[5,6])
        assert tuple(x['literal_boundary'])==rows[i]
        ex=exact_serialized(x['exact_same_frame_list'],rows[i],p,(0,1),hs)
        assert ex['degree']==1 and len(ex['palette'])==2 and ex['slack']==1
        COUNTS['shared_degree_one_leaf_bridge_slack_controls_checked']+=1
    bridge=data['shared_contact_original_leaf_bridge_audit']
    assert bridge['shared_contact_leaf_bridge_is_possible'] is False and bridge['degree_two_shared_contacts_on_internal_bridge_chains_retained'] is True
    for x in bridge['exact_same_frame_slack_witnesses']:
        h=x['hypothetical_original_shared_contact_boundary_attachment']; i=x['common_rejected_row_index']; p=tuple(x['legal_original_G_minus_C_root_pair'])
        assert all(not sigma>>i&1 for sigma in (933,941)) and p in solve(B|{5,6},SKELETON,rows[i],[5,6])
        assert tuple(x['literal_boundary'])==rows[i]
        ex=exact(rows[i],p,(0,1),(h,))
        assert x['actual_external_neighbor_colors']==[*p,rows[i][h]]
        assert x['exact_list']==ex['palette'] and x['connected_slack']==ex['slack']==1
        COUNTS['common_shared_degree_one_leaf_bridge_slack_witnesses_checked']+=1

    ledger=data['complete_leaf_type_and_original_exterior_path_ledger']
    ledger_names={'none_04':'none04','none_34':'none34','a_only_0':'a0','b_only_3':'b3','shared_a_b':'sharedab'}
    assert unique([x['original_leaf_type'] for x in ledger])==set(ledger_names)
    for x in ledger:
        role,hs=LEAVES[ledger_names[x['original_leaf_type']]]; owners=OWNERS[role]
        hubs=list(hs)+[5+j for j in owners]
        # Ledger lists roots first, whereas exact-list entries list frame first.
        hubs=([5,0] if role=='a_only' else [6,3] if role=='b_only' else hubs)
        assert x['actual_private_external_neighbors']==hubs and edge(*hubs) in SKELETON
        assert tuple(x['actual_adjacent_hub_edge'])==edge(*hubs)
        path=x['actual_complementary_exterior_path']
        assert len(unique(path))==len(path) and set(path)==(B|{5,6})-set(hubs)
        assert all(edge(v,w) in SKELETON for v,w in zip(path,path[1:]))
        for h,e in zip(hubs,x['actual_hub_to_exterior_edge_witnesses'],strict=True):
            assert tuple(e) in SKELETON and h in e and next(v for v in e if v!=h) in path
        eligible=set()
        for name,p in named.items():
            counts=Counter(tuple(j for j in (0,1) if any(p[i]==v for i in (2*j,2*j+1))) for v in set(p))
            if not owners or counts[owners]>=2: eligible.add(name)
        assert unique(x['possible_labelled_contact_identities'])==eligible
        assert x['contact_leaf_is_triangle']==bool(owners)
        COUNTS['five_leaf_original_hub_complementary_path_ledgers_checked']+=1

    def reconstruct(rec,key):
        a,b=rec['original_root_order']; contacts=rec['ordered_original_contacts']
        assert normalize(contacts)==named[rec[key]]
        c=rec['original_components']['C']; cv=unique(c['vertices'])
        assert cv.isdisjoint(B|{a,b}) and set(contacts)<=cv and c['ordered_contacts']==contacts
        original=edges(rec['original_edges']); vs={v for e in original for v in e}
        assert vs==B|{a,b}|cv and rec['original_vertex_order']==sorted(vs)
        assert edges(rec['literal_frame_edges'])==FRAME and {e for e in original if set(e)<=B}==FRAME
        ce={e for e in original if set(e)&cv and not set(e)&{a,b}}
        internal={e for e in ce if set(e)<=cv}
        assert edges(c['edges'])==ce and edges(c['internal_edges'])==internal and connected(cv,internal)
        attachments={v:sorted(w if z==v else z for z,w in original if v in (z,w) and set((z,w))&B) for v in cv}
        assert {int(v):hs for v,hs in c['actual_attachments'].items()}==attachments
        assert c['actual_support']==sorted({h for hs in attachments.values() for h in hs})
        assert set(c['actual_support'])<=ENVELOPE
        owners={v:sorted(r for r in (a,b) if edge(r,v) in original) for v in cv}
        assert {int(v):sorted(rs) for v,rs in c['actual_original_owners'].items()}==owners
        assert owners=={v:sorted(set(([a] if v in contacts[:2] else [])+([b] if v in contacts[2:] else []))) for v in cv}
        owner_edges={edge(r,v) for v,rs in owners.items() for r in rs}
        assert edges(c['original_root_contact_edges'])==owner_edges and c['owners_by_ordered_role']==[a,a,b,b]
        assert rec['original_spoke_supports']==[[0,1],[2,3]]
        spokes={edge(a,h) for h in (0,1)}|{edge(b,h) for h in (2,3)}
        assert original==FRAME|ce|owner_edges|spokes|{edge(a,b)}
        degrees={v:sum(v in e for e in original) for v in vs}
        assert degrees=={int(v):n for v,n in rec['original_complete_degrees'].items()}
        assert all(degrees[v]==(5 if v in (a,b) else 4) for v in vs-B)
        assert rec['boundary_cyclic_order']==sorted(B) and rec['exact_actual_support_envelope']==sorted(ENVELOPE)
        COUNTS['complete_degree_graph_structures_reconstructed']+=1
        return a,b,contacts,c,cv,ce,internal,original,vs,spokes

    groups=[('cycle',fixed['complete_degree_relation_controls']),('internal_shared_bridge',fixed['positive_original_internal_shared_bridge_relation_controls'])]
    for label,recs in groups:
        assert len(recs)==(14 if label=='cycle' else 2)
        expected=set(product(named if label=='cycle' else ['S00'],(False,True)))
        assert unique([(r['identity'],r['root_swapped']) for r in recs])==expected
        cache={}; prefix=label+'_'
        for rec in recs:
            a,b,contacts,c,cv,ce,internal,original,vs,spokes=reconstruct(rec,'identity')
            assert [a,b]==([6,5] if rec['root_swapped'] else [5,6])
            assert c['actual_support']==sorted(ENVELOPE)
            if label=='internal_shared_bridge':
                chain=c['actual_original_internal_shared_bridge_chain']; shared=c['original_shared_bridge_internal_vertex']
                assert shared==7 and chain==[11,8,7,9,12]
                assert c['original_shared_vertex_C_degree']==2 and c['shared_vertex_is_degree_one_leaf'] is False
                incident={e for e in internal if shared in e}
                assert incident=={edge(8,7),edge(7,9)}==edges(c['original_shared_incident_C_edges_both_bridges'])
                assert c['actual_attachments'][str(shared)]==[] and set(c['actual_original_owners'][str(shared)])=={a,b}
                assert {frozenset(g) for g in c['original_block_vertex_sets']}==set(blocks(cv,internal))
                for e in incident:
                    assert not connected(cv,internal-{e})
                    COUNTS['positive_shared_incident_internal_bridge_deletions_checked']+=1
            assert unique([r['row_index'] for r in rec['rows']])==set(range(10))
            for row in rec['rows']:
                i=row['row_index']; beta=tuple(row['literal_boundary']); assert beta==rows[i]
                order=row['original_C_vertex_order']; assert order==sorted(B|cv)
                rc=stored_relation(row['complete_original_R_C'],order,FRAME|ce,beta,contacts,'original_R_C_witnesses_checked')
                assert rc==solve(B|cv,FRAME|ce,beta,contacts)
                COUNTS[prefix+'independent_complete_four_contact_relations']+=1
                variants=row['variants']; assert unique([v['name'] for v in variants])=={'G','G-C','G-a0','G-a1','G-b2','G-b3'}
                variant_data={}; byname={v['name']:v for v in variants}
                for v in variants:
                    oe=None if v['omitted_original_edge'] is None else edge(*v['omitted_original_edge'])
                    omit_c=v['original_C_omitted']; assert (v['name']=='G-C')==omit_c
                    assert oe is None or oe in spokes
                    actual=original-({oe} if oe else set())
                    if omit_c: actual={e for e in actual if not set(e)&cv}
                    active=B|{a,b}|(set() if omit_c else cv); ports=[a,b]+([] if omit_c else contacts)
                    assert edges(v['actual_edges'])==actual and v['original_vertex_order']==sorted(active) and v['original_port_order']==ports
                    assert v['named_role_order']==['a','b']+([] if omit_c else ['x0','x1','y0','y1'])
                    direct=solve(active,actual,beta,ports)
                    stored=stored_relation(v['complete_joint'],sorted(active),actual,beta,ports,'complete_joint_witnesses_checked')
                    assert stored==direct
                    def joined(beta,crelation):
                        return {(A,D,*t) for A,D in product(range(4),repeat=2)
                            if A!=D and not any(A==beta[h] for h in (0,1) if edge(a,h)!=oe)
                            and not any(D==beta[h] for h in (2,3) if edge(b,h)!=oe)
                            for t in ([()] if omit_c else crelation)
                            if omit_c or (A not in t[:2] and D not in t[2:])}
                    assert joined(beta,rc)==direct
                    COUNTS[prefix+'independent_complete_whole_graph_joints']+=1
                    cache[(rec['control_index'],i,v['name'])]=direct
                    variant_data[v['name']]=(active,actual,ports,direct)
                    assert unique([(f['a_color'],f['b_color']) for f in v['pinned_a_b_fibres']])==set(product(range(4),repeat=2))
                    for f in v['pinned_a_b_fibres']:
                        A,D=f['a_color'],f['b_color']; pf={t[2:] for t in solve(active,actual,beta,ports,{a:A,b:D})}
                        assert unique([tuple(t) for t in f['complete_C_role_fibre']])==pf=={t[2:] for t in direct if t[:2]==(A,D)}
                        entries=f['complete_C_role_fibre_with_original_witnesses']
                        assert unique([tuple(e['ordered_C_role_tuple']) for e in entries])==pf and f['empty_fibre']==(not pf)
                        for e in entries:
                            t=e['complete_literal_join_tuple']; assert tuple(t)==(A,D,*e['ordered_C_role_tuple'])
                            witness(sorted(active),e['original_complete_coloring_witness'],actual,beta,ports,t)
                            assert e['original_complete_coloring_witness']==next(z['coloring'] for z in v['complete_joint'] if z['tuple']==t)
                            COUNTS['complete_literal_fibre_witnesses_checked']+=1
                        COUNTS[prefix+'independent_pinned_root_pair_fibres']+=1
                        COUNTS[prefix+'independent_empty_pinned_root_pair_fibres']+=not pf
                    if oe:
                        r=next(z for z in oe if z in (a,b)); h=next(z for z in oe if z in B); pos=(a,b).index(r)
                        assert {t for t in direct if t[pos]!=beta[h]}=={tuple(t['tuple']) for t in byname['G']['complete_joint']}
                        COUNTS[prefix+'exact_original_spoke_restorations_checked']+=1
                assert unique([tuple(s['global_color_permutation']) for s in row['global_S4_controls']])==set(permutations(range(4)))
                for s in row['global_S4_controls']:
                    cp=s['global_color_permutation']; moved=tuple(cp[c] for c in beta)
                    assert tuple(s['transported_literal_boundary'])==moved
                    moved_rc=solve(B|cv,FRAME|ce,moved,contacts)
                    assert moved_rc=={tuple(cp[c] for c in t) for t in rc}
                    assert s['independently_recomputed_complete_C_relation_size']==len(moved_rc)
                    COUNTS[prefix+'independently_recomputed_global_S4_C_relations']+=1
                    for v in variants:
                        active,actual,ports,direct=variant_data[v['name']]
                        transformed={tuple(cp[c] for c in t) for t in direct}
                        # Recompute complete transported joint using literal original edges.
                        assert solve(active,actual,moved,ports)==transformed
                        COUNTS[prefix+'independently_recomputed_global_S4_whole_graph_joints']+=1
                        for item in v['complete_joint']:
                            witness(sorted(active),[cp[c] for c in item['coloring']],actual,moved,ports,[cp[c] for c in item['tuple']])
                            COUNTS[prefix+'global_S4_individual_joint_witnesses_checked']+=1
        for left,right in zip(recs[::2],recs[1::2],strict=True):
            rename=lambda z:11-z if z in (5,6) else z
            assert {edge(rename(v),rename(w)) for v,w in edges(left['original_edges'])}==edges(right['original_edges'])
            for lr,rr in zip(left['rows'],right['rows'],strict=True):
                assert lr['literal_boundary']==rr['literal_boundary']
                assert [e['tuple'] for e in lr['complete_original_R_C']]==[e['tuple'] for e in rr['complete_original_R_C']]
                for lv,rv in zip(lr['variants'],rr['variants'],strict=True):
                    assert {edge(rename(v),rename(w)) for v,w in edges(lv['actual_edges'])}==edges(rv['actual_edges'])
                    assert [rename(z) for z in lv['original_port_order']]==rv['original_port_order']
                    assert cache[(left['control_index'],lr['row_index'],lv['name'])]==cache[(right['control_index'],rr['row_index'],rv['name'])]
                    for lf,rf in zip(lv['pinned_a_b_fibres'],rv['pinned_a_b_fibres'],strict=True):
                        assert (lf['a_color'],lf['b_color'],lf['complete_C_role_fibre'],lf['empty_fibre'])==(rf['a_color'],rf['b_color'],rf['complete_C_role_fibre'],rf['empty_fibre'])
                    COUNTS[prefix+'literal_root_swap_relations_and_fibres_checked']+=1

    def validate_bags(rec,original,key):
        bags=rec[key]; assert len(bags)==5
        assert all(len(unique(g))==len(g) and connected(g,original) for g in bags)
        flat=[v for g in bags for v in g]; assert len(unique(flat))==len(flat)
        witnesses=rec['ten_original_edge_witnesses']
        assert unique([tuple(w['branch_set_pair']) for w in witnesses])==set(combinations(range(5),2))
        for w in witnesses:
            i,j=w['branch_set_pair']; v,z=w['original_edge']
            assert edge(v,z) in original and ((v in bags[i] and z in bags[j]) or (z in bags[i] and v in bags[j]))
            COUNTS['original_K5_interbag_edge_witnesses_checked']+=1
        return bags
    minors=fixed['conditional_original_leaf_K5_minor_controls']
    assert len(unique([x['name'] for x in minors]))==30
    leaf_counts=Counter()
    for x in minors:
        a,b,contacts,c,cv,ce,internal,original,vs,spokes=reconstruct(x,'original_contact_identity')
        leaf=x['original_leaf_odd_cycle']; private=x['original_leaf_private_vertices']; cut=x['original_leaf_cutvertex']
        assert len(leaf)>=3 and len(leaf)%2==1 and len(unique(leaf))==len(leaf) and leaf[0]==cut and private==leaf[1:]
        assert all(edge(v,w) in internal for v,w in zip(leaf,leaf[1:]+leaf[:1]))
        actual_blocks=blocks(cv,internal); assert unique([frozenset(g) for g in c['original_block_vertex_sets']])==set(actual_blocks)
        assert frozenset(leaf) in actual_blocks and all(set(leaf)&set(g)<={cut} for g in actual_blocks if g!=frozenset(leaf))
        role,hs=LEAVES[x['private_leaf_type']]; owners=OWNERS[role]
        assert x['private_leaf_original_owner']==role
        for v in private:
            assert sum(v in e for e in internal)==2
            assert set(c['actual_original_owners'][str(v)])=={(a,b)[j] for j in owners}
            assert tuple(c['actual_attachments'][str(v)])==hs
        hubs=x['original_adjacent_hub_pair']; assert edge(*hubs) in original
        assert all({w if z==v else z for z,w in original if v in (z,w) and (w if z==v else z) not in cv}==set(hubs) for v in private)
        remainder=cv-set(private); assert unique(x['original_C_minus_private_vertices'])==remainder and connected(remainder,internal)
        exterior=(B|{a,b})-set(hubs)
        assert unique(x['complementary_original_exterior_vertices'])==exterior
        assert edges(x['all_complementary_original_exterior_edges'])=={e for e in original if set(e)<=exterior}
        assert connected(exterior,original)
        bags=validate_bags(x,original,'five_original_connected_branch_sets')
        assert set(bags[0])|set(bags[1])==set(private) and set(bags[2])==remainder|exterior and bags[3:]==[[hubs[0]],[hubs[1]]]
        for p in x['actual_original_paths']:
            path=p['original_vertex_path']; assert len(unique(path))==len(path) and path[0]==cut and set(path)<=set(bags[2])
            pe=[edge(v,w) for v,w in zip(path,path[1:])]
            assert all(e in original for e in pe) and [tuple(e) for e in p['original_edge_path']]==pe
            COUNTS['conditional_leaf_actual_original_paths_checked']+=1
        leaf_counts[x['private_leaf_type']]+=1
        COUNTS['conditional_leaf_K5_controls_checked']+=1
        COUNTS['independent_block_cut_decompositions_checked']+=1
    assert dict(leaf_counts)=={'none04':6,'none34':6,'a0':3,'b3':3,'sharedab':12}
    for x in data['conditional_K4_actual_tether_controls']:
        original=edges(x['original_edges']); clique=unique(x['original_K4'])
        assert len(clique)==4 and all(edge(v,w) in original for v,w in combinations(clique,2))
        assert all(sum(v in e for e in original)==4 for v in clique)
        paths=x['actual_four_tether_paths']; assert unique([p[0] for p in paths])==clique
        interiors=[]
        for p in paths:
            assert len(unique(p))==len(p) and p[-1] in B|{5,6}
            assert all(edge(v,w) in original for v,w in zip(p,p[1:])); interiors.extend(p[1:-1])
            COUNTS['conditional_K4_actual_tether_paths_checked']+=1
        assert len(unique(interiors))==len(interiors) and not set(interiors)&(B|{5,6}|clique)
        bags=validate_bags(x,original,'five_original_branch_sets')
        assert set(bags[4])==B|{5,6}|set(interiors)
        assert x['unused_degree_edges_not_completed'] is True and x['fixed_pinned_root_pair_edge_minimality_used'] is False
        COUNTS['conditional_K4_tether_K5_controls_checked']+=1
    assert COUNTS['original_R_C_witnesses_checked']==2646
    assert COUNTS['complete_joint_witnesses_checked']==11414
    assert COUNTS['complete_literal_fibre_witnesses_checked']==11414
    assert sum('tuple' in x and 'coloring' in x for x in walk(data))==14060
    assert COUNTS['cycle_independent_complete_whole_graph_joints']==840
    assert COUNTS['internal_shared_bridge_independent_complete_whole_graph_joints']==120
    assert COUNTS['cycle_independent_pinned_root_pair_fibres']==13440
    assert COUNTS['internal_shared_bridge_independent_pinned_root_pair_fibres']==1920
    assert COUNTS['cycle_independent_empty_pinned_root_pair_fibres']==10024
    assert COUNTS['internal_shared_bridge_independent_empty_pinned_root_pair_fibres']==1432
    assert COUNTS['cycle_independently_recomputed_global_S4_C_relations']==3360
    assert COUNTS['internal_shared_bridge_independently_recomputed_global_S4_C_relations']==480
    assert COUNTS['cycle_global_S4_individual_joint_witnesses_checked']==257280
    assert COUNTS['internal_shared_bridge_global_S4_individual_joint_witnesses_checked']==16656
    assert COUNTS['original_K5_interbag_edge_witnesses_checked']==320
    assert COUNTS['conditional_leaf_actual_original_paths_checked']==42
    advertised=fixed['summary']
    for label,prefix,summary in [('cycle','cycle_',advertised),
            ('internal_shared_bridge','internal_shared_bridge_',advertised['internal_shared_bridge_control_summary'])]:
        assert summary['complete_degree_original_graphs']==(14 if label=='cycle' else 2)
        for declared,observed in [
                ('independently_recomputed_original_graph_joins','independent_complete_whole_graph_joints'),
                ('independently_recomputed_pinned_a_b_fibres','independent_pinned_root_pair_fibres'),
                ('explicitly_preserved_empty_pinned_a_b_fibres','independent_empty_pinned_root_pair_fibres'),
                ('exact_original_spoke_restorations','exact_original_spoke_restorations_checked'),
                ('root_swap_variant_checks','literal_root_swap_relations_and_fibres_checked'),
                ('independently_recomputed_global_S4_C_relations','independently_recomputed_global_S4_C_relations'),
                ('global_S4_complete_joint_witness_checks','global_S4_individual_joint_witnesses_checked')]:
            assert summary[declared]==COUNTS[prefix+observed]
        assert summary['all_nonempty_fibres_have_original_complete_coloring_witnesses'] is True
    assert advertised['conditional_original_leaf_K5_minors']==30
    assert advertised['independently_checked_original_minor_adjacencies']==300
    assert advertised['independently_checked_actual_external_paths']==42
    assert advertised['private_leaf_types']==5 and advertised['original_owner_types']==4
    assert advertised['finite_actual_attachment_subset_checks']==52
    assert advertised['finite_same_frame_row_root_pair_attachment_checks']==546
    assert advertised['positive_complete_degree_internal_shared_bridge_controls']==2
    assert advertised['fixed_controls_are_disk_source_realizations'] is False
    assert advertised['target_Sigma_or_criticality_claimed'] is False
    for key in ('full_mixed22_branch_excluded','epsilon_three_proved','source_graph_catalogue_enumerated','source_realizability_claimed','new_lean_theorem'):
        assert data['summary'][key] is False
    assert data['summary']['fixed_control_summary']==fixed['summary']
    result['summary']={'primary_named_sources':['W933-101','W941-139'],'named_long_face_residuals':0,
        'complete_degree_relation_graphs':16,'cycle_relation_graphs':14,'positive_shared_bridge_relation_graphs':2,
        'independent_four_contact_relations':160,'independent_whole_graph_joints':960,
        'literal_root_pair_fibres':15360,'empty_literal_root_pair_fibres':11456,
        'original_R_C_witnesses':2646,'original_joint_witnesses':11414,'original_fibre_witnesses':11414,
        'global_S4_C_relations':3840,'global_S4_direct_whole_graph_joints':23040,
        'global_S4_joint_witnesses':273936,'leaf_K5_minors':30,'K4_tether_K5_minors':2,
        'all_original_K5_interbag_edge_witnesses':320,'actual_leaf_exterior_paths':42,
        'attachment_subsets':52,'rejected_row_pair_exact_lists':546,
        'shared_degree_one_leaf_slack_controls':6,'shared_internal_bridge_edge_deletion_controls':4,
        'five_leaf_type_counts':dict(leaf_counts),'all_producer_modules_imported':False}
    result['counts']=dict(sorted(COUNTS.items())); result['all_checks_passed']=True
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--snapshot',type=Path,default=Path(__file__).resolve().parents[1]/'snapshot')
    parser.add_argument('--output',type=Path,default=Path(__file__).resolve().parent)
    args=parser.parse_args(); out=args.output.resolve(); out.mkdir(parents=True,exist_ok=True)
    attempts=out/'attempts'; attempts.mkdir(exist_ok=True)
    n=1
    while (attempts/f'{n:04d}').exists(): n+=1
    run=attempts/f'{n:04d}'; run.mkdir()
    for name in ('audit_b3.py','independent_core.py'):
        shutil.copy2(Path(__file__).resolve().parent/name,run/name)
    started=time.monotonic(); result=None; failure=None
    with (run/'run.log').open('w') as log, redirect_stdout(log), redirect_stderr(log):
        try:
            result=audit(args.snapshot.resolve())
        except BaseException as exc:
            failure=exc; traceback.print_exc()
            result={'all_checks_passed':False,'exception_type':type(exc).__name__,
                'exception':str(exc),'traceback':traceback.format_exc(),'counts':dict(sorted(COUNTS.items()))}
        result['elapsed_seconds']=round(time.monotonic()-started,3)
        result['attempt_directory']=str(run)
        print(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2))
    payload=json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    (run/'results.json').write_text(payload)
    if failure is not None:
        print(f'FAILED; preserved {run}',file=sys.stderr)
        raise failure
    (out/'results.json').write_text(payload)
    print(json.dumps({'all_checks_passed':True,'attempt_directory':str(run),'elapsed_seconds':result['elapsed_seconds'],'summary':result['summary']},sort_keys=True))


if __name__=='__main__': main()
