"""Bounded safe octagon replacements retaining one interior vertex.

All ports keep their ordered identities and one common literal palette.
This searches candidate patches only; it makes no original-source assertion.
"""
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
AUTHORITY = ROOT / 'audits/2026-10-23-941-types-wrong-side-round7-6b09cd4/certificate.json'
SOURCE = HERE / 'entry/certificate.json'


@lru_cache(None)
def polygon_triangulations(poly):
    if len(poly) < 3:
        return (frozenset(),)
    rim = {tuple(sorted((poly[i], poly[(i+1) % len(poly)]))) for i in range(len(poly))}
    out = set()
    for k in range(1, len(poly)-1):
        for left in polygon_triangulations(poly[:k+1]):
            for right in polygon_triangulations(poly[k:]):
                es = left | right | {tuple(sorted((poly[0], poly[k]))), tuple(sorted((poly[k], poly[-1])))}
                out.add(frozenset(es - rim))
    return tuple(sorted(out, key=lambda x: sorted(x)))


def make_catalog(words):
    allmask = (1 << len(words)) - 1
    equality = {p: sum(1 << i for i, w in enumerate(words) if w[p[0]] == w[p[1]])
                for p in combinations(range(8), 2)}
    catalog = {}
    triangulated_count = labeled_count = 0
    for size in range(3, 9):
        for neighbors in combinations(range(8), size):
            arcs = []
            bases = set()
            for j, a in enumerate(neighbors):
                b = neighbors[(j+1) % size]
                path = tuple(i % 8 for i in range(a, b+1 if b > a else b+9))
                arcs.append(polygon_triangulations(path))
                if len(path) > 2:
                    bases.add(tuple(sorted((a, b))))
            center_mask = sum(1 << i for i, w in enumerate(words)
                              if len({w[v] for v in neighbors}) < 4)
            for triangulations in product(*arcs):
                diagonals = sorted(bases.union(*triangulations))
                assert len(diagonals) == 8-size
                triangulated_count += 1
                for bits in product((False, True), repeat=len(diagonals)):
                    labeled_count += 1
                    mask = center_mask
                    for pair, equal in zip(diagonals, bits):
                        mask &= equality[pair] if equal else allmask ^ equality[pair]
                    if mask and mask not in catalog:
                        catalog[mask] = dict(neighbors=list(neighbors),
                            equal=[list(p) for p,b in zip(diagonals,bits) if b],
                            different=[list(p) for p,b in zip(diagonals,bits) if not b])
    return catalog, dict(triangulations=triangulated_count, labelings=labeled_count,
                         distinct_nonempty_relations=len(catalog))


def run():
    raw = SOURCE.read_bytes()
    source = json.loads(raw)
    words = [tuple(r['word']) for r in source['caps'][0]['complete_fibres']]
    catalog, counts = make_catalog(words)
    out = dict(schema='941-k8-one-center-v1', source=str(AUTHORITY.relative_to(ROOT)),
               source_sha256=hashlib.sha256(raw).hexdigest(), library=counts, caps=[])
    for cap in source['caps']:
        assert words == [tuple(r['word']) for r in cap['complete_fibres']]
        support = sum(1 << i for i,r in enumerate(cap['complete_fibres']) if r['full_lifts'])
        old_residual = {tuple(w) for w in cap['residual_accepting_words']}
        union = 0
        safe = []
        for mask, model in sorted(catalog.items()):
            if mask & ~support:
                continue
            union |= mask
            safe.append(dict(**model, relation=[list(w) for i,w in enumerate(words) if mask >> i & 1]))
        new_residual = [list(w) for i,w in enumerate(words) if w in old_residual and not (union >> i & 1)]
        row = dict(distribution=cap['distribution'], old_residual_count=len(old_residual),
                   safe_candidates=safe, new_residual=new_residual)
        out['caps'].append(row)
        print(cap['distribution'], 'safe', len(safe), 'old',len(old_residual),'new',len(new_residual), flush=True)
    with (HERE/'ONE_CENTER.json').open('x') as f:
        json.dump(out,f,sort_keys=True,indent=2)
        f.write('\n')
    print(counts)


if __name__ == '__main__':
    run()
