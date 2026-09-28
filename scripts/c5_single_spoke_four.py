#!/usr/bin/env python3
"""Three rejected palettes on one block tree: local and source-minor controls.

The unbounded structure/tether proof is in docs/c5_single_spoke_four.md.
The skeletons below are not disk realizations or a source-graph catalogue.
Only this layer's artifact is written.
"""
import argparse
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, permutations, product
import json
from pathlib import Path

from c5_single_spoke_three_one import edge, validate_minor

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_single_spoke_four/observations.json'
U = frozenset(range(4))
Q = (0, 1, 0, 1, 2)
RHO = (3, 2, 1, 0, 4)
PI = (1, 0, 2, 3)


def subsets(xs):
    return [frozenset(c) for n in range(len(xs) + 1)
            for c in combinations(sorted(xs), n)]


def pair_sign(x, y, a, b):
    return next((t for t in (-1, 0, 1) if all(
        int(c in x) - int(c in y) == t * (int(c == b) - int(c == a))
        for c in U)), None)


def block_table(e):
    available = sorted(U - {e})
    records = []
    for size in (1, 2):
        palettes = [p for p in subsets(U) if len(p) == size]
        for rows in product(palettes, repeat=3):
            signs = [pair_sign(rows[i], rows[j], available[i], available[j])
                     for i, j in combinations(range(3), 2)]
            if None in signs:
                continue
            assert len(set(signs)) == 1
            sign = signs[0]
            if sign == 1:
                assert size == 2
                assert all(p == U - {e, d} for d, p in zip(available, rows))
            elif sign == -1:
                assert all(p == ({d} if size == 1 else {d, e})
                           for d, p in zip(available, rows))
            else:
                assert rows[0] == rows[1] == rows[2]
            records.append(dict(size=size, sign=sign,
                                palettes=[sorted(p) for p in rows]))
    assert len(records) == 13
    return records


def incidence_table(e, blocks):
    available = sorted(U - {e})
    records = []
    for count in range(1, 5):
        for ids in combinations_with_replacement(range(len(blocks)), count):
            bs = [blocks[i] for i in ids]
            degree = sum(b['size'] for b in bs)
            if degree > 4:
                continue
            rows = [set().union(*(set(b['palettes'][j]) for b in bs))
                    for j in range(3)]
            if any(len(row) != degree for row in rows):
                continue
            signs = [pair_sign(rows[i], rows[j], available[i], available[j])
                     for i, j in combinations(range(3), 2)]
            if signs == [0, 0, 0]:
                contact = False
            elif signs == [1, 1, 1] and degree <= 3:
                contact = True
            else:
                continue
            active = sorted(b['sign'] for b in bs if b['sign'])
            assert active in ([[1]] if contact else [[], [-1, 1]])
            records.append(dict(block_ids=list(ids), contact=contact,
                                degree_in_C=degree, active_signs=active,
                                lists=[sorted(p) for p in rows]))
    return records


def attachments():
    records = []
    for s, contact, support in product(range(5), (False, True), subsets(range(5))):
        degree = 4 - len(support) - int(contact)
        if degree < 1:
            continue
        available = sorted(U - {Q[s]})
        external = [Q[i] for i in sorted(support)]
        rows = [U - set(external + ([d] if contact else [])) for d in available]
        if any(len(p) != degree for p in rows):
            continue
        for i, j in combinations(range(3), 2):
            assert pair_sign(rows[i], rows[j], available[i], available[j]) == int(contact)
        if contact:
            assert set(external) <= {Q[s]} and len(external) <= 1
        records.append(dict(spoke=s, contact=contact, support=sorted(support),
                            degree_in_C=degree, rejected=available,
                            lists=[sorted(p) for p in rows]))
    by_key = {(r['spoke'], r['contact'], tuple(r['support'])): r for r in records}
    for r in records:
        target = by_key[RHO[r['spoke']], r['contact'],
                        tuple(sorted(RHO[i] for i in r['support']))]
        moved = {PI[d]: sorted(PI[c] for c in p)
                 for d, p in zip(r['rejected'], r['lists'])}
        assert target['lists'] == [moved[d] for d in target['rejected']]
    return records


def forest_controls():
    # The paper proves these are the only four-leaf shapes for arbitrary lengths.
    # Here we independently solve sign alternation on bounded subdivisions.
    connected = []
    for gap, arms in product(range(5), product(range(4), repeat=4)):
        solutions = []
        for left in (-1, 1):
            right = left * (-1) ** (gap + 1)
            bridge_signs = [left * (-1) ** i for i in range(1, gap + 1)]
            ends = []
            for center, length in zip((left, left, right, right), arms):
                bridge_signs.extend(center * (-1) ** i for i in range(1, length + 1))
                ends.append(center * (-1) ** length)
            if ends != [1] * 4:
                continue
            # A bridge cannot have the common positive sign for three rows.
            if 1 in bridge_signs:
                continue
            solutions.append([left, right])
        expected = gap == 1 and arms == (0, 0, 0, 0)
        assert bool(solutions) == expected
        if expected:
            assert solutions == [[1, 1]]
        connected.append(dict(central_bridges=gap, arm_lengths=list(arms),
                              triangle_signs=solutions))
    split = []
    for lengths in product(range(1, 8), repeat=2):
        valid = True
        for length in lengths:
            signs = [(-1) ** i for i in range(length)]
            valid &= signs[-1] == 1 and 1 not in signs
        assert not valid
        split.append(dict(path_lengths=list(lengths), compatible=valid))
    return connected, split


def full_relations():
    # One common six-vertex graph, preserving all four coordinates at once.
    # Every vertex has the abstract residual list U\{e}; these are not disk claims.
    internal_edges = [(0, 1), (0, 4), (1, 4), (2, 3), (2, 5), (3, 5), (4, 5)]
    results = []
    for e in range(4):
        available = U - {e}
        colorings = [p for p in product(sorted(available), repeat=6)
                     if all(p[i] != p[j] for i, j in internal_edges)]
        relation = sorted({p[:4] for p in colorings})
        forbidden = set.intersection(*(set(t) for t in relation))
        assert len(colorings) == len(relation) == 24 and forbidden == available
        witnesses = []
        for d, j in product(sorted(available), range(4)):
            t = next(t for t in relation if t[j] == d
                     and all(t[k] != d for k in range(4) if k != j))
            witnesses.append(dict(rejected=d, contact=j, tuple=list(t)))
        results.append(dict(excluded_color=e, edges=internal_edges,
                            contact_order=[0, 1, 2, 3], relation=relation,
                            forbidden=sorted(forbidden), release_witnesses=witnesses))
    return results


def minor(s, order, lengths, targets):
    # order gives geometric roles; the named tuple coordinates remain u0..u3.
    a, b, c, d = [f'u{i}' for i in order]
    es = {edge(f'b{i}', f'b{(i+1)%5}') for i in range(5)}
    es.add(edge('z', f'b{s}'))
    es.update(edge('z', f'u{i}') for i in range(4))
    es.update(edge(u, v) for tri in ((a, b, 'x'), (c, d, 'y'))
              for u, v in combinations(tri, 2))
    es.add(edge('x', 'y'))
    groups = [{a}, {b}, {'x'}, {'z', c, d, 'y'}, {f'b{i}' for i in range(5)}]
    tethers = []
    for i, (v, length, target) in enumerate(zip((a, b, 'x'), lengths, targets)):
        tether = [v] + [f'w{i}_{j}' for j in range(length - 1)] + [f'b{target}']
        es.update(edge(u, w) for u, w in zip(tether, tether[1:]))
        groups[4].update(tether[1:-1])
        tethers.append(tether)
    record = dict(spoke=s, contact_order=[f'u{i}' for i in range(4)],
                  triangle_roles=[a, b, 'x', c, d, 'y'], tethers=tethers,
                  edges=sorted(es), branch_sets=[sorted(g) for g in groups])
    assert validate_minor(record)
    assert {v if u == 'z' else u for u, v in es if 'z' in (u, v)} == {
        'u0', 'u1', 'u2', 'u3', f'b{s}'}
    record['adjacency'] = [dict(pair=[i, j], edge=next(
        edge(u, v) for u in sorted(groups[i]) for v in sorted(groups[j])
        if edge(u, v) in es)) for i, j in combinations(range(5), 2)]
    return record


def negative_controls(base):
    results = []
    a, b, x, c, d, y = base['triangle_roles']
    failures = [('missing_spoke', [edge('z', 'b0')]),
                ('missing_contact', [edge('z', a)]),
                ('missing_central_bridge', [edge(x, y)]),
                ('missing_triangle_edge', [edge(a, b)]),
                ('missing_tether', [edge(*base['tethers'][2][:2])]),
                ('disconnected_Z', [edge('z', c), edge('z', d)])]
    for name, removed in failures:
        damaged = dict(base, edges=[e for e in base['edges'] if e not in removed])
        assert not validate_minor(damaged)
        results.append(name)
    groups = [list(g) for g in base['branch_sets']]
    groups[0].append('z')
    assert not validate_minor(dict(base, branch_sets=groups))
    results.append('overlapping_branch_sets')
    # The predecessor's two-path countercontrol cannot acquire a third row:
    # a positive bridge would require a two-color palette.
    for third in subsets(U):
        if len(third) == 1:
            assert not (pair_sign({1}, third, 0, 2) == 1
                        and pair_sign({0}, third, 1, 2) == 1)
    results.append('two_row_positive_bridge_has_no_third_row')
    return results


def run():
    blocks = {e: block_table(e) for e in range(4)}
    incidence = {e: incidence_table(e, blocks[e]) for e in range(4)}
    attachment_rows = attachments()
    connected, split = forest_controls()
    relations = full_relations()
    minors = []
    length_cases = [(1, 1, 1), (1, 2, 3), (3, 1, 2), (2, 3, 1)]
    for s, order, lengths, coincident in product(
            range(5), permutations(range(4)), length_cases, (False, True)):
        targets = (s, s, s) if coincident else tuple((s+i) % 5 for i in (1, 3, 4))
        minors.append(minor(s, order, lengths, targets))
    for r in minors:
        def move(v):
            return f'b{RHO[int(v[1:])]}' if v.startswith('b') else v
        reflected = dict(r, edges=[edge(move(u), move(v)) for u, v in r['edges']],
                         branch_sets=[[move(v) for v in g] for g in r['branch_sets']])
        assert validate_minor(reflected)
        assert [move(v) for v in r['contact_order']] == r['contact_order']
    negatives = negative_controls(minor(0, (0, 1, 2, 3), (1, 1, 1), (0, 0, 0)))
    inputs = ['scripts/c5_single_spoke_three_one.py',
              'artifacts/c5_single_spoke_three_one/observations.json',
              'scripts/c5_single_spoke_cores.py',
              'artifacts/c5_single_spoke_cores/observations.json']
    return dict(scope='finite controls for a paper arbitrary-size exclusion; no disk realization or Lean theorem',
                inputs_sha256={p: sha256((ROOT / p).read_bytes()).hexdigest() for p in inputs},
                block_palettes=blocks, local_incidence=incidence,
                tight_attachments=attachment_rows, connected_forests=connected,
                split_forests=split, full_relations=relations, minors=minors,
                negative_controls=negatives,
                summary=dict(block_palette_triples_tested=4*(4**3+6**3),
                             compatible_block_triples=sum(map(len, blocks.values())),
                             local_incidence_states=sum(map(len, incidence.values())),
                             tight_attachment_rows=len(attachment_rows),
                             connected_forest_controls=len(connected),
                             split_forest_controls=len(split), full_relations=len(relations),
                             one_spoke_K5_certificates=len(minors), reflected_minors=len(minors),
                             negative_controls=len(negatives)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = run()
    payload = json.dumps(result, sort_keys=True, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == payload, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
