#!/usr/bin/env python3
"""Read-only exact four-edge W7 source proof and twelve-profile residual.

No solver, graph enumeration, symmetry, or marginal relation is used.
"""
from array import array
from collections import defaultdict, deque
from copy import deepcopy
from hashlib import sha256
from pathlib import Path
import argparse
import gzip
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = 'audits/2026-10-20-r6-941-j1-five-edge-417732f'
PARENT = 'audits/2026-10-21-w7-u1v-30f2d19/RESIDUAL.json'
BASE = 'd23f94f739468593db653ec03f903c30adfd5fb0'
IDS = [0,1,3,5,6,8,40,41,60,61,64,65]
EDGES = [['u4','v'],['u3','s'],['u2','v'],['u2','w']]
RIM = ['a','n','u4','u3','u2','u1','L','q','c','s','v','w','t']
TARGETS = [44459,44466]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def packed(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def decode(row):
    return [(row >> (2*(12-i))) & 3 for i in range(13)]


def canon(row):
    rename = {}
    return [rename.setdefault(c, len(rename)) for c in decode(row)]


def component_blocks(column):
    rows = [decode(h) for h in column]
    reference = rows[0]
    groups = defaultdict(list)
    for i in range(13):
        require(all(t[i]//2 == reference[i]//2 for t in rows),
                'a column changes palette membership')
        profile = tuple((t[i] ^ reference[i]) & 1 for t in rows)
        groups[(reference[i]//2, profile)].append(i)
    blocks = sorted(groups.values(), key=lambda b:b[0])
    anchors = [next(j for j,b in enumerate(blocks) if reference[b[0]]//2 == p)
               for p in (0,1)]
    generated = [column[0]]
    for j,b in enumerate(blocks):
        if j not in anchors:
            mask = sum(1 << (2*(12-i)) for i in b)
            generated += [h ^ mask for h in generated]
    require(sorted(generated) == column,
            'complete component flips do not regenerate a proof column')
    return [[RIM[i] for i in b] for b in blocks]


def prepare():
    manifest = json.loads((HERE/'BASE.json').read_text())
    require(manifest['base'] == BASE, 'BASE changed')
    hashes = {}
    objects = {}
    for record in manifest['inputs']:
        if record['authority'] != 'immutable-input':
            continue
        name = record['path']
        raw = (ROOT/name).read_bytes()
        require(len(raw) == record['bytes'] and sha256(raw).hexdigest() == record['sha256'],
                'frozen input drift: '+name)
        hashes[name] = record['sha256']
        if name.endswith('.json') or name.endswith('.gz'):
            objects[name] = json.loads(gzip.decompress(raw) if name.endswith('.gz') else raw)
    caps = objects[SOURCE+'/counting/caps.json.gz']
    orbit = objects[SOURCE+'/counting/orbits.json.gz']
    require(caps['ordered_rim'] == RIM, 'original rotation/rim changed')
    require(len(orbit['columns']) == 307197 and len(orbit['live']) == 61308,
            'original complete family changed')
    require(hashes[SOURCE+'/counting/orbits.json.gz'] ==
            '542ee11de93a846bfbc321b098214b153c5b600318ba2e0bc5621a73ad2a55ad',
            'original pre-chord family was replaced')
    parent = objects[PARENT]
    profiles = [p for p in parent['profiles']
                if len(sum(p['retained_columns'].values(), [])) == 15]
    require([p['original_profile_id'] for p in profiles] == IDS,
            'full fifteen-column profiles changed')
    row_codes = array('I', (h for h,s in orbit['rowids']))
    row_states = array('I', (s for h,s in orbit['rowids']))
    lookup = {h:i for i,h in enumerate(row_codes)}
    row_state = dict(orbit['rowids'])
    state_rows = [[] for _ in caps['states']]
    for i,s in enumerate(row_states):
        require(canon(row_codes[i]) == caps['states'][s], 'literal state mismatch')
        state_rows[s].append(i)
    columns = [array('I', (lookup[h] for h in col)) for col in orbit['columns']]
    incident = [[] for _ in row_codes]
    for j,col in enumerate(columns):
        for h in col:
            incident[h].append(j)
    require(all(len(state_rows[s]) == 3 and all(incident[h] for h in state_rows[s])
                for s in orbit['live']), 'incomplete original state family')
    return {'hashes':hashes, 'caps':caps, 'orbit':orbit, 'profiles':profiles,
            'row_codes':row_codes, 'row_states':row_states, 'lookup':lookup,
            'row_state':row_state, 'state_rows':state_rows, 'columns':columns,
            'incident':incident}


def proof_check(cert, p):
    require(cert['scope'] == 'same complete strict only-R/W7 source; four original-edge exclusions',
            'source scope changed')
    require(cert['input_sha256'] == p['hashes'], 'proof authority changed')
    require([b['original_edge'] for b in cert['branches']] == EDGES,
            'original edge branches changed')
    component_records = {r['column_id']:r for r in cert['full_component_columns']}
    used = set()
    summaries = []
    for branch in cert['branches']:
        edge = branch['original_edge']
        indices = [RIM.index(name) for name in edge]
        known = set()
        depths = {}
        for node in branch['zero_nodes']:
            s = node['state']
            require(type(s) is int and s not in known, 'invalid/duplicate proof state')
            require(node['literal_tuple'] == p['caps']['states'][s], 'proof tuple changed')
            if node['rule'] == 'original-edge':
                require(p['caps']['states'][s][indices[0]] ==
                        p['caps']['states'][s][indices[1]], 'direct zero is proper on original edge')
                depth = 0
            elif node['rule'] == 'all-incident-columns-zero':
                h = node['halfrow']
                require(type(h) is int and p['row_state'].get(h) == s,
                        'zero rule uses wrong original half-row')
                ids = p['incident'][p['lookup'][h]]
                pairs = node['column_zero_witnesses']
                require([x[0] for x in pairs] == ids and bool(ids),
                        'complete incident-column cover is missing')
                for j,t,k in pairs:
                    require(all(type(v) is int for v in (j,t,k)), 'noninteger proof witness')
                    require(t in known and p['row_state'].get(k) == t and
                            k in p['orbit']['columns'][j], 'column has no already-zero full fibre')
                    used.add(j)
                depth = 1+max(depths[t] for j,t,k in pairs)
            else:
                raise ValueError('unknown zero proof rule')
            require(node['depth'] == depth, 'zero DAG depth changed')
            known.add(s)
            depths[s] = depth
        require(all(s in known for s in TARGETS), 'original positive target sum not contradicted')
        require(branch['target_zero_depths'] == [depths[s] for s in TARGETS],
                'target depth changed')
        covered = [r['original_profile_id'] for r in p['profiles']
                   if any(set(e) == set(edge) for e in r['original_chords'])]
        require(branch['covered_full15_profile_ids'] == covered, 'complete profile coverage changed')
        summaries.append({'original_edge':edge, 'zero_nodes':len(known),
                          'target_zero_depths':[depths[s] for s in TARGETS],
                          'covered_full15_profile_ids':covered})
    require(set(component_records) == used, 'component certificate coverage changed')
    for j in sorted(used):
        record = component_records[j]
        col = p['orbit']['columns'][j]
        require(record['all_halfrows'] == col, 'complete proof orbit row list changed')
        require(record['boundary_components'] == component_blocks(col),
                'full actual component contacts changed')
    return summaries


def transport_check(transport, p):
    require(transport['scope'] == 'same complete D literal component involutions',
            'literal transport scope changed')
    require(len(transport['steps']) == 6, 'short component-transport steps changed')
    for step in transport['steps']:
        s,t,h,k = [step[name] for name in
                   ('from_state','to_state','from_halfrow','to_halfrow')]
        require(p['row_state'].get(h) == s and p['row_state'].get(k) == t,
                'literal transport uses wrong state halfrow')
        ids = p['incident'][p['lookup'][h]]
        require(step['all_incident_columns'] == ids and ids,
                'short transport omitted an original incident column')
        for j in ids:
            col = p['orbit']['columns'][j]
            require(k in col, 'short transport lost its destination full fibre')
            blocks = component_blocks(col)
            row = list(p['caps']['states'][s])
            for action in step['actual_component_union_swaps']:
                pair = action['pair']
                roots = action['roots']
                require(len(pair) == 2 and len(set(pair)) == 2 and roots,
                        'invalid actual component swap')
                chosen = [b for b in blocks if set(b).intersection(roots)]
                require(all(row[RIM.index(root)] in pair for root in roots),
                        'a root is outside its actual palette')
                contacts = set(name for b in chosen for name in b)
                require(all(row[RIM.index(name)] in pair for name in contacts),
                        'an actual component has a contact outside its palette')
                for name in contacts:
                    i = RIM.index(name)
                    row[i] = pair[0] ^ pair[1] ^ row[i]
            require(row == p['caps']['states'][t],
                    'the complete actual component action has wrong literal endpoint')
    return len(transport['steps'])


def close(profile, p):
    states = p['row_states']
    columns = p['columns']
    alive = bytearray(len(p['caps']['states']))
    for s in p['orbit']['live']:
        alive[s] = 1
    active = bytearray([1])*len(columns)
    degree = array('I', (len(x) for x in p['incident']))
    witness = array('i', [-1])*len(columns)
    queue = deque()
    steps = []
    chords = profile['original_chords']
    for s in p['orbit']['live']:
        row = p['caps']['states'][s]
        bad = next((e for e in chords if row[RIM.index(e[0])] == row[RIM.index(e[1])]), None)
        if bad is not None:
            alive[s] = 0
            queue.append(s)
            steps.append([s,'original-chord',bad])
    initial = len(steps)
    while queue:
        s = queue.popleft()
        for h in p['state_rows'][s]:
            for j in p['incident'][h]:
                if not active[j]:
                    continue
                active[j] = 0
                witness[j] = s
                for k in columns[j]:
                    require(degree[k] > 0, 'negative halfrow support degree')
                    degree[k] -= 1
                    t = states[k]
                    if degree[k] == 0 and alive[t]:
                        alive[t] = 0
                        queue.append(t)
                        steps.append([t,'empty-halfrow',p['row_codes'][k]])
    live_states = [s for s in p['orbit']['live'] if alive[s]]
    live_columns = [j for j,v in enumerate(active) if v]
    require(all(all(alive[states[h]] for h in columns[j]) for j in live_columns),
            'a residual column touches an empty fibre')
    require(all(all(degree[h] for h in p['state_rows'][s]) for s in live_states),
            'a residual state has empty palette support')
    return {'original_profile_id':profile['original_profile_id'],
            'all_original_chords':chords, 'initial_chord_zero_count':initial,
            'new_zero_steps':steps, 'live_state_ids':live_states,
            'live_column_ids':live_columns,
            'killed_column_zero_state_witness':list(witness),
            'counts':{'live_states':len(live_states), 'live_columns':len(live_columns),
                      'propagated_state_zeros':len(steps)-initial},
            'target_A_live':bool(alive[44459]),'target_B_live':bool(alive[44466]),
            'two_column_live':[bool(active[j]) for j in (66582,67755)]}


def controls(cert, p):
    def omit_column(c):
        node = next(n for n in c['branches'][0]['zero_nodes'] if n['rule'] != 'original-edge')
        node['column_zero_witnesses'].pop()
    def wrong_edge(c):
        c['branches'][0]['original_edge'] = ['a','u4']
    def wrong_zero(c):
        node = next(n for n in c['branches'][0]['zero_nodes'] if n['rule'] == 'original-edge')
        node['state'] = 44459
        node['literal_tuple'] = p['caps']['states'][44459]
    def omit_block(c):
        c['full_component_columns'][0]['boundary_components'].pop()
    def wrong_scope(c):
        c['scope'] = 'all C13 disks'
    rejected = []
    for name,mutate in [('missing_incident',omit_column),('wrong_edge',wrong_edge),
                        ('proper_direct_zero',wrong_zero),('omitted_component',omit_block),
                        ('unrestricted_claim',wrong_scope)]:
        bad = deepcopy(cert)
        mutate(bad)
        try:
            proof_check(bad,p)
        except (ValueError,KeyError,IndexError):
            rejected.append(name)
    require(len(rejected) == 5, 'a damaged certificate was accepted')
    return rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--controls',action='store_true')
    parser.add_argument('--certificate',type=Path,default=HERE/'certificate.json')
    args = parser.parse_args()
    p = prepare()
    cert = json.loads(args.certificate.read_text())
    branches = proof_check(cert,p)
    transport = json.loads((HERE/'transport.json').read_text())
    transport_steps = transport_check(transport,p)
    recorded = json.loads(gzip.decompress((HERE/'closure.json.gz').read_bytes()))
    computed = [close(profile,p) for profile in p['profiles']]
    require(recorded == computed, 'complete twelve-profile residual changed')
    result = {'result':'PASS: four original-edge source exclusions; 10 of 12 full15 profiles excluded',
              'branches':branches,
              'complete_literal_component_involutions':transport_steps,
              'profiles':[{'id':r['original_profile_id'],**r['counts'],
                           'targets_live':[r['target_A_live'],r['target_B_live']]}
                          for r in computed],
              'remaining_profile_ids':[r['original_profile_id'] for r in computed
                                       if r['target_A_live'] or r['target_B_live']],
              'source_realizability':'not established', 'general_W7':'OPEN',
              'new_Lean':False,'LP_used':False}
    if args.controls:
        result['rejected_corruptions'] = controls(cert,p)
        bad_transport = deepcopy(transport)
        step = next(s for s in bad_transport['steps'] if s['from_state'] == 44050)
        step['actual_component_union_swaps'][0]['roots'] = ['s']
        try:
            transport_check(bad_transport,p)
        except ValueError:
            result['rejected_corruptions'].append('omitted_component_union_root')
        require(len(result['rejected_corruptions']) == 6,
                'a boundary-only component-union shortcut was accepted')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
