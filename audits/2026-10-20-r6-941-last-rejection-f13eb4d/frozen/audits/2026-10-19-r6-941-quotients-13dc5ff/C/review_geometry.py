#!/usr/bin/env python3
"""Independent bounded-pocket reconstruction of the arbitrary-size chord lemma."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
PINS=('a','n','R','L','q','c','s','v','w','t')
DEGREES=(3,3,4,4,3,2,4,4,4,4)

def triangulations(poly):
    if len(poly)<=3:return {()}
    result=set()
    for j in range(1,len(poly)-1):
        for first in triangulations(poly[:j+1]):
            for second in triangulations(poly[j:]):
                edges=set(first)|set(second)
                if j>1:edges.add(tuple(sorted((poly[0],poly[j]))))
                if j<len(poly)-2:edges.add(tuple(sorted((poly[j],poly[-1]))))
                result.add(tuple(sorted(edges)))
    return result

def compute():
    records=[];survivors=[]
    for i,j in itertools.combinations(range(10),2):
        if j-i in (1,9):continue
        paths=[tuple(range(i,j+1)),tuple(list(range(j,10))+list(range(0,i+1)))]
        pockets=[]
        for arc in paths:
            if not 2<=len(arc)-1<=4:continue
            m=len(arc);edges={tuple(sorted((arc[u],arc[(u+1)%m]))) for u in range(m)}
            choices=[]
            for tri in sorted(triangulations(arc)):
                es=edges|set(tri)
                degrees={x:sum(x in e for e in es) for x in arc}
                valid=all(degrees[x]>=DEGREES[x] for x in arc[1:-1])
                choices.append({'kind':'empty','diagonals':tri,'intermediate_degrees':[degrees[x] for x in arc[1:-1]],'valid':valid})
            if m==5:
                # Exactly one interior 5-wheel has one extra incident edge per rim vertex.
                deg=[3]*(m-2)
                choices.append({'kind':'W5','diagonals':(), 'intermediate_degrees':deg,'valid':all(3>=DEGREES[x] for x in arc[1:-1])})
            assert len(choices)=={3:1,4:2,5:6}[m]
            pockets.append({'arc':arc,'fillings':choices,'admissible':sum(c['valid'] for c in choices)})
        allowed=all(p['admissible'] for p in pockets)
        records.append({'pair':(i,j),'names':(PINS[i],PINS[j]),'pockets':pockets,'degree_rule_allows':allowed})
        if allowed:survivors.append((PINS[i],PINS[j]))
    # ac and ns have independent original-source exclusions.
    assert survivors==[('a','c'),('n','s'),('R','v'),('L','s'),('L','v'),('L','w'),('q','s'),('q','t')]
    envelope=[p for p in survivors if p not in [('a','c'),('n','s')]]
    assert envelope==[('R','v'),('L','s'),('L','v'),('L','w'),('q','s'),('q','t')]
    controls=json.loads((ROOT/'audits/2026-10-19-r6-941-leakage-b89c591/A/source-positive-certificate.json').read_text())['records']
    def canon(t):
        d={};return tuple(d.setdefault(x,len(d)) for x in t)
    def cycles(n,prefix=()):
        if len(prefix)==n:
            if prefix[-1]!=prefix[0]:yield prefix
            return
        for x in range(4):
            if not prefix or prefix[-1]!=x:yield from cycles(n,prefix+(x,))
    ten=sorted({canon(t) for t in cycles(10)})
    projection=[]
    for control in controls:
        sums={a+b:sum(n for t,n in zip(ten,control['core_counts']) if t[PINS.index(a)]==t[PINS.index(b)]) for a,b in envelope}
        assert all(n>0 for n in sums.values())
        projection.append({'name':control['name'],'chord_equal_colour_fibre_sums':sums,'true_source_realization_would_require':'induced C10','source_realized':False})
    return {'pin_order':PINS,'core_degree_lower_bounds':DEGREES,'all_potential_chords':records,
            'degree_rule_excluded':27,'independent_source_excluded':['ac','ns'],'envelope':envelope,'controls':projection}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--build',action='store_true');ap.add_argument('--certificate',type=Path,default=HERE/'geometry-review.json');args=ap.parse_args()
    result=json.loads(json.dumps(compute()))
    if args.build:
        with args.certificate.open('x') as f:json.dump(result,f,separators=(',',':'));f.write('\n')
    assert json.loads(args.certificate.read_text())==result
    reviewed=json.loads((HERE.parent/'B/certificate.json').read_text())['geometry']
    assert reviewed['minimum_core_degrees']==result['core_degree_lower_bounds']
    assert reviewed['possible_chords']==[''.join(pair) for pair in result['envelope']]
    for old,new in zip(reviewed['pockets'],result['all_potential_chords']):
        assert old['chord']==''.join(new['names'])
        assert old['short_rule_forbidden']==(not new['degree_rule_allows'])
        assert len(old['short_arcs'])==len(new['pockets'])
        for arc0,arc1 in zip(old['short_arcs'],new['pockets']):
            assert arc0['arc']==[PINS[i] for i in arc1['arc']]
            old_cases={}
            for case in arc0['cases']:
                ds=tuple(tuple(sorted((arc1['arc'][i],arc1['arc'][j]))) for i,j in case['diagonals'])
                old_cases[(case['type'],tuple(sorted(ds)))]=(case['degrees'][1:-1],case['admissible'])
            new_cases={(case['kind'],tuple(map(tuple,case['diagonals']))):(case['intermediate_degrees'],case['valid']) for case in arc1['fillings']}
            assert old_cases==new_cases
    for old,new in zip(reviewed['control_chord_fibres'],result['controls']):
        assert old['name']==new['name']
        assert old['fixed_representative_equal_colour_sums']==new['chord_equal_colour_fibre_sums']
    print(json.dumps({'status':'PASS','potential_chords':35,'degree_excluded':27,'other_source_excluded':2,'envelope':result['envelope'],'controls':result['controls'],'sha256':hashlib.sha256(args.certificate.read_bytes()).hexdigest()},sort_keys=True))

if __name__=='__main__':main()
