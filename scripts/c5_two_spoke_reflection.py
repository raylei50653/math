#!/usr/bin/env python3
"""q-preserving transport and next-orbit controls; no graph enumeration."""
import argparse
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path

from c5_degree5_two_spoke_sectors import Q, U, ROWS
from c5_two_spoke_middle_21 import relation, forbidden, colorings

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_two_spoke_reflection/observations.json'
RHO = (3, 2, 1, 0, 4)
PI = (1, 0, 2, 3)


def row_image(b):
    return tuple(PI[b[RHO[i]]] for i in range(5))


def reflect_vertex(v):
    return RHO[v] if v < 5 else v


def faces(rotation):
    seen, result = set(), []
    for u, ns in enumerate(rotation):
        assert len(ns) == len(set(ns)) and u not in ns
        for v in ns:
            assert u in rotation[v]
            if (u, v) in seen:
                continue
            face, a, b = [], u, v
            while (a, b) not in seen:
                seen.add((a, b))
                face.append(a)
                ring = rotation[b]
                a, b = b, ring[(ring.index(a) - 1) % len(ring)]
            assert (a, b) == (u, v)
            result.append(face)
    return result


def support_screen():
    # Linear boundary order of the long region, with z at both ends.
    order = (3, 2, 1, 0, 4)
    pos = {v: i for i, v in enumerate(order)}
    supports = [set(s) for n in range(1, 6) for s in combinations(range(5), n)]
    records = []
    for a in supports:
        for d in supports:
            if not ({Q[i] for i in a} >= {0} and {Q[i] for i in d} == {0, 1, 2}):
                continue
            # D touches b4, the rightmost point. Disjoint connected components,
            # each joined to z, must have nonoverlapping support intervals.
            if max(pos[i] for i in a) > min(pos[i] for i in d):
                continue
            if 2 in d:
                assert a <= {2, 3}
                reason = 'existing_two_hub_extraction: Q_D to b2, hub1=b3'
            else:
                assert d == {0, 1, 4} and a <= {1, 2, 3} and 2 in a
                if a <= {1, 2}:
                    reason = 'existing_two_hub_extraction: hub0=z-b3-b2, hub1=b1'
                elif a <= {2, 3}:
                    reason = 'existing_two_hub_extraction: hub0=Q_D(z,b0)-b1-b2, hub1=b3'
                else:
                    assert a == {1, 2, 3}
                    reason = 'retained_support_only'
            record = dict(A=sorted(a), D=sorted(d), result=reason)
            if reason != 'retained_support_only':
                # Vertex 6 denotes the interior of the actual simple D path,
                # suppressed only for this finite exterior-incidence control.
                if 2 in d:
                    path, one = [5, 6, 2], 3
                elif a <= {1, 2}:
                    path, one = [5, 3, 2], 1
                else:
                    path, one = [5, 6, 0, 1, 2], 3
                zero = set(path)
                assert one not in zero
                assert {i for i in a if Q[i] == 0} | {5} <= zero
                assert {i for i in a if Q[i] == 1} <= {one}
                exterior_edges = {tuple(sorted((i, (i+1) % 5))) for i in range(5)}
                exterior_edges |= {(3, 5), (4, 5), (5, 6)}
                exterior_edges |= {tuple(sorted((6, i))) for i in d}
                assert all(tuple(sorted(e)) in exterior_edges for e in zip(path, path[1:]))
                assert any(tuple(sorted((i, one))) in exterior_edges for i in zero)
                record.update(X0_path=path, X1=[one],
                              scope='exterior path incidence; 6 suppresses a real D path')
            records.append(record)
    assert sum(r['result'] == 'retained_support_only' for r in records) == 1
    return records


def audit(w):
    es = {tuple(e) for e in w['edges']}
    vs = sorted({v for e in es for v in e})
    z = w['z']
    adj = {v: {y if x == v else x for x, y in es if v in (x, y)} for v in vs}
    spokes = sorted(adj[z] & set(range(5)))
    c5 = {tuple(sorted((i, (i+1) % 5))) for i in range(5)}
    assert {e for e in es if max(e) < 5} == c5
    assert all(len(adj[v]) == (5 if v == z else 4) for v in vs if v >= 5)
    pieces, unseen = [], set(vs) - set(range(5)) - {z}
    while unseen:
        comp, todo = set(), [min(unseen)]
        while todo:
            v = todo.pop()
            if v in comp:
                continue
            comp.add(v)
            todo.extend((adj[v] & unseen) - comp)
        unseen -= comp
        pieces.append((sorted(comp), sorted(comp & adj[z])))
    pieces.sort(key=lambda c: -len(c[1]))
    assert [len(p) for _, p in pieces] == [2, 1]
    rotation = w['apex_rotation']
    apex = len(rotation) - 1
    ae = es | {tuple(sorted((i, apex))) for i in range(5)}
    assert {tuple(sorted((u, v))) for u, ns in enumerate(rotation) for v in ns} == ae
    assert len(rotation) - len(ae) + len(faces(rotation)) == 2
    # Explicitly mirror the rotation, retaining the same apex and internal vertices.
    rr = [None] * len(rotation)
    for v, ns in enumerate(rotation):
        rr[reflect_vertex(v)] = [reflect_vertex(u) for u in reversed(ns)]
    re = {tuple(sorted((reflect_vertex(u), reflect_vertex(v)))) for u, v in es}
    assert {tuple(sorted((u, v))) for u, ns in enumerate(rr) for v in ns} == (
        re | {tuple(sorted((i, apex))) for i in range(5)})
    assert len(rr) - len(ae) + len(faces(rr)) == 2
    q_orbit = {tuple(p[c] for c in Q) for p in permutations(range(4))}
    rows = []
    for b in ROWS:
        parts, bans = [], []
        for vertices, ports in pieces:
            ce = {e for e in es if set(e) <= set(vertices)}
            att = {v: sorted(adj[v] & set(range(5))) for v in vertices}
            rel = relation(vertices, ce, att, ports, b)
            ra = {v: [RHO[i] for i in att[v]] for v in vertices}
            rrel = relation(vertices, ce, ra, ports, row_image(b))
            assert rrel == sorted(tuple(PI[x] for x in t) for t in rel)
            ban = forbidden(rel)
            assert forbidden(rrel) == sorted(PI[a] for a in ban)
            bans.append(set(ban))
            # The stated partial all-row laws, in the common frame.
            if spokes == [3, 4]:
                if len(ports) == 2 and b[1] == b[3]:
                    assert ban == [b[2]]
                if len(ports) == 1 and len({b[0], b[1], b[4]}) == 3:
                    assert set(ban) == U - {b[0], b[1], b[4]}
            parts.append(dict(vertices=vertices, contacts=ports, attachments=att,
                              tuples=rel, forbidden=ban))
        allowed = sorted(U - {b[i] for i in spokes} - set.union(*bans))
        lists = {v: U for v in vs} | {i: {b[i]} for i in range(5)}
        actual = sorted({f[z] for f in colorings(vs, es, lists)})
        assert actual == allowed
        assert bool(allowed) == (b not in q_orbit)
        if b == Q:
            missing = next(iter(U - {Q[i] for i in spokes} - {3}))
            assert bans == [{missing}, {3}]
            expected = ({1, 2, 3}, {0, 1, 4}) if spokes == [3, 4] else (
                {0, 1, 2}, {2, 3, 4})
            for (vertices, _), support in zip(pieces, expected):
                assert set.union(*(adj[v] & set(range(5)) for v in vertices)) == support
        rows.append(dict(boundary=b, reflected_boundary=row_image(b),
                         C2=parts[0], C1=parts[1], allowed=allowed))
    deletions = []
    lists = {v: U for v in vs} | {i: {Q[i]} for i in range(5)}
    for e in sorted(es - c5):
        f = next(colorings(vs, es - {e}, lists), None)
        assert f is not None
        rf = {reflect_vertex(v): PI[c] for v, c in f.items()}
        er = tuple(sorted(reflect_vertex(v) for v in e))
        assert all(rf[i] == Q[i] for i in range(5))
        assert all(rf[u] != rf[v] for u, v in re - {er})
        deletions.append(dict(edge=e, coloring=f, reflected_edge=er, reflected_coloring=rf))
    return dict(source_index=w['source_index'], spokes=spokes, edges=sorted(es),
                apex_rotation=rotation, reflected_apex_rotation=rr,
                q_edge_deletions=deletions, rows=rows,
                scope='existing disk witness; rejects exactly the 24 labelled q rows')


def run():
    assert row_image(Q) == Q
    assert all(row_image(row_image(b)) == b and row_image(b) in ROWS for b in ROWS)
    # Enumerate the stabilizer within D5 x S4, not arbitrary boundary permutations.
    symmetries = []
    for sign in (1, -1):
        for shift in range(5):
            r = tuple((shift + sign*i) % 5 for i in range(5))
            for p in permutations(range(4)):
                if all(p[Q[r[i]]] == Q[i] for i in range(5)):
                    symmetries.append(dict(boundary=r, colors=p))
    assert len(symmetries) == 2
    src = ROOT / 'artifacts/c5_degree5_two_spoke_sectors/observations.json'
    retained = [(i, r) for i, r in enumerate(json.loads(src.read_text())['records'])
                if r['ports'] == [2, 1] and r['result'] == 'retained']
    def key(r):
        return (tuple(r['spokes']), tuple(tuple(sorted(a)) for a in r['arcs']),
                tuple(tuple(b) for b in r['q_bans']))
    indices = {key(r): i for i, r in retained}
    mapping = []
    for i, r in retained:
        mapped = dict(spokes=sorted(RHO[x] for x in r['spokes']),
                      arcs=[[RHO[x] for x in a] for a in r['arcs']],
                      q_bans=[sorted(PI[x] for x in b) for b in r['q_bans']])
        j = indices[key(mapped)]
        mapping.append(dict(source=i, reflected=j, spokes=r['spokes'],
                            q_bans=r['q_bans'], reflected_bans=mapped['q_bans']))
    assert len(mapping) == 18
    assert all(next(s['reflected'] for s in mapping if s['source'] == r['reflected']) == r['source']
               for r in mapping)
    witness_path = ROOT / 'artifacts/c5_degree5_interfaces/observations.json'
    controls = []
    for w in json.loads(witness_path.read_text())['witnesses']:
        if not w['accepts_T4'] or w['port_partition'] != [2, 1]:
            continue
        z = w['z']
        s = sorted(v if u == z else u for u, v in w['edges'] if z in (u, v) and min(u, v) < 5)
        if s in ([3, 4], [0, 4]):
            controls.append(audit(w))
    assert len(controls) == 8
    supports = support_screen()
    return dict(scope='exact transport, necessary supports, existing positive controls; no general separation theorem',
                source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                               for p in (src, witness_path)},
                symmetries=symmetries, table_transport=mapping, support_screen=supports,
                controls=controls, summary=dict(stabilizer_size=2, table_entries=18,
                    cumulative_excluded=6, remaining_entries=12, next_adjacent_entries=4,
                    disk_controls=8, full_relation_rows=1920, reflected_component_rows=3840,
                    q_edge_deletions=sum(len(w['q_edge_deletions']) for w in controls),
                    support_pairs=len(supports)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = run()
    payload = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.check:
        assert OUT.read_text() == payload, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
