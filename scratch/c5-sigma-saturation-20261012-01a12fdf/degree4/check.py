#!/usr/bin/env python3
"""Independent finite degree-four saturation counterexample certificate."""
import hashlib
import itertools
import json
import pathlib
import sys
import networkx as nx

ROOT = pathlib.Path('/home/ray/developer/ai/math')
SOURCE = ROOT / 'artifacts/c5_cells/cells.json'
OUT = pathlib.Path(__file__).parent / 'report.json'
COLORS = range(4)
B = tuple(range(5))
C5 = {(min(i,(i+1)%5),max(i,(i+1)%5)) for i in B}
EXTRA = {(2,4),(0,5),(0,7),(1,6),(1,7),(2,5),(2,6),(4,5),(5,6),(5,7),(6,7)}
E = C5 | EXTRA
FACIAL = [(0,1,7),(0,7,5),(1,6,7),(1,2,6),(2,5,4),(2,6,5),(5,7,6),(0,5,4),(2,4,3)]

def normalize(colors):
    image={}; out=[]
    for color in colors:
        if color not in image: image[color]=len(image)
        out.append(image[color])
    return tuple(out)

BOUNDARIES = [b for b in itertools.product(COLORS,repeat=5) if all(b[i]!=b[(i+1)%5] for i in B)]
REPS = sorted({normalize(b) for b in BOUNDARIES})
assert len(BOUNDARIES)==240 and len(REPS)==10

def brute(vertices,edges,boundary):
    inner=sorted(set(vertices)-set(B)); found=[]
    for values in itertools.product(COLORS,repeat=len(inner)):
        c=dict(enumerate(boundary)); c.update(zip(inner,values))
        if all(c[u]!=c[v] for u,v in edges): found.append(values)
    return found

def backtrack(vertices,edges,boundary):
    inner=sorted(set(vertices)-set(B)); adj={u:set() for u in vertices}
    for u,v in edges: adj[u].add(v); adj[v].add(u)
    c=dict(enumerate(boundary)); found=[]
    if any(u in c and v in c and c[u]==c[v] for u,v in edges): return []
    def go():
        remaining=[u for u in inner if u not in c]
        if not remaining:
            found.append(tuple(c[u] for u in inner)); return
        palettes={u: [a for a in COLORS if all(c.get(v)!=a for v in adj[u])] for u in remaining}
        u=min(remaining,key=lambda u:(len(palettes[u]),-len(adj[u]),u))
        for a in palettes[u]: c[u]=a;go();del c[u]
    go();return sorted(found)

def quotient(pair):
    gone,keep=pair
    assert gone>=5 and keep<5
    vertices=set(range(8))-{7,gone}
    q=set()
    for u,v in E:
        if 7 in (u,v): continue
        a=keep if u==gone else u;b=keep if v==gone else v
        assert a!=b
        q.add(tuple(sorted((a,b))))
    assert C5<=q
    return vertices,q

VERTICES=set(range(8))
A=quotient((6,0)); D=quotient((5,1))
GRAPHS={'G':(VERTICES,E),'H_06':A,'H_15':D}
result={'class':'simple plane disk, named outer C5, boundary chords allowed','boundary':B,'extra_edges':sorted(EXTRA),'degree4_vertex':7,'cyclic_link':[0,1,6,5],'pattern_order':REPS,'graphs':{},'source':{'catalogue_path':str(SOURCE),'catalogue_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'networkx_version':nx.__version__,'networkx_planarity_sha256':hashlib.sha256(pathlib.Path(nx.algorithms.planarity.__file__).read_bytes()).hexdigest()},'explicit_internal_faces':FACIAL}
for name,(vs,es) in GRAPHS.items():
    fibers=[brute(vs,es,b) for b in REPS]
    bits=sum(1<<j for j,f in enumerate(fibers) if f)
    for b in BOUNDARIES:
        assert brute(vs,es,b)==backtrack(vs,es,b)
        j=REPS.index(normalize(b))
        assert bool(brute(vs,es,b))==bool(bits>>j&1)
    g=nx.Graph();g.add_nodes_from(vs);g.add_edges_from(es)
    apex=max(vs)+1;g.add_edges_from((apex,i) for i in B)
    planar,embedding=nx.check_planarity(g)
    assert planar
    result['graphs'][name]={'vertices':sorted(vs),'edges':sorted(es),'interior_vertices':sorted(vs-set(B)),'sigma_bits':bits,'fibres':fibers,'counts':[len(f) for f in fibers],'apex_planar':planar,'all_240_boundary_full_fibres_brute_equals_backtracking':True,'global_color_orbit_check':True}

# Every explicitly listed internal edge is twice on the facial boundaries;
# every C5 edge occurs once. Nine triangles give Euler's 3k+7 equality.
face_counts={e:0 for e in E}
for f in FACIAL:
    for i in range(3):
        edge=tuple(sorted((f[i],f[(i+1)%3])))
        assert edge in E;face_counts[edge]+=1
assert all(face_counts[e]==(1 if e in C5 else 2) for e in E)
assert len(E)==16==3*3+7 and len(FACIAL)==9==2*3+3
assert result['graphs']['G']['sigma_bits']==429
assert result['graphs']['H_06']['sigma_bits']==424
assert result['graphs']['H_15']['sigma_bits']==165
assert 424|165==429 and 424!=429 and 165!=429

# Recompute branch masks directly on original graph colorings, including v.
original=result['graphs']['G']['fibres'];branch=[0,0];branch_fibres=[[],[]]
for j,(b,fiber) in enumerate(zip(REPS,original)):
    ac=[f for f in fiber if f[1]==b[0]]
    bd=[f for f in fiber if f[0]==b[1]]
    assert set(ac)|set(bd)==set(fiber)
    branch_fibres[0].append(ac);branch_fibres[1].append(bd)
    if ac:branch[0]|=1<<j
    if bd:branch[1]|=1<<j
assert branch==[424,165]
result['direct_original_branch_fibres']={'a_equals_c':branch_fibres[0],'b_equals_d':branch_fibres[1]}
result['exclusive_rows']={'only_H_06':[j for j in range(10) if (424 & ~165)>>j&1],'only_H_15':[j for j in range(10) if (165 & ~424)>>j&1]}
catalogue=json.loads(SOURCE.read_text())
assert catalogue['pattern_order']==[list(b) for b in REPS]
result['catalogue_key429_minimum_k_eff_observed']=catalogue['cells']['429']['k_eff']
assert result['catalogue_key429_minimum_k_eff_observed']==3
result['saturation_reason']='Fixed outer C5 has E=3k+7 with all 9 internal faces triangular; no planar simple edge can be added inside that fixed disk.'
OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'out':str(OUT),'script_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),'json_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'graphs':{key:{field:value[field] for field in ['sigma_bits','counts','apex_planar']} for key,value in result['graphs'].items()},'exclusive_rows':result['exclusive_rows'],'source':result['source']},ensure_ascii=False))
