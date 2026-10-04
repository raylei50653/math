#!/usr/bin/env python3
"""Independent serialized graph/witness/projection audit; never writes source artifacts."""
from pathlib import Path
import json
from itertools import product
from collections import Counter
import time
import argparse

ROOT = Path.cwd()
OUT = Path(__file__).resolve().parent
COLORS = range(4)
FRAME = {tuple(sorted((i, (i + 1) % 5))) for i in range(5)}

def es(values):
    return {tuple(sorted(e)) for e in values}

def coloring(order, values):
    assert len(order) == len(values) and len(set(order)) == len(order)
    return dict(zip(order, values))

def validate(f, edges, beta, ports=(), values=()):
    assert all(c in COLORS for c in f.values())
    assert all(f[i] == c for i, c in enumerate(beta))
    assert all(f[a] != f[b] for a, b in edges)
    assert tuple(f[z] for z in ports) == tuple(values)

def enumerate_colorings(vertices, edges, beta, ports):
    """New MRV backtracking, no imports from repository enumeration/helpers."""
    adj = {z: set() for z in vertices}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    f = dict(enumerate(beta))
    assert all(f[a] != f[b] for a, b in edges if a in f and b in f)
    remaining = set(vertices) - set(f)
    result = set()
    def visit():
        if not remaining:
            result.add(tuple(f[z] for z in ports))
            return
        domains = {z: set(COLORS) - {f[w] for w in adj[z] if w in f} for z in remaining}
        z = min(remaining, key=lambda z: (len(domains[z]), -len(adj[z]), z))
        if not domains[z]:
            return
        remaining.remove(z)
        for c in domains[z]:
            f[z] = c
            visit()
        f.pop(z, None)
        remaining.add(z)
    visit()
    return result

def audit_stage(stage):
    started = time.monotonic()
    data = json.loads((ROOT / f'artifacts/c5_excess_two_mixed_core_four_spoke_{stage}/observations.json').read_text())
    controls = data['fixed_complete_degree_graph_controls']
    counts = Counter()
    projection_results = Counter()
    examples = {}
    for left,right in zip(controls['records'][::2],controls['records'][1::2],strict=True):
        move=lambda z: 11-z if z in (5,6) else z
        assert {tuple(sorted((move(z),move(w)))) for z,w in left['original_edges']} == es(right['original_edges'])
        for label in ('C','U','V'):
            p,q=left['original_components'][label],right['original_components'][label]
            assert p['vertices']==q['vertices'] and p['ordered_contacts']==q['ordered_contacts']
            assert [move(z) for z in p['owners']]==q['owners']
            assert p['internal_edges']==q['internal_edges'] and p['actual_attachments']==q['actual_attachments']
        for lr,rr in zip(left['rows'],right['rows'],strict=True):
            assert lr['literal_boundary']==rr['literal_boundary']
            for lv,rv in zip(lr['variants'],rr['variants'],strict=True):
                assert {tuple(sorted((move(z),move(w)))) for z,w in lv['actual_edges']}==es(rv['actual_edges'])
                assert [move(z) for z in lv['port_order']]==rv['port_order']
                assert {tuple(t['tuple']) for t in lv['complete_joint']}=={tuple(t['tuple']) for t in rv['complete_joint']}
                assert lv['pinned_a_b_fibers']==rv['pinned_a_b_fibers']
                counts['literal_full_graph_root_swap_checks']+=1
    for rec in controls['records']:
        counts['graphs'] += 1
        components = rec['original_components']
        a, b = components['C']['owners']
        x, y = components['C']['ordered_contacts']
        u = components['U']['ordered_contacts'][0]
        v = components['V']['ordered_contacts'][0]
        original = es(rec['original_edges'])
        vertex_sets = [set(p['vertices']) for p in components.values()]
        assert all(not vs & set(range(5)) for vs in vertex_sets)
        assert all(not vs & {a, b} for vs in vertex_sets)
        assert all(not vertex_sets[i] & vertex_sets[j] for i in range(3) for j in range(i))
        if x == y:
            counts['shared_contact_graphs'] += 1
        assert rec['shared_original_contact'] == (x == y)
        spoke_edges = {e for e in original if (a in e or b in e) and set(e) & set(range(5))}
        assert len(spoke_edges) == 4
        rebuilt = FRAME | spoke_edges | {tuple(sorted((a, b)))}
        for part in components.values():
            part_es = es(part['internal_edges']) | {tuple(sorted((z, h))) for z in part['vertices'] for h in part['actual_attachments'][str(z)]}
            assert part_es == es(part['edges'])
            rebuilt |= part_es
            rebuilt |= {tuple(sorted((r, z))) for r, z in zip(part['owners'], part['ordered_contacts'])}
        assert original == rebuilt
        vertices = set(range(5)) | {a, b} | set.union(*vertex_sets)
        assert all(sum(z in e for e in original) == (5 if z in (a, b) else 4) for z in vertices - set(range(5)))
        for row in rec['rows']:
            counts['rows'] += 1
            beta = row['literal_boundary']
            relations = {}
            for entry in row['original_relations']:
                label = entry['component']
                part = components[label]
                order = entry.get('vertex_order', entry.get('original_vertex_order'))
                part_es = FRAME | es(part['edges'])
                actual_tuples = {tuple(t['tuple']) for t in entry['complete_tuples']}
                direct = enumerate_colorings(set(order), part_es, beta, part['ordered_contacts'])
                assert actual_tuples == direct, (stage, rec['control_index'], row['row_index'], label)
                counts['independent_component_relations'] += 1
                relations[label] = actual_tuples
                for witness in entry['complete_tuples']:
                    validate(coloring(order, witness['coloring']), part_es, beta, part['ordered_contacts'], witness['tuple'])
                    counts['component_witnesses'] += 1
            variants = {var['name']: var for var in row['variants']}
            for var in row['variants']:
                counts['variants'] += 1
                edges = es(var['actual_edges'])
                missing = var['omitted_original_edge']
                expected = original - ({tuple(sorted(missing))} if missing is not None else set())
                if var['original_C_omitted']:
                    expected = {e for e in expected if not set(e) & set(components['C']['vertices'])}
                    assert var['port_order'] == [a, b, u, v]
                else:
                    assert var['port_order'] == [a, b, x, y, u, v]
                assert expected == edges
                actual_joint = {tuple(t['tuple']) for t in var['complete_joint']}
                direct_joint = enumerate_colorings(set(var['vertex_order']), edges, beta, var['port_order'])
                assert actual_joint == direct_joint, (stage, rec['control_index'], row['row_index'], var['name'])
                counts['independent_whole_graph_relations'] += 1
                for w in var['complete_joint']:
                    validate(coloring(var['vertex_order'], w['coloring']), edges, beta, var['port_order'], w['tuple'])
                    if x == y and not var['original_C_omitted']:
                        assert w['tuple'][2] == w['tuple'][3]
                        counts['shared_contact_full_tuples'] += 1
                    counts['whole_graph_witnesses'] += 1
                assert len(var['pinned_a_b_fibers']) == 16
                keys = set()
                for fib in var['pinned_a_b_fibers']:
                    key = (fib['a_color'], fib['b_color'])
                    assert key not in keys
                    keys.add(key)
                    expected_fiber = {t[2:] for t in direct_joint if t[:2] == key}
                    assert {tuple(t) for t in fib['full_remaining_port_fiber']} == expected_fiber
                    counts['pinned_fibers'] += 1
                    counts['empty_pinned_fibers'] += not expected_fiber
                assert keys == set(product(COLORS, repeat=2))
                if not var['original_C_omitted'] and missing is not None:
                    original_joint = {tuple(t['tuple']) for t in variants['G']['complete_joint']}
                    # Recover colors using role-to-original-vertex map, including duplicate x=y.
                    kept = set()
                    for t in actual_joint:
                        f = dict(enumerate(beta)) | dict(zip(var['port_order'], t))
                        if f[missing[0]] != f[missing[1]]:
                            kept.add(t)
                    assert kept == original_joint
                    counts['restored_full_joint_equalities'] += 1
            original_joint = {tuple(t['tuple']) for t in variants['G']['complete_joint']}
            for label,keep in [('G-au',[0,1,2,3,5]),('G-bv',[0,1,2,3,4]),('G-ax',[0,1,4,5]),('G-by',[0,1,4,5])]:
                if label not in variants:
                    continue
                om_joint = {tuple(t['tuple']) for t in variants[label]['complete_joint']}
                project = lambda relation: {tuple(t[i] for i in keep) for t in relation}
                projection_results[label+'_projected_equal'] += project(original_joint) == project(om_joint)
                projection_results[label+'_projected_different'] += project(original_joint) != project(om_joint)
                projection_results[label+'_six_role_equal'] += original_joint == om_joint
                projection_results[label+'_six_role_different'] += original_joint != om_joint
                if project(original_joint)==project(om_joint) and original_joint!=om_joint and label not in examples:
                    examples[label]=dict(control_index=rec['control_index'],row_index=row['row_index'],literal_boundary=beta,retained_positions=keep,omission_tuple_outside_original=min(om_joint-original_joint))
            if stage == 'short_face':
                audits = [row['conditional_U_projection_extension_audit']]
            elif stage == 'long_face':
                audits = row['conditional_unary_projection_extension_audits']
            elif stage == 'crosscut':
                audits = row['whole_original_C_replacement_audits']
            else:
                audits = []
            for audit in audits:
                if stage == 'short_face':
                    wset=components['U']['vertices'];keep=audit['retained_tuple_positions'];label='G-au'
                    replacements=audit['original_U_replacement_witnesses']
                    keys=('G_au_coloring','extended_original_G_coloring')
                elif stage == 'long_face':
                    side=audit['original_unary_component'];wset=components[side]['vertices'];keep=audit['retained_tuple_positions'];label='G-au' if side=='U' else 'G-bv'
                    replacements=audit['original_unary_replacement_witnesses'];keys=('original_omission_coloring','extended_original_G_coloring')
                else:
                    wset=components['C']['vertices'];keep=[0,1,4,5]
                    label=next(var['name'] for var in row['variants'] if var['omitted_original_edge']==audit['variant_original_edge'] and var['name']!='G')
                    replacements=audit['original_C_replacement_witnesses'];keys=('original_variant_coloring','extended_original_G_coloring')
                om=variants[label]
                project=lambda relation: {tuple(t[i] for i in keep) for t in relation}
                op=project(original_joint)
                vp={tuple(t['tuple']) for t in om['complete_joint']} if om['original_C_omitted'] else project({tuple(t['tuple']) for t in om['complete_joint']})
                assert audit['projections_equal'] == (op==vp)
                if stage in ('short_face','long_face'):
                    hypothesis=audit.get('at_least_two_original_U_contact_colors',audit.get('at_least_two_contact_colors'))
                    counts['five_role_equalities_under_multicolor_hypothesis']+=bool(hypothesis)
                    side='U' if stage=='short_face' else audit['original_unary_component']
                    counts['five_role_'+side+'_equalities_under_multicolor_hypothesis']+=bool(hypothesis)
                    counts['singleton_'+side+'_projection_failure_rows']+=not hypothesis and op!=vp
                    if hypothesis:
                        assert op==vp
                else:
                    counts['four_role_equalities']=counts.get('four_role_equalities',0)+1
                for replacement in replacements:
                    before=coloring(om['vertex_order'], replacement[keys[0]])
                    after=coloring(variants['G']['vertex_order'], replacement[keys[1]])
                    assert all(before[z]==after[z] for z in set(before)-set(wset))
                    validate(after, original, beta, variants['G']['port_order'], replacement['extended_original_G_tuple'])
                    assert tuple(after[z] for z in [a,b,u,v] if z not in set(wset)) == tuple(before[z] for z in [a,b,u,v] if z not in set(wset))
                    counts['replacement_witnesses_outside_unchanged'] += 1
            if stage=='short_arc' and row['constructed_original_01021_witness'] is not None:
                q=row['constructed_original_01021_witness']
                assert beta==[0,1,0,2,1]
                f=coloring(q['original_vertex_order'], q['complete_original_G_coloring'])
                validate(f,original,beta,variants['G']['port_order'],q['original_six_role_tuple'])
                assert tuple(q['original_six_role_tuple']) in original_joint
                counts['specified_rejected_row_full_colorings']+=1
    counts['elapsed_seconds']=round(time.monotonic()-started,3)
    return dict(stage=stage,counts=dict(counts),projection_comparison_counts=dict(projection_results),projected_equal_but_full_joint_different_examples=examples)

def audit_schemas():
    data=json.loads((ROOT/'artifacts/c5_excess_two_mixed_core_four_spoke_short_arc/observations.json').read_text())['fixed_full_ordered_relation_controls']
    all_tuples=list(product(COLORS,repeat=2));swap=[0,3,2,1]
    expected=set()
    for bits in range(1,1<<16):
        relation=frozenset(t for i,t in enumerate(all_tuples) if bits>>i&1)
        if frozenset((swap[x],swap[y]) for x,y in relation)!=relation:
            continue
        if set.intersection(*(set(t) for t in relation)):
            continue
        expected.add(relation)
    actual={frozenset(map(tuple,s['complete_literal_ordered_C_tuples'])) for s in data['all_complete_C_relation_schemas']}
    assert actual==expected and len(actual)==963
    assert sum(all(x==y for x,y in rel) for rel in actual)==5
    upal={p['palette_index']:set(p['complete_original_U_contact_colors']) for p in data['all_nonempty_stable_original_U_palettes']}
    vpal={p['palette_index']:set(p['complete_original_V_contact_colors']) for p in data['all_nonempty_original_V_palettes']}
    constructions=0
    for schema in data['all_complete_C_relation_schemas']:
        rel=set(map(tuple,schema['complete_literal_ordered_C_tuples']))
        assert {tuple(t) for t in schema['complete_A2_D1_guarded_C_fiber']}=={t for t in rel if t[0]!=2 and t[1]!=1}
        assert {tuple(t) for t in schema['complete_A2_D3_guarded_C_fiber']}=={t for t in rel if t[0]!=2 and t[1]!=3}
        for t,join in zip(schema['selected_literal_six_role_joint_witnesses_in_join_index_order'],data['same_literal_frame_join_order'],strict=True):
            a,b,x,y,u,v=t
            assert a==2 and b in {1,3} and a!=b and a!=x and b!=y and a!=u and b!=v
            assert (x,y) in rel and u in upal[join['U_palette_index']] and v in vpal[join['V_palette_index']]
            if schema['compatible_with_shared_original_contact']:
                assert x==y
            constructions+=1
    assert constructions==101115
    return dict(independently_enumerated_16_tuple_subsets=65535,complete_stable_Fempty_relations=963,diagonal_relations=5,selected_six_role_tuple_witnesses=constructions)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,default=ROOT,help='Repository or isolated snapshot root (default: current directory).')
    parser.add_argument('--output',type=Path,default=OUT,help='Directory for independent audit results (default: script directory).')
    args=parser.parse_args()
    ROOT=args.repo.resolve()
    OUT=args.output.resolve()
    OUT.mkdir(parents=True,exist_ok=True)
    result=[]
    for stage in ['equal_pair','short_face','long_face','crosscut','short_arc']:
        audit=audit_stage(stage)
        result.append(audit)
        print(json.dumps(audit,sort_keys=True),flush=True)
        (OUT/'results.json').write_text(json.dumps(dict(stages=result),ensure_ascii=False,indent=2)+'\n')
    schemas=audit_schemas()
    print(json.dumps(dict(short_arc_abstract_schema_audit=schemas),sort_keys=True),flush=True)
    (OUT/'results.json').write_text(json.dumps(dict(stages=result,short_arc_abstract_schema_audit=schemas),ensure_ascii=False,indent=2)+'\n')
