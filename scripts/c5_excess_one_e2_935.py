#!/usr/bin/env python3
"""Replay fixed epsilon-one spoke restorations for E2; exclude triple-arc Q.

No source graph census, four-colour theorem, or planarity oracle is used.
Unbounded core classification and original-contact tail transfer are paper
premises, not conclusions of this finite checker. Archived inputs are read
without invoking their producers or writing to their paths.
"""

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_one_e2_935/observations.json'
CELLS = ROOT / 'artifacts/c5_cells/cells.json'
INPUTS = {
    'two_spoke': ROOT / 'artifacts/c5_941_two_spoke/observations.json',
    'three_spoke': ROOT / 'artifacts/c5_941_three_spoke/observations.json',
}
B = set(range(5))
FRAME = {tuple(sorted((v, (v + 1) % 5))) for v in B}
U = set(range(4))
T4_INDICES = {2, 5, 7, 8, 9}


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def proper(witness, vertices, edges, row):
    """Witness lists use literal vertex order B followed by sorted interiors."""
    order = list(range(5)) + sorted(vertices)
    assert len(witness) == len(order)
    f = dict(zip(order, witness))
    assert all(f[v] == row[v] for v in B)
    assert all(f[v] in U for v in order)
    assert all(f[a] != f[b] for a, b in edges)
    return f


def complete_relation(vertices, edges, row, ports):
    """Independent literal-colour backtracking; keep one full witness per tuple."""
    vertices = set(vertices)
    included = B | vertices
    relevant = {e for e in edges if set(e) <= included}
    neighbors = {v: set() for v in included}
    for a, b in relevant:
        neighbors[a].add(b)
        neighbors[b].add(a)
    f = dict(enumerate(row))
    relation = {}
    total = 0
    order = list(range(5)) + sorted(vertices)

    def visit(left):
        nonlocal total
        if not left:
            total += 1
            key = tuple(f[v] for v in ports)
            if key not in relation:
                relation[key] = [f[v] for v in order]
            return
        domains = {
            v: U - {f[w] for w in neighbors[v] if w in f}
            for v in left
        }
        v = min(left, key=lambda x: (len(domains[x]), x))
        for color in sorted(domains[v]):
            f[v] = color
            visit(left - {v})
            del f[v]

    visit(vertices)
    tuples = sorted(relation)
    return tuples, [relation[t] for t in tuples], total


def reject_positions(sigma, singleton):
    return sorted(value for key, value in singleton.items() if not sigma & (1 << int(key)))


def q_shape(q):
    if len(q) == 1:
        return 'singleton'
    if len(q) == 2:
        return 'adjacent_pair' if (q[0] - q[1]) % 5 in (1, 4) else 'nonadjacent_pair'
    if len(q) == 3:
        e = sum(v in q and (v + 1) % 5 in q for v in B)
        return 'three_arc' if e == 2 else 'two_arc_plus_singleton'
    return 'other'


def k33_certificate(edges, root, contacts):
    """Original K3,3 branch sets; no apex or planarity oracle."""
    x, y = contacts
    sx = sorted(b for b in B if tuple(sorted((b, x))) in edges)
    sy = sorted(b for b in B if tuple(sorted((b, y))) in edges)
    sr = sorted(b for b in B if tuple(sorted((b, root))) in edges)
    assert sx == sy and len(sx) == 2
    a, b = sx
    assert tuple(sorted((a, b))) in FRAME
    rest = sorted(B - {a, b})
    assert sr == rest
    sides = [[[a], [b], [root]], [[x], [y], rest]]
    flat = [set(s) for side in sides for s in side]
    assert all(flat[i].isdisjoint(flat[j]) for i in range(6) for j in range(i))
    internal = []
    for branch in flat:
        reached = {min(branch)}
        while True:
            new = reached | {v for u, v in edges if u in reached and v in branch} | {
                u for u, v in edges if v in reached and u in branch}
            if new == reached:
                break
            reached = new
        assert reached == branch
        internal.append(sorted(e for e in edges if set(e) <= branch))
    crossings = []
    for i, left in enumerate(sides[0]):
        for j, right in enumerate(sides[1]):
            candidates = sorted(e for e in edges if
                (e[0] in left and e[1] in right) or (e[1] in left and e[0] in right))
            assert candidates
            crossings.append(dict(left_branch=i, right_branch=j, edge=candidates[0]))
    return dict(left_branch_sets=sides[0], right_branch_sets=sides[1],
                internal_edges=internal, nine_cross_edges=crossings,
                shared_adjacent_support=sx,
                paper_obstruction='K3,3 minor in the original graph; B minus the shared adjacent pair is one connected path')


def validate_component(model, saved, name, edges, row, counts):
    vertices = model[name + '_vertices']
    ports = model['binary_contacts'] if name == 'binary' else [model['unary_contact']]
    relevant = {e for e in edges if set(e) <= B | set(vertices)}
    relation, _, _ = complete_relation(vertices, relevant, row, ports)
    assert relation == [tuple(t) for t in saved['ordered_relation']]
    forbidden = set.intersection(*(set(t) for t in relation)) if relation else U
    assert sorted(forbidden) == saved['forbidden']
    for t, witness in zip(saved['ordered_relation'], saved['tuple_witnesses']):
        f = proper(list(row) + witness, vertices, relevant, row)
        assert tuple(f[v] for v in ports) == tuple(t)
        counts['archived_component_witnesses'] += 1
    counts['complete_component_queries'] += 1


def replay(name, data, rows, singleton):
    assert data['pattern_order'] == rows
    q4 = data['normalized_omitted_row']
    assert q4 == rows[0]
    t4 = sum(1 << i for i in T4_INDICES)
    counts = Counter()
    controls, triples = [], []
    histogram = Counter()
    t4_shapes = Counter()
    for base in data['bases']:
        edges = {tuple(e) for e in base['edges']}
        assert FRAME <= edges
        assert all(a < b for a, b in edges)
        assert all(sum(v in e for e in edges) == 4 for v in range(5, base['vertices']))
        for record in base['q4_critical_witnesses']:
            edge = tuple(record['edge'])
            assert edge in edges - FRAME
            proper(record['coloring'], range(5, base['vertices']), edges - {edge}, q4)
            counts['archived_critical_witnesses'] += 1
    for model_id, model in enumerate(data['marked_models']):
        base = data['bases'][model['base_id']]
        vertices = set(range(5, base['vertices']))
        edges = {tuple(e) for e in base['edges']}
        ports, root = model['port_order'], model['root']
        base_relations = []
        for row, saved in zip(rows, model['rows']):
            assert saved['row'] == row
            relation, _, _ = complete_relation(vertices, edges, row, ports)
            assert relation == [tuple(t) for t in saved['ordered_port_relation']]
            assert len(relation) == len(saved['tuple_witnesses'])
            for t, witness in zip(relation, saved['tuple_witnesses']):
                f = proper(witness, vertices, edges, row)
                assert tuple(f[v] for v in ports) == t
                counts['archived_port_witnesses'] += 1
            validate_component(model, saved['binary'], 'binary', edges, row, counts)
            if name == 'two_spoke':
                validate_component(model, saved['unary'], 'unary', edges, row, counts)
            base_relations.append(relation)
            counts['complete_base_queries'] += 1
        for addition_id, addition in enumerate(model['additions']):
            added = tuple(addition['added_spoke'])
            assert added not in edges and root in added and added[0] in B
            extended = edges | {added}
            result_rows = []
            sigma = 0
            for i, (row, original, saved) in enumerate(zip(rows, base_relations, addition['rows'])):
                indices = [j for j, t in enumerate(original) if t[0] != row[added[0]]]
                assert indices == saved['retained_port_tuple_indices']
                filtered = [original[j] for j in indices]
                actual, witnesses, total = complete_relation(vertices, extended, row, ports)
                assert filtered == actual
                if actual:
                    sigma |= 1 << i
                result_rows.append(dict(row=row, original_ordered_relation=original,
                    retained_original_tuple_indices=indices, ordered_relation=actual,
                    full_tuple_witnesses=witnesses, full_extension_count=total))
                counts['complete_restored_queries'] += 1
            assert sigma == addition['sigma']
            q = reject_positions(sigma, singleton)
            assert q == addition['rejected_singleton_positions']
            accepts = sigma & t4 == t4
            assert accepts == addition['accepts_T4']
            shape = q_shape(q)
            histogram[sigma] += 1
            if accepts:
                t4_shapes[shape] += 1
                assert shape != 'nonadjacent_pair'
                assert shape in ({'singleton', 'adjacent_pair'} if name == 'two_spoke'
                                  else {'singleton', 'adjacent_pair', 'three_arc'})
            key = dict(model_id=model_id, base_id=model['base_id'], addition_id=addition_id,
                       root=root, added_spoke=added, sigma=sigma,
                       rejected_singleton_positions=q, accepts_T4=accepts)
            controls.append(dict(**key, complete_join_sha256=digest(result_rows)))
            if accepts and shape == 'three_arc':
                assert name == 'three_spoke' and base['family'] == 'bare_triangle'
                certificate = k33_certificate(extended, root, model['binary_contacts'])
                triples.append(dict(**key, vertices=base['vertices'], boundary_order=list(range(5)),
                    edges=sorted(extended), source_family=base['family'],
                    port_order=ports, binary_vertices=model['binary_vertices'],
                    binary_contacts=model['binary_contacts'], binary_support=model['binary_support'],
                    binary_boundary_attachments=model['binary_boundary_attachments'],
                    rows=result_rows, original_binary_rows=[r['binary'] for r in model['rows']],
                    original_component_owner=root, k33=certificate))
    assert len(controls) == (592 if name == 'two_spoke' else 1194)
    assert len(triples) == (0 if name == 'two_spoke' else 9)
    return dict(scope='fixed archived original-contact relations and named spoke additions',
                source=str(INPUTS[name].relative_to(ROOT)), bases=len(data['bases']),
                marked_models=len(data['marked_models']), additions=len(controls),
                sigma_histogram=dict(sorted(histogram.items())), T4_shapes=dict(sorted(t4_shapes.items())),
                controls=controls, triple_arc_nonplanar_models=triples,
                checks=dict(sorted(counts.items())))


def build():
    cells = json.loads(CELLS.read_text())
    rows, singleton = cells['pattern_order'], cells['singleton_of_three_colour']
    assert len(rows) == 10 and all(len(r) == 5 for r in rows)
    assert {i for i, row in enumerate(rows) if len(set(row)) == 4} == T4_INDICES
    results = {name: replay(name, json.loads(path.read_text()), rows, singleton)
               for name, path in INPUTS.items()}
    dependencies = [Path(__file__).resolve(), CELLS] + list(INPUTS.values())
    return dict(schema=1, pattern_order=rows, singleton_of_three_colour=singleton,
        T4_pattern_indices=sorted(T4_INDICES), source_sha256={
            str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in dependencies},
        evidence_layers=dict(paper='unbounded degree-four core classification, saturation, and original-contact tail transfer are cited premises',
            external='inherited degree-list/Gallai characterization; K3,3 nonplanarity',
            python='exact fixed-domain full ordered joins, literal-colour witnesses, and nine explicit original K3,3 minors',
            lean='no new Lean theorem'),
        no_four_colour_theorem_oracle=True, no_planarity_oracle=True,
        no_new_source_graph_census=True, archived_artifacts_unchanged=True,
        results=results,
        summary=dict(two_spoke_restorations=results['two_spoke']['additions'],
            three_spoke_restorations=results['three_spoke']['additions'],
            independent_complete_restored_ten_row_queries=sum(r['checks']['complete_restored_queries'] for r in results.values()),
            nonadjacent_pair_T4_restorations=0,
            two_spoke_triple_arc_T4_restorations=0,
            three_spoke_triple_arc_T4_restorations=9,
            triple_arc_original_K33_certificates=9,
            triple_arc_disk_survivors_in_this_necessary_domain=0))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    payload = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.check:
        assert OUT.read_bytes() == payload.encode(), f'certificate differs: {OUT}'
    else:
        assert not OUT.exists(), f'refusing to overwrite existing certificate: {OUT}'
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
