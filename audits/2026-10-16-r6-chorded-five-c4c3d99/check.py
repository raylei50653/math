#!/usr/bin/env python3
"""Read-only finite facial-ear calibration; not an arbitrary-source verifier."""
import argparse
from collections import Counter
from functools import lru_cache
import hashlib
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def edge(a, b):
    return tuple(sorted((a, b)))


def components(vertices, edges):
    unseen = set(vertices)
    adj = {v: set() for v in unseen}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    out = []
    while unseen:
        c = {min(unseen)}
        todo = list(c)
        unseen -= c
        while todo:
            new = adj[todo.pop()] & unseen
            unseen -= new
            c |= new
            todo.extend(sorted(new))
        out.append(c)
    return out


def cycles5(vertices, edges):
    adj = {v: set() for v in vertices}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    found = set()
    def visit(path):
        if len(path) == 5:
            if path[0] in adj[path[-1]]:
                found.add(min(tuple(path), tuple([path[0]] + path[:0:-1])))
            return
        for v in sorted(adj[path[-1]]):
            if v > path[0] and v not in path:
                visit(path + [v])
    for v in vertices:
        visit([v])
    return sorted(found)


def calibrate(g):
    vertices = g['J_vertices']
    edges = {tuple(e) for e in g['J_edges']}
    faces = [frozenset(f) for f in g['J_faces']]
    triangles = {frozenset(t) for t in combinations(vertices, 3)
                 if all(edge(a, b) in edges for a, b in combinations(t, 2))}
    facial = triangles == set(faces)
    dual = {e: tuple(i for i, f in enumerate(faces) if set(e) <= f) for e in edges}
    require(all(len(v) == 2 for v in dual.values()), 'non-spherical edge incidence')
    adj = {i: set() for i in range(len(faces))}
    for a, b in dual.values():
        adj[a].add(b)
        adj[b].add(a)

    @lru_cache(None)
    def pm(free):
        if not free:
            return ()
        u = min(free)
        for v in sorted(adj[u] & free):
            sub = pm(free - {u, v})
            if sub is not None:
                return ((u, v),) + sub
        return None

    stats = Counter()
    witnesses = []
    counterexamples = []
    for q in cycles5(vertices, edges):
        boundary = {edge(q[i], q[(i+1) % 5]) for i in range(5)}
        chords = sorted({edge(a, b) for a, b in combinations(q, 2)} & edges - boundary)
        sides = components(range(len(faces)), [d for e, d in dual.items() if e not in boundary])
        require(len(sides) == 2, 'five-cycle must separate two face sets')
        stats['five_cycles'] += 1
        for c in sides:
            if len(c) <= 1 or len(c) % 2 == 0:
                continue
            lifts = {str(v): pm(frozenset(c - {v})) for v in sorted(c)}
            fc = all(w is not None for w in lifts.values())
            stats['nontrivial_odd_sides'] += 1
            stats['factor_critical_sides'] += int(fc)
            for xy in chords:
                stats['chord_side_pairs'] += 1
                inside = all(v in c for v in dual[xy])
                common = [q[i] for i in range(5)
                          if {q[(i-1) % 5], q[(i+1) % 5]} == set(xy)]
                require(len(common) == 1, 'unique short ear')
                t = common[0]
                triangle = frozenset((*xy, t))
                if facial:
                    fi = faces.index(triangle)
                    require((fi in c) == inside, 'ear orientation')
                    if inside:
                        stats['interior_ears_rejected'] += 1
                        require(not fc, 'factor-critical side contains interior ear')
                        require(len(adj[fi] & c) == 1, 'ear must have degree one')
                        v = next(iter(adj[fi] & c))
                        require(lifts[str(v)] is None, 'deletion witness must fail')
                    else:
                        require(len(adj[fi] & c) == 2, 'exterior ear has two neighbours')
                        r = c | {fi}
                        b4 = {e for e, d in dual.items() if (d[0] in r) != (d[1] in r)}
                        require(len(b4) == 4, 'ear expansion must give four-cut')
                        verts4 = set().union(*map(set, b4))
                        induced = {e for e in edges if set(e) <= verts4} == b4
                        if len(r) >= 3 and len(faces) - len(r) >= 3:
                            require(induced, 'large sides must give induced C4')
                            stats['induced_four_expansions'] += 1
                        if fc:
                            stats['chorded_factor_critical_sides'] += 1
                            if not witnesses:
                                witnesses.append(dict(cycle=q, faces=sorted(c), chord=xy,
                                                      ear=fi, deletion_matchings=lifts))
                elif inside and fc:
                    counterexamples.append(dict(cycle=q, faces=sorted(c), chord=xy))
    return dict(name=g['name'], all_triangles_facial=facial, counts=dict(sorted(stats.items())),
                chorded_fc_witness=witnesses,
                nonfacial_interior_chord_fc_counterexamples=counterexamples[:1])


def build():
    raw = (HERE / 'graphs.json').read_bytes()
    base = json.loads((HERE / 'BASE.json').read_text())
    require(hashlib.sha256(raw).hexdigest() == base['control_sha256'], 'control drift')
    rows = [calibrate(g) for g in json.loads(raw) if 'J_vertices' in g]
    require(sum(r['counts'].get('interior_ears_rejected', 0) for r in rows) > 0,
            'interior-ear control not triggered')
    require(sum(r['counts'].get('induced_four_expansions', 0) for r in rows) > 0,
            'four-expansion control not triggered')
    return dict(schema=1, source_status='not triggered', arbitrary_size_proof='paper only',
                controls=rows)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--write', type=Path)
    p.add_argument('--check', type=Path)
    args = p.parse_args()
    require(not (args.write and args.check), 'choose write or check')
    expected = json.loads(json.dumps(build()))
    if args.write:
        with args.write.open('x') as f:
            json.dump(expected, f, indent=2, sort_keys=True)
            f.write('\n')
    if args.check:
        require(json.loads(args.check.read_text()) == expected, 'certificate mismatch')
    print(json.dumps(expected, sort_keys=True))


if __name__ == '__main__':
    main()
