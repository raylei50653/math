#!/usr/bin/env python3
"""Original type-II double-five patch, full joint lifts and same-F orbits.

Only private/private U,V gives a simple 14-cycle F boundary.  Tail aliases
instead use all color-compatible set partitions after equal-vertex union;
no disk Euler or noncrossing sufficiency is imposed on those cases.
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
PRIOR = 'audits/2026-10-21-w7-k1-mixed-30dde27'
COLLAR = 'audits/2026-10-21-w7-profile0-13e51db/check.py'
HELPER = PRIOR+'/transport/check.py'
RESIDUAL = PRIOR+'/full-exterior-v3.json.gz'
RIM = ['a','n','u4','u3','u2','u1','L','q','c','s','v','w','t']
P = ['n','u4','u3','u2','u1','L']
INNER = P+['z5','K']
F_WALK = ['a','z1','z2','z3','z4','V','U','HL_0','q','c','s','v','w','t']
E_RIM = ['a','z1','z2','z3','z4','z5','HL_0','q','c','s','v','w','t']


def require(ok,message):
    if not ok:
        raise ValueError(message)


def packed(x):
    return json.dumps(x,sort_keys=True,separators=(',',':'))


def load_module(path,name):
    sp = importlib.util.spec_from_file_location(name,path)
    out = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(out)
    return out


def normalized_groups(groups):
    return sorted(sorted(row) for row in groups)


def canonical(t):
    d = {}
    return tuple(d.setdefault(x,len(d)) for x in t)


def prepare():
    manifest = json.loads((HERE/'BASE.json').read_text())
    require(manifest['base'] == BASE,'exclusive BASE changed')
    inputs,data = {},{}
    for rec in manifest['inputs']:
        raw = (HERE/'frozen'/rec['path']).read_bytes()
        require(len(raw) == rec['bytes'] and sha256(raw).hexdigest() == rec['sha256'],
                'frozen source drift: '+rec['path'])
        require((ROOT/rec['path']).read_bytes() == raw,'live source drift: '+rec['path'])
        inputs[rec['path']] = {k:rec[k] for k in ('bytes','sha256','authority')}
        if rec['path'].endswith('.gz'):
            data[rec['path']] = json.loads(gzip.decompress(raw))
    caps = data[SOURCE+'/counting/caps.json.gz']
    orbit = data[SOURCE+'/counting/orbits.json.gz']
    require(caps['ordered_rim'] == RIM and len(orbit['columns']) == 307197,'original D authority changed')
    helper = load_module(HERE/'frozen'/HELPER,'frozen_complete_cap_assignments')
    collar = load_module(HERE/'frozen'/COLLAR,'frozen_original_collar')
    return inputs,caps,orbit,data[RESIDUAL]['L_complete_residual'],helper,collar


def typed_nc(side):
    """All NC partitions respecting boundary edges and the disk block count."""
    transitions = sum(side[i] != side[(i+1)%len(side)] for i in range(len(side)))
    wanted = transitions//2+1
    def visit(t,stack,palettes):
        i = len(t)
        if len(palettes)>wanted:
            return
        if i == len(side):
            if len(palettes) == wanted and (side[0] != side[-1] or t[0] == t[-1]):
                yield t
            return
        if side[i] == side[i-1]:
            yield from visit(t+(t[-1],),stack,palettes)
            return
        for j,x in enumerate(stack):
            if palettes[x] == side[i]:
                yield from visit(t+(x,),stack[:j+1],palettes)
        if len(palettes)<wanted:
            yield from visit(t+(len(palettes),),stack+(len(palettes),),palettes+(side[i],))
    yield from visit((0,),(0,),(side[0],))


def all_set_partitions(n,t=(0,),blocks=1):
    if n == 0:
        yield ()
        return
    if len(t) == n:
        yield t
        return
    for x in range(blocks+1):
        yield from all_set_partitions(n,t+(x,),max(blocks,x+1))


class DSU:
    def __init__(self,vertices):
        self.parent = {v:v for v in vertices}
    def find(self,v):
        while self.parent[v] != v:
            v = self.parent[v]
        return v
    def union(self,a,b):
        self.parent[self.find(a)] = self.find(b)


def alias_partition_cover(names,side):
    """All possible component identifications; no topology assumptions."""
    dsu = DSU(names)
    for i,a in enumerate(names):
        j = (i+1)%len(names)
        if side[i] == side[j]:
            dsu.union(a,names[j])
    bases = [sorted({dsu.find(names[i]) for i in range(len(names)) if side[i] == p}) for p in (0,1)]
    for p0,p1 in product(all_set_partitions(len(bases[0])),all_set_partitions(len(bases[1]))):
        groups = {root:(p0[j] if p == 0 else max(p0)+1+p1[j])
                  for p,roots in enumerate(bases) for j,root in enumerate(roots)}
        rename = {}
        yield tuple(rename.setdefault(groups[dsu.find(v)],len(rename)) for v in names)


def initial_E_join(names,word,partition,mate,replace):
    pairs = [(0,mate),tuple(c for c in range(4) if c not in (0,mate))]
    colors = dict(zip(names,word))|{'z5':3,'K':2}
    dsu = DSU(colors)
    for b in sorted(set(partition)):
        group = [names[i] for i,x in enumerate(partition) if x == b]
        for v in group[1:]:
            dsu.union(group[0],v)
    edges = [('z4','z5'),('z5','HL_0')]+[('K',replace.get(z,z)) for z in ('HL_0','U','V','z4','z5')]
    for a,b in edges:
        if any(colors[a] in pair and colors[b] in pair for pair in pairs):
            dsu.union(a,b)
    groups = defaultdict(list)
    for v in E_RIM:
        groups[dsu.find(v)].append(v)
    return normalized_groups(groups.values())


def graph_for(collar,uname,vname):
    _,graph = collar.collar(0,[0,0,0,0,0,1],with_graph=True)
    graph = {v:adj-{'p','h','R'} for v,adj in graph.items() if v not in {'p','h','R'}}
    for i,a in enumerate(RIM):
        b = RIM[(i+1)%13]
        graph.setdefault(a,set()).add(b)
        graph.setdefault(b,set()).add(a)
    replace = {'U':uname,'V':vname}
    for a,b in [('HL_0','U'),('U','V'),('V','z4')]+[('K',z) for z in ('HL_0','U','V','z4','z5')]:
        a,b = replace.get(a,a),replace.get(b,b)
        graph.setdefault(a,set()).add(b)
        graph.setdefault(b,set()).add(a)
    require(graph['z5'] == {'L','u1','z4','K','HL_0'},'the original z5 full five-star changed')
    require(graph['K'] == {'HL_0',uname,vname,'z4','z5'},'the original K full five-star changed')
    require(uname not in graph['z5'] and vname not in graph['z5'],'type-II original nonedges were lost')
    return graph,replace


def compute():
    inputs,caps,orbit,residual,helper,collar = prepare()
    index = {tuple(t):i for i,t in enumerate(caps['states'])}
    live = set(orbit['live'])
    cap_pool,cap_ids,kernel_pool,kernel_ids = [],{},[],{}

    def cap_ref(row):
        key = tuple(row)
        if key not in cap_ids:
            sid = index[canonical(row)]
            data = helper.full_caps(key)
            require(all(data['full_cap_counts'][g] == [caps['matrices'][g][r][sid] for r in range(10)]
                        for g in helper.ZERO),'complete cap assignments disagree with frozen original matrices')
            data = dict(data,canonical_state=sid,original_D_fibre_proved_zero=sid not in live)
            cap_ids[key] = len(cap_pool)
            cap_pool.append(data)
        return cap_ids[key]

    identities = [(44459,'U','V'),(44459,'U','w'),(44459,'v','V'),(44459,'v','w'),
                  (44466,'U','V'),(44466,'w','V')]
    original_cases,partition_cases,summaries = [],[],[]
    for target,uname,vname in identities:
        graph,replace = graph_for(collar,uname,vname)
        names = [replace.get(v,v) for v in F_WALK]
        original = ((0,3,0,3,0,1,0,1,3,1,2,0,1,2) if target == 44459
                    else (0,3,0,3,0,1,0,1,3,1,2,1,0,2))
        private = uname == 'U' and vname == 'V'
        identity_label = f'{target}:U={uname}:V={vname}'

        def kernel_ref(word):
            key = (identity_label,tuple(word))
            if key in kernel_ids:
                return kernel_ids[key]
            fixed = dict(zip(names,word))
            require(all(fixed[names[i]] == word[i] for i in range(14)),
                    'one actual aliased vertex acquired two different colors')
            require(all(fixed[a] != fixed[b] for a in fixed for b in graph[a] if b in fixed),
                    'an actual exterior component action broke an original exterior edge')
            lifts = []
            def visit(assigned):
                remaining = set(INNER)-assigned.keys()
                if not remaining:
                    complete = fixed|assigned
                    ref = cap_ref([complete[v] for v in RIM])
                    lifts.append({'all_eight_inner_colors':[complete[v] for v in INNER],
                                  'literal_D_rim':[complete[v] for v in RIM],'cap_pool_id':ref})
                    return
                colors = fixed|assigned
                domains = {v:set(range(4))-{colors[w] for w in graph[v] if w in colors} for v in remaining}
                v = min(remaining,key=lambda v:(len(domains[v]),v))
                for color in sorted(domains[v]):
                    visit(assigned|{v:color})
            visit({})
            lifts.sort(key=lambda r:r['all_eight_inner_colors'])
            data = {'identity':identity_label,'ordered_F_boundary_walk':names,
                    'literal_F_boundary_walk':list(word),'inner_order':INNER,
                    'all_joint_eight_point_lifts':lifts,
                    'empty_joint_fibre':not lifts,
                    'has_original_D_zero_lift':any(cap_pool[r['cap_pool_id']]['original_D_fibre_proved_zero'] for r in lifts),
                    'has_original_forbidden_cap_lift':any(cap_pool[r['cap_pool_id']]['all_bad_full_cap_lifts'] for r in lifts)}
            kernel_ids[key] = len(kernel_pool)
            kernel_pool.append(data)
            return kernel_ids[key]

        initial = kernel_ref(original)
        require(len(kernel_pool[initial]['all_joint_eight_point_lifts']) == 6 and
                not kernel_pool[initial]['has_original_D_zero_lift'] and
                not kernel_pool[initial]['has_original_forbidden_cap_lift'],
                'the original double-five six-lift calibration changed')
        original_cases.append({'identity':identity_label,'target':target,'U_actual_name':uname,'V_actual_name':vname,
            'simple_private_F_boundary':private,'original_joint_kernel_ref':initial,
            'complete_z5_star':sorted(graph['z5']),'complete_K_star':sorted(graph['K'])})
        for mate in (1,2,3):
            pairs = [(0,mate),tuple(c for c in range(4) if c not in (0,mate))]
            side = tuple(0 if c in pairs[0] else 1 for c in original)
            source = next(r for r in residual if r['E_state'] == (560 if target == 44459 else 572)
                          and r['split_containing_0'] == [0,mate])
            require(source['literal_E_target'] ==
                    [original[F_WALK.index(v)] if v != 'z5' else 3 for v in E_RIM],
                    'the inherited original E partition changed its literal source frame')
            expected = {packed(normalized_groups(r['component_blocks'])):r['column_id']
                        for r in source['complete_surviving_columns']}
            parts = list(typed_nc(side) if private else alias_partition_cover(names,side))
            source_pass,final_pass = [],[]
            for pid,part in enumerate(parts):
                require(all(side[i] == side[j] for i in range(14) for j in range(14) if part[i] == part[j]),
                        'a proposed actual component mixes palettes')
                require(all(part[i] == part[j] for i in range(14) for j in range(14) if names[i] == names[j]),
                        'an actual tail alias was split into two components')
                merged = initial_E_join(names,original,part,mate,replace)
                old_column = expected.get(packed(merged))
                rec = {'identity':identity_label,'mate_of_zero':mate,'partition_id':pid,
                       'original_partition':list(part),'source_E_joined_blocks':merged,
                       'source_E_original_column':old_column,'all_same_partition_action_kernel_refs':[],
                       'all_zero_action_masks':[],'necessary_partition_survives':False}
                if old_column is not None:
                    source_pass.append(pid)
                    for mask in range(1 << (max(part)+1)):
                        word = tuple((pairs[side[i]][0]^pairs[side[i]][1]^c) if mask>>part[i]&1 else c
                                     for i,c in enumerate(original))
                        ref = kernel_ref(word)
                        rec['all_same_partition_action_kernel_refs'].append(ref)
                        # Empty joint fibre does not prove an exterior fibre empty.
                        if kernel_pool[ref]['has_original_D_zero_lift']:
                            rec['all_zero_action_masks'].append(mask)
                    if not rec['all_zero_action_masks']:
                        final_pass.append(pid)
                        rec['necessary_partition_survives'] = True
                partition_cases.append(rec)
            transitions = sum(side[i] != side[(i+1)%14] for i in range(14))
            summaries.append({'identity':identity_label,'mate_of_zero':mate,
                'palette_transitions_in_boundary_walk':transitions,
                'cover':'all typed noncrossing disk partitions' if private else 'all palette set partitions after actual-vertex and boundary-edge unions',
                'initial_partitions':len(parts),'passes_same_initial_E_join':source_pass,
                'final_necessary_survivors':final_pass,
                'source_subcase_excluded':not final_pass,
                'complete_multi_disk_realizability_family_claimed':False})
    require([r['initial_partitions'] for r in summaries if r['identity'] in
             ('44459:U=U:V=V','44466:U=U:V=V')] == [42,42,14,42,42,14],
            'the private/private typed partition coverage changed')
    require([len(r['final_necessary_survivors']) for r in summaries] ==
            [4,4,3,2,5,6,2,8,3,2,2,2,4,4,3,2,0,3],
            'the exact double-five stopping point changed')

    # Full five-boundary interface relation for deleting original K and
    # adding the two type-I fan diagonals.  These ten rows cover all literal
    # proper Q5 tuples by one common global color permutation.
    q5_relations = []
    for row in helper.ROWS:
        t = list(map(int,row))
        require(all(t[i] != t[(i+1)%5] for i in range(5)),'the Q5 interface row is improper')
        old = [c for c in range(4) if c not in t]
        new = int(t[4] != t[1] and t[4] != t[2])
        q5_relations.append({'literal_Q5_order':['Y','U','V','z4','z5'],'canonical_literal':t,
                            'all_old_K_lifts':old,'all_new_empty_lifts':[[]] if new else [],
                            'old_nonempty':bool(old),'new_nonempty':bool(new)})
    require(sum(r['old_nonempty'] for r in q5_relations) == 5 and
            sum(r['new_nonempty'] for r in q5_relations) == 4 and
            sum(r['old_nonempty'] and r['new_nonempty'] for r in q5_relations) == 1,
            'the complete Q5 replacement obstruction changed')
    # The B alias contradiction is a direct original two-edge 02 path.
    b02 = next(r for r in residual if r['E_state'] == 572 and r['split_containing_0'] == [0,2])
    require(all(not any('w' in b and 'z4' in b for b in r['component_blocks'])
                for r in b02['complete_surviving_columns']), 'the B w/z4 separation disappeared')
    require(next(r for r in summaries if r['identity'] == '44466:U=w:V=V' and r['mate_of_zero'] == 2)
            ['passes_same_initial_E_join'] == [], 'the original B alias contradiction was not reconstructed')
    for eid,expected in [(560,['HL_0','t','w']),(572,['HL_0','t'])]:
        old12 = next(r for r in residual if r['E_state'] == eid and r['split_containing_0'] == [0,3])
        require(len(old12['complete_surviving_columns']) == 1,'the original complete E12 source block changed')
        block = next(b for b in old12['complete_surviving_columns'][0]['component_blocks'] if 'HL_0' in b)
        require(sorted(block) == expected,'the original V tail-identity gate changed')
    return {'base':BASE,'inputs':inputs,'scope':'original typeII Q5 with complete z5/K degree-five stars',
        'original_identity_cases':original_cases,'complete_literal_cap_kernel_pool':cap_pool,
        'complete_literal_joint_kernel_pool':kernel_pool,'complete_fixed_partition_cases':partition_cases,
        'partition_summaries':summaries,'complete_Q5_old_wheel_new_fan_relations':q5_relations,
        'original_alias_source_subcase_excluded':{'target':44466,'U':'w','reason':'same original E 02 path w-K-z4 contradicts both inherited whole E partitions',
            'all_original_02_columns':[r['column_id'] for r in b02['complete_surviving_columns']]},
        'V_tail_identity_gate':{'44459':['new private V','w'],'44466':['new private V'],
            'reason':'original K2 joins V1 to Y1 in the same original E12 component'},
        'all_typeII_sources_excluded':False,'conditional_legal_smaller_replacement_proved':False,
        'cross_palette_common_source_realization_claimed':False,'LP_run':False,'new_Lean':False}


def verify(cert,expected):
    require(packed(cert) == packed(expected),'damaged complete double-five relation or expanded source conclusion')


def controls(cert):
    def omit(c):
        r = c['original_identity_cases'][0]['original_joint_kernel_ref']
        c['complete_literal_joint_kernel_pool'][r]['all_joint_eight_point_lifts'].pop()
    def alias(c):
        next(r for r in c['original_identity_cases'] if r['identity'] == '44459:U=v:V=w')['simple_private_F_boundary'] = True
    def empty(c):
        r = next(r for r in c['complete_literal_joint_kernel_pool'] if r['empty_joint_fibre'])
        r['has_original_D_zero_lift'] = True
    def replace(c):
        c['conditional_legal_smaller_replacement_proved'] = True
    def close(c):
        c['all_typeII_sources_excluded'] = True
    variants = [('omit_joint_eight_point_lift',omit),('split_actual_tail_alias_into_simple14',alias),
                ('empty_patch_fibre_is_not_exterior_zero',empty),('claim_unsupported_delete_K_replacement',replace),
                ('claim_all_typeII_excluded',close)]
    rejected = []
    for name,mutate in variants:
        bad = deepcopy(cert)
        mutate(bad)
        try:
            verify(bad,cert)
        except ValueError:
            rejected.append(name)
    require(len(rejected) == len(variants),'a double-five negative control was accepted')
    return rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build',action='store_true')
    parser.add_argument('--certificate',type=Path)
    args = parser.parse_args()
    require(not(args.build and args.certificate),'conflicting certificate modes')
    expected = compute()
    path = args.certificate or HERE/'certificate.json.gz'
    if args.build:
        with path.open('xb') as raw:
            with gzip.GzipFile(fileobj=raw,mode='wb',mtime=0) as stream:
                stream.write((packed(expected)+'\n').encode())
    else:
        raw = path.read_bytes()
        actual = json.loads(gzip.decompress(raw) if path.suffix == '.gz' else raw)
        verify(actual,expected)
    print(json.dumps({'result':'PASS: typeII B/U=w excluded; remaining double-five sources OPEN',
        'original_identity_cases':6,'original_joint_lifts_each':6,
        'fixed_partition_cases':len(expected['complete_fixed_partition_cases']),
        'joint_kernel_pool':len(expected['complete_literal_joint_kernel_pool']),
        'complete_cap_kernel_pool':len(expected['complete_literal_cap_kernel_pool']),
        'private_partition_survivors':[len(r['final_necessary_survivors']) for r in expected['partition_summaries']
                                      if r['identity'] in ('44459:U=U:V=V','44466:U=U:V=V')],
        'negative_controls_rejected':controls(expected),'all_typeII_excluded':False},sort_keys=True))


if __name__ == '__main__':
    main()
