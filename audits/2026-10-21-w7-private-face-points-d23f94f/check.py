#!/usr/bin/env python3
"""Narrow profile 0/1 face/link and whole-family 03 custody checks.

The general Jordan/link arguments are in PROOF.md.  The color tables are
local calibration, not enumeration or realization of full 941 sources.
"""
from collections import defaultdict
from copy import deepcopy
from hashlib import sha256
from itertools import product
from pathlib import Path
import argparse
import gzip
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = 'd23f94f739468593db653ec03f903c30adfd5fb0'
SOURCE = 'audits/2026-10-20-r6-941-j1-five-edge-417732f'
OLD = 'audits/2026-10-21-w7-structural-30f2d19'
RIM = ['a','n','u4','u3','u2','u1','L','q','c','s','v','w','t']
PATH = ['n','u4','u3','u2','u1','L']
C7 = ['n','h','L','u1','u2','u3','u4']
FAMILY_SHA = '542ee11de93a846bfbc321b098214b153c5b600318ba2e0bc5621a73ad2a55ad'


def require(ok,message):
    if not ok:
        raise ValueError(message)


def packed(x):
    return json.dumps(x,sort_keys=True,separators=(',',':'))


def decode(h):
    return [(h >> (2*(12-i))) & 3 for i in range(13)]


def components(column):
    rows = [decode(h) for h in column]
    first = rows[0]
    groups = defaultdict(list)
    for i in range(13):
        require(all(row[i]//2==first[i]//2 for row in rows),'palette membership drift')
        groups[(first[i]//2,tuple((row[i]^first[i])&1 for row in rows))].append(i)
    blocks = sorted(groups.values(),key=lambda b:b[0])
    anchors = [next(j for j,b in enumerate(blocks) if first[b[0]]//2==p) for p in (0,1)]
    generated = [column[0]]
    for j,b in enumerate(blocks):
        if j not in anchors:
            mask = sum(1 << (2*(12-i)) for i in b)
            generated += [h^mask for h in generated]
    require(sorted(generated)==column,'full component flips do not regenerate the original column')
    return blocks


def load():
    manifest = json.loads((HERE/'BASE.json').read_text())
    require(manifest['base']==BASE,'BASE changed')
    hashes,data = {},{}
    for r in manifest['inputs']:
        raw = (ROOT/r['path']).read_bytes()
        require(len(raw)==r['bytes'] and sha256(raw).hexdigest()==r['sha256'],
                'frozen source drift: '+r['path'])
        hashes[r['path']] = {'bytes':len(raw),'sha256':r['sha256']}
        if r['path'].endswith('.gz'):
            data[r['path']] = json.loads(gzip.decompress(raw))
        elif r['path'].endswith('.json'):
            data[r['path']] = json.loads(raw)
    require(hashes[SOURCE+'/counting/orbits.json.gz']['sha256']==FAMILY_SHA,
            'the original full family was replaced')
    return hashes,data


def compute():
    hashes,data = load()
    caps = data[SOURCE+'/counting/caps.json.gz']
    orbit = data[SOURCE+'/counting/orbits.json.gz']
    geo = data[OLD+'/geometry/certificate.json']
    require(caps['ordered_rim']==RIM and geo['C13']==RIM,'original ordered rim changed')
    require(len(orbit['columns'])==307197,'original family size changed')
    profiles = []
    for pid,expected_chords in [(0,[]),(1,[['a','u4']])]:
        r = next(x for x in geo['profiles'] if x['original_profile_id']==pid)
        require(r['chords']==expected_chords,'the fixed complete source profile changed')
        graph = defaultdict(set)
        for i,a in enumerate(RIM):
            b = RIM[(i+1)%13]
            graph[a].add(b)
            graph[b].add(a)
        for a,b in expected_chords:
            graph[a].add(b)
            graph[b].add(a)
        candidates = [sorted(graph[a]&graph[b]) for a,b in zip(PATH,PATH[1:])]
        require(candidates==([[],[],[],[],[]] if pid==0 else [['a'],[],[],[],[]]),
                'rim third-face candidates changed')
        if pid==1:
            require(['a','n','u4'] in r['topology_cells'], 'the actual n-u4-a face was lost')
            forced = next(x for x in r['forced_degree5_centers'] if x['center']=='n')
            require(forced['forced_complete_degree']==5 and
                    forced['forced_complete_neighbors']==['R','a','h','p','u4'],
                    'the full original n-five star changed')
        profiles.append({'original_profile_id':pid,'all_original_chords':expected_chords,
            'all_rim_third_face_candidates':candidates,
            'z1_is_a':pid==1,'private_third_face_points':
                ['z1','z2','z3','z4','z5'] if pid==0 else ['z2','z3','z4','z5'],
            'all_five_face_points_pairwise_distinct':True,
            'exact_C7_contacts':{f'z{i+1}':PATH[i:i+2] for i in range(5)},
            'source_excluded':False})
    incident = {12302027:[],12302051:[]}
    for j,col in enumerate(orbit['columns']):
        for h in set(col)&incident.keys():
            incident[h].append(j)
    require(incident=={12302027:[306985],12302051:[306993]},'complete target 03 incidences changed')
    forced = []
    for sid,h,j,z0 in [(44459,12302027,306985,'v'),(44466,12302051,306993,'w')]:
        t = caps['states'][sid]
        require([t[RIM.index(x)] for x in PATH]==[1,2,1,2,1,2], 'target path colors changed')
        require(t[0]==0 and t[7]==3, 'the fixed a/q color frame changed')
        blocks = components(orbit['columns'][j])
        contacts = [[RIM[i] for i in b] for b in blocks if t[b[0]] in (0,3)]
        require(contacts==[['a'],['q',z0]],'whole original target 03 contacts changed')
        forced.append({'state':sid,'literal_tuple':t,'halfrow':h,
            'all_incident_columns':[j],'all_03_boundary_component_contacts':contacts,
            'possible_K03_zi_rim_contacts':[[],['a'],['q',z0]],
            'these_choices_independently_realizable':False})
    # Complete tiny local color tables, with arbitrary extra link neighbors
    # through length three; these do not claim to realize the original source.
    local_tables = []
    for center in (1,2):
        opposite = 3-center
        for extras in range(4):
            good,connected,blocked = [],0,0
            for a,b in product((0,3),repeat=2):
                for middle in product([x for x in range(4) if x!=center],repeat=extras):
                    arc = [a,*middle,b]
                    if any(x==y for x,y in zip(arc,arc[1:])):
                        continue
                    good.append(arc)
                    in03 = all(x in (0,3) for x in arc)
                    require(in03 == (opposite not in middle), 'local color blocker criterion failed')
                    connected += in03
                    blocked += not in03
            if extras==0:
                require(len(good)==2 and connected==2,'degree-five edge calibration failed')
            local_tables.append({'center_color':center,'extra_link_neighbors':extras,
                'all_proper_color_arcs':good,'all_03_arcs':connected,'blocked_arcs':blocked})
    return {'base':BASE,'inputs':hashes,
        'scope':'same original strict only-R/W7 source, fixed complete profile 0 or 1',
        'ordered_D_rim':RIM,'original_C7':C7,'ordered_five_edge_path':PATH,
        'profiles':profiles,'all_zi_color_domain_in_both_targets':[0,3],
        'whole_original_target_03_forcing':forced,'complete_link_templates':{
            't_i_for_i_1_to_4':['R','t_(i-1)','z_i','H_i...','z_(i+1)','t_(i+1)'],
            'profile0_n':['a','p','h','R','u4','z1','H_n...'],
            'profile1_n':['a','p','h','R','u4'],
            'L':['h','R','u1','z5','H_L...','q']},
        'degree_equivalences':[
            'for i=1..4: zi-z(i+1) is an original edge iff d_G(t_i)=5',
            'z5-q is an original edge iff d_G(L)=5',
            'profile0: a-z1 is an original edge iff d_G(n)=6'],
        'source_color_blocker_conclusion':{
            'profile0_centers':['n','u4','u3','u2','u1','L'],
            'profile1_centers':['u4','u3','u2','u1','L'],
            'some_extra_outer_link_vertex_has_opposite_12_color_to_its_center':True,
            'all_original_extra_neighbors_retained':True},
        'local_link_color_tables':local_tables,
        'local_control_scope':'only local link calibration; full 941 source not triggered',
        'profile0_or_1_source_excluded':False,'smaller_source_constructed':False,
        'complete_boundary_relation_preserving_replacement_proved':False,
        'general_W7':'OPEN','J1_J2':'OPEN','new_Lean':False,'LP_run':False}


def verify(cert,expected):
    require(packed(cert)==packed(expected),'damaged or overextended structural certificate')


def controls(cert):
    variants = [
        ('five_private_points_in_profile1',lambda c:c['profiles'][1].__setitem__('private_third_face_points',['z1','z2','z3','z4','z5'])),
        ('omit_the_a_face',lambda c:c['profiles'][1].__setitem__('z1_is_a',False)),
        ('merge_a_q_components',lambda c:c['whole_original_target_03_forcing'][0].__setitem__('all_03_boundary_component_contacts',[['a','q','v']])),
        ('drop_unknown_outer_neighbors',lambda c:c['source_color_blocker_conclusion'].__setitem__('all_original_extra_neighbors_retained',False)),
        ('invent_minimality_replacement',lambda c:c.__setitem__('smaller_source_constructed',True)),
        ('claim_profile_exclusion',lambda c:c.__setitem__('profile0_or_1_source_excluded',True)),
    ]
    rejected = []
    for name,mutate in variants:
        bad = deepcopy(cert)
        mutate(bad)
        try:
            verify(bad,cert)
        except ValueError:
            rejected.append(name)
    require(len(rejected)==len(variants),'a structural corruption was accepted')
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
            json.dump(result,stream,indent=2,sort_keys=True)
            stream.write('\n')
    else:
        verify(json.loads(path.read_text()),result)
    print(json.dumps({'result':'PASS: profile 0/1 face/link custody; both sources remain OPEN',
        'private_face_point_counts':[5,4],'profile1_z1':'a',
        'target_03_incidence':[[306985],[306993]],
        'negative_controls_rejected':controls(result),'source_realization':'not triggered',
        'source_exclusion':False,'smaller_source_constructed':False},sort_keys=True))


if __name__=='__main__':
    main()
