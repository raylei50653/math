#!/usr/bin/env python3
"""Finite controls for the no-spoke exterior and four branch exclusions.

The arbitrary-size proofs are in docs/c5_no_spoke_exterior.md. Cover tables
are necessary algebra only; minor skeletons are not degree-list disk sources.
Only this layer's artifact is written.
"""
import argparse
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, permutations, product
import json
from pathlib import Path

from c5_single_spoke_four import pair_sign
from c5_single_spoke_three_one import edge, validate_minor

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_no_spoke_exterior/observations.json'
U = frozenset(range(4))
RHO = (3, 2, 1, 0, 4)
PI = (1, 0, 2, 3)
PARTITIONS = ((5,), (4, 1), (3, 2), (3, 1, 1), (2, 2, 1), (2, 1, 1, 1))


def subsets(xs):
    return [frozenset(c) for n in range(len(xs) + 1)
            for c in combinations(sorted(xs), n)]


def covers():
    records = []
    for partition in PARTITIONS:
        choices = [[f for f in subsets(U) if 0 < len(f) <= k] for k in partition]
        for fs in product(*choices):
            if set().union(*fs) != U:
                continue
            private = [f - set().union(*(g for j, g in enumerate(fs) if i != j))
                       for i, f in enumerate(fs)]
            if not all(private):
                continue
            if len(fs) > 1:
                assert all(f != U for f in fs)
            if partition == (5,):
                reason = 'four_rejections_odd_contacts'
            elif partition == (4, 1):
                assert len(fs[0]) == 3 and fs[0] == U - fs[1]
                reason = 'four_contacts_three_rejections'
            elif partition in ((3, 2), (3, 1, 1)):
                assert len(fs[0]) >= 2
                reason = 'three_contacts_two_rejections'
            else:
                reason = 'open'
                sizes = tuple(map(len, fs))
                if partition == (2, 2, 1):
                    assert sizes in ((2, 1, 1), (1, 2, 1), (2, 2, 1))
                    if sizes == (2, 2, 1):
                        assert len(fs[0] & fs[1]) == 1
                        assert fs[2] == U - (fs[0] | fs[1])
                else:
                    assert sizes == (1, 1, 1, 1)
            records.append(dict(partition=list(partition), forbidden=[sorted(f) for f in fs],
                                private=[sorted(p) for p in private], status=reason))
    keys = {(tuple(r['partition']), tuple(tuple(f) for f in r['forbidden'])) for r in records}
    for r in records:
        assert (tuple(r['partition']), tuple(tuple(sorted(PI[c] for c in f))
                                             for f in r['forbidden'])) in keys
    # No boundary support gives the full S4 symmetry, not just one swap.
    invariant = [f for f in subsets(U) if all(
        {p[c] for c in f} == f for p in permutations(range(4)))]
    assert invariant == [frozenset(), U]
    return records


def four_palettes():
    records = []
    pairs = list(combinations(range(4), 2))
    for size in (1, 2, 3):
        options = [s for s in subsets(U) if len(s) == size]
        for rows in product(options, repeat=4):
            signs = [pair_sign(rows[a], rows[b], a, b) for a, b in pairs]
            if None in signs:
                continue
            assert len(set(signs)) == 1
            sign = signs[0]
            if sign == 1:
                assert size == 3 and all(rows[d] == U - {d} for d in U)
            elif sign == -1:
                assert size == 1 and all(rows[d] == {d} for d in U)
            else:
                assert len(set(rows)) == 1
            records.append(dict(size=size, sign=sign, palettes=[sorted(p) for p in rows]))
    assert len(records) == 16
    palette_keys = {(r['size'], r['sign'], tuple(tuple(p) for p in r['palettes'])) for r in records}
    for r in records:
        moved = {PI[d]: tuple(sorted(PI[c] for c in p)) for d, p in enumerate(r['palettes'])}
        assert (r['size'], r['sign'], tuple(moved[d] for d in range(4))) in palette_keys
    incidence = []
    for count in range(1, 5):
        for ids in combinations_with_replacement(range(len(records)), count):
            bs = [records[i] for i in ids]
            degree = sum(b['size'] for b in bs)
            if degree > 4:
                continue
            rows = [set().union(*(set(b['palettes'][d]) for b in bs)) for d in U]
            if any(len(row) != degree for row in rows):
                continue
            for contact in (False, True):
                if degree + int(contact) > 4:
                    continue
                if any(pair_sign(rows[a], rows[b], a, b) != int(contact) for a, b in pairs):
                    continue
                active = [b['sign'] for b in bs if b['sign']]
                if contact:
                    assert sorted(active) == [1] and len(bs) == 1 and degree == 3
                elif active:
                    assert sorted(active) == [-1, 1] and len(bs) == 2 and degree == 4
                incidence.append(dict(block_ids=list(ids), contact=contact,
                                      degree_in_C=degree, active_signs=sorted(active)))
    return records, incidence


def relation_controls():
    results = []
    for count in (1, 2):
        vertices = list(range(4 * count))
        edges = [(4*i+a, 4*i+b) for i in range(count) for a, b in combinations(range(4), 2)]
        if count == 2:
            edges.append((3, 4))
        ports = vertices if count == 1 else [0, 1, 2, 5, 6, 7]
        colorings = [f for f in product(range(4), repeat=len(vertices))
                     if all(f[u] != f[v] for u, v in edges)]
        relation = sorted({tuple(f[v] for v in ports) for f in colorings})
        forbidden = set.intersection(*(set(t) for t in relation))
        assert forbidden == U and len(ports) == 2 + 2 * count
        assert all({t[i] for t in relation} == U for i in range(len(ports)))
        # The product of endpoint marginals would incorrectly allow every z color.
        marginal_product = product(range(4), repeat=len(ports))
        assert set.intersection(*(set(t) for t in marginal_product)) == set()
        record = dict(K4_count=count, edges=edges, contact_order=ports,
                      relation=relation, forbidden=sorted(forbidden))
        if count == 2:
            five_ports = ports[:-1]
            reduced = sorted({tuple(f[v] for v in five_ports) for f in colorings})
            assert set.intersection(*(set(t) for t in reduced)) == set()
            record['five_contact_negative'] = dict(contact_order=five_ports, relation=reduced,
                                                    forbidden=[])
            record['five_contact_negative_scope'] = 'removed contact loses full-degree-4 premise'
        results.append(record)
    return results


def add_path(es, path):
    es.update(edge(u, v) for u, v in zip(path, path[1:]))


def finish(kind, es, groups, **extra):
    record = dict(kind=kind, edges=sorted(es), branch_sets=[sorted(g) for g in groups], **extra)
    assert validate_minor(record)
    record['adjacency'] = [dict(pair=[i, j], edge=next(
        edge(u, v) for u in sorted(groups[i]) for v in sorted(groups[j]) if edge(u, v) in es))
        for i, j in combinations(range(5), 2)]
    return record


def skeleton(kind, target, long, mask=0, lengths=(0, 0, 0), partition=(3, 2), order=(0, 1, 2, 3)):
    es = {edge(f'b{i}', f'b{(i+1)%5}') for i in range(5)}
    boundary = {f'b{i}' for i in range(5)}
    external = ['z', 'd0'] + (['d1', 'd2'] if long else []) + [f'b{target}']
    add_path(es, external)
    tethers = []
    if kind == 'K4':
        core = [f'k{i}' for i in range(4)]
        es.update(edge(u, v) for u, v in combinations(core, 2))
        groups = [{v} for v in core] + [boundary | set(external)]
        for i, v in enumerate(core):
            end = 'z' if mask & (1 << i) else f'b{(target+i)%5}'
            path = [v] + ([f'w{i}_0', f'w{i}_1'] if long else []) + [end]
            add_path(es, path)
            groups[4].update(path[1:])
            tethers.append(path)
        return finish(kind, es, groups, external_path=external, tethers=tethers,
                      target=target, z_tether_mask=mask)
    if kind == 'three_contact':
        core = [f'v{i}' for i in range(3)]
        es.update(edge(u, v) for u, v in combinations(core, 2))
        groups = [{'z'}] + [{v} for v in core] + [boundary | set(external[1:])]
        ports, arms = [], []
        for i, (v, length) in enumerate(zip(core, lengths)):
            path = [v] + [f'a{i}_{j}' for j in range(length)]
            add_path(es, path)
            es.add(edge('z', path[-1]))
            groups[i+1].update(path)
            arms.append(path)
            ports.append(path[-1])
        es.add(edge('z', 'd_extra'))
        if partition == (3, 2):
            es.add(edge('d0', 'd_extra'))
        else:
            es.add(edge('d_extra', f'b{(target+1)%5}'))
        components = [ports, ['d0', 'd_extra']] if partition == (3, 2) else [ports, ['d0'], ['d_extra']]
        extra = dict(arms=arms, contact_components=components)
    else:
        a, b, c, d = [f'u{i}' for i in order]
        core = [a, b, 'x']
        es.update(edge(u, v) for tri in (core, [c, d, 'y']) for u, v in combinations(tri, 2))
        es.add(edge('x', 'y'))
        es.update(edge('z', f'u{i}') for i in range(4))
        groups = [{v} for v in core] + [{'z', c, d, 'y'}, boundary | set(external[1:])]
        components = [[f'u{i}' for i in range(4)], ['d0']]
        extra = dict(contact_components=components, triangle_roles=core + [c, d, 'y'])
    for i, v in enumerate(core):
        path = [v] + ([f'w{i}_0', f'w{i}_1'] if long else []) + [f'b{(target+i)%5}']
        add_path(es, path)
        groups[4].update(path[1:])
        tethers.append(path)
    contacts = set().union(*(set(p) for p in components))
    assert len(contacts) == 5
    assert {v if u == 'z' else u for u, v in es if 'z' in (u, v)} == contacts
    # Read back H-z from the actual skeleton edges; labels alone do not certify
    # that all original contacts remain in the stated distinct components.
    interior = set().union(*(set(e) for e in es)) - boundary - {'z'}
    pending, actual = set(interior), []
    while pending:
        seen = {min(pending)}
        while True:
            expanded = seen | {v for u in seen for v in interior if edge(u, v) in es}
            if expanded == seen:
                break
            seen = expanded
        pending -= seen
        actual.append(frozenset(seen & contacts))
    assert set(actual) == {frozenset(p) for p in components}
    return finish(kind, es, groups, external_path=external, tethers=tethers, target=target, **extra)


def minor_controls():
    records = [skeleton('K4', t, long, mask=mask)
               for t, long, mask in product(range(5), (False, True), range(16))]
    arm_cases = [(0, 0, 0), (0, 2, 0), (2, 0, 2), (2, 2, 2),
                 (1, 1, 1), (1, 3, 1), (3, 1, 3), (3, 3, 3)]
    records += [skeleton('three_contact', t, long, lengths=ls, partition=p)
                for t, long, ls, p in product(range(5), (False, True), arm_cases, ((3, 2), (3, 1, 1)))]
    records += [skeleton('four_contact', t, long, order=o)
                for t, long, o in product(range(5), (False, True), permutations(range(4)))]
    for r in records:
        def move(v):
            return f'b{RHO[int(v[1:])]}' if v.startswith('b') else v
        assert validate_minor(dict(r, edges=sorted(edge(move(u), move(v)) for u, v in r['edges']),
                                   branch_sets=[[move(v) for v in g] for g in r['branch_sets']]))
        assert not any(u == 'z' and v.startswith('b') or v == 'z' and u.startswith('b')
                       for u, v in r['edges'])
    negatives = []
    for kind in ('K4', 'three_contact', 'four_contact'):
        base = skeleton(kind, 0, False, mask=3)
        for name, removed in [('missing_external_path', edge('z', 'd0')),
                              ('missing_tether', edge(*base['tethers'][0][:2]))]:
            damaged = dict(base, edges=[e for e in base['edges'] if e != removed])
            assert not validate_minor(damaged)
            negatives.append(kind + '_' + name)
        groups = [list(g) for g in base['branch_sets']]
        groups[0].append('b0')
        assert not validate_minor(dict(base, branch_sets=groups))
        negatives.append(kind + '_overlapping_hub')
    return records, negatives


def run():
    cover_rows = covers()
    palettes, incidence = four_palettes()
    relations = relation_controls()
    minors, negatives = minor_controls()
    # This is a control of the paper's forest identity, not graph enumeration.
    forest_counts = [dict(components=h, K4_blocks=k, contacts=2*h+2*k)
                     for h in range(1, 6) for k in range(h, 10)]
    assert all(r['contacts'] != 5 for r in forest_counts)
    inputs = ['scripts/c5_single_spoke_four.py',
              'artifacts/c5_single_spoke_four/observations.json',
              'scripts/c5_single_spoke_three_one.py',
              'artifacts/c5_single_spoke_three_one/observations.json']
    return dict(scope='necessary covers and finite controls for paper no-spoke exclusions; no disk realization or Lean theorem',
                inputs_sha256={p: sha256((ROOT / p).read_bytes()).hexdigest() for p in inputs},
                covers=cover_rows, four_row_palettes=palettes, local_incidence=incidence,
                even_leaf_controls=forest_counts, full_relations=relations,
                minors=minors, negative_controls=negatives,
                summary=dict(cover_counts={str(p): sum(tuple(r['partition']) == p for r in cover_rows)
                                           for p in PARTITIONS},
                             open_cover_rows=sum(r['status'] == 'open' for r in cover_rows),
                             palette_quadruples_tested=2*4**4+6**4,
                             compatible_palette_quadruples=len(palettes), local_incidence_states=len(incidence),
                             full_relations=len(relations), even_leaf_controls=len(forest_counts),
                             K5_counts={k: sum(r['kind'] == k for r in minors)
                                        for k in ('K4', 'three_contact', 'four_contact')},
                             reflected_minors=len(minors), negative_minor_controls=len(negatives)))


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
