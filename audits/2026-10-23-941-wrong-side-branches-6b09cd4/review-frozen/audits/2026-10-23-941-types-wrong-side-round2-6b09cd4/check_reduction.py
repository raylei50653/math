#!/usr/bin/env python3
"""Read-only full K6 relations and same-candidate backfill certificate.

Planarity, sealed original stars and global minimality are paper obligations.
"""
import argparse
from copy import deepcopy
from hashlib import sha256
from itertools import combinations,product
import json
from pathlib import Path
import random
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
CAP='audits/2026-10-23-941-gamma8-empty-m2-6b09cd4/K6_CAPS.json'
CAT='artifacts/c5_cells/cells.json'

def require(ok,why):
    if not ok:raise ValueError(why)

def canonical(w):
    names={}
    return tuple(names.setdefault(x,len(names)) for x in w)

def custody():
    count=0
    for name,key in [('INPUTS.json','entries'),('REDUCTION_INPUTS.json','inputs'),('GEOMETRY_INPUTS.json','inputs')]:
        data=json.loads((HERE/name).read_text())
        for row in data[key]:
            frozen=(HERE/'entry'/row['path']).read_bytes()
            require((len(frozen),sha256(frozen).hexdigest())==(row['bytes'],row['sha256']),'frozen input drift '+row['path'])
            if not row.get('routing',False):
                require((ROOT/row['path']).read_bytes()==frozen,'live authority drift '+row['path'])
            count+=1
    return count

def expected_graphs():
    out={}
    cycle=[(i,(i+1)%6) for i in range(6)]
    for name,indices in [('even',(0,2,4)),('odd',(1,3,5))]:
        for op in ('identify','triangle'):
            mapping=[indices[0] if op=='identify' and i in indices else i for i in range(6)]
            edges={tuple(sorted((mapping[a],mapping[b]))) for a,b in cycle}
            if op=='triangle':edges|=set(combinations(indices,2))
            require(all(a!=b for a,b in edges),'quotient loop')
            out[name+'_'+op]=dict(id=name+'_'+op,operation=op,chosen_positions=list(indices),vertex_map=mapping,vertices=sorted(set(mapping)),edges=sorted([list(e) for e in edges]),completed_interior_saving=7+6-len(set(mapping)))
    return out

def original_relations(words):
    result={}
    caps=json.loads((HERE/'entry'/CAP).read_text())['caps']
    for cap in caps:
        boundary=cap['ordered_boundary'];inner=cap['ordered_inner']
        require(boundary==['d','p_d','U','p_x','x','zeta'],'ordered original K6')
        require(len(cap['edges'])==30 and len(inner)==7,'original cap scope')
        inner_edges=[(inner.index(a),inner.index(b)) for a,b in cap['edges'] if a in inner and b in inner]
        crossing=[(inner.index(a),boundary.index(b)) if a in inner else (inner.index(b),boundary.index(a)) for a,b in cap['edges'] if (a in inner)!=(b in inner)]
        complete=[t for t in product(range(4),repeat=7) if all(t[a]!=t[b] for a,b in inner_edges)]
        require(len(complete)==264,'all internal assignments')
        result[cap['core']]={w:sorted([list(t) for t in complete if all(t[a]!=w[b] for a,b in crossing)]) for w in words}
    require(set(result)=={'L','R'},'two original named caps')
    return result

def candidate_relation(g,words):
    out={w:[] for w in words};vertices=g['vertices']
    for t in product(range(4),repeat=len(vertices)):
        col=dict(zip(vertices,t))
        if any(col[a]==col[b] for a,b in g['edges']):continue
        w=tuple(col[v] for v in g['vertex_map'])
        if canonical(w)==w:
            require(w in out,'candidate failed inherited boundary cycle')
            out[w].append(list(t))
    return out

def reconstruct(cert,seed):
    count=custody()
    require(cert['schema']=='941-k6-four-candidate-reduction-v1','certificate schema')
    require(cert['base']=='6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd','BASE')
    require(cert['ordered_boundary']==['d','p_d','U','p_x','x','zeta'],'boundary order')
    require(cert['paper_obligations'] and all(v is True for v in cert['paper_obligations'].values()),'missing paper obligation declaration')
    expected=expected_graphs();require(len(cert['candidates'])==4,'four candidate operations')
    require({g['id'] for g in cert['candidates']}==set(expected),'candidate identity coverage')
    for g in cert['candidates']:require(g==expected[g['id']],'candidate mapping/edge/cost drift')
    words=sorted({canonical(w) for w in product(range(4),repeat=6) if all(w[i]!=w[(i+1)%6] for i in range(6))})
    require(len(words)==31,'complete proper six-frame domain')
    old=original_relations(words)
    new={name:candidate_relation(g,words) for name,g in expected.items()}
    got=[]
    for w in words:
        got.append(dict(word=list(w),complete_original_lifts={core:old[core][w] for core in ('L','R')},candidates=[dict(candidate=g['id'],complete_lifts=new[g['id']][w]) for g in cert['candidates']]))
    claimed=deepcopy(cert['relation']);random.Random(seed).shuffle(claimed)
    require(sorted(got,key=lambda r:r['word'])==sorted(claimed,key=lambda r:r['word']),'complete relation/fibres/lifts drift')
    support={core:{w for w in words if old[core][w]} for core in old}
    require(support['L']==support['R'] and len(support['L'])==19,'original R19')
    masks={name:{w for w in words if relation[w]} for name,relation in new.items()}
    for name,rel in masks.items():require(rel<=support['L'],'backfill leakage '+name)
    require(set().union(*masks.values())==support['L'],'accepted witness not covered')
    policy={w:next(name for name in expected if w in masks[name]) for w in sorted(support['L'])}
    # Each accepted tuple chooses once; the chosen graph must backfill every row.
    require(all(all(not new[name][z] or old['L'][z] for z in words) for w,name in policy.items()),'same-candidate global backfill')
    catalogue=json.loads((HERE/'entry'/CAT).read_text());rows=[''.join(map(str,w)) for w in catalogue['pattern_order']]
    require(rows==['01012','01021','01023','01201','01202','01203','01212','01213','01231','01232'],'catalogue row frame')
    known=set(map(int,catalogue['cells']));require(len(known)==132,'complete K132 catalogue')
    require(not any((m&594)==512 for m in known),'four-row catalogue countermodel')
    require((941&594)==512,'source four-row trigger')
    sizes=[len(masks[g['id']]) for g in cert['candidates']]
    require(cert['finite_summary']==dict(complete_proper_canonical_words=31,nonempty_original=19,empty_original=12,candidate_sizes=sizes,union_equals_original=True,each_candidate_backfills=True),'finite summary drift')
    return dict(status='PASS',seed=seed,frozen_inputs=count,immutable_drift=0,complete_proper_words=31,original_nonempty=19,original_empty=12,complete_original_lifts_each=sum(map(len,old['L'].values())),candidate_sizes=sizes,each_candidate_backfills=True,union_equals_original=True,accepted_tuple_choices=19,same_candidate_global_row_checks=19*31,catalogue_masks=132,catalogue_four_row_matches=0,paper_reduction='conditional on sealed original K6, all contacts original C5-interior, planarity and minimum-source premises; see PROOF.md',source_controls='not triggered',new_Lean=False)

def main():
    p=argparse.ArgumentParser();p.add_argument('--certificate',type=Path,default=HERE/'reduction-certificate.json');p.add_argument('--seed',type=int,default=0);p.add_argument('--negative',action='store_true');a=p.parse_args()
    c=json.loads(a.certificate.read_text());result=reconstruct(c,a.seed)
    if a.negative:
        tests=[('missing_empty_fibre',lambda x:x['relation'].pop(3)),('missing_full_lift',lambda x:x['relation'][0]['complete_original_lifts']['L'].pop()),('wrong_contact_frame',lambda x:x['ordered_boundary'].reverse()),('crossed_identification_map',lambda x:x['candidates'][0]['vertex_map'].__setitem__(1,0)),('missing_cover_candidate',lambda x:x['candidates'].pop()),('wrong_completed_cost',lambda x:x['candidates'][0].update(completed_interior_saving=7)),('missing_same_graph_declaration',lambda x:x['paper_obligations'].update(accepted_witness_selects_one_graph_for_all_rows=False)),('false_cover_summary',lambda x:x['finite_summary'].update(union_equals_original=False))]
        rejected=[]
        for name,mutate in tests:
            bad=deepcopy(c);mutate(bad)
            try:reconstruct(bad,a.seed)
            except (ValueError,KeyError,IndexError):rejected.append(name)
            else:raise ValueError('negative accepted '+name)
        result=dict(status='PASS',seed=a.seed,semantic_negatives_rejected=rejected,source_controls='not triggered')
    print(json.dumps(result,sort_keys=True))
if __name__=='__main__':
    try:main()
    except Exception as e:
        print(json.dumps(dict(status='FAIL',reason=str(e)),sort_keys=True));raise SystemExit(1)
