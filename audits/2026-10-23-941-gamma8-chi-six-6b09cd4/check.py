#!/usr/bin/env python3
"""Read-only, independent finite reconstruction; source exclusion is the paper proof."""
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
CELLS='audits/2026-10-23-941-gamma8-cells-6b09cd4/certificate.json'
CAPS='audits/2026-10-23-941-gamma8-empty-m2-6b09cd4/K6_CAPS.json'
REDUCTION='audits/2026-10-23-941-types-wrong-side-round2-6b09cd4/reduction-certificate.json'
KB=['d','p_d','U','p_x','x','zeta']
INNER=['r','T','s','tau','a','y','b']

def require(ok,msg):
    if not ok:raise ValueError(msg)

def edge(a,b):return tuple(sorted((a,b)))

def frozen(name):return json.loads((HERE/'frozen'/name).read_text())

def custody():
    m=json.loads((HERE/'INPUTS.json').read_text())
    require(m['schema']=='941-gamma8-chi-six-inputs-v1' and m['base']==BASE,'authority contract')
    for r in m['inputs']+m['routing_entry']:
        raw=(HERE/r['snapshot']).read_bytes()
        require((len(raw),sha256(raw).hexdigest())==(r['bytes'],r['sha256']),'frozen drift '+r['path'])
    for r in m['inputs']:
        raw=(ROOT/r['path']).read_bytes()
        require((len(raw),sha256(raw).hexdigest())==(r['bytes'],r['sha256']),'live authority drift '+r['path'])
    return dict(authority_inputs=len(m['inputs']),routing_snapshots=len(m['routing_entry']),immutable_drift=0)

def with_star(edges,center,link):
    return edges|{edge(center,z) for z in link}|{edge(a,b) for a,b in zip(link,link[1:]+link[:1])}

def link_options(start,pool):
    # All degree >=5 complete cycles containing the two prescribed source faces.
    for n in range(2,len(pool)+1):
        for chosen in combinations(pool,n):
            for perm in permutations(chosen):yield [*start,*perm]

def setup(cell,contract,chi,alias):
    image=lambda z:'d' if alias and z=='U' else z
    colors={image(v):c for v,c in dict(contract['original_colors'],a=3,b=3,y=1,p_d=2,p_x=2,U=0,chi=chi).items()}
    labels={image(v):c for v,c in dict(contract['original_component_labels'],a='N',b='N',y='N',p_d='K',p_x='K',U='K',chi='L' if chi==2 else 'B').items()}
    old={edge(*e) for e in cell['edges']}
    es=old|{edge(*e) for e in [('T','a'),('T','y'),('T','b'),('r','a'),('a','y'),('y','b'),('b','s'),('d','p_d'),('x','p_x')]}
    full=dict(T=['r','tau','s','b','y','a'])
    for v in ('tau','zeta'):full[v]=[b if a==v else a for a,b in old if v in (a,b)]
    return image,colors,labels,es,old,full

def valid(es,colors,labels,cell,old,full):
    adj={z:set() for z in colors}
    original=set(['r','T','s','x','h','W','e','d','tau','zeta'])
    rootless={'M','N'}
    psi={z:(c^2 if labels[z]=='K' else c) for z,c in colors.items()}
    for a,b in es:
        if a==b or colors[a]==colors[b]:return False
        if {a,b}<=original and edge(a,b) not in old:return False
        if {a,b}&{'tau','zeta'} and not {a,b}<=original:return False
        if {colors[a],colors[b]}<={0,2} and labels[a]!=labels[b]:return False
        if {colors[a],colors[b]}<={1,3} and labels[a]!=labels[b]:return False
        # Complete J-K rootless branch excludes contact to any rooted non-K node.
        if labels[a]!='K' and labels[b]!='K' and ((labels[a] in rootless)!=(labels[b] in rootless)):return False
        adj[a].add(b);adj[b].add(a)
    cside={'r','d','e','U'}&set(colors)
    eside={'s','x','h'}
    unseen={z for z in colors if psi[z] in (1,2)}
    while unseen:
        start=min(unseen);stack=[start];seen={start};unseen.remove(start)
        while stack:
            v=stack.pop()
            for w in adj[v]&unseen:
                if psi[w] in (1,2):unseen.remove(w);seen.add(w);stack.append(w)
        if seen&cside and seen&eside:return False
    for v,link in full.items():
        if len(link)!=len(set(link)) or adj[v]!=set(link):return False
        if v in ('tau','zeta'):continue
        if any(edge(a,b) not in es for a,b in zip(link,link[1:]+link[:1])):return False
        for i,a in enumerate(link):
            for j,b in enumerate(link):
                if i<j and j-i not in (1,len(link)-1) and edge(a,b) in es:return False
    for a,b in combinations(colors,2):
        if colors[a]==colors[b] and len(adj[a]&adj[b])>2:return False
    forbidden=[('r','s'),('d','x')]
    if cell['core'] in ('L','O'):forbidden.append(('T','x'))
    if cell['core'] in ('R','O'):forbidden.append(('T','d'))
    ext={'a','b','y','p_d','p_x','U','chi'}
    if any(adj[a]&adj[b]&ext for a,b in forbidden):return False
    return True

def reconstruct_stars():
    contract=frozen(CELLS);caps={c['core']:c for c in frozen(CAPS)['caps']};out=[]
    for cell in contract['candidates']:
        if cell['classification']!='local_necessary_type':continue
        for chi,alias in product((2,3),(False,True)):
            image,colors,labels,es,old,full=setup(cell,contract,chi,alias)
            pool=sorted({image(v) for v in ['d','x','U','p_d','p_x','chi']})
            ys=[];joins=[]
            for yl in link_options(['a','T','b'],pool):
                ey=with_star(es,'y',yl);fy=dict(full,y=yl)
                if not valid(ey,colors,labels,cell,old,fy):continue
                ys.append(yl)
                singles={}
                for center,anchor in [('a','r'),('b','s')]:
                    singles[center]=[]
                    for lk in link_options([anchor,'T','y'],pool):
                        ex=with_star(ey,center,lk);fx=dict(fy,**{center:lk})
                        if valid(ex,colors,labels,cell,old,fx):singles[center].append(lk)
                for al,bl in product(singles['a'],singles['b']):
                    eab=with_star(with_star(ey,'a',al),'b',bl)
                    fab=dict(fy,a=al,b=bl)
                    if not valid(eab,colors,labels,cell,old,fab):continue
                    chosen=set(KB+INNER)
                    actual={e for e in eab if set(e)<=chosen}
                    require(cell['core']!='O','O source-star contradiction lost')
                    cap=caps[cell['core']]
                    require(actual=={edge(*e) for e in cap['edges']},'different sealed cap')
                    require(not any('chi' in e for e in eab),'chi attached rootless star')
                    joins.append(dict(y=yl,a=al,b=bl,cap=cell['core']))
            out.append(dict(cell=cell['id'],core=cell['core'],chi_color=chi,U_equals_d=alias,
                complete_y_links=ys,joint_star_rows=joins,
                status='sealed_K6_required' if joins else 'excluded_star_join'))
    require(len(out)==44,'eleven/two-chi/two-U domain')
    require(sum(len(r['joint_star_rows']) for r in out)==16,'expected eight core-ear rows times two chi')
    return out

def canonical(w):
    d={};return tuple(d.setdefault(c,len(d)) for c in w)

def full_lifts(cap,word):
    # Independent backtracking through actual original edges, no producer mask.
    adj={v:set() for v in cap['vertices']}
    for a,b in cap['edges']:adj[a].add(b);adj[b].add(a)
    assigned=dict(zip(KB,word));result=[]
    order=sorted(INNER,key=lambda v:(-len(adj[v]),v))
    def visit(i):
        if i==len(order):result.append([assigned[v] for v in INNER]);return
        v=order[i]
        for color in range(4):
            if all(assigned.get(w)!=color for w in adj[v]):assigned[v]=color;visit(i+1);del assigned[v]
    visit(0)
    return sorted(result)

def verify_rotation(cap):
    edges={edge(*e) for e in cap['edges']};directed={}
    faces=cap['oriented_actual_faces']
    require(len(faces)==18 and len({tuple(sorted(f)) for f in faces})==18,'actual face domain')
    for f in faces:
        require(len(set(f))==3 and set(f)&set(INNER),'private original face owner')
        for a,b in zip(f,f[1:]+f[:1]):
            require(edge(a,b) in edges and (a,b) not in directed,'face incidence or common orientation')
            directed[a,b]=True
    require({e for e in directed if e[::-1] not in directed}==set(zip(KB,KB[1:]+KB[:1])),'oriented actual boundary')
    for center in INNER:
        faces_at=[f for f in faces if center in f];n={z for e in edges if center in e for z in e if z!=center}
        arcs=[]
        for f in faces_at:
            i=f.index(center);arcs.append((f[(i+1)%3],f[(i+2)%3]))
        require(len(arcs)==len(n) and {a for a,b in arcs}==n and {b for a,b in arcs}==n,'interior complete rotation')
        nxt=dict(arcs);start=min(n);cycle=[start]
        while nxt[cycle[-1]]!=start:
            cycle.append(nxt[cycle[-1]]);require(len(cycle)<=len(n),'noncyclic private rotation')
        require(len(cycle)==len(n),'split private rotation')

def candidate_graphs():
    ring={tuple(sorted((i,(i+1)%6))) for i in range(6)};out=[]
    for p in (0,1):
        ports=list(range(6));chosen=list(range(p,6,2))
        chords={tuple(sorted((a,b))) for a,b in combinations(chosen,2)}
        for kind in ('triangle','identify'):
            pm=ports if kind=='triangle' else [chosen[0] if i in chosen else i for i in ports]
            es=ring|chords if kind=='triangle' else {tuple(sorted((pm[a],pm[b]))) for a,b in ring}
            vertices=sorted(set(pm));relation=set()
            for w in product(range(4),repeat=len(vertices)):
                col=dict(zip(vertices,w))
                if all(col[a]!=col[b] for a,b in es):relation.add(tuple(col[v] for v in pm))
            out.append(dict(id=kind+'_'+('even' if p==0 else 'odd'),port_map=pm,edges=[list(e) for e in sorted(es)],
                k_drop=7 if kind=='triangle' else 9,relation=relation))
    return out

def reconstruct_relations():
    words=sorted({canonical(w) for w in product(range(4),repeat=6) if all(w[i]!=w[(i+1)%6] for i in range(6))})
    require(len(words)==31,'all proper normalized six-frame rows')
    graphs=candidate_graphs();caprows=[]
    for cap in frozen(CAPS)['caps']:
        verify_rotation(cap)
        rows=[dict(word=list(w),full_lifts=full_lifts(cap,w)) for w in words]
        relation={tuple(r['word']) for r in rows if r['full_lifts']}
        require(len(relation)==19 and sum(len(r['full_lifts']) for r in rows)==52,'R19 complete fibres')
        covering=[]
        for graph in graphs:
            domain={canonical(w) for w in graph['relation']}
            require(domain<=relation,'candidate single-direction backfill failed')
            covering.append(domain)
        require(set.union(*covering)==relation,'same-frame complete coverage failed')
        caprows.append(dict(core=cap['core'],ordered_boundary=KB,ordered_inner=INNER,normalized_rows=rows,
            vertices=cap['vertices'],original_edges=cap['edges'],oriented_actual_faces=cap['oriented_actual_faces']))
    return caprows,[{k:v for k,v in g.items() if k!='relation'}|dict(
        normalized_support=[list(w) for w in sorted({canonical(w) for w in g['relation']})],
        complete_literal_relation=''.join('1' if w in g['relation'] else '0' for w in product(range(4),repeat=6))) for g in graphs]

def calculate():
    stars=reconstruct_stars();caps,graphs=reconstruct_relations()
    return dict(schema='941-gamma8-chi-six-v1',base=BASE,
        paper_contract=dict(Gamma_interior_points=2,full_M2_empty=True,T_degree=6,exterior_private_points=6,
            chi_original_color_options=[2,3],chi_anticomplete_full_rootless_J_minus_K_branch=True,
            same_original_graph_rotation_and_literal_frame=True,U_F_link_is_not_complete_cyclic_star=True),
        complete_star_cases=stars,exact_K6_caps=caps,four_reduction_graphs=graphs,
        authority_boundaries=dict(finite_control='triggered and holds',source_realizability='not triggered',
            paper_excluded_branch='empty_M2_T6_X6',paper_empty_M2_minimum_exterior=7,
            paper_all_eleven_minimum_exterior=7,eleven_entire_type_exclusions=0,common_k_lower_bound=23,
            empty_M2_seven_exterior='OPEN',general_wrong_side='OPEN',new_Lean=False,new_LP=False))

def validate(c,expected,seed=0):
    require(c==expected,'semantic certificate disagreement')
    shuffled=list(c['complete_star_cases']);random.Random(seed).shuffle(shuffled)
    require(len(shuffled)==44,'shuffled domain lost')
    return dict(star_cases=44,complete_star_rows=sum(len(r['joint_star_rows']) for r in shuffled),
        exact_caps=2,normalized_cap_fibres=62,full_lifts=104,empty_normalized_cap_fibres=24,
        reduction_graphs=4,literal_candidate_relation_bits=4*4096,source_realizability='not triggered')

def negatives(c,expected):
    changes=[('drop_case',lambda z:z['complete_star_cases'].pop()),
        ('change_chi_ownership',lambda z:z['paper_contract'].update(chi_anticomplete_full_rootless_J_minus_K_branch=False)),
        ('invent_U_cyclic_star',lambda z:z['paper_contract'].update(U_F_link_is_not_complete_cyclic_star=False)),
        ('drop_full_lift',lambda z:next(r for r in z['exact_K6_caps'][0]['normalized_rows'] if r['full_lifts'])['full_lifts'].pop()),
        ('erase_empty_fibre',lambda z:z['exact_K6_caps'][0]['normalized_rows'].pop()),
        ('reverse_single_actual_face',lambda z:z['exact_K6_caps'][0]['oriented_actual_faces'][0].reverse()),
        ('change_quotient',lambda z:z['four_reduction_graphs'][1]['port_map'].__setitem__(2,2)),
        ('change_completed_cost',lambda z:z['four_reduction_graphs'][0].update(k_drop=6)),
        ('invent_source',lambda z:z['authority_boundaries'].update(source_realizability='triggered and holds')),
        ('raise_global_k',lambda z:z['authority_boundaries'].update(common_k_lower_bound=24))]
    rows=[]
    for name,mutate in changes:
        bad=deepcopy(c);mutate(bad)
        try:validate(bad,expected)
        except ValueError:rows.append(dict(name=name,status='rejected'))
        else:raise ValueError('negative accepted '+name)
    return rows

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--certificate',type=Path,default=HERE/'certificate.json')
    ap.add_argument('--seed',type=int,default=0);ap.add_argument('--negative',action='store_true');args=ap.parse_args()
    auth=custody();expected=calculate();c=json.loads(args.certificate.read_text())
    result=dict(status='PASS',seed=args.seed,custody=auth,**validate(c,expected,args.seed))
    if args.negative:result['semantic_negatives']=negatives(c,expected)
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,IndexError,TypeError,OSError,json.JSONDecodeError) as exc:
        print(json.dumps(dict(status='REJECT',reason=str(exc)),sort_keys=True));sys.exit(1)
