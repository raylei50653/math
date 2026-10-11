#!/usr/bin/env python3
"""Exact multiport interfaces for one degree-five vertex; no new graph catalog.

Replay existing disk witnesses, block-palette certificates and deletion erasure.
The arbitrary-size interface and minimality equivalences are paper proofs.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

import networkx as nx

from c5_cell_enumerator import REPS, T4
from c5_disk_deletions import BOUNDARY, CYCLE, faces_of
from c5_k4_blocks import coloring

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'artifacts/c5_tree_cores/observations.json'
OUT = ROOT / 'artifacts/c5_degree5_interfaces/observations.json'
U = frozenset(range(4))
Q = (0, 1, 0, 1, 2)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def join(left, right):
    """Natural join, retaining shared variable identity and the common color frame."""
    ls, lr = left
    rs, rr = right
    scope = tuple(sorted(set(ls) | set(rs)))
    shared = sorted(set(ls) & set(rs))
    li, ri = [ls.index(v) for v in shared], [rs.index(v) for v in shared]
    index = {}
    for row in rr:
        index.setdefault(tuple(row[i] for i in ri), []).append(row)
    rows = set()
    for a in lr:
        for b in index.get(tuple(a[i] for i in li), ()):
            values = dict(zip(ls, a)) | dict(zip(rs, b))
            rows.add(tuple(values[v] for v in scope))
    return scope, rows


def interface(graph, lists, ports):
    """Exact factor elimination; only nonports are existentially forgotten."""
    factors = [((v,), {(c,) for c in lists[v]}) for v in sorted(graph)]
    factors += [(tuple(sorted((u, v))), {(a, b) for a in U for b in U if a != b})
                for u, v in sorted(graph.edges())]
    remaining = set(graph) - set(ports)
    while remaining:
        def width(v):
            return len(set().union(*(set(s) for s, _ in factors if v in s))), v
        v = min(remaining, key=width)
        bucket = [f for f in factors if v in f[0]]
        factors = [f for f in factors if v not in f[0]]
        result = ((), {()})
        for factor in bucket:
            result = join(result, factor)
        scope, rows = result
        i = scope.index(v)
        factors.append((scope[:i] + scope[i+1:], {r[:i] + r[i+1:] for r in rows}))
        remaining.remove(v)
    result = ((), {()})
    for factor in factors:
        result = join(result, factor)
    assert result[0] == tuple(ports)
    return result[1]


def brute_interface(graph, lists, ports):
    vertices = sorted(graph)
    witnesses = {}
    for row in product(*(sorted(lists[v]) for v in vertices)):
        colors = dict(zip(vertices, row))
        if all(colors[u] != colors[v] for u, v in graph.edges()):
            witnesses.setdefault(tuple(colors[v] for v in ports), row)
    return witnesses


def forbidden(rows):
    return {a for a in U if not any(a not in row for row in rows)}


def block_palettes(graph, lists):
    """Witness for blockwise uniform degree lists, or None; K1 handled explicitly."""
    if any(len(lists[v]) != graph.degree(v) for v in graph):
        return None
    blocks = sorted(tuple(sorted(b)) for b in nx.biconnected_components(graph))
    if len(graph) == 1:
        return []  # tightness means the sole list is empty
    options = []
    for block in blocks:
        sub = graph.subgraph(block)
        if sub.number_of_edges() == len(block) * (len(block)-1) // 2:
            size = len(block)-1
        elif len(block) % 2 == 1 and all(d == 2 for _, d in sub.degree()):
            size = 2
        else:
            return None
        common = set.intersection(*(set(lists[v]) for v in block))
        options.append(list(combinations(sorted(common), size)))
    for palettes in product(*options):
        if all(sum(len(p) for b, p in zip(blocks, palettes) if v in b)
               == len(set().union(*(set(p) for b, p in zip(blocks, palettes) if v in b)))
               and set().union(*(set(p) for b, p in zip(blocks, palettes) if v in b)) == lists[v]
               for v in graph):
            return [dict(vertices=b, palette=p) for b, p in zip(blocks, palettes)]
    return None


def component_row(graph, boundary, vertices, ports):
    sub = graph.subgraph(vertices).copy()
    lists = {v: U - {boundary[b] for b in graph[v] if b < 5} for v in vertices}
    rows = interface(sub, lists, ports)
    witnesses = brute_interface(sub, lists, ports)
    assert rows == set(witnesses)
    blocked = forbidden(rows)
    certificates = []
    for a in sorted(U):
        residual = {v: lists[v] - ({a} if v in ports else set()) for v in vertices}
        assert all(len(residual[v]) >= sub.degree(v) for v in vertices)
        certificate = block_palettes(sub, residual)
        assert (certificate is not None) == (a in blocked)
        if a in blocked:
            certificates.append(dict(z_color=a, blocks=certificate))
    return dict(vertices=vertices, ports=ports, lists=[sorted(lists[v]) for v in vertices],
                tuples=[dict(colors=row, witness=witnesses[row]) for row in sorted(rows)],
                forbidden=sorted(blocked), block_certificates=certificates)


def local_controls():
    # Named algebra controls only; these are not claimed to be C5 disk lifts.
    shapes = [nx.empty_graph(1), nx.path_graph(2), nx.path_graph(4),
              nx.cycle_graph(3), nx.cycle_graph(5), nx.cycle_graph(7),
              nx.complete_graph(4), nx.Graph([(0, 1), (1, 2), (0, 2), (2, 3)]),
              nx.Graph([(0, 1), (1, 2), (0, 2), (2, 3), (3, 4), (2, 4)]),
              nx.cycle_graph(4)]
    records = []
    for i, graph in enumerate(shapes):
        eligible = [v for v in sorted(graph) if graph.degree(v) < 4]
        for count in sorted({1, min(2, len(eligible)), min(5, len(eligible))}):
            ports = eligible[:count]
            for shift in range(4):
                lists = {v: set((shift+j) % 4 for j in range(graph.degree(v) + (v in ports)))
                         for v in graph}
                rows = interface(graph, lists, ports)
                assert rows == set(brute_interface(graph, lists, ports))
                blocked = forbidden(rows)
                for a in U:
                    residual = {v: lists[v] - ({a} if v in ports else set()) for v in graph}
                    assert (block_palettes(graph, residual) is not None) == (a in blocked)
                records.append(dict(shape=i, edges=sorted(tuple(sorted(e)) for e in graph.edges()),
                                    vertices=sorted(graph), ports=ports,
                                    lists=[sorted(lists[v]) for v in sorted(graph)],
                                    tuples=sorted(rows), forbidden=sorted(blocked)))
    return records


def audit_graph(source_index, source):
    graph = nx.Graph(source['edges'])
    z, = [v for v in graph if v >= 5 and graph.degree(v) == 5]
    assert all(graph.degree(v) == 4 for v in graph if v >= 5 and v != z)
    vertices = sorted(v for v in graph if v >= 5 and v != z)
    components = sorted(sorted(c) for c in nx.connected_components(graph.subgraph(vertices)))
    ports = [sorted(set(vs) & set(graph[z])) for vs in components]
    assert all(ports)
    z_spokes = sorted(v for v in graph[z] if v < 5)
    rotation = source['apex_rotation']
    apex_edges = set(map(tuple, source['edges'])) | {(b, 10) for b in range(5)}
    assert {tuple(sorted((u, v))) for u, ns in enumerate(rotation) for v in ns} == apex_edges
    assert len(rotation) - len(apex_edges) + len(faces_of(rotation)) == 2
    pattern_rows, accepted, deletion_rows = [], [], []
    projection_control = None
    for b in REPS:
        parts = [component_row(graph, b, vs, ps) for vs, ps in zip(components, ports)]
        available = U - {b[v] for v in z_spokes}
        bans = [set(p['forbidden']) for p in parts]
        allowed = available - set().union(*bans)
        for a in U:
            witness = coloring(graph, dict(enumerate(b)) | {z: a})
            assert (witness is not None) == (a in allowed)
        accepted.append(bool(allowed))
        pattern_rows.append(dict(boundary=b, z_list=sorted(available), z_allowed=sorted(allowed),
                                 components=parts))
        if b == Q:
            assert not allowed
            assert set().union(*bans) == available
            private = [ban - set().union(*(other for j, other in enumerate(bans) if i != j))
                       for i, ban in enumerate(bans)]
            assert all(private) and len(components) <= len(available)
            assert max(map(len, ports)) >= 2
            for part, ban in zip(parts, bans):
                rows = [tuple(t['colors']) for t in part['tuples']]
                marginal = [{row[j] for row in rows} for j in range(len(part['ports']))]
                false_allowed = {a for a in U if all(values - {a} for values in marginal)} & ban
                if false_allowed and projection_control is None:
                    projection_control = dict(boundary=b, vertices=part['vertices'], ports=part['ports'],
                                              marginals=list(map(sorted, marginal)),
                                              incorrectly_allowed=sorted(false_allowed),
                                              forbidden=part['forbidden'])
        for e in sorted(set(map(tuple, source['edges'])) - CYCLE):
            child = graph.copy()
            child.remove_edge(*e)
            if z in e and min(e) < 5:
                new_available = U - {b[v] for v in z_spokes if v not in e}
                predicted = new_available - set().union(*bans)
            else:
                owner, = [i for i, vs in enumerate(components) if set(e) & set(vs)]
                predicted = available - set().union(*(ban for i, ban in enumerate(bans) if i != owner))
                # Independent check of the stronger erasure statement for all four z colors.
                piece = child.subgraph(set(range(5)) | {z} | set(components[owner])).copy()
                piece.remove_edges_from((z, v) for v in z_spokes)
                for a in U:
                    assert coloring(piece, dict(enumerate(b)) | {z: a}) is not None
            actual = []
            for a in U:
                witness = coloring(child, dict(enumerate(b)) | {z: a})
                assert (witness is not None) == (a in predicted)
                if witness is not None:
                    actual.append(a)
            if b == Q:
                assert actual
                witness = coloring(child, dict(enumerate(b)) | {z: actual[0]})
                deletion_rows.append(dict(edge=e, z_allowed=actual,
                                          witness=[witness[v] for v in sorted(graph)]))
    sigma = sum(int(a) << i for i, a in enumerate(accepted))
    assert sigma == source['sigma']
    # Full 240 rows, with independent reconstruction in the ORIGINAL color frame.
    full = []
    for b in BOUNDARY:
        bans = []
        for vs, ps in zip(components, ports):
            lists = {v: U - {b[w] for w in graph[v] if w < 5} for v in vs}
            bans.append(forbidden(interface(graph.subgraph(vs), lists, ps)))
        allowed = U - {b[v] for v in z_spokes} - set().union(*bans)
        full.append(bool(allowed))
        for a in U:
            assert (coloring(graph, dict(enumerate(b)) | {z: a}) is not None) == (a in allowed)
    full_hex = format(sum(int(a) << i for i, a in enumerate(full)), '060x')
    assert full_hex == source['full_relation']
    # All switches of the fixed-host deletion formula. One edge per damaged
    # component suffices; the preceding audit checks every individual choice.
    switches = []
    for keep in product((False, True), repeat=len(components)+len(z_spokes)):
        child = graph.copy()
        for i, vs in enumerate(components):
            if not keep[i]:
                child.remove_edge(z, ports[i][0])
        retained_spokes = [v for j, v in enumerate(z_spokes) if keep[len(components)+j]]
        child.remove_edges_from((z, v) for v in z_spokes if v not in retained_spokes)
        bits = 0
        for j, pattern in enumerate(pattern_rows):
            b = pattern['boundary']
            bans = [set(p['forbidden']) for i, p in enumerate(pattern['components']) if keep[i]]
            allowed = U - {b[v] for v in retained_spokes} - set().union(*bans)
            assert (coloring(child, dict(enumerate(b))) is not None) == bool(allowed)
            bits |= int(bool(allowed)) << j
        switches.append(dict(intact_components=keep[:len(components)],
                             retained_z_spokes=retained_spokes, sigma=bits))
    return dict(source_index=source_index, edges=source['edges'], z=z,
                apex_rotation=rotation, port_partition=sorted(map(len, ports), reverse=True),
                sigma=sigma, full_relation=full_hex, accepts_T4=(sigma & T4 == T4),
                missing_patterns=[b for i, b in enumerate(REPS) if not (sigma >> i & 1)],
                patterns=pattern_rows, q_deletions=deletion_rows,
                deletion_switches=switches,
                marginal_failure=projection_control)


def build():
    source = json.loads(SOURCE.read_text())
    for path, expected in source['source_sha256'].items():
        assert digest(ROOT / path) == expected, path
    local = local_controls()
    rows = [audit_graph(i, row) for i, row in enumerate(source['cyclic_probe']['disk_templates'])
            if sorted(row['interior_degrees']) == [4, 4, 4, 4, 5]]
    assert len(rows) == 32
    counts = Counter((r['accepts_T4'], len(r['missing_patterns'])) for r in rows)
    assert counts == {(True, 1): 16, (False, 2): 16}
    assert all(max(b) == 3 for r in rows for b in r['missing_patterns'] if tuple(b) != Q)
    assert Counter(tuple(r['port_partition']) for r in rows) == {(2, 1): 16, (2, 2): 16}
    assert all(r['marginal_failure'] is not None for r in rows)
    dependencies = [Path(__file__).resolve()] + [ROOT / 'scripts' / f'{name}.py' for name in
                    ('c5_cell_enumerator', 'c5_disk_deletions', 'c5_k4_blocks',
                     'boundary_relations', 'local_closure')]
    return dict(schema=1, scope='Exact interfaces and named controls; no arbitrary disk exclusion or Lean theorem.',
                input_sha256={str(SOURCE.relative_to(ROOT)): digest(SOURCE)},
                source_sha256={str(p.relative_to(ROOT)): digest(p) for p in dependencies},
                pattern_order=REPS, local_controls=local, witnesses=rows,
                summary=dict(local_controls=len(local), disk_witnesses=len(rows),
                             full_boundary_rows=len(rows)*len(BOUNDARY),
                             fixed_z_checks=len(rows)*len(BOUNDARY)*4,
                             canonical_deletion_checks=sum(len(r['q_deletions']) for r in rows)*len(REPS)*4,
                             deletion_switches=sum(len(r['deletion_switches']) for r in rows),
                             T4_single_missing=16, non_T4_double_missing=16,
                             marginal_failure_witnesses=32))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    data = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == data, 'certificate differs; rebuild explicitly'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__':
    main()
