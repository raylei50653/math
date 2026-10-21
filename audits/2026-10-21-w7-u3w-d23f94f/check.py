#!/usr/bin/env python3
"""Exact whole-component, complete-incidence exclusion of original u3w.

This small proof uses the original 307197-column family.  It does not consume
any added u3v/u1v zeros, a support-closure transcript, or a graph symmetry.
"""
from collections import defaultdict
from copy import deepcopy
from hashlib import sha256
from pathlib import Path
import argparse
import gzip
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = 'audits/2026-10-20-r6-941-j1-five-edge-417732f'
PROFILE = 'audits/2026-10-21-w7-structural-30f2d19/review/profile_orbits.json'
BASE = 'd23f94f739468593db653ec03f903c30adfd5fb0'
FAMILY_SHA = '542ee11de93a846bfbc321b098214b153c5b600318ba2e0bc5621a73ad2a55ad'
RIM = ['a','n','u4','u3','u2','u1','L','q','c','s','v','w','t']
IDS = [16,17,46,47,62,63,66,67]
SCOPE = 'complete 941/J1 strict only-R/W7 source with actual original edge u3w'
# Topological proof order. Each pair is (complete original column, zero state).
SPECS = [
    (49643,12161437,[(295461,38163),(295476,38159),(300558,50413),
                    (300559,50393),(300567,48769),(301428,49645),(301431,49641)]),
    (60707,11955809,[(261889,22388),(261890,22388),(261892,22388),
                    (261893,22388),(261894,22388),(262146,22435),(262147,22435)]),
    (49955,10204899,[(194216,49643),(194217,60707),(238063,49643),
                    (238195,60707),(238197,60707)]),
    (44466,6712722,[(43335,28064),(43336,28064),(43380,28064),(43381,28064),
                   (48620,29704),(48647,29704),(66584,42819),(66602,49955),
                   (67756,44459),(67765,49955)]),
]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def packed(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'))


def decode(h):
    return [(h >> (2*(12-i))) & 3 for i in range(13)]


def encode(t):
    return sum(c << (2*(12-i)) for i,c in enumerate(t))


def canonical(t):
    mapping = {}
    out = []
    for c in t:
        if c not in mapping:
            mapping[c] = len(mapping)
        out.append(mapping[c])
    return out


def halfrow(t,mate):
    other = [c for c in (1,2,3) if c != mate]
    perm = {0:0,mate:1,other[0]:2,other[1]:3}
    u = [perm[c] for c in t]
    a = u[0]
    b = next(c for c in u if c//2 != a//2)
    normal = {a:0,a^1:1,b:2,b^1:3}
    return encode([normal[c] for c in u])


def components(column):
    rows = [decode(h) for h in column]
    first = rows[0]
    groups = defaultdict(list)
    for i in range(13):
        require(all(row[i]//2==first[i]//2 for row in rows),
                'one column changed its literal palette membership')
        groups[(first[i]//2,tuple((row[i]^first[i])&1 for row in rows))].append(i)
    blocks = sorted(groups.values(),key=lambda block:block[0])
    anchors = [next(j for j,block in enumerate(blocks) if first[block[0]]//2==p)
               for p in (0,1)]
    generated = [column[0]]
    for j,block in enumerate(blocks):
        if j not in anchors:
            mask = sum(1 << (2*(12-i)) for i in block)
            generated += [h^mask for h in generated]
    require(sorted(generated)==column,
            'whole recovered component flips fail to regenerate the complete column')
    return blocks


def literal_operation(t,h,k,blocks):
    source,target = decode(h),decode(k)
    half_to_literal = {}
    for a,b in zip(source,t):
        require(a not in half_to_literal or half_to_literal[a]==b,
                'the current literal color frame is inconsistent')
        half_to_literal[a] = b
    require(len(half_to_literal)==4, 'the four-color frame was lost')
    out = list(t)
    operations = []
    for block in blocks:
        differences = {source[i]^target[i] for i in block}
        require(differences in ({0},{1}), 'a proposed row flips only part of a component')
        if differences=={1}:
            p = source[block[0]]//2
            pair = sorted([half_to_literal[2*p],half_to_literal[2*p+1]])
            for i in block:
                out[i] = pair[0]^pair[1]^out[i]
            operations.append({'palette':pair,'boundary_contacts':[RIM[i] for i in block]})
    require(out==[half_to_literal[a] for a in target], 'the literal whole-component action differs')
    # Apply the identical full-component swaps in reverse. Private vertices in
    # each actual component travel with it; boundary-free components are fixed.
    back = list(out)
    for action in reversed(operations):
        x,y = action['palette']
        for name in action['boundary_contacts']:
            i = RIM.index(name)
            back[i] = x^y^back[i]
    require(back==t, 'the literal action is not an involution')
    return {'source_literal_tuple':t,'whole_actual_component_swaps':operations,
            'result_literal_tuple':out,'result_canonical_tuple':canonical(out)}


def load():
    manifest = json.loads((HERE/'BASE.json').read_text())
    require(manifest['base']==BASE, 'exclusive BASE changed')
    expected = [SOURCE+'/SOURCE_CONTRACT.md',SOURCE+'/counting/PROOF.md',
                SOURCE+'/counting/caps.json.gz',SOURCE+'/counting/orbits.json.gz',PROFILE]
    require([r['path'] for r in manifest['inputs']]==expected, 'authority inputs changed')
    values,hashes = {},{}
    for entry in manifest['inputs']:
        p = entry['path']
        data = (ROOT/p).read_bytes()
        require(len(data)==entry['bytes'] and sha256(data).hexdigest()==entry['sha256'],
                'frozen source drift: '+p)
        hashes[p] = {'bytes':len(data),'sha256':entry['sha256']}
        if p.endswith('.gz'):
            values[p] = json.loads(gzip.decompress(data))
        elif p.endswith('.json'):
            values[p] = json.loads(data)
    require(hashes[SOURCE+'/counting/orbits.json.gz']['sha256']==FAMILY_SHA,
            'the original family was replaced by an augmented residual')
    return hashes,values


def compute():
    hashes,values = load()
    caps = values[SOURCE+'/counting/caps.json.gz']
    orbit = values[SOURCE+'/counting/orbits.json.gz']
    profiles = values[PROFILE]
    require(caps['ordered_rim']==RIM, 'original ordered rim changed')
    require(len(orbit['columns'])==307197, 'original complete family size changed')
    row_state = dict(orbit['rowids'])
    needed = {h for _,h,_ in SPECS}|{12302051}
    incident = {h:[] for h in needed}
    for j,column in enumerate(orbit['columns']):
        for h in needed.intersection(column):
            incident[h].append(j)
    direct_states = sorted({w for _,_,pairs in SPECS for _,w in pairs
                            if w not in {s for s,_,_ in SPECS}})
    zeros = set(direct_states)
    for s in direct_states:
        require(caps['states'][s][3]==caps['states'][s][11],
                'a direct-zero state is proper on actual u3w')
    nodes = []
    for s,h,pairs in SPECS:
        require(row_state[h]==s and canonical(decode(h))==caps['states'][s],
                'named half-row lost its complete state')
        require(incident[h]==[j for j,_ in pairs], 'the full incident-column cover is incomplete')
        branches = []
        for j,w in pairs:
            require(w in zeros, 'the proof is not topologically justified')
            column = orbit['columns'][j]
            witnesses = [k for k in column if row_state[k]==w]
            require(bool(witnesses), 'an incident column lost its already-zero full fibre')
            k = min(witnesses)
            blocks = components(column)
            action = literal_operation(caps['states'][s],h,k,blocks)
            require(action['result_canonical_tuple']==caps['states'][w],
                    'literal transport changes the specified witness state')
            branches.append({'column_id':j,'complete_half_rows':column,
                'complete_canonical_states':[row_state[x] for x in column],
                'complete_boundary_components':[[RIM[i] for i in b] for b in blocks],
                'zero_witness_state':w,'zero_witness_halfrow':k,**action})
        nodes.append({'state':s,'literal_tuple':caps['states'][s],
                      'source_halfrow':h,'all_incident_columns':incident[h],
                      'branches':branches})
        zeros.add(s)
    require({44459,44466}<=zeros, 'the original positive witness sum was not contradicted')
    wanted = []
    for record in profiles['profiles']:
        if ['u3','w'] in record['original_chords'] and any(record['retained_columns'].values()):
            wanted.append(record)
    require([r['original_profile_id'] for r in wanted]==IDS, 'the eight source profiles changed')
    require(all(r['retained_columns']['44466_only']==[66602,67765] and
                not r['retained_columns']['44459_only'] and
                not r['retained_columns']['shared'] for r in wanted),
            'the fixed source target support changed')
    require(all(6712722 in orbit['columns'][j] for j in (66602,67765)),
            'the requested original X columns lost their zero B fibre')
    require(incident[12302051]==[306993], 'the preliminary B 03|12 family changed')
    prelim_column = orbit['columns'][306993]
    prelim_blocks = components(prelim_column)
    require([[RIM[i] for i in b] for b in prelim_blocks]==
            [['a'],['n','u4','u3','u2','u1','L','t'],['q','w'],['c','s','v']],
            'the literal B forcing was incorrectly reflected from A')
    prelim_action = literal_operation(caps['states'][44466],12302051,
                                     12301239,prelim_blocks)
    require(prelim_action['result_canonical_tuple']==caps['states'][44107],
            'the literal B first step changed')
    return {'scope':SCOPE,'base':BASE,'inputs':hashes,'ordered_rim':RIM,
        'original_edge':['u3','w'],'original_profile_ids':IDS,
        'profiles':[{'original_profile_id':r['original_profile_id'],
                     'all_original_chords':r['original_chords']} for r in wanted],
        'direct_edge_zero_states':[{'state':s,'literal_tuple':caps['states'][s]}
                                   for s in direct_states],
        'topologically_ordered_complete_incidence_proof':nodes,
        'preliminary_B_03_12':{'state':44466,'source_halfrow':12302051,
            'all_incident_columns':[306993],
            'complete_boundary_components':[[RIM[i] for i in b] for b in prelim_blocks],
            **prelim_action},
        'all_original_columns_scanned':307197,'proof_incident_columns':29,
        'zero_columns':[66602,67765],'derived_zero_states':[49643,60707,49955,44466],
        'positive_original_witness_sum':[44459,44466],
        'strict_u3w_branch_excluded':True,'general_W7_excluded':False,
        'graph_symmetry_used':False,'u3v_u1v_zeros_used':False,
        'support_closure_transcript_consumed':False,'LP_run':False,
        'new_original_graph_enumeration':False,'source_realized':False,
        'new_Lean':False}


def verify(cert,expected):
    require(packed(cert)==packed(expected), 'damaged or incomplete exact certificate')


def controls(cert):
    variants = [
        ('omit_incident_column',lambda x:x['topologically_ordered_complete_incidence_proof'][2]['all_incident_columns'].pop()),
        ('swap_only_boundary_w',lambda x:x['topologically_ordered_complete_incidence_proof'][3]['branches'][-1]['whole_actual_component_swaps'][0].__setitem__('boundary_contacts',['w'])),
        ('proper_tuple_as_direct_zero',lambda x:x['direct_edge_zero_states'][0].__setitem__('literal_tuple',[0,1,2,1,2,1,2,3,1,2,1,0,2])),
        ('wrong_original_edge',lambda x:x.__setitem__('original_edge',['u3','v'])),
        ('omit_source_profile',lambda x:x['original_profile_ids'].pop()),
        ('bool_column',lambda x:x['topologically_ordered_complete_incidence_proof'][0]['all_incident_columns'].__setitem__(0,True)),
        ('claim_general_W7',lambda x:x.__setitem__('general_W7_excluded',True)),
    ]
    rejected = []
    for name,mutate in variants:
        bad = deepcopy(cert)
        mutate(bad)
        try:
            verify(bad,cert)
        except ValueError:
            rejected.append(name)
    require(len(rejected)==len(variants), 'a corrupted proof was accepted')
    return rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build',action='store_true')
    parser.add_argument('--certificate',type=Path)
    args = parser.parse_args()
    require(not(args.build and args.certificate), 'build and alternate certificate conflict')
    result = compute()
    path = args.certificate or HERE/'certificate.json'
    if args.build:
        with path.open('x') as stream:
            json.dump(result,stream,indent=2,sort_keys=True)
            stream.write('\n')
    else:
        verify(json.loads(path.read_text()),result)
    rejected = controls(result)
    print(json.dumps({'result':'PASS: original u3w eight-profile complete-source exclusion',
        'zero_columns':result['zero_columns'],'derived_zero_states':result['derived_zero_states'],
        'profiles':IDS,'proof_incident_columns':29,'all_original_columns_scanned':307197,
        'negative_controls_rejected':rejected,'general_W7':'OPEN'},sort_keys=True))


if __name__=='__main__':
    main()
