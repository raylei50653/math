#!/usr/bin/env python3
"""Narrow exploratory reconstruction of the six fixed u-link cases."""
import argparse
from copy import deepcopy
from hashlib import sha256
import json
import random
from itertools import combinations, permutations
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = '6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'
PREV = 'audits/2026-10-23-941-gamma8-six-equality-6b09cd4/certificate.json'


def require(ok, why):
    if not ok: raise ValueError(why)


def custody():
    data=json.loads((HERE/'INPUTS.json').read_text())
    require(data['base']==BASE and len(data['inputs'])==8,'input domain/BASE')
    for row in data['inputs']:
        for path in [HERE/row['snapshot'], ROOT/row['path']]:
            raw=path.read_bytes()
            require((len(raw),sha256(raw).hexdigest())==(row['bytes'],row['sha256']),'immutable input drift: '+str(path))
    return {'frozen_direct_inputs':8,'immutable_drift':0}


def cells(cert):
    c=cert['complete_predecessor_certificate']
    for _ in range(3): c=c['complete_predecessor_certificate']
    return c,[r for r in c['candidates'] if r['classification']=='local_necessary_type']


def graph(contract, cell):
    colors=dict(contract['original_colors'],m=2,n=3,u=1,v=3,p_d=2,p_x=2,U=0)
    labels=dict(contract['original_component_labels'],m='M',n='N',u='N',v='N',p_d='K',p_x='K',U='K')
    adj={v:set() for v in colors}
    edges=cell['edges']+[['T','m'],['T','n'],['m','r'],['m','n'],['m','u'],['m','v'],['n','u'],['u','v'],['v','r'],['n','s'],['d','p_d'],['x','p_x']]
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    return colors,labels,adj


def reconstruct_stars(cert, seed=0):
    contract, actual = cells(cert)
    random.Random(seed).shuffle(actual)
    out = []
    for cell in actual:
        case = next(row for row in cert['six_point_cases'] if row['cell'] == cell['id'] and row['side'] == 'C' and row['u_color'] == 1 and row['v_color'] == 3)
        for ul in case['complete_u_links']:
            phi, labels, adj = graph(contract, cell)
            links = dict(m=['r','T','n','u','v'], T=['r','tau','s','n','m'], u=ul)
            for a,b in zip(ul, ul[1:] + ul[:1]):
                adj[a].add(b); adj[b].add(a)
            for w in ul:
                adj['u'].add(w); adj[w].add('u')
            sides = dict(r='C',d='C',e='C',s='E',x='E',h='E',m='C',u='C',U='C')
            gamma = set(contract['boundary'])
            pool = gamma | {'m','n','u','v','p_d','p_x','U'}

            def basic(a,b):
                if a == b or phi[a] == phi[b]: return False
                if {labels[a],labels[b]} == {'M','B'}: return False
                if {phi[a],phi[b]} <= {0,2} and labels[a] != labels[b]: return False
                if {phi[a],phi[b]} <= {1,3} and labels[a] != labels[b]: return False
                psi = {z: c ^ 2 if labels[z] == 'K' else c for z,c in phi.items()}
                if {psi[a],psi[b]} == {1,2} and a in sides and b in sides and sides[a] != sides[b]: return False
                if a in ('tau','zeta') or b in ('tau','zeta'): return b in adj[a]
                if a in gamma and b in gamma: return b in adj[a]
                for z,link in links.items():
                    if a == z and b not in link: return False
                    if b == z and a not in link: return False
                    if a in link and b in link and (link.index(a)-link.index(b)) % len(link) not in (1,len(link)-1): return False
                return True

            def valid(a):
                for z in a:
                    if any(not basic(z,w) for w in a[z]): return False
                for z,w in combinations(a,2):
                    common = a[z] & a[w]
                    if len(common)>2: return False
                return True

            def complete(center,arc,a):
                allowed = sorted(z for z in pool if basic(center,z))
                extras = sorted(set(allowed)-set(arc))
                result = []
                for k in range(max(0,5-len(arc)),len(extras)+1):
                    for chosen in combinations(extras,k):
                        if not a[center] <= set(arc)|set(chosen): continue
                        for seq in permutations(chosen):
                            link = list(arc)+list(seq)
                            edges = list(zip(link,link[1:]+link[:1]))+[(center,w) for w in link]
                            if any(not basic(z,w) for z,w in edges): continue
                            trial = {z:set(nbs) for z,nbs in a.items()}
                            for z,w in edges: trial[z].add(w);trial[w].add(z)
                            if not valid(trial): continue
                            # Complete links have no chords, all C3 are faces.
                            if any(w in trial[z] and (link.index(z)-link.index(w)) % len(link) not in (1,len(link)-1) for z,w in combinations(link,2)): continue
                            result.append((link,trial))
                return allowed,result

            allow_n, nlinks = complete('n',['s','T','m','u'],adj)
            joint=[]
            for nl,na in nlinks:
                links['n']=nl
                allow_v,vlinks=complete('v',['r','m','u'],na)
                for vl,va in vlinks:
                    links['v']=vl
                    def inner_arc(center,start,end):
                        la={w:set() for w in contract['original_colors'] if w != center}
                        for f in cell['faces']:
                            if center in f:
                                z,w=[z for z in f if z != center]
                                la[z].add(w);la[w].add(z)
                        arc=[start]
                        while arc[-1] != end:
                            arc.append(next(z for z in la[arc[-1]] if len(arc)<2 or z != arc[-2]))
                        return arc
                    ra=inner_arc('r','d','T')+['m','v']
                    _,rlinks=complete('r',ra,va)
                    sra=[]
                    for rl,rga in rlinks:
                        links['r']=rl
                        sa=inner_arc('s','T','x')
                        _,slinks=complete('s',sa,rga)
                        sra.extend(dict(r=rl,s=sl) for sl,_ in slinks)
                        del links['r']
                    joint.append(dict(n=nl,v=vl,rs=sra))
                    del links['v']
                del links['n']
            out.append(dict(cell=cell['id'], core=cell['core'], u=ul, allowed_n=allow_n, n_links=[x[0] for x in nlinks], joint=joint, valid_initial=valid(adj)))
    result=[]
    for case in out:
        for nv in case['joint']:
            for rs in nv['rs']:
                ul,nl,vl=case['u'],nv['n'],nv['v']
                if ul==['n','m','v','U','p_x']:
                    family='A-short-v' if len(vl)==5 else 'A-long-v'
                    un=['p_d','v','u','p_x']
                elif len(ul)==5:
                    family='B';un=['p_d','u','n','p_x']
                else:
                    family='C';un=['p_d','u','p_x']
                all_links=dict(u=ul,n=nl,v=vl,**rs)
                # Triangles through the already complete N stars independently
                # reconstruct each exit's N-side path, without a family formula.
                exit_arcs={}
                for center,start in [('p_d','d'),('p_x','x')]:
                    face_link={}
                    for z,link in all_links.items():
                        for i,w in enumerate(link):
                            if w != center:continue
                            for nb in [link[(i-1)%len(link)],link[(i+1)%len(link)]]:
                                face_link.setdefault(z,set()).add(nb)
                                face_link.setdefault(nb,set()).add(z)
                    arc=[start]
                    while arc[-1]!='U':
                        choices=face_link.get(arc[-1],set())-set(arc)
                        require(len(choices)==1,'exit N arc is not a single forced path')
                        arc.append(next(iter(choices)))
                    exit_arcs[center]=arc
                result.append(dict(cell=case['cell'],core=case['core'],family=family,
                    n_x_edge='x' in nl,full_links=all_links,exit_N_arcs=exit_arcs,U_N_arc=un))
    return sorted(result,key=lambda r:(r['cell'],r['full_links']['u'],r['full_links']['n'],r['full_links']['v']))


def reconstruct_B():
    result=[]
    for ev,hc in [(False,False),(False,True),(True,False)]:
        e='V' if ev else 'e';h='c' if hc else 'h'
        vertices=sorted({'V','Y','q','c','W',e,h})
        colors={v:3 if v in ['W','q'] else 1 for v in vertices}
        mandatory={tuple(sorted(p)) for p in [('W','V'),('W',e),('W',h),('q','Y'),('q','c')]}
        possible={tuple(sorted((a,b))) for a,b in combinations(vertices,2)
                  if colors[a]!=colors[b] and {a,b} not in [{'V','q'},{'Y','W'}]}
        optional=sorted(possible-mandatory)
        for bits in range(1<<len(optional)):
            edges=mandatory|{p for i,p in enumerate(optional) if bits&(1<<i)}
            adj={v:set() for v in vertices}
            for a,b in edges:adj[a].add(b);adj[b].add(a)
            seen={'V'};todo=['V']
            while todo:
                v=todo.pop()
                for w in adj[v]-seen:seen.add(w);todo.append(w)
            if len(seen)!=len(vertices):continue
            # The original C4 has no bounded-side points; both same-color
            # diagonals cannot be absent in a triangulation.
            if any(colors[a]==colors[b] and len(adj[a]&adj[b])>=2 for a,b in combinations(vertices,2)):continue
            common=adj['W']&adj['q'];require(len(common)==1,'unique B bridge')
            bridge=next(iter(common))
            # Breadth-first reconstruct the actual unique V-to-Y tree path.
            paths=[['V']]
            while paths and paths[0][-1]!='Y':
                path=paths.pop(0)
                paths.extend(path+[w] for w in sorted(adj[path[-1]]) if w not in path)
            require(paths,'B path missing')
            result.append(dict(e_equals_V=ev,h_equals_c=hc,bridge=bridge,
                vertices=vertices,edges=sorted([list(p) for p in edges]),shortest_V_Y_path=paths[0]))
    return sorted(result,key=lambda r:(r['e_equals_V'],r['h_equals_c'],r['bridge']))


def validate(certificate, seed=0):
    prior=json.loads((HERE/'frozen'/PREV).read_text())
    require(certificate['schema']=='941-gamma8-u-link-v1' and certificate['base']==BASE,'schema/BASE')
    require(certificate['complete_predecessor_certificate']==prior,'predecessor fibres/full lifts drift')
    rows=reconstruct_stars(prior,seed)
    require(certificate['star_restrictions']==rows,'complete-star domain or value drift')
    bs=reconstruct_B()
    require(sorted(certificate['B_models'],key=lambda r:(r['e_equals_V'],r['h_equals_c'],r['bridge']))==bs,'complete B tree domain drift')
    require(certificate['U_F_link_contract']==dict(endpoints=['V','Y'],
        permitted_V_arms=[['V'],['V','W'],['V','W','e']],Y_arm=['Y'],
        exit_orders=[['p_d','p_x'],['p_x','p_d']],e_V_alias_drops_third_arm=True,
        exit_other_arcs_are_paths_in_same_B_model=True,exit_original_degrees_at_least_five=True,
        unknown_B_paths_not_claimed_feasible=True),'ordered U link contract drift')
    require(certificate['paper_contract']==dict(same_original_graph_and_literal_frame=True,j=2,
        M2_nonempty=True,exterior_private_count=6,M_equals=['T','m'],m_side='C',d_not_U=True,
        W_not_q=True,e_not_Y=True,complete_original_B_has_only_W_q_color3=True,
        E_may_be_rootless=True,full_fibres_and_lifts_preserved=True),'paper premise drift')
    require(certificate['authority_boundaries']==dict(finite_control='triggered and holds',
        source_realizability='not triggered',eleven_type_exclusions=0,full_exterior_disk='OPEN',
        general_wrong_side='OPEN',common_k_lower_bound=23,new_Lean=False,new_LP=False,smaller_bad=False),'unsupported authority promotion')
    require(len(rows)==60 and len(bs)==6,'bounded-domain coverage')
    return dict(complete_star_restrictions=60,B_models=6,
        per_core={c:sum(r['core']==c for r in rows) for c in ['L','R','O']},
        source_realizability='not triggered',eleven_type_exclusions=0)


def negatives(cert):
    controls=[('missing_star',lambda c:c['star_restrictions'].pop()),
        ('false_nx_L',lambda c:c['star_restrictions'][0].update(n_x_edge=True)),
        ('lost_full_n',lambda c:c['star_restrictions'][0]['full_links']['n'].pop()),
        ('bad_exit_arc',lambda c:c['star_restrictions'][0]['exit_N_arcs']['p_x'].pop()),
        ('bad_U_arc',lambda c:c['star_restrictions'][0]['U_N_arc'].pop()),
        ('missing_B',lambda c:c['B_models'].pop()),
        ('false_B_edge',lambda c:c['B_models'][0]['edges'].append(['V','q'])),
        ('wrong_B_bridge',lambda c:c['B_models'][0].update(bridge='V')),
        ('allow_W_q',lambda c:c['paper_contract'].update(W_not_q=False)),
        ('allow_e_Y',lambda c:c['paper_contract'].update(e_not_Y=False)),
        ('root_E',lambda c:c['paper_contract'].update(E_may_be_rootless=False)),
        ('claim_source',lambda c:c['authority_boundaries'].update(source_realizability='triggered and holds')),
        ('claim_type_exclusion',lambda c:c['authority_boundaries'].update(eleven_type_exclusions=1)),
        ('wrong_U_order',lambda c:c['U_F_link_contract']['endpoints'].reverse())]
    rejected=[]
    for name,mutate in controls:
        bad=deepcopy(cert);mutate(bad)
        try:validate(bad)
        except (ValueError,KeyError,TypeError):rejected.append(name)
        else:raise ValueError('negative accepted: '+name)
    return {'negative_controls_rejected':rejected,'count':len(rejected)}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--negative',action='store_true');parser.add_argument('--certificate',type=Path,default=HERE/'certificate.json')
    args=parser.parse_args();cert=json.loads(args.certificate.read_text())
    result={'custody':custody(),'validation':validate(cert,args.seed)}
    if args.negative:result['negative']=negatives(cert)
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':main()
