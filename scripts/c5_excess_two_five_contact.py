#!/usr/bin/env python3
"""Five contacts and three rejected root colours: fixed controls and K5 minors.

The unbounded active-forest and actual-tether arguments are in the companion
report. These abstract residual models and minor skeletons are not disk sources.
"""
import argparse
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from c5_single_spoke_four import block_table, incidence_table
from c5_single_spoke_three_one import edge, validate_minor

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_five_contact/observations.json'
U = frozenset(range(4))


def active_tree_controls():
    # Suppress negative bridges. The remaining nodes are positive/negative
    # odd cycles. Five leaves gives sum(|cycle|-2)=3, hence these two lists.
    records = []
    for sizes in ((5,), (3, 3, 3)):
        trees = [()] if len(sizes) == 1 else [tuple((i, center) for i in range(3)
                   if i != center) for center in range(3)]
        for tree in trees:
            degrees = [sum(i in pair for pair in tree) for i in range(len(sizes))]
            for signs in product((-1, 1), repeat=len(sizes)):
                valid = all(not (signs[i] == signs[j] == -1) for i, j in tree)
                valid &= all(d <= size if sign == 1 else d == size
                             for d, size, sign in zip(degrees, sizes, signs))
                contacts = sum(size - d for d, size, sign in zip(degrees, sizes, signs)
                               if sign == 1)
                valid &= contacts == 5
                assert valid == all(sign == 1 for sign in signs)
                records.append(dict(cycle_sizes=sizes, cycle_tree=tree, signs=signs,
                                    cycle_degrees=degrees, contact_count=contacts,
                                    feasible=valid))
    assert len(records) == 26
    assert sum(r['feasible'] for r in records) == 4
    # Every active component has at least three contact leaves.
    assert all(a + b > 5 for a, b in product(range(3, 6), repeat=2))
    return records


def structure(kind, order=tuple(range(5))):
    ports = [f'u{i}' for i in order]
    if kind == 'positive_C5':
        cycles = [ports]
        bridges = []
        selected = ports
        groups = [set(ports[:3]), {ports[3]}, {ports[4]}, {'r'}]
    else:
        a, b, c, d, e = ports
        cycles = [[a, b, 'x'], ['y', c, 'z'], ['w', d, e]]
        bridges = [('x', 'y'), ('z', 'w')]
        selected = cycles[0]
        groups = [{a}, {b}, {'x'}, {'r', 'y', c, 'z', 'w', d, e}]
    es = {edge(cycle[i], cycle[(i + 1) % len(cycle)])
          for cycle in cycles for i in range(len(cycle))}
    es.update(edge(*pair) for pair in bridges)
    return ports, cycles, bridges, selected, groups, es


def relation_controls():
    records = []
    for kind, e in product(('positive_C5', 'three_positive_triangles'), range(4)):
        ports, cycles, bridges, _, _, es = structure(kind)
        vertices = sorted(set().union(*(set(pair) for pair in es)))
        available = sorted(U - {e})
        witnesses = {}
        coloring_count = 0
        for colors in product(available, repeat=len(vertices)):
            f = dict(zip(vertices, colors))
            if any(f[v] == f[w] for v, w in es):
                continue
            coloring_count += 1
            t = tuple(f[p] for p in ports)
            witnesses.setdefault(t, colors)
        relation = sorted(witnesses)
        assert relation
        forbidden = set.intersection(*(set(t) for t in relation))
        assert forbidden == set(available)
        # Complete six-port join, not the product of five marginal domains.
        joined = [(a,) + t for a in range(4) for t in relation if a not in t]
        assert {t[0] for t in joined} == {e}
        assert not [t for t in joined if t[0] != e]
        # A missing root-contact really destroys all three forbidden colours.
        release = []
        for i, a in product(range(5), available):
            t = next(t for t in relation if all(c != a for j, c in enumerate(t) if j != i))
            release.append(dict(contact_index=i, root_color=a, tuple=t,
                                coloring=witnesses[t]))
        records.append(dict(kind=kind, omitted_color=e, original_contact_order=ports,
            vertex_order=vertices, original_edges=sorted(es), cycles=cycles,
            negative_bridges=bridges, residual_lists=[available for _ in vertices],
            full_coloring_count=coloring_count, ordered_contact_relation=relation,
            tuple_witnesses=[witnesses[t] for t in relation], forbidden_colors=sorted(forbidden),
            full_six_port_join=joined, deleted_contact_lifts=release))
    return records


def minor(kind, spoke, order, length, shared):
    ports, cycles, bridges, selected, groups, es = structure(kind, order)
    es.update(edge(f'b{i}', f'b{(i + 1) % 5}') for i in range(5))
    es.add(edge('r', f'b{spoke}'))
    es.update(edge('r', p) for p in ports)
    groups.append({f'b{i}' for i in range(5)})
    tethers = []
    for i, v in enumerate(selected):
        target = 0 if shared else i
        path = [v] + [f't{i}_{j}' for j in range(length - 1)] + [f'b{target}']
        es.update(edge(x, y) for x, y in zip(path, path[1:]))
        groups[4].update(path[1:-1])
        tethers.append(path)
    record = dict(kind=kind, spoke=spoke, contact_order=[f'u{i}' for i in range(5)],
        role_permutation=order, cycles=cycles, negative_bridges=bridges,
        actual_tethers=tethers, edges=sorted(es), branch_sets=[sorted(g) for g in groups])
    assert validate_minor(record)
    assert {v if u == 'r' else u for u, v in es if 'r' in (u, v)} == set(ports + [f'b{spoke}'])
    record['adjacency'] = [dict(pair=[i, j], edge=next(
        edge(v, w) for v in sorted(groups[i]) for w in sorted(groups[j])
        if edge(v, w) in es)) for i, j in combinations(range(5), 2)]
    return record


def minor_controls():
    records, digest, count = [], sha256(), 0
    for kind, spoke, length, shared in product(
            ('positive_C5', 'three_positive_triangles'), range(5), (1, 3), (False, True)):
        for order in permutations(range(5)):
            record = minor(kind, spoke, order, length, shared)
            digest.update(json.dumps(record, sort_keys=True).encode())
            count += 1
            if order == tuple(range(5)):
                records.append(record)
    assert count == 4800 and len(records) == 40
    negatives = []
    for kind in ('positive_C5', 'three_positive_triangles'):
        base = minor(kind, 0, tuple(range(5)), 1, True)
        damaged = dict(base, edges=[pair for pair in base['edges'] if pair != edge('r', 'b0')])
        assert not validate_minor(damaged)
        negatives.append(dict(kind=kind, failure='missing_original_spoke'))
        groups = [g[:] for g in base['branch_sets']]
        groups[0].append('r')
        assert not validate_minor(dict(base, branch_sets=groups))
        negatives.append(dict(kind=kind, failure='overlapping_branch_sets'))
        groups = [g[:] for g in base['branch_sets']]
        groups[4].append('invented_vertex')
        assert not validate_minor(dict(base, branch_sets=groups))
        negatives.append(dict(kind=kind, failure='invented_tether_vertex'))
    return dict(controls=count, representative_records=records,
        role_permutations=list(permutations(range(5))), all_records_sha256=digest.hexdigest(),
        negative_controls=negatives)


def build():
    palettes = [dict(spoke_color=e, blocks=block_table(e),
                    incidence=incidence_table(e, block_table(e))) for e in range(4)]
    trees = active_tree_controls()
    relations = relation_controls()
    minors = minor_controls()
    paths = [Path(__file__).resolve(), ROOT / 'scripts/c5_single_spoke_four.py',
             ROOT / 'scripts/c5_single_spoke_three_one.py']
    return dict(schema=1, scope='t=1 five-contact whole-source exclusion',
        source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths},
        palette_controls=palettes, active_tree_controls=trees,
        abstract_full_relations=relations, minor_controls=minors,
        paper_dependencies=['degree-list block characterization and tightness',
            'connected exterior K4 exclusion without a root-degree restriction',
            'one common tau for three rejected colors',
            'unbounded five-leaf classification and actual boundary tethers'],
        summary=dict(active_tree_cases=len(trees), feasible_labeled_trees=4,
            geometric_shapes=2, palette_types=sum(len(p['blocks']) for p in palettes),
            incidence_controls=sum(len(p['incidence']) for p in palettes),
            abstract_complete_relations=len(relations),
            complete_relation_tuples=sum(len(r['ordered_contact_relation']) for r in relations),
            original_coloring_lifts=sum(len(r['deleted_contact_lifts']) for r in relations),
            K5_minor_controls=minors['controls'], negative_controls=len(minors['negative_controls']),
            graph_enumeration=False, disk_realizability_claim=False, new_Lean_theorem=False))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    payload = json.dumps(result, sort_keys=True, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == payload, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
