#!/usr/bin/env python3
"""Whole-component W7 transport and bounded necessary connectivity gates.

The original full D family is retained.  Local collar partitions may merge in
the original exterior; compatible partitions do not constitute a common lift.
No source graph is generated, and no LP is used.
"""
from collections import Counter, defaultdict
from copy import deepcopy
from hashlib import sha256
from itertools import product
from pathlib import Path
import argparse
import gzip
import importlib.util
import json
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BASE = '30dde27293b5d3ad63c75fae73cda5be96db705b'
SOURCE = 'audits/2026-10-20-r6-941-j1-five-edge-417732f'
COLLAR = 'audits/2026-10-21-w7-profile0-13e51db/check.py'
RIM = ['a','n','u4','u3','u2','u1','L','q','c','s','v','w','t']
P = ['n','u4','u3','u2','u1','L']
TARGETS = [(44459,'v',306985),(44466,'w',306993)]
PHASES = [(0,0),(1,0),(0,1),(1,1)]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def packed(x):
    return json.dumps(x,sort_keys=True,separators=(',',':'))


def canon(row):
    names = {}
    return [names.setdefault(c,len(names)) for c in row]


def encode(row):
    return sum(c << (2*(12-i)) for i,c in enumerate(row))


def decode(row):
    return [(row >> (2*(12-i))) & 3 for i in range(13)]


def halfrow(t, mate):
    other = [c for c in (1,2,3) if c != mate]
    perm = {0:0,mate:1,other[0]:2,other[1]:3}
    u = [perm[c] for c in t]
    a = u[0]
    b = next(c for c in u if c//2 != a//2)
    normal = {a:0,a^1:1,b:2,b^1:3}
    return encode([normal[c] for c in u])


def blocks(column):
    rows = [decode(h) for h in column]
    first = rows[0]
    groups = defaultdict(list)
    for i in range(13):
        require(all(row[i]//2 == first[i]//2 for row in rows),'palette membership drift')
        groups[(first[i]//2,tuple((row[i]^first[i])&1 for row in rows))].append(i)
    out = sorted(groups.values(),key=lambda b:b[0])
    anchors = [next(j for j,b in enumerate(out) if first[b[0]]//2 == p) for p in (0,1)]
    regenerated = [column[0]]
    for j,b in enumerate(out):
        if j not in anchors:
            mask = sum(1 << (2*(12-i)) for i in b)
            regenerated += [h^mask for h in regenerated]
    require(sorted(regenerated) == column,'complete boundary component flips lost a row')
    return out


def swap(row, names, pair):
    out = list(row)
    for name in names:
        i = RIM.index(name)
        require(out[i] in pair,'root component leaves its palette')
        out[i] ^= pair[0]^pair[1]
    return out


def compositions(total, width):
    if width == 1:
        yield (total,)
    else:
        for first in range(total+1):
            for tail in compositions(total-first,width-1):
                yield (first,)+tail


def graph_components(graph, colors, pair):
    unseen = {v for v in graph if colors[v] in pair}
    out = []
    while unseen:
        todo, seen = [min(unseen)], set()
        while todo:
            v = todo.pop()
            if v not in seen:
                seen.add(v)
                todo.extend((graph[v]&unseen)-seen)
        unseen -= seen
        out.append(sorted(seen))
    return out


def prepare():
    manifest = json.loads((HERE/'BASE.json').read_text())
    require(manifest['base'] == BASE,'exclusive BASE changed')
    inputs, data = {}, {}
    for row in manifest['inputs']:
        raw = (HERE/'frozen'/row['path']).read_bytes()
        require(len(raw) == row['bytes'] and sha256(raw).hexdigest() == row['sha256'],
                'frozen source drift: '+row['path'])
        live = (ROOT/row['path']).read_bytes()
        require(live == raw,'live source drift: '+row['path'])
        inputs[row['path']] = {'bytes':len(raw),'sha256':row['sha256']}
        if row['path'].endswith('.gz'):
            data[row['path']] = json.loads(gzip.decompress(raw))
    require(inputs[SOURCE+'/counting/orbits.json.gz']['sha256'] ==
            '542ee11de93a846bfbc321b098214b153c5b600318ba2e0bc5621a73ad2a55ad',
            'the original pre-chord family was replaced')
    spec = importlib.util.spec_from_file_location('frozen_collar',HERE/'frozen'/COLLAR)
    source = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(source)
    caps = data[SOURCE+'/counting/caps.json.gz']
    orbit = data[SOURCE+'/counting/orbits.json.gz']
    require(caps['ordered_rim'] == RIM and source.P == P,'original order changed')
    require(len(orbit['columns']) == 307197,'original full family changed')
    return inputs, source, caps, orbit


def compute():
    inputs, source, caps, orbit = prepare()
    state_id = {tuple(t):i for i,t in enumerate(caps['states'])}
    row_state = dict(orbit['rowids'])
    live = set(orbit['live'])
    requests, request_by_key = [], {}
    phases, actions, mixed = [], [], []

    def request(label, row, mate):
        h = halfrow(row,mate)
        requests.append({'label':label,'literal_tuple':row,'mate_of_zero':mate,
                         'halfrow':h,'canonical_state':state_id[tuple(canon(row))]})
        request_by_key[label] = h
        return h

    for target,z0,j in TARGETS:
        t = caps['states'][target]
        require(t[:8] == [0,1,2,1,2,1,2,3],'target frame changed')
        cblock = ['c','s'] if target == 44459 else ['c','s','v']
        generator = {'a':(['a'],(0,3)), 'q':(['q',z0],(0,3)),
                     'c':(cblock,(1,2))}
        phase_rows = []
        for aa,qq in PHASES:
            out = list(t)
            if aa:
                out = swap(out,['a'],(0,3))
            if qq:
                out = swap(out,['q',z0],(0,3))
            phase_rows.append({'a_flip':aa,'q_flip':qq,'literal_tuple':out,
                               'canonical_state':state_id[tuple(canon(out))]})
            for mate in (1,2,3):
                request(f'{target}:{aa}:{qq}:{mate}',out,mate)
        phases.append({'target':target,'z0':z0,'whole_03_column':j,'phases':phase_rows})
        # All ordered words of lengths 1, 2, 3 in these three commuting
        # actual components.  The literal tuple, not just its canonical ID,
        # is retained after every action.
        for length in (1,2,3):
            for word in product(('a','q','c'),repeat=length):
                out, history = list(t), [list(t)]
                for letter in word:
                    names,pair = generator[letter]
                    out = swap(out,names,pair)
                    history.append(out)
                dest = state_id[tuple(canon(out))]
                require(dest in live,'a complete same-palette word reached a zero fibre')
                actions.append({'target':target,'word':''.join(word),
                                'literal_history':history,'canonical_endpoint':dest})
        middle = swap(swap(t,['q',z0],(0,3)),cblock,(1,2))
        mid = state_id[tuple(canon(middle))]
        require(mid == (44111 if target == 44459 else 44107),'two-component middle changed')
        request(f'{target}:middle:2',middle,2)
        mixed.append({'target':target,'middle_state':mid,'middle_literal':middle,
                      'root':z0,'palette':[1,3]})

    incidences = {h:[] for h in request_by_key.values()}
    for j,col in enumerate(orbit['columns']):
        for h in set(col)&incidences.keys():
            incidences[h].append(j)
    used = sorted({j for js in incidences.values() for j in js})
    partition = {j:blocks(orbit['columns'][j]) for j in used}
    lookup = {j:{i:k for k,b in enumerate(bs) for i in b} for j,bs in partition.items()}
    for r in requests:
        require(row_state[r['halfrow']] == r['canonical_state'],'full half-row state mismatch')
        r['all_incident_columns'] = incidences[r['halfrow']]
        require(bool(r['all_incident_columns']),'a requested full fibre has no source column')
    for target,z0,j in TARGETS:
        require(incidences[request_by_key[f'{target}:0:0:3']] == [j],
                'full target 03 incidence changed')

    for record in mixed:
        h = request_by_key[f"{record['target']}:middle:2"]
        branches = defaultdict(list)
        for j in incidences[h]:
            root_block = next(b for b in partition[j] if RIM.index(record['root']) in b)
            names = [RIM[i] for i in root_block]
            out = swap(record['middle_literal'],names,(1,3))
            dest = state_id[tuple(canon(out))]
            require(dest in live,'a mixed component step reached an already-zero complete fibre')
            branches[(tuple(names),dest)].append(j)
        record['all_incident_columns'] = incidences[h]
        record['root_component_branches'] = [
            {'whole_boundary_contacts':list(names),'canonical_endpoint':dest,
             'all_source_columns':js}
            for (names,dest),js in sorted(branches.items())]
    require(mixed[0]['root_component_branches'] == [{
        'whole_boundary_contacts':['s','v','w'],'canonical_endpoint':44127,
        'all_source_columns':[147448,147449,167802,226130,231666]}],
        'A third-step whole-component forcing changed')

    def compatible(graph, colors, mate, ids):
        groups = []
        for pair in [(0,mate),tuple(c for c in range(4) if c not in (0,mate))]:
            for component in graph_components(graph,colors,pair):
                contacts = [RIM.index(v) for v in component if v in RIM]
                if len(contacts)>1:
                    groups.append(contacts)
        return [j for j in ids if all(len({lookup[j][v] for v in group}) == 1
                                     for group in groups)]

    patterns, pattern_ids, records = [], {}, []
    aggregate, zero_gates = Counter(), []
    positions = 0
    for profile,width in [(0,6),(1,5)]:
        for K in range(1,6):
            for counts in compositions(K,width):
                data,graph = source.collar(profile,counts,with_graph=True)
                graph = {v:adj-{'p','h','R'} for v,adj in graph.items() if v not in {'p','h','R'}}
                for i,a in enumerate(RIM):
                    b = RIM[(i+1)%13]
                    graph.setdefault(a,set()).add(b)
                    graph.setdefault(b,set()).add(a)
                path = data['boundary'][1:]
                hnodes = [v for v in path if v.startswith('H')]
                centers = {v:next(t for t in P if t in graph[v]) for v in hnodes}
                for y in hnodes:
                    pos = path.index(y)
                    local = dict(zip(P,[1,2,1,2,1,2]))
                    for i,v in enumerate(path):
                        local[v] = ([0,3][i%2] if i<pos else 3-local[centers[v]] if i==pos
                                    else [3,0][(len(path)-1-i)%2])
                    require(all(local[a] != local[b] for a in local for b in graph[a] if b in local),
                            'the unique-barrier local color word is improper')
                    require([v for v in hnodes if local[v] in (1,2)] == [y],
                            'a local word does not have its exact unique barrier')
                    epsilon = int(local[path[pos-1]] != local[path[pos+1]])
                    require(epsilon == ((1+K-profile)%2),'arbitrary-K unique-barrier phase failed')
                    prefix,suffix = set(path[:pos]),set(path[pos+1:])
                    selected = []
                    for target,z0,j in TARGETS:
                        original = local|dict(zip(RIM,caps['states'][target]))
                        gate_rows = []
                        for aa,qq in PHASES:
                            colors = dict(original)
                            for active,side,contacts in [(aa,prefix,['a']),(qq,suffix,['q',z0])]:
                                if active:
                                    for v in side|set(contacts):
                                        colors[v] = 3-colors[v]
                            require(all(colors[a] != colors[b] for a in graph for b in graph[a]),
                                    'whole forced component intersection became improper')
                            require(colors[y] == original[y], 'an 03 action changed the barrier')
                            for mate in (1,2,3):
                                label = f'{target}:{aa}:{qq}:{mate}'
                                allowed = compatible(graph,colors,mate,incidences[request_by_key[label]])
                                gate_rows.append(allowed)
                                if not allowed:
                                    zero_gates.append([profile,list(counts),y,label])
                        # The c-component is disjoint from K12(P), and hence
                        # from every barrier.  All other A vertices are 03.
                        middle_colors = dict(original)
                        for v in suffix|{'q',z0}:
                            middle_colors[v] = 3-middle_colors[v]
                        for v in (['c','s'] if target == 44459 else ['c','s','v']):
                            middle_colors[v] = 3-middle_colors[v]
                        label = f'{target}:middle:2'
                        allowed = compatible(graph,middle_colors,2,incidences[request_by_key[label]])
                        gate_rows.append(allowed)
                        if not allowed:
                            zero_gates.append([profile,list(counts),y,label])
                        key = packed(gate_rows)
                        if key not in pattern_ids:
                            pattern_ids[key] = len(patterns)
                            patterns.append(gate_rows)
                        selected.append(pattern_ids[key])
                        aggregate[(profile,K,target)] += 1
                    records.append([profile,list(counts),y,*selected])
                    positions += 1
    require(positions == 3030 and not zero_gates,'bounded necessary gates changed')

    # A single 03 flip leaves the original image in one specific column.
    # The complete destination fibre has other admissible columns, including
    # an a/q joined one.  This rejects refilling the image by the whole fibre.
    image_controls = []
    for target,z0,j in TARGETS:
        ids = incidences[request_by_key[f'{target}:0:1:3']]
        joined = [k for k in ids if lookup[k][0] == lookup[k][7]]
        require(len(ids) == 3 and j in ids and len(joined) == 1 and joined[0] != j,
                'the false-image-refill countercontrol disappeared')
        image_controls.append({'target':target,'actual_image_03_column':j,
            'all_destination_03_columns':ids,'joined_a_q_countercontrol':joined[0]})

    return {'base':BASE,'inputs':inputs,'ordered_rim':RIM,
        'scope':'same original D; unique-barrier arbitrary-K paper forcing and K<=5 calibration',
        'full_family_columns_scanned':len(orbit['columns']),
        'complete_requests':requests,'whole_03_phase_actions':phases,
        'all_ordered_component_words_length_at_most_three':actions,
        'third_step_mixed_component_branches':mixed,
        'complete_used_columns':[{'column_id':j,'all_halfrows':orbit['columns'][j],
            'canonical_states':[row_state[h] for h in orbit['columns'][j]],
            'boundary_components':[[RIM[i] for i in b] for b in partition[j]]} for j in used],
        'local_connectivity_calibration':{
            'K_max':5,'unique_barrier_positions':positions,'target_color_words':2*positions,
            'gates_per_word':13,'gate_count':26*positions,'zero_gates':zero_gates,
            'gate_order':'four a/q parities in PHASES, each mates 1/2/3; then q+c middle mate 2',
            'PHASES':[list(x) for x in PHASES],
            'pattern_table':patterns,'complete_position_pattern_rows':records,
            'row_columns':['profile','ordered_H_lengths','barrier','A_pattern_id','B_pattern_id'],
            'aggregate':[{'profile':p,'K':k,'target':t,'color_words':n}
                         for (p,k,t),n in sorted(aggregate.items())]},
        'image_refill_countercontrols':image_controls,
        'arbitrary_K_conclusions':[
            'a/q whole 03 flips act on entire prefix/suffix and keep the unique barrier',
            'one side flip toggles epsilon and also changes a/q endpoint colors',
            'two side flips plus global 03 normalization fix A colors but may flip boundary-free private components',
            'all A barriers belong to K12(P); c-side K12(c) contains no A vertices',
            'after A q+c, K13(v) avoids every zi and all H attached to color-1 P centers',
            'local palette connectivity may only merge in the exterior; accepted partitions do not give joint source lifts'],
        'new_source_exclusions_by_this_transport':[],
        'full_source_realizability':'not triggered','general_W7':'OPEN',
        'new_Lean':False,'LP_run':False,'new_source_graph_enumeration':False}


def verify(cert, expected):
    require(packed(cert) == packed(expected),'damaged or overextended transport certificate')


def negative_controls(cert):
    def omit(c):
        c['third_step_mixed_component_branches'][1]['all_incident_columns'].pop()
    def partial(c):
        c['third_step_mixed_component_branches'][0]['root_component_branches'][0]['whole_boundary_contacts'] = ['v']
    def refill(c):
        c['image_refill_countercontrols'][0]['all_destination_03_columns'] = [306985]
    def invent_zero(c):
        c['new_source_exclusions_by_this_transport'] = [0]
    variants = [('omitted_original_incident_column',omit),('partial_mixed_component',partial),
                ('refill_image_with_target_rule',refill),('invent_profile_exclusion',invent_zero)]
    rejected = []
    for name,mutate in variants:
        bad = deepcopy(cert)
        mutate(bad)
        try:
            verify(bad,cert)
        except ValueError:
            rejected.append(name)
    require(len(rejected) == len(variants),'a corrupted transport certificate was accepted')
    return rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build',action='store_true')
    parser.add_argument('--certificate',type=Path)
    args = parser.parse_args()
    require(not(args.build and args.certificate),'conflicting certificate options')
    result = compute()
    path = args.certificate or HERE/'certificate.json'
    if args.build:
        with path.open('x') as stream:
            json.dump(result,stream,sort_keys=True,indent=2)
            stream.write('\n')
    else:
        verify(json.loads(path.read_text()),result)
    print(json.dumps({'result':'PASS: exact whole-component transport; this method excludes no new source',
        'full_family_columns_scanned':result['full_family_columns_scanned'],
        'complete_component_words':len(result['all_ordered_component_words_length_at_most_three']),
        'unique_barrier_positions':result['local_connectivity_calibration']['unique_barrier_positions'],
        'gate_count':result['local_connectivity_calibration']['gate_count'],
        'zero_gates':len(result['local_connectivity_calibration']['zero_gates']),
        'negative_controls_rejected':negative_controls(result),'source_realizability':'not triggered'},sort_keys=True))


if __name__ == '__main__':
    main()
