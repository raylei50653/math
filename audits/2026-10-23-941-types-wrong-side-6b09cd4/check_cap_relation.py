#!/usr/bin/env python3
"""Read-only independent complete C6 relations and bounded cap controls."""
import argparse
from copy import deepcopy
from hashlib import sha256
from itertools import combinations,product
import json
from pathlib import Path
import random
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

def require(ok,why):
    if not ok: raise ValueError(why)

def norm(w):
    d={}
    return tuple(d.setdefault(c,len(d)) for c in w)

def crossing(a,b):
    i,j=sorted(a); k,l=sorted(b)
    return len({i,j,k,l})==4 and ((i<k<j<l) or (k<i<l<j))

def reconstruct(cert,seed):
    path=cert['input_path'];raw=(HERE/cert.get('input_snapshot','entry/'+path)).read_bytes()
    require(sha256(raw).hexdigest()==cert['input_sha256'],'cap input hash')
    require((ROOT/path).read_bytes()==raw,'live named cap drift')
    caps=json.loads(raw)['caps']
    words=sorted({norm(w) for w in product(range(4),repeat=6) if all(w[i]!=w[(i+1)%6] for i in range(6))})
    require(len(words)==31,'complete six-frame domain')
    got=[]
    for cap in caps:
        inner=cap['ordered_inner'];boundary=cap['ordered_boundary']
        ie=[(inner.index(a),inner.index(b)) for a,b in cap['edges'] if a in inner and b in inner]
        cross=[(inner.index(a),boundary.index(b)) if a in inner else (inner.index(b),boundary.index(a)) for a,b in cap['edges'] if (a in inner)!=(b in inner)]
        candidates=[t for t in product(range(4),repeat=7) if all(t[i]!=t[j] for i,j in ie)]
        require(len(candidates)==264,'internal assignment coverage')
        for w in words:
            lifts=sorted([list(t) for t in candidates if all(t[i]!=w[j] for i,j in cross)])
            got.append(dict(core=cap['core'],ordered_boundary=boundary,word=list(w),ordered_inner=inner,complete_lifts=lifts))
    expected=deepcopy(cert['relations']);random.Random(seed).shuffle(expected)
    require(sorted(got,key=lambda r:(r['core'],r['word']))==sorted(expected,key=lambda r:(r['core'],r['word'])),'complete fibres/full lifts drift')
    for core in ('L','R'):
        rows=[r for r in got if r['core']==core]
        require(sum(bool(r['complete_lifts']) for r in rows)==19,'nonempty fibre count')
        require(sum(len(r['complete_lifts']) for r in rows)==52,'complete lift count')
    old={tuple(r['word']) for r in got if r['core']=='L' and r['complete_lifts']}
    require(old=={tuple(r['word']) for r in got if r['core']=='R' and r['complete_lifts']},'ordered L/R relation inequality')
    # An independent triangulation reconstruction from maximal noncrossing chords.
    boundary_edges={tuple(sorted((i,(i+1)%6))) for i in range(6)}
    diagonals=[e for e in combinations(range(6),2) if e not in boundary_edges]
    tris=[t for t in combinations(diagonals,3) if all(not crossing(a,b) for a,b in combinations(t,2))]
    require(len(tris)==14,'all empty hexagon triangulations')
    safe=[];unsafe=[]
    for t in tris:
        rel={w for w in words if all(w[i]!=w[j] for i,j in t)}
        (safe if rel<=old else unsafe).append(dict(diagonals=[list(e) for e in t],leak=[list(w) for w in sorted(rel-old)]))
    require(len(safe)==2 and len(unsafe)==12,'bounded empty-cap controls')
    alternating=(0,1,0,1,0,1)
    require(alternating in old and all(any(alternating[i]==alternating[j] for i,j in t) for t in tris),'empty caps lose alternating accepted fibre')
    wheel={w for w in words if len(set(w))<4}
    require(bool(wheel-old),'single-wheel leakage control')
    two_hub=[]
    for i in range(3):
        j=i+3;quads=[[(i+k)%6 for k in range(4)],[(j+k)%6 for k in range(4)]]
        rel={w for w in words if w[i]!=w[j] and all(len({w[k] for k in q})<4 for q in quads)}
        require(len(rel-old)==4,'two-wheel leakage coverage')
        two_hub.append(dict(diameter=[i,j],leak=[list(w) for w in sorted(rel-old)]))
    return dict(status='PASS',seed=seed,normalized_ordered_words=31,nonempty_each=19,empty_each=12,complete_lifts_each=52,empty_caps_safe=safe,empty_caps_unsafe_count=12,wheel_leak=[list(w) for w in sorted(wheel-old)],two_hub_leaks=two_hub,source_realizability='not triggered',replacement='not established',original_caps='only new named K6 cap independently recomputed; upstream complete fibres/lifts retained')

def main():
    p=argparse.ArgumentParser();p.add_argument('--seed',type=int,default=0);p.add_argument('--negative',action='store_true');p.add_argument('--certificate',type=Path,default=HERE/'CAP_RELATION-v2.json');args=p.parse_args()
    c=json.loads(args.certificate.read_text())
    require(c['schema']=='941-k6-independent-complete-relation-v1','schema')
    result=reconstruct(c,args.seed)
    if args.negative:
        names=[]
        for name,mutate in [('delete_empty_fibre',lambda x:x['relations'].pop(3)),('delete_full_lift',lambda x:x['relations'][0]['complete_lifts'].pop()),('wrong_boundary_order',lambda x:x['relations'][0]['ordered_boundary'].reverse()),('input_hash',lambda x:x.update(input_sha256='0'*64))]:
            bad=deepcopy(c);mutate(bad)
            try: reconstruct(bad,args.seed)
            except (ValueError,KeyError,IndexError):names.append(name)
            else:raise ValueError('accepted negative '+name)
        result=dict(status='PASS',seed=args.seed,negative_controls_rejected=names,source_realizability='not triggered')
    print(json.dumps(result,sort_keys=True))
if __name__=='__main__':
    try:main()
    except Exception as e:
        print(json.dumps(dict(status='FAIL',reason=str(e)),sort_keys=True));raise SystemExit(1)
