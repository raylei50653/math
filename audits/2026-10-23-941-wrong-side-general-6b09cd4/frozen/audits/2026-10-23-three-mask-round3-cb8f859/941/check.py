#!/usr/bin/env python3
"""Read-only independent contract checker; arbitrary-size proofs are in PROOF.md."""
import argparse
from collections import deque
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import random
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BASE = 'cb8f8593e273a7426ecadd59797a6e643cc4768e'
PREV = 'audits/2026-10-23-three-mask-round2-cb8f859/941/certificate.json'
B14 = ['a','z1','z2','z3','z4','V','U','HL_0','q','c','s','v','w','t']


def require(condition, message):
    if not condition:
        raise ValueError(message)


def inputs():
    manifest = json.loads((HERE/'INPUTS.json').read_text())
    require(manifest['base']==BASE,'wrong frozen BASE')
    for row in manifest['inputs']:
        data = (HERE/'frozen'/row['path']).read_bytes()
        require((len(data),sha256(data).hexdigest())==(row['bytes'],row['sha256']),
                'frozen mathematical drift: '+row['path'])
        require(data==(ROOT/row['path']).read_bytes(),'live mathematical drift: '+row['path'])
    entry = manifest['entry_base']
    data = (HERE/entry['snapshot']).read_bytes()
    require((len(data),sha256(data).hexdigest())==(entry['bytes'],entry['sha256']),'entry BASE drift')
    require(data==(ROOT/entry['path']).read_bytes(),'live entry BASE drift')
    base_entries = {r['path']:r for r in json.loads(data)['predecessors']}
    for row in manifest['inputs']:
        if row['path'] in base_entries:
            require(all(row[k]==base_entries[row['path']][k] for k in ['bytes','sha256']),
                    'input differs from third-round entry bytes')
    routing = []
    for row in manifest['routing_entry']:
        data = (HERE/row['snapshot']).read_bytes()
        require((len(data),sha256(data).hexdigest())==(row['bytes'],row['sha256']),'routing entry drift')
        live = (ROOT/row['path']).read_bytes()
        routing.append(dict(path=row['path'],changed=live!=data,
                            entry_sha256=row['sha256'],live_sha256=sha256(live).hexdigest()))
    return manifest,routing


def path_between(edges, start, end):
    adjacency = {}
    for a,b in edges:
        adjacency.setdefault(a,set()).add(b)
        adjacency.setdefault(b,set()).add(a)
    queue = deque([[start]])
    seen = {start}
    while queue:
        walk = queue.popleft()
        if walk[-1]==end:
            return walk
        for nxt in sorted(adjacency[walk[-1]]):
            if nxt not in seen:
                seen.add(nxt)
                queue.append(walk+[nxt])
    raise ValueError('required successor tree path absent')


def validate(cert, seed=0):
    prior = json.loads((HERE/'frozen'/PREV).read_text())
    require(set(cert)=={'schema','base','scope','full_component_trees_include_all_rootless_components',
                       'arbitrary_private_size_bound','degree5_sides_both_retained','degree_at_least6_retained',
                       'source_realized','new_pair_exclusions','new_smaller_bad','new_Lean',
                       'original_941_source_control','finite_disk_survival_controls_added','paper_status',
                       'source_rows','upstream_complete_fibre_custody'},'unknown or missing top-level field')
    require(cert['schema']=='941-round3-certificate-v1' and cert['base']==BASE,'wrong certificate domain')
    require(cert['scope']=='same F ordinary short Type-I; initial02 13/36; complete whole-K successor',
            'scope changed')
    require(cert['full_component_trees_include_all_rootless_components'] is True,'rootless components omitted')
    require(cert['arbitrary_private_size_bound'] is None,'private-size bound introduced')
    require(cert['degree5_sides_both_retained'] is True and cert['degree_at_least6_retained'] is True,
            'degree branch omitted')
    require(cert['source_realized'] is False and cert['new_pair_exclusions']==0 and
            cert['new_smaller_bad'] is False and cert['new_Lean'] is False,'unsupported source/theorem promotion')
    require(cert['original_941_source_control']=='not triggered','source control upgraded')
    require(cert['finite_disk_survival_controls_added']==0,'finite source search substituted for proof')
    require(cert['paper_status']=='conditional arbitrary-size same-source lemmas; not Lean formalized',
            'paper/finite boundary lost')
    require(cert['upstream_complete_fibre_custody']==prior['upstream_complete_fibre_custody'],
            'complete upstream fibre custody changed')
    old = {(r['target'],r['initial_02_type']):r for r in prior['source_rows']}
    require(len(cert['source_rows'])==4,'missing or extra source contract row')
    observed = [(r['target'],r['initial_02_type']) for r in cert['source_rows']]
    require(len(set(observed))==4 and set(observed)==set(old),'source row domain changed')
    rows = list(cert['source_rows'])
    random.Random(seed).shuffle(rows)
    bridge_count = private_count = 0
    for row in rows:
        original = old[row['target'],row['initial_02_type']]
        require(row['complete_predecessor_record']==original,'complete predecessor fibre/lift/partition record changed')
        require(row['initial_03_type_choices']==original['initial_03_type_choices']==[4,9],
                'initial03 alternative omitted')
        target = row['target']
        cs = dict(zip(B14,[0,3,0,3,0,1,0,1,3,1,2,*((0,1) if target==44459 else (1,0)),2]))
        require(row['original_boundary_colors']==cs,'original literal changed')
        ps = dict(cs)
        ps['U'] = 2
        require(row['whole_K_successor_boundary_colors']==ps,'whole-K boundary image changed')
        require(original['actual_K_boundary_contacts']==['U'],'actual complete K contact set changed')
        blocks = original['full_03_successor_boundary_contacts']
        require(len(blocks)==4 and sorted(v for b in blocks for v in b)==sorted(B14),
                'successor contacts incomplete')
        contacts = dict(A03='a',C12='U',Q03='q',D12='c')
        named = {n:next(b for b in blocks if v in b) for n,v in contacts.items()}
        require(row['complete_successor_boundary_components']==named,'complete successor component changed')
        for name,block in named.items():
            require(set(ps[v] for v in block)<=({0,3} if name.endswith('03') else {1,2}),
                    'successor palette changed')
        ids = {v:n for n,block in named.items() for v in block}
        # Derive all boundary-induced component adjacencies directly from original cycle edges.
        derived_edges = {tuple(sorted((ids[a],ids[b]))) for a,b in zip(B14,B14[1:]+B14[:1])
                         if ids[a]!=ids[b]}
        route = path_between(derived_edges,'A03','D12')
        require(route==['A03','C12','Q03','D12'] and len(derived_edges)==3,
                'four distinct rooted nodes no longer force the tree path')
        require(row['forced_tree_path']==route,'wrong forced successor path')
        witnesses = row['original_edges_for_tree_path']
        require(witnesses==[['z4','V'],['HL_0','q'],['q','c']],'original tree edge witnesses changed')
        require([sorted([ids[a],ids[b]]) for a,b in witnesses]==
                [sorted(x) for x in zip(route,route[1:])],'original tree edges do not realize the required path')
        require(row['full_A_D_anticomplete'] is True,'full successor anticompleteness omitted')
        last = row['last_bridge']
        require(last['quantifier']=='last C vertex on each shortest actual original01 U-to-c path',
                'last-exit quantifier weakened or confused with first exit')
        require(last['original_color']==0 and last['outside_complete_K'] is True and
                last['actual_successor_03_component']==path_between(derived_edges,'C12','D12')[1],
                'last bridge placed in wrong actual successor component')
        require(last['old_first_bridge_is_not_reidentified'] is True,'old first bridge silently replaced')
        require(last['all_original_2_neighbors_outside_K'] is True and
                last['all_original_3_neighbors_in_complete_Q'] is True,'complete original-neighbor obligation lost')
        require(last['private_degree5_multiset']==[1,1,2,3,3] and
                last['private_degree_at_least6_retained'] is True,'private link branches changed')
        gates = last['boundary_classification']
        require(len(gates)==4,'an original01 alternative omitted')
        require([g['complete_initial_01_contacts'] for g in gates]==original['complete_initial_01_gate'],
                'complete original01 gate changed')
        order = list(range(4))
        random.Random(seed+target+row['initial_02_type']).shuffle(order)
        for i in order:
            gate = gates[i]
            block = next(b for b in original['complete_initial_01_gate'][i] if 'U' in b)
            require('c' in block,'actual original01 U-c premise missing')
            former = [v for v in B14 if v!='U' and cs[v]==0 and v in block]
            # Independent set intersection, keeping original boundary order.
            candidates = [v for v in B14 if v in block and v in named['Q03'] and cs[v]==0 and v!='U']
            require(gate['predecessor_first_bridge_boundary_candidates']==former,
                    'predecessor first-bridge alternatives were erased')
            require(gate['last_C_bridge_boundary_candidates']==candidates,'wrong last-bridge boundary identity')
            require(gate['canonical_last_bridge_forced_private']==(len(candidates)==0),
                    'private bridge claim is too strong or too weak')
            require(set(candidates)<={'v' if target==44459 else 'w'},'non-tip boundary bridge survived')
            bridge_count += 1
            private_count += (len(candidates)==0)
        x = row['type4_only_joint_X']
        require(x['requires_initial_03_type']==4,'X obligation applied to an unsupported03 type')
        require(x['private_X_color']==3 and x['X_in_complete_original_B13'] is True and
                x['X_in_actual_successor_A03'] is True,'same-source X membership changed')
        require(x['X_T_nonedge'] is True and x['X_anticomplete_to_full_D12'] is True,
                'joint X/T/full-D restriction omitted')
        require(x['any_actual_original_B13_X_to_q_path_visits']==path_between(derived_edges,'A03','Q03'),
                'same-B13 path bypasses forced C node')
        require(x['selected_R_color']==1 and x['selected_R_in_complete_B13_and_C12'] is True,
                'same-B13 bridge R obligation changed')
        require(x['R_may_be_V_or_Y'] is True and
                x['R_is_not_identified_with_01_bridge_neighbors'] is True and
                x['T_original_02_component_is_not_identified_with_L'] is True,
                'unsupported witness identification or privacy claim')
        require(row['pair_excluded'] is False,'source pair exclusion falsely claimed')
    require(bridge_count==16 and private_count==8,'full bridge classification totals changed')
    return dict(source_contract_rows=4,complete_initial01_branches=bridge_count,
                branches_with_forced_private_last_bridge=private_count,
                full_successor_A_D_anticomplete_rows=4,
                X_T_and_B13_joint_rows_requires_initial03_type4=4,
                source_control='not triggered',new_pair_exclusions=0)


def negative_checks(cert):
    mutations = [
        ('drop_rootless',lambda c:c.update(full_component_trees_include_all_rootless_components=False)),
        ('claim_pair_exclusion',lambda c:c.update(new_pair_exclusions=1)),
        ('put_last_T_in_A',lambda c:c['source_rows'][0]['last_bridge'].update(actual_successor_03_component='A03')),
        ('confuse_first_and_last',lambda c:c['source_rows'][0]['last_bridge'].update(old_first_bridge_is_not_reidentified=False)),
        ('allow_last_boundary_a',lambda c:c['source_rows'][0]['last_bridge']['boundary_classification'][0]['last_C_bridge_boundary_candidates'].append('a')),
        ('force_all_T_private',lambda c:c['source_rows'][0]['last_bridge']['boundary_classification'][0].update(canonical_last_bridge_forced_private=True)),
        ('erase_03_type9',lambda c:c['source_rows'][0].update(initial_03_type_choices=[4])),
        ('apply_X_to_03_type9',lambda c:c['source_rows'][0]['type4_only_joint_X'].update(requires_initial_03_type=9)),
        ('allow_X_T_edge',lambda c:c['source_rows'][0]['type4_only_joint_X'].update(X_T_nonedge=False)),
        ('drop_full_A_D_nonedge',lambda c:c['source_rows'][0].update(full_A_D_anticomplete=False)),
        ('identify_T_component_with_L',lambda c:c['source_rows'][0]['type4_only_joint_X'].update(T_original_02_component_is_not_identified_with_L=False)),
        ('erase_empty_fibres',lambda c:c['upstream_complete_fibre_custody'].update(empty_seven_point_fibres=0)),
        ('change_global_inverse',lambda c:c['source_rows'][0]['complete_predecessor_record']['successor_global_inverse'].reverse()),
        ('drop_complete_01_gate',lambda c:c['source_rows'][0]['last_bridge']['boundary_classification'].pop()),
        ('drop_complete_seven_point_lift',lambda c:c['source_rows'][0]['complete_predecessor_record']['complete_successor_seven_point_kernel']['complete_seven_point_fibre'].pop()),
        ('drop_original_cap_lift',lambda c:c['source_rows'][0]['complete_predecessor_record']['complete_successor_original_cap_records'][1]['complete_original_cap_fibres']['Q1']['01021'].pop()),
    ]
    rejected = []
    for name,mutate in mutations:
        bad = deepcopy(cert)
        mutate(bad)
        try:
            validate(bad)
        except (ValueError,KeyError,TypeError,IndexError):
            rejected.append(name)
        else:
            raise ValueError('semantic negative falsely accepted: '+name)
    return rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate',type=Path,default=HERE/'certificate.json')
    parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--negative',action='store_true')
    args = parser.parse_args()
    manifest,routing = inputs()
    cert = json.loads(args.certificate.read_text())
    stats = validate(cert,args.seed)
    result = dict(status='PASS',scope=cert['scope'],paper_status=cert['paper_status'],
                  seed=args.seed,immutable_input_drift=0,frozen_mathematical_inputs=len(manifest['inputs']),
                  certificate_sha256=sha256(args.certificate.read_bytes()).hexdigest(),
                  routing_live_drift=routing,**stats)
    if args.negative:
        result['semantic_negatives_rejected'] = negative_checks(cert)
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':
    try:
        main()
    except (ValueError,KeyError,TypeError,IndexError,OSError,json.JSONDecodeError) as exc:
        print(json.dumps(dict(status='REJECT',reason=str(exc)),sort_keys=True))
        sys.exit(1)
