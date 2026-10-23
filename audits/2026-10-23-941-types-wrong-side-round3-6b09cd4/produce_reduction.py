#!/usr/bin/env python3
"""Select a small safe cover on frozen six-contact cap relations, exclusive-create."""
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CAP = 'audits/2026-10-23-941-gamma8-joint-bpaths-6b09cd4/EXACT_CAPS.json'
BASE = '6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'


def crossing(e, f):
    a, b = e
    c, d = f
    return a < c < b < d or c < a < d < b


def graph(constraints, spokes=()):
    parent = list(range(6))
    def find(v):
        while parent[v] != v:
            v = parent[v]
        return v
    for (a, b), different in constraints:
        if not different:
            a, b = find(a), find(b)
            parent[max(a, b)] = min(a, b)
    mapping = [find(i) for i in range(6)]
    edges = {tuple(sorted((mapping[i], mapping[(i+1) % 6]))) for i in range(6)}
    edges.update(tuple(sorted((mapping[a], mapping[b]))) for (a, b), different in constraints if different)
    edges.update((mapping[i], 6) for i in spokes)
    vertices = sorted(set(mapping) | ({6} if spokes else set()))
    return dict(constraints=[[list(e), s] for e, s in constraints], spokes=list(spokes),
                vertex_map=mapping, vertices=vertices, edges=[list(e) for e in sorted(edges)],
                completed_interior_saving=8+6-len(set(mapping))-bool(spokes))


def lifts(g, w):
    colors = {}
    for i, c in enumerate(w):
        v = g['vertex_map'][i]
        if v in colors and colors[v] != c:
            return []
        colors[v] = c
    result = []
    for c in range(4) if g['spokes'] else [None]:
        if c is not None:
            colors[6] = c
        if all(colors[a] != colors[b] for a, b in g['edges']):
            result.append([colors[v] for v in g['vertices']])
    return result


def main():
    old = json.loads((HERE/'entry'/CAP).read_text())
    words = old['proper_S4_words']
    diagonals = [(a,b) for a,b in combinations(range(6),2) if b-a not in (1,5)]
    pool = {}
    for mask in range(1 << len(diagonals)):
        selected = [e for i,e in enumerate(diagonals) if mask >> i & 1]
        if any(crossing(e,f) for e,f in combinations(selected,2)):
            continue
        for signs in product((0,1), repeat=len(selected)):
            constraints = list(zip(selected,signs))
            support = frozenset(i for i,w in enumerate(words)
                if all((w[a] != w[b]) == bool(s) for (a,b),s in constraints))
            if not support:
                continue
            g = graph(constraints)
            if support not in pool or len(constraints) < len(pool[support]['constraints']):
                pool[support] = g
    wheel = graph([((0,4),1)], range(5))
    wheel_support = frozenset(i for i,w in enumerate(words) if lifts(wheel,w))
    pool[wheel_support] = wheel
    candidates = []
    caps = []
    for cap in old['caps']:
        support = {i for i,r in enumerate(cap['relations']) if r['full_lifts']}
        remaining = set(support)
        chosen = []
        safe = [(s,g) for s,g in pool.items() if s <= support]
        while remaining:
            s,g = max(safe, key=lambda item:(len(item[0]&remaining),
                -bool(item[1]['spokes']),-len(item[1]['constraints']),
                json.dumps(item[1],sort_keys=True)))
            if not (s & remaining):
                raise ValueError('incomplete cover '+str(cap['id']))
            if g not in candidates:
                candidates.append(g)
            chosen.append(candidates.index(g))
            remaining -= s
        caps.append(dict(cap_id=cap['id'],candidates=chosen,relations=cap['relations']))
    for i,g in enumerate(candidates):
        g['id'] = i
        g['relations'] = [dict(word=w,full_lifts=lifts(g,w)) for w in words]
    certificate = dict(schema='941-eight-inner-safe-cover-v1',base=BASE,
        ordered_boundary=old['boundary'], ordered_inner=old['inner'],
        words=words,candidates=candidates,caps=caps,
        selection='one genuine original 01232 full witness selects one graph once; every rejection backfills through that same graph',
        source_controls='not triggered',paper='PROOF.md')
    with (HERE/'reduction-certificate.json').open('x') as f:
        json.dump(certificate,f,indent=2,sort_keys=True)
        f.write('\n')
    print(json.dumps(dict(caps=len(caps),candidates=len(candidates),
        selected_counts=[len(c['candidates']) for c in caps],
        savings=sorted(set(g['completed_interior_saving'] for g in candidates)))))


if __name__ == '__main__':
    main()
