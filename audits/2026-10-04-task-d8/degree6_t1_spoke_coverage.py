#!/usr/bin/env python3
"""Audit the omitted t=1 relative-spoke cases in the unchanged checker.
Uses its finite helper only; fixed rows q0,q1,q3, no extra acceptance bits.
The actual original geometry and its ownership are rotated with the spoke.
"""
import argparse
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
TARGET=ROOT/'scripts/c5_excess_two_e3_degree6.py'
OUT=Path(__file__).with_suffix('.json')

def build():
    spec=importlib.util.spec_from_file_location('d6audit',TARGET)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    slit=[(a,b) for a in range(6) for b in range(a+2,6)]
    ordered=[(a,b) for a,b in m.product(slit,repeat=2) if a[1]<=b[0]]
    base=[tuple(tuple(i%5 for i in range(iv[j][0],iv[j][1]+1)) for j in order) for iv in ordered for order in m.permutations(range(2))]
    rows=[]
    for root_spoke in range(5):
        geometries=[tuple(tuple((i+root_spoke)%5 for i in e) for e in g) for g in base]
        for kind in ('t1_(4,1)','t1_(3,2)'):
            result=[m.solve((root_spoke,),g,(2,1),fourbags=0,Drole=1,contact_arities=(4,1)) if kind=='t1_(4,1)' else m.solve((root_spoke,),g,(2,1),paths=(0,),Drole=1,contact_arities=(2,3)) for g in geometries]
            survives=[x for x in result if x['surviving_necessary_profile'] is not None]
            rows.append(dict(kind=kind,original_spoke=root_spoke,named_geometries=len(result),remaining=len(survives),search_nodes=sum(x['search_counts']['search_nodes'] for x in result),survivors=survives))
    return dict(scope='Audit extension of existing helper domain to every original spoke; fixed q0 q1 q3 frame; no claim these abstract profiles are realizable',results=rows)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');args=ap.parse_args()
    result=build();payload=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.check:assert OUT.read_bytes()==payload.encode()
    else:
        with OUT.open('x') as f:f.write(payload)
    for r in result['results']:
        print(r['kind'],r['original_spoke'],'geometries',r['named_geometries'],'remaining',r['remaining'],'nodes',r['search_nodes'])
if __name__=='__main__':main()
