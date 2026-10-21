#!/usr/bin/env python3
"""Universal run-template Fourier row spans, exact finite exploration only."""
from collections import Counter
import argparse
import json, time
from pathlib import Path


def nc(n, t=(0,), stack=(0,), b=1):
    if len(t) == n:
        yield t
        return
    for j, x in enumerate(stack):
        yield from nc(n, t+(x,), stack[:j+1], b)
    yield from nc(n, t+(b,), stack+(b,), b+1)


def templates(k):
    n=2*k
    for p in nc(n):
        if max(p)+1 != k+1:
            continue
        if any((i-j)%2 for i in range(n) for j in range(i) if p[i]==p[j]):
            continue
        other=p[1]
        free=[x for x in range(k+1) if x not in (0,other)]
        flips=[sum(1<<(i-2) for i in range(2,n) if p[i]==x) for x in free]
        yield p, flips


def inspect(k):
    ts=list(templates(k)); rows=1<<(2*k-2)
    union=set(); multiplicity=Counter()
    for p,flips in ts:
        freq=[a for a in range(rows) if all((a&v).bit_count()%2==0 for v in flips)]
        if len(freq) != 1<<(k-1):
            raise ValueError('invalid Fourier support size')
        union.update(freq); multiplicity.update(freq)
    return dict(k=k,runs=2*k,rows=rows,partition_templates=len(ts),
                columns=len(ts)*(1<<(k-1)),nonzeros_per_column=1<<(k-1),
                exact_row_rank=len(union),universal_row_identities=rows-len(union),
                fourier_support_multiplicity=dict(sorted(Counter(multiplicity.values()).items())),
                allowed_frequencies=sorted(union))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--build', action='store_true', help='exclusive-create ranks.json')
    args=ap.parse_args()
    start=time.monotonic()
    out={'status':'exact universal template rank; not a cone verdict',
         'proof':'All cosets of each flip subgroup occur; their Fourier spans are exactly the coordinate subspaces on the subgroup annihilators. The union of these supports gives the exact rational rank.',
         'templates':[inspect(k) for k in range(1,7)]}
    dest=Path(__file__).with_name('ranks.json')
    if args.build:
        with dest.open('x') as f: json.dump(out,f,indent=2); f.write('\n')
    elif json.loads(dest.read_text()) != json.loads(json.dumps(out)):
        raise ValueError('saved universal Fourier ranks differ from exact reconstruction')
    print(json.dumps([{q:v for q,v in r.items() if q!='allowed_frequencies'} for r in out['templates']],indent=2))
    print('seconds',time.monotonic()-start)


if __name__=='__main__': main()
