#!/usr/bin/env python3
"""Re-query exactly 800 frozen controls, including every equal-pin full lift."""
from pathlib import Path
from importlib.machinery import SourceFileLoader
from collections import Counter
from hashlib import sha256
import argparse
import json

HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
B=AUDIT/'frozen'


def encoded(value):
    return (json.dumps(value,sort_keys=True,indent=2)+'\n').encode()


def generate():
    base=json.loads((AUDIT/'BASE.json').read_text())
    for item in base['inputs']:
        raw=(B/(item['path']+'.snapshot')).read_bytes()
        assert len(raw)==item['bytes']
        assert sha256(raw).hexdigest()==item['sha256']
    p=B/'audits/2026-10-11-n2-long-mask-sync/controls/observations.json.snapshot'
    d=json.loads(p.read_text())
    s=SourceFileLoader('frozen_functions',str(B/'audits/2026-10-11-n2-long-mask-sync/controls/checker.py.snapshot')).load_module()
    out=[];hist=Counter();negative=None;newlaw_counterexamples=[]
    for m in d['bounded_motif_signature_tables']:
        for j,x in enumerate(m['entries']):
            vs=m['ordered_vertices'];edges=s.edgeset(m['original_internal_edges'])
            for v in m['contact_vertices']:
                edges.add((5,v))
            for v,bs in x['actual_boundary_attachments']:
                for b in bs:
                    edges.add(tuple(sorted((v,b))))
            fs={};lifts={}
            for label,q in s.QS.items():
                lift=[s.assignments(vs,edges,{**dict(enumerate(q)),5:a}) for a in range(4)]
                fs[str(label)]=[a for a in range(4) if not lift[a]]
                lifts[str(label)]=lift
                if len(set(fs[str(label)])&set(q))>1:
                    newlaw_counterexamples.append([m['name'],j,label])
            hist[(m['name'],all(fs.values()))]+=1
            record={'motif':m['name'],'frozen_entry_index':j,'arc_start':x['arc_start'],
                    'actual_boundary_attachments':x['actual_boundary_attachments'],
                    'forbidden_equal_pins':fs,'complete_equal_pin_lifts':lifts,
                    'has_empty_forbidden_row':not all(fs.values()),
                    'target_capacity_k_minus_F':{i:len(m['contact_vertices'])-len(f) for i,f in fs.items()}}
            out.append(record)
            if m['name']=='triangle_two_bridge_tail_three_contacts' and j==34:
                mixed=s.edgeset(m['original_internal_edges'])
                mixed.add((5,m['contact_vertices'][0]))
                for v in m['contact_vertices'][1:]:
                    mixed.add((6,v))
                for v,bs in x['actual_boundary_attachments']:
                    for b in bs:
                        mixed.add(tuple(sorted((v,b))))
                rows=[]
                for ix,q in enumerate(d['literal_boundary_table']):
                    unary=[s.assignments(vs,edges,{**dict(enumerate(q)),5:a}) for a in range(4)]
                    ambient=s.fibres(vs,mixed,[5,6],q)
                    assert [ambient[5*a] for a in range(4)]==unary
                    rows.append({'row_index':ix,'literal_beta':q,
                                 'complete_unary_lifts_by_owner_color':unary,
                                 'forbidden_owner_colors':[a for a in range(4) if not unary[a]],
                                 'complete_original_mixed_lifts_by_ordered_pins':ambient})
                bags=[{8},{9},{7},{5,10,11},set(range(5))]
                graph_edges=edges|set(s.BEDGES)
                assert all(s.connected(bag,graph_edges) for bag in bags)
                adjacency=[]
                for i in range(5):
                    for j in range(i+1,5):
                        witnesses=[list(e) for e in sorted(graph_edges)
                                   if (e[0] in bags[i] and e[1] in bags[j])
                                   or (e[1] in bags[i] and e[0] in bags[j])]
                        assert witnesses
                        adjacency.append({'bag_pair':[i,j],'original_edge_witnesses':witnesses})
                negative={'reference':'frozen_tailtriangle_entry34',
                          'original_vertices':vs,'original_internal_edges':m['original_internal_edges'],
                          'equal_pin_unary_owner':5,'equal_pin_unary_contact_vertices':m['contact_vertices'],
                          'equal_pin_unary_region_edges':sorted(map(list,edges)),
                          'original_mixed_ordered_roots':[5,6],
                          'original_mixed_ordered_contacts':[[m['contact_vertices'][0]],m['contact_vertices'][1:]],
                          'original_mixed_region_edges':sorted(map(list,mixed)),
                          'actual_boundary_attachments':x['actual_boundary_attachments'],
                          'actual_support':[0,1,2],'root_incidence_total':3,
                          'complete_degree_four':all(sum(v in e for e in edges)==4 for v in vs),
                          'leaf_blocks':{'triangle':[7,8,9],'bridge':[10,11]},
                          'leaf_private_contacts':{'triangle':[8,9],'bridge':[11]},
                          'ordinary_private_cycle_vertices':[],
                          'H_degree_two_attachment_injection':[[10,[0,1]],[11,[1,2]]],
                          'strong_empty_forbidden_row_status':'counterexample',
                          'forbidden_colors_unused_only_status':'counterexample',
                          'full_target_source_status':'not triggered',
                          'source_rotation_status':'not supplied',
                          'equal_pin_unary_planarity_status':'counterexample',
                          'equal_pin_unary_K5_minor':{'bags':[sorted(bag) for bag in bags],
                                                     'adjacencies':adjacency},
                          'full_target_capacity_status':'counterexample',
                          'source_capacity_violating_target_rows':[i for i,f in fs.items() if 3-len(f)>1],
                          'rows':rows}
    assert len(out)==800
    assert sum(not x['has_empty_forbidden_row'] for x in out)==10
    assert not newlaw_counterexamples
    assert negative is not None
    return {'scope':'Exactly 800 already-frozen named controls, no source enumeration. Equal pins give the unary query; named negative additionally preserves the original mixed off-diagonal full relation.',
            'base_head':base['head'],'frozen_input_hashes_verified':len(base['inputs']),
            'counts':{'controls':len(out),'all_rows_nonempty':sum(not x['has_empty_forbidden_row'] for x in out),
                      'used_one_violations':len(newlaw_counterexamples)},
            'histogram':[{'motif':k[0],'all_rows_nonempty':k[1],'count':v} for k,v in sorted(hist.items())],
            'named_negative_full_fibres':negative,'controls':out}


def main():
    parser=argparse.ArgumentParser()
    mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write',action='store_true')
    mode.add_argument('--check',action='store_true')
    parser.add_argument('--artifact',type=Path,default=HERE/'equal_pin_full_probe.json')
    args=parser.parse_args()
    value=generate();raw=encoded(value)
    if args.write:
        with args.artifact.open('xb') as handle:
            handle.write(raw)
    elif args.artifact.read_bytes()!=raw:
        raise SystemExit('artifact mismatch')
    print(json.dumps({'mode':'write' if args.write else 'check','bytes':len(raw),
                      'sha256':sha256(raw).hexdigest(),'counts':value['counts']},sort_keys=True))


if __name__=='__main__':
    main()
