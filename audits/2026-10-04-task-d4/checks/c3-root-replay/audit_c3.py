#!/usr/bin/env python3
"""D4 independent C3 audit. Reads snapshot data; imports no production code.

Each invocation must have a fresh output directory. Full named relations,
including empty root fibres and coloring lifts, are written to that directory.
The arbitrary-size proof is reviewed in notes.md, not proved by this program.
"""
import argparse
from copy import deepcopy
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path
import traceback

from independent_helpers import Audit, edge, connected, CONTEXT, TRIANGLE, PROJECTION, ALIASES

HERE = Path(__file__).resolve().parent
SNAPSHOT = HERE.parent / 'snapshot'
Q, U = (0, 1, 0, 1, 2), set(range(4))
CONTACTS, P3 = (10, 11, 12), (7, 8, 9)
C = 'artifacts/c5_mixed_p3_common_endpoint/observations.json'
C2 = 'artifacts/c5_mixed_p3_one_color_ternary_unary/observations.json'
C3 = 'artifacts/c5_mixed_p3_two_frame_ternary_unary/observations.json'

def canonical(value):
    return json.loads(json.dumps(value, sort_keys=True))

def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=1) + '\n')

def solve(vertices, edges, pins):
    """Enumerate all colorings by dynamic minimum-remaining-values search."""
    vertices, edges = set(vertices), set(edges)
    if set(pins) - vertices or any(a not in vertices or b not in vertices for a,b in edges):
        raise ValueError('coloring graph domain mismatch')
    if any(a in pins and b in pins and pins[a] == pins[b] for a,b in edges):
        return []
    neighbors = {v: {b if a == v else a for a,b in edges if v in (a,b)} for v in vertices}
    out, col = [], dict(pins)
    def visit():
        if len(col) == len(vertices):
            out.append(dict(col)); return
        available = {v: U - {col[w] for w in neighbors[v] if w in col} for v in vertices - col.keys()}
        v = min(available, key=lambda v: (len(available[v]), -len(neighbors[v]), v))
        for color in sorted(available[v]):
            col[v] = color; visit(); del col[v]
    visit()
    return out

def fibres(vertices, edges, contacts=CONTACTS):
    """All 16 same-graph root fibres, including empties, with one lift per tuple."""
    result = []
    for z,w in product(range(4), repeat=2):
        pins = dict(enumerate(Q)) | {5:z, 6:w}
        cols = solve(set(range(7)) | set(vertices), edges, pins)
        lifts = {}
        for col in cols:
            lifts.setdefault(tuple(col[v] for v in contacts), col)
        result.append(dict(root_pair=[z,w], coloring_count=len(cols),
                           complete_contact_tuples=[list(t) for t in sorted(lifts)],
                           lifts=[dict(ordered_contact_tuple=list(t), coloring=lifts[t]) for t in sorted(lifts)]))
    return result

def contact_relation(vertices, edges):
    boundary = {e for e in edges if 5 not in e and 6 not in e}
    cols = solve(set(range(5)) | set(vertices), boundary, dict(enumerate(Q)))
    lifts = {}
    for col in cols:
        lifts.setdefault(tuple(col[v] for v in CONTACTS), col)
    return [list(t) for t in sorted(lifts)], [dict(ordered_contact_tuple=list(t), coloring=lifts[t]) for t in sorted(lifts)]

def subsets(xs):
    return [set(c) for n in range(len(xs)+1) for c in combinations(sorted(xs), n)]

def side_roles():
    roles = []
    partitions = {0:[()], 1:[(1,)], 2:[(2,),(1,1)], 3:[(3,),(2,1),(1,1,1)]}
    for spokes in subsets({0,1,2}):
        if len(spokes) > 3: continue
        for counts in partitions[3-len(spokes)]:
            choices = [[s for s in subsets(U) if 1 <= len(s) <= n] for n in counts]
            for fs in product(*choices):
                union = set().union(*fs)
                if union & spokes or sum(map(len,fs)) != len(union): continue
                residual = U - spokes - union
                if not 1 <= len(residual) <= 2: continue
                roles.append(dict(spoke_colors=sorted(spokes), unary_contacts=list(counts),
                                  unary_forbidden=[sorted(f) for f in fs], residual=sorted(residual)))
    return roles

def minimal_joins(roles, forbidden):
    out = []
    for zi,wi in product(range(len(roles)), repeat=2):
        zr,wr = roles[zi], roles[wi]
        ez,ew = set(zr['residual']), set(wr['residual'])
        square = set(product(ez,ew)); diag = {(c,c) for c in U}
        if square - forbidden - diag or not ((square & diag)-forbidden) or not (square-diag): continue
        release_z = zr['unary_forbidden'] + [[c] for c in zr['spoke_colors']]
        release_w = wr['unary_forbidden'] + [[c] for c in wr['spoke_colors']]
        if any(not(set(product(released,ew))-diag-forbidden) for released in release_z): continue
        if any(not(set(product(ez,released))-diag-forbidden) for released in release_w): continue
        out.append([zi,wi])
    return out

def independent_front(a, parent):
    roles = side_roles()
    a.ck('front/complete_named_side_roles', roles == parent['local']['side_roles'])
    locals_, cases, joins_a = [], [], {}
    for supports in product(combinations(range(5),3), combinations(range(5),2), combinations(range(5),1)):
        lists = [U-{Q[v] for v in s} for s in supports]
        tuples = [t for t in product(*map(sorted,lists)) if t[0]!=t[1] and t[1]!=t[2]]
        forbidden = {(z,w) for z,w in product(range(4),repeat=2) if not any(t[2] not in (z,w) for t in tuples)}
        local = dict(id=len(locals_), actual_supports=[list(s) for s in supports],
                     complete_triples=[list(t) for t in tuples], lists=[sorted(s) for s in lists])
        stored = parent['local']['configurations'][local['id']]
        a.ck(f"front/local_{local['id']}/named_relation", all(local[k]==stored[k] for k in local))
        a.ck(f"front/local_{local['id']}/forbidden_pairs", stored['forbidden_pair_mask']==sum(1<<(4*z+w) for z,w in forbidden))
        if forbidden:
            d = tuples[0][1]; c, = {Q[v] for v in supports[2]}; ac, = U-{c,d,3}
            joins = minimal_joins(roles,forbidden)
            local.update(a=ac,c=c,d=d,forbidden=sorted(forbidden))
            a.ck(f"front/local_{local['id']}/complete_joins", len(joins)==125 and joins==parent['local']['joins_by_a'][str(ac)])
            joins_a[str(ac)] = joins
            expected = (((ac,3),(ac,3)),((ac,),(ac,3)),((3,),(ac,3)),((ac,3),(ac,)),((ac,3),(3,)))
            for branch,(ez,ew) in enumerate(expected):
                ids=[j for j,(zi,wi) in enumerate(joins) if roles[zi]['residual']==list(ez) and roles[wi]['residual']==list(ew)]
                case=dict(id=len(cases), name=f"CPP-{local['id']:03d}-{branch}",local_id=local['id'],branch=branch,
                          z_residual=list(ez),w_residual=list(ew),side_join_ids=ids)
                a.ck(f"front/case_{case['id']}",case==parent['local']['cases'][case['id']] and len(ids)==25)
                cases.append(case)
        locals_.append(local)
    a.ck('front/500_local_configurations_560_cases',len(locals_)==500 and len(cases)==560)
    perms=list(permutations(range(4)))
    support_options=[list(s) for n in range(1,6) for s in combinations(range(5),n)]
    orders=((2,0,1),(2,1,0),(0,1,2),(1,0,2)); names=('A_z','A_w','S2')
    geometries=[]; retained_cases=set()
    for case in cases:
        local=locals_[case['local_id']]; s0,s1,s2=local['actual_supports']; sectors=[]
        for anchor in s0:
            end=anchor+min((v-anchor)%5 for v in s0 if v!=anchor)
            t1=sorted(anchor+(v-anchor)%5 for v in s1); s=anchor+(s2[0]-anchor)%5
            if max(t1)>end or s>end:continue
            for child,(left,right) in enumerate(zip([anchor]+t1,t1+[end])):
                if left<=s<=right:
                    sectors.append(dict(anchor=anchor,I=[anchor,end],S1_lifts=t1,child=child,J=[left,right],S2_lift=s))
        choices=[]
        for residual in (case['z_residual'],case['w_residual']):
            admissible=[]
            for support in support_options:
                colors={Q[v] for v in support}
                if not any(all(p[c]==c for c in colors) and {p[c] for c in residual}!=set(residual) for p in perms):
                    admissible.append(support)
            choices.append(admissible)
        for az,aw in product(*choices):
            for sector in sectors:
                anchor=sector['anchor']; blocks=[sorted(anchor+(v-anchor)%5 for v in side) for side in (az,aw,[sector['S2_lift']%5])]
                left,right=sector['J']
                if any(min(t)<left or max(t)>right for t in blocks):continue
                matched=next((order for order in orders if all(max(blocks[i])<=min(blocks[j]) for i,j in zip(order,order[1:]))),None)
                if matched is None:continue
                geometry=dict(id=len(geometries),case_id=case['id'],case_name=case['name'],local_id=local['id'],
                    actual_side_supports=[az,aw],**sector,block_lifts=blocks,named_order=[names[i] for i in matched])
                a.ck(f"front/geometry_{geometry['id']}/all_named_fields",geometry==parent['geometry']['retained_geometries'][geometry['id']])
                geometries.append(geometry);retained_cases.add(case['id']);break
    a.ck('front/preserved_36_cases_140_geometries_900_case_joins',len(retained_cases)==36 and len(geometries)==140 and sum(len(cases[c]['side_join_ids']) for c in retained_cases)==900)
    ledger=[]
    for g in geometries:
        case=cases[g['case_id']];local=locals_[g['local_id']]
        p3_tuples=local['complete_triples']
        p3_fibres=[dict(root_pair=[z,w],complete_original_P3_tuples=[t for t in p3_tuples if t[2] not in (z,w)],
                       full_P3_lifts=[dict(zip(['x0','x1','x2'],t)) for t in p3_tuples if t[2] not in (z,w)]) for z,w in product(range(4),repeat=2)]
        for join_id in case['side_join_ids']:
            side_ids=joins_a[str(local['a'])][join_id];zr,wr=[roles[i] for i in side_ids]
            key=[case['name'],g['id'],join_id];closed=[]
            if key==['CPP-134-1',30,20]:closed=['C2']
            if key==['CPP-134-1',34,20]:closed=['C3']
            components=[]
            for root,role,support in zip(('z','w'),(zr,wr),g['actual_side_supports']):
                for i,(n,f) in enumerate(zip(role['unary_contacts'],role['unary_forbidden'])):
                    exact=len(role['unary_contacts'])==1 and not role['spoke_colors']
                    name=f'D_{root}_{i}'
                    components.append(dict(component=name,root=root,ordered_original_contacts=[f'{root}_u{i}_{j}' for j in range(n)],
                         actual_own_support=support if exact else None,actual_own_support_scope='exact own support' if exact else 'unknown; whole-side support cannot be assigned to this component',
                         complete_relation=f'R_{name}(q) subset U^{n}; original same-source relation unknown',forbidden_colors=f,
                         full_symbolic_root_fibres=[dict(root_color=h,relation=f'{{t in R_{name}(q): all(t[j] != {h})}}',nonempty=h not in f) for h in range(4)]))
            joint=sorted(set(product(zr['residual'],wr['residual']))-{tuple(p) for p in local['forbidden']})
            ledger.append(dict(key=key,status='closed_named_key' if closed else 'not_audited_by_C2_C3',closed_by=closed,
                 common_color_frame=list(Q),original_components=dict(P3='x0-x1-x2',root_masks=[0,0,3],ordered_vertices=['x0','x1','x2']),
                 original_P3_actual_supports=local['actual_supports'],original_P3_complete_tuples=p3_tuples,original_P3_forbidden_pairs=local['forbidden'],
                 complete_P3_root_fibres=p3_fibres,case=case,geometry=g,side_ids=side_ids,z_role=zr,w_role=wr,original_unary_components=components,
                 complete_role_join_without_zw=joint,complete_role_join_with_zw=[list(p) for p in joint if p[0]!=p[1]],
                 source_provenance=dict(artifact=C,local_id=local['id'],case_id=case['id'],geometry_id=g['id'],side_join_id=join_id),
                 evidence_limit='necessary named skeleton and color-role join; no disk realization, target extension, or full Sigma'))
    a.ck('ledger/3500_distinct_full_named_keys',len(ledger)==3500 and len({tuple(r['key']) for r in ledger})==3500)
    a.ck('ledger/exactly_two_closed_keys',{tuple(r['key']) for r in ledger if r['closed_by']}=={('CPP-134-1',30,20),('CPP-134-1',34,20)})
    return ledger

def audit_model(a, record, n):
    label=f'N{n}';cycle=list(range(20,20+n));c,va,vb=cycle[-1],cycle[0],cycle[1]
    vertices=cycle+list(CONTACTS)
    attachments={v:[1,2] for v in cycle[:-1]} | {c:[2],10:[5],11:[1,5],12:[1,5]}
    internal={edge(v,w) for v,w in zip(cycle,cycle[1:]+cycle[:1])}|{edge(v,w) for v,w in combinations(CONTACTS,2)}|{edge(c,10)}
    expected=internal|{edge(v,w) for v,ws in attachments.items() for w in ws}
    edges=a.edges(record['edges'],label+'/all_original_edges',expected)
    a.ck(label+'/named_vertices_contacts_cycle_cut_bridge',set(record['vertices'])==set(vertices) and record['ordered_contacts']==list(CONTACTS) and record['leaf_cycle']==cycle and record['cut_vertex']==c and record['bridge']==list(edge(c,10)))
    a.ck(label+'/exact_attachments',{int(v):ws for v,ws in record['actual_attachments'].items()}==attachments)
    a.ck(label+'/original_degree_four',all(sum(v in e for e in edges)==4 for v in vertices) and record['original_vertex_degrees']=={str(v):4 for v in vertices})
    a.ck(label+'/actual_own_support',[1,2]==record['actual_support']==sorted({w for ws in attachments.values() for w in ws if w<5}))
    tuples,lifts=contact_relation(vertices,edges)
    a.ck(label+'/complete_relation',tuples==record['complete_contact_tuples']==[list(t) for t in sorted(permutations((0,2,3)))])
    a.ck(label+'/stored_contact_lifts_exact_tuple_coverage',len(record['tuple_witnesses'])==6 and sorted(r['ordered_contact_tuple'] for r in record['tuple_witnesses'])==tuples)
    for i,witness in enumerate(record['tuple_witnesses']):
        col=a.coloring(witness['coloring'],vertices,{e for e in edges if e[0]>=7 and e[1]>=7},{},f'{label}/stored_contact_lift_{i}')
        if col:
            a.ck(f'{label}/stored_contact_lift_{i}/tuple_and_frame_attachments',list(map(col.get,CONTACTS))==witness['ordered_contact_tuple'] and all(col[v]!=Q[w] for v,ws in attachments.items() for w in ws if w<5))
    full=fibres(vertices,edges);relation=[r['root_pair'] for r in full if r['complete_contact_tuples']]
    a.ck(label+'/complete_root_relation',relation==record['root_pair_relation']==[[1,w] for w in range(4)])
    for pin in record['intact_pins']:
        h=pin['z'];computed=next(r for r in full if r['root_pair']==[h,1])
        a.ck(f'{label}/intact_{h}/empty',(pin['coloring'] is None)==(not computed['complete_contact_tuples']))
        if pin['coloring'] is not None:a.coloring(pin['coloring'],set(range(7))|set(vertices),edges,dict(enumerate(Q))|{5:h,6:1},f'{label}/intact_{h}/lift')
    bridge=edge(c,10);bridge_rows=[]
    a.ck(label+'/three_bridge_pins',{r['z'] for r in record['deleted_bridge_endpoint_controls']}=={0,2,3} and len(record['deleted_bridge_endpoint_controls'])==3)
    for control in record['deleted_bridge_endpoint_controls']:
        h=control['z'];pin_rows=[]
        for left,right in product(range(4),repeat=2):
            pins=dict(enumerate(Q))|{5:h,6:1,c:left,10:right}
            cols=solve(set(range(7))|set(vertices),edges-{bridge},pins)
            pin_rows.append(dict(endpoint_colors=[left,right],coloring_count=len(cols),full_same_graph_lifts=cols))
        endpoint_relation=[r['endpoint_colors'] for r in pin_rows if r['coloring_count']]
        a.ck(f'{label}/bridge_z{h}/complete_same_graph_relation',endpoint_relation==control['complete_endpoint_relation']==[[1,1]])
        a.ck(f'{label}/bridge_z{h}/identity',control['w']==1 and control['ordered_endpoints']==[c,10] and control['deleted_edge']==list(bridge))
        for i,lift in enumerate(control['full_same_deleted_graph_lifts']):
            a.coloring(lift['coloring'],set(range(7))|set(vertices),edges-{bridge},dict(enumerate(Q))|{5:h,6:1,c:lift['endpoint_colors'][0],10:lift['endpoint_colors'][1]},f'{label}/bridge_z{h}/stored_lift_{i}')
        a.ck(f'{label}/bridge_z{h}/lift_cover',[r['endpoint_colors'] for r in control['full_same_deleted_graph_lifts']]==endpoint_relation)
        bridge_rows.append(dict(z=h,w=1,ordered_endpoints=[c,10],all_16_endpoint_pin_fibres=pin_rows,complete_endpoint_relation=endpoint_relation))
    projection=a.edges(record['original_context_projection_edges'],label+'/preserved_original_context_projection',CONTEXT|edges)
    a.ck(label+'/original_context_retained',record['original_context_edges_retained'] is True)
    a.ck(label+'/source_degrees_and_symbolic_w',sum(5 in e for e in projection)==5 and sum(6 in e for e in projection)==2 and all(sum(v in e for e in projection)==4 for v in (*P3,*vertices)))
    deletions=[]
    a.ck(label+'/exact_all_deletion_edges',len(record['deletions'])==len(edges) and {tuple(r['deleted_edge']) for r in record['deletions']}==edges)
    for row in record['deletions']:
        deleted=tuple(row['deleted_edge']);stem=f'{label}/delete_{deleted[0]}_{deleted[1]}'
        after=fibres(vertices,edges-{deleted});root_relation=[r['root_pair'] for r in after if r['complete_contact_tuples']]
        a.ck(stem+'/complete_U2_root_relation',root_relation==row['root_pair_relation_after']==[list(p) for p in product(range(4),repeat=2)])
        a.ck(stem+'/four_local_pins',len(row['local_witnesses'])==4 and {r['z'] for r in row['local_witnesses']}==U)
        for witness in row['local_witnesses']:
            h=witness['z'];col=a.coloring(witness['coloring'],set(range(7))|set(vertices),edges-{deleted},dict(enumerate(Q))|{5:h,6:1},stem+f'/stored_pin_{h}')
            if h in (0,2,3) and col:a.ck(stem+f'/deleted_ends_equal_{h}',col[deleted[0]]==col[deleted[1]])
        pins=dict(enumerate(Q))|{5:0,6:1};partial_cols=solve(set(range(10))|set(vertices),projection-{deleted},pins)
        col=a.coloring(row['original_context_partial_witness'],set(range(10))|set(vertices),projection-{deleted},pins,stem+'/partial_context')
        if col:a.ck(stem+'/original_partial_P3_and_deleted_ends',tuple(col[v] for v in P3)==(3,0,3) and col[deleted[0]]==col[deleted[1]])
        a.ck(stem+'/partial_evidence_limit','not enumerated' in row['w_completion'])
        after_tuples,after_lifts=contact_relation(vertices,edges-{deleted})
        deletions.append(dict(deleted_edge=list(deleted),complete_contact_relation=after_tuples,contact_lifts=after_lifts,all_16_root_fibres=after,
                              original_context_partial_coloring_count=len(partial_cols),original_context_partial_lifts=partial_cols,
                              evidence_limit='D_w original relation unknown; no whole-M edge minimality certificate'))
    groups=[{va},{vb},{1},{2},(set(vertices)-{va,vb})|{5,9,0,3,4}]
    a.ck(label+'/five_exact_named_bags',record['branch_sets']==[sorted(g) for g in groups] and record['branch_set_names']==['a','b','b1','b2','X'])
    a.minor(projection,record['branch_sets'],record['adjacency'],label+'/original_K5_minor')
    return dict(cycle_length=n,vertices=vertices,edges=sorted(edges),ordered_contacts=list(CONTACTS),actual_attachments=attachments,
                complete_contact_tuples=tuples,tuple_lifts=lifts,all_16_intact_root_fibres=full,deleted_bridge_controls=bridge_rows,
                deletions=deletions,original_K5_bags=record['branch_sets'],ten_original_edge_adjacencies=record['adjacency'])

def run(source,out):
    a=Audit();data=json.loads((source/C3).read_bytes());parent=json.loads((source/C).read_bytes());previous=json.loads((source/C2).read_bytes())
    hashes={}
    for name,expected in data['inputs_sha256'].items():
        actual=sha256((source/name).read_bytes()).hexdigest();hashes[name]=actual;a.ck('input_sha256/'+name,actual==expected)
    for name,expected in parent['scripts_sha256'].items():a.ck('front_script_sha256/'+name,sha256((source/name).read_bytes()).hexdigest()==expected)
    identity=data['identity'];g=identity['geometry'];local=identity['local'];case=identity['case']
    a.ck('identity/exact_original_predecessor_handoff',g==previous['identity']['next_entry']['geometry'])
    a.ck('identity/exact_named_scope',(case['name'],g['id'],identity['side_join_id'])==('CPP-134-1',34,20) and (case['id'],local['id'],case['branch'])==(86,134,1))
    a.ck('identity/full_named_parent_records',g==parent['geometry']['retained_geometries'][34] and case==parent['local']['cases'][86] and local==parent['local']['configurations'][134])
    a.ck('identity/shared_frame',identity['common_color_frame']==list(Q) and {int(v):n for v,n in identity['aliases'].items()}==ALIASES)
    a.edges(identity['original_context_edges'],'identity/original_context',CONTEXT)
    a.ck('identity/three_contacts_each_no_spokes',identity['side_ids']==[8,1] and all(identity[k]['unary_contacts']==[3] and not identity[k]['spoke_colors'] for k in ('z_role','w_role')))
    a.ck('identity/exact_own_support_forbidden_unknown_full_relations',identity['preserved_z_component']['actual_support']==[1,2] and identity['preserved_z_component']['forbidden']==[0,2,3] and identity['preserved_w_component']['actual_support']==[2,4] and identity['preserved_w_component']['forbidden']==[0,2] and all('unknown' in identity[k]['relation'] for k in ('preserved_z_component','preserved_w_component')))
    rows=data['local_degree_lists'];a.ck('lists/eight_original_identity_types',len(rows)==8 and {(r['original_z_contact'],r['original_b1_attachment'],r['original_b2_attachment']) for r in rows}==set(product((False,True),repeat=3)))
    retained=0;type_rows=[]
    for i,row in enumerate(rows):
        p,s1,s2=[int(row[k]) for k in ('original_z_contact','original_b1_attachment','original_b2_attachment')];degree=4-p-s1-s2
        a.ck(f'lists/type_{i}/degree',row['degree_in_D']==degree)
        a.ck(f'lists/type_{i}/four_pins',len(row['pinned_lists'])==4 and {r['z'] for r in row['pinned_lists']}==U)
        for pin in row['pinned_lists']:
            h=pin['z'];external=([h] if p else [])+([1] if s1 else [])+([0] if s2 else []);allowed=U-set(external)
            a.ck(f'lists/type_{i}/pin_{h}',pin['external_colors']==external and pin['list']==sorted(allowed) and pin['slack']==len(allowed)-degree==int(p and ((h==0 and s2) or (h==1 and s1))))
        keep=not(p and s2);kind='T' if keep and degree==2 and p else 'N' if keep and degree==2 else None
        a.ck(f'lists/type_{i}/retained_identity',row['compatible_with_pin_zero_tightness']==keep and row['private_degree_two_type']==kind)
        if keep:retained+=1;a.ck(f'lists/type_{i}/retained_min_degree_two',degree>=2)
        type_rows.append(dict(p=p,s1=s1,s2=s2,degree=degree,retained=keep,private_type=kind,pinned_lists=row['pinned_lists']))
    a.ck('lists/six_retained_two_slack_excluded',retained==6)
    for pin in data['leaf_palette_controls']['pins']:
        h=pin['z'];a.ck(f'leaf/palette_{h}',pin['private_type_palettes']=={'T':sorted(U-{1,h}),'N':[2,3]} and pin['equal_palette_pairs']==[['T','T'],['N','N']])
    models=[audit_model(a,r,n) for r,n in zip(data['n_leaf_controls']['records'],(3,5,7,9))]
    a.ck('N/exact_four_models',[r['cycle_length'] for r in data['n_leaf_controls']['records']]==[3,5,7,9])
    a.ck('N/exact_derived_24_tuples_104_deleted_edges_416_local_104_partial',
         sum(len(r['complete_contact_tuples']) for r in data['n_leaf_controls']['records'])==24 and
         sum(len(r['deletions']) for r in data['n_leaf_controls']['records'])==104 and
         sum(len(e['local_witnesses']) for r in data['n_leaf_controls']['records'] for e in r['deletions'])==416 and
         sum('original_context_partial_witness' in e for r in data['n_leaf_controls']['records'] for e in r['deletions'])==104)
    tether_ids=[]
    for i,r in enumerate(data['k4_tether_controls']['records']):
        label=f'K4_route_{i}';paths=r['tethers'];clique={edge(v,w) for v,w in combinations((30,31,32,33),2)};tails=set()
        a.ck(label+'/four_paths',len(paths)==4)
        for j,p in enumerate(paths):
            a.ck(label+f'/path_{j}/named_original_endpoints',p[0]==30+j and p[-1] in (1,2,5) and p[1:-1] in ([],[50+j]) and len(p)==len(set(p)))
            tails|={edge(v,w) for v,w in zip(p,p[1:])}
        a.ck(label+'/common_subdivision_length',tuple(map(len,paths)) in ((2,)*4,(3,)*4))
        for j,k in combinations(range(4),2):a.ck(label+f'/paths_{j}_{k}/disjoint_before_hub',not(set(paths[j][:-1])&set(paths[k][:-1])))
        edges=a.edges(r['edges'],label+'/edges',CONTEXT|clique|tails)
        hub={0,1,2,3,4,5,9}|set().union(*(set(p[1:-1]) for p in paths));groups=[{30},{31},{32},{33},hub]
        a.ck(label+'/exact_five_bags',r['branch_sets']==[sorted(s) for s in groups])
        a.minor(edges,r['branch_sets'],r['adjacency'],label+'/minor');tether_ids.append((tuple(p[-1] for p in paths),tuple(map(len,paths))))
    expected_ids={(ends,shape) for ends in product((1,2,5),repeat=4) for shape in ((2,)*4,(3,)*4)}
    a.ck('K4/exact_162_original_route_controls',len(tether_ids)==162 and set(tether_ids)==expected_ids)
    tri=data['conditional_triangle'];a.edges(tri['edges'],'conditional_triangle/original_edges',TRIANGLE)
    a.ck('conditional_triangle/exact_six_tuples',tri['complete_contact_tuples']==[list(t) for t in sorted(permutations((0,2,3)))])
    a.ck('conditional_triangle/support_mismatch',tri['conditional_reduct_actual_support']==[1] and tri['required_original_actual_support']==[1,2] and tri['compatible_with_required_original_support'] is False)
    tri_fibres=fibres(CONTACTS,TRIANGLE);tri_deletions=[]
    a.ck('conditional_triangle/nine_deletions',len(tri['deletions'])==9 and {tuple(r['deleted_edge']) for r in tri['deletions']}==TRIANGLE)
    for row in tri['deletions']:
        e=tuple(row['deleted_edge']);stem=f'conditional_triangle/delete_{e[0]}_{e[1]}';after=fibres(CONTACTS,TRIANGLE-{e})
        a.ck(stem+'/complete_U2_fibres',all(r['complete_contact_tuples'] for r in after))
        a.ck(stem+'/four_stored_pins',len(row['local_witnesses'])==4 and {r['z'] for r in row['local_witnesses']}==U)
        for w in row['local_witnesses']:
            h=w['z'];col=a.coloring(w['coloring'],set(range(7))|set(CONTACTS),TRIANGLE-{e},dict(enumerate(Q))|{5:h,6:1},stem+f'/stored_local_{h}')
            if h in (0,2,3) and col:a.ck(stem+f'/equal_ends_{h}',col[e[0]]==col[e[1]])
        col=a.coloring(row['original_context_witness'],range(13),PROJECTION-{e},dict(enumerate(Q))|{5:0,6:1},stem+'/stored_partial')
        if col:a.ck(stem+'/partial_P3',tuple(col[v] for v in P3)==(3,0,3) and col[e[0]]==col[e[1]])
        a.ck(stem+'/missing_w_limit','not enumerated' in row['missing_w_completion'])
        tri_deletions.append(dict(deleted_edge=list(e),all_16_root_fibres=after))
    a.edges(tri['original_source_projection_edges'],'conditional_triangle/context_projection',PROJECTION)
    subdivisions=[a.subdivision(r,PROJECTION,f'conditional_triangle/K5_{i}') for i,r in enumerate(data['conditional_triangle_k5_subdivisions'])]
    a.ck('conditional_triangle/two_original_outer_routes',len(subdivisions)==2)
    rotation=identity['positive_geometry_control'];skeleton=CONTEXT|{edge(root,b) for root,bs in zip((5,6),([1,2],[2,4])) for b in bs}
    rot={int(v):ws for v,ws in rotation['rotation'].items()};darts={(v,w) for e in skeleton for v,w in (e,e[::-1])};visited=set();faces=[]
    for v in range(10):a.ck(f'rotation/vertex_{v}/full_neighbor_cycle',len(rot[v])==len(set(rot[v])) and set(rot[v])=={w if x==v else x for x,w in skeleton if v in (x,w)})
    for start in sorted(darts):
        if start in visited:continue
        cur=start;face=[]
        while cur not in visited:
            visited.add(cur);v,w=cur;face.append(v);ns=rot[w];cur=(w,ns[(ns.index(v)-1)%len(ns)])
        a.ck('rotation/facial_orbit_closed',cur==start);faces.append(face)
    a.ck('rotation/exact_faces_and_disk_Euler',faces==rotation['faces'] and visited==darts and 10-len(skeleton)+len(faces)==2 and list(range(5)) in faces)
    a.ck('rotation/contracted_root_degree_only',rotation['root_degrees']==[4,4] and 'contracted' in rotation['scope'])
    ledger=independent_front(a,parent)
    next_=identity['next_entry'];next_key=['CPP-134-1',34,60];next_row=next(r for r in ledger if r['key']==next_key)
    a.ck('stop/exact_next_named_unaccepted_split',next_['side_ids']==next_row['side_ids']==[27,1] and next_['z_role']==next_row['z_role'] and next_['w_role']==next_row['w_role'] and next_row['status']=='not_audited_by_C2_C3')
    a.ck('scope/one_new_branch_no_target_no_table_deletion',data['summary']['named_source_branches_closed']==1 and data['summary']['target_queries']==0 and data['summary']['predecessor_deletions']==0)
    negatives=[]
    for name,mutate in [('missing_ten_pair_edge',lambda r:r['adjacency'][0].__setitem__('actual_edge',[0,2])),('overlapping_bags',lambda r:r['branch_sets'][1].append(r['branch_sets'][0][0])),('disconnected_X',lambda r:r['branch_sets'][-1].append(999))]:
        r=deepcopy(data['n_leaf_controls']['records'][0]);mutate(r);check=Audit();check.minor(set(map(tuple,r['original_context_projection_edges'])),r['branch_sets'],r['adjacency'],'negative/'+name)
        negatives.append(dict(mutation=name,caught=bool(check.failures),failures=check.failures))
    a.ck('negative_controls/all_bad_minors_rejected',all(r['caught'] for r in negatives))
    for key,expected in [('local_vertex_types',8),('pinned_list_checks',32),('n_leaf_controls',4),('n_leaf_deleted_edges',104),('n_leaf_local_deletion_colorings',416),('n_leaf_original_context_partial_colorings',104),('deleted_bridge_endpoint_relations',12),('k4_tether_controls',162),('conditional_triangle_deleted_edges',9),('conditional_triangle_local_deletion_colorings',36)]:a.ck('production_summary/'+key,data['summary'][key]==expected)
    save(out/'scope_ledger.json',dict(scope='3500 distinct geometry/join keys; source catalog remains 36 cases/140 geometries/900 case joins',closed_named_keys=[r['key'] for r in ledger if r['closed_by']],not_audited_named_keys=3498,ledger=ledger))
    save(out/'relations.json',dict(common_color_frame=list(Q),original_unknown_components=identity['preserved_z_component']|{'preserved_w_component':identity['preserved_w_component']},degree_identity_rows=type_rows,N_models=models,conditional_triangle=dict(intact_fibres=tri_fibres,deletions=tri_deletions,subdivisions=subdivisions),negative_controls=negatives))
    audit_sources={name:sha256((HERE/name).read_bytes()).hexdigest() for name in ('audit_c3.py','independent_helpers.py')}
    save(out/'audit_source_versions.json',audit_sources)
    for name in audit_sources:(out/name).write_bytes((HERE/name).read_bytes())
    result=dict(status='pass' if not a.failures else 'fail',checks=a.checks,failures=a.failures,input_sha256=hashes,
      audited_artifact_sha256={name:sha256((source/name).read_bytes()).hexdigest() for name in (C,C2,C3)},
      independent_audit_sources_sha256=audit_sources,
      scope=dict(closed_C2=['CPP-134-1',30,20],closed_C3=['CPP-134-1',34,20],next_unaccepted=['CPP-134-1',34,60],ledger_keys=len(ledger),unaccepted_keys=3498,predecessor_cases=36,predecessor_geometries=140,predecessor_case_joins=900),
      finite_counts=dict(vertex_identity_types=8,list_pins=32,N_models=4,full_contact_tuples=24,N_deleted_edges=104,stored_N_local_deletion_witnesses=416,stored_N_context_partial_witnesses=104,bridge_pin_relations=12,bridge_endpoint_pin_queries=192,K4_routes=162,N_K5_minors=4,conditional_triangle_tuples=6,conditional_triangle_deleted_edges=9,conditional_triangle_local_witnesses=36,conditional_triangle_subdivisions=2),
      evidence_limit='Paper arbitrary-size proof reviewed separately; solver covers fixed controls only. Original unknown unary relations preserved symbolically; partial contexts do not certify whole-M minimality. No Lean theorem, target extension, full Sigma, general exits, K infinity equals K <=5.')
    save(out/'results.json',result)
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--snapshot',type=Path,default=SNAPSHOT);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=False)
    try:
        result=run(args.snapshot,args.output)
    except Exception:
        result=dict(status='exception',traceback=traceback.format_exc());save(args.output/'exception.json',result)
    print(json.dumps(result,ensure_ascii=False,indent=1))
    raise SystemExit(0 if result['status']=='pass' else 1)

if __name__=='__main__':main()
