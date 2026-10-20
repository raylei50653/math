"""Exact interfaces for legal no-new-vertex hexagon fillings.

Cyclic rim is (a,b,q,L,R,n). All 14 triangulations use index pairs,
lexicographically sorted as tuples. No graph-realizability is asserted for
abstract count vectors supplied to these interfaces.
"""
import itertools
from collections import Counter

ROWS=('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')

def canonical(t):
    seen={}
    return tuple(seen.setdefault(c,len(seen)) for c in t)

def proper(t):
    return all(t[i]!=t[(i+1)%len(t)] for i in range(len(t)))

def triangulations(n=6):
    ds=[(i,j) for i in range(n) for j in range(i+1,n) if j-i not in (1,n-1)]
    def crosses(u,v):
        a,b=u;c,d=v
        return a<c<b<d or c<a<d<b
    return [t for t in itertools.combinations(ds,n-3)
            if not any(crosses(u,v) for u,v in itertools.combinations(t,2))]

def left_matrix(eight,diagonals):
    """10 by |C8| fixed-word count transfer, rim=(a,b,q,L,R,n)."""
    ix={t:i for i,t in enumerate(eight)}
    answer=[]
    for row in ROWS:
        x,y,a,b,c=map(int,row)
        co=Counter()
        for n,right,left,q in itertools.product(range(4),repeat=4):
            e=(a,n,right,left,q,c,x,y)
            rim=(a,b,q,left,right,n)
            if proper(e) and b not in (a,c,q) and all(rim[i]!=rim[j] for i,j in diagonals):
                co[ix[canonical(e)]]+=1
        answer.append([co[i] for i in range(len(eight))])
    return answer

def mv(matrix,vector):
    return [sum(a*b for a,b in zip(row,vector)) for row in matrix]

def mask(ns):
    return sum(1<<i for i,n in enumerate(ns) if n>0)
