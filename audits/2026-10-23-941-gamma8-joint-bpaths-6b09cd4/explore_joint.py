#!/usr/bin/env python3
"""Joint finite B-path gluing in one literal cap/B/U graph; exploratory."""
from collections import Counter
from itertools import combinations,product
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
PREV='audits/2026-10-23-941-gamma8-u-link-6b09cd4/certificate.json'


def edge(a,b):return tuple(sorted((a,b)))


def path_in_tree(adj,a,b):
    todo=[(a,[a])]
    while todo:
        v,path=todo.pop()
        if v==b:return path
        todo.extend((w,path+[w]) for w in adj[v] if w not in path)
    raise ValueError('tree disconnected')


def faces_of_cycle(z,link):
    return {tuple(sorted((z,a,b))) for a,b in zip(link,link[1:]+link[:1])}


def orientation(faces):
    incid={}
    for i,f in enumerate(faces):
        for a,b in zip(f,f[1:]+f[:1]):incid.setdefault(edge(a,b),[]).append((i,1 if a<b else -1))
    if any(len(v)>2 for v in incid.values()):return False
    adj={i:[] for i in range(len(faces))}
    for pair in incid.values():
        if len(pair)==2:
            (i,s),(j,t)=pair;adj[i].append((j,-s*t));adj[j].append((i,-s*t))
    signs={}
    for i in adj:
        if i in signs:continue
        signs[i]=1;todo=[i]
        while todo:
            k=todo.pop()
            for j,r in adj[k]:
                s=signs[k]*r
                if j in signs and signs[j]!=s:return False
                if j not in signs:signs[j]=s;todo.append(j)
    return True


def main():
    prior=json.loads((HERE/'frozen'/PREV).read_text())
    c=prior['complete_predecessor_certificate']['complete_predecessor_certificate']
    for _ in range(3):c=c['complete_predecessor_certificate']
    cells={r['id']:r for r in c['candidates']}
    stats=Counter();survivors=[]
    for ri,row in enumerate(prior['star_restrictions']):
        cell=cells[row['cell']]
        for bi,b in enumerate(prior['B_models']):
            mp={z:z for z in c['original_colors']}
            if b['e_equals_V']:mp['e']='V'
            if b['h_equals_c']:mp['h']='c'
            def mapped(es):return {edge(mp.get(a,a),mp.get(d,d)) for a,d in es}
            co={mp[z]:v for z,v in c['original_colors'].items()}
            co.update(m=2,n=3,u=1,v=3,p_d=2,p_x=2,U=0,V=1,Y=1,q=3,c=1)
            labels={mp[z]:v for z,v in c['original_component_labels'].items()}
            labels.update(m='M',n='N',u='N',v='N',p_d='K',p_x='K',U='K',V='B',Y='B',q='B',c='B')
            bad_alias=len(co)!=len(set(co))
            gamma=set(mp[z] for z in c['boundary'])
            induced=set(mp[z] for z in c['original_colors'])
            original=mapped(cell['edges'])
            links={z:[mp.get(w,w) for w in l] for z,l in row['full_links'].items()}
            links.update(m=['r','T','n','u','v'],T=['r','tau','s','n','m'])
            la={w:set() for w in c['original_colors'] if w!='tau'}
            for f in cell['faces']:
                if 'tau' in f:
                    a,d=[z for z in f if z!='tau'];la[a].add(d);la[d].add(a)
            tl=['r'];prev=None
            while True:
                nxt=next(z for z in sorted(la[tl[-1]]) if z!=prev)
                if nxt==tl[0]:break
                prev=tl[-1];tl.append(nxt)
            links['tau']=tl
            base_faces={tuple(sorted(mp[z] for z in f)) for f in cell['faces']}
            for z,l in links.items():base_faces |= faces_of_cycle(z,l)
            base=original|{edge(a,d) for f in base_faces for a,d in combinations(f,2)}
            base|={tuple(e) for e in b['edges']}|{edge('U','V'),edge('U','Y'),edge('Y','q'),edge('q','c')}
            badj={z:set() for z in b['vertices']}
            for a,d in b['edges']:badj[a].add(d);badj[d].add(a)
            un=row['U_N_arc']
            for reverse,armtype in product([False,True],range(3 if not b['e_equals_V'] else 2)):
                arm=['V']+(['W'] if armtype else [])+(['e'] if armtype==2 else [])
                unarc=list(reversed(un)) if reverse else un
                ul=arm+unarc+['Y']
                anchors={unarc[0]:arm[-1],unarc[-1]:'Y'}
                Ufaces={tuple(sorted(['U',a,d])) for a,d in zip(ul,ul[1:])}
                ue={edge('U',z) for z in ul}|{edge(a,d) for a,d in zip(ul,ul[1:])}
                for bd,bx in product(b['vertices'],repeat=2):
                    stats['raw_joint_rows']+=1
                    paths=dict(p_d=path_in_tree(badj,anchors['p_d'],bd),p_x=path_in_tree(badj,anchors['p_x'],bx))
                    plinks={p:row['exit_N_arcs'][p]+paths[p] for p in ['p_d','p_x']}
                    if any(len(l)<5 for l in plinks.values()):stats['exit_degree']+=1;continue
                    full=dict(links,**plinks)
                    fs=base_faces|Ufaces
                    for z,l in plinks.items():fs |= faces_of_cycle(z,l)
                    es=base|ue|{edge(a,d) for f in fs for a,d in combinations(f,2)}
                    failure=None
                    # Complete d/x stars: only a path in the same exact B tree
                    # remains between the two ends of their known face-link.
                    for z in ['d','x']:
                        ladj={}
                        for f in fs:
                            if z in f:
                                a,d=[w for w in f if w!=z];ladj.setdefault(a,set()).add(d);ladj.setdefault(d,set()).add(a)
                        if any(len(v)>2 for v in ladj.values()):failure='d_x_link_branch';break
                        ends=[w for w in ladj if len(ladj[w])==1]
                        if ends:
                            if len(ends)!=2 or any(w not in badj for w in ends):failure='d_x_wrong_gap';break
                            bp=path_in_tree(badj,*ends)
                            if set(bp[1:-1])&set(ladj):failure='d_x_B_path_repeat';break
                            for a,d in zip(bp,bp[1:]):
                                fs.add(tuple(sorted([z,a,d])));es|={edge(z,a),edge(z,d),edge(a,d)}
                                ladj.setdefault(a,set()).add(d);ladj.setdefault(d,set()).add(a)
                        if any(len(v)!=2 for v in ladj.values()):failure='d_x_not_cycle';break
                        start=min(ladj);ll=[start];prev=None
                        while True:
                            nxt=next(w for w in sorted(ladj[ll[-1]]) if w!=prev)
                            if nxt==start:break
                            if nxt in ll:failure='d_x_disconnected';break
                            prev=ll[-1];ll.append(nxt)
                        if failure:break
                        if len(ll)!=len(ladj) or len(ll)<5:failure='d_x_degree';break
                        full[z]=ll
                    if failure:stats[failure]+=1;continue
                    adj={z:set() for z in co}
                    for a,d in es:adj[a].add(d);adj[d].add(a)
                    # All complete stars are simultaneous, including U's full F arc.
                    for z,l in full.items():
                        if adj[z]!=set(l):failure='full_star_conflict';break
                        if any(edge(a,d) in es and (l.index(a)-l.index(d))%len(l) not in [1,len(l)-1] for a,d in combinations(l,2)):failure='full_link_chord';break
                    if not failure and adj['U']!=set(ul):failure='U_extra_neighbor'
                    if not failure:
                        for a,d in es:
                            if co[a]==co[d]:failure='improper';break
                            if a in induced and d in induced and edge(a,d) not in original:failure='original_induced';break
                            if {co[a],co[d]}<={0,2} and labels[a]!=labels[d]:failure='original_02';break
                            if {co[a],co[d]}<={1,3} and labels[a]!=labels[d]:failure='original_13';break
                    if not failure and (adj['V']&adj['Y'])-{'U'}:failure='fixed_V_Y_common'
                    if not failure:
                        for a,d in combinations(adj,2):
                            common=adj[a]&adj[d]
                            if len(common)>2:failure='three_common';break
                            if edge(a,d) not in es and len(common)==2 and edge(*common) not in es:failure='chordless_C4';break
                    if not failure:
                        triangles={tuple(sorted([a,d,w])) for a,d in es for w in adj[a]&adj[d]}
                        if triangles-fs:failure='nonfacial_C3'
                    if not failure and not orientation(sorted(fs)):failure='orientation'
                    if failure:stats[failure]+=1;continue
                    stats['survivors']+=1
                    survivors.append(dict(star_row=ri,B_model=bi,reverse=reverse,V_arm=arm,
                        B_paths=paths,full_links=full,U_F_link=ul,edges=[list(e) for e in sorted(es)],faces=[list(f) for f in sorted(fs)]))
    result=dict(statistics=dict(stats),survivors=survivors)
    (HERE/'JOINT_EXPLORATION.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(dict(stats),sort_keys=True))
    print(repr(Counter((r['B_model'],tuple(r['V_arm'])) for r in survivors)))


if __name__=='__main__':main()
