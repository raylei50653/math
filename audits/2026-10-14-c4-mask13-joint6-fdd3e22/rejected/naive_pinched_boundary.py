import itertools,json
from functools import lru_cache

N=6
EDGES=((0,1),(1,2),(2,3),(3,0),(0,4),(4,5),(5,0))
WALK=(0,1,2,3,0,4,5)
PAIRS=(((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2)))
def canon(row):
    d={}
    return tuple(d.setdefault(c,len(d)) for c in row)

def allowed(row):
    if any(row[a]==row[b] for a,b in EDGES):return False
    q=canon(row[:4])
    if q==(0,1,0,2):return False
    if q==(0,1,0,1):return set(row[4:])==set(range(4))-set(row[:4])
    if q==(0,1,2,3):return set(row[4:])=={row[1],row[3]}
    return q==(0,1,2,1)

def partitions(items):
    if not items:
        yield ()
        return
    v=items[0]
    for p in partitions(items[1:]):
        yield ((v,),)+p
        for i in range(len(p)):
            yield p[:i]+((v,)+p[i],)+p[i+1:]

def noncrossing(part):
    labels={v:i for i,b in enumerate(part) for v in b}
    w=[labels[v] for v in WALK]
    for i,j,k,l in itertools.combinations(range(len(w)),4):
        if w[i]==w[k] and w[j]==w[l] and w[i]!=w[j]:return False
    return True

@lru_cache(None)
def pair_partitions(row,pair):
    vs=tuple(v for v,c in enumerate(row) if c in pair)
    es=[(a,b) for a,b in EDGES if a in vs and b in vs]
    out=[]
    for p in partitions(vs):
        labels={v:i for i,b in enumerate(p) for v in b}
        if all(labels[a]==labels[b] for a,b in es):out.append(p)
    return out

def switch_orbit(row,parts,pairing):
    blocks=parts[0]+parts[1]
    colors=[pairing[0]]*len(parts[0])+[pairing[1]]*len(parts[1])
    out=set()
    for mask in range(1<<len(blocks)):
        r=list(row)
        for i,b in enumerate(blocks):
            if mask>>i&1:
                a,c=colors[i]
                for v in b:r[v]=c if r[v]==a else a
        out.add(canon(r))
    return frozenset(out)

ROWS=sorted({canon(row) for row in itertools.product(range(4),repeat=6) if allowed(row)})
OPTIONS={}
for row in ROWS:
    OPTIONS[row]=[]
    for pairing in PAIRS:
        opts=[]
        for a,b in itertools.product(*(pair_partitions(row,pair) for pair in pairing)):
            if not noncrossing(a+b):continue
            orbit=switch_orbit(row,(a,b),pairing)
            opts.append((a,b,orbit))
        OPTIONS[row].append(opts)

live=set(ROWS)
rounds=[]
while True:
    dead={row for row in live if any(not any(o<=live for a,b,o in opts) for opts in OPTIONS[row])}
    rounds.append({'live':sorted(live),'remove':sorted(dead)})
    if not dead:break
    live-=dead

def fmt(row):return ''.join('ABCD'[i] for i in row)
print('rows',len(ROWS),[fmt(r) for r in ROWS])
for n,r in enumerate(rounds):print('round',n,'remove',[fmt(x) for x in r['remove']])
for row in sorted(live):
    print('\n',fmt(row))
    for pairing,opts in zip(PAIRS,OPTIONS[row]):
        good=[(a,b,o) for a,b,o in opts if o<=live]
        print('pairing',pairing,'options',len(good))
        for a,b,o in good:print(' ',a,b,sorted(fmt(r) for r in o))

report={'walk':WALK,'edges':EDGES,'rows':[fmt(r) for r in ROWS],
        'rounds':[{key:[fmt(v) for v in vals] for key,vals in r.items()} for r in rounds],
        'survivors':[fmt(r) for r in sorted(live)]}
open('/tmp/c4-mask13-joint6-interface/kempe.json','w').write(json.dumps(report,indent=2)+'\n')
