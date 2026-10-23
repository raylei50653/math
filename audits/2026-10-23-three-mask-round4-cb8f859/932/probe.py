#!/usr/bin/env python3
"""Bounded C9-only folded-separator support probe; no graph/LP search."""
import gzip,itertools,json
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
SOURCE='audits/2026-10-13-c9-932-source-d521163/frozen/audits/2026-10-13-c5-no4ct-frontier-6943561/c9/finite/certificate.v2.json.gz'

def norm(w):
    seen={};return tuple(seen.setdefault(x,len(seen)) for x in w)

def row_ids(mask):return [i for i in range(820) if mask>>i&1]

def grid(rows,site,equal):
    index={tuple(r):i for i,r in enumerate(rows)};end=0 if equal else 1
    group=[p for p in itertools.permutations(range(4)) if p[0]==0 and p[end]==end]
    paths=[]
    for length,start,finish in [(3,0,end),(4,end,0)]:
        words=[w for w in itertools.product(range(4),repeat=length) if all(a!=b for a,b in zip((start,)+w,w+(finish,)))];orbits={}
        for w in words:
            orbit=tuple(sorted({tuple(g[c] for c in w) for g in group}));orbits[orbit[0]]=orbit
        paths.append(sorted(orbits.items()))
    cells=[];coords={}
    for a,(u,uo) in enumerate(paths[0]):
        line=[]
        for b,(v,vo) in enumerate(paths[1]):
            options=set()
            for image in vo:
                shifted=(0,)+u+(end,)+image
                original=shifted[-site:]+shifted[:-site] if site else shifted
                options.add(index[norm(original)])
            mask=sum(1<<p for p in options);line.append(mask)
            for p in options:
                assert p not in coords;coords[p]=(a,b)
        cells.append(line)
    return cells,coords

def rejects(orbit,support,g):
    cells,coords=g;aa=set();bb=set()
    for p in row_ids(orbit):
        if p in coords:
            a,b=coords[p];aa.add(a);bb.add(b)
    return any(not(cells[a][b]&support) for a in aa for b in bb)

def main():
    src=json.loads(gzip.decompress((REPO/SOURCE).read_bytes()));rows=src['inner_pattern_order'];ob=src['kempe_obligations']
    # JSON stores bitsets as integers.
    queries=[q for q in src['queries'] if q['target']==932 and q['geometry_id']=='induced' and q['status']=='necessary_condition_residual']
    gs={site:[grid(rows,site,False),grid(rows,site,True)] for site in range(9)}
    print(json.dumps({'grids':{str(s):[[len(g[0]),len(g[0][0]),len(g[1])] for g in gg] for s,gg in gs.items()}}),flush=True)
    results=[]
    for q in queries:
        for site in range(9):
            support=q['fixed_point'];rounds=[]
            while True:
                remove=[]
                for p in row_ids(support):
                    bad=[si for si,opts in enumerate(ob[p]) if all(o&~support or any(rejects(o,support,g) for g in gs[site]) for o in opts)]
                    if bad:remove.append((p,bad))
                if not remove:break
                rounds.append(len(remove));support &= ~sum(1<<p for p,_ in remove)
            results.append({'query_id':q['query_id'],'site':site,'initial':q['fixed_point'].bit_count(),'rounds':rounds,'final':support.bit_count()})
        print(json.dumps({'query_id':q['query_id'],'results':results[-9:]}),flush=True)
    with (HERE/'probe-results.json').open('x') as f:json.dump(results,f,indent=2);f.write('\n')

if __name__=='__main__':main()
