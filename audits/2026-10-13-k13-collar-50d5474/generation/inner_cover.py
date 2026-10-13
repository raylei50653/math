#!/usr/bin/env python3
"""A second exhaustive route: cone the inner C, enumerate min4 spheres on14.

No adjacency or chord pruning.  Every degree-compatible five-apex subset is
glued to the forced original B annulus and mapped to the min5 sphere source.
"""
from collections import Counter
from itertools import combinations
from pathlib import Path
import argparse
import json
import generate as g

HERE = Path(__file__).resolve().parent

def rotation_from_faces(n, fs):
    successors = [{} for _ in range(n)]
    for f in fs:
        for i,v in enumerate(f):
            u,w = f[i-1],f[(i+1)%len(f)]
            assert w not in successors[v]
            successors[v][w] = u
    out=[]
    for succ in successors:
        first=min(succ); row=[first]; nxt=succ[first]
        while nxt!=first:
            assert nxt not in row
            row.append(nxt); nxt=succ[nxt]
        assert len(row)==len(succ)
        out.append(row)
    assert sorted(g.faces(out))==sorted(_norm(f) for f in fs)
    return out

def _norm(f):
    p=f.index(min(f));return f[p:]+f[:p]

def complete(Hrot,C,A):
    hv=sorted(Hrot)
    to_new={v:i for i,v in enumerate(hv)}
    B=list(range(13,18));z=18
    fs=[[to_new[v] for v in f] for f in g.faces(Hrot) if len(f)==3]
    for i in range(5):
        fs.append([B[(i+1)%5],B[i],to_new[A[i]]])
        a=C.index(A[i-1]);b=C.index(A[i]);path=[]
        j=a
        while j!=b:
            path.append(C[j]);j=(j+1)%len(C)
        path.append(C[b])
        for u,v in zip(path,path[1:]):
            fs.append([B[i],to_new[u],to_new[v]])
        fs.append([z,B[i],B[(i+1)%5]])
    r=rotation_from_faces(19,fs)
    g.validate_sphere(r)
    return r,hv

def compositions(n,k):
    if k==1:
        yield (n,);return
    for x in range(n+1):
        for rest in compositions(n-x,k-1):yield (x,)+rest

def main():
    global HERE
    ap=argparse.ArgumentParser()
    ap.add_argument('--directory',type=Path,default=HERE)
    HERE=ap.parse_args().directory
    rr=g.parse_pc((HERE/'inner_spheres14.pc').read_bytes())
    prim=g.parse_pc((HERE/'spheres19.pc').read_bytes())
    keys=[g.canonical_embedding(r,True) for r in prim]
    bykey={k:(sid,order,sign) for sid,(k,order,sign) in enumerate(keys)}
    filters=[]; cores=[]
    for sid,r in enumerate(rr):
        assert len(r)==14 and min(map(len,r))>=4
        assert all(len(f)==3 for f in g.faces(r)) and len(g.edges(r))==36
        for q,ns in enumerate(r):
            if len(ns) not in (9,10,11,12):continue
            h=len(ns)-5; I=sorted(set(range(14))-set(ns)-{q})
            forced=sorted(v for v in ns if len(r[v])==4)
            lowI=[v for v in I if len(r[v])<5]
            record=dict(sphere_id=sid,q=q,h=h,rotation=r,
                        I=I,degree=list(map(len,r)),forced_apices=forced,
                        bad_interior_degree=lowI)
            record['status']='kept' if not lowI and len(forced)<=5 else 'degree_excluded'
            record['reason']=('strict interior degree below5' if lowI else
                'more than5 forced apices' if len(forced)>5 else 'holds')
            filters.append(record)
            if record['status']!='kept':continue
            hr={v:[w for w in r[v] if w!=q] for v in range(14) if v!=q}
            outs=[f for f in g.faces(hr) if len(f)!=3]
            assert len(outs)==1 and len(outs[0])==len(ns)
            C=outs[0]
            for positions in combinations(range(len(C)),5):
                A=[C[i] for i in positions]
                if not set(forced)<=set(A):continue
                R,hmap=complete(hr,C,A)
                key,order,sign=g.canonical_embedding(R,True)
                target,porder,psign=bykey[key]
                iso={order[i]:porder[i] for i in range(19)}
                assert {tuple(sorted((iso[u],iso[v]))) for u,v in g.edges(R)}==set(map(tuple,g.edges(prim[target])))
                targetz=iso[18];targetB=prim[target][targetz]
                mappedB=[iso[v] for v in range(13,18)]
                frame=next(dict(shift=s,direction=t) for t in (1,-1) for s in range(5)
                    if [targetB[(s+t*i)%5] for i in range(5)]==mappedB)
                e=[(positions[i]-positions[i-1]-1)%len(C) for i in range(5)]
                assert sum(e)==h
                ce={tuple(sorted((C[i],C[(i+1)%len(C)]))) for i in range(len(C))}
                chords=[edge for edge in g.edges(hr) if set(edge)<=set(C) and tuple(edge) not in ce]
                cores.append(dict(id=f'H{len(cores):03d}',sphere_id=sid,q=q,h=h,
                    C=C,apex=A,I=I,e=e,H_rotation=hr,H_edges=g.edges(hr),
                    H_faces=g.faces(hr),C_chords=chords,completed_rotation=R,
                    completed_to_H_original=hmap+[f'b{i}' for i in range(5)]+['z'],
                    target_sphere=target,target_z=targetz,target_source=f'S{target:03d}-z{targetz:02d}',
                    completed_to_target=iso,orientation=sign*psign,target_B_frame=frame))
    g.dump(HERE/'inner_filters.json',filters)
    g.dump(HERE/'inner_cores.json',cores)
    # Every named excess distribution, including every empty formal domain.
    config=[]
    for h in range(4,8):
        for e in compositions(h,5):
            orbit=[(tuple(e[(s+t*i)%5] for i in range(5)),s,t) for t in (1,-1) for s in range(5)]
            rep,s,t=min(orbit)
            placements=[]
            for core in cores:
                if core['h']!=h:continue
                for tt in (1,-1):
                    for ss in range(5):
                        if tuple(core['e'][(ss+tt*i)%5] for i in range(5))==e:
                            placements.append(dict(core=core['id'],shift=ss,direction=tt,
                                B_new_to_core=[(ss+tt*i)%5 for i in range(5)]))
            config.append(dict(h=h,e=e,representative=rep,
                representative_to_original_B=[(s+t*i)%5 for i in range(5)],
                shift=s,direction=t,core_placements=placements))
    g.dump(HERE/'named_configurations.json',config)
    primary_roots=json.loads((HERE/'rooted_sources.json').read_text())
    selected=[x for x in primary_roots if x['h'] in (4,5,6,7)]
    primary_root_keys={g.canonical_embedding(prim[x['sphere_id']],fixed_root=x['z']) for x in selected}
    inner_root_keys={g.canonical_embedding(x['completed_rotation'],fixed_root=18) for x in cores}
    assert primary_root_keys==inner_root_keys
    root_matching=[]
    for x in selected:
        key=g.canonical_embedding(prim[x['sphere_id']],fixed_root=x['z'])
        matches=[c['id'] for c in cores if g.canonical_embedding(c['completed_rotation'],fixed_root=18)==key]
        assert matches
        root_matching.append(dict(source=x['id'],inner_cores=matches))
    g.dump(HERE/'primary_to_inner.json',root_matching)
    summary=dict(inner_spheres=len(rr),raw_cone_roots=dict(sorted(Counter(x['h'] for x in filters).items())),
        degree_eligible_roots=dict(sorted(Counter(x['h'] for x in filters if x['status']=='kept').items())),
        apex_placement_cores=dict(sorted(Counter(x['h'] for x in cores).items())),
        named_configuration_counts={h:sum(x['h']==h for x in config) for h in range(4,8)},
        nonempty_named_configuration_counts={h:sum(x['h']==h and bool(x['core_placements']) for x in config) for h in range(4,8)},
        d5_orbit_counts={h:len({tuple(x['representative']) for x in config if x['h']==h}) for h in range(4,8)},
        all_cores_mapped_to_primary=True,
        primary_inner_rooted_embedding_sets_equal=True,
        rooted_embedded_isomorphism_classes=len(primary_root_keys))
    g.dump(HERE/'inner_summary.json',summary)
    print(json.dumps(summary,sort_keys=True))

if __name__=='__main__':main()
