#!/usr/bin/env python3
"""Exact u1v domination certificate using the original unaugmented family.

All three states belong to one complete original core. No graph relabeling,
u3v zero gate, numerical solver, or selected-history invariance is used.
"""
import argparse
from copy import deepcopy
import gzip
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
AUDIT = HERE.parent
SOURCE = 'audits/2026-10-20-r6-941-j1-five-edge-417732f'
PROFILE_PATH = 'audits/2026-10-21-w7-structural-30f2d19/review/profile_orbits.json'
IDS = [68,69,78,79,88,89,92,93]
SCOPE = 'complete 941/J1 strict only-R/W7 source with original edge u1v'
ORIGINAL_FAMILY_SHA = '542ee11de93a846bfbc321b098214b153c5b600318ba2e0bc5621a73ad2a55ad'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def load():
    manifest = json.loads((AUDIT/'BASE.json').read_text())
    frozen = {entry['path']:entry for entry in manifest['inputs']}
    paths = [SOURCE+'/counting/caps.json.gz', SOURCE+'/counting/orbits.json.gz', PROFILE_PATH,
             SOURCE+'/SOURCE_CONTRACT.md', SOURCE+'/counting/PROOF.md']
    values = []
    hashes = {}
    for name in paths:
        raw = (ROOT/name).read_bytes()
        require(hashlib.sha256(raw).hexdigest()==frozen[name]['sha256'] and
                len(raw)==frozen[name]['bytes'], 'frozen input drift: '+name)
        hashes[name] = frozen[name]['sha256']
        if name in paths[:3]:
            values.append(json.loads(gzip.decompress(raw) if name.endswith('.gz') else raw))
    require(hashes[paths[1]]==ORIGINAL_FAMILY_SHA,
            'the original pre-chord family was replaced by a restricted residual')
    return hashes, *values


def canonical(h):
    names = {}
    result = []
    for i in range(13):
        c = (h >> (2*(12-i))) & 3
        if c not in names:
            names[c] = len(names)
        result.append(names[c])
    return result


def proposal(hashes):
    return {'scope':SCOPE, 'input_sha256':hashes, 'original_edge':['u1','v'],
        'original_profile_ids':IDS,
        'dominations':[
            {'from_state':44459,'from_halfrow':12302027,'to_state':44111,
             'to_halfrow':12301211,'all_incident_columns':[306985]},
            {'from_state':44111,'from_halfrow':10064313,'to_state':44127,
             'to_halfrow':10064365,'all_incident_columns':[147448,147449,167802,226130,231666]}],
        'edge_zero_states':[44127,44466],
        'zero_columns':[{'id':48617,'zero_halfrow':6712710,'state':44459},
                        {'id':67755,'zero_halfrow':6712710,'state':44459}],
        'positive_original_witness_sum':[44459,44466]}


def verify(cert, inputs):
    hashes,caps,orbits,profiles = inputs
    require(cert['scope']==SCOPE, 'source scope changed')
    require(cert['original_edge']==['u1','v'], 'the actual premise edge changed')
    require(cert['input_sha256']==hashes, 'input family or source contract changed')
    require(cert['original_profile_ids']==IDS, 'eight-profile coverage changed')
    table = {row['original_profile_id']:row for row in profiles['profiles']}
    require(all(['u1','v'] in table[i]['original_chords'] for i in IDS),
            'a covered original profile lacks u1v')
    require(all(table[i]['retained_columns']['44459_only']==[48617,67755] for i in IDS),
            'the requested two-column source branch changed')
    row_state = dict(orbits['rowids'])
    needed = {step['from_halfrow'] for step in cert['dominations']}
    require(all(type(h) is int for h in needed), 'noninteger half-row')
    incident = {h:[] for h in needed}
    for j,column in enumerate(orbits['columns']):
        for h in needed.intersection(column):
            incident[h].append(j)
    for step in cert['dominations']:
        a,b,h,k = (step[name] for name in ('from_state','to_state','from_halfrow','to_halfrow'))
        require(all(type(x) is int for x in (a,b,h,k)), 'noninteger proof state')
        require(row_state.get(h)==a and row_state.get(k)==b,
                'a half-row has the wrong original state')
        require(canonical(h)==caps['states'][a] and canonical(k)==caps['states'][b],
                'independent literal normalization disagrees')
        ids = step['all_incident_columns']
        require(all(type(j) is int for j in ids) and ids==sorted(set(ids)),
                'proof columns must be unique sorted exact integers')
        require(ids==incident[h] and bool(ids), 'the full incident-column cover is incomplete')
        require(all(k in orbits['columns'][j] for j in ids), 'domination lacks its common row')
    index = {name:i for i,name in enumerate(caps['ordered_rim'])}
    zeros = set()
    for state in cert['edge_zero_states']:
        require(type(state) is int, 'noninteger zero state')
        row = caps['states'][state]
        require(row[index['u1']]==row[index['v']], 'a purported original-edge zero is proper')
        zeros.add(state)
    for step in reversed(cert['dominations']):
        require(step['to_state'] in zeros, 'the zero chain is not justified')
        zeros.add(step['from_state'])
    dead = []
    for step in cert['zero_columns']:
        j,h,s = (step[key] for key in ('id','zero_halfrow','state'))
        require(all(type(x) is int for x in (j,h,s)), 'noninteger column witness')
        require(s in zeros and row_state.get(h)==s and h in orbits['columns'][j],
                'a target column lacks a zero-fibre witness')
        dead.append(j)
    require(dead==[48617,67755], 'wrong requested columns')
    require(cert['positive_original_witness_sum']==[44459,44466] and
            all(s in zeros for s in (44459,44466)), 'the source witness sum was not contradicted')
    return {'result':'PASS: strict W7 u1v eight-profile source exclusion',
            'scope':SCOPE,'zero_columns':dead,'zero_states':sorted(zeros),
            'chain':'0<=Z44459<=Z44111<=Z44127=0',
            'all_original_columns_scanned':len(orbits['columns']),
            'covered_original_profile_ids':IDS,'extra_edge_premise':['u1','v'],
            'u3v_edge_premise_used':False,'graph_symmetry_used':False,
            'general_W7':'OPEN','general_J1_J2':'OPEN','new_Lean':False}


def controls(cert, inputs):
    variants = [
        ('missing_column',lambda p:p['dominations'][1]['all_incident_columns'].pop()),
        ('wrong_state',lambda p:p['dominations'][0].__setitem__('to_state',44480)),
        ('proper_state_as_direct_zero',lambda p:p['edge_zero_states'].__setitem__(0,44459)),
        ('wrong_original_edge',lambda p:p.__setitem__('original_edge',['u3','v'])),
        ('bool_column',lambda p:p['dominations'][0]['all_incident_columns'].__setitem__(0,True)),
        ('omitted_profile',lambda p:p['original_profile_ids'].pop()),
        ('unrestricted_source_claim',lambda p:p.__setitem__('scope','all C13 disks'))]
    rejected = []
    for name,mutate in variants:
        bad = deepcopy(cert)
        mutate(bad)
        try:
            verify(bad,inputs)
        except (ValueError,KeyError,IndexError):
            rejected.append(name)
    require(len(rejected)==len(variants), 'a damaged proof was accepted')
    return rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build',action='store_true')
    parser.add_argument('--controls',action='store_true')
    parser.add_argument('--certificate',type=Path)
    args = parser.parse_args()
    require(not(args.build and args.certificate), 'build and certificate are mutually exclusive')
    inputs = load()
    path = args.certificate or HERE/'certificate.json'
    cert = proposal(inputs[0]) if args.build else json.loads(path.read_text())
    result = verify(cert,inputs)
    if args.controls:
        result['corrupt_proofs_rejected'] = controls(cert,inputs)
    if args.build:
        with path.open('x') as stream:
            json.dump(cert,stream,indent=2)
            stream.write('\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
