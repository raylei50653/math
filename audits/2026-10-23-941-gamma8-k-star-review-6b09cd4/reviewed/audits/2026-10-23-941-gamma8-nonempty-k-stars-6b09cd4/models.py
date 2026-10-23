#!/usr/bin/env python3
"""Necessary same-graph N stars with one extra K point; no source claim."""
import json
from itertools import combinations, permutations
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
CELL='audits/2026-10-23-941-gamma8-cells-6b09cd4/certificate.json'
PREV='audits/2026-10-23-941-gamma8-nonempty-resource-stars-6b09cd4/certificate.json'

def reconstruct():
    contract=json.loads((HERE/'frozen'/CELL).read_text())
    prior=json.loads((HERE/'frozen'/PREV).read_text())
    out=[]
    for cell in contract['candidates']:
        if cell['classification']!='local_necessary_type':continue
        for kind in ['K0','K2']:
            for a,b,side,dU in [(a,b,side,dU) for a,b,side in [('r','s','C'),('s','r','E')] for dU in ([False,True] if kind=='K0' else [False])]:
                for ul in next(r for r in prior['u_full_link_trials'] if r['omega_type']==kind)['all_proper_complete_u_links']:
                    ul=['d' if dU and w=='U' else w for w in ul]
                    phi=dict(contract['original_colors'],m=2,n=3,u=1,v=3,p_d=2,p_x=2,U=0,omega=int(kind[1]))
                    labels=dict(contract['original_component_labels'],m='M',n='N',u='N',v='N',p_d='K',p_x='K',U='K',omega='K')
                    if dU:del phi['U'];del labels['U']
                    adj={v:set() for v in phi}
                    links=dict(m=[a,'T','n','u','v'],T=[a,'tau',b,'n','m'],u=ul)
                    edges=cell['edges']+[['d','p_d'],['x','p_x']]
                    for center,link in links.items():
                        edges += [[center,w] for w in link]+[[w,link[(i+1)%len(link)]] for i,w in enumerate(link)]
                    for z,w in edges:adj[z].add(w);adj[w].add(z)
                    sides=dict(r='C',d='C',e='C',s='E',x='E',h='E',m=side,u=side,U='C')
                    gamma=set(contract['boundary'])
                    pool=gamma|{'m','n','u','v','p_d','p_x','U','omega'}
                    if dU:pool.remove('U')
                    def basic(z,w):
                        if z==w or phi[z]==phi[w]:return False
                        if {labels[z],labels[w]}=={'M','B'}:return False
                        if {phi[z],phi[w]}<={0,2} and labels[z]!=labels[w]:return False
                        if {phi[z],phi[w]}<={1,3} and labels[z]!=labels[w]:return False
                        psi={t:c^2 if labels[t]=='K' else c for t,c in phi.items()}
                        if {psi[z],psi[w]}=={1,2} and z in sides and w in sides and sides[z]!=sides[w]:return False
                        if z in ('tau','zeta') or w in ('tau','zeta'):return w in adj[z]
                        if z in gamma and w in gamma:return w in adj[z]
                        for center,link in links.items():
                            if z==center and w not in link:return False
                            if w==center and z not in link:return False
                            if z in link and w in link and (link.index(z)-link.index(w))%len(link) not in (1,len(link)-1):return False
                        return True
                    def valid(graph):
                        if any(not basic(z,w) for z in graph for w in graph[z]):return False
                        return all(len(graph[z]&graph[w])<=2 for z,w in combinations(graph,2))
                    def complete(center,arc,graph):
                        allowed=sorted(z for z in pool if basic(center,z))
                        extras=sorted(set(allowed)-set(arc))
                        result=[]
                        for k in range(max(0,5-len(arc)),len(extras)+1):
                            for chosen in combinations(extras,k):
                                if not graph[center]<=set(arc)|set(chosen):continue
                                for seq in permutations(chosen):
                                    link=list(arc)+list(seq)
                                    es=list(zip(link,link[1:]+link[:1]))+[(center,w) for w in link]
                                    if any(not basic(z,w) for z,w in es):continue
                                    trial={z:set(nbs) for z,nbs in graph.items()}
                                    for z,w in es:trial[z].add(w);trial[w].add(z)
                                    if not valid(trial):continue
                                    if any(w in trial[z] and (link.index(z)-link.index(w))%len(link) not in (1,len(link)-1) for z,w in combinations(link,2)):continue
                                    result.append((link,trial))
                        return result
                    def inner_arc(center,start,end):
                        la={w:set() for w in contract['original_colors'] if w!=center}
                        for f in cell['faces']:
                            if center in f:
                                z,w=[z for z in f if z!=center];la[z].add(w);la[w].add(z)
                        arc=[start]
                        while arc[-1]!=end:arc.append(next(z for z in la[arc[-1]] if len(arc)<2 or z!=arc[-2]))
                        return arc
                    if not valid(adj):continue
                    for nl,na in complete('n',[b,'T','m','u'],adj):
                        links['n']=nl
                        for vl,va in complete('v',[a,'m','u'],na):
                            links['v']=vl
                            arc=inner_arc(a,'d' if a=='r' else 'x','T')+['m','v']
                            for al,aa in complete(a,arc,va):
                                links[a]=al
                                barc=inner_arc(b,'T','x' if b=='s' else 'd')
                                for bl,ba in complete(b,barc,aa):
                                    all_links=dict(links,**{b:bl})
                                    out.append(dict(cell=cell['id'],core=cell['core'],omega_type=kind,m_side=side,anchor=a,d_equals_U=dU,
                                        full_links={z:all_links[z] for z in ['T','m','u','n','v','r','s']},
                                        edges=[list(e) for e in sorted({tuple(sorted((z,w))) for z in ba for w in ba[z]})]))
                                del links[a]
                            del links['v']
                        del links['n']
    return out

def refinements(rows):
    """Source restrictions deliberately omitted from the relaxed enumerator."""
    rejected=[]
    for i,row in enumerate(rows):
        adj={x:set() for e in row['edges'] for x in e}
        adj.setdefault('omega',set())
        for z,w in row['edges']:adj[z].add(w);adj[w].add(z)
        sides={z:'C' for z in ['r','d','e','U']}
        sides.update({z:'E' for z in ['s','x','h']})
        sides.update(m=row['m_side'],u=row['m_side'])
        if row['omega_type']=='K0' and len({sides[z] for z in adj['omega']&sides.keys()})>1:
            rejected.append(dict(row=i,reason='omega-known-C-E-12-path'))
        elif 'x' in adj['p_d'] or 'd' in adj['p_x']:
            rejected.append(dict(row=i,reason='K02-bichromatic-original-C4'))
    return rejected

def k_interfaces(rows,rejected):
    """Complete K-star domains, with arbitrary outside 13 tails preserved."""
    bad={r['row'] for r in rejected}
    result=[]
    for i,row in enumerate(rows):
        if i in bad:continue
        kind=row['omega_type'];dU=row['d_equals_U']
        active_U='d' if dU else 'U'
        known={x:set() for e in row['edges'] for x in e}
        known.setdefault('omega',set())
        for z,w in row['edges']:known[z].add(w);known[w].add(z)
        faces=set()
        for center,link in row['full_links'].items():
            for j,z in enumerate(link):faces.add(tuple(sorted([center,z,link[(j+1)%len(link)]])))
        # Only complete rootless stars contribute forced outside faces here;
        # no F-link of U is promoted to a cyclic original G-link.
        star_rows=[]
        for center in ['p_d','p_x','omega']:
            adj={}
            for face in faces:
                if center not in face:continue
                z,w=[x for x in face if x!=center]
                adj.setdefault(z,set()).add(w);adj.setdefault(w,set()).add(z)
            star_rows.append(dict(center=center,mandatory_neighbors=sorted(known[center]),
                forced_face_link_edges=[list(e) for e in sorted({tuple(sorted((z,w))) for z in adj for w in adj[z]})],
                original_degree_at_least=5,
                other_original_neighbors_may_include_Z_external_13=True,
                whole_original_star_completed=False))
        result.append(dict(row=i,omega_type=kind,d_equals_U=dU,
            K0_domain=(['d','x'] if dU else ['d','x','U'])+(['omega'] if kind=='K0' else []),
            K2_external_domain=['p_d','p_x']+(['omega'] if kind=='K2' else []),
            K_connected_requirements=(
                [dict(center='omega',at_least_one_original_neighbor=['p_d','p_x'])]
                +([] if dU else [dict(center='U',at_least_one_original_neighbor=['p_d','p_x'])])
                if kind=='K0' else
                [dict(center='omega',at_least_one_original_neighbor=['d','x','U']),
                 dict(center='U',at_least_one_original_neighbor=['p_d','p_x','omega'])]),
            U_original2_neighbor_envelope_in_F=['p_d','p_x']+(['omega'] if kind=='K2' else [])+(['zeta'] if dU else []),
            U_F_link_endpoints=['V','Y'],
            U_original_full_cyclic_link_not_claimed=True,
            exit_and_omega_partial_stars=star_rows))
    return result
