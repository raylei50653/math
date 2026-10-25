"""Seven outer-row necessary Kempe fixedpoint; source realization stays OPEN."""
from functools import lru_cache
from itertools import combinations, permutations, product
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import time

HERE=Path(__file__).resolve().parent
PARENT=HERE.parent
SOURCE=PARENT/'frozen/audits/2026-10-23-941-types-wrong-side-round7-6b09cd4/certificate.json'
SPEC=importlib.util.spec_from_file_location('exterior_parent',HERE/'entry/exterior_parent.py')
P=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(P)
ROWS=tuple(tuple(map(int,q)) for q in ('01012','01023','01201','01203','01213','01231','01232'))
ROW_ID={q:i for i,q in enumerate(ROWS)}
PAIRS=P.PAIRS
PERMS=tuple(permutations(range(4)))


def encode(word):
    return sum(c<<(2*i) for i,c in enumerate(word))


def decode(code,n):
    return tuple((code>>(2*i))&3 for i in range(n))


def state(q,w):
    return (ROW_ID[q]<<16)|encode(w)


@lru_cache(None)
def normalization(outer):
    palette={}
    for c in outer:
        palette.setdefault(c,len(palette))
    q=tuple(palette[c] for c in outer)
    for c in range(4):
        if c not in palette:
            palette[c]=len(palette)
    return q,tuple(palette[c] for c in range(4))


@lru_cache(None)
def exterior_catalog(active):
    points=[(v,) for v in range(13) if active>>v&1]
    edges=[(i,(i+1)%8) for i in range(8)]+[(8+i,8+(i+1)%5) for i in range(5)]
    forced=P.join([points,[(a,b) for a,b in edges if active>>a&1 and active>>b&1]])
    result=[]
    for p in P.partitions(len(forced)):
        blocks=tuple(sorted(tuple(sorted(v for j in b for v in forced[j])) for b in p))
        if P.noncrossing(blocks,range(8)) and P.noncrossing(blocks,range(8,13)):
            result.append(blocks)
    return tuple(result)


@lru_cache(None)
def annular(partition):
    return P.annular_necessary(partition)


def compatible(a,b):
    return annular(tuple(sorted(a+b)))


def successor_states(q,w,pair,full):
    colors=w+q
    a,b=pair
    successors=set()
    blocks=[sum(1<<v for v in block) for block in full]
    for choice in range(1<<len(blocks)):
        flip=0
        for j,block in enumerate(blocks):
            if choice>>j&1:
                flip|=block
        outer=tuple(a+b-c if flip>>(i+8)&1 else c for i,c in enumerate(q))
        nq,palette=normalization(outer)
        if nq not in ROW_ID:
            return None
        nw=tuple(palette[a+b-c if flip>>i&1 else c] for i,c in enumerate(w))
        successors.add(state(nq,nw))
    return frozenset(successors)


def initial(cap):
    canonical=[tuple(f['word']) for f in cap['complete_fibres'] if f['full_lifts']]
    support=sorted({tuple(p[c] for c in w) for w in canonical for p in PERMS})
    residual=sorted({tuple(p[c] for c in w) for w in cap['residual_accepting_words'] for p in PERMS})
    states={(q,w):state(q,w) for q in ROWS for w in (residual if q==ROWS[-1] else support)}
    return states


def build_table(cap,progress=None):
    start=time.monotonic()
    states=initial(cap)
    available=set(states.values())
    canonical_fibres={tuple(f['word']):f['full_lifts'] for f in cap['complete_fibres']}
    @lru_cache(None)
    def local_signatures(cw,cpair):
        return tuple(sorted({P.cap_connections(cap,cw,lift,cpair) for lift in canonical_fibres[cw]}))
    table={}
    for count,((q,w),sid) in enumerate(sorted(states.items()),1):
        cw,palette=normalization(w)
        row=[]
        for pair in PAIRS:
            cp=tuple(sorted(palette[c] for c in pair))
            locals=local_signatures(cw,cp)
            active=sum(1<<i for i,c in enumerate(w+q) if c in pair)
            allowed=[]
            for part in exterior_catalog(active):
                outcomes=set()
                for local in locals:
                    ts=successor_states(q,w,pair,P.join([part,local]))
                    if ts is None or not ts<=available:
                        break
                    outcomes.update(ts)
                else:
                    allowed.append((part,frozenset(outcomes)))
            row.append(tuple(allowed))
        table[sid]=tuple(row)
        if count%1000==0:
            print('built',count,'/',len(states),'seconds',round(time.monotonic()-start,2),flush=True)
            if progress:
                progress(count,len(states),time.monotonic()-start)
    return table


def analyze(cap,index):
    table=build_table(cap)
    current=set(table)
    rounds=[]
    witnesses={}
    while True:
        removed=[]
        witnesses={}
        for sid in sorted(current):
            allowed=[[p for p,ts in row if ts<=current] for row in table[sid]]
            choices=[]
            for i in range(3):
                j=5-i
                chosen=next(((a,b) for a in allowed[i] for b in allowed[j] if compatible(a,b)),None)
                if chosen is None:
                    break
                choices.append(chosen)
            if len(choices)==3:
                witnesses[sid]=choices
            else:
                removed.append(sid)
        counts=[sum(sid>>16==i for sid in current) for i in range(7)]
        removed_counts=[sum(sid>>16==i for sid in removed) for i in range(7)]
        rounds.append(dict(before=counts,removed_counts=removed_counts,removed=removed))
        print('round',len(rounds),'before',counts,'removed',removed_counts,flush=True)
        if not removed:
            break
        current.difference_update(removed)
    return dict(index=index,distribution=cap['distribution'],initial=len(table),rounds=rounds,
                remaining=sorted(current),necessary_controls=[dict(state=s,choices=c) for s,c in sorted(witnesses.items())])


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--indices',nargs='+',type=int,default=[0,1,2,3])
    parser.add_argument('--output',default='EXPLORATION.json')
    args=parser.parse_args()
    raw=SOURCE.read_bytes()
    source=json.loads(raw)
    out=dict(schema='941-k8-seven-row-necessary-v1',source_sha256=hashlib.sha256(raw).hexdigest(),
             rows=[''.join(map(str,q)) for q in ROWS],caps=[])
    start=time.monotonic()
    for index in args.indices:
        result=analyze(source['caps'][index],index)
        out['caps'].append(result)
        with (HERE/f'CAP_{index}.json').open('x') as f:
            json.dump(result,f,sort_keys=True,separators=(',',':'));f.write('\n')
        print('cap',index,'done seconds',round(time.monotonic()-start,2),flush=True)
    with (HERE/args.output).open('x') as f:
        json.dump(out,f,sort_keys=True,separators=(',',':'));f.write('\n')


if __name__=='__main__':
    main()
