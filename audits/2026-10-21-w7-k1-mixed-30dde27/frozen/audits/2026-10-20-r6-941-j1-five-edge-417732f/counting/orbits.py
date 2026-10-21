#!/usr/bin/env python3
"""Exact complementary-pair orbit columns, generated modulo four global flips.

Only columns not touching the proved-zero full-fibre rows are retained.
This is an optimization of the frozen enumerator, checked against its C11 K.
"""
from pathlib import Path
from collections import Counter
from itertools import product
import argparse,gzip,hashlib,importlib.util,json,pickle,time

D=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('caps',D/'check.py')
c=importlib.util.module_from_spec(sp);sp.loader.exec_module(c)

def nc(n,t=(0,),stack=(0,),b=1):
    if len(t)==n:yield t;return
    for j,x in enumerate(stack):yield from nc(n,t+(x,),stack[:j+1],b)
    yield from nc(n,t+(b,),stack+(b,),b+1)

def encode(t):
    a=0
    for x in t:a=4*a+x
    return a

def half(t):
    # Normalize colour at position zero, its palette mate, then the other side.
    a=t[0];b=next(x for x in t if x//2!=a//2)
    p={a:0,a^1:1,b:2,b^1:3}
    return tuple(p[x] for x in t)

def rowmap(states):
    out={}
    for i,t in enumerate(states):
        for mate in (1,2,3):
            other=[x for x in (1,2,3) if x!=mate]
            perm={0:0,mate:1,other[0]:2,other[1]:3}
            row=encode(half(tuple(perm[x] for x in t)))
            assert row not in out or out[row]==i
            out[row]=i
    assert len(out)==3*len(states)
    return out

def build(states,initial_live):
    n=len(states[0]);rowids=rowmap(states);live=set(initial_live)
    cols=set();hist=Counter();parts=0;admissible=0;generated=0
    family_digest=hashlib.sha256()
    start=time.monotonic()
    for p in nc(n):
        parts+=1;b=max(p)+1
        if b==1 or sum(p[i]!=p[(i+1)%n] for i in range(n))!=2*(b-1):continue
        adj=[set() for _ in range(b)]
        for i in range(n):
            x,y=p[i],p[(i+1)%n]
            if x!=y:adj[x].add(y);adj[y].add(x)
        side=[None]*b;side[0]=0;stack=[0];okay=True
        while stack:
            x=stack.pop()
            for y in adj[x]:
                if side[y] is None:side[y]=1-side[x];stack.append(y)
                elif side[y]==side[x]:okay=False
        if not okay:continue
        assert all(x is not None for x in side)
        admissible+=1
        first=[p.index(x) for x in range(b)]
        other=next(x for x in p if side[x])
        flipblocks=[x for x in range(b) if x not in (0,other)]
        masks=[sum(1<<(2*(n-1-i)) for i in range(n) if p[i]==x) for x in flipblocks]
        free=[i for i in range(1,n) if p[i]!=p[i-1] and i!=first[p[i]]]
        for choices in product((0,1),repeat=len(free)):
            chosen=dict(zip(free,choices));bits=[0]*n
            for i in range(1,n):
                if p[i]==p[i-1]:bits[i]=1-bits[i-1]
                elif i in chosen:bits[i]=chosen[i]
            if p[-1]==p[0] and bits[-1]==bits[0]:continue
            t=tuple(2*side[p[i]]+bits[i] for i in range(n))
            assert c.m.proper(t) and half(t)==t
            orbit=[encode(t)]
            for mask in masks:orbit += [x^mask for x in orbit]
            assert len(set(orbit))==len(orbit)
            generated+=1
            family_digest.update(c.packed(sorted(orbit))+b'\n')
            if all(rowids[x] in live for x in orbit):cols.add(tuple(sorted(orbit)))
        if parts%100000==0:print('parts',parts,'columns',len(cols),'seconds',time.monotonic()-start,flush=True)
    cols=sorted(cols);rounds=[]
    while True:
        good=[col for col in cols if all(rowids[r] in live for r in col)]
        covered={r for col in good for r in col}
        bad={i for r,i in rowids.items() if i in live and r not in covered}
        if not bad:cols=good;break
        rounds.append(sorted(bad));live-=bad;cols=good
    return {'rowids':rowids,'columns':cols,'live':sorted(live),'rounds':rounds,
            'noncrossing_count':parts,'admissible_partitions':admissible,
            'generated_columns_before_deduplication':generated,
            'full_generated_columns_sha256':family_digest.hexdigest(),
            'rowids_sha256':hashlib.sha256(c.packed(sorted(rowids.items()))).hexdigest(),
            'live_columns_sha256':hashlib.sha256(c.packed(cols)).hexdigest(),
            'coefficients_per_row':4,'full_half_row_size':8}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--c11-control',action='store_true')
    ap.add_argument('--build',action='store_true')
    ap.add_argument('--certificate',type=Path,default=D/'orbits.json')
    ap.add_argument('--columns-certificate',type=Path,default=D/'orbits.json.gz')
    args=ap.parse_args();start=time.monotonic()
    if args.c11_control:
        f=D.parent/'frozen/audits/2026-10-20-r6-941-j1-c11-1148ce0/counting/discovery.pickle'
        with f.open('rb') as src:old,*_=pickle.load(src)
        ans=build(old['states'],range(len(old['states'])))
        oldcols={tuple(sorted(encode(old['hrows'][r]) for r,v in col)) for col in old['columns']}
        assert all(v==4 for col in old['columns'] for r,v in col)
        assert oldcols==set(ans['columns'])
        print(json.dumps({'control':'PASS','columns':len(oldcols),
                          'all_columns_equal':True,'all_entry_multiplicities':4,
                          'seconds':time.monotonic()-start}))
        return
    data=json.load(gzip.open(D/'caps.json.gz','rt'));ans=build(data['states'],data['initial_live'])
    live=set(ans['live'])
    report={k:v for k,v in ans.items() if k not in ('columns','rowids','live')}
    report.update({'status':'exact full complementary-pair orbit necessary closure',
      'states':len(data['states']),'initial_live':len(data['initial_live']),
      'live':len(live),'columns':len(ans['columns']),
      'witnesses':[dict(w,orbit_survives=w['canonical_id'] in live) for w in data['witnesses']],
      'source_positive_rows_survive':[any(data['matrices']['G'][j][i] for i in live) for j in (0,2,3,5,7,8,9)],
      'source_excluded':False,'source_realized':False})
    if args.build:
        with args.certificate.open('x') as out:json.dump(report,out,indent=2);out.write('\n')
        # This complete deterministic integer object also supports downstream LPs.
        cert=dict(ans,rowids=sorted(ans['rowids'].items()))
        with (D/'orbits.json.gz').open('xb') as raw:
            with gzip.GzipFile(fileobj=raw,mode='wb',mtime=0) as out:out.write(c.packed(cert)+b'\n')
    else:
        assert report==json.loads(args.certificate.read_text())
        frozen=json.load(gzip.open(args.columns_certificate,'rt'))
        assert c.packed(dict(ans,rowids=sorted(ans['rowids'].items())))==c.packed(frozen)
    print(json.dumps({k:v for k,v in report.items() if k!='rounds'}|{'seconds':time.monotonic()-start},sort_keys=True))

if __name__=='__main__':main()
