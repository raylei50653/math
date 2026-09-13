#!/usr/bin/env python3
"""Fixed-port noncrossing path grammar. Complete finite computation, not disk completeness.

Each letter inserts a fresh two-edge path between two distinct boundary vertices.
Interior vertices of different paths are distinct. Multiplicity is forgotten by
this combinatorial grammar. The geometry interpretation is documented separately.
"""
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/local_closure/classification.json'


def cross(e, f):
    a, b = e
    c, d = f
    return a < c < b < d or c < a < d < b


def orient(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])


def segment_cross(e, f):
    # Independent exact straight-segment calculation on a convex integer polygon.
    a, b, c, d = [(i, i*i) for i in (*e, *f)]
    return orient(a,b,c)*orient(a,b,d) < 0 and orient(c,d,a)*orient(c,d,b) < 0


def direct_ok(edges):
    return all(not segment_cross(e, f) for e, f in combinations(edges, 2))


def selected(mask, edges):
    return [e for i, e in enumerate(edges) if mask >> i & 1]


def direct_extend(n, paths, boundary):
    # Build the actual graph, including the outer cycle, then backtrack interiors.
    # Repeated path endpoints introduce distinct vertices (no graph deduplication).
    edges = [(i, (i+1) % n) for i in range(n)]
    for k, (a, b) in enumerate(paths, n):
        edges.extend([(a, k), (k, b)])
    return direct_graph_extend(n + len(paths), edges, boundary)


def direct_graph_extend(vertex_count, edges, boundary):
    n = len(boundary)
    colors = list(boundary) + [-1] * (vertex_count-n)
    if any(colors[a] == colors[b] for a, b in edges if a < n and b < n):
        return False
    neighbors = [[] for _ in colors]
    for a, b in edges:
        neighbors[a].append(b)
        neighbors[b].append(a)
    def visit(v):
        if v == len(colors):
            return True
        for c in range(4):
            if all(colors[w] != c for w in neighbors[v]):
                colors[v] = c
                if visit(v+1):
                    return True
        colors[v] = -1
        return False
    return visit(n)


def classify(n):
    edges = list(combinations(range(n), 2))
    m = len(edges)
    conflict = [sum(1 << j for j, f in enumerate(edges) if cross(e, f)) for e in edges]
    assert all(cross(e,f) == segment_cross(e,f) for e in edges for f in edges)
    valid, reps, signature_of = [], {}, {}
    geometry_replays = 0
    for mask in range(1 << m):
        forbidden = 0
        for i in range(m):
            if mask >> i & 1:
                forbidden |= conflict[i]
        ok = mask & forbidden == 0
        assert ok == direct_ok(selected(mask, edges))
        geometry_replays += 1
        if ok:
            valid.append(mask)
            reps.setdefault(forbidden, mask)
            signature_of[mask] = forbidden
    signatures = sorted(reps)
    ids = {f: i for i, f in enumerate(signatures)}
    dead = len(ids) if any(signatures) else None
    states = []
    for forbidden in signatures:
        delta = [dead if forbidden >> i & 1 else ids[forbidden | conflict[i]]
                 for i in range(m)]
        states.append(dict(id=ids[forbidden], forbidden_mask=forbidden,
                           representative_mask=reps[forbidden], delta=delta, live=True))
    if dead is not None:
        states.append(dict(id=dead, delta=[dead]*m, live=False))
    transitions_checked = 0
    for mask in valid:
        q = ids[signature_of[mask]]
        for i, e in enumerate(edges):
            target = states[q]['delta'][i]
            # Direct geometry replay includes duplicate insertions.
            ok = direct_ok(selected(mask, edges) + [e])
            expected = ids[signature_of[mask | (1 << i)]] if ok else dead
            assert target == expected
            transitions_checked += 1
    separators = []
    for q, r in combinations(range(len(states)), 2):
        if q == dead or r == dead:
            separators.append([q,r,[]])
            assert states[q]['live'] != states[r]['live']
        else:
            difference = signatures[q] ^ signatures[r]
            letter = (difference & -difference).bit_length()-1
            outcomes = [direct_ok(selected(reps[signatures[s]],edges)+[edges[letter]])
                        for s in (q,r)]
            assert outcomes[0] != outcomes[1]
            separators.append([q,r,[letter]])
    coloring_checks = 0
    if n == 4:
        for mask in valid:
            for b in product(range(4), repeat=n):
                expected = all(b[i] != b[(i+1) % n] for i in range(n))
                assert direct_extend(n, selected(mask, edges), b) == expected
                coloring_checks += 1
    return dict(n=n, alphabet=edges, valid_supports=len(valid), live_classes=len(ids),
                total_classes=len(states), states=states, separators=separators,
                support_to_class=[[s,ids[signature_of[s]]] for s in valid],
                checks=dict(geometry_supports=geometry_replays,
                            transitions=transitions_checked, separators=len(separators),
                            full_graph_boundary_assignments=coloring_checks))


def counterexample():
    p, q, continuation = [(0,2)], [(1,3)], [(0,2)]
    relations = []
    for paths in (p,q,p+continuation,q+continuation):
        relations.append([b for b in product(range(4), repeat=4) if direct_extend(4,paths,b)])
    assert all(r == relations[0] for r in relations)
    assert direct_ok(p+continuation) and not direct_ok(q+continuation)
    # Explicit planar polygonal drawings for P+C: two fresh centers on opposite
    # sides of diagonal 02 of a diamond. Verify all nonincident edges are disjoint.
    points = [(0,0),(2,2),(0,4),(-2,2),(-1,2),(1,2)]
    edges = [(0,1),(1,2),(2,3),(3,0),(0,4),(4,2),(0,5),(5,2)]
    for e,f in combinations(edges,2):
        if set(e) & set(f):
            continue
        a,b,c,d = [points[i] for i in (*e,*f)]
        # No collinear contact in this witness; strict side separation suffices.
        assert (orient(a,b,c)*orient(a,b,d)>0 or orient(c,d,a)*orient(c,d,b)>0)
    # If the outer C4 were facial, an exterior apex adjacent to all four
    # boundary vertices would produce a planar K5 subdivision. Verify its model.
    negative_edges = [(0,1),(1,2),(2,3),(3,0),(0,4),(4,2),(1,5),(5,3)]
    apex_edges = negative_edges + [(6,i) for i in range(4)]
    branches = [0,1,2,3,6]
    model = [[0,1],[0,4,2],[0,3],[0,6],[1,2],[1,5,3],[1,6],[2,3],[2,6],[3,6]]
    edge_set = {frozenset(e) for e in apex_edges}
    assert {tuple(sorted((p[0],p[-1]))) for p in model} == set(combinations(branches,2))
    interiors = [v for p in model for v in p[1:-1]]
    assert len(interiors) == len(set(interiors)) and not set(interiors) & set(branches)
    assert all(frozenset(e) in edge_set for p in model for e in zip(p,p[1:]))
    return dict(P=p,Q=q,continuation=continuation,
                equal_full_coloring_relations=True,relation_size=len(relations[0]),
                relation=relations[0], grammar_acceptance=[True,False],
                planar_positive_witness=dict(points=points,edges=edges),
                negative_witness=dict(alternating_endpoints=[0,1,2,3],
                                      internally_disjoint_paths=[[0,4,2],[1,5,3]],
                                      exterior_apex=6, apex_edges=apex_edges, K5_subdivision=model),
                topology_status='Alternation and K5 subdivision checked; disk obstruction uses unformalized topology')


def sealed_wheel():
    cycle = [(i,(i+1)%4) for i in range(4)]
    wheel = cycle + [(i,4) for i in range(4)]
    before, after = [], []
    for b in product(range(4),repeat=4):
        if direct_graph_extend(4,cycle,b):
            before.append(b)
        ok = direct_graph_extend(5,wheel,b)
        assert ok == (all(b[i] != b[(i+1)%4] for i in range(4)) and len(set(b)) < 4)
        if ok:
            after.append(b)
    assert len(before)==84 and len(after)==60
    for i,j in combinations(range(4),2):
        assert {(b[i],b[j]) for b in before} == {(b[i],b[j]) for b in after}
    assert (0,1,2,3) in before and (0,1,2,3) not in after
    return dict(boundary=list(range(4)),edges=wheel,private_vertices=[4],
                cycle_relation_size=len(before),sealed_relation_size=len(after),
                all_pair_projections_equal=True,separator=[0,1,2,3],
                sealed_relation=after,restriction='boundary omits at least one of four colors')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args = parser.parse_args()
    result = dict(schema=1,status='computationally observed',
                  scope='fixed ordered ports; pairwise noncrossing length-two path insertion grammar',
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  classifications=[classify(n) for n in range(3,7)],
                  coloring_geometry_counterexample=counterexample(), sealed_wheel=sealed_wheel())
    data = json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.check:
        if OUT.read_text() != data:
            raise SystemExit('artifact mismatch')
    else:
        OUT.parent.mkdir(parents=True,exist_ok=True)
        OUT.write_text(data)
    for row in result['classifications']:
        print(f"n={row['n']}: {row['valid_supports']} supports, "
              f"{row['live_classes']} live / {row['total_classes']} total residuals; {row['checks']}")
    print('same-coloring/different-geometry counterexample: verified')


if __name__ == '__main__':
    main()
