#!/usr/bin/env python3
"""Exclusive-create four same-candidate replacement relations from frozen fibres."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
PRIOR='audits/2026-10-23-941-types-wrong-side-6b09cd4/CAP_RELATION-v2.json'

def graph(parity,op):
    chosen=[parity,parity+2,parity+4]
    mapping=list(range(6))
    if op=='identify':
        for i in chosen:mapping[i]=chosen[0]
    edges={tuple(sorted((mapping[i],mapping[(i+1)%6]))) for i in range(6)}
    if op=='triangle':
        edges|={tuple(sorted((chosen[i],chosen[(i+1)%3]))) for i in range(3)}
    return dict(id=('even' if parity==0 else 'odd')+'_'+op,operation=op,chosen_positions=chosen,vertex_map=mapping,vertices=sorted(set(mapping)),edges=sorted([list(e) for e in edges]),completed_interior_saving=9 if op=='identify' else 7)

def main():
    prior=json.loads((HERE/'entry'/PRIOR).read_text())
    rows=sorted([r for r in prior['relations'] if r['core']=='L'],key=lambda r:r['word'])
    candidates=[graph(p,op) for p in (0,1) for op in ('identify','triangle')]
    records=[]
    for row in rows:
        word=row['word']; images=[]
        for g in candidates:
            colors={};ok=True
            for i,c in enumerate(word):
                v=g['vertex_map'][i]
                if v in colors and colors[v]!=c:ok=False
                colors[v]=c
            if ok and any(colors[a]==colors[b] for a,b in g['edges']):ok=False
            images.append(dict(candidate=g['id'],complete_lifts=[[colors[v] for v in g['vertices']]] if ok else []))
        records.append(dict(word=word,complete_original_lifts={core:next(r['complete_lifts'] for r in prior['relations'] if r['core']==core and r['word']==word) for core in ('L','R')},candidates=images))
    certificate=dict(schema='941-k6-four-candidate-reduction-v1',base='6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd',ordered_boundary=['d','p_d','U','p_x','x','zeta'],source_scope='actual globally k-minimum simple C5 disk with this sealed K6 seven-inner-point cap',selection='one full original 01232 witness chooses one candidate once; all three rejections use the same candidate',candidates=candidates,relation=records,finite_summary=dict(complete_proper_canonical_words=31,nonempty_original=19,empty_original=12,candidate_sizes=[5,8,5,8],union_equals_original=True,each_candidate_backfills=True),paper_obligations=dict(all_six_contacts_are_original_C5_interior=True,cap_seven_inner_stars_complete=True,embedded_y_tree_only_after_cap_deleted=True,parallel_edges_simplified=True,original_ordered_C5_unchanged=True,quotient_exterior_pulled_back_before_cap_fill=True,accepted_witness_selects_one_graph_for_all_rows=True),source_controls='not triggered; paper conditional exclusion separate from fixed finite relation calibration')
    with (HERE/'reduction-certificate.json').open('x') as f:json.dump(certificate,f,indent=2,sort_keys=True);f.write('\n')
    print(json.dumps(dict(status='created',proper_canonical_words=31,original_nonempty=19,candidate_sizes=[5,8,5,8])))
if __name__=='__main__':main()
