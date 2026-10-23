#!/usr/bin/env python3
"""Independent graph/quotient relation checker using frozen complete old fibres."""
import argparse
from copy import deepcopy
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import random
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BASE='6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'
PREV='audits/2026-10-23-941-gamma8-empty-m2-6b09cd4/certificate.json'
REL='audits/2026-10-23-941-types-wrong-side-6b09cd4/CAP_RELATION-v2.json'


def require(ok,why):
    if not ok:raise ValueError(why)


def canonical(word):
    labels={};out=[]
    for c in word:
        if c not in labels:labels[c]=len(labels)
        out.append(labels[c])
    return tuple(out)


def custody():
    total=0
    for name in ['INPUTS.json','INPUTS_REPLACEMENT.json','INPUTS_GEOMETRY.json']:
        m=json.loads((HERE/name).read_text());require(m['base']==BASE,'authority BASE drift')
        for row in m['inputs']:
            for path in [ROOT/row['path'],HERE/row['snapshot']]:
                raw=path.read_bytes();require((len(raw),sha256(raw).hexdigest())==(row['bytes'],row['sha256']),'authority drift '+str(path))
            total+=1
    replay=json.loads((HERE/'PREDECESSOR_HASH_REPLAY.json').read_text())
    require(replay['status']=='PASS' and replay['immutable_drift']==0 and replay['related_entries']==32,'predecessor final manifest replay')
    for row in replay['entries']:
        raw=(ROOT/row['path']).read_bytes()
        require((len(raw),sha256(raw).hexdigest())==(row['bytes'],row['sha256']),'predecessor manifest drift '+row['path'])
    return dict(direct_inputs=total,previous_manifest_entries=32,immutable_drift=0)


def graph_models():
    # Build both graphs independently from cyclic position sets, then take the
    # actual quotient graph for each identification; no producer formulas used.
    ring={tuple(sorted((i,(i+1)%6))) for i in range(6)}
    rows=[]
    for parity in (0,1):
        p=list(range(parity,6,2));name='even' if parity==0 else 'odd'
        diagonals={tuple(sorted((p[i],p[(i+1)%3]))) for i in range(3)}
        edges=ring|diagonals
        rows.append(dict(id='triangle_'+name,port_map=list(range(6)),vertices=list(range(6)),
            edges=edges,kind='add_three_internal_chords',k_drop=7))
    for parity in (0,1):
        p=list(range(parity,6,2));name='even' if parity==0 else 'odd'
        port=[p[0] if i in p else i for i in range(6)]
        edges={tuple(sorted((port[a],port[b]))) for a,b in ring}
        require(all(a!=b for a,b in edges),'identification loop')
        rows.append(dict(id='identify_'+name,port_map=port,vertices=sorted(set(port)),
            edges=edges,kind='contract_empty_disk_Y_tree',k_drop=7+6-len(set(port))))
    return rows


def full_graph_relation(model):
    observed=set()
    for assignment in product(range(4),repeat=len(model['vertices'])):
        colors=dict(zip(model['vertices'],assignment))
        if all(colors[a]!=colors[b] for a,b in model['edges']):
            observed.add(tuple(colors[v] for v in model['port_map']))
    return observed


def validate(c,seed=0):
    require(c['schema']=='941-gamma8-k6-exterior-reduction-v1' and c['base']==BASE,'schema/BASE drift')
    prior=json.loads((HERE/'frozen'/PREV).read_text());old=json.loads((HERE/'frozen'/REL).read_text())
    require(c['complete_predecessor_certificate']==prior,'old complete source fibres/full lifts changed')
    require(c['complete_predecessor_K6_fibres']==old,'old complete K6 fibres/full lifts changed')
    require(old['normalized_boundary_words']==31 and old['nonempty_per_core']==19 and old['empty_per_core']==12,'old complete K6 domain')
    tables={core:{tuple(r['word']):r['complete_lifts'] for r in old['relations'] if r['core']==core} for core in ('L','R')}
    require(set(tables['L'])==set(tables['R']) and len(tables['L'])==31,'complete old boundary frame')
    require(all(bool(tables['L'][w])==bool(tables['R'][w]) for w in tables['L']),'two cores differ in support')
    expected=graph_models();require(len(c['candidates'])==4,'four fixed candidates missing')
    relations=[]
    allwords=list(product(range(4),repeat=6))
    for actual,model in zip(c['candidates'],expected):
        require(actual['id']==model['id'] and actual['port_map']==model['port_map'] and actual['vertices']==model['vertices'],'candidate identities changed')
        require({tuple(sorted(e)) for e in actual['edges']}==model['edges'] and len(actual['edges'])==len(model['edges']),'candidate actual edges changed')
        require(actual['kind']==model['kind'] and actual['k_drop']==model['k_drop'],'candidate operation/completed cost drift')
        relation=full_graph_relation(model);relations.append(relation)
        mask=''.join('1' if w in relation else '0' for w in allwords)
        require(actual['complete_literal_port_relation']==mask,'candidate complete quotient relation changed')
    proper=[w for w in allwords if all(w[i]!=w[(i+1)%6] for i in range(6))]
    normalized=sorted(w for w in proper if canonical(w)==w)
    require(len(proper)==732 and len(normalized)==31,'literal/S4 domain coverage')
    require([tuple(r['word']) for r in c['normalized_boundary_rows']]==normalized,'normalized row ordering/coverage')
    for r in c['normalized_boundary_rows']:
        w=tuple(r['word']);require(r['candidate_acceptance']==[w in s for s in relations],'normalized candidate row drift')
    order=list(proper);random.Random(seed).shuffle(order)
    for word in order:
        normalized_word=canonical(word)
        old_nonempty=bool(tables['L'][normalized_word])
        new=[word in s for s in relations]
        require(any(new)==old_nonempty,'four-candidate union leaks or misses old fibre')
    # Test literal inverse colour transport of every stored full old lift.  No
    # independent normalization of exterior, candidate, or patch is allowed.
    caps=json.loads((HERE/'frozen/audits/2026-10-23-941-gamma8-empty-m2-6b09cd4/K6_CAPS.json').read_text())
    cap_by_core={r['core']:r for r in caps['caps']}
    literal_old_lifts=0
    for word in proper:
        norm=canonical(word);forward={};back={}
        for actual,normal in zip(word,norm):forward[actual]=normal;back[normal]=actual
        for normal,actual in zip(sorted(set(range(4))-set(back)),sorted(set(range(4))-set(forward))):back[normal]=actual
        for core in ('L','R'):
            for lift in tables[core][norm]:
                require(len(lift)==7 and all(v in range(4) for v in lift),'old full lift malformed')
                literal=[back[v] for v in lift]
                require(len(literal)==7,'lost literal full lift')
                cap=cap_by_core[core]
                colors=dict(zip(cap['ordered_boundary'],word))
                colors.update(zip(cap['ordered_inner'],literal))
                require(set(colors)==set(cap['vertices']),'literal full lift loses source vertices')
                require(all(colors[a]!=colors[b] for a,b in cap['edges']),'literal inverse transport is not a full proper lift')
                literal_old_lifts+=1
    require(c['paper_contract']==dict(same_original_graph_and_literal_C5=True,j=2,full_M2_empty=True,
        original_T_degree=6,exterior_private_points=5,all_six_K6_ports_original_C5_private=True,
        sealed_seven_private_vertices=True,choose_candidate_once_from_one_actual_01232_witness=True,
        quotient_coloring_pulled_back_to_same_exterior=True,all_three_rejected_rows_share_same_candidate=True,
        planar_Y_contraction_before_simplifying_parallel_edges=True,no_original_target_target_edge=True,
        no_completion_vertices=True,E_rootless_retained=True,U_only_F_side_link=True,
        normalised_candidate_need_not_preserve_r6_or_degrees=True),'paper/source quantifiers drift')
    require(c['authority_boundaries']==dict(finite_cover='triggered and holds',source_instance_control='not triggered',
        paper_minimal_source_five_point_branch='excluded',minimum_exterior_private_points=6,
        all_eleven_j2_types_minimum_exterior_private_points=6,eleven_type_exclusions=0,
        general_wrong_side='OPEN',common_k_lower_bound=23,new_Lean=False,new_LP=False),'source/general authority promotion')
    return dict(candidates=4,normalized_boundary_words=31,old_support_classes=19,old_empty_classes=12,
        complete_literal_boundary_tuples=4096,proper_literal_tuples=732,old_nonempty_literal_tuples=444,
        candidate_support_classes=[sum(w in r for w in normalized) for r in relations],
        candidate_literal_tuple_counts=[len(r) for r in relations],literal_old_full_lifts_checked=literal_old_lifts,
        source_instance_control='not triggered',paper_minimal_source_five_point_branch='excluded')


def negatives(c):
    tests=[('lose_fixed_candidate',lambda x:x['candidates'].pop()),
        ('change_triangle_edge',lambda x:x['candidates'][0]['edges'].pop()),
        ('change_quotient_ports',lambda x:x['candidates'][2]['port_map'].__setitem__(4,4)),
        ('lose_normalized_empty_row',lambda x:x['normalized_boundary_rows'].pop()),
        ('invent_literal_extension',lambda x:x['candidates'][0].update(complete_literal_port_relation='1'*4096)),
        ('wrong_completed_cost',lambda x:x['candidates'][2].update(k_drop=10)),
        ('lose_original_empty_fibre',lambda x:x['complete_predecessor_K6_fibres']['relations'].pop()),
        ('lose_full_old_lift',lambda x:next(r for r in x['complete_predecessor_K6_fibres']['relations'] if r['complete_lifts'])['complete_lifts'].pop()),
        ('choose_per_rejected_row',lambda x:x['paper_contract'].update(all_three_rejected_rows_share_same_candidate=False)),
        ('erase_accepted_witness',lambda x:x['paper_contract'].update(choose_candidate_once_from_one_actual_01232_witness=False)),
        ('pretend_exterior_unchanged',lambda x:x['paper_contract'].update(quotient_coloring_pulled_back_to_same_exterior=False)),
        ('identify_outer_C5',lambda x:x['paper_contract'].update(all_six_K6_ports_original_C5_private=False)),
        ('cyclic_U_star',lambda x:x['paper_contract'].update(U_only_F_side_link=False)),
        ('pretend_source_triggered',lambda x:x['authority_boundaries'].update(source_instance_control='triggered and holds')),
        ('exclude_whole_eleven_type',lambda x:x['authority_boundaries'].update(eleven_type_exclusions=1)),
        ('raise_global_k',lambda x:x['authority_boundaries'].update(common_k_lower_bound=24))]
    rejected=[]
    for name,mutate in tests:
        bad=deepcopy(c);mutate(bad)
        try:validate(bad)
        except (ValueError,KeyError,IndexError,TypeError):rejected.append(dict(name=name,status='rejected'))
        else:raise ValueError('accepted negative '+name)
    return rejected


def main():
    p=argparse.ArgumentParser();p.add_argument('--certificate',type=Path,default=HERE/'certificate.json');p.add_argument('--seed',type=int,default=0);p.add_argument('--negative',action='store_true');a=p.parse_args()
    auth=custody();c=json.loads(a.certificate.read_text());r=dict(status='PASS',seed=a.seed,custody=auth,**validate(c,a.seed))
    if a.negative:r['semantic_negatives']=negatives(c)
    print(json.dumps(r,sort_keys=True))


if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,IndexError,TypeError,OSError,json.JSONDecodeError) as e:
        print(json.dumps(dict(status='REJECT',reason=str(e))));sys.exit(1)
