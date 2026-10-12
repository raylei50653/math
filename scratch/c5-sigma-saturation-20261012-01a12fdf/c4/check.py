#!/usr/bin/env python3
"""Finite C4 interface certificate from the fixed C5 catalogue.
The universal C4 theorem additionally uses the published universal C5 necessary
screen: every catalogue-exterior feasible relation accepts all T4, so a chorded
C5 cell's relation lies in the catalogue. This script verifies only the finite
map, all literal witnesses, planarity, and full assignment fibres.
"""
import hashlib,itertools,json,pathlib,sys
import networkx as nx
SOURCE=pathlib.Path('/home/ray/developer/ai/math/artifacts/c5_cells/cells.json')
OUT=pathlib.Path(__file__).parent/'report.json'
p=json.loads(SOURCE.read_text())
def normalize(colors):
    d={};out=[]
    for c in colors:
        if c not in d:d[c]=len(d)
        out.append(d[c])
    return tuple(out)
def legal_cycle(colors):return all(colors[i]!=colors[(i+1)%len(colors)] for i in range(len(colors)))
C4_REPS=sorted({normalize(b) for b in itertools.product(range(4),repeat=4) if legal_cycle(b)})
C5_REPS=sorted({normalize(b) for b in itertools.product(range(4),repeat=5) if legal_cycle(b)})
assert len(C4_REPS)==4 and len(C5_REPS)==10
assert [list(r) for r in C5_REPS]==p['pattern_order']
BOUND4=[b for b in itertools.product(range(4),repeat=4) if legal_cycle(b)]
BOUND5=[b for b in itertools.product(range(4),repeat=5) if legal_cycle(b)]
C4_VERTS=(0,2,3,4);DUMMY=1
C4_EDGES={tuple(sorted((C4_VERTS[i],C4_VERTS[(i+1)%4]))) for i in range(4)}
C5_EDGES={tuple(sorted((i,(i+1)%5))) for i in range(5)}

def brute(vs,es,bvs,b):
    inner=sorted(set(vs)-set(bvs));found=[]
    for vals in itertools.product(range(4),repeat=len(inner)):
        c=dict(zip(bvs,b));c.update(zip(inner,vals))
        if all(c[u]!=c[v] for u,v in es):found.append(vals)
    return found

def backtrack(vs,es,bvs,b):
    inner=sorted(set(vs)-set(bvs));adj={u:set() for u in vs}
    for u,v in es:adj[u].add(v);adj[v].add(u)
    c=dict(zip(bvs,b));found=[]
    if any(u in c and v in c and c[u]==c[v] for u,v in es):return []
    def visit():
        rest=[u for u in inner if u not in c]
        if not rest:found.append(tuple(c[u] for u in inner));return
        options={u:[t for t in range(4) if all(c.get(v)!=t for v in adj[u])] for u in rest}
        u=min(rest,key=lambda v:(len(options[v]),-len(adj[v]),v))
        for t in options[u]:c[u]=t;visit();del c[u]
    visit();return sorted(found)

def apex_planar(vs,es,bvs):
    g=nx.Graph();g.add_nodes_from(vs);g.add_edges_from(es)
    apex=max(vs)+1;g.add_edges_from((apex,v) for v in bvs)
    return nx.check_planarity(g)[0]

pattern_map=[]
for j,r in enumerate(C5_REPS):
    permitted=r[0]!=r[2]
    c4tuple=normalize(tuple(r[i] for i in C4_VERTS)) if permitted else None
    pattern_map.append({'c5_index':j,'c5_pattern':r,'chord_02_permits':permitted,'c4_pattern':c4tuple,'c4_index':C4_REPS.index(c4tuple) if permitted else None})

result={'boundary_geometry':'Original C4=(a,b,c,x); add exterior dummy z with edges az,zb, retain ab; augmented C5=(a,z,b,c,x), original edge ab is chord02. Dummy label1 is deleted from returned witnesses.','C4_boundary_labels':C4_VERTS,'C4_pattern_order':C4_REPS,'C5_pattern_order':C5_REPS,'full_pattern_map':pattern_map,'all_16_mask_map':[],'witnesses':[],'universal_paper_premise':'Published C5 necessary screen implies that every realizable chorded-C5 boundary relation is in K; finite checks below do not prove this premise.','source':{'catalogue_path':str(SOURCE),'catalogue_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'networkx_version':nx.__version__,'networkx_planarity_sha256':hashlib.sha256(pathlib.Path(nx.algorithms.planarity.__file__).read_bytes()).hexdigest()}}
for mask in range(16):
    lifted=sum(1<<r['c5_index'] for r in pattern_map if r['chord_02_permits'] and mask>>r['c4_index']&1)
    entry=p['cells'].get(str(lifted))
    result['all_16_mask_map'].append({'c4_mask':mask,'lifted_c5_mask':lifted,'in_catalogue':entry is not None,'catalogue_k_eff':entry['k_eff'] if entry else None})
    if entry is None:continue
    es5=C5_EDGES|{tuple(sorted(e)) for e in entry['edges']}
    vs5=set(v for e in es5 for v in e)
    assert {v for e in es5 if 1 in e for v in e if v!=1}=={0,2}
    assert (0,2) in es5
    vs4=vs5-{1};es4={e for e in es5 if 1 not in e}
    assert C4_EDGES<=es4
    f4=[brute(vs4,es4,C4_VERTS,b) for b in C4_REPS]
    m4=sum(1<<j for j,f in enumerate(f4) if f)
    f5=[brute(vs5,es5,tuple(range(5)),b) for b in C5_REPS]
    m5=sum(1<<j for j,f in enumerate(f5) if f)
    assert m4==mask and m5==lifted
    for b in BOUND4:
        assert brute(vs4,es4,C4_VERTS,b)==backtrack(vs4,es4,C4_VERTS,b)
        assert bool(brute(vs4,es4,C4_VERTS,b))==bool(mask>>C4_REPS.index(normalize(b))&1)
    for b in BOUND5:
        assert brute(vs5,es5,tuple(range(5)),b)==backtrack(vs5,es5,tuple(range(5)),b)
    assert apex_planar(vs5,es5,tuple(range(5))) and apex_planar(vs4,es4,C4_VERTS)
    assert len(vs4-set(C4_VERTS))==entry['k_eff']<=3
    result['witnesses'].append({'c4_mask':mask,'c5_mask':lifted,'interior_count':entry['k_eff'],'dummy_degree':2,'literal_C5_vertices':sorted(vs5),'literal_C5_edges':sorted(es5),'literal_C4_vertices':sorted(vs4),'literal_C4_edges':sorted(es4),'C4_interior_order':sorted(vs4-set(C4_VERTS)),'C4_full_fibres':f4,'C4_counts':[len(f) for f in f4],'C5_full_fibres':f5,'apex_planar_C4_and_C5':True,'all_84_C4_and_240_C5_boundary_full_fibres_brute_equals_backtracking':True})
assert len(BOUND4)==84 and len(result['witnesses'])==7
assert [r['c4_mask'] for r in result['witnesses']]==[7,10,11,12,13,14,15]
result['summary']={'possible_c4_masks_under_paper_premise':[7,10,11,12,13,14,15],'maximum_witness_interiors':3,'full_C4_boundary_assignments':len(BOUND4),'full_C5_boundary_assignments':len(BOUND5),'finite_mapping_complete':True}
OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'out':str(OUT),'script_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),'json_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'summary':result['summary'],'witnesses':[{k:r[k] for k in ['c4_mask','c5_mask','interior_count','dummy_degree','C4_counts']} for r in result['witnesses']],'source':result['source']},ensure_ascii=False))
