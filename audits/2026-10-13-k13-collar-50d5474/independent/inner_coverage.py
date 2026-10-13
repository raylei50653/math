#!/usr/bin/env python3
"""Independent cone-root/apex-subset enumeration and graph-isomorphism coverage."""
import argparse
from collections import Counter
import itertools
import json
import networkx as nx
from check import HERE,AUDIT,planar_code,faces,edges,cycle_key,encode,sha
from review import assert_faces


def embedding_map(source,target,mapping):
    for direction in (1,-1):
        if all(cycle_key([mapping[v] for v in source[u]])==cycle_key(target[mapping[u]][::direction]) for u in source):
            return direction
    raise AssertionError('mapping does not preserve one whole-graph rotation orientation')

def iso_root(g,z,h,w):
    a=nx.Graph();a.add_nodes_from((v,{'root':v==z}) for v in g);a.add_edges_from(edges(g))
    b=nx.Graph();b.add_nodes_from((v,{'root':v==w}) for v in h);b.add_edges_from(edges(h))
    gm=nx.algorithms.isomorphism.GraphMatcher(a,b,node_match=lambda x,y:x['root']==y['root'])
    for mapping in gm.isomorphisms_iter():
        try:orientation=embedding_map(g,h,mapping)
        except AssertionError:continue
        return {'mapping':mapping,'orientation':orientation}
    return None

def run():
    sph=planar_code(AUDIT/'generation/inner_spheres14.pc')
    primary=planar_code(AUDIT/'generation/spheres19.pc')
    cores=json.loads((AUDIT/'generation/inner_cores.json').read_text())
    expected={};counts={h:Counter() for h in range(4,8)}
    for sid,g in enumerate(sph):
        fs=faces(g)
        assert len(g)==14 and len(edges(g))==36 and len(fs)==24 and all(len(f)==3 for f in fs)
        assert min(map(len,g.values()))>=4
        for q,C in g.items():
            if len(C) not in (9,10,11,12):continue
            h=len(C)-5;counts[h]['cone_roots']+=1
            H={u:[v for v in ns if v!=q] for u,ns in g.items() if u!=q}
            I=set(H)-set(C)
            assert len(I)==8-h and len(edges(H))==31-h
            if any(len(H[v])<5 for v in I):continue
            counts[h]['interior_degree_eligible']+=1
            forced={v for v in C if len(H[v])==3}
            if len(forced)>5:continue
            options=sorted(set(C)-forced)
            for extra in itertools.combinations(options,5-len(forced)):
                A=forced|set(extra);key=(sid,q,tuple(sorted(A)))
                assert key not in expected
                expected[key]=(H,C);counts[h]['apex_subsets']+=1
    actual={(r['sphere_id'],r['q'],tuple(sorted(r['apex']))):r for r in cores}
    assert len(actual)==len(cores) and set(actual)==set(expected),'omitted or duplicate cone-root/apex subset'
    for key,rec in actual.items():
        H,C=expected[key]
        assert rec['H_rotation']=={str(u):ns for u,ns in H.items()},'wrong original H rotation'
        assert rec['H_edges']==edges(H),'missing original H edge/chord'
        assert_faces(rec['H_faces'],faces(H))
        assert cycle_key(rec['C']) in (cycle_key(C),cycle_key(C[::-1])),'wrong H outer boundary'
        cyc_edges={tuple(sorted((C[i],C[(i+1)%len(C)]))) for i in range(len(C))}
        chords=[e for e in edges(H) if set(e)<=set(C) and tuple(e) not in cyc_edges]
        assert rec['C_chords']==chords,'missing H chord'
        complete={u:ns for u,ns in enumerate(rec['completed_rotation'])}
        complete_faces=faces(complete)
        assert len(complete)==19 and len(edges(complete))==51 and all(len(f)==3 for f in complete_faces)
        assert min(map(len,complete.values()))>=5
        names=rec['completed_to_H_original'];rev={v:i for i,v in enumerate(names)}
        assert set(H)|{'b0','b1','b2','b3','b4','z'}==set(names) and len(names)==19
        for u in H:
            # Same literal H, cyclic order retained after annulus completion.
            ns=[names[v] for v in complete[rev[u]] if isinstance(names[v],int)]
            assert cycle_key(ns)==cycle_key(H[u]),'completion modified H rotation'
        z=rev['z'];B=[rev[f'b{i}'] for i in range(5)]
        assert cycle_key(complete[z]) in (cycle_key(B),cycle_key(B[::-1]))
        assert rec['e']==[len(complete[b])-5 for b in B],'wrong named excess'
        assert [set(v for v in complete[rev[a]] if v in B) for a in rec['apex']]==[{B[i],B[(i+1)%5]} for i in range(5)],'wrong apex attachments'
        for y in set(C)-set(rec['apex']):assert len(set(complete[rev[y]])&set(B))==1
        for v in set(H)-set(C):assert not(set(complete[rev[v]])&set(B))
        mapping={int(u):v for u,v in rec['completed_to_target'].items()};target=primary[rec['target_sphere']]
        assert set(mapping)==set(complete) and set(mapping.values())==set(target)
        assert mapping[z]==rec['target_z']
        assert embedding_map(complete,target,mapping)==rec['orientation'],'wrong recorded global orientation'
        frame=rec['target_B_frame'];target_B=target[rec['target_z']]
        assert [mapping[b] for b in B]==[target_B[(frame['shift']+frame['direction']*i)%5] for i in range(5)],'wrong target B frame'
    # Independently search rooted graph isomorphisms; do not trust saved mapping list.
    src=json.loads((AUDIT/'generation/rooted_sources.json').read_text())
    wanted=[r for r in src if r['h'] in (4,5,6,7)]
    observed=[]
    for source in wanted:
        matches=[]
        for core in cores:
            if source['h']!=core['h']:continue
            completed={u:ns for u,ns in enumerate(core['completed_rotation'])}
            match=iso_root(primary[source['sphere_id']],source['z'],completed,18)
            if match:matches.append(core['id'])
        assert matches,'primary root absent from independent interior classification'
        observed.append({'source':source['id'],'inner_cores':matches})
    saved=json.loads((AUDIT/'generation/primary_to_inner.json').read_text())
    assert observed==saved,'saved primary-to-inner mapping differs from independent rooted isomorphisms'
    configs=json.loads((AUDIT/'generation/named_configurations.json').read_text())
    expected_configs={(h,e) for h in range(4,8) for e in itertools.product(range(h+1),repeat=5) if sum(e)==h}
    assert {(r['h'],tuple(r['e'])) for r in configs}==expected_configs and len(configs)==len(expected_configs),'missing named composition'
    config_counts=Counter();orbit_counts={h:set() for h in range(4,8)}
    for rec in configs:
        e=rec['e'];h=rec['h'];config_counts[h]+=1
        images=[tuple(e[(s+d*i)%5] for i in range(5)) for d in (1,-1) for s in range(5)]
        representative=min(images)
        assert tuple(rec['representative'])==representative,'wrong D5 composition representative'
        assert tuple(e[i] for i in rec['representative_to_original_B'])==representative,'wrong composition-to-representative mapping'
        orbit_counts[h].add(representative)
        placements=[]
        for core in cores:
            for direction in (1,-1):
                for shift in range(5):
                    indices=[(shift+direction*i)%5 for i in range(5)]
                    if [core['e'][i] for i in indices]==e:
                        placements.append({'core':core['id'],'direction':direction,'shift':shift,'B_new_to_core':indices})
        assert placements==rec['core_placements'],'missing labelled core placement'
    return {'status':'pass','networkx_version':nx.__version__,'inner_spheres':len(sph),'h_counts':{str(h):dict(counts[h]) for h in range(4,8)},'inner_cores':len(cores),'primary_roots_covered':len(wanted),'named_configurations':dict(config_counts),'D5_orbits':{str(h):len(s) for h,s in orbit_counts.items()},'input_sha256':{f:sha(AUDIT/'generation'/f) for f in ('inner_spheres14.pc','inner_cores.json','primary_to_inner.json','named_configurations.json')}}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');args=ap.parse_args();result=run()
    path=HERE/'inner_coverage.json';data=encode(result)+b'\n'
    if args.check:assert path.read_bytes()==data,'inner coverage replay differs'
    else:
        with path.open('xb') as f:f.write(data)
    print(json.dumps(result,indent=2,sort_keys=True))
