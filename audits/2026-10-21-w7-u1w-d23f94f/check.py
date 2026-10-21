#!/usr/bin/env python3
"""Original-edge u1w exclusion by complete incident-column coverage.

Every rule ranges over the original 307197-column family.  Each case carries
its full partition and one literal whole-component operation to an earlier
zero fibre.  No graph relabeling, LP, or actual-graph enumeration is used.
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
SCOPE = 'same original 941/J1 strict only-R/W7 core with actual original edge u1w'
NAMES = ['a','n','u4','u3','u2','u1','L','q','c','s','v','w','t']
PROFILES = [96,97,100,101]
# The proof order is topological. Each entry explicitly covers the whole
# original incidence family, including columns already killed by u1w.
RULES = [
    (44722,12292509,[(306623,44740),(306626,44740)]),
    (45945,12283489,[(304587,42071),(304588,42071),(304669,42118)]),
    (65628,12021345,[(261890,27309),(261893,27309),(262147,27356),
        (263979,27309),(276925,27309),(276926,27309),(277007,27356)]),
    (45034,10073827,[(152303,44722),(152304,44722),(152306,45945),
        (152307,45945),(152308,65628),(152310,45945),(169872,44722),
        (170670,45945),(170679,45945),(227631,45945),(227642,45945),
        (227655,44722),(227656,45945),(228263,65628),(228269,65628),
        (232035,44722),(232167,45945),(232169,45945)]),
    (44466,6712722,[(43335,44459),(43336,44459),(43380,28064),
        (43381,28064),(48620,44459),(48647,45034),(66584,44459),
        (66602,42826),(67756,44459),(67765,45034)]),
]
DIRECT_ZEROS = [27309,27356,28064,42071,42118,42826,44459,44740]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def decode(row):
    return [(row >> (2*(12-i))) & 3 for i in range(13)]


def encode(row):
    return sum(c << (2*(12-i)) for i,c in enumerate(row))


def canonical(row):
    mapping = {}
    return [mapping.setdefault(c,len(mapping)) for c in row]


def normalize(row, mate):
    other = [c for c in (1,2,3) if c != mate]
    first = {0:0,mate:1,other[0]:2,other[1]:3}
    value = [first[c] for c in row]
    a = value[0]
    b = next(c for c in value if c//2 != a//2)
    second = {a:0,a^1:1,b:2,b^1:3}
    literal_to_normal = {c:second[first[c]] for c in range(4)}
    return encode([literal_to_normal[c] for c in row]), literal_to_normal


def recover(column):
    rows = [decode(h) for h in column]
    reference = rows[0]
    groups = defaultdict(list)
    for i in range(13):
        require(all(t[i]//2 == reference[i]//2 for t in rows),
                'a complete column changed palette membership')
        profile = tuple((t[i]^reference[i]) & 1 for t in rows)
        groups[(reference[i]//2,profile)].append(i)
    blocks = sorted(groups.values(),key=lambda b:b[0])
    anchors = [next(j for j,b in enumerate(blocks)
                    if reference[b[0]]//2==p) for p in (0,1)]
    generated = [column[0]]
    for j,block in enumerate(blocks):
        if j not in anchors:
            mask = sum(1 << (2*(12-i)) for i in block)
            generated += [h^mask for h in generated]
    require(sorted(generated)==column,
            'recovered components do not regenerate all and only the full column')
    return blocks


def load():
    manifest = json.loads((HERE/'BASE.json').read_text())
    require(manifest['base']==BASE,'BASE changed')
    frozen = {entry['path']:entry for entry in manifest['inputs']}
    hashes, values = {}, {}
    for name,entry in frozen.items():
        data = (ROOT/name).read_bytes()
        digest = sha256(data).hexdigest()
        require(len(data)==entry['bytes'] and digest==entry['sha256'],
                'frozen source drift: '+name)
        hashes[name] = digest
        if name.endswith('.gz'):
            values[name] = json.loads(gzip.decompress(data))
        elif name.endswith('.json'):
            values[name] = json.loads(data)
    require(hashes[SOURCE+'/counting/orbits.json.gz']==FAMILY_SHA,
            'the original unaugmented family has been replaced')
    caps = values[SOURCE+'/counting/caps.json.gz']
    orbit = values[SOURCE+'/counting/orbits.json.gz']
    require(caps['ordered_rim']==NAMES,'the original ordered rim changed')
    require(len(orbit['columns'])==307197,'the complete original family changed')
    require(orbit['coefficients_per_row']==4 and orbit['full_half_row_size']==8,
            'the full-fibre count coefficients changed')
    wanted = {h for s,h,cases in RULES}
    wanted.add(12302051)
    incidence = {h:[] for h in wanted}
    for j,column in enumerate(orbit['columns']):
        for h in wanted.intersection(column):
            incidence[h].append(j)
    return hashes,caps,orbit,values[PROFILE],incidence


def action(column, source_state, source_halfrow, target_halfrow, caps):
    literal = caps['states'][source_state]
    normalizers = [normal for mate in (1,2,3)
                   for h,normal in [normalize(literal,mate)] if h==source_halfrow]
    require(len(normalizers)==1,'a source half-row lacks a unique literal palette')
    to_literal = {v:k for k,v in normalizers[0].items()}
    source = decode(source_halfrow)
    target = decode(target_halfrow)
    require([to_literal[c] for c in source]==literal,'literal source changed')
    flips = []
    for block in recover(column):
        changed = {source[i]^target[i] for i in block}
        require(changed in ({0},{1}),'an action split a whole actual component')
        if changed=={1}:
            p = source[block[0]]//2
            flips.append({'palette':sorted([to_literal[2*p],to_literal[2*p+1]]),
                          'boundary_contacts':[NAMES[i] for i in block]})
    result = list(literal)
    for operation in flips:
        a,b = operation['palette']
        for name in operation['boundary_contacts']:
            i = NAMES.index(name)
            result[i] ^= a^b
    endpoint = [to_literal[c] for c in target]
    require(result==endpoint,'whole-component action has the wrong literal endpoint')
    require(canonical(endpoint)==canonical(target),
            'the global frame permutation has changed a fibre')
    return {'source_literal_tuple':literal,'endpoint_literal_tuple':endpoint,
            'whole_actual_components_flipped':flips}


def proposal(inputs):
    hashes,caps,orbit,parent,incidence = inputs
    row_state = dict(orbit['rowids'])
    rules = []
    used = {306993}
    for state,h,cases in RULES:
        covered = []
        for j,zero_state in cases:
            used.add(j)
            matches = [k for k in orbit['columns'][j] if row_state[k]==zero_state]
            require(len(matches)==1,'the chosen zero fibre is not a unique full half-row')
            k = matches[0]
            covered.append({'column_id':j,'zero_state':zero_state,'zero_halfrow':k,
                            'actual_action':action(orbit['columns'][j],state,h,k,caps)})
        rules.append({'state':state,'literal_tuple':caps['states'][state],
                      'halfrow':h,'all_incident_columns':incidence[h],
                      'complete_case_cover':covered})
    columns = []
    for j in sorted(used):
        col = orbit['columns'][j]
        columns.append({'column_id':j,'all_half_rows':col,
                        'all_canonical_states':[row_state[h] for h in col],
                        'all_boundary_components':[[NAMES[i] for i in block]
                                                    for block in recover(col)]})
    table = {r['original_profile_id']:r for r in parent['profiles']}
    return {'scope':SCOPE,'base':BASE,'input_sha256':hashes,'original_edge':['u1','w'],
        'original_ordered_rim':NAMES,'all_original_columns_scanned':307197,
        'direct_zero_fibres':[{'state':s,'literal_tuple':caps['states'][s]}
                              for s in DIRECT_ZEROS],
        'topologically_ordered_rules':rules,'complete_columns':columns,
        'original_profiles':[{'original_profile_id':s,
                              'all_original_chords':table[s]['original_chords']}
                             for s in PROFILES],
        'zero_columns':[48647,67765],'positive_original_witness_sum':[44459,44466],
        'first_B03_operation':{'source_state':44466,'source_halfrow':12302051,
             'all_incident_columns':incidence[12302051],
             'to_state':44107,'to_halfrow':12301239,
             'actual_action':action(orbit['columns'][306993],44466,12302051,12301239,caps)},
        'graph_or_vertex_symmetry_used':False,'LP_used':False,
        'actual_original_graph_enumeration_used':False,
        'source_realizability_claimed':False,'new_Lean':False,
        'general_strict_W7':'OPEN','general_J1_J2':'OPEN','smaller_bad':'OPEN'}


def verify(cert, inputs):
    hashes,caps,orbit,parent,incidence = inputs
    require(cert['scope']==SCOPE and cert['base']==BASE,'the source scope or BASE changed')
    require(cert['input_sha256']==hashes,'source authority hashes changed')
    require(cert['original_edge']==['u1','w'],'the actual original edge changed')
    require(cert['original_ordered_rim']==NAMES,'the original color frame changed')
    require(cert['all_original_columns_scanned']==len(orbit['columns']),
            'the complete original family was not consumed')
    row_state = dict(orbit['rowids'])
    table = {r['original_profile_id']:r for r in parent['profiles']}
    require([r['original_profile_id'] for r in cert['original_profiles']]==PROFILES,
            'the four fixed original profiles were not covered')
    for record in cert['original_profiles']:
        p = table[record['original_profile_id']]
        require(record['all_original_chords']==p['original_chords'] and
                ['u1','w'] in record['all_original_chords'],
                'a fixed original profile lost an edge or an attachment')
        require(p['retained_columns']=={'44459_only':[], '44466_only':[48647,67765], 'shared':[]},
                'the fixed target support changed')
    zeros = set()
    require([r['state'] for r in cert['direct_zero_fibres']]==DIRECT_ZEROS,
            'direct zero terminal fibres changed')
    for record in cert['direct_zero_fibres']:
        state = record['state']
        require(type(state) is int and record['literal_tuple']==caps['states'][state],
                'a direct-zero literal tuple changed')
        require(record['literal_tuple'][5]==record['literal_tuple'][11],
                'an alleged original-edge zero is actually proper')
        zeros.add(state)
    rules = cert['topologically_ordered_rules']
    require([r['state'] for r in rules]==[r[0] for r in RULES],
            'the proof rules lost their topological source coverage')
    used = {306993}
    all_actions = 0
    for record in rules:
        state,h = record['state'],record['halfrow']
        require(type(state) is int and type(h) is int and row_state.get(h)==state,
                'a source half-row has the wrong canonical state')
        require(record['literal_tuple']==caps['states'][state] and
                canonical(decode(h))==record['literal_tuple'],
                'a source literal tuple changed')
        require(record['all_incident_columns']==incidence[h] and bool(incidence[h]),
                'the complete original incident-column family was truncated')
        cases = record['complete_case_cover']
        require([r['column_id'] for r in cases]==incidence[h],
                'a complete column is missing its same-source zero witness')
        for case in cases:
            j,k,s = case['column_id'],case['zero_halfrow'],case['zero_state']
            require(all(type(x) is int for x in (j,k,s)),
                    'proof column IDs, half-rows, and states must be exact integers')
            require(k in orbit['columns'][j] and row_state[k]==s and s in zeros,
                    'a full column lacks an earlier same-source zero fibre')
            require(case['actual_action']==action(orbit['columns'][j],state,h,k,caps),
                    'a literal operation omitted or changed a whole actual component')
            endpoint = case['actual_action']['endpoint_literal_tuple']
            require(canonical(endpoint)==caps['states'][s],
                    'the complete actual action enters the wrong zero fibre')
            used.add(j)
            all_actions += 1
        zeros.add(state)
    require(cert['zero_columns']==[48647,67765] and
            cert['positive_original_witness_sum']==[44459,44466] and
            {44459,44466} <= zeros,'the original positive witness was not contradicted')
    for j in cert['zero_columns']:
        require(6712722 in orbit['columns'][j],'a target column lost its B-zero half-row')
    columns = cert['complete_columns']
    require([r['column_id'] for r in columns]==sorted(used),
            'the proof omitted a complete component partition')
    for record in columns:
        j = record['column_id']
        require(record['all_half_rows']==orbit['columns'][j] and
                record['all_canonical_states']==[row_state[h] for h in orbit['columns'][j]],
                'the complete full-column state list was changed')
        require(record['all_boundary_components']==
                [[NAMES[i] for i in block] for block in recover(orbit['columns'][j])],
                'the complete actual component contacts changed')
    first = cert['first_B03_operation']
    require(first==proposal(inputs)['first_B03_operation'],
            'the independent literal B03 operation changed')
    require(first['all_incident_columns']==[306993] and
            row_state[first['to_halfrow']]==44107,'the original B03 first step changed')
    for key in ('graph_or_vertex_symmetry_used','LP_used',
                'actual_original_graph_enumeration_used','source_realizability_claimed','new_Lean'):
        require(cert[key] is False,'an unsupported authority or method was introduced')
    require(all(cert[k]=='OPEN' for k in ('general_strict_W7','general_J1_J2','smaller_bad')),
            'a parent source gap was closed without evidence')
    return {'result':'PASS: four original u1w profiles excluded',
        'original_profile_ids':PROFILES,'zero_target_states':[44459,44466],
        'zero_target_columns':[48647,67765],'topological_rule_states':[r[0] for r in RULES],
        'complete_rule_incidence_sizes':[len(r[2]) for r in RULES],
        'all_original_columns_scanned':len(orbit['columns']),
        'complete_partitions_regenerated':len(columns),'literal_whole_component_actions':all_actions,
        'graph_symmetry_used':False,'LP_used':False,'general_W7':'OPEN','general_J1_J2':'OPEN'}


def controls(cert, inputs):
    variants = [
        ('omitted_incident_column', lambda p:p['topologically_ordered_rules'][3]['all_incident_columns'].pop()),
        ('omitted_case_witness', lambda p:p['topologically_ordered_rules'][4]['complete_case_cover'].pop()),
        ('only_endpoint_swapped',lambda p:p['topologically_ordered_rules'][3]['complete_case_cover'][0]
             ['actual_action']['whole_actual_components_flipped'].clear()),
        ('wrong_original_edge',lambda p:p.__setitem__('original_edge',['u1','v'])),
        ('omitted_source_profile',lambda p:p['original_profiles'].pop()),
        ('bool_column_id',lambda p:p['topologically_ordered_rules'][0]['complete_case_cover'][0]
             .__setitem__('column_id',True)),
        ('proper_fibre_as_edge_zero',lambda p:p['direct_zero_fibres'][0]
             .__setitem__('literal_tuple',[0,1,2,1,2,1,2,3,1,2,1,0,2])),
        ('unrestricted_C13_claim',lambda p:p.__setitem__('scope','all C13 disks')),
    ]
    rejected = []
    for name,mutate in variants:
        corrupt = deepcopy(cert)
        mutate(corrupt)
        try:
            verify(corrupt,inputs)
        except (ValueError,KeyError,IndexError):
            rejected.append(name)
    require(len(rejected)==len(variants),'a corrupted proof was accepted')
    return rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build',action='store_true')
    parser.add_argument('--controls',action='store_true')
    parser.add_argument('--certificate',type=Path)
    args = parser.parse_args()
    require(not(args.build and args.certificate),'build and custom certificate are incompatible')
    inputs = load()
    path = args.certificate or HERE/'certificate.json'
    cert = proposal(inputs) if args.build else json.loads(path.read_text())
    result = verify(cert,inputs)
    if args.controls:
        result['corrupt_proofs_rejected'] = controls(cert,inputs)
    if args.build:
        with path.open('x') as stream:
            json.dump(cert,stream,indent=2,sort_keys=True)
            stream.write('\n')
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
