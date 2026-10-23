#!/usr/bin/env python3
"""Read-only independent reconstruction of the finite contract and negative disk."""
import argparse
from collections import Counter,deque
from copy import deepcopy
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import random
import sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
BASE='cb8f8593e273a7426ecadd59797a6e643cc4768e'
PREV='audits/2026-10-23-three-mask-round3-cb8f859/941/certificate.json'
B14=['a','z1','z2','z3','z4','V','U','HL_0','q','c','s','v','w','t']


def require(ok,message):
    if not ok:raise ValueError(message)


def authority():
    m=json.loads((HERE/'INPUTS.json').read_text());require(m['base']==BASE,'BASE changed')
    for row in m['inputs']:
        data=(HERE/'frozen'/row['path']).read_bytes()
        require((len(data),sha256(data).hexdigest())==(row['bytes'],row['sha256']),'frozen authority drift')
        require(data==(ROOT/row['path']).read_bytes(),'live immutable authority drift: '+row['path'])
    entry=m['entry_base'];data=(HERE/entry['snapshot']).read_bytes()
    require((len(data),sha256(data).hexdigest())==(entry['bytes'],entry['sha256']),'entry BASE drift')
    require(data==(ROOT/entry['path']).read_bytes(),'live BASE drift')
    entries={x['path']:x for x in json.loads(data)['predecessors']}
    for row in m['inputs']:
        if row['path'] in entries:
            require(all(row[k]==entries[row['path']][k] for k in ('bytes','sha256')),'input not at entry bytes')
    routing=[]
    for row in m['routing_entry']:
        data=(HERE/row['snapshot']).read_bytes();live=(ROOT/row['path']).read_bytes()
        require((len(data),sha256(data).hexdigest())==(row['bytes'],row['sha256']),'routing snapshot drift')
        routing.append(dict(path=row['path'],changed=live!=data,entry_sha256=row['sha256'],live_sha256=sha256(live).hexdigest()))
    return m,routing


def components(vertices,edges):
    adjacency={v:set() for v in vertices}
    for a,b in edges:
        if a in adjacency and b in adjacency:adjacency[a].add(b);adjacency[b].add(a)
    result=[]
    while adjacency:
        todo=[min(adjacency)];seen=set()
        while todo:
            v=todo.pop()
            if v not in seen:seen.add(v);todo.extend(adjacency[v]-seen)
        result.append(sorted(seen))
        for v in seen:del adjacency[v]
    return sorted(result)


def path(edges,start,end):
    adjacency={v:set() for e in edges for v in e}
    for a,b in edges:adjacency[a].add(b);adjacency[b].add(a)
    todo=deque([[start]]);seen={start}
    while todo:
        walk=todo.popleft()
        if walk[-1]==end:return walk
        for v in sorted(adjacency[walk[-1]]):
            if v not in seen:seen.add(v);todo.append(walk+[v])
    raise ValueError('required tree route absent')


def verify_negative_disk(g):
    cs=g['colors'];bd=g['boundary'];faces=g['faces']
    require(cs==dict(U=0,r=1,q=3,s=1,x=0,z=2,h=3,j=1),'negative calibration colors changed')
    require(len(set(bd))==len(bd)==6 and len(cs)==8,'negative calibration domain changed')
    incidence={}
    for f in faces:
        require(len(set(f))==3 and set(f)<=set(cs),'malformed triangle')
        for a,b in zip(f,f[1:]+f[:1]):incidence.setdefault(tuple(sorted((a,b))),[]).append((a,b))
    edges=list(incidence)
    require(all(cs[a]!=cs[b] for a,b in edges),'negative calibration improper')
    outer={tuple(sorted((a,b))) for a,b in zip(bd,bd[1:]+bd[:1])}
    require({e for e,fs in incidence.items() if len(fs)==1}==outer,'negative calibration not full disk')
    require(all(len(fs)==1 or (len(fs)==2 and fs[0]==tuple(reversed(fs[1]))) for fs in incidence.values()),'triangle orientation failed')
    require(len(cs)-len(edges)+len(faces)==1,'disk Euler failed')
    for v in cs:
        link=[tuple(x for x in f if x!=v) for f in faces if v in f]
        ns={x for e in link for x in e};degrees=Counter(x for e in link for x in e)
        require(len(components(ns,link))==1,'disconnected vertex link')
        expected=[1,1]+[2]*(len(ns)-2) if v in bd else [2]*len(ns)
        require(sorted(degrees.values())==expected,'boundary or private link incomplete')
    K=next(x for x in components({v for v,c in cs.items() if c in (0,2)},edges) if 'U' in x)
    ps={v:(c^2 if v in K else c) for v,c in cs.items()}
    C=next(x for x in components({v for v,c in ps.items() if c in (1,2)},edges) if 'U' in x)
    outside=sorted(v for v in K if cs[v]==0 and v not in C)
    require(K==g['complete_K'] and [v for v in bd if v in K]==g['complete_K_boundary_contacts']==['U'],'negative K boundary changed')
    require(C==g['successor12_component_of_U'] and outside==g['K0_outside_that_component']==['x'],'invalid K0 connectivity promoted')
    require(g['original941_source_control']=='not triggered','negative control promoted to original source')
    return dict(status='counterexample',original_full_K=K,actual_successor_C=C,K0_outside_C=outside,
                original941_source_control='not triggered')


def marked_link_calibration(seed):
    # Complete local cyclic links only; no source disks or private-size cutoff.
    output={}
    for degree in (5,6):
        words=list(product((0,1,3),repeat=degree));random.Random(seed+degree).shuffle(words)
        count=0;sides=set();no_one=0
        for colors in words:
            if any(colors[i]==colors[(i+1)%degree] for i in range(degree)):continue
            zero=[i for i,c in enumerate(colors) if c==0]
            for membership in product((False,True),repeat=len(zero)):
                marked=dict(zip(zero,membership))
                if not any(membership) or all(membership):continue
                # A link path using only phi0/1 becomes psi2/1. Its zeros must
                # have one actual successor12 component label.
                allowed=True
                for comp in components({i for i,c in enumerate(colors) if c in (0,1)},
                                       [(i,(i+1)%degree) for i in range(degree)]):
                    values={marked[i] for i in comp if i in marked}
                    if len(values)>1:allowed=False;break
                if not allowed:continue
                require(colors.count(0)>=2 and colors.count(3)>=2,'marked link misses separator')
                if degree==5:
                    require(sorted(colors)==[0,0,1,3,3],'wrong degree5 marked-Z link')
                    one=colors.index(1)
                    adjacent=[i for i in ((one-1)%degree,(one+1)%degree) if colors[i]==0]
                    require(len(adjacent)==1,'unique original1 does not have one zero link neighbor')
                    sides.add('C' if marked[adjacent[0]] else 'outside_C')
                no_one+=(1 not in colors);count+=1
        output[str(degree)]=dict(marked_links=count,unique1_sides=sorted(sides),without_original1=no_one)
    require(output['5']['unique1_sides']==['C','outside_C'],'one degree5 side deleted')
    require(output['6']['without_original1']>0,'even high degree branch deleted')
    return output


def validate(c,seed=0):
    prior=json.loads((HERE/'frozen'/PREV).read_text())
    require(c['schema']=='941-round4-certificate-v1' and c['base']==BASE,'certificate BASE/domain')
    require(c['scope']=='same F ordinary short Type-I; initial02 13/36; original T branch versus marked private insertion Z','scope changed')
    require(c['arbitrary_private_size_bound'] is None and c['all_original_X_T_degree_sides_retained'] is True,'old degree/private branch lost')
    require(c['initial03_type9_has_no_X_R_triple_lemma'] is True,'X lemma expanded to03 type9')
    require(c['new_pair_exclusions']==0 and c['source_realized'] is False and c['new_smaller_bad'] is False and c['new_Lean'] is False,'unsupported theorem promotion')
    require(c['full941_source_and_wrong_side_trigger']=='not triggered' and c['finite_disk_survival_controls_added']==0,'finite source control promoted')
    require(c['upstream_complete_fibre_custody']==prior['upstream_complete_fibre_custody'],'empty/full fibre custody lost')
    old={(r['target'],r['initial_02_type']):r for r in prior['source_rows']}
    rows=list(c['source_rows']);random.Random(seed).shuffle(rows)
    require(len(rows)==4 and set((r['target'],r['initial_02_type']) for r in rows)==set(old),'contract rows missing')
    for r in rows:
        p=old[r['target'],r['initial_02_type']]
        require(r['complete_predecessor_record']==p,'predecessor full contacts/caps/lifts changed')
        require(r['initial03_choices']==[4,9],'initial03 alternative omitted')
        jblocks=p['complete_predecessor_record']['complete_initial_02_contacts']
        labels={v:i for i,b in enumerate(jblocks) for v in b};K=labels['U'];B=labels['V']
        require(jblocks[K]==['U'] and labels['HL_0']==B==labels['q']==labels['c'],'original complete K/B premise changed')
        # The original boundary minus U is one path; every boundary component
        # except K occurs on it. This is independent of all private branches.
        boundary_without_U=B14[B14.index('U')+1:]+B14[:B14.index('U')]
        require(len(boundary_without_U)==13 and all(labels[v]!=K for v in boundary_without_U),'boundary-minus-K still meets K')
        projection=[labels[v] for v in boundary_without_U]
        boundary_edges={tuple(sorted((a,b))) for a,b in zip(projection,projection[1:]) if a!=b}
        require(len(components(set(projection),boundary_edges))==1 and B in projection,'boundary components not one B-side walk')
        require(r['all_boundary_components_in_JminusK_B_side'] is True and r['rootless_branches_retained'] is True,'rootless/boundary side obligation changed')
        require(r['T_original02_component_not_assumed_L'] is True,'M identified with L without proof')
        require(r['last_original_K_exit']==dict(next_original1_in_complete_B=True,
                next_original1_successor12_component='actual E_prime, not assumed C'),'last-K exit silently assumes actual C')
        h=p['complete_successor_boundary_components'];named={v:k for k,b in h.items() for v in b}
        h_edges={tuple(sorted((named[a],named[b]))) for a,b in zip(B14,B14[1:]+B14[:1]) if named[a]!=named[b]}
        require(path(h_edges,'C12','D12')==['C12','Q03','D12'],'wrong actual successor path')
        branch=r['branch_implication']
        require(branch['premise']=='M02(T) outside B component of J minus K','wrong-side condition omitted')
        require(branch['wrong_side_T_private'] is True and branch['original01_tail_returns_K0'] is True and
                branch['return_K0_in_Q_side_of_HminusC'] is True,'conditional return path lost')
        z=branch['canonical_Z']
        require(z['quantifier']=='last C exit on an actual K02 path from U to a tail-return x','arbitrary Z substituted for marked Z')
        require(z['original_color']==2 and all(z[k] is True for k in ['private','in_complete_K','in_actual_successor_Q',
            'two_path_neighbors_original0_in_K','first_path_neighbor_in_C','second_path_neighbor_outside_C',
            'all_original0_neighbors_in_K','all_original3_neighbors_in_complete_Q',
            'at_least_two_original0_and_two_original3_neighbors','degree_at_least6_retained',
            'no_original1_even_degree_at_least6_retained']),'marked Z source obligation lost')
        require(z['degree5_neighbor_multiset']==[0,0,1,3,3] and
                z['unique_original1_successor12_sides']==['C','outside_C'],'marked Z degree5 side changed')
        joint=r['type4_joint']
        require(joint['requires_initial03_type']==4 and joint['requires_wrong_original_T_side'] is True,'joint triple scope expanded')
        require(joint['X_T_Z_distinct_private'] is True and joint['three_original_nonedges']==[['X','T'],['X','Z'],['T','Z']],
                'same-source private triple/nonedges changed')
        require(joint['original_B13_path_R_still_in_C'] is True and joint['R_not_identified_with_r_or_s'] is True and
                joint['R_distinct_from_u_and_s'] is True,'B13 and01 witness alias invented')
        require(r['pair_excluded'] is False,'pair exclusion falsely claimed')
    return dict(source_contract_rows=4,conditional_wrong_side_to_marked_Z_rows=4,
        original_boundary_side_reconstructions=4,marked_Z_link_calibration=marked_link_calibration(seed),
        negative_disk=verify_negative_disk(c['negative_graph_control']),new_pair_exclusions=0,
        source_trigger='not triggered')


def negatives(c):
    tests=[
        ('force_all_K0_into_C',lambda x:x['source_rows'][0]['last_original_K_exit'].update(next_original1_successor12_component='C')),
        ('erase_wrong_side_premise',lambda x:x['source_rows'][0]['branch_implication'].update(premise='always')),
        ('identify_M_with_L',lambda x:x['source_rows'][0].update(T_original02_component_not_assumed_L=False)),
        ('delete_rootless',lambda x:x['source_rows'][0].update(rootless_branches_retained=False)),
        ('claim_arbitrary_Z',lambda x:x['source_rows'][0]['branch_implication']['canonical_Z'].update(quantifier='any point of K2 intersect Q')),
        ('put_Z_in_A',lambda x:x['source_rows'][0]['branch_implication']['canonical_Z'].update(in_actual_successor_Q=False)),
        ('delete_Z_degree5_side',lambda x:x['source_rows'][0]['branch_implication']['canonical_Z']['unique_original1_successor12_sides'].pop()),
        ('delete_Z_high_degree',lambda x:x['source_rows'][0]['branch_implication']['canonical_Z'].update(degree_at_least6_retained=False)),
        ('identify_R_with_r',lambda x:x['source_rows'][0]['type4_joint'].update(R_not_identified_with_r_or_s=False)),
        ('apply_X_triple_to_type9',lambda x:x['source_rows'][0]['type4_joint'].update(requires_initial03_type=9)),
        ('delete_XZ_nonedge',lambda x:x['source_rows'][0]['type4_joint']['three_original_nonedges'].pop(1)),
        ('invent_pair_exclusion',lambda x:x.update(new_pair_exclusions=1)),
        ('erase_empty_fibre_custody',lambda x:x['upstream_complete_fibre_custody'].update(empty_seven_point_fibres=0)),
        ('erase_one_full_lift',lambda x:x['source_rows'][0]['complete_predecessor_record']['complete_predecessor_record']['complete_successor_seven_point_kernel']['complete_seven_point_fibre'].pop()),
        ('erase_original_cap_lift',lambda x:x['source_rows'][0]['complete_predecessor_record']['complete_predecessor_record']['complete_successor_original_cap_records'][1]['complete_original_cap_fibres']['Q1']['01021'].pop()),
        ('fake_negative_C',lambda x:x['negative_graph_control']['successor12_component_of_U'].append('x')),
    ]
    result=[]
    for name,mutate in tests:
        bad=deepcopy(c);mutate(bad)
        try:validate(bad)
        except (ValueError,KeyError,IndexError,TypeError):result.append(dict(name=name,status='counterexample rejected'))
        else:raise ValueError('negative falsely accepted: '+name)
    return result


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--negative',action='store_true')
    parser.add_argument('--seed',type=int,default=0);parser.add_argument('--certificate',type=Path,default=HERE/'certificate.json')
    args=parser.parse_args();m,routing=authority();c=json.loads(args.certificate.read_text());stats=validate(c,args.seed)
    result=dict(status='PASS',seed=args.seed,scope=c['scope'],paper_status='conditional arbitrary-size same-source proof; no source exclusion',
        immutable_input_drift=0,frozen_mathematical_inputs=len(m['inputs']),routing_live_drift=routing,
        certificate_sha256=sha256(args.certificate.read_bytes()).hexdigest(),**stats)
    if args.negative:result['semantic_negatives']=negatives(c)
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,IndexError,TypeError,OSError,json.JSONDecodeError) as exc:
        print(json.dumps(dict(status='REJECT',reason=str(exc)),sort_keys=True));sys.exit(1)
