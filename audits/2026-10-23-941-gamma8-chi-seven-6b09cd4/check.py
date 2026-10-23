#!/usr/bin/env python3
"""Independent cap/complete-lift replay; no unknown source-disk enumeration."""
import argparse
from copy import deepcopy
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import random

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BASE='6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'
PREV='audits/2026-10-23-941-gamma8-u-link-6b09cd4/certificate.json'
BOUND=['U','p_d','d','zeta','x','p_x']
INNER=['r','T','s','tau','m','n','u','v']


def require(value,message):
    if not value:raise ValueError(message)


def custody():
    info=json.loads((HERE/'INPUTS.json').read_text())
    require(info['base']==BASE and len(info['immutable_inputs'])==10,'input domain')
    require((HERE/'BASE').read_text().strip()==BASE,'BASE drift')
    for row in info['immutable_inputs']:
        for path in [HERE/row['snapshot'],ROOT/row['path']]:
            raw=path.read_bytes()
            require((len(raw),sha256(raw).hexdigest())==(row['bytes'],row['sha256']),'immutable drift: '+str(path))
    return len(info['immutable_inputs'])


def edge(a,b):return tuple(sorted((a,b)))


def domains():
    # Directly normalize all 4096 literal six-tuples, retaining every proper
    # S4 orbit, including those whose complete cap fibre is empty.
    words=set()
    for tup in product(range(4),repeat=6):
        if any(a==b for a,b in zip(tup,tup[1:]+tup[:1])):continue
        names={};words.add(tuple(names.setdefault(c,len(names)) for c in tup))
    require(len(words)==31,'proper six-frame count')
    return [list(w) for w in sorted(words)]


def topology(cap):
    es={tuple(e) for e in cap['edges']};fs=[tuple(f) for f in cap['faces']]
    incidence={e:[] for e in es}
    for i,f in enumerate(fs):
        require(len(set(f))==3,'degenerate face')
        for a,b in combinations(f,2):incidence[edge(a,b)].append(i)
    rim={edge(a,b) for a,b in zip(BOUND,BOUND[1:]+BOUND[:1])}
    require({e for e,v in incidence.items() if len(v)==1}==rim,'boundary incidence')
    require(all(len(v)==(1 if e in rim else 2) for e,v in incidence.items()),'edge manifold')
    dual={i:set() for i in range(len(fs))}
    for uses in incidence.values():
        if len(uses)==2:
            a,b=uses;dual[a].add(b);dual[b].add(a)
    reached={0};pending=[0]
    while pending:
        for j in dual[pending.pop()]-reached:reached.add(j);pending.append(j)
    require(len(reached)==len(fs),'connected face union')
    # Coherent orientation follows shared edges, never independent star flips.
    signs={0:1};pending=[0]
    def direction(face,a,b):
        seq=list(face);return 1 if (seq.index(b)-seq.index(a))%3==1 else -1
    while pending:
        i=pending.pop()
        for j in dual[i]:
            a,b=sorted(set(fs[i])&set(fs[j]));want=-signs[i]*direction(fs[i],a,b)*direction(fs[j],a,b)
            if j in signs:require(signs[j]==want,'shared orientation')
            else:signs[j]=want;pending.append(j)
    for center in BOUND+INNER:
        link={}
        for f in fs:
            if center in f:
                a,b=[v for v in f if v!=center];link.setdefault(a,set()).add(b);link.setdefault(b,set()).add(a)
        require(sum(len(v)==1 for v in link.values())==(2 if center in BOUND else 0),'vertex-link ends')
        require(all(1<=len(v)<=2 for v in link.values()),'branched vertex link')
        seen={next(iter(link))};todo=list(seen)
        while todo:
            for v in link[todo.pop()]-seen:seen.add(v);todo.append(v)
        require(len(seen)==len(link),'disconnected vertex link')
    require((len(BOUND)+len(INNER),len(es),len(fs))==(14,33,20),'cap size')
    require(14-len(es)+len(fs)==1,'Euler disk')


def all_lifts(cap,word):
    adj={v:set() for v in BOUND+INNER}
    for a,b in cap['edges']:adj[a].add(b);adj[b].add(a)
    # Fixed variable order, distinct from predecessor's dynamic CSP ordering.
    order=sorted(INNER,key=lambda v:(-len(adj[v]),v))
    colors=dict(zip(BOUND,word));found=[]
    def visit(i):
        if i==len(order):found.append([colors[v] for v in INNER]);return
        v=order[i];used={colors[w] for w in adj[v] if w in colors}
        for c in range(4):
            if c not in used:colors[v]=c;visit(i+1);del colors[v]
    visit(0);return sorted(found)


def reconstruct(prior,words):
    cells=prior['complete_predecessor_certificate']['complete_predecessor_certificate']
    for _ in range(3):cells=cells['complete_predecessor_certificate']
    original={r['id']:r for r in cells['candidates']}
    groups={}
    for row in prior['star_restrictions']:
        c=original[row['cell']]
        links=dict(row['full_links'],m=['r','T','n','u','v'],T=['r','tau','s','n','m'])
        es={tuple(e) for e in c['edges'] if set(e)<=set(BOUND+INNER)}
        for center,link in links.items():
            es.update(edge(center,v) for v in link)
            es.update(edge(a,b) for a,b in zip(link,link[1:]+link[:1]))
        adj={v:set() for v in BOUND+INNER}
        for a,b in es:adj[a].add(b);adj[b].add(a)
        require(adj['tau']==set(c['full_private_stars']['tau']),'tau original full star')
        for center,link in links.items():require(adj[center]==set(link),'full-star union drift')
        fs={tuple(sorted((a,b,v))) for a,b in es for v in adj[a]&adj[b]}
        key=tuple(sorted(es))
        if key not in groups:groups[key]=dict(boundary=BOUND,inner=INNER,edges=[list(e) for e in sorted(es)],faces=[list(f) for f in sorted(fs)],source_rows=[])
        groups[key]['source_rows'].append(dict(cell=row['cell'],family=row['family'],nx=row['n_x_edge']))
    out=[]
    for i,cap in enumerate(groups.values()):
        cap['id']=i;topology(cap)
        cap['relations']=[dict(word=w,full_lifts=all_lifts(cap,w)) for w in words]
        cap['statistics']=dict(vertices=14,edges=33,faces=20,nonempty=sum(bool(r['full_lifts']) for r in cap['relations']),total_lifts=sum(len(r['full_lifts']) for r in cap['relations']))
        out.append(cap)
    return out


def validate(cert,seed=0):
    require(cert['schema']=='941-gamma8-chi-seven-sealed-caps-v1' and cert['base']==BASE,'schema/BASE')
    require(cert['paper_domain']==dict(j=2,M2_nonempty=True,exterior_private_count=7,same_original_graph=True,literal_frame=True,E_may_be_rootless=True),'paper domain')
    require(cert['chi_options']==[dict(original_color=2,original_component='L02(z4)',successor_component='C12(U)'),dict(original_color=3,original_component='B13(V)',successor_component='A03(a)')],'chi ownership')
    table=[]
    for chi,r in product([2,3],range(4)):
        if chi==r:reason='same_color'
        elif {chi,r}<={0,2}:reason='different_complete_02'
        elif {chi,r}<={1,3}:reason='different_complete_13'
        else:reason='rootless_component_would_be_rooted'
        table.append(dict(chi_color=chi,rootless_color=r,adjacency_allowed=False,reason=reason))
    require(cert['entire_rootless_branch_anticompleteness']==table,'chi/rootless adjacency')
    # Bounds make their own finite domain: n<=1, degree_m<=5, D<=5.
    equalities=[]
    for n in range(1,8):
        for degree_m in range(5,13):
            for b in range(3):
                if n+3+degree_m-b>7:continue
                for D in range(5,11):
                    if D+degree_m-3<=7:equalities.append([n,degree_m,b,D])
    require(equalities==[[1,5,2,5]],'seven equality arithmetic')
    require(cert['equality_consequences']==dict(M2=['m'],M=['T','m'],degree_T=5,degree_m=5,bGamma_m=2,m_side='C',d_not_U=True,U_u_edge=True,exterior_private_vertices=['m','n','u','v','p_d','p_x','chi'],chi_strictly_outside_sealed_cap=True,chi_anticomplete_cap_interior=True),'seven equality consequences')
    prior=json.loads((HERE/'frozen'/PREV).read_text())
    require(cert['inherited_star_restrictions']==prior['star_restrictions'],'old complete star rows lost')
    require(len(cert['inherited_star_restrictions'])==60,'complete row count')
    require(cert['predecessor_preservation']==dict(complete_fibres_including_empty=True,all_full_lifts=True,frozen_certificate=PREV,inherited_scopes=['60_rootless_complete_star_rows','fixed_K2_N_side_arcs','16_sealed_K6_caps'],exterior_B_and_full_U_F_link='requires_fresh_join_when_chi3'),'inheritance scope drift')
    words=domains();require(cert['proper_S4_words']==words and cert['boundary']==BOUND and cert['inner']==INNER,'ordered cap frame')
    caps=reconstruct(prior,words);require(len(caps)==16,'cap class count')
    indices=list(range(16));random.Random(seed).shuffle(indices)
    for i in indices:require(cert['caps'][i]==caps[i],'full cap/fibre mismatch '+str(i))
    require(len(cert['caps'])==16,'extra cap')
    require(cert['authority_boundaries']==dict(finite_control='triggered and holds',source_realizability='not triggered',paper_result='conditional_sealed_cap_inheritance',seven_point_exclusion='requires_separate_safe_replacement',eleven_type_exclusions=0,common_k_lower_bound=23,general_wrong_side='OPEN',new_Lean=False,new_LP=False,smaller_bad=False),'authority boundary drift')
    return dict(status='PASS',chi_rootless_cases=len(table),arithmetic_equalities=equalities,inherited_star_rows=60,caps=16,ordered_boundary_rows=16*31,empty_fibres=sum(not r['full_lifts'] for c in caps for r in c['relations']),total_full_lifts=sum(c['statistics']['total_lifts'] for c in caps),source_realizability='not triggered',seven_point_exclusion='requires_separate_safe_replacement')


def negative(cert):
    changes=[
        ('chi_to_rootless_edge',lambda c:c['entire_rootless_branch_anticompleteness'][1].update(adjacency_allowed=True)),
        ('second_M2',lambda c:c['equality_consequences']['M2'].append('m2')),
        ('chi_inside_cap',lambda c:c['equality_consequences'].update(chi_strictly_outside_sealed_cap=False)),
        ('lost_full_star',lambda c:c['inherited_star_restrictions'][0]['full_links']['n'].pop()),
        ('old_B_inherited',lambda c:c['predecessor_preservation'].update(exterior_B_and_full_U_F_link='inherited')),
        ('lost_full_lift',lambda c:next(r for r in c['caps'][0]['relations'] if r['full_lifts'])['full_lifts'].pop()),
        ('lost_empty_fibre',lambda c:c['caps'][0]['relations'].remove(next(r for r in c['caps'][0]['relations'] if not r['full_lifts']))),
        ('false_source',lambda c:c['authority_boundaries'].update(source_realizability='triggered and holds')),
        ('false_exclusion',lambda c:c['authority_boundaries'].update(seven_point_exclusion='PROVED'))]
    for label,change in changes:
        other=deepcopy(cert);change(other)
        try:validate(other)
        except (ValueError,KeyError,IndexError):continue
        raise ValueError('negative accepted: '+label)
    return dict(status='PASS',negative_controls_rejected=len(changes),labels=[name for name,_ in changes])


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--certificate',type=Path,default=HERE/'certificate.json');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--negative',action='store_true');args=ap.parse_args()
    count=custody();cert=json.loads(args.certificate.read_text())
    result=negative(cert) if args.negative else validate(cert,args.seed)
    result.update(frozen_inputs=count,immutable_drift=0);print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
