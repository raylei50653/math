#!/usr/bin/env python3
"""Deterministic deletion minimization, not a proof of global minimality."""
import argparse
import json
from pathlib import Path
from construct_boundary import accepted, certificate
from search_boundary import CYCLE


def bad(n, edges):
    s = accepted(n, sorted(edges))
    return bool(s) and all(len(set(b)) == 4 for b in s)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input', default='artifacts/construction/bad_certificates.jsonl')
    p.add_argument('--output', default='artifacts/construction')
    a = p.parse_args()
    root = Path(a.output)
    root.mkdir(parents=True, exist_ok=True)
    original = json.loads(Path(a.input).read_text().splitlines()[0])
    n, edges = original['n'], set(map(tuple, original['edges']))
    history = []
    changed = True
    while changed:
        changed = False
        for v in range(5, n):
            smaller = {(u - (u > v), w - (w > v)) for u, w in edges
                       if u != v and w != v}
            if bad(n - 1, smaller):
                history.append(dict(delete_vertex=v, before_n=n))
                n, edges, changed = n - 1, smaller, True
                break
        if changed:
            continue
        for edge in sorted(edges - set(CYCLE)):
            if bad(n, edges - {edge}):
                history.append(dict(delete_edge=edge))
                edges.remove(edge)
                changed = True
                break
    assert not any(bad(n, edges - {e}) for e in edges - set(CYCLE))
    contractions = []
    for u, v in sorted(edges):
        if v < 5:
            continue
        mapping = [u if w == v else w for w in range(n)]
        mapping = [w - (w > v) for w in mapping]
        smaller = {tuple(sorted((mapping[x], mapping[y]))) for x, y in edges
                   if mapping[x] != mapping[y]}
        if any(y < 5 and (x, y) not in CYCLE for x, y in smaller):
            continue
        contractions.append(dict(edge=[u, v], bad=bad(n-1, smaller)))
    c = certificate(n, edges, accepted(n, sorted(edges)))
    (root / 'minimized.jsonl').write_text(json.dumps(c, sort_keys=True,
                                                   separators=(',', ':'))+'\n')
    (root / 'minimization.json').write_text(json.dumps(dict(
        history=history, n=n, m=len(edges), contractions=contractions,
        claim='single interior-vertex / non-boundary-edge deletion minimal; not global'),
        sort_keys=True, indent=2)+'\n')
    print('Deletion minimal:', n, len(edges), 'Sigma', c['color_orbits'])


if __name__ == '__main__':
    main()
