#!/usr/bin/env python3
"""Exact finite interfaces for the named r6 double-cap necessary model."""
from collections import Counter
import itertools

ROWS=('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
NAMES=('G','Q1','Q2','GB')
PERMS=tuple(p for p in itertools.permutations(range(4)) if p[0]//2==p[1]//2 and p[2]//2==p[3]//2)

def canonical(t):
    d={}
    return tuple(d.setdefault(x,len(d)) for x in t)

def growth(n,p=(0,),four=False):
    if len(p)==n:
        yield p
        return
    for x in range(min(3,max(p)+1)+1 if four else max(p)+2):
        yield from growth(n,p+(x,),four)

def proper(t):
    return all(t[i]!=t[(i+1)%len(t)] for i in range(len(t)))

def nc(p):
    return not any(p[i]==p[k] and p[j]==p[l] and p[i]!=p[j]
                   for i,j,k,l in itertools.combinations(range(len(p)),4))

def hc(t):
    return min(tuple(p[x] for x in t) for p in PERMS)

def literal(n,t=()):
    if len(t)==n:
        if t[-1]!=t[0]:
            yield t
        return
    for c in range(4):
        if not t or c!=t[-1]:
            yield from literal(n,t+(c,))

def build():
    eight=[t for t in growth(8,four=True) if proper(t)]
    ten=[t for t in growth(10,four=True) if proper(t)]
    index={t:i for i,t in enumerate(ten)}
    i8={t:i for i,t in enumerate(eight)}
    transfer=[]
    # One fixed literal E assignment, every complete cap assignment.
    for a,n,right,left,q,c,x,y in eight:
        entries=Counter()
        for s,v,w,t,r in itertools.product(range(4),repeat=5):
            core=(a,n,right,left,q,c,s,v,w,t)
            if not proper(core) or x in {s,r} or y in {t,r} or r in {s,v,w,t}:
                continue
            entries[index[canonical(core)]]+=1
        transfer.append(sorted(entries.items()))
    hist=Counter(hc(t) for t in literal(10))
    hrows=sorted(hist)
    hi={t:i for i,t in enumerate(hrows)}
    parts=[p for p in growth(10) if proper(p) and nc(p)]
    original={name:[[0]*274 for _ in ROWS] for name in NAMES}
    for ri,row in enumerate(ROWS):
        x,y,a,b,c=map(int,row)
        for n,right,left,q in itertools.product(range(4),repeat=4):
            boundary=(a,n,right,left,q,c,x,y)
            if not proper(boundary) or b in {a,q,c}:
                continue
            i=i8[canonical(boundary)]
            original['G'][ri][i]+=sum(p not in {a,b,q,n,h} and h not in {p,q,left,right,n}
                                     for p,h in itertools.product(range(4),repeat=2))
            original['Q1'][ri][i]+=int(n==b and right==q)
            original['Q2'][ri][i]+=int(n==b and left==b)
            original['GB'][ri][i]+=int(b not in {n,left,right})
    umatrix=[[0]*len(ten) for _ in ROWS]
    for ri,row in enumerate(ROWS):
        a,s,v,w,t=map(int,row)
        for n,right,left,q in itertools.product(range(4),repeat=4):
            core=(a,n,right,left,q,a,s,v,w,t)
            if not proper(core):
                continue
            lifts=sum(p not in {a,q,n,h} and h not in {p,q,left,right,n}
                      for p,h in itertools.product(range(4),repeat=2))
            umatrix[ri][index[canonical(core)]]+=lifts
    assert (len(eight),len(ten),len(hrows),sum(hist.values()),len(parts))==(274,2461,7382,59052,603)
    return eight,ten,index,transfer,hrows,hi,hist,parts,original,umatrix

def mv(matrix,vector):
    return [sum(x*y for x,y in zip(row,vector)) for row in matrix]

def mask(counts):
    return sum(1<<i for i,n in enumerate(counts) if n>0)

def orbit_column(start,partition,hi):
    start=tuple(start);partition=tuple(partition)
    assert len(start)==len(partition)==10 and proper(start),'orbit domain'
    assert canonical(partition)==partition and nc(partition),'noncrossing component partition'
    side=tuple(x//2 for x in start)
    assert all(side[i]==side[j] for i in range(10) for j in range(i) if partition[i]==partition[j]),'one side per component'
    assert all(side[i]!=side[(i+1)%10] or partition[i]==partition[(i+1)%10] for i in range(10)),'actual boundary edges'
    b=max(partition)+1
    assert b==sum(side[i]!=side[(i+1)%10] for i in range(10))//2+1,'triangulation component count'
    orbit=[tuple(c^1 if chosen&(1<<partition[i]) else c for i,c in enumerate(start))
           for chosen in range(1<<b)]
    assert len(set(orbit))==len(orbit),'free complete boundary switches'
    return Counter(hi[hc(t)] for t in orbit)


def source_positive_subsets(index):
    """All complete C10 restrictions of the two fixed D_old fibres."""
    answer={}
    # D_old(z,s,r,t,q,h,n)=ABABCAB and ABABCBC; A,B,C,D=0,1,2,3.
    for name,h,n in (('h_equals_a',0,1),('h_equals_b',1,2)):
        values=set()
        for right,left,v,w in itertools.product(range(4),repeat=4):
            a=c=r=0;s=t=b=1;q=2;p=3;x=2;y=3
            core=(a,n,right,left,q,c,s,v,w,t)
            if not proper(core):
                continue
            if r in {x,y,s,v,w,t} or x in {s,r} or y in {t,r}:
                continue
            if b in {a,c,p,q} or p in {a,b,q,h,n} or h in {p,q,left,right,n}:
                continue
            values.add(index[canonical(core)])
        answer[name]=sorted(values)
    assert [len(answer[name]) for name in ('h_equals_a','h_equals_b')]==[6,4]
    return answer
