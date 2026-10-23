#!/usr/bin/env python3
"""Read-only custody and exact set-system extremum replay, not source realization."""
import argparse
from copy import deepcopy
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import random

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = '6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'

def require(ok, why):
    if not ok:
        raise ValueError(why)

def custody():
    data = json.loads((HERE/'INPUTS.json').read_text())
    require(data['base']==BASE, 'BASE drift')
    routing = {}
    for row in data['inputs']:
        raw=(HERE/row['snapshot']).read_bytes()
        require((len(raw),sha256(raw).hexdigest())==(row['bytes'],row['sha256']), 'snapshot drift')
        if row['authority']=='immutable':
            require((ROOT/row['path']).read_bytes()==raw, 'live authority drift: '+row['path'])
        else:
            routing[row['path']]=raw
    prior=json.loads((HERE/'entry/audits/2026-10-23-941-types-wrong-side-round3-6b09cd4/FINAL_MANIFEST.json').read_text())
    for row in prior['entries']:
        raw=routing[row['path']] if row['path'] in routing else (ROOT/row['path']).read_bytes()
        require((len(raw),sha256(raw).hexdigest())==(row['bytes'],row['sha256']), 'predecessor drift: '+row['path'])
    return len(data['inputs']),len(prior['entries'])

def validate(cert, seed=0):
    require(cert['schema']=='941-two-complete-M2-stars-v1' and cert['base']==BASE, 'schema/BASE')
    require(cert['ordered_gamma']==['r','T','s','x','h','W','e','d'], 'literal frame')
    require(cert['degree_lower_bound']==5 and cert['q_minimum']==2, 'full original degree/domain')
    require(cert['source_controls']=='not triggered' and cert['whole_type_exclusions']==0, 'source authority')
    require(cert['global_k_lower_bound']==23, 'global bound')
    require(cert['reservoir_bound']=='q+7' and cert['exterior_bound']=='q+7+t' and cert['spectator_minimum']==1, 'claimed bound')
    # Discover the six admissible circle-neighbor sets directly from all subsets.
    options=[]
    for n in range(4):
        for a in combinations(['T','r','s'],n):
            if not {'r','s'}<=set(a):
                options.append(frozenset(a))
    expected={frozenset((a,b)) for i,a in enumerate(options) for b in options[i:]}
    seen=set(); offsets=[]; assignments=0
    rows=list(cert['rows']); random.Random(seed).shuffle(rows)
    for row in rows:
        a,b=frozenset(row['a']),frozenset(row['b'])
        require(len(a)==len(row['a']) and len(b)==len(row['b']), 'duplicate circle contact')
        require(a in options and b in options, 'forbidden circle neighbors')
        key=frozenset((a,b)); require(key not in seen, 'repeated pair case'); seen.add(key)
        sizes=[5-len(a),5-len(b)]
        require(row['outside_sizes']==sizes, 'lost full-star neighbor')
        require(row['max_common']==2-len(a&b), 'lost shared circle neighbor')
        first=set(range(sizes[0])); values=[]
        # Any two finite sets can be relabeled to put the first in this position.
        for second_tuple in combinations(range(sum(sizes)),sizes[1]):
            second=set(second_tuple); assignments+=1
            if len(first&second)+len(a&b)<=2:
                values.append(len(first|second))
        require(values and min(values)==row['minimum_union'], 'incorrect exact union extremum')
        s1,s2=map(set,row['witness'])
        require([len(s1),len(s2)]==sizes and all(len(s)==len(v) for s,v in zip((s1,s2),row['witness'])), 'incomplete star witness')
        require(len(s1&s2)+len(a&b)<=2 and len(s1|s2)==min(values), 'false extremum witness')
        require(row['reservoir_offset']==2+min(values), 'lost complete M2/outlets')
        offsets.append(row['reservoir_offset'])
    require(seen==expected and len(rows)==21, 'incomplete pair domain')
    require(min(offsets)==7, 'unproved universal offset')
    return dict(pair_cases=len(rows), outside_set_assignments=assignments,
                reservoir_minimum_for_q2=2+min(offsets), exterior_minimum_for_q2=2+min(offsets)+1,
                source_controls='not triggered', whole_type_exclusions=0, global_k_lower_bound=23)

def negatives(cert):
    changes=[('missing_pair',lambda c:c['rows'].pop()),
             ('lost_full_star_neighbor',lambda c:c['rows'][0]['outside_sizes'].__setitem__(0,4)),
             ('ignored_circle_intersection',lambda c:c['rows'][-1].__setitem__('max_common',2)),
             ('false_union_minimum',lambda c:c['rows'][0].__setitem__('minimum_union',3)),
             ('missing_witness_neighbor',lambda c:c['rows'][0]['witness'][0].pop()),
             ('false_source',lambda c:c.__setitem__('source_controls','triggered and holds')),
             ('false_type_exclusion',lambda c:c.__setitem__('whole_type_exclusions',1)),
             ('raised_global_k',lambda c:c.__setitem__('global_k_lower_bound',24))]
    rejected=[]
    for name,change in changes:
        broken=deepcopy(cert); change(broken)
        try:
            validate(broken)
        except (ValueError,KeyError,TypeError):
            rejected.append(name)
        else:
            raise ValueError('negative accepted: '+name)
    return rejected

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--certificate',type=Path,default=HERE/'pair-star-certificate.json')
    parser.add_argument('--seed',type=int,default=0); parser.add_argument('--negative',action='store_true')
    args=parser.parse_args(); n,p=custody(); cert=json.loads(args.certificate.read_text())
    result=validate(cert,args.seed)
    if args.negative:
        result['semantic_negatives_rejected']=negatives(cert)
    result.update(status='PASS',frozen_inputs=n,predecessor_manifest_entries=p,immutable_drift=0)
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':
    main()
