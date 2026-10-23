#!/usr/bin/env python3
"""Read-only reconstruction of bounded whole-star joins and complete K6 fibres."""
import argparse
from copy import deepcopy
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path
import random
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BASE='6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'
SIX='audits/2026-10-23-941-gamma8-six-equality-6b09cd4/certificate.json'
CELLS='audits/2026-10-23-941-gamma8-cells-6b09cd4/certificate.json'
INNER=['r','T','s','tau','a','y','b']
KB=['d','p_d','U','p_x','x','zeta']


def require(ok,why):
    if not ok: raise ValueError(why)


def edge(a,b): return tuple(sorted((a,b)))


def custody():
    m=json.loads((HERE/'INPUTS.json').read_text())
    require(m['base']==BASE and m['schema']=='941-gamma8-empty-m2-inputs-v1','input contract drift')
    for row in m['inputs']+m['routing_entry']:
        raw=(HERE/row['snapshot']).read_bytes()
        require((len(raw),sha256(raw).hexdigest())==(row['bytes'],row['sha256']),'snapshot drift '+row['path'])
    for row in m['inputs']:
        raw=(ROOT/row['path']).read_bytes()
        require((len(raw),sha256(raw).hexdigest())==(row['bytes'],row['sha256']),'live authority drift '+row['path'])
    return dict(direct_inputs=len(m['inputs']),routing_snapshots=len(m['routing_entry']),immutable_drift=0)


def original(cell,contract,ylink):
    colors=dict(contract['original_colors'],a=3,y=1,b=3,p_d=2,p_x=2,U=0)
    labels=dict(contract['original_component_labels'],a='N',y='N',b='N',p_d='K',p_x='K',U='K')
    es={edge(*e) for e in cell['edges']}
    es|={edge(*e) for e in [('T','a'),('T','y'),('T','b'),('r','a'),('a','y'),('y','b'),('b','s'),('d','p_d'),('x','p_x')]}
    es|={edge('y',v) for v in ylink}
    es|={edge(a,b) for a,b in zip(ylink,ylink[1:]+ylink[:1])}
    complete=dict(T=['r','tau','s','b','y','a'],y=ylink)
    for v in ('tau','zeta'):
        complete[v]=[b if a==v else a for a,b in cell['edges'] if v in (a,b)]
    return colors,labels,es,complete


def valid(es,colors,labels,cell,complete):
    adj={v:set() for v in colors}
    old={edge(*e) for e in cell['edges']}
    gamma=set(['r','T','s','x','h','W','e','d'])
    oldpoints=gamma|{'tau','zeta'}
    side=dict(r='C',d='C',e='C',s='E',x='E',h='E',y='C',U='C')
    psi={v:(c^2 if labels[v]=='K' else c) for v,c in colors.items()}
    for a,b in es:
        if a==b or colors[a]==colors[b]: return False
        if a in oldpoints and b in oldpoints and edge(a,b) not in old:return False
        if {a,b}&{'tau','zeta'} and not {a,b}<=oldpoints:return False
        if {colors[a],colors[b]}<={0,2} and labels[a]!=labels[b]:return False
        if {colors[a],colors[b]}<={1,3} and labels[a]!=labels[b]:return False
        if {labels[a],labels[b]}=={'M','B'}:return False
        if {psi[a],psi[b]}=={1,2} and a in side and b in side and side[a]!=side[b]:return False
        adj[a].add(b);adj[b].add(a)
    for v,link in complete.items():
        if adj[v]!=set(link):return False
        if v in ('tau','zeta'):continue
        if any(edge(a,b) not in es for a,b in zip(link,link[1:]+link[:1])):return False
        for i,a in enumerate(link):
            for j,b in enumerate(link):
                if i<j and (j-i) not in (1,len(link)-1) and edge(a,b) in es:return False
    for a,b in combinations(colors,2):
        if colors[a]==colors[b] and len(adj[a]&adj[b])>2:return False
    forbidden=[('r','s'),('d','x')]+([('T','x')] if cell['core'] in ('L','O') else [])+([('T','d')] if cell['core'] in ('R','O') else [])
    exterior={'a','y','b','p_d','p_x','U'}
    if any(adj[a]&adj[b]&exterior for a,b in forbidden):return False
    return True


def choices(start,colors):
    # Exhaust all complete cyclic links anchored by the actual start-T-y faces.
    pool=['d','x','U','p_d','p_x']
    for size in range(2,6):
        for chosen in combinations(pool,size):
            for p in permutations(chosen):
                link=[start,'T','y',*p]
                if all(colors[a]!=colors[b] for a,b in zip(link,link[1:]+link[:1])):
                    yield link


def add_star(es,center,link):
    return es|{edge(center,v) for v in link}|{edge(a,b) for a,b in zip(link,link[1:]+link[:1])}


def join_links(cell,contract,ylink):
    colors,labels,es,complete=original(cell,contract,ylink)
    rows=[]
    if not valid(es,colors,labels,cell,complete):return rows
    for alink in choices('r',colors):
        ea=add_star(es,'a',alink);ca=dict(complete,a=alink)
        if not valid(ea,colors,labels,cell,ca):continue
        for blink in choices('s',colors):
            eb=add_star(ea,'b',blink);cb=dict(ca,b=blink)
            if valid(eb,colors,labels,cell,cb):
                rows.append(dict(a=alink,b=blink))
    return sorted(rows,key=lambda r:(r['a'],r['b']))


def neighbour_cycle(center,es,first):
    neigh={b if a==center else a for a,b in es if center in (a,b)}
    la={v:{w for w in neigh if edge(v,w) in es} for v in neigh}
    require(all(len(n)==2 for n in la.values()),'complete link not forced')
    out=list(first)
    require(out[1] in la[out[0]],'bad cycle anchor')
    while len(out)<len(neigh):
        nxt=la[out[-1]]-{out[-2]}
        require(len(nxt)==1,'cycle ambiguity')
        out.append(next(iter(nxt)))
    require(out[0] in la[out[-1]] and len(set(out))==len(neigh),'not a cycle')
    return out


def direct_fibres(es):
    selected=set(INNER+KB)
    patch=[e for e in es if set(e)<=selected]
    require(len(patch)==30,'K6 disk edge count')
    rows=[]
    for word in ([0,2,0,2,0,2],[2,0,2,0,2,0]):
        fixed=dict(zip(KB,word));mask=[];lifts=[]
        for assignment in product(range(4),repeat=7):
            colors=dict(fixed,**dict(zip(INNER,assignment)))
            ok=all(colors[a]!=colors[b] for a,b in patch)
            mask.append('1' if ok else '0')
            if ok:lifts.append(list(assignment))
        rows.append(dict(ordered_boundary=KB,literal_boundary_word=word,ordered_inner=INNER,
            complete_assignment_mask=''.join(mask),full_lifts=lifts,empty_assignments=mask.count('0')))
    return rows


def reconstruct():
    prior=json.loads((HERE/'frozen'/SIX).read_text())
    contract=json.loads((HERE/'frozen'/CELLS).read_text())
    cases=[];survivors=[];b_rows=[]
    for cell in contract['candidates']:
        if cell['classification']!='local_necessary_type':continue
        previous=next(r for r in prior['empty_M2_five_point_cases'] if r['cell']==cell['id'] and not r['U_equals_d'])
        for ylink in previous['complete_y_links']:
            joins=join_links(cell,contract,ylink)
            if cell['core']=='O':require(not joins,'O complete-star contradiction lost')
            cases.append(dict(cell=cell['id'],core=cell['core'],complete_y_link=ylink,
                complete_a_b_links=joins,classification='necessary_joint_star_row' if joins else
                    ('O_previously_excluded' if cell['core']=='O' else 'excluded_complete_star_join')))
            if not joins:continue
            require(len(joins)==1,'multiple a/b completions')
            colors,labels,es,complete=original(cell,contract,ylink)
            for center in ('a','b'):
                complete[center]=joins[0][center];es=add_star(es,center,complete[center])
            # The two original boundary-side faces seal r and s; the link cycle
            # is read from those actual edges, without imposing degree five.
            complete['r']=neighbour_cycle('r',es,['d','zeta'] if cell['core']=='L' else ['T','tau'])
            complete['s']=neighbour_cycle('s',es,['T','tau'] if cell['core']=='L' else ['x','zeta'])
            stars={v:complete[v] for v in ('T','a','b','y','r','s')}
            arc=['p_d','y','b','p_x'] if cell['core']=='L' else ['p_d','a','y','p_x']
            require(all(edge(a,b) in es for a,b in zip(arc,arc[1:])),'U F-side arc not forced')
            require(all(edge('U',v) in es for v in arc),'U F-side neighbour lost')
            kpoints=sorted(v for v in colors if labels[v]=='K')
            require(kpoints==sorted(KB),'complete original K point set')
            require({e for e in es if set(e)<=set(KB)}=={edge(a,b) for a,b in zip(KB,KB[1:]+KB[:1])},'complete K cycle')
            survivors.append(dict(cell=cell['id'],core=cell['core'],complete_stars=stars,
                complete_original_M=['T'],complete_original_N=sorted(v for v in colors if labels[v]=='N'),
                complete_original_K_cycle=KB,required_U_F_link_arc=arc,
                U_arc_allows_reversal=True,U_F_link_is_not_cyclic=True,literal_K6_fibres=direct_fibres(es)))
            for e_identity in ('private','V'):
                # Independently exhaust all ways of joining the complete B13
                # graph with its two original colour-3 vertices W and q.
                ones=sorted({'V','Y','c','h', 'e' if e_identity=='private' else 'V'})
                forced={edge('q','Y'),edge('q','c'),edge('W','h'),edge('W','e' if e_identity=='private' else 'V'),edge('W','V')}
                optional=[edge('q','h'),edge('W','c')]+([edge('q','e')] if e_identity=='private' else [])
                for bits in product((0,1),repeat=len(optional)):
                    be=forced|{e for e,on in zip(optional,bits) if on}
                    common=[v for v in ones if edge('W',v) in be and edge('q',v) in be]
                    if len(common)!=1:continue
                    connector=common[0]
                    b_rows.append(dict(cell=cell['id'],e_identity=e_identity,unique_W_q_connector=connector,
                        shortest_original_B13_V_Y_path=['V','W',connector,'q','Y'],classification='necessary_B13_tree_row'))
    return prior,cases,survivors,b_rows


def validate(c,seed=0):
    require(c['schema']=='941-gamma8-empty-m2-v1' and c['base']==BASE,'certificate contract drift')
    prior,cases,survivors,b_rows=reconstruct()
    require(c['complete_predecessor_certificate']==prior,'complete predecessor fibres/empty rows/full lifts changed')
    for key,expected in [('joint_link_cases',cases),('complete_star_survivors',survivors),('necessary_B13_tree_rows',b_rows)]:
        actual=c[key];require(len(actual)==len(expected),key+' coverage drift')
        canonical=lambda rows:sorted(json.dumps(r,sort_keys=True) for r in rows)
        order=list(expected);random.Random(seed).shuffle(order)
        require(canonical(actual)==canonical(order),key+' reconstruction disagreement')
    require(c['paper_contract']==dict(j=2,full_M2_empty=True,original_T_degree=6,
        exterior_private_points=5,same_original_graph_and_literal_frame=True,E_may_be_rootless=True,
        full_stars_and_rotation_retained=True,U_is_only_rootless_star_frame_exception=True,
        d_not_U=True,h_not_c=True,W_not_q=True,original_V_W_edge=True,e_not_Y=True,E_rootless=True,
        exact_B13_connector=True,no_complete_U_cyclic_star_assumption=True),'paper contract drift')
    require(c['authority_boundaries']==dict(finite_control='triggered and holds',source_realizability='not triggered',
        conditional_L_R_complete_star_rows=8,eleven_type_exclusions=0,remaining_exterior_completion='OPEN',
        general_wrong_side='OPEN',common_k_lower_bound=23,new_Lean=False,new_LP=False,smaller_bad=False),'unsupported promotion')
    caps=json.loads((HERE/'K6_CAPS.json').read_text())
    require(caps['schema']=='941-gamma8-empty-m2-K6-caps-v1' and caps['base']==BASE,'cap export contract')
    require(len(caps['caps'])==2,'cap export coverage')
    contract=json.loads((HERE/'frozen'/CELLS).read_text())
    for core,cap in zip(('L','R'),caps['caps']):
        row=next(r for r in survivors if r['core']==core)
        cell=next(r for r in contract['candidates'] if r['id']==row['cell'])
        colors,labels,es,complete=original(cell,contract,row['complete_stars']['y'])
        for v in ('a','b'):es=add_star(es,v,row['complete_stars'][v])
        selected=set(INNER+KB);pe={e for e in es if set(e)<=selected}
        require(cap['core']==core and cap['ordered_boundary']==KB and cap['ordered_inner']==INNER,'cap ordered frame')
        require(cap['vertices']==sorted(selected) and cap['edges']==[list(e) for e in sorted(pe)],'cap actual edges')
        require(cap['original_colors']=={v:colors[v] for v in selected},'cap original literal colors')
        require(cap['exchanged_K_colors']=={v:colors[v]^2 if v in KB else colors[v] for v in selected},'cap exchanged literal colors')
        require(cap['status']=='necessary_source_cap_not_source_realization','cap source promotion')
        faces=cap['oriented_actual_faces'];require(len(faces)==18,'actual face coverage')
        require(len({tuple(sorted(f)) for f in faces})==18,'repeated actual face')
        directed={}
        for face in faces:
            require(len(face)==len(set(face))==3 and set(face)&set(INNER),'face misses private source-star center')
            for a,b in zip(face,face[1:]+face[:1]):
                require(edge(a,b) in pe,'non-original face edge')
                directed[a,b]=directed.get((a,b),0)+1
        require(all(v==1 for v in directed.values()),'repeated oriented face edge')
        residual={e for e in directed if e[::-1] not in directed}
        require(residual==set(zip(KB,KB[1:]+KB[:1])),'actual face cancellation is not ordered K6')
    return dict(joint_link_cases=len(cases),complete_star_rows=len(survivors),B13_tree_rows=len(b_rows),
        complete_literal_fibres=sum(len(r['literal_K6_fibres']) for r in survivors),
        full_lifts=sum(len(f['full_lifts']) for r in survivors for f in r['literal_K6_fibres']),
        empty_assignments=sum(f['empty_assignments'] for r in survivors for f in r['literal_K6_fibres']),
        source_realizability='not triggered',eleven_type_exclusions=0)


def negatives(c):
    tests=[('lose_joint_case',lambda x:x['joint_link_cases'].pop()),
        ('lose_star_row',lambda x:x['complete_star_survivors'].pop()),
        ('change_original_link',lambda x:x['complete_star_survivors'][0]['complete_stars']['a'].reverse()),
        ('erase_U_F_arc',lambda x:x['complete_star_survivors'][0]['required_U_F_link_arc'].pop()),
        ('drop_full_lift',lambda x:x['complete_star_survivors'][0]['literal_K6_fibres'][0]['full_lifts'].pop()),
        ('drop_empty_assignment',lambda x:x['complete_star_survivors'][0]['literal_K6_fibres'][0].update(complete_assignment_mask='1'*4**7)),
        ('wrong_literal_frame',lambda x:x['complete_star_survivors'][0]['literal_K6_fibres'][0]['literal_boundary_word'].__setitem__(0,2)),
        ('drop_B13_exit',lambda x:x['necessary_B13_tree_rows'].pop()),
        ('presume_E_rooted',lambda x:x['paper_contract'].update(E_may_be_rootless=False)),
        ('cyclic_U_star',lambda x:x['paper_contract'].update(no_complete_U_cyclic_star_assumption=False)),
        ('invent_source',lambda x:x['authority_boundaries'].update(source_realizability='triggered and holds')),
        ('exclude_eleven_type',lambda x:x['authority_boundaries'].update(eleven_type_exclusions=1)),
        ('raise_k',lambda x:x['authority_boundaries'].update(common_k_lower_bound=24)),
        ('lose_prior_fibre',lambda x:x['complete_predecessor_certificate']['empty_M2_five_point_cases'].pop())]
    out=[]
    for name,mutate in tests:
        bad=deepcopy(c);mutate(bad)
        try:validate(bad)
        except (ValueError,KeyError,IndexError,TypeError):out.append(dict(name=name,status='rejected'))
        else:raise ValueError('accepted negative '+name)
    return out


def main():
    p=argparse.ArgumentParser();p.add_argument('--certificate',type=Path,default=HERE/'certificate.json')
    p.add_argument('--seed',type=int,default=0);p.add_argument('--negative',action='store_true');a=p.parse_args()
    auth=custody();c=json.loads(a.certificate.read_text());result=dict(status='PASS',seed=a.seed,custody=auth,**validate(c,a.seed))
    if a.negative:result['semantic_negatives']=negatives(c)
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,IndexError,TypeError,OSError,json.JSONDecodeError) as exc:
        print(json.dumps(dict(status='REJECT',reason=str(exc))));sys.exit(1)
