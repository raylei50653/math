#!/usr/bin/env python3
"""Local algebra and source-shaped K5 certificates for S={b0,b1}, (2,1).

No graph catalogue or inference of arbitrary-length topology from samples.
"""
import argparse
from itertools import combinations, permutations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_two_spoke_adjacent_21/observations.json'
U = frozenset(range(4))
Q = (0, 1, 0, 1, 2)


def support_table():
    records = []
    for size in range(6):
        for attached in combinations(range(5), size):
            stabilizer = [p for p in permutations(range(4))
                          if all(p[Q[i]] == Q[i] for i in attached)]
            fixed = [a for a in (2, 3) if all(p[a] == a for p in stabilizer)]
            if 2 in fixed:
                assert 4 in attached
            if 3 in fixed:
                assert {Q[i] for i in attached} == {0, 1, 2}
            if set(attached) <= {0, 4}:
                assert 3 not in fixed
            records.append(dict(attachments=attached, possible_singletons=fixed))
    return records


def transport_table():
    records = []
    for b in product(range(4), repeat=5):
        if any(b[i] == b[(i+1) % 5] for i in range(5)):
            continue
        ps = [p for p in permutations(range(4)) if p[0] == b[0] and p[2] == b[4]]
        assert ps and {p[2] for p in ps} == {b[4]}
        available = U - {b[0], b[1]}
        # The other component stays distinct; its forbidden set is not renamed.
        for mask in range(16):
            other = {a for a in U if mask & (1 << a)}
            assert available - ({b[4]} | other) == U - {b[0], b[1], b[4]} - other
        records.append(dict(boundary=b, short_forbidden=[b[4]],
                            permutations=ps, other_masks_checked=16))
    assert len(records) == 240
    return records


def local_palettes():
    # Once K4 is excluded and 1/3 membership agrees, only these blocks remain.
    options = [frozenset({0}), frozenset({2}), frozenset({1, 3})]
    records = []
    for external in (frozenset(), frozenset({0}), frozenset({2}), frozenset({0, 2})):
        for flags in product((0, 1), repeat=3):
            palettes = [p for p, flag in zip(options, flags) if flag]
            total = sum(map(len, palettes)) + len(external)
            union = external.union(*palettes)
            if total != 4 or union != U:
                continue
            assert palettes.count(frozenset({1, 3})) == 1
            directions = sorted(list(external) + [next(iter(p)) for p in palettes if len(p) == 1])
            assert directions == [0, 2]
            records.append(dict(external_colors=sorted(external),
                                palettes=[sorted(p) for p in palettes],
                                tether_colors=directions))
    assert len(records) == 4
    return records


def coloring_controls():
    """Actual short-component list graphs, not planar full-core witnesses."""
    records = []
    for k in (1, 2):
        attachments = [[0] if i < k else [0, 4] for i in range(3)]
        rows = []
        for b in product(range(4), repeat=5):
            if any(b[i] == b[(i+1) % 5] for i in range(5)):
                continue
            tuples = set()
            for colors in permutations(range(4), 3):
                if all(colors[i] not in {b[j] for j in attachments[i]} for i in range(3)):
                    tuples.add(colors[:k])
            forbidden = [a for a in U if not any(all(c != a for c in t) for t in tuples)]
            assert forbidden == [b[4]]
            rows.append(dict(boundary=b, tuples=sorted(tuples), forbidden=forbidden))
        qrow = next(r for r in rows if tuple(r['boundary']) == Q)
        if k == 2:
            marginals = [{t[i] for t in qrow['tuples']} for i in range(k)]
            assert all(s - {2} for s in marginals)
            assert not any(all(c != 2 for c in t) for t in qrow['tuples'])
        records.append(dict(contacts=list(range(k)), triangle=[0, 1, 2],
                            attachments=attachments, rows=rows))
    return records


def edge(a, b):
    return tuple(sorted((a, b)))


def connected(vertices, edges):
    reached = {min(vertices)}
    while True:
        more = reached | {v for u in reached for v in vertices if edge(u, v) in edges}
        if more == reached:
            return reached == set(vertices)
        reached = more


def minor(n, short_contacts, subdivisions, other_length):
    es = {edge(f'b{i}', f'b{(i+1)%5}') for i in range(5)}
    es |= {edge('z', 'b0'), edge('z', 'b1')}
    cycle = [f'v{i}' for i in range(n)]
    es.update(edge(cycle[i], cycle[(i+1) % n]) for i in range(n))
    other = [f'w{i}' for i in range(other_length)]
    es.update(edge(a, b) for a, b in zip(other, other[1:]))
    es |= {edge('z', other[0]), edge(other[-1], 'b4')}
    other_contacts = [other[0]]
    if short_contacts == 1:
        es.add(edge('z', other[-1]))
        other_contacts.append(other[-1])
    groups = [{'b0'}, {'z', 'b4', *other}, {cycle[0]}, {cycle[1]}, set(cycle[2:])]
    short_vertices = set(cycle)
    ports = []
    tethers = []
    for i, v in enumerate(cycle):
        for color in (0, 2):
            target = 'b0' if color == 0 else ('z' if i < short_contacts else 'b4')
            inside = [f't{i}_{color}_{j}' for j in range(subdivisions)]
            path = [v, *inside, target]
            es.update(edge(a, b) for a, b in zip(path, path[1:]))
            short_vertices.update(inside)
            groups[color // 2].update(inside)
            if target == 'z':
                ports.append(path[-2])
            tethers.append(dict(color=color, path=path))
    assert len(ports) == short_contacts and len(other_contacts) == 3-short_contacts
    assert connected(short_vertices, es) and connected(set(other), es)
    assert not any(edge(u, v) in es for u in short_vertices for v in other)
    for vertices, named_ports in ((short_vertices, ports), (set(other), other_contacts)):
        assert {v for v in vertices if edge(v, 'z') in es} == set(named_ports)
    assert sum(map(len, groups)) == len(set().union(*groups))
    assert all(connected(g, es) for g in groups)
    adjacency = []
    for i, j in combinations(range(5), 2):
        witness = next((edge(u, v) for u in sorted(groups[i]) for v in sorted(groups[j])
                        if edge(u, v) in es), None)
        assert witness is not None
        adjacency.append(dict(pair=[i, j], edge=witness))
    components = [dict(vertices=sorted(short_vertices), ports=ports, extraction_forbidden=[2]),
                  dict(vertices=other, ports=other_contacts, extraction_forbidden=[3])]
    # Forbidden labels describe the extraction roles, not computed lists of this
    # deliberately incomplete subgraph. Keep the original C2/C1 names separate.
    components.sort(key=lambda c: -len(c['ports']))
    return dict(odd_cycle_length=n, components=dict(C2=components[0], C1=components[1]),
                tethers=tethers, other_path=['z', *other, 'b4'], edges=sorted(es),
                branch_sets=[sorted(g) for g in groups], adjacency=adjacency)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    support = support_table()
    transport = transport_table()
    local = local_palettes()
    controls = coloring_controls()
    minors = [minor(n, k, subdivisions, length)
              for n, k, subdivisions, length in product((3, 5, 7, 9), (1, 2), (0, 1, 3), (2, 4))]
    result = dict(scope='finite local algebra and minor subgraphs; general extraction is a paper proof',
                  supports=support, transports=transport, local_palettes=local,
                  coloring_controls=controls, minors=minors,
                  summary=dict(support_subsets=len(support), boundary_rows=len(transport),
                               join_checks=240*16, local_palette_states=len(local),
                               K5_certificates=len(minors), forbidden_orders=2,
                               full_relation_control_rows=240*len(controls)))
    payload = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.check:
        assert OUT.read_text() == payload, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
