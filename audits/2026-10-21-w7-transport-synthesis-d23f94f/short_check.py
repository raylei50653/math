#!/usr/bin/env python3
"""Independent compact proof verifier: eight conditional edge-zero proofs.

The same-source nonnegative equation 2 Z_i = sum X_j is the only propagation
rule. Every full incident column is checked against the frozen original family.
"""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
from independent import read_inputs, require

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
EDGES=[['u3','v'],['u1','v'],['u3','w'],['u1','w'],
       ['u4','v'],['u3','s'],['u2','v'],['u2','w']]
SCOPE='same original 941/Q1 acceptance-zero/J1 type-III five-edge strict only-R/W7 source'


def canonical_halfrow(h):
    colors=[(h >> (2*(12-i)))&3 for i in range(13)]
    mapping={}
    return [mapping.setdefault(c,len(mapping)) for c in colors]


def verify(cert, caps, orbit, profiles):
    require(len(orbit['columns'])==307197 and orbit['coefficients_per_row']==4 and
            orbit['full_half_row_size']==8,'the same-source equation coefficients changed')
    require(cert['scope']=='eight separately conditional original-edge exclusions','invalid proof collection scope')
    require([b['original_edge'] for b in cert['branches']]==EDGES,'an original-edge premise changed or was omitted')
    rowstate=dict(orbit['rowids'])
    needed={n['halfrow'] for b in cert['branches'] for n in b['rules']}
    incident={h:[] for h in needed}
    for j,column in enumerate(orbit['columns']):
        for h in needed.intersection(column): incident[h].append(j)
    covered=set(); summaries=[]
    for branch in cert['branches']:
        require(branch['scope']==SCOPE,'a branch source scope changed')
        edge=branch['original_edge']; i,k=[caps['ordered_rim'].index(v) for v in edge]
        zero=set()
        for s in branch['direct_zero_states']:
            require(type(s) is int and 0<=s<len(caps['states']),'invalid direct zero state')
            require(caps['states'][s][i]==caps['states'][s][k],'a proper edge was used as a zero seed')
            zero.add(s)
        for node in branch['rules']:
            s,h=node['state'],node['halfrow']
            require(type(s) is int and type(h) is int and rowstate.get(h)==s,'invalid state/half-row assignment')
            require(canonical_halfrow(h)==caps['states'][s],'half-row normalization disagrees')
            pairs=node['column_zero_halfrows']
            require(all(type(j) is int and type(w) is int for j,w in pairs),'noninteger proof incidence')
            require([j for j,w in pairs]==incident[h] and bool(pairs),'incomplete full incident-column coverage')
            for j,w in pairs:
                require(w in orbit['columns'][j] and rowstate.get(w) in zero,'a column lacks an earlier zero-fibre witness')
            zero.add(s)
        require({44459,44466}<=zero,'the complete positive witness sum is not zero')
        for j in branch['zero_columns']:
            require(type(j) is int and any(rowstate[h] in zero for h in orbit['columns'][j]),'the requested X has no zero witness')
        ids=[]
        for p in profiles['profiles']:
            if any(p['retained_columns'].values()) and any(set(c)==set(edge) for c in p['original_chords']):
                ids.append(p['original_profile_id']); covered.add(p['original_profile_id'])
        summaries.append({'original_edge':edge,'direct_zero_count':len(branch['direct_zero_states']),
                          'derived_zero_count':len(branch['rules']),'all_incident_branches':sum(len(n['column_zero_halfrows']) for n in branch['rules']),
                          'covered_original_profile_ids':ids,'zero_columns':branch['zero_columns']})
    original={p['original_profile_id'] for p in profiles['profiles'] if any(p['retained_columns'].values())}
    require(len(original)==40 and sorted(original-covered)==[0,1],'the proved edge cover does not leave exactly profiles0/1')
    return {'result':'PASS: eight separate same-source edge-zero proofs','branches':summaries,
            'covered_profile_count':len(covered),'remaining_profiles':[0,1],
            'general_W7':'OPEN','general_J1_J2':'OPEN','new_Lean':False}


def controls(cert, inputs):
    mutations=[('omitted complete incident column',lambda b:b['branches'][2]['rules'][-1]['column_zero_halfrows'].pop()),
               ('wrong original edge',lambda b:b['branches'][3].__setitem__('original_edge',['u1','v'])),
               ('proper fibre as zero seed',lambda b:b['branches'][2]['direct_zero_states'].__setitem__(0,44466)),
               ('wrong zero halfrow',lambda b:b['branches'][2]['rules'][-1]['column_zero_halfrows'][0].__setitem__(1,6712722)),
               ('boolean column id',lambda b:b['branches'][2]['rules'][0]['column_zero_halfrows'][0].__setitem__(0,True)),
               ('broadened source domain',lambda b:b['branches'][2].__setitem__('scope','all C13 disks'))]
    for name,mutation in mutations:
        bad=deepcopy(cert); mutation(bad)
        try: verify(bad,*inputs)
        except (ValueError,KeyError,IndexError): pass
        else: raise ValueError('negative control accepted: '+name)
    return [name+' rejected' for name,mutation in mutations]


def main():
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--controls',action='store_true'); args=parser.parse_args()
    for r in json.loads((HERE/'SHORT_INPUTS.json').read_text()):
        raw=(ROOT/r['path']).read_bytes()
        require(len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256'],'branch certificate drift: '+r['path'])
    inputs=read_inputs(); cert=json.loads((HERE/'short-proofs.json').read_text()); result=verify(cert,*inputs)
    if args.controls: result['negative_controls']=controls(cert,inputs)
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__': main()
