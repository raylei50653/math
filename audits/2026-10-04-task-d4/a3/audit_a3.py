#!/usr/bin/env python3
"""Independent frozen A3 audit. Only standard library and prior D2 audit utilities.

No production module is imported. Exhaustive literal-color MRV search rebuilds
relations; a separate incidence join checks each variant; all stored witnesses,
six/five-role joints, all 16 pinned fibres and whole-C replacements are checked.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import time

import independent_core as I
import independent_a2 as A2

N = Counter()
B, FRAME, COLORS = I.BOUNDARY, I.FRAME, I.COLORS
edge, es, unique, relation, validate, fibres = I.edge, I.es, I.unique, I.relation, I.validate, I.fibres
Q = (0, 1, 2, 0, 2)


def literal_rotation(r, move=lambda v:v):
    result = []
    for p in r['rotation']:
        ring = [move(v) for v in p['ring']]
        i = ring.index(min(ring))
        result.append((move(p['vertex']), tuple(ring[i:] + ring[:i])))
    return tuple(sorted(result))


def identity(data, inherited, a1, generic, rows):
    prior = A2.identity(inherited, a1, generic, rows)
    source = {f['named_frame_id']:f for t in inherited['targets'] for f in t['complete_remaining_named_original_frames']}
    selected = data['selected_complete_original_frames']
    unique([s['named_frame_id'] for s in selected], 'A3 selected ids')
    chosen_ids = {k for k,f in source.items() if f['original_a_spokes']==f['original_b_spokes']==[0,1]}
    assert {s['named_frame_id'] for s in selected}==chosen_ids and len(chosen_ids)==4
    unique([t['source_sigma'] for t in data['targets']], 'A3 sigma identities')
    assert {t['source_sigma'] for t in data['targets']}=={933,941}
    results = []
    for t in data['targets']:
        sigma=t['source_sigma']
        original=[f for f in source.values() if f['source_sigma']==sigma]
        chosen=[f for f in original if f['named_frame_id'] in chosen_ids]
        remaining=[f for f in original if f['named_frame_id'] not in chosen_ids]
        unique(t['inherited_named_frame_ids'], 'A3 inherited ids')
        unique(t['newly_excluded_named_frame_ids'], 'A3 excluded ids')
        assert t['inherited_named_frame_ids']==[f['named_frame_id'] for f in original]
        assert t['newly_excluded_named_frame_ids']==[f['named_frame_id'] for f in chosen]
        assert t['complete_remaining_named_original_frames']==remaining
        ns=sum(len(f['remaining_named_original_U_placements']) for f in remaining)
        nr=sum(len(p['complete_singleton_unary_relation_schedules']) for f in remaining for p in f['remaining_named_original_U_placements'])
        expected=dict(remaining_named_frames=len(remaining),remaining_actual_U_support_records=ns,remaining_complete_singleton_schedules=nr)
        assert t['summary']==expected and list(expected.values())==([18,44,56] if sigma==933 else [22,70,102])
        results.append(dict(source_sigma=sigma,inherited_frames=len(original),newly_excluded_frames=len(chosen),**expected))
    for s in selected:
        f=s['inherited_complete_named_frame'];a,b=f['original_a'],f['original_b'];sigma=f['source_sigma']
        assert f==source[s['named_frame_id']]
        assert f['original_a_spokes']==f['original_b_spokes']==[0,1]
        assert s['universal_six_role_joint_equality_claimed'] is False
        assert s['whole_C_witness_replacement_preserves_all_exterior_vertices'] is True
        assert s['exact_projection']=='pi_(a,b,u) J_G(beta) = pi_(a,b,u) J_(G-ax)(beta)'
        skeleton=FRAME|{edge(a,b)}|{edge(r,h) for r in (a,b) for h in (0,1)}
        assert es(f['original_root_and_boundary_edges'])==skeleton
        assignments, rebuilt=I.disk_rotations(skeleton)
        rotations=f['exhaustive_original_skeleton_rotations']['all_disk_rotations']
        assert assignments==144 and len(rebuilt)==len(rotations)==4
        stored={literal_rotation(r):frozenset(map(tuple,r['original_disk_faces'])) for r in rotations}
        assert stored==rebuilt
        N['selected_skeletons']+=1;N['selected_rotation_assignments']+=assignments;N['selected_disk_rotations']+=len(rotations)
        ge=s['same_embedding_C_U_geometry']
        assert ge['full_source_touch_all_B_requires_actual_U_support_contains']==[2,3,4]
        rr=ge['all_four_original_rotations'];unique([r['original_rotation_index'] for r in rr], 'A3 geometry rotation indices')
        assert [r['original_rotation_index'] for r in rr]==list(range(4))
        for i,r in enumerate(rr):
            assert r['complete_original_rotation']==rotations[i]
            common=sorted([list(I.cycle([a,b,h])) for h in (0,1)])
            assert r['original_C_common_faces']==common==sorted(p for p in rotations[i]['original_disk_faces'] if a in p and b in p)
            placements=r['all_original_a_incident_U_faces']
            unique([tuple(p['original_U_face']) for p in placements], 'A3 all U faces in each rotation')
            assert [p['original_U_face'] for p in placements]==[p for p in rotations[i]['original_disk_faces'] if a in p]
            for p in placements:
                envelope=sorted(set(p['original_U_face']) & B)
                assert p['exact_boundary_envelope']==envelope
                assert p['compatible_original_C_common_faces']==common
                assert p['can_have_actual_support_234']==({2,3,4}<=set(envelope))
                if p['can_have_actual_support_234']:
                    assert p['original_U_face']==list(I.cycle([0,4,3,2,1,a]))
                    assert i in ((0,3) if a==5 else (1,2))
                N['selected_same_rotation_U_placements']+=1
        hubs=ge['original_C_hub_instances']
        assert {tuple(h['original_C_face']) for h in hubs}=={I.cycle([a,b,h]) for h in (0,1)}
        for inst in hubs:
            h,=set(inst['original_C_face']) & B
            assert inst['actual_C_support_subsets']==[[],[h]] and inst['possible_actual_C_supports']==[[h]]
            assert inst['empty_actual_support_excluded_by_degree_handshake']
            assert inst['boundary_attachment_edge_count_is_odd']=='4|C|=2|E(C)|+3+|E(C,B)|'
            assert inst['literal_hub_bags']==[[a],[b],[h]]
            adj=inst['all_original_hub_adjacencies'];assert len(adj)==3
            assert {tuple(p['hub_pair']) for p in adj}==set(combinations((a,b,h),2))
            for p in adj:assert tuple(p['original_edge'])==edge(*p['hub_pair']) in skeleton
            legal=inst['all_legal_root_pair_exact_list_instances']
            expected={(ri,ac,bc) for ri,q in enumerate(rows) for ac,bc in product(sorted(set(COLORS)-{q[0],q[1]}),repeat=2) if ac!=bc}
            unique([(p['row_index'],*p['original_a_b_colors']) for p in legal], 'A3 legal literal root pairs')
            assert {(p['row_index'],*p['original_a_b_colors']) for p in legal}==expected
            for p in legal:
                ri=p['row_index'];q=rows[ri];ac,bc=p['original_a_b_colors'];hc=q[h]
                assert p['literal_boundary']==list(q) and p['boundary_hub_color']==hc and len({ac,bc,hc})==3
                subsets=p['all_local_C_external_neighbor_subsets']
                unique([tuple(t['actual_external_neighbor_indices']) for t in subsets], 'A3 exact-list subset coverage')
                assert {tuple(t['actual_external_neighbor_indices']) for t in subsets}=={t for n in range(4) for t in combinations(range(3),n)}
                for t in subsets:
                    ns=t['actual_external_neighbor_indices'];colors=sorted(set(COLORS)-{[ac,bc,hc][j] for j in ns})
                    assert t['exact_C_list']==colors and t['internal_C_degree']==len(colors)==4-len(ns)
                    assert t['degree_preserved_by_literal_distinct_hubs']
                    N['selected_exact_degree_list_subsets']+=1
                N['selected_legal_three_hub_root_pairs']+=1
            N['selected_three_hub_instances']+=1
        audits=s['complete_actual_U_support_schedule_audits']
        assert [p['inherited_complete_original_U_placement'] for p in audits]==f['remaining_named_original_U_placements']
        for au in audits:
            p=au['inherited_complete_original_U_placement'];support=p['actual_original_U_support'];schedules=p['complete_singleton_unary_relation_schedules']
            rs,domains,constraints,computed=I.schedules(sigma,(0,1),tuple(support),rows)
            assert {tuple(x['singleton_colors']) for x in schedules}=={v for v,(e,c) in computed.items() if e and c}
            compatible={2,3,4}<=set(support)
            assert au['full_source_support_compatible']==compatible
            assert au['missing_actual_full_source_boundary_endpoints']==sorted({2,3,4}-set(support))
            paper=au['designated_row_complete_joint_paper_instances'];assert len(paper)==len(schedules)
            for si,x in enumerate(paper):
                original=schedules[si];qr,=[z for z in original['complete_singleton_unary_relations'] if z['literal_boundary']==list(Q)];d,=qr['complete_R_U'][0]
                assert d in (2,3) and x['inherited_schedule_index']==si and x['complete_R_U']==[[d]]
                assert x['designated_row_index']==rows.index(Q) and x['literal_boundary']==list(Q)
                assert x['original_a_b_u_colors']==[5-d,d,d]
                assert x['full_joint_claim']==[5-d,d,'X','Y0','Y1',d]
                assert x['C_witness_guards']==['X != a','Y0 != b','Y1 != b']
                N['paper_designated_singleton_'+str(d)+'_instances']+=1
                N['selected_inherited_singleton_schedules']+=1
                N['selected_geometry_compatible_schedules']+=compatible
            N['selected_inherited_support_records']+=1;N['selected_geometry_compatible_support_records']+=compatible
    unique([x['original_frame_id'] for x in data['root_swap_checks']], 'A3 selected root swaps')
    for x in data['root_swap_checks']:
        left,right=(source[x[k]] for k in ('original_frame_id','swapped_frame_id'))
        move=lambda v:11-v if v in (5,6) else v
        assert es([[move(v),move(w)] for v,w in left['original_root_and_boundary_edges']])==es(right['original_root_and_boundary_edges'])
        lr=left['exhaustive_original_skeleton_rotations']['all_disk_rotations'];rr=right['exhaustive_original_skeleton_rotations']['all_disk_rotations']
        positions={literal_rotation(r):i for i,r in enumerate(rr)};mapping=[positions[literal_rotation(r,move)] for r in lr]
        assert mapping==x['original_to_swapped_rotation_indices']==[1,0,3,2]
        pairs=x['complete_original_U_placement_bijection'];assert len(pairs)==len(left['remaining_named_original_U_placements'])
        for l,p in zip(left['remaining_named_original_U_placements'],pairs,strict=True):
            moved=list(I.cycle([move(v) for v in l['original_U_face']]))
            r,=[z for z in right['remaining_named_original_U_placements'] if z['original_U_face']==moved and z['actual_original_U_support']==l['actual_original_U_support']]
            assert p['original_U_face']==l['original_U_face'] and p['swapped_U_face']==moved and p['actual_U_support']==l['actual_original_U_support']
            assert r['complete_singleton_unary_relation_schedules']==l['complete_singleton_unary_relation_schedules']
            assert r['supporting_original_rotation_indices']==sorted(mapping[i] for i in l['supporting_original_rotation_indices'])
            assert r['compatible_original_C_common_faces']==sorted([dict(face=list(I.cycle([move(v) for v in z['face']])),supporting_rotation_indices=sorted(mapping[i] for i in z['supporting_rotation_indices'])) for z in l['compatible_original_C_common_faces']],key=lambda z:z['face'])
            N['selected_root_swap_full_placements']+=1
        N['selected_root_swap_pairs']+=1
    return dict(prior_A_A2_identity_revalidated=prior,ledger=results)


def graphs(data, rows):
    controls=data['fixed_full_degree_same_graph_controls'];records=controls['records'];rebuilt=[]
    unique([r['control_index'] for r in records], 'A3 control ids');assert [r['control_index'] for r in records]==list(range(36))
    designated={x['control_index']:x for x in controls['designated_row_fixed_exterior_audits']};assert len(designated)==36
    graph_masks=Counter()
    for r in records:
        a,b=r['original_a'],r['original_b'];cp,up=r['C'],r['unary_U'];cv,uv=set(cp['vertices']),set(up['vertices']);x,y0,y1=cp['ordered_contacts'];u,=up['ordered_contacts'];ports=[a,b,x,y0,y1,u]
        assert cp['owners']==[a,b,b] and up['owner']==a and y0!=y1
        assert r['complete_port_order']==ports and cp['incidence']==[1,2]
        alias='y0' if x==y0 else 'y1' if x==y1 else None;assert cp['x_y_alias']==alias
        N['distinct_x_y0_y1_graphs' if alias is None else 'x_equals_'+alias+'_graphs']+=1
        assert not cv&uv and not (cv|uv)&(B|{a,b})
        original=es(r['original_edges']);parts={}
        for name,p in (('C',cp),('U',up)):
            vs=set(p['vertices']);inner=es(p['original_internal_edges']);assert all(set(e)<=vs for e in inner) and I.connected(vs,inner)
            attachments={edge(int(v),h) for v,hs in p['actual_attachments'].items() for h in hs}
            assert set(map(int,p['actual_attachments']))==vs and all(h in B for hs in p['actual_attachments'].values() for h in hs)
            assert p['actual_support']==sorted({h for hs in p['actual_attachments'].values() for h in hs})
            parts[name]=inner|attachments
            for w in p['original_owner_to_attachment_paths']:
                path=w['original_path'];assert path[0]==w['owner'] and path[-1]==w['boundary_endpoint']
                assert w['owner'] in ([a,b] if name=='C' else [a]) and set(path[1:-1])<=vs and len(path)==len(set(path))
                assert all(edge(v,z) in original for v,z in zip(path,path[1:]));N['actual_attachment_path_witnesses']+=1
        assert len(cp['actual_support'])==1 and cp['actual_support'][0] in (0,1)
        crosscut=up['original_a_to_2_crosscut'];assert crosscut[0]==a and crosscut[-1]==2 and set(crosscut[1:-1])<=uv and len(crosscut)==len(set(crosscut))
        assert all(edge(v,w) in original for v,w in zip(crosscut,crosscut[1:]))
        assert r['original_root_spokes']==dict(a=[0,1],b=[0,1])
        graph=FRAME|parts['C']|parts['U']|{edge(a,b),edge(a,x),edge(a,u),edge(b,y0),edge(b,y1)}|{edge(z,h) for z in (a,b) for h in (0,1)}
        assert graph==original and r['vertex_order']==sorted(B|{a,b}|cv|uv)
        assert all(sum(v in e for e in original)==(5 if v in (a,b) else 4) for v in {a,b}|cv|uv)
        assert {(z,v) for z in (a,b) for v in cv if edge(z,v) in original}=={(a,x),(b,y0),(b,y1)}
        masks=Counter();outrows=[]
        assert len(r['rows'])==len(rows)==10
        for ri,row in enumerate(r['rows']):
            beta=rows[ri];assert row['row_index']==ri and row['literal_boundary']==list(beta)
            cr=relation(cp['vertex_order'],FRAME|parts['C'],beta,[x,y0,y1],row['C_complete_tuples'],'A3_C_ternary')
            ur=relation(up['vertex_order'],FRAME|parts['U'],beta,[u],row['U_complete_tuples'],'A3_U_unary')
            variants=row['variants'];unique([v['id'] for v in variants], 'A3 graph variants')
            assert {v['id'] for v in variants}=={'original','a_x','a_u','a_spoke_0','a_spoke_1','b_spoke_0','b_spoke_1','whole_U'}
            joints={};outvars=[]
            for v in variants:
                whole=v['id']=='whole_U'
                actual={e for e in original if not set(e)&uv} if whole else original-({edge(*v['omitted_original_edge'])} if v['omitted_original_edge'] is not None else set())
                assert es(v['actual_edges'])==actual
                assert v['vertex_order']==sorted((B|{a,b}|cv) if whole else (B|{a,b}|cv|uv))
                p=ports[:5] if whole else ports;assert v['complete_port_order']==p
                field='complete_five_role_joint' if whole else 'complete_joint_tuples';tail='complete_x_y0_y1_fiber' if whole else 'complete_x_y0_y1_u_fiber'
                j=relation(v['vertex_order'],actual,beta,p,v[field],'A3_five_role' if whole else 'A3_six_role');joints[v['id']]=j
                fibres(v['pinned_a_b_fibers'],j,tail)
                N['independent_pinned_a_b_fibers']+=16;N['empty_pinned_fibers']+=sum(not [t for t in j if t[:2]==(ac,bc)] for ac,bc in product(COLORS,repeat=2))
                N['complete_five_role_tuple_witnesses' if whole else 'complete_joint_tuple_witnesses']+=len(j)
                masks[v['id']]+=(1<<ri) if j else 0
                if whole:
                    assert v['removed_original_vertices']==sorted(uv)
                    joined={(ac,bc,xc,c0,c1) for xc,c0,c1 in cr for ac,bc in product(COLORS,repeat=2) if ac!=bc and ac!=xc and bc not in (c0,c1) and all(ac!=beta[h] for h in (0,1)) and all(bc!=beta[h] for h in (0,1))}
                else:
                    assert v['retained_a_spokes']==[h for h in (0,1) if edge(a,h) in actual] and v['retained_b_spokes']==[h for h in (0,1) if edge(b,h) in actual]
                    joined={(ac,bc,xc,c0,c1,uc) for xc,c0,c1 in cr for uc, in ur for ac,bc in product(COLORS,repeat=2) if ac!=bc and all(ac!=beta[h] for h in B if edge(a,h) in actual) and all(bc!=beta[h] for h in B if edge(b,h) in actual) and (edge(a,x) not in actual or ac!=xc) and (edge(a,u) not in actual or ac!=uc) and bc not in (c0,c1)}
                assert joined==j;N['independent_whole_graph_joins']+=1
                info=v.get('exact_reattachment',{})
                if 'removed_joint_tuples' in info:
                    position=0 if v['id'].startswith('a_') else 1;h=v['omitted_original_edge'][0]
                    assert info['root_tuple_position']==position and info['boundary_endpoint']==h and info['literal_forbidden_color']==beta[h]
                    removed=I.tuples(info['removed_joint_tuples'],'A3 removed spoke tuples');assert removed=={t for t in j if t[position]==beta[h]}
                    for w in info['removed_joint_tuples']:validate(v['vertex_order'],w['coloring'],actual,beta,p,w['tuple'])
                outvars.append(dict(id=v['id'],complete_tuples=sorted(j),all_literal_root_pair_fibres=[dict(a_color=ac,b_color=bc,complete_fibre=sorted(t[2:] for t in j if t[:2]==(ac,bc))) for ac,bc in product(COLORS,repeat=2)]))
            restored=joints['original']
            for v in variants:
                if v['id'] in ('original','whole_U'):continue
                omitted=v['omitted_original_edge'];filtered=set()
                for t in joints[v['id']]:
                    colors=dict(enumerate(beta))|dict(zip(ports,t,strict=True))
                    if colors[omitted[0]]!=colors[omitted[1]]:filtered.add(t)
                assert filtered==restored
                N['exact_spoke_reattachments' if 'spoke' in v['id'] else 'exact_ax_reattachments' if v['id']=='a_x' else 'exact_au_products_and_reattachments']+=1
            ax,=[v for v in variants if v['id']=='a_x'];info=ax['exact_reattachment'];projection=lambda j:{(t[0],t[1],t[5]) for t in j}
            assert projection(restored)==projection(joints['a_x'])==set(map(tuple,info['complete_original_a_b_u_projection']))==set(map(tuple,info['complete_ax_omitted_a_b_u_projection']))
            assert info['complete_a_b_u_projection_equal'] and info['complete_six_role_equality_claimed'] is False
            N['exact_ax_exterior_projection_equalities']+=1
            replacements=info['whole_C_witness_replacements_preserving_exterior'];unique([tuple(w['omitted_six_role_tuple']) for w in replacements], 'A3 whole C replacement inputs')
            assert {tuple(w['omitted_six_role_tuple']) for w in replacements}==joints['a_x']
            for w in replacements:
                t,rt=tuple(w['omitted_six_role_tuple']),tuple(w['restored_six_role_tuple']);assert t in joints['a_x'] and rt in restored and (t[0],t[1],t[5])==(rt[0],rt[1],rt[5])
                om=validate(r['vertex_order'],w['omitted_full_coloring'],original-{edge(a,x)},beta,ports,t)
                rm=validate(r['vertex_order'],w['restored_full_coloring'],original,beta,ports,rt)
                assert w['original_C_vertices_only_recolored']==cp['vertices'] and all(om[v]==rm[v] for v in set(r['vertex_order'])-cv)
                N['ax_projection_witness_replacements']+=1
            extensions=info['complete_C_legal_root_pair_extensions'];allowed=set(COLORS)-{beta[0],beta[1]}
            unique([(z['a_color'],z['b_color']) for z in extensions], 'A3 legal C root pair fibres')
            assert {(z['a_color'],z['b_color']) for z in extensions}=={(ac,bc) for ac,bc in product(allowed,repeat=2) if ac!=bc}
            for z in extensions:
                ac,bc=z['a_color'],z['b_color'];ts=I.tuples(z['complete_C_fixed_root_fiber'],'A3 whole C fixed roots')
                assert ts=={t for t in cr if t[0]!=ac and bc not in t[1:]} and ts
                assert z['three_distinct_original_hub_colors']==[ac,bc,beta[cp['actual_support'][0]]] and len(set(z['three_distinct_original_hub_colors']))==3
                for w in z['complete_C_fixed_root_fiber']:validate(cp['vertex_order'],w['coloring'],FRAME|parts['C'],beta,[x,y0,y1],w['tuple'])
                N['complete_C_legal_root_pair_extensions']+=1
            assert joints['a_u']=={(*t,uc) for t in joints['whole_U'] for uc, in ur}
            ad,ud={t[0] for t in joints['whole_U']},{t[0] for t in ur}
            assert ad and ud and (not restored)==(ad==ud and len(ad)==1);N['nonempty_domain_singleton_identity_checks']+=1
            whole,=[v for v in variants if v['id']=='whole_U'];assert whole['all_literal_a_colors_after_complete_join']==sorted(ad) and whole['complete_original_U_contact_colors']==sorted(ud)
            designated_row=row['designated_rejected_row_audit']
            if beta!=Q:assert designated_row is None
            else:
                assert ud=={2};N['designated_row_complete_unary_singletons']+=1
                for z in (designated_row,designated[r['control_index']]):
                    assert z.get('control_index',r['control_index'])==r['control_index']
                    assert z['fixed_original_exterior']==dict(a=3,b=2,u=2) and z['has_complete_C_extension']
                    relation(up['vertex_order'],FRAME|parts['U'],beta,[u],z['complete_original_R_U'],'A3_designated_U_duplicate')
                    for field,expected,order,edges,p in (
                        ('complete_original_C_fixed_root_fiber',{t for t in cr if t[0]!=3 and 2 not in t[1:]},cp['vertex_order'],FRAME|parts['C'],[x,y0,y1]),
                        ('complete_original_joint_at_fixed_exterior',{t for t in restored if (t[0],t[1],t[5])==(3,2,2)},r['vertex_order'],original,ports)):
                        assert I.tuples(z[field],field)==expected and expected
                        for w in z[field]:validate(order,w['coloring'],edges,beta,p,w['tuple'])
                N['designated_row_fixed_exterior_C_extensions']+=1
            outrows.append(dict(row_index=ri,literal_boundary=beta,complete_C_ternary=sorted(cr),complete_U_unary=sorted(ur),variants=outvars))
        assert len(r['independently_computed_control_boundary_images'])==8
        for z in r['independently_computed_control_boundary_images']:assert z['full_boundary_image']==masks[z['variant_id']]
        graph_masks[masks['original']]+=1;N['fixed_full_degree_graphs']+=1
        rebuilt.append(dict(control_index=r['control_index'],original_edges=r['original_edges'],complete_port_order=ports,rows=outrows))
    for swap in controls['root_swap_controls']:
        l,r=(records[swap[k]] for k in ('original_control_index','exchanged_control_index'));move=lambda v:11-v if v in (5,6) else v
        assert es([[move(v),move(w)] for v,w in l['original_edges']])==es(r['original_edges'])
        for lr,rr in zip(l['rows'],r['rows'],strict=True):
            assert lr['C_complete_tuples']==rr['C_complete_tuples'] and lr['U_complete_tuples']==rr['U_complete_tuples']
            for lv,rv in zip(lr['variants'],rr['variants'],strict=True):
                field='complete_five_role_joint' if lv['id']=='whole_U' else 'complete_joint_tuples'
                assert lv['pinned_a_b_fibers']==rv['pinned_a_b_fibers'] and [move(v) for v in lv['complete_port_order']]==rv['complete_port_order']
                for lw,rw in zip(lv[field],rv[field],strict=True):
                    assert lw['tuple']==rw['tuple'];f=dict(zip(lv['vertex_order'],lw['coloring'],strict=True))
                    assert [f[move(v)] for v in rv['vertex_order']]==rw['coloring'];N['root_swap_full_witnesses']+=1
        N['root_swap_graph_checks']+=1
    negatives={}
    for name in ('ternary_marginal_collision','six_role_joint_inequivalence'):
        z=controls[name];r=records[z['control_index']];row=r['rows'][z['row_index']];beta=rows[z['row_index']]
        if name=='ternary_marginal_collision':
            cp=r['C'];assert z['complete_C_tuples']==row['C_complete_tuples'];edges=FRAME|es(cp['original_internal_edges'])|{edge(int(v),h) for v,hs in cp['actual_attachments'].items() for h in hs}
            cr=relation(cp['vertex_order'],edges,beta,cp['ordered_contacts'],z['complete_C_tuples'],'A3_negative_C');ac,bc=z['literal_a_b_colors']
            assert not {t for t in cr if t[0]!=ac and bc not in t[1:]}
            fake={t for t in product(*[{t[i] for t in cr} for i in range(3)]) if t[0]!=ac and bc not in t[1:]};assert fake
            negatives[name]=dict(rebuilt_false_marginal_tuples=sorted(fake),rebuilt_complete_guarded_fibre=[],saved_full_counterexample=z)
        else:
            original,=[v for v in row['variants'] if v['id']=='original'];ax,=[v for v in row['variants'] if v['id']=='a_x']
            assert z['original_complete_joint']==original['complete_joint_tuples'] and z['ax_omitted_complete_joint']==ax['complete_joint_tuples']
            j=relation(r['vertex_order'],es(original['actual_edges']),beta,r['complete_port_order'],z['original_complete_joint'],'A3_negative_original')
            k=relation(r['vertex_order'],es(ax['actual_edges']),beta,r['complete_port_order'],z['ax_omitted_complete_joint'],'A3_negative_ax');t=tuple(z['omission_only_tuple'])
            assert t in k-j and t[0]==t[2] and {(x[0],x[1],x[5]) for x in j}=={(x[0],x[1],x[5]) for x in k}
            validate(r['vertex_order'],z['omission_only_full_coloring'],es(ax['actual_edges']),beta,r['complete_port_order'],t)
            replacement,=[w for w in ax['exact_reattachment']['whole_C_witness_replacements_preserving_exterior'] if tuple(w['omitted_six_role_tuple'])==t]
            negatives[name]=dict(rebuilt_original_tuple_count=len(j),rebuilt_omission_tuple_count=len(k),saved_full_counterexample=z,saved_whole_C_replacement=replacement)
        negatives[name].update(original_edges=r['original_edges'],literal_boundary=beta,vertex_order=r['vertex_order'],complete_port_order=r['complete_port_order'])
    assert dict(graph_masks)=={1023:36}
    for key,value in N.items():
        if key in controls['summary']:assert controls['summary'][key]==value, ('summary count mismatch',key,value,controls['summary'][key])
    assert controls['summary']['original_control_boundary_image_counts']==[dict(full_boundary_image=1023,graphs=36)]
    return dict(control_Sigma_counts=dict(graph_masks),negative_controls=negatives),rebuilt


def coloring_fields(x):
    if isinstance(x,list):return sum(map(coloring_fields,x))
    if isinstance(x,dict):return sum(int(k in ('coloring','omission_only_full_coloring','omitted_full_coloring','restored_full_coloring'))+coloring_fields(v) for k,v in x.items())
    return 0


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[1]/'snapshot')
    p.add_argument('--output',type=Path,required=True,help='Fresh attempt directory inside this audit folder')
    args=p.parse_args();base=Path(__file__).resolve().parent;out=args.output.resolve();assert out.is_relative_to(base.resolve()) and not out.exists(), 'Use a fresh audit-local output directory for every attempt'
    out.mkdir(parents=True);started=time.monotonic()
    names=('c5_excess_two_mixed_core_four_spoke_mixed12_01_01','c5_excess_two_mixed_core_four_spoke_mixed12_01_12','c5_excess_two_mixed_core_four_spoke_mixed12','c5_excess_two_mixed_core_single_spoke')
    paths=[args.repo/'artifacts'/n/'observations.json' for n in names]
    before={str(p.relative_to(args.repo)):sha256(p.read_bytes()).hexdigest() for p in paths}
    data,inherited,a1,generic=[json.loads(p.read_text()) for p in paths]
    for name,expected in data['input_sha256'].items():
        assert sha256((args.repo/name).read_bytes()).hexdigest()==expected, ('frozen bound input hash drift',name)
        N['bound_input_hashes_verified']+=1
    rows=tuple(sorted({I.normalized(q)[0] for q in product(COLORS,repeat=5) if all(q[v]!=q[w] for v,w in FRAME)}))
    assert tuple(map(tuple,data['pattern_order']))==rows
    ledger=identity(data,inherited,a1,generic,rows)
    before_graph=I.COUNTS['stored_colorings_validated']
    audited,rebuilt=graphs(data,rows)
    validated=I.COUNTS['stored_colorings_validated']-before_graph
    assert validated==coloring_fields(data), ('serialized coloring field accounting',validated,coloring_fields(data))
    N['all_A3_serialized_coloring_fields_validated']=validated
    after={str(p.relative_to(args.repo)):sha256(p.read_bytes()).hexdigest() for p in paths};assert before==after
    payload=json.dumps(rebuilt,ensure_ascii=False,sort_keys=True,indent=1)+'\n'
    (out/'rebuilt_complete_relations.json').write_text(payload)
    (out/'counterexamples.json').write_text(json.dumps(audited['negative_controls'],ensure_ascii=False,sort_keys=True,indent=2)+'\n')
    result=dict(status='PASS',all_checks_passed=True,frozen_input_root=str(args.repo.resolve()),input_sha256=before,source_artifact_bytes_preserved=True,identity=ledger,graphs={k:v for k,v in audited.items() if k!='negative_controls'},counts=dict(N),independent_solver_counts=dict(I.COUNTS),rebuilt_complete_relations_sha256=sha256(payload.encode()).hexdigest(),audit_source_sha256={p.name:sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),base/'independent_core.py',base/'independent_a2.py')},elapsed_seconds=round(time.monotonic()-started,3),paper_review=dict(accepted_conditional_scope='Original shared spokes 01/01 with whole root swap only; under the documented fixed-source hypotheses original ax is noncritical.',external_primary_source='https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf',external_result='Lemma 7 and Theorem 10: connected degree assignment slack and Gallai/blockwise-uniform classification.',checked_steps=['Four original rotations force C into hab and complete-source support fixes U to its same-rotation long face.','Parity of 4|C|=2|E(C)|+3+|E(C,B)| excludes empty C support.','Literal hubs a,b,h form a triangle and have distinct exterior colors, including shared x=y0/y1.','Expanded K4 argument uses bridge deletion slack on each connected side and four disjoint paths to connected exterior.','Unbounded three-hub leaf odd-cycle and leaf-bridge proof yields K5 minor under rejection.','C-only replacement preserves the complete exterior coloring; only (a,b,u) projection equality is claimed.']),limits=['Finite graph controls are all Sigma1023; no disk, criticality or source-Sigma933/941 realization is established.','Arbitrary-size topology/Gallai/K4/K5 proof remains a paper argument with externally verified list theorem; audit solver certifies fixed controls only.','All 36 finite designated-row controls have singleton2. Singleton3 is covered by retained source schedules and the paper instance, not a separate finite singleton3 graph.','18/22 named frames,44/70 support records,56/102 schedules remain. No mixed12-wide exclusion, epsilon>=3, general exit, new Lean theorem or K-infinity=K-at-most5 follows.'])
    (out/'results.json').write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',ledger=ledger['ledger'],counts=dict(N),elapsed_seconds=result['elapsed_seconds']),sort_keys=True),flush=True)


if __name__=='__main__':main()
