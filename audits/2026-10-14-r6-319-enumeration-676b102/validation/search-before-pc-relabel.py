#!/usr/bin/env python3
"""Original-label replay, seven-pin full-lift search, and exact receipts.

No graph-generation claim is made by this module. FILTER coverage is checked
against unfiltered planar_code, separately from coloring certificates.
"""
import argparse
from collections import Counter
import gzip
import hashlib
from itertools import product
import json
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent.parent
WORDS = ('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
PQ = ('12 21','12 21 23 32','12 13 21 23 31 32','12 21 23 32',
      '12 21','12 13 21 23 31 32','','','23 32','')
LABELS = ('spheres','roots5','frames_degree444','induced_boundary','unique_apices',
          'apex_degrees','boundary_excess','apex_skeleton','r_fan','seven_pin_edges','emitted_spheres')

def seal():
    manifest = json.loads((HERE/'INPUTS.json').read_text())
    for item in manifest['inputs']:
        assert hashlib.sha256((HERE/'frozen'/item['path']).read_bytes()).hexdigest() == item['sha256'], item['path']
    return hashlib.sha256((HERE/'INPUTS.json').read_bytes()).hexdigest()

def read_pc(path):
    data = Path(path).read_bytes()
    head = b'>>planar_code<<'
    assert data.startswith(head)
    pos = len(head)
    while pos < len(data):
        n = data[pos]; pos += 1
        assert 0 < n < 64
        rot = []
        for _ in range(n):
            end = data.index(0,pos)
            rot.append([v-1 for v in data[pos:end]])
            pos = end+1
        yield rot

def topology(rot):
    n = len(rot)
    darts = {(u,v) for u,ns in enumerate(rot) for v in ns}
    assert len(darts) == sum(map(len,rot))
    assert all(u != v and (v,u) in darts for u,v in darts)
    todo = set(darts); faces = []
    while todo:
        first = next(iter(todo)); e = first; f=[]
        while True:
            assert e in todo
            todo.remove(e); u,v=e; f.append(u)
            e=(v,rot[v][(rot[v].index(u)+1)%len(rot[v])])
            if e == first: break
        assert len(set(f)) == len(f) == 3
        faces.append(f)
    assert n-len(darts)//2+len(faces)==2
    seen={0}; pending=[0]
    while pending:
        for v in rot[pending.pop()]:
            if v not in seen: seen.add(v);pending.append(v)
    assert len(seen)==n

def frames(rot, counts=None):
    """Independent set/face reconstruction of the output-only C filter."""
    if counts is None: counts=Counter()
    counts['spheres']+=1
    adj=list(map(set,rot)); deg=list(map(len,rot)); result=[]
    for u,nb in enumerate(rot):
        if deg[u]!=5: continue
        counts['roots5']+=1
        for sign in (-1,1):
            for start in range(5):
                B=[nb[(start+sign*i)%5] for i in range(5)]
                x,y,a,b,c=B
                if [deg[x],deg[y],deg[b]] != [5,5,5]: continue
                counts['frames_degree444']+=1
                if any(adj[B[i]]&set(B) != {B[(i-1)%5],B[(i+1)%5]} for i in range(5)): continue
                counts['induced_boundary']+=1
                corners=[(adj[B[i]]&adj[B[(i+1)%5]])-set(B)-{u} for i in range(5)]
                if any(len(vs)!=1 for vs in corners):continue
                A=[next(iter(vs)) for vs in corners]
                if len(set(A))!=5 or any(adj[A[i]]&set(B)!={B[i],B[(i+1)%5]} for i in range(5)):continue
                counts['unique_apices']+=1
                r,t,p,q,s=A
                if deg[r]!=6 or min(deg[s],deg[t])<6:continue
                counts['apex_degrees']+=1
                if sum(deg[v]-5 for v in B)<3:continue
                counts['boundary_excess']+=1
                required={frozenset(e) for e in [(r,s),(r,t),(p,q)]}
                if deg[a]==5:required.add(frozenset((t,p)))
                if deg[c]==5:required.add(frozenset((s,q)))
                actual={frozenset((i,j)) for i in A for j in A if j in adj[i]}
                if actual!=required or (p in adj[t] and q in adj[s]):continue
                counts['apex_skeleton']+=1
                fan=None
                for direction in (1,-1):
                    rr=[rot[r][(rot[r].index(x)+direction*i)%6] for i in range(6)]
                    if rr[:3]==[x,y,t] and rr[-1]==s:fan=rr
                if fan is None:continue
                w,v=fan[3:5]
                if {w,v}&(set(B)|{p,q}):continue
                counts['r_fan']+=1
                frame={'root':u,'B':B,'apices':A,'v':v,'w':w}
                _,ua=make_u(rot,frame)
                mandatory={(0,1),(1,2),(2,3),(3,4),(0,4),(0,5),(0,6),(5,6)}
                actual={(i,j) for i in range(7) for j in range(i+1,7) if j in ua[i]}
                if not mandatory <= actual <= mandatory|{(4,5),(1,6)}:continue
                counts['seven_pin_edges']+=1;result.append(frame)
    if result:counts['emitted_spheres']+=1
    return result

def make_u(rot,f):
    x,y,a,b,c=f['B'];r,t,p,q,s=f['apices'];u=f['root']
    removed={u,x,y,b,r}
    pins=[a,s,f['v'],f['w'],t,p,q]
    assert len(set(pins))==7 and not set(pins)&removed
    original=pins+sorted(set(range(len(rot)))-removed-{c}-set(pins))
    index={v:i for i,v in enumerate(original)};index[c]=0
    adj=[set() for _ in original]
    for i,nb in enumerate(rot):
        if i in removed:continue
        for j in nb:
            if j in removed:continue
            assert index[i]!=index[j], 'loop in a=c quotient'
            adj[index[i]].add(index[j])
    return original,adj

def solve(adj,fixed,all_lifts=False):
    """MRV with propagated domains, exact integer bit sets, no timeout-as-UNSAT."""
    n=len(adj); domains=[15]*n; colors=[-1]*n; solutions=[]
    for v,col in enumerate(fixed):
        if not (domains[v]>>col&1):return []
        colors[v]=col;domains[v]=1<<col
        for w in adj[v]:
            if colors[w]==col:return []
            if colors[w]<0:
                domains[w]&=~(1<<col)
                if not domains[w]:return []
    def visit(left):
        if not left:
            solutions.append(''.join(map(str,colors)))
            return not all_lifts
        v=min(left,key=lambda w:(domains[w].bit_count(),-len(adj[w]),w))
        rest=left-{v}; available=domains[v]
        while available:
            bit=available&-available;available-=bit
            colors[v]=bit.bit_length()-1;changed=[];valid=True
            for w in adj[v]:
                if colors[w]<0 and domains[w]&bit:
                    changed.append((w,domains[w]));domains[w]&=~bit
                    if not domains[w]:valid=False;break
            stop=valid and visit(rest)
            for w,d in changed:domains[w]=d
            colors[v]=-1
            if stop:return True
        return False
    visit(set(range(len(fixed),n)))
    return solutions

def proper(adj,lift):
    return len(lift)==len(adj) and set(lift)<={'0','1','2','3'} and all(lift[u]!=lift[v] for u,ns in enumerate(adj) for v in ns)

def classify(adj):
    queries=0
    # Existence in any forbidden outer fibre already refutes the source contract.
    for i in (6,7,9):
        queries+=1;full=solve(adj,list(map(int,WORDS[i])))
        if full:return {'outcome':'forbidden_outer','row':i,'lift':full[0],'queries':queries}
    for i in (0,1,2,3,4,5,8):
        for p,q in product(range(1,4),repeat=2):
            if p==q or f'{p}{q}' in PQ[i].split():continue
            queries+=1;full=solve(adj,list(map(int,WORDS[i]))+[p,q])
            if full:return {'outcome':'forbidden_joint','row':i,'lift':full[0],'queries':queries}
    # Only residuals require all complete fibres, including the empty ones.
    fibres={}
    for i,word in enumerate(WORDS):
        for pq in PQ[i].split():
            queries+=1;fibres[word+pq]=solve(adj,list(map(int,word+pq)),all_lifts=True)
    mask=sum(1<<i for i,w in enumerate(WORDS) if any(fibres.get(w+pq) for pq in PQ[i].split()))
    return {'outcome':'joint_residual' if mask==319 else 'missing_required_outer',
            'mask':mask,'fibres':fibres,'queries':queries}

def open_read(path):
    path=Path(path)
    return gzip.open(path,'rt') if path.suffix=='.gz' else path.open()

def audit(input_path,output):
    start=time.monotonic();counts=Counter();seal_sha=seal()
    with open_read(input_path) as inp, gzip.open(output,'xt') as out:
        for line in inp:
            rec=json.loads(line);rot=rec['rotation'];topology(rot)
            # The independent filter also validates all supplied frames and their coverage on this sphere.
            assert rec['frames']==frames(rot), 'frame disagreement'
            results=[]
            for f in rec['frames']:
                order,adj=make_u(rot,f);res=classify(adj)
                if 'lift' in res:assert proper(adj,res['lift'])
                counts[res['outcome']]+=1;counts['queries']+=res['queries'];counts['frames']+=1
                results.append({'frame':f,'u_original_order':order,**res})
            counts['spheres']+=1
            out.write(json.dumps({'sphere':rec['sphere'],'results':results},separators=(',',':'))+'\n')
    summary={'input':str(input_path),'output':str(output),'input_seal_sha256':seal_sha,
             'counts':dict(counts),'elapsed':time.monotonic()-start}
    Path(str(output)+'.summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary),flush=True)

def coverage(raw,filtered,receipt):
    counts=Counter();expected=[]
    for sid,rot in enumerate(read_pc(raw)):
        topology(rot);fs=frames(rot,counts)
        if fs:expected.append({'sphere':sid,'rotation':rot,'frames':fs})
    with open_read(filtered) as stream:actual=[json.loads(line) for line in stream]
    assert actual==expected, 'raw/filter coverage mismatch'
    log=json.loads(Path(receipt).read_text())
    c=json.loads(next(line.removeprefix('R6_COUNTS ') for line in log['stderr'].splitlines() if line.startswith('R6_COUNTS ')))
    assert c=={key:counts[key] for key in LABELS}, (c,counts)
    print(json.dumps({'status':'PASS complete raw/filter comparison','counts':c}),flush=True)

def main():
    p=argparse.ArgumentParser();sub=p.add_subparsers(dest='mode',required=True)
    a=sub.add_parser('audit');a.add_argument('input');a.add_argument('output')
    a=sub.add_parser('coverage');a.add_argument('raw');a.add_argument('filtered');a.add_argument('receipt')
    args=p.parse_args();seal()
    if args.mode=='audit':audit(args.input,args.output)
    else:coverage(args.raw,args.filtered,args.receipt)

if __name__=='__main__':main()
