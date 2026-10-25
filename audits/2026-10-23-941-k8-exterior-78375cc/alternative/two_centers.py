"""Bounded octagon patches with exactly two retained interior vertices."""
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
from one_center import polygon_triangulations, HERE, ROOT, SOURCE, AUTHORITY


@lru_cache(None)
def one_topologies(poly):
    n = len(poly)
    out = []
    for size in range(3, n+1):
        for positions in combinations(range(n), size):
            neighbors = tuple(poly[p] for p in positions)
            arcs = []
            bases = set()
            for j,a in enumerate(positions):
                b = positions[(j+1) % size]
                path = tuple(poly[i % n] for i in range(a,b+1 if b>a else b+n+1))
                arcs.append(polygon_triangulations(path))
                if len(path)>2:
                    bases.add(tuple(sorted((path[0],path[-1]))))
            for tris in product(*arcs):
                diagonals = tuple(sorted(bases.union(*tris)))
                assert len(diagonals) == n-size
                out.append((neighbors,diagonals))
    return tuple(out)


def two_topologies():
    out = set()
    def add(n1,n2,edge,diagonals):
        ns = sorted((tuple(sorted(n1)),tuple(sorted(n2))))
        out.add((ns[0],ns[1],edge,tuple(sorted(diagonals))))
    for neighbors,diagonals in one_topologies(tuple(range(8))):
        for a,b in combinations(range(len(neighbors)),2):
            add(neighbors[a:b+1],neighbors[b:]+neighbors[:a+1],True,diagonals)
    for a,b in combinations(range(8),2):
        if b-a in (1,7):
            continue
        poly1=tuple(range(a,b+1))
        poly2=tuple(i%8 for i in range(b,a+9))
        for (n1,d1),(n2,d2) in product(one_topologies(poly1),one_topologies(poly2)):
            add(n1,n2,False,set(d1)|set(d2)|{(a,b)})
    return sorted(out)


def make_catalog(words):
    allmask = (1 << len(words))-1
    equality = {p: sum(1<<i for i,w in enumerate(words) if w[p[0]]==w[p[1]])
                for p in combinations(range(8),2)}
    @lru_cache(None)
    def center_relation(n1,n2,edge):
        mask=0
        for i,w in enumerate(words):
            a=set(range(4))-{w[v] for v in n1}
            b=set(range(4))-{w[v] for v in n2}
            if a and b and (not edge or len(a|b)>1):
                mask |= 1<<i
        return mask
    catalog={}
    labelings=0
    topologies=two_topologies()
    for n1,n2,edge,diagonals in topologies:
        base=center_relation(n1,n2,edge)
        for bits in product((False,True),repeat=len(diagonals)):
            labelings+=1
            mask=base
            for pair,equal in zip(diagonals,bits):
                mask &= equality[pair] if equal else allmask ^ equality[pair]
            if mask and mask not in catalog:
                catalog[mask]=dict(neighbors=[list(n1),list(n2)],centers_adjacent=edge,
                    equal=[list(p) for p,b in zip(diagonals,bits) if b],
                    different=[list(p) for p,b in zip(diagonals,bits) if not b])
    return catalog,dict(triangulations=len(topologies),labelings=labelings,
                        distinct_nonempty_relations=len(catalog))


def run():
    raw=SOURCE.read_bytes()
    source=json.loads(raw)
    words=[tuple(r['word']) for r in source['caps'][0]['complete_fibres']]
    catalog,counts=make_catalog(words)
    out=dict(schema='941-k8-two-centers-v1',source=str(AUTHORITY.relative_to(ROOT)),
             source_sha256=hashlib.sha256(raw).hexdigest(),library=counts,caps=[])
    for cap in source['caps']:
        support=sum(1<<i for i,r in enumerate(cap['complete_fibres']) if r['full_lifts'])
        residual={tuple(w) for w in cap['residual_accepting_words']}
        union=0
        safe=[]
        for mask,model in sorted(catalog.items()):
            if mask & ~support:
                continue
            union|=mask
            safe.append(dict(**model,relation=[list(w) for i,w in enumerate(words) if mask>>i&1]))
        missing=[list(w) for i,w in enumerate(words) if w in residual and not(union>>i&1)]
        out['caps'].append(dict(distribution=cap['distribution'],old_residual_count=len(residual),
                               safe_candidates=safe,new_residual=missing))
        print(cap['distribution'],'safe',len(safe),'old',len(residual),'new',len(missing),flush=True)
    with (HERE/'TWO_CENTERS.json').open('x') as f:
        json.dump(out,f,sort_keys=True,indent=2)
        f.write('\n')
    print(counts)


if __name__=='__main__':
    run()
