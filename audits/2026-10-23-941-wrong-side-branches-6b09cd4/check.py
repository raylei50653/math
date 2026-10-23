#!/usr/bin/env python3
"""Independent bounded component and full-link identities; paper handles all sources."""
import argparse
from collections import defaultdict
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import random
import sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BASE='6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'

def need(ok,why):
    if not ok:raise ValueError(why)

def custody():
    m=json.loads((HERE/'INPUTS.json').read_text());need(m['base']==BASE,'BASE drift')
    for r in m['inputs']:
        b=(HERE/r['snapshot']).read_bytes();need((len(b),sha256(b).hexdigest())==(r['bytes'],r['sha256']),'frozen drift')
        need((ROOT/r['path']).read_bytes()==b,'live authority drift: '+r['path'])
    for r in m['routing_entry']:
        b=(HERE/r['snapshot']).read_bytes();need((len(b),sha256(b).hexdigest())==(r['bytes'],r['sha256']),'routing snapshot drift')
    need(m['verified_prior_final_entries']==91 and m['verified_inherited_live_authority']==54,'previous final audit count changed')
    return len(m['inputs'])

def graph(colors,edges):
    adj={v:set() for v in colors};seen=set()
    for a,b in edges:
        need(a in adj and b in adj and a!=b and colors[a]!=colors[b],'bad literal original edge')
        e=frozenset((a,b));need(e not in seen,'duplicate edge');seen.add(e)
        adj[a].add(b);adj[b].add(a)
    return adj

def component(adj,start,removed):
    seen={start};todo=[start]
    while todo:
        v=todo.pop()
        for w in adj[v]-seen-{removed}:seen.add(w);todo.append(w)
    return seen

def path_check(path,adj):
    need(len(path)==len(set(path)) and all(b in adj[a] for a,b in zip(path,path[1:])),'not a same-graph simple path')

def dynamic_minimum(kind,n,m,alphabet):
    # DP enumerates all proper path/cycle color words anchored at color1,
    # recording actual color1 count and actual non1/non1 edge count.
    states={(1,1,0):1}
    for degree in range(1,12):
        found=0
        for (last,ones,non1),count in states.items():
            closed=(last!=1) if kind=='cyclic' else last==1
            if degree>1 and closed and ones>=n and non1>=m:found+=count
        if found:return degree,found
        nxt=defaultdict(int)
        for (last,ones,non1),count in states.items():
            for col in alphabet:
                if col!=last:nxt[col,ones+(col==1),non1+(last!=1 and col!=1)]+=count
        states=nxt
    raise ValueError('DP length exceeded')

def links(rows,seed):
    required={(kind,n,m) for kind,n in [('cyclic',3),('path',3),('path',4),('path',5)] for m in range(3)}
    got={(r['kind'],r['minimum_color1_neighbors'],r['required_distinct_non1_edges']) for r in rows}
    need(len(rows)==12 and got==required,'link control coverage incomplete')
    shuffled=list(rows);random.Random(seed).shuffle(shuffled);stats=[]
    for r in shuffled:
        kind,n,m=r['kind'],r['minimum_color1_neighbors'],r['required_distinct_non1_edges']
        center=0 if kind=='path' and n==3 else 3
        need(r['original_center_color']==center,'literal original center changed')
        alphabet=set(range(4))-{center}
        degree,count=dynamic_minimum(kind,n,m,alphabet)
        formula=2*n+m if kind=='cyclic' else 2*n+m-1
        need(degree==r['minimum_degree']==formula,'minimum complete-link degree mismatch')
        w=r['witness_color_word'];need(len(w)==degree and w[0]==1 and set(w)<=alphabet,'wrong local literal word')
        es=list(zip(w,w[1:]))+([(w[-1],w[0])] if kind=='cyclic' else [])
        need(all(a!=b for a,b in es) and (kind=='cyclic' or w[-1]==1),'local link improper')
        ones=w.count(1);non1=sum(a!=1 and b!=1 for a,b in es)
        need(ones>=n and non1>=m,'local word insufficient')
        need(non1==(degree-2*ones if kind=='cyclic' else degree+1-2*ones),'full edge-count identity wrong')
        need(r['word_is_not_a_source'] is True,'word promoted to source')
        stats.append(dict(kind=kind,n1=n,D0=m,minimum_degree=degree,minimum_color_words=count))
    return sorted(stats,key=lambda r:(r['kind'],r['n1'],r['D0']))

def B_controls(rows):
    need(len(rows)==3,'B controls missing');stats=[]
    for r in rows:
        need(set(r['colors'].values())<={1,3},'not complete13 palette')
        adj=graph(r['colors'],r['edges']);A=component(adj,'b',r['cut'])
        need(len(component(adj,'b',None))==len(adj),'B named graph disconnected')
        need(A==set(r['b_component']) and not A&set(r['C_in_B']),'B cut/all-C separation mismatch')
        hasc='c' in A;need(hasc==r['c_in_b_component'],'c membership mismatch')
        trigger=r['cut']=='q' and hasc;need(trigger==r['corner_trigger'],'q corner trigger wrong')
        need('Y' in adj['q'] and 'c' in adj['q'],'original boundary Y-q-c missing')
        if trigger:
            S=r['special_Y_q_c_path'];path_check(S,adj)
            need(S[:3]==['Y','q','c'] and S[-1]=='b' and set(S[2:])<=A,'q-c-b full same-component path lost')
            need(set(S[1:]).isdisjoint(r['C_in_B']),'wrong last-C vertex on S')
        else:need(r['special_Y_q_c_path'] is None,'untriggered corner path invented')
        frames=A&{'V','Y','q','c'}
        need(bool(frames)==trigger,'private vs q rootless-tail distinction wrong')
        stats.append(dict(name=r['name'],b_component=sorted(A),boundary_contact_count=len(frames),conditional_exclusion_triggered=trigger))
    return stats

def C_controls(rows):
    need(len(rows)==2,'C controls missing');stats=[]
    for r in rows:
        need(set(r['colors'].values())<={1,2},'not complete12 palette')
        adj=graph(r['colors'],r['edges']);R=component(adj,'r','U');E=component(adj,'e','U')
        need(R==set(r['r_branch']) and E==set(r['e_branch']) and not R&E,'C-U r/e components wrong')
        need({'V','Y'}<=adj['U'],'original UV/UY edges missing')
        trigger=bool(R&{'V','Y'}) and bool(E&{'V','Y'});need(trigger==r['corner_trigger'],'U corner trigger wrong')
        if trigger:
            L=r['special_r_e_path'];path_check(L,adj)
            i=L.index('U');need(L[i-1:i+2] in [['V','U','Y'],['Y','U','V']],'U path does not use the two boundary edges')
        else:need(r['special_r_e_path'] is None,'untriggered U path invented')
        stats.append(dict(name=r['name'],r_neighbor_frames=sorted(R&{'V','Y'}),e_neighbor_frames=sorted(E&{'V','Y'}),conditional_exclusion_triggered=trigger))
    return stats

def escape(r):
    adj=graph(r['colors'],r['original_edges']);P=r['same_P_tail'];path_check(P,adj)
    need(P==['b','x','c'] and [r['colors'][v] for v in P]==[1,0,1],'same literal01 tail lost')
    B={v for v,c in r['colors'].items() if c in (1,3)}
    need(B==set(r['B13_vertices']) and component({v:adj[v]&B for v in B},'b','q')=={'b'},'B-q tail component wrong')
    need(not set(P[1:-1])&B and not set(P)&set(r['original_K_vertices']),'escape supplemented inside B or through K')
    need(r['root02_label']=='L0' and r['not_a_source'] is True,'L0/source qualification lost')
    return dict(P01=P,B13_component_after_q_deletion=['b'],P_internal_vertices_not_in_B=['x'])

def validate(c,seed=0):
    need(c['schema']=='941-wrong-side-branches-v2' and c['base']==BASE,'certificate scope drift')
    need(c['paper_claims']==['exact_two_shared_b3_b_branch_has_no_B14_contact_including_q_case','private_shared_b3_degree_at_least_6_plus_D0','q_shared_b3_F_degree_at_least_7_plus_D0','q_both_patch_b1_not_Y_F_degree_at_least_9_plus_D0','same_P_tail_has_B_free_01_escape_in_nonK_J_minus_B_branch','opposite_patches_shared_U_r_e_branches_cannot_split_V_Y','opposite_patches_shared_U_F_degree_at_least_5_plus_D0','opposite_patches_shared_U_G_degree_at_least_6_plus_D0'],'paper label contract changed')
    need(c['boundaries']==dict(source_control='not triggered',finite_calibration='triggered and holds',source_realized=False,general_wrong_side='OPEN',initial_pair_exclusions=0,common_k_lower_bound=23,new_Lean=False,smaller_bad=False,Wstar_may_equal_q=True,E_may_be_rootless=True,U_and_q_use_F_link_paths=True,P_tail_not_assumed_inside_B=True),'unsupported source promotion or erased exception')
    return dict(links=links(c['link_controls'],seed),B13=B_controls(c['B13_controls']),C12=C_controls(c['C12_controls']),P_escape=escape(c['escape_control']))

def negatives(c):
    mutations=[('drop_link_domain',lambda x:x['link_controls'].pop()),('lower_private_degree',lambda x:x['link_controls'][0].update(minimum_degree=5)),('lower_q_path_degree',lambda x:x['link_controls'][6].update(minimum_degree=5)),('break_proper_link',lambda x:x['link_controls'][0]['witness_color_word'].__setitem__(1,1)),('erase_q_c_component',lambda x:x['B13_controls'][1].update(c_in_b_component=False)),('skip_original_qc',lambda x:x['B13_controls'][1]['special_Y_q_c_path'].remove('c')),('invent_U_untriggered',lambda x:x['C12_controls'][0].update(corner_trigger=False)),('make_tail_inside_B',lambda x:x['escape_control']['B13_vertices'].append('x')),('promote_source',lambda x:x['boundaries'].update(source_realized=True)),('erase_frame_path_exception',lambda x:x['boundaries'].update(U_and_q_use_F_link_paths=False)),('erase_rootless_E',lambda x:x['boundaries'].update(E_may_be_rootless=False))]
    out=[]
    for name,mutate in mutations:
        b=deepcopy(c);mutate(b)
        try:validate(b)
        except (ValueError,KeyError,IndexError,TypeError):out.append(dict(name=name,status='rejected'))
        else:raise ValueError('accepted corruption: '+name)
    return out

def main():
    p=argparse.ArgumentParser();p.add_argument('--seed',type=int,default=0);p.add_argument('--negative',action='store_true');p.add_argument('--certificate',type=Path,default=HERE/'certificate-v2.json');a=p.parse_args()
    n=custody();c=json.loads(a.certificate.read_text());stats=validate(c,a.seed)
    out=dict(status='PASS',seed=a.seed,authority_inputs=n,finite_calibration='triggered and holds',source_control='not triggered',statistics=stats)
    if a.negative:out['negative_controls']=negatives(c)
    print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
