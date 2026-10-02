#!/usr/bin/env python3
"""Replay marked degree-four cores with one original root-spoke restored.

Arbitrary-size coverage uses the paper reduction, not a new graph census.
Keep the complete (r,x,y,u) relation and named factor omission identities.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

from c5_independent_support_capacity import (
    B, FRAME, ROWS, T4, U, colorings, components, normalize,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_941_two_spoke/observations.json'
BRANCHES = ROOT / 'artifacts/c5_triangle_branches/observations.json'
PATHS = ROOT / 'artifacts/c5_triangle_path_reduction/observations.json'
DOUBLE = ROOT / 'artifacts/c5_two_triangle_blocks/observations.json'
ALL_ROWS = tuple(b for b in product(range(4), repeat=5)
                 if all(b[a] != b[c] for a, c in FRAME))
Q4 = (0, 1, 0, 1, 2)


def search(vertices, edges, fixed):
    """Independent small-graph backtracking; keep every full coloring."""
    adjacent = {v: {b if a == v else a for a, b in edges if v in (a, b)}
                for v in vertices}
    assignment = dict(fixed)

    def visit(todo):
        if not todo:
            yield dict(assignment)
            return
        choices = {v: U - {assignment[w] for w in adjacent[v] if w in assignment}
                   for v in todo}
        v = min(todo, key=lambda w: (len(choices[w]), w))
        for c in sorted(choices[v]):
            assignment[v] = c
            yield from visit(todo - {v})
        assignment.pop(v, None)

    yield from visit(set(vertices))


def root_colors(neighborhoods, row):
    available = U - {row[b] for b in neighborhoods[-1]}
    for neighbors in reversed(neighborhoods[:-1]):
        available = {c for c in U - {row[b] for b in neighbors}
                     if available - {c}}
    return available


def tail_controls(bases, path_data):
    """Strengthen the inherited bridge equality to the original tail root."""
    uniform, switched, digest = [], [], sha256()
    for bi, base in enumerate(bases):
        for slot in range(len(base['branch_colors'])):
            first, leaf = base['neighborhoods'][3 + 2*slot:5 + 2*slot]
            adjacent = tuple(sorted(first)) in FRAME
            contained = set(first) <= set(leaf)
            assert adjacent or contained
            rows = []
            for row in ALL_ROWS:
                short = root_colors([first, leaf], row)
                masks = [sorted(root_colors([first]*length + [leaf], row))
                         for length in (1, 3, 5, 7)]
                assert all(set(mask) == short for mask in masks)
                digest.update((json.dumps([bi, slot, row, masks]) + '\n').encode())
                if row in ROWS:
                    rows.append(dict(row=row, root_colors=sorted(short)))
            uniform.append(dict(base=bi, slot=slot, first=first, leaf=leaf,
                                first_pair_adjacent=adjacent,
                                first_pair_contained_in_leaf=contained,
                                canonical_rows=rows))
    for old in path_data['normal_forms']:
        bi, slot = old['base'], old['slot']
        ns = old['neighborhoods']
        short = bases[bi]['neighborhoods'][3 + 2*slot:5 + 2*slot]
        edges = {(5 + i, 6 + i) for i in range(len(ns) - 1)}
        edges |= {(b, 5 + i) for i, support in enumerate(ns) for b in support}
        rows = []
        for row in ALL_ROWS:
            choices = colorings(range(5, 5 + len(ns)), edges, dict(enumerate(row)))
            actual = {f[5] for f in choices}
            assert actual == root_colors(ns, row) == root_colors(short, row)
            digest.update((json.dumps([bi, slot, row, sorted(actual)]) + '\n').encode())
            if row in ROWS:
                rows.append(dict(row=row, root_colors=sorted(actual),
                                 witnesses=[dict(root_color=c,
                                     coloring=[next(f for f in choices if f[5] == c)[v]
                                               for v in range(5 + len(ns))])
                                     for c in sorted(actual)]))
        switched.append(dict(base=bi, slot=slot, long_neighborhoods=ns,
                             short_neighborhoods=short, canonical_rows=rows))
    assert len(uniform) == 20 and len(switched) == 8 and len(ALL_ROWS) == 240
    return dict(uniform_slots=uniform, two_run_forms=switched,
                uniform_odd_lengths=[1, 3, 5, 7],
                full_row_uniform_checks=len(uniform)*len(ALL_ROWS)*4,
                full_row_two_run_checks=len(switched)*len(ALL_ROWS),
                enumeration_sha256=digest.hexdigest())


def check_rotation(n, edges, rotation):
    apex_edges = edges | {(b, n) for b in range(5)}
    assert len(rotation) == n + 1
    assert all(len(ring) == len(set(ring)) for ring in rotation)
    assert {(min(v, w), max(v, w)) for v, ring in enumerate(rotation)
            for w in ring} == apex_edges
    seen, faces = set(), 0
    for v, ring in enumerate(rotation):
        for w in ring:
            if (v, w) in seen:
                continue
            a, b = v, w
            while (a, b) not in seen:
                seen.add((a, b))
                around = rotation[b]
                assert a in around
                a, b = b, around[(around.index(a) - 1) % len(around)]
            assert (a, b) == (v, w)
            faces += 1
    assert len(seen) == 2*len(apex_edges)
    assert n + 1 - len(apex_edges) + faces == 2
    return faces


def base_record(family, index, base):
    edges = {tuple(e) for e in base['edges']}
    n = 5 + len(base['neighborhoods'])
    assert all(a < b for a, b in edges) and FRAME <= edges
    assert all(sum(v in e for e in edges) == 4 for v in range(5, n))
    faces = check_rotation(n, edges, base['apex_rotation'])
    rows = []
    for row in ROWS:
        choices = list(search(range(5, n), edges, dict(enumerate(row))))
        rows.append(bool(choices))
    mask = sum(1 << i for i, accepted in enumerate(rows) if accepted)
    assert mask == base['sigma'] == 1022
    critical = []
    for edge in sorted(edges - FRAME):
        witness = next(search(range(5, n), edges - {edge}, dict(enumerate(Q4))), None)
        assert witness is not None
        critical.append(dict(edge=edge, coloring=[witness[v] for v in range(n)]))
    return dict(family=family, input_index=index, vertices=n, edges=sorted(edges),
                neighborhoods=base['neighborhoods'], sigma=mask,
                apex_rotation=base['apex_rotation'], apex_faces=faces,
                q4_critical_witnesses=critical)


def forbidden(relation):
    assert relation
    return set.intersection(*(set(t) for t in relation))


def component_record(vertices, contacts, edges, row):
    choices = colorings(vertices, edges, dict(enumerate(row)))
    relation = sorted({tuple(f[v] for v in contacts) for f in choices})
    witnesses = [[next(f for f in choices if tuple(f[v] for v in contacts) == t)[v]
                  for v in vertices] for t in relation]
    return dict(ordered_relation=relation, tuple_witnesses=witnesses,
                forbidden=sorted(forbidden(relation)))


def singleton_positions(mask):
    return sorted(next(j for j in range(5) if row.count(row[j]) == 1)
                  for i, row in enumerate(ROWS) if not (mask >> i & 1)
                  and len(set(row)) == 3)


def relabel_mask(mask, mapping):
    result = 0
    for i, row in enumerate(ROWS):
        renamed = [None]*5
        for j in range(5):
            renamed[mapping[j]] = row[j]
        if mask >> i & 1:
            result |= 1 << ROWS.index(normalize(renamed))
    return result


def marked_record(base_id, base, r, target_orbit):
    n, edges = base['vertices'], set(map(tuple, base['edges']))
    neighbors = {v: {b if a == v else a for a, b in edges if v in (a, b)}
                 for v in range(n)}
    spoke, = sorted(neighbors[r] & B)
    interior = set(range(5, n))
    parts = components(interior - {r}, edges)
    binary, = [vs for vs in parts if len(set(vs) & neighbors[r]) == 2]
    unary, = [vs for vs in parts if len(set(vs) & neighbors[r]) == 1]
    x, y = sorted(set(binary) & neighbors[r])
    u, = sorted(set(unary) & neighbors[r])
    assert (x, y) in edges and len(parts) == 2
    ports = [r, x, y, u]
    rows = []
    for row in ROWS:
        c = component_record(binary, [x, y], edges, row)
        unit = component_record(unary, [u], edges, row)
        expected = sorted((a, cx, cy, cu[0]) for a in sorted(U - {row[spoke]})
                          for cx, cy in c['ordered_relation']
                          for cu in unit['ordered_relation'] if a not in {cx, cy, cu[0]})
        choices = list(search(interior, edges, dict(enumerate(row))))
        relation = sorted({tuple(f[v] for v in ports) for f in choices})
        assert relation == expected
        witnesses = [[next(f for f in choices if tuple(f[v] for v in ports) == t)[v]
                      for v in range(n)] for t in relation]
        rows.append(dict(row=row, binary=c, unary=unit,
                         ordered_port_relation=relation, tuple_witnesses=witnesses))
    additions = []
    for added in sorted(B - {spoke}):
        extended = edges | {(added, r)}
        result_rows = []
        for row, saved in zip(ROWS, rows):
            retained = [i for i, t in enumerate(saved['ordered_port_relation'])
                        if t[0] != row[added]]
            exact = {tuple(f[v] for v in ports)
                     for f in search(interior, extended, dict(enumerate(row)))}
            assert exact == {saved['ordered_port_relation'][i] for i in retained}
            factors = [{row[spoke]}, {row[added]},
                       set(saved['binary']['forbidden']), set(saved['unary']['forbidden'])]
            residual = U - set.union(*factors)
            assert residual == {t[0] for t in exact}
            omitted = [i for i in range(4) if set.union(
                *(f for j, f in enumerate(factors) if i != j)) == U]
            assert not omitted or not retained
            # Component deletion retains the other original attachments.
            for i in range(4):
                removed = ({(spoke, r)} if i == 0 else {(added, r)} if i == 1
                           else {e for e in extended if set(e) & set(binary if i == 2 else unary)})
                remaining = interior - (set(binary) if i == 2 else set(unary) if i == 3 else set())
                child = next(search(remaining, extended - removed, dict(enumerate(row))), None)
                assert (child is None) == (i in omitted)
            result_rows.append(dict(retained_port_tuple_indices=retained,
                                    omitted_factor_indices=omitted))
        sigma = sum(1 << i for i, data in enumerate(result_rows)
                    if data['retained_port_tuple_indices'])
        assert sigma not in target_orbit
        t4 = sigma & T4 == T4
        rejected = singleton_positions(sigma)
        if t4:
            assert len(rejected) == 1 or (len(rejected) == 2 and
                                         (rejected[0] - rejected[1]) % 5 in (1, 4))
        additions.append(dict(added_spoke=[added, r], sigma=sigma, accepts_T4=t4,
                              rejected_singleton_positions=rejected, rows=result_rows))
    return dict(base_id=base_id, root=r, existing_spoke=[spoke, r],
                binary_vertices=binary, binary_contacts=[x, y],
                binary_support=sorted(set.union(*(neighbors[v] & B for v in binary))),
                unary_vertices=unary, unary_contact=u,
                unary_support=sorted(set.union(*(neighbors[v] & B for v in unary))),
                port_order=ports, factor_order=['existing_spoke', 'added_spoke', 'C_2', 'U'],
                rows=rows, additions=additions)


def build():
    branch_data = json.loads(BRANCHES.read_text())
    path_data = json.loads(PATHS.read_text())
    double_data = json.loads(DOUBLE.read_text())
    tails = tail_controls(branch_data['disk_templates'], path_data)
    target_orbit = sorted({relabel_mask(941, [(s*j + t) % 5 for j in range(5)])
                           for s in (-1, 1) for t in range(5)})
    bases, marked, counts = [], [], Counter()
    for family, data in [('single_triangle', branch_data), ('double_triangle', double_data)]:
        for index, base in enumerate(data['disk_templates']):
            if base['sigma'] != 1022:
                continue
            saved = base_record(family, index, base)
            base_id = len(bases)
            bases.append(saved)
            counts[family + '_bases'] += 1
            for r in range(5, saved['vertices']):
                if sum(r in e and min(e) >= 5 for e in saved['edges']) != 3:
                    continue
                record = marked_record(base_id, saved, r, target_orbit)
                marked.append(record)
                counts[family + '_marked_roots'] += 1
    additions = [addition for model in marked for addition in model['additions']]
    histogram = Counter(a['sigma'] for a in additions)
    assert len(bases) == 82 and len(marked) == 148 and len(additions) == 592
    assert sum(a['accepts_T4'] for a in additions) == 444
    dependencies = [Path(__file__).resolve(),
                    ROOT / 'scripts/c5_independent_support_capacity.py', BRANCHES, PATHS, DOUBLE]
    return dict(schema=1,
                scope='finite marked-core restoration; arbitrary-size coverage and tail transfer are paper arguments',
                source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                               for p in dependencies},
                pattern_order=ROWS, normalized_omitted_row=Q4, target_D5_orbit=target_orbit,
                tail_root_controls=tails, bases=bases, marked_models=marked,
                tuple_index_semantics='each addition row indexes the complete base port relation and its full coloring witnesses',
                summary=dict(**dict(sorted(counts.items())), bases=len(bases), marked_roots=len(marked),
                    restored_spoke_models=len(additions), full_ten_row_checks=10*len(additions),
                    factor_deletion_queries=40*len(additions), T4_accepting_models=444,
                    sigma_histogram=dict(sorted(histogram.items())), candidate_941_models=0,
                    uniform_tail_root_checks=tails['full_row_uniform_checks'],
                    two_run_tail_root_checks=tails['full_row_two_run_checks'],
                    remaining_941_excess_one_spokes=[3], candidate_941_excess_lower_bound=1,
                    restored_graph_disk_realizability_checked=False,
                    new_source_graph_census=False, new_lean_theorem=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    payload = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.check:
        assert OUT.read_bytes() == payload.encode(), f'certificate differs: {OUT}'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
