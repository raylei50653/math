#!/usr/bin/env python3
"""Read-only bounded same-F component-tree/bridge audit; no source enumeration."""
import argparse
from collections import deque
from copy import deepcopy
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import random
import sys
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BASE = 'cb8f8593e273a7426ecadd59797a6e643cc4768e'
PREV = 'audits/2026-10-23-three-mask-methods-cb8f859/941/'
Y = 'HL_0'
B14 = ['a','z1','z2','z3','z4','V','U',Y,'q','c','s','v','w','t']

def require(ok, reason):
    if not ok:
        raise ValueError(reason)

def packed(v):
    return (json.dumps(v, sort_keys=True, separators=(',', ':'))+'\n').encode()

def frozen(path):
    return (HERE/'frozen'/path).read_bytes()

def authority():
    m = json.loads((HERE/'INPUTS.json').read_text())
    require(m['base'] == BASE, 'BASE changed')
    for row in m['inputs']:
        b = frozen(row['path'])
        require(len(b)==row['bytes'] and sha256(b).hexdigest()==row['sha256'], 'frozen mathematical drift: '+row['path'])
        require((ROOT/row['path']).read_bytes()==b, 'live mathematical drift: '+row['path'])
    routing = []
    for row in m['routing_entry']:
        b = (HERE / row.get('snapshot_path', 'routing-entry/'+row['path'])).read_bytes()
        require(len(b)==row['bytes'] and sha256(b).hexdigest()==row['sha256'], 'routing entry snapshot drift')
        live = (ROOT/row['path']).read_bytes()
        routing.append(dict(path=row['path'], entry_sha256=row['sha256'], live_sha256=sha256(live).hexdigest(), changed=live!=b))
    return m, routing

def components(vertices, edges):
    adj = {v:set() for v in vertices}
    for a,b in edges:
        if a in adj and b in adj:
            adj[a].add(b); adj[b].add(a)
    out = []
    while adj:
        todo = [min(adj)]; seen = set()
        while todo:
            v = todo.pop()
            if v in seen:
                continue
            seen.add(v); todo.extend(adj[v]-seen)
        out.append(sorted(seen))
        for v in seen:
            del adj[v]
    return sorted(out)

def edges_of(faces):
    return sorted({tuple(sorted((f[i],f[(i+1)%3]))) for f in faces for i in range(3)})

def wheel(name, center, center_color, rim):
    names = [x[0] for x in rim]
    return dict(name=name, colors={center:center_color,**dict(rim)}, boundary=names,
                faces=[[center,names[i],names[(i+1)%len(names)]] for i in range(len(names))])

def ear(g, a, b, name, color):
    bd = g['boundary']; i = bd.index(a)
    require(bd[(i+1)%len(bd)]==b, 'ear not on ordered boundary edge')
    bd.insert(i+1,name); g['colors'][name]=color; g['faces'].append([a,name,b])

def cap_corner(g, a, old, b, name, color):
    bd=g['boundary']; i=bd.index(old)
    require(bd[(i-1)%len(bd)]==a and bd[(i+1)%len(bd)]==b, 'cap not on boundary corner')
    bd[i]=name; g['colors'][name]=color
    g['faces'].extend([[a,name,old],[old,name,b]])

def controls():
    result=[]
    g=wheel('exit5_K2_inside', 'X',3,[('U',0),('p',1),('L',0),('r',1),('Z',2)])
    cap_corner(g,'r','Z','U','R',3)
    g.update(kind='exit',root='U',target='L',actual_path=['U','X','L'],marked='X',private_original_degree=5,fifth_2_in_K=True)
    result.append(g)
    g=wheel('exit5_K2_outside','X',3,[('U',0),('p',1),('L',0),('Z',2),('r',1)])
    g.update(kind='exit',root='U',target='L',actual_path=['U','X','L'],marked='X',private_original_degree=5,fifth_2_in_K=False)
    result.append(g)
    g=wheel('exit6_without_2','X',3,[('U',0),('p',1),('L',0),('r',1),('W',0),('s',1)])
    g.update(kind='exit',root='U',target='L',actual_path=['U','X','L'],marked='X',private_original_degree=6)
    result.append(g)
    for side,rim in [('C',[('r',1),('A',3),('c',1),('B',3),('Z',2)]),
                     ('outside_C',[('r',1),('A',3),('Z',2),('c',1),('B',3)])]:
        g=wheel('bridge5_fifth2_'+side,'T',0,rim)
        ear(g,'r','A','U',0)
        g.update(kind='bridge',root='U',target='c',actual_path=['U','r','T','c'],marked='T',private_original_degree=5,fifth_2_in_C=(side=='C'))
        result.append(g)
    g=wheel('bridge6_without_2','T',0,[('r',1),('A',3),('c',1),('B',3),('p',1),('D',3)])
    ear(g,'r','A','U',0)
    g.update(kind='bridge',root='U',target='c',actual_path=['U','r','T','c'],marked='T',private_original_degree=6)
    result.append(g)
    g=wheel('rootless_13_branch_retained','h',3,[('U',0),('Z',2),('A',0),('B',2),('C',0),('D',2)])
    ear(g,'U','Z','V',1); ear(g,'U','V','J',3); ear(g,'J','V','L',0)
    g.update(kind='rootless',root='U',target='L',actual_path=['U','J','L'],marked='J',rootless_vertex='h')
    result.append(g)
    return result

def disk_check(g):
    cs=g['colors']; faces=g['faces']; bd=g['boundary']; edges=edges_of(faces)
    require(len(set(bd))==len(bd), 'boundary not simple')
    require(all(len(set(f))==3 and set(f)<=set(cs) for f in faces), 'malformed face')
    require(all(cs[a]!=cs[b] for a,b in edges), 'improper original edge')
    incid={e:[] for e in edges}
    for f in faces:
        for i in range(3):
            a,b=f[i],f[(i+1)%3]; incid[tuple(sorted((a,b)))].append((a,b))
    boundary_edges={tuple(sorted((bd[i],bd[(i+1)%len(bd)]))) for i in range(len(bd))}
    require({e for e,fs in incid.items() if len(fs)==1}==boundary_edges, 'untriangulated boundary or missing face')
    require(all(len(fs)==1 or (len(fs)==2 and fs[0]==tuple(reversed(fs[1]))) for fs in incid.values()), 'inconsistent oriented triangulation')
    require(len(cs)-len(edges)+len(faces)==1, 'disk Euler characteristic changed')
    # At each interior vertex, the complete link must be a single cycle.
    for v in cs:
        le=[tuple(x for x in f if x!=v) for f in faces if v in f]
        ns={x for e in le for x in e}
        require(len(components(ns,le))==1, 'disconnected vertex link')
        ds={x:sum(x in e for e in le) for x in ns}
        if v not in bd:
            require(all(d==2 for d in ds.values()), 'private link not complete cyclic link')
        else:
            require(sorted(ds.values()).count(1)==2 and all(d in {1,2} for d in ds.values()), 'boundary link not a path')
    return edges

def partition(cs, edges, palette, boundary):
    comps=components({v for v,c in cs.items() if c in palette},edges)
    return [dict(vertices=c,boundary_contacts=[v for v in boundary if v in c]) for c in comps]

def component_tree(g, edges):
    cs=g['colors']; bd=g['boundary']; split=[]; labels={}
    for palette in ({0,2},{1,3}):
        for row in partition(cs,edges,palette,bd):
            lab=len(split); split.append(dict(id=lab,palette=sorted(palette),**row))
            labels.update({v:lab for v in row['vertices']})
    pairs={tuple(sorted((labels[a],labels[b]))) for a,b in edges if (cs[a]%2)!=(cs[b]%2)}
    require(len(pairs)==len(split)-1 and len(components(range(len(split)),pairs))==1,'full component adjacency is not a tree')
    # Independent interface construction: one zero-level segment per triangle.
    cross={tuple(sorted((a,b))) for a,b in edges if cs[a]%2!=cs[b]%2}
    segments=[]
    for f in g['faces']:
        xs=[tuple(sorted((f[i],f[(i+1)%3]))) for i in range(3) if cs[f[i]]%2!=cs[f[(i+1)%3]]%2]
        require(len(xs)==2, 'triangular face misses one palette group')
        segments.append(tuple(xs))
    ic=components(cross,segments)
    interface_pairs=[]
    for line in ic:
        ns={tuple(sorted((labels[a],labels[b]))) for a,b in line}
        require(len(ns)==1,'an interface changes its full component sides')
        interface_pairs.append(list(next(iter(ns))))
    require(sorted(interface_pairs)==[list(x) for x in sorted(pairs)],'interface dual disagrees with direct full-component graph')
    return dict(complete_components=split,edges=[list(e) for e in sorted(pairs)],interface_components=[[list(e) for e in line] for line in ic]),labels

def shortest(cs, edges, palette, start, end):
    adj={v:[] for v,c in cs.items() if c in palette}
    for a,b in edges:
        if a in adj and b in adj:
            adj[a].append(b); adj[b].append(a)
    todo=deque([[start]]);seen={start}
    while todo:
        p=todo.popleft()
        if p[-1]==end:
            return p
        for v in sorted(adj[p[-1]]):
            if v not in seen:
                seen.add(v); todo.append(p+[v])
    raise ValueError('named actual path absent')

def local_record(g):
    edges=disk_check(g); tree,labels=component_tree(g,edges); cs=g['colors']; root=g['root']; target=g['target']
    K=set(next(c for c in components({v for v,c in cs.items() if c in {0,2}},edges) if root in c))
    changed={v:(c^2 if v in K else c) for v,c in cs.items()}
    require(all(changed[a]!=changed[b] for a,b in edges),'whole-K swap improper')
    palette={0,1} if g['kind']=='bridge' else {0,3}
    p=g['actual_path']; actual=shortest(cs,edges,palette,root,target)
    require(len(p)==len(actual),'named path is not shortest in actual induced graph')
    require(all(tuple(sorted((a,b))) in edges for a,b in zip(p,p[1:])) and all(cs[v] in palette for v in p),'path has a false original edge/palette')
    rec=dict(name=g['name'],graph=g,original_edges=[list(e) for e in edges],full_02_13_component_tree=tree,
             complete_K=sorted(K),complete_K_boundary_contacts=[v for v in g['boundary'] if v in K],shortest_actual_path=p,
             complete_before_after_palette_relations={},original_941_source_control='not triggered')
    for pal in combinations(range(4),2):
        key=''.join(map(str,pal))
        rec['complete_before_after_palette_relations'][key]=dict(before=partition(cs,edges,set(pal),g['boundary']),after=partition(changed,edges,set(pal),g['boundary']))
    if g['kind'] in {'exit','rootless'}:
        i=max(i for i,v in enumerate(p) if cs[v]==0 and v in K)
        X=p[i+1]; require(X==g['marked'],'last-exit marker wrong')
        B=labels[X]; L=labels[target]; k=labels[root]
        require([min(k,B),max(k,B)] in tree['edges'] and [min(B,L),max(B,L)] in tree['edges'],'K-B-L tree path absent')
        require(all(v not in K for v in p[i+1:]), 'last exit tail returns to K')
        require(X in next(c for c in components({v for v,c in changed.items() if c in {0,3}},edges) if target in c),'last exit loses unchanged 03 tail')
        rec['bottleneck']=dict(last_exit=X,complete_13_component=tree['complete_components'][B],next_0_component_is_not_assumed_to_equal_L=True)
        if g['kind']=='rootless':
            H=tree['complete_components'][labels[g['rootless_vertex']]]
            require(H['boundary_contacts']==[] and H['id']!=B,'rootless branch disappeared or used as last exit')
            rec['retained_rootless_13_branch']=H
        elif g['private_original_degree']==5:
            require(('Z' in K)==g['fifth_2_in_K'],'fifth-2 K side changed')
    else:
        C=set(next(c for c in components({v for v,c in changed.items() if c in {1,2}},edges) if root in c))
        require(target not in C,'post-swap forbidden bridge is already connected')
        one_positions=[i for i,v in enumerate(p) if cs[v]==1]
        transition=next((i,j) for i,j in zip(one_positions,one_positions[1:]) if (p[i] in C)!=(p[j] in C))
        i,j=transition; require(j==i+2,'01 path is not alternating')
        T=p[i+1];require(T==g['marked'] and T not in K and cs[T]==0,'bridge zero is not outside K')
        neighbors={b if a==T else a for a,b in edges if T in (a,b)}
        require(all(v not in K for v in neighbors if cs[v]==2),'bridge has a K2 neighbour')
        require(sum(cs[v]==3 for v in neighbors)>=2,'missing two original colour3 separators')
        three={v for v in neighbors if cs[v]==3}
        new03=next(c for c in components({v for v,c in changed.items() if c in {0,3}},edges) if T in c)
        require(three<=set(new03),'bridge colour3 neighbours split across new03 components')
        if g['private_original_degree']==5:
            require(sorted(cs[v] for v in neighbors)==[1,1,2,3,3] and ('Z' in C)==g['fifth_2_in_C'],'private degree-five bridge classification failed')
        else:
            require(not any(cs[v]==2 for v in neighbors) and len(neighbors)==6,'even degree-six no2 branch omitted')
        rec['bridge']=dict(vertex=T,successor_C=sorted(C),two_neighbouring_1_vertices=[p[i],p[j]],all_original_2_neighbours_outside_K=True,
                           original_colour3_neighbours=sorted(three),one_actual_successor_03_component=new03)
    return rec

def source_rows(prior):
    out=[]
    for old in prior['component_interface_rows']:
        row=deepcopy(old); target=row['target']; e0,e1=(0,1) if target==44459 else (1,0)
        cs=dict(zip(B14,[0,3,0,3,0,1,0,1,3,1,2,e0,e1,2]));changed={**cs,'U':2}
        bs=row['full_03_successor_boundary_contacts']; C=next(b for b in bs if 'U' in b)
        require(set(changed[v] for v in C)<={1,2} and {'V',Y,'t'}<=set(C) and 'c' not in C,'unique successor 12 separation lost')
        require(next(b for b in row['complete_initial_02_contacts'] if 'U' in b)==['U'],'K boundary contacts changed')
        require(next(b for b in row['complete_initial_02_contacts'] if 'V' in b)==['V',Y,'q','c'],'B13 contacts changed')
        gates=[]
        for gate in row['complete_initial_01_gate']:
            big=next(b for b in gate if 'U' in b)
            require('c' in big,'original01 U-c obligation lost')
            allowed=[v for v in B14 if v!='U' and cs[v]==0 and v in big]
            gates.append(dict(complete_initial_01_contacts=gate,possible_boundary_bridge_zeros=allowed,
                              successor_03_component_of_boundary_bridge={v:next(b for b in bs if v in b) for v in allowed}))
        row['new_joint_restrictions']=dict(
            full_component_adjacency_tree_includes_all_rootless_components=True,
            forced_tree_path=['K02(U)','B13(V,Y,q,c)','L02(z4)'],
            initial03_type4_last_exit=dict(original_colour=3,private=True,belongs_to_complete_B13=True,
                all_original_colour1_neighbours_in_complete_B13=True,
                next_0_component_may_be_a_different_branch_than_L=True,
                complete_B13_connections_required_to=['V',Y,'q','c']),
            original01_successor12_bridge=dict(exists_on_one_shortest_actual_original01_U_to_c_path=True,
                original_colour=0,outside_complete_K=True,all_original_colour2_neighbours_outside_K=True,
                private_case_degree5_neighbour_multiset=[1,1,2,3,3],private_case_at_least_two_original_colour3_neighbours=True,
                all_colour3_neighbours_in_one_actual_successor03_component=True,
                private_degree_at_least6_branch_retained=True,complete_boundary_cases_by_initial01=gates))
        out.append(row)
    return out

def build(seed):
    authority(); prior=json.loads(frozen(PREV+'certificate.json'))
    gs=controls(); random.Random(seed).shuffle(gs)
    local=sorted([local_record(g) for g in gs],key=lambda r:r['name'])
    require(any(r.get('retained_rootless_13_branch') for r in local),'rootless private component omitted')
    return dict(base=BASE,scope='ordinary short Type-I; same complete F; initial02 types13/36; no source realization',
                source_rows=source_rows(prior),local_controls=local,
                upstream_complete_fibre_custody=prior['upstream_complete_fibre_custody'],
                source_lemma_status='conditional paper proof; finite local calibration',
                original_941_controls_triggered=0,new_pair_exclusions=0,source_realized=False,
                degree5_sides_both_retained=True,degree_at_least6_retained=True,
                rootless_components_retained=True,arbitrary_private_size_bound=None,new_Lean=False,new_smaller_bad=False)

def validate(value, expected):
    require(value==expected,'certificate differs from frozen full reconstruction')

def negatives(expected):
    variants=[]
    c=deepcopy(expected);c['source_rows'][0]['new_joint_restrictions']['initial03_type4_last_exit']['belongs_to_complete_B13']=False;variants.append(c)
    c=deepcopy(expected);c['source_rows'][0]['new_joint_restrictions']['initial03_type4_last_exit']['next_0_component_may_be_a_different_branch_than_L']=False;variants.append(c)
    c=deepcopy(expected);c['source_rows'][0]['new_joint_restrictions']['original01_successor12_bridge']['all_original_colour2_neighbours_outside_K']=False;variants.append(c)
    c=deepcopy(expected);c['source_rows'][0]['complete_successor_seven_point_kernel']['complete_seven_point_fibre'].pop();variants.append(c)
    c=deepcopy(expected)
    nonempty=next(lifts for r in c['source_rows'][0]['complete_successor_original_cap_records'] for g in r['complete_original_cap_fibres'].values() for lifts in g.values() if lifts)
    nonempty.pop();variants.append(c)
    c=deepcopy(expected);c['local_controls']=[r for r in c['local_controls'] if r['name']!='rootless_13_branch_retained'];variants.append(c)
    c=deepcopy(expected);c['degree_at_least6_retained']=False;variants.append(c)
    c=deepcopy(expected);c['new_pair_exclusions']=1;variants.append(c)
    c=deepcopy(expected);c['source_realized']=True;variants.append(c)
    for c in variants:
        try: validate(c,expected)
        except ValueError: pass
        else: raise ValueError('corrupted certificate accepted')
    g=controls()[0];g['faces'].pop()
    try: disk_check(g)
    except ValueError: pass
    else: raise ValueError('nontriangulated source premise accepted')
    # Concrete obstruction when triangular-face coverage is absent:
    # U0-V1-L0-H3-U0 has quotient cycle and last exit H != V.
    square={'U':0,'V':1,'L':0,'H':3}; es=[('U','V'),('V','L'),('L','H'),('H','U')]
    cs02=components({'U','L'},es);cs13=components({'V','H'},es)
    require(len(cs02)+len(cs13)==4 and shortest(square,es,{0,3},'U','L')==['U','H','L'],'missing-triangulation obstruction changed')
    return len(variants)+2

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--build',action='store_true');ap.add_argument('--seed',type=int)
    ap.add_argument('--certificate',type=Path,default=HERE/'certificate.json')
    args=ap.parse_args(); expected=json.loads(packed(build(args.seed)))
    n=negatives(expected)
    if args.build:
        with args.certificate.open('xb') as f: f.write(packed(expected))
    validate(json.loads(args.certificate.read_text()),expected)
    _,routing=authority()
    print(json.dumps(dict(result='PASS',base=BASE,source_rows=len(expected['source_rows']),
        complete_local_controls=len(expected['local_controls']),negative_controls=n,
        mathematical_input_drift=0,routing_drift=routing,original_941_controls_triggered=0,
        new_pair_exclusions=0,complete_fibre_custody=expected['upstream_complete_fibre_custody']),sort_keys=True))
if __name__=='__main__':
    main()
