#!/usr/bin/env python3
"""Independent K13 replay: planar-code, dart topology, propagated-domain CSP.

Imports no generating/main-checker module. All colourings for all ten fixed
boundary words are enumerated, including explicit empty fibres. Only files
under independent/ are written, using exclusive creation unless --check.
"""
from __future__ import annotations
import argparse
from collections import Counter
from copy import deepcopy
import gzip
import hashlib
import itertools
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
WORDS=['01012','01021','01023','01201','01202','01203','01212','01213','01231','01232']

def norm(word):
    names={}
    return ''.join(str(names.setdefault(c,len(names))) for c in word)

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def encode(obj):
    return json.dumps(obj,sort_keys=True,separators=(',',':')).encode()

def planar_code(path):
    data=Path(path).read_bytes(); header=b'>>planar_code<<'
    assert data.startswith(header), 'planar_code header'
    at=len(header); answer=[]
    while at<len(data):
        n=data[at]; at+=1
        assert 1<=n<256, 'only one-byte planar_code supported'
        adj={}
        for u in range(n):
            row=[]
            while True:
                assert at<len(data), 'truncated planar_code'
                x=data[at];at+=1
                if not x:break
                row.append(x-1)
            adj[u]=row
        answer.append(adj)
    return answer

def edges(adj):
    return sorted([u,v] for u in adj for v in adj[u] if u<v)

def cycle_key(c):
    c=tuple(c)
    return min(c[i:]+c[:i] for i in range(len(c)))

def faces(adj):
    for u,row in adj.items():
        assert u not in row and len(row)==len(set(row)), 'simple rotation'
        assert all(v in adj and u in adj[v] for v in row), 'reciprocal rotation'
    todo={(u,v) for u in adj for v in adj[u]}; fs=[]
    while todo:
        first=min(todo); dart=first; face=[]
        while True:
            assert dart in todo, 'face permutation closes at wrong dart'
            todo.remove(dart);u,v=dart;face.append(u)
            dart=(v,adj[v][(adj[v].index(u)+1)%len(adj[v])])
            if dart==first:break
        assert len(set(face))==len(face), 'non-simple face'
        fs.append(face)
    # Connectedness and orientable genus zero follow separately.
    seen={next(iter(adj))}; stack=list(seen)
    while stack:
        for v in adj[stack.pop()]:
            if v not in seen:seen.add(v);stack.append(v)
    assert len(seen)==len(adj), 'disconnected embedding'
    assert len(adj)-len(edges(adj))+len(fs)==2, 'rotation has nonzero genus'
    return sorted(fs,key=cycle_key)

def verify_disk(adj,B,z,sphere):
    assert B==sphere[z], 'wrong original B labels'
    expected={u:[v for v in ns if v!=z] for u,ns in sphere.items() if u!=z}
    assert adj==expected, 'disk edges or rotation differ from literal root deletion'
    fs=faces(adj)
    outer=[f for f in fs if len(f)==5]
    assert len(outer)==1 and all(len(f) in (3,5) for f in fs), 'wrong outer face'
    assert cycle_key(B) in (cycle_key(outer[0]),cycle_key(outer[0][::-1])), 'B is not specified outer face'
    assert len(adj)==18 and len(edges(adj))==46, 'disk Euler dimensions'
    assert all(len(adj[b])>=4 for b in B), 'B degree bound'
    assert all(len(adj[v])>=5 for v in adj if v not in B), 'inner degree bound'
    return fs

def collar(adj,B,fs):
    bset=set(B); inside=set(adj)-bset
    attach={v:[i for i,b in enumerate(B) if b in adj[v]] for v in sorted(inside)}
    h=sum(len(adj[b])-4 for b in B)
    # This predicate uses only the prior collar theorem, with no pruning before colouring.
    if any(len(ns)>2 or (len(ns)==2 and (ns[1]-ns[0])%5 not in (1,4)) for ns in attach.values()):
        return {'valid':False,'h':h,'reason':'nonadjacent B attachments'}
    apex=[]
    for i,b in enumerate(B):
        nxt=B[(i+1)%5]
        third=[next(v for v in f if v not in (b,nxt)) for f in fs if len(f)==3 and b in f and nxt in f]
        if len(third)!=1:return {'valid':False,'h':h,'reason':'boundary edge face not unique'}
        apex.append(third[0])
    Cset={v for v in inside if attach[v]}
    innerfaces=[f for f in fs if not set(f)&bset]
    edgecounts=Counter(tuple(sorted((f[i],f[(i+1)%3]))) for f in innerfaces for i in range(3))
    boundary=[e for e,count in edgecounts.items() if count==1]
    gadj={v:[] for v in Cset}
    for u,v in boundary:
        if u not in Cset or v not in Cset:return {'valid':False,'h':h,'reason':'collar boundary mismatch'}
        gadj[u].append(v);gadj[v].append(u)
    if len(Cset)!=5+h or any(len(ns)!=2 for ns in gadj.values()):
        return {'valid':False,'h':h,'reason':'collar not simple expected cycle'}
    C=[apex[0]];prev=None
    while True:
        nxt=next(v for v in sorted(gadj[C[-1]]) if v!=prev)
        if nxt==C[0]:break
        if nxt in C:return {'valid':False,'h':h,'reason':'collar disconnected'}
        prev,C=C[-1],C+[nxt]
    if len(C)!=len(Cset):return {'valid':False,'h':h,'reason':'collar disconnected'}
    H={v:[w for w in adj[v] if w in inside] for v in sorted(inside)}
    ce={tuple(sorted((C[i],C[(i+1)%len(C)]))) for i in range(len(C))}
    chords=[e for e in edges(H) if set(e)<=Cset and tuple(e) not in ce]
    Y=sorted(Cset-set(apex));I=sorted(inside-Cset)
    assert len(H)==13 and len(edges(H))==31-h, 'H Euler dimensions'
    assert all(len(H[v])>=3 and len(attach[v])==2 for v in apex), 'apex degree/attachment'
    assert all(len(H[v])>=4 and len(attach[v])==1 for v in Y), 'Y degree/attachment'
    assert all(len(H[v])>=5 and not attach[v] for v in I), 'strict interior degree/attachment'
    return {'valid':True,'h':h,'e':[len(adj[b])-4 for b in B], 'C':C,'apex':apex,'y':Y,'I':I,'chords':chords,'H_edges':edges(H),'attachments':{str(v):attach[v] for v in sorted(Cset)}}

def colourings(adj,B,word):
    verts=sorted(adj); pos={v:i for i,v in enumerate(verts)}
    neighbors=[[pos[v] for v in adj[u]] for u in verts]
    domains=[15]*len(verts)
    for b,c in zip(B,word):domains[pos[b]]=1<<int(c)
    answer=[];nodes=0
    def search(dom):
        nonlocal nodes
        nodes+=1
        # Unit propagation reaches a fixed point, detecting even fixed-fixed conflicts.
        todo=[i for i,d in enumerate(dom) if d.bit_count()==1];done=set()
        while todo:
            u=todo.pop()
            if u in done:continue
            done.add(u);bit=dom[u]
            for v in neighbors[u]:
                if dom[v]&bit:
                    if dom[v]==bit:return
                    dom[v]^=bit
                    if dom[v].bit_count()==1:todo.append(v)
        unassigned=[i for i,d in enumerate(dom) if d.bit_count()>1]
        if not unassigned:
            answer.append(''.join(str(d.bit_length()-1) for d in dom));return
        u=min(unassigned,key=lambda i:(dom[i].bit_count(),-len(neighbors[i]),i))
        choices=dom[u]
        while choices:
            bit=choices&-choices;choices-=bit
            child=dom.copy();child[u]=bit;search(child)
    search(domains)
    return sorted(answer),nodes

def d5_relation(B,rows):
    frames=[]
    for direction in (1,-1):
        for shift in range(5):
            indices=[(shift+direction*i)%5 for i in range(5)]
            transported=[0]*10
            for w,row in zip(WORDS,rows):transported[WORDS.index(norm([w[i] for i in indices]))]=row['count']
            frames.append({'shift':shift,'direction':direction,'B':[B[i] for i in indices], 'counts':transported,'mask':sum(1<<i for i,n in enumerate(transported) if n)})
    return frames

def calculate():
    spheres=planar_code(AUDIT/'generation/spheres19.pc')
    cat=AUDIT/'frozen/artifacts/c5_cells/cells.json'
    known=set(map(int,json.loads(cat.read_text())['cells']))
    assert len(known)==132,'K132 cardinality'
    records=[];counts=Counter();total_lifts=0
    for sid,sphere in enumerate(spheres):
        sf=faces(sphere)
        assert len(sphere)==19 and len(edges(sphere))==51 and len(sf)==34 and all(len(f)==3 for f in sf), 'sphere dimensions'
        assert min(map(len,sphere.values()))>=5,'sphere minimum degree'
        for z in sorted(sphere):
            if len(sphere[z])!=5:continue
            B=sphere[z].copy();adj={u:[v for v in ns if v!=z] for u,ns in sphere.items() if u!=z}
            fs=verify_disk(adj,B,z,sphere);rows=[]
            for word in WORDS:
                lifts,nodes=colourings(adj,B,word)
                rows.append({'word':word,'count':len(lifts),'lifts':lifts,'search_nodes':nodes})
                total_lifts+=len(lifts)
            mask=sum(1<<i for i,row in enumerate(rows) if row['count'])
            frames=d5_relation(B,rows)
            assert mask in known and all(f['mask'] in known for f in frames),'catalogue-outside actual graph'
            col=collar(adj,B,fs)
            record={'id':f'S{sid:03d}-z{z:02d}','sphere_id':f'S{sid:03d}','z':z,'B':B,'vertices':sorted(adj),'rotation':{str(u):adj[u] for u in sorted(adj)},'edges':edges(adj),'faces':fs,'degree':{str(u):len(adj[u]) for u in sorted(adj)},'collar':col,'mask':mask,'rows':rows,'d5_frames':frames}
            records.append(record);counts[str(col['h'])]+=1
    return {'schema':'independent-propagated-csp-v1','planar_code_sha256':sha(AUDIT/'generation/spheres19.pc'),'catalogue_sha256':sha(cat),'words':WORDS,'spheres':len(spheres),'rooted_disks':len(records),'all_roots_h':dict(sorted(counts.items())),'total_full_lifts':total_lifts,'records':records}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',default='relations.json.gz');args=ap.parse_args()
    result=calculate();data=encode(result);path=HERE/args.output
    if args.check:
        assert gzip.decompress(path.read_bytes())==data,'independent replay differs'
    else:
        with path.open('xb') as stream:stream.write(gzip.compress(data,mtime=0))
    print(json.dumps({k:v for k,v in result.items() if k!='records'},sort_keys=True))
    print('PASS independent complete topology/relations; mathematical payload SHA256',hashlib.sha256(data).hexdigest())

if __name__=='__main__':main()
