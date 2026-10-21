#!/usr/bin/env python3
"""Exact W7 full-star caps. A necessary count interface, never realizability."""
from pathlib import Path
from itertools import product, permutations
from functools import lru_cache
from collections import Counter, defaultdict
import argparse, gzip, hashlib, importlib.util, json, time

D = Path(__file__).resolve().parent
A = D.parent
F = A / 'frozen/audits/2026-10-20-r6-941-fibre-continuation-9c36e3c'
W = A / 'frozen/audits/2026-10-20-r6-941-j1-c11-1148ce0/frozen/audits/2026-10-20-r6-941-j1-w5-9c36e3c'
sp = importlib.util.spec_from_file_location('frozen_w5', W/'interface/check.py')
up = importlib.util.module_from_spec(sp); sp.loader.exec_module(up)
m = up.m
RIM = ('a','n','u4','u3','u2','u1','L','q','c','s','v','w','t')
N = len(RIM)

def packed(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':')).encode()

def proper_growth(n, t=(0,)):
    if len(t) == n:
        if t[-1] != t[0]: yield t
        return
    for x in range(min(3, max(t)+1)+1):
        if x != t[-1]: yield from proper_growth(n, t+(x,))

@lru_cache(None)
def left(a,n,L,q,c,rmask):
    rs = [r for r in range(4) if not rmask >> r & 1]
    g = [(b,p,h,R) for b,p,h,R in product(range(4), repeat=4)
         if R in rs and b not in (a,c,q,p) and p not in (a,q,n,h)
         and h not in (q,L,R,n)]
    q1 = [(b,R) for b,R in product(range(4), repeat=2)
          if R in rs and b == n and R == q and b not in (a,c,q)]
    j1 = [(b,R) for b,R in product(range(4), repeat=2)
          if R in rs and b == L and a != R and b not in (a,c,q)]
    return {'G':g, 'Q1':q1, 'J1':j1}

@lru_cache(None)
def right(a,c,s,v,w,t):
    return [(x,y,r) for x,y,r in product(range(4), repeat=3)
            if r not in (s,v,w,t,x,y) and x not in (c,s,y)
            and y not in (a,t)]

@lru_cache(None)
def cap_counts(a,n,L,q,c,s,v,w,t,rmask):
    out = {g:[0]*10 for g in ('G','Q1','J1')}
    sectors = [0,0]
    ls = left(a,n,L,q,c,rmask)
    for g, lifts in ls.items():
        for lift in lifts:
            b=lift[0]
            for x,y,r in right(a,c,s,v,w,t):
                j=m.ROWS.index(''.join(map(str,m.canonical((x,y,a,b,c)))))
                out[g][j]+=1
                if g=='G' and j==9:
                    sectors[0] += lift[2] == a
                    sectors[1] += lift[2] == b
    return out,sectors

def compute_caps():
    states=list(proper_growth(N)); index={s:i for i,s in enumerate(states)}
    ten=list(proper_growth(10)); i10={t:i for i,t in enumerate(ten)}
    parent_path=F/'frozen/audits/2026-10-20-r6-941-last-rejection-f13eb4d/J1/certificate.json'
    parent=json.loads(parent_path.read_text()); parent_live=set(parent['final_live'])
    matrices={g:[[] for _ in range(10)] for g in ('G','Q1','J1')}
    sectors=[[],[]]; capzero=[]; inherited=[]; allzero=[]
    for i, state in enumerate(states):
        a,n,u4,u3,u2,u1,L,q,c,s,v,w,t=state
        rmask=sum(1<<x for x in set((n,u4,u3,u2,u1,L)))
        values,sc=cap_counts(a,n,L,q,c,s,v,w,t,rmask)
        for g in matrices:
            for j in range(10): matrices[g][j].append(values[g][j])
        for j in range(2):sectors[j].append(sc[j])
        badcap=(any(values['G'][j] for j in (1,4,6)) or values['Q1'][9]
                or any(values['J1'][j] for j in (4,6)))
        badR=[R for R in range(4) if not rmask>>R&1
              and i10[m.canonical((a,n,R,L,q,c,s,v,w,t))] not in parent_live]
        if badcap:capzero.append(i)
        if badR:inherited.append([i,badR])
        if badcap or badR:allzero.append(i)
    zero=set(allzero);live=[i for i in range(len(states)) if i not in zero]
    witnesses=[]
    for e0,e1 in ((0,1),(1,0)):
        t=(0,1,2,1,2,1,2,3,1,2,e0,e1,2);i=index[m.canonical(t)]
        witnesses.append({'literal':t,'canonical_id':i,'cap_survives':i in live})
    return {'status':'exact W7 cap necessary interface; source not realized',
            'ordered_rim':RIM,'states':states,'matrices':matrices,'sectors':sectors,
            'cap_zero':capzero,'inherited_C10_zero_R_lifts':inherited,
            'initial_zero':allzero,'initial_live':live,'witnesses':witnesses,
            'source_positive_rows_survive':[any(matrices['G'][j][i] for i in live)
                for j in (0,2,3,5,7,8,9)],
            'parent_C10_sha256':hashlib.sha256(parent_path.read_bytes()).hexdigest(),
            'source_excluded':False,'source_realized':False,
            'selected_path_filter_used_as_source_count':False}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--build',action='store_true')
    ap.add_argument('--certificate',type=Path,default=D/'caps.json.gz')
    args=ap.parse_args();start=time.monotonic();data=json.loads(packed(compute_caps()))
    if args.build:
        with args.certificate.open('xb') as raw:
            with gzip.GzipFile(fileobj=raw,mode='wb',mtime=0) as out:out.write(packed(data)+b'\n')
    else:assert data==json.load(gzip.open(args.certificate,'rt'))
    print(json.dumps({'status':data['status'],'states':len(data['states']),
        'cap_zero':len(data['cap_zero']),'initial_live':len(data['initial_live']),
        'inherited_C10_zero_R_lifts':len(data['inherited_C10_zero_R_lifts']),
        'source_positive_rows_survive':data['source_positive_rows_survive'],
        'witnesses':data['witnesses'],'seconds':time.monotonic()-start},sort_keys=True))

if __name__=='__main__':main()
