#!/usr/bin/env python3
"""D5 independent B4 W933-129 shared-contact actual attachment {4} audit.

Reads immutable returned reports and artifact bytes. All complete relations,
pinned fibres and witnesses are checked by audit-only original-edge MRV search.
No production checker, solver, joint helper or witness validator is imported.
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
    normalize, powerset, connected, solve, solve_witnesses, witness,
    stored_relation, rotation_faces, rotation_key, exhaustive_disk_rotations)

REL = 'artifacts/c5_excess_two_mixed_core_four_spoke_mixed22_shared4/observations.json'
PREV = 'artifacts/c5_excess_two_mixed_core_four_spoke_mixed22/observations.json'
LONG = 'artifacts/c5_excess_two_mixed_core_four_spoke_mixed22_long_face/observations.json'
REPORT = 'docs/c5_excess_two_mixed_core_four_spoke_mixed22_shared4.md'
HISTORY = 'docs/history/2026-10-04-excess-two-four-spoke-mixed22-shared4.md'
SA, SB = (0, 4), (1, 2)
ENVELOPE = {2, 3, 4}
SKELETON = FRAME | {edge(5,6)} | {edge(5,h) for h in SA} | {edge(6,h) for h in SB}
OWNERS = {'none': (), 'a_only': (0,), 'b_only': (1,), 'shared_a_b': (0,1)}
ALLOWED = {'none': {(),(2,),(3,),(4,),(2,3),(3,4)},
           'a_only': {(),(4,)}, 'b_only': {(),(2,),(4,)}, 'shared_a_b': {(),(4,)}}
SURVIVING = {k:{(),(4,)} for k in OWNERS}


def dump(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2)+'\n')


def named_identities():
    result = {}
    for p in {normalize(t) for t in product(range(4),repeat=4) if t[0]!=t[1] and t[2]!=t[3]}:
        shared = [(i,j-2) for i in range(2) for j in range(2,4) if p[i]==p[j]]
        name = ('D4' if not shared else f'S{shared[0][0]}{shared[0][1]}' if len(shared)==1
            else 'Pstraight' if shared==[(0,0),(1,1)] else 'Pcross')
        result[name] = p
    assert len(result)==7
    return result


def private_list(beta, pair, owners, attachments):
    degree=4-len(owners)-len(attachments)
    ls=U-{beta[h] for h in attachments}-{pair[j] for j in owners}
    return degree, sorted(ls)


def validate_path(path, bag, es, start=None, finish=None):
    assert path and len(unique(path))==len(path) and set(path)<=set(bag)
    assert start is None or path[0]==start
    assert finish is None or path[-1]==finish
    assert all(edge(v,w) in es for v,w in zip(path,path[1:]))
    COUNTS['actual_original_paths_checked']+=1


def relation_records(relation):
    return [{'tuple':list(t),'coloring':f} for t,f in sorted(relation.items())]


def audit(base, run):
    data=json.loads((base/REL).read_text())
    source=json.loads((base/PREV).read_text())
    long=json.loads((base/LONG).read_text())
    rows=[tuple(q) for q in data['pattern_order']]
    assert rows==sorted({normalize(q) for q in product(range(4),repeat=5)
        if all(q[h]!=q[(h+1)%5] for h in B)})
    assert rows==[tuple(q) for q in source['pattern_order']]
    hashes={p:sha256((base/p).read_bytes()).hexdigest() for p in
        sorted({REL,PREV,LONG,REPORT,HISTORY,*data['input_sha256']})}
    for p,h in data['input_sha256'].items():
        assert hashes[p]==h
        COUNTS['declared_input_hashes_checked']+=1
    assert data['original_relation_contract']==source['original_relation_contract']
    assert data['source_omission_and_q_core_conclusions']==source['original_omission_q_core_identity']
    assert data['inherited_B3_scope']==long['summary']
    assert data['named_original_frame']=='W933-129'
    target=next(t for t in source['targets'] if t['source_sigma']==933)
    frames=target['original_named_frames']
    frame=next(f for f in frames if f['inherited_named_skeleton_index']==129)
    assert data['inherited_original_named_frame']==frame
    assert frame['original_spoke_supports']==[list(SA),list(SB)]
    assert edges(frame['original_root_and_boundary_edges'])==SKELETON
    face=data['selected_original_long_face']
    assert face in frame['retained_original_C_face_necessities']
    assert face['original_face']==[2,6,5,4,3]
    assert face['exact_actual_support_envelope']==sorted(ENVELOPE)
    assert all(edge(v,w) in SKELETON for v,w in zip(face['original_face'],face['original_face'][1:]+face['original_face'][:1]))
    assert {tuple(f['exact_actual_support_envelope']) for f in frame['retained_original_C_face_necessities']}=={(0,1),(2,3,4)}
    saved_rots=frame['fixed_original_skeleton_rotation_audit']['disk_rotations']
    n_rot, all_rots=exhaustive_disk_rotations(SKELETON)
    assert len(saved_rots)==2
    saved_keys=set()
    for rr in saved_rots:
        rotation={r['vertex']:r['ring'] for r in rr['rotation']}
        fs=rotation_faces(rotation,SKELETON)
        assert {frozenset(f) for f in fs if {5,6}<=set(f)}=={frozenset([0,5,6,1]),frozenset([2,6,5,4,3])}
        assert {frozenset(f) for f in rr['mixed_capable_original_faces']}=={frozenset(f) for f in fs if {5,6}<=set(f)}
        assert rr['original_outer_boundary'] in fs
        saved_keys.add(rotation_key(rotation))
        COUNTS['literal_original_frame_rotations_checked']+=1
    assert saved_keys==all_rots
    COUNTS['all_original_frame_rotation_candidates_enumerated']=n_rot

    named=named_identities()
    identities=data['all_seven_original_identities_and_designated_shared_branches']
    assert unique([x['inherited_original_identity']['identity'] for x in identities])==set(named)
    assert [x['inherited_original_identity'] for x in identities]==source['contact_identity_table']
    scope=[]
    for item in identities:
        ident=item['inherited_original_identity']; name=ident['identity']; p=named[name]
        assert tuple(ident['original_vertex_partition'])==p
        assert ident['original_ordered_roles']==['x0','x1','y0','y1']
        expected=[{'original_vertex_class':v,'roles':[ident['original_ordered_roles'][i]
            for i,k in enumerate(p) if k==v]} for v in sorted(set(p))
            if v in p[:2] and v in p[2:]]
        assert item['possible_designated_shared_vertices']==expected
        status='excluded_by_original_cut_parity_K5' if expected else 'not_applicable_no_shared_contact'
        assert item['designated_shared_attachment4_status']==status
        assert item['other_actual_attachment_branches']=='retained_without_new_claim'
        scope.append({'identity':name,'partition':list(p),'conditional_designated_choices':expected,
            'actual_designated_attachment':[4] if expected else None,'this_attachment_branch_excluded':bool(expected),
            'other_attachment_branches_retained':True})
        COUNTS['original_contact_identities_checked']+=1
        COUNTS['designated_shared_original_vertex_choices']+=len(expected)
    assert COUNTS['designated_shared_original_vertex_choices']==8

    rejected={i for i in range(10) if not 933>>i&1}
    assert rejected=={1,3,4,6}
    root_rel={i:solve(B|{5,6},SKELETON,rows[i],[5,6]) for i in rejected}
    assert sum(map(len,root_rel.values()))==11
    rr=face['rejected_rows_with_complete_original_root_pairs']
    assert unique([x['row_index'] for x in rr])==rejected
    for row in rr:
        i=row['row_index']; assert tuple(row['row'])==rows[i]
        assert unique([tuple(p) for p in row['original_G_minus_C_root_pairs']])==root_rel[i]
    allowed={}
    for tab in face['per_original_vertex_attachment_necessities']:
        role=tab['original_vertex_role']; owners=OWNERS[role]
        assert tuple(tab['fixed_root_owners'])==owners
        candidates={hs for hs in powerset(ENVELOPE) if 4-len(owners)-len(hs)>=1}
        permitted={hs for hs in candidates if all(private_list(rows[i],p,owners,hs)[0]==
            len(private_list(rows[i],p,owners,hs)[1]) for i in rejected for p in root_rel[i])}
        assert permitted==ALLOWED[role]=={tuple(hs) for hs in tab['permissible_actual_boundary_attachment_subsets']}
        allowed[role]=permitted
        COUNTS['independent_initial_actual_attachment_subsets_enumerated']+=len(candidates)
    leaf_audit=data['original_leaf_and_bridge_cross_row_lists']
    assert leaf_audit['designated_leaf_actual_attachments']==[4]
    assert leaf_audit['designated_leaf_original_C_edge_is_bridge'] is True
    assert leaf_audit['B3_shared_leaf_slack_exclusion_does_not_apply'] is True
    leaf_rows=leaf_audit['all_original_rejected_rows_and_literal_pairs']
    assert unique([x['row_index'] for x in leaf_rows])==rejected
    leaf_colors={}
    for row in leaf_rows:
        i=row['row_index']; assert tuple(row['literal_boundary'])==rows[i]
        assert unique([tuple(x['original_root_pair']) for x in row['all_legal_root_pairs']])==root_rel[i]
        for x in row['all_legal_root_pairs']:
            p=tuple(x['original_root_pair']); degree,ls=private_list(rows[i],p,(0,1),(4,))
            assert degree==len(ls)==1
            assert x['actual_leaf_external_colors']==[*p,rows[i][4]]
            assert x['exact_leaf_list']==ls and x['original_C_degree']==1
            assert x['original_complete_degree']==4 and x['exact_degree_slack']==0
            leaf_colors[i,p]=ls[0]
            COUNTS['complete_rejected_row_pair_leaf_singletons_checked']+=1
    neighbor_cases=leaf_audit['all_possible_actual_bridge_neighbor_candidates']
    assert unique([(x['original_neighbor_owner'],tuple(x['actual_neighbor_boundary_attachments'])) for x in neighbor_cases])=={
        (role,hs) for role in OWNERS for hs in allowed[role]}
    survivor_table={r:set() for r in OWNERS}
    rebuilt_lists=[]
    for case in neighbor_cases:
        role=case['original_neighbor_owner']; owners=OWNERS[role]
        hs=tuple(case['actual_neighbor_boundary_attachments']); degree=4-len(owners)-len(hs)
        assert case['original_neighbor_C_degree']==degree
        recs=case['all_rejected_row_pair_exact_lists']
        assert unique([(x['row_index'],tuple(x['original_root_pair'])) for x in recs])==set(leaf_colors)
        rebuilt=[]
        for x in recs:
            i=x['row_index']; p=tuple(x['original_root_pair']); c=leaf_colors[i,p]
            d,ls=private_list(rows[i],p,owners,hs); after=sorted(set(ls)-{c}); slack=len(after)-(d-1)
            assert d==degree==len(ls) and slack in (0,1)
            assert tuple(x['literal_boundary'])==rows[i] and x['designated_leaf_forced_color']==c
            assert x['original_neighbor_exact_list']==ls
            assert x['C_minus_leaf_neighbor_degree']==d-1
            assert x['exact_neighbor_list_after_fixing_original_leaf']==after
            assert x['connected_remainder_slack']==slack
            rebuilt.append({'row':i,'boundary':list(rows[i]),'pair':list(p),'leaf_color':c,
                'neighbor_list':ls,'K_neighbor_list':after,'K_degree':d-1,'slack':slack})
            COUNTS['cross_row_bridge_neighbor_exact_lists_checked']+=1
        failures=[x for x in recs if x['connected_remainder_slack']]
        assert case['actual_cross_row_slack_witness']==(failures[0] if failures else None)
        assert case['survives_leaf_deletion_slack_necessity']==(not failures)
        assert case['retained_candidate_is_not_a_source_realization'] is True
        if failures: COUNTS['bridge_neighbor_actual_attachment_slack_exclusions']+=1
        else:
            survivor_table[role].add(hs)
            COUNTS['bridge_neighbor_actual_attachment_slack_survivors']+=1
        COUNTS['bridge_neighbor_actual_attachment_candidates_checked']+=1
        rebuilt_lists.append({'owner':role,'attachments':list(hs),'lists':rebuilt,'retained':not failures})
    assert survivor_table==SURVIVING
    assert leaf_audit['summary']=={'candidates':13,'pair_checks':143,'excluded':5,'retained':8}

    star=data['actual_star_rotation_and_face_crosscheck']
    assert star['rotation_insertions_checked']==108
    extended=star['original_long_face_extensions']; assert len(extended)==2
    star_edges=SKELETON|{edge(w,7) for w in (4,5,6)}
    for saved,ext in zip(saved_rots,extended,strict=True):
        assert ext['inherited_original_rotation']==saved
        assert edges(ext['original_augmented_edges'])==star_edges and ext['designated_shared_leaf']==7
        orig={r['vertex']:r['ring'] for r in saved['rotation']}
        found=[]
        for slots,ring7 in product(product(range(3),repeat=3),((4,5,6),(4,6,5))):
            rotation={v:list(r) for v,r in orig.items()}
            for w,slot in zip((4,5,6),slots,strict=True): rotation[w].insert(slot+1,7)
            rotation[7]=list(ring7)
            fs=rotation_faces(rotation,star_edges,require_sphere=False)
            COUNTS['literal_shared_star_rotation_insertions_enumerated']+=1
            if len(rotation)-len(star_edges)+len(fs)!=2: continue
            if saved['original_outer_boundary'] not in fs: continue
            if not any(set(f)=={2,3,4,6,7} for f in fs): continue
            assert {frozenset(f) for f in fs if {5,6,7}<=set(f)}=={frozenset([5,6,7])}
            assert any(set(f)=={4,5,7} for f in fs)
            found.append((rotation,fs))
        assert len(found)==1 and len(ext['selected_long_face_extensions'])==1
        item=ext['selected_long_face_extensions'][0]
        rotation,fs=found[0]
        assert {r['vertex']:r['ring'] for r in item['rotation']}==rotation
        canonical=lambda f:min(tuple(f[j:]+f[:j]) for j in range(len(f)))
        assert {canonical(f) for f in item['all_original_augmented_faces']}=={canonical(f) for f in fs}
        assert set(item['sole_face_incident_to_a_b_and_designated_shared_leaf'])=={5,6,7}
        assert item['original_outer_boundary']==saved['original_outer_boundary']
        COUNTS['literal_original_long_face_extensions_checked']+=1

    fixed=data['fixed_complete_degree_relations_and_original_K5_controls']
    records=fixed['records']; assert len(records)==40
    expected=set()
    for name,p in named.items():
        contacts=tuple(7+k for k in p); shared=set(contacts[:2])&set(contacts[2:])
        for v in shared:
            for shape in (['minimal_shared_edge'] if len(shared)==2 else [])+['short_K_cycle','long_K_cycle']:
                for swap in (False,True): expected.add((name,v,shape,swap))
    assert unique([(x['identity'],x['designated_shared_contact'],x['component_shape'],x['root_swapped']) for x in records])==expected
    rebuilt_relations={'schema':1,'literal_frame_edges':sorted(FRAME),'pattern_order':rows,'records':[]}
    cache={}
    for rec in records:
        ci=rec['control_index']; a,b=rec['original_root_order']; contacts=rec['ordered_original_contacts']
        assert normalize(contacts)==named[rec['identity']]
        assert [a,b]==([6,5] if rec['root_swapped'] else [5,6])
        assert rec['a']==a and rec['b']==b and rec['target_original_frame_id']=='W933-129'
        assert rec['target_mask']==933 and rec['original_spoke_supports']==[list(SA),list(SB)]
        assert rec['boundary_cyclic_order']==sorted(B) and edges(rec['literal_frame_edges'])==FRAME
        assert rec['target_long_face_envelope']==sorted(ENVELOPE)
        c=rec['original_components']['C']; cv=unique(c['vertices']); v=rec['designated_shared_contact']
        assert cv.isdisjoint(B|{a,b}) and set(contacts)<=cv and c['ordered_contacts']==contacts
        original=edges(rec['original_edges']); vs={z for e in original for z in e}
        assert vs==B|{a,b}|cv and rec['original_vertex_order']==sorted(vs)
        assert {e for e in original if set(e)<=B}==FRAME
        internal={e for e in original if set(e)<=cv}
        ce={e for e in original if set(e)&cv and not set(e)&{a,b}}
        assert edges(c['internal_edges'])==internal and edges(c['edges'])==ce and connected(cv,internal)
        attachments={z:sorted(w if t==z else t for t,w in original if z in (t,w) and set((t,w))&B) for z in cv}
        assert {int(z):hs for z,hs in c['actual_attachments'].items()}==attachments
        support=sorted({h for hs in attachments.values() for h in hs})
        assert c['actual_support']==support and set(support)<=ENVELOPE
        owner_edges={edge(a,z) for z in contacts[:2]}|{edge(b,z) for z in contacts[2:]}
        assert edges(c['original_root_contact_edges'])==owner_edges
        assert c['owners_by_ordered_role']==[a,a,b,b]
        assert {e for e in original if set(e)&cv and set(e)&{a,b}}==owner_edges
        spokes={edge(a,h) for h in SA}|{edge(b,h) for h in SB}
        assert original==FRAME|ce|owner_edges|spokes|{edge(a,b)}
        degrees={z:sum(z in e for e in original) for z in vs}
        assert degrees=={int(z):d for z,d in rec['original_complete_degrees'].items()}
        assert all(degrees[z]==(5 if z in (a,b) else 4) for z in vs-B)
        c_degrees={z:sum(z in e for e in internal) for z in cv}
        assert c_degrees=={int(z):d for z,d in c['original_C_degrees'].items()}
        shared=set(contacts[:2])&set(contacts[2:])
        assert c['shared_contacts']==sorted(shared) and v in shared
        assert c['designated_shared_contact']==v and c['shared_contact_actual_attachment']==[4]
        assert attachments[v]==[4] and c_degrees[v]==1
        bridge=next(e for e in internal if v in e); t=next(z for z in bridge if z!=v)
        assert tuple(c['original_shared_leaf_bridge'])==bridge and not connected(cv,internal-{bridge})
        COUNTS['literal_original_shared_bridge_deletion_checks']+=1
        k=cv-{v}; ki={e for e in internal if set(e)<=k}
        assert k and connected(k,ki) and unique(c['K_vertices'])==k
        for p in c['original_K_connectivity_paths_from_bridge_neighbor']:
            validate_path(p,k,ki,start=t)
        assert {p[-1] for p in c['original_K_connectivity_paths_from_bridge_neighbor']}==k
        cycle=c['original_K_cycle']
        if rec['component_shape']=='minimal_shared_edge':
            assert len(cv)==2 and not cycle and ki==set()
            COUNTS['minimal_two_shared_original_edge_controls']+=1
        else:
            assert len(cycle)>=3 and unique(cycle)==k
            assert all(edge(z,w) in ki for z,w in zip(cycle,cycle[1:]+cycle[:1]))
        for sub in c['construction_subdivisions']:
            assert edge(*sub['removed_template_edge']) not in internal
            validate_path(sub['original_long_path'],k,ki,start=sub['removed_template_edge'][0],finish=sub['removed_template_edge'][1])
            assert sub['short_long_relation_equivalence_claimed'] is False
        minor=rec['original_K5_minor']; bags=minor['original_branch_sets']
        assert set(bags)=={'a','b','v','B','K'}
        assert bags=={'a':[a],'b':[b],'v':[v],'B':sorted(B),'K':sorted(k)}
        assert all(bag and connected(bag,original) for bag in bags.values())
        flat=[z for bag in bags.values() for z in bag]; assert len(unique(flat))==len(flat)
        assert set(flat)==vs
        bagpaths=minor['original_branch_set_connectivity_paths']; assert set(bagpaths)==set(bags)
        for name,paths in bagpaths.items():
            assert len(paths)==len(bags[name]) and {p[-1] for p in paths}==set(bags[name])
            for p in paths: validate_path(p,bags[name],original,start=min(bags[name]))
        witnesses=minor['original_K5_cross_bag_witnesses']
        assert unique([frozenset(x['bags']) for x in witnesses])=={frozenset(p) for p in combinations(bags,2)}
        for x in witnesses:
            left,right=x['bags']; z,w=x['edge']
            assert edge(z,w) in original
            assert (z in bags[left] and w in bags[right]) or (w in bags[left] and z in bags[right])
            COUNTS['all_ten_original_K5_interbag_edges_checked']+=1
        ax=next(z for z in contacts[:2] if z!=v); by=next(z for z in contacts[2:] if z!=v)
        assert ax in k and by in k and minor['remaining_a_contact']==ax and minor['remaining_b_contact']==by
        fixed_cut={edge(a,ax),edge(b,by),bridge}; assert len(fixed_cut)==3
        kcut={e for e in original if len(set(e)&k)==1}
        bcut={e for e in kcut if set(e)&B}
        assert kcut==fixed_cut|bcut
        assert edges(minor['original_K_external_edges'])==kcut
        assert edges(minor['three_fixed_original_external_edges'])==fixed_cut
        assert edges(minor['original_K_boundary_attachment_edges'])==bcut
        n_b=len(bcut); assert 4*len(k)==2*len(ki)+3+n_b and n_b>0 and n_b%2==1
        parity=minor['parity']
        assert parity=={'K_size':len(k),'original_K_internal_edge_count':len(ki),
            'complete_K_degree_sum':4*len(k),'fixed_external_edge_count':3,
            'original_K_boundary_attachment_count':n_b,'identity_holds':True,'boundary_attachment_count_is_odd':True}
        assert minor['bridge_neighbor']==t and tuple(minor['original_shared_leaf_bridge'])==bridge
        assert minor['original_B_connectivity_path']==[4,3,2,1,0]
        validate_path(minor['original_B_connectivity_path'],B,FRAME,start=4,finish=0)
        namedpaths=minor['actual_K_paths_from_shared_bridge_neighbor']
        validate_path(namedpaths['to_remaining_a_contact'],k,ki,start=t,finish=ax)
        validate_path(namedpaths['to_remaining_b_contact'],k,ki,start=t,finish=by)
        endpoint=namedpaths['to_selected_K_boundary_attachment_endpoint'][-1]
        assert any(endpoint in e for e in bcut)
        validate_path(namedpaths['to_selected_K_boundary_attachment_endpoint'],k,ki,start=t)
        COUNTS['complete_degree_original_graphs_checked']+=1
        COUNTS['original_K5_minors_checked']+=1
        rebuilt_rec={'control_index':ci,'identity':rec['identity'],'designated_shared_contact':v,
            'root_order':[a,b],'contacts':contacts,'original_edges':sorted(original),
            'original_C_edges':sorted(internal),'actual_attachments':attachments,
            'original_K5_minor':minor,'rows':[]}
        assert unique([r['row_index'] for r in rec['rows']])==set(range(10))
        for row in rec['rows']:
            i=row['row_index']; beta=tuple(row['literal_boundary']); assert beta==rows[i]
            corder=sorted(B|cv); assert row['original_C_vertex_order']==corder
            stored=stored_relation(row['complete_original_R_C'],corder,FRAME|ce,beta,contacts,'stored_complete_R_C_witnesses_checked')
            rcw=solve_witnesses(B|cv,FRAME|ce,beta,contacts); rc=set(rcw)
            assert stored==rc
            COUNTS['independent_complete_R_C_relations']+=1
            rebuilt_row={'row_index':i,'literal_boundary':beta,'C_vertex_order':corder,
                'complete_R_C':relation_records(rcw),'variants':[]}
            variants=row['variants']; byname={x['name']:x for x in variants}
            assert unique(byname)=={'G','G-a0','G-a4','G-b1','G-b2','G-C'}
            variant_data={}
            for variant in variants:
                name=variant['name']; omitted=variant['omitted_original_edge']
                oe=None if omitted is None else edge(*omitted); omit_c=variant['original_C_omitted']
                assert omit_c==(name=='G-C')
                expected_omission=None
                if name not in ('G','G-C'):
                    role,h=name[2],int(name[3:]); expected_omission=edge(a if role=='a' else b,h)
                assert oe==expected_omission
                actual=original-({oe} if oe else set())
                if omit_c: actual={e for e in actual if not set(e)&cv}
                active=B|{a,b}|(set() if omit_c else cv); ports=[a,b]+([] if omit_c else contacts)
                order=sorted(active)
                assert edges(variant['actual_edges'])==actual
                assert variant['original_vertex_order']==order and variant['original_port_order']==ports
                assert variant['named_role_order']==['a','b']+([] if omit_c else ['x0','x1','y0','y1'])
                directw=solve_witnesses(active,actual,beta,ports); direct=set(directw)
                observed=stored_relation(variant['complete_joint'],order,actual,beta,ports,'stored_complete_joint_witnesses_checked')
                assert observed==direct
                joined={(A,D,*ct) for A,D in product(range(4),repeat=2)
                    if A!=D and not any(A==beta[h] for h in SA if edge(a,h)!=oe)
                    and not any(D==beta[h] for h in SB if edge(b,h)!=oe)
                    for ct in ([()] if omit_c else rc) if omit_c or (A not in ct[:2] and D not in ct[2:])}
                assert joined==direct
                COUNTS['independent_complete_whole_graph_joints']+=1
                cache[ci,i,name]=direct
                variant_data[name]=(active,actual,ports,direct)
                fibres=variant['pinned_a_b_fibres']
                assert unique([(f['a_color'],f['b_color']) for f in fibres])==set(product(range(4),repeat=2))
                rebuilt_fibres=[]
                for f in fibres:
                    A,D=f['a_color'],f['b_color']
                    pinned=solve(active,actual,beta,ports,{a:A,b:D})
                    pf={t[2:] for t in pinned}
                    assert pf=={t[2:] for t in direct if t[:2]==(A,D)}
                    assert unique([tuple(t) for t in f['complete_C_role_fibre']])==pf
                    items=f['complete_full_original_pinned_joint']
                    assert unique([tuple(z['tuple']) for z in items])==pinned
                    for z in items:
                        witness(order,z['coloring'],actual,beta,ports,z['tuple'])
                        assert z['coloring']==next(w['coloring'] for w in variant['complete_joint'] if w['tuple']==z['tuple'])
                        COUNTS['stored_complete_fibre_witnesses_checked']+=1
                    COUNTS['independent_pinned_root_pair_fibres']+=1
                    COUNTS['independent_empty_pinned_root_pair_fibres']+=not pinned
                    rebuilt_fibres.append({'a_color':A,'b_color':D,'empty':not pinned,
                        'complete_C_role_fibre':sorted(pf),'complete_joint':sorted(pinned)})
                rebuilt_row['variants'].append({'name':name,'actual_edges':sorted(actual),
                    'vertex_order':order,'port_order':ports,'complete_joint':relation_records(directw),
                    'pinned_a_b_fibres':rebuilt_fibres})
                if oe:
                    root=next(z for z in oe if z in (a,b)); h=next(z for z in oe if z in B)
                    assert {t for t in direct if t[(a,b).index(root)]!=beta[h]}=={
                        tuple(x['tuple']) for x in byname['G']['complete_joint']}
                    COUNTS['literal_original_spoke_restorations_checked']+=1
            color_controls=row['global_S4_color_controls']
            assert unique([tuple(x['global_color_permutation']) for x in color_controls])==set(permutations(range(4)))
            for cp_rec in color_controls:
                cp=cp_rec['global_color_permutation']; moved=tuple(cp[x] for x in beta)
                assert tuple(cp_rec['transported_literal_boundary'])==moved
                rc_moved=solve(B|cv,FRAME|ce,moved,contacts)
                assert rc_moved=={tuple(cp[x] for x in t) for t in rc}
                assert cp_rec['independently_recomputed_complete_C_relation_size']==len(rc_moved)
                COUNTS['independent_global_S4_complete_C_relations']+=1
                for variant in variants:
                    active,actual,ports,direct=variant_data[variant['name']]
                    assert solve(active,actual,moved,ports)=={tuple(cp[x] for x in t) for t in direct}
                    COUNTS['independent_global_S4_complete_whole_graph_joints']+=1
                    for z in variant['complete_joint']:
                        witness(sorted(active),[cp[x] for x in z['coloring']],actual,moved,ports,[cp[x] for x in z['tuple']])
                        COUNTS['individual_global_S4_original_joint_witnesses_checked']+=1
            rebuilt_rec['rows'].append(rebuilt_row)
        rebuilt_relations['records'].append(rebuilt_rec)
    for left,right in zip(records[::2],records[1::2],strict=True):
        rename=lambda v:11-v if v in (5,6) else v
        assert left['identity']==right['identity'] and left['designated_shared_contact']==right['designated_shared_contact']
        assert left['component_shape']==right['component_shape']
        assert {edge(rename(z),rename(w)) for z,w in edges(left['original_edges'])}==edges(right['original_edges'])
        for lr,rr in zip(left['rows'],right['rows'],strict=True):
            assert lr['complete_original_R_C']==rr['complete_original_R_C']
            for lv,rv in zip(lr['variants'],rr['variants'],strict=True):
                assert {edge(rename(z),rename(w)) for z,w in edges(lv['actual_edges'])}==edges(rv['actual_edges'])
                assert [rename(z) for z in lv['original_port_order']]==rv['original_port_order']
                assert cache[left['control_index'],lr['row_index'],lv['name']]==cache[right['control_index'],rr['row_index'],rv['name']]
                for lf,rf in zip(lv['pinned_a_b_fibres'],rv['pinned_a_b_fibres'],strict=True):
                    assert (lf['a_color'],lf['b_color'],lf['complete_C_role_fibre'])==(rf['a_color'],rf['b_color'],rf['complete_C_role_fibre'])
                COUNTS['literal_root_swap_complete_relations_and_fibres_checked']+=1
    advertised=fixed['summary']
    checks={'complete_degree_original_graphs':'complete_degree_original_graphs_checked',
        'original_K5_minors':'original_K5_minors_checked','original_K5_cross_bag_edges':'all_ten_original_K5_interbag_edges_checked',
        'minimal_two_shared_original_edge_controls':'minimal_two_shared_original_edge_controls',
        'independent_whole_graph_joins':'independent_complete_whole_graph_joints',
        'independent_pinned_a_b_fibres':'independent_pinned_root_pair_fibres',
        'saved_empty_pinned_a_b_fibres':'independent_empty_pinned_root_pair_fibres',
        'saved_complete_R_C_tuples':'stored_complete_R_C_witnesses_checked',
        'saved_complete_joint_tuples':'stored_complete_joint_witnesses_checked',
        'exact_original_spoke_restorations':'literal_original_spoke_restorations_checked',
        'root_swap_variant_checks':'literal_root_swap_complete_relations_and_fibres_checked',
        'independently_recomputed_S4_C_relations':'independent_global_S4_complete_C_relations',
        'global_S4_variant_witness_checks':'independent_global_S4_complete_whole_graph_joints'}
    for declared,observed in checks.items(): assert advertised[declared]==COUNTS[observed], (declared,advertised[declared],COUNTS[observed])
    assert advertised['fixed_controls_are_disk_source_realizations'] is False
    assert advertised['fixed_controls_are_target_Sigma_certificates'] is False
    assert advertised['short_long_relation_equivalence_claimed'] is False
    assert data['summary']['fixed_control_summary']==advertised
    for k in ('entire_W933_129_frame_excluded','full_mixed22_branch_excluded','epsilon_three_proved',
        'source_graph_catalogue_enumerated','source_realizability_claimed','new_lean_theorem','original_B_and_B3_artifacts_rewritten'):
        assert data['summary'][k] is False
    retained=target['retained_named_skeleton_indices']
    assert len(unique(retained))==20 and 129 in retained
    theorem=data['arbitrary_size_original_cut_parity_lemma']
    assert theorem['literal_degree_identity']=='4*|K| = 2*|E(K)| + 3 + |E(K,B)|'
    assert theorem['five_original_connected_bags']==['{a}','{b}','{v}','original B','complete original K']
    assert theorem['shared_remaining_contact_still_gives_two_distinct_root_edges'] is True
    assert theorem['no_minor_preservation_of_relation_fibres_or_Sigma_claimed'] is True
    scope_ledger={'schema':1,'source_sigma':933,'named_original_frame':'W933-129','literal_roots':[5,6],
        'original_spokes':[list(SA),list(SB)],'selected_long_face':[2,6,5,4,3],'actual_support_envelope':sorted(ENVELOPE),
        'conditional_actual_attachment':[4],'identity_ledger':scope,'shared_identities':6,'designated_choices':8,
        'this_conditional_attachment_branch_residuals':0,'entire_skeleton_excluded':False,'entire_long_face_excluded':False,
        'historical_B_933_retained_named_rows':retained,'historical_B_933_retained_count':20,
        'historical_B_941_retained_named_rows':next(t for t in source['targets'] if t['source_sigma']==941)['retained_named_skeleton_indices'],
        'historical_B_941_retained_count':20,'historical_B_table_rewritten':False,
        'other_actual_attachments_retained':True,'root_swap_control_registers_no_other_frame_exclusion':True,
        'arbitrary_size_scope':'Paper original degree/cut parity and connected K5 bags under B source hypotheses',
        'finite_controls_scope':'Full-degree graphs and interfaces; no disk, target Sigma, criticality or source realization',
        'external_connected_slack_scope':'Only ancillary 13-to-8 table; direct spanning-tree proof in notes',
        'new_lean_theorem':False,'lake_build_formalizes_this_paper_argument':False}
    dump(run/'relations.json',rebuilt_relations)
    dump(run/'scope_ledger.json',scope_ledger)
    dump(run/'exact_lists.json',{'leaf_singletons':[{'row':i,'pair':p,'color':c} for (i,p),c in sorted(leaf_colors.items())],
        'neighbor_cases':rebuilt_lists})
    return {'schema':1,'all_checks_passed':True,'scope':__doc__,'input_sha256':hashes,
        'summary':{'named_frame':'W933-129','long_face_envelope':sorted(ENVELOPE),
            'shared_identities':6,'designated_shared_choices':8,'leaf_singleton_checks':11,
            'neighbor_candidates':13,'neighbor_lists':143,'neighbor_slack_exclusions':5,'neighbor_slack_survivors':8,
            'complete_degree_graphs':40,'complete_R_C_relations':400,'complete_joint_relations':2400,
            'root_pair_fibres':38400,'empty_root_pair_fibres':29768,'R_C_witnesses':5336,'joint_witnesses':25416,
            'fibre_witnesses':25416,'original_K5_minors':40,'all_ten_original_K5_edges':400,
            'shared_bridge_deletion_controls':40,'original_frame_rotations':2,'shared_star_insertions':108,
            'selected_long_face_extensions':2,'producer_imports':False},
        'counts':dict(sorted(COUNTS.items())),
        'claims_not_certified_by_fixed_python':['arbitrary-size paper topology','disk or source realizability',
            'target Sigma or criticality','all mixed22','epsilon >= 3','general exits','K-infinity = K-at-most-5','new Lean theorem']}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo','--snapshot',dest='repo',type=Path,default=Path(__file__).resolve().parents[1]/'snapshot')
    parser.add_argument('--output',type=Path,default=Path(__file__).resolve().parent)
    args=parser.parse_args(); out=args.output.resolve(); out.mkdir(parents=True,exist_ok=True)
    attempts=out/'attempts'; attempts.mkdir(exist_ok=True); n=1
    while (attempts/f'{n:04d}').exists(): n+=1
    run=attempts/f'{n:04d}'; run.mkdir(); here=Path(__file__).resolve().parent
    versions={}
    for name in ('audit_b4.py','independent_core.py'):
        shutil.copy2(here/name,run/name)
        versions[name]=sha256((here/name).read_bytes()).hexdigest()
    versions['adapted_helper_provenance']='audits/2026-10-04-task-d4/b3/independent_core.py'
    provenance=here.parents[1]/'2026-10-04-task-d4/b3/independent_core.py'
    if provenance.exists(): versions['adapted_helper_provenance_sha256']=sha256(provenance.read_bytes()).hexdigest()
    dump(run/'audit_source_versions.json',versions)
    started=time.monotonic(); failure=None
    with (run/'run.log').open('w') as log, redirect_stdout(log), redirect_stderr(log):
        try: result=audit(args.repo.resolve(),run)
        except BaseException as exc:
            failure=exc; traceback.print_exc()
            result={'all_checks_passed':False,'exception_type':type(exc).__name__,'exception':str(exc),
                'traceback':traceback.format_exc(),'counts':dict(sorted(COUNTS.items()))}
        print(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2))
    dump(run/'results.json',result)
    metadata={'repo':str(args.repo.resolve()),'output':str(run),'elapsed_seconds':round(time.monotonic()-started,3),
        'all_checks_passed':result['all_checks_passed'],'source_versions':versions}
    dump(run/'execution_metadata.json',metadata)
    if failure is not None:
        print(f'FAILED; immutable attempt preserved at {run}',file=sys.stderr)
        raise failure
    for name in ('results.json','relations.json','scope_ledger.json','exact_lists.json','audit_source_versions.json'):
        shutil.copy2(run/name,out/name)
    print(json.dumps({'all_checks_passed':True,'attempt_directory':str(run),'elapsed_seconds':metadata['elapsed_seconds'],
        'summary':result['summary']},ensure_ascii=False,sort_keys=True))


if __name__=='__main__': main()
