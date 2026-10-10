#!/usr/bin/env python3
"""Independent input/finite-control audit. Does not import or modify PG code.
Its symbolic checks support, but do not prove, arbitrary-size paper claims.
"""
import collections,hashlib,itertools,json,subprocess
from pathlib import Path
D=Path(__file__).resolve().parent
I=json.loads((D/'inputs.json').read_text())
ROOT=Path(I['root']); BASE=I['BASE']
sha=lambda b:hashlib.sha256(b).hexdigest()
for e in I['entries']:
    data=(D/e['frozen']).read_bytes()
    assert sha(data)==e['sha256'] and len(data)==e['bytes']
    if e['role'].startswith('BASE-'):
        data=subprocess.check_output(['git','show',e['source']],cwd=ROOT)
        assert sha(data)==e['sha256']
        assert subprocess.check_output(['git','rev-parse',e['source']],cwd=ROOT).decode().strip()==e['git_blob']
    elif e['role']!='current-context-not-mathematical-dependency':
        assert sha((ROOT/e['source']).read_bytes())==e['sha256']
J=json.loads((D/'frozen/pg/certificate.json').read_text())
# Independently assign labeled consecutive two-edge arcs to U,L, remainder to S.
arcs={frozenset([i,(i+1)%5]) for i in range(5)}
partitions={(u,l,frozenset(set(range(5))-u-l)) for u in arcs for l in arcs if not u&l and len(set(range(5))-u-l)==1}
assert len(partitions)==10
edge=lambda a,b:frozenset([a,b])
B={edge('b'+str(i),'b'+str((i+1)%5)) for i in range(5)}
G=B|{edge(p,'b'+str(i)) for p,indices in [('U',[0,1,2]),('L',[2,3,4]),('S',[4,0])] for i in indices}|{edge('r',p) for p in ['U','L','S']}|{edge('s',p) for p in ['L','S']}
# All nine actual original edges supplied by paper, with ports assigned to whole pieces.
ports={**{x:'U' for x in ['u0','u2','x']},**{x:'L' for x in ['l3','l4','lr','ls']},**{x:'S' for x in ['v0','v4','vr','vs']}}
models=[
('rb4',[{'U'},{'b4'},{'L','s'}],[{'S','b0'},{'b2','b3'},{'r'}],[[('u0','b0'),('u2','b2'),('x','r')],[('b4','v4'),('b4','b3'),('b4','r')],[('s','vs'),('l3','b3'),('lr','r')]]),
('sb0',[{'U','b0'},{'L'},{'S'}],[{'r'},{'s'},{'b4'}],[[('x','r'),('b0','s'),('b0','b4')],[('lr','r'),('ls','s'),('l4','b4')],[('vr','r'),('vs','s'),('v4','b4')]]),
('sb2',[{'U','b2'},{'L'},{'S'}],[{'r'},{'s'},{'b3','b4'}],[[('x','r'),('b2','s'),('b2','b3')],[('lr','r'),('ls','s'),('l4','b4')],[('vr','r'),('vs','s'),('v4','b4')]])]
for label,A,Z,rows in models:
    assert sum(map(len,A+Z))==len(set.union(*A,*Z))
    for i in range(3):
        for j in range(3):
            a,b=rows[i][j]
            assert ports.get(a,a) in A[i] and ports.get(b,b) in Z[j]
            assert edge(ports.get(a,a),ports.get(b,b)) in G|{edge(label[0],'b'+label[-1])}
# Shared contact identifications within one piece never change its whole-bag membership.
# Original connectivity follows from connected P and the named connecting edges, not templates.
for m in J['whole_D5_and_root_swap_minor_templates']:
    start=m['frame_start'];direction=m['frame_direction'];swap=m['whole_root_swap']
    def tr(x):
        if x.startswith('b'):return 'b'+str((start+direction*int(x[1:]))%5)
        return {'r':'s','s':'r'}.get(x,x) if swap else x
    graph={edge(tr(a),tr(b)) for a,b in (tuple(e) for e in G)}|{edge(*m['assumed_spoke'])}
    bags=list(map(set,m['A_bags']+m['B_bags']))
    assert sum(map(len,bags))==len(set.union(*bags))
    for bag in bags:
        reached={next(iter(bag))}
        while True:
            more={b for a in reached for b in bag if edge(a,b) in graph}-reached
            if not more:break
            reached|=more
        assert reached==bag
    assert len(m['nine_original_quotient_edges'])==9
    assert {(j['A'],j['B']) for j in m['nine_original_quotient_edges']}==set(itertools.product(range(1,4),repeat=2))
    for j in m['nine_original_quotient_edges']:
        a,b=j['retained_edge']
        assert edge(a,b) in graph
        assert (a in bags[j['A']-1] and b in bags[j['B']+2]) or (b in bags[j['A']-1] and a in bags[j['B']+2])
# Inspect supplied embeddings directly: every dart, cyclic rotation, Euler, designated B.
for m in J['abstract_contracted_disk_embeddings']:
    graph=G|{edge('r',b) for b in m['r_spokes']}|{edge('s',b) for b in m['s_spokes']}
    dart=collections.Counter((f[i],f[(i+1)%len(f)]) for f in m['faces'] for i in range(len(f)))
    assert all(n==1 for n in dart.values()) and len(dart)==2*len(graph)
    assert {edge(a,b) for a,b in dart}==graph
    assert all((b,a) in dart for a,b in dart)
    for v,rotation in m['rotation'].items():
        assert set(rotation)=={next(iter(e-{v})) for e in graph if v in e}
    assert len(m['rotation'])-len(graph)+len(m['faces'])==2
    assert any(set(f)=={'b'+str(i) for i in range(5)} and len(f)==5 for f in m['faces'])
# Incidence profiles reconstructed arithmetically, before literal/source constraints.
expected=set()
for rset in [(),(0,),(2,),(0,2)]:
    for sset in [(),(4,)]:
        for kr in range(1,4-len(rset)):
            for ks in range(1,5-len(sset)):
                expected.add((rset,sset,kr,ks,4-len(rset)-kr,5-len(sset)-ks))
actual={(tuple(int(x[1:]) for x in p['r_spokes']),tuple(int(x[1:]) for x in p['s_spokes']),*p['L_incidence'],*p['S_incidence']) for p in J['necessary_incidence_profiles']}
assert actual==expected and len(expected)==56
# Exhaustive local one-vertex palette, not a source search.
local=0
for c0,c4 in itertools.permutations(range(4),2):
    for a in range(4):
        assert any(c not in {c0,c4,a} for c in range(4))
        local+=1
assert J['counts']=={'named_shield_partitions':10,'minor_templates_with_whole_root_swap':60,'abstract_spoke_embeddings':8,'necessary_integer_profiles':56,'single_vertex_local_colour_oracles':12,'complete_target_sources':0}
print(json.dumps({'task':'N45-PGA','input_hashes_verified':len(I['entries']),'BASE_git_dependencies_verified':4,'named_partitions':10,'original_nine_edge_models':3,'nine_edge_joins':27,'whole_frame_minor_controls':60,'abstract_embeddings':8,'necessary_integer_profiles':56,'local_one_vertex_assignments_checked':local,'complete_target_sources':0,'arbitrary_size_proof_by':'independent paper derivation in REPORT.md, not this finite check','status':'PASS'},sort_keys=True))
