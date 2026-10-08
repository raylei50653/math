#!/usr/bin/env python3
"""U3 mixed11: finite controls for the paper shield/slack exclusion.

The controls are full-degree graphs, not a source census or disk/critical
realizability certificates. Arbitrary-size coverage is supplied by paper.
Standard-library replay checks literal witnesses and exact same-frame joins.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_nonadjacent_one_mixed_core44/observations.json'
SOURCES = [ROOT / 'docs/c5_unary_shield_budget.md',
           ROOT / 'docs/c5_k4_blocks.md', ROOT / 'docs/c5_triangle_forks.md',
           ROOT / 'docs/c5_two_triangle_blocks.md']
B = set(range(5))
COLORS = set(range(4))
FRAME = {tuple(sorted((b, (b+1) % 5))) for b in B}


def normalize(values):
    labels = {}
    return tuple(labels.setdefault(c, len(labels)) for c in values)


ROWS = tuple(sorted({normalize(r) for r in product(range(4), repeat=5)
                     if all(r[a] != r[b] for a, b in FRAME)}))


def adjacency(edges, vertices):
    result = {v: set() for v in vertices}
    for a, b in edges:
        result[a].add(b)
        result[b].add(a)
    return result


def piece_relation(vertices, edges, row, contacts):
    """Whole-piece MRV search: one complete witness for every contact tuple."""
    order = sorted(B | set(vertices))
    adjacent = adjacency(edges, order)
    fixed = dict(enumerate(row))
    result = {}

    def visit():
        todo = set(vertices) - fixed.keys()
        if not todo:
            result.setdefault(tuple(fixed[v] for v in contacts),
                              tuple(fixed[v] for v in order))
            return
        choices = {v: COLORS - {fixed[u] for u in adjacent[v] if u in fixed}
                   for v in todo}
        v = min(todo, key=lambda x: (len(choices[x]), -len(adjacent[x]), x))
        for color in sorted(choices[v]):
            fixed[v] = color
            visit()
        fixed.pop(v, None)

    visit()
    return result


def graph_relation(vertices, edges, row, roots):
    """Independent fixed-order whole-graph search, with root colors pinned."""
    order = sorted(B | set(vertices))
    adjacent = adjacency(edges, order)
    interior = sorted(vertices)
    result = {}
    for pair in product(range(4), repeat=2):
        fixed = dict(enumerate(row)) | dict(zip(roots, pair, strict=True))
        if any(a in fixed and b in fixed and fixed[a] == fixed[b] for a, b in edges):
            continue
        todo = [v for v in interior if v not in fixed]

        def extend(index):
            if index == len(todo):
                return tuple(fixed[v] for v in order)
            v = todo[index]
            for color in range(4):
                if any(fixed.get(u) == color for u in adjacent[v]):
                    continue
                fixed[v] = color
                answer = extend(index+1)
                if answer is not None:
                    return answer
            fixed.pop(v, None)
            return None

        witness = extend(0)
        if witness is not None:
            result[pair] = witness
    return result


def verify_witness(witness, order, edges, row, ports=(), values=()):
    assert len(witness) == len(order)
    fixed = dict(zip(order, witness, strict=True))
    assert all(c in COLORS for c in fixed.values())
    assert tuple(fixed[b] for b in range(5)) == row
    assert all(fixed[a] != fixed[b] for a, b in edges)
    assert tuple(fixed[v] for v in ports) == values


def components(vertices, edges):
    todo, result = set(vertices), []
    adjacent = adjacency(edges, B | set(vertices) | {5, 6})
    while todo:
        reached, pending = set(), [min(todo)]
        while pending:
            v = pending.pop()
            if v in reached:
                continue
            reached.add(v)
            pending.extend(adjacent[v] & todo - reached)
        todo -= reached
        result.append(sorted(reached))
    return result


def budget_controls():
    capacities = []
    for k in range(1, 5):
        t = 4-k  # Original degree five: sole mixed incidence one.
        for kind in ('spoke', 'unit_unary'):
            possible = t >= 1 if kind == 'spoke' else k == 1
            retained_k = k if kind == 'spoke' else 0
            interior_degree = 1+retained_k
            admitted = possible and interior_degree <= 3
            capacities.append(dict(unary_capacity=k, original_spokes=t,
                omitted_unit=kind, capacity_one_omission_possible=possible,
                retained_internal_degree=interior_degree,
                admitted_by_paper_core_maximum_degree_three=admitted))
    admitted = [(r['unary_capacity'], r['omitted_unit']) for r in capacities
                if r['admitted_by_paper_core_maximum_degree_three']]
    assert admitted == [(1, 'spoke'), (1, 'unit_unary'), (2, 'spoke')]
    arcs = []
    for start in range(5):
        vertices = [(start+i) % 5 for i in range(3)]
        edges = {tuple(sorted(e)) for e in zip(vertices, vertices[1:])}
        arcs.append((vertices, edges))
    witnesses = []
    for (uz, ez), (uw, ew) in product(arcs, repeat=2):
        if ez & ew:
            continue
        usable = sorted(B - {uz[1], uw[1]})
        assert len(usable) == 3
        edges = FRAME | {(b, r) for b in usable for r in (5, 6)}
        augmented = edges | {(b, 7) for b in B}
        paths = [[a, b] for a in (5, 6, 7) for b in usable]
        assert all(tuple(sorted(path)) in augmented for path in paths)
        assert len({tuple(sorted(path)) for path in paths}) == 9
        witnesses.append(dict(unary_shield_vertex_order=[uz, uw],
            unary_shield_edges=[sorted(ez), sorted(ew)],
            actual_unary_support=[sorted(uz), sorted(uw)],
            common_spoke_vertices=usable, core_edges=sorted(edges),
            exterior_apex=7, augmented_edges=sorted(augmented),
            subdivision=dict(model='K3,3', branch_partition=[[5, 6, 7], usable],
                             paths=paths)))
    assert len(witnesses) == 10
    double = {(5, 7), (5, 8), (7, 8), (6, 9), (6, 10), (9, 10), (5, 6)}
    degrees = {v: sum(v in e for e in double) for v in range(5, 11)}
    assert sorted(v for v, d in degrees.items() if d == 3) == [5, 6]
    return dict(capacity_rows=capacities, ordered_two_two_shields=witnesses,
        double_triangle_control=dict(interior_edges=sorted(double),
            internal_degrees=degrees, degree_three_vertices=[5, 6],
            direct_bridge=[5, 6], bridge_endpoints_adjacent=True),
        paper_dependency='The arbitrary-size degree-four classification supplies internal maximum degree three and the exact six-vertex directly bridged double-triangle form. The displayed double-triangle is a finite structural control, not a proof of that classification.')


def slack_controls():
    records = []
    for degree in range(3):
        pin_count = 2-degree
        for color in range(4):
            for pins in product(range(4), repeat=pin_count):
                neighbors = [color, color] + list(pins)
                assert len(neighbors)+degree == 4
                available = sorted(COLORS - set(neighbors))
                assert len(available) >= degree+1
                records.append(dict(internal_degree=degree,
                    repeated_boundary_neighbor_color=color, root_pins=pins,
                    external_neighbor_colors=neighbors, available_colors=available,
                    list_slack=len(available)-degree))
    assert len(records) == 84
    return dict(records=records,
        meaning='Finite list arithmetic when the two actual boundary neighbors of every C vertex repeat a color; paper supplies connected spanning-tree extension for arbitrary path length.')


def make_graph(length, kind, exchange):
    edges = set(FRAME)
    roots = [5, 6]
    z, w = roots
    next_vertex = 7

    def allocate(count):
        nonlocal next_vertex
        result = list(range(next_vertex, next_vertex+count))
        next_vertex += count
        return result

    def edge(a, b):
        edges.add(tuple(sorted((a, b))))

    def attach(v, support):
        for b in support:
            edge(v, b)

    for b in (0, 2, 4):
        edge(z, b)
    for b in (2, 4):
        edge(w, b)
    uz = allocate(2 if kind == 'long_z_unary' else 1)
    edge(z, uz[0])
    if len(uz) == 1:
        attach(uz[0], (0, 1, 2))
    else:
        edge(*uz)
        attach(uz[0], (0, 1))
        attach(uz[1], (0, 1, 2))
    uw = allocate(3 if kind == 'long_w_unary' else 2)
    x, y = uw[:2]
    edge(w, x)
    edge(w, y)
    edge(x, y)
    if len(uw) == 2:
        attach(x, (2, 3))
    else:
        edge(x, uw[2])
        attach(x, (2,))
        attach(uw[2], (2, 3, 4))
    attach(y, (3, 4))
    mixed = allocate(length)
    edge(z, mixed[0])
    edge(w, mixed[-1])
    for a, b in zip(mixed, mixed[1:]):
        edge(a, b)
    for v in mixed:
        attach(v, (2, 4))
    pieces = [('U_z', uz), ('U_w', uw), ('C', mixed)]
    if exchange:
        rename = lambda v: 11-v if v in (5, 6) else v
        edges = {tuple(sorted((rename(a), rename(b)))) for a, b in edges}
        z, w = rename(z), rename(w)
    interior = list(range(5, next_vertex))
    assert all(sum(v in e for e in edges) == (5 if v in roots else 4) for v in interior)
    assert (5, 6) not in edges
    assert components(set(interior)-set(roots), edges) == [vs for _, vs in pieces]
    records = []
    for name, vs in pieces:
        contacts = [[v for v in vs if tuple(sorted((r, v))) in edges] for r in roots]
        owners = [r for r, cs in zip(roots, contacts, strict=True) if cs]
        attachment = [dict(vertex=v, boundary_neighbors=sorted(b for b in B if (b, v) in edges)) for v in vs]
        records.append(dict(id=name, vertices=vs,
            ownership=owners, root_contacts=contacts,
            ordered_distinct_contacts=sorted(set().union(*map(set, contacts))),
            boundary_attachments=attachment,
            actual_support=sorted({b for a in attachment for b in a['boundary_neighbors']}),
            piece_edges=sorted(e for e in edges if set(e) <= (B | set(vs))),
            root_incidence_edges=sorted(e for e in edges if set(e) & set(vs) and set(e) & set(roots))))
    assert [len(cs) for cs in records[2]['root_contacts']] == [1, 1]
    assert records[0]['actual_support'] == [0, 1, 2]
    assert records[1]['actual_support'] == [2, 3, 4]
    assert records[2]['actual_support'] == [2, 4]
    return dict(c_path_length=length, side_kind=kind, roots_exchanged=exchange,
        original_root_order=roots, high_spoke_root=z, triangle_root=w,
        interior_order=interior, edges=sorted(edges), pieces=records,
        original_root_spokes=[[b for b in sorted(B) if (b, r) in edges] for r in roots],
        boundary_endpoint_pair=[2, 4])


def graph_control(graph):
    edges = set(map(tuple, graph['edges']))
    interior, roots = graph['interior_order'], graph['original_root_order']
    order = sorted(B | set(interior))
    ports = roots + sorted({v for p in graph['pieces'] for v in p['ordered_distinct_contacts']})
    records, sigma = [], 0
    for ri, row in enumerate(ROWS):
        pieces = []
        for piece in graph['pieces']:
            es = set(map(tuple, piece['piece_edges']))
            contact_order = piece['ordered_distinct_contacts']
            relation = piece_relation(piece['vertices'], es, row, contact_order)
            piece_order = sorted(B | set(piece['vertices']))
            for values, witness in relation.items():
                verify_witness(witness, piece_order, es, row, contact_order, values)
            pieces.append(dict(piece_id=piece['id'], contact_order=contact_order,
                tuples=sorted(relation), witness_vertex_order=piece_order,
                full_piece_witnesses=[relation[t] for t in sorted(relation)]))
        fibres, joined_pairs = [], set()
        direct = graph_relation(interior, edges, row, roots)
        for pair in product(range(4), repeat=2):
            pins = dict(zip(roots, pair, strict=True))
            retained = {}
            if all(pair[j] != row[b] for j, spokes in enumerate(graph['original_root_spokes']) for b in spokes):
                for choices in product(*(range(len(p['tuples'])) for p in pieces)):
                    values = dict(pins)
                    lift = dict(enumerate(row)) | pins
                    for saved, choice in zip(pieces, choices, strict=True):
                        contact_tuple = saved['tuples'][choice]
                        values.update(zip(saved['contact_order'], contact_tuple, strict=True))
                        lift.update(zip(saved['witness_vertex_order'],
                                        saved['full_piece_witnesses'][choice], strict=True))
                    if all(values[a] != values[b] for piece in graph['pieces']
                           for a, b in piece['root_incidence_edges']):
                        contact_tuple = tuple(values[v] for v in ports)
                        verify_witness(tuple(lift[v] for v in order), order,
                                       edges, row, ports, contact_tuple)
                        retained.setdefault(contact_tuple, choices)
            assert bool(retained) == (pair in direct)
            witness = direct.get(pair)
            if witness is not None:
                joined_pairs.add(pair)
                verify_witness(witness, order, edges, row, roots, pair)
            tuples = sorted(retained)
            fibres.append(dict(root_pair=pair, joint_tuples=tuples,
                joint_tuple_piece_witness_indices=[retained[t] for t in tuples],
                full_graph_witness=witness))
        assert joined_pairs == set(direct)
        repeating = row[2] == row[4]
        assert not repeating or joined_pairs
        if joined_pairs:
            sigma |= 1 << ri
        records.append(dict(row_index=ri, boundary_row=row, piece_relations=pieces,
            all_sixteen_root_fibres=fibres,
            accepted_root_pairs=sorted(joined_pairs),
            repeated_mixed_attachment_color=repeating,
            accepted=bool(joined_pairs)))
    return dict(graph, full_coloring_vertex_order=order, joint_port_order=ports,
                sigma=sigma, rows=records)


def build():
    index = {row: i for i, row in enumerate(ROWS)}
    orbits = {str(mask): sorted({sum(1 << index[normalize(
        [row[(sign*j+shift) % 5] for j in range(5)])]
        for ri, row in enumerate(ROWS) if mask >> ri & 1)
        for sign in (-1, 1) for shift in range(5)}) for mask in (933, 941)}
    targets = set().union(*map(set, orbits.values()))
    row_coverage = []
    for pair in combinations(range(5), 2):
        if pair in FRAME:
            continue
        cases = []
        for mask in sorted(targets):
            rejected = [ri for ri, row in enumerate(ROWS)
                        if not (mask >> ri & 1) and row[pair[0]] == row[pair[1]]]
            assert rejected, 'Every original diagonal pair must repeat in a rejected row'
            cases.append(dict(target_mask=mask, rejected_repeating_rows=rejected))
        row_coverage.append(dict(actual_boundary_pair=pair, target_cases=cases))
    assert len(row_coverage) == 5 and sum(len(c['target_cases']) for c in row_coverage) == 50
    graphs = [graph_control(make_graph(length, kind, exchange))
              for length, kind, exchange in product(range(1, 5),
                  ('bare_sides', 'long_z_unary', 'long_w_unary'), (False, True))]
    assert len(graphs) == 24
    assert not targets.intersection(g['sigma'] for g in graphs)
    return dict(schema=1,
        scope='Finite budget/topology/list and whole-graph controls for U3 sole mixed11; arbitrary-size source exclusion is a separate paper argument.',
        source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                       for p in SOURCES + [Path(__file__).resolve()]},
        pattern_order=ROWS, target_D5_orbits=orbits,
        rejected_row_pair_coverage=row_coverage,
        budget=budget_controls(), duplicate_neighbor_list_slack=slack_controls(),
        actual_graph_controls=graphs,
        witness_semantics='Every piece tuple has a witness on that entire original piece and fixed ordered boundary. Each of sixteen root fibres is obtained by joining those tuples in the same literal color frame and checking all original root incidences. Each joint tuple references its three whole-piece witness indices, whose composite is checked on every original full-graph edge. Nonempty fibres also have an independently searched whole-graph witness; empty fibres are checked by the same independent search. Shared C contact is one vertex coordinate.',
        summary=dict(actual_graphs=len(graphs), original_graph_row_queries=240,
            pinned_root_fibres=3840, piece_whole_tuple_relations=720,
            ordered_two_two_shields=10, duplicate_neighbor_slack_checks=84,
            rejected_pair_mask_coverage_checks=50,
            sigma_histogram=dict(sorted(Counter(g['sigma'] for g in graphs).items())),
            repeating_endpoint_row_queries=sum(r['repeated_mixed_attachment_color'] for g in graphs for r in g['rows']),
            target_hits=0, graph_census=False, source_realizability_claimed=False,
            disk_or_sigma_critical_claimed_for_controls=False, new_lean_theorem=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build()
    encoded = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n'
    if args.check:
        assert OUT.read_text() == encoded, 'Certificate differs; do not overwrite historical inputs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(encoded)
    print(json.dumps(dict(status='checked' if args.check else 'written', **data['summary']), sort_keys=True))


if __name__ == '__main__':
    main()
