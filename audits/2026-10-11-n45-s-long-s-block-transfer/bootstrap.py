"""Exclusive finite input declaration; no colouring enumeration."""
import hashlib
import json
from pathlib import Path
import shutil

HERE = Path(__file__).resolve().parent
DISPATCH = HERE.parent / '2026-10-11-n45-s-long-s-rfibre-dispatch'
BASE = 'f2692089ad4259808e27d9b7e882ac09505b180a'

def write(name, value):
    with (HERE / name).open('x') as f:
        json.dump(value, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write('\n')

def cycle(name, vs):
    return {'id': name, 'type': 'odd_cycle', 'vertices': vs}

def case(name, lv, blocks, attachments, s_l, expected_valid):
    vs = ['r'] + lv + ['s0', 's1']
    edges = []
    for block in blocks:
        bv = block['vertices']
        be = list(zip(bv, bv[1:] + bv[:1])) if block['type']=='odd_cycle' else [tuple(bv)]
        edges.extend([list(e) for e in be])
    at = {v: attachments.get(v, []) for v in vs}
    at['s0'] = ['b4', 'b0']
    at['s1'] = ['b0']
    contacts = [s_l, 's1']
    rotation = {}
    for v in vs:
        ns = [y if x==v else x for x,y in edges if v in (x,y)] + at[v]
        if v in contacts:
            ns.append('s')
        if v=='r':
            ns.append('b4')  # original omitted spoke, G-fragment only
        rotation[v] = ns
    return {
        'id':name, 'expected_valid':expected_valid, 'vertices':vs,
        'original_edges':edges, 'blocks':blocks,
        'pieces':{'L':lv, 'S':['s0','s1']},
        'ownership':{v:('root' if v=='r' else 'L' if v in lv else 'S') for v in vs},
        'boundary_attachments':at, 's_contacts':contacts,
        'r_contacts':{'L':[v for v in lv if ['r',v] in edges or [v,'r'] in edges], 'S':['s0','s1']},
        'support_order':{'L':['b2','b3','b4'],'S':['b4','b0']},
        'U_owner':'s', 'original_e':['r','b4'], 't_r':1,
        'retained_r_spokes':[], 's_spoke_variants':[['b0'],['b2'],['b0','b2']],
        'rotation':rotation,
        'rotation_scope':'cyclic neighbour data on original C/B/s/e fragment only',
        'disk_topology_verified':False, 'actual_U_supplied':False, 'actual_G_supplied':False,
        'K11_witnesses':None, 'K12_witnesses':None,
        'finite_role':'named interface microcase, not a target source'
    }

def main():
    pins = json.loads((DISPATCH/'input-pins.json').read_text())
    for p in pins['inputs']:
        data = (DISPATCH/p['frozen_path']).read_bytes()
        assert hashlib.sha256(data).hexdigest()==p['sha256']
        dest = HERE/p['frozen_path']
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open('xb') as f:
            f.write(data)
    write('inputs.json', {
        'task_id':'N45-S-LONG-S-BLOCK-TRANSFER', 'base':BASE,
        'status':'待獨立驗收', 'BASE_blobs':[p for p in pins['inputs'] if p['authority']=='BASE Git blob'],
        'sealed_audit_SHA256':[p for p in pins['inputs'] if p['authority']=='sealed audit physical SHA256'],
        'dispatch_pin':{'path':str(DISPATCH/'input-pins.json'),'sha256':hashlib.sha256((DISPATCH/'input-pins.json').read_bytes()).hexdigest()},
        'external_theorem_pins':[{
            'name':'Dvorak degree-list Lemma7/Theorem10',
            'url':'https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf',
            'sha256':'50e998fcb016418698ef31b932c6c2e728007f5e3b3348b93744781196ac1aea',
            'git_blob':None,'role':'inherited context for adopted C block structure only',
            'origin_refetched':False, 'payload_supplied_in_this_delivery':False,
            'recurrence_dependency':False,
            'pin_authority':'sealed fibre-paper-review.md'
        }],
        'missing_BASE_findings':[
            {'path':p,'authority_admitted':False,'finite_replay':{'executed':False,'status':'not triggered'},'finding_log':'logs/missing-'+str(i)+'.result.json'}
            for i,p in enumerate(['artifacts/c5_no_spoke_exterior/observations.json','artifacts/c5_single_spoke_residual_locality/observations.json'])
        ],
        'review_corrections':{'query_partition':[12,4,10,4], 'SF-RESIDUAL_additional_dependency':'SF-T2-Q0-Q1-RESTORED'},
        'original_B_pending_fields':'historical unchanged bytes; adoption follows sealed acceptance/corrections',
        'finite_inputs':'cases.json declared before colouring enumeration',
        'whole_source_normalization':'fixed jointly U012/L234/S40; no per-case renormalization'
    })
    kl=cycle('K_L',['r','l0','l1']); ks=cycle('K_S',['r','s0','s1'])
    bridge={'id':'B_L0_L2','type':'bridge','vertices':['l0','l2']}
    cases=[
        case('TT5', ['l0','l1'], [kl,ks], {'l0':['b2','b3'],'l1':['b4']},'l1',True),
        case('T5_7', ['l0','l1','l2','l3'],[cycle('K_L',['r','l0','l1','l2','l3']),ks],
             {'l0':['b2','b3'],'l1':['b3','b4'],'l2':['b2','b4'],'l3':['b4']},'l3',True),
        case('BRIDGE_BAD6', ['l0','l1','l2'], [kl,ks,bridge],
             {'l0':['b2','b3'],'l1':['b3'],'l2':['b2','b3','b4']},'l1',False),
        case('BRIDGE_FIX6', ['l0','l1','l2'], [kl,ks,bridge],
             {'l0':['b2'],'l1':['b3'],'l2':['b2','b3','b4']},'l1',True),
        case('NONROOT_CYCLE7', ['l0','l1','l2','l3'],[kl,ks,cycle('K_BRANCH',['l0','l2','l3'])],
             {'l1':['b2'],'l2':['b3','b4'],'l3':['b2','b3']},'l1',True)
    ]
    write('cases.json',{'schema':1,'status':'待獨立驗收','declaration_before_colouring_enumeration':True,
        'maximum_named_cases':8,'maximum_C_vertices_per_case':11,
        'declared_case_count':5,'declared_largest_C':7,
        'literals':['01012','01021','01023','01201','01202','01203','01212','01213','01231','01232'],
        'negative_control_plan':['change r colour in one full ambient preimage','delete one empty ambient fibre','omit one original nonroot branch vertex'],
        'cases':cases})
    print(json.dumps({'declared_cases':[c['id'] for c in cases],'colouring_enumeration_executed':False,'status':'declared'},sort_keys=True))

if __name__=='__main__':
    main()
