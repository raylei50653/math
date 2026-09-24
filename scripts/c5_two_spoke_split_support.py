#!/usr/bin/env python3
"""Split-support all-row certificate; finite forms justified in the report.

Generation uses NetworkX. --check replays saved rotations/subdivisions without
a planarity oracle. No general graph enumeration or marginal contact products.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from c5_degree5_two_spoke_sectors import Q, ROWS, U
from c5_two_spoke_middle_21 import colorings, relation, forbidden
from c5_two_spoke_reflection import faces, row_image, RHO, PI

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_two_spoke_split_support/observations.json'
CYCLE = {tuple(sorted((i, (i+1) % 5))) for i in range(5)}
P = (0, 1, 2, 0, 1)
TRIPLE = (0, 1, 2, 3, 1)


def edge(u, v):
    return tuple(sorted((u, v)))


def topology_check(es, cert):
    if 'rotation' in cert:
        rot = cert['rotation']
        assert {edge(u, v) for u, ns in enumerate(rot) for v in ns} == es
        assert len(rot) - len(es) + len(faces(rot)) == 2
        return True
    branches = set(cert['branch_vertices'])
    interiors, used, links = set(), set(), set()
    for path in cert['paths']:
        assert len(path) >= 2 and len(set(path)) == len(path)
        assert path[0] in branches and path[-1] in branches
        mid = set(path[1:-1])
        assert not mid & (branches | interiors)
        interiors |= mid
        link = edge(path[0], path[-1])
        assert link not in links
        links.add(link)
        for u, v in zip(path, path[1:]):
            e = edge(u, v)
            assert e in es and e not in used
            used.add(e)
    if cert['model'] == 'K5':
        assert len(branches) == 5 and links == set(combinations(sorted(branches), 2))
    else:
        assert cert['model'] == 'K3,3' and len(branches) == 6
        assert any(links == {edge(u, v) for u in side for v in branches-set(side)}
                   for side in combinations(branches, 3))
    return False


def get_topology(es, n, old, pool):
    if old is not None:
        topology_check(es, old)
        return old
    for cert in pool:
        needed = {edge(u, v) for p in cert['paths'] for u, v in zip(p, p[1:])}
        if needed <= es:
            return cert
    import networkx as nx
    from c5_odd_join_cores import kuratowski_certificate
    graph = nx.Graph(sorted(es))
    planar, emb = nx.check_planarity(graph)
    if planar:
        cert = dict(rotation=[list(emb.neighbors_cw_order(v)) for v in range(n)])
    else:
        cert = kuratowski_certificate(graph)
        pool.append(cert)
    topology_check(es, cert)
    return cert


def templates():
    yield 'triangle', list(range(5, 8)), {(5, 6), (5, 7), (6, 7)}
    yield 'two_triangles', list(range(5, 11)), {
        (5, 6), (5, 7), (6, 7), (5, 8), (8, 9), (8, 10), (9, 10)}


def a_forms(saved):
    records, counts, pool = [], Counter(), []
    old = saved['A_forms'] if saved else None
    for kind, vs, es in templates():
        opts = [[s for s in combinations(range(4), 4-sum(v in e for e in es))
                 if len({Q[i] for i in s}) == len(s)] for v in vs]
        for aa in product(*opts):
            att = dict(zip(vs, aa))
            ports = [v for v in vs if 0 in att[v]]
            if len(ports) not in (1, 2) or set().union(*map(set, aa)) != set(range(4)):
                continue
            counts[kind + '_degree_support'] += 1
            if relation(vs, es, att, [], Q):
                continue
            counts[kind + '_q_rejecting'] += 1
            apex = max(vs)+1
            padded = es | CYCLE | {edge(v, b) for v in vs for b in att[v]}
            ae = padded | {(b, apex) for b in range(5)}
            prior = old[len(records)]['topology'] if old is not None else None
            cert = get_topology(ae, apex+1, prior, pool)
            record = dict(kind=kind, padded_attachments=aa, contacts=ports,
                          interior_edges=sorted(es), topology=cert)
            if topology_check(ae, cert):
                counts[kind + '_disk'] += 1
                # Padded boundary (z,b3,b2,b1,dummy); only A is retained.
                actual = {v: sorted({1: 3, 2: 2, 3: 1}[b] for b in att[v] if b != 0)
                          for v in vs}
                seed_rows = (Q, TRIPLE)
                seeds = [relation(vs, es, actual, ports, b) for b in seed_rows]
                assert forbidden(seeds[0]) == [0] and forbidden(seeds[1]) == []
                rows = []
                for b in ROWS:
                    r = relation(vs, es, actual, ports, b)
                    expected = [b[2]] if b[1] == b[3] else []
                    assert forbidden(r) == expected
                    source = 0 if b[1] == b[3] else 1
                    perms = [p for p in permutations(range(4))
                             if all(p[seed_rows[source][i]] == b[i] for i in (1, 2, 3))]
                    assert perms
                    assert all(sorted(tuple(p[c] for c in t) for t in seeds[source]) == r
                               for p in perms)
                    ra = {v: [RHO[i] for i in actual[v]] for v in vs}
                    rr = relation(vs, es, ra, ports, row_image(b))
                    assert rr == sorted(tuple(PI[c] for c in t) for t in r)
                    # Independent fixed-hub list queries, at every colour.
                    for a in U:
                        lists = {v: U-{b[i] for i in actual[v]}-({a} if v in ports else set())
                                 for v in vs}
                        assert bool(next(colorings(vs, es, lists), None)) == (a not in expected)
                    rows.append(dict(boundary=b, tuples=r, forbidden=expected))
                deletions = []
                all_vs = list(range(apex))
                lists = {v: U for v in all_vs} | {i: {Q[i]} for i in range(5)}
                for e in sorted(padded-CYCLE):
                    f = next(colorings(all_vs, padded-{e}, lists), None)
                    assert f is not None
                    deletions.append(dict(edge=e, coloring=f))
                record.update(attachments=actual, rows=rows, seed_relations=seeds,
                              padded_q_edge_deletions=deletions)
                counts['full_A_rows'] += len(rows)
                counts['A_contacts_' + str(len(ports))] += 1
            records.append(record)
    if old is not None:
        assert len(old) == len(records)
    assert counts['triangle_disk'] == 24 and counts['two_triangles_disk'] == 40
    assert counts['A_contacts_1'] == 12 and counts['A_contacts_2'] == 52
    return records, counts


def d_exceptional_forms():
    records = []
    # z=5 is a non-bridge triangle vertex (two original contacts).
    forms = [('triangle', [6, 7], {(6, 7)}) ,
             ('two_triangles', list(range(6, 11)),
              {(6, 7), (6, 8), (8, 9), (8, 10), (9, 10)})]
    for kind, vs, es in forms:
        ports = [6, 7]
        opts = [list(combinations((0, 1, 4),
                                 4-sum(v in e for e in es)-int(v in ports))) for v in vs]
        for aa in product(*opts):
            att = dict(zip(vs, aa))
            qr = relation(vs, es, att, ports, Q)
            pr = relation(vs, es, att, ports, P)
            fq, fp = forbidden(qr), forbidden(pr)
            assert not (fq == [3] and fp == [2, 3])
            records.append(dict(kind=kind, vertices=vs, edges=sorted(es), contacts=ports,
                                attachments=att, q_tuples=qr, p_tuples=pr,
                                q_forbidden=fq, p_forbidden=fp))
    assert len(records) == 252
    return records


def row_table():
    rows = []
    orbit = {tuple(p[c] for c in Q) for p in permutations(range(4))}
    for b in ROWS:
        fa = {b[2]} if b[1] == b[3] else set()
        fd = U-{b[0], b[1], b[4]} if b[1] != b[4] else set()
        z = U-{b[3], b[4]}-fa-fd
        assert bool(z) == (b not in orbit)
        rb = row_image(b)
        rfa = {rb[1]} if rb[0] == rb[2] else set()
        rfd = U-{rb[2], rb[3], rb[4]} if rb[2] != rb[4] else set()
        rz = U-{rb[4], rb[0]}-rfa-rfd
        assert rz == {PI[a] for a in z}
        rows.append(dict(boundary=b, A_forbidden=sorted(fa), D_forbidden=sorted(fd),
                         z_colors=sorted(z), reflected_boundary=rb,
                         reflected_z_colors=sorted(rz)))
    return rows


def run(saved):
    # This is a small audit of the cited canonical-tail coverage, not a rerun
    # of its 177,280-lift topology classification.
    tail_path = ROOT / 'artifacts/c5_triangle_branches/observations.json'
    bases = json.loads(tail_path.read_text())['disk_templates']
    assert len(bases) == 18
    assert all(any(4 in ns for ns in b['neighborhoods']) for b in bases)
    forms, counts = a_forms(saved)
    exceptional = d_exceptional_forms()
    rows = row_table()
    prior_path = ROOT / 'artifacts/c5_two_spoke_reflection/observations.json'
    prior = json.loads(prior_path.read_text())
    table = {tuple(r['boundary']): r for r in rows}
    controls = []
    for w in prior['controls']:
        if w['spokes'] != [3, 4]:
            continue
        for r in w['rows']:
            target = table[tuple(r['boundary'])]
            assert r['C2']['forbidden'] == target['A_forbidden']
            assert r['C1']['forbidden'] == target['D_forbidden']
            assert r['allowed'] == target['z_colors']
        controls.append(w['source_index'])
    dependencies = [tail_path, prior_path,
                    ROOT/'artifacts/c5_multi_odd_cycles/observations.json',
                    ROOT/'artifacts/c5_triangle_forks/observations.json',
                    ROOT/'artifacts/c5_triangle_path_reduction/observations.json',
                    ROOT/'artifacts/c5_two_triangle_blocks/observations.json',
                    ROOT/'Math/TwoSpokeReflection.lean', Path(__file__)]
    counts.update(D_exceptional_forms=len(exceptional), labelled_rows=len(rows),
                  accepted_rows=sum(bool(r['z_colors']) for r in rows),
                  rejected_rows=sum(not r['z_colors'] for r in rows),
                  inherited_tail_bases=len(bases), existing_source_controls=len(controls))
    return dict(scope='all-row split-support theorem with inherited arbitrary-size reduction',
                source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                               for p in dependencies},
                A_forms=forms, D_exceptional_forms=exceptional, rows=rows,
                existing_source_controls=controls, summary=dict(counts))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    saved = json.loads(OUT.read_text()) if args.check else None
    result = run(saved)
    payload = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.check:
        assert OUT.read_text() == payload, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
