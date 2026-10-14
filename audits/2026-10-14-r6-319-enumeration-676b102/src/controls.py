#!/usr/bin/env python3
"""Brute-force solver calibration, complete seven-pin table, negative controls."""
import copy
import importlib.util
from itertools import product
import json
import search
import replay

def main():
    search.seal();h=search.HERE
    cells=json.loads((h/'frozen/artifacts/c5_cells/cells.json').read_text())
    checks=0
    for mask in (271,314,319):
        cell=cells['cells'][str(mask)];n=5+cell['k_eff'];adj=[set() for _ in range(n)]
        for u,v in [(i,(i+1)%5) for i in range(5)]+cell['edges']:
            adj[u].add(v);adj[v].add(u)
        actual_mask=0
        for i,word in enumerate(search.WORDS):
            expected=[]
            for tail in product('0123',repeat=n-5):
                lift=word+''.join(tail)
                if search.proper(adj,lift):expected.append(lift)
            actual=search.solve(adj,list(map(int,word)),True)
            assert sorted(actual)==sorted(expected)
            one=search.solve(adj,list(map(int,word)))
            assert bool(one)==bool(expected) and all(v in expected for v in one)
            if actual:actual_mask|=1<<i
            checks+=1
        assert actual_mask==mask
    # Independent direct all-r-lifts predicate, without importing the search table.
    def normalize(row):
        names={};return tuple(names.setdefault(c,len(names)) for c in row)
    edges=[(i,(i+1)%5) for i in range(5)]+[(0,5),(5,6),(6,0)]
    permitted=set()
    for f in product(range(4),repeat=7):
        if any(f[u]==f[v] for u,v in edges):continue
        z,s,v,w,t,p,q=f;good=True
        for r in set(range(4))-{s,v,w,t}:
            if z==r:ok=s==t and {p,q}==set(range(4))-{z,s}
            elif s==t:ok=bool({p,q}&(set(range(4))-{z,s,r,t}))
            else:ok={p,q}=={s,t}
            good &= ok
        if good:permitted.add(normalize(f))
    table={tuple(map(int,word+pq)) for word,pqs in zip(search.WORDS,search.PQ) for pq in pqs.split()}
    assert permitted==table and len(table)==26
    # Validate and tamper an actual pilot complete-coloring witness.
    with search.open_read(h/'runs/pilot29-filter.jsonl') as stream:source=json.loads(next(stream))
    with search.open_read(h/'runs/pilot29-audit.jsonl.gz') as stream:record=json.loads(next(stream))
    frame=source['frames'][0];result=record['results'][0]
    replay.validate(source['rotation'],frame,result)
    negative=0
    corrupt=copy.deepcopy(result);corrupt['lift']='0'*len(result['lift'])
    try:replay.validate(source['rotation'],frame,corrupt)
    except AssertionError:negative+=1
    corrupt=copy.deepcopy(result);corrupt['row']=0
    try:replay.validate(source['rotation'],frame,corrupt)
    except AssertionError:negative+=1
    corrupt=copy.deepcopy(result);corrupt['u_original_order'][5],corrupt['u_original_order'][6]=corrupt['u_original_order'][6],corrupt['u_original_order'][5]
    try:replay.validate(source['rotation'],frame,corrupt)
    except AssertionError:negative+=1
    assert negative==3
    print(json.dumps({'status':'PASS','brute_full_fibres':checks,'labelled_seven_pin_assignments':4**7,'allowed_canonical_joint_rows':len(table),'rejected_corruptions':negative}))

if __name__=='__main__':main()
