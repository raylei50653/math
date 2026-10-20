#!/usr/bin/env python3
"""Exact same-core projections for original r-hole competitors; no graph realization."""
import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OLD = ROOT / 'audits/2026-10-19-r6-941-leakage-b89c591'


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


def compute():
    model = module('old_count_model', OLD / 'A/model.py')
    left = module('left_completions', HERE / 'B/minimality.py')
    eight, ten, index, _, _, _, _, _, originals, _ = model.build()
    controls = json.loads((OLD / 'A/source-positive-certificate.json').read_text())['records']
    rim = ('x', 'y', 't', 'w', 'v', 's')
    pairs = [(rim[i], rim[j]) for i in range(6) for j in range(i + 1, 6)
             if (j-i) not in (1, 5)]
    triangles = left.triangulations(6)
    catalogue = set(map(int, json.loads((ROOT / 'artifacts/c5_cells/cells.json').read_text())['cells']))
    records = []
    for kind, operations in [('quotient', pairs), ('triangulation', triangles)]:
        for operation in operations:
            transfer = []
            full_lifts = []
            for a,n,R,L,q,c,x,y in eight:
                entries = {}
                lifts = []
                for s,v,w,t in itertools.product(range(4), repeat=4):
                    core = (a,n,R,L,q,c,s,v,w,t)
                    if not model.proper(core) or x == s or y == t:
                        continue
                    f = dict(zip(('x','y','t','w','v','s'), (x,y,t,w,v,s)))
                    if kind == 'quotient':
                        if f[operation[0]] != f[operation[1]]:
                            continue
                    elif any(f[rim[i]] == f[rim[j]] for i,j in operation):
                        continue
                    i = index[model.canonical(core)]
                    entries[i] = entries.get(i, 0) + 1
                    lifts.append([s,v,w,t,i])
                transfer.append(sorted(entries.items()))
                full_lifts.append(lifts)
            projections = []
            for control in controls:
                z = control['core_counts']
                e = [sum(z[i]*weight for i,weight in entries) for entries in transfer]
                graph_counts = {name:model.mv(matrix,e) for name,matrix in originals.items()}
                if kind == 'triangulation':
                    graph_counts.update({'left_tri_' + str(j):model.mv(left.left_matrix(eight,d),e)
                                         for j,d in enumerate(triangles)})
                projections.append({'name':control['name'], 'counts':graph_counts,
                                    'masks':{name:model.mask(v) for name,v in graph_counts.items()},
                                    'outside_K132':[name for name,v in graph_counts.items() if model.mask(v) not in catalogue]})
            records.append({'kind':kind,'operation':operation,'all_lifts_svwti':full_lifts,
                            'projections':projections})
    return {'base':'13dc5ff163045c85b5c82dde438eb5f275dab999',
            'authority':'necessary same-source minimality comparisons; controls are not realized sources',
            'E_order':['a','n','R','L','q','c','x','y'],
            'E_rows':eight,'r_link':rim,'records':records}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--build',action='store_true')
    parser.add_argument('--certificate',type=Path,default=HERE/'right-minimality.json')
    args=parser.parse_args()
    result=compute()
    payload=(json.dumps(result,sort_keys=True,separators=(',',':'))+'\n').encode()
    if args.build:
        with args.certificate.open('xb') as stream:
            stream.write(payload)
    else:
        assert args.certificate.read_bytes()==payload,'complete right-hole competitor projection mismatch'
    print(json.dumps({'status':'PASS','records':len(result['records']),
                      'outside':[{ 'kind':r['kind'],'operation':r['operation'],
                                   'controls':[{ 'name':p['name'],'outside':p['outside_K132']} for p in r['projections']]}
                                  for r in result['records']],
                      'sha256':hashlib.sha256(payload).hexdigest()},sort_keys=True))


if __name__=='__main__':
    main()
