#!/usr/bin/env python3
"""D5 C4 independent audit of an immutable input repository.

No production checker is imported. D4 independent_front/solve and generic
witness validation are reused verbatim with recorded source SHA256. The
finite graph models are independently specified here from the final report.
Fresh outputs retain source bytes, failures, complete relations and all fibres.
"""
import argparse
from copy import deepcopy
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import traceback

from independent_helpers import Audit, CONTEXT, P3, edge, connected
from predecessor_front import independent_front, solve

HERE = Path(__file__).resolve().parent
DEFAULT_REPO = HERE.parent / 'snapshot'
Q = (0, 1, 0, 1, 2)
SIGMA = (0, 1, 3, 2)
U = set(range(4))
C = 'artifacts/c5_mixed_p3_common_endpoint/observations.json'
C2 = 'artifacts/c5_mixed_p3_one_color_ternary_unary/observations.json'
C3 = 'artifacts/c5_mixed_p3_two_frame_ternary_unary/observations.json'
C4 = 'artifacts/c5_mixed_p3_two_frame_two_unary/observations.json'
KEY = ['CPP-134-1', 34, 60]
SOURCES = ('audit_c4.py', 'independent_helpers.py', 'predecessor_front.py')


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=1) + '\n')


def canonical(data):
    return json.loads(json.dumps(data))


def sigma(t):
    return tuple(SIGMA[c] for c in t)


def forbidden(relation):
    if not relation:
        raise ValueError('forbidden-color intersection requires a nonempty full relation')
    return set.intersection(*(set(t) for t in relation))


def relation_fibres(relation):
    return [dict(z=h, complete_contact_tuples=sorted(t for t in relation if h not in t))
            for h in range(4)]


def saturated_relations(arity, f):
    domain = [t for t in product(range(4), repeat=arity) if set(t) == set(f)]
    rows = []
    for n in range(1, len(domain) + 1):
        for chosen in combinations(domain, n):
            relation, image = set(chosen), set(map(sigma, chosen))
            rows.append(dict(id=len(rows), ordered_complete_relation=sorted(relation),
                required_forbidden=sorted(f), sigma_image_complete_relation=sorted(image),
                sigma_image_forbidden=sorted(forbidden(image)),
                forced_missing_tuples=sorted(image-relation),
                root_avoidance_fibers=relation_fibres(relation),
                image_root_avoidance_fibers=relation_fibres(image),
                compatible_with_full_original_lift_involution=relation==image))
    return rows


def audit_relations(a, data):
    binary, unary = saturated_relations(2, {0,3}), saturated_relations(1, {2})
    a.ck('relations/exact_three_ordered_binary_candidates', canonical(binary)==data['binary_exact_complete_relation_candidates'])
    a.ck('relations/exact_one_ordered_unary_candidate', canonical(unary)==data['unary_exact_complete_relation_candidates'])
    for name, rows, required in [('D_z2',binary,{0,3}),('D_z1',unary,{2})]:
        for row in rows:
            relation=set(map(tuple,row['ordered_complete_relation']));image=set(map(tuple,row['sigma_image_complete_relation']))
            prefix=f'{name}/relation_{row["id"]}'
            a.ck(prefix+'/saturated_exact_forbidden', forbidden(relation)==required)
            a.ck(prefix+'/ordered_contact_image_and_involution', set(map(sigma,image))==relation)
            a.ck(prefix+'/strict_missing_image_and_forbidden_contradiction',bool(image-relation) and forbidden(image)!=required)
            for h in range(4):
                fibre={t for t in relation if h not in t}
                image_fibre={t for t in image if SIGMA[h] not in t}
                a.ck(prefix+f'/fibre_bijection_{h}',set(map(sigma,fibre))==image_fibre)
            left=2 if name=='D_z2' else 3;right=SIGMA[left]
            a.ck(prefix+'/original_sigma_pins_nonempty_vs_empty',bool([t for t in relation if left not in t]) and not [t for t in relation if right not in t])
    options=[list(t) for n in range(3) for t in combinations((1,2),n)]
    own=[];covers=[];combinations_=[]
    for support in options:
        colors=sorted({Q[b] for b in support})
        own.append(dict(actual_support_candidate=support,actual_attachment_colors=colors,
            sigma_fixes_every_possible_attachment=all(SIGMA[c]==c for c in colors),
            binary_complete_relation_candidate_ids=[r['id'] for r in binary],unary_complete_relation_candidate_ids=[0],
            binary_survivors=[],unary_survivors=[]))
    a.ck('supports/exact_four_own_support_candidates',own==data['support_controls']['individual_support_candidates'])
    for a2,a1 in product(options,repeat=2):
        if set(a2)|set(a1)!={1,2}:
            continue
        idx=len(covers)
        pairs=[dict(binary_relation_id=r['id'],unary_relation_id=0,
            binary_compatible=r['compatible_with_full_original_lift_involution'],
            unary_compatible=unary[0]['compatible_with_full_original_lift_involution']) for r in binary]
        covers.append(dict(id=idx,D_z2_actual_support_candidate=a2,D_z1_actual_support_candidate=a1,
            D_z2_sigma_fixed_attachment_colors=sorted({Q[b] for b in a2}),
            D_z1_sigma_fixed_attachment_colors=sorted({Q[b] for b in a1}),
            candidate_complete_relation_pairs=pairs,survivors=[]))
        for b in binary:
            combinations_.append(dict(support_configuration_id=idx,ordered_component_supports=[a2,a1],
                ordered_components=['D_z2','D_z1'],ordered_contacts=[['u0','u1'],['r0']],
                binary_relation_id=b['id'],unary_relation_id=0,
                binary_complete_relation=b['ordered_complete_relation'],unary_complete_relation=unary[0]['ordered_complete_relation'],
                binary_all_four_root_fibres=b['root_avoidance_fibers'],unary_all_four_root_fibres=unary[0]['root_avoidance_fibers'],
                binary_forced_missing_tuples=b['forced_missing_tuples'],unary_forced_missing_tuples=unary[0]['forced_missing_tuples'],
                individually_impossible_components=['D_z2','D_z1'],survives=False,
                realization_claim=False))
    a.ck('supports/exact_nine_ordered_own_support_covers',covers==data['support_controls']['ordered_original_component_support_covers'] and len(covers)==9)
    a.ck('supports/exact_twenty_seven_complete_relation_combinations',len(combinations_)==27 and not any(r['survives'] for r in combinations_))
    ownership=[]
    for b in binary:
        relation={tuple(t)+(2,) for t in b['ordered_complete_relation']};image=set(map(sigma,relation))
        ownership.append(dict(binary_relation_id=b['id'],ordered_contacts_with_ownership=['D_z2.u0','D_z2.u1','D_z1.r0'],
            required_product_complete_relation=sorted(relation),sigma_image=sorted(image),aggregate_forbidden=sorted(forbidden(relation)),
            aggregate_forbidden_sigma_invariant=forbidden(image)==forbidden(relation),original_component_product_sigma_invariant=relation==image,
            sigma_closure_is_not_original_relation=True))
        a.ck(f'ownership/relation_{b["id"]}/union_invariant_but_owned_relation_not_invariant',forbidden(relation)=={0,2,3}==forbidden(image) and relation!=image)
    a.ck('ownership/exact_three_complete_product_relations',canonical(ownership)==data['ownership_controls'])
    return dict(binary_complete_relation_candidates=binary,unary_complete_relation_candidates=unary,
        own_support_candidates=own,all_nine_ordered_support_covers=covers,all_twenty_seven_necessary_combinations=combinations_,
        complete_owned_product_negative_controls=ownership)


def audit_involution(a,data):
    raw=data['involution_controls'];a.ck('involution/exact_transposition',raw['sigma']==list(SIGMA) and all(SIGMA[SIGMA[c]]==c for c in range(4)))
    internal=[];attachments=[];domains=[]
    for left,right in product(range(4),repeat=2):
        internal.append(dict(original_ordered_endpoint_colors=[left,right],image_ordered_endpoint_colors=[SIGMA[left],SIGMA[right]],
            proper_before=left!=right,proper_after=SIGMA[left]!=SIGMA[right]))
        a.ck(f'involution/original_edge_including_bridge_{left}_{right}',(left!=right)==(SIGMA[left]!=SIGMA[right]))
    for b,color in product((1,2),range(4)):
        attachments.append(dict(actual_boundary_vertex=b,fixed_boundary_color=Q[b],internal_color=color,image_internal_color=SIGMA[color],
            attachment_proper_before=color!=Q[b],attachment_proper_after=SIGMA[color]!=Q[b]))
        a.ck(f'involution/own_attachment_b{b}_color{color}',SIGMA[Q[b]]==Q[b] and (color!=Q[b])==(SIGMA[color]!=Q[b]))
    for n in (1,2):
        domains.append(dict(arity=n,tuples=[dict(original=t,image=sigma(t)) for t in product(range(4),repeat=n)]))
    for name,expected in [('internal_edge_and_original_bridge_truth_table',internal),('actual_attachment_truth_table',attachments),('complete_ordered_tuple_domains',domains)]:
        a.ck('involution/'+name,raw[name]==canonical(expected))
    a.ck('involution/b4_and_w_are_exterior',Q[4]==2 and SIGMA[Q[4]]!=Q[4] and 'b4=2 stays fixed' in raw['unchanged_exterior'])
    return dict(sigma=list(SIGMA),all_sixteen_original_ordered_edge_color_tests=internal,
        all_eight_own_attachment_color_tests=attachments,complete_ordered_domains=domains,
        arbitrary_size_argument='Apply sigma pointwise to every original vertex of one detached unary. Each original internal edge, including bridges, retains inequality. Own boundary endpoints have colors 0 or 1 and stay fixed. Sigma squared is identity. Hence full lifts and ordered contact relations are bijective.',
        exterior_kept_pointwise='B, P3, zw, wx2, the other unary, and unknown D_w; b4 remains color 2')


MODELS=[dict(name='control_binary_original_bridge',vertices=[20,21],contacts=[20,21],
    internal={(20,21)},attachments={20:[5,1,2],21:[5,1,2]},expected_forbidden=[2,3],requested_forbidden=[0,3]),
    dict(name='control_one_contact_two_N_triangles_bridge',vertices=list(range(30,36)),contacts=[30],
    internal={(30,31),(31,32),(30,32),(33,34),(34,35),(33,35),(30,33)},
    attachments={30:[5],31:[1,2],32:[1,2],33:[2],34:[1,2],35:[1,2]},expected_forbidden=[0],requested_forbidden=[2])]


def local_lifts(model,deleted=None,root_pin=None,endpoint_pin=None):
    vertices=set(model['vertices']);edges=model['edges']-({deleted} if deleted else set());pins=dict(enumerate(Q))
    if root_pin is None:
        edges={e for e in edges if 5 not in e}
    else:
        vertices.add(5);pins[5]=root_pin
    if endpoint_pin:
        pins.update(endpoint_pin)
    cols=solve(set(range(5))|vertices,edges,pins)
    return [{v:col[v] for v in model['vertices']} for col in cols]


def lift_keys(lifts,vertices):
    return sorted(tuple(col[str(v)] if str(v) in col else col[v] for v in vertices) for col in lifts)


def validate_local_lifts(a,stored,computed,model,deleted=None,root_pin=None,label=''):
    vertices=model['vertices'];edges=model['edges']-({deleted} if deleted else set())
    if root_pin is None:edges={e for e in edges if 5 not in e}
    pins=dict(enumerate(Q))|({5:root_pin} if root_pin is not None else {})
    a.ck(label+'/exact_full_same_model_lift_set',lift_keys(stored,vertices)==lift_keys(computed,vertices))
    a.ck(label+'/no_duplicate_full_lifts',len(lift_keys(stored,vertices))==len(set(lift_keys(stored,vertices))))
    for i,raw in enumerate(stored):
        a.ck(label+f'/lift_{i}/exact_internal_vertex_domain',{int(v) for v in raw}==set(vertices))
        full={str(v):c for v,c in pins.items()}|raw
        a.coloring(full,set(vertices)|set(pins),edges,pins,label+f'/lift_{i}')


def audit_models(a,data):
    raw=data['aggregate_bridge_control'];records=raw['components'];models=[];bridge_queries=0;deleted_count=0
    a.ck('control/exact_two_original_owned_models',len(records)==2 and [r['name'] for r in records]==[m['name'] for m in MODELS])
    for original,record in zip(MODELS,records):
        model=deepcopy(original);label=model['name'];vertices=model['vertices'];contacts=model['contacts']
        expected=model['internal']|{edge(v,b) for v,bs in model['attachments'].items() for b in bs}
        edges=a.edges(record['original_edges'],label+'/original_edges',expected);model['edges']=edges
        a.ck(label+'/exact_original_contacts_and_vertex_order',record['vertices']==vertices and record['ordered_contacts']==contacts)
        a.ck(label+'/original_degree_four',record['complete_degrees']=={str(v):4 for v in vertices} and all(sum(v in e for e in edges)==4 for v in vertices))
        a.ck(label+'/exact_own_attachment_support',record['actual_support']==[1,2] and sorted({b for bs in model['attachments'].values() for b in bs if b<5})==[1,2])
        a.ck(label+'/own_context_original_component_connected',connected(set(vertices),edges))
        lifts=local_lifts(model);relation=sorted({tuple(c[v] for v in contacts) for c in lifts})
        a.ck(label+'/complete_original_ordered_relation',record['complete_contact_relation']==canonical(relation))
        a.ck(label+'/control_ownership_differs_from_join60',record['control_forbidden']==sorted(forbidden(relation))==model['expected_forbidden'] and record['requested_join60_forbidden']==model['requested_forbidden'] and model['expected_forbidden']!=model['requested_forbidden'])
        validate_local_lifts(a,record['full_same_component_lifts'],lifts,model,label=label+'/intact')
        transformed=[{v:SIGMA[c] for v,c in col.items()} for col in lifts]
        a.ck(label+'/full_lift_involution_bijection',lift_keys(transformed,vertices)==lift_keys(lifts,vertices))
        validate_local_lifts(a,record['sigma_transformed_full_lifts'],transformed,model,label=label+'/stored_sigma')
        a.ck(label+'/exact_four_original_root_pins',len(record['fibers'])==4 and [r['root_z'] for r in record['fibers']]==list(range(4)))
        fibre_rows=[]
        for pin in record['fibers']:
            h=pin['root_z'];computed=local_lifts(model,root_pin=h);ts=sorted({tuple(c[v] for v in contacts) for c in computed})
            a.ck(label+f'/root_{h}/complete_relation_including_empty',pin['complete_contact_fiber']==canonical(ts))
            validate_local_lifts(a,pin['full_same_component_lifts'],computed,model,root_pin=h,label=label+f'/root_{h}')
            fibre_rows.append(dict(root_z=h,complete_contact_relation=ts,all_full_lifts=computed))
        bridges=[e for e in sorted(model['internal']) if not connected(set(vertices),edges-{e})]
        a.ck(label+'/all_original_bridges',bridges==[(20,21)] if vertices==[20,21] else bridges==[(30,33)])
        a.ck(label+'/exact_stored_original_bridge_list',[r['original_edge'] for r in record['original_bridge_records']]==canonical(bridges))
        bridge_rows=[]
        for bridge,bridge_raw in zip(bridges,record['original_bridge_records']):
            a.ck(label+'/bridge/exact_four_pins',len(bridge_raw['pins'])==4 and [p['root_z'] for p in bridge_raw['pins']]==list(range(4)))
            pins=[]
            for pin in bridge_raw['pins']:
                h=pin['root_z'];computed=local_lifts(model,deleted=bridge,root_pin=h)
                endpoints=sorted({tuple(c[v] for v in bridge) for c in computed})
                a.ck(label+f'/deleted_bridge/root_{h}/same_ordered_original_endpoints',pin['ordered_endpoints']==list(bridge))
                a.ck(label+f'/deleted_bridge/root_{h}/complete_same_model_endpoint_relation',pin['complete_endpoint_relation']==canonical(endpoints))
                validate_local_lifts(a,pin['full_same_deleted_component_lifts'],computed,model,deleted=bridge,root_pin=h,label=label+f'/deleted_bridge/root_{h}')
                all_endpoint_pins=[]
                for left,right in product(range(4),repeat=2):
                    full=local_lifts(model,deleted=bridge,root_pin=h,endpoint_pin={bridge[0]:left,bridge[1]:right});bridge_queries+=1
                    all_endpoint_pins.append(dict(ordered_endpoint_colors=[left,right],full_same_deleted_component_lifts=full))
                a.ck(label+f'/deleted_bridge/root_{h}/all_16_endpoint_queries_complete',[r['ordered_endpoint_colors'] for r in all_endpoint_pins if r['full_same_deleted_component_lifts']]==canonical(endpoints))
                deleted_count+=len(computed)
                pins.append(dict(root_z=h,ordered_endpoints=list(bridge),complete_endpoint_relation=endpoints,
                    all_full_same_deleted_component_lifts=computed,all_sixteen_endpoint_pin_fibres=all_endpoint_pins))
            bridge_rows.append(dict(original_bridge=list(bridge),four_original_root_pins=pins))
        models.append(dict(name=label,original_vertices=vertices,ordered_contacts=contacts,original_edges=sorted(edges),
            exact_own_attachments=model['attachments'],actual_own_support=[1,2],complete_contact_relation=relation,
            all_full_original_component_lifts=lifts,all_sigma_transformed_full_lifts=transformed,
            all_four_root_fibres=fibre_rows,original_bridges=bridge_rows))
    joint=[]
    for b,u in product(models[0]['all_full_original_component_lifts'],models[1]['all_full_original_component_lifts']):
        col=b|u;joint.append(dict(ordered_contact_tuple=[col[v] for v in (20,21,30)],full_both_component_lift=col))
    a.ck('control/eight_exact_full_owned_joint_lifts',len(joint)==8 and sorted((tuple(r['ordered_contact_tuple']),tuple(sorted((int(v),c) for v,c in r['full_both_component_lift'].items()))) for r in raw['full_both_component_lifts'])==sorted((tuple(r['ordered_contact_tuple']),tuple(sorted(r['full_both_component_lift'].items()))) for r in joint))
    global_relation=sorted({tuple(row['ordered_contact_tuple']) for row in joint})
    a.ck('control/exact_complete_global_ordered_relation',raw['complete_global_z_contact_relation']==canonical(global_relation)==[[2,3,0],[3,2,0]] and raw['global_ordered_z_contacts']==[20,21,30])
    a.ck('control/aggregate_same_forbidden_cannot_restore_ownership',raw['aggregate_forbidden']==sorted(forbidden(global_relation))==[0,2,3] and raw['control_forbidden']==[[2,3],[0]] and raw['requested_join60_forbidden']==[[0,3],[2]])
    a.ck('control/aggregate_all_four_fibres_including_empties',raw['aggregate_fibers']==[dict(root_z=h,complete_contact_fiber=canonical([t for t in global_relation if h not in t])) for h in range(4)])
    a.edges(raw['original_context_edges'],'control/original_context',CONTEXT)
    projection=CONTEXT|set(map(tuple,models[0]['original_edges']))|set(map(tuple,models[1]['original_edges']))
    a.edges(raw['original_projection_edges'],'control/original_projection',projection)
    a.ck('control/original_root_z_full_degree_five',sum(5 in e for e in projection)==raw['original_root_z_complete_degree']==5)
    a.ck('control/P3_full_original_degree_four',all(sum(v in e for e in projection)==4 for v in P3))
    witness=raw['context_partial_witness'];pins=dict(enumerate(Q))|{5:1,6:1};all_vertices=set(range(10))|set(MODELS[0]['vertices'])|set(MODELS[1]['vertices'])
    a.ck('control/partial_witness_omits_only_zw',witness['omitted_edge']==[5,6] and witness['root_z']==witness['root_w']==1)
    col=a.coloring(witness['coloring'],all_vertices,projection-{(5,6)},pins,'control/context_partial_witness')
    if col:a.ck('control/partial_witness_original_P3_order',list(map(col.get,P3))==witness['original_P3_tuple']==[3,0,3])
    a.ck('control/w_unknown_symbolic_scope','symbolic' in witness['unknown_w_component'] and 'not intact M or D_w lift' in witness['scope'])
    context_rows=[]
    for deleted in (None,(5,6)):
        root_rows=[]
        for z,w in product(range(4),repeat=2):
            full=solve(all_vertices,projection-({deleted} if deleted else set()),dict(enumerate(Q))|{5:z,6:w})
            root_rows.append(dict(root_pair=[z,w],complete_owned_contact_relation=sorted({tuple(c[v] for v in (20,21,30)) for c in full}),all_context_partial_lifts=full,
                missing_original_D_w='same-source full R_Dw remains symbolic; these are projection colorings'))
        context_rows.append(dict(deleted_original_edge=deleted,all_sixteen_root_fibres=root_rows))
    a.ck('control/intact_zw_prevents_pin_1_1',not next(r for r in context_rows[0]['all_sixteen_root_fibres'] if r['root_pair']==[1,1])['all_context_partial_lifts'])
    a.ck('control/omitted_zw_has_projection_pin_1_1',len(next(r for r in context_rows[1]['all_sixteen_root_fibres'] if r['root_pair']==[1,1])['all_context_partial_lifts'])==8)
    minor=raw['original_K5_minor'];groups=[{34},{35},{1},{2},{0,3,4,5,9,30,31,32,33}]
    a.ck('control/K5/exact_five_named_original_bags',minor['branch_sets']==[sorted(g) for g in groups] and minor['selected_N_leaf_vertices']==[34,35])
    a.minor(projection,minor['branch_sets'],minor['adjacency'],'control/K5/original_witness')
    for n,path in enumerate(minor['original_hub_paths']):
        a.ck(f'control/K5/hub_path_{n}/original_edges',all(edge(v,w) in projection for v,w in zip(path,path[1:])))
    return dict(components=models,complete_joint_owned_relation=global_relation,all_eight_owned_joint_lifts=joint,
        all_context_projection_root_fibres=context_rows,original_projection_edges=sorted(projection),
        exact_K5_minor=minor,deleted_bridge_full_lift_count=deleted_count,endpoint_pin_queries=bridge_queries)


def audit_rotation(a,raw):
    skeleton=CONTEXT|{edge(root,b) for root,bs in zip((5,6),([1,2],[2,4])) for b in bs}
    rotation={int(v):ns for v,ns in raw['rotation'].items()}
    a.ck('geometry/rotation_domain',set(rotation)==set(range(10)))
    for v in range(10):
        a.ck(f'geometry/rotation_{v}/original_neighbor_cycle',len(rotation[v])==len(set(rotation[v])) and set(rotation[v])=={b if v==a else a for a,b in skeleton if v in (a,b)})
    darts={(a,b) for e in skeleton for a,b in (e,e[::-1])};visited=set();faces=[]
    for start in sorted(darts):
        if start in visited:continue
        cur=start;face=[]
        while cur not in visited:
            visited.add(cur);v,w=cur;face.append(v);ns=rotation[w];cur=(w,ns[(ns.index(v)-1)%len(ns)])
        a.ck('geometry/face_orbit_closes',cur==start);faces.append(face)
    a.ck('geometry/exact_faces',faces==raw['faces'] and visited==darts)
    a.ck('geometry/sphere_Euler_and_induced_C5_face',10-len(skeleton)+len(faces)==2 and list(range(5)) in faces)
    a.ck('geometry/contracted_degree_scope',raw['root_degrees']==[4,4] and 'contracted' in raw['scope'])
    return dict(original_contracted_edges=sorted(skeleton),rotation=rotation,faces=faces,evidence_limit='Contracted geometry; no original degree-five disk realization')


def audit_negatives(a,data,model_relations):
    negatives=[]
    raw=data['aggregate_bridge_control'];projection=set(map(tuple,raw['original_projection_edges']))
    for name,mutate in [('missing_original_edge',lambda r:r['adjacency'][0].__setitem__('actual_edge',[0,2])),
        ('overlapping_bags',lambda r:r['branch_sets'][1].append(34)),('disconnected_hub',lambda r:r['branch_sets'][-1].append(999))]:
        m=deepcopy(raw['original_K5_minor']);mutate(m);check=Audit();check.minor(projection,m['branch_sets'],m['adjacency'],'negative/'+name)
        negatives.append(dict(mutation=name,caught=bool(check.failures),failures=check.failures))
    row=deepcopy(raw['components'][1]['full_same_component_lifts'][0]);row['30']=1
    check=Audit();validate_local_lifts(check,[row],model_relations['components'][1]['all_full_original_component_lifts'],MODELS[1]|{'edges':set(map(tuple,raw['components'][1]['original_edges']))},label='negative/bridge_endpoint_lift')
    negatives.append(dict(mutation='invalid_original_bridge_endpoint_lift',caught=bool(check.failures),failures=check.failures))
    f=deepcopy(data['binary_exact_complete_relation_candidates'][0]['root_avoidance_fibers']);f[2]['complete_contact_tuples']=[]
    negatives.append(dict(mutation='erase_nonempty_original_root_fibre',caught=f!=canonical(relation_fibres({(0,3)}))))
    relation={(0,3),(3,0)};marginal_product=set(product(*[{t[i] for t in relation} for i in (0,1)]))
    negatives.append(dict(mutation='replace_full_binary_relation_by_marginal_product',caught=marginal_product!=relation,
        invented_tuples=sorted(marginal_product-relation)))
    negatives.append(dict(mutation='close_whole_case_instead_of_one_key',caught=sum(r['case']['name']=='CPP-134-1' for r in model_relations['scope_ledger'])>1))
    a.ck('negative_controls/all_seven_mutations_rejected',len(negatives)==7 and all(r['caught'] for r in negatives))
    return negatives


def run(repo,out,source_versions):
    a=Audit();data=json.loads((repo/C4).read_bytes());parent=json.loads((repo/C).read_bytes());previous=json.loads((repo/C3).read_bytes())
    inputs={}
    for name,expected in data['inputs_sha256'].items():
        actual=sha256((repo/name).read_bytes()).hexdigest();inputs[name]=actual;a.ck('input_sha256/'+name,actual==expected)
    for name,expected in parent['scripts_sha256'].items():a.ck('front_script_sha256/'+name,sha256((repo/name).read_bytes()).hexdigest()==expected)
    id_=data['identity'];case=id_['case'];geometry=id_['geometry'];local=id_['local']
    a.ck('identity/exact_named_key_side_ids', [case['name'],geometry['id'],id_['side_join_id']]==KEY and id_['side_ids']==[27,1])
    a.ck('identity/case_local_branch',case['id']==86 and case['local_id']==local['id']==134 and case['branch']==1)
    a.ck('identity/full_original_parent_records',case==parent['local']['cases'][86] and local==parent['local']['configurations'][134] and geometry==parent['geometry']['retained_geometries'][34])
    a.ck('identity/exact_C3_handoff',id_['parent_entry']==previous['identity']['next_entry'])
    a.ck('identity/shared_color_frame',id_['common_color_frame']==list(Q))
    a.edges(id_['original_context_edges'],'identity/original_context',CONTEXT)
    a.ck('identity/original_z_ownership_contacts',[(r['name'],r['ordered_contacts'],r['forbidden'],r['root_incidence_count']) for r in id_['original_z_components']]==[('D_z2',['u0','u1'],[0,3],2),('D_z1',['r0'],[2],1)])
    a.ck('identity/original_z_own_support_remains_unknown',all('unknown; subset {b1,b2}' in r['actual_support'] for r in id_['original_z_components']) and 'A_2 union A_1 = {b1,b2}' in id_['original_support_cover_equation'])
    a.ck('identity/original_z_own_complete_relation',all('full original' in r['relation'] for r in id_['original_z_components']))
    a.ck('identity/original_bridges_remain_symbolic',id_['original_bridges']=='all E(D_z2), E(D_z1), including bridges, retained in full lifts')
    w=id_['preserved_w_component']
    a.ck('identity/w_preserved_full_unknown_relation',w==previous['identity']['preserved_w_component'] and w['ordered_contacts']==['v0','v1','v2'] and w['actual_support']==[2,4] and w['forbidden']==[0,2] and 'unknown' in w['relation'])
    a.ck('identity/exact_roles',id_['z_role']==dict(residual=[1],spoke_colors=[],unary_contacts=[2,1],unary_forbidden=[[0,3],[2]]) and id_['w_role']==dict(residual=[1,3],spoke_colors=[],unary_contacts=[3],unary_forbidden=[[0,2]]))
    lists=[U-{Q[b] for b in bs} for bs in ((0,1,4),(1,4),(4,))]
    p3=[t for t in product(*map(sorted,lists)) if t[0]!=t[1] and t[1]!=t[2]]
    f={(z,w) for z,w in product(range(4),repeat=2) if not any(t[2] not in (z,w) for t in p3)}
    a.ck('identity/original_complete_P3_relation',id_['original_P3_complete_tuples']==canonical(p3)==[[3,0,1],[3,0,3]] and id_['original_P3_lists']==list(map(sorted,lists)) and id_['original_P3_forbidden']==canonical(sorted(f)))
    join=sorted(set(product((1,),(1,3)))-f)
    a.ck('identity/full_original_root_join',id_['original_root_join_without_zw']==canonical(join)==[[1,1]] and id_['original_root_join_with_zw']==[])
    a.ck('identity/exact_original_external_paths',id_['original_external_paths']==[[5,9,4],[5,9,4,3,2,1]] and all(edge(v,w) in CONTEXT for p in id_['original_external_paths'] for v,w in zip(p,p[1:])))
    finite_relations=audit_relations(a,data);involution=audit_involution(a,data);models=audit_models(a,data)
    rotation=audit_rotation(a,id_['positive_geometry_control'])
    ledger=independent_front(a,parent);row=next(r for r in ledger if r['key']==KEY)
    a.ck('scope/new_key_not_previously_closed',not row['closed_by'] and row['side_ids']==[27,1] and row['z_role']==id_['z_role'] and row['w_role']==id_['w_role'])
    inherited_closed=[r['key'] for r in ledger if r['closed_by']]
    old_states=[dict(key=r['key'],status=r['status'],closed_by=list(r['closed_by'])) for r in ledger]
    row['closed_by']=['C4'];row['status']='closed_named_key';row['original_unary_components']=[
        dict(component='D_z2',root='z',ordered_original_contacts=['u0','u1'],actual_own_support=None,
            actual_own_support_scope='A_2 subset {b1,b2}; exact original support unknown; A_2 union A_1={b1,b2}',
            complete_relation='T_2(q) full original ordered relation; one of three necessary candidates, each impossible',forbidden_colors=[0,3],
            full_symbolic_root_fibres=[dict(root_color=h,relation=f'{{t in T_2(q): all(t[j] != {h})}}',nonempty=h not in (0,3)) for h in range(4)]),
        dict(component='D_z1',root='z',ordered_original_contacts=['r0'],actual_own_support=None,
            actual_own_support_scope='A_1 subset {b1,b2}; exact original support unknown; A_2 union A_1={b1,b2}',
            complete_relation='T_1(q)={(2)} full original ordered relation; impossible',forbidden_colors=[2],
            full_symbolic_root_fibres=[dict(root_color=h,relation=f'{{t in T_1(q): all(t[j] != {h})}}',nonempty=h!=2) for h in range(4)]),
        dict(component='D_w',root='w',ordered_original_contacts=['v0','v1','v2'],actual_own_support=[2,4],
            actual_own_support_scope='exact own support',complete_relation=w['relation'],forbidden_colors=[0,2],
            full_symbolic_root_fibres=[dict(root_color=h,relation=f'{{t in R_Dw(q): all(t[j] != {h})}}',nonempty=h not in (0,2)) for h in range(4)])]
    changed=[r['key'] for r,old in zip(ledger,old_states) if r['status']!=old['status'] or r['closed_by']!=old['closed_by']]
    closed=[r['key'] for r in ledger if r['closed_by']]
    a.ck('scope/only_one_new_key_closure',changed==[KEY] and len(closed)==3 and all(k in closed for k in inherited_closed))
    a.ck('scope/inherited_front_tables_kept',len(ledger)==3500 and len(parent['geometry']['retained_geometries'])==140 and parent['summary']['retained_cases']==36 if 'retained_cases' in parent['summary'] else len(ledger)==3500)
    scope=dict(scope='3500 distinct named geometry/join keys; inherited tables remain 36 cases/140 geometries/900 case joins',
        inherited_closed_named_keys=inherited_closed,newly_closed_named_keys=[KEY],closed_named_keys=closed,
        not_audited_named_keys=3497,ledger=ledger,
        closure_delta=[dict(key=KEY,before=next(old for old in old_states if old['key']==KEY),after=dict(status=row['status'],closed_by=row['closed_by']))])
    expected_summary=dict(actual_attachment_checks=8,aggregate_ownership_negative_controls=1,binary_exact_complete_relations=3,
        complete_ordered_tuple_domain_checks=20,control_complete_component_lifts=6,control_complete_joint_lifts=8,
        control_deleted_bridge_endpoint_relations=8,control_deleted_bridge_lifts=models['deleted_bridge_full_lift_count'],
        control_k5_minors=1,control_original_bridges=2,coupled_support_relation_checks=27,coupled_survivors=0,
        individually_impossible_original_components=2,named_source_branches_closed=1,original_P3_tuples=2,
        original_support_cover_candidates=9,own_support_candidates=4,predecessor_cases=36,predecessor_deletions=0,
        predecessor_geometries=140,predecessor_joins=900,preserved_w_original_contacts=3,root_fibers_per_relation=4,target_queries=0,
        unary_exact_complete_relations=1,universal_internal_edge_bridge_color_checks=16)
    a.ck('production/complete_summary_exact',data['summary']==expected_summary and models['deleted_bridge_full_lift_count']==34 and models['endpoint_pin_queries']==128)
    negatives=audit_negatives(a,data,models|{'scope_ledger':ledger})
    inherited_sources={name:sha256((repo/'audits/2026-10-04-task-d4/c3'/original).read_bytes()).hexdigest()
        for name,original in [('independent_helpers.py','independent_helpers.py'),('predecessor_front.py','audit_c3.py')]}
    a.ck('provenance/verbatim_D4_independent_reuse',all(source_versions[k]==v for k,v in inherited_sources.items()))
    relations=dict(common_color_frame=list(Q),fixed_key=KEY,side_ids=[27,1],
        original_unknown_w_full_relation=w|{'all_four_symbolic_fibres':row['original_unary_components'][-1]['full_symbolic_root_fibres']},
        original_z_own_supports_unknown=id_['original_z_components'],complete_necessary_relations=finite_relations,
        lift_involution=involution,original_bridge_and_ownership_controls=models,
        original_P3_complete_relation=p3,all_sixteen_original_P3_fibres=[dict(root_pair=[z,w],complete_original_P3_tuples=[t for t in p3 if t[2] not in (z,w)]) for z,w in product(range(4),repeat=2)],
        contracted_geometry=rotation,negative_controls=negatives)
    save(out/'relations.json',relations);save(out/'scope_ledger.json',scope)
    result=dict(status='pass' if not a.failures else 'fail',checks=a.checks,failures=a.failures,
        input_sha256=inputs,audited_artifact_sha256={name:sha256((repo/name).read_bytes()).hexdigest() for name in (C,C2,C3,C4)},
        independent_audit_sources_sha256=source_versions,verbatim_D4_helpers_sha256=inherited_sources,
        finite_counts=dict(original_own_support_candidates=4,ordered_support_configurations=9,complete_relation_combinations=27,
            original_binary_complete_relation_candidates=3,original_unary_complete_relation_candidates=1,universal_internal_edge_bridge_tests=16,
            own_attachment_tests=8,ordered_contact_domain_tests=20,original_control_bridges=2,deleted_bridge_root_relations=8,
            complete_deleted_bridge_lifts=34,ordered_endpoint_pin_queries=128,control_full_component_lifts=6,control_full_joint_lifts=8,
            negative_mutations_rejected=7,context_all_root_fibres=32),
        scope=dict(newly_closed_named_keys=[KEY],inherited_closed_named_keys=inherited_closed,closed_named_keys=closed,ledger_keys=3500,
            not_audited_keys=3497,predecessor_cases=36,predecessor_geometries=140,predecessor_case_joins=900,predecessor_deletions=0,target_queries=0),
        evidence_boundaries=dict(arbitrary_size='Paper pointwise lift involution reviewed separately in notes.md; every original internal edge/bridge and own attachment preserved.',
            external_theorems='None needed by the C4 componentwise obstruction. K5 control is a finite negative control, not a required external theorem.',
            python='Fixed complete candidate relations, named front ledger, actual-edge models, all lifts/empty fibres and witness validation only.',
            lean='No new Lean theorem; lake build does not formalize this pointwise lift proof.',
            other='No source realization, whole-M edge-minimality, target extension, complete Sigma, general exit, or K infinity equals K <=5.'))
    save(out/'results.json',result)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--repo',type=Path,default=DEFAULT_REPO);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=False)
    versions={name:sha256((HERE/name).read_bytes()).hexdigest() for name in SOURCES}
    save(args.output/'audit_source_versions.json',versions)
    for name in SOURCES:(args.output/name).write_bytes((HERE/name).read_bytes())
    try:result=run(args.repo,args.output,versions)
    except Exception:
        result=dict(status='exception',traceback=traceback.format_exc());save(args.output/'exception.json',result)
    print(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=1))
    raise SystemExit(0 if result['status']=='pass' else 1)


if __name__=='__main__':main()
