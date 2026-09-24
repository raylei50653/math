#!/usr/bin/env python3
"""Fixed-domain relation controls and source-shaped minors, not a graph search."""
import argparse
from itertools import combinations, permutations, product
import json
from pathlib import Path

from c5_two_spoke_adjacent_21 import U, Q, connected, edge

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_two_spoke_middle_21/observations.json'


def colorings(vertices, edges, lists):
    vertices = sorted(vertices, key=lambda v: (len(lists[v]), str(v)))
    colors = {}
    neighbors = {v: {w for e in edges if v in e for w in e if w != v} for v in vertices}

    def visit(i):
        if i == len(vertices):
            yield colors.copy()
            return
        v = vertices[i]
        for a in sorted(lists[v]):
            if all(colors.get(w) != a for w in neighbors[v]):
                colors[v] = a
                yield from visit(i + 1)
                del colors[v]
    yield from visit(0)


def relation(vertices, edges, attachments, ports, b):
    lists = {v: U - {b[i] for i in attachments[v]} for v in vertices}
    return sorted({tuple(f[v] for v in ports) for f in colorings(vertices, edges, lists)})


def forbidden(tuples):
    return [a for a in sorted(U) if not any(all(x != a for x in t) for t in tuples)]


def controls():
    records = []
    rows = [b for b in product(range(4), repeat=5)
            if all(b[i] != b[(i+1) % 5] for i in range(5))]
    for count in (2, 1):
        # A is a triangle forbidding 2. All its attachments are on the left arc.
        av = ['a0', 'a1', 'a2']
        ae = {edge(u, v) for u, v in combinations(av, 2)}
        ap = av[:count]
        aa = {v: [1] if v in ap else [1, 4] for v in av}
        if count == 2:
            dv, de, dp, da = ['d0'], set(), ['d0'], {'d0': [0, 1, 4]}
        else:
            # A triangle with a genuine 3-forcing leaf; no fictitious boundary 3.
            dv = ['d0', 'd1', 'd2', 'd3']
            de = {edge(u, v) for u, v in combinations(dv[:3], 2)} | {edge('d2', 'd3')}
            dp = dv[:2]
            da = {v: [1] for v in dv[:3]} | {'d3': [0, 1, 4]}
        data = []
        full_edges = ae | de | {edge('z', v) for v in ap + dp}
        full_edges |= {edge(v, f'b{i}') for v, ids in (aa | da).items() for i in ids}
        full_edges |= {edge('z', 'b1'), edge('z', 'b2')}
        full_edges |= {edge(f'b{i}', f'b{(i+1)%5}') for i in range(5)}
        interior = av + dv + ['z']
        assert all(sum(v in e for e in full_edges) == (5 if v == 'z' else 4) for v in interior)
        for b in rows:
            ar = relation(av, ae, aa, ap, b)
            dr = relation(dv, de, da, dp, b)
            af, df = forbidden(ar), forbidden(dr)
            allowed = sorted(U - {b[1], b[2]} - set(af) - set(df))
            lists = {v: U for v in interior} | {f'b{i}': {b[i]} for i in range(5)}
            actual = sorted({f['z'] for f in colorings(list(lists), full_edges, lists)})
            assert allowed == actual
            if b == Q:
                assert af == [2] and df == [3] and not allowed
                r2 = ar if count == 2 else dr
                a = 2 if count == 2 else 3
                assert all(any(t[i] != a for t in r2) for i in (0, 1))
                assert not any(all(x != a for x in t) for t in r2)
            comps = [dict(ports=ap, tuples=ar, forbidden=af), dict(ports=dp, tuples=dr, forbidden=df)]
            comps.sort(key=lambda c: -len(c['ports']))
            data.append(dict(boundary=b, C2=comps[0], C1=comps[1], allowed=allowed))
        deletions = []
        lists = {v: U for v in interior} | {f'b{i}': {Q[i]} for i in range(5)}
        for e in sorted(full_edges):
            if all(v.startswith('b') for v in e):
                continue
            witness = next(colorings(list(lists), full_edges - {e}, lists), None)
            assert witness is not None
            deletions.append(dict(edge=e, coloring=witness))
        other_path = ['z', 'd0', 'b4'] if count == 2 else ['z', 'd0', 'd2', 'd3', 'b4']
        groups = [{v} for v in av] + [{'b1'}, set(other_path)]
        assert all(connected(g, full_edges) for g in groups)
        assert sum(map(len, groups)) == len(set().union(*groups))
        assert all(any(edge(u, v) in full_edges for u in groups[i] for v in groups[j])
                   for i, j in combinations(range(5), 2))
        records.append(dict(order='I' if count == 2 else 'II', edges=sorted(full_edges),
                            K5_branch_sets=[sorted(g) for g in groups],
                            rows=data, q_edge_deletions=deletions,
                            scope='complete degree/minimality algebra control; not a disk witness'))
    return records


def support_checks():
    records = []
    for size in range(4):
        for support in combinations(range(3), size):
            ps = [p for p in permutations(range(4)) if all(p[a] == a for a in support)]
            for roots in ({3}, {3, 0}, {3, 1}, {3, 2}):
                invariant = all({p[a] for a in roots} == roots for p in ps)
                required = set(range(3)) - roots
                assert not invariant or required <= set(support)
                records.append(dict(support=support, root_set=sorted(roots), invariant=invariant))
    return records


def leaf_controls():
    records = []
    # Single odd cycles, leaf cycles with bridges, and a central cycle avoiding 3.
    for n, h in product((3, 5, 7), range(3)):
        vs = [f'v{i}' for i in range(n)]
        es = {edge(vs[i], vs[(i+1) % n]) for i in range(n)}
        lists = {v: {3, h} for v in vs}
        for with_bridge in (False, True):
            ws, edges, ls = vs.copy(), es.copy(), lists.copy()
            if with_bridge:
                k = min(U - {3, h})
                ws += ['w']
                edges.add(edge('v0', 'w'))
                ls['v0'] = {3, h, k}
                ls['w'] = {k}
            assert not list(colorings(ws, edges, ls))
            remain = set(ws) - set(vs[1:])
            re = {e for e in edges if set(e) <= remain}
            roots = {f['v0'] for f in colorings(remain, re, ls)}
            assert roots == {3, h}
            records.append(dict(cycle_length=n, palette=[3, h], bridge=with_bridge,
                                root_set=sorted(roots)))
    es = {edge(f'c{i}', f'c{j}') for i, j in combinations(range(3), 2)}
    ls = {f'c{i}': set(U) for i in range(3)}
    for i in range(3):
        tri = [f'c{i}', f'u{i}', f'v{i}']
        es |= {edge(u, v) for u, v in combinations(tri, 2)}
        ls[f'u{i}'] = ls[f'v{i}'] = {2, 3}
    assert not list(colorings(ls, es, ls))
    remain = set(ls) - {'u0', 'v0'}
    roots = {f['c0'] for f in colorings(remain, {e for e in es if set(e) <= remain}, ls)}
    assert roots == {2, 3}
    records.append(dict(kind='central palette 01 with three shared leaf triangles 23',
                        edges=sorted(es), lists={v: sorted(s) for v, s in ls.items()},
                        root_set=sorted(roots)))
    return records


def minor(side, count, kind, length):
    es = {edge(f'b{i}', f'b{(i+1)%5}') for i in range(5)}
    es |= {edge('z', 'b1'), edge('z', 'b2')}
    dv = ['d0', 'd1', 'd2']
    es |= {edge('z', 'd0'), edge('d0', 'd1'), edge('d1', 'd2'), edge('d2', 'b4')}
    dp = ['d0'] if count == 2 else ['d0', 'd2']
    es |= {edge('z', v) for v in dp}
    hubs = [{'b0'}, {'b1'}, {'z', 'b4', *dv}] if side == 'left' else [
        {'b2'}, {'b3'}, {'z', 'b4', *dv}]
    targets = [min(hubs[0]), min(hubs[1]), 'b4']
    if kind == 'bridge3':
        w0 = [f'u{i}' for i in range(length)]
        w1 = [f'v{i}' for i in range(length)]
        for w in (w0, w1):
            es |= {edge(a, b) for a, b in zip(w, w[1:])}
            es |= {edge(w[-1], t) for t in targets}
        es.add(edge(w0[0], w1[0]))
        av = set(w0 + w1)
        ap = [w0[0]] if count == 1 else [w0[0], w1[0]]
        groups = [set(w0), set(w1), *hubs]
    else:
        h = int(kind[-1])
        k, l = sorted(U - {3, h})
        cycle = ['x'] + [f'v{i}' for i in range(length-1)]
        es |= {edge(cycle[i], cycle[(i+1) % length]) for i in range(length)}
        w = ['x', 'w0', 'w1']
        es |= {edge(a, b) for a, b in zip(w, w[1:])}
        for v in cycle[1:] + ['w1']:
            es |= {edge(v, targets[c]) for c in (k, l)}
        av = set(cycle + w)
        ap = ['w0'] if count == 1 else ['w0', 'w1']
        groups = [{cycle[1]}, set(cycle[2:]), set(w), hubs[k], hubs[l]]
    es |= {edge('z', v) for v in ap}
    assert connected(av, es) and connected(set(dv), es)
    assert not any(edge(a, d) in es for a in av for d in dv)
    for vertices, ports in ((av, ap), (set(dv), dp)):
        assert {v for v in vertices if edge(v, 'z') in es} == set(ports)
    assert len(ap) + len(dp) == 3
    assert sum(map(len, groups)) == len(set().union(*groups))
    assert all(connected(g, es) for g in groups)
    adj = []
    for i, j in combinations(range(5), 2):
        e = next((edge(u, v) for u in sorted(groups[i]) for v in sorted(groups[j])
                  if edge(u, v) in es), None)
        assert e is not None
        adj.append(dict(pair=[i, j], edge=e))
    comps = [dict(vertices=sorted(av), contacts=ap, role='A'),
             dict(vertices=dv, contacts=dp, role='D')]
    comps.sort(key=lambda c: -len(c['contacts']))
    return dict(side=side, order='I' if count == 2 else 'II', kind=kind, length=length,
                edges=sorted(es), branch_sets=[sorted(g) for g in groups], adjacency=adj,
                C2=comps[0], C1=comps[1], other_path=['z', *dv, 'b4'],
                scope='extracted-shape subgraph; degrees and forbidden sets not asserted')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    supports, leaves, relations = support_checks(), leaf_controls(), controls()
    minors = [minor(side, count, kind, n)
              for side, count in product(('left', 'right'), (2, 1))
              for kind in ('bridge3', 'cycle0', 'cycle1', 'cycle2')
              for n in ((1, 2, 5) if kind == 'bridge3' else (3, 5, 7, 9))]
    result = dict(supports=supports, leaf_controls=leaves, relation_controls=relations,
                  minors=minors, summary=dict(orders=2, support_checks=len(supports),
                      leaf_controls=len(leaves), full_relation_rows=480,
                      q_edge_deletions=sum(len(c['q_edge_deletions']) for c in relations),
                      K5_certificates=len(minors)))
    payload = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.check:
        assert OUT.read_text() == payload, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
