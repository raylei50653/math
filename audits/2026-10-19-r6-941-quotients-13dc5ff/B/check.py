#!/usr/bin/env python3
"""Read-only, exact replay of source pockets and completed local comparisons."""
import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path
import minimality as m

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
BASE='13dc5ff163045c85b5c82dde438eb5f275dab999'
OLD=Path('audits/2026-10-19-r6-941-leakage-b89c591')
CAT=Path('audits/2026-10-18-smaller-bad-counts-e1617a2/frozen/artifacts/c5_cells/cells.json')
PINS=('a','n','R','L','q','c','s','v','w','t')
MINDEG=(3,3,4,4,3,2,4,4,4,4)
INPUTS=(
 OLD/'B/SOURCE_CONTRACT.md',OLD/'B/CORE.md',OLD/'B/FORCED_SECTORS.md',
 OLD/'A/PROOF.md',OLD/'A/source-positive-certificate.json',CAT,
 Path('audits/2026-10-18-smaller-bad-e1617a2/B/PROOF.md'),
 Path('audits/2026-10-14-c4-return-branches-a11d4bb/pq/PROOF.md'),
 Path('audits/2026-10-14-lowpq-source-676b102/pq/PROOF.md'),
 Path('audits/2026-10-14-c4-mask13-joint6-fdd3e22/SOURCE_GEOMETRY.md'),
)

def growth(n,p=(0,)):
    if len(p)==n:
        yield p
    else:
        for c in range(min(3,max(p)+1)+1):
            yield from growth(n,p+(c,))

def pocket(arc):
    n=len(arc)
    cases=[]
    for ds in m.triangulations(n):
        deg=[2]*n
        for i,j in ds:
            deg[i]+=1;deg[j]+=1
        cases.append({'type':'empty','diagonals':[list(d) for d in ds],
                      'degrees':deg,'admissible':all(deg[i]>=MINDEG[arc[i]] for i in range(1,n-1))})
    if n==5:
        cases.append({'type':'W5','diagonals':[],'degrees':[3]*5,
                      'admissible':all(3>=MINDEG[j] for j in arc[1:-1])})
    return cases

def geometry(ten,controls):
    pockets=[]
    forbidden=[]
    possible=[]
    for i,j in itertools.combinations(range(10),2):
        if j-i in (1,9):
            continue
        arcs=[list(range(i,j+1)),list(range(j,10))+list(range(i+1))]
        records=[{'arc':[PINS[k] for k in arc],'cases':pocket(arc)} for arc in arcs if len(arc)<=5]
        blocked=any(not any(case['admissible'] for case in rec['cases']) for rec in records)
        name=PINS[i]+PINS[j]
        if blocked:
            forbidden.append(name)
        elif name not in ('ac','ns'):
            possible.append(name)
        pockets.append({'chord':name,'short_arcs':records,'short_rule_forbidden':blocked})
    assert len(forbidden)==27
    assert possible==['Rv','Ls','Lv','Lw','qs','qt']
    chord_fibres=[]
    for rec in controls:
        z=rec['core_counts']
        sums={name:sum(z[r] for r,u in enumerate(ten) if u[PINS.index(name[0])]==u[PINS.index(name[1])]) for name in possible}
        assert all(v>0 for v in sums.values())
        chord_fibres.append({'name':rec['name'],'fixed_representative_equal_colour_sums':sums,
                             'necessary_core_if_realized':'induced C10','source_realized':False})
    return {'pin_order':list(PINS),'minimum_original_q_degree':6,'minimum_core_degrees':list(MINDEG),
            'pockets':pockets,'short_rule_forbidden':forbidden,'additional_original_non_edges':['ac','ns'],
            'possible_chords':possible,'control_chord_fibres':chord_fibres}

def quotient_interfaces(eight):
    ix={e:i for i,e in enumerate(eight)}
    records=[]
    pairs={'p':(('a','q'),('a','h'),('b','h'),('b','n'),('q','n')),
           'h':(('p','L'),('p','R'),('q','R'),('q','n'),('L','n'))}
    for deleted in ('p','h'):
        survivor='h' if deleted=='p' else 'p'
        for u,v in pairs[deleted]:
            fibres=[]
            for row in m.ROWS:
                x,y,a,b,c=map(int,row)
                entries=[]
                for n,right,left,q,s in itertools.product(range(4),repeat=5):
                    e=(a,n,right,left,q,c,x,y)
                    if not m.proper(e) or b in (a,c,q):
                        continue
                    f=dict(a=a,b=b,c=c,n=n,R=right,L=left,q=q)
                    f[survivor]=s
                    if f[u]!=f[v]:
                        continue
                    bad=(q,left,right,n) if deleted=='p' else (a,b,q,n)
                    if s not in bad:
                        entries.append([ix[m.canonical(e)],n,right,left,q,s])
                fibres.append({'word':row,'entries':entries})
            records.append({'name':f'del_{deleted}__{u}_eq_{v}','operation':{'delete':deleted,'identify':[u,v]},
                            'interior_delta':-2,'surviving_cap_vertex':survivor,
                            'entry_fields':['C8_id','n','R','L','q',survivor],'fibres':fibres})
    return records

def filling_interfaces(eight):
    ix={e:i for i,e in enumerate(eight)}
    records=[]
    for ti,ds in enumerate(m.triangulations()):
        fibres=[]
        for row in m.ROWS:
            x,y,a,b,c=map(int,row)
            entries=[]
            for n,right,left,q in itertools.product(range(4),repeat=4):
                e=(a,n,right,left,q,c,x,y)
                rim=(a,b,q,left,right,n)
                if m.proper(e) and b not in (a,c,q) and all(rim[i]!=rim[j] for i,j in ds):
                    entries.append([ix[m.canonical(e)],n,right,left,q])
            fibres.append({'word':row,'entries':entries})
        records.append({'name':f'left_T{ti:02d}','delete':['p','h'],'rim':['a','b','q','L','R','n'],
                        'diagonals':[list(d) for d in ds],'interior_delta':-2,
                        'entry_fields':['C8_id','n','R','L','q'],'fibres':fibres})
    return records

def project(records,controls,K):
    result=[]
    for control in controls:
        e=control['exterior_counts']
        entries=[]
        for graph in records:
            ns=[sum(e[entry[0]] for entry in f['entries']) for f in graph['fibres']]
            support=m.mask(ns)
            entries.append({'graph':graph['name'],'counts':ns,'support':support,'in_K132':support in K})
        result.append({'name':control['name'],'source_realized':False,'graphs':entries})
    return result

def compute():
    seal=json.loads((HERE/'INPUTS.json').read_text())
    hashes={str(p):hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in INPUTS}
    assert seal=={'base':BASE,'inputs':hashes},'BASE input hashes'
    eight=[e for e in growth(8) if m.proper(e)]
    ten=[e for e in growth(10) if m.proper(e)]
    assert len(eight)==274 and len(ten)==2461
    controls=json.loads((ROOT/OLD/'A/source-positive-certificate.json').read_text())['records']
    assert [c['name'] for c in controls]==['Q2_source_positive','allK_source_positive']
    K=set(map(int,json.loads((ROOT/CAT).read_text())['cells']))
    assert len(K)==132 and 941 not in K and 1023 in K
    quotients=quotient_interfaces(eight)
    fillings=filling_interfaces(eight)
    projected_q=project(quotients,controls,K)
    projected_f=project(fillings,controls,K)
    for rec in projected_q:
        bad=[g['graph'] for g in rec['graphs'] if not g['in_K132']]
        assert bad==(['del_h__L_eq_n'] if rec['name']=='Q2_source_positive' else [])
    assert all(g['in_K132'] for rec in projected_f for g in rec['graphs'])
    return {'base':BASE,'source_realized':False,'main_target_proved':False,
            'input_manifest_sha256':hashlib.sha256((HERE/'INPUTS.json').read_bytes()).hexdigest(),
            'C8_rows':[list(e) for e in eight],'literal_frame':['x','y','a','b','c'],'words':list(m.ROWS),
            'geometry':geometry(ten,controls),'quotient_interfaces':quotients,
            'filling_interfaces':fillings,'quotient_control_projections':projected_q,
            'filling_control_projections':projected_f}

def verify(cert,expected):
    assert cert==expected,'complete source geometry, operations, literal fibres, all lifts and same-control counts'

def negatives(cert,expected):
    records=[]
    def reject(name,mutate):
        wrong=copy.deepcopy(cert)
        mutate(wrong)
        try:
            verify(wrong,expected)
        except AssertionError:
            records.append({'name':name,'rejected':True})
        else:
            raise AssertionError('accepted bad certificate '+name)
    reject('omit-original-q-degree-lemma',lambda c:c['geometry'].__setitem__('minimum_original_q_degree',5))
    reject('forget-completed-identification-cost',lambda c:c['quotient_interfaces'][0].__setitem__('interior_delta',-1))
    reject('silently-assume-c-at-least-five',lambda c:c['geometry']['minimum_core_degrees'].__setitem__(5,3))
    reject('lose-one-complete-survivor-lift',lambda c:c['quotient_interfaces'][0]['fibres'][0]['entries'].pop())
    reject('splice-counts-from-another-source',lambda c:c['quotient_control_projections'][0].__setitem__('graphs',c['quotient_control_projections'][1]['graphs']))
    return records

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--build',action='store_true')
    ap.add_argument('--certificate',type=Path,default=HERE/'certificate.json')
    args=ap.parse_args()
    expected=compute()
    if args.build:
        with args.certificate.open('x') as out:
            json.dump(expected,out,ensure_ascii=False,separators=(',',':'))
            out.write('\n')
    cert=json.loads(args.certificate.read_text())
    verify(cert,expected)
    nc=negatives(cert,expected)
    print(json.dumps({'ok':True,'short_pockets':len(cert['geometry']['pockets']),
                      'possible_chords':cert['geometry']['possible_chords'],
                      'completed_quotients':10,'completed_left_fillings':14,
                      'control_source_realizations':0,'main_target_proved':False,
                      'negative_controls':nc},ensure_ascii=False,sort_keys=True))

if __name__=='__main__':
    main()
