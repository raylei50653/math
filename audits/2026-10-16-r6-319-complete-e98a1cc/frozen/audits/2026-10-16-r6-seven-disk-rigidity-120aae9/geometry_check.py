#!/usr/bin/env python3
"""Independent finite controls. Synthetic disks only; no source supplied."""
import argparse
import collections
import copy
import hashlib
import itertools
import json
import random
from pathlib import Path


def edge(a, b):
    return (min(a, b), max(a, b))


def connected(vertices, edges):
    if not vertices:
        return True
    adj = {v: set() for v in vertices}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    reached = {next(iter(vertices))}
    todo = list(reached)
    while todo:
        for w in adj[todo.pop()] - reached:
            reached.add(w)
            todo.append(w)
    return reached == set(vertices)


def five_vertex_controls():
    """Every connected n=5,e=6 all-bounded-triangle core has two triangles.

    Enumerate all labelled edge sets. For their only possible core shapes,
    construct the full six-step exterior face walk, including repetitions.
    The checks are necessary collar conditions, not claimed sufficient ones.
    """
    candidates = []
    counts = collections.Counter()
    pairs = list(itertools.combinations(range(5), 2))
    for chosen in itertools.combinations(pairs, 6):
        E = set(chosen)
        if not connected(range(5), E):
            continue
        triangles = [t for t in itertools.combinations(range(5), 3)
                     if all(edge(a, b) in E for a, b in itertools.combinations(t, 2))]
        if len(triangles) != 2:
            continue
        degree = {v: sum(v in e for e in E) for v in range(5)}
        shared = set(triangles[0]) & set(triangles[1])
        if len(shared) == 1:
            c = next(iter(shared))
            ends = [sorted(set(t) - {c}) for t in triangles]
            walk = [c] + ends[0] + [c] + ends[1]
            shape = 'bowtie'
        else:
            assert len(shared) == 2
            leaf = next(v for v in range(5) if degree[v] == 1)
            attach = next(v for v in range(5) if edge(v, leaf) in E)
            contour_edges = E - {edge(*sorted(shared)), edge(leaf, attach)}
            contour_adj = {v: set() for v in range(5) if v != leaf}
            for a, b in contour_edges:
                contour_adj[a].add(b)
                contour_adj[b].add(a)
            outer = [attach]
            prev, current = None, attach
            while True:
                nxt = min(contour_adj[current] - ({prev} if prev is not None else set()))
                if nxt == attach:
                    break
                outer.append(nxt)
                prev, current = current, nxt
            assert len(outer) == 4
            walk = [attach, leaf] + outer
            shape = 'diamond_leaf_shared' if degree[attach] == 4 else 'diamond_leaf_outer'
        assert len(walk) == 6
        assert all(edge(walk[k], walk[(k + 1) % 6]) in E for k in range(6))
        occurrence = collections.Counter(walk)
        boundary_neighbours = {v: 5 - degree[v] for v in range(5)}
        corner_feasible = all(boundary_neighbours[v] >= occurrence[v] for v in range(5))
        possible_parities = []
        required_owners = {v for v in range(5) if boundary_neighbours[v] > occurrence[v]}
        for p in (0, 1):
            owners = {walk[k] for k in range(p, 6, 2)}
            if corner_feasible and required_owners <= owners:
                possible_parities.append(p)
        assert not possible_parities
        counts[shape] += 1
        candidates.append(dict(edges=sorted(E), triangles=triangles, outer_walk=walk,
                               shape=shape, degree=degree,
                               boundary_neighbours=boundary_neighbours,
                               corner_feasible=corner_feasible,
                               required_owners=sorted(required_owners),
                               possible_owner_parities=possible_parities))
    assert counts == dict(bowtie=15, diamond_leaf_shared=60, diamond_leaf_outer=60)
    return dict(scope='labelled five-interior core necessary collar constraints',
                counts=dict(counts), candidates=candidates, survivors=0)


def local_patch():
    # Core A,B,C = 7,8,9; ears a,b,c = 10,11,12. Outer Q is 0..6.
    E = {edge(a, b) for a, b in [(7, 8), (8, 9), (9, 7),
                                (10, 7), (10, 8), (11, 8), (11, 9),
                                (12, 9), (12, 7)]}
    owners = [10, 10, 11, 11, 12, 12, 12]
    bridge = {frozenset((10, 11)): 8, frozenset((11, 12)): 9,
              frozenset((12, 10)): 7}
    for u in range(7):
        E.add(edge(u, (u + 1) % 7))
        a, b = owners[(u - 1) % 7], owners[u]
        E.update((edge(u, a), edge(u, b)))
        if a != b:
            E.add(edge(u, bridge[frozenset((a, b))]))
    V = set(range(13))
    adj = {v: {w for e in E if v in e for w in e if w != v} for v in V}
    triangles = sorted(t for t in itertools.combinations(V, 3)
                       if all(edge(a, b) in E for a, b in itertools.combinations(t, 2)))
    assert len(triangles) == 17
    incidence = collections.defaultdict(list)
    for i, t in enumerate(triangles):
        for a, b in itertools.combinations(t, 2):
            incidence[edge(a, b)].append(i)
    Qedges = {edge(u, (u + 1) % 7) for u in range(7)}
    assert set(incidence) == E
    assert all(len(fs) == (1 if e in Qedges else 2) for e, fs in incidence.items())
    DE = {edge(*fs) for fs in incidence.values() if len(fs) == 2}
    ports = [incidence[edge(u, (u + 1) % 7)][0] for u in range(7)]
    assert len(set(ports)) == 7
    Dadj = {v: {w for e in DE if v in e for w in e if w != v} for v in range(17)}
    assert all(len(Dadj[v]) == (2 if v in ports else 3) for v in range(17))
    assert connected(range(17), DE)
    c4 = [list(S) for S in itertools.combinations(V, 4)
          if all(len(adj[v] & set(S)) == 2 for v in S)]
    assert c4 == []
    c5 = [list(S) for S in itertools.combinations(V, 5)
          if all(len(adj[v] & set(S)) == 2 for v in S)]
    links = {tuple(sorted(adj[v])): v for v in range(7, 13) if len(adj[v]) == 5}
    assert len(c5) == 5 and {tuple(S) for S in c5} == set(links)
    return dict(vertices=sorted(V), edges=sorted(E), faces=triangles,
                degrees={v: len(adj[v]) for v in V}, boundary=list(range(7)),
                boundary_t=[len(adj[v] - set(range(7))) for v in range(7)],
                induced_C4=c4,
                induced_C5=[dict(cycle=S, full_W5_centre=links[tuple(S)]) for S in c5],
                dual_edges=sorted(DE), dual_ports=ports)


def all_matchings(vertices, edges, rng):
    adj = {v: set() for v in vertices}
    for a, b in edges:
        if a in adj and b in adj:
            adj[a].add(b)
            adj[b].add(a)
    def recurse(remaining):
        if not remaining:
            yield ()
            return
        v = min(remaining, key=lambda w: (len(adj[w] & remaining), w))
        neighbours = sorted(adj[v] & remaining)
        rng.shuffle(neighbours)
        for w in neighbours:
            for rest in recurse(remaining - {v, w}):
                yield tuple(sorted((edge(v, w),) + rest))
    return sorted(set(recurse(set(vertices))))


def complement_data(matching, patch):
    E = set(map(tuple, patch['dual_edges'])) - set(matching)
    adj = {v: set() for v in range(17)}
    for a, b in E:
        adj[a].add(b)
        adj[b].add(a)
    remaining = set(range(17))
    components = []
    while remaining:
        seed = min(remaining)
        component = {seed}
        todo = [seed]
        while todo:
            for w in adj[todo.pop()] - component:
                component.add(w)
                todo.append(w)
        remaining -= component
        ends = sorted(v for v in component if len(adj[v]) == 1)
        assert len(ends) in (0, 2)
        start = ends[0] if ends else min(component)
        walk = [start]
        prev, cur = None, start
        while True:
            options = sorted(adj[cur] - ({prev} if prev is not None else set()))
            if not options:
                break
            nxt = options[0]
            if nxt == start:
                break
            walk.append(nxt)
            prev, cur = cur, nxt
        assert set(walk) == component
        length = len(walk) - 1 if ends else len(walk)
        components.append(dict(kind='path' if ends else 'cycle', vertices=walk,
                               edges=length, parity=length % 2))
    return components


def build(seed):
    rng = random.Random(seed)
    patch = local_patch()
    E = list(map(tuple, patch['dual_edges']))
    full_vertices = set(range(17))
    fc = []
    for deleted in range(17):
        matchings = all_matchings(full_vertices - {deleted}, E, rng)
        assert matchings
        fc.append(dict(deleted_vertex=deleted, matchings=matchings))
    fibres = []
    for mask in range(128):
        A = [i for i in range(7) if mask & (1 << i)]
        deleted = {patch['dual_ports'][j] for j in A}
        matchings = all_matchings(full_vertices - deleted, E, rng)
        if len(A) % 2 == 0:
            assert not matchings
        if len(A) == 1:
            assert matchings
        fibres.append(dict(selected_ports=A, deleted_vertices=sorted(deleted),
                           matchings=[dict(edges=M, complement=complement_data(M, patch))
                                      for M in matchings]))
    return dict(kind='synthetic finite controls; actual sources supplied: zero',
                five_interior_control=five_vertex_controls(), synthetic_patch=patch,
                factor_critical_full_deletion_fibres=fc, full_ordered_port_fibres=fibres)


def verify(certificate):
    expected = build(0)
    assert certificate == json.loads(json.dumps(expected)), 'certificate differs from independent reconstruction'
    for fibre in certificate['full_ordered_port_fibres']:
        A = fibre['selected_ports']
        ports = certificate['synthetic_patch']['dual_ports']
        unmatched_ports = {ports[j] for j in range(7) if j not in A}
        for lift in fibre['matchings']:
            edges = lift['edges']
            covered = [v for e in edges for v in e]
            expected_vertices = set(range(17)) - set(fibre['deleted_vertices'])
            assert len(covered) == len(set(covered)) and set(covered) == expected_vertices
            endpoint_set = {v for comp in lift['complement'] if comp['kind'] == 'path'
                            for v in (comp['vertices'][0], comp['vertices'][-1])}
            assert endpoint_set == unmatched_ports
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--certificate', type=Path)
    parser.add_argument('--verify', type=Path)
    parser.add_argument('--negative', action='store_true')
    args = parser.parse_args()
    if args.verify:
        cert = json.loads(args.verify.read_text())
    else:
        cert = json.loads(json.dumps(build(args.seed)))
    if args.negative:
        corrupted = []
        bad = copy.deepcopy(cert)
        bad['synthetic_patch']['boundary_t'][0] += 2
        corrupted.append(('boundary incidence', bad))
        bad = copy.deepcopy(cert)
        fibre = next(f for f in bad['full_ordered_port_fibres'] if f['matchings'])
        fibre['matchings'].pop()
        corrupted.append(('omitted complete matching lift', bad))
        bad = copy.deepcopy(cert)
        fibre = next(f for f in bad['full_ordered_port_fibres'] if not f['matchings'])
        fibre['matchings'].append(dict(edges=[], complement=[]))
        corrupted.append(('false nonempty fibre', bad))
        rejected = []
        for name, bad in corrupted:
            try:
                verify(bad)
            except AssertionError:
                rejected.append(name)
            else:
                raise AssertionError('corrupted certificate was accepted: ' + name)
        print(json.dumps(dict(negative_control='PASS', rejected=rejected)))
        return
    verify(cert)
    payload = (json.dumps(cert, sort_keys=True, separators=(',', ':')) + '\n').encode()
    if args.certificate:
        with args.certificate.open('xb') as stream:
            stream.write(payload)
    print(json.dumps(dict(result='PASS', source_instances=0, actual_source_status='not triggered',
                          five_interior_core_candidates=135, five_interior_survivors=0,
                          synthetic_dual_vertices=17, synthetic_factor_critical_vertices=17,
                          ordered_port_fibres=128,
                          empty_port_fibres=sum(not f['matchings'] for f in cert['full_ordered_port_fibres']),
                          matching_lifts=sum(len(f['matchings']) for f in cert['full_ordered_port_fibres']),
                          sha256=hashlib.sha256(payload).hexdigest()), sort_keys=True))


if __name__ == '__main__':
    main()
