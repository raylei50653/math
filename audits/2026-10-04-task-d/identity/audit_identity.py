#!/usr/bin/env python3
"""Independent read-only identity/transport audit; no research modules imported."""
import argparse
import json
from pathlib import Path
from itertools import product
from collections import Counter
from hashlib import sha256

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo', type=Path, default=Path.cwd(), help='Read-only repository or immutable snapshot root')
parser.add_argument('--output', type=Path, default=Path('/tmp/math-task-d-identity-audit'), help='Standalone output directory')
args = parser.parse_args()
BASE = args.repo.resolve()
OUT = args.output.resolve()
NAMES = ['equal_pair', 'short_face', 'long_face', 'crosscut', 'short_arc', 'disjoint_pairs']
B = set(range(5))
U = set(range(4))
edge = lambda x, y: tuple(sorted((x, y)))
FRAME = {edge(i, (i + 1) % 5) for i in B}

def read(name):
    return json.loads((BASE / f'artifacts/c5_excess_two_mixed_core_{name}/observations.json').read_text())

def normalize(row):
    colors = {}
    return tuple(colors.setdefault(c, len(colors)) for c in row)

def transport(row, move):
    moved = [None] * 5
    for h in B:
        moved[move[h]] = row[h]
    target = normalize(moved)
    colors = dict(zip(moved, target))
    for c, d in zip(sorted(U - set(colors)), sorted(U - set(colors.values()))):
        colors[c] = d
    cp = [colors[c] for c in range(4)]
    assert sorted(cp) == list(range(4))
    assert all(target[move[h]] == cp[row[h]] for h in B)
    return target, cp

def span(s):
    if len(s) <= 1:
        return 0
    return min(k for k in range(1, 5) if any(s <= {(start+j)%5 for j in range(k+1)} for start in B))

def faces(rotation, edges):
    assert set(rotation) == {z for e in edges for z in e}
    for z, ring in rotation.items():
        ns = {b if a == z else a for a,b in edges if z in (a,b)}
        assert len(ring) == len(set(ring)) and set(ring) == ns
    seen, result = set(), []
    for z in sorted(rotation):
        for w in rotation[z]:
            if (z,w) in seen:
                continue
            start, dart, face = (z,w), (z,w), []
            while dart not in seen:
                seen.add(dart)
                a,b = dart
                face.append(a)
                ring = rotation[b]
                dart = b, ring[(ring.index(a)-1)%len(ring)]
            assert dart == start
            result.append(face)
    assert len(seen) == 2*len(edges)
    assert len(rotation)-len(edges)+len(result) == 2
    return result

def walk(obj):
    if isinstance(obj,dict):
        yield obj
        for v in obj.values():
            yield from walk(v)
    elif isinstance(obj,list):
        for v in obj:
            yield from walk(v)

def powerset(s):
    s=list(s)
    return {tuple(sorted(z for j,z in enumerate(s) if bits>>j&1)) for bits in range(1<<len(s))}

source = read('single_spoke')
stages = {n: read('four_spoke_'+n) for n in NAMES}
ROWS = [tuple(r) for r in source['pattern_order']]
assert len(ROWS)==10 and len(set(ROWS))==10
counts = Counter()
result = {'independent_checker_scope':'Only JSON, itertools, hashlib; research checker modules not imported.',
          'source_artifact_sha256':sha256((BASE/'artifacts/c5_excess_two_mixed_core_single_spoke/observations.json').read_bytes()).hexdigest(),
          'stages':NAMES, 'targets':[], 'failures':[], 'canonical_rotation_root_swap_non_covariance':[]}

for sigma in (933,941):
    src=next(t for t in source['targets'] if t['source_sigma']==sigma)
    records=src['named_spoke_skeletons']['records']
    selected={i:r for i,r in enumerate(records) if r['status']=='necessary_skeleton_only' and list(map(len,r['original_spoke_supports']))==[2,2]}
    assert len(selected)==(47 if sigma==933 else 75)
    counts['independently_filtered_source_frames']+=len(selected)
    by_edges={tuple(map(tuple,r['retained_source_edges'])):i for i,r in selected.items()}
    assert len(by_edges)==len(selected)
    partners={}
    for i,r in selected.items():
        a,b=r['root_order']
        assert [a,b]==[5,6]
        supports=r['original_spoke_supports']
        edges=set(map(tuple,r['retained_source_edges']))
        assert edges == FRAME|{edge(a,b)}|{edge(a,h) for h in supports[0]}|{edge(b,h) for h in supports[1]}
        apex=r['boundary_apex']
        augmented=edges|{edge(apex,h) for h in B}
        assert augmented==set(map(tuple,r['augmented_edges']))
        rotation=dict(enumerate(r['apex_rotation']))
        source_faces=faces(rotation,augmented)
        counts['source_augmented_rotation_checks']+=1
        assert set(rotation[apex])==B and len(rotation[apex])==5
        source_disk_rotation={z:[w for w in ring if w!=apex] for z,ring in rotation.items() if z!=apex}
        source_disk_faces=faces(source_disk_rotation,edges)
        assert len([f for f in source_disk_faces if len(f)==5 and set(f)==B])==1
        counts['source_rotation_C5_outer_face_after_apex_removal_checks']+=1
        swap=lambda z:b if z==a else a if z==b else z
        swapped=tuple(sorted(edge(swap(z),swap(w)) for z,w in edges))
        partner_i=by_edges[swapped]
        partner=selected[partner_i]
        assert partner['original_spoke_supports']==supports[::-1]
        partners[i]=partner_i
        pfaces=faces(dict(enumerate(partner['apex_rotation'])),set(map(tuple,partner['augmented_edges'])))
        swapped_rotation={swap(z):[swap(w) for w in ring] for z,ring in rotation.items()}
        swapped_augmented={edge(swap(z),swap(w)) for z,w in augmented}
        transported_faces=faces(swapped_rotation,swapped_augmented)
        assert set(swapped_rotation[apex])==B and len(swapped_rotation[apex])==5
        swapped_disk_rotation={z:[w for w in ring if w!=apex] for z,ring in swapped_rotation.items() if z!=apex}
        swapped_disk_edges={edge(swap(z),swap(w)) for z,w in edges}
        swapped_disk_faces=faces(swapped_disk_rotation,swapped_disk_edges)
        assert len([f for f in swapped_disk_faces if len(f)==5 and set(f)==B])==1
        counts['root_swapped_rotation_C5_outer_face_after_apex_removal_checks']+=1
        assert {frozenset(map(swap,f)) for f in source_faces}=={frozenset(f) for f in transported_faces}
        same_canonical_faces={frozenset(map(swap,f)) for f in source_faces}=={frozenset(f) for f in pfaces}
        if not same_canonical_faces:
            assert i==partner_i and supports[0]==supports[1]
            result['canonical_rotation_root_swap_non_covariance'].append({'source_sigma':sigma,'self_identity_index':i,
                 'source_faces':source_faces,'transported_root_swap_faces':transported_faces,
                 'scope':'Source NetworkX canonical rotation witness need not commute with root-swap automorphism; transported rotation is valid.'})
        shared=lambda fs:{frozenset(f) for f in fs if {a,b}<=set(f)}
        assert shared(transported_faces)==shared(pfaces)
        if i==partner_i:
            expected_seals={frozenset((a,b,h)) for h in supports[0]}
            assert shared(source_faces)==shared(transported_faces)==shared(pfaces)==expected_seals
            counts['equal_pair_swap_invariant_exact_triangle_seals_checked']+=1
        counts['source_root_swap_transported_rotations_and_shared_root_faces_checked']+=1
        counts['source_root_swap_canonical_full_face_sets_equal']+=same_canonical_faces
        for sign,shift in product((-1,1),range(5)):
            move=[(sign*h+shift)%5 for h in range(5)]
            rename=lambda z:move[z] if z in B else z
            medges={edge(rename(z),rename(w)) for z,w in edges}
            assert medges == FRAME|{edge(a,b)}|{edge(a,move[h]) for h in supports[0]}|{edge(b,move[h]) for h in supports[1]}
            maug={edge(rename(z),rename(w)) for z,w in augmented}
            mrotation={rename(z):[rename(w) for w in ring] for z,ring in rotation.items()}
            mfaces=faces(mrotation,maug)
            assert {frozenset(map(rename,f)) for f in source_faces}=={frozenset(f) for f in mfaces}
            counts['D5_source_edges_supports_rotations_checked']+=1
            transported_indices=[]
            for ri,row in enumerate(ROWS):
                tr,cp=transport(row,move)
                ti=ROWS.index(tr)
                transported_indices.append(ti)
                for ra,rb in product(range(4),repeat=2):
                    legal=(ra!=rb and all(ra!=row[h] for h in supports[0]) and all(rb!=row[h] for h in supports[1]))
                    moved_legal=(cp[ra]!=cp[rb] and all(cp[ra]!=tr[move[h]] for h in supports[0]) and all(cp[rb]!=tr[move[h]] for h in supports[1]))
                    assert legal==moved_legal
                    counts['D5_literal_root_pair_guards_checked']+=1
                counts['D5_source_row_color_checks']+=1
            assert len(set(transported_indices))==10
            msigma=sum(1<<ti for ri,ti in enumerate(transported_indices) if sigma>>ri&1)
            assert all(bool(msigma>>ti&1)==bool(sigma>>ri&1) for ri,ti in enumerate(transported_indices))
            counts['D5_complete_source_mask_checks']+=1
    assert all(partners[partners[i]]==i for i in partners)
    remaining=set(selected)
    steps=[]
    identity_occurrences=0
    for name,data in stages.items():
        t=next(t for t in data['targets'] if t['source_sigma']==sigma)
        if name=='equal_pair':
            ex=[r['inherited_named_skeleton_index'] for r in t['excluded_common_pair_frames']]
            first_domain=ex+[r['inherited_named_skeleton_index'] for r in t['remaining_unequal_pair_frames']]
            assert len(first_domain)==len(set(first_domain)) and set(first_domain)==set(selected)
        else:
            ex=t['newly_excluded_named_frame_indices']
            analysis_names={'short_face':('one_common_boundary_vertex_analysis','excluded_by_noncritical_original_unary_edge'),
                            'long_face':('one_common_boundary_vertex_analysis','excluded_by_common_long_face_unary_order'),
                            'crosscut':('one_common_boundary_vertex_analysis','excluded_by_original_unary_crosscut_and_mixed_hubs'),
                            'short_arc':('original_short_arc_frame_analyses',None),
                            'disjoint_pairs':('newly_excluded_frame_analyses',None)}
            analysis_key,predicate=analysis_names[name]
            analyses=t[analysis_key]
            analysis_indices=[a['inherited_named_skeleton_index'] for a in analyses]
            assert len(analysis_indices)==len(set(analysis_indices))
            predicted=[a['inherited_named_skeleton_index'] for a in analyses if predicate is None or a[predicate]]
            assert ex==predicted
        assert len(ex)==len(set(ex))
        assert set(ex)<=remaining
        assert {partners[i] for i in ex}==set(ex)
        remaining-=set(ex)
        remain_indices=[r['inherited_named_skeleton_index'] for r in t['remaining_unequal_pair_frames']]
        assert len(remain_indices)==len(set(remain_indices)) and set(remain_indices)==remaining
        assert {partners[i] for i in remaining}==remaining
        for item in walk(t):
            if 'inherited_named_skeleton_index' not in item:
                continue
            i=item['inherited_named_skeleton_index']
            assert i in selected
            original=selected[i]
            pairs=[('original_root_order','root_order'),('original_spoke_supports','original_spoke_supports'),
                   ('original_root_and_boundary_edges','retained_source_edges'),('inherited_skeleton_apex_rotation','apex_rotation')]
            for left,right in pairs:
                assert item[left]==original[right],(name,sigma,i,left)
            identity_occurrences+=1
            rot=item.get('exhaustive_fixed_skeleton_rotations')
            if rot:
                edges=set(map(tuple,item['original_root_and_boundary_edges']))
                disk_faces=[]
                for rr in rot['all_original_C5_outer_face_rotations']:
                    computed=faces({x['vertex']:x['ring'] for x in rr['rotation']},edges)
                    outer=rr['original_outer_boundary_face']
                    assert outer in computed and len(outer)==5 and set(outer)==B
                    inner=[f for f in computed if f!=outer]
                    assert {tuple(f) for f in inner}=={tuple(f) for f in rr['original_disk_faces']}
                    disk_faces.append({frozenset(f) for f in inner})
                    counts['all_carried_disk_rotations_validated']+=1
                assert disk_faces[0]==disk_faces[1]
        steps.append({'stage':name,'excluded_count':len(ex),'remaining_count':len(remaining),'exact_excluded_indices':ex})
    assert not remaining
    ledger=next(x for x in stages['disjoint_pairs']['complete_original_named_subtype_exclusion_ledger'] if x['source_sigma']==sigma)
    assert ledger['complete_original_named_frame_indices']==sorted(selected)
    assert [s['excluded_original_named_indices'] for s in ledger['ordered_exclusion_stages']]==[sorted(s['exact_excluded_indices']) for s in steps]
    result['targets'].append({'source_sigma':sigma,'complete_domain_size':len(selected),'source_root_swap_self_identities':sum(i==j for i,j in partners.items()),
                             'source_root_swap_nontrivial_pairs':sum(i!=j for i,j in partners.items())//2,'all_carried_original_identity_occurrences_checked':identity_occurrences,'partition':steps})

# Independently verify actual support domains, order tests, selected short paths,
# transported paths, and explicit subdivisions from every relevant record.
for name,data in stages.items():
    for t in data['targets']:
        for obj in walk(t):
            if 'original_root_and_boundary_edges' not in obj:
                continue
            edges=set(map(tuple,obj['original_root_and_boundary_edges']))
            roots=obj['original_root_order']
            for key in ('common_long_face_support_controls','common_long_original_support_controls'):
                if key not in obj:
                    continue
                con=obj[key]
                arc=con['common_original_face_boundary_arc']
                items=con.get('actual_support_pairs',con.get('all_actual_original_support_pairs'))
                domains=[(tuple(sorted(i['actual_original_U_support'])),tuple(sorted(i['actual_original_V_support']))) for i in items]
                assert len(domains)==len(set(domains)) and set(domains)==set(product(powerset(arc),repeat=2))
                pos={h:j for j,h in enumerate(arc)}
                for it in items:
                    su,sv=(set(it[k]) for k in ('actual_original_U_support','actual_original_V_support'))
                    pu,pv=sorted(pos[h] for h in su),sorted(pos[h] for h in sv)
                    compatible=not su or not sv or max(pu)<=min(pv)
                    assert compatible==it['original_disjoint_path_order_compatible']
                    assert [span(su),span(sv)]==it['minimal_cyclic_support_spans']
                    for sign,shift in product((-1,1),range(5)):
                        move=[(sign*h+shift)%5 for h in range(5)]
                        rename=lambda z:move[z] if z in B else z
                        msu,msv={move[h] for h in su},{move[h] for h in sv}
                        mpos={move[h]:j for j,h in enumerate(arc)}
                        mpu,mpv=sorted(mpos[h] for h in msu),sorted(mpos[h] for h in msv)
                        assert [span(msu),span(msv)]==[span(su),span(sv)]
                        assert (not msu or not msv or max(mpu)<=min(mpv))==compatible
                        me={edge(rename(z),rename(w)) for z,w in edges}
                        for ins in it['certified_short_original_unaries']:
                            support={move[h] for h in ins['actual_support']}
                            pair={move[h] for h in ins['enclosing_original_boundary_edge']}
                            path=[rename(z) for z in ins['original_external_path']]
                            assert support<=pair and edge(*sorted(pair)) in FRAME and path[-1] not in pair
                            assert path[0]==ins['original_unary_owner'] and set(path[1:-1])<=set(roots)-{path[0]}
                            assert all(edge(z,w) in me for z,w in zip(path,path[1:]))
                            counts['independent_D5_actual_short_support_path_checks']+=1
                        counts['independent_D5_actual_support_pair_checks']+=1
                    counts['independent_actual_support_pairs']+=1
            if 'all_actual_forced_unary_support_subsets' in obj:
                items=obj['all_actual_forced_unary_support_subsets']
                arc=obj['original_common_two_edge_boundary_arc']
                su=[tuple(sorted(i['actual_original_forced_unary_support'])) for i in items]
                assert len(su)==len(set(su)) and set(su)==powerset(arc)
                for i in items:
                    s=set(i['actual_original_forced_unary_support'])
                    assert span(s)==i['minimal_cyclic_support_span']
                    assert (span(s)>=2)==i['compatible_with_original_unary_edge_criticality']
                    assert {arc[0],arc[-1]}<=s if span(s)>=2 else not {arc[0],arc[-1]}<=s
                    counts['independent_crosscut_U_support_checks']+=1
                con=obj['original_C_support_separation_controls']
                ci=con['all_actual_original_C_support_subsets']
                cs=[tuple(sorted(i['actual_original_C_support'])) for i in ci]
                assert len(cs)==len(set(cs)) and set(cs)==powerset(arc)
                for i in ci:
                    assert (set(i['actual_original_C_support'])<={arc[-1]})==i['compatible_with_original_U_crosscut']
                    counts['independent_crosscut_C_support_checks']+=1

# Six short-arc identities: literal whole-graph rows, masks, role maps and every
# schema witness are pulled back with ONE color permutation per original row.
arc_data=stages['short_arc']
alg=arc_data['fixed_full_ordered_relation_controls']
assert alg['named_role_order']==['a','b','x','y','u','v']
Q=tuple(alg['literal_boundary'])
schemas=alg['all_complete_C_relation_schemas']
joins=alg['same_literal_frame_join_order']
assert len(schemas)==963 and len(joins)==105
bits=[s['stable_orbit_mask'] for s in schemas]
assert len(bits)==len(set(bits))
all_orbits=[list(map(tuple,o)) for o in alg['full_ordered_C_tuple_orbits']]
assert {t for o in all_orbits for t in o}==set(product(range(4),repeat=2))
c_swap=alg['C_pointwise_support_color_stabilizer']
u_swap=alg['U_pointwise_support_color_stabilizer']
assert c_swap==[0,3,2,1] and u_swap==[0,1,3,2]
for orbit in all_orbits:
    t=orbit[0]
    assert set(orbit)=={t,tuple(c_swap[c] for c in t)}
expected_masks=set()
for mask in range(1,1<<len(all_orbits)):
    rel={t for i,o in enumerate(all_orbits) if mask>>i&1 for t in o}
    if not set.intersection(*(set(t) for t in rel)):
        expected_masks.add(mask)
assert set(bits)==expected_masks
all_palettes={tuple(sorted(s)) for s in powerset(range(4)) if s}
stable_palettes={p for p in all_palettes if {u_swap[c] for c in p}==set(p)}
actual_up=[tuple(r['complete_original_U_contact_colors']) for r in alg['all_nonempty_stable_original_U_palettes']]
actual_vp=[tuple(r['complete_original_V_contact_colors']) for r in alg['all_nonempty_original_V_palettes']]
assert len(actual_up)==len(set(actual_up)) and set(actual_up)==stable_palettes
assert len(actual_vp)==len(set(actual_vp)) and set(actual_vp)==all_palettes
counts['independently_exhausted_stable_C_orbit_masks']=len(expected_masks)
for s in schemas:
    relation=set(map(tuple,s['complete_literal_ordered_C_tuples']))
    actual={t for i,o in enumerate(all_orbits) if s['stable_orbit_mask']>>i&1 for t in o}
    assert relation==actual
    assert not set.intersection(*(set(t) for t in relation))
    assert s['compatible_with_shared_original_contact']==all(x==y for x,y in relation)
    assert len(s['selected_literal_six_role_joint_witnesses_in_join_index_order'])==105

for t in arc_data['targets']:
    sigma=t['source_sigma']
    for rec in t['original_short_arc_frame_analyses']:
        move=rec['one_global_boundary_permutation']
        trs=rec['all_ten_simultaneous_whole_graph_row_color_transports']
        translated=[]
        for ri,(row,tr) in enumerate(zip(ROWS,trs)):
            expected,cp=transport(row,move)
            assert tr['source_row']==list(row) and tr['transported_row']==list(expected) and tr['color_permutation']==cp
            assert tr['transported_row_index']==ROWS.index(expected)
            translated.append(ROWS.index(expected))
            counts['stored_short_arc_whole_graph_transports_checked']+=1
        msigma=sum(1<<ti for ri,ti in enumerate(translated) if sigma>>ri&1)
        assert msigma==rec['transported_source_sigma']
        oi=rec['original_rejected_row_index']
        row=ROWS[oi]
        assert not sigma>>oi&1 and not msigma>>ROWS.index(Q)&1
        expected,cp=transport(row,move)
        assert expected==Q and cp==rec['selected_one_global_color_permutation']
        inv={v:k for k,v in enumerate(cp)}
        swapped=rec['whole_graph_root_role_swap']
        role_map=[1,0,3,2,5,4] if swapped else list(range(6))
        assert rec['canonical_role_to_original_roles']==[['a','b','x','y','u','v'][i] for i in role_map]
        supports=rec['original_spoke_supports']
        for s in schemas:
            relation=set(map(tuple,s['complete_literal_ordered_C_tuples']))
            for join,w in zip(joins,s['selected_literal_six_role_joint_witnesses_in_join_index_order']):
                assert (w[2],w[3]) in relation
                up=alg['all_nonempty_stable_original_U_palettes'][join['U_palette_index']]['complete_original_U_contact_colors']
                vp=alg['all_nonempty_original_V_palettes'][join['V_palette_index']]['complete_original_V_contact_colors']
                assert w[4] in up and w[5] in vp
                pulled=[inv[c] for c in w]
                orig=[pulled[i] for i in role_map]
                a,b,x,y,u,v=orig
                assert a!=b and a!=x and b!=y and a!=u and b!=v
                assert all(a!=row[h] for h in supports[0]) and all(b!=row[h] for h in supports[1])
                if s['compatible_with_shared_original_contact']:
                    assert x==y
                    counts['short_arc_shared_contact_witness_pullbacks']+=1
                counts['short_arc_same_source_six_role_witness_pullbacks']+=1
        counts['short_arc_source_masks_checked']+=1

cross=stages['crosscut']['selected_original_933_to_941_geometry_transport']
move=cross['one_global_boundary_permutation']
mask=sum(1<<ROWS.index(transport(row,move)[0]) for ri,row in enumerate(ROWS) if 933>>ri&1)
assert mask==cross['transported_original_source_sigma']==940 and mask!=cross['comparison_source_sigma']==941
result['selected_crosscut_geometry_transport']={'source_sigma':933,'transported_sigma':mask,'comparison_sigma':941,'relation_identity_preserved_by_equating_source_masks':False}
result['counts']=dict(sorted(counts.items()))
result['all_checks_passed']=True
OUT.mkdir(parents=True, exist_ok=True)
(OUT/'identity_results.json').write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
print(json.dumps({'all_checks_passed':True,'counts':result['counts'],'target_totals':[t['complete_domain_size'] for t in result['targets']]},sort_keys=True))
