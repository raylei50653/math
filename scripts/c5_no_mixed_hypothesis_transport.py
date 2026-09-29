#!/usr/bin/env python3
"""Read-only support audit for root-compatible whole-component recoloring.
No new graph enumeration, source exclusions, or target accepts.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
Q=(0,1,0,1,2)
U=set(range(4))
PERMS=tuple(permutations(range(4)))
FAMILIES={'AA':'t2_path_palettes','AB':'t2_t1_endpoints','AC':'t2_t0_pairs','AE':'t2_t0_singles','BB':'bb','BC':'bc','BE':'be'}

def original(record):
    while 'original_record' in record or 'inherited_record' in record:
        record=record.get('original_record',record.get('inherited_record'))
    return record

def context(record,source):
    comps=[]
    offset=0
    for root in ('z','w'):
        side=source[root]
        for i,(ports,banned) in enumerate(zip(side['ports'],side['forbidden'],strict=True)):
            comps.append({'name':'CDE'[i]+root,'root':root,'support':record['supports'][offset],
                          'ports':ports,'source_forbidden':banned})
            offset+=1
        spokes=record['supports'][offset:offset+len(side['root_boundary'])]
        assert all(len(s)==1 for s in spokes)
        assert sorted(s[0] for s in spokes)==side['root_boundary']
        offset+=len(spokes)
    assert offset==len(record['supports'])
    c=source['z']['common']
    assert c==source['w']['common']
    for r in ('z','w'):
        forbidden=set().union(*(set(comp['source_forbidden']) for comp in comps if comp['root']==r))
        assert U-{Q[i] for i in source[r]['root_boundary']}-forbidden=={c}
    return comps,{r:source[r]['root_boundary'] for r in ('z','w')},c

def pairs(z,w):
    return [[a,b] for a,b in product(sorted(z),sorted(w)) if a!=b]

def analyze(comps,spokes,c,p):
    H={r:U-{p[i] for i in spokes[r]} for r in ('z','w')}
    # Etr is exact if every component transports; otherwise an upper bound.
    Etr={r:set(H[r]) for r in ('z','w')}
    G={r:set(H[r]) for r in ('z','w')}
    data=[]
    for comp in comps:
        pp=[pi for pi in PERMS if all(pi[Q[i]]==p[i] for i in comp['support'])]
        images={pi[c] for pi in pp}
        H[comp['root']] &= images
        local_available=U-set(comp['source_forbidden'])
        transported_available={pi[x] for pi in pp for x in local_available}
        G[comp['root']] &= transported_available
        assert images <= transported_available
        forbidden_images={tuple(sorted(pi[x] for x in comp['source_forbidden'])) for pi in pp}
        assert len(forbidden_images)<=1,comp
        if pp:
            banned=set(next(iter(forbidden_images)))
            assert not images & banned
            Etr[comp['root']] -= banned
        else:banned=None
        data.append(comp|{'permutations':[list(pi) for pi in pp], 'common_color_images':sorted(images),
                         'target_forbidden_if_transport':sorted(banned) if banned is not None else None,
                         'transported_local_available':sorted(transported_available)})
    assert all(H[r]<=G[r]<=Etr[r] for r in ('z','w'))
    hp=pairs(H['z'],H['w'])
    all_transport=all(d['permutations'] for d in data)
    ep=pairs(Etr['z'],Etr['w']) if all_transport else None
    if hp:assert all_transport and ep
    if all_transport:assert G==Etr
    gp=pairs(G['z'],G['w'])
    assert bool(gp)==bool(ep)
    return {'components':data,'H':{r:sorted(H[r]) for r in H},'H_pairs':hp,
            'all_components_transport':all_transport,'G':{r:sorted(G[r]) for r in G},'G_pairs':gp,
            'E_if_all_transport':{r:sorted(Etr[r]) for r in Etr} if all_transport else None,
            'exact_pairs_if_all_transport':ep}

def build():
    output={'scope':'Finite audit of existing necessary supports, not realizable graphs or new target proof',
            'criterion':'H_r = (U minus p(root_boundary)) intersect intersection_C {pi(c): pi(q_i)=p_i on all actual support}',
            'inputs_sha256':{},'families':{},'queries':[]}
    for family,suffix in FAMILIES.items():
        path=ROOT/f'artifacts/c5_adjacent_degree5_no_mixed_{suffix}/observations.json'
        raw=path.read_bytes(); output['inputs_sha256'][str(path.relative_to(ROOT))]=sha256(raw).hexdigest()
        bundle=json.loads(raw)
        sources=bundle.get('original_records',bundle.get('original_frontier'))
        count=Counter()
        for final in bundle['records']:
            record=original(final)
            if record.get('status') in ('excluded','source_excluded'):continue
            source=sources[record['source_id']]
            comps,spokes,c=context(record,source)
            count['retained_supports']+=1
            targets=final.get('final_targets',final.get('targets',[]))
            assert len(targets)==2 and all(t['status']=='accept' for t in targets)
            for target in targets:
                p=tuple(target['row']); assert p in ((0,1,0,2,1),(0,1,2,1,2))
                a=analyze(comps,spokes,c,p)
                count['queries']+=1
                if a['G_pairs']:count['local_preimage_criterion_accepts']+=1
                if a['H_pairs']:count['criterion_accepts']+=1
                elif a['all_components_transport']:count['all_transport_but_criterion_fails']+=1
                else:count['some_component_cannot_transport']+=1
                if a['all_components_transport']:
                    count['all_components_transport']+=1
                    assert a['exact_pairs_if_all_transport']
                output['queries'].append({'family':family,'record_id':record['id'],'source_id':record['source_id'],
                    'source_side_ids':source['side_ids'],'source_common':c,'row':p,
                    'root_boundary':spokes,'inherited_target_status':target['status']}|a)
        output['families'][family]=dict(sorted(count.items()))
    total=Counter()
    for c in output['families'].values():total.update(c)
    assert total['retained_supports']==2082 and total['queries']==4164
    assert total['criterion_accepts']+total['all_transport_but_criterion_fails']+total['some_component_cannot_transport']==4164
    output['totals']=dict(sorted(total.items()))
    # Check the closed-form common-color image set using only equality patterns.
    checks=0
    for mask in range(1<<5):
        support=[i for i in range(5) if mask>>i&1]
        for p in ((0,1,0,2,1),(0,1,2,1,2)):
            phi={}
            compatible=True
            for i in support:
                if Q[i] in phi and phi[Q[i]]!=p[i]:compatible=False
                phi[Q[i]]=p[i]
            if len(set(phi.values()))!=len(phi):compatible=False
            for c in range(4):
                expected=set() if not compatible else ({phi[c]} if c in phi else U-set(phi.values()))
                actual={pi[c] for pi in PERMS if all(pi[Q[i]]==p[i] for i in support)}
                assert expected==actual
                checks+=1
    output['equality_pattern_controls']=checks
    output['script_sha256']=sha256(Path(__file__).read_bytes()).hexdigest()
    return output

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',default=str(ROOT / 'artifacts/c5_no_mixed_hypothesis_audit/transport.json'))
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    data=build(); raw=json.dumps(data,sort_keys=True,ensure_ascii=False,indent=2)+'\n'
    out=Path(args.out)
    if args.check:assert out.read_text()==raw,'audit differs from saved output'
    else:out.write_text(raw)
    print(json.dumps({'families':data['families'],'totals':data['totals'],'equality_pattern_controls':data['equality_pattern_controls']},indent=2))
if __name__=='__main__':main()
