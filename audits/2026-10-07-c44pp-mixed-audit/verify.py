#!/usr/bin/env python3
"""Read-only independent verifier of four existing fixed-domain certificates.

Standard library only; no imports of historical producers, no planarity oracle.
Paper supplies arbitrary-size coverage. This checks the finite exclusion layer.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FRAME = {tuple(sorted((i, (i + 1) % 5))) for i in range(5)}
PERMS = list(permutations(range(4)))


def edge_set(edges):
    result = {tuple(sorted(e)) for e in edges}
    assert len(result) == len(edges) and all(a != b for a, b in result)
    return result


def normalized(word):
    seen = {}
    return tuple(seen.setdefault(c, len(seen)) for c in word)


def orbits(rows):
    lookup = {tuple(r): i for i, r in enumerate(rows)}
    return {str(mask): sorted({sum(1 << lookup[normalized(
        [r[(sign * j + shift) % 5] for j in range(5)])]
        for i, r in enumerate(rows) if mask >> i & 1)
        for sign in (-1, 1) for shift in range(5)}) for mask in (933, 941)}


def relation(edges, row, ports):
    """Enumerate whole-graph colorings using independent minimum-domain search."""
    vertices = set().union(*map(set, edges))
    adjacency = {v: set() for v in vertices}
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    colors = dict(enumerate(row))
    result = set()

    def visit():
        pending = vertices - colors.keys()
        if not pending:
            result.add(tuple(colors[v] for v in ports))
            return
        options = {v: set(range(4)) - {colors[u] for u in adjacency[v] if u in colors}
                   for v in pending}
        v = min(pending, key=lambda u: (len(options[u]), -len(adjacency[u]), u))
        for c in sorted(options[v]):
            colors[v] = c
            visit()
            del colors[v]

    assert all(colors[a] != colors[b] for a, b in edges if a < 5 and b < 5)
    visit()
    return result


def critical(form, edges, row, order):
    assert all(sum(v in e for e in edges) == 4 for v in order if v >= 5)
    records = form['q4_critical_witnesses']
    assert {tuple(r['edge']) for r in records} == edges - FRAME
    for record in records:
        colors = dict(zip(order, record['coloring'], strict=True))
        assert tuple(colors[b] for b in range(5)) == tuple(row)
        assert all(c in range(4) for c in colors.values())
        assert all(colors[a] != colors[b] for a, b in edges - {tuple(record['edge'])})


def domains(rows, binary=False):
    pairs = list(product(range(4), repeat=2))
    forbidden = [()] + [(p,) for p in pairs] + [tuple(ps) for ps in combinations(pairs, 2)
        if ps[0][0] != ps[1][0] and ps[0][1] != ps[1][1]]
    assert len(forbidden) == 89
    result = []
    for mask in range(32):
        support = [b for b in range(5) if mask >> b & 1]
        shapes, choices, reps, transports, shape_ids = {}, [], [], [], []
        for row in rows:
            values = tuple(row[b] for b in support)
            shape = normalized(values)
            if shape not in shapes:
                shapes[shape] = len(choices)
                reps.append(values)
                stabilizer = [p for p in PERMS if all(p[c] == c for c in values)]
                if binary:
                    choices.append([f for f in forbidden if all(
                        tuple(sorted((p[a], p[b]) for a, b in f)) == f for p in stabilizer)])
                else:
                    choices.append([-1] + [c for c in range(4)
                        if all(p[c] == c for p in stabilizer)])
            sid = shapes[shape]
            maps = [p for p in PERMS if tuple(p[c] for c in reps[sid]) == values]
            outputs = []
            for choice in choices[sid]:
                images = {tuple(sorted((p[a], p[b]) for a, b in choice)) for p in maps} if binary else (
                    {-1} if choice == -1 else {p[choice] for p in maps})
                assert len(images) == 1
                outputs.append(images.pop())
            shape_ids.append(sid)
            transports.append(outputs)
        result.append((choices, shape_ids, transports))
    return result


def compare_domains(saved, rebuilt, binary=False):
    for mask, (record, domain) in enumerate(zip(saved, rebuilt, strict=True)):
        choices, ids, transports = domain
        assert record['id'] == mask
        assert record['actual_boundary_support'] == [b for b in range(5) if mask >> b & 1]
        convert = (lambda x: tuple(map(tuple, x))) if binary else (lambda x: x)
        assert [[convert(c) for c in s['choices']] for s in record['local_shapes']] == choices
        assert [t['local_shape'] for t in record['row_transports']] == ids
        assert [[convert(c) for c in t['literal_forbidden_choices']]
                for t in record['row_transports']] == transports


def possible(ks, target, domain, binary=False):
    choices, ids, transports = domain
    allowed = [set(range(len(cs))) for cs in choices]
    for ri, (k, sid, outputs) in enumerate(zip(ks, ids, transports, strict=True)):
        accepted = bool(target >> ri & 1)
        allowed[sid] &= {i for i, f in enumerate(outputs) if (
            bool(set(k) - set(f)) if binary else bool(set(k) - ({f} if f >= 0 else set()))) == accepted}
    return all(allowed)


def subdivision(record, expected):
    assert edge_set(record['minor_edges']) == expected
    cert = record['obstruction']
    branches = set(cert['branch_vertices'])
    assert len(branches) == len(cert['branch_vertices'])
    internal, links = set(), set()
    for path in cert['paths']:
        assert len(path) >= 2 and len(path) == len(set(path))
        a, b = path[0], path[-1]
        assert a in branches and b in branches and a != b
        middle = set(path[1:-1])
        assert not middle & (branches | internal)
        internal |= middle
        link = tuple(sorted((a, b)))
        assert link not in links
        links.add(link)
        assert all(tuple(sorted(e)) in expected for e in zip(path, path[1:]))
    if cert['model'] == 'K5':
        assert len(branches) == 5 and links == set(combinations(sorted(branches), 2))
    else:
        assert cert['model'] == 'K3,3' and len(branches) == 6
        assert any(links == {tuple(sorted((a, b))) for a in left for b in branches - set(left)}
                   for left in combinations(sorted(branches), 3))


def tables(ks, target, du, dv):
    offset = len(du[0])
    merged = {}
    for ri, k in enumerate(ks):
        key = (du[1][ri], offset + dv[1][ri])
        pairs = {(i, j) for i, a in enumerate(du[2][ri]) for j, b in enumerate(dv[2][ri])
                 if any(x != a and y != b for x, y in k) == bool(target >> ri & 1)}
        merged[key] = merged.get(key, pairs) & pairs
    return [set(range(len(cs))) for cs in du[0] + dv[0]], sorted(merged.items())


def unsat(proof, state, constraints):
    steps, end = proof
    for ci, am, bm in steps:
        (a, b), pairs = constraints[ci]
        live = {(i, j) for i, j in pairs if i in state[a] and j in state[b]}
        aa, bb = {i for i, _ in live}, {j for _, j in live}
        assert aa and bb and (aa, bb) != (state[a], state[b])
        assert (am, bm) == (sum(1 << i for i in aa), sum(1 << j for j in bb))
        state[a], state[b] = aa, bb
    if end[0] == 'empty':
        (a, b), pairs = constraints[end[1]]
        assert not any(i in state[a] and j in state[b] for i, j in pairs)
    else:
        assert end[0] == 'branch'
        v, children = end[1:]
        assert [c for c, _ in children] == sorted(state[v])
        for c, child in children:
            narrowed = state.copy()
            narrowed[v] = {c}
            unsat(child, narrowed, constraints)


def run_coverage(retaining, omitted):
    """Independent marked compression controls; unbounded argument is in REPORT.

    Generate lengths through 12, compress each UNMARKED gap by parity, and
    check every adjacent bridge marker against the saved 344-form domain.
    """
    counts = Counter()
    for size in (2, 3, 4):
        for available in combinations(range(4), size):
            for left, right in product(range(4), repeat=2):
                outcomes = []
                for length in range(1, 13):
                    last = set(available) - {left}
                    for _ in range(length - 1):
                        last = {c for c in available if any(c != d for d in last)}
                    outcomes.append(bool(last - {right}))
                assert all(outcomes[n] == outcomes[n % 2] for n in range(12))
                counts['transfer_queries'] += 12
    domain = {(tuple(map(tuple, f['edges'])), tuple(f['original_root_order'])) for f in omitted}
    reached = set()

    def make(tails, triangle, marked=None):
        edges = set(FRAME)
        next_vertex = 8 if triangle else 5
        if triangle:
            edges |= set(combinations((5, 6, 7), 2))
            for v, support in enumerate(triangle, 5):
                edges |= {(b, v) for b in support}
        ports = {}
        for slot, tail in enumerate(tails):
            previous = 5 + slot if triangle else None
            for support, label in tail:
                v = next_vertex
                next_vertex += 1
                edges |= {(b, v) for b in support}
                if previous is not None:
                    edges.add((previous, v))
                if label is not None:
                    ports[label] = v
                previous = v
        if marked:
            for i, v in enumerate(marked):
                if v < 8 and triangle:
                    ports[i] = v
        return tuple(sorted(edges)), tuple(sorted(ports.values()))

    def check(tails, triangle):
        plain = [[(s, None) for s in t] for t in tails]
        edges, _ = make(plain, triangle)
        candidates = [e for e in edges if e[0] >= 5 and
                      (not triangle or not set(e) <= {5, 6, 7})]
        for pair in candidates:
            tagged, vertex = [], 8 if triangle else 5
            for tail in tails:
                t = []
                for support in tail:
                    t.append((support, pair.index(vertex) if vertex in pair else None))
                    vertex += 1
                tagged.append(t)
            reduced = []
            for tail in tagged:
                if not tail:
                    reduced.append([])
                    continue
                # Leaves stay singleton; all other same-support runs may compress.
                result, start = [], 0
                while start < len(tail) - 1:
                    end = start + 1
                    while end < len(tail) - 1 and tail[end][0] == tail[start][0]:
                        end += 1
                    gap = []
                    for item in tail[start:end]:
                        if item[1] is None:
                            gap.append(item)
                        else:
                            result.extend(gap[:1 if len(gap) % 2 else 2] if gap else [])
                            gap = []
                            result.append(item)
                    result.extend(gap[:1 if len(gap) % 2 else 2] if gap else [])
                    start = end
                result.append(tail[-1])
                reduced.append(result)
            signature = make(reduced, triangle, pair)
            assert signature in domain, ('marked compression missing', signature)
            reached.add(signature)
            counts['marked_compressions'] += 1

    for form in retaining:
        if not form['family'].startswith('single_triangle'):
            continue
        edges = edge_set(form['edges'])
        internal = {v for v in form['interior_order']}
        tails = []
        for parent in (5, 6, 7):
            tail, previous, v = [], parent, next((v for v in internal - {5, 6, 7}
                if tuple(sorted((parent, v))) in edges), None)
            while v is not None:
                tail.append(form['neighborhoods'][v - 5])
                following = [u for u in internal if u != previous and tuple(sorted((u, v))) in edges]
                assert len(following) <= 1
                previous, v = v, following[0] if following else None
            tails.append(tail)
        if form['family'] == 'single_triangle_two_runs':
            assert len(tails[0]) == 4 and not tails[1] and not tails[2]
            first, other, _, leaf = tails[0]
            for length in range(2, 13, 2):
                check([[first] + [other] * length + [leaf], [], []], form['neighborhoods'][:3])
        else:
            lengths = [range(1, 12, 2) if tail else (0,) for tail in tails]
            for lens in product(*lengths):
                check([[tail[0]] * length + [tail[-1]] if tail else []
                       for tail, length in zip(tails, lens, strict=True)], form['neighborhoods'][:3])
    L, R, A, C = [0, 1, 4], [2, 3, 4], [1, 4], [2, 4]
    for runs in ([], [A], [C], [A, C]):
        for lens in product(range(2, 13, 2), repeat=len(runs)):
            tail = [L] + [s for s, n in zip(runs, lens, strict=True) for _ in range(n)] + [R]
            for oriented in (tail, list(reversed(tail))):
                check([oriented], None)
    # The double-triangle family has no uniform run to compress.
    for form in omitted:
        if form['family'] == 'double_triangle':
            reached.add((tuple(map(tuple, form['edges'])), tuple(form['original_root_order'])))
    assert reached == domain and len(domain) == 344
    counts['covered_marked_forms'] = len(reached)
    return dict(counts)


def audit(name, common):
    path = ROOT / f'artifacts/c5_excess_two_{name}/observations.json'
    data = json.loads(path.read_text())
    hashes = {str(path.relative_to(ROOT)): sha256(path.read_bytes()).hexdigest()}
    for rel, expected in data['source_sha256'].items():
        actual = sha256((ROOT / rel).read_bytes()).hexdigest()
        assert actual == expected, f'Historical provenance mismatch: {rel}'
        hashes[rel] = actual
    rows = data['pattern_order']
    assert len(set(map(tuple, rows))) == 10 and rows == common.setdefault('rows', rows)
    targets = orbits(rows)
    assert targets == data['target_D5_orbits']
    all_targets = set().union(*map(set, targets.values()))
    binary = name == 'mixed_omission'
    forms = data['original_marked_cores'] if binary else data['necessary_forms']
    count = Counter(forms=len(forms))
    unary = domains(rows)
    if name != 'mixed_core_spokes':
        rebuilt = domains(rows, binary) if binary else unary
        compare_domains(data['fixed_support_domains'], rebuilt, binary)
    if binary:
        topology = data['contraction_star_subdivisions']
    elif name == 'mixed_core_spoke_unary':
        topology = data['original_contracted_star_obstructions']
    elif name == 'mixed_core_two_unary':
        topology = data['same_source_two_star_subdivisions']
    else:
        topology = []
    keys = set()
    for fi, form in enumerate(forms):
        edges = edge_set(form['edges'] if 'edges' in form else form['original_edges'])
        order = form.get('original_coloring_order', form.get('witness_vertex_order',
                    list(range(max(max(e) for e in edges) + 1))))
        keys.add(tuple(sorted(edges)))
        critical(form, edges, rows[0], order)
        marks = [form] if binary else form['marked_cores']
        expected_marks = {e for t in combinations([v for v in order if v >= 5], 3)
                          if all(e in edges for e in combinations(t, 2)) for e in combinations(t, 2)}
        if not binary:
            assert {tuple(m.get('original_root_order', m.get('root_order'))) for m in marks} == expected_marks
        for mark in marks:
            pair = tuple(mark.get('original_root_order', mark.get('root_order')))
            assert pair in edges
            cut = edges - {pair}
            ks = [relation(edges, row, pair) for row in rows]
            count['independent_core_rows'] += 10
            assert sum(1 << i for i, k in enumerate(ks) if k) == 1022
            count['marked_cores'] += 1
            if name == 'mixed_core_spokes':
                kernel = [relation(cut, row, pair) for row in rows]
                assert [set(map(tuple, r['ordered_relation'])) for r in mark['root_edge_deleted_kernel']] == kernel
                additions = mark['restorations']
                expected = set(product([b for b in range(5) if (b, pair[0]) not in edges],
                                       [b for b in range(5) if (b, pair[1]) not in edges]))
                assert {tuple(e[0] for e in a['original_omitted_spokes']) for a in additions} == expected
                for addition in additions:
                    restored = addition['original_omitted_spokes']
                    assert edge_set(addition['G_edges']) == edges | set(map(tuple, restored))
                    sigma = sum(1 << i for i, k in enumerate(ks) if any(
                        a != rows[i][restored[0][0]] and b != rows[i][restored[1][0]] for a, b in k))
                    assert sigma == addition['sigma'] and sigma not in all_targets
                    count['restorations'] += 1
            elif name == 'mixed_core_spoke_unary':
                additions = mark['original_restorations']
                assert {tuple(a['original_spoke']) for a in additions} == {
                    (b, r) for r in pair for b in range(5) if (b, r) not in edges}
                for addition in additions:
                    b, r = addition['original_spoke']
                    side = pair.index(r)
                    colors = [{t[1 - side] for t in k if t[side] != row[b]}
                              for k, row in zip(ks, rows, strict=True)]
                    assert colors == [set(r['unary_root_colors']) for r in addition['rows']]
                    exclusions = addition['target_exclusions']
                    assert len(exclusions) == 10 and {e['target_mask'] for e in exclusions} == all_targets
                    for exc in exclusions:
                        target = exc['target_mask']
                        if exc['reason'] == 'target_accepted_row_already_empty':
                            ri = exc['row_index']
                            assert target >> ri & 1 and not colors[ri]
                        elif exc['reason'] == 'survives_every_nonempty_original_unary':
                            ri = exc['row_index']
                            assert not target >> ri & 1 and len(colors[ri]) >= 2
                        else:
                            assert exc['reason'] == 'fixed_support_equivariance_or_original_star_minor'
                            assert [t['support_id'] for t in exc['support_tests']] == list(range(32))
                            for mask, test in enumerate(exc['support_tests']):
                                compatible = possible(colors, target, unary[mask])
                                assert compatible == ('contracted_star_obstruction_id' in test)
                                if compatible:
                                    rec = topology[test['contracted_star_obstruction_id']]
                                    assert rec['form_id'] == fi and rec['original_root_order'] == list(pair)
                                    assert rec['original_restored_spoke'] == [b, r]
                                    assert rec['actual_unary_boundary_support'] == [j for j in range(5) if mask >> j & 1]
                                count['support_tests'] += 1
                        count['target_comparisons'] += 1
                    count['restorations'] += 1
            elif name == 'mixed_core_two_unary':
                coverage = {tuple(c['actual_support_masks']): c['obstruction_id']
                            for c in mark['same_source_actual_support_minor_coverage']}
                exclusions = mark['target_exclusions']
                assert len(exclusions) == 10 and {e['target_mask'] for e in exclusions} == all_targets
                for exc in exclusions:
                    target = exc['target_mask']
                    if exc['reason'] == 'target_accepted_row_already_empty':
                        ri = exc['row_index']
                        assert target >> ri & 1 and not ks[ri]
                    elif exc['reason'] == 'survives_every_two_nonempty_original_unaries':
                        ri = exc['row_index']
                        assert not target >> ri & 1 and all(any(x != a and y != b for x, y in ks[ri])
                            for a, b in product(range(-1, 4), repeat=2))
                    else:
                        assert exc['reason'] == 'fixed_two_support_functions_or_same_source_two_star_minor'
                        query = data['shared_support_queries'][exc['shared_support_query_id']]
                        assert query['target_mask'] == target
                        assert [set(map(tuple, k)) for k in query['root_pair_relations']] == ks
                        for su, sv in query['compatible_support_pairs']:
                            rec = topology[coverage[su, sv]]
                            assert rec['form_id'] == fi and rec['original_root_order'] == list(pair)
                            ru, rv = rec['retained_support_masks']
                            assert ru & su == ru and rv & sv == rv
                    count['target_comparisons'] += 1
            else:
                assert ks == [set(map(tuple, r['original_bridge_retained_pairs'])) for r in form['rows']]
                exclusions = form['target_comparisons']
                assert len(exclusions) == 10 and {e['target_mask'] for e in exclusions} == all_targets
                for exc in exclusions:
                    target = exc['target_mask']
                    if exc['exclusion'] == 'target_accepts_empty_core_row':
                        ri = exc['row_index']
                        assert target >> ri & 1 and not ks[ri]
                    elif exc['exclusion'] == 'mixed_capacity':
                        ri = exc['row_index']
                        k = ks[ri]
                        assert not target >> ri & 1 and k and (len(k) > 2 or
                            len({a for a, _ in k}) != len(k) or len({b for _, b in k}) != len(k))
                    else:
                        assert exc['exclusion'] == 'fixed_support_transport_or_nondisk_star'
                        assert [t['support_id'] for t in exc['support_tests']] == list(range(32))
                        for mask, test in enumerate(exc['support_tests']):
                            compatible = possible(ks, target, rebuilt[mask], True)
                            assert compatible == ('contraction_star_subdivision_index' in test)
                            if compatible:
                                rec = topology[test['contraction_star_subdivision_index']]
                                assert rec['form_id'] == fi and rec['original_root_order'] == list(pair)
                                assert rec['actual_boundary_support'] == [j for j in range(5) if mask >> j & 1]
                            count['support_tests'] += 1
                    count['target_comparisons'] += 1
    if not binary:
        assert keys == common.setdefault('retaining_core_edges', keys)
        if name == 'mixed_core_spokes':
            common['retaining_forms'] = forms
    else:
        count.update(run_coverage(common['retaining_forms'], forms))
    for rec in topology:
        form = forms[rec['form_id']]
        edges = edge_set(form.get('edges', form.get('original_edges')))
        pair = rec['original_root_order']
        apex = rec['boundary_apex']
        expected = edges | {(b, apex) for b in range(5)}
        if name == 'mixed_core_spoke_unary':
            c = rec['contracted_original_unary_vertex']
            assert rec['unary_root'] == pair[1 - pair.index(rec['spoke_root'])]
            assert rec['original_restored_spoke'][1] == rec['spoke_root']
            expected |= {tuple(rec['original_restored_spoke']), tuple(sorted((rec['unary_root'], c)))}
            expected |= {(b, c) for b in rec['actual_unary_boundary_support']}
        elif name == 'mixed_core_two_unary':
            assert rec['retained_boundary_supports'] == [[b for b in range(5) if mask >> b & 1]
                                                        for mask in rec['retained_support_masks']]
            for r, c, support in zip(pair, rec['contracted_original_unary_vertices'],
                                     rec['retained_boundary_supports'], strict=True):
                expected |= {tuple(sorted((r, c)))} | {(b, c) for b in support}
        else:
            c = rec['contracted_original_mixed_vertex']
            expected |= {tuple(sorted((r, c))) for r in pair} | {(b, c) for b in rec['actual_boundary_support']}
        subdivision(rec, expected)
        count['subdivisions'] += 1
    if name == 'mixed_core_two_unary':
        for query in data['shared_support_queries']:
            assert len(query['tests']) == 1024
            compatible = []
            for index, (tag, proof) in enumerate(query['tests']):
                su, sv = divmod(index, 32)
                state, constraints = tables(query['root_pair_relations'], query['target_mask'], unary[su], unary[sv])
                if tag == 0:
                    unsat(proof, state, constraints)
                    count['unsat_proofs'] += 1
                else:
                    assert tag == 1 and len(proof) == len(state)
                    assert all(c in s for c, s in zip(proof, state, strict=True))
                    assert all((proof[a], proof[b]) in ps for (a, b), ps in constraints)
                    compatible.append([su, sv])
                    count['compatible_assignments'] += 1
            assert compatible == query['compatible_support_pairs']
    return {'status': 'PASS', 'counts': dict(count), 'input_sha256': hashes}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    common, result = {}, {}
    for name in ('mixed_core_spokes', 'mixed_core_spoke_unary', 'mixed_core_two_unary', 'mixed_omission'):
        result[name] = audit(name, common)
        print(name, json.dumps(result[name]['counts'], sort_keys=True), flush=True)
    result['verifier_sha256'] = sha256(Path(__file__).read_bytes()).hexdigest()
    if args.output:
        args.output.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + '\n')


if __name__ == '__main__':
    main()
