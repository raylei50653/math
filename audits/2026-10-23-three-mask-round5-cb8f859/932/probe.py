#!/usr/bin/env python3
"""Fixed s=0 original C9--Q9 annulus probe; no source graph enumeration."""
import gzip,itertools,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[2]
SRC='audits/2026-10-13-c9-932-source-d521163/frozen/audits/2026-10-13-c5-no4ct-frontier-6943561/c9/finite/certificate.v2.json.gz'
def norm(w):
    d={};return tuple(d.setdefault(c,len(d)) for c in w)
def bits(m):
    while m:
        b=m&-m;yield b.bit_length()-1;m-=b
def main():
    s=json.loads(gzip.decompress((REPO/SRC).read_bytes()));rows=[tuple(w) for w in s['inner_pattern_order']];index={w:i for i,w in enumerate(rows)};ob=s['kempe_obligations'];band=[]
    for q in rows:
        options=[tuple(c for c in range(4) if c not in [q[(i-1)%9],q[i]]) for i in range(9)];counts={}
        for c in itertools.product(*options):
            if any(c[i]==c[(i+1)%9] for i in range(9)):continue
            j=index[norm(c)];counts[j]=counts.get(j,0)+1
        band.append(counts)
    print('band',len(band),'nonzero entries',sum(map(len,band)),'full lifts',sum(sum(x.values()) for x in band),flush=True)
    out=[]
    for query in s['queries']:
        if not(query['target']==932 and query['geometry_id']=='induced' and query['status']=='necessary_condition_residual'):continue
        support=query['fixed_point'];initial=sum(1<<i for i,entry in enumerate(band) if entry and all(support>>j&1 for j in entry));cur=initial;rounds=[]
        while True:
            remove=[p for p in bits(cur) if any(all(o&~cur for o in options) for options in ob[p])]
            if not remove:break
            rounds.append(len(remove));cur&=~sum(1<<p for p in remove)
        record={'query_id':query['query_id'],'original_C_support':support.bit_count(),'Q_initial':initial.bit_count(),'rounds':rounds,'Q_final':cur.bit_count()};out.append(record);print(json.dumps(record),flush=True)
    with (HERE/'probe-results.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
if __name__=='__main__':main()
