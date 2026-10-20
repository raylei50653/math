#!/usr/bin/env python3
"""Read-only stdlib replay of one common C10 count vector per control."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import model

D=Path(__file__).resolve().parent
ROOT=D.parents[2]


def verify(cert,data):
    eight,ten,index,transfer,hrows,hi,hist,parts,matrices,umatrix=data
    assert cert['base']=='b89c5913cea9df2305845be0f65fa6f1c1aaf55f','BASE'
    assert cert['input_sha256']=={'../INPUTS.json':hashlib.sha256((D.parent/'INPUTS.json').read_bytes()).hexdigest()},'input binding'
    assert cert['source_realized'] is False and cert['smaller_bad_source_constructed'] is False,'authority boundary'
    assert cert['pin_order']==['a','n','R','L','q','c','s','v','w','t'] and cert['rows']==list(model.ROWS),'literal frames'
    positive=cert.get('require_both_source_subsets',False)
    expected=['Q2_source_positive','allK_source_positive'] if positive else ['Q1','Q2','GB','allK']
    assert [r['name'] for r in cert['records']]==expected,'complete control domain'
    if positive:
        assert cert['source_positive_subset_ids']==model.source_positive_subsets(index),'mandatory original D7 subsets'
    manifest=json.loads((D.parent/'INPUTS.json').read_text())
    catrel='audits/2026-10-18-smaller-bad-counts-e1617a2/frozen/artifacts/c5_cells/cells.json'
    raw=(ROOT/catrel).read_bytes()
    assert hashlib.sha256(raw).hexdigest()==manifest['inputs'][catrel],'frozen catalogue SHA'
    catalogue=json.loads(raw)
    K=set(map(int,catalogue['cells']))
    summary=[]
    for rec in cert['records']:
        z=rec['core_counts']
        assert len(z)==2461 and all(type(v) is int and v>=0 for v in z),'complete nonnegative core counts'
        # Inclusion-exclusion columns have signed integer coefficients; no positivity claimed.
        coeff=rec['planar_coefficients']
        assert len({j for j,v in coeff})==len(coeff) and all(type(j) is int and 0<=j<603 and type(v) is int and v for j,v in coeff),'planar coefficient domain'
        rebuilt=[0]*2461
        for j,value in coeff:
            p=parts[j]
            pairs=[(i,next(k for k in range(i) if p[k]==p[i])) for i in range(10) if p[i] in p[:i]]
            for i,t in enumerate(ten):
                if all(t[a]==t[b] for a,b in pairs):
                    rebuilt[i]+=value
        assert rebuilt==z,'same core planar span'
        residual=[-hist[t]*z[index[model.canonical(t)]] for t in hrows]
        seen=set()
        for orbit in rec['orbits']:
            key=(tuple(orbit['start']),tuple(orbit['partition']))
            assert key not in seen,'duplicate orbit descriptions'
            seen.add(key)
            weight=orbit['weight']
            assert type(weight) is int and weight>0,'nonnegative complete orbit weights'
            for j,value in model.orbit_column(*key,hi).items():
                residual[j]+=value*weight
        assert not any(residual),'full literal counted-component equations'
        e=[sum(value*z[i] for i,value in entries) for entries in transfer]
        assert e==rec['exterior_counts'],'same core cap transfer'
        graph_counts={name:model.mv(matrix,e) for name,matrix in matrices.items()}
        assert graph_counts==rec['graph_counts'],'all complete original and candidate lifts'
        assert model.mask(graph_counts['G'])==941,'source complete support'
        u=model.mv(umatrix,z)
        assert u==rec['U_counts'] and model.mask(u)==319,'full same-core U319 lifts including positive rows'
        masks={name:model.mask(values) for name,values in graph_counts.items() if name!='G'}
        if positive:
            sectors={name:sum(z[i] for i in ids) for name,ids in cert['source_positive_subset_ids'].items()}
            assert sectors==rec['source_positive_subset_counts'] and all(v>0 for v in sectors.values()),'both actual source-positive D7 subsets'
        if rec['name'] in ('allK','allK_source_positive'):
            assert masks=={'Q1':1023,'Q2':1023,'GB':1023} and all(v in K for v in masks.values()),'simultaneous all-K control'
        else:
            selected=rec['name'].split('_')[0]
            assert model.mask(graph_counts[selected]) in (932,941),'one specified candidate four-row certificate'
            assert graph_counts[selected][9]>0 and all(graph_counts[selected][j]==0 for j in (1,4,6)),'same selected candidate all four queries'
        summary.append({'name':rec['name'],'positive_core_fibres':sum(v>0 for v in z),'positive_E_fibres':sum(v>0 for v in e),'component_orbits':len(rec['orbits']),'source_mask':941,'U_mask':319,'candidate_masks':masks})
    # The three predecessor controls survive with their exact original common counts.
    oldrel='audits/2026-10-18-smaller-bad-counts-e1617a2/A/941-counted-candidate-probes.json'
    raw=(ROOT/oldrel).read_bytes()
    assert hashlib.sha256(raw).hexdigest()==manifest['inputs'][oldrel],'frozen old control SHA'
    old=json.loads(raw)
    for rec in cert['records'][:3] if not positive else []:
        previous=next(r for r in old['results'] if r['candidate']==rec['name'])
        assert rec['exterior_counts']==[4*v for v in previous['counts']],'same predecessor control up to one common scale'
    return summary


def negative_controls(cert,data):
    controls=[]
    def reject(name,mutate):
        bad=copy.deepcopy(cert)
        mutate(bad)
        try:
            verify(bad,data)
        except AssertionError as exc:
            controls.append({'name':name,'rejected':True,'reason':str(exc)})
        else:
            raise AssertionError('negative control accepted: '+name)
    reject('different-core-for-cached-fibres',lambda c:c['records'][0].__setitem__('core_counts',c['records'][2]['core_counts']))
    reject('drop-complete-orbit-multiplicity',lambda c:c['records'][0]['orbits'][0].__setitem__('weight',c['records'][0]['orbits'][0]['weight']+1))
    reject('truncate-signed-planar-span',lambda c:c['records'][0]['planar_coefficients'].pop())
    reject('omit-positive-U319-fibre',lambda c:c['records'][0]['U_counts'].__setitem__(8,0))
    reject('cross-candidate-rejection-splice',lambda c:c['records'][0]['graph_counts'].__setitem__('Q1',c['records'][2]['graph_counts']['Q1']))
    return controls


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--negative-controls',action='store_true')
    args=p.parse_args()
    data=model.build()
    cert=json.loads((D/'certificate.json').read_text())
    summary=verify(cert,data)
    source_positive=json.loads((D/'source-positive-certificate.json').read_text())
    source_summary=verify(source_positive,data)
    out={'pass':True,'exact_integer_replay':True,'same_vector_counted_C10_and_planar_span':True,'actual_source_realized':False,'smaller_bad_source_constructed':False,'results':summary,'source_positive_results':source_summary}
    if args.negative_controls:
        out['negative_controls']=negative_controls(cert,data)
        bad=copy.deepcopy(source_positive)
        bad['records'][0]['source_positive_subset_counts']['h_equals_a']=0
        try:
            verify(bad,data)
        except AssertionError as exc:
            out['negative_controls'].append({'name':'omit-mandatory-original-positive-sector','rejected':True,'reason':str(exc)})
        else:
            raise AssertionError('source-positive negative control accepted')
    print(json.dumps(out,ensure_ascii=False))


if __name__=='__main__':
    main()
