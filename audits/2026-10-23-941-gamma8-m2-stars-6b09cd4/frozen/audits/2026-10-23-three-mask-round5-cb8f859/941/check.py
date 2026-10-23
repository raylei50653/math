#!/usr/bin/env python3
"""Read-only independent reconstruction of coupled interface rotations and small patch gluings."""
import argparse
from collections import Counter,deque
from copy import deepcopy
from hashlib import sha256
from itertools import combinations,product
import json
from pathlib import Path
import random
import sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
BASE='cb8f8593e273a7426ecadd59797a6e643cc4768e'
PREV='audits/2026-10-23-three-mask-round4-cb8f859/941/certificate.json'
B14=['a','z1','z2','z3','z4','V','U','HL_0','q','c','s','v','w','t']


def require(ok,message):
    if not ok:raise ValueError(message)


def authority():
    m=json.loads((HERE/'INPUTS.json').read_text());require(m['base']==BASE,'BASE changed')
    for row in m['inputs']:
        data=(HERE/'frozen'/row['path']).read_bytes()
        require((len(data),sha256(data).hexdigest())==(row['bytes'],row['sha256']),'frozen authority drift')
        require(data==(ROOT/row['path']).read_bytes(),'live immutable authority drift: '+row['path'])
    entry=m['entry_base'];data=(HERE/entry['snapshot']).read_bytes()
    require((len(data),sha256(data).hexdigest())==(entry['bytes'],entry['sha256']),'entry BASE drift')
    require(data==(ROOT/entry['path']).read_bytes(),'live BASE drift')
    entries={x['path']:x for x in json.loads(data)['predecessors']}
    for row in m['inputs']:
        if row['path'] in entries:
            require(all(row[k]==entries[row['path']][k] for k in ('bytes','sha256')),'input not at entry bytes')
    routing=[]
    for row in m['routing_entry']:
        data=(HERE/row['snapshot']).read_bytes();live=(ROOT/row['path']).read_bytes()
        require((len(data),sha256(data).hexdigest())==(row['bytes'],row['sha256']),'routing snapshot drift')
        routing.append(dict(path=row['path'],changed=live!=data,entry_sha256=row['sha256'],live_sha256=sha256(live).hexdigest()))
    return m,routing


def components(vertices,edges):
    adjacency={v:set() for v in vertices}
    for a,b in edges:
        if a in adjacency and b in adjacency:adjacency[a].add(b);adjacency[b].add(a)
    result=[]
    while adjacency:
        todo=[min(adjacency)];seen=set()
        while todo:
            v=todo.pop()
            if v not in seen:seen.add(v);todo.extend(adjacency[v]-seen)
        result.append(sorted(seen))
        for v in seen:del adjacency[v]
    return sorted(result)


def path(edges,start,end):
    adjacency={v:set() for e in edges for v in e}
    for a,b in edges:adjacency[a].add(b);adjacency[b].add(a)
    todo=deque([[start]]);seen={start}
    while todo:
        walk=todo.popleft()
        if walk[-1]==end:return walk
        for v in sorted(adjacency[walk[-1]]):
            if v not in seen:seen.add(v);todo.append(walk+[v])
    raise ValueError('required tree route absent')


def rotation_check(records,seed):
    domain={(e,l,r) for e in ((0,3),(2,1)) for l in set(range(4))-set(e) for r in set(range(4))-set(e)}
    require(len(records)==8 and {(tuple(r['center_original_colors']),*r['third_original_colors']) for r in records}==domain,'local rotation domain incomplete')
    order=list(records);random.Random(seed).shuffle(order);crossings=0
    quadrants={(1,1):0,(-1,1):1,(-1,-1):2,(1,-1):3}
    for row in order:
        a,b=row['center_original_colors'];l,r=row['third_original_colors']
        cs=dict(a=a,b=b,l=l,r=r);ps={v:(c^2 if c%2==0 else c) for v,c in cs.items()}
        xyz=dict(a=(-2,0),b=(2,0),l=(0,2),r=(0,-2));arms={}
        for face in (('a','b','l'),('b','a','r')):
            for name,color_group in [('J',lambda v:cs[v]%2),('H',lambda v:int(ps[v] in (1,2)))]:
                edges=[(u,v) for u,v in zip(face,face[1:]+face[:1]) if color_group(u)!=color_group(v)]
                require(len(edges)==2,'one zero segment per triangle failed')
                other=next((u,v) for u,v in edges if set((u,v))!={'a','b'})
                midpoint=tuple((xyz[other[0]][i]+xyz[other[1]][i])//2 for i in (0,1))
                arms[quadrants[midpoint]]=name
        word=[arms[i] for i in range(4)];transverse=all(word[i]!=word[(i+1)%4] for i in range(4))
        require(row['cyclic_zero_arm_labels']==word,'zero arms disagree with direct triangle geometry')
        require(row['transverse']==transverse and row['four_role_patch']==transverse,'tangent confused with transverse crossing')
        if transverse:
            require(len(set(cs.values()))==4,'transverse patch not four-colored')
            crossings+=1
    require(crossings==4,'wrong transverse calibration total')
    return dict(configurations=8,transverse=4,tangent=4)


def gluing_check(records,seed):
    wanted={(s,i,j) for s in (None,0,1,2,3) for i,j in product(range(2),repeat=2)}
    require(len(records)==20 and {(r['split_original_color'],*r['diagonal_choices']) for r in records}==wanted,'small-gluing domain incomplete')
    counts=Counter();order=list(records);random.Random(seed+43).shuffle(order)
    cyc=(0,2,3,1);diagonals=((0,3),(2,1))
    for rec in order:
        split=rec['split_original_color'];ds=rec['diagonal_choices']
        roles=[{c:f'{c}a' for c in cyc},{c:f'{c}b' if c==split else f'{c}a' for c in cyc}]
        require(rec['first_roles']=={str(c):v for c,v in roles[0].items()} and rec['second_roles']=={str(c):v for c,v in roles[1].items()},'original identity schema changed')
        edges=set();centers=[];faces=[]
        for role,d in zip(roles,ds):
            edges.update(tuple(sorted((role[a],role[b]))) for a,b in zip(cyc,cyc[1:]+cyc[:1]))
            e=tuple(sorted(role[c] for c in diagonals[d]));centers.append(list(e));edges.add(e)
            triples=((0,2,3),(0,3,1)) if d==0 else ((0,2,1),(2,3,1))
            faces.extend([[role[c] for c in t] for t in triples])
        require(rec['original_edges']==[list(e) for e in sorted(edges)] and rec['centers']==centers and rec['original_faces']==faces,'original patch edges/faces changed')
        vertices=sorted(set(v for e in edges for v in e));require(len(vertices) in (4,5),'small schema has wrong vertex count')
        four=next((list(vs) for vs in combinations(vertices,4) if all(tuple(sorted(e)) in edges for e in combinations(vs,2))),None)
        if centers[0]==centers[1]:
            classification='not_two_distinct_centers';require(rec['blocker'] is None,'same center assigned a wrong blocker')
            # A split third point would also demand three distinct original
            # facial triangles on one edge; it cannot provide two crossings.
            distinct_faces={tuple(sorted(f)) for f in faces}
            require(sum(set(centers[0])<=set(f) for f in distinct_faces)<=3,'bad shared-center face count')
        elif four is not None:
            classification='forbidden_original_K4'
            require(rec['blocker']==dict(vertices=four),'K4 witness changed')
        else:
            classification='forbidden_original_C4_without_diagonals';block=rec['blocker']
            cycle=block['cycle'];require(len(set(cycle))==4 and all(tuple(sorted((a,b))) in edges for a,b in zip(cycle,cycle[1:]+cycle[:1])),'false original C4')
            same=block['same_color_diagonal'];other=block['other_diagonal']
            require(set(same)=={roles[0][split],roles[1][split]} and len(set(same))==2,'same-color original nonedge lost')
            require(set(other)==set(cycle)-set(same),'other forbidden diagonal wrong')
            require(tuple(sorted(same)) not in edges and tuple(sorted(other)) not in edges,'asserted original nonedge already present')
            augmented=edges|{tuple(sorted(other))}
            require(any(all(tuple(sorted(e)) in augmented for e in combinations(vs,2)) for vs in combinations(vertices,4)),'other diagonal does not complete original K4')
            require(block['other_diagonal_forbidden_by']=='would complete original K4','bounded-side diagonal argument lost')
        require(rec['classification']==classification,'small-gluing source obstruction changed');counts[classification]+=1
    require(dict(counts)=={'not_two_distinct_centers':6,'forbidden_original_K4':10,'forbidden_original_C4_without_diagonals':4},'wrong complete gluing classification')
    return dict(counts)


def validate(c,seed=0):
    previous=json.loads((HERE/'frozen'/PREV).read_text())
    require(c['schema']=='941-round5-certificate-v1' and c['base']==BASE,'certificate domain changed')
    require(c['scope']=='ordinary short Type-I initial02 13/36; wrong original T side forces two coupled interface patches','scope changed')
    require(c['source_control']=='not triggered' and c['finite_calibrations']=='triggered and holds','source trigger or finite authority changed')
    require(c['no_private_size_or_degree_upper_bound'] is True and c['original_degree5_sides_and_high_degree_retained'] is True and c['rootless_and_boundary_tip_retained'] is True,'source branch dropped')
    require(c['new_initial_pair_exclusions']==0 and c['new_smaller_bad'] is False and c['new_Lean'] is False and c['source_realized'] is False and c['finite_source_survival_search'] is False,'unsupported theorem/source promotion')
    require(c['upstream_complete_fibre_custody']==previous['upstream_complete_fibre_custody'],'full/empty fibre custody changed')
    old={(r['target'],r['initial_02_type']):r for r in previous['source_rows']};rows=list(c['source_rows']);random.Random(seed).shuffle(rows)
    require(len(rows)==4 and {(r['target'],r['initial_02_type']) for r in rows}==set(old),'missing source contract row')
    for row in rows:
        p=old[row['target'],row['initial_02_type']];require(row['complete_predecessor_record']==p,'complete predecessor contacts/caps/lifts changed')
        third=p['complete_predecessor_record'];blocks=third['complete_successor_boundary_components'];labels={v:n for n,b in blocks.items() for v in b}
        cq={tuple(sorted((a,b))) for a,b in zip(B14,B14[1:]+B14[:1]) if {labels[a],labels[b]}=={'C12','Q03'}}
        require({tuple(sorted(e)) for e in row['beta_boundary_edges']}==cq and len(cq)==2,'wrong true C-Q interface endpoints')
        require({tuple(sorted(e)) for e in row['alpha_boundary_edges']}=={tuple(sorted(e)) for e in [('U','V'),('U','HL_0')]},'wrong original K-B interface endpoints')
        require(row['applies_initial03_types']==[4,9] and row['premise']=='M02(T) outside B component of J minus K','conditional branch scope changed')
        for key in ['marked_K_internal_C_Q_edge','beta_ends_outside_alpha_U_side','at_least_two_transverse_crossings',
                    'center_has_two_original_facial_triangles','other_diagonal_original_nonedge',
                    'only_K2_role_forced_private','K0_may_equal_U','B3_may_equal_q',
                    'patch_K2_not_identified_with_marked_Z','patch_B1_not_identified_with_R_or_r',
                    'R_and_r_may_equal_or_differ','M_not_identified_with_L',
                    'same_P_last_K_exit_b_in_B_outside_C','same_B_last_C_bridge_W_in_Q',
                    'bridge_W_may_be_boundary_q','X_R_lemmas_require_initial03_type4']:
            require(row[key] is True,'conditional/identity claim changed: '+key)
        require(row['patch_roles']=={'0':'K intersect C','2':'K intersect Q','1':'B intersect C','3':'B intersect Q'},'same-source patch roles changed')
        require(row['patch_cycle_original_colors']==[0,2,3,1] and row['patch_center_options']==[[0,3],[2,1]],'patch original edges changed')
        require(row['two_distinct_center_patches_need_at_least_original_vertices']==6,'original/private vertex bound changed')
        require(row['pair_excluded'] is False,'initial pair falsely excluded')
    return dict(source_contract_rows=4,rotation_calibration=rotation_check(c['local_rotations'],seed),
        small_gluing_calibration=gluing_check(c['small_patch_gluings'],seed),
        conditional_minimum_transverse_patches=2,conditional_minimum_union_original_vertices=6,
        source_trigger='not triggered',new_initial_pair_exclusions=0)


def negatives(c):
    tests=[
        ('erase_wrong_side_premise',lambda x:x['source_rows'][0].update(premise='always')),
        ('erase_true_crossing_requirement',lambda x:x['source_rows'][0].update(at_least_two_transverse_crossings=False)),
        ('allow_five_joint_vertices',lambda x:x['source_rows'][0].update(two_distinct_center_patches_need_at_least_original_vertices=5)),
        ('erase_q_exception',lambda x:x['source_rows'][0].update(B3_may_equal_q=False)),
        ('force_R_distinct_from_r',lambda x:x['source_rows'][0].update(R_and_r_may_equal_or_differ=False)),
        ('identify_patch_K2_with_Z',lambda x:x['source_rows'][0].update(patch_K2_not_identified_with_marked_Z=False)),
        ('identify_patch_B1_with_r',lambda x:x['source_rows'][0].update(patch_B1_not_identified_with_R_or_r=False)),
        ('drop_rootless_or_tip',lambda x:x.update(rootless_and_boundary_tip_retained=False)),
        ('drop_degree_sides',lambda x:x.update(original_degree5_sides_and_high_degree_retained=False)),
        ('turn_tangent_into_crossing',lambda x:next(r for r in x['local_rotations'] if not r['transverse']).update(transverse=True)),
        ('erase_one_local_rotation',lambda x:x['local_rotations'].pop()),
        ('erase_one_small_gluing',lambda x:x['small_patch_gluings'].pop()),
        ('erase_C4_diagonal_obligation',lambda x:next(r for r in x['small_patch_gluings'] if r['classification']=='forbidden_original_C4_without_diagonals')['blocker'].update(other_diagonal_forbidden_by='unproved')),
        ('invent_initial_pair_exclusion',lambda x:x.update(new_initial_pair_exclusions=1)),
        ('erase_empty_fibres',lambda x:x['upstream_complete_fibre_custody'].update(empty_seven_point_fibres=0)),
        ('erase_full_kernel_lift',lambda x:x['source_rows'][0]['complete_predecessor_record']['complete_predecessor_record']['complete_predecessor_record']['complete_successor_seven_point_kernel']['complete_seven_point_fibre'].pop()),
    ]
    result=[]
    for name,mutate in tests:
        bad=deepcopy(c);mutate(bad)
        try:validate(bad)
        except (ValueError,KeyError,IndexError,TypeError):result.append(dict(name=name,status='counterexample rejected'))
        else:raise ValueError('corrupted certificate accepted: '+name)
    return result


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--negative',action='store_true');parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--certificate',type=Path,default=HERE/'certificate.json');args=parser.parse_args()
    m,routing=authority();c=json.loads(args.certificate.read_text());stats=validate(c,args.seed)
    result=dict(status='PASS',seed=args.seed,scope=c['scope'],paper_status='conditional arbitrary-size same-source interface proof; no initial pair exclusion',
        immutable_input_drift=0,frozen_mathematical_inputs=len(m['inputs']),routing_live_drift=routing,
        certificate_sha256=sha256(args.certificate.read_bytes()).hexdigest(),**stats)
    if args.negative:result['semantic_negatives']=negatives(c)
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,IndexError,TypeError,OSError,json.JSONDecodeError) as exc:
        print(json.dumps(dict(status='REJECT',reason=str(exc)),sort_keys=True));sys.exit(1)


