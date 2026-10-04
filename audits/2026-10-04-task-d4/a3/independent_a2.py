#!/usr/bin/env python3
"""Independent A2 successor audit, using only the independent D2 A utilities."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import sys
import time

import independent_core as independent

C = independent.COUNTS
FRAME, B, COLORS = independent.FRAME, independent.BOUNDARY, independent.COLORS
edge, es, unique, tuples = independent.edge, independent.es, independent.unique, independent.tuples
relation, fibres, validate = independent.relation, independent.fibres, independent.validate
Q = (0,1,2,0,2)


def subdivision(graph, cert):
    left, right = cert['left'], cert['right']
    assert len(left) == len(right) == 3 and len(set(left+right)) == 6
    branches = set(left+right)
    assert len(cert['paths']) == 9
    used = set()
    pairs = []
    for p in cert['paths']:
        assert p[0] in left and p[-1] in right and len(p) == len(set(p))
        assert all(edge(v,w) in graph for v,w in zip(p,p[1:]))
        middle = set(p[1:-1])
        assert not middle & (branches | used)
        used |= middle
        pairs.append((p[0],p[-1]))
        C['K33_subdivision_path_witnesses'] += 1
    assert set(pairs) == set(product(left,right))
    C['independent_K33_subdivisions'] += 1


def identity(data, inherited, generic, rows):
    # Reuse only the previous independent implementation, never A's named_frame.
    inherited_counts = independent.audit_identity(inherited, generic, rows)
    source_ids = {f['named_frame_id']: f for t in inherited['targets'] for f in t['remaining_named_original_frames']}
    selected = data['selected_complete_original_frames']
    unique([t['source_sigma'] for t in data['targets']], 'A2 target source masks')
    assert {t['source_sigma'] for t in data['targets']} == {933,941}
    unique([s['source_sigma'] for s in data['root_swap_checks']], 'A2 root-swap source masks')
    unique([s['named_frame_id'] for s in selected], 'A2 selected ids')
    expected_selected = {i for i,f in source_ids.items() if f['original_a_spokes'] == [0,1] and f['original_b_spokes'] == [1,2]}
    assert {s['named_frame_id'] for s in selected} == expected_selected and len(expected_selected) == 4
    results = []
    for target in data['targets']:
        sigma = target['source_sigma']
        original = [f for i,f in source_ids.items() if f['source_sigma'] == sigma]
        chosen = [f for f in original if f['named_frame_id'] in expected_selected]
        remaining = [f for f in original if f not in chosen]
        for field in ('inherited_named_frame_ids','newly_excluded_named_frame_ids'):
            unique(target[field], 'A2 '+field)
        unique([f['named_frame_id'] for f in target['complete_remaining_named_original_frames']], 'A2 remaining raw ids')
        assert set(target['inherited_named_frame_ids']) == {f['named_frame_id'] for f in original}
        assert set(target['newly_excluded_named_frame_ids']) == {f['named_frame_id'] for f in chosen}
        assert target['complete_remaining_named_original_frames'] == remaining
        assert all(f['source_sigma'] == sigma for f in target['complete_remaining_named_original_frames'])
        supports = sum(len(f['remaining_named_original_U_placements']) for f in remaining)
        schedules = sum(len(p['complete_singleton_unary_relation_schedules']) for f in remaining for p in f['remaining_named_original_U_placements'])
        assert target['summary'] == dict(remaining_named_frames=len(remaining),remaining_actual_U_support_records=supports,remaining_complete_singleton_schedules=schedules)
        results.append(dict(source_sigma=sigma,inherited_frames=len(original),newly_excluded=len(chosen),remaining_frames=len(remaining),remaining_actual_U_support_records=supports,remaining_singleton_schedules=schedules))
        swap, = [s for s in data['root_swap_checks'] if s['source_sigma']==sigma]
        assert swap['original_and_swapped_ids']==[f['named_frame_id'] for f in chosen]
        assert swap['whole_frame_root_swap_only'] and swap['same_actual_supports_and_literal_singleton_relations']
        C['new_selected_frame_root_swap_pairs'] += 1
    for s in selected:
        f = s['inherited_complete_named_frame']
        assert f == source_ids[s['named_frame_id']]
        a,b = f['original_a'],f['original_b']
        sigma = f['source_sigma']
        assert not sigma >> rows.index(Q) & 1
        supports = {(0,2,3),(0,2,3,4)} | ({(2,3,4)} if sigma == 941 else set())
        assert {tuple(p['actual_original_U_support']) for p in f['remaining_named_original_U_placements']} == supports
        for p in f['remaining_named_original_U_placements']:
            assert 2 in p['actual_original_U_support']
            assert len(p['complete_singleton_unary_relation_schedules']) == 1
            assert set(p['complete_singleton_unary_relation_schedules'][0]['singleton_colors']) == {2}
            C['selected_inherited_actual_supports'] += 1
        row = s['designated_original_rejected_row']
        assert row['literal_boundary'] == list(Q) and row['row_index'] == rows.index(Q)
        assert row['complete_R_U'] == [[2]] and row['chosen_original_a_b_u_colors'] == [3,0,2]
        perm = row['actual_attachment_stabilizer']
        assert sorted(perm) == list(COLORS) and all(perm[Q[h]] == Q[h] for h in (0,2,3,4))
        assert perm[2] == 2 and perm[3] != 3
        crosscut = s['long_face_original_crosscut']
        long_face = [a,0,4,3,2,b]
        assert crosscut['original_long_face'] == long_face and crosscut['actual_U_endpoint'] == 2
        Csupports = crosscut['all_actual_C_support_subsets']
        unique([tuple(x['actual_C_support']) for x in Csupports], 'A2 crosscut actual C subsets')
        assert {tuple(x['actual_C_support']) for x in Csupports} == {p for n in range(5) for p in combinations((0,2,3,4),n)}
        for p in Csupports:
            assert p['compatible_with_same_original_U_crosscut'] == (set(p['actual_C_support']) <= {2})
            assert p['forbidden_actual_endpoints'] == sorted(set(p['actual_C_support'])-{2})
            C['actual_C_crosscut_support_subset_checks'] += 1
        assert crosscut['surviving_actual_C_supports'] == [[],[2]]
        unique([c['forbidden_actual_C_boundary_endpoint'] for c in crosscut['crossing_path_controls']], 'A2 crosscut endpoint controls')
        assert {c['forbidden_actual_C_boundary_endpoint'] for c in crosscut['crossing_path_controls']} == {0,4,3}
        for control in crosscut['crossing_path_controls']:
            endpoint = control['forbidden_actual_C_boundary_endpoint']
            assert endpoint in (0,4,3)
            assert control['alternating_original_face_endpoint_order'] == [a,endpoint,2,b]
            assert [long_face.index(z) for z in (a,endpoint,2,b)] == sorted(long_face.index(z) for z in (a,endpoint,2,b))
            skeleton = es(f['original_root_and_boundary_edges'])
            graph = skeleton | {edge(a,7),edge(7,2),edge(b,8),edge(a,8),edge(8,endpoint)} | {edge(9,h) for h in B}
            assert es(control['contracted_edges']) == graph
            subdivision(graph, control['explicit_apex_subdivision'])
        unique([i['original_boundary_hub'] for i in s['complete_C_extension_paper_instances']], 'A2 C hub instances')
        assert {i['original_boundary_hub'] for i in s['complete_C_extension_paper_instances']} == {1,2}
        for instance in s['complete_C_extension_paper_instances']:
            h = instance['original_boundary_hub']
            assert h in (1,2) and instance['actual_C_support_subsets'] == [[],[h]]
            assert instance['original_a_b_u_colors'] == [3,0,2]
            colors = instance['auxiliary_C_hub_colors']
            assert colors == [3,0,Q[h]] and len(set(colors)) == 3
            hubs = instance['original_exterior_hub_instance']
            bags = [set(b) for b in hubs['connected_hub_bags']]
            assert len(bags) == 3 and all(not bags[i] & bags[j] for i in range(3) for j in range(i))
            graph = es(hubs.get('original_edges', hubs.get('contracted_exterior_control_edges')))
            assert all(independent.connected(bag,graph) for bag in bags)
            assert hubs['C_external_neighbor_order'] == [a,b,h] and hubs['external_neighbor_to_hub'] == [0,1,2]
            assert all(v in bags[i] for i,v in enumerate((a,b,h)))
            for adj in hubs['all_hub_adjacencies']:
                i,j = adj['hub_pair']
                v,w = adj.get('original_edge',adj.get('original_or_contracted_path_edge'))
                assert edge(v,w) in graph and ((v in bags[i] and w in bags[j]) or (w in bags[i] and v in bags[j]))
                C['hub_adjacency_witnesses'] += 1
            local = instance['all_local_C_external_neighbor_subsets']
            unique([tuple(x['actual_external_neighbor_indices']) for x in local], 'A2 exact-list external-neighbor subsets')
            assert {tuple(x['actual_external_neighbor_indices']) for x in local} == {p for n in range(4) for p in combinations(range(3),n)}
            for x in local:
                ns = x['actual_external_neighbor_indices']
                assert x['actual_external_neighbors'] == [[a,b,h][i] for i in ns]
                assert x['exact_C_list'] == sorted(set(COLORS)-{colors[i] for i in ns})
                assert x['internal_C_degree'] == len(x['exact_C_list']) == 4-len(ns)
                C['exact_degree_list_local_controls'] += 1
            C['paper_hub_instance_premise_checks'] += 1
    conflicts = data['actual_U_supports_without_2_complete_relation_conflicts']
    unique([(s['source_sigma'],tuple(s['actual_original_U_support'])) for s in conflicts], 'missing2 source-support screens')
    assert {(s['source_sigma'],tuple(s['actual_original_U_support'])) for s in conflicts} == {(sigma,p) for sigma in (933,941) for n in range(4) for p in combinations((0,3,4),n)}
    for screen in conflicts:
        independent.audit_schedule(screen,screen['source_sigma'],(0,1),screen['actual_original_U_support'],rows)
        assert not screen['surviving_schedules']
        C['actual_support_missing_2_conflict_screens'] += 1
    return dict(inherited_A_identity_revalidation=inherited_counts,new_A2_ledger=results)


def graphs(data,rows):
    controls = data['fixed_full_degree_same_graph_controls']
    records = controls['records']
    unique([r['control_index'] for r in records], 'A2 graph ids')
    designated_table = {d['control_index']:d for d in controls['designated_row_fixed_exterior_audits']}
    unique([d['control_index'] for d in controls['designated_row_fixed_exterior_audits']], 'A2 designated records')
    assert len(designated_table) == len(records)
    all_masks = Counter()
    for rec in records:
        a,b = rec['original_a'],rec['original_b']
        cp,up = rec['C'],rec['unary_U']
        cv,uv = set(cp['vertices']),set(up['vertices'])
        x,y0,y1 = cp['ordered_contacts'];u, = up['ordered_contacts']
        ports = [a,b,x,y0,y1,u]
        assert cp['owners'] == [a,b,b] and up['owner'] == a and y0 != y1
        assert rec['complete_port_order'] == ports
        assert cp['x_y_alias'] == ('y0' if x == y0 else 'y1' if x == y1 else None)
        C['new_contact_identity_'+str(cp['x_y_alias'])+'_graphs'] += 1
        assert not cv & uv and not (cv|uv)&(B|{a,b})
        original = es(rec['original_edges']);parts = {}
        for name,part in (('C',cp),('U',up)):
            vs = set(part['vertices']);internal = es(part['original_internal_edges'])
            assert all(set(e)<=vs for e in internal) and independent.connected(vs,internal)
            attach = {edge(int(v),h) for v,hs in part['actual_attachments'].items() for h in hs}
            assert set(map(int,part['actual_attachments'])) == vs
            assert set(part['actual_support']) == {h for hs in part['actual_attachments'].values() for h in hs}
            parts[name] = internal|attach
            for p in part['original_owner_to_attachment_paths']:
                path = p['original_path']
                assert path[0] == p['owner'] and path[-1] == p['boundary_endpoint']
                assert p['owner'] in ([a,b] if name == 'C' else [a])
                assert len(path) == len(set(path)) and set(path[1:-1])<=vs
                assert all(edge(v,w) in original for v,w in zip(path,path[1:]))
                C['new_actual_attachment_path_witnesses'] += 1
        path = up['original_a_to_2_crosscut']
        assert path[0] == a and path[-1] == 2 and len(path) == len(set(path)) and set(path[1:-1])<=uv
        assert all(edge(v,w) in original for v,w in zip(path,path[1:]))
        C['new_actual_U_crosscut_paths'] += 1
        rebuilt = FRAME|parts['C']|parts['U']|{edge(a,b),edge(a,x),edge(a,u),edge(b,y0),edge(b,y1)}
        rebuilt |= {edge(a,h) for h in rec['original_root_spokes']['a']}|{edge(b,h) for h in rec['original_root_spokes']['b']}
        assert rebuilt == original
        order = sorted(B|{a,b}|cv|uv);assert rec['vertex_order'] == order
        assert all(sum(v in e for e in original)==(5 if v in (a,b) else 4) for v in {a,b}|cv|uv)
        masks = Counter()
        for ri,row in enumerate(rec['rows']):
            beta = rows[ri];assert row['row_index']==ri and row['literal_boundary']==list(beta)
            cr = relation(cp['vertex_order'],FRAME|parts['C'],beta,[x,y0,y1],row['C_complete_tuples'],'new_C_ternary')
            ur = relation(up['vertex_order'],FRAME|parts['U'],beta,[u],row['U_complete_tuples'],'new_U_unary')
            unique([v['id'] for v in row['variants']], 'A2 variants')
            assert {v['id'] for v in row['variants']} == {'original','a_x','a_u','a_spoke_0','a_spoke_1','b_spoke_1','b_spoke_2','whole_U'}
            joints = {}
            for v in row['variants']:
                if v['id']=='whole_U':
                    expected = {e for e in original if not set(e)&uv}
                    assert v['vertex_order']==sorted(set(order)-uv) and v['complete_port_order']==ports[:5]
                    assert v['removed_original_vertices']==sorted(uv)
                    field,cat = 'complete_five_role_joint','new_N_five_role'
                    tail = 'complete_x_y0_y1_fiber'
                else:
                    omitted=v['omitted_original_edge'];expected=original-({edge(*omitted)} if omitted is not None else set())
                    assert v['vertex_order']==order and v['complete_port_order']==ports
                    field,cat = 'complete_joint_tuples','new_full_six_role'
                    tail='complete_x_y0_y1_u_fiber'
                assert es(v['actual_edges'])==expected
                joint=relation(v['vertex_order'],expected,beta,v['complete_port_order'],v[field],cat)
                joints[v['id']]=joint;masks[v['id']] += (1<<ri) if joint else 0
                fibres(v['pinned_a_b_fibers'],joint,tail)
                if v['id']!='whole_U':
                    joined={(ac,bc,xc,c0,c1,uc) for xc,c0,c1 in cr for uc, in ur for ac,bc in product(COLORS,repeat=2)
                            if ac!=bc and all(ac!=beta[h] for h in B if edge(a,h) in expected)
                            and all(bc!=beta[h] for h in B if edge(b,h) in expected)
                            and (edge(a,x) not in expected or ac!=xc) and (edge(a,u) not in expected or ac!=uc)
                            and bc!=c0 and bc!=c1}
                    assert joined==joint;C['new_independent_same_graph_joins']+=1
                info=v.get('exact_reattachment',{})
                if 'removed_joint_tuples' in info:
                    removed=tuples(info['removed_joint_tuples'],'A2 removed tuples')
                    assert removed=={t for t in joint if t[info['root_tuple_position']]==beta[info['boundary_endpoint']]}
                    for w in info['removed_joint_tuples']:
                        validate(order,w['coloring'],expected,beta,ports,w['tuple']);C['new_removed_tuple_witnesses']+=1
            restored=joints['original']
            for name,joint in joints.items():
                if name in ('original','whole_U'):continue
                var, = [v for v in row['variants'] if v['id']==name];omitted=var['omitted_original_edge']
                expected=set()
                for t in joint:
                    f=dict(enumerate(beta))|dict(zip(ports,t,strict=True))
                    if f[omitted[0]]!=f[omitted[1]]:expected.add(t)
                assert expected==restored;C['new_exact_edge_reattachments']+=1
            n=joints['whole_U'];assert joints['a_u']=={(*t,uc) for t in n for uc, in ur}
            C['new_exact_U_omission_products']+=1
            ad,ud={t[0] for t in n},{t[0] for t in ur}
            assert (not restored)==(ad==ud and len(ad)==1)
            C['new_nonempty_domain_singleton_checks']+=1
            designated=row['designated_rejected_row_audit']
            if beta!=Q:assert designated is None;continue
            assert designated['fixed_original_exterior']==dict(a=3,b=0,u=2)
            assert ud=={2}
            for dest in (designated, designated_table[rec['control_index']]):
                assert dest.get('control_index',rec['control_index'])==rec['control_index']
                assert dest['complete_original_R_U']==row['U_complete_tuples']
                relation(up['vertex_order'],FRAME|parts['U'],beta,[u],dest['complete_original_R_U'],'new_designated_U_duplicate')
                actual=tuples(dest['complete_original_C_fixed_root_fiber'],'designated C fibre')
                assert actual=={t for t in cr if t[0]!=3 and t[1]!=0 and t[2]!=0} and actual
                for w in dest['complete_original_C_fixed_root_fiber']:
                    validate(cp['vertex_order'],w['coloring'],FRAME|parts['C'],beta,[x,y0,y1],w['tuple']);C['new_designated_C_duplicate_witnesses']+=1
                actual=tuples(dest['complete_original_joint_at_fixed_exterior'],'designated original joint')
                assert actual=={t for t in restored if (t[0],t[1],t[5])==(3,0,2)} and actual
                for w in dest['complete_original_joint_at_fixed_exterior']:
                    validate(order,w['coloring'],original,beta,ports,w['tuple']);C['new_designated_joint_duplicate_witnesses']+=1
                C['new_designated_complete_extension_records']+=1
        for image in rec['independently_computed_control_boundary_images']:
            assert image['full_boundary_image']==masks[image['variant_id']];C['new_complete_control_Sigma_masks']+=1
        all_masks[masks['original']]+=1;C['new_fixed_full_degree_graphs']+=1
    for swap in controls['root_swap_controls']:
        left,right=(records[swap[k]] for k in ('original_control_index','exchanged_control_index'))
        move=lambda v:11-v if v in (5,6) else v
        assert {edge(move(v),move(w)) for v,w in left['original_edges']}==es(right['original_edges'])
        for lr,rr in zip(left['rows'],right['rows'],strict=True):
            assert lr['C_complete_tuples']==rr['C_complete_tuples'] and lr['U_complete_tuples']==rr['U_complete_tuples']
            for lv,rv in zip(lr['variants'],rr['variants'],strict=True):
                field='complete_five_role_joint' if lv['id']=='whole_U' else 'complete_joint_tuples'
                assert lv['pinned_a_b_fibers']==rv['pinned_a_b_fibers']
                assert [move(v) for v in lv['complete_port_order']]==rv['complete_port_order']
                assert [w['tuple'] for w in lv[field]]==[w['tuple'] for w in rv[field]]
                for lw,rw in zip(lv[field],rv[field],strict=True):
                    f=dict(zip(lv['vertex_order'],lw['coloring'],strict=True))
                    assert [f[move(v)] for v in rv['vertex_order']]==rw['coloring'];C['new_root_swap_full_witness_checks']+=1
                C['new_root_swap_literal_joint_checks']+=1
        C['new_root_swap_graph_pairs']+=1
    negatives={}
    for name in ('ternary_marginal_collision','six_role_joint_inequivalence'):
        item=controls[name];rec=records[item['control_index']];row=rec['rows'][item['row_index']];beta=rows[item['row_index']]
        if name=='ternary_marginal_collision':
            cp=rec['C'];cr=tuples(item['complete_C_tuples'],'A2 negative C')
            assert item['complete_C_tuples']==row['C_complete_tuples']
            edges=FRAME|es(cp['original_internal_edges'])|{edge(int(v),h) for v,hs in cp['actual_attachments'].items() for h in hs}
            relation(cp['vertex_order'],edges,beta,cp['ordered_contacts'],item['complete_C_tuples'],'new_negative_C')
            ac,bc=item['literal_a_b_colors'];assert not {t for t in cr if t[0]!=ac and t[1]!=bc and t[2]!=bc}
            fake={t for t in product(*[{t[i] for t in cr} for i in range(3)]) if t[0]!=ac and t[1]!=bc and t[2]!=bc};assert fake
            negatives[name]=dict(fake_marginal_tuples=sorted(fake),exact_fibre=[])
        else:
            original, = [v for v in row['variants'] if v['id']=='original'];ax, = [v for v in row['variants'] if v['id']=='a_x']
            assert item['original_complete_joint']==original['complete_joint_tuples'] and item['ax_omitted_complete_joint']==ax['complete_joint_tuples']
            j=relation(rec['vertex_order'],es(original['actual_edges']),beta,rec['complete_port_order'],item['original_complete_joint'],'new_negative_original_joint')
            k=relation(rec['vertex_order'],es(ax['actual_edges']),beta,rec['complete_port_order'],item['ax_omitted_complete_joint'],'new_negative_ax_joint')
            t=tuple(item['omission_only_tuple']);assert t in k-j
            validate(rec['vertex_order'],item['omission_only_full_coloring'],es(ax['actual_edges']),beta,rec['complete_port_order'],t)
            negatives[name]=dict(omitted_only_tuple=t,original_tuple_count=len(j),omission_tuple_count=len(k))
        negatives[name].update(literal_boundary=beta,original_edges=rec['original_edges'],vertex_order=rec['vertex_order'],complete_port_order=rec['complete_port_order'],stored_counterexample_and_full_witnesses=item)
    return dict(control_Sigma_counts=dict(all_masks),counterexamples=negatives)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,default=Path('/tmp/math-task-d2-successor-v2'))
    args=parser.parse_args();out=Path(__file__).resolve().parent;started=time.monotonic()
    paths=[args.repo/'artifacts'/f'{s}/observations.json' for s in ('c5_excess_two_mixed_core_four_spoke_mixed12_01_12','c5_excess_two_mixed_core_four_spoke_mixed12','c5_excess_two_mixed_core_single_spoke')]
    before={str(p.relative_to(args.repo)):sha256(p.read_bytes()).hexdigest() for p in paths}
    data,inherited,generic=[json.loads(p.read_text()) for p in paths]
    for name,expected in data['input_sha256'].items():
        assert sha256((args.repo/name).read_bytes()).hexdigest()==expected, ('input hash drift',name)
        C['new_bound_input_hashes_verified']+=1
    rows=tuple(sorted({independent.normalized(q)[0] for q in product(COLORS,repeat=5) if all(q[a]!=q[b] for a,b in FRAME)}))
    assert tuple(map(tuple,data['pattern_order']))==rows
    ledger=identity(data,inherited,generic,rows)
    result_graphs=graphs(data,rows)
    def coloring_count(x):
        if isinstance(x,list):return sum(map(coloring_count,x))
        if isinstance(x,dict):return sum(int(k in ('coloring','omission_only_full_coloring'))+coloring_count(v) for k,v in x.items())
        return 0
    assert coloring_count(data)==C['stored_colorings_validated']
    C['all_new_serialized_coloring_fields_accounted_for']=coloring_count(data)
    after={str(p.relative_to(args.repo)):sha256(p.read_bytes()).hexdigest() for p in paths};assert before==after
    result=dict(all_checks_passed=True,status='PASS',frozen_input_root=str(args.repo),input_sha256=before,source_artifact_bytes_preserved=True,identity=ledger,graphs=result_graphs,summary=dict(C),counts=dict(C),independent_utility_sha256=sha256(Path(independent.__file__).read_bytes()).hexdigest(),elapsed_seconds=round(time.monotonic()-started,3),limits=['Independent finite identity/minor/relation audit; arbitrary-size crosscut and Gallai/K4 extension remain paper arguments.','36 controls all have complete Sigma1023; no disk/criticality/Sigma933/941 realization established.','20/24 other mixed12 frames remain; epsilon>=3, general exits, Lean topology and K-infinity=K-at-most5 remain unproved.'])
    (out/'results.json').write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
    (out/'counterexamples.json').write_text(json.dumps(result_graphs['counterexamples'],ensure_ascii=False,sort_keys=True,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',identity=ledger,counts=dict(C),elapsed_seconds=result['elapsed_seconds']),sort_keys=True),flush=True)


if __name__=='__main__':main()
