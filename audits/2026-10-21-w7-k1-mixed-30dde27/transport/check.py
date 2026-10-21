#!/usr/bin/env python3
"""Same original D orbit, marked Y, and full same-E strip/cap joins.

No next-state fibre is refilled.  All actions use one fixed original 01|23
component partition.  Hidden components retain their original color phase.
"""
from collections import Counter, defaultdict
from copy import deepcopy
from functools import lru_cache
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
OLD = 'audits/2026-10-21-w7-single-barrier-30dde27/transport/check.py'
COLLAR = 'audits/2026-10-21-w7-profile0-13e51db/check.py'
RIM = ['a','n','u4','u3','u2','u1','L','q','c','s','v','w','t']
P = ['n','u4','u3','u2','u1','L']
ROWS = ['01012','01021','01023','01201','01202',
        '01203','01212','01213','01231','01232']
ZERO = {'G':{'01021','01202','01212'},'Q1':{'01232'},'J1':{'01202','01212'}}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def packed(x):
    return json.dumps(x,sort_keys=True,separators=(',',':'))


def module(path, name):
    spec = importlib.util.spec_from_file_location(name,path)
    out = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(out)
    return out


def canonical(t):
    renaming = {}
    return tuple(renaming.setdefault(c,len(renaming)) for c in t)


def prepare():
    manifest = json.loads((HERE/'BASE.json').read_text())
    require(manifest['base'] == BASE,'exclusive BASE changed')
    inputs = {}
    for rec in manifest['inputs']:
        raw = (HERE/'frozen'/rec['path']).read_bytes()
        require(len(raw) == rec['bytes'] and sha256(raw).hexdigest() == rec['sha256'],
                'frozen source drift: '+rec['path'])
        require((ROOT/rec['path']).read_bytes() == raw,'live source drift: '+rec['path'])
        inputs[rec['path']] = {'bytes':len(raw),'sha256':rec['sha256'],'authority':rec['authority']}
    caps = json.loads(gzip.decompress((HERE/'frozen'/SOURCE/'counting/caps.json.gz').read_bytes()))
    orbit = json.loads(gzip.decompress((HERE/'frozen'/SOURCE/'counting/orbits.json.gz').read_bytes()))
    require(inputs[SOURCE+'/counting/orbits.json.gz']['sha256'] ==
            '542ee11de93a846bfbc321b098214b153c5b600318ba2e0bc5621a73ad2a55ad',
            'the original pre-chord full family was replaced')
    require(caps['ordered_rim'] == RIM and len(orbit['columns']) == 307197,
            'original full D authority changed')
    return inputs,caps,orbit,module(HERE/'frozen'/OLD,'frozen_whole_components'),module(HERE/'frozen'/COLLAR,'frozen_collar')


@lru_cache(None)
def full_caps(literal_rim):
    a,n,u4,u3,u2,u1,L,q,c,s,v,w,t = literal_rim
    spokes = {n,u4,u3,u2,u1,L}
    right = [list(z) for z in product(range(4),repeat=3)
             if z[2] not in (s,v,w,t,z[0],z[1])
             and z[0] not in (c,s,z[1]) and z[1] not in (a,t)]
    left = {
        'G':[list(z) for z in product(range(4),repeat=4)
             if z[0] not in (a,c,q,z[1]) and z[1] not in (a,q,n,z[2])
             and z[2] not in (q,L,z[3],n) and z[3] not in spokes],
        'Q1':[list(z) for z in product(range(4),repeat=2)
              if z[0] == n and z[1] == q and z[0] not in (a,c,q) and z[1] not in spokes],
        'J1':[list(z) for z in product(range(4),repeat=2)
              if z[0] == L and a != z[1] and z[0] not in (a,c,q) and z[1] not in spokes]}
    lifts,counts,bad = {},{},[]
    for graph in ZERO:
        rows = [[] for _ in ROWS]
        for li,ls in enumerate(left[graph]):
            for ri,rs in enumerate(right):
                frame = [rs[0],rs[1],a,ls[0],c]
                word = ''.join(map(str,canonical(frame)))
                require(word in ROWS,'a full cap has an improper original outer frame')
                rows[ROWS.index(word)].append([li,ri])
                if word in ZERO[graph]:
                    bad.append({'graph':graph,'row':word,'left_cap':ls,'right_cap':rs,
                                'literal_outer_frame':frame})
        lifts[graph] = rows
        counts[graph] = list(map(len,rows))
    return {'literal_D_rim':list(literal_rim),'complete_left_caps':left,
            'complete_right_caps':right,'all_full_lift_pairs_by_row':lifts,
            'full_cap_counts':counts,'all_bad_full_cap_lifts':bad}


def compute():
    inputs,caps,orbit,old,collar = prepare()
    state_id = {tuple(t):i for i,t in enumerate(caps['states'])}
    row_state = dict(orbit['rowids'])
    incidence = {}
    for target in (44459,44466):
        h = old.halfrow(caps['states'][target],1)
        incidence[target] = [j for j,col in enumerate(orbit['columns']) if h in col]
        require(len(incidence[target]) == 10,'complete original 01|23 source incidence changed')
    used = sorted(set(incidence[44459]+incidence[44466]))
    partition = {j:old.blocks(orbit['columns'][j]) for j in used}
    columns = [{'column_id':j,'all_halfrows':orbit['columns'][j],
                'canonical_states':[row_state[h] for h in orbit['columns'][j]],
                'boundary_components':[[RIM[i] for i in b] for b in partition[j]]} for j in used]
    cap_pool,cap_ids,kernel_ids = [],{},{}
    kernels = []
    cases, summary, families = [],Counter(),{}

    def cap_ref(row):
        key = tuple(row)
        if key not in cap_ids:
            data = full_caps(key)
            sid = state_id[canonical(row)]
            require(all(data['full_cap_counts'][g] == [caps['matrices'][g][r][sid] for r in range(10)]
                        for g in ZERO),'direct all-cap lifts disagree with original frozen matrices')
            data['canonical_state'] = sid
            cap_ids[key] = len(cap_pool)
            cap_pool.append(data)
        return cap_ids[key]

    for center_index in (2,4,5):
        counts = [0]*6
        counts[center_index] = 1
        case,graph = collar.collar(0,counts,with_graph=True)
        graph = {v:adj-{'p','h','R'} for v,adj in graph.items() if v not in {'p','h','R'}}
        for i,a in enumerate(RIM):
            b = RIM[(i+1)%13]
            graph.setdefault(a,set()).add(b)
            graph.setdefault(b,set()).add(a)
        A = case['boundary'][1:]
        E_boundary = A+['c','s','v','w','t']
        y = next(v for v in A if v.startswith('H'))
        cut = A.index(y)
        local = dict(zip(P,[1,2,1,2,1,2]))
        for i,v in enumerate(A):
            local[v] = ([0,3][i%2] if i<cut else 3-local[P[center_index]] if i==cut
                        else [3,0][(len(A)-1-i)%2])
        require(local[A[cut-1]] == local[A[cut+1]],'profile0 K1 phase changed')

        def kernel_ref(colors):
            eword = tuple(colors[v] for v in E_boundary)
            key = (center_index,eword)
            if key in kernel_ids:
                return kernel_ids[key]
            fixed = {v:colors[v] for v in graph if v not in P}
            domains = [sorted(set(range(4))-{fixed[z] for z in graph[t] if z in fixed}) for t in P]
            rows = []
            for path in product(*domains):
                if any(a == b for a,b in zip(path,path[1:])):
                    continue
                complete = colors|dict(zip(P,path))
                require(all(complete[a] != complete[b] for a in graph for b in graph[a]),
                        'the full same-E strip kernel contains an improper lift')
                ref = cap_ref([complete[v] for v in RIM])
                rows.append({'P_colors':list(path),'cap_pool_id':ref})
            require(bool(rows),'a true complete orbit image lost its same-E strip lift')
            data = {'center':P[center_index],'ordered_E_boundary':E_boundary,
                    'literal_E_boundary':list(eword),'complete_P_domains':domains,
                    'all_same_E_strip_lifts':rows,
                    'has_bad_cap':any(cap_pool[r['cap_pool_id']]['all_bad_full_cap_lifts'] for r in rows)}
            kernel_ids[key] = len(kernels)
            kernels.append(data)
            return kernel_ids[key]

        for target in (44459,44466):
            original = local|dict(zip(RIM,caps['states'][target]))
            eta = original[y]
            for j in incidence[target]:
                bs = partition[j]
                lookup = {i:k for k,b in enumerate(bs) for i in b}
                # Every zi's actual component contains its unique same-palette P endpoint.
                base_membership = {v:lookup[RIM.index(v)] for v in RIM}
                for zi in [f'z{i}' for i in range(1,6)]:
                    pair = {0,1} if original[zi] in (0,1) else {2,3}
                    endpoints = [t for t in P if t in graph[zi] and original[t] in pair]
                    require(len(endpoints) == 1,'a face point lost its unique same-palette P endpoint')
                    base_membership[zi] = base_membership[endpoints[0]]
                for pair in ((0,1),(2,3)):
                    for group in old.graph_components(graph,original,pair):
                        contacts = [v for v in group if v in RIM]
                        require(len({base_membership[v] for v in contacts}) <= 1,
                                'a source column splits a known local original component')
                markers = [k for k,b in enumerate(bs) if original[RIM[b[0]]]//2 == eta//2]+[None]
                for marked in markers:
                    membership = dict(base_membership)
                    # None records a private boundary-free component, held fixed.
                    membership[y] = len(bs) if marked is None else marked
                    all_kernels = []
                    for mask in range(1 << len(bs)):
                        colors = {v:(co^1 if mask >> membership[v]&1 else co) for v,co in original.items()}
                        require(all(colors[a] != colors[b] for a in graph for b in graph[a]),
                                'a complete same-orbit component action is locally improper')
                        all_kernels.append(kernel_ref(colors))
                    bad_masks = [mask for mask,ref in enumerate(all_kernels) if kernels[ref]['has_bad_cap']]
                    marked_contacts = [] if marked is None else [RIM[i] for i in bs[marked]]
                    rec = {'center':P[center_index],'target':target,'source_column':j,
                           'source_literal_A':[[v,original[v]] for v in A],
                           'marked_y_component_boundary_contacts':marked_contacts,
                           'boundary_free_y_component':marked is None,
                           'component_membership_on_known_original_graph':membership,
                           'all_orbit_masks_kernel_ids':all_kernels,
                           'all_bad_masks':bad_masks,'conditional_branch_excluded':bool(bad_masks)}
                    if bad_masks:
                        # A single complete component always suffices here.
                        singles = [m for m in bad_masks if m and (m & (m-1)) == 0]
                        require(bool(singles),'a claimed one-component short proof needs a union')
                        if center_index in (2,4):
                            a_block = base_membership['a']
                            p_contacts = [t for t in P if base_membership[t] == a_block]
                            family = tuple(p_contacts)
                            chosen = a_block if family == ('n',) else base_membership['u4']
                            mask = 1 << chosen
                            require(mask in bad_masks,'the fixed short-proof component does not reach a zero cap')
                            if family == ('n',):
                                desired = [2,1,3,2,1,2] if center_index == 2 else [2,1,2,1,3,2]
                                left,right = [2,0,1,0],[1,0,3]
                            else:
                                inside = marked == chosen
                                if family == ('n','u1'):
                                    desired = ([3,1,2 if inside else 3,1,3,1] if center_index == 2
                                               else [3,1,3,1,2 if inside else 3,1])
                                else:
                                    require(family in (('n','u3'),('n','u3','u1')),'unexpected source family')
                                    desired = ([3,1,2 if inside else 3,1,2,1] if center_index == 2
                                               else [3,1,2,1,2 if inside else 3,1])
                                left,right = [2,1,2,0],[0,1,3]
                            kr = kernels[all_kernels[mask]]
                            row = next((r for r in kr['all_same_E_strip_lifts'] if r['P_colors'] == desired),None)
                            require(row is not None,'the paper short proof uses an unavailable same-E P lift')
                            bad = next((r for r in cap_pool[row['cap_pool_id']]['all_bad_full_cap_lifts']
                                        if r['graph'] == 'G' and r['row'] == '01021'
                                        and r['left_cap'] == left and r['right_cap'] == right),None)
                            require(bad is not None,'the fixed original G01021 witness is missing')
                            rec['fixed_short_proof'] = {'family_P_contacts':p_contacts,
                                'swap_whole_boundary_component':[RIM[i] for i in bs[chosen]],
                                'mask':mask,'P_colors':desired,'bad_full_cap_lift':bad}
                            families[(P[center_index],target,family)] = True
                        else:
                            mask = singles[0]
                            rec['one_component_zero_witness_mask'] = mask
                    elif center_index == 5:
                        require(marked == base_membership['a'],'L survivor does not have Y in K01(a)')
                    summary[(P[center_index],target,marked is None,bool(bad_masks))] += 1
                    cases.append(rec)
    require(len(cases) == 250,'complete marked-Y branch coverage changed')
    require(all(r['conditional_branch_excluded'] for r in cases if r['center'] in ('u3','u1')),
            'u3/u1 has an uncovered source branch')
    survivors = [r for r in cases if not r['conditional_branch_excluded']]
    require(len(survivors) == 20 and all(r['center'] == 'L' for r in survivors),
            'the exact L marked-component stopping point changed')
    return {'base':BASE,'inputs':inputs,'scope':'same original profile0 K1 center u3/u1/L',
        'all_original_family_columns_scanned':len(orbit['columns']),
        'all_original_target_01_incident_columns':{str(k):v for k,v in incidence.items()},
        'complete_original_columns':columns,'complete_cap_pool':cap_pool,
        'complete_same_E_strip_kernel_pool':kernels,'complete_marked_Y_cases':cases,
        'summary':[{'center':c,'target':t,'boundary_free_Y':free,'excluded':bad,'cases':n}
                   for (c,t,free,bad),n in sorted(summary.items())],
        'profile0_K1_positions_newly_excluded':['u3','u1'],
        'profile0_K1_L_forcing':'K01(Y) = K01(a), hence it contains a,n,c',
        'L_surviving_marked_cases':len(survivors),
        'actual_E_source_realization_claimed':False,'profile0_excluded':False,
        'profile1_excluded':False,'general_W7':'OPEN','new_Lean':False,'LP_run':False}


def verify(cert,expected):
    require(packed(cert) == packed(expected),'damaged complete source history, cap lift, or enlarged closure')


def controls(cert):
    def omit(c):
        c['all_original_target_01_incident_columns']['44459'].pop()
    def split(c):
        c['complete_marked_Y_cases'][0]['component_membership_on_known_original_graph']['z1'] = -1
    def cap(c):
        r = next(r for r in c['complete_marked_Y_cases'] if 'fixed_short_proof' in r)
        r['fixed_short_proof']['bad_full_cap_lift']['left_cap'][0] = 0
    def claim(c):
        c['profile0_excluded'] = True
    mutations = [('omit_original_source_column',omit),('split_original_face_component',split),
                 ('corrupt_full_cap_witness',cap),('claim_whole_profile0_exclusion',claim)]
    rejected = []
    for name,change in mutations:
        bad = deepcopy(cert)
        change(bad)
        try:
            verify(bad,cert)
        except ValueError:
            rejected.append(name)
    require(len(rejected) == len(mutations),'a negative source control was accepted')
    return rejected


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--build',action='store_true')
    ap.add_argument('--certificate',type=Path)
    args = ap.parse_args()
    require(not(args.build and args.certificate),'conflicting certificate options')
    expected = compute()
    path = args.certificate or HERE/'certificate.json'
    if args.build:
        with path.open('x') as stream:
            json.dump(expected,stream,indent=2,sort_keys=True)
            stream.write('\n')
    else:
        verify(json.loads(path.read_text()),expected)
    print(json.dumps({'result':'PASS: profile0 K1 u3/u1 excluded; L requires K01(Y)=K01(a)',
        'source_columns_per_target':[10,10],'marked_cases':250,
        'same_E_complete_strip_kernels':len(expected['complete_same_E_strip_kernel_pool']),
        'complete_literal_cap_kernels':len(expected['complete_cap_pool']),
        'L_surviving_marked_cases':20,'newly_excluded_positions':['u3','u1'],
        'negative_controls_rejected':controls(expected),'whole_profile_excluded':False},sort_keys=True))


if __name__ == '__main__':
    main()
