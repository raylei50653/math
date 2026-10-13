#!/usr/bin/env python3
"""Exact independent-of-generator reconstruction and static-order full-lift replay.
No isomorphism pruning and no relation/degree/collar pruning of the 306 roots.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
P5 = ['01012','01021','01023','01201','01202','01203','01212','01213','01231','01232']


def need(test, message):
    if not test:
        raise ValueError(message)


def read_pc(path):
    data = path.read_bytes()
    header = b'>>planar_code<<'
    need(data.startswith(header), 'planar_code header')
    p = len(header)
    out = []
    while p < len(data):
        n = data[p]; p += 1
        need(n == 19, '19 sphere vertices')
        rot = []
        for _ in range(n):
            j = data.index(0, p)
            rot.append([v-1 for v in data[p:j]])
            p = j+1
        out.append(rot)
    return out


def cyclic(word):
    return min(tuple(word[i:]+word[:i]) for i in range(len(word)))


def get_faces(rot):
    darts = {(u,v) for u,row in enumerate(rot) for v in row}
    need(all(u in rot[v] for u,v in darts), 'symmetric rotation')
    need(all(len(set(row)) == len(row) and u not in row for u,row in enumerate(rot)), 'simple graph')
    todo = set(darts)
    ans = []
    while todo:
        start = min(todo); u,v = start; face = []
        while True:
            need((u,v) in todo, 'closed directed face without reused dart')
            todo.remove((u,v)); face.append(u)
            u,v = v,rot[v][(rot[v].index(u)+1) % len(rot[v])]
            if (u,v) == start:
                break
        ans.append(list(cyclic(face)))
    need(sum(map(len,ans)) == len(darts), 'all darts covered')
    return sorted(ans)


def edges(rot):
    return [[u,v] for u,row in enumerate(rot) for v in row if u < v]


def norm(word):
    names = {}; ans=[]
    for c in word:
        if c not in names:
            names[c]=len(names)
        ans.append(names[c])
    return ''.join(map(str,ans))


def all_lifts(n, ee, pinword):
    """Every coloring exactly once, fixed vertex order and all four literal colors."""
    adj = [set() for _ in range(n)]
    for u,v in ee:
        adj[u].add(v); adj[v].add(u)
    a = list(map(int,pinword)) + [-1]*(n-5)
    if any(a[u] == a[v] and a[u] >= 0 for u,v in ee):
        return []
    order = sorted(range(5,n),key=lambda v:(-len(adj[v]),v))
    lifts=[]
    def visit(t):
        if t == len(order):
            lifts.append(''.join(map(str,a))); return
        v=order[t]; forbidden={a[w] for w in adj[v] if a[w]>=0}
        for c in range(4):
            if c not in forbidden:
                a[v]=c; visit(t+1)
        a[v]=-1
    visit(0)
    return sorted(lifts)


def rows(n,ee):
    return [dict(pattern=p,count=len(fs),lifts=fs) for p in P5 for fs in [all_lifts(n,ee,p)]]


def relation(rs):
    return sum(1<<i for i,r in enumerate(rs) if r['count'])


def frame_data(rs,mapping):
    frames=[]
    for sign in (1,-1):
        for start in range(5):
            new_to_base=[(start+sign*i)%5 for i in range(5)]+list(range(5,18))
            perm=[]
            for p in P5:
                old=[None]*5
                for i,v in enumerate(new_to_base[:5]): old[v]=p[i]
                perm.append(P5.index(norm(old)))
            counts=[rs[j]['count'] for j in perm]
            frames.append(dict(start=start,sign=sign,new_to_base=new_to_base,
                canonical_to_original=[mapping[v] for v in new_to_base],
                row_new_to_base=perm,counts=counts,mask=sum(1<<i for i,c in enumerate(counts) if c)))
    return frames


def core(rot,sid,z):
    need(len(rot[z])==5, 'degree5 root')
    mapping=rot[z]+sorted(set(range(19))-set(rot[z])-{z})
    inv={v:i for i,v in enumerate(mapping)}
    rr=[[inv[v] for v in rot[u] if v!=z] for u in mapping]
    ee=edges(rr); ff=get_faces(rr); deg=list(map(len,rr))
    need(len(ee)==46 and len(ff)==30 and 18-len(ee)+len(ff)==2,'G Euler')
    outer=[f for f in ff if len(f)!=3]
    # Our successor-dart convention walks the deleted-root face opposite to
    # the stored clockwise rotation at z. This is one global orientation.
    need(outer==[list(cyclic(list(range(4,-1,-1))))], 'specified ordered B is outer face')
    need(all(deg[i]>=4 for i in range(5)) and all(d>=5 for d in deg[5:]),'complete degrees')
    need(all(v-u in (1,4) for u,v in ee if v<5),'B chordless')
    e=[deg[v]-4 for v in range(5)]; h=sum(e)
    n5=sum(d==5 for d in deg[5:]); high=sum(max(0,d-6) for d in deg[5:])
    need(n5==6+h+high,'original Euler curvature')
    Hedges=[[u,v] for u,v in ee if u>=5]
    need(len(Hedges)==31-h,'H edge budget')
    attachments={v:[b for b in range(5) if b in rr[v]] for v in range(5,18)}
    apex=[]
    for i in range(5):
        matches=[v for v in range(5,18) if attachments[v]==sorted([i,(i+1)%5])]
        need(len(matches)==1,'unique original edge apex'); apex+=matches
    y=[]
    for i in range(5):
        a,b=apex[(i-1)%5],apex[i]
        seqs=[]
        for direction in (1,-1):
            ix=rr[i].index(a); seq=[]
            for t in range(1,e[i]+1): seq.append(rr[i][(ix+direction*t)%deg[i]])
            end=rr[i][(ix+direction*(e[i]+1))%deg[i]]
            if end==b and all(attachments.get(v)==[i] for v in seq): seqs.append(seq)
        need(len(seqs)==1,'original rotation fixes y order'); y+=seqs
    C=[]
    for i in range(5): C += [apex[i]]+y[(i+1)%5]
    need(len(C)==len(set(C))==5+h,'simple original collar')
    I=sorted(set(range(5,18))-set(C))
    need(all(attachments[v]==[] for v in I),'strict interior has no B attachment')
    cc={tuple(sorted((C[i],C[(i+1)%len(C)]))) for i in range(len(C))}
    chords=[uv for uv in Hedges if set(uv)<=set(C) and tuple(uv) not in cc]
    hrot=[[v-5 for v in rr[u] if v>=5] for u in range(5,18)]
    hfaces=get_faces(hrot)
    hc=[list(cyclic([v-5 for v in C])),list(cyclic([v-5 for v in C[::-1]]))]
    need([f for f in hfaces if len(f)!=3][0] in hc,'specified C bounds H')
    need(sum(len(f)!=3 for f in hfaces)==1,'only H outer face nontriangular')
    Hdeg=list(map(len,hrot))
    need(all(Hdeg[a-5]>=3 for a in apex),'apex H-degree')
    need(all(Hdeg[v-5]>=4 for ys in y for v in ys),'private H-degree')
    need(all(Hdeg[v-5]>=5 for v in I),'strict H-degree')
    rs=rows(18,ee)
    return dict(id=f's{sid:02d}-z{z:02d}',sphere=sid,root=z,canonical_to_original=mapping,
        B=list(range(5)),edges=ee,rotation=rr,faces=ff,outer_face=outer[0],degree=deg,
        e=e,h=h,n5=n5,apex=apex,y=y,C=C,I=I,H_edges=Hedges,H_degree=Hdeg,
        H_rotation=hrot,H_faces=hfaces,C_chords=chords,attachments={str(v):a for v,a in attachments.items()},
        rows=rs,mask=relation(rs),frames=frame_data(rs,mapping))


def encode(obj):
    return (json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n').encode()


def store_or_check(path,obj,write):
    b=encode(obj)
    if write:
        path.parent.mkdir(parents=True,exist_ok=True)
        with path.open('xb') as f: f.write(gzip.compress(b,mtime=0) if path.suffix=='.gz' else b)
    else:
        actual=gzip.decompress(path.read_bytes()) if path.suffix=='.gz' else path.read_bytes()
        need(actual==b,'certificate mismatch: '+str(path))
    return hashlib.sha256(b).hexdigest()


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--write',action='store_true'); ap.add_argument('--check',action='store_true')
    args=ap.parse_args(); need(args.write!=args.check,'choose --write or --check')
    manifest=json.loads((HERE/'INPUTS.json').read_text())
    for p,d in manifest['sha256'].items():
        need(hashlib.sha256((HERE/'frozen'/p).read_bytes()).hexdigest()==d,'frozen hash '+p)
    catalogue=json.loads((HERE/'frozen/artifacts/c5_cells/cells.json').read_text())
    need(catalogue['pattern_order']==[list(map(int,p)) for p in P5],'ten-row order')
    K=set(map(int,catalogue['cells'])); need(len(K)==132,'K132')
    rotations=read_pc(HERE/'generation/spheres19.pc')
    allcores=[]; hashes={}
    for sid,rot in enumerate(rotations):
        sf=get_faces(rot); se=edges(rot)
        need(len(rot)==19 and len(se)==51 and len(sf)==34 and all(len(f)==3 for f in sf),'sphere Euler triangulation')
        need(min(map(len,rot))>=5,'sphere min degree5')
        cs=[core(rot,sid,z) for z in range(19) if len(rot[z])==5]
        for c in cs:
            need(c['mask'] in K,'outside catalogue source '+c['id'])
            need(all(f['mask'] in K for f in c['frames']),'D5 transported K membership')
        hashes[f'cores/sphere-{sid:02d}.json.gz']=store_or_check(HERE/f'cores/sphere-{sid:02d}.json.gz',cs,args.write)
        allcores+=cs
    calibration=[]
    for name,n,ee in [('C5',5,[[i,(i+1)%5] for i in range(5)]),
        ('C5-chord02',5,[[i,(i+1)%5] for i in range(5)]+[[0,2]]),
        ('wheel5',6,[[i,(i+1)%5] for i in range(5)]+[[i,5] for i in range(5)])]:
        rr=rows(n,ee);calibration.append(dict(id=name,n=n,edges=ee,rows=rr,mask=relation(rr)))
    need(any(r['count']==0 for c in calibration for r in c['rows']),'empty fibre control triggered')
    hashes['calibration.json']=store_or_check(HERE/'calibration.json',calibration,args.write)
    summary=dict(base=manifest['base'],pattern_order=P5,spheres=len(rotations),roots=len(allcores),
        h_counts=dict(sorted(Counter(c['h'] for c in allcores).items())),
        relation_counts=dict(sorted(Counter(c['mask'] for c in allcores).items())),
        full_lifts=sum(r['count'] for c in allcores for r in c['rows']),
        framed_roots=10*len(allcores),accepted_rows=sum(bool(r['count']) for c in allcores for r in c['rows']),
        rejected_rows=sum(not r['count'] for c in allcores for r in c['rows']),
        core_uncompressed_sha256=hashes,
        h4_to_h7={str(h):dict(roots=sum(c['h']==h for c in allcores),
            chord_counts=dict(sorted(Counter(len(c['C_chords']) for c in allcores if c['h']==h).items())),
            ids=[c['id'] for c in allcores if c['h']==h]) for h in range(4,8)})
    store_or_check(HERE/'RESULTS.json',summary,args.write)
    print(json.dumps({k:v for k,v in summary.items() if k not in ('core_uncompressed_sha256','h4_to_h7')},sort_keys=True))

if __name__=='__main__':main()
