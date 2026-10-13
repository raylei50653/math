#!/usr/bin/env python3
"""Independent small-order generator test by all labelled edge subsets.

Enumerates every simple graph with 3n-6 edges (n=4..7), then independently
recognises planarity using NetworkX 3.5. No expansion/reduction/plantri code is
used to generate this universe. Isomorphism collapses it only after testing.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import tempfile
import networkx as nx
from check import HERE,AUDIT,planar_code,edges,sha,encode


def run():
    result={'method':'all labelled edge subsets; networkx left-right planarity; VF2 isomorphism','networkx_version':nx.__version__,'domains':[]}
    for n in range(4,8):
        universe=list(itertools.combinations(range(n),2)); wanted=3*n-6
        statistics={'n':n,'edge_sets':0,'minimum_degree_three':0,'planar_labelled':0,'classes':0,'plantri_classes':0}
        representatives=[]
        # Complement enumeration covers the whole choose(C(n,2),3n-6) set exactly.
        for missing in itertools.combinations(universe,len(universe)-wanted):
            statistics['edge_sets']+=1; omitted=set(missing)
            selected=[e for e in universe if e not in omitted]
            deg=[0]*n
            for u,v in selected:deg[u]+=1;deg[v]+=1
            if min(deg)<3:continue
            statistics['minimum_degree_three']+=1
            graph=nx.Graph();graph.add_nodes_from(range(n));graph.add_edges_from(selected)
            planar,_=nx.check_planarity(graph)
            if not planar:continue
            statistics['planar_labelled']+=1
            signature=tuple(sorted(deg))
            if not any(signature==sig and nx.is_isomorphic(graph,rep) for sig,rep in representatives):
                representatives.append((signature,graph))
        statistics['classes']=len(representatives)
        command=[str(AUDIT/'generation/plantri'),str(n)]
        proc=subprocess.run(command,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        with tempfile.NamedTemporaryFile(dir=HERE,suffix='.pc') as f:
            f.write(proc.stdout);f.flush();produced=planar_code(f.name)
        gen=[]
        for rotation in produced:
            graph=nx.Graph();graph.add_nodes_from(rotation);graph.add_edges_from(edges(rotation));gen.append(graph)
        statistics['plantri_classes']=len(gen)
        assert len(gen)==len(representatives)
        assert all(sum(nx.is_isomorphic(rep,g) for g in gen)==1 for _,rep in representatives)
        assert all(sum(nx.is_isomorphic(rep,g) for _,rep in representatives)==1 for g in gen)
        statistics['representative_edges']=[sorted([list(e) for e in rep.edges()]) for _,rep in representatives]
        statistics['plantri_stdout_sha256']=hashlib.sha256(proc.stdout).hexdigest()
        statistics['plantri_stderr']=proc.stderr.decode().strip()
        result['domains'].append(statistics)
        print(n,statistics['edge_sets'],statistics['planar_labelled'],statistics['classes'],flush=True)
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    answer=run();path=HERE/'small_exhaustive.json';data=encode(answer)
    # Runtime printed by plantri is deliberately not part of mathematical comparison.
    if args.check:
        old=json.loads(path.read_text())
        for domain in old['domains']:domain.pop('plantri_stderr',None)
        for domain in answer['domains']:domain.pop('plantri_stderr',None)
        assert old==answer
    else:
        with path.open('xb') as f:f.write(data+b'\n')
    print('PASS: independent complete labelled small-order graph enumeration')
