import itertools, json, pathlib
import networkx as nx
OUT=pathlib.Path(__file__).parent
REPS=[(0,1,0,1,2),(0,1,0,2,1),(0,1,0,2,3),(0,1,2,0,1),(0,1,2,0,2),(0,1,2,0,3),(0,1,2,1,2),(0,1,2,1,3),(0,1,2,3,1),(0,1,2,3,2)]
E={tuple(sorted(e)) for e in [(0,1),(1,2),(2,3),(3,4),(4,0),(0,2)]}
faces=[(0,1,2),(0,2,3,4)]
patches=[]
old=2
for j in range(2):
    a,b,c=5+3*j,6+3*j,7+3*j
    # The octahedron has opposite pairs (0,a), (1,b), (old,c).
    vs=(0,1,old,a,b,c)
    missing={tuple(sorted(e)) for e in [(0,a),(1,b),(old,c)]}
    for u,v in itertools.combinations(vs,2):
        edge=tuple(sorted((u,v)))
        if edge not in missing:E.add(edge)
    faces.remove((0,1,old))
    fs=[(0,1,c),(0,old,b),(1,old,a),(0,b,c),(1,a,c),(old,a,b),(a,b,c)]
    faces.extend(fs)
    patches.append({'outer':[0,1,old],'inner':[a,b,c],'opposite_pairs':[[0,a],[1,b],[old,c]],'faces':fs})
    old=c
G=nx.Graph();G.add_nodes_from(range(11));G.add_edges_from(E)
# Apex certificate proves the C5 can be the outer boundary of a disk.
A=G.copy();A.add_edges_from((11,i) for i in range(5))
assert nx.check_planarity(A)[0]
# Explicit face decomposition: each boundary edge in one interior face, all other edges in two.
counts={e:0 for e in E}
for f in faces:
    for u,v in zip(f,f[1:]+f[:1]):counts[tuple(sorted((u,v)))]+=1
B={tuple(sorted(e)) for e in [(0,1),(1,2),(2,3),(3,4),(4,0)]}
assert all(n==(1 if e in B else 2) for e,n in counts.items())
assert len(faces)==14 and len(E)==24
cofacial=sorted({tuple(sorted((u,v))) for f in faces for u,v in itertools.combinations(f,2) if not G.has_edge(u,v)})
assert cofacial==[(0,3),(2,4)]
def fibres(extra=()):
    edges=sorted(E|{tuple(sorted(e)) for e in extra})
    ans=[]
    for b in REPS:
        fs=[]
        for x in itertools.product(range(4),repeat=6):
            coloring=b+x
            if all(coloring[u]!=coloring[v] for u,v in edges):fs.append(x)
        ans.append(fs)
    return ans
def mask(fs):return sum(1<<i for i,f in enumerate(fs) if f)
F=fibres();assert mask(F)==1016
rows=[{'index':i,'pattern':b,'count':len(f),'lifts':f} for i,(b,f) in enumerate(zip(REPS,F))]
assert [len(f) for f in F]==[0,0,0,16,16,16,16,16,16,16]
additions=[]
for e in cofacial:
    fs=fibres([e]);additions.append({'edge':e,'mask':mask(fs),'removed_bits':mask(F)&~mask(fs),'rows':[{'index':i,'count':len(f),'lifts':f} for i,f in enumerate(fs)]})
assert [a['mask'] for a in additions]==[960,424]
# All simple cycles of interior induced graph (at most 6 verts), exact length 5 test.
I=G.subgraph(range(5,11));cycles=[]
for tup in itertools.permutations(range(5,11),5):
    if tup[0]!=min(tup) or tup[1]>tup[-1]:continue
    if all(I.has_edge(u,v) for u,v in zip(tup,tup[1:]+tup[:1])):cycles.append(tup)
assert not cycles
# Optional topology check all graph C5 separations disjoint from boundary.
report={'boundary':[0,1,2,3,4],'interior':list(range(5,11)),'edges':sorted(E),'inner_faces':faces,'octahedron_patches':patches,'k':6,'E':len(E),'internal_face_count':len(faces),'triangle_count':sum(len(f)==3 for f in faces),'quadrilateral_count':sum(len(f)==4 for f in faces),'interior_degree':{v:G.degree[v] for v in range(5,11)},'interior_induced_edges':sorted(I.edges()),'interior_induced_blocks':[sorted(b) for b in nx.biconnected_components(I)],'all_interior_C5':cycles,'apex_planar':True,'mask':mask(F),'rows':rows,'admissible_fixed_embedding_nonedges':cofacial,'additions':additions}
(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('rows','additions')},indent=2))
print('base_counts', [len(f) for f in F])
for a in additions:print('addition',a['edge'],'mask',a['mask'],'removed',a['removed_bits'],'counts',[r['count'] for r in a['rows']])
# Second route: independent constraint backtracking with dynamically selected variables.
def backtrack_fibres(edges):
    adj={v:set() for v in range(11)}
    for u,v in edges:adj[u].add(v);adj[v].add(u)
    all_rows=[]
    for boundary in REPS:
        colors={i:boundary[i] for i in range(5)}
        if any(colors[u]==colors[v] for u,v in edges if u<5 and v<5):all_rows.append([]);continue
        solutions=[]
        def visit():
            if len(colors)==11:
                solutions.append(tuple(colors[i] for i in range(5,11)));return
            choices=[]
            for v in range(5,11):
                if v not in colors:
                    avail=tuple(c for c in range(4) if all(colors.get(w)!=c for w in adj[v] if w in colors))
                    choices.append((len(avail),-sum(w in colors for w in adj[v]),v,avail))
            _,_,v,avail=min(choices)
            for c in avail:
                colors[v]=c;visit();del colors[v]
        visit();all_rows.append(sorted(solutions))
    return all_rows
assert backtrack_fibres(E)==F
for a in additions:
    extra={tuple(a['edge'])}
    assert backtrack_fibres(E|extra)==[r['lifts'] for r in a['rows']]
# All abstract disk-admissible added edges, permitting a different planar embedding.
# Apex planarity is the existing project condition for an outer C5 disk.
apex_admissible=[]
for e in itertools.combinations(range(11),2):
    if G.has_edge(*e):continue
    trial=A.copy();trial.add_edge(*e)
    if nx.check_planarity(trial)[0]:apex_admissible.append(e)
assert apex_admissible==cofacial
report['apex_admissible_nonedges']=apex_admissible
report['independent_full_fibre_backtracking_match']=True
# Turn interior face cycles into coherent directed cycles, opposite across every edge.
remaining=[tuple(f) for f in faces];oriented=[(0,1,2,3,4)]
# 'Outer' boundary orientation above is opposite the orientation of every inner incident face.
while remaining:
    used={(u,v) for f in oriented for u,v in zip(f,f[1:]+f[:1])}
    for i,f in enumerate(remaining):
        arcs=list(zip(f,f[1:]+f[:1]))
        shared=[(u,v) for u,v in arcs if (u,v) in used or (v,u) in used]
        if not shared:continue
        same=sum((u,v) in used for u,v in shared)
        reverse=sum((v,u) in used for u,v in shared)
        assert not (same and reverse)
        oriented.append(tuple(reversed(f)) if same else f)
        remaining.pop(i);break
    else:raise AssertionError('face dual disconnected')
all_arcs=[(u,v) for f in oriented for u,v in zip(f,f[1:]+f[:1])]
assert len(set(all_arcs))==2*len(E) and len(all_arcs)==2*len(E)
assert all((u,v) in all_arcs and (v,u) in all_arcs for u,v in E)
report['oriented_faces_outer_first']=oriented
report['enumeration_routes']={'direct_product':{'assignments_per_row':4**6,'rows_per_graph':10,'graphs':3},'constraint_backtracking':{'compared':'each complete six-vertex lift tuple per row','all_match':True},'apex_nonedge_check':{'nonedges_checked':55-len(E),'accepted':apex_admissible}}
(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print('all abstract disk-admissible additions',apex_admissible)
print('independent full fibre backtracking: all 30 rows match')
print('oriented faces',oriented)
print('full common fibre for all accepted rows',F[3])
